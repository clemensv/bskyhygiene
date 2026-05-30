"""
Generate chronology visualizations for all three bot campaign investigations.
Uses matplotlib (no Chrome/kaleido dependency).

Produces:
- b-short ring: deployment_timeline.png, expansion_wave.png
- burst-follow: campaign_acceleration.png, daily_follows.png
- louisville: charity_fraud_timeline.png, pds_parasitism.png
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# --- Design constants (matching cards.py style) ---
BG_COLOR = "#ffffff"
TEXT_COLOR = "#1a1a1a"
ACCENT = "#cc0000"
ACCENT2 = "#cc5500"
ACCENT3 = "#996600"
MUTED = "#555555"
GRID_COLOR = "#e0e0e0"

plt.rcParams.update({
    "figure.facecolor": BG_COLOR,
    "axes.facecolor": BG_COLOR,
    "axes.edgecolor": GRID_COLOR,
    "axes.labelcolor": TEXT_COLOR,
    "xtick.color": TEXT_COLOR,
    "ytick.color": TEXT_COLOR,
    "text.color": TEXT_COLOR,
    "grid.color": GRID_COLOR,
    "grid.alpha": 0.7,
    "font.size": 11,
    "axes.titlesize": 14,
    "figure.titlesize": 18,
})

ROOT = Path(__file__).resolve().parent.parent
BSHORT_ASSETS = ROOT / "investigations" / "2026-05-27-bshort-japanese-ring" / "assets"
BURST_ASSETS = ROOT / "investigations" / "2026-05-28-burst-follow-spam" / "assets"
LOUISVILLE_ASSETS = ROOT / "investigations" / "2026-05-28-louisvillebsky-haruhwa" / "assets"
FOOTER = "bskyhygiene • Bluesky Firehose KQL Analysis • 2026-05-29"


def save_chart(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(str(path), dpi=150, bbox_inches="tight", facecolor=BG_COLOR)
    plt.close(fig)
    print(f"  ✓ {path.relative_to(ROOT)}")


def add_footer(fig: plt.Figure) -> None:
    fig.text(0.5, 0.01, FOOTER, ha="center", va="bottom",
             fontsize=8, color="#777777")


# =============================================================================
# B-SHORT RING CHARTS
# =============================================================================

def bshort_deployment_timeline() -> None:
    """Hourly follow + post activity during the May 27 deployment."""
    hours = ["00:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]
    follows = [72, 1, 941, 1, 25962, 2530, 1312]
    posts = [0, 0, 20, 11, 601, 1, 0]

    fig, ax1 = plt.subplots(figsize=(10, 5.6))
    x = np.arange(len(hours))
    width = 0.5

    bars = ax1.bar(x, follows, width, color=ACCENT, alpha=0.85, label="Follows")
    ax1.set_xlabel("May 27 — Hour (UTC)")
    ax1.set_ylabel("Follows", color=ACCENT)
    ax1.tick_params(axis="y", labelcolor=ACCENT)
    ax1.set_xticks(x)
    ax1.set_xticklabels(hours)
    ax1.grid(axis="y", alpha=0.4)

    ax2 = ax1.twinx()
    ax2.plot(x, posts, color=ACCENT2, linewidth=2.5, marker="o", markersize=7, label="Posts")
    ax2.set_ylabel("Posts", color=ACCENT2)
    ax2.tick_params(axis="y", labelcolor=ACCENT2)

    # Annotate peak
    ax1.annotate("25,962 follows\nMAIN BURST", xy=(4, 25962), xytext=(4, 28000),
                 fontsize=10, fontweight="bold", color=ACCENT, ha="center",
                 arrowprops=dict(arrowstyle="->", color=ACCENT))

    fig.suptitle("b-short Ring: Deployment Timeline", fontsize=16, fontweight="bold", y=0.98)
    ax1.set_title("May 27 activation — 30,746 follows + 633 posts in 4 hours",
                  fontsize=11, color=MUTED, pad=10)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", framealpha=0.9)

    add_footer(fig)
    fig.tight_layout(rect=[0, 0.03, 1, 0.93])
    save_chart(fig, BSHORT_ASSETS / "deployment_timeline.png")


def bshort_expansion_wave() -> None:
    """Campaign phases grouped bar chart."""
    phases = ["Assembly\n(Apr 30–May 26)", "Ignition\n(May 27 00h)",
              "Full Deploy\n(May 27 13–17h)", "Expansion\n(May 28 21:17)"]
    follows_phase = [200, 72, 30746, 0]
    posts_phase = [0, 0, 633, 601]
    dids_phase = [50, 0, 570, 597]

    fig, ax = plt.subplots(figsize=(10, 5.6))
    x = np.arange(len(phases))
    width = 0.25

    ax.bar(x - width, follows_phase, width, color=ACCENT, alpha=0.85, label="Follows")
    ax.bar(x, posts_phase, width, color=ACCENT2, alpha=0.85, label="Posts")
    ax.bar(x + width, dids_phase, width, color=ACCENT3, alpha=0.85, label="New DIDs")

    ax.set_xticks(x)
    ax.set_xticklabels(phases)
    ax.set_ylabel("Count")
    ax.set_yscale("log")
    ax.set_ylim(bottom=1)
    ax.grid(axis="y", alpha=0.4)
    ax.legend(loc="upper left", framealpha=0.9)

    # Annotate expansion
    ax.annotate("597 new DIDs\nin 2 minutes", xy=(3, 597), xytext=(3, 2500),
                fontsize=10, fontweight="bold", color=ACCENT3, ha="center",
                arrowprops=dict(arrowstyle="->", color=ACCENT3))

    fig.suptitle("b-short Ring: Campaign Phases", fontsize=16, fontweight="bold", y=0.98)
    ax.set_title("From slow assembly to explosive deployment — ring grew ~10% in 2 min on May 28",
                 fontsize=11, color=MUTED, pad=10)

    add_footer(fig)
    fig.tight_layout(rect=[0, 0.03, 1, 0.93])
    save_chart(fig, BSHORT_ASSETS / "expansion_wave.png")


# =============================================================================
# BURST-FOLLOW CHARTS
# =============================================================================

def burst_campaign_acceleration() -> None:
    """Daily bot activations showing exponential growth."""
    dates = ["May 9", "May 13", "May 18", "May 19", "May 20",
             "May 23", "May 24", "May 25", "May 26", "May 27", "May 28", "May 29"]
    bots = [1, 1, 7, 14, 17, 42, 52, 61, 93, 72, 106, 6]
    follows = [1577, 921, 7006, 14014, 17010, 42024, 51989, 61045, 94364, 73990, 106209, 13178]

    fig, ax1 = plt.subplots(figsize=(10, 5.6))
    x = np.arange(len(dates))

    ax1.bar(x, bots, color=ACCENT, alpha=0.85, label="Bots Activated")
    ax1.set_xlabel("Date (2026)")
    ax1.set_ylabel("Bots Activated", color=ACCENT)
    ax1.tick_params(axis="y", labelcolor=ACCENT)
    ax1.set_xticks(x)
    ax1.set_xticklabels(dates, rotation=45, ha="right")
    ax1.grid(axis="y", alpha=0.4)

    ax2 = ax1.twinx()
    ax2.plot(x, follows, color=ACCENT2, linewidth=2.5, marker="o", markersize=6, label="Follows Generated")
    ax2.set_ylabel("Follows Generated", color=ACCENT2)
    ax2.tick_params(axis="y", labelcolor=ACCENT2)
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, p: f"{v/1000:.0f}K"))

    # Peak annotation
    ax1.annotate("106 bots\n106K follows", xy=(10, 106), xytext=(10, 125),
                 fontsize=10, fontweight="bold", color=ACCENT, ha="center",
                 arrowprops=dict(arrowstyle="->", color=ACCENT))
    # Still active
    ax1.annotate("Still active\n(partial day)", xy=(11, 6), xytext=(9.5, 40),
                 fontsize=9, color=MUTED, ha="center",
                 arrowprops=dict(arrowstyle="->", color=MUTED))

    fig.suptitle("Burst-Follow: Campaign Acceleration", fontsize=16, fontweight="bold", y=0.98)
    ax1.set_title("472 bots, 483K follows — exponential growth over 20 days, still active",
                  fontsize=11, color=MUTED, pad=10)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", framealpha=0.9)

    add_footer(fig)
    fig.tight_layout(rect=[0, 0.03, 1, 0.93])
    save_chart(fig, BURST_ASSETS / "campaign_acceleration.png")


def burst_daily_follows() -> None:
    """Cumulative follows showing campaign scale."""
    dates = ["May 9", "May 13", "May 18", "May 19", "May 20",
             "May 23", "May 24", "May 25", "May 26", "May 27", "May 28", "May 29"]
    follows = [1577, 921, 7006, 14014, 17010, 42024, 51989, 61045, 94364, 73990, 106209, 13178]
    cumulative = np.cumsum(follows)

    fig, ax = plt.subplots(figsize=(10, 5.6))
    x = np.arange(len(dates))

    ax.fill_between(x, cumulative, alpha=0.08, color=ACCENT)
    ax.plot(x, cumulative, color=ACCENT, linewidth=3, marker="o", markersize=7)

    # 500K line
    ax.axhline(y=500000, color=MUTED, linestyle=":", linewidth=1.5, alpha=0.7)
    ax.text(len(dates) - 1, 510000, "500K threshold", ha="right", fontsize=9, color=MUTED)

    ax.set_xticks(x)
    ax.set_xticklabels(dates, rotation=45, ha="right")
    ax.set_xlabel("Date (2026)")
    ax.set_ylabel("Cumulative Follows")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, p: f"{v/1000:.0f}K"))
    ax.grid(axis="y", alpha=0.4)
    ax.set_ylim(bottom=0)

    # Final value annotation
    ax.annotate(f"{cumulative[-1]:,.0f} total\nand counting",
                xy=(11, cumulative[-1]), xytext=(9, cumulative[-1] + 30000),
                fontsize=11, fontweight="bold", color=ACCENT, ha="center",
                arrowprops=dict(arrowstyle="->", color=ACCENT))

    fig.suptitle("Burst-Follow: Cumulative Impact", fontsize=16, fontweight="bold", y=0.98)
    ax.set_title("483K fake follows injected into Bluesky — approaching 500K in 20 days",
                 fontsize=11, color=MUTED, pad=10)

    add_footer(fig)
    fig.tight_layout(rect=[0, 0.03, 1, 0.93])
    save_chart(fig, BURST_ASSETS / "daily_follows.png")


# =============================================================================
# LOUISVILLE / HARUHWA CHARTS
# =============================================================================

def louisville_charity_fraud_timeline() -> None:
    """30-day continuous posting activity."""
    import pandas as pd
    dates = pd.date_range("2026-04-30", "2026-05-29", freq="D")
    posts = [9, 13, 13, 9, 13, 22, 6, 19, 11, 6, 5, 23, 16, 18, 21, 16, 17, 14, 9, 8, 15, 9, 8, 12, 10, 17, 10, 2, 7, 5]
    authors = [7, 13, 9, 8, 9, 11, 5, 14, 10, 6, 5, 19, 16, 14, 19, 14, 12, 12, 9, 8, 12, 9, 7, 10, 7, 12, 10, 2, 7, 4]
    date_strs = [d.strftime("%b %d") for d in dates]

    fig, ax1 = plt.subplots(figsize=(12, 5.6))
    x = np.arange(len(dates))

    ax1.bar(x, posts, color=ACCENT, alpha=0.75, label="Posts/Day")
    ax1.set_xlabel("Date (2026)")
    ax1.set_ylabel("Posts", color=ACCENT)
    ax1.tick_params(axis="y", labelcolor=ACCENT)
    ax1.set_xticks(x[::2])
    ax1.set_xticklabels([date_strs[i] for i in range(0, len(date_strs), 2)], rotation=45, ha="right")
    ax1.grid(axis="y", alpha=0.4)
    ax1.set_ylim(bottom=0)

    ax2 = ax1.twinx()
    ax2.plot(x, authors, color=ACCENT2, linewidth=2.5, marker="o", markersize=5, label="Unique Authors")
    ax2.set_ylabel("Unique Authors", color=ACCENT2)
    ax2.tick_params(axis="y", labelcolor=ACCENT2)

    # Mark today
    ax1.axvline(x=29, color=ACCENT, linestyle="--", linewidth=1.5, alpha=0.7)
    ax1.text(29, max(posts) + 1, "Today", ha="center", fontsize=9, color=ACCENT, fontweight="bold")

    fig.suptitle("Louisville: Charity Fraud — 30 Days Continuous", fontsize=16, fontweight="bold", y=0.98)
    ax1.set_title("Arabic crisis narratives posted daily since Apr 30 — STILL ACTIVE (5 posts today)",
                  fontsize=11, color=MUTED, pad=10)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right", framealpha=0.9)

    add_footer(fig)
    fig.tight_layout(rect=[0, 0.03, 1, 0.93])
    save_chart(fig, LOUISVILLE_ASSETS / "charity_fraud_timeline.png")


def louisville_pds_parasitism() -> None:
    """Shows the Louisville PDS being parasitized by b-short ring."""
    categories = ["Original Louisville\n(Follow Inflation)", "Original Louisville\n(Charity Fraud)",
                  "b-short Parasites\n(Japanese Spam Ring)"]
    accounts = [3400, 112, 35]
    colors = [ACCENT2, ACCENT, ACCENT3]

    fig, ax = plt.subplots(figsize=(10, 5.6))

    bars = ax.bar(categories, accounts, color=colors, alpha=0.85)
    ax.set_ylabel("Accounts")
    ax.set_yscale("log")
    ax.set_ylim(bottom=1)
    ax.grid(axis="y", alpha=0.4)

    # Value labels on bars
    for bar, val in zip(bars, accounts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() * 1.3,
                f"{val:,}", ha="center", fontsize=13, fontweight="bold", color=TEXT_COLOR)

    # Annotation
    ax.annotate("Independent operator\nexploiting open registration",
                xy=(2, 35), xytext=(2, 200),
                fontsize=10, color=ACCENT3, ha="center",
                arrowprops=dict(arrowstyle="->", color=ACCENT3))

    fig.suptitle("Louisville PDS: Multi-Operator Abuse", fontsize=16, fontweight="bold", y=0.98)
    ax.set_title("Open registration policy enables parasitic use by unrelated campaigns",
                 fontsize=11, color=MUTED, pad=10)

    add_footer(fig)
    fig.tight_layout(rect=[0, 0.03, 1, 0.93])
    save_chart(fig, LOUISVILLE_ASSETS / "pds_parasitism.png")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("Generating chronology charts (matplotlib)...")
    print()

    print("b-short Ring:")
    bshort_deployment_timeline()
    bshort_expansion_wave()
    print()

    print("Burst-Follow:")
    burst_campaign_acceleration()
    burst_daily_follows()
    print()

    print("Louisville/Haruhwa:")
    louisville_charity_fraud_timeline()
    louisville_pds_parasitism()
    print()

    print("Done — 6 charts generated.")
