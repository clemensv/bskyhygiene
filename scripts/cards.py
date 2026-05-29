"""
Visualization cards for bskyhygiene bot investigations.

Adapted from the nius botfinder project. Produces publication-quality
matplotlib charts as PNG exports for inclusion in reports and the repo.

Two key visualizations:
- Creation-vs-Follow scatter: shows accounts following targets almost
  immediately after creation (automation signal)
- Network cluster graph: shows co-follow relationships between bot
  accounts and their targets
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import networkx as nx
import numpy as np
import pandas as pd

# --- Design constants ---
CARD_W, CARD_H = 1200, 675
CARD_SQUARE = 1200
BG_COLOR = "#ffffff"
TEXT_COLOR = "#1a1a1a"
ACCENT = "#cc0000"
ACCENT2 = "#cc5500"
ACCENT3 = "#996600"
MUTED = "#555555"
GRID_COLOR = "#e0e0e0"
FONT = "DejaVu Sans"
FONT_BOLD = "DejaVu Sans"

DPI = 150


def _apply_card_style(
    fig: plt.Figure, ax: plt.Axes, title: str = "", subtitle: str = "",
) -> plt.Figure:
    """Apply consistent card styling to a matplotlib figure."""
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    if title:
        fig.suptitle(title, fontsize=16, fontweight="bold", color=TEXT_COLOR,
                     fontfamily=FONT_BOLD, y=0.97)
    if subtitle:
        ax.set_title(subtitle, fontsize=10, color=MUTED, fontfamily=FONT, pad=12)
    fig.text(0.5, 0.01, "bskyhygiene \u2022 Bluesky Firehose + AT Protocol \u2022 Bot Infrastructure Analysis",
             ha="center", fontsize=7, color="#777777", fontfamily=FONT)
    return fig


def creation_vs_follow_scatter(
    detail_df: pd.DataFrame,
    title: str = "Account Creation vs. Time-to-Follow",
    subtitle: str = "Red dots = follow within minutes of account creation (automation signal)",
) -> plt.Figure:
    """
    Scatter plot: x = account creation datetime, y = minutes until first follow.

    Expected columns in detail_df:
        - follower_created_at: datetime
        - age_at_follow_minutes: float
        - handle: str (optional)
        - pds: str (optional) — PDS server name for color coding
    """
    df = detail_df.dropna(subset=["age_at_follow_minutes"]).copy()
    fig, ax = plt.subplots(figsize=(CARD_W / DPI, CARD_H / DPI), dpi=DPI)

    if df.empty:
        ax.text(0.5, 0.5, "No timing data available", transform=ax.transAxes,
                ha="center", va="center", fontsize=14, color=MUTED)
        _apply_card_style(fig, ax, title=title)
        return fig

    df["age_capped"] = df["age_at_follow_minutes"].clip(upper=120)
    df["created_dt"] = pd.to_datetime(df["follower_created_at"])

    palette = [ACCENT, ACCENT2, ACCENT3, "#3498db", "#9b59b6"]

    if "pds" in df.columns and df["pds"].nunique() > 1:
        pds_servers = df["pds"].unique()
        for i, pds in enumerate(pds_servers):
            pds_df = df[df["pds"] == pds]
            ax.scatter(pds_df["created_dt"], pds_df["age_capped"],
                       s=18, alpha=0.7, color=palette[i % len(palette)],
                       label=pds, edgecolors="none")
        ax.legend(loc="upper left", fontsize=8, framealpha=0.85,
                  edgecolor="#cccccc", fancybox=False)
    else:
        colors = np.where(df["age_capped"] <= 5, ACCENT, ACCENT3)
        ax.scatter(df["created_dt"], df["age_capped"],
                   s=18, alpha=0.7, c=colors, edgecolors="none")

    ax.axhline(y=5, linestyle="--", color=ACCENT, linewidth=1.2, alpha=0.8)
    ax.text(0.98, 5.5, "5-min threshold", transform=ax.get_yaxis_transform(),
            ha="right", va="bottom", fontsize=8, color=ACCENT, fontstyle="italic")

    ax.set_xlabel("Account Created (UTC)", fontsize=10, color=TEXT_COLOR)
    ax.set_ylabel("Minutes until Follow", fontsize=10, color=TEXT_COLOR)
    ax.set_ylim(bottom=0)
    ax.yaxis.grid(True, color=GRID_COLOR, linewidth=0.5)
    ax.xaxis.grid(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.autofmt_xdate(rotation=30)
    plt.tight_layout(rect=[0, 0.03, 1, 0.92])
    _apply_card_style(fig, ax, title=title, subtitle=subtitle)
    return fig


def network_cluster_graph(
    nodes_df: pd.DataFrame,
    edges_df: pd.DataFrame,
    title: str = "Bot Co-Follow Network",
    subtitle: str = "Accounts sharing bot followers \u2014 size = suspect follower count",
    min_suspect: int = 10,
) -> plt.Figure:
    """
    Network graph showing co-follow relationships between targets of bot accounts.

    Expected columns in nodes_df:
        - handle: str
        - suspect_followers: int
        - is_cluster_member: bool (optional)

    Expected columns in edges_df:
        - source: str
        - target: str
        - shared_followers: int
    """
    fig, ax = plt.subplots(figsize=(CARD_SQUARE / DPI, CARD_SQUARE / DPI), dpi=DPI)

    G = nx.Graph()
    filtered_nodes = nodes_df[nodes_df["suspect_followers"] >= min_suspect].copy()
    for _, row in filtered_nodes.iterrows():
        G.add_node(row["handle"], weight=row["suspect_followers"])

    handles_set = set(filtered_nodes["handle"])
    for _, row in edges_df.iterrows():
        if row["source"] in handles_set and row["target"] in handles_set:
            G.add_edge(row["source"], row["target"], weight=row["shared_followers"])

    if len(G.nodes()) == 0:
        ax.text(0.5, 0.5, "Insufficient cluster data", transform=ax.transAxes,
                ha="center", va="center", fontsize=14, color=MUTED)
        ax.set_axis_off()
        _apply_card_style(fig, ax, title=title)
        return fig

    weights = nx.get_node_attributes(G, "weight")
    max_w = max(weights.values()) if weights else 1

    cluster_members = set(
        nodes_df[nodes_df["is_cluster_member"] == True]["handle"]
    ) if "is_cluster_member" in nodes_df.columns else set(G.nodes())

    core_nodes = [n for n in G.nodes() if n in cluster_members]
    periphery_nodes = [n for n in G.nodes() if n not in cluster_members]
    periphery_set = set(periphery_nodes)

    # Layout: spring for core, shell for periphery
    if len(G.nodes()) > 1:
        pos = nx.spring_layout(G, k=1.5 / np.sqrt(len(G.nodes())), iterations=80, seed=42)
    else:
        pos = {list(G.nodes())[0]: np.array([0.0, 0.0])}

    # Draw edges: core=red, periphery=green
    core_edges = [(u, v) for u, v in G.edges() if u not in periphery_set and v not in periphery_set]
    peri_edges = [(u, v) for u, v in G.edges() if u in periphery_set or v in periphery_set]

    nx.draw_networkx_edges(G, pos, edgelist=core_edges, ax=ax,
                           edge_color="red", alpha=0.12, width=0.5)
    nx.draw_networkx_edges(G, pos, edgelist=peri_edges, ax=ax,
                           edge_color="green", alpha=0.15, width=0.4)

    # Draw nodes
    node_list = list(G.nodes())
    node_sizes = [max(30, 400 * (weights.get(n, 0) / max_w)) for n in node_list]
    node_colors = []
    for n in node_list:
        if n in periphery_set:
            node_colors.append("#aaaaaa")
        elif weights.get(n, 0) >= max_w * 0.3:
            node_colors.append(ACCENT)
        else:
            node_colors.append(ACCENT2)

    nx.draw_networkx_nodes(G, pos, nodelist=node_list, node_size=node_sizes,
                           node_color=node_colors, edgecolors="#333333",
                           linewidths=0.5, alpha=0.9, ax=ax)

    # Labels for top 15 nodes
    sorted_nodes = sorted(G.nodes(), key=lambda n: weights.get(n, 0), reverse=True)
    top_labels = {n: "@" + n.split(".")[0] for n in sorted_nodes[:15]}
    nx.draw_networkx_labels(G, pos, labels=top_labels, font_size=6,
                            font_color=TEXT_COLOR, font_family=FONT, ax=ax)

    ax.set_axis_off()

    # Legend
    legend_handles = [
        mpatches.Patch(color=ACCENT, label="Top targets (high bot follower count)"),
        mpatches.Patch(color=ACCENT2, label="Cluster members (core)"),
        mpatches.Patch(color="#aaaaaa", label="Periphery targets"),
        mlines.Line2D([], [], color="red", alpha=0.5, linewidth=1.5, label="Core co-follow edge"),
        mlines.Line2D([], [], color="green", alpha=0.5, linewidth=1.5, label="Periphery edge"),
    ]
    ax.legend(handles=legend_handles, loc="lower left", fontsize=7,
              framealpha=0.85, edgecolor="#cccccc", fancybox=False)

    plt.tight_layout(rect=[0, 0.03, 1, 0.92])
    _apply_card_style(fig, ax, title=title, subtitle=subtitle)
    return fig
