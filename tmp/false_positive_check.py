"""
False-positive check: Identify accounts in the cluster that might be real users.

Criteria for potential false positives:
- High post count (organic activity)
- Follows many accounts beyond the cluster targets
- Follow timing spread over days (not burst)
- Profile has meaningful bio, many followers
- Account age predates the campaign significantly
"""
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx

sys.path.insert(0, r"C:\Users\clemensv\OneDrive - Microsoft\Agents\nius")
from nius_bot_dossier.kusto_client import execute_query

BSKY_API = "https://public.api.bsky.app/xrpc"
client = httpx.Client(timeout=30)

# Load cluster DIDs
with open(r"d:\bskyhygiene\investigations\2026-05-30-german-literary-bots\bot_dids.json") as f:
    cluster_data = json.load(f)

cluster_dids = cluster_data["dids"]
target_dids = [t["did"] for t in cluster_data["targets"]]

print("=" * 70)
print("FALSE-POSITIVE ANALYSIS")
print("=" * 70)
print(f"Cluster size: {len(cluster_dids)} accounts")
print(f"Target accounts: {len(target_dids)}")

# Step 1: Resolve all cluster profiles via API
print("\n--- Resolving all profiles via API ---")
profiles = {}
for i in range(0, len(cluster_dids), 25):
    batch = cluster_dids[i:i+25]
    params = [("actors", d) for d in batch]
    try:
        r = client.get(f"{BSKY_API}/app.bsky.actor.getProfiles", params=params)
        r.raise_for_status()
        for p in r.json().get("profiles", []):
            profiles[p["did"]] = p
    except Exception as e:
        print(f"  Error batch {i}: {e}")
    time.sleep(0.3)

print(f"Resolved: {len(profiles)} profiles")

# Step 2: Identify suspects (potential false positives)
suspects = []
for did, p in profiles.items():
    score = 0
    reasons = []
    
    posts = p.get("postsCount", 0)
    followers = p.get("followersCount", 0)
    follows = p.get("followsCount", 0)
    handle = p.get("handle", "?")
    display = p.get("displayName", "")
    desc = p.get("description", "")
    created = p.get("createdAt", "")
    
    # High post count is suspicious of being real
    if posts >= 5:
        score += 3
        reasons.append(f"{posts} posts")
    elif posts >= 2:
        score += 1
        reasons.append(f"{posts} posts")
    
    # Many followers suggests real account
    if followers >= 10:
        score += 3
        reasons.append(f"{followers} followers")
    elif followers >= 3:
        score += 1
        reasons.append(f"{followers} followers")
    
    # Following many accounts beyond cluster targets
    if follows > 20:
        score += 3
        reasons.append(f"{follows} following (>> cluster targets)")
    elif follows > 14:
        score += 1
        reasons.append(f"{follows} following")
    
    # Meaningful description
    if desc and len(desc) > 30 and "IG + TG" not in desc:
        score += 2
        reasons.append("meaningful bio")
    
    # Old account (created before campaign start May 2026)
    if created:
        try:
            created_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
            if created_dt.year < 2026:
                score += 3
                reasons.append(f"created {created[:10]} (pre-2026)")
            elif created_dt.month < 4:
                score += 2
                reasons.append(f"created {created[:10]} (pre-April)")
        except:
            pass
    
    if score >= 3:
        suspects.append({
            "did": did,
            "handle": handle,
            "display": display,
            "posts": posts,
            "followers": followers,
            "follows": follows,
            "desc": desc[:80],
            "created": created[:10] if created else "?",
            "score": score,
            "reasons": reasons
        })

suspects.sort(key=lambda x: x["score"], reverse=True)

print(f"\n{'='*70}")
print(f"POTENTIAL FALSE POSITIVES (score >= 3): {len(suspects)}")
print(f"{'='*70}\n")

for s in suspects:
    print(f"  [{s['score']:>2}] @{s['handle']}")
    print(f"       Posts: {s['posts']} | Followers: {s['followers']} | Following: {s['follows']} | Created: {s['created']}")
    print(f"       Display: '{s['display']}' | Bio: '{s['desc']}'")
    print(f"       Reasons: {', '.join(s['reasons'])}")
    print()

# Step 3: Deep-dive on high-score suspects — check their full follow lists
print(f"\n{'='*70}")
print("DEEP DIVE: Full follow-lists of top suspects")
print(f"{'='*70}")

top_suspects = [s for s in suspects if s["score"] >= 4]

for s in top_suspects:
    print(f"\n  @{s['handle']} (score={s['score']}):")
    try:
        resp = client.get(f"{BSKY_API}/app.bsky.graph.getFollows",
                          params={"actor": s["did"], "limit": 100})
        resp.raise_for_status()
        data = resp.json()
        all_follows = data.get("follows", [])
        
        cluster_follows = [f for f in all_follows if f["did"] in target_dids]
        non_cluster = [f for f in all_follows if f["did"] not in target_dids and f["did"] not in cluster_dids]
        
        print(f"    Total follows: {len(all_follows)}")
        print(f"    Cluster targets followed: {len(cluster_follows)}/{len(target_dids)}")
        print(f"    Non-cluster follows: {len(non_cluster)}")
        
        if non_cluster:
            print(f"    Non-cluster accounts followed:")
            for f in non_cluster[:15]:
                print(f"      -> @{f.get('handle', '?'):40s} ({f.get('displayName', '')[:30]})")
            if len(non_cluster) > 15:
                print(f"      ... and {len(non_cluster)-15} more")
    except Exception as e:
        print(f"    Error: {e}")
    time.sleep(0.5)

# Step 4: Kusto timing check for suspects — did they follow in a burst?
print(f"\n{'='*70}")
print("TIMING ANALYSIS: Did suspects follow in bursts?")
print(f"{'='*70}")

suspect_dids = [s["did"] for s in top_suspects]
if suspect_dids:
    dids_kql = ", ".join([f'"{d}"' for d in suspect_dids])
    q_timing = f"""
    let suspects = dynamic([{dids_kql}]);
    ['Bluesky.Graph.Follow_v1']
    | where did in (suspects)
    | order by did asc, ___time asc
    | project did, subject, ___time
    """
    df_timing = execute_query(q_timing)
    
    for s in top_suspects:
        bot_follows = df_timing[df_timing["did"] == s["did"]].sort_values("___time")
        if len(bot_follows) == 0:
            print(f"\n  @{s['handle']}: No follow data in Kusto")
            continue
            
        first = bot_follows["___time"].iloc[0]
        last = bot_follows["___time"].iloc[-1]
        duration = (last - first).total_seconds()
        n = len(bot_follows)
        
        # Check if follows are clustered in time
        if n > 1:
            gaps = bot_follows["___time"].diff().dt.total_seconds().dropna()
            max_gap = gaps.max()
            median_gap = gaps.median()
        else:
            max_gap = 0
            median_gap = 0
        
        print(f"\n  @{s['handle']}:")
        print(f"    Follows in graph: {n}")
        print(f"    First: {first}")
        print(f"    Last:  {last}")
        print(f"    Total duration: {duration:.0f}s ({duration/3600:.1f}h)")
        print(f"    Median gap between follows: {median_gap:.1f}s")
        print(f"    Max gap: {max_gap:.0f}s ({max_gap/3600:.1f}h)")
        
        if duration > 86400:
            print(f"    ⚠️  SPREAD OVER DAYS — possible real user or multi-wave bot")
        elif duration < 300 and n >= 5:
            print(f"    🤖 BURST ({n} follows in {duration:.0f}s) — bot pattern")
        elif duration < 300:
            print(f"    🤖 Quick burst — bot pattern")
        
        # Show individual follows with timestamps
        target_handles = {t["did"]: t["handle"] for t in cluster_data["targets"]}
        print(f"    Follow sequence:")
        for _, row in bot_follows.iterrows():
            subj = target_handles.get(row["subject"], row["subject"][:30])
            print(f"      {row['___time']} → {subj}")

# Step 5: Check for goth-girl accounts that are IN the cluster (dual role)
print(f"\n{'='*70}")
print("GOTH-GIRL ACCOUNTS IN CLUSTER (spam nodes, not false positives)")
print(f"{'='*70}")
goth_handles = [h for h, p in [(profiles[d].get("handle", ""), profiles[d]) 
                                for d in profiles]
                if any(w in h for w in ["goth", "riley", "sophie", "vanessa", "furry", "scarred"])]
for h in sorted(goth_handles):
    print(f"  @{h} — these are SPAM nodes, NOT false positives")

print(f"\n{'='*70}")
print("VERDICT SUMMARY")
print(f"{'='*70}")
print(f"\nTotal suspects needing review: {len(top_suspects)}")
print(f"(Accounts with score >= 4 that might be real users caught in co-follow filter)")

client.close()
