import sys
sys.path.insert(0, r'C:\Users\clemensv\OneDrive - Microsoft\Agents\nius\nius_bot_dossier')
from kusto_client import get_client

client = get_client()
db = "bluesky"

# Check indexed_at type
q_schema = """
['Bluesky.Graph.Block_v1'] | getschema
"""
result = client.execute(db, q_schema)
rows = list(result.primary_results[0])
for r in rows:
    if 'indexed' in str(r).lower() or 'created' in str(r).lower():
        print(r)
print("---")
# Just show first few columns
for r in rows[:10]:
    print(dict(r))
