import json, sys
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.identity import DefaultAzureCredential

CLUSTER = "https://trd-fssgb36e98qh3fk58u.z2.kusto.fabric.microsoft.com"
DATABASE = "bluesky"

def get_client():
    kcsb = KustoConnectionStringBuilder.with_azure_token_credential(
        CLUSTER, credential=DefaultAzureCredential()
    )
    return KustoClient(kcsb)

def run_query(client, query, label):
    sep = "=" * 70
    print(f"\n{sep}")
    print(f"QUERY: {label}")
    print(f"{sep}")
    response = client.execute(DATABASE, query)
    rows = []
    for row in response.primary_results[0]:
        rows.append(dict(zip([c.column_name for c in response.primary_results[0].columns], row)))
    print(f"Results: {len(rows)} rows")
    for i, row in enumerate(rows[:30]):
        print(json.dumps(row, default=str, ensure_ascii=False))
    if len(rows) > 30:
        print(f"... ({len(rows) - 30} more rows)")
    return rows

Q1 = """
// Co-follow clusters: hot targets among new accounts (last 7d)
let new_followers = 
    ['Bluesky.Graph.Follow_v1']
    | where ___time > ago(7d)
    | join kind=inner (
        ['Bluesky.Actor.Profile_v2']
        | summarize arg_max(___time, *) by did
        | where todatetime(created_at) > ago(30d)
        | project did, account_created=todatetime(created_at)
    ) on did
    | where subject != "did:plc:z72i7hdynmk6r22z27h6tvur"
    | project follower=did, target=subject, follow_time=todatetime(created_at), account_created;
let hot_targets =
    new_followers
    | summarize follower_count=dcount(follower) by target
    | where follower_count >= 50
    | project target;
new_followers
| where target in (hot_targets)
| summarize followers=make_set(follower, 200), cnt=dcount(follower) by target
| order by cnt desc
| take 30
"""

Q2 = """
// Temporal burst: accounts created same hour, then follow same targets
let recent_profiles =
    ['Bluesky.Actor.Profile_v2']
    | summarize arg_max(___time, *) by did
    | where todatetime(created_at) > ago(7d)
    | project did, created_hour=bin(todatetime(created_at), 1h);
let recent_follows =
    ['Bluesky.Graph.Follow_v1']
    | where ___time > ago(7d)
    | where subject != "did:plc:z72i7hdynmk6r22z27h6tvur"
    | project follower=did, target=subject, follow_time=todatetime(created_at);
recent_profiles
| join kind=inner recent_follows on $left.did == $right.follower
| summarize 
    accounts=dcount(did),
    sample_dids=take_any(did, 5),
    sample_targets=take_any(target, 3)
    by created_hour, target
| where accounts >= 20
| order by accounts desc
| take 50
"""

Q3 = """
// Follow-farm: targets receiving many followers from accounts with high overlap
let new_account_follows =
    ['Bluesky.Graph.Follow_v1']
    | where ___time > ago(7d)
    | join kind=inner (
        ['Bluesky.Actor.Profile_v2']
        | summarize arg_max(___time, *) by did
        | where todatetime(created_at) > ago(14d)
        | project did
    ) on did
    | where subject != "did:plc:z72i7hdynmk6r22z27h6tvur"
    | project follower=did, target=subject;
let follower_sets =
    new_account_follows
    | summarize targets=make_set(target), target_count=dcount(target) by follower
    | where target_count between (3 .. 50);
let popular_targets =
    new_account_follows
    | summarize inbound=dcount(follower) by target
    | where inbound >= 50;
new_account_follows
| where target in (popular_targets)
| join kind=inner follower_sets on follower
| summarize 
    follower_count=dcount(follower),
    avg_set_size=avg(target_count),
    median_set_size=percentile(target_count, 50)
    by target
| where follower_count >= 50
| order by follower_count desc
| take 30
"""

def main():
    client = get_client()
    print("Connected to Kusto cluster.")
    results = {}

    for name, query, label in [
        ("cofollow_clusters", Q1, "Co-Follow Clusters (hot targets among new accounts)"),
        ("burst_creation", Q2, "Temporal Burst Creation (same hour + same targets)"),
        ("follow_farm", Q3, "Follow-Farm Customer Detection (high overlap inbound)"),
    ]:
        try:
            results[name] = run_query(client, query, label)
        except Exception as e:
            print(f"{name} ERROR: {e}")
            results[name] = str(e)

    out_path = "d:/bskyhygiene/tmp/cofollow_results.json"
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(results, fh, default=str, ensure_ascii=False, indent=2)
    print(f"\nResults saved to {out_path}")

if __name__ == "__main__":
    main()
