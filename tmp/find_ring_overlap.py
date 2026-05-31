"""Find accounts with high block overlap with smatsto (central crawling engine).

Queries the Kusto/Eventhouse database for accounts that share significant
block targets with smatsto, filtering out already-known ring members.
"""
import sys
sys.path.insert(0, r'C:\Users\clemensv\OneDrive - Microsoft\Agents\nius')
from nius_bot_dossier.kusto_client import execute_query
import requests
import json

SMATSTO = 'did:plc:gjcwwrezaz5qdcjn3347qvtl'

# Already known ring members (core + extended)
KNOWN_MEMBERS = {
    'did:plc:gjcwwrezaz5qdcjn3347qvtl',  # smatsto
    'did:plc:kd4wtd75a637g2gvg2dh2b3t',  # louisbetonberlin
    'did:plc:qildfzoh5p24jgion4xiycvz',  # core
    'did:plc:hwpiekun4iebo4oqevjfe6ss',  # core
    'did:plc:xcytuwwb3b33ipiqzmqzbs45',  # core
    'did:plc:tfspkb2htmw7vwdgqj7mzx7m',  # core (wystrach.de)
    'did:plc:ajvwz5alprhutyx3zuwrg7dc',  # kaffchris
    'did:plc:gkg3mo2wltuzdzww53rkxfqg',  # fuenfuhrteefix
    'did:plc:33wcrgvuwuxvzpa74yud37qp',  # holbidope
    'did:plc:45nedwgk4a222oynw3mcp4vl',  # kunststein
    'did:plc:yw4a6u3yriokk4bnrp57qp4u',  # dqita
    'did:plc:x2ttzjlz7lhmjrlbqogslkwj',  # adametokirkfor
    'did:plc:gqqmj4xnlnxoeeglwnpvfzgo',  # maribel1917
    'did:plc:42yv3c3jcxb7tkm3cevxnkoe',  # castironirish
    'did:plc:oolq4vjiw3jbflxswcewjm5c',  # solire
    'did:plc:dkvdnw2t4ksfqfstxdbddwfr',  # sasunarusasu
    'did:plc:wvqkmh5o77epcmqj7tjsyj43',  # fakeflamesprite
    'did:plc:rqzwirjnmh3h46fcnqnfkprg',  # fkftsh
    'did:plc:7wkxjc74ydpbaduvomwibwmf',  # vappytoy
    'did:plc:44vclvhbz4byahypbnq3yoxq',  # verezi
}

# Step 1: Find all accounts that share 1000+ blocks with smatsto's targets
print("=== FINDING ACCOUNTS WITH HIGH OVERLAP WITH SMATSTO ===")
print("(This may take a moment...)\n")

q_overlap = f"""
let smatsto_targets = ['Bluesky.Graph.Block_v1']
| where did == '{SMATSTO}'
| distinct subject;
['Bluesky.Graph.Block_v1']
| where subject in (smatsto_targets)
| where did != '{SMATSTO}'
| summarize shared_blocks = count(), first_block = min(___time), last_block = max(___time) by did
| where shared_blocks > 1000
| order by shared_blocks desc
| take 100
"""

df = execute_query(q_overlap)
print(f"Found {len(df)} accounts with >1000 shared targets with smatsto\n")

# Filter out known members
new_accounts = []
for _, row in df.iterrows():
    if row['did'] not in KNOWN_MEMBERS:
        new_accounts.append(row)

print(f"After filtering known members: {len(new_accounts)} NEW accounts\n")
print(f"{'DID':<45} {'Shared':>8} {'First block':<20} {'Last block':<20}")
print("-" * 100)
for row in new_accounts[:50]:
    print(f"{row['did']:<45} {row['shared_blocks']:>8} {str(row['first_block'])[:19]:<20} {str(row['last_block'])[:19]:<20}")

# Step 2: For the new accounts, get their total block counts and timing
if new_accounts:
    print("\n\n=== DETAILED ANALYSIS OF NEW ACCOUNTS ===\n")
    new_dids = [r['did'] for r in new_accounts[:30]]
    did_list = "', '".join(new_dids)
    
    q_details = f"""
    ['Bluesky.Graph.Block_v1']
    | where did in ('{did_list}')
    | summarize 
        total_blocks = count(),
        unique_targets = dcount(subject),
        first_block = min(___time),
        last_block = max(___time),
        active_days = dcount(bin(___time, 1d))
    by did
    | order by total_blocks desc
    """
    df_details = execute_query(q_details)
    
    print(f"{'DID':<45} {'Total':>8} {'Unique':>8} {'Days':>5} {'First':<12} {'Last':<12}")
    print("-" * 100)
    for _, row in df_details.iterrows():
        print(f"{row['did']:<45} {row['total_blocks']:>8} {row['unique_targets']:>8} {row['active_days']:>5} {str(row['first_block'])[:10]:<12} {str(row['last_block'])[:10]:<12}")

    # Step 3: Resolve handles for new accounts
    print("\n\n=== RESOLVING HANDLES ===\n")
    for did in new_dids[:30]:
        try:
            r = requests.get(
                'https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile',
                params={'actor': did},
                timeout=10
            )
            if r.status_code == 200:
                p = r.json()
                handle = p.get('handle', '?')
                display = p.get('displayName', '')
                followers = p.get('followersCount', 0)
                following = p.get('followsCount', 0)
                posts = p.get('postsCount', 0)
                labels = ', '.join(l.get('val', '') for l in p.get('labels', []))
                # Find this DID's overlap count
                overlap_count = next((r2['shared_blocks'] for r2 in new_accounts if r2['did'] == did), 0)
                print(f"  {handle:<35} {display:<25} F:{followers:<6} Blk-overlap:{overlap_count:<8} Posts:{posts}")
            else:
                print(f"  {did} — HTTP {r.status_code}")
        except Exception as e:
            print(f"  {did} — Error: {e}")

    # Step 4: Check inter-block timing for the top new accounts (automation check)
    print("\n\n=== TIMING ANALYSIS (TOP 10 NEW ACCOUNTS) ===\n")
    for did in new_dids[:10]:
        q_timing = f"""
        ['Bluesky.Graph.Block_v1']
        | where did == '{did}'
        | order by ___time asc
        | extend gap_ms = datetime_diff('millisecond', ___time, prev(___time))
        | where isnotnull(gap_ms) and gap_ms > 0 and gap_ms < 600000
        | summarize 
            median_gap = percentile(gap_ms, 50),
            p5_gap = percentile(gap_ms, 5),
            p95_gap = percentile(gap_ms, 95),
            fast_blocks = countif(gap_ms < 200),
            total_gaps = count()
        """
        df_t = execute_query(q_timing)
        if len(df_t) > 0:
            row = df_t.iloc[0]
            pct_fast = (row['fast_blocks'] / row['total_gaps'] * 100) if row['total_gaps'] > 0 else 0
            print(f"  {did[:40]:<42} median:{row['median_gap']:>8.0f}ms  p95:{row['p95_gap']:>8.0f}ms  fast(<200ms):{pct_fast:.0f}%")
