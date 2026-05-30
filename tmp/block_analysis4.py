import sys
sys.path.insert(0, r'C:\Users\clemensv\OneDrive - Microsoft\Agents\nius')
from nius_bot_dossier.kusto_client import execute_query
import requests
import json

DID = 'did:plc:kd4wtd75a637g2gvg2dh2b3t'

# Resolve the top mass-blockers who share victims with louisbetonberlin
print("=== RESOLVING TOP COORDINATED BLOCKERS ===")
top_dids = [
    'did:plc:gjcwwrezaz5qdcjn3347qvtl',  # 85K blocks, 7291 shared
    'did:plc:qildfzoh5p24jgion4xiycvz',  # 51K blocks, 5213 shared
    'did:plc:hwpiekun4iebo4oqevjfe6ss',  # 7K blocks, 4252 shared
    'did:plc:xcytuwwb3b33ipiqzmqzbs45',  # 43K blocks, 4221 shared
    'did:plc:tfspkb2htmw7vwdgqj7mzx7m',  # 14K blocks, 3585 shared
    'did:plc:ajvwz5alprhutyx3zuwrg7dc',  # shared 3333
    'did:plc:gkg3mo2wltuzdzww53rkxfqg',  # shared 2979
    'did:plc:33wcrgvuwuxvzpa74yud37qp',  # 34K blocks, 2301 shared
    'did:plc:45nedwgk4a222oynw3mcp4vl',  # shared 2224
    'did:plc:4shas75br73nivnphp6xtfo5',  # 13K blocks, 2213 shared
    'did:plc:mkwktns2qtmt5igmolj32ffm',  # 34K blocks
    'did:plc:jyqk4xrplfhsl6dfeibuw37c',  # 22K blocks
    'did:plc:ktgilppmthvr4jm4fwcrbwie',  # 21K blocks
    'did:plc:zcx3ryxqcbc4tawv7bam64mq',  # 20K blocks
    'did:plc:22msnh4bnrc6gg54kvrrtc4o',  # 16K blocks
]

# Resolve in batches of 25
params = [('actors[]', d) for d in top_dids[:25]]
r = requests.get('https://public.api.bsky.app/xrpc/app.bsky.actor.getProfiles', params=params)
if r.status_code == 200:
    profiles = r.json().get('profiles', [])
    for p in profiles:
        handle = p.get('handle', '?')
        display = p.get('displayName', '')
        followers = p.get('followersCount', 0)
        posts = p.get('postsCount', 0)
        desc = (p.get('description') or '')[:80]
        labels = [l.get('val','') for l in p.get('labels', [])]
        print(f"  {handle:40s} | {display:25s} | F:{followers:>6} P:{posts:>6} | L:{labels}")
        if desc:
            print(f"    Bio: {desc}")
else:
    print(f"  API error: {r.status_code}")

# Check if there's timing correlation - do they all block at the same hour?
print("\n\n=== TIMING CORRELATION: DO THEY BLOCK IN SYNC? ===")
top3 = [
    'did:plc:gjcwwrezaz5qdcjn3347qvtl',
    'did:plc:qildfzoh5p24jgion4xiycvz',
    'did:plc:xcytuwwb3b33ipiqzmqzbs45',
]
q = f"""
['Bluesky.Graph.Block_v1']
| where did in ('{top3[0]}', '{top3[1]}', '{top3[2]}', '{DID}')
| where ___time > ago(3d)
| summarize blocks = count() by did, bin(___time, 1h)
| order by ___time asc, did
"""
df = execute_query(q)
# Pivot by hour
from collections import defaultdict
pivot = defaultdict(dict)
for _, row in df.iterrows():
    t = str(row['___time'])[:16]
    pivot[t][row['did'][-8:]] = row['blocks']

print(f"\n{'Hour':<20} | {'louis':<8} | {'gjcw':<8} | {'qild':<8} | {'xcyt':<8}")
print("-" * 70)
for t in sorted(pivot.keys()):
    vals = pivot[t]
    print(f"{t:<20} | {vals.get('g2dh2b3t',''):>7} | {vals.get('347qvtl',''):>7} | {vals.get('mqzbs45',''):>7} | {vals.get('mqzbs45',''):>7}")

# Also: check how many unique victims total across this group
print("\n\n=== TOTAL UNIQUE VICTIMS ACROSS TOP 5 BLOCKERS ===")
q2 = f"""
['Bluesky.Graph.Block_v1']
| where did in ('{DID}', '{top3[0]}', '{top3[1]}', '{top3[2]}', 'did:plc:hwpiekun4iebo4oqevjfe6ss')
| summarize total_blocks = count(), unique_victims = dcount(subject)
"""
df2 = execute_query(q2)
print(df2.to_string())

# Per-account stats
print("\n=== PER-ACCOUNT BLOCK STATS (all time) ===")
q3 = f"""
['Bluesky.Graph.Block_v1']
| where did in ('{DID}', '{top3[0]}', '{top3[1]}', '{top3[2]}', 'did:plc:hwpiekun4iebo4oqevjfe6ss')
| summarize total = count(), unique = dcount(subject), first = min(___time), last = max(___time) by did
| order by total desc
"""
df3 = execute_query(q3)
print(df3.to_string())
