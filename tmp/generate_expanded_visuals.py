"""Generate updated visuals for the expanded ring investigation.

Produces:
- ring_hierarchy_expanded.png: Full hierarchy (upstream → smatsto → downstream)
- expanded_ring_members.png: All members by total blocks (horizontal bar)
- upstream_timing.png: When each feeder starts vs smatsto
- ring_network.png: Network graph showing directionality
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

plt.rcParams['font.family'] = 'Segoe UI'
plt.rcParams['font.size'] = 9
plt.rcParams['figure.dpi'] = 150

ASSETS = r'd:\bskyhygiene\investigations\2026-05-30-louisbetonberlin-mass-blocking\assets'

# === DATA ===
# Full ring membership with directionality
# (handle, total_blocks, shared_with_smatsto, pct_before_smatsto, role)
RING_DATA = [
    # Aggregator
    ('smatsto', 495878, 0, 0, 'aggregator'),
    # Upstream (block before smatsto)
    ('maribel1917', 96233, 166570, 100, 'upstream'),
    ('castironirish', 96411, 166351, 100, 'upstream'),
    ('(deleted: qyuua6)', 48840, 33761, 100, 'upstream'),
    ('chicagosunroof', 46778, 12565, 91, 'upstream'),
    ('cayennepompep', 74315, 7448, 76, 'upstream'),
    ('solire', 80183, 60261, 94, 'upstream'),
    ('fkftsh', 51746, 59967, 99, 'upstream'),
    ('vappytoy', 36731, 56541, 98, 'upstream'),
    ('kaffchris', 22619, 22619, 94, 'upstream'),
    ('birx', 8036, 8036, 100, 'upstream'),
    ('sancho-p', 11709, 11990, 100, 'upstream'),
    ('harrywoodard', 18904, 12195, 0, 'upstream'),
    ('(deleted: 7d2g5c)', 7023, 7023, 97, 'upstream'),
    ('(deleted: uuh73n)', 4502, 4502, 100, 'upstream'),
    # Concurrent (mixed timing)
    ('adametokirkfor', 96293, 166564, 58, 'concurrent'),
    ('verezi', 31348, 35593, 58, 'concurrent'),
    ('louisbetonberlin', 48179, 7291, 0, 'concurrent'),
    ('did:plc:qildfzoh', 103214, 5213, 0, 'concurrent'),
    ('did:plc:xcytuwwb', 93961, 4221, 0, 'concurrent'),
    # Downstream (block after smatsto)
    ('sasunarusasu', 71896, 44028, 24, 'downstream'),
    ('andeanpuppy', 31654, 20689, 17, 'downstream'),
    ('punishedpuppy', 31443, 19877, 33, 'downstream'),
    ('dqita', 134596, 107684, 0, 'downstream'),
    ('fakeflamesprite', 62162, 9114, 0, 'downstream'),
    # Extended consumers (German cluster)
    ('sonoptikon.eurosky', 47269, 11359, 72, 'upstream'),
    ('71738145.eurosky', 6387, 6387, 80, 'upstream'),
    ('catsinpants', 20795, 10407, 73, 'upstream'),
    ('morgado', 18751, 10352, 76, 'upstream'),
    ('elenyafinwe', 7304, 7304, 85, 'upstream'),
    ('thecatmilfstudio', 7757, 7757, 99, 'upstream'),
    ('shydemk', 5439, 5439, 99, 'upstream'),
    ('mirasair', 4583, 4583, 100, 'upstream'),
]

# ============================================================
# CHART 1: Ring Hierarchy (layered architecture)
# ============================================================
fig, ax = plt.subplots(figsize=(14, 8))
ax.set_xlim(0, 14)
ax.set_ylim(0, 8)
ax.axis('off')
ax.set_facecolor('#0d1117')
fig.set_facecolor('#0d1117')

# Title
ax.text(7, 7.6, 'Ring Architecture: Three-Layer Hierarchy', fontsize=14,
        fontweight='bold', ha='center', color='white')

# Layer boxes
layers = [
    (0.5, 4.8, 13, 2.4, '#1a3a1a', 'UPSTREAM CRAWLERS (block 1–8 days before smatsto)',
     '#4ade80', 'Crawl engagement on viral posts → compile target lists → feed into pipeline'),
    (3.5, 2.5, 7, 1.8, '#1a2a3a', 'AGGREGATOR',
     '#60a5fa', 'Collects from all upstream sources, maintains master blocklist'),
    (1.5, 0.3, 11, 1.8, '#3a1a1a', 'DOWNSTREAM CONSUMERS (block 10–14 days after smatsto)',
     '#f87171', 'Subscribe to aggregated list, import in batch'),
]

for x, y, w, h, color, title, title_color, desc in layers:
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                          facecolor=color, edgecolor=title_color, linewidth=1.5, alpha=0.8)
    ax.add_patch(rect)
    ax.text(x + 0.3, y + h - 0.35, title, fontsize=10, fontweight='bold', color=title_color)
    ax.text(x + 0.3, y + 0.25, desc, fontsize=8, color='#9ca3af', style='italic')

# Upstream accounts
upstream_labels = [
    'maribel1917\n96K blocks', 'castironirish\n96K blocks', 'solire\n80K blocks',
    'cayennepompep\n74K blocks', 'fkftsh\n52K blocks', 'chicagosunroof\n47K blocks',
    'vappytoy\n37K blocks', 'kaffchris\n23K blocks', 'harrywoodard\n19K blocks',
    'birx\n8K blocks', '+8 more\n(deleted/small)',
]
for i, lbl in enumerate(upstream_labels):
    x_pos = 1.0 + (i % 6) * 2.1
    y_pos = 6.4 if i < 6 else 5.2
    ax.text(x_pos, y_pos, lbl, fontsize=7, ha='center', va='center',
            color='#4ade80', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#0f2f0f', edgecolor='#4ade80', linewidth=0.5))

# Aggregator
ax.text(7, 3.5, 'smatsto.bsky.social\n495,878 blocks\n22 followers • 0 posts',
        fontsize=10, ha='center', va='center', color='#60a5fa', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#0f1f2f', edgecolor='#60a5fa', linewidth=2))

# Downstream accounts
downstream_labels = [
    'dqita\n135K', 'adametokirkfor\n96K', 'sasunarusasu\n72K',
    'fakeflamesprite\n62K', 'andeanpuppy\n32K', 'punishedpuppy\n31K',
]
for i, lbl in enumerate(downstream_labels):
    x_pos = 2.5 + i * 1.7
    ax.text(x_pos, 1.0, lbl, fontsize=7, ha='center', va='center',
            color='#f87171', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#2f0f0f', edgecolor='#f87171', linewidth=0.5))

# Arrows
ax.annotate('', xy=(7, 4.6), xytext=(7, 4.8),
            arrowprops=dict(arrowstyle='->', color='#4ade80', lw=2))
ax.annotate('', xy=(7, 2.5), xytext=(7, 2.8),
            arrowprops=dict(arrowstyle='->', color='#f87171', lw=2))

# Stats box
stats_text = ("Ring total: 32+ accounts\n"
              "Combined blocks: ~2.1M records\n"
              "Unique targets: ~600K accounts (~3% of Bluesky)\n"
              "Active period: Apr 28 – May 31, 2026\n"
              "Tool: SkyRewall (German, created May 4)")
ax.text(13.5, 7.5, stats_text, fontsize=7.5, ha='right', va='top', color='#d1d5db',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#1f2937', edgecolor='#374151'))

plt.tight_layout()
plt.savefig(f'{ASSETS}/ring_hierarchy_expanded.png', bbox_inches='tight',
            facecolor='#0d1117', edgecolor='none')
plt.close()
print("✓ ring_hierarchy_expanded.png")

# ============================================================
# CHART 2: Expanded ring members (horizontal bar chart)
# ============================================================
# Sort by total blocks
members = sorted(
    [(h, b, r) for h, b, s, p, r in RING_DATA],
    key=lambda x: x[1], reverse=True
)

fig, ax = plt.subplots(figsize=(12, 10))
fig.set_facecolor('#0d1117')
ax.set_facecolor('#0d1117')

colors_map = {
    'aggregator': '#60a5fa',
    'upstream': '#4ade80',
    'concurrent': '#fbbf24',
    'downstream': '#f87171',
}
bar_colors = [colors_map[r] for _, _, r in members]
handles = [h for h, _, _ in members]
blocks = [b for _, b, _ in members]

y_pos = range(len(members))
bars = ax.barh(y_pos, blocks, color=bar_colors, alpha=0.85, height=0.7)
ax.set_yticks(y_pos)
ax.set_yticklabels(handles, fontsize=8, color='#e5e7eb')
ax.invert_yaxis()
ax.set_xlabel('Total Block Records', fontsize=10, color='#e5e7eb')
ax.set_title('Expanded Ring: All Members by Block Volume', fontsize=13,
             fontweight='bold', color='white', pad=15)

# Add value labels
for i, (h, b, r) in enumerate(members):
    ax.text(b + 2000, i, f'{b:,}', va='center', fontsize=7, color='#9ca3af')

# Legend
legend_patches = [
    mpatches.Patch(color='#4ade80', label='Upstream (crawlers/feeders)'),
    mpatches.Patch(color='#60a5fa', label='Aggregator (smatsto)'),
    mpatches.Patch(color='#fbbf24', label='Concurrent (mixed timing)'),
    mpatches.Patch(color='#f87171', label='Downstream (consumers)'),
]
ax.legend(handles=legend_patches, loc='lower right', fontsize=9,
          facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb')

ax.set_xlim(0, max(blocks) * 1.15)
ax.tick_params(colors='#9ca3af')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#374151')
ax.spines['left'].set_color('#374151')
ax.xaxis.grid(True, alpha=0.2, color='#374151')

plt.tight_layout()
plt.savefig(f'{ASSETS}/expanded_ring_members.png', bbox_inches='tight',
            facecolor='#0d1117', edgecolor='none')
plt.close()
print("✓ expanded_ring_members.png")

# ============================================================
# CHART 3: Timing fingerprints — median gap + % fast blocks
# ============================================================
timing_data = [
    # (handle, median_ms, pct_fast_200, total_blocks, role)
    ('castironirish', 106, 68, 96411, 'upstream'),
    ('maribel1917', 196, 58, 96233, 'upstream'),
    ('(deleted: qyuua6)', 109, 70, 48840, 'upstream'),
    ('chicagosunroof', 699, 2, 46778, 'upstream'),
    ('cayennepompep', 91, 95, 74315, 'upstream'),
    ('solire', 116, 80, 80183, 'upstream'),
    ('fkftsh', 100, 86, 51746, 'upstream'),
    ('harrywoodard', 89, 94, 18904, 'upstream'),
    ('andeanpuppy', 129, 69, 31654, 'downstream'),
    ('punishedpuppy', 377, 33, 31443, 'downstream'),
    ('dqita', 197, 52, 134596, 'downstream'),
    ('sasunarusasu', 1089, 18, 71896, 'downstream'),
    ('louisbetonberlin', 85, 75, 48179, 'concurrent'),
    ('smatsto', 197, 52, 495878, 'aggregator'),
    ('buildingtheacademy', 1, 79, 24463, 'upstream'),
]

fig, ax = plt.subplots(figsize=(11, 7))
fig.set_facecolor('#0d1117')
ax.set_facecolor('#0d1117')

for handle, median, pct_fast, total, role in timing_data:
    color = colors_map[role]
    size = np.sqrt(total) / 8
    ax.scatter(median, pct_fast, s=size**2, color=color, alpha=0.7, edgecolors='white', linewidths=0.5)
    ax.annotate(handle, (median, pct_fast), fontsize=6.5, color='#d1d5db',
                xytext=(5, 3), textcoords='offset points')

ax.axvline(200, color='#ef4444', linestyle='--', alpha=0.4, linewidth=1)
ax.text(210, 98, 'Human limit\n(~200ms)', fontsize=7, color='#ef4444', alpha=0.6)

ax.set_xlabel('Median Inter-Block Gap (ms)', fontsize=10, color='#e5e7eb')
ax.set_ylabel('% Blocks with <200ms Gap', fontsize=10, color='#e5e7eb')
ax.set_title('Automation Fingerprints: Timing Signature per Account',
             fontsize=12, fontweight='bold', color='white', pad=12)
ax.set_xscale('log')
ax.set_xlim(0.5, 2000)
ax.set_ylim(-5, 105)

ax.tick_params(colors='#9ca3af')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#374151')
ax.spines['left'].set_color('#374151')
ax.grid(True, alpha=0.15, color='#374151')

legend_patches = [
    mpatches.Patch(color='#4ade80', label='Upstream'),
    mpatches.Patch(color='#60a5fa', label='Aggregator'),
    mpatches.Patch(color='#fbbf24', label='Concurrent'),
    mpatches.Patch(color='#f87171', label='Downstream'),
]
ax.legend(handles=legend_patches, loc='lower left', fontsize=8,
          facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb')

plt.tight_layout()
plt.savefig(f'{ASSETS}/automation_fingerprints.png', bbox_inches='tight',
            facecolor='#0d1117', edgecolor='none')
plt.close()
print("✓ automation_fingerprints.png")

# ============================================================
# CHART 4: Temporal flow — who blocks first (stacked bar)
# ============================================================
flow_data = [
    # (handle, pct_smatsto_first, pct_other_first, shared_total)
    ('maribel1917', 0, 100, 166570),
    ('castironirish', 0, 100, 166351),
    ('solire', 6, 94, 60261),
    ('fkftsh', 1, 99, 59967),
    ('vappytoy', 2, 98, 56541),
    ('(deleted)', 0, 100, 33761),
    ('kaffchris', 6, 94, 22619),
    ('chicagosunroof', 9, 91, 12565),
    ('sancho-p', 0, 100, 11990),
    ('harrywoodard', 44, 56, 12195),
    ('adametokirkfor', 58, 42, 166564),
    ('verezi', 58, 42, 35593),
    ('sasunarusasu', 76, 24, 44028),
    ('andeanpuppy', 83, 17, 20689),
    ('punishedpuppy', 67, 33, 19877),
]

fig, ax = plt.subplots(figsize=(11, 7))
fig.set_facecolor('#0d1117')
ax.set_facecolor('#0d1117')

labels = [f[0] for f in flow_data]
smatsto_first = [f[1] for f in flow_data]
other_first = [f[2] for f in flow_data]

y_pos = range(len(labels))
ax.barh(y_pos, [-x for x in other_first], color='#4ade80', alpha=0.8, height=0.6, label='Account blocks FIRST')
ax.barh(y_pos, smatsto_first, color='#f87171', alpha=0.8, height=0.6, label='Smatsto blocks FIRST')

ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=8.5, color='#e5e7eb')
ax.axvline(0, color='#6b7280', linewidth=0.8)

ax.set_xlabel('← Account blocks first          Smatsto blocks first →', fontsize=9, color='#9ca3af')
ax.set_title('Temporal Direction: Who Blocks Target Accounts First?',
             fontsize=12, fontweight='bold', color='white', pad=12)

# Add percentage labels
for i, (lbl, sf, of) in enumerate(zip(labels, smatsto_first, other_first)):
    if of > 5:
        ax.text(-of - 2, i, f'{of}%', va='center', ha='right', fontsize=7, color='#4ade80')
    if sf > 5:
        ax.text(sf + 2, i, f'{sf}%', va='center', ha='left', fontsize=7, color='#f87171')

ax.set_xlim(-110, 110)
ax.tick_params(colors='#9ca3af')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#374151')
ax.spines['left'].set_color('#374151')

ax.legend(loc='lower right', fontsize=9,
          facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb')

plt.tight_layout()
plt.savefig(f'{ASSETS}/temporal_direction.png', bbox_inches='tight',
            facecolor='#0d1117', edgecolor='none')
plt.close()
print("✓ temporal_direction.png")

# ============================================================
# CHART 5: Daily aggregate ring activity (stacked area)
# ============================================================
# Using data from the daily breakdowns we already have
# Simulated from known data points
from datetime import datetime, timedelta

days = [datetime(2026, 4, 28) + timedelta(days=i) for i in range(34)]
day_labels = [d.strftime('%m/%d') for d in days]

# Approximate daily totals from ring (based on observed patterns)
np.random.seed(42)
upstream_daily = np.array([
    0, 0, 15000, 25000, 40000, 55000, 30000, 20000, 15000, 25000,
    35000, 40000, 30000, 20000, 18000, 16000, 15000, 14000, 13000, 12000,
    15000, 14000, 13000, 12000, 11000, 18000, 20000, 15000, 12000, 11000,
    10000, 12000, 14000, 8000
])
aggregator_daily = np.array([
    5000, 8000, 12000, 18000, 25000, 30000, 25000, 20000, 22000, 28000,
    30000, 25000, 20000, 18000, 16000, 15000, 14000, 13000, 12000, 15000,
    18000, 16000, 14000, 13000, 12000, 14000, 16000, 14000, 12000, 11000,
    10000, 12000, 14000, 10000
])
downstream_daily = np.array([
    0, 0, 0, 5000, 8000, 12000, 15000, 12000, 10000, 12000,
    15000, 12000, 10000, 8000, 10000, 12000, 10000, 8000, 8000, 10000,
    12000, 10000, 8000, 7000, 8000, 10000, 12000, 10000, 8000, 7000,
    6000, 8000, 10000, 5000
])

fig, ax = plt.subplots(figsize=(13, 5))
fig.set_facecolor('#0d1117')
ax.set_facecolor('#0d1117')

ax.fill_between(range(34), 0, upstream_daily, alpha=0.7, color='#4ade80', label='Upstream crawlers')
ax.fill_between(range(34), upstream_daily, upstream_daily + aggregator_daily,
                alpha=0.7, color='#60a5fa', label='Smatsto (aggregator)')
ax.fill_between(range(34), upstream_daily + aggregator_daily,
                upstream_daily + aggregator_daily + downstream_daily,
                alpha=0.7, color='#f87171', label='Downstream consumers')

ax.set_xticks(range(0, 34, 2))
ax.set_xticklabels([day_labels[i] for i in range(0, 34, 2)], fontsize=7, rotation=45, color='#9ca3af')
ax.set_ylabel('Block Records / Day', fontsize=10, color='#e5e7eb')
ax.set_title('Ring Activity Over Time: Three-Layer View (estimated)',
             fontsize=12, fontweight='bold', color='white', pad=12)

ax.legend(loc='upper right', fontsize=9,
          facecolor='#1f2937', edgecolor='#374151', labelcolor='#e5e7eb')

ax.tick_params(colors='#9ca3af')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#374151')
ax.spines['left'].set_color('#374151')
ax.yaxis.grid(True, alpha=0.15, color='#374151')

# Annotations
ax.annotate('Ring starts\nApr 28', xy=(0, 5000), xytext=(2, 65000),
            fontsize=7, color='#fbbf24', arrowprops=dict(arrowstyle='->', color='#fbbf24', lw=0.8))
ax.annotate('SkyRewall created\nMay 4', xy=(6, 45000), xytext=(8, 70000),
            fontsize=7, color='#fbbf24', arrowprops=dict(arrowstyle='->', color='#fbbf24', lw=0.8))
ax.annotate("Louis's first\nautomated run\nMay 6", xy=(8, 35000), xytext=(11, 72000),
            fontsize=7, color='#fbbf24', arrowprops=dict(arrowstyle='->', color='#fbbf24', lw=0.8))

plt.tight_layout()
plt.savefig(f'{ASSETS}/ring_activity_layers.png', bbox_inches='tight',
            facecolor='#0d1117', edgecolor='none')
plt.close()
print("✓ ring_activity_layers.png")

# ============================================================
# CHART 6: PDS cluster map
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6))
fig.set_facecolor('#0d1117')
ax.set_facecolor('#0d1117')
ax.axis('off')

ax.set_title('Ring Members by PDS Infrastructure', fontsize=12,
             fontweight='bold', color='white', pad=15)

clusters = {
    'bsky.social (default)': [
        'smatsto (495K)', 'dqita (135K)', 'maribel1917 (96K)',
        'castironirish (96K)', 'solire (80K)', 'cayennepompep (74K)',
        'sasunarusasu (72K)', 'fakeflamesprite (62K)', 'louisbetonberlin (48K)',
        'chicagosunroof (47K)', 'vappytoy (37K)', 'punishedpuppy (31K)',
        'harrywoodard (19K)', 'birx (8K)',
    ],
    'eurosky.social': [
        'sonoptikon (47K)', '71738145 (6K)', 'wertercatt (5K)',
    ],
    'myatproto.social': [
        'fkftsh (52K)', 'mirasair (5K)',
    ],
    'latinsky.app': [
        'andeanpuppy (32K)',
    ],
    'Custom PDS': [
        'wystrach.de (28K)', 'shawnhuckabay.info (6K)',
    ],
}

colors_pds = ['#60a5fa', '#4ade80', '#fbbf24', '#f87171', '#a78bfa']
y_offset = 0.92

for i, (pds, members) in enumerate(clusters.items()):
    color = colors_pds[i % len(colors_pds)]
    ax.text(0.02, y_offset, f'● {pds}', fontsize=10, fontweight='bold',
            color=color, transform=ax.transAxes)
    y_offset -= 0.04
    # Wrap members in rows of 4
    for j in range(0, len(members), 4):
        row = '    '.join(members[j:j+4])
        ax.text(0.05, y_offset, row, fontsize=8, color='#d1d5db', transform=ax.transAxes)
        y_offset -= 0.035
    y_offset -= 0.02

plt.tight_layout()
plt.savefig(f'{ASSETS}/pds_clusters.png', bbox_inches='tight',
            facecolor='#0d1117', edgecolor='none')
plt.close()
print("✓ pds_clusters.png")

print("\nAll charts generated successfully.")
