# Full blocklist audit — 2026-11-12

Scope: all `games/*.txt` files, `sources.json -> game_map`, global aggregates, production validator, managed updaters, and repository policies.

## Structural audit

The first forced run of the new `scripts/audit_all_blocklists.py` completed successfully:

- 32 gaming profiles and 32 `game_map` entries, with no orphans in either direction;
- 0 duplicated/invalid production entries found by the validator;
- exact equivalence of global domain and IP aggregates to the allowed union of game lists;
- correct exclusions of `Cloudflare_AWS`, `OutlastTrials`, regional `Darktide`/`Fallout76_AWS` ranges, and selected community AWS CoH2 entries;
- an audited full table of every profile is available in the GitHub Actions report artifact.

Run:

- https://github.com/YOZH3G/ru-gaming-blocklist/actions/runs/43163254758

The original first-pass snapshot had 1,285 global domains and 377 global IP/CIDR entries.

## Forced live-source pass

The managed workflow re-queried Cloudflare and AWS provider feeds, RIPE/BGP prefixes and Riot purpose communities, Kuro manifests, the Relic CoH2 article, WARDOGS provider ownership and current WB Agora DNS endpoints.

The authoritative refresh identified:

### Roblox

Added an AS22697-announced prefix:

- `2620:135:605e::/48`

This was absent from the previous checked-in BGP snapshot.

### Mortal Kombat 11

Six of six configured WB Agora/Insights hosts resolved successfully. The refreshed managed snapshot replaced these five earlier transient A records:

- `35.169.93.117/32`
- `52.206.122.187/32`
- `67.202.16.235/32`
- `100.56.72.62/32`
- `100.62.178.28/32`

with the current DNS answers:

- `32.194.7.188/32`
- `32.197.3.85/32`
- `54.156.167.239/32`
- `54.161.16.37/32`
- `100.28.158.17/32`

The five evidence-backed historical/static addresses configured by the existing MK11 updater are retained.

### Mortal Kombat 1

The previous MK1 list kept only four older /32 observations. It now follows the verified MK1 WB backend domains `k1-api.wbagora.com` and `prod-network-api.wbagora.com` and dynamically refreshes their IPv4 A records.

The initial November 12 discovery found:

- `3.218.246.218/32`
- `44.197.89.18/32`
- `32.197.3.85/32`
- `100.28.158.17/32`

The latter two overlap contemporaneous MK11 WB backend entries. All four older MK1 observations are preserved. No generic AWS regional ranges or realtime/PvP hostnames were added.

The managed run reported a HTTP 403 for some `mtgarena-support.wizards.com` and `streetfighter.com` page requests, but other authoritative first-party checks succeeded. These isolated page-access failures were not treated as proof of obsolete game endpoints.

Live run and source-driven diff:

- https://github.com/YOZH3G/ru-gaming-blocklist/actions/runs/43163254548
- https://github.com/YOZH3G/ru-gaming-blocklist/actions/runs/43163679456

## Operating policy

After this change, **19 of the 32 game profiles** have a source-aware update or verification path, including the dedicated daily AWS refreshers for Darktide/Fallout 76 and the new Mortal Kombat 1 DNS backend refresh.

The other **13** require evidence-based manual candidate review: Apex Legends/Rocket League, Arma Reforger, Battlefield, Dead by Daylight, EA/Origin, Epic/Fortnite, Gears of War, Goose Goose Duck, Minecraft, Outlast Trials, Photon Engine, Ubisoft/R6 Siege, and VRChat.

These profiles are still covered by the complete daily structural audit and the existing review-only collector; lack of a game-specific authoritative machine-readable source is not justification for generating generic AWS/Cloudflare/Akamai prefixes.

The new daily GitHub Actions audit checks every game file for syntax, duplicates, mapping coverage, and exact global aggregate membership, and uploads a Markdown report. It does not arbitrarily rewrite evidence-reviewed production lists or merge PRs.

See also:

- `evidence/mortal-kombat-1.md`
- `evidence/mortal-kombat-11.md`
- `scripts/audit_all_blocklists.py`
- `.github/workflows/audit-all-blocklists.yml`
