import sys
sys.path.insert(0, r'C:\Users\clemensv\OneDrive - Microsoft\Agents\nius\nius_bot_dossier')
from kusto_client import get_client

client = get_client()
db = "bluesky"

# Known ring members
ring_dids = [
    "did:plc:kd4wtd75a637g2gvg2dh2b3t",  # louisbetonberlin
    "did:plc:gjcwwrezaz5qdcjn3347qvtl",  # smatsto
    "did:plc:qildfzoh5p24jgion4xiycvz",  # fuenfuhrteefix
    "did:plc:xcytuwwb3b33ipiqzmqzbs45",  # holbidope
    "did:plc:hwpiekun4iebo4oqevjfe6ss",  # kaffchris
    "did:plc:tfspkb2htmw7vwdgqj7mzx7m",  # kunststein
]

# Query 1: Find accounts that share a high overlap with the ring's blocklist
# Take smatsto's blocks (largest set) and find who else blocks the same accounts
print("=== Finding accounts with high overlap to smatsto's blocklist ===")
q1 = """
let smatsto_blocks = ['Bluesky.Graph.Block_v1']
    | where did == "did:plc:gjcwwrezaz5qdcjn3347qvtl"
    | distinct subject;
let ring_dids = dynamic([
    "did:plc:kd4wtd75a637g2gvg2dh2b3t",
    "did:plc:gjcwwrezaz5qdcjn3347qvtl",
    "did:plc:qildfzoh5p24jgion4xiycvz",
    "did:plc:xcytuwwb3b33ipiqzmqzbs45",
    "did:plc:hwpiekun4iebo4oqevjfe6ss",
    "did:plc:tfspkb2htmw7vwdgqj7mzx7m"
]);
['Bluesky.Graph.Block_v1']
| where did !in (ring_dids)
| where subject in (smatsto_blocks)
| summarize shared_blocks = dcount(subject), total_blocks = count() by did
| where shared_blocks > 1000
| order by shared_blocks desc
| take 30
"""
result = client.execute(db, q1)
rows = list(result.primary_results[0])
print(f"\nAccounts with >1000 shared blocks with smatsto (outside known ring):")
print(f"{'DID':<45} {'Shared':>8} {'Total':>8}")
print("-" * 65)
for r in rows:
    print(f"{r['did']:<45} {r['shared_blocks']:>8} {r['total_blocks']:>8}")

# Query 2: Check mutual follows among ring members
print("\n\n=== Follow relationships among ring members ===")
q2 = """
let ring_dids = dynamic([
    "did:plc:kd4wtd75a637g2gvg2dh2b3t",
    "did:plc:gjcwwrezaz5qdcjn3347qvtl",
    "did:plc:qildfzoh5p24jgion4xiycvz",
    "did:plc:xcytuwwb3b33ipiqzmqzbs45",
    "did:plc:hwpiekun4iebo4oqevjfe6ss",
    "did:plc:tfspkb2htmw7vwdgqj7mzx7m"
]);
['Bluesky.Graph.Follow_v1']
| where did in (ring_dids) and subject in (ring_dids)
| project did, subject
"""
result2 = client.execute(db, q2)
rows2 = list(result2.primary_results[0])

# Map DIDs to handles
handle_map = {
    "did:plc:kd4wtd75a637g2gvg2dh2b3t": "louisbetonberlin",
    "did:plc:gjcwwrezaz5qdcjn3347qvtl": "smatsto",
    "did:plc:qildfzoh5p24jgion4xiycvz": "fuenfuhrteefix",
    "did:plc:xcytuwwb3b33ipiqzmqzbs45": "holbidope",
    "did:plc:hwpiekun4iebo4oqevjfe6ss": "kaffchris",
    "did:plc:tfspkb2htmw7vwdgqj7mzx7m": "kunststein",
}

print(f"\nFollow edges among ring members ({len(rows2)} total):")
print(f"{'Follower':<20} → {'Follows':<20}")
print("-" * 45)
for r in rows2:
    follower = handle_map.get(r['did'], r['did'][:20])
    followed = handle_map.get(r['subject'], r['subject'][:20])
    print(f"{follower:<20} → {followed:<20}")

# Count followers/following per member within ring
print("\n\nIn-ring follow summary:")
for did, handle in handle_map.items():
    following_in_ring = sum(1 for r in rows2 if r['did'] == did)
    followers_in_ring = sum(1 for r in rows2 if r['subject'] == did)
    print(f"  {handle:<20}: follows {following_in_ring} ring members, followed by {followers_in_ring}")
