"""Check if ring members use Bluesky moderation lists."""
import sys
sys.path.insert(0, r'C:\Users\clemensv\OneDrive - Microsoft\Agents\nius\nius_bot_dossier')
from kusto_client import get_client

client = get_client()
db = 'bluesky'

RING_ALL = [
    'did:plc:kd4wtd75a637g2gvg2dh2b3t',
    'did:plc:gjcwwrezaz5qdcjn3347qvtl',
    'did:plc:qildfzoh5p24jgion4xiycvz',
    'did:plc:xcytuwwb3b33ipiqzmqzbs45',
    'did:plc:hwpiekun4iebo4oqevjfe6ss',
    'did:plc:tfspkb2htmw7vwdgqj7mzx7m',
    'did:plc:3c7r453vexmpwu6nheazyikk',
    'did:plc:u4e3ytzjxb7vapbdmr4oz7ld',
    'did:plc:5v7itrhmq6zhvpqn2sfmcwaw',
    'did:plc:l3fkqug2hhn4upcdewogsijh',
    'did:plc:vb6p4kuz3kmtqrcix2ghjkwf',
    'did:plc:oqc7737mwl6y22wjqdduujex',
    'did:plc:qbw4i5hcyc6dtuckixaogxlc',
    'did:plc:dvhyaxbrf7uh6eemujbd4jao',
    'did:plc:qq2eg3kbh44gytxlghozodeb',
    'did:plc:5sjri67leyvnlenx7tzgfulk',
]
dids_str = '","'.join(RING_ALL)

def run(query):
    try:
        r = client.execute(db, query)
        cols = [c.column_name for c in r.primary_results[0].columns]
        rows = list(r.primary_results[0])
        return cols, rows
    except Exception as e:
        return None, str(e)

# 1. Moderation lists CREATED by ring members
print("=== MODERATION LISTS CREATED BY RING MEMBERS ===")
q1 = f"""
['Bluesky.Graph.List_v1']
| where did in ("{dids_str}")
| project did, name, purpose, description, created_at
"""
cols, rows = run(q1)
if cols:
    print(f"Found {len(rows)} lists")
    for row in rows:
        print(dict(zip(cols, row)))
else:
    print(f"Error: {rows}")

# 2. List BLOCK subscriptions (subscribing to someone's modlist)
print("\n=== LIST BLOCK SUBSCRIPTIONS BY RING MEMBERS ===")
q2 = f"""
['Bluesky.Graph.Listblock_v1']
| where did in ("{dids_str}")
| summarize count() by did
"""
cols, rows = run(q2)
if cols:
    print(f"Found {len(rows)} accounts with listblock subscriptions")
    for row in rows:
        print(dict(zip(cols, row)))
else:
    print(f"Error: {rows}")

# 3. List items (accounts added to lists BY these members)
print("\n=== LIST ITEMS CREATED BY RING MEMBERS ===")
q3 = f"""
['Bluesky.Graph.Listitem_v1']
| where did in ("{dids_str}")
| summarize items=count() by did
"""
cols, rows = run(q3)
if cols:
    print(f"Found {len(rows)} accounts creating list items")
    for row in rows:
        print(dict(zip(cols, row)))
else:
    print(f"Error: {rows}")

# 4. Check if ANY list exists that contains a large portion of the blocked targets
# (i.e., is there a public moderation list someone else maintains that they subscribe to?)
print("\n=== LISTS THAT TARGET THE SAME VICTIMS (top 10 largest modlists) ===")
q4 = """
['Bluesky.Graph.List_v1']
| where purpose == "app.bsky.graph.defs#modlist"
| join kind=inner (
    ['Bluesky.Graph.Listitem_v1']
    | summarize items=count() by did
) on did
| where items > 10000
| project did, name, purpose, items
| order by items desc
| take 20
"""
cols, rows = run(q4)
if cols:
    print(f"Found {len(rows)} large modlists (>10K items)")
    for row in rows:
        print(dict(zip(cols, row)))
else:
    print(f"Error: {rows}")

# 5. Check if ring members SUBSCRIBE to any list via listblock
print("\n=== WHAT LISTS DO RING MEMBERS SUBSCRIBE TO? ===")
q5 = f"""
['Bluesky.Graph.Listblock_v1']
| where did in ("{dids_str}")
| project did, subject
"""
cols, rows = run(q5)
if cols:
    print(f"Found {len(rows)} list subscriptions")
    for row in rows:
        print(dict(zip(cols, row)))
else:
    print(f"Error: {rows}")
