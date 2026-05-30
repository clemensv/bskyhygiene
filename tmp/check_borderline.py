"""Quick timing check for borderline suspects (score=3)."""
import json
import sys
import time

import httpx

sys.path.insert(0, r"C:\Users\clemensv\OneDrive - Microsoft\Agents\nius")
from nius_bot_dossier.kusto_client import execute_query

with open(r"d:\bskyhygiene\investigations\2026-05-30-german-literary-bots\bot_dids.json") as f:
    cluster_data = json.load(f)

target_handles = {t["did"]: t["handle"] for t in cluster_data["targets"]}

# Resolve suspects
client = httpx.Client(timeout=30)
handles = [
    "fraurollmops.bsky.social",
    "alerta93.bsky.social",
    "sylveev2justexists.bsky.social",
    "derrechtenutzer.bsky.social",
]
params = [("actors", h) for h in handles]
r = client.get("https://public.api.bsky.app/xrpc/app.bsky.actor.getProfiles", params=params)
r.raise_for_status()
profs = {p["handle"]: p["did"] for p in r.json()["profiles"]}
print("Resolved:", list(profs.keys()))

# Also get their full follow lists
for handle, did in profs.items():
    time.sleep(0.3)
    resp = client.get(
        "https://public.api.bsky.app/xrpc/app.bsky.graph.getFollows",
        params={"actor": did, "limit": 100},
    )
    resp.raise_for_status()
    all_follows = resp.json().get("follows", [])
    target_follows = [f for f in all_follows if f["did"] in target_handles]
    non_cluster = [
        f for f in all_follows
        if f["did"] not in target_handles and f["did"] not in cluster_data["dids"]
    ]
    print(f"\n@{handle}:")
    print(f"  Total follows: {len(all_follows)} | Targets: {len(target_follows)}/{len(target_handles)} | Non-cluster: {len(non_cluster)}")
    if non_cluster:
        for f in non_cluster[:10]:
            print(f"    -> @{f.get('handle', '?')} ({f.get('displayName', '')[:30]})")

# Kusto timing
dids_kql = ", ".join([f'"{d}"' for d in profs.values()])
q = f"""
let suspects = dynamic([{dids_kql}]);
['Bluesky.Graph.Follow_v1']
| where did in (suspects)
| order by did asc, ___time asc
| project did, subject, ___time
"""
df = execute_query(q)

print("\n" + "=" * 70)
print("TIMING ANALYSIS")
print("=" * 70)

for handle, did in profs.items():
    rows = df[df["did"] == did].sort_values("___time")
    if len(rows) == 0:
        print(f"\n@{handle}: No data in Kusto")
        continue
    first = rows["___time"].iloc[0]
    last = rows["___time"].iloc[-1]
    dur = (last - first).total_seconds()
    n = len(rows)
    target_count = rows["subject"].isin(target_handles.keys()).sum()
    print(f"\n@{handle}:")
    print(f"  Follows: {n} | Targets hit: {target_count}/{len(target_handles)} | Duration: {dur:.0f}s ({dur/3600:.1f}h)")
    if n > 1:
        gaps = rows["___time"].diff().dt.total_seconds().dropna()
        print(f"  Median gap: {gaps.median():.1f}s | Max gap: {gaps.max():.0f}s ({gaps.max()/3600:.1f}h)")
    print("  Sequence:")
    for _, row in rows.iterrows():
        subj = target_handles.get(row["subject"], row["subject"][:40])
        print(f"    {row['___time']} -> {subj}")

client.close()
