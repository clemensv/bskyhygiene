import sys
sys.path.insert(0, r'C:\Users\clemensv\OneDrive - Microsoft\Agents\nius')
from nius_bot_dossier.kusto_client import execute_query
import requests
import json

DID = 'did:plc:kd4wtd75a637g2gvg2dh2b3t'

# 1. Check if they're using a known blocklist tool (mass-blocking from lists)
# Look at the block rate pattern - is it constant ~100ms or variable?
print("=== BLOCK RATE PATTERN (last 2000 blocks today) ===")
q = f"""
['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| where ___time > ago(24h)
| order by ___time asc
| extend prev_time = prev(___time)
| extend delta_ms = datetime_diff("millisecond", ___time, prev_time)
| where isnotnull(prev_time)
| summarize count() by bin(delta_ms, 50)
| order by delta_ms asc
| take 20
"""
df = execute_query(q)
print(df.to_string())

# 2. Check if this account also has unusual follow patterns
print("\n=== FOLLOW ACTIVITY ===")
q2 = f"""
['Bluesky.Graph.Follow_v1']
| where did == '{DID}'
| summarize total_follows = count(),
    first_follow = min(___time),
    last_follow = max(___time)
"""
df2 = execute_query(q2)
print(df2.to_string())

# 3. Resolve a sample of blocked accounts to see what they look like
print("\n=== RESOLVING SAMPLE OF BLOCKED ACCOUNTS ===")
q3 = f"""
['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| where ___time > ago(24h)
| order by ___time desc
| take 25
| project subject
"""
df3 = execute_query(q3)
dids = df3['subject'].tolist()

# Resolve via API in batch of 25
params = [('actors[]', d) for d in dids[:25]]
r = requests.get('https://public.api.bsky.app/xrpc/app.bsky.actor.getProfiles', params=params)
if r.status_code == 200:
    profiles = r.json().get('profiles', [])
    for p in profiles:
        handle = p.get('handle', '?')
        display = p.get('displayName', '')
        followers = p.get('followersCount', 0)
        posts = p.get('postsCount', 0)
        created = p.get('createdAt', '')[:10]
        desc = (p.get('description') or '')[:60]
        print(f"  {handle:40s} | {display:20s} | F:{followers:>6} P:{posts:>5} | {created} | {desc}")
else:
    print(f"  API error: {r.status_code}")

# 4. Check if blocked accounts overlap with any known pattern
# Do the blocked accounts tend to be German? Political? Random?
print("\n=== BLOCK VOLUME BY DAY (last 7 days by hour) ===")
q4 = f"""
['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| where ___time > ago(3d)
| summarize blocks = count() by bin(___time, 1h)
| order by ___time asc
"""
df4 = execute_query(q4)
print(df4.to_string())

# 5. Check if there are unblocks too (to see if it's a rotating pattern)
print("\n=== LOOKING FOR UNBLOCK PATTERNS (checking ___type) ===")
q5 = f"""
['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| summarize count() by ___type
"""
df5 = execute_query(q5)
print(df5.to_string())
