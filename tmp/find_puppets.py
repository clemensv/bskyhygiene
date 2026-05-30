import sys, json, urllib.request
sys.path.insert(0, r'C:\Users\clemensv\OneDrive - Microsoft\Agents\nius\nius_bot_dossier')
from kusto_client import get_client

client = get_client()
db = "bluesky"

# Find ALL accounts with >5000 blocks that overlap significantly with smatsto
# Then we'll check their profiles to find puppets
print("=== Finding all high-volume blockers sharing smatsto's list ===\n")

q = """
let smatsto_blocks = ['Bluesky.Graph.Block_v1']
    | where did == "did:plc:gjcwwrezaz5qdcjn3347qvtl"
    | distinct subject;
let known = dynamic([
    "did:plc:kd4wtd75a637g2gvg2dh2b3t",
    "did:plc:gjcwwrezaz5qdcjn3347qvtl",
    "did:plc:qildfzoh5p24jgion4xiycvz",
    "did:plc:xcytuwwb3b33ipiqzmqzbs45",
    "did:plc:hwpiekun4iebo4oqevjfe6ss",
    "did:plc:tfspkb2htmw7vwdgqj7mzx7m",
    "did:plc:3c7r453vexmpwu6nheazyikk",
    "did:plc:u4e3ytzjxb7vapbdmr4oz7ld",
    "did:plc:5v7itrhmq6zhvpqn2sfmcwaw",
    "did:plc:l3fkqug2hhn4upcdewogsijh",
    "did:plc:vb6p4kuz3kmtqrcix2ghjkwf",
    "did:plc:oqc7737mwl6y22wjqdduujex",
    "did:plc:qbw4i5hcyc6dtuckixaogxlc",
    "did:plc:dvhyaxbrf7uh6eemujbd4jao",
    "did:plc:qq2eg3kbh44gytxlghozodeb",
    "did:plc:5sjri67leyvnlenx7tzgfulk"
]);
['Bluesky.Graph.Block_v1']
| where did !in (known)
| where subject in (smatsto_blocks)
| summarize shared_blocks = dcount(subject), total_blocks = count() by did
| where shared_blocks > 500
| order by shared_blocks desc
| take 50
"""

result = client.execute(db, q)
rows = list(result.primary_results[0])
dids = [r['did'] for r in rows]
print(f"Found {len(dids)} accounts with >500 shared blocks with smatsto\n")

# Resolve profiles via Bluesky API
def resolve_profiles(dids):
    profiles = {}
    for i in range(0, len(dids), 25):
        batch = dids[i:i+25]
        params = "&".join(f"actors={d}" for d in batch)
        url = f"https://public.api.bsky.app/xrpc/app.bsky.actor.getProfiles?{params}"
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read())
                for p in data.get("profiles", []):
                    profiles[p["did"]] = p
        except Exception as e:
            print(f"  API error for batch starting {batch[0][:20]}: {e}")
    return profiles

profiles = resolve_profiles(dids)

# Identify puppets: low followers, low posts, high blocks
print(f"{'Handle':<35} {'Display':<20} {'Fllwrs':>6} {'Fllwng':>6} {'Posts':>6} {'Shared':>7} {'Total':>7} {'Labels'}")
print("-" * 130)

puppets = []
for r in rows:
    did = r['did']
    p = profiles.get(did, {})
    handle = p.get("handle", "???")
    display = (p.get("displayName", "") or "")[:19]
    followers = p.get("followersCount", "?")
    following = p.get("followsCount", "?")
    posts = p.get("postsCount", "?")
    labels = ", ".join(l.get("val", "") for l in p.get("labels", []))
    shared = r['shared_blocks']
    total = r['total_blocks']
    
    # Flag as puppet if: low followers AND high block ratio
    is_puppet = False
    if isinstance(followers, int) and isinstance(posts, int):
        if followers < 50 and total > 1000:
            is_puppet = True
        elif posts < 100 and total > 5000:
            is_puppet = True
    
    marker = " ◄ PUPPET" if is_puppet else ""
    print(f"{handle:<35} {display:<20} {followers:>6} {following:>6} {posts:>6} {shared:>7} {total:>7} {labels}{marker}")
    
    if is_puppet:
        puppets.append({
            "handle": handle, "display": display, 
            "followers": followers, "following": following,
            "posts": posts, "shared": shared, "total": total,
            "labels": labels, "did": did
        })

print(f"\n\n=== IDENTIFIED PUPPETS ({len(puppets)}) ===\n")
print(f"{'Handle':<35} {'Followers':>9} {'Posts':>6} {'Blocks':>7} {'Shared w/smatsto':>16}")
print("-" * 80)
for p in puppets:
    print(f"{p['handle']:<35} {p['followers']:>9} {p['posts']:>6} {p['total']:>7} {p['shared']:>16}")
