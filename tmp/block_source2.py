import sys
sys.path.insert(0, r'C:\Users\clemensv\OneDrive - Microsoft\Agents\nius')
from nius_bot_dossier.kusto_client import execute_query
import requests

DID = 'did:plc:kd4wtd75a637g2gvg2dh2b3t'

# Resolve the top common follow targets
print("=== WHO ARE THE COMMON FOLLOW TARGETS? ===")
top_dids = [
    'did:plc:mxwlsvdgs6tn75lq6jrr2vp7',
    'did:plc:sjog5j7brym6onfw5bqtu455',
    'did:plc:dusbgwd7sb6dazxmvhiz74rr',
    'did:plc:pw7pbpp6pktso7lzuiz2lufs',
    'did:plc:5e7kpfgbe6ddtzosyhm46wfy',
    'did:plc:3efnghm2thiwta6u5mcf5eyq',
    'did:plc:p3sarboifd2spjkbwryx7rrm',
    'did:plc:prphuhcevxklilgwsqxqnvfo',
    'did:plc:kdoldb2lixkuj4pm3qv6dxky',
    'did:plc:rwvs5jl3mvqywhuwho5iwvxw',
]
params = [('actors[]', d) for d in top_dids]
r = requests.get('https://public.api.bsky.app/xrpc/app.bsky.actor.getProfiles', params=params)
if r.status_code == 200:
    for p in r.json().get('profiles', []):
        handle = p.get('handle', '?')
        display = p.get('displayName', '')
        followers = p.get('followersCount', 0)
        desc = (p.get('description') or '')[:80]
        print(f"  {handle:40s} | {display:25s} | F:{followers:>7} | {desc}")

# Hypothesis 2: Are they blocking based on WHO FOLLOWS louisbetonberlin?
# i.e., are any of the blocked accounts people who follow louisbetonberlin?
print("\n\n=== ARE BLOCKED ACCOUNTS FOLLOWERS OF LOUISBETONBERLIN? ===")
q2 = f"""
let victims = ['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| distinct subject;
['Bluesky.Graph.Follow_v1']
| where did in (victims)
| where subject == '{DID}'
| count
"""
df2 = execute_query(q2)
print(df2.to_string())

# Hypothesis 3: Block ordering - are they going through follower lists sequentially?
# Check if blocks correlate with follower ordering of some target account
# Look at whether the blocked DIDs appear in sequential follower-list order for any account
print("\n\n=== BLOCK ORDERING vs FOLLOW TIME ===")
print("(Are blocks in the same order as someone's follower list?)")
# Take the top common target and check if the block order matches the follow order
q3 = f"""
let victims_ordered = ['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| where ___time between(datetime(2026-05-27) .. datetime(2026-05-28))
| order by ___time asc
| project subject, block_time = ___time
| serialize block_rank = row_number();
let follow_times = ['Bluesky.Graph.Follow_v1']
| where subject == 'did:plc:mxwlsvdgs6tn75lq6jrr2vp7'
| where did in (victims_ordered)
| project did, follow_time = ___time;
victims_ordered
| join kind=inner follow_times on $left.subject == $right.did
| order by block_rank asc
| take 30
| project block_rank, block_time, follow_time
"""
df3 = execute_query(q3)
print(df3.to_string())

# Hypothesis 4: Are they using ClearSky or another blocklist tool?
# ClearSky exports show up as "blocked by N accounts" - check if there's a concentration
# of blocks that started exactly when louisbetonberlin started (Apr 29)
print("\n\n=== WHEN DID THE RING MEMBERS START BLOCKING? ===")
ring = [
    DID,
    'did:plc:gjcwwrezaz5qdcjn3347qvtl',
    'did:plc:qildfzoh5p24jgion4xiycvz',
    'did:plc:xcytuwwb3b33ipiqzmqzbs45',
    'did:plc:hwpiekun4iebo4oqevjfe6ss',
    'did:plc:tfspkb2htmw7vwdgqj7mzx7m',
]
dids_str = "', '".join(ring)
q4 = f"""
['Bluesky.Graph.Block_v1']
| where did in ('{dids_str}')
| summarize first_block = min(___time), last_block = max(___time), total = count() by did
| order by first_block asc
"""
df4 = execute_query(q4)
print(df4.to_string())

# Hypothesis 5: Are they using "who liked a specific post" or "who replied to X"?
# Check: do blocks come in batches with victims that all interacted with same content?
print("\n\n=== DO BLOCKED ACCOUNTS SHARE INTERACTIONS? ===")
print("(Checking if victims replied to same posts)")
q5 = f"""
let victims_batch = ['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| where ___time between(datetime(2026-05-27 20:00) .. datetime(2026-05-27 21:00))
| take 500
| distinct subject;
['Bluesky.Feed.Post_v1']
| where did in (victims_batch)
| where isnotempty(reply_root)
| summarize repliers = dcount(did) by reply_root
| where repliers > 5
| order by repliers desc
| take 10
"""
df5 = execute_query(q5)
print(df5.to_string())
