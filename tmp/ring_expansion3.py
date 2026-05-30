import sys, json, urllib.request
sys.path.insert(0, r'C:\Users\clemensv\OneDrive - Microsoft\Agents\nius\nius_bot_dossier')
from kusto_client import get_client

client = get_client()
db = "bluesky"

# Top new DIDs
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

ring_dids = [
    "did:plc:kd4wtd75a637g2gvg2dh2b3t",
    "did:plc:gjcwwrezaz5qdcjn3347qvtl",
    "did:plc:qildfzoh5p24jgion4xiycvz",
    "did:plc:xcytuwwb3b33ipiqzmqzbs45",
    "did:plc:hwpiekun4iebo4oqevjfe6ss",
    "did:plc:tfspkb2htmw7vwdgqj7mzx7m",
]

# Check timing per account for top 5
print("=== Block timing for top new accounts ===\n")
for did in new_dids[:5]:
    q = f"""
    ['Bluesky.Graph.Block_v1']
    | where did == "{did}"
    | order by indexed_at asc
    | extend prev_t = prev(indexed_at)
    | where isnotnull(prev_t)
    | extend gap_ms = (indexed_at - prev_t) / 1ms
    | where gap_ms > 0 and gap_ms < 600000
    | summarize
        median_gap = percentile(gap_ms, 50),
        p95_gap = percentile(gap_ms, 95),
        min_gap = min(gap_ms),
        total_blocks = count() + 1
    """
    try:
        result = client.execute(db, q)
        rows = list(result.primary_results[0])
        if rows:
            r = rows[0]
            print(f"  {did[:40]}  blocks={r['total_blocks']:>8}  median={r['median_gap']:>6.0f}ms  p95={r['p95_gap']:>6.0f}ms  min={r['min_gap']:>4.0f}ms")
    except Exception as e:
        print(f"  {did[:40]}  ERROR: {e}")

# Follow connections between new accounts and known ring
print("\n\n=== Follow connections: new accounts ↔ known ring ===")
all_new_str = '", "'.join(new_dids)
ring_str = '", "'.join(ring_dids)

q_follows = f"""
['Bluesky.Graph.Follow_v1']
| where (did in ("{all_new_str}") and subject in ("{ring_str}"))
   or (did in ("{ring_str}") and subject in ("{all_new_str}"))
| project did, subject
"""
result2 = client.execute(db, q_follows)
rows2 = list(result2.primary_results[0])
print(f"\nFound {len(rows2)} follow edges between new accounts and ring:")
for r in rows2:
    print(f"  {r['did'][:40]} → {r['subject'][:40]}")

# Follow connections among new accounts themselves
print("\n\n=== Follow connections among new accounts themselves ===")
q_follows2 = f"""
['Bluesky.Graph.Follow_v1']
| where did in ("{all_new_str}") and subject in ("{all_new_str}")
| project did, subject
"""
result3 = client.execute(db, q_follows2)
rows3 = list(result3.primary_results[0])
print(f"\nFound {len(rows3)} follow edges among new accounts")
for r in rows3:
    print(f"  {r['did'][:40]} → {r['subject'][:40]}")

# Also check: do any of the expanded set follow the ring?
print("\n\n=== Follow connections: ALL accounts (ring+new) ↔ each other ===")
all_dids = ring_dids + new_dids
all_str = '", "'.join(all_dids)
q_all = f"""
['Bluesky.Graph.Follow_v1']
| where did in ("{all_str}") and subject in ("{all_str}")
| project did, subject
"""
result4 = client.execute(db, q_all)
rows4 = list(result4.primary_results[0])
print(f"\nFound {len(rows4)} total follow edges across all 21 accounts")
for r in rows4:
    print(f"  {r['did'][:40]} → {r['subject'][:40]}")
