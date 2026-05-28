# Bluesky Network Hygiene

Investigations into coordinated inauthentic behavior on the Bluesky social network.

## Investigations

| Date | Target | Accounts | Summary |
|------|--------|----------|---------|
| [2026-05-28](investigations/2026-05-28-louisvillebsky-haruhwa/) | pds.louisvillebsky.app & haruhwa.com | 3,584 | Coordinated bot infrastructure: follow inflation, engagement rings, impersonation |

## Methodology

Analysis performed via KQL queries against Bluesky Firehose data ingested into Microsoft Fabric Eventhouse. Signals include:
- Profile completeness (avatar, description, display name)
- Follow/follower ratios and cadence
- Account creation temporal patterns
- Handle generation pattern analysis
- Co-follow network clustering
