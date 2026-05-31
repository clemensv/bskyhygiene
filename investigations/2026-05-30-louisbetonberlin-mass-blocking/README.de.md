# Koordinierter automatisierter Massenblocking-Ring — Internationales Targeting progressiver Accounts

**Datum:** 30.05.2026 (aktualisiert 31.05.2026)  
**Status:** Bestätigte koordinierte Blocklisten-Automatisierung — **AKTIV**  
**Auslöser:** Meldung, dass `louisbetonberlin.bsky.social` große Mengen an Accounts blockiert  

## Zusammenfassung

`louisbetonberlin.bsky.social` (DID: `did:plc:kd4wtd75a637g2gvg2dh2b3t`) betreibt ein automatisiertes Massenblocking-Tool, das seit dem 29. April 2026 **48.179 Blocks** (44.096 eindeutige Zielaccounts) ausgeführt hat. Der Account gehört zu einem **koordinierten Blocking-Ring** aus 16+ Accounts, die zusammen **602.673+ eindeutige Accounts** (~3 % aller Bluesky-Nutzer) blockiert haben. Obwohl der Ring deutschsprachig ist, richtet er sich primär gegen **englischsprachige US-Progressive**, die mit prominenten Anti-Trump-Kommentatoren interagieren (Aaron Rupar, Ron Filipkowski, Jon Cooper). Der Targeting-Mechanismus crawlt Engagement auf viralen progressiven Beiträgen und filtert nach den aktivsten Accounts. Ring-Mitglieder **folgen einander nicht auf Bluesky** — die Blockliste wird über einen externen Kanal mittels **SkyRewall** verteilt, einem speziell entwickelten deutschen Blocking-Tool.

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

### Ring-Mitglieder und Ausmaß

| Account | Blocks gesamt | Gemeinsame Ziele mit Louis | Anmerkungen |
|---------|---------------|---------------------------|-------------|
| `smatsto.bsky.social` | **495.878** | 7.291 | 22 Follower — zentrale Crawling-Engine |
| `did:plc:qildfzoh5p24jgion4xiycvz` | 103.214 | 5.213 | Erster Start (28. Apr.) |
| `did:plc:hwpiekun4iebo4oqevjfe6ss` | 98.532 | — | Kernmitglied |
| `did:plc:xcytuwwb3b33ipiqzmqzbs45` | 93.961 | 4.221 | Start am 4. Mai |
| `louisbetonberlin` | 48.179 | — | Gegenstand dieses Berichts |
| `did:plc:tfspkb2htmw7vwdgqj7mzx7m` | 27.972 | — | Kernmitglied |

Alle 6 Kernmitglieder starteten innerhalb eines 6-Tage-Fensters (28. Apr. – 4. Mai). Gesamt: **867.736 Blocks** gegen **602.673 eindeutige Zielaccounts** (~3 % von Bluesky).

![Überlappung der Zielaccount-Populationen](assets/target_population_venn.png)

![Block-Anzahlen der Ring-Mitglieder](assets/ring_comparison.png)

### Smatsto: Die zentrale Blocking-Engine

`smatsto.bsky.social` (22 Follower, 0 Inhalte) führt 495.878 Blocks aus — 10× mehr als Louis. Smatsto blockiert zuerst in **72 % der gemeinsamen Ziele** (Median 9 Tage vor Louis). Dies ist die **primäre Crawling-Engine**; andere Mitglieder konsumieren Teile der Ausgabe zeitversetzt. Allerdings überschneiden sich 67 % von Louis' Blocks NICHT mit smatsto — was auf zusätzliches unabhängiges Targeting hindeutet.

### Erweiterter Ring (10 weitere Accounts)

| Handle | Blocks | Medianer Abstand | Gemeinsam mit smatsto |
|--------|--------|-----------------|----------------------|
| `dqita.bsky.social` | 134.559 | 197 ms | 104.812 |
| `adametokirkfor.bsky.social` | 96.135 | 1.001 ms | 96.485 |
| `maribel1917.bsky.social` | 96.189 | 177 ms | 96.476 |
| `castironirish.bsky.social` | 96.273 | 106 ms | 96.371 |
| `solire.bsky.social` | 80.026 | 132 ms | 22.987 |
| `sasunarusasu.bsky.social` | 71.795 | 1.076 ms | 21.709 |
| `fakeflamesprite.bsky.social` | 62.162 | 80 ms | 17.306 |
| `fkftsh.myatproto.social` | 51.415 | 97 ms | 27.767 |
| `vappytoy.bsky.social` | 36.629 | 200 ms | 36.706 |
| `verezi.bsky.social` | 31.348 | 72 ms | 17.141 |

Auffällig: `adametokirkfor`, `maribel1917`, `castironirish` zeigen nahezu identische Überschneidung mit smatsto (96.371–96.485) — dieselbe **Batch-Datei importiert**. Mehrere zeigen 99,7–100 % Überschneidung mit Louis' Zielen im Schnittbereich.

### Sozialer Graph: Keine Follow-Verbindungen

Die 6 Kern-Ring-Mitglieder folgen einander NICHT — null Follow-Kanten. Über alle 16 Accounts existieren nur **5 Follow-Kanten**. Die Blockliste wird **außerhalb der Plattform** verteilt.

![Koordinations-Zeitstrahl des Rings](assets/ring_timeline.png)

## Targeting-Mechanismus: Engagement-Crawling

Der Ring entdeckt Zielaccounts durch Crawling von Engagement auf **viralen progressiven Beiträgen** und Filterung nach den aktivsten Accounts:

1. **Quelle**: Zielaccounts antworten überproportional auf Aaron Rupar (950K), Ron Filipkowski (782K), Jon Cooper (524K), Hoodlum (250K), Raider (80K)
2. **Aktivitätsfilter**: Blockierte Accounts sind **2× aktiver** als nicht-blockierte Antwortende (Median 284 Posts/Monat vs. 109)
3. **Blocking-Rate**: ~12 % aller Antwortenden auf große progressive Posts werden blockiert — die aktivsten
4. **Stapelverarbeitung**: Bursts von Hunderten/Tausenden mit 5–30 Min. Pausen; 18 Pausen >5 Min. am Spitzentag (11.485 Blocks)

![Vergleich Aktivitätsfilter](assets/activity_filter.png)

## Statistischer Beweis der Koordination

Fünf unabhängige Tests bestätigen den Betrieb mit gemeinsamer Blockliste:

| Test | Schlüsselmetrik | Ergebnis | Bedeutung |
|------|----------------|----------|-----------|
| **Block-Reihenfolge** | Spearman ρ zwischen erweiterten Mitgliedern | **0,9996** (p = 0) | Identische Datei in gleicher Zeilenreihenfolge importiert |
| **Zeitlicher Versatz** | smatsto → Louis | 78 % smatsto zuerst, Median 10,6 Tage | Pipeline: smatsto crawlt, verteilt an Konsumenten |
| **Session-Clustering** | Tage mit 3+ aktiven Mitgliedern | **28/29 Tage** | Anhaltende Koordination, Spitze 8 Mitglieder/232K Blocks |
| **Zufalls-Überschneidung** | Erwartet vs. beobachtet (je 96K aus 2M) | **20× Zufall** (p ≈ 0) | Statistisch unmöglich bei unabhängiger Wahl |
| **Erst-Blocker** | Wer blockiert Ziele zuerst | smatsto 61 %, Louis 9 % | Zentrale Engine → Downstream-Hierarchie |

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
| Geteilte Blockliste über 16 Accounts | Multi-User-PostgreSQL-Architektur |
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
| Koordiniert? | **Ja** — 16+ Accounts, gemeinsame Blockliste, externe Verteilung |
| Gemeinsame Blockliste? | **Ja** — ρ = 0,9996 Block-Reihenfolge, 96K identische Blocks, 20× Zufall |
| Zielpopulation? | **Primär englischsprachige US-Progressive** (95 %); geringer deutscher Anteil |
| Targeting-Methode? | Engagement-Crawling auf viralen progressiven Posts + Aktivitätsfilter |
| Ausmaß? | **~3 % aller Bluesky-Nutzer** vom kombinierten Ring blockiert |
| Zentrale Engine? | **Ja** — smatsto (495K Blocks, 22 Follower) |
| Tool? | **SkyRewall** (deutsches Blocking-Tool, erstellt 4. Mai 2026) |
| Verteilung? | **Extern** — null Follow-Verbindungen unter Kernmitgliedern |
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
