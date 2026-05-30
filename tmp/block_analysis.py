import sys
sys.path.insert(0, r'C:\Users\clemensv\OneDrive - Microsoft\Agents\nius')
from nius_bot_dossier.kusto_client import execute_query

DID = 'did:plc:kd4wtd75a637g2gvg2dh2b3t'

# 1. Burst timing on heaviest day (May 27)
print("=== INTER-BLOCK TIMING (May 27) ===")
q = f"""
['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| where ___time between (datetime(2026-05-27) .. datetime(2026-05-28))
| order by ___time asc
| extend prev_time = prev(___time)
| extend delta_ms = datetime_diff("millisecond", ___time, prev_time)
| where isnotnull(prev_time)
| summarize 
    p50_delta_ms = percentile(delta_ms, 50),
    p10_delta_ms = percentile(delta_ms, 10),
    p90_delta_ms = percentile(delta_ms, 90),
    min_delta_ms = min(delta_ms),
    max_delta_ms = max(delta_ms),
    count_sub_100ms = countif(delta_ms < 100),
    count_sub_1s = countif(delta_ms < 1000),
    total = count()
"""
df = execute_query(q)
print(df.to_string())

# 2. Hourly distribution on May 27
print("\n=== HOURLY DISTRIBUTION (May 27) ===")
q2 = f"""
['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| where ___time between (datetime(2026-05-27) .. datetime(2026-05-28))
| summarize blocks = count() by hour = bin(___time, 1h)
| order by hour asc
"""
df2 = execute_query(q2)
print(df2.to_string())

# 3. Who is being blocked? Check if they share characteristics
print("\n=== SAMPLE BLOCKED ACCOUNTS (last 100) ===")
q3 = f"""
['Bluesky.Graph.Block_v1']
| where did == '{DID}'
| order by ___time desc
| take 100
| project ___time, subject, subject_handle
"""
df3 = execute_query(q3)
print(df3.to_string())
