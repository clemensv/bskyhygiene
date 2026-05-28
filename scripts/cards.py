"""
Visualization cards for bskyhygiene bot investigations.

Adapted from the nius botfinder project. Produces publication-quality
Plotly charts as PNG exports for inclusion in reports and the repo.

Two key visualizations:
- Creation-vs-Follow scatter: shows accounts following targets almost
  immediately after creation (automation signal)
- Network cluster graph: shows co-follow relationships between bot
  accounts and their targets
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- Design constants (per AGENTS.md Plotly standards) ---
CARD_W, CARD_H = 1200, 675
CARD_SQUARE = 1200
BG_COLOR = "#ffffff"
TEXT_COLOR = "#1a1a1a"
ACCENT = "#cc0000"
ACCENT2 = "#cc5500"
ACCENT3 = "#996600"
MUTED = "#555555"
GRID_COLOR = "#e0e0e0"
FONT = "Roboto, sans-serif"
FONT_BOLD = "Roboto Black, Roboto, sans-serif"


def card_layout(
    fig: go.Figure, title: str = "", subtitle: str = "",
    width: int = CARD_W, height: int = CARD_H,
    margin_t: int = 80, margin_b: int = 60,
) -> go.Figure:
    """Apply consistent card styling."""
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
        text="bskyhygiene • Bluesky Firehose + AT Protocol • Bot Infrastructure Analysis",
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


def creation_vs_follow_scatter(
    detail_df: pd.DataFrame,
    title: str = "Account Creation vs. Time-to-Follow",
    subtitle: str = "Red dots = follow within minutes of account creation (automation signal)",
) -> go.Figure:
    """
    Scatter plot showing when bot accounts were created (x-axis) vs how
    quickly they followed a target after creation (y-axis, in minutes).

    Expected columns in detail_df:
        - follower_created_at: datetime — when the follower account was created
        - age_at_follow_minutes: float — minutes between account creation and first follow
        - handle: str (optional) — for hover text
        - pds: str (optional) — PDS server name for color coding
    """
    df = detail_df.dropna(subset=["age_at_follow_minutes"]).copy()
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No timing data available", xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False, font=dict(size=16, family=FONT),
        )
        return card_layout(fig, title=title)

    df["age_capped"] = df["age_at_follow_minutes"].clip(upper=120)
    df["created_str"] = pd.to_datetime(df["follower_created_at"]).dt.strftime("%Y-%m-%d %H:%M")

    # Color by PDS if available
    if "pds" in df.columns:
        pds_servers = df["pds"].unique()
        color_map = {}
        palette = [ACCENT, ACCENT2, ACCENT3, "#3498db", "#9b59b6"]
        for i, pds in enumerate(pds_servers):
            color_map[pds] = palette[i % len(palette)]

        fig = go.Figure()
        for pds in pds_servers:
            pds_df = df[df["pds"] == pds]
            hover_text = [
                f"@{h}<br>Created: {c}<br>Follow after: {a:.1f} min"
                for h, c, a in zip(
                    pds_df.get("handle", [""] * len(pds_df)),
                    pds_df["created_str"],
                    pds_df["age_at_follow_minutes"],
                )
            ]
            fig.add_trace(go.Scatter(
                x=pds_df["created_str"],
                y=pds_df["age_capped"],
                mode="markers",
                name=pds,
                marker=dict(size=5, opacity=0.7, color=color_map[pds]),
                hovertext=hover_text,
                hoverinfo="text",
            ))
        fig.update_layout(legend=dict(
            x=0.01, y=0.99, xanchor="left", yanchor="top",
            bgcolor="rgba(255,255,255,0.85)", bordercolor="#cccccc", borderwidth=1,
            font=dict(size=11, family=FONT),
        ))
    else:
        hover_text = [
            f"Created: {c}<br>Follow after: {a:.1f} min"
            for c, a in zip(df["created_str"], df["age_at_follow_minutes"])
        ]
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["created_str"],
            y=df["age_capped"],
            mode="markers",
            marker=dict(
                size=5, opacity=0.7,
                color=df["age_capped"].values,
                colorscale="RdYlGn",
                cmin=0, cmax=60,
                showscale=True,
                colorbar=dict(
                    title=dict(text="Minutes", font=dict(size=12, family=FONT)),
                    tickfont=dict(size=11, family=FONT),
                ),
            ),
            hovertext=hover_text,
            hoverinfo="text",
            showlegend=False,
        ))

    # Threshold line at 5 minutes
    fig.add_hline(
        y=5, line_dash="dash", line_color=ACCENT, line_width=1.5,
        annotation_text="5-min threshold", annotation_position="top right",
        annotation_font=dict(size=12, family=FONT, color=ACCENT),
    )

    fig.update_xaxes(
        title_text="Account Created (UTC)", tickfont=dict(size=11, family=FONT),
        type="category", tickangle=-45,
    )
    fig.update_yaxes(
        title_text="Minutes until Follow", tickfont=dict(size=12, family=FONT),
        showgrid=True, gridcolor=GRID_COLOR, rangemode="tozero",
    )
    return card_layout(fig, title=title, subtitle=subtitle, margin_b=80)


def network_cluster_graph(
    nodes_df: pd.DataFrame,
    edges_df: pd.DataFrame,
    title: str = "Bot Co-Follow Network",
    subtitle: str = "Accounts sharing bot followers — size = suspect follower count",
    min_suspect: int = 10,
) -> go.Figure:
    """
    Network graph showing co-follow relationships between targets of bot accounts.

    Expected columns in nodes_df:
        - handle: str — Bluesky handle
        - suspect_followers: int — number of suspected bot followers
        - is_cluster_member: bool (optional) — whether node is in core cluster

    Expected columns in edges_df:
        - source: str — handle
        - target: str — handle
        - shared_followers: int — number of shared bot followers
    """
    CARD_SIZE = CARD_SQUARE

    G = nx.Graph()
    filtered_nodes = nodes_df[nodes_df["suspect_followers"] >= min_suspect].copy()
    for _, row in filtered_nodes.iterrows():
        G.add_node(row["handle"], weight=row["suspect_followers"])

    handles_set = set(filtered_nodes["handle"])
    for _, row in edges_df.iterrows():
        if row["source"] in handles_set and row["target"] in handles_set:
            G.add_edge(row["source"], row["target"], weight=row["shared_followers"])

    if len(G.nodes()) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="Insufficient cluster data", xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False, font=dict(size=16, family=FONT),
        )
        fig.update_layout(width=CARD_SIZE, height=CARD_SIZE)
        return card_layout(fig, title=title, width=CARD_SIZE, height=CARD_SIZE)

    weights = nx.get_node_attributes(G, "weight")
    max_w = max(weights.values()) if weights else 1

    # Determine core vs periphery
    cluster_members = set(
        nodes_df[nodes_df["is_cluster_member"] == True]["handle"]
    ) if "is_cluster_member" in nodes_df.columns else set(G.nodes())

    core_nodes = [n for n in G.nodes() if n in cluster_members]
    periphery_nodes = [n for n in G.nodes() if n not in cluster_members]
    periphery_set = set(periphery_nodes)

    # Layout: concentric rings for core, perimeter for periphery
    core_sorted = sorted(core_nodes, key=lambda n: weights.get(n, 0), reverse=True)
    pos = {}
    rings = [1, 5, 15, 40, 80, 200]
    ring_radii = [0.0, 0.18, 0.35, 0.52, 0.68, 0.80]
    placed = 0
    for ring_idx in range(len(rings)):
        ring_count = rings[ring_idx] - (rings[ring_idx - 1] if ring_idx > 0 else 0)
        radius = ring_radii[ring_idx]
        nodes_in_ring = core_sorted[placed:placed + ring_count]
        if not nodes_in_ring:
            break
        for i, n in enumerate(nodes_in_ring):
            if radius == 0:
                pos[n] = np.array([0.0, 0.0])
            else:
                angle = 2 * np.pi * i / len(nodes_in_ring) + ring_idx * 0.3
                pos[n] = np.array([radius * np.cos(angle), radius * np.sin(angle)])
        placed += len(nodes_in_ring)
    remaining = core_sorted[placed:]
    if remaining:
        for i, n in enumerate(remaining):
            angle = 2 * np.pi * i / len(remaining) + 0.1
            pos[n] = np.array([0.85 * np.cos(angle), 0.85 * np.sin(angle)])

    # Periphery on outer square perimeter
    margin = 1.05
    if periphery_nodes:
        n_peri = len(periphery_nodes)
        perimeter = 8 * margin
        for i, n in enumerate(periphery_nodes):
            t = (i / n_peri) * perimeter
            if t < 2 * margin:
                pos[n] = np.array([-margin + t, margin])
            elif t < 4 * margin:
                pos[n] = np.array([margin, margin - (t - 2 * margin)])
            elif t < 6 * margin:
                pos[n] = np.array([margin - (t - 4 * margin), -margin])
            else:
                pos[n] = np.array([-margin, -margin + (t - 6 * margin)])

    # Edges
    edge_core_x, edge_core_y = [], []
    edge_peri_x, edge_peri_y = [], []
    for u, v in G.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        if u in periphery_set or v in periphery_set:
            edge_peri_x.extend([x0, x1, None])
            edge_peri_y.extend([y0, y1, None])
        else:
            edge_core_x.extend([x0, x1, None])
            edge_core_y.extend([y0, y1, None])

    edge_core_trace = go.Scatter(
        x=edge_core_x, y=edge_core_y, mode="lines",
        line=dict(width=0.4, color="rgba(200,0,0,0.15)"),
        hoverinfo="none", showlegend=False,
    )
    edge_peri_trace = go.Scatter(
        x=edge_peri_x, y=edge_peri_y, mode="lines",
        line=dict(width=0.4, color="rgba(0,160,0,0.18)"),
        hoverinfo="none", showlegend=False,
    )

    # Nodes
    node_x = [pos[n][0] for n in G.nodes()]
    node_y = [pos[n][1] for n in G.nodes()]
    node_sizes = [max(7, 45 * (weights.get(n, 0) / max_w)) for n in G.nodes()]
    node_colors = []
    for n in G.nodes():
        if n in periphery_set:
            node_colors.append("#aaaaaa")
        elif weights.get(n, 0) >= max_w * 0.3:
            node_colors.append(ACCENT)
        else:
            node_colors.append(ACCENT2)

    node_trace = go.Scatter(
        x=node_x, y=node_y, mode="markers",
        marker=dict(size=node_sizes, color=node_colors, line=dict(width=0.6, color="#333333")),
        hovertext=[f"@{n}: {weights.get(n,0)} suspects, {G.degree(n)} edges" for n in G.nodes()],
        hoverinfo="text", showlegend=False,
    )

    # Labels for top nodes
    sorted_nodes = sorted(G.nodes(), key=lambda n: weights.get(n, 0), reverse=True)
    top_labeled = sorted_nodes[:20]
    label_x = [pos[n][0] for n in top_labeled]
    label_y = [pos[n][1] for n in top_labeled]
    label_text = ["@" + n.split(".")[0] for n in top_labeled]
    label_trace = go.Scatter(
        x=label_x, y=label_y, mode="text",
        text=label_text, textposition="top center",
        textfont=dict(size=9, color=TEXT_COLOR, family=FONT),
        hoverinfo="none", showlegend=False,
    )

    fig = go.Figure(data=[edge_peri_trace, edge_core_trace, node_trace, label_trace])

    x_range = margin + 0.35
    y_range = margin + 0.25
    fig.update_xaxes(visible=False, range=[-x_range, x_range])
    fig.update_yaxes(visible=False, range=[-y_range, y_range], scaleanchor="x", scaleratio=1)

    # Legend traces
    fig.add_trace(go.Scatter(
        x=[None], y=[None], mode="markers",
        marker=dict(size=10, color=ACCENT), name="Top targets (high bot follower count)",
        showlegend=True,
    ))
    fig.add_trace(go.Scatter(
        x=[None], y=[None], mode="markers",
        marker=dict(size=10, color=ACCENT2), name="Cluster members (core)",
        showlegend=True,
    ))
    fig.add_trace(go.Scatter(
        x=[None], y=[None], mode="markers",
        marker=dict(size=10, color="#aaaaaa"), name="Periphery targets",
        showlegend=True,
    ))
    fig.add_trace(go.Scatter(
        x=[None], y=[None], mode="lines",
        line=dict(width=2, color="rgba(200,0,0,0.5)"), name="Edge: mutual follow",
        showlegend=True,
    ))
    fig.add_trace(go.Scatter(
        x=[None], y=[None], mode="lines",
        line=dict(width=2, color="rgba(0,160,0,0.6)"), name="Edge: one-way follow (target)",
        showlegend=True,
    ))

    fig.update_layout(
        width=CARD_SIZE, height=CARD_SIZE,
        paper_bgcolor=BG_COLOR, plot_bgcolor=BG_COLOR,
        margin=dict(l=10, r=10, t=70, b=70),
        font=dict(color=TEXT_COLOR, family=FONT, size=14),
        legend=dict(
            x=0.0, y=0.0, xanchor="left", yanchor="bottom",
            bgcolor="rgba(255,255,255,0.85)", bordercolor="#cccccc", borderwidth=1,
            font=dict(size=10, family=FONT), orientation="v",
        ),
    )

    return card_layout(fig, title=title, subtitle=subtitle, width=CARD_SIZE, height=CARD_SIZE)
