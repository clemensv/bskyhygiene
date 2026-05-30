import sys
sys.path.insert(0, r'C:\Users\clemensv\OneDrive - Microsoft\Agents\nius')
from nius_bot_dossier.kusto_client import execute_query
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from pathlib import Path

DID = 'did:plc:kd4wtd75a637g2gvg2dh2b3t'
ASSETS = Path(r'd:\bskyhygiene\investigations\2026-05-30-louisbetonberlin-mass-blocking\assets')
ASSETS.mkdir(exist_ok=True)

plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.bbox'] = 'tight'

# --- Chart 1: Daily block volume ---
print("Generating: daily block volume...")
q1 = f"""
['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| summarize blocks = count() by day = bin(___time, 1d)
| order by day asc
"""
df1 = execute_query(q1)
df1['day'] = pd.to_datetime(df1['day'])

fig, ax = plt.subplots(figsize=(12, 4))
ax.bar(df1['day'], df1['blocks'], width=0.8, color='#e63946', alpha=0.85)
ax.set_xlabel('')
ax.set_ylabel('Blocks')
ax.set_title('louisbetonberlin — Daily Block Volume', fontweight='bold')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
fig.autofmt_xdate()
# Mark automation onset
onset = pd.Timestamp('2026-05-06')
ax.axvline(onset, color='black', linestyle='--', alpha=0.6, linewidth=1)
ax.text(onset, ax.get_ylim()[1]*0.9, ' Automation\n onset', fontsize=8, va='top')
fig.savefig(ASSETS / 'daily_blocks.png')
plt.close()

# --- Chart 2: Inter-block gap distribution (log scale) ---
print("Generating: inter-block gap distribution...")
q2 = f"""
['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| where ___time > datetime(2026-05-06)
| order by ___time asc
| serialize
| extend gap_ms = datetime_diff('millisecond', ___time, prev(___time))
| where gap_ms > 0 and gap_ms < 600000
| project gap_ms
"""
df2 = execute_query(q2)

fig, ax = plt.subplots(figsize=(10, 4))
ax.hist(df2['gap_ms'], bins=np.logspace(1, 5.8, 80), color='#457b9d', alpha=0.85)
ax.set_xscale('log')
ax.axvline(80, color='#e63946', linestyle='--', linewidth=2, label='Median ~80ms')
ax.axvline(1000, color='orange', linestyle='--', linewidth=1.5, label='1 second')
ax.set_xlabel('Inter-block gap (ms, log scale)')
ax.set_ylabel('Count')
ax.set_title('Inter-Block Timing Distribution (Automated Phase)', fontweight='bold')
ax.legend()
fig.savefig(ASSETS / 'gap_distribution.png')
plt.close()

# --- Chart 3: Ring members - total blocks comparison ---
print("Generating: ring member comparison...")
ring = [
    DID,
    'did:plc:gjcwwrezaz5qdcjn3347qvtl',
    'did:plc:qildfzoh5p24jgion4xiycvz',
    'did:plc:xcytuwwb3b33ipiqzmqzbs45',
    'did:plc:hwpiekun4iebo4oqevjfe6ss',
    'did:plc:tfspkb2htmw7vwdgqj7mzx7m',
]
dids_str = "', '".join(ring)
q3 = f"""
['Bluesky.Graph.Block_v1']
| where did in ('{dids_str}')
| summarize blocks = count() by did
| order by blocks desc
"""
df3 = execute_query(q3)

labels_map = {
    DID: 'louisbetonberlin',
    'did:plc:gjcwwrezaz5qdcjn3347qvtl': 'smatsto',
    'did:plc:qildfzoh5p24jgion4xiycvz': 'fuenfuhrteefix',
    'did:plc:xcytuwwb3b33ipiqzmqzbs45': 'holbidope',
    'did:plc:hwpiekun4iebo4oqevjfe6ss': 'kaffchris',
    'did:plc:tfspkb2htmw7vwdgqj7mzx7m': 'kunststein',
}
df3['label'] = df3['did'].map(labels_map)

fig, ax = plt.subplots(figsize=(10, 4))
colors = ['#e63946' if d == DID else '#457b9d' for d in df3['did']]
ax.barh(df3['label'], df3['blocks'], color=colors, alpha=0.85)
ax.set_xlabel('Total Blocks')
ax.set_title('Ring Members — Total Block Count', fontweight='bold')
for i, (v, l) in enumerate(zip(df3['blocks'], df3['label'])):
    ax.text(v + 2000, i, f'{v:,}', va='center', fontsize=9)
ax.set_xlim(0, df3['blocks'].max() * 1.15)
fig.savefig(ASSETS / 'ring_comparison.png')
plt.close()

# --- Chart 4: Victim language distribution ---
print("Generating: victim language distribution...")
lang_data = {
    'English': 4702496,
    'Spanish': 326046,
    'German': 293444,
    'French': 153797,
    'Dutch': 123936,
    'Portuguese': 77360,
    'Italian': 57283,
    'Japanese': 51541,
    'Other': 30711+28190+27692+26166+23012+14956+9020
}
labels = list(lang_data.keys())
values = list(lang_data.values())

fig, ax = plt.subplots(figsize=(8, 5))
wedges, texts, autotexts = ax.pie(
    values, labels=labels, autopct=lambda p: f'{p:.1f}%' if p > 2 else '',
    colors=plt.cm.Set3(np.linspace(0, 1, len(labels))),
    startangle=90, pctdistance=0.8
)
ax.set_title('Language of Victim Posts (May 2026)', fontweight='bold')
fig.savefig(ASSETS / 'victim_languages.png')
plt.close()

# --- Chart 5: Blocks per hour on May 27 (peak day) ---
print("Generating: hourly pattern on peak day...")
q5 = f"""
['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| where ___time between(datetime(2026-05-27) .. datetime(2026-05-28))
| summarize blocks = count() by hour = bin(___time, 1h)
| order by hour asc
"""
df5 = execute_query(q5)
df5['hour'] = pd.to_datetime(df5['hour'])
df5['h'] = df5['hour'].dt.hour

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(df5['h'], df5['blocks'], color='#e63946', alpha=0.85, width=0.8)
ax.set_xlabel('Hour (UTC)')
ax.set_ylabel('Blocks')
ax.set_title('May 27: Peak Day Hourly Pattern (11,574 blocks)', fontweight='bold')
ax.set_xticks(range(0, 24))
# Add CET annotation
ax.axvspan(10, 21, alpha=0.08, color='blue')
ax.text(15.5, ax.get_ylim()[1] if ax.get_ylim()[1] > 0 else df5['blocks'].max()*0.9,
        '12:00–23:00 CET', ha='center', fontsize=9, color='navy', alpha=0.7)
fig.savefig(ASSETS / 'peak_day_hourly.png')
plt.close()

# --- Chart 6: Ring coordination timeline ---
print("Generating: ring coordination timeline...")
q6 = f"""
['Bluesky.Graph.Block_v1']
| where did in ('{dids_str}')
| summarize blocks = count() by did, day = bin(___time, 1d)
| order by day asc
"""
df6 = execute_query(q6)
df6['day'] = pd.to_datetime(df6['day'])
df6['label'] = df6['did'].map(labels_map)

fig, ax = plt.subplots(figsize=(12, 5))
for label in ['smatsto', 'fuenfuhrteefix', 'kaffchris', 'holbidope', 'kunststein', 'louisbetonberlin']:
    subset = df6[df6['label'] == label]
    style = {'linewidth': 2.5, 'alpha': 0.9} if label == 'louisbetonberlin' else {'linewidth': 1.2, 'alpha': 0.7}
    ax.plot(subset['day'], subset['blocks'], label=label, **style)
ax.set_xlabel('')
ax.set_ylabel('Daily Blocks')
ax.set_title('Ring Coordination — Daily Block Volume Per Member', fontweight='bold')
ax.legend(loc='upper left', fontsize=8)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
fig.autofmt_xdate()
fig.savefig(ASSETS / 'ring_timeline.png')
plt.close()

# --- Chart 7: Blocked vs unblocked replier activity ---
print("Generating: blocked vs unblocked activity comparison...")
fig, ax = plt.subplots(figsize=(7, 4))
categories = ['Blocked\nrepliers', 'Unblocked\nrepliers']
medians = [284, 109]
avgs = [533, 241]
x = np.arange(len(categories))
w = 0.35
ax.bar(x - w/2, medians, w, label='Median posts/month', color='#e63946', alpha=0.85)
ax.bar(x + w/2, avgs, w, label='Mean posts/month', color='#457b9d', alpha=0.85)
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.set_ylabel('Posts per month')
ax.set_title('Targeting Filter: Blocked Accounts Are 2× More Active', fontweight='bold')
ax.legend()
for i, (m, a) in enumerate(zip(medians, avgs)):
    ax.text(i - w/2, m + 5, str(m), ha='center', fontsize=9)
    ax.text(i + w/2, a + 5, str(a), ha='center', fontsize=9)
fig.savefig(ASSETS / 'activity_filter.png')
plt.close()

print(f"\nDone! {len(list(ASSETS.glob('*.png')))} charts saved to {ASSETS}")
