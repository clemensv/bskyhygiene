import sys
sys.path.insert(0, r'C:\Users\clemensv\OneDrive - Microsoft\Agents\nius')
from nius_bot_dossier.kusto_client import execute_query
import requests

DID = 'did:plc:kd4wtd75a637g2gvg2dh2b3t'

# The victims are mostly English-speaking US progressives!
# Common follow targets: Solidarity Social (38K), Law of Fairness (36K), etc.
# This suggests the ring is targeting people who follow large progressive accounts.

# Key hypothesis: They're CRAWLING the follower lists of large progressive hub accounts
# and blocking everyone they find. Let's verify:

# Check: What language do victims post in?
print("=== LANGUAGE DISTRIBUTION OF VICTIMS ===")
q_lang = f"""
let victims = ['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| distinct subject;
['Bluesky.Feed.Post_v1']
| where did in (victims)
| where ___time > datetime(2026-05-01)
| mv-expand lang = langs to typeof(string)
| summarize posts = count() by lang
| order by posts desc
| take 15
"""
df_lang = execute_query(q_lang)
print(df_lang.to_string())

# Check: Reply root analysis on a LARGER scale
# Do many victims reply to the same viral posts?
print("\n\n=== MOST COMMON REPLY TARGETS AMONG ALL VICTIMS ===")
q_reply = f"""
let victims = ['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| distinct subject;
['Bluesky.Feed.Post_v1']
| where did in (victims)
| where isnotempty(reply_root)
| where ___time > datetime(2026-05-01)
| summarize repliers = dcount(did) by reply_root
| where repliers > 20
| order by repliers desc
| take 20
"""
df_reply = execute_query(q_reply)
print(df_reply.to_string())

# Check: Does the smatsto account (495K blocks, 22 followers) share EXACT block lists?
# i.e., is louisbetonberlin's blocklist a SUBSET of smatsto's?
print("\n\n=== IS LOUIS'S BLOCKLIST A SUBSET OF SMATSTO? ===")
SMATSTO = 'did:plc:gjcwwrezaz5qdcjn3347qvtl'
q_subset = f"""
let louis_victims = ['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| distinct subject;
let smatsto_victims = ['Bluesky.Graph.Block_v1']
| where did == '{SMATSTO}'
| distinct subject;
let overlap = louis_victims | join kind=inner smatsto_victims on subject | count;
let louis_total = toscalar(louis_victims | count);
let smatsto_total = toscalar(smatsto_victims | count);
let overlap_count = toscalar(overlap);
print louis_total, smatsto_total, overlap_count
"""
q_subset2 = f"""
let louis_victims = ['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| distinct subject;
let smatsto_victims = ['Bluesky.Graph.Block_v1']
| where did == '{SMATSTO}'
| distinct subject;
louis_victims
| join kind=leftouter smatsto_victims on subject
| summarize in_both = countif(isnotempty(subject1)), only_louis = countif(isempty(subject1))
"""
df_sub = execute_query(q_subset2)
print(df_sub.to_string())

# Check: Timing - does smatsto block people BEFORE louisbetonberlin?
# If smatsto blocks first, then louis is consuming smatsto's list.
print("\n\n=== WHO BLOCKS FIRST: SMATSTO or LOUIS? ===")
q_timing = f"""
let louis_blocks = ['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| project subject, louis_time = ___time;
let smatsto_blocks = ['Bluesky.Graph.Block_v1']
| where did == '{SMATSTO}'
| project subject, smatsto_time = ___time;
louis_blocks
| join kind=inner smatsto_blocks on subject
| extend who_first = iff(louis_time < smatsto_time, "louis_first", "smatsto_first")
| extend gap_hours = datetime_diff('hour', louis_time, smatsto_time)
| summarize count() by who_first
"""
df_timing = execute_query(q_timing)
print(df_timing.to_string())

# Time gap distribution
print("\n=== TIME GAP DISTRIBUTION (SMATSTO - LOUIS) ===")
q_gap = f"""
let louis_blocks = ['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| project subject, louis_time = ___time;
let smatsto_blocks = ['Bluesky.Graph.Block_v1']
| where did == '{SMATSTO}'
| project subject, smatsto_time = ___time;
louis_blocks
| join kind=inner smatsto_blocks on subject
| extend gap_hours = datetime_diff('hour', smatsto_time, louis_time)
| summarize 
    avg_gap_h = avg(gap_hours),
    median_gap_h = percentile(gap_hours, 50),
    p10_gap_h = percentile(gap_hours, 10),
    p90_gap_h = percentile(gap_hours, 90)
"""
df_gap = execute_query(q_gap)
print(df_gap.to_string())
