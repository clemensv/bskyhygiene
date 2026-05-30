"""
Prove coordination among the blocking ring with three independent statistical tests:
1. Block-order correlation (Spearman rank) between ring member pairs
2. Temporal lag distribution (smatsto → others)
3. Session start-time clustering
"""
import sys
sys.path.insert(0, r'C:\Users\clemensv\OneDrive - Microsoft\Agents\nius')
from nius_bot_dossier.kusto_client import execute_query
import pandas as pd
import numpy as np
from scipy import stats

RING_CORE = [
    'did:plc:kd4wtd75a637g2gvg2dh2b3t',  # louisbetonberlin
    'did:plc:qildfzoh5p24jgion4xiycvz',  # ?
    'did:plc:hwpiekun4iebo4oqevjfe6ss',  # smatsto
    'did:plc:tfspkb2htmw7vwdgqj7mzx7m',  # ?
    'did:plc:xcytuwwb3b33ipiqzmqzbs45',  # ?
]

RING_EXTENDED = [
    'did:plc:u4afrfvqhpbvmiiwgsz5foah',  # dqita
    'did:plc:jnf4nqfg3tcsbn5y7cxhewsk',  # adametokirkfor
    'did:plc:wqiuzunhgxwrrz4x773uuuaq',  # maribel1917
    'did:plc:k7qncpjhcfhs2i6fpuzmvlcz',  # castironirish
    'did:plc:a7sglx3gv6ybiupmpfv6scla',  # solire
    'did:plc:eaztq5lfnzyxu4h56kmuxffy',  # sasunarusasu
    'did:plc:2zxfr4ykhb7dj3sq7vrsm3jl',  # fakeflamesprite
    'did:plc:7dqih3dvqq6fv3bydqamdjk3',  # fkftsh
    'did:plc:mpuymtmbz25zzh6e5nqgb3u6',  # vappytoy
    'did:plc:vrvxwx2m4nnkcsbnkqwcdwba',  # verezi
]

# First, resolve DIDs for ring members we only know by handle
print("=== RESOLVING RING MEMBER DIDs ===")
resolve_q = """
['Bluesky.Actor.Profile_v2']
| summarize arg_max(___time, *) by did
| where handle in (
    'smatsto.bsky.social',
    'louisbetonberlin.bsky.social',
    'kaffchris.bsky.social',
    'fuenfuhrteefix.bsky.social',
    'holbidope.bsky.social',
    'wystrach.de',
    'kunststein.bsky.social',
    'dqita.bsky.social',
    'adametokirkfor.bsky.social',
    'maribel1917.bsky.social',
    'castironirish.bsky.social',
    'solire.bsky.social',
    'sasunarusasu.bsky.social',
    'fakeflamesprite.bsky.social',
    'fkftsh.myatproto.social',
    'vappytoy.bsky.social',
    'verezi.bsky.social'
)
| project handle, did
"""
df_handles = execute_query(resolve_q)
print(df_handles.to_string())
handle_to_did = dict(zip(df_handles['handle'], df_handles['did']))
print(f"\nResolved {len(handle_to_did)} handles")

# Build complete DID list from resolution
SMATSTO_DID = handle_to_did.get('smatsto.bsky.social', 'did:plc:hwpiekun4iebo4oqevjfe6ss')
LOUIS_DID = 'did:plc:kd4wtd75a637g2gvg2dh2b3t'
ALL_DIDS = list(handle_to_did.values())

print(f"\n{'='*70}")
print("TEST 1: BLOCK-ORDER CORRELATION (Spearman rank)")
print(f"{'='*70}")
print("If two accounts independently decide whom to block, block order is random → ρ ≈ 0")
print("If they import the same list file, block order is identical → ρ ≈ 1.0\n")

# Get block sequences for shared victims between pairs
# Compare Louis vs smatsto block order
q_order = f"""
let louis_blocks = 
    ['Bluesky.Graph.Block_v1']
    | where did == '{LOUIS_DID}'
    | summarize first_block = min(___time) by subject
    | extend louis_rank = row_number(1, first_block asc);
let smatsto_blocks =
    ['Bluesky.Graph.Block_v1']
    | where did == '{SMATSTO_DID}'
    | summarize first_block = min(___time) by subject
    | extend smatsto_rank = row_number(1, first_block asc);
louis_blocks
| join kind=inner smatsto_blocks on subject
| project subject, louis_rank, smatsto_rank
| order by louis_rank asc
| take 50000
"""
print("Querying block order for Louis vs smatsto...")
df_order = execute_query(q_order)
if len(df_order) > 100:
    rho, pval = stats.spearmanr(df_order['louis_rank'], df_order['smatsto_rank'])
    print(f"  Shared victims: {len(df_order)}")
    print(f"  Spearman ρ = {rho:.4f}")
    print(f"  p-value = {pval:.2e}")
    print(f"  Interpretation: {'STRONG correlation → shared list' if rho > 0.5 else 'Weak correlation → independent targeting' if rho < 0.3 else 'Moderate correlation'}")
else:
    print(f"  Only {len(df_order)} shared victims — insufficient for rank correlation")

# Also test extended ring members with near-100% overlap
# Pick castironirish and adametokirkfor (both 96K blocks, ~100% overlap with each other)
if 'castironirish.bsky.social' in handle_to_did and 'adametokirkfor.bsky.social' in handle_to_did:
    cast_did = handle_to_did['castironirish.bsky.social']
    adam_did = handle_to_did['adametokirkfor.bsky.social']
    q_order2 = f"""
    let cast_blocks = 
        ['Bluesky.Graph.Block_v1']
        | where did == '{cast_did}'
        | summarize first_block = min(___time) by subject
        | extend cast_rank = row_number(1, first_block asc);
    let adam_blocks =
        ['Bluesky.Graph.Block_v1']
        | where did == '{adam_did}'
        | summarize first_block = min(___time) by subject
        | extend adam_rank = row_number(1, first_block asc);
    cast_blocks
    | join kind=inner adam_blocks on subject
    | project subject, cast_rank, adam_rank
    | order by cast_rank asc
    | take 50000
    """
    print("\nQuerying block order for castironirish vs adametokirkfor...")
    df_order2 = execute_query(q_order2)
    if len(df_order2) > 100:
        rho2, pval2 = stats.spearmanr(df_order2['cast_rank'], df_order2['adam_rank'])
        print(f"  Shared victims: {len(df_order2)}")
        print(f"  Spearman ρ = {rho2:.4f}")
        print(f"  p-value = {pval2:.2e}")
        print(f"  Interpretation: {'STRONG correlation → same list file imported' if rho2 > 0.5 else 'Weak → independent'}")

print(f"\n{'='*70}")
print("TEST 2: TEMPORAL LAG DISTRIBUTION (smatsto → ring members)")
print(f"{'='*70}")
print("If coordinated: consistent lag (hours/days) between smatsto blocking and others")
print("If independent: random lag with no characteristic peak\n")

q_lag = f"""
let smatsto_blocks = 
    ['Bluesky.Graph.Block_v1']
    | where did == '{SMATSTO_DID}'
    | summarize smatsto_time = min(___time) by subject;
let louis_blocks =
    ['Bluesky.Graph.Block_v1']
    | where did == '{LOUIS_DID}'
    | summarize louis_time = min(___time) by subject;
smatsto_blocks
| join kind=inner louis_blocks on subject
| extend lag_hours = datetime_diff("hour", louis_time, smatsto_time)
| summarize 
    count_total = count(),
    median_lag_hours = percentile(lag_hours, 50),
    p25_lag_hours = percentile(lag_hours, 25),
    p75_lag_hours = percentile(lag_hours, 75),
    pct_smatsto_first = countif(lag_hours > 0) * 100.0 / count(),
    pct_louis_first = countif(lag_hours < 0) * 100.0 / count(),
    pct_same_hour = countif(abs(lag_hours) <= 1) * 100.0 / count()
"""
print("Querying temporal lag smatsto → Louis...")
df_lag = execute_query(q_lag)
print(df_lag.to_string())

# Lag distribution histogram
q_lag_hist = f"""
let smatsto_blocks = 
    ['Bluesky.Graph.Block_v1']
    | where did == '{SMATSTO_DID}'
    | summarize smatsto_time = min(___time) by subject;
let louis_blocks =
    ['Bluesky.Graph.Block_v1']
    | where did == '{LOUIS_DID}'
    | summarize louis_time = min(___time) by subject;
smatsto_blocks
| join kind=inner louis_blocks on subject
| extend lag_days = datetime_diff("hour", louis_time, smatsto_time) / 24.0
| extend lag_bucket = case(
    lag_days < -7, "< -7d",
    lag_days < -1, "-7d to -1d",
    lag_days < 0, "-1d to 0",
    lag_days < 1, "0 to 1d",
    lag_days < 3, "1d to 3d",
    lag_days < 7, "3d to 7d",
    lag_days < 14, "7d to 14d",
    "> 14d"
)
| summarize count = count() by lag_bucket
| order by lag_bucket asc
"""
print("\nLag distribution (smatsto → Louis):")
df_lag_hist = execute_query(q_lag_hist)
print(df_lag_hist.to_string())

print(f"\n{'='*70}")
print("TEST 3: SESSION START-TIME CLUSTERING")
print(f"{'='*70}")
print("If coordinated: blocking sessions start within minutes of each other")
print("If independent: random session start times\n")

# Identify blocking sessions (gaps > 30 min = new session)
q_sessions = f"""
let all_ring_blocks =
    ['Bluesky.Graph.Block_v1']
    | where did in ('{LOUIS_DID}', '{SMATSTO_DID}')
    | where ___time > datetime(2026-05-01)
    | project did, ___time
    | order by did asc, ___time asc
    | extend prev_time = prev(___time), prev_did = prev(did)
    | extend gap_min = iff(did == prev_did, datetime_diff("minute", ___time, prev_time), 9999)
    | where gap_min > 30 or isnull(prev_time) or did != prev_did
    | project did, session_start = ___time;
all_ring_blocks
| extend session_hour = bin(session_start, 1h)
| summarize accounts = make_set(did), account_count = dcount(did) by session_hour
| where account_count > 1
| order by session_hour asc
"""
print("Querying overlapping session starts (Louis + smatsto)...")
df_sessions = execute_query(q_sessions)
print(f"Hours where both accounts started sessions: {len(df_sessions)}")
if len(df_sessions) > 0:
    print(df_sessions.head(20).to_string())

# Test 3b: For all ring members, find days where 3+ members run sessions
q_multi_sessions = """
let ring_dids = dynamic(['{dids}']);
['Bluesky.Graph.Block_v1']
| where did in (ring_dids)
| where ___time > datetime(2026-04-28)
| summarize 
    block_count = count(),
    first_block = min(___time),
    last_block = max(___time)
    by did, day = bin(___time, 1d)
| where block_count > 100
| summarize 
    active_accounts = dcount(did),
    account_list = make_set(did),
    total_blocks = sum(block_count)
    by day
| where active_accounts >= 3
| order by day asc
""".replace('{dids}', "','".join(ALL_DIDS))
print("\nDays with 3+ ring members active (>100 blocks each):")
df_multi = execute_query(q_multi_sessions)
print(df_multi.to_string())

print(f"\n{'='*70}")
print("TEST 4: IDENTICAL BATCH BOUNDARIES")
print(f"{'='*70}")
print("If same list file: batch pauses occur at same position in the victim sequence")
print("(Same DID blocked just before a pause in multiple accounts)\n")

# Find batch boundaries (gaps > 5 min) and check if same subject appears at boundaries
q_batches = f"""
let louis_batches =
    ['Bluesky.Graph.Block_v1']
    | where did == '{LOUIS_DID}'
    | where ___time between (datetime(2026-05-27) .. datetime(2026-05-28))
    | order by ___time asc
    | extend prev_time = prev(___time), prev_subject = prev(subject)
    | extend gap_sec = datetime_diff("second", ___time, prev_time)
    | where gap_sec > 300
    | project batch_end_subject = prev_subject, batch_start_subject = subject, 
             gap_sec, batch_start_time = ___time
    | extend source = "louis";
let smatsto_batches =
    ['Bluesky.Graph.Block_v1']
    | where did == '{SMATSTO_DID}'
    | where ___time between (datetime(2026-05-27) .. datetime(2026-05-28))
    | order by ___time asc
    | extend prev_time = prev(___time), prev_subject = prev(subject)
    | extend gap_sec = datetime_diff("second", ___time, prev_time)
    | where gap_sec > 300
    | project batch_end_subject = prev_subject, batch_start_subject = subject, 
             gap_sec, batch_start_time = ___time
    | extend source = "smatsto";
union louis_batches, smatsto_batches
| order by batch_start_time asc
"""
print("Querying batch boundaries on May 27...")
df_batches = execute_query(q_batches)
print(f"Batch pauses found: {len(df_batches)}")
if len(df_batches) > 0:
    print(df_batches.to_string())
    # Check if batch_start_subjects overlap
    louis_starts = set(df_batches[df_batches['source'] == 'louis']['batch_start_subject'])
    smatsto_starts = set(df_batches[df_batches['source'] == 'smatsto']['batch_start_subject'])
    overlap = louis_starts & smatsto_starts
    print(f"\nBatch-start subjects shared: {len(overlap)} / Louis: {len(louis_starts)}, smatsto: {len(smatsto_starts)}")

print(f"\n{'='*70}")
print("SUMMARY")
print(f"{'='*70}")
