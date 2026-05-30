"""Find the target DIDs via the follow table, then identify the cluster."""
import sys
sys.path.insert(0, r"C:\Users\clemensv\OneDrive - Microsoft\Agents\nius")
from nius_bot_dossier.kusto_client import execute_query

# Find DIDs from the follow table's subject_handle
q1 = """
['Bluesky.Graph.Follow_v1']
| where subject_handle has "colettemschmidt" or subject_handle has "schreibersnaturarium"
| summarize count() by subject, subject_handle
| take 10
"""
df1 = execute_query(q1)
print("Target DIDs from follow table:")
print(df1.to_string())

# Also try handle column (follower side)
q2 = """
['Bluesky.Graph.Follow_v1']
| where handle has "hungrigesherz"
| take 5
| project did, handle, subject, subject_handle, created_at, ___time
"""
df2 = execute_query(q2)
print("\nExample bot (miahungrigesherz):")
print(df2.to_string())
