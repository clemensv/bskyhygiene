"""Resolve handles for newly discovered upstream feeders."""
import sys
sys.path.insert(0, r'C:\Users\clemensv\OneDrive - Microsoft\Agents\nius')
from nius_bot_dossier.kusto_client import execute_query
import requests

# New accounts from the upstream list that aren't already known
NEW_UPSTREAM = [
    'did:plc:qq2eg3kbh44gytxlghozodeb',
    'did:plc:u4kyi5eku6acyjqiwrx45glt',
    'did:plc:qhmqv54lreu6hitrlxoxiwfo',
    'did:plc:gncqaxyrjk7lsx4egwc22qqn',
    'did:plc:txlljch2haw3i6vnepsyexkw',
    'did:plc:yeenqpcf3tkaz26bsirixkcg',
    'did:plc:my4y4kiye3p7fupbaixtjus2',
    'did:plc:omt6zz23vj44xfl6ekkqp5wo',
    'did:plc:x6gigvjpxnn4q5dxgx3bodhu',
    'did:plc:odx5orgsms2mzt7pwdmaovux',
    'did:plc:gzymou6pwrauuqn7wuqfggj2',
    'did:plc:7d2g5clfogwwcz6fqrawok53',
    'did:plc:wdle4b3gjbetxgu6zlosts3m',
    'did:plc:r3ywamne2b2sjrbxxmwkhd4z',
    'did:plc:pw5ytxlw2sadqwygvlou2fja',
    'did:plc:d6qtq6hxj7aezzgfez3ptu6x',
    'did:plc:y5olvi5q3puwchgm5cqhdq3h',
    'did:plc:33onfgatewrcdlrh5euc34lp',
    'did:plc:ijlan7hjfdzxnuiefzarujpt',
    'did:plc:aozmdbjiozwbz7ws7lhjnt6j',
    'did:plc:uuh73n45gf4imkalnskvoait',
    # Also the original high-overlap list members not yet resolved
    'did:plc:4fn4mppxm73jldgas7a52kcu',
    'did:plc:lsaii34slgzwooxhfesamrk2',
    'did:plc:jyqk4xrplfhsl6dfeibuw37c',
    'did:plc:zcx3ryxqcbc4tawv7bam64mq',
    'did:plc:ye2r45gcu33r5gkbb2dajb34',
    'did:plc:qyuua6edp64sxlwcb6myitst',
]

print("=== RESOLVING HANDLES FOR NEW UPSTREAM ACCOUNTS ===\n")
print(f"{'DID':<45} {'Handle':<35} {'Display':<25} {'F':>5} {'Posts':>6}")
print("-" * 125)

for did in NEW_UPSTREAM:
    try:
        r = requests.get(
            'https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile',
            params={'actor': did},
            timeout=10
        )
        if r.status_code == 200:
            p = r.json()
            handle = p.get('handle', '?')
            display = p.get('displayName', '')[:24]
            followers = p.get('followersCount', 0)
            posts = p.get('postsCount', 0)
            print(f"{did:<45} {handle:<35} {display:<25} {followers:>5} {posts:>6}")
        elif r.status_code == 400:
            print(f"{did:<45} {'*** DELETED/SUSPENDED ***':<35} {'':<25}")
        else:
            print(f"{did:<45} {'HTTP ' + str(r.status_code):<35}")
    except Exception as e:
        print(f"{did:<45} Error: {e}")
