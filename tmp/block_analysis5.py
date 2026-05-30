import sys
sys.path.insert(0, r'C:\Users\clemensv\OneDrive - Microsoft\Agents\nius')
from nius_bot_dossier.kusto_client import execute_query

DID = 'did:plc:kd4wtd75a637g2gvg2dh2b3t'

# Simpler query: louisbetonberlin's unique victim count and first/last
print("=== LOUISBETONBERLIN BLOCK STATS ===")
q = f"""
['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| summarize total = count(), unique = dcount(subject), first_block = min(___time), last_block = max(___time)
"""
df = execute_query(q)
print(df.to_string())

# Check inter-block timing grouped by day to see if consistent automation
print("\n=== BLOCKS PER DAY WITH MEDIAN INTER-BLOCK TIME ===")
q2 = f"""
['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| order by ___time asc
| extend prev = prev(___time)
| extend delta_ms = datetime_diff("millisecond", ___time, prev)
| where isnotnull(prev)
| summarize blocks = count(), 
    median_gap_ms = percentile(delta_ms, 50),
    p95_gap_ms = percentile(delta_ms, 95)
    by bin(___time, 1d)
| order by ___time asc
"""
df2 = execute_query(q2)
print(df2.to_string())

# Check the victim overlap count (just top 1 mass-blocker)
print("\n=== OVERLAP: TOP BLOCKER vs LOUISBETONBERLIN ===")
q3 = f"""
let louis_victims = ['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| distinct subject;
['Bluesky.Graph.Block_v1']
| where did == 'did:plc:gjcwwrezaz5qdcjn3347qvtl'
| where subject in (louis_victims)
| summarize shared_victims = dcount(subject)
"""
df3 = execute_query(q3)
print(df3.to_string())

# Check louisbetonberlin's overall victims: are they mostly German bluesky?
# Get creation date cluster by looking at a wider sample
print("\n=== VICTIM ACCOUNT AGE (random 100 from all-time blocks) ===")
q4 = f"""
['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| sample 100
| project subject
"""
df4 = execute_query(q4)
import requests
dids = df4['subject'].tolist()
all_profiles = []
for i in range(0, len(dids), 25):
    batch = dids[i:i+25]
    params = [('actors[]', d) for d in batch]
    r = requests.get('https://public.api.bsky.app/xrpc/app.bsky.actor.getProfiles', params=params)
    if r.status_code == 200:
        all_profiles.extend(r.json().get('profiles', []))

from collections import Counter
years = Counter()
follower_ranges = Counter()
has_no_unauthenticated = 0

for p in all_profiles:
    created = p.get('createdAt', '')[:4]
    years[created] += 1
    fc = p.get('followersCount', 0)
    if fc < 10: follower_ranges['<10'] += 1
    elif fc < 100: follower_ranges['10-99'] += 1
    elif fc < 1000: follower_ranges['100-999'] += 1
    else: follower_ranges['1000+'] += 1
    labels = [l.get('val','') for l in p.get('labels', [])]
    if '!no-unauthenticated' in labels:
        has_no_unauthenticated += 1

print(f"Resolved: {len(all_profiles)}/{len(dids)}")
print(f"Creation years: {dict(sorted(years.items()))}")
print(f"Follower ranges: {dict(sorted(follower_ranges.items()))}")
print(f"With !no-unauthenticated label: {has_no_unauthenticated}/{len(all_profiles)}")
