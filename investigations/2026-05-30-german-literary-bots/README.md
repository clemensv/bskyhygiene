# Deutschsprachiges Literatur-Bot-Netzwerk auf Bluesky

**Datum:** 30. Mai 2026 (aktualisiert: Runde 2)  
**Status:** RUHEND — keine neuen Bots in den letzten 48 Stunden  
**Umfang:** **72 bestätigte Bot-Accounts**, ~780 Fake-Follows an 11 Kern-Ziele  
**Infrastruktur:** Offizielle Bluesky-PDS (bsky.network)  
**Hinweisgeber:** [@schreibersnaturarium.de](https://bsky.app/profile/schreibersnaturarium.de) (Autorin Jasmin Schreiber)  
**Verwandt mit anderen Clustern:** Nein — eigenständige Operation, kein Overlap mit Seasoning Rings, Burst-Follow-Spam oder cislost24-Netzwerk  
**Suspendierungen:** 0 von 72 — alle Accounts weiterhin aktiv

---

## Zusammenfassung

Ein subtiles Bot-Netzwerk wurde identifiziert, das gezielt deutschsprachige Kultur- und
Literatur-Accounts auf Bluesky mit Fake-Followern versorgt. Im Gegensatz zu den bekannten
Burst-Follow-Netzwerken (die 1.000+ Follows in Minuten abfeuern) arbeitet dieses Cluster
mit einer **gestaffelten Aktivierung**: Jeder Bot folgt nur **3–20 Accounts** (Modus: exakt 11)
und feuert seine Follows in einem schnellen Burst ab (Median: 128 Sekunden). Der Effekt
der „2–3 neuen Follower pro Tag" entsteht, weil **jeden Tag neue Bots aktiviert werden** —
nicht weil einzelne Bots langsam agieren.

Die Autorin Jasmin Schreiber (@schreibersnaturarium.de) bemerkte das Muster am 30. Mai 2026:

> „Hab gerade so so viele von diesen Accounts hier geblockt... die sind recht unauffällig,
> weil da vielleicht 2–3 am Tag reinfolgen, sehr unter dem Radar. Summiert sich aber auch.
> Interessant: Die folgen nicht untereinander, allerdings immer so zwischen 9 und 14 Accounts,
> extrem oft exakt 11."

**Korrektur (Runde 2):** Die „2–3 pro Tag"-Wahrnehmung entsteht nicht durch langsame
Auslieferung pro Bot, sondern durch **tägliche Aktivierung neuer Bots**. Jeder einzelne Bot
feuert alle Follows in unter 2 Minuten ab (Median).

## Kern-Indikatoren

| Signal | Wert |
|--------|------|
| Bestätigte Bot-Accounts | **72** |
| Follows pro Bot | 3–20 (Modus: **exakt 11**, 40%) |
| Geschätzte Fake-Follows | ~780 |
| Kampagnenstart | **2. Mai 2026** (erster Follow im Graph) |
| Letzte Aktivität | **30. Mai 2026** |
| Posts pro Bot | **0–17** (19 Bots mit Posts, davon 2 mit >10) |
| Follow-Burst-Dauer (Median) | **128 Sekunden** |
| Bots folgen einander | **Nein** |
| Kern-Ziele | 11 Accounts (deutsch + international) |
| Spam-Accounts im Mix | 9 „Goth Girl"-Lockvogel-Profile |
| Avatare | **58/66** (88%) haben ein Profilbild |
| Suspendiert/Gelöscht | **0** |

## Ziel-Accounts (Co-Follow-Analyse)

Die Bots folgen fast ausschließlich denselben ~11 Accounts. Die Kern-Ziele sind
deutschsprachige Autor:innen, Kulturinstitutionen, Journalist:innen und Politiker:

![Co-Follow-Ziele des Bot-Clusters](assets/cofollow_targets.png)

| Rang | Account | Bots | Follower | Beschreibung |
|------|---------|------|----------|--------------|
| 1 | @schreibersnaturarium.de | 72/72 | 20.514 | Autorin (Hinweisgeberin) |
| 2 | @colettemschmidt.bsky.social | 72/72 | 11.619 | Journalistin |
| 3 | @bsky.app | 66/72 | 33.484.526 | Bluesky-Standard-Follow |
| 4 | @wernerkogler.bsky.social | 58/72 | 9.318 | Österreichischer Politiker |
| 5 | @datgestruepp.bsky.social | 52/72 | 6.065 | Kultur-Account |
| 6 | @jungeakademie.bsky.social | 52/72 | 2.774 | Junge Akademie |
| 7 | @purrtah.bsky.social | 51/72 | 4.902 | Kultur/Illustration |
| 8 | @musermeku.bsky.social | 45/72 | 3.203 | Museumskultur |
| 9 | @kunstderfuge.bsky.social | 42/72 | 3.537 | Kunst/Kultur |
| 10 | @kunstjonas.bsky.social | 42/72 | 2.394 | Kunst |
| 11 | @elsschot.bsky.social | 39/72 | 9.861 | Literatur |

**Sekundärziele (gelegentlich mitgenommen):** @kattascha (40.098 Follower),
@golod (24.151), @islieb (15.464), @faznet (19.497), @afelia/Marina Weisband (75.904),
@spdfraktion.de (14.741), @suhrkamp.de (8.370), @krajamine (8.491), @mareicares (4.737).

### Spam-/Lockvogel-Accounts

9 „Goth Girl"-Spam-Profile mit je 4–7 Bot-Followern — offenbar die
Monetarisierungs-Ziele des Operators (Instagram-/Telegram-Weiterleitung):

| Account | Bots | Follower | Beschreibung |
|---------|------|----------|--------------|
| @gothgirlvanesssa.bsky.social | 7 | 14 | „19 · Miami · The girl from your nightmares" |
| @redheadfurry.bsky.social | 7 | 14 | „Redhead 🧡 · 19 · Your favorite Fury" |
| @gothgirlrumi.bsky.social | 7 | 12 | „19 · IG + TG: @gothgirlrumi" |
| @rileygothvampire.bsky.social | 7 | 13 | „19 · From the darkness" |
| @gothgirlrileyy.bsky.social | 7 | 12 | „Hi 🖤 I am Riley · 19 · LA" |
| @itssophiierose.bsky.social | 5 | 11 | „It's Sophie Rose · 19 · Los Angeles" |
| @rileyraygoth.bsky.social | 4 | 9 | „Hi, I am Riley · 19 · New York" |
| @sophierosegoth.bsky.social | 4 | 11 | „🖤 Can you fix me? 🖤" |
| @itsvanessabeckerr.bsky.social | 4 | 9 | „19 · Looking for the one · Digital Creator" |

Alle „Goth Girl"-Accounts verweisen auf Instagram/Telegram — klassisches Social-Engineering.

## Follow-Verteilung

Die extrem enge Verteilung um 11 Follows ist ein starker Bot-Indikator, wobei Runde 2
eine breitere Streuung (3–20) zeigt als initial angenommen:

![Verteilung der Follows pro Bot-Account](assets/follow_distribution.png)

| Follows | Accounts |
|---------|----------|
| 3 | 6 |
| 5 | 1 |
| 6 | 3 |
| 7 | 1 |
| 8 | 1 |
| 9 | 2 |
| 10 | 3 |
| **11** | **29** (40%) |
| 12 | 7 |
| 13 | 5 |
| 14 | 2 |
| 15 | 3 |
| 16 | 1 |
| 17 | 1 |
| 18 | 5 |
| 19 | 1 |
| 20 | 1 |

**40% der Bots folgen exakt 11 Accounts** — ein eindeutiges Fingerprint-Muster.
Die niedrigeren Zahlen (3–6 Follows) sind vermutlich Bots, die noch nicht alle Ziele
abgearbeitet haben oder deren Follow-Operationen teilweise fehlschlugen.

## Bot-Erstellungs-Timeline

Die Accounts werden über den gesamten Mai 2026 aktiviert — erste Graph-Aktivität
am 2. Mai, letzte am 30. Mai:

![Bot-Erstellungs-Timeline](assets/creation_timeline.png)

## Follow-Timing: Burst pro Bot, gestaffelt pro Ziel

**Korrektur gegenüber Runde 1:** Jeder einzelne Bot feuert alle seine Follows in einem
schnellen Burst ab — nicht über Stunden oder Tage verteilt.

![Follow-Kadenz](assets/follow_cadence.png)

| Metrik | Wert |
|--------|------|
| Median Burst-Dauer | **128 Sekunden** |
| Abgeschlossen in < 1 Minute | 27/72 (38%) |
| Abgeschlossen in < 5 Minuten | 40/72 (56%) |
| Abgeschlossen in < 1 Stunde | 48/72 (67%) |
| Nahm > 1 Stunde | 24/72 (33%) |

Die Bots mit langer Gesamtdauer (Stunden/Tage) wurden für **mehrere Wellen** reaktiviert:
Erst folgten sie den initialen 11 Kern-Zielen, Tage später wurden die Goth-Girl-Spam-
Accounts hinzugefügt. Die Dauer misst first-to-last-follow, nicht kontinuierliche Aktivität.

**Warum Jasmin Schreiber „2–3 pro Tag" beobachtete:** Nicht weil einzelne Bots langsam
ausliefern, sondern weil jeden Tag 2–7 NEUE Bots aktiviert werden, die jeweils sofort
alle Follows abfeuern.

## Tägliche Aktivität

Die Gesamtaktivität des Clusters zeigt Wellen, mit einem Peak um den 17. Mai 2026:

![Tägliche Follow-Aktivität](assets/daily_activity.png)

## Bot-Profil-Muster (API-verifiziert)

Die Bot-Accounts zeigen ein überraschend hohes Profil-Ausstattungsniveau:

| Merkmal | Anteil |
|---------|--------|
| Profilbild (Avatar) | **58/66** (88%) |
| Display-Name | 22/66 (33%) |
| Beschreibung/Bio | 12/66 (18%) |
| Mindestens 1 Post | 19/66 (29%) |
| Suspendiert/Gelöscht | **0/72** (0%) |

### Zwei Bot-Populationen im selben Cluster

**Population A — „Deutschsprachige Tarnbots":**
- Plausible deutsche Handles: `miahungrigesherz`, `fraurollmops`, `jens-kessler`
- Manche mit echtwirkenden Bios: „Lehrkraft für Politik und Geschichte", „Fußgängerin, Serienkuckerin"
- Einige mit realen Posts (bis zu 17)
- Avatare vorhanden, aber generisch

**Population B — „Goth Girl"-Spam:**
- Englische Handles: `gothgirlrileyy`, `rileyraygoth`, `sophierosegoth`
- Standardisierte Bios: „19 | [City] | IG + TG: @handle"
- Immer genau 1–2 Posts
- Alle verweisen auf Instagram/Telegram (Social-Engineering → Krypto-/Romance-Scam)

**Bemerkenswerte Bots mit Posts:**
- `alerta93.bsky.social` — 14 Posts
- `jens-kessler.bsky.social` — 17 Posts („Lehrkraft für Politik und Geschichte")
- `derrechtenutzer.bsky.social` — 7 Posts
- `fckafdemail.bsky.social` — 5 Posts

Die Accounts mit vielen Posts könnten **kompromittierte echte Accounts** oder besonders
gut vorbereitete Sock-Puppets sein.

## Hypothese: Geschäftsmodell

```
┌─────────────────────────────────────────────────────┐
│  OPERATOR erstellt 2-7 Bot-Accounts pro Tag         │
│  (mit Avatar, manchmal Bio — nicht triviale Bots)   │
│  ↓                                                  │
│  Jeder Bot feuert ~11 Follows in < 2 Minuten:      │
│    • 6-11 echte deutsche Kultur-Accounts (Tarnung)  │
│    • 0-5 Spam-/Goth-Girl-Accounts (Monetarisierung) │
│  ↓                                                  │
│  Tägliche Staffelung neuer Bots erzeugt „Tropf"-    │
│  Effekt bei den Zielen (2-3 neue Follower/Tag)      │
│  → Unter dem Radar der Moderation                   │
│  ↓                                                  │
│  Spam-Accounts zielen auf Instagram/Telegram ab     │
│  → Krypto-Scam oder Romance-Scam-Pipeline           │
└─────────────────────────────────────────────────────┘
```

Die echten Kultur-Accounts dienen als **Tarnung**: Ein Account der @schreibersnaturarium.de,
@wernerkogler und @elsschot folgt, sieht auf den ersten Blick aus wie ein deutschsprachiger
Neuankömmling. Die eigentlichen Kunden sind die „Goth Girl"-Spam-Profile.

## Handle-Muster (vollständige Liste)

Alle 66 über API aufgelösten Bot-Handles (alphabetisch):

```
a-hmadsaleem        adr46              alerta93            anianina
avawilander         bennymy            berger51            boogibomber
casimiruua          catzastrophe       derglsndb           derrechtenutzer
drabons             dro36              ella-aust           fckafdemail
fraurollmops        gothgirlrileyy     gothgirlrumi        guidohoes
haasbarbara         hasipups           heinerthiel         hiep54
holgergollnast61    improvisando       iskanderfrancis     itssophiierose
itsvanessabeckerr   jajhahja           janhoekema          jens-kessler
jokon84             kaatvndveld        knight-of-justice   knut44
kopprene566-83      kuchenzahn-club    lisamarinna         lobsi
mafabuh             malte161           martin-daniel       matthes-young
miahungrigesherz    moebes             ni-els              nittsmav
nornadim2320-90     pilot-747-check    rileyraygoth        rudi62
scarredfury         sergiusch          skunny22            sophierosegoth
sophierosenurse     sylveev2justexists timo1980            tobias-namenlos
vanessabeckrr       veraenderung       veraltetgianni      whitewinterowl
willykaufmann       zoeymyheart
```

**Muster:**
- 66/66 rein lowercase
- 16/66 enthalten Ziffern (24%)
- 5/66 englische Spam-Pattern (`gothgirl*`, `riley*`, `sophie*`)
- Rest: plausible deutsche/niederländische Personennamen

## Abgrenzung zu anderen Netzwerken

| Merkmal | Dieses Cluster | Seasoning Rings | Burst-Follow-Spam |
|---------|----------------|-----------------|-------------------|
| Follows/Bot | 3–20 (Modus 11) | 62–182 | ~1.024 |
| Burst-Dauer/Bot | Median 128s | Sekunden | 3–5 Min |
| Staffelung | 2–7 Bots/Tag | 50–100 Bots/Tag | 10–106 Bots/Tag |
| Posts | 0–17 | 0 | 0 (dann Spam) |
| Avatare | 88% | ~0% | ~30% |
| Bots folgen einander | Nein | **Ja** (Ring-Muster) | Nein |
| Ziel-Sprache | Deutsch | Japanisch | Englisch |
| Handle-Muster | Deutsch/generisch | Japanisch | Ornate weibliche Namen |

## Erkennungsmethodik

Dieses Cluster ist besonders schwer zu erkennen, weil:

1. **Geringe Follow-Zahl:** 11 Follows ist im Normalbereich eines neuen Nutzers
2. **Keine Inter-Follows:** Keine Ring-Struktur sichtbar
3. **Gestaffelte Aktivierung:** Kein plötzlicher Follower-Spike beim Ziel
4. **Plausible Profile:** Deutsche Handles, 88% mit Avatar, manche mit Posts
5. **Mischnutzung:** Echte Kultur-Accounts als Tarnung neben Spam-Zielen

**Erkennung gelang durch:**
- Co-Follow-Analyse: 72/72 Bots folgen @schreibersnaturarium.de UND @colettemschmidt → statistisch unmöglich zufällig
- Fixed follow count: 40% folgen exakt 11 Accounts
- Burst-Timing: Alle Follows eines Bots in < 2 Minuten (Median)
- Community-Hinweis (Jasmin Schreiber)
- API-Verifizierung: Kein einziger Bot ist suspendiert oder gelöscht

## Nächste Schritte

- [x] Bot-DIDs exportiert (72 DIDs in `bot_dids.json`)
- [x] Timing-Daten exportiert (`assets/timing_data.json`)
- [ ] Bot-DIDs zur Moderations-Blockliste hinzufügen
- [ ] Breitere Suche: Cluster-Erweiterung über Sekundärziele (kattascha, golod, islieb)
- [ ] Monitoring: Tägliche Erkennung neuer Accounts mit diesem Fingerprint
- [ ] Meldung an Bluesky Trust & Safety
- [ ] Untersuchung der „kompromittiert?"-Accounts (jens-kessler, alerta93)

---

*Analyse erstellt am 30. Mai 2026 auf Basis von Bluesky-Firehose-Daten (Kusto/Fabric)
und öffentlicher Bluesky-API-Abfragen. Runde 2 ergänzt mit vollständiger API-
Profilauflösung und korrigierter Timing-Analyse.*
