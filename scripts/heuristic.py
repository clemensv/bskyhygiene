"""
Bluesky Bot Heuristic Scanner

Scans CONFIRMED bot PDS clusters for coordinated inauthentic behavior.
Only targets PDS servers that have been positively identified as bot
infrastructure through investigation (shared test accounts, synchronized
bulk creation, identical handle templates, same operator evidence).

This is NOT a general-purpose bot detector. It is a targeted blocklist
generator for known-bad infrastructure.

Heuristic signals (each contributes to a 0-1 bot score):
- Profile completeness: no avatar, no description, no display name
- Handle generation patterns: firstname+number, random alphanumeric, adjective-noun
- Activity signals: zero posts, zero followers, high follow/follower ratio
- Network signals: follow-only behavior (many follows, zero posts)
"""

import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx

# --- Configuration ---
# Only confirmed bot infrastructure clusters go here.
# Each entry requires prior investigation proving coordinated inauthentic behavior.
TARGET_PDS_SERVERS = [
    "https://pds.louisvillebsky.app",
    "https://haruhwa.com",
]

BLUESKY_API = "https://bsky.social/xrpc"
BOT_SCORE_THRESHOLD = 0.45  # accounts scoring above this go on the blocklist

# --- Handle pattern detectors ---
PATTERN_FIRSTNAME_NUMBER = re.compile(
    r"^[a-z]{3,12}(?:[a-z]{3,12})?(?:\d{2,6})$", re.IGNORECASE
)
PATTERN_RANDOM_ALPHANUM = re.compile(r"^[a-z0-9]{7,12}$", re.IGNORECASE)
PATTERN_ADJECTIVE_NOUN = re.compile(
    r"^[a-z]{3,10}-[a-z]{3,10}$", re.IGNORECASE
)
PATTERN_COMPOUND_NUMBER = re.compile(
    r"^[a-z]{4,10}[a-z]{3,10}\d{3,6}$", re.IGNORECASE
)
PATTERN_CONSONANT_CLUSTER = re.compile(r"^[b-df-hj-np-tv-z]{4,8}$", re.IGNORECASE)


def detect_handle_pattern(handle: str) -> str:
    """Classify a handle into generation pattern categories."""
    local = handle.split(".")[0] if "." in handle else handle
    if PATTERN_CONSONANT_CLUSTER.match(local):
        return "consonant_cluster"
    if PATTERN_RANDOM_ALPHANUM.match(local):
        return "random_alphanum"
    if PATTERN_ADJECTIVE_NOUN.match(local):
        return "adjective_noun"
    if PATTERN_COMPOUND_NUMBER.match(local):
        return "compound_number"
    if PATTERN_FIRSTNAME_NUMBER.match(local):
        return "firstname_number"
    return "other"


def score_account(profile: dict, handle_pattern: str) -> tuple[float, list[str]]:
    """
    Compute a bot score (0.0 to 1.0) for an account.
    Returns (score, list_of_triggered_signals).
    """
    signals = []
    score = 0.0

    # --- Profile completeness (max 0.30) ---
    if not profile.get("avatar"):
        score += 0.10
        signals.append("no_avatar")
    if not profile.get("description"):
        score += 0.10
        signals.append("no_description")
    if not profile.get("displayName"):
        score += 0.10
        signals.append("no_display_name")

    # --- Handle pattern (max 0.25) ---
    pattern_scores = {
        "consonant_cluster": 0.25,
        "random_alphanum": 0.20,
        "compound_number": 0.15,
        "firstname_number": 0.10,
        "adjective_noun": 0.10,
        "other": 0.0,
    }
    pattern_score = pattern_scores.get(handle_pattern, 0.0)
    if pattern_score > 0:
        score += pattern_score
        signals.append(f"handle_pattern:{handle_pattern}")

    # --- Activity signals (max 0.30) ---
    posts_count = profile.get("postsCount", 0)
    followers_count = profile.get("followersCount", 0)
    follows_count = profile.get("followsCount", 0)

    if posts_count == 0:
        score += 0.15
        signals.append("zero_posts")
    elif posts_count <= 3:
        score += 0.08
        signals.append("very_few_posts")

    if followers_count == 0 and follows_count > 10:
        score += 0.15
        signals.append("follow_only_no_followers")
    elif follows_count > 0 and followers_count > 0:
        ratio = follows_count / followers_count
        if ratio > 10:
            score += 0.12
            signals.append(f"high_follow_ratio:{ratio:.1f}")
        elif ratio > 5:
            score += 0.06
            signals.append(f"elevated_follow_ratio:{ratio:.1f}")

    # --- Follow-only bot pattern (bonus 0.15) ---
    if follows_count > 50 and posts_count == 0:
        score += 0.15
        signals.append("mass_follow_zero_posts")

    return min(score, 1.0), signals


def list_pds_repos(client: httpx.Client, pds_url: str) -> list[str]:
    """List all DIDs hosted on a PDS server using com.atproto.sync.listRepos."""
    dids = []
    cursor = None
    while True:
        params = {"limit": 1000}
        if cursor:
            params["cursor"] = cursor
        try:
            resp = client.get(f"{pds_url}/xrpc/com.atproto.sync.listRepos", params=params)
            resp.raise_for_status()
        except httpx.HTTPError as e:
            print(f"  Error listing repos from {pds_url}: {e}", file=sys.stderr)
            break
        data = resp.json()
        repos = data.get("repos", [])
        for repo in repos:
            did = repo.get("did")
            if did:
                dids.append(did)
        cursor = data.get("cursor")
        if not cursor or not repos:
            break
    return dids


def get_profile(client: httpx.Client, did: str, auth_token: str | None = None) -> dict | None:
    """Fetch a profile from the Bluesky AppView."""
    headers = {}
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"
    try:
        resp = client.get(
            f"{BLUESKY_API}/app.bsky.actor.getProfile",
            params={"actor": did},
            headers=headers,
        )
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 429:
            retry_after = int(resp.headers.get("retry-after", "30"))
            print(f"  Rate limited, waiting {retry_after}s...", file=sys.stderr)
            time.sleep(retry_after)
            return get_profile(client, did, auth_token)
        else:
            return None
    except httpx.HTTPError:
        return None


def get_profiles_batch(client: httpx.Client, dids: list[str], auth_token: str | None = None) -> list[dict]:
    """Fetch up to 25 profiles in a single batch call."""
    headers = {}
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"
    try:
        resp = client.get(
            f"{BLUESKY_API}/app.bsky.actor.getProfiles",
            params=[("actors", did) for did in dids[:25]],
            headers=headers,
        )
        if resp.status_code == 200:
            return resp.json().get("profiles", [])
        elif resp.status_code == 429:
            retry_after = int(resp.headers.get("retry-after", "30"))
            print(f"  Rate limited, waiting {retry_after}s...", file=sys.stderr)
            time.sleep(retry_after)
            return get_profiles_batch(client, dids, auth_token)
        else:
            return []
    except httpx.HTTPError:
        return []


def authenticate(client: httpx.Client, identifier: str, app_password: str) -> str | None:
    """Authenticate to Bluesky and return an access token."""
    try:
        resp = client.post(
            f"{BLUESKY_API}/com.atproto.server.createSession",
            json={"identifier": identifier, "password": app_password},
        )
        if resp.status_code == 200:
            return resp.json().get("accessJwt")
        else:
            print(f"Auth failed: {resp.status_code} {resp.text}", file=sys.stderr)
            return None
    except httpx.HTTPError as e:
        print(f"Auth error: {e}", file=sys.stderr)
        return None


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Bluesky Bot Heuristic Scanner")
    parser.add_argument("--identifier", help="Bluesky handle or DID for auth")
    parser.add_argument("--app-password", help="Bluesky app password")
    parser.add_argument(
        "--output", default="blocklists/blocklist.json", help="Output blocklist path"
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=BOT_SCORE_THRESHOLD,
        help="Bot score threshold (default: 0.45)",
    )
    parser.add_argument(
        "--clusters", default="clusters.json", help="Path to clusters config file"
    )
    args = parser.parse_args()

    # Load cluster config (PDS servers to scan + allowlist)
    clusters_path = Path(args.clusters)
    if clusters_path.exists():
        clusters_config = json.loads(clusters_path.read_text(encoding="utf-8"))
        pds_servers = [c["url"] for c in clusters_config.get("clusters", [])]
        allowlist_dids = set(clusters_config.get("allowlist_dids", []))
        allowlist_handles = set(h.lower() for h in clusters_config.get("allowlist_handles", []))
    else:
        pds_servers = TARGET_PDS_SERVERS
        allowlist_dids = set()
        allowlist_handles = set()
        print(f"WARNING: {clusters_path} not found, using built-in defaults", file=sys.stderr)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    client = httpx.Client(timeout=30, follow_redirects=True)
    auth_token = None

    if args.identifier and args.app_password:
        print("Authenticating...", file=sys.stderr)
        auth_token = authenticate(client, args.identifier, args.app_password)
        if auth_token:
            print("Authenticated successfully", file=sys.stderr)
        else:
            print("WARNING: Auth failed, continuing without auth (rate limits apply)", file=sys.stderr)

    all_results = []
    scan_time = datetime.now(timezone.utc).isoformat()

    for pds_url in pds_servers:
        pds_name = pds_url.replace("https://", "")
        print(f"\n{'='*60}", file=sys.stderr)
        print(f"Scanning PDS: {pds_name}", file=sys.stderr)
        print(f"{'='*60}", file=sys.stderr)

        # List all repos on the PDS
        dids = list_pds_repos(client, pds_url)
        print(f"  Found {len(dids)} DIDs on {pds_name}", file=sys.stderr)

        # Fetch profiles in batches of 25
        processed = 0
        for i in range(0, len(dids), 25):
            batch = dids[i : i + 25]
            profiles = get_profiles_batch(client, batch, auth_token)

            for profile in profiles:
                did = profile.get("did", "")
                handle = profile.get("handle", "")

                # Skip allowlisted accounts
                if did in allowlist_dids or handle.lower() in allowlist_handles:
                    continue

                handle_pattern = detect_handle_pattern(handle)
                bot_score, signals = score_account(profile, handle_pattern)

                entry = {
                    "did": did,
                    "handle": handle,
                    "displayName": profile.get("displayName", ""),
                    "pds": pds_name,
                    "botScore": round(bot_score, 3),
                    "signals": signals,
                    "handlePattern": handle_pattern,
                    "postsCount": profile.get("postsCount", 0),
                    "followersCount": profile.get("followersCount", 0),
                    "followsCount": profile.get("followsCount", 0),
                    "createdAt": profile.get("createdAt", ""),
                }

                if bot_score >= args.threshold:
                    all_results.append(entry)

            processed += len(batch)
            if processed % 100 == 0:
                print(
                    f"  Processed {processed}/{len(dids)} ({len(all_results)} flagged so far)",
                    file=sys.stderr,
                )

            # Small delay to be respectful of rate limits
            time.sleep(0.5)

    # Sort by bot score descending
    all_results.sort(key=lambda x: x["botScore"], reverse=True)

    # Build output
    blocklist = {
        "metadata": {
            "generated_at": scan_time,
            "threshold": args.threshold,
            "total_flagged": len(all_results),
            "pds_servers_scanned": [u.replace("https://", "") for u in pds_servers],
            "allowlisted": len(allowlist_dids) + len(allowlist_handles),
            "heuristic_version": "1.1",
        },
        "accounts": all_results,
    }

    # Write JSON blocklist
    output_path.write_text(json.dumps(blocklist, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"DONE: {len(all_results)} accounts flagged (threshold: {args.threshold})", file=sys.stderr)
    print(f"Output: {output_path}", file=sys.stderr)

    # Also write a simple DID-only list for easy import
    did_list_path = output_path.with_suffix(".txt")
    did_list_path.write_text(
        "\n".join(entry["did"] for entry in all_results) + "\n", encoding="utf-8"
    )
    print(f"DID list: {did_list_path}", file=sys.stderr)

    # Write summary stats
    high = sum(1 for a in all_results if a["botScore"] >= 0.7)
    medium = sum(1 for a in all_results if 0.45 <= a["botScore"] < 0.7)
    print(f"\nScore distribution:", file=sys.stderr)
    print(f"  High (>=0.7):    {high}", file=sys.stderr)
    print(f"  Medium (0.45-0.7): {medium}", file=sys.stderr)


if __name__ == "__main__":
    main()
