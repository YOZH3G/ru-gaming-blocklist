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

## Field-confirmed endpoint expansion — 2026-09-26

A maintainer-supplied user report confirmed that extending the WARDOGS routing list with the following addresses restored/improved connectivity:

- `52.215.132.236/32`
- `54.73.85.151/32`
- `54.247.140.91/32`
- `54.75.198.69/32`
- `52.209.230.193/32`
- `99.80.68.196/32`
- `52.50.63.173/32`
- `108.133.35.6/32`
- `104.18.124.108/32`
- `104.18.125.108/32`

### AWS pattern

The eight addresses in the `52.*`, `54.*`, `99.80.*`, and `108.133.*` groups all map to Amazon EC2 infrastructure in `eu-west-1` (Ireland).

Representative public reverse-DNS/routing evidence:

- `52.209.230.193` → `ec2-52-209-230-193.eu-west-1.compute.amazonaws.com`
- `99.80.68.196` → `ec2-99-80-68-196.eu-west-1.compute.amazonaws.com`
- `54.247.140.91` is inside the `54.247.0.0/16` EC2 Ireland space
- `108.133.35.6` is inside the `108.133.0.0/16` EC2 Ireland space

Sources:

- https://ipinfo.io/ips/52.209.230.0/24
- https://ipinfo.io/ips/99.80.68.0/24
- https://en.ntunhs.net/IPInfo/EN/54/247.htm
- https://ar.ntunhs.net/IPInfo/AR/108/133.htm

The managed updater additionally validates all eight reported addresses against the current official AWS `ip-ranges.json` feed and requires them to remain in:

- `service == EC2`
- `region == eu-west-1`

If AWS reallocates any of them outside that classification, the updater fails closed instead of silently preserving stale attribution.

This is strong evidence that WARDOGS currently uses a rotating/dynamic EC2 presence in Ireland, but one operational report is not yet enough to promote the entire `eu-west-1` EC2 region into the production profile. The exact observed `/32` entries are therefore preferred for now.

### Epic API / Cloudflare

The remaining two addresses:

- `104.18.124.108`
- `104.18.125.108`

are the current A records for the already-listed WARDOGS dependency `api.epicgames.dev`.

The hostname is Cloudflare-fronted:

- https://www.ipaddress.com/website/api.epicgames.dev/

The updater therefore does not hard-code these two addresses permanently. On every managed refresh it:

1. resolves `api.epicgames.dev` to IPv4;
2. verifies every returned address is inside Cloudflare's official IPv4 ranges;
3. writes the current A records as `/32` entries.

This keeps IP-only routing consumers functional without promoting the entire Cloudflare address space into the normal WARDOGS profile.

## Promotion threshold for broad eu-west-1

If independent future reports show that WARDOGS repeatedly rotates across substantially more unrelated EC2 `eu-west-1` addresses, the next logical step is to treat WARDOGS like Darktide/Fallout 76 and make its AWS portion an automatically generated game-specific regional profile.

Until then, the exact field-confirmed endpoints remain the lower-false-positive choice.
