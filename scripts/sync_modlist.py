"""
Bluesky Moderation List Sync

Syncs the local blocklist.json to a Bluesky moderation list (app.bsky.graph.list).
Creates the list if it doesn't exist, then adds/removes members to match the blocklist.

Usage:
    python scripts/sync_modlist.py \
        --identifier <handle> \
        --app-password <app-password> \
        --blocklist blocklists/blocklist.json \
        --list-name "Bot Infrastructure Blocklist"
"""

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx

BLUESKY_API = "https://bsky.social/xrpc"


class BlueskyClient:
    """Minimal Bluesky AT Protocol client for moderation list operations."""

    def __init__(self, identifier: str, app_password: str):
        self.client = httpx.Client(timeout=30, follow_redirects=True)
        self.access_token = None
        self.did = None
        self._authenticate(identifier, app_password)

    def _authenticate(self, identifier: str, app_password: str):
        resp = self.client.post(
            f"{BLUESKY_API}/com.atproto.server.createSession",
            json={"identifier": identifier, "password": app_password},
        )
        resp.raise_for_status()
        data = resp.json()
        self.access_token = data["accessJwt"]
        self.did = data["did"]
        print(f"Authenticated as {data['handle']} ({self.did})", file=sys.stderr)

    def _headers(self) -> dict:
        return {"Authorization": f"Bearer {self.access_token}"}

    def _rate_limit_wait(self, resp: httpx.Response):
        if resp.status_code == 429:
            wait = int(resp.headers.get("retry-after", "30"))
            print(f"  Rate limited, waiting {wait}s...", file=sys.stderr)
            time.sleep(wait)
            return True
        return False

    def get_lists(self) -> list[dict]:
        """Get all lists owned by the authenticated user."""
        lists = []
        cursor = None
        while True:
            params = {"actor": self.did, "limit": 100}
            if cursor:
                params["cursor"] = cursor
            resp = self.client.get(
                f"{BLUESKY_API}/app.bsky.graph.getLists",
                params=params,
                headers=self._headers(),
            )
            if self._rate_limit_wait(resp):
                continue
            resp.raise_for_status()
            data = resp.json()
            lists.extend(data.get("lists", []))
            cursor = data.get("cursor")
            if not cursor:
                break
        return lists

    def find_list_by_name(self, name: str) -> dict | None:
        """Find a moderation list by name."""
        for lst in self.get_lists():
            if lst.get("name") == name and lst.get("purpose") == "app.bsky.graph.defs#modlist":
                return lst
        return None

    def create_list(self, name: str, description: str) -> str:
        """Create a new moderation list. Returns the list URI."""
        record = {
            "$type": "app.bsky.graph.list",
            "name": name,
            "purpose": "app.bsky.graph.defs#modlist",
            "description": description,
            "createdAt": datetime.now(timezone.utc).isoformat(),
        }
        resp = self.client.post(
            f"{BLUESKY_API}/com.atproto.repo.createRecord",
            json={
                "repo": self.did,
                "collection": "app.bsky.graph.list",
                "record": record,
            },
            headers=self._headers(),
        )
        resp.raise_for_status()
        data = resp.json()
        print(f"Created moderation list: {data['uri']}", file=sys.stderr)
        return data["uri"]

    def get_list_items(self, list_uri: str) -> dict[str, str]:
        """Get all items in a list. Returns {did: record_uri}."""
        items = {}
        cursor = None
        while True:
            params = {"list": list_uri, "limit": 100}
            if cursor:
                params["cursor"] = cursor
            resp = self.client.get(
                f"{BLUESKY_API}/app.bsky.graph.getList",
                params=params,
                headers=self._headers(),
            )
            if self._rate_limit_wait(resp):
                continue
            resp.raise_for_status()
            data = resp.json()
            for item in data.get("items", []):
                subject_did = item.get("subject", {}).get("did")
                item_uri = item.get("uri")
                if subject_did and item_uri:
                    items[subject_did] = item_uri
            cursor = data.get("cursor")
            if not cursor:
                break
        return items

    def add_to_list(self, list_uri: str, subject_did: str) -> str:
        """Add a DID to a moderation list."""
        record = {
            "$type": "app.bsky.graph.listitem",
            "list": list_uri,
            "subject": subject_did,
            "createdAt": datetime.now(timezone.utc).isoformat(),
        }
        while True:
            resp = self.client.post(
                f"{BLUESKY_API}/com.atproto.repo.createRecord",
                json={
                    "repo": self.did,
                    "collection": "app.bsky.graph.listitem",
                    "record": record,
                },
                headers=self._headers(),
            )
            if self._rate_limit_wait(resp):
                continue
            resp.raise_for_status()
            return resp.json()["uri"]

    def remove_from_list(self, record_uri: str):
        """Remove an item from a moderation list by its record URI."""
        # Parse the rkey from the URI: at://did/collection/rkey
        parts = record_uri.replace("at://", "").split("/")
        repo = parts[0]
        collection = parts[1]
        rkey = parts[2]
        while True:
            resp = self.client.post(
                f"{BLUESKY_API}/com.atproto.repo.deleteRecord",
                json={
                    "repo": repo,
                    "collection": collection,
                    "rkey": rkey,
                },
                headers=self._headers(),
            )
            if self._rate_limit_wait(resp):
                continue
            resp.raise_for_status()
            return


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Sync blocklist to Bluesky moderation list")
    parser.add_argument("--identifier", required=True, help="Bluesky handle or DID")
    parser.add_argument("--app-password", required=True, help="Bluesky app password")
    parser.add_argument(
        "--blocklist", default="blocklists/blocklist.json", help="Path to blocklist JSON"
    )
    parser.add_argument(
        "--list-name",
        default="Bot Infrastructure Blocklist",
        help="Name of the moderation list on Bluesky",
    )
    parser.add_argument(
        "--list-description",
        default="Automated blocklist of accounts from confirmed bot PDS infrastructure. Updated daily. See https://github.com/clemensv/bskyhygiene",
        help="Description for the moderation list",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would be done without making changes"
    )
    args = parser.parse_args()

    # Load blocklist
    blocklist_path = Path(args.blocklist)
    if not blocklist_path.exists():
        print(f"ERROR: Blocklist not found: {blocklist_path}", file=sys.stderr)
        sys.exit(1)

    blocklist_data = json.loads(blocklist_path.read_text(encoding="utf-8"))
    target_dids = set(account["did"] for account in blocklist_data.get("accounts", []))
    print(f"Blocklist contains {len(target_dids)} DIDs", file=sys.stderr)

    if args.dry_run:
        print("[DRY RUN] Would sync these DIDs to moderation list:", file=sys.stderr)
        print(f"  List name: {args.list_name}", file=sys.stderr)
        print(f"  Total to add: {len(target_dids)}", file=sys.stderr)
        return

    # Connect to Bluesky
    bsky = BlueskyClient(args.identifier, args.app_password)

    # Find or create the moderation list
    existing_list = bsky.find_list_by_name(args.list_name)
    if existing_list:
        list_uri = existing_list["uri"]
        print(f"Found existing list: {list_uri}", file=sys.stderr)
    else:
        list_uri = bsky.create_list(args.list_name, args.list_description)

    # Get current list members
    current_items = bsky.get_list_items(list_uri)
    current_dids = set(current_items.keys())
    print(f"Current list has {len(current_dids)} members", file=sys.stderr)

    # Calculate diff
    to_add = target_dids - current_dids
    to_remove = current_dids - target_dids

    print(f"  To add:    {len(to_add)}", file=sys.stderr)
    print(f"  To remove: {len(to_remove)}", file=sys.stderr)
    print(f"  Unchanged: {len(current_dids & target_dids)}", file=sys.stderr)

    # Remove accounts no longer on blocklist
    for i, did in enumerate(to_remove):
        record_uri = current_items[did]
        bsky.remove_from_list(record_uri)
        if (i + 1) % 50 == 0:
            print(f"  Removed {i + 1}/{len(to_remove)}", file=sys.stderr)
        time.sleep(0.2)

    if to_remove:
        print(f"  Removed {len(to_remove)} accounts from list", file=sys.stderr)

    # Add new accounts
    for i, did in enumerate(to_add):
        bsky.add_to_list(list_uri, did)
        if (i + 1) % 50 == 0:
            print(f"  Added {i + 1}/{len(to_add)}", file=sys.stderr)
        time.sleep(0.2)

    if to_add:
        print(f"  Added {len(to_add)} accounts to list", file=sys.stderr)

    print(f"\n{'='*60}", file=sys.stderr)
    print(f"DONE: Moderation list synced ({len(target_dids)} total members)", file=sys.stderr)
    print(f"List URI: {list_uri}", file=sys.stderr)


if __name__ == "__main__":
    main()
