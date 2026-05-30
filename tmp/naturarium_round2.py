"""
Round 2: Deep cluster analysis using verified DIDs.
Key discovery: the bots follow all targets in a single burst, not drip!
"""
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter

import httpx
import pandas as pd

sys.path.insert(0, r"C:\Users\clemensv\OneDrive - Microsoft\Agents\nius")
from nius_bot_dossier.kusto_client import execute_query

BSKY_API = "https://public.api.bsky.app/xrpc"
OUT_DIR = Path(r"d:\bskyhygiene\investigations\2026-05-30-german-literary-bots")

# Known target DIDs from miahungrigesherz's follow list
TARGET_DIDS = [
    "did:plc:kiopixvqglbzrhwghloh3uco",  # schreibersnaturarium.de
    "did:plc:oaxo5prfxkq4zq2yjkymdm26",  # ?
    "did:plc:6ak4q2mrzm7tg6ni2cn4lle6",  # ?
    "did:plc:c5xeh5ozplpba5jxbtbq2egq",  # ?
    "did:plc:cphgfu544qoxz4mzia2iqmyz",  # ?
    "did:plc:5u46hge3spaaqp4736zrajq3",  # ?
    "did:plc:jpadgbliidzui5mdtggo6vww",  # ?
    "did:plc:igwuf5murxubnimwnbvfvnvu",  # ?
    "did:plc:jhxbuuzxsjnvjzblgpn263mn",  # ?
    "did:plc:thn65yzogscrhqmqdf3zp66j",  # ?
    "did:plc:z72i7hdynmk6r22z27h6tvur",  # bsky.app (the default follow)
]

# ─── Step 1: Identify the full cluster ───────────────────────────────────────

print("=" * 60)
print("STEP 1: Identify full cluster via co-follow of 2 key targets")
print("=" * 60)

q_cluster = """
let schreiber = "did:plc:kiopixvqglbzrhwghloh3uco";
let target2 = "did:plc:oaxo5prfxkq4zq2yjkymdm26";
let f_schreiber = ['Bluesky.Graph.Follow_v1'] | where subject == schreiber | distinct did;
let f_target2 = ['Bluesky.Graph.Follow_v1'] | where subject == target2 | distinct did;
let both = f_schreiber | join kind=inner f_target2 on did | project did;
['Bluesky.Graph.Follow_v1']
| where did in (both)
| summarize 
    follow_count = dcount(subject),
    first_follow = min(___time),
    last_follow = max(___time)
  by did
| where follow_count <= 20
| project did, follow_count, first_follow, last_follow
| order by first_follow asc
"""

df_cluster = execute_query(q_cluster)
print(f"Cluster size: {len(df_cluster)} accounts")
print(f"Follow counts: {df_cluster['follow_count'].value_counts().sort_index().to_dict()}")
print(f"First activity: {df_cluster['first_follow'].min()}")
print(f"Last activity: {df_cluster['last_follow'].max()}")

# ─── Step 2: Resolve all target DIDs via API ─────────────────────────────────

print("\n" + "=" * 60)
print("STEP 2: Resolve target account identities via API")
print("=" * 60)

client = httpx.Client(timeout=30)

params = [("actors", d) for d in TARGET_DIDS]
resp = client.get(f"{BSKY_API}/app.bsky.actor.getProfiles", params=params)
resp.raise_for_status()
target_profiles = resp.json().get("profiles", [])
print(f"\nResolved {len(target_profiles)} target accounts:")
for p in target_profiles:
    print(f"  {p['handle']:40s} | {p.get('followersCount', 0):>8,} followers | {p.get('displayName', '')}")

# ─── Step 3: Full co-follow analysis from Kusto ─────────────────────────────

print("\n" + "=" * 60)
print("STEP 3: Complete co-follow matrix from Kusto")
print("=" * 60)

cluster_dids = df_cluster["did"].tolist()
dids_kql = ", ".join([f'"{d}"' for d in cluster_dids])

q_cofollow = f"""
let cluster_dids = dynamic([{dids_kql}]);
['Bluesky.Graph.Follow_v1']
| where did in (cluster_dids)
| summarize bot_count = dcount(did) by subject
| order by bot_count desc
| take 30
"""

df_cofollow = execute_query(q_cofollow)
print(f"\nAll co-followed accounts (top 30):")

# Resolve these via API
all_subjects = df_cofollow["subject"].tolist()
subject_profiles = {}
for i in range(0, len(all_subjects), 25):
    batch = all_subjects[i:i+25]
    params = [("actors", d) for d in batch]
    try:
        r = client.get(f"{BSKY_API}/app.bsky.actor.getProfiles", params=params)
        r.raise_for_status()
        for p in r.json().get("profiles", []):
            subject_profiles[p["did"]] = p
    except Exception as e:
        print(f"  Error resolving batch: {e}")
    time.sleep(0.5)

print(f"\n{'Handle':45s} | {'Bots':>4s} | {'Followers':>10s} | {'Posts':>5s} | Display Name")
print("-" * 120)
for _, row in df_cofollow.iterrows():
    p = subject_profiles.get(row["subject"], {})
    handle = p.get("handle", row["subject"][:30])
    followers = p.get("followersCount", "?")
    posts = p.get("postsCount", "?")
    display = p.get("displayName", "")[:30]
    print(f"  {handle:43s} | {row['bot_count']:>4d} | {followers:>10} | {posts:>5} | {display}")

# ─── Step 4: Resolve bot profiles and check status ───────────────────────────

print("\n" + "=" * 60)
print("STEP 4: Resolve bot profiles via API (check deletions)")
print("=" * 60)

bot_profiles = []
for i in range(0, len(cluster_dids), 25):
    batch = cluster_dids[i:i+25]
    params = [("actors", d) for d in batch]
    try:
        r = client.get(f"{BSKY_API}/app.bsky.actor.getProfiles", params=params)
        r.raise_for_status()
        for p in r.json().get("profiles", []):
            bot_profiles.append(p)
    except httpx.HTTPStatusError as e:
        for d in batch:
            try:
                r2 = client.get(f"{BSKY_API}/app.bsky.actor.getProfile", params={"actor": d})
                r2.raise_for_status()
                bot_profiles.append(r2.json())
            except Exception:
                bot_profiles.append({"did": d, "handle": "DELETED", "deactivated": True})
            time.sleep(0.2)
    time.sleep(0.5)

print(f"Resolved {len(bot_profiles)} bot profiles")

active = [p for p in bot_profiles if p.get("handle") != "DELETED" and "handle.invalid" not in p.get("handle", "")]
deleted = [p for p in bot_profiles if p.get("handle") == "DELETED"]
invalid = [p for p in bot_profiles if "handle.invalid" in p.get("handle", "")]
has_avatar = [p for p in active if p.get("avatar")]
has_posts = [p for p in active if p.get("postsCount", 0) > 0]
has_description = [p for p in active if p.get("description")]
has_display = [p for p in active if p.get("displayName")]

print(f"\n  Active: {len(active)}")
print(f"  Deleted/Deactivated: {len(deleted)}")
print(f"  Handle.invalid: {len(invalid)}")
print(f"  With avatar: {len(has_avatar)}")
print(f"  With display name: {len(has_display)}")
print(f"  With description: {len(has_description)}")
print(f"  With posts: {len(has_posts)}")

if has_avatar:
    print(f"\n  Bots WITH avatar:")
    for p in has_avatar:
        print(f"    {p['handle']} — '{p.get('displayName', '')}' — '{p.get('description', '')[:60]}'")

if has_posts:
    print(f"\n  Bots WITH posts (unusual!):")
    for p in has_posts:
        print(f"    {p['handle']} — {p['postsCount']} posts")

if has_description:
    print(f"\n  Bot descriptions:")
    for p in has_description:
        print(f"    {p['handle']}: '{p.get('description', '')[:80]}'")

# ─── Step 5: Follow timing analysis — burst vs drip ─────────────────────────

print("\n" + "=" * 60)
print("STEP 5: Follow timing — burst detection")
print("=" * 60)

q_timing = f"""
let cluster_dids = dynamic([{dids_kql}]);
['Bluesky.Graph.Follow_v1']
| where did in (cluster_dids)
| summarize
    follow_count = count(),
    first_ts = min(___time),
    last_ts = max(___time),
    duration_sec = datetime_diff('second', max(___time), min(___time))
  by did
| extend duration_min = duration_sec / 60.0
| order by first_ts asc
"""

df_timing = execute_query(q_timing)
print(f"\nFollow session durations:")
print(f"  Total bots: {len(df_timing)}")
print(f"  Completed in < 1 second: {len(df_timing[df_timing['duration_sec'] <= 1])}")
print(f"  Completed in < 60 seconds: {len(df_timing[df_timing['duration_sec'] <= 60])}")
print(f"  Completed in < 5 minutes: {len(df_timing[df_timing['duration_min'] <= 5])}")
print(f"  Completed in < 1 hour: {len(df_timing[df_timing['duration_min'] <= 60])}")
print(f"  Took > 1 hour: {len(df_timing[df_timing['duration_min'] > 60])}")
print(f"\n  Mean duration: {df_timing['duration_sec'].mean():.1f} seconds")
print(f"  Median duration: {df_timing['duration_sec'].median():.1f} seconds")
print(f"  Max duration: {df_timing['duration_sec'].max():.1f} seconds ({df_timing['duration_sec'].max()/3600:.1f} hours)")

print(f"\n  Sample timing (first 10 bots):")
for _, row in df_timing.head(10).iterrows():
    h = next((p["handle"] for p in bot_profiles if p.get("did") == row["did"]), row["did"][:30])
    print(f"    {h:40s} | {row['follow_count']:>2} follows | {row['duration_sec']:>6.0f}s ({row['duration_min']:.1f}min)")

# ─── Step 6: Check for new bots in last 48h ─────────────────────────────────

print("\n" + "=" * 60)
print("STEP 6: New bots in last 48 hours")
print("=" * 60)

q_recent = """
let schreiber = "did:plc:kiopixvqglbzrhwghloh3uco";
let target2 = "did:plc:oaxo5prfxkq4zq2yjkymdm26";
let recent_schreiber = ['Bluesky.Graph.Follow_v1']
    | where subject == schreiber and ___time > ago(48h)
    | distinct did;
let recent_both = recent_schreiber
    | join kind=inner (['Bluesky.Graph.Follow_v1'] | where subject == target2 | distinct did) on did
    | project did;
['Bluesky.Graph.Follow_v1']
| where did in (recent_both)
| summarize follow_count = dcount(subject), first_ts = min(___time), last_ts = max(___time) by did
| where follow_count <= 20
| order by first_ts desc
"""

df_recent = execute_query(q_recent)
known_dids = set(cluster_dids)
new_bots = df_recent[~df_recent["did"].isin(known_dids)]
print(f"Bots active in last 48h: {len(df_recent)}")
print(f"NEW bots (not in existing cluster): {len(new_bots)}")

if len(new_bots) > 0:
    new_dids = new_bots["did"].tolist()
    params = [("actors", d) for d in new_dids[:25]]
    try:
        r = client.get(f"{BSKY_API}/app.bsky.actor.getProfiles", params=params)
        r.raise_for_status()
        for p in r.json().get("profiles", []):
            print(f"  NEW: {p['handle']:40s} | {p.get('followsCount', 0)} follows | "
                  f"{p.get('postsCount', 0)} posts | created {p.get('createdAt', '?')[:10]}")
    except Exception as e:
        print(f"  Error resolving new bots: {e}")
        for _, row in new_bots.iterrows():
            print(f"  NEW: {row['did']} | {row['follow_count']} follows | first: {row['first_ts']}")

# ─── Step 7: Investigate spam/customer accounts ──────────────────────────────

print("\n" + "=" * 60)
print("STEP 7: Investigate spam/customer accounts")
print("=" * 60)

# Find accounts followed by cluster bots that have low bot_count (potential customers)
q_customers = f"""
let cluster_dids = dynamic([{dids_kql}]);
['Bluesky.Graph.Follow_v1']
| where did in (cluster_dids)
| summarize bot_count = dcount(did) by subject
| where bot_count >= 3 and bot_count < 30
| order by bot_count desc
"""

df_customers = execute_query(q_customers)
print(f"Accounts followed by 3-29 bots: {len(df_customers)}")

if len(df_customers) > 0:
    cust_dids = df_customers["subject"].tolist()
    cust_profiles = []
    for i in range(0, len(cust_dids), 25):
        batch = cust_dids[i:i+25]
        params = [("actors", d) for d in batch]
        try:
            r = client.get(f"{BSKY_API}/app.bsky.actor.getProfiles", params=params)
            r.raise_for_status()
            for p in r.json().get("profiles", []):
                cust_profiles.append(p)
        except Exception:
            pass
        time.sleep(0.5)
    
    print(f"\n  Low-follower accounts followed by cluster (likely customers/spam):")
    print(f"  {'Handle':40s} | {'Bots':>4s} | {'Flrs':>5s} | {'Posts':>5s} | Description")
    print("  " + "-" * 110)
    for p in sorted(cust_profiles, key=lambda x: x.get("followersCount", 0)):
        if p.get("followersCount", 0) < 100:
            did = p["did"]
            bc = df_customers[df_customers["subject"] == did]["bot_count"].iloc[0] if did in df_customers["subject"].values else "?"
            desc = p.get("description", "")[:50].replace("\n", " ")
            print(f"  {p['handle']:40s} | {bc:>4} | {p.get('followersCount', 0):>5} | {p.get('postsCount', 0):>5} | {desc}")

# ─── Step 8: Sample bot follow-lists ─────────────────────────────────────────

print("\n" + "=" * 60)
print("STEP 8: Sample bot follow-lists via API")
print("=" * 60)

sample_bots = [p for p in active[:5]]
for p in sample_bots:
    try:
        resp = client.get(f"{BSKY_API}/app.bsky.graph.getFollows",
                          params={"actor": p["did"], "limit": 50})
        resp.raise_for_status()
        data = resp.json()
        follows = [f.get("handle", f.get("did")) for f in data.get("follows", [])]
        print(f"\n  {p['handle']} ({len(follows)} follows):")
        for f in sorted(follows):
            print(f"    -> {f}")
    except Exception as e:
        print(f"  {p['handle']}: Error — {e}")
    time.sleep(0.5)

# ─── Step 9: Handle patterns ────────────────────────────────────────────────

print("\n" + "=" * 60)
print("STEP 9: Handle pattern analysis")
print("=" * 60)

handles = [p.get("handle", "") for p in active]
handles_clean = [h.replace(".bsky.social", "") for h in handles if ".bsky.social" in h]

patterns = Counter()
for h in handles_clean:
    if any(c.isdigit() for c in h):
        patterns["contains_digits"] += 1
    if len(h) > 15:
        patterns["long_handle"] += 1
    if h.islower():
        patterns["all_lowercase"] += 1
    if any(w in h.lower() for w in ["herz", "frau", "blume", "wald", "licht", "stern", "traum", "fee", "kind", "meer", "regen", "wolke"]):
        patterns["german_words"] += 1
    if any(w in h.lower() for w in ["girl", "goth", "furry", "vampire", "riley", "red"]):
        patterns["english_spam"] += 1

print(f"  Total handles: {len(handles_clean)}")
for pat, count in patterns.most_common():
    print(f"    {pat}: {count}")

print(f"\n  All handles (sorted):")
for h in sorted(handles_clean):
    print(f"    {h}")

# ─── Step 10: Export ─────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("STEP 10: Export data")
print("=" * 60)

export = {
    "cluster": "german-literary-bots",
    "date": "2026-05-30",
    "total_bots": len(cluster_dids),
    "active": len(active),
    "deleted_suspended": len(deleted) + len(invalid),
    "new_bots_48h": len(new_bots) if len(new_bots) > 0 else 0,
    "dids": cluster_dids,
    "targets": [{"did": p["did"], "handle": p["handle"], "followersCount": p.get("followersCount", 0)}
                for p in target_profiles],
    "bot_handles": [p.get("handle") for p in active],
}
export_path = OUT_DIR / "bot_dids.json"
with open(export_path, "w") as f:
    json.dump(export, f, indent=2)
print(f"Exported to {export_path}")

timing_export = df_timing[["did", "follow_count", "duration_sec", "first_ts", "last_ts"]].copy()
timing_export["first_ts"] = timing_export["first_ts"].astype(str)
timing_export["last_ts"] = timing_export["last_ts"].astype(str)
timing_path = OUT_DIR / "assets" / "timing_data.json"
timing_export.to_json(timing_path, orient="records", indent=2)
print(f"Timing data exported to {timing_path}")

client.close()

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)
