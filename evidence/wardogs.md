# WARDOGS endpoint evidence — 2026-09-24

Game: **WARDOGS** (BULKHEAD / Team17, Steam AppID 1867240).

## Production domains

### First-party / official relationship

- `wardogs.com` — official game site.
- `account.wardogs.com` — WARDOGS account/privacy portal.
- `community.wardogs.com` — official game community endpoint.
- `bulkhead.com` — developer.
- `team17.com` — publisher.
- `pragmaengine.com` — Pragma backend platform.
- `firstlook.gg` — FirstLook / Pragma playtest platform.
- `player.gg` — playtest/beta provider referenced by the current WARDOGS privacy policy.
- `anybrain.gg` — anti-cheat/fraud/security provider referenced by the current privacy policy.
- `vivox.com` — voice provider referenced by the current privacy policy.

Official privacy source:
https://www.wardogs.com/privacy

### Operationally observed

- `live.wardogs.bulkhead.pragmaengine.com`
- `api.epicgames.dev`
- `elytra.ac`

The Pragma live endpoint and Epic endpoint repeatedly appear in September 2026 reports from Russian players who restored login/game connectivity through selective routing/Zapret rules.

Operational sources:

- https://steamcommunity.com/app/1867240/discussions/0/562541634873704474/
- https://steamcommunity.com/app/1867240/discussions/0/562541634873690077/
- https://github.com/Flowseal/zapret-discord-youtube/discussions/16983
- https://github.com/max-alekseyev/WarLink/blob/master/games/wardogs-hosts.txt

`elytra.ac` is retained because current game-routing profiles associate Elytra processes/endpoints with WARDOGS. It is not interpreted as “must bypass”; the repository list is action-neutral.

## Production IP/CIDR

### 54.115.0.0/16

Community packet/server observations identify this range as a major WARDOGS match-server pool. The current AWS official feed also identifies `54.115.0.0/16` as a GLOBAL EC2 prefix.

Sources:

- https://gist.github.com/JampireX
- https://ip-ranges.amazonaws.com/ip-ranges.json

### 85.236.96.0/21

A narrower range repeatedly used in working WARDOGS IPSet configurations and overlapping the wider voice/game-hosting range used by specialized WARDOGS routing profiles.

Sources:

- https://github.com/Flowseal/zapret-discord-youtube/discussions/16983
- https://github.com/max-alekseyev/WarLink/blob/master/games/wardogs-hosts.txt

The narrower `/21` is preferred over the broader community `85.236.96.0/19` for the default game list.

## Not promoted

The following broad/shared candidates are deliberately not placed in `Wardogs.txt`:

- generic `amazonaws.com`, CloudFront, Cloudflare and Akamai roots;
- `3.128.0.0/9`, `108.128.0.0/13`, `108.136.0.0/14` and similar broad AWS blocks;
- the wider Vivox/community ranges `108.181.0.0/16`, `195.154.239.0/24`, `45.43.142.0/24` without sufficient endpoint-specific corroboration.

Shared cloud infrastructure can instead be handled by the separate opt-in `Cloudflare_AWS.txt` profile.
