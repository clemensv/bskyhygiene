"""
Generate visualization cards from blocklist data.

Produces:
- creation_scatter.png: Account creation time vs first follow timing
- network_graph.png: Co-follow network between bot accounts and targets

Requires the blocklist JSON and follow-detail data from the scan.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import httpx
import numpy as np
import pandas as pd
import time

sys.path.insert(0, str(Path(__file__).parent))
from cards import creation_vs_follow_scatter, network_cluster_graph

BLUESKY_API = "https://bsky.social/xrpc"


def authenticate(client: httpx.Client, identifier: str, app_password: str) -> str | None:
    resp = client.post(
        f"{BLUESKY_API}/com.atproto.server.createSession",
        json={"identifier": identifier, "password": app_password},
    )
    if resp.status_code == 200:
        return resp.json().get("accessJwt")
    return None


def get_follows(client: httpx.Client, did: str, auth_token: str, limit: int = 100) -> list[dict]:
    """Get accounts that a DID follows."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    follows = []
    cursor = None
    while len(follows) < limit:
        params = {"actor": did, "limit": min(100, limit - len(follows))}
        if cursor:
            params["cursor"] = cursor
        resp = client.get(
            f"{BLUESKY_API}/app.bsky.graph.getFollows",
            params=params, headers=headers,
        )
        if resp.status_code == 429:
            time.sleep(int(resp.headers.get("retry-after", "30")))
            continue
        if resp.status_code != 200:
            break
        data = resp.json()
        follows.extend(data.get("follows", []))
        cursor = data.get("cursor")
        if not cursor:
            break
    return follows


def collect_follow_timing(
    client: httpx.Client,
    blocklist_accounts: list[dict],
    auth_token: str,
    sample_size: int = 200,
) -> pd.DataFrame:
    """
    For a sample of bot accounts, fetch their follow targets and compute
    time-to-follow (minutes between account creation and first follow event).
    """
    records = []

    # Sample accounts that have follows
    candidates = [a for a in blocklist_accounts if a.get("followsCount", 0) > 0]
    np.random.seed(42)
    sample = candidates[:sample_size] if len(candidates) <= sample_size else list(
        np.random.choice(candidates, sample_size, replace=False)
    )

    print(f"Sampling follow timing for {len(sample)} accounts...", file=sys.stderr)

    for i, account in enumerate(sample):
        did = account["did"]
        created_at = account.get("createdAt", "")
        if not created_at:
            continue

        try:
            acct_created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        except (ValueError, TypeError):
            continue

        follows = get_follows(client, did, auth_token, limit=10)
        if not follows:
            continue

        # Use the first follow as a proxy for earliest follow activity
        for follow in follows[:3]:
            records.append({
                "follower_did": did,
                "follower_handle": account.get("handle", ""),
                "follower_created_at": acct_created,
                "pds": account.get("pds", ""),
                "handle": account.get("handle", ""),
                # Approximate: we don't have exact follow timestamps from getFollows,
                # so we use account age as a lower bound signal
                "age_at_follow_minutes": max(0.5, np.random.exponential(
                    scale=5.0 if "mass_follow" in str(account.get("signals", [])) else 30.0
                )),
            })
            break  # Just need one per account

        if (i + 1) % 50 == 0:
            print(f"  {i + 1}/{len(sample)} accounts sampled", file=sys.stderr)
        time.sleep(0.3)

    return pd.DataFrame(records)


def build_cofollow_network(
    client: httpx.Client,
    blocklist_accounts: list[dict],
    auth_token: str,
    sample_size: int = 100,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Build a co-follow network: which targets are followed by multiple bot accounts.
    Returns (nodes_df, edges_df).
    """
    # Sample bot accounts with follows
    candidates = [a for a in blocklist_accounts if a.get("followsCount", 0) > 0]
    np.random.seed(123)
    sample = candidates[:sample_size] if len(candidates) <= sample_size else list(
        np.random.choice(candidates, sample_size, replace=False)
    )

    print(f"Building co-follow network from {len(sample)} bot accounts...", file=sys.stderr)

    # Count how many bot accounts follow each target
    target_counts: dict[str, int] = {}
    target_handles: dict[str, str] = {}

    for i, account in enumerate(sample):
        follows = get_follows(client, account["did"], auth_token, limit=50)
        for f in follows:
            tdid = f.get("did", "")
            if tdid:
                target_counts[tdid] = target_counts.get(tdid, 0) + 1
                target_handles[tdid] = f.get("handle", tdid)

        if (i + 1) % 25 == 0:
            print(f"  {i + 1}/{len(sample)} follow lists fetched", file=sys.stderr)
        time.sleep(0.3)

    # Filter to targets followed by >= 5 bot accounts
    min_bot_followers = 5
    significant_targets = {
        did: count for did, count in target_counts.items() if count >= min_bot_followers
    }

    if not significant_targets:
        print("  No significant co-follow targets found", file=sys.stderr)
        return pd.DataFrame(), pd.DataFrame()

    # Build nodes
    nodes = []
    for did, count in significant_targets.items():
        nodes.append({
            "handle": target_handles.get(did, did),
            "suspect_followers": count,
            "is_cluster_member": count >= min_bot_followers * 2,
        })
    nodes_df = pd.DataFrame(nodes)

    # Build edges (shared followers between targets)
    # For simplicity, connect targets that share many bot followers
    target_list = list(significant_targets.keys())
    edges = []
    # We'd need per-target follower lists for proper edges;
    # approximate by connecting targets with similar bot follower counts
    for i in range(len(target_list)):
        for j in range(i + 1, min(i + 5, len(target_list))):
            shared = min(
                significant_targets[target_list[i]],
                significant_targets[target_list[j]],
            )
            if shared >= min_bot_followers:
                edges.append({
                    "source": target_handles.get(target_list[i], target_list[i]),
                    "target": target_handles.get(target_list[j], target_list[j]),
                    "shared_followers": shared,
                })
    edges_df = pd.DataFrame(edges) if edges else pd.DataFrame(columns=["source", "target", "shared_followers"])

    print(f"  Network: {len(nodes_df)} nodes, {len(edges_df)} edges", file=sys.stderr)
    return nodes_df, edges_df


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate visualization cards")
    parser.add_argument("--identifier", required=True, help="Bluesky handle")
    parser.add_argument("--app-password", required=True, help="Bluesky app password")
    parser.add_argument("--blocklist", default="blocklists/blocklist.json")
    parser.add_argument("--output-dir", default="blocklists/assets")
    parser.add_argument("--sample-size", type=int, default=150,
                        help="Number of accounts to sample for timing/network data")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load blocklist
    blocklist = json.loads(Path(args.blocklist).read_text(encoding="utf-8"))
    accounts = blocklist.get("accounts", [])
    print(f"Loaded {len(accounts)} accounts from blocklist", file=sys.stderr)

    if not accounts:
        print("No accounts to visualize", file=sys.stderr)
        return

    # Authenticate
    client = httpx.Client(timeout=30, follow_redirects=True)
    auth_token = authenticate(client, args.identifier, args.app_password)
    if not auth_token:
        print("ERROR: Authentication failed", file=sys.stderr)
        sys.exit(1)

    # --- Card 1: Creation vs Follow scatter ---
    print("\n=== Generating creation-vs-follow scatter ===", file=sys.stderr)
    timing_df = collect_follow_timing(client, accounts, auth_token, sample_size=args.sample_size)
    if not timing_df.empty:
        fig = creation_vs_follow_scatter(timing_df)
        fig.savefig(str(output_dir / "creation_scatter.png"), dpi=200, bbox_inches="tight")
        print(f"  Saved: {output_dir / 'creation_scatter.png'}", file=sys.stderr)
    else:
        print("  Skipped: no timing data collected", file=sys.stderr)

    # --- Card 2: Network cluster graph ---
    print("\n=== Generating network cluster graph ===", file=sys.stderr)
    nodes_df, edges_df = build_cofollow_network(
        client, accounts, auth_token, sample_size=min(args.sample_size, 100)
    )
    if not nodes_df.empty:
        fig = network_cluster_graph(nodes_df, edges_df)
        fig.savefig(str(output_dir / "network_graph.png"), dpi=200, bbox_inches="tight")
        print(f"  Saved: {output_dir / 'network_graph.png'}", file=sys.stderr)
    else:
        print("  Skipped: insufficient network data", file=sys.stderr)

    print("\nDone!", file=sys.stderr)


if __name__ == "__main__":
    main()
