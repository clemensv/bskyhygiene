"""Deep-dive: accounts that block BEFORE smatsto (upstream candidates)."""
import sys
sys.path.insert(0, r'C:\Users\clemensv\OneDrive - Microsoft\Agents\nius')
from nius_bot_dossier.kusto_client import execute_query
import requests

SMATSTO = 'did:plc:gjcwwrezaz5qdcjn3347qvtl'

# Upstream candidates (block before smatsto)
UPSTREAM = [
    ('did:plc:qyuua6edp64sxlwcb6myitst', '(deleted)'),
    ('did:plc:4fn4mppxm73jldgas7a52kcu', 'chicagosunroof'),
    ('did:plc:ye2r45gcu33r5gkbb2dajb34', 'cayennepompep'),
]

# More accounts from the >5000 overlap list to check directionality
MORE_CANDIDATES = [
    ('did:plc:5v7itrhmq6zhvpqn2sfmcwaw', 'maribel1917 (verify)'),
    ('did:plc:u4e3ytzjxb7vapbdmr4oz7ld', 'adametokirkfor (verify)'),
    ('did:plc:l3fkqug2hhn4upcdewogsijh', 'castironirish (verify)'),
    ('did:plc:vb6p4kuz3kmtqrcix2ghjkwf', 'vappytoy (verify)'),
    ('did:plc:dvhyaxbrf7uh6eemujbd4jao', 'sasunarusasu (verify)'),
    ('did:plc:5sjri67leyvnlenx7tzgfulk', 'verezi (verify)'),
    ('did:plc:qbw4i5hcyc6dtuckixaogxlc', 'solire (verify)'),
]

print("=== DIRECTIONALITY: MORE EXTENDED MEMBERS vs SMATSTO ===\n")
for did, label in MORE_CANDIDATES:
    q_first = f"""
    let a = ['Bluesky.Graph.Block_v1']
    | where did == '{SMATSTO}'
    | project subject, t_smatsto = ___time;
    let b = ['Bluesky.Graph.Block_v1']
    | where did == '{did}'
    | project subject, t_other = ___time;
    a
    | join kind=inner b on subject
    | extend who_first = iff(t_smatsto < t_other, 'smatsto', 'other')
    | summarize 
        smatsto_first = countif(who_first == 'smatsto'),
        other_first = countif(who_first == 'other'),
        total = count(),
        median_lag_hours = percentile(datetime_diff('hour', t_other, t_smatsto), 50)
    """
    df = execute_query(q_first)
    if len(df) > 0:
        r = df.iloc[0]
        pct_s = (r['smatsto_first'] / r['total'] * 100) if r['total'] > 0 else 0
        direction = "→ DOWNSTREAM" if pct_s > 60 else ("← UPSTREAM" if pct_s < 40 else "↔ CONCURRENT")
        print(f"  {label:<28} smatsto first: {pct_s:.0f}% ({r['smatsto_first']:.0f}/{r['total']:.0f})  lag: {r['median_lag_hours']:.0f}h  {direction}")

# Now check: do the upstream accounts follow any common patterns?
print("\n\n=== UPSTREAM ACCOUNTS: CREATION TIMING & FIRST BLOCKS ===\n")
print("When did each start blocking relative to ring start (Apr 28)?")
for did, label in UPSTREAM:
    q_start = f"""
    ['Bluesky.Graph.Block_v1']
    | where did == '{did}'
    | order by ___time asc
    | take 20
    | project ___time, subject
    """
    df_s = execute_query(q_start)
    print(f"\n  {label} — first 5 blocks:")
    for _, r in df_s.head(5).iterrows():
        print(f"    {r['___time']}  → {r['subject']}")

# Check: do upstream accounts overlap with EACH OTHER?
print("\n\n=== UPSTREAM INTER-OVERLAP ===\n")
pairs = [
    (UPSTREAM[0], UPSTREAM[1]),
    (UPSTREAM[0], UPSTREAM[2]),
    (UPSTREAM[1], UPSTREAM[2]),
]
for (did_a, label_a), (did_b, label_b) in pairs:
    q_inter = f"""
    let a = ['Bluesky.Graph.Block_v1']
    | where did == '{did_a}'
    | distinct subject;
    let b = ['Bluesky.Graph.Block_v1']
    | where did == '{did_b}'
    | distinct subject;
    a | join kind=inner b on subject | count
    """
    df_i = execute_query(q_inter)
    if len(df_i) > 0:
        overlap = df_i.iloc[0]['Count']
        print(f"  {label_a:<20} ∩ {label_b:<20} = {overlap:>7}")

# Check: are there more accounts that block BEFORE smatsto with high overlap?
print("\n\n=== FINDING ALL UPSTREAM FEEDERS (block before smatsto, >2000 overlap) ===\n")
q_upstream = f"""
let smatsto_blocks = ['Bluesky.Graph.Block_v1']
| where did == '{SMATSTO}'
| project subject, t_smatsto = ___time;
['Bluesky.Graph.Block_v1']
| where subject in ((smatsto_blocks | project subject))
| where did != '{SMATSTO}'
| join kind=inner smatsto_blocks on subject
| extend is_before = iff(___time < t_smatsto, 1, 0)
| summarize 
    shared = count(),
    before_smatsto = sum(is_before),
    pct_before = round(100.0 * sum(is_before) / count(), 1)
by did
| where shared > 2000 and pct_before > 70
| order by shared desc
| take 30
"""
df_up = execute_query(q_upstream)
print(f"Found {len(df_up)} accounts that predominantly block BEFORE smatsto (>70%):\n")
print(f"{'DID':<45} {'Shared':>7} {'Before':>7} {'%Before':>7}")
print("-" * 75)
for _, r in df_up.iterrows():
    print(f"{r['did']:<45} {r['shared']:>7.0f} {r['before_smatsto']:>7.0f} {r['pct_before']:>6.1f}%")
