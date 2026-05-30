"""Quick test to verify the Kusto table structure and find the correct DIDs."""
import sys
sys.path.insert(0, r"C:\Users\clemensv\OneDrive - Microsoft\Agents\nius")
from nius_bot_dossier.kusto_client import execute_query

# Test 1: Find colettemschmidt's DID from the profile table
q1 = """
['Bluesky.Actor.Profile_v2']
| where handle == "colettemschmidt.bsky.social"
| summarize arg_max(___time, *) by did
| project did, handle, display_name, created_at
"""
df1 = execute_query(q1)
print("colettemschmidt DID:")
print(df1.to_string())

# Test 2: Find schreibersnaturarium
q2 = """
['Bluesky.Actor.Profile_v2']
| where handle == "schreibersnaturarium.de"
| summarize arg_max(___time, *) by did
| project did, handle, display_name, created_at
"""
df2 = execute_query(q2)
print("\nschreibersnaturarium DID:")
print(df2.to_string())

# Test 3: Check follow table columns
q3 = """
['Bluesky.Graph.Follow_v1']
| take 3
| getschema
"""
df3 = execute_query(q3)
print("\nFollow table schema:")
print(df3.to_string())
