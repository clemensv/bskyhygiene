import sys
sys.path.insert(0, r'C:\Users\clemensv\OneDrive - Microsoft\Agents\nius')
from nius_bot_dossier.kusto_client import execute_query

DID = 'did:plc:kd4wtd75a637g2gvg2dh2b3t'

# Hypothesis 1: Are they blocking followers of specific large accounts?
# Check what accounts the VICTIMS commonly follow
print("=== WHAT DO BLOCKED ACCOUNTS FOLLOW IN COMMON? ===")
print("(Top followed-by targets among 5000 recent block victims)")
q = f"""
let victims = ['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| where ___time > ago(7d)
| sample 5000
| distinct subject;
['Bluesky.Graph.Follow_v1']
| where did in (victims)
| summarize followers_in_blocklist = dcount(did) by subject
| where followers_in_blocklist > 100
| order by followers_in_blocklist desc
| take 30
"""
df = execute_query(q)
print(df.to_string())
