# Burst-Follow Spam Network (watchmelive.my.id / livechats.my.id)

**Date:** 2026-05-28  
**Status:** Active (ongoing waves)  
**Scope:** 389 bot accounts, ~394,000 fake follows generated in 5 days  
**Infrastructure:** Official Bluesky PDS (bsky.network), not self-hosted  
**Relation to louisvillebsky/haruhwa:** None — independent operation, zero follow-target overlap

---

## Executive Summary

A large-scale follow-spam and adult content promotion operation was detected on Bluesky,
creating **389 accounts** between May 23–28, 2026. Each account issues exactly **~1,001 follows**
within a 3–5 minute window (200–640 follows/minute), then updates its profile with adult
spam links. Unlike the louisvillebsky/haruhwa cluster, these bots use standard Bluesky PDS
infrastructure rather than self-hosted servers.

## Key Indicators

| Signal | Value |
|--------|-------|
| Total accounts | 389 |
| Avg follows per account | 1,013 |
| Follow burst duration | < 5 minutes per account |
| Peak follow rate | 640 follows/minute |
| Account creation pattern | Waves of 24–126 per hour |
| Active period | May 23–28, 2026 (ongoing) |
| PDS infrastructure | Official bsky.network shards |
| Shared target | `bsky.app` (followed by 387/389 bots) |
| Spam domains | `watchmelive.my.id`, `livechats.my.id` |

## Handle Naming Pattern

All accounts use a consistent **female first name + 2-4 random alphanumeric suffix** pattern:

```
mirellaytwd.bsky.social       lysandras2tu.bsky.social
antoinetta8pkf.bsky.social    marchelinetca1.bsky.social
catherine2hcj.bsky.social     dominikapqv4.bsky.social
yohannajbhk.bsky.social       angelettat0mg.bsky.social
aurelia2nl1.bsky.social        olivianasqku.bsky.social
marcellinael6e.bsky.social    petronela43s7.bsky.social
celiniace6q.bsky.social        clarissajfuo.bsky.social
andromeda4v6m.bsky.social     desideria9qn7.bsky.social
valerina17ql.bsky.social       calistangp4.bsky.social
emilia9quk.bsky.social         franciskav0j6.bsky.social
```

The names skew toward uncommon/ornate female names (Lysandra, Marchelina, Petronela,
Desideria, Calista, Andromeda) suggesting generation from a curated wordlist rather than
common name databases.

## Profile Template

All bots that have updated their profile use an identical template:

```
"Do you want to meet me?" ✨ ADULT EXCLUSIVE CONTENT HERE 👉 https://{domain}/{unique_id}
```

Two domains are rotated:
- `watchmelive.my.id` — Indonesian TLD (.my.id)
- `livechats.my.id` — same registrar/TLD

Each link has a unique tracking suffix (e.g., `/37sqzk9e4`, `/ofzx9dytu`, `/v5h19e5ip`),
suggesting per-account attribution for the spam campaign.

## Temporal Pattern — Account Creation Waves

```
May 23, 13:00 UTC  ████████░░░░░░░░░░░░  27 accounts
May 23, 14:00 UTC  ████████████████░░░░  60 accounts
May 23, 15:00 UTC  ████████░░░░░░░░░░░░  27 accounts
May 24, 01:00 UTC  ████████░░░░░░░░░░░░  27 accounts
May 24, 02:00 UTC  ████████████████████  78 accounts
May 24, 07:00 UTC  █████████░░░░░░░░░░░  30 accounts
May 25, 02:00 UTC  ██████████████████████████████████  126 accounts ← peak
May 25, 13:00 UTC  ███████░░░░░░░░░░░░░  24 accounts
May 25, 14:00 UTC  ███████░░░░░░░░░░░░░  24 accounts
May 26, 05:00 UTC  ██████████░░░░░░░░░░  36 accounts
May 26, 06:00 UTC  █████████████░░░░░░░  48 accounts
May 26, 12:00 UTC  ████████████████████  72 accounts
May 26, 15:00 UTC  ████████████████████████████░░  108 accounts
May 27, 12:00 UTC  ██████████████░░░░░░  54 accounts
May 27, 13:00 UTC  ██████████░░░░░░░░░░  37 accounts
May 27, 22:00 UTC  █████████████░░░░░░░  48 accounts
May 28, 01:00 UTC  ██████████████████████░░  84 accounts
May 28, 03:00 UTC  █████████░░░░░░░░░░░  30 accounts
May 28, 04:00 UTC  ████████████░░░░░░░░  45 accounts
May 28, 05:00 UTC  ███████████░░░░░░░░░  42 accounts
```

Creation happens in distinct waves with gaps of 4–12 hours between them, suggesting
either manual operator triggers or rate-limit avoidance.

## Behavioral Signature

1. **Account creation** — new DID registered on official Bluesky PDS
2. **Handle assignment** — `femalename+random.bsky.social`
3. **Follow burst** — exactly ~1,001 follows issued in 3–5 minutes
4. **Profile update** — adult spam link added to description
5. **Dormancy** — no further activity observed

The 1,001 follow count is almost certainly a hardcoded constant in the automation script
(likely `range(1001)` or similar). The slight variations (1,001–1,666) may indicate
different script configurations or batching logic.

## Infrastructure Details

Unlike the louisvillebsky/haruhwa operation which runs self-hosted PDS servers, this
operation uses Bluesky's own infrastructure:

| Bot DID | PDS Shard |
|---------|-----------|
| did:plc:ia3pm4p6dd2bfcgwlsowlr7y | blusher.us-east.host.bsky.network |
| did:plc:dzg3ixjasiezk32bnsrqfjny | jellybaby.us-east.host.bsky.network |
| did:plc:yvnekwdgasyxcvp5crubyz4g | (official bsky shard) |
| did:plc:okpke3lawx4435zdhvghhobs | (official bsky shard) |

This means the operator does not need any server infrastructure — they only need
the ability to register accounts at scale on bsky.social.

## Single Shared Follow Target

All 387 of the 389 burst-follow bots follow **`bsky.app`** (`did:plc:z72i7hdynmk6r22z27h6tvur`) —
the official Bluesky team account. This is likely:
- A canary/test follow executed before the bulk follow script runs
- A "seed" follow to make the account appear active
- An artifact of the account creation flow being automated

The remaining follows target random legitimate users (no overlap with louisvillebsky targets).

## Comparison with louisvillebsky/haruhwa Operation

| Attribute | louisvillebsky/haruhwa | Burst-follow spam |
|-----------|----------------------|-------------------|
| Scale | 3,584 accounts | 389 accounts |
| PDS | Self-hosted (3 servers) | Official bsky.network |
| Purpose | Follow inflation (progressive/media) | Adult content promotion |
| Follow targets | Curated political/media list | Random users + bsky.app |
| Handle pattern | firstname+number, random | femalename+random |
| Profile content | Motivational quotes | Adult spam links |
| Follow behavior | Gradual, multi-day | Burst 1,001 in 5 min |
| Overlap | — | Zero shared targets |
| Operator | Likely same (cross-PDS proof) | Independent |

## Conclusion

This is an **independent bot operation** with no technical linkage to the
louisvillebsky/haruhwa/tranquil.mosphere.at cluster. It represents a different
threat model:

- **louisvillebsky**: Sophisticated follow-inflation targeting specific communities,
  using self-hosted infrastructure to avoid detection
- **Burst-follow spam**: Blunt-force adult content promotion using disposable accounts
  on official infrastructure, trivially detectable by rate analysis

## Detection Heuristic

```
IF account_follows >= 1000
   AND follow_time_span < 600 seconds
   AND handle matches /^[a-z]+\d{1,4}[a-z]*\.bsky\.social$/
   AND profile_description contains "my.id" OR "watchmelive" OR "livechats"
THEN confidence = 0.99 (spam bot)
```

## Sample DIDs for Verification

```
did:plc:ia3pm4p6dd2bfcgwlsowlr7y  (dddpod.bsky.social)
did:plc:iuwjzd7oh5kviej3q2saqotn
did:plc:a2wzk4tfzu5lygirq2x2xweu
did:plc:dzg3ixjasiezk32bnsrqfjny  (antoinetta8pkf.bsky.social)
did:plc:udoghe27igarvn4dwb5aq4jg  (catherine2hcj.bsky.social)
did:plc:zsdpzmxccxfblwu3ynbqhipc
did:plc:okpke3lawx4435zdhvghhobs  (marchelinetca1.bsky.social)
did:plc:adyh5v6vcxrc63nnhnfl2ese  (aurelia2nl1.bsky.social)
did:plc:jsogvoz7ubdgn2fnnrsxnp5s  (mikaelasg3m.bsky.social)
did:plc:xhmcqmuiucas3eidh6jljrww  (olivianasqku.bsky.social)
```

---

*Investigation conducted via KQL queries against Bluesky Firehose data (Microsoft Fabric Eventhouse).*
