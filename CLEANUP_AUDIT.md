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

- global domain list: 1,202 domains after restoring specific evidence-backed shared endpoints;
- global IP/CIDR list: 35 prefixes;
- `Cloudflare_AWS.txt` removed;
- `Other_Games.txt` removed;
- historical review queue reset;
- automatic production writes disabled by default;
- repository discovery disabled;
- short ambiguous aliases removed;
- production validator added and wired into CI.

## IP policy

The lists are action-neutral: consumers may use them either as include lists or as excludes. IP/CIDR therefore describes infrastructure associated with the game, not whether the address should be bypassed.

Network ownership remains strong evidence, but it is not the only acceptable evidence. Narrow third-party IPs may be retained when operational evidence ties them to a game. Very broad cloud/CDN prefixes are still excluded because they are not specific enough for a neutral game list.

The current verified owned-network baseline includes Riot Games (AS6507), Roblox (AS22697), and Valve (AS32590).

## Domain policy

Per-game files contain domains tied to the game, publisher, anti-cheat, platform backend, or an evidenced service dependency.

Shared infrastructure is allowed when the hostname itself is specific enough (for example a Riot/Vanguard ELB, Steam Akamai hostname, or Ubisoft S3 bucket) or when a concrete source supports the association. Bare provider roots such as `cloudfront.net`, `amazonaws.com` or `cloudflare.com` remain excluded.

Provenance for less obvious shared endpoints is documented in `evidence/shared-endpoints.json`.

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