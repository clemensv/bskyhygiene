import sys
sys.path.insert(0, r'C:\Users\clemensv\OneDrive - Microsoft\Agents\nius')
from nius_bot_dossier.kusto_client import execute_query

DID = 'did:plc:kd4wtd75a637g2gvg2dh2b3t'

# Check schema
print("=== POST TABLE SCHEMA ===")
q = "['Bluesky.Feed.Post_v1'] | getschema"
df = execute_query(q)
print(df.to_string())
