"""Resolve DIDs for false positive handles."""
import httpx
client = httpx.Client(timeout=30)
handles = ["jens-kessler.bsky.social", "alerta93.bsky.social"]
params = [("actors", h) for h in handles]
r = client.get("https://public.api.bsky.app/xrpc/app.bsky.actor.getProfiles", params=params)
r.raise_for_status()
for p in r.json()["profiles"]:
    print(f"{p['handle']}: {p['did']}")
client.close()
