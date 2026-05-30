# Coordinated Automated Mass-Blocking Ring — International Progressive Targeting

**Date:** 2026-05-30 (updated 2026-05-31)  
**Status:** Confirmed coordinated blocklist automation — **ACTIVE**  
**Trigger:** Report of `louisbetonberlin.bsky.social` blocking large numbers of accounts  

## Summary

`louisbetonberlin.bsky.social` (DID: `did:plc:kd4wtd75a637g2gvg2dh2b3t`) is operating
an automated mass-blocking tool that has issued **48,179 blocks** (44,096 unique victims)
since April 29, 2026. The account is part of a **coordinated blocking ring** of 16+ accounts
that have collectively blocked **602,673+ unique accounts** (~3% of Bluesky). Despite being
German-speaking, the ring primarily targets **English-speaking US progressives** who engage
with major anti-Trump commentators (Aaron Rupar, Ron Filipkowski, Jon Cooper). The targeting
mechanism crawls engagement on viral progressive posts and filters for the most active accounts.
The ring members **do not follow each other on Bluesky** — the blocklist is distributed via
an off-platform channel.

## Key Account

| Field | Value |
|-------|-------|
| Handle | `louisbetonberlin.bsky.social` |
| DID | `did:plc:kd4wtd75a637g2gvg2dh2b3t` |
| Display | Louis Beton |
| Created | 2023-08-24 |
| Followers | 942 |
| Following | 692 |
| Posts | 11,966 |
| Bio | Silver Jews quote + "Santiago (Chile) & Hamburg & Frankfurt Main & Hildesheim & Berlin" |
| Labels | `!no-unauthenticated` |

## Evidence of Automation

### Timing Analysis

The inter-block timing makes manual operation physically impossible:

| Metric | Value |
|--------|-------|
| Total blocks | 48,179 |
| Unique victims | 44,096 |
| Median inter-block gap (automated days) | **71–97 ms** |
| P95 gap (automated days) | 187–265 ms |
| Blocks with <100ms gap on May 27 | 7,945 |
| Peak single-day volume (May 27) | 11,574 blocks |
| Sample: 100 blocks in 6 seconds | Confirmed |

![Daily block volume](assets/daily_blocks.png)

![Inter-block gap distribution](assets/gap_distribution.png)

### Phase Transition: Manual → Automated

The account shows a clear phase transition from manual blocking to tool-assisted mass-blocking:

| Period | Behavior | Median gap | Daily volume |
|--------|----------|-----------|-------------|
| Apr 29 – May 5 | Manual | 69–279 sec | 4–48 blocks |
| May 6 (onset) | First automation run | **94 ms** | 1,714 blocks |
| May 7 – May 12 | Mixed manual/auto | Variable | 1–109 |
| May 13 onwards | Regular automated runs | **71–97 ms** | 446–11,574 |

### Operating Hours

All automated blocking sessions occur during **German daytime hours** (12:00–23:00 CET),
concentrated 13:00–22:00, consistent with Hamburg/Berlin timezone.

![Peak day hourly pattern](assets/peak_day_hourly.png)

## Victim Profile

Sampled 100 blocked accounts (random from all-time blocks):

| Characteristic | Count |
|----------------|-------|
| Created 2023 | 40% |
| Created 2024 | 36% |
| Created 2025 | 18% |
| Created 2026 | 6% |
| **1000+ followers** | **45%** |
| 100–999 followers | 36% |
| 10–99 followers | 16% |
| <10 followers | 3% |
| `!no-unauthenticated` label | 30% |

### Thematic Profile of Victims

Sample blocked accounts include:

- **Doro Blancke** (4,275 followers) — Human Rights Defender, Austria/Greece
- **Mosie** (4,755 followers) — "Progressive lefty" 70-something
- **Nosoda** (576 followers) — "Demokratie, Klimaschutz, AFDNEE"
- **Todotoday** (402 followers) — "#Klimakatastrophe / auf der Suche nach Lösungen"
- **Michael Felzmann** (51 followers) — "Grüne Mauerbach, Klima und Biodiversität"
- **Musikschule Bad Salzuflen** (970 followers) — Music school
- **gammaray** (1,557 followers) — "Kohlenstoffbasierte Lebensform"
- **xgrnsxs** (348 followers) — "Metalhead und ITler mit ADHS"
- **Fridde** (111 followers) — "Feministin, Ehefrau, Mutter"

The blocklist targets the **German-speaking progressive community** broadly — climate, feminism,
anti-AfD, Greens, human rights advocates, and general left-leaning accounts. Some non-German
accounts are also included.

## Coordinated Ring

### Shared Victim Overlap

The same blocklist is being used by multiple accounts:

| Account | Total blocks (7d) | Shared victims with louisbetonberlin |
|---------|-------------------|--------------------------------------|
| `smatsto.bsky.social` | 85,062 | **7,291** |
| `did:plc:qildfzoh5p24jgion4xiycvz` | 51,019 | 5,213 |
| `kaffchris.bsky.social` | ~7,270 | 4,252 |
| `did:plc:xcytuwwb3b33ipiqzmqzbs45` | 43,176 | 4,221 |
| `wystrach.de` | 14,224 | 3,585 |
| `did:plc:ajvwz5alprhutyx3zuwrg7dc` | — | 3,333 |
| `did:plc:gkg3mo2wltuzdzww53rkxfqg` | — | 2,979 |
| `did:plc:33wcrgvuwuxvzpa74yud37qp` | 33,998 | 2,301 |

### Ring Member Profiles

| Handle | Display | Followers | Labels | Notes |
|--------|---------|-----------|--------|-------|
| `smatsto.bsky.social` | — | 22 | — | Tiny account, 85K blocks |
| `kaffchris.bsky.social` | Kaffchris | 436 | `!no-unauthenticated` | FC Wacker München |
| `fuenfuhrteefix.bsky.social` | O'Fünfuhrteefix | 268 | `!no-unauthenticated` | Münster |
| `holbidope.bsky.social` | Berger Smith | 323 | `!no-unauthenticated` | "stay-in-bed hermit" |
| `wystrach.de` | Thomas Wystrach | 1,811 | `!no-unauthenticated` | Politics & religion writer |
| `kunststein.bsky.social` | Kunststein | 171 | `!no-unauthenticated` | "suspected of being Antifa" |
| `louisbetonberlin.bsky.social` | Louis Beton | 942 | `!no-unauthenticated` | Subject of this report |

### Ring Characteristics

- Most ring members use `!no-unauthenticated` label (privacy-conscious)
- `smatsto.bsky.social` has only 22 followers but 85K blocks — likely a dedicated blocking account
- Victim overlap of 7,291 accounts between the top two blockers confirms a **shared blocklist source**
- All automated blocking runs show the same ~70–100ms inter-block timing pattern

![Ring member block counts](assets/ring_comparison.png)

![Ring coordination timeline](assets/ring_timeline.png)

## Targeting Mechanism

### How Victims Are Found

The investigation tested multiple hypotheses for how the ring discovers accounts to block:

| Hypothesis | Result |
|-----------|--------|
| Scraping a single account's follower list | **No** — no single account >3.8% overlap with blocklist |
| Alphabetically sorted DID iteration | **No** — correlation = −0.04 (random) |
| Sequential follower-list order | **No** — block order does not match any target's follow timestamps |
| Blocking their own followers | **No** — only 3 of 44K blocked accounts follow Louis |
| Single shared blocklist | **Partial** — only 17% of Louis's blocks overlap with smatsto |

### Actual Mechanism: Engagement Crawling + Activity Filtering

The evidence points to a **crawl-and-filter approach targeting people who engage with viral
progressive posts**:

1. **Source: Viral post engagement** — Victims disproportionately reply to posts by major
   progressive accounts:
   - **Aaron Rupar** (`atrupar.com`, 950K followers) — independent journalist
   - **Ron Filipkowski** (782K followers) — MeidasNews editor
   - **Jon Cooper** (524K followers) — Democratic strategist
   - **Hoodlum** (250K followers) — progressive commentary
   - **Raider** (80K followers) — progressive activist

2. **Filter: Activity level** — Blocked accounts are **2× more active** than unblocked repliers
   to the same posts (median 284 posts/month vs. 109). The tool selects the most vocal accounts.

   ![Activity filter comparison](assets/activity_filter.png)

3. **Blocking rate on viral posts**: Approximately **12%** of all repliers to major progressive
   posts end up blocked — not all repliers, but the most active ones.

4. **Batch processing**: Blocks arrive in distinct batches separated by 5–30+ minute pauses,
   with peak rates of 1,116 blocks/minute within a batch. On May 27, there were 18 pauses
   >5 minutes across the day's 11,485 blocks.

### Language Profile of Victims (Posts in May 2026)

| Language | Posts |
|----------|-------|
| English | 4,702,496 |
| Spanish | 326,046 |
| German | 293,444 |
| French | 153,797 |
| Dutch | 123,936 |

**Key finding**: Despite the ring being German-speaking, the overwhelming majority of victims are
**English-speaking US progressives**. German accounts are only ~5% of the target pool. This is an
**internationally-scoped political blocking campaign** — not a German-community-internal dispute.

![Language of victim posts](assets/victim_languages.png)

### Ring Coordination Timeline

| DID/Account | First block | Last block | Total blocks |
|------------|-------------|------------|-------------|
| `did:plc:qildfzoh5p24jgion4xiycvz` | Apr 28 | May 30 | 103,214 |
| `louisbetonberlin` | Apr 29 | May 30 | 48,179 |
| `did:plc:hwpiekun4iebo4oqevjfe6ss` | Apr 29 | May 30 | 98,532 |
| `did:plc:tfspkb2htmw7vwdgqj7mzx7m` | Apr 29 | May 30 | 27,972 |
| `smatsto.bsky.social` | May 1 | May 30 | **495,878** |
| `did:plc:xcytuwwb3b33ipiqzmqzbs45` | May 4 | May 30 | 93,961 |

All 6 members started within a 6-day window (Apr 28 – May 4). Combined, the ring has issued
**867,736 blocks** against **602,673 unique accounts** — approximately 3% of all Bluesky users.

### Smatsto: The Central Blocking Engine

`smatsto.bsky.social` (22 followers, 0 meaningful content) runs **495,878 blocks** — 10× more than
Louis. Timing analysis shows smatsto blocks first in **72% of shared targets** (median 9 days
before Louis). This account appears to be the **primary crawling engine** that discovers targets,
with other ring members consuming portions of its output on a delay.

However, 67% of Louis's blocks (29,992) do NOT overlap with smatsto at all — suggesting Louis
also runs independent targeting in addition to consuming shared lists.

### Infrastructure

The automation characteristics are:

- **Rate-limited API calls** — 70–100ms gap is consistent with `com.atproto.repo.createRecord`
  rate limits
- **Zero moderation lists** (associated.lists = 0) — direct API blocking, not Bluesky's native
  list feature
- **Batch import pattern** — bursts of hundreds/thousands with pauses for loading next batch
- **German timezone operation** — all runs between 12:00–23:00 CET

## Extended Ring: Additional Blocklist Consumers

Beyond the 6 core members, at least **10 additional accounts** consume the same blocklist with
automated timing patterns:

| Handle | Blocks | Median gap | Shared w/ smatsto | Active period |
|--------|--------|-----------|-------------------|---------------|
| `dqita.bsky.social` | 134,559 | 197 ms | 104,812 | May 9–11 |
| `adametokirkfor.bsky.social` | 96,135 | 1,001 ms | 96,485 | Apr 30 – May 30 |
| `maribel1917.bsky.social` | 96,189 | 177 ms | 96,476 | May 6–23 |
| `castironirish.bsky.social` | 96,273 | 106 ms | 96,371 | May 1–30 |
| `solire.bsky.social` | 80,026 | 132 ms | 22,987 | Apr 29 – May 29 |
| `sasunarusasu.bsky.social` | 71,795 | 1,076 ms | 21,709 | May 4–23 |
| `fakeflamesprite.bsky.social` | 62,162 | 80 ms | 17,306 | Apr 29 – May 30 |
| `fkftsh.myatproto.social` | 51,415 | 97 ms | 27,767 | Apr 30 – May 30 |
| `vappytoy.bsky.social` | 36,629 | 200 ms | 36,706 | Apr 30 – May 30 |
| `verezi.bsky.social` | 31,348 | 72 ms | 17,141 | Apr 30 – May 24 |

Notable characteristics:
- `dqita` ("Dept of Queer, Intersex…") — 134K blocks in **just 2 days**, 48 followers
- `adametokirkfor`, `maribel1917`, `castironirish` — 96K blocks each, near-identical overlap
  with smatsto (96,371–96,485), suggesting the **same batch file imported**
- `vappytoy` — 3 followers, 0 posts, `!no-unauthenticated` — pure blocking puppet
- `wertercatt.eurosky.social` — flagged as `bot` by label service, 1,387 followers but 9,231 following

### Overlap with louisbetonberlin's targets

| Handle | Shared w/ Louis | Total blocks | Overlap % |
|--------|----------------|--------------|-----------|
| `sasunarusasu` | 4,600 | 4,610 | 99.8% |
| `solire` | 3,770 | 4,919 | 76.6% |
| `dqita` | 3,386 | 3,592 | 94.3% |
| `adametokirkfor` | 3,226 | 3,225 | 100.0% |
| `castironirish` | 3,186 | 3,195 | 99.7% |
| `maribel1917` | 3,161 | 3,169 | 99.7% |
| `fkftsh` | 3,139 | 3,272 | 95.9% |
| `vappytoy` | 1,447 | 1,448 | 99.9% |

Several accounts show **99.7–100% overlap** with Louis's targets (where they intersect),
confirming identical blocklist source.

### Social Graph: No Follow Connections

**The 6 core ring members do NOT follow each other** — zero follow edges among them.

Across all 16 accounts (6 core + 10 extended), only **5 follow edges** exist:

| From | To | Type |
|------|----|------|
| `fuenfuhrteefix` | `adametokirkfor` | one-way |
| `fuenfuhrteefix` | `fkftsh` | → |
| `fkftsh` | `fuenfuhrteefix` | ← (mutual) |
| `fkftsh` | `adametokirkfor` | → |
| `adametokirkfor` | `fkftsh` | ← (mutual) |

This means the blocklist is distributed **off-platform** — the participants share the tool or
blocklist via an external channel (Discord, Telegram, or a shared web tool), not through
Bluesky's social features.

## Statistical Proof of Coordination

Five independent statistical tests confirm that these accounts operate from a shared blocklist
rather than arriving at the same targets independently.

### Test 1: Block-Order Correlation (Spearman Rank)

If two accounts independently decide whom to block, the order in which they block shared victims
is random (ρ ≈ 0). If they import the same list file, they block in the same sequence (ρ ≈ 1.0).

| Pair | Shared victims | Spearman ρ | p-value | Interpretation |
|------|---------------|-----------|---------|----------------|
| Louis vs smatsto | 7,341 | 0.058 | 8.4×10⁻⁷ | Weak — shared targets, different import order |
| Extended member A vs B | 95,806 | **0.9996** | 0 | **Identical list file imported in same row order** |

The ρ = 0.9996 between two extended ring members is the **smoking gun**: these accounts literally
imported the same file with victims in the same sequence. The 95,806 shared blocks appear in
virtually identical order — this cannot occur by independent decision-making.

The low correlation between Louis and smatsto (ρ = 0.058) shows Louis imports the list in a
**different batch order** (reshuffled or subset extraction), but the targets themselves are shared.

![Block-order rank correlation scatter plots](assets/block_order_correlation.png)

### Test 2: Temporal Lag (smatsto → Louis)

For the 7,341 victims blocked by both smatsto and Louis:

| Metric | Value |
|--------|-------|
| smatsto blocks first | **78.1%** of shared targets |
| Louis blocks first | 21.9% |
| Median lag | **254 hours** (~10.6 days) |
| IQR | 83–454 hours (3.5–19 days) |

Lag distribution:

| Bucket | Count |
|--------|-------|
| smatsto first by >14 days | 3,033 |
| smatsto first by 7–14 days | 1,818 |
| smatsto first by 3–7 days | 664 |
| smatsto first by 1–3 days | 103 |
| Same hour | 1 |
| Louis first by <1 day | 134 |
| Louis first by 1–7 days | 858 |
| Louis first by >7 days | 613 |

**Interpretation:** smatsto discovers targets first in 78% of cases, with a characteristic
~10-day delay before Louis imports. This is the signature of a pipeline: smatsto crawls
and generates the list, then distributes it to consumers who import days later.

![Temporal lag histogram — smatsto blocks first](assets/temporal_lag_histogram.png)

### Test 3: Multi-Account Session Clustering

Days where 3+ ring members each ran >100 automated blocks:

| Period | Days with 3+ active | Peak day | Max simultaneous members |
|--------|---------------------|----------|--------------------------|
| May 2–30 | **28 out of 29 days** | May 10 | 8 members, 232,272 blocks |
| Average | — | — | 5 members/day, 61K blocks/day |

On 28 of 29 days, at least 3 ring members ran automated blocking sessions. Peak coordination
saw **8 accounts blocking 232K targets in a single day**. Independent actors do not exhibit
this degree of temporal clustering over a sustained period.

![Ring activity heatmap — 28/29 days coordinated](assets/coordination_heatmap.png)

### Test 4: Statistical Impossibility of Chance Overlap

| Parameter | Value |
|-----------|-------|
| Universe (unique blocked accounts, Apr 28–May 30) | 1,946,818 |
| Blocks by Account A | ~96,000 |
| Blocks by Account B | ~96,000 |
| Expected overlap by random chance | **4,734** |
| Observed overlap | **96,000** |
| Ratio (observed / expected) | **20×** |
| p-value (hypergeometric test) | ≈ 0 |

Two accounts each blocking 96K out of ~2M possible targets would share only ~4,700 by random
chance. The observed overlap of 96,000 is **20 times the random expectation** — a probability
so small it is computationally indistinguishable from zero.

![Chance vs observed overlap — 20× random expectation](assets/chance_vs_observed.png)

### Test 5: First-Blocker Analysis

Among all shared targets across 4 ring members (Louis, smatsto, and 2 extended):

| Account | Times first-blocker | Role |
|---------|-------------------|------|
| smatsto | **261,428** (61%) | Primary discovery engine |
| Extended member B | 96,211 (22%) | Secondary importer |
| Louis | 38,751 (9%) | Downstream consumer |
| Extended member A | 32,414 (8%) | Downstream consumer |

smatsto is the first account to block a given target in **61% of all cases**, confirming its
role as the central crawling engine. Other members consume its output with characteristic delays.

![First-blocker analysis — smatsto as discovery engine](assets/first_blocker.png)

### Coordination Conclusion

The five tests collectively establish:

1. **Shared list file** — ρ = 0.9996 block-order correlation proves identical file import
2. **Central engine** — smatsto blocks first in 78% of cases, with 10-day median lag to consumers
3. **Sustained coordination** — 28/29 days with 3+ members simultaneously active
4. **Statistical impossibility** — 20× random expectation rules out coincidence (p ≈ 0)
5. **Distribution hierarchy** — smatsto → extended members → core members (Louis)

These accounts are not independently arriving at the same conclusions. They are consuming
the same machine-generated blocklist from a shared source, imported via API automation.

## Ruling Out Bluesky's Native Moderation List Feature

A natural alternative hypothesis is that the ring members simply subscribe to a shared Bluesky
moderation list (`app.bsky.graph.list` with purpose `app.bsky.graph.defs#modlist`). This
explanation is ruled out by multiple independent observations:

### 1. No list records in the AT Protocol firehose

Bluesky's native moderation lists work via `app.bsky.graph.listblock` — a user subscribes to a
list, and blocks are applied *through the subscription*. This mechanism does **not** generate
individual `app.bsky.graph.block` records on the firehose. The data shows hundreds of thousands
of individual block records per account — these can only be created by explicit
`com.atproto.repo.createRecord` API calls for each target.

### 2. Zero associated lists in profile data

The Bluesky API profile data shows `associated.lists = 0` for all ring members. They do not
create moderation lists, and they do not subscribe to any.

### 3. Timing incompatible with list subscriptions

A list subscription applies all existing blocks **instantly** at subscription time. New entries
added by the list maintainer are applied as they are added. This would produce:
- Simultaneous application across all subscribers (not 10-day lag)
- No 70–100 ms sequential inter-block gaps (the API rate-limiting signature)
- No batch-import bursts followed by multi-minute pauses

All three patterns are present in the data and are inconsistent with list subscriptions.

### 4. Block-order correlation excludes list mechanism

List subscriptions do not preserve or expose insertion order to subscribers. The ρ = 0.9996
Spearman rank correlation between extended ring members proves they are reading the **same
ordered file sequentially** — a list subscription cannot produce row-order preservation.

### 5. Summary: Off-platform list ≠ native list

The ring does consume a shared target list — but it is distributed **off-platform** (via
external channel) and imported via **direct API automation**, deliberately bypassing Bluesky's
native moderation list feature. This distinction matters:

| | Bluesky Native Moderation List | What This Ring Does |
|---|---|---|
| Transparency | List creator visible, list publicly browsable | No attribution, undetectable |
| Accountability | Bluesky can moderate abusive lists | Platform cannot intervene |
| Mechanism | Single `listblock` subscription record | 600K+ individual `block` records per member |
| Detection | Identifiable via list metadata | Requires firehose timing analysis |
| Targets | Curated, typically hundreds to low thousands | 600K+ via automated crawling |

The ring specifically avoids the native list feature to evade transparency and platform
oversight while operating at a scale (3% of all users) that no native moderation list achieves.

## Assessment

| Question | Answer |
|----------|--------|
| Is this automated? | **Yes** — physically impossible manually (72–197ms median gap) |
| Is this coordinated? | **Yes** — 16+ accounts, shared blocklist, off-platform distribution |
| Is this a shared blocklist? | **Yes** — top 4 extended accounts show 96K+ identical blocks with smatsto |
| What is being targeted? | **Primarily English-speaking US progressives** (95% English); minor German component |
| How are targets found? | Crawling engagement on viral progressive posts, filtering for high-activity accounts |
| What is the scale? | **~3% of all Bluesky users** blocked by the combined ring |
| Is there a central engine? | **Yes** — smatsto (495K blocks, 22 followers) is the primary crawler |
| Is there a tool involved? | **Yes** — custom API automation with batch processing |
| Do ring members follow each other? | **No** — zero follow connections among 6 core members |
| Distribution channel? | **Off-platform** — only 5 follow edges across 16 accounts |
| Violates Bluesky TOS? | Blocking is allowed; mass-automated blocking is ambiguous |
| Is this harmful? | Blocking 3% of the platform degrades network utility for victims |

## Account Content Analysis

The account is a **real, active human user** — not a bot. Posts are 97% German, averaging 40–58
posts/week (mix of originals and replies). Content is casual personal posting:

### Posting Stats

| Metric | Value |
|--------|-------|
| Language | 97.9% German, 2.1% English |
| Weekly volume | 40–58 posts |
| Replies vs originals | ~40% replies, 60% originals |
| Content types | 54% text-only, 21% external links, 12% images, 10% quote-posts |

### Content Themes

The account posts about:
- **Pop culture & music** — Krautrock, Hamburg School, Udo Lindenberg, Iggy Pop, Silver Jews, metal
- **Daily life** — cooking Bolognese, library visits, job interviews, stomach aches from heat
- **German politics (mild)** — FDP/Kubicki criticism, anti-AfD sentiment, Bundeswehr/Zivi nostalgia
- **Literature & film** — Flann O'Brien, Almodóvar DVDs, ARD Mediathek documentaries
- **Humor** — Star Wars sausage, "AuraChirurgie" ads, skateboarding in your 40s

### Sample Recent Posts

> "Falls wer irgendwelche Promille & Kubicki Witze machen mag, das blocke ich alle weg, just saying."

> "Öffentliche Bibliotheken sind das KaDeWe des armen Mannes"

> "Die FDP gibt genug Anlass zur Kritik, da muss man für ein paar Klicks nicht die mögliche Suchterkrankung einer Person bekalauern, imho"

> "Schaue noch mal die BBC Krautrock Doku & auf dem Herd blubbert lecker Bolognese"

### Assessment of Content vs Blocking Behavior

The account is clearly a **real person** (cultural references, personal anecdotes, genuine conversations).
The post about "blocke ich alle weg" confirms awareness of and intent behind the blocking behavior.

This is **not a bot account** — it's a human user operating API automation tools to conduct
mass-blocking while maintaining normal social media presence.

## Follow-Up

- [ ] Monitor whether the blocklist continues growing
- [ ] Determine if a public blocklist document/list is being shared
- [ ] Check if any of the ring members are known political actors
- [ ] Report to Bluesky Trust & Safety if automation constitutes platform abuse
- [ ] Cross-reference with the `haruhwa` investigation (similar German political blocking patterns)
