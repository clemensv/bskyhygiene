"""Block-order correlation and first-blocker analysis for new accounts."""
import sys
sys.path.insert(0, r'C:\Users\clemensv\OneDrive - Microsoft\Agents\nius')
from nius_bot_dossier.kusto_client import execute_query

SMATSTO = 'did:plc:gjcwwrezaz5qdcjn3347qvtl'

TARGETS = [
    ('did:plc:qyuua6edp64sxlwcb6myitst', '(deleted)'),
    ('did:plc:4fn4mppxm73jldgas7a52kcu', 'chicagosunroof'),
    ('did:plc:lsaii34slgzwooxhfesamrk2', 'harrywoodard'),
    ('did:plc:jyqk4xrplfhsl6dfeibuw37c', 'andeanpuppy'),
    ('did:plc:zcx3ryxqcbc4tawv7bam64mq', 'punishedpuppy'),
    ('did:plc:ye2r45gcu33r5gkbb2dajb34', 'cayennepompep'),
]

# Who blocks first: smatsto or new account?
print("=== WHO BLOCKS FIRST: SMATSTO vs NEW ACCOUNT ===\n")
for did, label in TARGETS:
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
    df_f = execute_query(q_first)
    if len(df_f) > 0:
        r = df_f.iloc[0]
        pct_s = (r['smatsto_first'] / r['total'] * 100) if r['total'] > 0 else 0
        print(f"  {label:<28} smatsto first: {pct_s:.0f}% ({r['smatsto_first']:.0f}/{r['total']:.0f})  median lag: {r['median_lag_hours']:.0f}h")

# Block-order analysis: Spearman rank via sampled approach
print("\n\n=== BLOCK-ORDER SIMILARITY (sampled top-10K shared) ===\n")
for did, label in TARGETS:
    q_order = f"""
    let a = ['Bluesky.Graph.Block_v1']
    | where did == '{SMATSTO}'
    | order by ___time asc
    | extend rank_a = row_number()
    | project subject, rank_a;
    let b = ['Bluesky.Graph.Block_v1']
    | where did == '{did}'
    | order by ___time asc
    | extend rank_b = row_number()
    | project subject, rank_b;
    a
    | join kind=inner b on subject
    | top 10000 by rank_b asc
    | summarize 
        shared = count(),
        avg_rank_a = avg(rank_a),
        avg_rank_b = avg(rank_b),
        stdev_a = stdev(rank_a),
        stdev_b = stdev(rank_b),
        covar = avg(rank_a * rank_b) - avg(rank_a) * avg(rank_b)
    """
    df_o = execute_query(q_order)
    if len(df_o) > 0:
        r = df_o.iloc[0]
        # Pearson correlation from covariance
        if r['stdev_a'] > 0 and r['stdev_b'] > 0:
            corr = r['covar'] / (r['stdev_a'] * r['stdev_b'])
        else:
            corr = 0
        print(f"  {label:<28} shared={r['shared']:>7.0f}  rank_corr≈{corr:.4f}")
    else:
        print(f"  {label:<28} (no data)")

# Account creation dates and profile info
print("\n\n=== ACCOUNT CREATION & TOTAL BLOCKS ===\n")
did_list = "', '".join(d for d, _ in TARGETS)
q_info = f"""
['Bluesky.Graph.Block_v1']
| where did in ('{did_list}')
| summarize 
    total_blocks = count(),
    first_block = min(___time),
    last_block = max(___time),
    active_days = dcount(bin(___time, 1d)),
    blocks_per_active_day = count() / dcount(bin(___time, 1d))
by did
| order by total_blocks desc
"""
df_info = execute_query(q_info)
print(f"{'DID':<45} {'Total':>7} {'Days':>5} {'Blk/day':>8} {'First':<12} {'Last':<12}")
print("-" * 100)
for _, r in df_info.iterrows():
    print(f"{r['did']:<45} {r['total_blocks']:>7} {r['active_days']:>5} {r['blocks_per_active_day']:>8.0f} {str(r['first_block'])[:10]:<12} {str(r['last_block'])[:10]:<12}")
