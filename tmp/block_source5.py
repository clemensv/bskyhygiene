import sys
sys.path.insert(0, r'C:\Users\clemensv\OneDrive - Microsoft\Agents\nius')
from nius_bot_dossier.kusto_client import execute_query
import requests

DID = 'did:plc:kd4wtd75a637g2gvg2dh2b3t'

# did:plc:4llrhdclvdlmmynkwsmg5tdc appears 8 times in top reply targets
# Let's resolve the key accounts whose posts victims engage with
print("=== RESOLVING KEY POST AUTHORS THAT VICTIMS ENGAGE WITH ===")
key_dids = [
    'did:plc:4llrhdclvdlmmynkwsmg5tdc',  # 8x in top 20 reply targets
    'did:plc:t6ubj2wlhc34awzcymh3qpur',  # 3x in top 20
    'did:plc:7qqkq2zdwq4j5jingukgtuky',  # Top reply target (560 repliers)
    'did:plc:udnac33pmf2iwcblpeai5a5p',  # #2 (463 repliers)
    'did:plc:vuwppziky7qk4aqhwx7nz424',  # 403 repliers
    'did:plc:sk6jryjhuavqchpa53jlcsyu',  # 402 repliers
]
params = [('actors[]', d) for d in key_dids]
r = requests.get('https://public.api.bsky.app/xrpc/app.bsky.actor.getProfiles', params=params)
if r.status_code == 200:
    for p in r.json().get('profiles', []):
        handle = p.get('handle', '?')
        display = p.get('displayName', '')
        followers = p.get('followersCount', 0)
        desc = (p.get('description') or '')[:100]
        print(f"  {handle:40s} | {display:30s} | F:{followers:>7} | {desc}")

# Now the critical question: Are they blocking EVERYONE who replies to these viral posts?
# Or are they using a different discovery mechanism?
# Check: What percentage of repliers to the top viral post got blocked?
print("\n\n=== WHAT % OF REPLIERS TO TOP VIRAL POSTS GOT BLOCKED? ===")
top_posts = [
    'at://did:plc:7qqkq2zdwq4j5jingukgtuky/app.bsky.feed.post/3mkt2mns3n22u',
    'at://did:plc:4llrhdclvdlmmynkwsmg5tdc/app.bsky.feed.post/3mmbv46us452m',
    'at://did:plc:t6ubj2wlhc34awzcymh3qpur/app.bsky.feed.post/3mliqlkwdoc2i',
]
for post_uri in top_posts:
    q = f"""
    let repliers = ['Bluesky.Feed.Post_v1']
    | where reply_root == '{post_uri}'
    | distinct did;
    let total_repliers = toscalar(repliers | count);
    let blocked_repliers = toscalar(
        ['Bluesky.Graph.Block_v1']
        | where did == '{DID}'
        | where subject in (repliers)
        | distinct subject
        | count
    );
    print total_repliers, blocked_repliers, pct = round(100.0 * blocked_repliers / total_repliers, 1)
    """
    df = execute_query(q)
    print(f"  Post: ...{post_uri[-20:]} | Total repliers: {df.iloc[0, 0]:>5} | Blocked: {df.iloc[0, 1]:>5} | {df.iloc[0, 2]}%")

# Final check: Is there a moderation list or external tool being used?
# Check the ALL ring members: how many total UNIQUE people do they block together?
print("\n\n=== TOTAL UNIQUE BLOCKS ACROSS ALL RING MEMBERS ===")
ring = [
    DID,
    'did:plc:gjcwwrezaz5qdcjn3347qvtl',
    'did:plc:qildfzoh5p24jgion4xiycvz',
    'did:plc:xcytuwwb3b33ipiqzmqzbs45',
    'did:plc:hwpiekun4iebo4oqevjfe6ss',
    'did:plc:tfspkb2htmw7vwdgqj7mzx7m',
]
dids_str = "', '".join(ring)
q_total = f"""
['Bluesky.Graph.Block_v1']
| where did in ('{dids_str}')
| summarize total_blocks = count(), unique_targets = dcount(subject)
"""
df_total = execute_query(q_total)
print(df_total.to_string())

# How many are blocked by ALL 6 members? (shared core list)
q_core = f"""
['Bluesky.Graph.Block_v1']
| where did in ('{dids_str}')
| summarize blockers = dcount(did) by subject
| summarize targets_by_blocker_count = count() by blockers
| order by blockers desc
"""
df_core = execute_query(q_core)
print("\nTargets by how many ring members block them:")
print(df_core.to_string())

# What % of Louis's blocks are also blocked by at least 2 other ring members?
q_shared = f"""
let louis_targets = ['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| distinct subject;
let ring_blocks = ['Bluesky.Graph.Block_v1']
| where did in ('{dids_str}')
| where did != '{DID}'
| summarize other_blockers = dcount(did) by subject;
louis_targets
| join kind=leftouter ring_blocks on subject
| summarize 
    only_louis = countif(isempty(subject1) or other_blockers == 0),
    shared_1 = countif(other_blockers == 1),
    shared_2 = countif(other_blockers == 2),
    shared_3plus = countif(other_blockers >= 3)
"""
df_shared = execute_query(q_shared)
print("\nOf Louis's blocks, how many are shared with ring:")
print(df_shared.to_string())
