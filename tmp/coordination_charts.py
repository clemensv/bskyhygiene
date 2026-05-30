"""
Generate charts for the Statistical Proof of Coordination section.
"""
import sys
sys.path.insert(0, r'C:\Users\clemensv\OneDrive - Microsoft\Agents\nius\nius_bot_dossier')
from kusto_client import get_client
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

client = get_client()
DB = "bluesky"
ASSETS = r"d:\bskyhygiene\investigations\2026-05-30-louisbetonberlin-mass-blocking\assets"

def run(query):
    result = client.execute(DB, query)
    cols = [c.column_name for c in result.primary_results[0].columns]
    rows = [dict(zip(cols, row)) for row in result.primary_results[0]]
    return pd.DataFrame(rows)

LOUIS = "did:plc:kd4wtd75a637g2gvg2dh2b3t"
SMATSTO = "did:plc:gjcwwrezaz5qdcjn3347qvtl"
PAIR_A = "did:plc:3c7r453vexmpwu6nheazyikk"
PAIR_B = "did:plc:5v7itrhmq6zhvpqn2sfmcwaw"

RING_ALL = [
    LOUIS, SMATSTO,
    "did:plc:qildfzoh5p24jgion4xiycvz",
    "did:plc:xcytuwwb3b33ipiqzmqzbs45",
    "did:plc:hwpiekun4iebo4oqevjfe6ss",
    "did:plc:tfspkb2htmw7vwdgqj7mzx7m",
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
]

plt.style.use('dark_background')
COLORS = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24', '#6c5ce7', '#a29bfe', '#fd79a8', '#00b894']

# ============================================================
# CHART 1: Block-order scatter — Extended pair (ρ = 0.9996)
# ============================================================
print("Chart 1: Block-order correlation scatter...")
q_order = f"""
let a_seq = ['Bluesky.Graph.Block_v1']
    | where did == "{PAIR_A}"
    | summarize first_block = min(___time) by subject
    | order by first_block asc
    | serialize a_rank = row_number();
let b_seq = ['Bluesky.Graph.Block_v1']
    | where did == "{PAIR_B}"
    | summarize first_block = min(___time) by subject
    | order by first_block asc
    | serialize b_rank = row_number();
a_seq
| join kind=inner b_seq on subject
| project a_rank, b_rank
| sample 5000
"""
df_order = run(q_order)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Extended pair — near-perfect correlation
ax1.scatter(df_order['a_rank'], df_order['b_rank'], s=1, alpha=0.3, c='#4ecdc4')
ax1.plot([0, df_order['a_rank'].max()], [0, df_order['b_rank'].max()], 
         'r--', alpha=0.7, linewidth=1, label='Perfect correlation')
ax1.set_xlabel('Account A — Block sequence rank', fontsize=10)
ax1.set_ylabel('Account B — Block sequence rank', fontsize=10)
ax1.set_title(f'Extended Ring Members\nSpearman ρ = 0.9996 (n=95,806)', fontsize=12, fontweight='bold')
ax1.legend(loc='lower right')
ax1.text(0.05, 0.92, 'IDENTICAL LIST FILE', transform=ax1.transAxes, 
         fontsize=11, color='#ff6b6b', fontweight='bold')

# Louis vs smatsto — weak correlation
print("  Fetching Louis vs smatsto order...")
q_order2 = f"""
let louis_seq = ['Bluesky.Graph.Block_v1']
    | where did == "{LOUIS}"
    | summarize first_block = min(___time) by subject
    | order by first_block asc
    | serialize louis_rank = row_number();
let smatsto_seq = ['Bluesky.Graph.Block_v1']
    | where did == "{SMATSTO}"
    | summarize first_block = min(___time) by subject
    | order by first_block asc
    | serialize smatsto_rank = row_number();
louis_seq
| join kind=inner smatsto_seq on subject
| project louis_rank, smatsto_rank
| sample 5000
"""
df_order2 = run(q_order2)

ax2.scatter(df_order2['louis_rank'], df_order2['smatsto_rank'], s=1, alpha=0.3, c='#f9ca24')
ax2.plot([0, df_order2['louis_rank'].max()], [0, df_order2['smatsto_rank'].max()], 
         'r--', alpha=0.7, linewidth=1, label='Perfect correlation')
ax2.set_xlabel('Louis — Block sequence rank', fontsize=10)
ax2.set_ylabel('smatsto — Block sequence rank', fontsize=10)
ax2.set_title(f'Louis vs smatsto\nSpearman ρ = 0.058 (n=7,341)', fontsize=12, fontweight='bold')
ax2.legend(loc='lower right')
ax2.text(0.05, 0.92, 'SHARED TARGETS,\nDIFFERENT IMPORT ORDER', transform=ax2.transAxes, 
         fontsize=10, color='#f9ca24', fontweight='bold')

plt.tight_layout()
plt.savefig(f'{ASSETS}/block_order_correlation.png', dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
plt.close()
print("  ✓ Saved block_order_correlation.png")

# ============================================================
# CHART 2: Temporal lag histogram (smatsto → Louis)
# ============================================================
print("Chart 2: Temporal lag histogram...")
q_lag = f"""
let smatsto_blocks = ['Bluesky.Graph.Block_v1']
    | where did == "{SMATSTO}"
    | summarize smatsto_time = min(___time) by subject;
let louis_blocks = ['Bluesky.Graph.Block_v1']
    | where did == "{LOUIS}"
    | summarize louis_time = min(___time) by subject;
smatsto_blocks
| join kind=inner louis_blocks on subject
| extend lag_days = datetime_diff("hour", louis_time, smatsto_time) / 24.0
| project lag_days
"""
df_lag = run(q_lag)

fig, ax = plt.subplots(figsize=(12, 5))
lag_vals = df_lag['lag_days'].astype(float)
bins = np.linspace(-20, 30, 100)
ax.hist(lag_vals, bins=bins, color='#4ecdc4', alpha=0.8, edgecolor='none')
ax.axvline(x=0, color='white', linestyle='--', alpha=0.5, label='Same time')
median_lag = lag_vals.median()
ax.axvline(x=median_lag, color='#ff6b6b', linestyle='-', linewidth=2, 
           label=f'Median: {median_lag:.1f} days')
ax.set_xlabel('Lag (days) — positive = smatsto blocks first', fontsize=11)
ax.set_ylabel('Number of shared victims', fontsize=11)
ax.set_title('Temporal Lag: smatsto → Louis\nsmatsto blocks first in 78% of shared targets', 
             fontsize=13, fontweight='bold')
ax.legend(fontsize=11)
ax.text(0.72, 0.85, f'n = {len(lag_vals):,}\nMedian = {median_lag:.1f} days\n78% smatsto first', 
        transform=ax.transAxes, fontsize=10, color='white',
        bbox=dict(boxstyle='round', facecolor='#2d2d44', alpha=0.8))
plt.tight_layout()
plt.savefig(f'{ASSETS}/temporal_lag_histogram.png', dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
plt.close()
print("  ✓ Saved temporal_lag_histogram.png")

# ============================================================
# CHART 3: Multi-account daily activity heatmap
# ============================================================
print("Chart 3: Multi-account daily activity...")
dids_str = '","'.join(RING_ALL)
q_daily = f"""
['Bluesky.Graph.Block_v1']
| where did in ("{dids_str}")
| where ___time > datetime(2026-04-28)
| summarize blocks = count() by did, day = startofday(___time)
| where blocks >= 10
"""
df_daily = run(q_daily)

fig, ax = plt.subplots(figsize=(14, 6))

# Get unique DIDs sorted by total blocks
did_totals = df_daily.groupby('did')['blocks'].sum().sort_values(ascending=False)
top_dids = did_totals.head(12).index.tolist()

# Short labels
labels = {
    SMATSTO: 'smatsto',
    LOUIS: 'Louis',
}
for i, d in enumerate(top_dids):
    if d not in labels:
        labels[d] = f'Ring #{i+1}'

# Plot bars stacked by day
days = sorted(df_daily['day'].unique())
day_indices = {d: i for i, d in enumerate(days)}

for idx, did in enumerate(top_dids):
    did_data = df_daily[df_daily['did'] == did]
    x_positions = [day_indices[d] for d in did_data['day']]
    ax.scatter(x_positions, [idx] * len(x_positions), 
               s=did_data['blocks'].values / 200, 
               alpha=0.7, c=COLORS[idx % len(COLORS)], label=labels.get(did, did[:12]))

ax.set_yticks(range(len(top_dids)))
ax.set_yticklabels([labels.get(d, d[:15]) for d in top_dids], fontsize=9)
ax.set_xlabel('Day (Apr 28 – May 30, 2026)', fontsize=11)
ax.set_title('Ring Activity Heatmap — 28/29 days with 3+ members active\n(dot size = block volume)', 
             fontsize=13, fontweight='bold')

# X-axis labels
tick_positions = list(range(0, len(days), 3))
tick_labels = [str(days[i])[:10] for i in tick_positions]
ax.set_xticks(tick_positions)
ax.set_xticklabels(tick_labels, rotation=45, ha='right', fontsize=8)
ax.grid(axis='x', alpha=0.2)
plt.tight_layout()
plt.savefig(f'{ASSETS}/coordination_heatmap.png', dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
plt.close()
print("  ✓ Saved coordination_heatmap.png")

# ============================================================
# CHART 4: Chance vs observed overlap
# ============================================================
print("Chart 4: Chance vs observed overlap...")
fig, ax = plt.subplots(figsize=(8, 5))

categories = ['Expected by\nrandom chance', 'Observed\noverlap']
values = [4734, 96000]
colors = ['#636e72', '#ff6b6b']
bars = ax.bar(categories, values, color=colors, width=0.5, edgecolor='white', linewidth=0.5)
ax.set_ylabel('Shared blocked accounts', fontsize=11)
ax.set_title('Overlap Between Two Ring Members\nvs Random Expectation (Universe = 1.95M accounts)', 
             fontsize=12, fontweight='bold')
ax.bar_label(bars, labels=[f'{v:,.0f}' for v in values], padding=5, fontsize=12, fontweight='bold')
ax.text(0.5, 0.75, '20× random\nexpectation\np ≈ 0', transform=ax.transAxes, 
        fontsize=14, ha='center', color='#ff6b6b', fontweight='bold')
ax.set_ylim(0, 115000)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}K'))
plt.tight_layout()
plt.savefig(f'{ASSETS}/chance_vs_observed.png', dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
plt.close()
print("  ✓ Saved chance_vs_observed.png")

# ============================================================
# CHART 5: First-blocker pie chart
# ============================================================
print("Chart 5: First-blocker analysis...")
fig, ax = plt.subplots(figsize=(7, 7))

labels_pie = ['smatsto\n(261,428)', 'Extended B\n(96,211)', 'Louis\n(38,751)', 'Extended A\n(32,414)']
sizes = [261428, 96211, 38751, 32414]
colors_pie = ['#ff6b6b', '#4ecdc4', '#f9ca24', '#6c5ce7']
explode = (0.05, 0, 0, 0)

wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels_pie, colors=colors_pie,
                                   autopct='%1.0f%%', shadow=False, startangle=90,
                                   textprops={'fontsize': 11, 'color': 'white'})
for at in autotexts:
    at.set_fontweight('bold')
    at.set_fontsize(12)
ax.set_title('Who Blocks First Among Shared Targets?\n(smatsto = central discovery engine)', 
             fontsize=13, fontweight='bold', color='white')
plt.tight_layout()
plt.savefig(f'{ASSETS}/first_blocker.png', dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
plt.close()
print("  ✓ Saved first_blocker.png")

print("\n✓ All 5 charts saved to assets/")
