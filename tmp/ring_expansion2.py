import sys, json, urllib.request
sys.path.insert(0, r'C:\Users\clemensv\OneDrive - Microsoft\Agents\nius\nius_bot_dossier')
from kusto_client import get_client

client = get_client()
db = "bluesky"

# Top new DIDs not in the known ring
new_dids = [
    "did:plc:3c7r453vexmpwu6nheazyikk",
    "did:plc:u4e3ytzjxb7vapbdmr4oz7ld",
    "did:plc:5v7itrhmq6zhvpqn2sfmcwaw",
    "did:plc:l3fkqug2hhn4upcdewogsijh",
    "did:plc:vb6p4kuz3kmtqrcix2ghjkwf",
    "did:plc:oqc7737mwl6y22wjqdduujex",
    "did:plc:qbw4i5hcyc6dtuckixaogxlc",
    "did:plc:dvhyaxbrf7uh6eemujbd4jao",
    "did:plc:qq2eg3kbh44gytxlghozodeb",
    "did:plc:5sjri67leyvnlenx7tzgfulk",
    "did:plc:33wcrgvuwuxvzpa74yud37qp",
    "did:plc:6nrykjezbxfxeubizsoipwbo",
    "did:plc:qyuua6edp64sxlwcb6myitst",
    "did:plc:ajvwz5alprhutyx3zuwrg7dc",
    "did:plc:jyqk4xrplfhsl6dfeibuw37c",
]

# Resolve profiles via Bluesky API
def resolve_profiles(dids):
    profiles = {}
    for i in range(0, len(dids), 25):
        batch = dids[i:i+25]
        params = "&".join(f"actors={d}" for d in batch)
        url = f"https://public.api.bsky.app/xrpc/app.bsky.actor.getProfiles?{params}"
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            for p in data.get("profiles", []):
                profiles[p["did"]] = p
    return profiles

profiles = resolve_profiles(new_dids)

print("=== Resolved profiles of top overlap accounts ===\n")
print(f"{'Handle':<35} {'Display':<25} {'Followers':>9} {'Following':>9} {'Posts':>7} {'Labels'}")
print("-" * 120)
for did in new_dids:
    p = profiles.get(did, {})
    handle = p.get("handle", "???")
    display = p.get("displayName", "")[:24]
    followers = p.get("followersCount", "?")
    following = p.get("followsCount", "?")
    posts = p.get("postsCount", "?")
    labels = ", ".join(l.get("val", "") for l in p.get("labels", []))
    print(f"{handle:<35} {display:<25} {followers:>9} {following:>9} {posts:>7} {labels}")

# Check timing characteristics of top blockers
print("\n\n=== Block timing for top new accounts ===")
top_new = new_dids[:5]
did_list = '", "'.join(top_new)
q_timing = f"""
['Bluesky.Graph.Block_v1']
| where did in ("{did_list}")
| order by did, indexed_at asc
| serialize
| extend prev_time = prev(indexed_at), prev_did = prev(did)
| where did == prev_did
| extend gap_ms = datetime_diff('millisecond', indexed_at, prev_time)
| where gap_ms > 0 and gap_ms < 600000
| summarize
    median_gap = percentile(gap_ms, 50),
    p95_gap = percentile(gap_ms, 95),
    min_gap = min(gap_ms),
    total_blocks = count() + 1
  by did
| order by total_blocks desc
"""
result = client.execute(db, q_timing)
rows = list(result.primary_results[0])
print(f"\n{'DID':<45} {'Blocks':>8} {'Median ms':>10} {'P95 ms':>10} {'Min ms':>8}")
print("-" * 85)
for r in rows:
    handle = profiles.get(r['did'], {}).get("handle", r['did'][:30])
    print(f"{handle:<45} {r['total_blocks']:>8} {r['median_gap']:>10.0f} {r['p95_gap']:>10.0f} {r['min_gap']:>8}")

# Check follow relationships between new accounts and known ring
print("\n\n=== Follow connections: new accounts → known ring ===")
all_new = '", "'.join(new_dids)
ring_str = '", "'.join([
    "did:plc:kd4wtd75a637g2gvg2dh2b3t",
    "did:plc:gjcwwrezaz5qdcjn3347qvtl",
    "did:plc:qildfzoh5p24jgion4xiycvz",
    "did:plc:xcytuwwb3b33ipiqzmqzbs45",
    "did:plc:hwpiekun4iebo4oqevjfe6ss",
    "did:plc:tfspkb2htmw7vwdgqj7mzx7m",
])
q_follows = f"""
['Bluesky.Graph.Follow_v1']
| where (did in ("{all_new}") and subject in ("{ring_str}"))
   or (did in ("{ring_str}") and subject in ("{all_new}"))
| project did, subject
"""
result2 = client.execute(db, q_follows)
rows2 = list(result2.primary_results[0])
if rows2:
    print(f"\nFound {len(rows2)} follow edges:")
    for r in rows2:
        follower = profiles.get(r['did'], {}).get("handle", r['did'][:30])
        followed = profiles.get(r['subject'], {}).get("handle", r['subject'][:30])
        print(f"  {follower} → {followed}")
else:
    print("\nNo follow connections between new accounts and known ring members.")

# Check follows among the new accounts themselves
print("\n\n=== Follow connections among new accounts themselves ===")
q_follows2 = f"""
['Bluesky.Graph.Follow_v1']
| where did in ("{all_new}") and subject in ("{all_new}")
| project did, subject
"""
result3 = client.execute(db, q_follows2)
rows3 = list(result3.primary_results[0])
if rows3:
    print(f"\nFound {len(rows3)} follow edges among new accounts:")
    for r in rows3:
        follower = profiles.get(r['did'], {}).get("handle", r['did'][:30])
        followed = profiles.get(r['subject'], {}).get("handle", r['subject'][:30])
        print(f"  {follower} → {followed}")
else:
    print("\nNo follow connections among new accounts either.")
