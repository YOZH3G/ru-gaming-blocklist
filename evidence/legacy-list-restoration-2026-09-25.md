# Legacy game list restoration — 2026-09-25

This pass restores three names that existed in `sources.json -> game_map` but no longer had matching files in `games/`.

The restored lists follow the same evidence-based, action-neutral policy as the rest of the repository.

## Fallout76_AWS

Production entries:

- `api.bethesda.net`
- `bethesda.net`
- `fallout.bethesda.net`

Evidence:

- Bethesda still requires a Bethesda.net account for live titles such as Fallout 76:
  https://help.bethesda.net/app/answers/detail/a_id/55114/
- Fallout 76's current official site and seasons/news remain under `fallout.bethesda.net`:
  https://fallout.bethesda.net/en/seasons
- Bethesda's API remains a live service endpoint in 2026; network-routing failures to `api.bethesda.net` are still reported by Bethesda titles, and prior routing reports explicitly identified it as affecting Fallout 76:
  https://github.com/zhovner/zaborona_help/issues/427

Not restored:

- generic `amazonaws.com`, S3 roots or arbitrary AWS IP space — those belong in the opt-in `Cloudflare_AWS.txt` profile;
- `fallout76.com` — historical upstream entry, but not sufficiently useful/current to justify production inclusion.

The filename `Fallout76_AWS.txt` is kept for compatibility with the existing `game_map` key even though the restored precision list does not contain broad AWS roots.

## GearsOfWar

Production entries:

- `gearsofwar.com`
- `xboxlive.com`
- `xbox.com`

Evidence:

- The current official Gears service/status site is under `gearsofwar.com`:
  https://status.gearsofwar.com/
- Gears of War: E-Day uses Xbox services for online/multiplayer/account features; the current official beta FAQ references Xbox Live network requirements:
  https://www.gearsofwar.com/en-us/news/openbeta/
- Microsoft's current GDK documentation identifies `*.xboxlive.com` and `*.xbox.com` as required Xbox service domains:
  https://learn.microsoft.com/en-us/gaming/gdk/docs/gdk-dev/console-dev/dev-kits/settings/configure-dev-network

Not restored:

- broad `microsoft.com`, `bing.com` or `akamai.net` roots;
- static/dynamic Xbox IP ranges without Gears-specific evidence.

## MagicTheGathering

Production entries:

- `magic-the-gathering-arena.com`
- `magic.wizards.com`
- `mtgarena.com`
- `mtgarena.downloads.wizards.com`
- `wizards.com`

Evidence:

- Wizards' current official MTG Arena page:
  https://magic.wizards.com/en/mtgarena
- Wizards support currently distributes the Windows installer from `mtgarena.downloads.wizards.com`:
  https://mtgarena-support.wizards.com/hc/en-us/articles/360053494251-Installer-prompts-you-to-install-the-game-to-a-drive-you-no-longer-have
- A January 2026 Russian routing report states that wildcard-routing `magic-the-gathering-arena.com`, `wizards.com`, and `mtgarena.com` through VPN restored MTGA connectivity:
  https://github.com/Flowseal/zapret-discord-youtube/discussions/2763
- Historical client logs identify `*.magic-the-gathering-arena.com` as the live game/match front-door namespace and `assets.mtgarena.wizards.com` as an asset endpoint:
  https://farewell-ladmin.com/investigating-and-mitigating-mtg-arena-network-errors/

No Azure IPs are promoted: the historical front-door hosts resolved to Azure and those addresses are infrastructure-dependent and not stable enough for a neutral game list.

## Result

After this restoration, every `game_map` entry again has a matching `games/<name>.txt` file.
