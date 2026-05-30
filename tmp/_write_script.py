import pathlib

script = '''import json, sys
from datetime import datetime, timezone
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.identity import DefaultAzureCredential

CLUSTER = "https://trd-fssgb36e98qh3fk58u.z2.kusto.fabric.microsoft.com"
DATABASE = "bluesky"

def get_client():
    kcsb = KustoConnectionStringBuilder.with_azure_token_credential(
        CLUSTER, credential=DefaultAzureCredential()
    )
    return KustoClient(kcsb)
'''

pathlib.Path(r'd:\bskyhygiene\tmp\cofollow_hunter.py').write_text(script, encoding='utf-8')
print('Part 1 written')
