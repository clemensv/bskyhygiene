import sys
sys.path.insert(0, r'C:\Users\clemensv\OneDrive - Microsoft\Agents\nius')
from nius_bot_dossier.kusto_client import execute_query
import requests

DID = 'did:plc:kd4wtd75a637g2gvg2dh2b3t'

# 12% of repliers to viral posts get blocked. What distinguishes that 12%?
# Hypothesis: They block accounts with high follower counts (the "influential progressives")
# or accounts that have certain features (like engagement level, post frequency)

# Check: Among repliers to the top viral post, compare blocked vs not-blocked
print("=== WHAT DISTINGUISHES BLOCKED vs NOT-BLOCKED REPLIERS? ===")
print("(Comparing post frequency of blocked vs unblocked repliers to viral post)")
q = f"""
let post_uri = 'at://did:plc:7qqkq2zdwq4j5jingukgtuky/app.bsky.feed.post/3mkt2mns3n22u';
let repliers = ['Bluesky.Feed.Post_v1']
| where reply_root == post_uri
| distinct did;
let blocked = ['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| distinct subject;
let blocked_repliers = repliers | join kind=inner blocked on $left.did == $right.subject | project did;
let unblocked_repliers = repliers | join kind=leftanti blocked on $left.did == $right.subject | project did;
let blocked_activity = ['Bluesky.Feed.Post_v1']
| where did in (blocked_repliers)
| where ___time > datetime(2026-05-01)
| summarize posts = count() by did
| summarize 
    avg_posts = avg(posts), 
    median_posts = percentile(posts, 50),
    p90_posts = percentile(posts, 90),
    sample_size = count()
| extend group = "blocked";
let unblocked_activity = ['Bluesky.Feed.Post_v1']
| where did in (unblocked_repliers)
| where ___time > datetime(2026-05-01)
| summarize posts = count() by did
| summarize 
    avg_posts = avg(posts), 
    median_posts = percentile(posts, 50),
    p90_posts = percentile(posts, 90),
    sample_size = count()
| extend group = "unblocked";
union blocked_activity, unblocked_activity
"""
df = execute_query(q)
print(df.to_string())

# Check: Are they blocking accounts that ALSO follow certain accounts?
# If they block people who follow specific progressive hubs:
print("\n\n=== DO BLOCKED REPLIERS FOLLOW MORE PROGRESSIVE HUBS? ===")
# Among repliers to the viral post, check if blocked ones follow the top targets more
q2 = f"""
let post_uri = 'at://did:plc:7qqkq2zdwq4j5jingukgtuky/app.bsky.feed.post/3mkt2mns3n22u';
let repliers = ['Bluesky.Feed.Post_v1']
| where reply_root == post_uri
| distinct did;
let blocked = ['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| distinct subject;
let progressive_hubs = dynamic([
    'did:plc:mxwlsvdgs6tn75lq6jrr2vp7',
    'did:plc:sjog5j7brym6onfw5bqtu455',
    'did:plc:3efnghm2thiwta6u5mcf5eyq',
    'did:plc:prphuhcevxklilgwsqxqnvfo',
    'did:plc:pw7pbpp6pktso7lzuiz2lufs'
]);
let blocked_repliers = repliers | join kind=inner blocked on $left.did == $right.subject | project did;
let unblocked_repliers = repliers | join kind=leftanti blocked on $left.did == $right.subject | project did;
let blocked_follows_hubs = ['Bluesky.Graph.Follow_v1']
| where did in (blocked_repliers)
| where subject in (progressive_hubs)
| summarize hub_follows = dcount(subject) by did
| summarize avg_hubs = avg(hub_follows), sample = count()
| extend group = "blocked";
let unblocked_follows_hubs = ['Bluesky.Graph.Follow_v1']
| where did in (unblocked_repliers)
| where subject in (progressive_hubs)
| summarize hub_follows = dcount(subject) by did
| summarize avg_hubs = avg(hub_follows), sample = count()
| extend group = "unblocked";
union blocked_follows_hubs, unblocked_follows_hubs
"""
df2 = execute_query(q2)
print(df2.to_string())

# Critical check: Is there a KNOWN BLOCKING TOOL on Bluesky?
# SkyTools, ClearSky Block Packs, or custom tools use moderation lists
# But we confirmed 0 lists. So it must be API-direct.
# Check: Does block cadence suggest batches from an exported list?
print("\n\n=== BLOCK CADENCE ANALYSIS ON PEAK DAY ===")
print("(Are there pauses suggesting batch imports from a list?)")
q3 = f"""
['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| where ___time between(datetime(2026-05-27 12:00) .. datetime(2026-05-27 23:00))
| order by ___time asc
| serialize rn = row_number()
| extend gap_ms = datetime_diff('millisecond', ___time, prev(___time))
| where gap_ms > 5000
| project ___time, gap_ms, rn
| take 30
"""
df3 = execute_query(q3)
print(df3.to_string())

# Check: What is the OVERALL blocking pattern - continuous stream or batch/pause/batch?
print("\n=== BLOCKS PER MINUTE ON MAY 27 ===")
q4 = f"""
['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| where ___time between(datetime(2026-05-27 12:00) .. datetime(2026-05-27 23:00))
| summarize blocks = count() by bin(___time, 1m)
| order by ___time asc
"""
df4 = execute_query(q4)
# Show summary stats
print(f"Minutes with activity: {len(df4)}")
print(f"Total blocks: {df4['blocks'].sum()}")
print(f"Max blocks/minute: {df4['blocks'].max()}")
print(f"Mean blocks/minute: {df4['blocks'].mean():.1f}")
# Show gaps > 5 min
import pandas as pd
df4['___time'] = pd.to_datetime(df4['___time'])
df4['gap_min'] = df4['___time'].diff().dt.total_seconds() / 60
gaps = df4[df4['gap_min'] > 5]
print(f"\nGaps > 5 minutes: {len(gaps)}")
if len(gaps) > 0:
    print(gaps[['___time', 'gap_min', 'blocks']].to_string())
