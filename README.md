# Bluesky Network Hygiene

Investigations into coordinated inauthentic behavior on the Bluesky social network.

## Investigations

| Date | Target | Accounts | Summary |
|------|--------|----------|---------|
| [2026-06-20](investigations/2026-06-20-niusde-afd-revisit/) | @niusde.bsky.social → AfD (vs. SPD/Grüne controls) | 195 | Follow-amplification bot swarm boosting NIUS & AfD: 88% dense co-follow core vs. 28% for SPD/Grüne controls; 195 hardcore bots. Six-weeks-later revisit (20 Jun): 93% still live (barely moderated) but the operation has gone dormant — coordinated follows down to 1–10/day from the 867/48h May peak, zero current ≥3-follow targets. German-language dossier. |
| [2026-06-17](investigations/2026-06-17-haruhwa-multi-pds-expansion/) | 8 self-hosted PDS (haruhwa operator) | ≥74,038 | Multi-PDS sleeper expansion: same operator scaled onto 7 new PDS; 68K accounts in 4 days, synchronized 20.9s 8-host genesis + lockstep 06-15 pause, dormant pre-activation, nirasynth.xxx funnel |
| [2026-06-17](investigations/2026-06-17-haruhwa-spike/) | haruhwa.com | 10,585 | Sleeper-account surge: 702 → 10,585 (~15×) in 19 days; 94.6% created June 14–17 in machine-paced bursts, dormant stockpile, same operator |
| [2026-06-17](investigations/2026-06-17-onlyfans-funnel-swarm/) | OnlyFans affiliate funnel (account-level, bsky.network) | 3,326 | LLM-driven flirty reply-bot swarm: 638K posts in 30 days (88.5% replies) funnelling via s.gy → onlyfans.com referral codes to 2,142 creators; leaked LLM caption text + identical traceback across 79 accounts prove shared tooling; 28% already suspended |
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

A daily GitHub Actions workflow scans all confirmed bot clusters and produces a scored blocklist:

- **[blocklists/blocklist.json](blocklists/blocklist.json)** — Full scored list with signals
- **[blocklists/blocklist.txt](blocklists/blocklist.txt)** — Plain DID list for import
- **[Heuristic documentation](blocklists/README.md)** — Scoring methodology
- **[🦋 Bluesky Moderation List](https://bsky.app/profile/did:plc:sthd2dnrddxe6icdqza2oryx/lists/3mmvjoj2jqq2p)** — Subscribe to block all identified bots

The workflow runs at 06:00 UTC daily and can be triggered manually.
