"""
Check if target accounts appear together in any popular public lists.
A shared list could be used as follow-source by automation.
"""
import json
import sys
import time

import httpx

sys.path.insert(0, r"C:\Users\clemensv\OneDrive - Microsoft\Agents\nius")

BSKY_API = "https://public.api.bsky.app/xrpc"
client = httpx.Client(timeout=30)

with open(r"d:\bskyhygiene\investigations\2026-05-30-german-literary-bots\bot_dids.json") as f:
    cluster_data = json.load(f)

targets = [t for t in cluster_data["targets"] if t["handle"] != "bsky.app"]

print("=" * 70)
print("SHARED LIST ANALYSIS — do targets appear in common lists?")
print("=" * 70)

# For each target, get the lists they appear in (as subject)
# app.bsky.graph.getLists only shows lists created by an actor
# There's no direct "what lists is this user on?" endpoint
# But we can check via searchPosts or other means

# Alternative approach: Check if any target account has lists on their profile
# that contain other targets
print("\n--- Checking lists CREATED by targets that contain other targets ---")

target_dids = set(t["did"] for t in targets)

for t in targets:
    time.sleep(0.3)
    try:
        r = client.get(
            f"{BSKY_API}/app.bsky.graph.getLists",
            params={"actor": t["did"], "limit": 50},
        )
        r.raise_for_status()
        lists = r.json().get("lists", [])
        if lists:
            for lst in lists:
                purpose = lst.get("purpose", "")
                name = lst.get("name", "?")
                uri = lst.get("uri", "")
                list_item_count = lst.get("listItemCount", 0)
                # Only check curate lists (not mod lists)
                if "curatelist" in purpose or list_item_count > 0:
                    print(f"\n  @{t['handle']} -> List: '{name}' ({list_item_count} items, {purpose})")
                    # Check contents
                    time.sleep(0.3)
                    try:
                        r2 = client.get(
                            f"{BSKY_API}/app.bsky.graph.getList",
                            params={"list": uri, "limit": 100},
                        )
                        r2.raise_for_status()
                        items = r2.json().get("items", [])
                        item_dids = set(item["subject"]["did"] for item in items)
                        overlap = target_dids.intersection(item_dids)
                        if len(overlap) > 1:
                            print(f"    ⚠️  Contains {len(overlap)} target accounts!")
                            for d in overlap:
                                h = next((t2["handle"] for t2 in targets if t2["did"] == d), d)
                                print(f"      - @{h}")
                        else:
                            print(f"    Contains {len(overlap)} target(s) — not significant")
                    except Exception as e:
                        print(f"    Error checking list: {e}")
    except Exception as e:
        print(f"  @{t['handle']}: ERROR - {e}")

# Step 2: Search for "Literatur" or "Kultur" starter packs/lists that might contain targets
print(f"\n\n--- Searching for popular German Literatur/Kultur lists ---")
# Use searchActors or a known German literary community account
# Check a few well-known accounts that curate German literary lists
curators = [
    "kattascha.bsky.social",
    "suhrkamp.de",
]
for curator in curators:
    time.sleep(0.3)
    try:
        r = client.get(
            f"{BSKY_API}/app.bsky.graph.getLists",
            params={"actor": curator, "limit": 50},
        )
        r.raise_for_status()
        lists = r.json().get("lists", [])
        for lst in lists:
            name = lst.get("name", "?")
            uri = lst.get("uri", "")
            count = lst.get("listItemCount", 0)
            print(f"\n  @{curator} -> '{name}' ({count} items)")
            if count > 5:
                time.sleep(0.3)
                r2 = client.get(f"{BSKY_API}/app.bsky.graph.getList", params={"list": uri, "limit": 100})
                r2.raise_for_status()
                items = r2.json().get("items", [])
                item_dids = set(item["subject"]["did"] for item in items)
                overlap = target_dids.intersection(item_dids)
                if overlap:
                    print(f"    Contains {len(overlap)} target(s):")
                    for d in overlap:
                        h = next((t2["handle"] for t2 in targets if t2["did"] == d), d)
                        print(f"      - @{h}")
    except Exception as e:
        print(f"  @{curator}: ERROR - {e}")

# Step 3: Check starter packs via search (look for German literary packs)
print(f"\n\n--- Searching for starter packs containing multiple targets ---")
# Try searching for packs via the suggestion endpoint
# Actually, let's check getActorStarterPacks for known curators
pack_curators = [
    "kattascha.bsky.social",
    "suhrkamp.de",
    "afelia.bsky.social",
    "golod.bsky.social",
    "buchkolumne.bsky.social",
    "54books.bsky.social",
]
for curator in pack_curators:
    time.sleep(0.3)
    try:
        r = client.get(
            f"{BSKY_API}/app.bsky.graph.getActorStarterPacks",
            params={"actor": curator, "limit": 50},
        )
        r.raise_for_status()
        packs = r.json().get("starterPacks", [])
        for sp in packs:
            name = sp.get("record", {}).get("name", "?")
            joined = sp.get("joinedAllTimeCount", 0)
            list_uri = sp.get("record", {}).get("list", "")
            if list_uri and joined > 0:
                print(f"\n  @{curator} -> '{name}' (joined: {joined})")
                time.sleep(0.3)
                r2 = client.get(f"{BSKY_API}/app.bsky.graph.getList", params={"list": list_uri, "limit": 100})
                r2.raise_for_status()
                items = r2.json().get("items", [])
                item_dids = set(item["subject"]["did"] for item in items)
                overlap = target_dids.intersection(item_dids)
                if overlap:
                    print(f"    Contains {len(overlap)} target(s):")
                    for d in overlap:
                        h = next((t2["handle"] for t2 in targets if t2["did"] == d), d)
                        print(f"      - @{h}")
                else:
                    print(f"    No target overlap")
    except Exception as e:
        print(f"  @{curator}: {e}")

print(f"\n{'='*70}")
print("SUMMARY")
print("=" * 70)
client.close()
