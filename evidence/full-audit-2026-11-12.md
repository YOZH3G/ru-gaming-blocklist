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


## Independent review and updater safety correction

Reviewed all 32 profiles again against PR commit `91b001f8737ee67e7a8b367179ba7d3cfa784b51` on 2026-11-12. The production validator and exact aggregate audit passed locally: 1,285 global domains and 380 global IP/CIDR entries. Live-source run 43163953911 was independently checked: it completed at 05:50 UTC with an unchanged generated snapshot; MK1 resolved 2/2 and MK11 6/6 configured hosts. This is a point-in-time source check, not an in-game connectivity test.

Found a destructive partial-DNS case in both WB updaters: a single successful hostname previously allowed replacement of the whole IP set. Both now require every configured hostname to return public IPv4 addresses before writing. Failure preserves the previous file and raises an error. Regression coverage includes complete, partial, empty, private-only, and totally failed DNS responses for both games (10 scenarios).

All CIDRs are canonical. Containment exists in BattleNet (43 entries), CallOfDuty (2), OutlastTrials (1), and Roblox (68). These are redundant more-specific routes, not syntax errors; they are retained to preserve authoritative BGP snapshots and curated profile provenance. Overlap across separate game profiles is allowed.

### Comparison with upstream

Source: `medvedeff-true/ru-gaming-blocklist` tree `66d4da2caa73a1abcddff99b82428b44576fbb3a`. Exact line-set comparison of every matching game file follows. Counts are differences, not approved candidates or new upstream changes. The upstream contains known scraper noise (e.g. `winws.exe`, `services.msc`, private networks, unrelated services, broad cloud ranges); its extra lines were not promoted automatically. Profiles without an upstream counterpart require their own evidence. No claim is made that every upstream-only entry is invalid.

| Profile | Upstream-only entries | Fork-only entries |
| --- | ---: | ---: |
| ApexLegends_RocketLeague.txt | 220 | 0 |
| Arknights.txt | 81 | 3 |
| ArmaReforger.txt | 118 | 0 |
| BattleNet.txt | 121 | 181 |
| Battlefield6.txt | 182 | 0 |
| BlueArchive.txt | 405 | 3 |
| CallOfDuty.txt | no counterpart | — |
| Cloudflare_AWS.txt | 696 | 433 |
| CompanyOfHeroes2.txt | no counterpart | — |
| Darktide.txt | no counterpart | — |
| DeadByDaylight.txt | 248 | 0 |
| EA_Origin.txt | 130 | 1 |
| EpicGames_Fortnite.txt | 251 | 0 |
| Fallout76_AWS.txt | no counterpart | — |
| GearsOfWar.txt | no counterpart | — |
| GooseGooseDuck.txt | 1 | 1 |
| LeagueOfLegends.txt | 1081 | 6 |
| MagicTheGathering.txt | no counterpart | — |
| Minecraft_Extra.txt | 196 | 0 |
| MortalKombat1.txt | 0 | 12 |
| MortalKombat11.txt | no counterpart | — |
| OutlastTrials.txt | no counterpart | — |
| PhotonEngine.txt | 8 | 0 |
| RiotGames_Valorant.txt | 328 | 0 |
| Roblox.txt | 408 | 35 |
| Steam.txt | 791 | 64 |
| StreetFighter6.txt | no counterpart | — |
| Ubisoft_Rainbow_Six_Siege.txt | 334 | 0 |
| VRChat.txt | 63 | 0 |
| Wardogs.txt | no counterpart | — |
| Warframe.txt | 13738 | 9 |
| WutheringWaves.txt | 71 | 9 |

The 13 review-only profiles remain structurally audited, but their complete live endpoint coverage is unverified without fresh game traffic captures. Provider ownership and successful DNS alone do not prove a Russian ISP blocks an endpoint or that the endpoint serves a particular game.
