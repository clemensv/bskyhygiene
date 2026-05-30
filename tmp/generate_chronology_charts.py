"""
Generate chronology visualizations for all three bot campaign investigations.

Produces:
- b-short ring: deployment_timeline.png, expansion_wave.png
- burst-follow: campaign_acceleration.png, daily_follows.png
- louisville: charity_fraud_timeline.png, pds_parasitism.png

Uses the same Plotly card styling as scripts/cards.py.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- Design constants (matching cards.py) ---
CARD_W, CARD_H = 1200, 675
BG_COLOR = "#ffffff"
TEXT_COLOR = "#1a1a1a"
ACCENT = "#cc0000"
ACCENT2 = "#cc5500"
ACCENT3 = "#996600"
MUTED = "#555555"
GRID_COLOR = "#e0e0e0"
FONT = "Roboto, sans-serif"
FONT_BOLD = "Roboto Black, Roboto, sans-serif"

ROOT = Path(__file__).resolve().parent.parent
BSHORT_ASSETS = ROOT / "investigations" / "2026-05-27-bshort-japanese-ring" / "assets"
BURST_ASSETS = ROOT / "investigations" / "2026-05-28-burst-follow-spam" / "assets"
LOUISVILLE_ASSETS = ROOT / "investigations" / "2026-05-28-louisvillebsky-haruhwa" / "assets"


def card_layout(
    fig: go.Figure, title: str = "", subtitle: str = "",
    width: int = CARD_W, height: int = CARD_H,
    margin_t: int = 80, margin_b: int = 60,
) -> go.Figure:
    annotations = list(fig.layout.annotations) if fig.layout.annotations else []
    if title:
        annotations.append(dict(
            text=f"<b>{title}</b>", xref="paper", yref="paper",
            x=0.5, y=1.14, showarrow=False, xanchor="center", yanchor="top",
            font=dict(size=28, color=TEXT_COLOR, family=FONT_BOLD),
        ))
    if subtitle:
        annotations.append(dict(
            text=subtitle, xref="paper", yref="paper",
            x=0.5, y=1.05, showarrow=False, xanchor="center", yanchor="top",
            font=dict(size=15, color=MUTED, family=FONT),
        ))
    annotations.append(dict(
        text="bskyhygiene • Bluesky Firehose KQL Analysis • 2026-05-29",
        xref="paper", yref="paper", x=0.5, y=-0.14, showarrow=False,
        xanchor="center", yanchor="bottom",
        font=dict(size=10, color="#777777", family=FONT),
    ))
    fig.update_layout(
        width=width, height=height,
        paper_bgcolor=BG_COLOR, plot_bgcolor=BG_COLOR,
        margin=dict(l=60, r=60, t=margin_t, b=margin_b),
        annotations=annotations,
        font=dict(color=TEXT_COLOR, family=FONT, size=14),
    )
    return fig


def save_chart(fig: go.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_image(str(path), scale=2)
    print(f"  ✓ {path.relative_to(ROOT)}")


# =============================================================================
# B-SHORT RING CHARTS
# =============================================================================

def bshort_deployment_timeline() -> None:
    """Hourly follow + post activity during the May 27 deployment."""
    hours = [
        "May 27\n00:00", "May 27\n12:00", "May 27\n13:00", "May 27\n14:00",
        "May 27\n15:00", "May 27\n16:00", "May 27\n17:00",
    ]
    follows = [72, 1, 941, 1, 25962, 2530, 1312]
    posts = [0, 0, 20, 11, 601, 1, 0]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Bar(
        x=hours, y=follows, name="Follows",
        marker_color=ACCENT, opacity=0.85,
    ), secondary_y=False)

    fig.add_trace(go.Scatter(
        x=hours, y=posts, name="Posts",
        mode="lines+markers", line=dict(color=ACCENT2, width=3),
        marker=dict(size=8, color=ACCENT2),
    ), secondary_y=True)

    fig.update_xaxes(title_text="Time (UTC)", tickfont=dict(size=11, family=FONT))
    fig.update_yaxes(
        title_text="Follows", secondary_y=False,
        showgrid=True, gridcolor=GRID_COLOR,
        tickfont=dict(size=12, family=FONT),
    )
    fig.update_yaxes(
        title_text="Posts", secondary_y=True,
        tickfont=dict(size=12, family=FONT),
    )
    fig.update_layout(legend=dict(
        x=0.01, y=0.99, xanchor="left", yanchor="top",
        bgcolor="rgba(255,255,255,0.85)", bordercolor="#cccccc", borderwidth=1,
    ))

    # Annotate the peak
    fig.add_annotation(
        x="May 27\n15:00", y=25962, text="<b>25,962 follows</b><br>MAIN BURST",
        showarrow=True, arrowhead=2, ax=0, ay=-40,
        font=dict(size=12, family=FONT, color=ACCENT),
    )

    fig = card_layout(
        fig,
        title="b-short Ring: Deployment Timeline",
        subtitle="May 27 activation — 30,746 follows + 633 posts in 4 hours",
    )
    save_chart(fig, BSHORT_ASSETS / "deployment_timeline.png")


def bshort_expansion_wave() -> None:
    """The May 28 expansion: 597 DIDs in 2 minutes."""
    # Timeline showing accumulation phases
    dates = ["Apr 30–\nMay 26", "May 27\n00:00", "May 27\n13–17h", "May 28\n21:17–19"]
    follows_cum = [200, 272, 30746, 30746]
    posts_cum = [0, 0, 633, 1234]
    dids_cum = [50, 50, 620, 1204]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=["Assembly<br>(Apr 30–May 26)", "Ignition<br>(May 27 00:00)",
           "Full Deploy<br>(May 27 13–17h)", "Expansion<br>(May 28 21:17)"],
        y=[200, 72, 30746, 0],
        name="Follows in phase",
        marker_color=ACCENT, opacity=0.85,
    ))
    fig.add_trace(go.Bar(
        x=["Assembly<br>(Apr 30–May 26)", "Ignition<br>(May 27 00:00)",
           "Full Deploy<br>(May 27 13–17h)", "Expansion<br>(May 28 21:17)"],
        y=[0, 0, 633, 601],
        name="Posts in phase",
        marker_color=ACCENT2, opacity=0.85,
    ))
    fig.add_trace(go.Bar(
        x=["Assembly<br>(Apr 30–May 26)", "Ignition<br>(May 27 00:00)",
           "Full Deploy<br>(May 27 13–17h)", "Expansion<br>(May 28 21:17)"],
        y=[50, 0, 570, 597],
        name="New DIDs activated",
        marker_color=ACCENT3, opacity=0.85,
    ))

    fig.update_layout(barmode="group")
    fig.update_xaxes(title_text="Phase", tickfont=dict(size=12, family=FONT))
    fig.update_yaxes(
        title_text="Count", showgrid=True, gridcolor=GRID_COLOR,
        tickfont=dict(size=12, family=FONT), type="log",
    )
    fig.update_layout(legend=dict(
        x=0.01, y=0.99, xanchor="left", yanchor="top",
        bgcolor="rgba(255,255,255,0.85)", bordercolor="#cccccc", borderwidth=1,
    ))

    fig.add_annotation(
        x="Expansion<br>(May 28 21:17)", y=597,
        text="<b>597 new DIDs</b><br>in 2 minutes",
        showarrow=True, arrowhead=2, ax=60, ay=-30,
        font=dict(size=12, family=FONT, color=ACCENT3),
    )

    fig = card_layout(
        fig,
        title="b-short Ring: Campaign Phases",
        subtitle="From slow assembly to explosive deployment — ring grew ~10% in 2 min on May 28",
    )
    save_chart(fig, BSHORT_ASSETS / "expansion_wave.png")


# =============================================================================
# BURST-FOLLOW CHARTS
# =============================================================================

def burst_campaign_acceleration() -> None:
    """Daily bot activations showing exponential growth."""
    dates = [
        "May 9", "May 13", "May 18", "May 19", "May 20",
        "May 23", "May 24", "May 25", "May 26", "May 27", "May 28", "May 29",
    ]
    bots = [1, 1, 7, 14, 17, 42, 52, 61, 93, 72, 106, 6]
    follows = [1577, 921, 7006, 14014, 17010, 42024, 51989, 61045, 94364, 73990, 106209, 13178]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Bar(
        x=dates, y=bots, name="Bots Activated",
        marker_color=ACCENT, opacity=0.85,
    ), secondary_y=False)

    fig.add_trace(go.Scatter(
        x=dates, y=follows, name="Follows Generated",
        mode="lines+markers", line=dict(color=ACCENT2, width=3),
        marker=dict(size=8, color=ACCENT2),
    ), secondary_y=True)

    fig.update_xaxes(title_text="Date (2026)", tickfont=dict(size=11, family=FONT), tickangle=-45)
    fig.update_yaxes(
        title_text="Bots Activated", secondary_y=False,
        showgrid=True, gridcolor=GRID_COLOR,
        tickfont=dict(size=12, family=FONT),
    )
    fig.update_yaxes(
        title_text="Follows Generated", secondary_y=True,
        tickfont=dict(size=12, family=FONT),
    )
    fig.update_layout(legend=dict(
        x=0.01, y=0.99, xanchor="left", yanchor="top",
        bgcolor="rgba(255,255,255,0.85)", bordercolor="#cccccc", borderwidth=1,
    ))

    # Peak annotation
    fig.add_annotation(
        x="May 28", y=106, text="<b>106 bots</b><br>106K follows",
        showarrow=True, arrowhead=2, ax=0, ay=-40,
        font=dict(size=12, family=FONT, color=ACCENT),
    )
    # Today annotation
    fig.add_annotation(
        x="May 29", y=6, text="Still active<br>(partial day)",
        showarrow=True, arrowhead=2, ax=40, ay=-30,
        font=dict(size=11, family=FONT, color=MUTED),
    )

    fig = card_layout(
        fig,
        title="Burst-Follow: Campaign Acceleration",
        subtitle="472 bots, 483K follows — exponential growth over 20 days, still active",
    )
    save_chart(fig, BURST_ASSETS / "campaign_acceleration.png")


def burst_daily_follows() -> None:
    """Cumulative follows showing campaign scale."""
    dates = [
        "May 9", "May 13", "May 18", "May 19", "May 20",
        "May 23", "May 24", "May 25", "May 26", "May 27", "May 28", "May 29",
    ]
    follows = [1577, 921, 7006, 14014, 17010, 42024, 51989, 61045, 94364, 73990, 106209, 13178]
    cumulative = []
    total = 0
    for f in follows:
        total += f
        cumulative.append(total)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dates, y=cumulative, name="Cumulative Follows",
        mode="lines+markers+text",
        line=dict(color=ACCENT, width=3),
        marker=dict(size=8, color=ACCENT),
        fill="tozeroy", fillcolor="rgba(204,0,0,0.08)",
        textposition="top center",
    ))

    # Horizontal line at 500K
    fig.add_hline(
        y=500000, line_dash="dot", line_color=MUTED, line_width=1.5,
        annotation_text="500K threshold", annotation_position="top right",
        annotation_font=dict(size=11, family=FONT, color=MUTED),
    )

    fig.update_xaxes(title_text="Date (2026)", tickfont=dict(size=11, family=FONT), tickangle=-45)
    fig.update_yaxes(
        title_text="Cumulative Follows", showgrid=True, gridcolor=GRID_COLOR,
        tickfont=dict(size=12, family=FONT), rangemode="tozero",
    )

    fig.add_annotation(
        x="May 29", y=cumulative[-1],
        text=f"<b>{cumulative[-1]:,}</b> total<br>and counting",
        showarrow=True, arrowhead=2, ax=-60, ay=-30,
        font=dict(size=13, family=FONT, color=ACCENT),
    )

    fig = card_layout(
        fig,
        title="Burst-Follow: Cumulative Impact",
        subtitle="483K fake follows injected into Bluesky — approaching 500K in 20 days",
    )
    save_chart(fig, BURST_ASSETS / "daily_follows.png")


# =============================================================================
# LOUISVILLE / HARUHWA CHARTS
# =============================================================================

def louisville_charity_fraud_timeline() -> None:
    """30-day continuous posting activity."""
    dates = pd.date_range("2026-04-30", "2026-05-29", freq="D")
    posts = [9, 13, 13, 9, 13, 22, 6, 19, 11, 6, 5, 23, 16, 18, 21, 16, 17, 14, 9, 8, 15, 9, 8, 12, 10, 17, 10, 2, 7, 5]
    authors = [7, 13, 9, 8, 9, 11, 5, 14, 10, 6, 5, 19, 16, 14, 19, 14, 12, 12, 9, 8, 12, 9, 7, 10, 7, 12, 10, 2, 7, 4]
    date_strs = [d.strftime("%b %d") for d in dates]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Bar(
        x=date_strs, y=posts, name="Posts/Day",
        marker_color=ACCENT, opacity=0.75,
    ), secondary_y=False)

    fig.add_trace(go.Scatter(
        x=date_strs, y=authors, name="Unique Authors",
        mode="lines+markers", line=dict(color=ACCENT2, width=2.5),
        marker=dict(size=6, color=ACCENT2),
    ), secondary_y=True)

    fig.update_xaxes(
        title_text="Date (2026)", tickfont=dict(size=9, family=FONT),
        tickangle=-45,
    )
    fig.update_yaxes(
        title_text="Posts", secondary_y=False,
        showgrid=True, gridcolor=GRID_COLOR,
        tickfont=dict(size=12, family=FONT), rangemode="tozero",
    )
    fig.update_yaxes(
        title_text="Unique Authors", secondary_y=True,
        tickfont=dict(size=12, family=FONT),
    )
    fig.update_layout(legend=dict(
        x=0.01, y=0.99, xanchor="left", yanchor="top",
        bgcolor="rgba(255,255,255,0.85)", bordercolor="#cccccc", borderwidth=1,
    ))

    # Mark today
    fig.add_vline(
        x=date_strs[-1], line_dash="dash", line_color=ACCENT, line_width=1.5,
        annotation_text="Today", annotation_position="top",
        annotation_font=dict(size=11, family=FONT, color=ACCENT),
    )

    fig = card_layout(
        fig,
        title="Louisville: Charity Fraud — 30 Days Continuous",
        subtitle="Arabic crisis narratives posted daily since Apr 30 — STILL ACTIVE (5 posts today)",
        margin_b=80,
    )
    save_chart(fig, LOUISVILLE_ASSETS / "charity_fraud_timeline.png")


def louisville_pds_parasitism() -> None:
    """Shows the Louisville PDS being parasitized by b-short ring."""
    categories = [
        "Original Louisville\n(Follow Inflation)",
        "Original Louisville\n(Charity Fraud)",
        "b-short Parasites\n(Japanese Spam Ring)",
    ]
    accounts = [3400, 112, 35]
    colors = [ACCENT2, ACCENT, ACCENT3]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=categories, y=accounts,
        marker_color=colors, opacity=0.85,
        text=[f"{a:,}" for a in accounts],
        textposition="outside", textfont=dict(size=14, family=FONT_BOLD),
    ))

    fig.update_xaxes(tickfont=dict(size=12, family=FONT))
    fig.update_yaxes(
        title_text="Accounts", showgrid=True, gridcolor=GRID_COLOR,
        tickfont=dict(size=12, family=FONT), rangemode="tozero",
        type="log",
    )

    fig.add_annotation(
        x="b-short Parasites\n(Japanese Spam Ring)", y=35,
        text="Independent operator<br>exploiting open registration",
        showarrow=True, arrowhead=2, ax=0, ay=-50,
        font=dict(size=11, family=FONT, color=ACCENT3),
    )

    fig = card_layout(
        fig,
        title="Louisville PDS: Multi-Operator Abuse",
        subtitle="Open registration policy enables parasitic use by unrelated campaigns",
    )
    save_chart(fig, LOUISVILLE_ASSETS / "pds_parasitism.png")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("Generating chronology charts...")
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
