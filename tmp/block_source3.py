import sys
sys.path.insert(0, r'C:\Users\clemensv\OneDrive - Microsoft\Agents\nius')
from nius_bot_dossier.kusto_client import execute_query
import requests

DID = 'did:plc:kd4wtd75a637g2gvg2dh2b3t'

# The ring all started within 2 days of each other (Apr 28-May 4).
# The #1 blocker (gjcwwrezaz5qdcjn3347qvtl) has 495K blocks total - that's a dedicated blocking machine.
# Let's understand the victim list better.

# Key question: Is there an account whose ENTIRE follower list is being blocked?
# Check: Among blocked accounts, which accounts do they follow that have HIGH coverage?
print("=== HIGH COVERAGE CHECK ===")
print("(Is there an account whose followers are being systematically blocked?)")
q = f"""
let victims = ['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| distinct subject;
let victim_count = toscalar(victims | count);
['Bluesky.Graph.Follow_v1']
| where did in (victims)
| summarize victims_following = dcount(did) by subject
| extend coverage_pct = round(100.0 * victims_following / victim_count, 1)
| where victims_following > 50
| order by victims_following desc
| take 20
"""
df = execute_query(q)
print(df.to_string())

# The top blocker has 495K blocks. That's way beyond any single follower list.
# This suggests a CRAWLING approach - likely scraping the network graph.
# Let's see if the blocks follow the Bluesky network topology

# Check: Are they blocking people who interacted with specific keywords/hashtags?
print("\n\n=== DO VICTIMS POST ABOUT SPECIFIC TOPICS? ===")
print("(Checking posts from a batch of victims on the day they were blocked)")
q2 = f"""
let victims_may27 = ['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| where ___time between(datetime(2026-05-27 12:00) .. datetime(2026-05-27 13:00))
| take 200
| distinct subject;
['Bluesky.Feed.Post_v1']
| where did in (victims_may27)
| where ___time between(datetime(2026-05-20) .. datetime(2026-05-27))
| summarize posts = count(), 
    sample_text = take_any(text)
    by did
| take 20
"""
df2 = execute_query(q2)
for _, row in df2.iterrows():
    txt = (row['sample_text'] or '')[:120]
    print(f"  Posts:{row['posts']:>3} | {txt}")

# Check: Does the block ORDER correlate with account creation date?
print("\n\n=== BLOCK ORDER vs ACCOUNT DID ALPHABETICAL ORDER ===")
print("(Testing if they're iterating a sorted list)")
q3 = f"""
['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| where ___time between(datetime(2026-05-27 12:57) .. datetime(2026-05-27 13:01))
| order by ___time asc
| take 50
| serialize block_rank = row_number()
| project block_rank, subject
| order by subject asc
| serialize alpha_rank = row_number()
| project block_rank, alpha_rank, subject
"""
df3 = execute_query(q3)
print(df3.to_string())

# Check: correlation between block_rank and alpha_rank?
import numpy as np
if len(df3) > 5:
    corr = np.corrcoef(df3['block_rank'], df3['alpha_rank'])[0, 1]
    print(f"\nCorrelation (block order vs DID alphabetical): {corr:.3f}")
    # If high correlation, they're iterating an alphabetically sorted DID list

# Also check: are they iterating a specific account's follower list by FOLLOW TIME?
# Try the biggest ring member's overlap account
print("\n\n=== DOES LOUISBETONBERLIN FOLLOW THE TOP BLOCKER? ===")
q4 = f"""
['Bluesky.Graph.Follow_v1']
| where did == '{DID}'
| project subject
"""
df4 = execute_query(q4)
print(f"Louis follows: {df4['subject'].tolist()}")

# Resolve the top blocker
print("\n=== RESOLVE TOP BLOCKER (495K blocks) ===")
params = [('actors[]', 'did:plc:gjcwwrezaz5qdcjn3347qvtl')]
r = requests.get('https://public.api.bsky.app/xrpc/app.bsky.actor.getProfiles', params=params)
if r.status_code == 200:
    for p in r.json().get('profiles', []):
        print(f"  Handle: {p.get('handle')}")
        print(f"  Display: {p.get('displayName')}")
        print(f"  Followers: {p.get('followersCount')}")
        print(f"  Following: {p.get('followsCount')}")
        print(f"  Posts: {p.get('postsCount')}")
        print(f"  Bio: {(p.get('description') or '')[:200]}")
        print(f"  Labels: {[l.get('val') for l in p.get('labels', [])]}")
        print(f"  Lists: {p.get('associated', {}).get('lists', 0)}")
