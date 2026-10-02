# WARDOGS endpoint evidence — updated 2026-10-02

Game: **WARDOGS** (BULKHEAD / Team17, Steam AppID 1867240).

## Current production policy: IP-only

As of 2026-10-02, `games/Wardogs.txt` is intentionally an **IP-only** profile.

Maintainer feedback from users showed that the mixed domain + IP profile was unreliable in practice, while routing with the tested IP set worked more consistently. For that reason the production game file now contains exactly the field-tested IP/CIDR set and no domains.

Current production entries:

- `52.50.63.173/32`
- `52.209.230.193/32`
- `52.215.132.236/32`
- `54.73.85.151/32`
- `54.75.198.69/32`
- `54.115.0.0/16`
- `54.247.140.91/32`
- `85.236.96.0/21`
- `99.80.68.196/32`
- `104.18.124.108/32`
- `104.18.125.108/32`
- `108.133.35.6/32`

The profile is deliberately kept stable. The managed updater validates ownership/classification but does not expand the set and does not replace the pinned addresses from DNS.

## AWS EC2 endpoints

The following eight observed addresses belong to Amazon EC2 infrastructure in `eu-west-1` (Ireland):

- `52.50.63.173/32`
- `52.209.230.193/32`
- `52.215.132.236/32`
- `54.73.85.151/32`
- `54.75.198.69/32`
- `54.247.140.91/32`
- `99.80.68.196/32`
- `108.133.35.6/32`

Representative public reverse-DNS/routing evidence:

- `52.209.230.193` → `ec2-52-209-230-193.eu-west-1.compute.amazonaws.com`
- `99.80.68.196` → `ec2-99-80-68-196.eu-west-1.compute.amazonaws.com`

Sources:

- https://ipinfo.io/ips/52.209.230.0/24
- https://ipinfo.io/ips/99.80.68.0/24
- https://en.ntunhs.net/IPInfo/EN/54/247.htm
- https://ar.ntunhs.net/IPInfo/AR/108/133.htm
- https://ip-ranges.amazonaws.com/ip-ranges.json

The updater checks all eight against the current AWS feed and requires:

- `service == EC2`
- `region == eu-west-1`

If AWS reallocates one of these addresses outside that classification, the updater fails closed instead of silently changing the profile.

## Stable network ranges

### 54.115.0.0/16

Community packet/server observations identify this range as a major WARDOGS match-server pool. The AWS feed also identifies the range as EC2 infrastructure.

Sources:

- https://gist.github.com/JampireX
- https://ip-ranges.amazonaws.com/ip-ranges.json

### 85.236.96.0/21

This narrower range repeatedly appears in working WARDOGS IPSet configurations and overlaps the game/voice hosting space used by specialized WARDOGS routing profiles.

Sources:

- https://github.com/Flowseal/zapret-discord-youtube/discussions/16983
- https://github.com/max-alekseyev/WarLink/blob/master/games/wardogs-hosts.txt

The narrower `/21` is retained instead of broader community ranges.

## Pinned Cloudflare endpoints

The two field-tested Cloudflare addresses are:

- `104.18.124.108/32`
- `104.18.125.108/32`

They were originally observed as A records for the WARDOGS dependency `api.epicgames.dev`.

Earlier updater behavior resolved that hostname on each run and replaced the IPs with the current DNS result. That behavior is intentionally removed because the production requirement is now to preserve the tested IP-only set exactly.

The updater only verifies that both pinned addresses remain inside Cloudflare's official IPv4 address space.

Source:

- https://www.cloudflare.com/ips-v4/

## Historical domain evidence

The following domains remain useful as provenance and troubleshooting references, but are **not part of the current WARDOGS production profile**:

- `wardogs.com`
- `account.wardogs.com`
- `community.wardogs.com`
- `bulkhead.com`
- `team17.com`
- `pragmaengine.com`
- `firstlook.gg`
- `player.gg`
- `anybrain.gg`
- `vivox.com`
- `live.wardogs.bulkhead.pragmaengine.com`
- `api.epicgames.dev`
- `elytra.ac`

Historical/operational sources:

- https://www.wardogs.com/privacy
- https://steamcommunity.com/app/1867240/discussions/0/562541634873704474/
- https://steamcommunity.com/app/1867240/discussions/0/562541634873690077/
- https://github.com/Flowseal/zapret-discord-youtube/discussions/16983
- https://github.com/max-alekseyev/WarLink/blob/master/games/wardogs-hosts.txt

`api.epicgames.dev` can still appear in the repository/global domain aggregate through the Epic Games profile. Removing it from `Wardogs.txt` does not imply that the endpoint is unrelated to Epic infrastructure.

## Deliberately not promoted

The WARDOGS production profile does not include:

- full `eu-west-1` EC2 ranges;
- full Cloudflare address space;
- generic `amazonaws.com`, CloudFront, Cloudflare or Akamai roots;
- broad candidates such as `3.128.0.0/9`, `108.128.0.0/13`, `108.136.0.0/14`;
- wider Vivox/community ranges without independent field confirmation.

The purpose of the current profile is operational reliability with the smallest tested set, not exhaustive infrastructure discovery.
