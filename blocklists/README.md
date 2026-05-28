# Blocklists

This directory is automatically updated daily by the [Update Blocklist](./../.github/workflows/update-blocklist.yml) workflow.

## Files

| File | Description |
|------|-------------|
| `blocklist.json` | Full scored blocklist with metadata and signals |
| `blocklist.txt` | Plain DID list (one per line) for easy import |
| `LATEST.md` | Summary stats from the most recent scan |

## Heuristic Scoring (v1.0)

Accounts are scored 0.0–1.0 based on these weighted signals:

| Signal | Weight | Description |
|--------|--------|-------------|
| `no_avatar` | +0.10 | Profile has no avatar image |
| `no_description` | +0.10 | Profile has no bio/description |
| `no_display_name` | +0.10 | Profile has no display name |
| `handle_pattern:consonant_cluster` | +0.25 | Handle is random consonants (e.g., `kamsjz`) |
| `handle_pattern:random_alphanum` | +0.20 | Handle is random alphanumeric (e.g., `n7uba880g`) |
| `handle_pattern:compound_number` | +0.15 | Handle is compound word+number (e.g., `mightybeam16344`) |
| `handle_pattern:firstname_number` | +0.10 | Handle is name+digits (e.g., `laurareyes474`) |
| `handle_pattern:adjective_noun` | +0.10 | Handle is adjective-noun (e.g., `soft-deer`) |
| `zero_posts` | +0.15 | Account has never posted |
| `very_few_posts` | +0.08 | Account has ≤3 posts |
| `follow_only_no_followers` | +0.15 | Follows >10 but has 0 followers |
| `high_follow_ratio` | +0.12 | Following/followers ratio >10 |
| `mass_follow_zero_posts` | +0.15 | >50 follows with zero posts |

**Threshold:** Accounts scoring ≥0.45 are included in the blocklist.

## Scanned PDS Servers

- `pds.louisvillebsky.app`
- `haruhwa.com`
