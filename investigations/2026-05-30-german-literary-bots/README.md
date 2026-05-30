# Deutschsprachiges Literatur-Bot-Netzwerk auf Bluesky

**Datum:** 30. Mai 2026  
**Status:** AKTIV — heute noch neue Bots erstellt  
**Umfang:** **56 bestätigte Bot-Accounts**, ~616 Fake-Follows an 11 Kern-Ziele  
**Infrastruktur:** Offizielle Bluesky-PDS (bsky.network)  
**Hinweisgeber:** [@schreibersnaturarium.de](https://bsky.app/profile/schreibersnaturarium.de) (Autorin Jasmin Schreiber)  
**Verwandt mit anderen Clustern:** Nein — eigenständige Operation, kein Overlap mit Seasoning Rings, Burst-Follow-Spam oder cislost24-Netzwerk

---

## Zusammenfassung

Ein subtiles Bot-Netzwerk wurde identifiziert, das gezielt deutschsprachige Kultur- und
Literatur-Accounts auf Bluesky mit Fake-Followern versorgt. Im Gegensatz zu den bekannten
Burst-Follow-Netzwerken (die 1.000+ Follows in Minuten abfeuern) arbeitet dieses Cluster
mit einer **Tropf-Taktik**: Jeder Bot folgt nur **9–14 Accounts** (sehr häufig exakt 11)
und liefert seine Follows über Stunden oder Tage verteilt ab.

Die Autorin Jasmin Schreiber (@schreibersnaturarium.de) bemerkte das Muster am 30. Mai 2026:

> „Hab gerade so so viele von diesen Accounts hier geblockt... die sind recht unauffällig,
> weil da vielleicht 2–3 am Tag reinfolgen, sehr unter dem Radar. Summiert sich aber auch.
> Interessant: Die folgen nicht untereinander, allerdings immer so zwischen 9 und 14 Accounts,
> extrem oft exakt 11."

## Kern-Indikatoren

| Signal | Wert |
|--------|------|
| Bestätigte Bot-Accounts | **56** |
| Follows pro Bot | 9–14 (Modus: **exakt 11**) |
| Geschätzte Fake-Follows | ~616 |
| Kampagnenstart | **30. April 2026** (erstes Konto erstellt) |
| Erstellungs-Kadenz | 2–7 neue Bots pro Tag |
| Posts pro Bot | **0** |
| Follow-Kadenz | 2–3 Follows/Tag (Tropf-Taktik) |
| Bots folgen einander | **Nein** |
| Kern-Ziele | 11 deutschsprachige Kultur-Accounts |
| Spam-Accounts im Mix | 5 „Goth Girl"-Lockvogel-Profile |

## Ziel-Accounts (Co-Follow-Analyse)

Die Bots folgen fast ausschließlich denselben ~11 Accounts. Alle Kern-Ziele sind
deutschsprachige Autor:innen, Kulturinstitutionen oder Journalist:innen:

![Co-Follow-Ziele des Bot-Clusters](assets/cofollow_targets.png)

| Rang | Account | Bots | Follower | Beschreibung |
|------|---------|------|----------|--------------|
| 1 | @colettemschmidt.bsky.social | 55/56 | 11.619 | Journalistin |
| 2 | @schreibersnaturarium.de | 54/56 | 20.514 | Autorin (Hinweisgeberin) |
| 3 | @bsky.app | 51/56 | 33.484.332 | Bluesky-Standard-Follow |
| 4 | @wernerkogler.bsky.social | 47/56 | 9.318 | Österreichischer Politiker |
| 5 | @datgestruepp.bsky.social | 47/56 | 6.065 | Kultur-Account |
| 6 | @jungeakademie.bsky.social | 46/56 | 2.774 | Junge Akademie |
| 7 | @purrtah.bsky.social | 45/56 | 4.903 | Kultur/Illustration |
| 8 | @musermeku.bsky.social | 40/56 | 3.203 | Museumskultur |
| 9 | @kunstderfuge.bsky.social | 37/56 | 3.537 | Kunst/Kultur |
| 10 | @kunstjonas.bsky.social | 37/56 | 2.394 | Kunst |
| 11 | @elsschot.bsky.social | 35/56 | 9.861 | Literatur |

Zusätzlich finden sich 5 Spam-/Lockvogel-Accounts mit je 6–7 Bot-Followern:

| Account | Bots | Follower | Typ |
|---------|------|----------|-----|
| @gothgirlrumi.bsky.social | 7 | 12 | Instagram-/Telegram-Spam |
| @redheadfurry.bsky.social | 7 | 14 | Instagram-/Telegram-Spam |
| @gothgirlrileyy.bsky.social | 6 | 12 | Instagram-/Telegram-Spam |
| @gothgirlvanesssa.bsky.social | 6 | 14 | Instagram-/Telegram-Spam |
| @rileygothvampire.bsky.social | 6 | 13 | Instagram-/Telegram-Spam |

Diese „Goth Girl"-Accounts sind vermutlich des Operators eigene Spam-Promotion-Ziele —
die echten Literatur-Accounts sind Camouflage-Ziele oder unfreiwillige Opfer.

## Follow-Verteilung

Die extrem enge Verteilung um genau 11 Follows ist ein starker Bot-Indikator:

![Verteilung der Follows pro Bot-Account](assets/follow_distribution.png)

| Follows | Accounts |
|---------|----------|
| 8 | 1 |
| 9 | 3 |
| 10 | 3 |
| **11** | **29** (52%) |
| 12 | 7 |
| 13 | 6 |
| 14 | 2 |
| 15 | 3 |
| 16 | 2 |

**52% der Bots folgen exakt 11 Accounts** — ein eindeutiges Fingerprint-Muster.

## Bot-Erstellungs-Timeline

Die Accounts werden in gleichmäßigem Tempo erstellt — nicht als Burst, sondern als
kontinuierlicher Aufbau von 2–7 Accounts pro Tag seit Ende April 2026:

![Bot-Erstellungs-Timeline](assets/creation_timeline.png)

Auffällig: Ein einzelner Account wurde bereits am **14. Februar 2026** erstellt — möglicherweise
ein Testlauf des Operators, bevor die Kampagne Ende April systematisch startete.

## Tropf-Taktik: Follow-Kadenz

Im Gegensatz zu den bekannten Burst-Bots (1.024 Follows in 3 Minuten) nutzt dieses
Netzwerk eine bewusste Verlangsamung, um unter dem Radar zu bleiben:

![Follow-Kadenz](assets/follow_cadence.png)

Die meisten Bots feuern ihre 11 Follows in kurzen Blöcken ab (Median < 5 Stunden),
aber verteilt über Tage — was bedeutet, dass ein Ziel-Account nur 2–3 neue Bot-Follower
pro Tag erhält. Genau das beobachtete @schreibersnaturarium.de.

## Tägliche Aktivität

Die Gesamtaktivität des Clusters zeigt Wellen, mit einem Peak um den 17. Mai 2026:

![Tägliche Follow-Aktivität](assets/daily_activity.png)

## Bot-Profil-Muster

Die Bot-Accounts teilen folgende Merkmale:

- **0 Posts** (ausnahmslos)
- **0–1 Follower** (nur wenn ein anderer Bot zufällig dasselbe Ziel hat)
- **Kein Avatar, kein Banner**
- **Kein Display-Name** (meistens) oder generischer deutscher/internationaler Name
- **Deutsche Handle-Muster:** z.B. `miahungrigesherz.bsky.social`, `fraurollmops.bsky.social`
- **Manche mit kopierten Bio-Texten:** „Neu hier! Fußgängerin, Serienkuckerin, Hausarbeitsvermeidererin"

Einige wenige Accounts (erstellt am 17. Mai) tragen stattdessen englische „Goth Girl"-Profile
mit Instagram-/Telegram-Verlinkungen — das sind die eigentlichen Spam-Nutzlasten.

## Hypothese: Geschäftsmodell

```
┌─────────────────────────────────────────────────────┐
│  OPERATOR erstellt 2-7 Bot-Accounts pro Tag         │
│  ↓                                                  │
│  Jeder Bot folgt ~11 Accounts:                      │
│    • 5-6 echte deutsche Kultur-Accounts (Tarnung)   │
│    • 4-5 Spam-/Kunden-Accounts (Monetarisierung)    │
│  ↓                                                  │
│  Langsame Auslieferung (2-3 Follows/Tag pro Ziel)   │
│  → Unter dem Radar der Moderation                   │
└─────────────────────────────────────────────────────┘
```

Die echten Kultur-Accounts dienen als **Tarnung**: Ein Account der @schreibersnaturarium.de,
@wernerkogler und @elsschot folgt, sieht auf den ersten Blick aus wie ein deutschsprachiger
Neuankömmling. Die eigentlichen Kunden sind die „Goth Girl"-Spam-Profile.

## Abgrenzung zu anderen Netzwerken

| Merkmal | Dieses Cluster | Seasoning Rings | Burst-Follow-Spam |
|---------|----------------|-----------------|-------------------|
| Follows/Bot | 9–14 | 62–182 | ~1.024 |
| Kadenz | Tropf (Stunden/Tage) | Rapid (Sekunden) | Burst (3–5 Min) |
| Posts | 0 | 0 | 0 (dann Spam) |
| Bots folgen einander | Nein | **Ja** (Ring-Muster) | Nein |
| Ziel-Sprache | Deutsch | Japanisch | Englisch |
| Handle-Muster | Deutsch/generisch | Japanisch | Ornate weibliche Namen |
| Tages-Kapazität | 2–7 neue Bots | 50–100 neue Bots | 10–106 Bots/Tag |

## Erkennungsmethodik

Dieses Cluster ist besonders schwer zu erkennen, weil:

1. **Geringe Follow-Zahl:** 11 Follows ist im Normalbereich eines neuen Nutzers
2. **Keine Inter-Follows:** Keine Ring-Struktur sichtbar
3. **Tropf-Lieferung:** Kein plötzlicher Follower-Spike beim Ziel
4. **Plausible Handles:** Deutsche Handles fügen sich in die Zielgruppe ein

**Erkennung gelang durch:**
- Co-Follow-Analyse: 55/56 Bots folgen @colettemschmidt → statistisch unmöglich zufällig
- Fixed follow count: 52% folgen exakt 11 Accounts
- Null-Post-Kriterium in Kombination mit niedrigem Following-Count
- Community-Hinweis (Jasmin Schreiber)

## Nächste Schritte

- [ ] Bot-DIDs zur Moderations-Blockliste hinzufügen
- [ ] Breitere Suche: Cluster-Erweiterung über weitere Co-Follow-Ziele
- [ ] Monitoring: Tägliche Erkennung neuer Accounts mit diesem Fingerprint
- [ ] Meldung an Bluesky Trust & Safety

---

*Analyse erstellt am 30. Mai 2026 auf Basis von Bluesky-Firehose-Daten (Kusto/Fabric)
und öffentlicher Bluesky-API-Abfragen.*
