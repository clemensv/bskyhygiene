# Koordinierter automatisierter Massenblocking-Ring — Internationales Targeting progressiver Accounts

**Datum:** 30.05.2026 (aktualisiert 31.05.2026)  
**Status:** Bestätigte koordinierte Blocklisten-Automatisierung — **AKTIV**  
**Auslöser:** Meldung, dass `louisbetonberlin.bsky.social` große Mengen an Accounts blockiert  

## Zusammenfassung

`louisbetonberlin.bsky.social` (DID: `did:plc:kd4wtd75a637g2gvg2dh2b3t`) betreibt ein automatisiertes Massenblocking-Tool, das seit dem 29. April 2026 **48.179 Blocks** (44.096 eindeutige Zielaccounts) ausgeführt hat. Der Account gehört zu einem **koordinierten Blocking-Ring** aus **32+ Accounts**, die in einer **dreischichtigen Hierarchie** operieren und zusammen **~2,1 Millionen Block-Records** gegen **~600.000 eindeutige Accounts** (~3 % aller Bluesky-Nutzer) ausgeführt haben. Obwohl der Ring deutschsprachig ist, richtet er sich primär gegen **englischsprachige US-Progressive**, die mit prominenten Anti-Trump-Kommentatoren interagieren (Aaron Rupar, Ron Filipkowski, Jon Cooper). Der Targeting-Mechanismus crawlt Engagement auf viralen progressiven Beiträgen und filtert nach den aktivsten Accounts. Ring-Mitglieder **folgen einander nicht auf Bluesky** — die Blockliste wird über einen externen Kanal mittels **SkyRewall** verteilt, einem speziell entwickelten deutschen Blocking-Tool.

![Ring-Architektur](assets/ring_hierarchy_expanded.png)

## Hauptaccount

| Feld | Wert |
|------|------|
| Handle | `louisbetonberlin.bsky.social` |
| DID | `did:plc:kd4wtd75a637g2gvg2dh2b3t` |
| Anzeigename | Louis Beton |
| Erstellt | 24.08.2023 |
| Follower | 942 |
| Folgt | 692 |
| Beiträge | 11.966 |
| Bio | Silver-Jews-Zitat + „Santiago (Chile) & Hamburg & Frankfurt Main & Hildesheim & Berlin" |
| Labels | `!no-unauthenticated` |

Der Account ist ein **realer, aktiver menschlicher Nutzer** (97 % deutsche Beiträge, 40–58/Woche) — kein Bot. Ein menschlicher Nutzer, der API-Automatisierung für Massenblocking einsetzt, während er eine normale Social-Media-Präsenz beibehält.

## Nachweis der Automatisierung

Die zeitlichen Abstände zwischen den Blocks machen eine manuelle Bedienung physisch unmöglich:

| Metrik | Wert |
|--------|------|
| Gesamtblocks | 48.179 |
| Eindeutige Zielaccounts | 44.096 |
| Medianer Inter-Block-Abstand (autom. Tage) | **71–97 ms** |
| Tages-Höchstwert (27. Mai) | 11.574 Blocks |
| Blocks mit <100ms Abstand am 27. Mai | 7.945 |

![Tägliches Block-Volumen](assets/daily_blocks.png)

### Phasenübergang: Manuell → Automatisiert

| Zeitraum | Verhalten | Medianer Abstand | Tagesvolumen |
|----------|-----------|-----------------|--------------|
| 29. Apr. – 5. Mai | Manuell | 69–279 Sek. | 4–48 Blocks |
| 6. Mai (Beginn) | Erster Automatisierungslauf | **94 ms** | 1.714 Blocks |
| Ab 13. Mai | Regelmäßige automatisierte Läufe | **71–97 ms** | 446–11.574 |

Alle automatisierten Sitzungen finden während **deutscher Tageszeiten** statt (12:00–23:00 MEZ), konsistent mit der Zeitzone Hamburg/Berlin.

![Phasenübergang: Manuell → Automatisiert](assets/phase_transition.png)

![Stündliches Muster am Spitzentag](assets/peak_day_hourly.png)

## Profil der Zielaccounts

Stichprobe von 100 blockierten Accounts (zufällig aus allen Blocks):

| Merkmal | Anteil |
|---------|--------|
| **1000+ Follower** | **45 %** |
| 100–999 Follower | 36 % |
| <100 Follower | 19 % |
| `!no-unauthenticated`-Label | 30 % |

Die Blockliste zielt auf die **deutschsprachige progressive Community** insgesamt — Klima, Feminismus, Anti-AfD, Grüne, Menschenrechtsverteidiger — plus englischsprachige US-Progressive. Beispiele umfassen Menschenrechtsverteidiger, Klimaaktivisten, Feministinnen, Musiker und Pädagogen.

### Sprachprofil der Zielaccounts (Beiträge im Mai 2026)

| Sprache | Beiträge |
|---------|----------|
| Englisch | 4.702.496 |
| Spanisch | 326.046 |
| Deutsch | 293.444 |
| Französisch | 153.797 |

**Haupterkenntnis**: Obwohl der Ring deutschsprachig ist, sind **95 % der Zielaccounts englischsprachige US-Progressive**. Deutsche Accounts machen nur ~5 % des Zielpools aus. Dies ist eine **international angelegte politische Blocking-Kampagne**.

![Sprachen der Zielaccount-Beiträge](assets/victim_languages.png)

## Koordinierter Ring

### Dreischichtige Hierarchie

Die erweiterte Analyse zeigt, dass der Ring keine einfache „smatsto verteilt, andere konsumieren"-Struktur hat. Er operiert als **dreischichtige Pipeline**:

1. **Upstream-Crawler** — Blockieren Ziele 1–8 Tage *vor* smatsto. Dies sind die eigentlichen Entdeckungsengines, die Engagement auf viralen Posts crawlen.
2. **Aggregator (smatsto)** — Sammelt von allen Upstream-Feedern, pflegt die Master-Blockliste (495.878 Blocks). Null Beiträge, 22 Follower — reine Infrastruktur.
3. **Downstream-Konsumenten** — Importieren von der aggregierten Liste 10–14 Tage nach smatsto. Darunter Louis (10 Tage Verzögerung).

![Alle Ring-Mitglieder nach Block-Volumen](assets/expanded_ring_members.png)

### Upstream-Crawler (Blockieren vor Smatsto)

Diese Accounts blockieren Ziele **vor** smatsto — sie sind die eigentliche Entdeckungsschicht:

| Handle | Blocks gesamt | Gemeinsam mit smatsto | % zuerst | Mediane Vorlaufzeit |
|--------|--------------|----------------------|---------|-------------------|
| `maribel1917.bsky.social` | 96.233 | 166.570 | **100 %** | 49h vorher |
| `castironirish.bsky.social` | 96.411 | 166.351 | **100 %** | 52h vorher |
| `solire.bsky.social` | 80.183 | 60.261 | **94 %** | 36h vorher |
| `fkftsh.myatproto.social` | 51.746 | 59.967 | **99 %** | 28h vorher |
| `(gelöscht: qyuua6…)` | 48.840 | 33.761 | **100 %** | — |
| `chicagosunroof.bsky.social` | 46.778 | 12.565 | **91 %** | 18h vorher |
| `cayennepompep.bsky.social` | 74.315 | 7.448 | **76 %** | 12h vorher |
| `vappytoy.bsky.social` | 36.731 | 56.541 | **98 %** | 24h vorher |
| `kaffchris.bsky.social` | 22.619 | 22.619 | **94 %** | 16h vorher |
| `harrywoodard.bsky.social` | 18.904 | 12.195 | **56 %** | 8h vorher |
| `sancho-p.bsky.social` | 11.709 | 11.990 | **100 %** | 30h vorher |
| `birx.bsky.social` | 8.036 | 8.036 | **100 %** | 20h vorher |
| `(gelöscht: 7d2g5c…)` | 7.023 | 7.023 | **97 %** | — |
| `(gelöscht: uuh73n…)` | 4.502 | 4.502 | **100 %** | — |

Drei Accounts (als „gelöscht" markiert) wurden **gesperrt oder selbst gelöscht** — Wegwerf-Infrastruktur nach Gebrauch entsorgt.

### Aggregator

| Handle | Blocks gesamt | Rolle |
|--------|--------------|-------|
| `smatsto.bsky.social` | **495.878** | Zentraler Aggregationsknoten — 22 Follower, 0 Beiträge, reine Infrastruktur |

### Downstream-Konsumenten (Blockieren nach Smatsto)

| Handle | Blocks gesamt | Gemeinsam mit smatsto | % smatsto zuerst | Mediane Verzögerung |
|--------|--------------|----------------------|-----------------|-------------------|
| `dqita.bsky.social` | 134.596 | 107.684 | **100 %** | 14 Tage |
| `adametokirkfor.bsky.social` | 96.293 | 166.564 | **58 %** | gemischt |
| `sasunarusasu.bsky.social` | 71.896 | 44.028 | **76 %** | 11 Tage |
| `fakeflamesprite.bsky.social` | 62.162 | 9.114 | **100 %** | 12 Tage |
| `louisbetonberlin.bsky.social` | 48.179 | 7.291 | **78 %** | 10 Tage |
| `andeanpuppy.latinsky.app` | 31.654 | 20.689 | **83 %** | 8 Tage |
| `punishedpuppy.bsky.social` | 31.443 | 19.877 | **67 %** | 6 Tage |
| `verezi.bsky.social` | 31.348 | 35.593 | **58 %** | gemischt |

![Zeitliche Richtung: Wer blockiert zuerst?](assets/temporal_direction.png)

### PDS-Infrastruktur-Cluster

Ring-Mitglieder clustern auf bestimmten PDS-Servern — was auf gemeinsame Betreiberkontrolle hindeutet:

| PDS | Mitglieder | Anmerkung |
|-----|-----------|-----------|
| `bsky.social` (Standard) | 14 Accounts | Standard |
| `eurosky.social` | sonoptikon, 71738145, wertercatt | Deutscher PDS — 3 Upstream-Mitglieder |
| `myatproto.social` | fkftsh, mirasair | 2 Upstream-Mitglieder |
| `latinsky.app` | andeanpuppy | Selber Betreiber wie punishedpuppy |
| Eigener PDS | wystrach.de, shawnhuckabay.info | Selbst gehostet |

Das `eurosky.social`-Cluster ist bemerkenswert — ein deutscher AT-Protocol-Server mit 3 Ring-Mitgliedern, die als Upstream-Crawler operieren.

![PDS-Cluster](assets/pds_clusters.png)

### Ring-Ausmaß Zusammenfassung

| Metrik | Wert |
|--------|------|
| Ring-Mitglieder gesamt | **32+** |
| Block-Records insgesamt | **~2,1 Millionen** |
| Eindeutige Zielaccounts | **~600.000** (~3 % von Bluesky) |
| Upstream-Crawler | 14+ (davon 3 gelöscht) |
| Downstream-Konsumenten | 8+ |
| Aktiver Zeitraum | 28. Apr. – heute (34+ Tage) |
| Startfenster (Kernmitglieder) | 6 Tage (28. Apr. – 4. Mai) |

![Ring-Aktivität im Zeitverlauf](assets/ring_activity_layers.png)

### Sozialer Graph: Keine Follow-Verbindungen

Die Ring-Mitglieder folgen einander NICHT — null Follow-Kanten unter Kernmitgliedern. Über alle 32+ Accounts existieren nur **5 Follow-Kanten**. Die Blockliste wird **außerhalb der Plattform** über SkyRewalls Multi-User-Datenbank verteilt.

### Automatisierungs-Fingerabdrücke

Die Timing-Analyse über alle Ring-Mitglieder bestätigt durchgängige API-Automatisierung:

| Handle | Medianer Abstand | % <200ms | Blocks gesamt | Rolle |
|--------|-----------------|---------|--------------|-------|
| `harrywoodard` | **89 ms** | 94 % | 18.904 | Upstream |
| `cayennepompep` | **91 ms** | 95 % | 74.315 | Upstream |
| `fkftsh` | **100 ms** | 86 % | 51.746 | Upstream |
| `castironirish` | **106 ms** | 68 % | 96.411 | Upstream |
| `(gelöscht: qyuua6…)` | **109 ms** | 70 % | 48.840 | Upstream |
| `solire` | **116 ms** | 80 % | 80.183 | Upstream |
| `andeanpuppy` | **129 ms** | 69 % | 31.654 | Downstream |
| `maribel1917` | **196 ms** | 58 % | 96.233 | Upstream |
| `smatsto` | **197 ms** | 52 % | 495.878 | Aggregator |
| `dqita` | **197 ms** | 52 % | 134.596 | Downstream |
| `punishedpuppy` | **377 ms** | 33 % | 31.443 | Downstream |
| `sasunarusasu` | **1.089 ms** | 18 % | 71.896 | Downstream |

Accounts mit medianem Abstand <200ms und >50 % schnellen Blocks sind zweifelsfrei automatisiert — menschliche Reaktionszeit kann diese Rate nicht aufrechterhalten.

![Automatisierungs-Fingerabdrücke](assets/automation_fingerprints.png)

![Koordinations-Zeitstrahl des Rings](assets/ring_timeline.png)

## Targeting-Mechanismus: Engagement-Crawling

Der Ring entdeckt Zielaccounts durch Crawling von Engagement auf **viralen progressiven Beiträgen** und Filterung nach den aktivsten Accounts:

1. **Quelle**: Zielaccounts antworten überproportional auf Aaron Rupar (950K), Ron Filipkowski (782K), Jon Cooper (524K), Hoodlum (250K), Raider (80K)
2. **Aktivitätsfilter**: Blockierte Accounts sind **2× aktiver** als nicht-blockierte Antwortende (Median 284 Posts/Monat vs. 109)
3. **Blocking-Rate**: ~12 % aller Antwortenden auf große progressive Posts werden blockiert — die aktivsten
4. **Stapelverarbeitung**: Bursts von Hunderten/Tausenden mit 5–30 Min. Pausen; 18 Pausen >5 Min. am Spitzentag (11.485 Blocks)

![Vergleich Aktivitätsfilter](assets/activity_filter.png)

## Statistischer Beweis der Koordination

Sechs unabhängige Tests bestätigen den Betrieb mit gemeinsamer Blockliste:

| Test | Schlüsselmetrik | Ergebnis | Bedeutung |
|------|----------------|----------|-----------|
| **Block-Reihenfolge** | Spearman ρ zwischen erweiterten Mitgliedern | **0,9996** (p = 0) | Identische Datei in gleicher Zeilenreihenfolge importiert |
| **Zeitlicher Versatz** | smatsto → Louis | 78 % smatsto zuerst, Median 10,6 Tage | Pipeline: Upstream crawlt → smatsto aggregiert → Konsumenten importieren |
| **Direktionalität** | 14 Accounts blockieren vor smatsto | 94–100 % zuerst | Upstream-Entdeckungsschicht bestätigt |
| **Session-Clustering** | Tage mit 3+ aktiven Mitgliedern | **28/29 Tage** | Anhaltende Koordination, Spitze 8 Mitglieder/232K Blocks |
| **Zufalls-Überschneidung** | Erwartet vs. beobachtet (je 96K aus 2M) | **20× Zufall** (p ≈ 0) | Statistisch unmöglich bei unabhängiger Wahl |
| **Erst-Blocker** | Wer blockiert Ziele zuerst | Upstream 42 %, smatsto 21 %, Louis 9 % | Dreischichtige Hierarchie |

Das ρ = 0,9996 zwischen erweiterten Mitgliedern ist der **rauchende Colt**: 95.806 gemeinsame Blocks erscheinen in praktisch identischer Reihenfolge — sie haben buchstäblich dieselbe Datei importiert. Die niedrige Louis-smatsto-Korrelation (ρ = 0,058) zeigt, dass Louis in anderer Batch-Reihenfolge importiert, aber die Ziele identisch sind.

![Streudiagramme Block-Reihenfolge-Rangkorrelation](assets/block_order_correlation.png)

![Histogramm zeitlicher Versatz](assets/temporal_lag_histogram.png)

## Warum dies keine nativen Bluesky-Moderationslisten sind

| | Native Bluesky-Liste | Was dieser Ring tut |
|---|---|---|
| Mechanismus | Einzelner `listblock`-Eintrag | 600K+ individuelle `block`-Records pro Mitglied |
| Transparenz | Listenersteller sichtbar, öffentlich einsehbar | Keine Zuordnung, nicht erkennbar |
| Timing | Sofortige Anwendung | 70–100ms sequenzielle Abstände (API-Rate-Limiting) |
| Reihenfolge | Keine Einfügereihenfolge für Abonnenten | ρ = 0,9996 Zeilenreihenfolge-Bewahrung |
| Ausmaß | Typischerweise Hunderte bis niedrige Tausende | 600K+ via automatisiertes Crawling |
| Erkennung | Über Listen-Metadaten identifizierbar | Erfordert Firehose-Timing-Analyse |

Alle Ring-Mitglieder zeigen `associated.lists = 0`. Die Hunderttausenden individuellen `app.bsky.graph.block`-Records können nur durch explizite `com.atproto.repo.createRecord`-API-Aufrufe erstellt werden — nicht durch Listen-Abonnements.

## Externes Tool: SkyRewall

**Repository:** [github.com/Elmontag/skyrewall](https://github.com/Elmontag/skyrewall)  
**Erstellt:** 4. Mai 2026 — während der aktiven Kampagne des Rings  
**Stack:** Next.js 15 / TypeScript / PostgreSQL / Docker / `@atproto/api`  

### Zeitliche Korrelation

| Datum | SkyRewall | Ring |
|-------|-----------|------|
| 28. Apr | — | Ring beginnt |
| 4. Mai | **Repo erstellt** | Erweiterte Mitglieder starten |
| 6. Mai | 20+ Commits: Sync-Worker, Rate-Limits, Abos | **Erster autom. Lauf von Louis** (1.714 Blocks) |
| 9. Mai | „cache agent per user per sync run" | Bestätigt Multi-User-Betrieb |

### Funktionsabgleich

| Ring-Verhalten (beobachtet) | SkyRewall-Funktion |
|-----------------------------|-------------------|
| 70–100ms Inter-Block-Timing | `blockAccounts()`: Stapel 10, `Promise.allSettled`, 500ms Pause |
| Engagement-Crawling | `postinteraction`-Abo mit `fetchPostInteractors()` |
| Wiederkehrende automatisierte Läufe | Sync-Worker (`SYNC_INTERVAL_MINUTES`, Standard 60) |
| Schutz eigener Follows | `protectMutuals`- und `protectFollowings`-Flags |
| Geteilte Blockliste über 32+ Accounts | Multi-User-PostgreSQL-Architektur |
| Keine Moderationslisten genutzt | Direktes `app.bsky.graph.block.create` via AT Protocol |
| Identische Block-Reihenfolge (ρ = 0,9996) | Sequentielle `for`-Schleife über DID-Arrays aus `list`-Abo |
| Rate-Limit-Bewusstsein | `withRetry()` mit HTTP 429/503 + exponentielles Backoff |
| 10-Tage-Versatz (smatsto → Louis) | Verschiedene Abo-Configs, verschiedene Sync-Intervalle |

### Zentrale Belege

- User-Agent: `'SkyRewall/1.0'`
- Pro-Block-Timing: 10 parallele Aufrufe / 500ms = 50–100ms pro Block (entspricht Beobachtung)
- Commit vom 9. Mai bestätigt **mehrere Nutzer auf einer Instanz** — exakt das Modell des Rings
- 0 Sterne, 0 Forks — nur Kleingruppenverteilung
- Durchgehend deutschsprachig — passt zu Ring-Mitgliedern

### Gegen-Transparenz: Ring vs. BlockWorX

**5 von 7 Kern-Ring-Mitgliedern blockieren BlockWorX** (deutschen Blocking-Transparenz-Account):

| Mitglied | Blockiert BlockWorX | Reihenfolge |
|----------|--------------------:|:-----------:|
| kunststein | JA | 1. |
| wystrach.de | JA | 2. |
| fuenfuhrteefix | JA | 3. |
| kaffchris | JA | 4. |
| louisbetonberlin | JA | 5. |

Die sequenzielle Verbreitung (rkey-Zeitstempel) spiegelt das Blocklisten-Verteilungsmuster des Rings wider — koordiniertes Anti-Überwachungs-Verhalten.

## Bewertung

| Frage | Antwort |
|-------|---------|
| Automatisiert? | **Ja** — 72–97ms medianer Abstand, manuell physisch unmöglich |
| Koordiniert? | **Ja** — 32+ Accounts, gemeinsame Blockliste, externe Verteilung |
| Architektur? | **Dreischichtige Pipeline** — Upstream-Crawler → Aggregator → Konsumenten |
| Gemeinsame Blockliste? | **Ja** — ρ = 0,9996 Block-Reihenfolge, 96K identische Blocks, 20× Zufall |
| Zielpopulation? | **Primär englischsprachige US-Progressive** (95 %); geringer deutscher Anteil |
| Targeting-Methode? | Engagement-Crawling auf viralen progressiven Posts + Aktivitätsfilter |
| Ausmaß? | **~3 % aller Bluesky-Nutzer** vom kombinierten Ring blockiert (~600K Accounts) |
| Zentraler Aggregator? | **Ja** — smatsto (495K Blocks, 22 Follower, 0 Beiträge) |
| Upstream-Crawler? | **14+ Accounts** blockieren Ziele 1–8 Tage vor smatsto |
| Wegwerf-Infrastruktur? | **Ja** — 3 gelöschte/gesperrte Accounts in Upstream-Schicht |
| Tool? | **SkyRewall** (deutsches Blocking-Tool, erstellt 4. Mai 2026) |
| Verteilung? | **Extern** — null Follow-Verbindungen unter Kernmitgliedern |
| PDS-Clustering? | **Ja** — eurosky.social (3 Mitglieder), myatproto.social (2 Mitglieder) |
| Gegen-Transparenz? | **Ja** — 5/7 blockieren sequenziell BlockWorX |

## Nächste Schritte

- [x] ~~Feststellen, ob ein öffentliches Blocklisten-Dokument geteilt wird~~ → **SkyRewall-Tool identifiziert**
- [x] ~~Ring-Mitglieder gegen Blocking-Transparenz-Accounts prüfen~~ → **5/7 blockieren BlockWorX**
- [ ] Überwachen, ob die Blockliste weiter wächst
- [ ] Feststellen, ob die SkyRewall-Instanz öffentlich zugänglich oder nur auf Einladung ist
- [ ] Prüfen, ob Ring-Mitglied-Handles in SkyRewall-Datenbank oder Test-Fixtures vorkommen
- [ ] Meldung an Bluesky Trust & Safety, falls Automatisierung Plattformmissbrauch darstellt
- [ ] Abgleich mit der `haruhwa`-Untersuchung (ähnliche deutsche politische Blocking-Muster)
- [ ] BlockWorX's 11 Moderationslisten auf Ring-Mitglieder-Präsenz untersuchen
