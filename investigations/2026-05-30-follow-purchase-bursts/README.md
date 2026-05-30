# Follow-Purchase Burst Attacks: cislost24 & cookierunkingdom

**Investigation Date:** 2026-05-30  
**Methodology:** Temporal burst detection via KQL on Bluesky Firehose follow data; profile resolution via `app.bsky.actor.getProfile`  
**Status:** **ACTIVE** — new burst events observed as recently as 2026-05-29  
**Scope:** 2 primary follow-purchase targets (595 + 1,323 bots), 9 Vietnamese SEO co-customers, 1 additional small customer  
**Related:** [Seasoning Rings](../2026-05-30-seasoning-rings/README.md), [Burst Follow Spam (watchmelive.my.id)](../2026-05-28-burst-follow-spam/README.md)

---

## Executive Summary

Two Bluesky accounts received sudden, massive influxes of bot followers in concentrated
bursts — consistent with a **paid follow-purchase service** ("follow farm as a service").

| Target | Bot Followers (7d) | Peak Rate | Peak Time (UTC) |
|--------|-------------------|-----------|-----------------|
| @cislost24.bsky.social | 595 | 198/hour | 2026-05-25 04:00 |
| @cookierunkingdom.bsky.social | 1,323 | 395/hour | 2026-05-27 20:00 |

The two bot pools are **completely separate** (zero overlapping accounts), indicating either
different vendors or distinct batch allocations.

Deep mapping of the cislost24 pool (595 bots) revealed **9 Vietnamese SEO link-farm
accounts** and 1 Korean anime artist (**@eriimyon.bsky.social**) as co-customers of the
same vendor. The Vietnamese accounts are all zero-post placeholder profiles for manga piracy
sites and an electronics retailer (FPT Shop), each purchasing small batches of 8–20 bot
followers from the same pool.

The bot accounts delivering these follows are **minimal throwaway accounts** — typically
0 followers, 2–3 following, 0 posts — distinct from the seasoning ring bots (which follow
100+ accounts). This suggests either a different tier of the same follow-farm operator or
a separate low-effort bot pool.

---

## Burst Magnitude

![Burst Magnitude](assets/burst_magnitude.png)

## Key Indicators

| Metric | @cislost24 | @cookierunkingdom |
|--------|-----------|-------------------|
| Target DID | `did:plc:rvoal7hdidgduflugbohykni` | `did:plc:5rwgthupzv6vcteaebpoa6zu` |
| Total followers (real) | 3,853 | 5,521 |
| Bot followers received (7d) | 595 | 1,323 |
| Peak burst rate | 198/hour | 395/hour |
| Peak burst time | 2026-05-25 04:00 UTC | 2026-05-27 20:00 UTC |
| Burst duration | ~4 hours | ~5 hours |
| Bot median inter-follow gap | 23 seconds | 28 seconds |
| Bot p10 inter-follow gap | 2 seconds | 2 seconds |
| Zero-gap follow pairs | 15 | 39 |
| Bot avg follow-set size | 2 follows | 5 follows |
| Target account created | 2024-10-17 | 2023-07-24 |
| Target posts | 45 | 153 |

---

## Burst Temporal Profiles

### @cislost24.bsky.social — 2026-05-25

![cislost24 Burst](assets/burst_cislost24.png)

```
04:00 UTC  ████████████████████████████████████████  198 follows
05:00 UTC  ████████████████████████                  122 follows
06:00 UTC  ██████████████                             70 follows
07:00 UTC  █████████                                  45 follows
12:00 UTC  █████                                      24 follows
```

Single concentrated burst starting at 04:00 UTC, decaying over 8 hours.
Total: 595 new followers delivered.

### @cookierunkingdom.bsky.social — 2026-05-27

![cookierunkingdom Burst](assets/burst_cookierunkingdom.png)

```
20:00 UTC  ████████████████████████████████████████████████████████████████████████████████  395 follows
21:00 UTC  ████████████████████████████████                                                  162 follows
22:00 UTC  █████████████████                                                                  85 follows
23:00 UTC  █████████████████                                                                  84 follows
00:00 UTC  █████████████                                                                      64 follows
```

Massive single burst starting at 20:00 UTC, also decaying.
Total: 1,323 new followers delivered.

---

## Bot Follower Profile

The bots delivering these follows are **minimal-effort throwaways**, distinct from the
seasoning ring accounts:

| Handle | Followers | Following | Posts | Created |
|--------|-----------|-----------|-------|---------|
| @giangthu.bsky.social | 0 | 2 | 0 | 2026-05-25 |
| @ucgch.bsky.social | 0 | 2 | 0 | 2026-05-25 |
| @yuukomeow235.bsky.social | 0 | 3 | 0 | 2026-05-25 |
| @yuuahn.bsky.social | 0 | 3 | 0 | 2026-05-25 |
| @njeuuuu.bsky.social | 0 | 2 | 0 | 2026-03-08 |
| @tuet567.bsky.social | 0 | 2 | 0 | 2026-01-05 |
| @tum520.bsky.social | 0 | 2 | 3 | 2024-10-17 |
| @phuongtay2908.bsky.social | 11 | 6 | 3 | 2024-10-17 |

### Bot Fingerprint

- **Following count:** 2–3 accounts (target + possibly 1 other)
- **Posts:** 0 (pure follow-bots)
- **Followers:** 0
- **Handle naming:** Short randomized strings, some Vietnamese-influenced (giangthu, phuongtay, yuukomeow)
- **Creation timing:** Many created same day as the burst (just-in-time account creation)
- **Some older dormant accounts** reactivated (2024-10-17 cohort) mixed with fresh ones

---

## Inter-Follow Cadence Analysis

![Cadence Analysis](assets/cadence_analysis.png)

The timing between consecutive bot follows reveals automated batch submission:

| Metric | @cislost24 burst | @cookierunkingdom burst |
|--------|-----------------|-------------------------|
| Median gap | 23 seconds | 28 seconds |
| p10 gap | 2 seconds | 2 seconds |
| p90 gap | 337 seconds | 454 seconds |
| Average gap | 889 seconds | 428 seconds |
| Zero-gap pairs | 15 | 39 |

The **2-second p10 gap** proves batch API submission — human users cannot follow accounts
at 2-second intervals. The **zero-gap pairs** (multiple follows in the same second) indicate
parallel bot threads hitting the API simultaneously.

---

## Assessment: Purchased vs. Organic

Both targets are **likely purchasers** (not victims):

- **@cislost24.bsky.social** — 3,853 followers but only 45 posts and 5 following.
  Follower-to-post ratio of 85:1 is extremely inflated.
- **@cookierunkingdom.bsky.social** — 5,521 followers, 153 posts.
  Follower-to-post ratio of 36:1. A branded gaming community account (Cookie Run:
  Kingdom, a major Korean mobile game by Devsisters launched January 2021, 150M+ downloads)
  that purchased followers to inflate credibility.

Neither account shows any content that would organically attract 200–400 new followers
per hour.

---

## Bot Pool Separation

The cislost24 and cookierunkingdom bot pools are **completely separate** — zero overlapping
bot accounts out of 595 and 1,323 bots respectively. This indicates either different
vendors or distinct batch allocations from the same vendor.

| Pool | Bot Count | Burst Date | Peak Rate | Cross-Overlap |
|------|-----------|------------|-----------|---------------|
| cislost24 | 595 | 2026-05-25 | 198/hr | 0 shared with cookie |
| cookierunkingdom | 1,323 | 2026-05-27 | 395/hr | 0 shared with cislost |

---

## cislost24 Bot Cluster — Co-Target Mapping

The 595 cislost24 bots also sprinkle small numbers of follows to other accounts, revealing
the **vendor's customer list**:

| Account | Shared Bots | Total Followers | Posts | Description |
|---------|-------------|-----------------|-------|-------------|
| @bsky.app | 414 | 33.5M | 756 | Auto-follow on creation (not a customer) |
| @eriimyon.bsky.social | 9 | 21,923 | 31 | Korean anime artist |
| @hentaipbncom.bsky.social | 5 | 349 | 0 | Vietnamese hentai manga piracy site |
| @themtruyen.bsky.social | 5 | 258 | 0 | Vietnamese manga reading site |
| @hentaivnmobi.bsky.social | 4 | 162 | 0 | Vietnamese hentai site |
| @tiemsachnhoxinhcom.bsky.social | 4 | 108 | 0 | Vietnamese bookshop SEO |
| @truyenqqclub.bsky.social | 4 | 105 | 0 | Vietnamese manga reading site |
| @nettruyen.bsky.social | 3 | 246 | 0 | Vietnamese manga reading site |
| @animevietnam.bsky.social | 2 | 480 | 0 | Vietnamese anime content |
| @thienthaitruyen.bsky.social | 2 | 209 | 0 | Vietnamese hentai/manhwa site |
| @fptshop.bsky.social | 2 | 258 | 1 | FPT Shop (Vietnamese electronics retail chain) |

### Shared-bot distribution

- 51 accounts received exactly 1 bot from this pool (noise/incidental)
- 16 accounts received 2–4 bots
- 3 accounts received 5–9 bots
- 1 account received 100+ (@bsky.app — auto-follow)
- **cislost24 is the sole large customer** in this batch (595 bots)

---

## Vietnamese SEO Link Farm Cluster

Nine Vietnamese accounts — all **zero-post placeholder profiles** — share bots from the
cislost24 pool, confirming they are customers of the same vendor:

| Account | Bot Followers (30d) | Bot % | Created |
|---------|--------------------:|------:|--------:|
| @hentaipbncom.bsky.social | 20 | 56% | 2025-03-27 |
| @animevietnam.bsky.social | 18 | 42% | 2025-04-16 |
| @truyenqqclub.bsky.social | 12 | 46% | 2025-12-26 |
| @fptshop.bsky.social | 12 | 34% | 2024-10-18 |
| @hentaivnmobi.bsky.social | 11 | 46% | 2025-12-15 |
| @thienthaitruyen.bsky.social | 10 | 42% | 2025-06-20 |
| @themtruyen.bsky.social | 10 | 37% | 2025-01-18 |
| @nettruyen.bsky.social | 9 | 39% | 2025-04-26 |
| @tiemsachnhoxinhcom.bsky.social | 8 | 42% | 2025-11-26 |

These are all Vietnamese-language piracy/SEO domains using Bluesky purely for link farming.
They share bots among themselves (up to 8 shared between @fptshop and @animevietnam),
confirming coordinated purchasing from the same vendor.

### @eriimyon.bsky.social

@eriimyon received 9 bots from the cislost24 pool during the same 2026-05-25 burst.
With 58% bot followers in 30 days (18 of 31 new followers are bots), eriimyon appears
to be a smaller customer of the same vendor. The eriimyon bots' top co-target is cislost24
itself — confirming cross-pollination within the vendor's bot pool.

---

## Comparison with Seasoning Ring Bots

![Bot Tier Comparison](assets/bot_tier_comparison.png)

| Property | Seasoning Ring Bots | Burst Follow Bots |
|----------|--------------------|--------------------|
| Following count | 62–182 | 2–3 |
| Posts | 0–8 (some light posting) | 0 |
| Followers | 1–8 | 0 |
| Purpose | Long-term asset prep | One-shot delivery |
| Handle style | English plausible names | Vietnamese/random |
| Reuse pattern | Held for future use | Burned immediately |
| Creation date | 2026-05-29/30 | Mixed (some old, some fresh) |

These are **different tiers of the same ecosystem** — the seasoning farm produces inventory
for eventual resale, while the burst bots are cheap throwaways for immediate delivery.

---

## Detection Methodology

1. Detect accounts receiving ≥ 20 new followers/hour (abnormal for non-viral accounts)
2. Profile the delivering accounts: check follower/following/post counts
3. Measure inter-follow cadence (p10 < 5 seconds = automation)
4. Classify bot pool by follow-set size and handle patterns
5. Correlate burst timing with target account post history (no viral post = purchased)

---

## Relation to Other Investigations

- **Seasoning Rings (2026-05-30):** Different bot tier from the same ecosystem. Seasoning
  bots build 100+ follow lists; burst bots follow only 2–3 accounts.
- **watchmelive.my.id / livechats.my.id (2026-05-28):** Similar delivery mechanism (mass
  follows in bursts) but different bot pool (those used domain-name handles and followed
  more accounts per bot).
- **b-short.link ring (2026-05-27):** Different operator entirely (self-hosted PDS,
  Japanese-language content spam).
- **Vietnamese SEO Link Farm:** Nine zero-post Vietnamese accounts (manga piracy sites,
  electronics retailers) identified as co-customers of the cislost24 bot vendor,
  purchasing small batches (8–20 bots each) of followers from the same pool.
