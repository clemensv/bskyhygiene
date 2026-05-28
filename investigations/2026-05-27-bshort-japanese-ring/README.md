# Japanese Adult Spam Ring: b-short.link/C85gz9

**Investigation Date:** 2026-05-28  
**Methodology:** KQL analysis of Bluesky Firehose data (profiles, follows, posts)  
**Scope:** 604 bot accounts sharing a single spam link in profile bios  
**Relation to other investigations:** Independent — zero account or follow-target overlap with louisvillebsky/haruhwa or burst-follow spam clusters

---

## Executive Summary

A coordinated **mutual-follow ring** of 604 bot accounts was deployed on Bluesky in a
single burst on **2026-05-27 13:00 UTC**. All accounts use Japanese female persona names,
share the same adult content redirect link (`b-short.link/C85gz9`), and operate as a
self-reinforcing engagement farm — each bot follows ~50 other bots in the ring to inflate
follower counts, then posts Japanese-language bait content with hashtags to attract
legitimate users.

---

## Key Indicators

| Signal | Value |
|--------|-------|
| Total accounts | 604 |
| Creation window | Single hour — 2026-05-27 13:00 UTC |
| Infrastructure | Official Bluesky PDS (bsky.network) |
| Mutual follows (internal) | 28,439 |
| Bots participating in ring | 591 (98%) |
| Median follows per bot | 50 |
| External follow targets | ~130 (720 total − 591 internal) |
| Total posts | 3,140 (~5.2 per account) |
| Language | Japanese (`ja`) |
| Spam domain | `b-short.link/C85gz9` |
| Overlap with louisvillebsky | **Zero** (accounts and targets) |
| Overlap with burst-follow | **Zero** |

---

## Creation Timeline

![Creation Timeline](assets/creation_timeline.png)

All 604 accounts appeared in the Bluesky firehose within a single hour — an unmistakable
bulk-creation event.

---

## Profile Template

All 604 accounts use Japanese female first names with emoji, and a two-line bio:

```
{cute phrase in Japanese}
{link phrase}→ https://b-short.link/C85gz9
```

### Sample Profiles

| Display Name | Bio Line 1 | Bio Line 2 |
|-------------|-------------|-------------|
| みゆき💤 | すき💗 | 一人で見てね→ (watch alone →) |
| ほのか🌃 | なにしてる？🤔 | えちちはこれ→ (lewd stuff here →) |
| なつき🌹 | はなびがすき🎆 | えちち→ |
| せな🍋 | なかよくして | えちち→ |
| あおい🍵 | よるのでんわすき | えちち→ (likes late-night calls) |
| さゆり🎶 | なでなでされたい | やばいの載せてる→ (posted something wild →) |
| はなこ🍎 | DMどうぞ | 一人で見てね→ |
| えま🌴 | つうわあいてぼしゅう | えちちはこれ→ (looking for call partner) |
| りりか🔮 | おかいものすき | やばいの載せてる→ |
| みずき🍑 | たのしいことしたい | やばいの載せてる→ |

### Link Phrase Variants

| Japanese | Translation | Frequency |
|----------|-------------|-----------|
| えちち→ | Lewd stuff → | High |
| えちちはこれ→ | Lewd stuff is here → | High |
| やばいの載せてる→ | Posted something wild → | High |
| 一人で見てね→ | Watch alone → | Medium |
| 配信→ | Streaming → | Low |

All point to the same shortened URL: `https://b-short.link/C85gz9`

---

## Mutual-Follow Ring Structure

![Network Graph](assets/network_graph.png)

This is a **pure engagement ring** — the bots primarily follow each other:

![Follow Distribution](assets/follow_distribution.png)

| Metric | Value |
|--------|-------|
| Internal follows (bot → bot) | 28,439 |
| Bots with internal follows | 591 (98%) |
| Avg internal follows per bot | ~48 |
| Total follows (all targets) | 29,590 |
| External follows | ~1,151 (4%) |
| Top followed bot | 67 followers from ring |

The most-followed accounts in the network are **themselves b-short bots** (confirmed:
さゆり🎶, あおい🍵, ゆずき🌃, れい✨ — all have the same spam link). This means
96% of all follow activity is internal ring-boosting.

The result: each bot appears to have 50–67 followers, making them look like small
but real accounts to casual observers.

---

## Post Content

![Post Activity](assets/post_activity.png)

All 604 accounts post — averaging **5.2 posts each** (3,140 total). Posts are in
Japanese and use Twitter/X-style engagement bait:

### Post Templates

| Japanese | English Translation |
|----------|-------------------|
| このツイートいいねくれた人だけに内緒のやつ送る😳 | "I'll secretly send something to everyone who likes this tweet 😳" |
| ひますぎて配りたい欲がやばい。いいねと「見たい」で秒！ | "So bored I want to give stuff away. Like + say 'want to see' for instant!" |
| いいねくれたら今日中にすごいの送るよ | "Like this and I'll send something amazing today" |
| さみしいからきてほしい | "I'm lonely, come to me" |
| 突然ですが、今から24時間限定で私の㊙️公開します！！！ | "Suddenly! For 24 hours only, I'm publishing my secret!!!" |
| 一緒にいてくれる人いない？ | "Anyone want to be with me?" |
| リプ「ほしい」で即配り | "Reply 'want' for instant delivery" |
| あそべるひとぼしゅうちゅうー | "Looking for someone to play with~" |

### Hashtags Used

| Hashtag | Translation |
|---------|-------------|
| `#通話相手募集中` | Looking for call partner |
| `#裏アカ女子` | Secret account girl |
| `#いいねでDM` | Like for DM |
| `#彼氏募集中` | Looking for boyfriend |
| `#裏アカ男子と繋がりたい` | Want to connect with secret account boys |
| `#通話相手募集` | Call partner wanted |

---

## Behavioral Pattern

The operation follows a specific playbook:

1. **Bulk creation** — 604 accounts in a single hour (automated)
2. **Profile setup** — Japanese name + emoji + b-short.link in bio
3. **Mutual follow** — each bot follows ~50 others in the ring (inflates follower count)
4. **Content posting** — 5+ Japanese engagement-bait posts per account
5. **Waiting** — the inflated follower counts + posts make accounts appear legitimate
6. **Monetization** — users clicking `b-short.link/C85gz9` are redirected to adult content sites

This is a **traffic farming** operation: the bots exist to generate clicks on the
shortened link, likely earning the operator revenue via affiliate/redirect payments.

---

## Connection to louisvillebsky Investigation

The louisvillebsky/haruhwa report previously included a "Japanese Female Persona Ring"
sub-cluster of 35 accounts with `mightybeam`/`happybeam` handles. That sub-cluster
used compound-English handles (not Japanese names) and was hosted on the louisvillebsky
PDS.

This b-short.link ring is **17× larger** (604 vs 35 accounts), uses authentic Japanese
display names, runs on official Bluesky PDS, and has **zero overlap** with the
louisvillebsky accounts or targets. They likely represent:

- **Different operator** running the same playbook (Japanese adult spam ring)
- Or a **shared template/tool** used by multiple operators

The louisvillebsky "Japanese ring" sub-cluster may have been an earlier/smaller test
by the same tool author, or an independent copycat.

---

## Detection Heuristic

```
IF description contains "b-short.link"
   AND display_name matches Japanese characters
   AND language = "ja"
   AND follows_internal_ring / total_follows > 0.8
THEN confidence = 0.99 (spam ring bot)
```

Broader detection for this pattern:
```
IF account_age < 48 hours
   AND followers > 40
   AND all followers share same link in bio
   AND posts contain #裏アカ女子 OR #通話相手募集
THEN confidence = 0.95 (mutual-follow ring)
```

---

## Sample DIDs

```
did:plc:oj4gt3uyvafrmam2cyarzc4j  (みゆき💤)
did:plc:fhtvxkam2nqxvfkqhjcjv3k7  (ひろ)
did:plc:wzjsctixei7wkhzhj53vvwhy  (ほのか🌃)
did:plc:txhfk67tenwadzkavnnoj7ti  (せいら)
did:plc:tlw2g6ig37j7twepalu6bl5t  (なつき🌹)
did:plc:r54ioqkmqs5fvmeol3k2znrj  (あすみ)
did:plc:hbk57kzzq77aw2g2jkh2cwto  (いつき)
did:plc:7uviw6f7s4xpuljuwps6vnmm  (えま🌴)
did:plc:lymvm745xgebzda4moh7eruo  (さゆり🎶 — top followed in ring, 67 followers)
did:plc:anv3x234iz46uclt7awkfbtg  (あおい🍵 — top followed in ring, 67 followers)
```

---

*Investigation conducted via KQL queries against Bluesky Firehose data (Microsoft Fabric Eventhouse).*
