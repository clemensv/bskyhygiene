"""Find cluster using known DIDs from previous session."""
import sys
sys.path.insert(0, r"C:\Users\clemensv\OneDrive - Microsoft\Agents\nius")
from nius_bot_dossier.kusto_client import execute_query

# Known DIDs from previous analysis
# miahungrigesherz.bsky.social = did:plc:ssi5lbrlise2g5b32hqzdbb4
# schreibersnaturarium.de = did:plc:kiopixvqglbzrhwghloh3uco

# Test: find follows FROM miahungrigesherz
q1 = """
['Bluesky.Graph.Follow_v1']
| where did == "did:plc:ssi5lbrlise2g5b32hqzdbb4"
| project did, handle, subject, subject_handle, created_at, ___time
| take 20
"""
df1 = execute_query(q1)
print(f"Follows FROM miahungrigesherz ({len(df1)} rows):")
print(df1.to_string())

# Test: find follows TO schreibersnaturarium
q2 = """
['Bluesky.Graph.Follow_v1']
| where subject == "did:plc:kiopixvqglbzrhwghloh3uco"
| summarize count()
"""
df2 = execute_query(q2)
print(f"\nFollows TO schreibersnaturarium:")
print(df2.to_string())

# Check what time range the table covers
q3 = """
['Bluesky.Graph.Follow_v1']
| summarize min(___time), max(___time), count()
"""
df3 = execute_query(q3)
print(f"\nFollow table time range:")
print(df3.to_string())
