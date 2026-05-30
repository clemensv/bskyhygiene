import sys
sys.path.insert(0, r'C:\Users\clemensv\OneDrive - Microsoft\Agents\nius')
from nius_bot_dossier.kusto_client import execute_query

DID = 'did:plc:kd4wtd75a637g2gvg2dh2b3t'

# Get recent posts from this account
print("=== RECENT POSTS (last 50) ===")
q = f"""
['Bluesky.Feed.Post_v1']
| where did == '{DID}'
| order by ___time desc
| take 50
| project ___time, text, langs, reply_parent, embed_type, embed_uri, tags
"""
df = execute_query(q)
for _, row in df.iterrows():
    t = str(row['___time'])[:19]
    text = (row['text'] or '')[:200]
    reply = "REPLY" if row['reply_parent'] else ""
    embed = row['embed_type'] or ''
    lang = row['langs'] or ''
    print(f"\n[{t}] {reply} {embed}")
    print(f"  {text}")
    if row['tags']:
        print(f"  Tags: {row['tags']}")

# Volume stats
print("\n\n=== POST VOLUME BY WEEK ===")
q2 = f"""
['Bluesky.Feed.Post_v1']
| where did == '{DID}'
| summarize posts = count(), 
    replies = countif(isnotempty(reply_parent)),
    originals = countif(isempty(reply_parent))
    by bin(___time, 7d)
| order by ___time desc
| take 10
"""
df2 = execute_query(q2)
print(df2.to_string())

# Language distribution
print("\n\n=== LANGUAGE DISTRIBUTION ===")
q3 = f"""
['Bluesky.Feed.Post_v1']
| where did == '{DID}'
| mv-expand langs
| summarize count() by tostring(langs)
| order by count_ desc
"""
df3 = execute_query(q3)
print(df3.to_string())

# Embed types (what kind of content)
print("\n\n=== CONTENT TYPES ===")
q4 = f"""
['Bluesky.Feed.Post_v1']
| where did == '{DID}'
| summarize count() by embed_type
| order by count_ desc
"""
df4 = execute_query(q4)
print(df4.to_string())
