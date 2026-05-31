"""Timing analysis for newly discovered high-overlap accounts."""
import sys
sys.path.insert(0, r'C:\Users\clemensv\OneDrive - Microsoft\Agents\nius')
from nius_bot_dossier.kusto_client import execute_query

TARGETS = [
    ('did:plc:qyuua6edp64sxlwcb6myitst', '(deleted account)'),
    ('did:plc:4fn4mppxm73jldgas7a52kcu', 'chicagosunroof'),
    ('did:plc:lsaii34slgzwooxhfesamrk2', 'harrywoodard'),
    ('did:plc:jyqk4xrplfhsl6dfeibuw37c', 'andeanpuppy.latinsky.app'),
    ('did:plc:zcx3ryxqcbc4tawv7bam64mq', 'punishedpuppy'),
    ('did:plc:ye2r45gcu33r5gkbb2dajb34', 'cayennepompep'),
    ('did:plc:dvhyaxbrf7uh6eemujbd4jao', 'sasunarusasu (recheck)'),
    ('did:plc:22msnh4bnrc6gg54kvrrtc4o', 'buildingtheacademy'),
    ('did:plc:oqc7737mwl6y22wjqdduujex', 'fkftsh (recheck)'),
    ('did:plc:qbw4i5hcyc6dtuckixaogxlc', 'solire (recheck)'),
]

print("=== TIMING ANALYSIS: NEW HIGH-OVERLAP ACCOUNTS ===\n")
print(f"{'Handle':<30} {'Median':>9} {'P5':>9} {'P95':>9} {'<200ms':>8} {'<100ms':>8} {'Total':>7}")
print("-" * 95)

for did, label in TARGETS:
    q = f"""
    ['Bluesky.Graph.Block_v1']
    | where did == '{did}'
    | order by ___time asc
    | extend gap_ms = datetime_diff('millisecond', ___time, prev(___time))
    | where isnotnull(gap_ms) and gap_ms > 0 and gap_ms < 600000
    | summarize 
        median_gap = percentile(gap_ms, 50),
        p5_gap = percentile(gap_ms, 5),
        p95_gap = percentile(gap_ms, 95),
        fast_200 = countif(gap_ms < 200),
        fast_100 = countif(gap_ms < 100),
        total_gaps = count()
    """
    df = execute_query(q)
    if len(df) > 0:
        r = df.iloc[0]
        pct200 = (r['fast_200'] / r['total_gaps'] * 100) if r['total_gaps'] > 0 else 0
        pct100 = (r['fast_100'] / r['total_gaps'] * 100) if r['total_gaps'] > 0 else 0
        print(f"  {label:<28} {r['median_gap']:>8.0f}ms {r['p5_gap']:>8.0f}ms {r['p95_gap']:>8.0f}ms {pct200:>7.0f}% {pct100:>7.0f}% {r['total_gaps']:>7.0f}")

# Daily breakdown for the most suspicious accounts
print("\n\n=== DAILY BLOCK VOLUME (TOP SUSPICIOUS) ===\n")
for did, label in TARGETS[:6]:
    q_daily = f"""
    ['Bluesky.Graph.Block_v1']
    | where did == '{did}'
    | summarize blocks = count() by day = bin(___time, 1d)
    | order by blocks desc
    | take 5
    """
    df_d = execute_query(q_daily)
    print(f"  {label}:")
    for _, row in df_d.iterrows():
        print(f"    {str(row['day'])[:10]}  {row['blocks']:>8} blocks")
    print()

# Block-order correlation: do the new accounts share order with smatsto?
print("\n=== BLOCK-ORDER CORRELATION WITH SMATSTO (TOP NEW ACCOUNTS) ===\n")
SMATSTO = 'did:plc:gjcwwrezaz5qdcjn3347qvtl'
for did, label in TARGETS[:6]:
    q_corr = f"""
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
    | summarize 
        shared = count(),
        corr = row_correlation(rank_a, rank_b)
    """
    df_c = execute_query(q_corr)
    if len(df_c) > 0:
        r = df_c.iloc[0]
        print(f"  {label:<28} shared={r['shared']:>7.0f}  rho={r['corr']:.4f}")
    else:
        print(f"  {label:<28} (no data)")

# Who blocks first: smatsto or new account?
print("\n\n=== WHO BLOCKS FIRST: SMATSTO vs NEW ACCOUNT ===\n")
for did, label in TARGETS[:6]:
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
