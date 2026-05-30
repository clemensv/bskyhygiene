import sys
sys.path.insert(0, r'C:\Users\clemensv\OneDrive - Microsoft\Agents\nius')
from nius_bot_dossier.kusto_client import execute_query
import requests
import json

DID = 'did:plc:kd4wtd75a637g2gvg2dh2b3t'

# 1. Check if the blocked accounts are also blocked by OTHER accounts in the same pattern
# This would indicate a shared blocklist/tool
print("=== DO OTHER ACCOUNTS BLOCK THE SAME PEOPLE? ===")
print("(checking 10 recently blocked DIDs)")
q = f"""
let blocked_sample = ['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| where ___time > ago(24h)
| order by ___time desc
| take 10
| project subject;
['Bluesky.Graph.Block_v1']
| where subject in (blocked_sample)
| where did != '{DID}'
| summarize blockers = dcount(did), blocks = count() by subject
| order by blockers desc
"""
df = execute_query(q)
print(df.to_string())

# 2. Check who ELSE is mass-blocking with similar patterns
print("\n=== TOP MASS BLOCKERS (last 7 days, >1000 blocks) ===")
q2 = """
['Bluesky.Graph.Block_v1']
| where ___time > ago(7d)
| summarize blocks = count() by did
| where blocks > 1000
| order by blocks desc
| take 20
"""
df2 = execute_query(q2)
print(df2.to_string())

# 3. Among those mass-blockers, check overlap with louisbetonberlin's victims
print("\n=== CHECKING OVERLAP BETWEEN TOP BLOCKERS AND LOUISBETONBERLIN'S VICTIMS ===")
q3 = f"""
let louis_victims = ['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| distinct subject;
let other_mass_blockers = ['Bluesky.Graph.Block_v1']
| where ___time > ago(7d)
| where did != '{DID}'
| summarize blocks = count() by did
| where blocks > 1000
| project did;
['Bluesky.Graph.Block_v1']
| where did in (other_mass_blockers)
| where subject in (louis_victims)
| summarize shared_blocks = count(), shared_victims = dcount(subject) by did
| order by shared_victims desc
| take 10
"""
df3 = execute_query(q3)
print(df3.to_string())

# 4. Check if this account is following the blocked people (block-after-follow)
print("\n=== DOES LOUISBETONBERLIN FOLLOW ANY BLOCKED ACCOUNTS? ===")
q4 = f"""
let blocked = ['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| distinct subject;
['Bluesky.Graph.Follow_v1']
| where did == '{DID}'
| where subject in (blocked)
| count
"""
df4 = execute_query(q4)
print(df4.to_string())

# 5. What's the creation date distribution of blocked accounts?
print("\n=== ARE BLOCKED ACCOUNTS NEW OR OLD? (resolve 50 random) ===")
q5 = f"""
['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| where ___time > ago(7d)
| sample 50
| project subject
"""
df5 = execute_query(q5)
dids = df5['subject'].tolist()

# Batch resolve
all_profiles = []
for i in range(0, len(dids), 25):
    batch = dids[i:i+25]
    params = [('actors[]', d) for d in batch]
    r = requests.get('https://public.api.bsky.app/xrpc/app.bsky.actor.getProfiles', params=params)
    if r.status_code == 200:
        all_profiles.extend(r.json().get('profiles', []))

# Analyze
from collections import Counter
years = Counter()
has_posts = 0
has_followers_100plus = 0
german_signal = 0

for p in all_profiles:
    created = p.get('createdAt', '')[:4]
    years[created] += 1
    if p.get('postsCount', 0) > 0:
        has_posts += 1
    if p.get('followersCount', 0) >= 100:
        has_followers_100plus += 1
    desc = (p.get('description') or '').lower()
    if any(w in desc for w in ['deutsch', 'german', 'berlin', 'hamburg', 'münchen', 'köln', 'links', 'grün', 'klima', 'feminism', 'antifa', 'noafd', 'demokrat']):
        german_signal += 1

print(f"\nResolved: {len(all_profiles)}/{len(dids)}")
print(f"Creation years: {dict(years)}")
print(f"Have posts: {has_posts}/{len(all_profiles)}")
print(f"Have 100+ followers: {has_followers_100plus}/{len(all_profiles)}")
print(f"German/political keywords in bio: {german_signal}/{len(all_profiles)}")
