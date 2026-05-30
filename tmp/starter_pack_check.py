"""
Check whether the 11 target accounts appear in any starter packs.
If targets are in a common starter pack, that could explain the co-follow pattern
as organic new-user onboarding rather than bot activity.
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

targets = cluster_data["targets"]
bot_dids = cluster_data["dids"]

print("=" * 70)
print("STARTER PACK ANALYSIS")
print("=" * 70)

# Step 1: Check if any target has created starter packs
print("\n--- Checking starter packs CREATED by target accounts ---")
all_starter_packs = []
for t in targets:
    if t["handle"] == "bsky.app":
        continue  # skip the default bsky follow
    time.sleep(0.3)
    try:
        r = client.get(
            f"{BSKY_API}/app.bsky.graph.getActorStarterPacks",
            params={"actor": t["did"], "limit": 50},
        )
        r.raise_for_status()
        packs = r.json().get("starterPacks", [])
        if packs:
            print(f"\n  @{t['handle']} created {len(packs)} starter pack(s):")
            for sp in packs:
                uri = sp.get("uri", "")
                name = sp.get("record", {}).get("name", "?")
                desc = sp.get("record", {}).get("description", "")[:80]
                joined = sp.get("joinedAllTimeCount", 0)
                list_uri = sp.get("record", {}).get("list", "")
                print(f"    - '{name}' (joined: {joined})")
                if desc:
                    print(f"      Desc: {desc}")
                all_starter_packs.append({
                    "uri": uri,
                    "name": name,
                    "creator": t["handle"],
                    "creator_did": t["did"],
                    "joined_count": joined,
                    "list_uri": list_uri,
                })
        else:
            print(f"  @{t['handle']}: no starter packs")
    except Exception as e:
        print(f"  @{t['handle']}: ERROR - {e}")

# Step 2: For each starter pack found, check if other targets are in it
if all_starter_packs:
    print(f"\n\n--- Checking starter pack contents for target overlap ---")
    target_dids = set(t["did"] for t in targets)
    
    for sp in all_starter_packs:
        print(f"\n  Starter Pack: '{sp['name']}' by @{sp['creator']}")
        # Get the list contents
        list_uri = sp.get("list_uri", "")
        if not list_uri:
            print("    No list URI found")
            continue
        
        time.sleep(0.3)
        try:
            # Get list items
            cursor = None
            members = []
            while True:
                params = {"list": list_uri, "limit": 100}
                if cursor:
                    params["cursor"] = cursor
                r = client.get(f"{BSKY_API}/app.bsky.graph.getList", params=params)
                r.raise_for_status()
                data = r.json()
                items = data.get("items", [])
                members.extend(items)
                cursor = data.get("cursor")
                if not cursor or not items:
                    break
                time.sleep(0.3)
            
            member_dids = set(item["subject"]["did"] for item in members)
            member_handles = {item["subject"]["did"]: item["subject"].get("handle", "?") for item in members}
            
            # Check overlap with targets
            target_overlap = target_dids.intersection(member_dids)
            bot_overlap = set(bot_dids).intersection(member_dids)
            
            print(f"    Total members: {len(members)}")
            print(f"    Target accounts in this pack: {len(target_overlap)}/{len(target_dids)}")
            if target_overlap:
                for d in target_overlap:
                    h = member_handles.get(d, next((t["handle"] for t in targets if t["did"] == d), "?"))
                    print(f"      - @{h}")
            print(f"    Bot accounts in this pack: {len(bot_overlap)}")
            if bot_overlap:
                for d in list(bot_overlap)[:10]:
                    print(f"      - @{member_handles.get(d, d[:30])}")
            
            # Check how many bots could have joined via this pack
            if len(target_overlap) >= 3:
                print(f"\n    ⚠️  SIGNIFICANT: {len(target_overlap)} targets in same starter pack!")
                print(f"    This could explain co-follow pattern for bots joining via this pack.")
                print(f"    Pack has {sp['joined_count']} total joins.")
            
        except Exception as e:
            print(f"    ERROR fetching list: {e}")

# Step 3: Check if bot accounts show starter pack join info in their profiles
print(f"\n\n--- Checking if bot profiles reference a starter pack ---")
# The associated starter pack appears in the profile if the user joined via one
sample_bots = bot_dids[:25]
params = [("actors", d) for d in sample_bots]
try:
    r = client.get(f"{BSKY_API}/app.bsky.actor.getProfiles", params=params)
    r.raise_for_status()
    sp_joiners = []
    for p in r.json().get("profiles", []):
        associated = p.get("associated", {})
        starter_pack = associated.get("starterPack") or p.get("joinedViaStarterPack")
        if starter_pack:
            sp_joiners.append((p.get("handle", "?"), starter_pack))
    
    if sp_joiners:
        print(f"  {len(sp_joiners)} bots joined via a starter pack:")
        for handle, sp in sp_joiners:
            if isinstance(sp, dict):
                print(f"    @{handle} -> '{sp.get('record', {}).get('name', '?')}' by @{sp.get('creator', {}).get('handle', '?')}")
            else:
                print(f"    @{handle} -> {sp}")
    else:
        print(f"  None of the first 25 bots show starter pack join info.")
except Exception as e:
    print(f"  ERROR: {e}")

# Check next batch
sample_bots2 = bot_dids[25:50]
if sample_bots2:
    time.sleep(0.3)
    params = [("actors", d) for d in sample_bots2]
    try:
        r = client.get(f"{BSKY_API}/app.bsky.actor.getProfiles", params=params)
        r.raise_for_status()
        for p in r.json().get("profiles", []):
            associated = p.get("associated", {})
            starter_pack = associated.get("starterPack") or p.get("joinedViaStarterPack")
            if starter_pack:
                if isinstance(starter_pack, dict):
                    print(f"    @{p.get('handle', '?')} -> '{starter_pack.get('record', {}).get('name', '?')}' by @{starter_pack.get('creator', {}).get('handle', '?')}")
                else:
                    print(f"    @{p.get('handle', '?')} -> {starter_pack}")
    except Exception as e:
        print(f"  ERROR batch 2: {e}")

# Check last batch
sample_bots3 = bot_dids[50:]
if sample_bots3:
    time.sleep(0.3)
    params = [("actors", d) for d in sample_bots3]
    try:
        r = client.get(f"{BSKY_API}/app.bsky.actor.getProfiles", params=params)
        r.raise_for_status()
        for p in r.json().get("profiles", []):
            associated = p.get("associated", {})
            starter_pack = associated.get("starterPack") or p.get("joinedViaStarterPack")
            if starter_pack:
                if isinstance(starter_pack, dict):
                    print(f"    @{p.get('handle', '?')} -> '{starter_pack.get('record', {}).get('name', '?')}' by @{starter_pack.get('creator', {}).get('handle', '?')}")
                else:
                    print(f"    @{p.get('handle', '?')} -> {starter_pack}")
    except Exception as e:
        print(f"  ERROR batch 3: {e}")

print(f"\n{'='*70}")
print("CONCLUSION")
print("=" * 70)

client.close()
