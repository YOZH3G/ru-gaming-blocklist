# Cleanup audit — 2026-09-23

## Summary

The repository accumulated a large amount of unrelated and overly broad data because automatic discovery results were appended directly to production files.

This cleanup changes the model from **append-first** to **review-first**.

### Before

- global domain list: about 19,393 non-empty entries;
- global IP/CIDR list: 18,544 entries;
- `games/Warframe.txt`: 13,765 entries, including 13,690 IP/CIDR entries;
- `games/Other_Games.txt`: 8,884 entries;
- review queue: more than 10,000 non-empty lines.

Examples of pollution observed during the audit included pseudo-domains/file names such as `winws.exe`, `services.msc`, `.zip`/installer names, unrelated web services, public DNS addresses, whole Cloudflare/AWS ranges, and domains belonging to unrelated games.

### After

- global domain list: 1,128 domains, rebuilt from cleaned per-game lists;
- global IP/CIDR list: 33 high-confidence network prefixes;
- `Cloudflare_AWS.txt` removed;
- `Other_Games.txt` removed;
- historical review queue reset;
- automatic production writes disabled by default;
- repository discovery disabled;
- short ambiguous aliases removed;
- production validator added and wired into CI.

## IP policy

IP/CIDR entries are retained only when network ownership can be reasonably tied to the gaming operator.

The initial verified set is intentionally conservative and includes prefixes associated with:

- Riot Games (AS6507);
- Roblox (AS22697);
- Valve (AS32590).

Generic AWS, Cloudflare, Google, Akamai and similar infrastructure is not treated as game-owned IP space.

## Domain policy

Per-game files are now filtered to domains tied to the game, publisher, platform backend, or a narrowly justified service dependency.

Generic infrastructure and unrelated third-party domains are excluded from production even when they appeared near a game name in GitHub issues or configuration snippets.

## Automation changes

`scripts/update_gaming_blocklists.py` now defaults to review-only behavior through `output.production_writes=false`.

`sources.json` no longer uses generic `Other_Games` / `Cloudflare_AWS` buckets and no longer performs broad repository discovery.

`scripts/validate_blocklists.py` rejects:

- malformed/pseudo-domains;
- common generic infrastructure in production;
- duplicate lines;
- non-global IP networks;
- excessively broad IPv4/IPv6 prefixes.

## Follow-up

Future additions should be reviewed before promotion from `_review/` to production. Completeness is secondary to avoiding collateral routing/blocking.
