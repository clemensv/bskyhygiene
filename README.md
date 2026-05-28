# Bluesky Network Hygiene

Investigations into coordinated inauthentic behavior on the Bluesky social network.

## Investigations

| Date | Target | Accounts | Summary |
|------|--------|----------|---------|
| [2026-05-28](investigations/2026-05-28-louisvillebsky-haruhwa/) | pds.louisvillebsky.app & haruhwa.com | 3,584 | Coordinated bot infrastructure: follow inflation + charity fraud scam |
| [2026-05-28](investigations/2026-05-28-burst-follow-spam/) | watchmelive.my.id / livechats.my.id | 389 | Burst-follow spam: 1,001 follows in <5 min, adult content promotion |
| [2026-05-27](investigations/2026-05-27-bshort-japanese-ring/) | b-short.link/C85gz9 | 604 | Japanese adult spam mutual-follow ring: 28K internal follows, traffic farming |

## Methodology

Analysis performed via KQL queries against Bluesky Firehose data ingested into Microsoft Fabric Eventhouse. Signals include:
- Profile completeness (avatar, description, display name)
- Follow/follower ratios and cadence
- Account creation temporal patterns
- Handle generation pattern analysis
- Co-follow network clustering

## Automated Blocklist

A daily GitHub Actions workflow scans both PDS servers and produces a scored blocklist:

- **[blocklists/blocklist.json](blocklists/blocklist.json)** — Full scored list with signals
- **[blocklists/blocklist.txt](blocklists/blocklist.txt)** — Plain DID list for import
- **[Heuristic documentation](blocklists/README.md)** — Scoring methodology

The workflow runs at 06:00 UTC daily and can be triggered manually.
