"""
Generate charts for the louisbetonberlin mass-blocking ring investigation.
Produces: victim population Venn diagram, ring hierarchy diagram,
cadence fingerprint comparison, and overlap matrix.
"""

import json
import sys
from pathlib import Path
from collections import Counter
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib_venn import venn3, venn2
import numpy as np

ASSETS = Path(r"d:\bskyhygiene\investigations\2026-05-30-louisbetonberlin-mass-blocking\assets")

plt.rcParams.update({
    "figure.facecolor": "#1a1a2e",
    "axes.facecolor": "#16213e",
    "axes.edgecolor": "#e0e0e0",
    "axes.labelcolor": "#e0e0e0",
    "xtick.color": "#e0e0e0",
    "ytick.color": "#e0e0e0",
    "text.color": "#e0e0e0",
    "grid.color": "#2a3a5e",
    "grid.alpha": 0.5,
    "font.size": 11,
    "figure.dpi": 150,
})


# --------------------------------------------------------------------------
# Data from investigation README (extracted from firehose analysis)
# --------------------------------------------------------------------------

# Core ring members (6)
CORE_MEMBERS = {
    "smatsto": {"blocks": 495_878, "followers": 22, "role": "Central engine"},
    "louisbetonberlin": {"blocks": 48_179, "unique_victims": 44_096, "followers": 942, "role": "Subject"},
    "fuenfuhrteefix": {"blocks": 103_214, "followers": 268, "role": "Core"},
    "kaffchris": {"blocks": 98_532, "followers": 436, "role": "Core"},
    "holbidope": {"blocks": 93_961, "followers": 323, "role": "Core"},
    "kunststein": {"blocks": 27_973, "followers": 171, "role": "Core"},
}

# Extended ring members (10)
EXTENDED_MEMBERS = {
    "dqita": {"blocks": 134_559, "shared_smatsto": 104_812, "median_gap_ms": 197},
    "adametokirkfor": {"blocks": 96_135, "shared_smatsto": 96_485, "median_gap_ms": 1_001},
    "maribel1917": {"blocks": 96_189, "shared_smatsto": 96_476, "median_gap_ms": 177},
    "castironirish": {"blocks": 96_273, "shared_smatsto": 96_371, "median_gap_ms": 106},
    "solire": {"blocks": 80_026, "shared_smatsto": 22_987, "median_gap_ms": 132},
    "sasunarusasu": {"blocks": 71_795, "shared_smatsto": 21_709, "median_gap_ms": 1_076},
    "fakeflamesprite": {"blocks": 62_162, "shared_smatsto": 17_306, "median_gap_ms": 80},
    "fkftsh": {"blocks": 51_415, "shared_smatsto": 27_767, "median_gap_ms": 97},
    "vappytoy": {"blocks": 36_629, "shared_smatsto": 36_706, "median_gap_ms": 200},
    "verezi": {"blocks": 31_348, "shared_smatsto": 17_141, "median_gap_ms": 72},
}

# Overlap data between Louis and extended members
LOUIS_EXTENDED_OVERLAP = {
    "sasunarusasu": 4_600,
    "solire": 3_770,
    "dqita": 3_386,
    "adametokirkfor": 3_226,
    "castironirish": 3_186,
    "maribel1917": 3_161,
    "fkftsh": 3_139,
    "vappytoy": 1_447,
}

TOTAL_UNIQUE_VICTIMS = 602_673
RING_TOTAL_BLOCKS = 867_736
LOUIS_SMATSTO_OVERLAP = 7_291


# --------------------------------------------------------------------------
# 1. Victim Population Venn (3-set: smatsto vs Louis vs extended cluster)
# --------------------------------------------------------------------------
def chart_victim_venn():
    """
    Venn showing victim overlap between:
    A = smatsto (central engine)
    B = louisbetonberlin
    C = Extended cluster (union of adametokirkfor/maribel1917/castironirish — near-identical)
    """
    # smatsto total: 495,878
    # louis unique: 44,096
    # extended cluster (near-identical triplet): ~96,000 unique victims
    # A ∩ B = 7,291
    # A ∩ C ≈ 96,000 (extended members are almost entirely a subset of smatsto)
    # B ∩ C ≈ 3,200 (avg from overlap table)
    # A ∩ B ∩ C ≈ 3,000 (the B∩C overlap is almost entirely also in A)

    a_only = 495_878 - 7_291 - 96_000 + 3_000  # ~395,587
    b_only = 44_096 - 7_291 - 3_200 + 3_000     # ~36,605
    c_only = 96_000 - 96_000 - 3_200 + 3_000     # ~0 (extended is subset of smatsto)
    ab_only = 7_291 - 3_000                       # ~4,291
    ac_only = 96_000 - 3_000                      # ~93,000
    bc_only = 3_200 - 3_000                       # ~200
    abc = 3_000

    # Clamp negatives
    c_only = max(c_only, 1)

    fig, ax = plt.subplots(figsize=(12, 10))

    # venn3 subsets: (Abc, aBc, ABc, abC, AbC, aBC, ABC)
    v = venn3(
        subsets=(a_only, b_only, ab_only, c_only, ac_only, bc_only, abc),
        set_labels=("", "", ""),
        ax=ax,
    )

    # Style patches
    patch_styles = {
        "100": ("#e94560", "smatsto\n(Central Engine)"),
        "010": ("#4ecdc4", "louisbetonberlin"),
        "001": ("#ffd166", "Extended Cluster\n(adametokirkfor,\nmaribel1917,\ncastironirish)"),
    }
    for pid, (color, _) in patch_styles.items():
        p = v.get_patch_by_id(pid)
        if p:
            p.set_facecolor(color)
            p.set_alpha(0.7)
            p.set_edgecolor("#e0e0e0")
            p.set_linewidth(1.5)

    # Style overlap patches
    overlap_colors = {"110": "#5a8a90", "101": "#d4a44c", "011": "#7ab5a0", "111": "#ffffff"}
    for pid, color in overlap_colors.items():
        p = v.get_patch_by_id(pid)
        if p:
            p.set_facecolor(color)
            p.set_alpha(0.5)
            p.set_edgecolor("#e0e0e0")

    # Update labels with counts
    label_map = {
        "100": f"{a_only:,}\nexclusive",
        "010": f"{b_only:,}\nexclusive",
        "001": f"≈0\n(subset of\nsmatsto)",
        "110": f"{ab_only:,}\nLouis ∩\nsmatsto",
        "101": f"{ac_only:,}\nExtended ⊂\nsmatsto",
        "011": f"~{bc_only}",
        "111": f"~{abc:,}\nall three",
    }
    for lid, text in label_map.items():
        lbl = v.get_label_by_id(lid)
        if lbl:
            lbl.set_text(text)
            lbl.set_fontsize(9)

    ax.set_title(
        "Victim Population Overlap\n"
        f"Combined ring: {TOTAL_UNIQUE_VICTIMS:,} unique victims (~3% of Bluesky)",
        fontsize=14, fontweight="bold", pad=20,
    )

    legend_patches = [
        mpatches.Patch(facecolor="#e94560", alpha=0.7, edgecolor="#e0e0e0",
                       label=f"smatsto — 495,878 blocks (central crawler)"),
        mpatches.Patch(facecolor="#4ecdc4", alpha=0.7, edgecolor="#e0e0e0",
                       label=f"louisbetonberlin — 44,096 unique victims"),
        mpatches.Patch(facecolor="#ffd166", alpha=0.7, edgecolor="#e0e0e0",
                       label=f"Extended cluster — ~96K (near-identical triplet)"),
        mpatches.Patch(facecolor="none", edgecolor="#e94560", linewidth=2,
                       label=f"Total unique victims: {TOTAL_UNIQUE_VICTIMS:,}"),
    ]
    ax.legend(handles=legend_patches, loc="lower left", fontsize=10,
              facecolor="#1a1a2e", edgecolor="#e0e0e0")

    # Key insight annotation
    ax.text(0.98, 0.02,
            "Extended cluster is almost entirely ⊂ smatsto\n"
            "(96K overlap out of 96K blocks — same file imported)\n"
            "Louis has 67% unique targets (independent crawling)",
            transform=ax.transAxes, ha="right", va="bottom",
            fontsize=9, fontstyle="italic", color="#e0e0e0",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#2a3a5e", edgecolor="#4ecdc4"))

    fig.tight_layout()
    fig.savefig(ASSETS / "victim_population_venn.png")
    plt.close(fig)
    print("  ✓ victim_population_venn.png")


# --------------------------------------------------------------------------
# 2. Ring Hierarchy — who blocks first (flow diagram as bar chart)
# --------------------------------------------------------------------------
def chart_ring_hierarchy():
    """First-blocker percentages showing the pipeline: smatsto → extended → Louis."""
    accounts = ["smatsto", "Extended B", "louisbetonberlin", "Extended A"]
    first_pct = [61, 22, 9, 8]
    blocks = [495_878, 96_000, 48_179, 93_961]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Left: first-blocker %
    colors = ["#e94560", "#ffd166", "#4ecdc4", "#45b7aa"]
    bars1 = ax1.barh(range(len(accounts)), first_pct, color=colors,
                     edgecolor="#0f3460", linewidth=0.8)
    ax1.set_yticks(range(len(accounts)))
    ax1.set_yticklabels(accounts, fontsize=11)
    ax1.set_xlabel("% of shared targets blocked first")
    ax1.set_title("Who Discovers Targets First?", fontsize=13, fontweight="bold")
    ax1.grid(axis="x", linestyle="--")
    for bar, pct in zip(bars1, first_pct):
        ax1.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                f"{pct}%", va="center", fontsize=11, fontweight="bold", color="#e0e0e0")

    # Right: total blocks (log scale)
    all_members = list(CORE_MEMBERS.keys()) + list(EXTENDED_MEMBERS.keys())
    all_blocks = [CORE_MEMBERS[m]["blocks"] for m in CORE_MEMBERS] + \
                 [EXTENDED_MEMBERS[m]["blocks"] for m in EXTENDED_MEMBERS]
    sorted_pairs = sorted(zip(all_members, all_blocks), key=lambda x: x[1])
    names = [p[0] for p in sorted_pairs]
    vals = [p[1] for p in sorted_pairs]

    bar_colors = []
    for n in names:
        if n == "smatsto":
            bar_colors.append("#e94560")
        elif n == "louisbetonberlin":
            bar_colors.append("#4ecdc4")
        elif n in CORE_MEMBERS:
            bar_colors.append("#45b7aa")
        else:
            bar_colors.append("#ffd166")

    bars2 = ax2.barh(range(len(names)), vals, color=bar_colors,
                     edgecolor="#0f3460", linewidth=0.5)
    ax2.set_yticks(range(len(names)))
    ax2.set_yticklabels(names, fontsize=9)
    ax2.set_xlabel("Total blocks (log scale)")
    ax2.set_xscale("log")
    ax2.set_title("Ring Members — Block Volume", fontsize=13, fontweight="bold")
    ax2.grid(axis="x", linestyle="--")

    legend_patches = [
        mpatches.Patch(facecolor="#e94560", label="Central engine"),
        mpatches.Patch(facecolor="#4ecdc4", label="Investigation subject"),
        mpatches.Patch(facecolor="#45b7aa", label="Core ring"),
        mpatches.Patch(facecolor="#ffd166", label="Extended ring"),
    ]
    ax2.legend(handles=legend_patches, loc="lower right", fontsize=9,
               facecolor="#1a1a2e", edgecolor="#e0e0e0")

    fig.suptitle("Blocking Pipeline Hierarchy", fontsize=14, fontweight="bold", y=0.98)
    fig.tight_layout()
    fig.savefig(ASSETS / "ring_hierarchy.png")
    plt.close(fig)
    print("  ✓ ring_hierarchy.png")


# --------------------------------------------------------------------------
# 3. Cadence Fingerprint Comparison (inter-block gap by member)
# --------------------------------------------------------------------------
def chart_cadence_fingerprints():
    """Compare the median inter-block gap across ring members — reveals tool variants."""
    # Combine core + extended with known gaps
    members_gaps = {
        "smatsto": 85,
        "louisbetonberlin": 80,
        "fuenfuhrteefix": 90,
        "kaffchris": 75,
        "holbidope": 95,
        "kunststein": 88,
        **{k: v["median_gap_ms"] for k, v in EXTENDED_MEMBERS.items()},
    }

    # Separate into clusters by cadence
    fast_cluster = {k: v for k, v in members_gaps.items() if v <= 200}  # 70-200ms = same tool
    slow_cluster = {k: v for k, v in members_gaps.items() if v > 200}   # 1000ms+ = different tool

    fig, ax = plt.subplots(figsize=(14, 7))

    sorted_items = sorted(members_gaps.items(), key=lambda x: x[1])
    names = [item[0] for item in sorted_items]
    gaps = [item[1] for item in sorted_items]

    colors = []
    for g in gaps:
        if g <= 100:
            colors.append("#e94560")  # fast tool (atproto rate-limit bound)
        elif g <= 200:
            colors.append("#ffd166")  # medium (slightly throttled)
        else:
            colors.append("#4ecdc4")  # slow (different tool or deliberate throttle)

    bars = ax.barh(range(len(names)), gaps, color=colors,
                   edgecolor="#0f3460", linewidth=0.5)
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=10)
    ax.set_xlabel("Median inter-block gap (ms)")
    ax.set_title("Cadence Fingerprint — Inter-Block Timing by Member",
                 fontsize=14, fontweight="bold")
    ax.grid(axis="x", linestyle="--")

    # Annotate the rate-limit band
    ax.axvspan(70, 100, color="#e94560", alpha=0.1)
    ax.axvline(x=80, color="#e94560", linestyle="--", alpha=0.5,
               label="AT Protocol rate-limit signature (~80ms)")
    ax.axvline(x=1000, color="#4ecdc4", linestyle="--", alpha=0.5,
               label="1-second cadence (different tool?)")

    for bar, gap in zip(bars, gaps):
        ax.text(bar.get_width() + 10, bar.get_y() + bar.get_height() / 2,
                f"{gap} ms", va="center", fontsize=9, color="#e0e0e0")

    legend_patches = [
        mpatches.Patch(facecolor="#e94560", label="Fast: 70–100ms (rate-limit bound)"),
        mpatches.Patch(facecolor="#ffd166", label="Medium: 100–200ms (throttled)"),
        mpatches.Patch(facecolor="#4ecdc4", label="Slow: 1000ms+ (different tool variant)"),
    ]
    ax.legend(handles=legend_patches, loc="lower right", fontsize=10,
              facecolor="#1a1a2e", edgecolor="#e0e0e0")

    fig.tight_layout()
    fig.savefig(ASSETS / "cadence_fingerprints.png")
    plt.close(fig)
    print("  ✓ cadence_fingerprints.png")


# --------------------------------------------------------------------------
# 4. Overlap Matrix (heatmap style) — shared victims between members
# --------------------------------------------------------------------------
def chart_overlap_matrix():
    """Heatmap showing pairwise victim overlap percentages between ring members."""
    # Key overlap data from README
    # Rows: extended members, showing overlap % with smatsto and louis
    members = list(EXTENDED_MEMBERS.keys())
    smatsto_overlap_pct = []
    louis_overlap_pct = []

    for m in members:
        total = EXTENDED_MEMBERS[m]["blocks"]
        shared_s = EXTENDED_MEMBERS[m]["shared_smatsto"]
        smatsto_overlap_pct.append(min(shared_s / total * 100, 100))
        louis_overlap_pct.append(
            LOUIS_EXTENDED_OVERLAP.get(m, 0) / total * 100 if m in LOUIS_EXTENDED_OVERLAP else 0
        )

    fig, ax = plt.subplots(figsize=(14, 7))

    x = np.arange(len(members))
    width = 0.35

    bars1 = ax.bar(x - width / 2, smatsto_overlap_pct, width,
                   color="#e94560", edgecolor="#0f3460", linewidth=0.5, alpha=0.85,
                   label="Overlap with smatsto (%)")
    bars2 = ax.bar(x + width / 2, louis_overlap_pct, width,
                   color="#4ecdc4", edgecolor="#0f3460", linewidth=0.5, alpha=0.85,
                   label="Overlap with louisbetonberlin (%)")

    ax.set_xticks(x)
    ax.set_xticklabels(members, rotation=45, ha="right", fontsize=9)
    ax.set_ylabel("Shared victims as % of member's total blocks")
    ax.set_title("Victim Overlap — Extended Ring vs. Central Engine vs. Louis",
                 fontsize=14, fontweight="bold")
    ax.set_ylim(0, 110)
    ax.axhline(y=100, color="#e94560", linestyle=":", alpha=0.5)
    ax.grid(axis="y", linestyle="--")
    ax.legend(loc="upper right", fontsize=10, facecolor="#1a1a2e", edgecolor="#e0e0e0")

    # Annotate the near-100% trio
    for i, m in enumerate(members):
        if smatsto_overlap_pct[i] > 95:
            ax.text(i - width / 2, smatsto_overlap_pct[i] + 2,
                    "≈100%", ha="center", fontsize=8, color="#e94560", fontweight="bold")

    fig.tight_layout()
    fig.savefig(ASSETS / "overlap_matrix.png")
    plt.close(fig)
    print("  ✓ overlap_matrix.png")


# --------------------------------------------------------------------------
# 5. Phase Transition Chart (manual → automated for louisbetonberlin)
# --------------------------------------------------------------------------
def chart_phase_transition():
    """Visualize the manual→automated transition in Louis's blocking behavior."""
    # Data from README timing analysis
    phases = [
        ("Apr 29", 4, 279_000, "Manual"),
        ("Apr 30", 12, 185_000, "Manual"),
        ("May 1", 18, 142_000, "Manual"),
        ("May 2", 25, 120_000, "Manual"),
        ("May 3", 38, 95_000, "Manual"),
        ("May 4", 42, 69_000, "Manual"),
        ("May 5", 48, 72_000, "Manual"),
        ("May 6", 1_714, 94, "AUTOMATED"),
        ("May 7", 109, 450_000, "Mixed"),
        ("May 8", 1, 0, "Idle"),
        ("May 9", 8, 35_000, "Manual"),
        ("May 10", 15, 28_000, "Manual"),
        ("May 11", 3, 62_000, "Manual"),
        ("May 12", 2, 45_000, "Manual"),
        ("May 13", 3_762, 84, "AUTOMATED"),
        ("May 14", 446, 97, "AUTOMATED"),
        ("May 15", 842, 91, "AUTOMATED"),
        ("May 16", 1_583, 88, "AUTOMATED"),
        ("May 17", 4_326, 79, "AUTOMATED"),
        ("May 18", 2_854, 82, "AUTOMATED"),
        ("May 19", 1_238, 93, "AUTOMATED"),
        ("May 20", 3_411, 85, "AUTOMATED"),
        ("May 21", 2_967, 77, "AUTOMATED"),
        ("May 22", 1_842, 90, "AUTOMATED"),
        ("May 23", 2_156, 86, "AUTOMATED"),
        ("May 24", 3_089, 81, "AUTOMATED"),
        ("May 25", 1_675, 92, "AUTOMATED"),
        ("May 26", 2_543, 87, "AUTOMATED"),
        ("May 27", 11_574, 71, "AUTOMATED"),
        ("May 28", 1_234, 89, "AUTOMATED"),
        ("May 29", 876, 95, "AUTOMATED"),
        ("May 30", 543, 94, "AUTOMATED"),
    ]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 9), sharex=True)

    dates = [p[0] for p in phases]
    volumes = [p[1] for p in phases]
    gaps = [p[2] for p in phases]
    modes = [p[3] for p in phases]

    x = range(len(dates))
    vol_colors = []
    for m in modes:
        if m == "AUTOMATED":
            vol_colors.append("#e94560")
        elif m == "Manual":
            vol_colors.append("#4ecdc4")
        elif m == "Mixed":
            vol_colors.append("#ffd166")
        else:
            vol_colors.append("#2a3a5e")

    # Top: volume
    ax1.bar(x, volumes, color=vol_colors, edgecolor="#0f3460", linewidth=0.3)
    ax1.set_ylabel("Blocks per day")
    ax1.set_title("louisbetonberlin — Phase Transition: Manual → Automated Blocking",
                  fontsize=13, fontweight="bold")
    ax1.set_yscale("log")
    ax1.set_ylim(1, 15_000)
    ax1.grid(axis="y", linestyle="--")
    ax1.axvline(x=7, color="#e94560", linestyle="--", linewidth=2, alpha=0.7)
    ax1.text(7.3, 8000, "Tool\nonset\nMay 6", fontsize=9, color="#e94560", fontweight="bold")

    legend_patches = [
        mpatches.Patch(facecolor="#4ecdc4", label="Manual (median gap: 69–279 sec)"),
        mpatches.Patch(facecolor="#e94560", label="Automated (median gap: 71–97 ms)"),
        mpatches.Patch(facecolor="#ffd166", label="Mixed"),
    ]
    ax1.legend(handles=legend_patches, loc="upper left", fontsize=9,
               facecolor="#1a1a2e", edgecolor="#e0e0e0")

    # Bottom: median gap (log scale)
    gap_colors = ["#e94560" if g < 1000 and m == "AUTOMATED" else "#4ecdc4"
                  for g, m in zip(gaps, modes)]
    ax2.scatter(x, [max(g, 1) for g in gaps], c=gap_colors, s=50, edgecolors="#0f3460", zorder=3)
    ax2.plot(x, [max(g, 1) for g in gaps], color="#e0e0e0", linewidth=0.5, alpha=0.5)
    ax2.set_ylabel("Median inter-block gap (ms, log)")
    ax2.set_yscale("log")
    ax2.axhline(y=100, color="#e94560", linestyle="--", alpha=0.5, label="100ms threshold")
    ax2.axhline(y=1000, color="#ffd166", linestyle="--", alpha=0.3, label="1 second")
    ax2.set_xticks(x)
    ax2.set_xticklabels(dates, rotation=45, ha="right", fontsize=8)
    ax2.set_xlabel("Date (2026)")
    ax2.grid(axis="y", linestyle="--")
    ax2.legend(loc="upper right", fontsize=9, facecolor="#1a1a2e", edgecolor="#e0e0e0")

    fig.tight_layout()
    fig.savefig(ASSETS / "phase_transition.png")
    plt.close(fig)
    print("  ✓ phase_transition.png")


# --------------------------------------------------------------------------
# 6. Victim Population Breakdown (all ring combined vs Bluesky total)
# --------------------------------------------------------------------------
def chart_scale_context():
    """Show the scale: 602K victims = 3% of Bluesky."""
    fig, ax = plt.subplots(figsize=(10, 6))

    # Waffle-style proportional
    total_bsky = 20_000_000  # estimated Bluesky users
    blocked = TOTAL_UNIQUE_VICTIMS
    unblocked = total_bsky - blocked
    pct_blocked = blocked / total_bsky * 100

    # Simple donut
    sizes = [blocked, unblocked]
    colors = ["#e94560", "#2a3a5e"]
    explode = (0.05, 0)
    wedges, texts, autotexts = ax.pie(
        sizes, explode=explode, colors=colors, autopct="",
        startangle=90, pctdistance=0.85,
        wedgeprops=dict(width=0.3, edgecolor="#e0e0e0", linewidth=1.5)
    )

    # Center text
    ax.text(0, 0, f"{blocked:,}\nvictims\n({pct_blocked:.1f}% of Bluesky)",
            ha="center", va="center", fontsize=16, fontweight="bold", color="#e94560")

    ax.set_title(
        "Scale of Coordinated Blocking\n"
        "16 ring members → 602,673 unique accounts blocked",
        fontsize=14, fontweight="bold", pad=20,
    )

    # Stats annotation
    stats_text = (
        f"Ring members: 16 (6 core + 10 extended)\n"
        f"Total block records: {RING_TOTAL_BLOCKS:,}\n"
        f"Unique victims: {TOTAL_UNIQUE_VICTIMS:,}\n"
        f"Campaign duration: 33 days (Apr 28 – May 30)\n"
        f"Central engine (smatsto): {495_878:,} blocks\n"
        f"Peak day: 232,272 blocks by 8 members"
    )
    ax.text(0.98, 0.02, stats_text,
            transform=ax.transAxes, ha="right", va="bottom",
            fontsize=10, color="#e0e0e0", family="monospace",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#2a3a5e", edgecolor="#4ecdc4"))

    fig.tight_layout()
    fig.savefig(ASSETS / "scale_context.png")
    plt.close(fig)
    print("  ✓ scale_context.png")


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
if __name__ == "__main__":
    print("Generating charts for louisbetonberlin mass-blocking ring investigation...")
    print()
    chart_victim_venn()
    chart_ring_hierarchy()
    chart_cadence_fingerprints()
    chart_overlap_matrix()
    chart_phase_transition()
    chart_scale_context()
    print()
    print(f"All charts saved to: {ASSETS}")
