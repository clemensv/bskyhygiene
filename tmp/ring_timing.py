import sys
sys.path.insert(0, r'C:\Users\clemensv\OneDrive - Microsoft\Agents\nius\nius_bot_dossier')
from kusto_client import get_client

client = get_client()
db = "bluesky"

new_dids = [
    "did:plc:3c7r453vexmpwu6nheazyikk",  # dqita
    "did:plc:u4e3ytzjxb7vapbdmr4oz7ld",  # adametokirkfor
    "did:plc:5v7itrhmq6zhvpqn2sfmcwaw",  # maribel1917
    "did:plc:l3fkqug2hhn4upcdewogsijh",  # castironirish
    "did:plc:vb6p4kuz3kmtqrcix2ghjkwf",  # vappytoy
    "did:plc:oqc7737mwl6y22wjqdduujex",  # fkftsh
    "did:plc:qbw4i5hcyc6dtuckixaogxlc",  # solire
    "did:plc:dvhyaxbrf7uh6eemujbd4jao",  # sasunarusasu
    "did:plc:qq2eg3kbh44gytxlghozodeb",  # fakeflamesprite
    "did:plc:5sjri67leyvnlenx7tzgfulk",  # verezi
]

handle_map = {
    "did:plc:3c7r453vexmpwu6nheazyikk": "dqita",
    "did:plc:u4e3ytzjxb7vapbdmr4oz7ld": "adametokirkfor",
    "did:plc:5v7itrhmq6zhvpqn2sfmcwaw": "maribel1917",
    "did:plc:l3fkqug2hhn4upcdewogsijh": "castironirish",
    "did:plc:vb6p4kuz3kmtqrcix2ghjkwf": "vappytoy",
    "did:plc:oqc7737mwl6y22wjqdduujex": "fkftsh",
    "did:plc:qbw4i5hcyc6dtuckixaogxlc": "solire",
    "did:plc:dvhyaxbrf7uh6eemujbd4jao": "sasunarusasu",
    "did:plc:qq2eg3kbh44gytxlghozodeb": "fakeflamesprite",
    "did:plc:5sjri67leyvnlenx7tzgfulk": "verezi",
}

print("=== Block timing for extended ring accounts ===\n")
print(f"{'Handle':<20} {'Blocks':>8} {'Median ms':>10} {'P95 ms':>10} {'Min ms':>8} {'First block':<12} {'Last block':<12}")
print("-" * 90)

for did in new_dids:
    q = f"""
    ['Bluesky.Graph.Block_v1']
    | where did == "{did}"
    | extend ts = todatetime(indexed_at)
    | order by ts asc
    | extend prev_t = prev(ts)
    | where isnotnull(prev_t)
    | extend gap_ms = (ts - prev_t) / 1ms
    | where gap_ms > 0 and gap_ms < 600000
    | summarize
        median_gap = percentile(gap_ms, 50),
        p95_gap = percentile(gap_ms, 95),
        min_gap = min(gap_ms),
        total_blocks = count() + 1,
        first_block = min(prev_t),
        last_block = max(ts)
    """
    try:
        result = client.execute(db, q)
        rows = list(result.primary_results[0])
        if rows:
            r = rows[0]
            fb = str(r['first_block'])[:10]
            lb = str(r['last_block'])[:10]
            print(f"{handle_map.get(did, '?'):<20} {r['total_blocks']:>8} {r['median_gap']:>10.0f} {r['p95_gap']:>10.0f} {r['min_gap']:>8.0f} {fb:<12} {lb:<12}")
    except Exception as e:
        print(f"{handle_map.get(did, '?'):<20} ERROR: {str(e)[:60]}")

# Check overlap between top 4 new accounts and louis
print("\n\n=== Overlap with louisbetonberlin's block targets ===")
q_overlap = """
let louis_blocks = ['Bluesky.Graph.Block_v1']
    | where did == "did:plc:kd4wtd75a637g2gvg2dh2b3t"
    | distinct subject;
let check_dids = dynamic([
    "did:plc:3c7r453vexmpwu6nheazyikk",
    "did:plc:u4e3ytzjxb7vapbdmr4oz7ld",
    "did:plc:5v7itrhmq6zhvpqn2sfmcwaw",
    "did:plc:l3fkqug2hhn4upcdewogsijh",
    "did:plc:vb6p4kuz3kmtqrcix2ghjkwf",
    "did:plc:oqc7737mwl6y22wjqdduujex",
    "did:plc:qbw4i5hcyc6dtuckixaogxlc",
    "did:plc:dvhyaxbrf7uh6eemujbd4jao"
]);
['Bluesky.Graph.Block_v1']
| where did in (check_dids)
| where subject in (louis_blocks)
| summarize shared_with_louis = dcount(subject), total = count() by did
| order by shared_with_louis desc
"""
result = client.execute(db, q_overlap)
rows = list(result.primary_results[0])
print(f"\n{'Handle':<20} {'Shared w/ Louis':>15} {'Total':>8} {'Overlap %':>10}")
print("-" * 60)
for r in rows:
    h = handle_map.get(r['did'], r['did'][:20])
    pct = r['shared_with_louis'] / r['total'] * 100 if r['total'] > 0 else 0
    print(f"{h:<20} {r['shared_with_louis']:>15} {r['total']:>8} {pct:>9.1f}%")
