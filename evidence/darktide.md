# Darktide unified profile — 2026-09-25

`games/Darktide.txt` is a single mixed domain + CIDR profile intended for z2k and other consumers that want one selectable Darktide list.

## Why the list is broad

Fatshark runs Warhammer 40,000: Darktide on AWS and uses Amazon GameLift. AWS explicitly documents Darktide as a GameLift/Fatshark customer, and AWS material describes the Darktide architecture as using GameLift and AWS Global Accelerator.

Sources:

- https://aws.amazon.com/gamelift/servers/resources/
- https://aws.amazon.com/blogs/gametech/aws-for-games-updates-from-reinvent-2023/

The Darktide matchmaker/server pool is dynamic. Community troubleshooting and Darktide console-log tooling consistently identify the European AWS regions used for routing/latency selection as:

- `eu-central-1` — Frankfurt
- `eu-north-1` — Stockholm
- `eu-west-2` — London

Sources:

- https://steamcommunity.com/app/1361210/discussions/0/565912359496959668/?ctp=8
- https://github.com/Vansinnet/darktidepingtool

## Generation rule

The CIDR portion is generated from the authoritative AWS feed:

https://ip-ranges.amazonaws.com/ip-ranges.json

Filter:

- `service == EC2`
- `region in {eu-central-1, eu-north-1, eu-west-2}`

Initial snapshot source date:

- AWS `createDate`: `2026-09-25-03-57-06`
- EC2 CIDRs selected: **180**

The repository does not preserve obsolete ranges merely because they appeared in an older Darktide workaround. When AWS removes a prefix from the selected region/service set, the next update removes it from `Darktide.txt`; new prefixes are added automatically.

Updater:

- `scripts/update_darktide_aws.py`
- `.github/workflows/update-darktide-aws.yml`
- scheduled daily and available through `workflow_dispatch`

## Domains

The unified file also keeps stable first-party domains:

- `playdarktide.com`
- `fatshark.se`

Fatshark identifies both as its websites, including in the Darktide/Fatshark privacy material:

https://www.fatshark.se/privacy-policy

## Aggregates

`Darktide.txt` is intentionally a broad game-specific profile.

- its first-party domains may be present in `medvedeff-game-list-all.txt`;
- its regional AWS EC2 CIDRs are **not** copied to `medvedeff-game-ipset.txt`.

This keeps the global IP set precision-oriented while still exposing the complete unified Darktide profile to z2k through `sources.json -> game_map -> Darktide`.
