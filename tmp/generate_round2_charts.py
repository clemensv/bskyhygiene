"""Generate updated charts for the German literary bot cluster (Round 2)."""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.use("Agg")
plt.style.use("seaborn-v0_8-darkgrid")

OUT = Path(r"d:\bskyhygiene\investigations\2026-05-30-german-literary-bots\assets")

# ─── Chart 1: Co-follow targets (updated numbers) ───────────────────────────

targets = [
    ("schreibersnaturarium.de", 72),
    ("colettemschmidt", 72),
    ("bsky.app", 66),
    ("wernerkogler", 58),
    ("datgestruepp", 52),
    ("jungeakademie", 52),
    ("purrtah", 51),
    ("musermeku", 45),
    ("kunstderfuge", 42),
    ("kunstjonas", 42),
    ("elsschot", 39),
]

fig, ax = plt.subplots(figsize=(10, 6))
names = [t[0] for t in targets]
counts = [t[1] for t in targets]
colors = ["#c0392b" if c >= 70 else "#e67e22" if c >= 50 else "#2980b9" for c in counts]
bars = ax.barh(range(len(names)), counts, color=colors)
ax.set_yticks(range(len(names)))
ax.set_yticklabels([f"@{n}" for n in names], fontsize=10)
ax.set_xlabel("Anzahl Bots die diesem Account folgen", fontsize=11)
ax.set_title("Co-Follow-Ziele des Bot-Clusters (n=72 Bots)", fontsize=13, fontweight="bold")
ax.axvline(x=72, color="red", linestyle="--", alpha=0.5, label="Cluster-Größe (72)")
ax.legend(loc="lower right")
for bar, count in zip(bars, counts):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, 
            str(count), va="center", fontsize=9)
ax.invert_yaxis()
plt.tight_layout()
plt.savefig(OUT / "cofollow_targets.png", dpi=150)
plt.close()
print("✓ cofollow_targets.png")

# ─── Chart 2: Follow distribution (updated) ─────────────────────────────────

follow_dist = {3: 6, 5: 1, 6: 3, 7: 1, 8: 1, 9: 2, 10: 3, 11: 29, 12: 7, 
               13: 5, 14: 2, 15: 3, 16: 1, 17: 1, 18: 5, 19: 1, 20: 1}

fig, ax = plt.subplots(figsize=(10, 5))
x = sorted(follow_dist.keys())
y = [follow_dist[k] for k in x]
colors = ["#c0392b" if k == 11 else "#3498db" for k in x]
bars = ax.bar(x, y, color=colors, edgecolor="white", linewidth=0.5)
ax.set_xlabel("Follows pro Bot-Account", fontsize=11)
ax.set_ylabel("Anzahl Accounts", fontsize=11)
ax.set_title("Verteilung: Follows pro Bot (n=72)", fontsize=13, fontweight="bold")
ax.set_xticks(x)
ax.annotate("Modus: exakt 11\n(40% aller Bots)", xy=(11, 29), xytext=(14, 25),
            fontsize=10, fontweight="bold", color="#c0392b",
            arrowprops=dict(arrowstyle="->", color="#c0392b"))
for bar, val in zip(bars, y):
    if val > 1:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, 
                str(val), ha="center", fontsize=8)
plt.tight_layout()
plt.savefig(OUT / "follow_distribution.png", dpi=150)
plt.close()
print("✓ follow_distribution.png")

# ─── Chart 3: Timing / burst analysis ───────────────────────────────────────

timing_path = OUT / "timing_data.json"
with open(timing_path) as f:
    timing_data = json.load(f)

durations = [r["duration_sec"] for r in timing_data]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Left: histogram of durations (log scale x)
bins = [0, 1, 10, 60, 300, 3600, 86400, max(durations)+1]
labels = ["<1s", "1-10s", "10s-1m", "1-5m", "5m-1h", "1h-1d", ">1d"]
hist_vals = []
for i in range(len(bins)-1):
    hist_vals.append(sum(1 for d in durations if bins[i] <= d < bins[i+1]))

colors_hist = ["#27ae60", "#27ae60", "#2ecc71", "#f39c12", "#e67e22", "#e74c3c", "#c0392b"]
ax1.bar(range(len(labels)), hist_vals, color=colors_hist, edgecolor="white")
ax1.set_xticks(range(len(labels)))
ax1.set_xticklabels(labels, fontsize=9)
ax1.set_xlabel("Burst-Dauer (first→last follow)", fontsize=10)
ax1.set_ylabel("Anzahl Bots", fontsize=10)
ax1.set_title("Follow-Burst-Dauer pro Bot", fontsize=12, fontweight="bold")
for i, v in enumerate(hist_vals):
    if v > 0:
        ax1.text(i, v + 0.3, str(v), ha="center", fontsize=9)

# Right: CDF
sorted_d = sorted(durations)
cdf_y = np.arange(1, len(sorted_d)+1) / len(sorted_d)
ax2.plot(sorted_d, cdf_y, color="#2980b9", linewidth=2)
ax2.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
ax2.axvline(x=128, color="#c0392b", linestyle="--", alpha=0.7, label="Median (128s)")
ax2.set_xscale("log")
ax2.set_xlabel("Dauer in Sekunden (log)", fontsize=10)
ax2.set_ylabel("Kumulative Verteilung", fontsize=10)
ax2.set_title("CDF: Burst-Dauer", fontsize=12, fontweight="bold")
ax2.legend(loc="lower right")

plt.tight_layout()
plt.savefig(OUT / "follow_cadence.png", dpi=150)
plt.close()
print("✓ follow_cadence.png")

# ─── Chart 4: Daily activity timeline ───────────────────────────────────────

from datetime import datetime

first_follows = [r["first_ts"] for r in timing_data]
dates = []
for ts in first_follows:
    try:
        dt = datetime.fromisoformat(ts.replace("+00:00", "").replace("Z", ""))
        dates.append(dt.date())
    except:
        pass

from collections import Counter
date_counts = Counter(dates)
all_dates = sorted(date_counts.keys())

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar([d.isoformat() for d in all_dates], [date_counts[d] for d in all_dates], 
       color="#3498db", edgecolor="white")
ax.set_xlabel("Datum (UTC)", fontsize=10)
ax.set_ylabel("Neue Bots aktiviert", fontsize=10)
ax.set_title("Tägliche Bot-Aktivierung (n=72)", fontsize=12, fontweight="bold")
plt.xticks(rotation=45, ha="right", fontsize=8)
plt.tight_layout()
plt.savefig(OUT / "daily_activity.png", dpi=150)
plt.close()
print("✓ daily_activity.png")

# ─── Chart 5: Bot profile characteristics ───────────────────────────────────

fig, ax = plt.subplots(figsize=(8, 5))
cats = ["Avatar", "Display-Name", "Bio/Beschreibung", "Posts > 0", "Suspendiert"]
vals = [58, 22, 12, 19, 0]
total = 66
pcts = [v/total*100 for v in vals]
colors_bar = ["#27ae60", "#f39c12", "#e67e22", "#9b59b6", "#2ecc71"]
bars = ax.barh(cats, pcts, color=colors_bar)
ax.set_xlabel("Prozent der Bots (%)", fontsize=10)
ax.set_title("Bot-Profil-Ausstattung (n=66 aufgelöst)", fontsize=12, fontweight="bold")
for bar, val, pct in zip(bars, vals, pcts):
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
            f"{val}/66 ({pct:.0f}%)", va="center", fontsize=9)
ax.set_xlim(0, 110)
ax.invert_yaxis()
plt.tight_layout()
plt.savefig(OUT / "bot_profiles.png", dpi=150)
plt.close()
print("✓ bot_profiles.png")

print("\nAll charts generated.")
