# The Outlast Trials broad routing profile — 2026-10-05

Game: **The Outlast Trials** (Red Barrels).

## Profile type

`games/OutlastTrials.txt` is intentionally a **broad, opt-in game profile**.

It is not suitable for inclusion in the repository-wide domain/IP aggregates because it contains:

- large AWS regional CIDRs, including prefixes broader than `/16`;
- generic infrastructure roots such as `amazonaws.com` and `cloudfront.net`;
- shared CDN networks from Cloudflare and Akamai.

For that reason the entire profile is excluded from both:

- `medvedeff-game-list-all.txt`
- `medvedeff-game-ipset.txt`

Consumers should enable `OutlastTrials.txt` only when they explicitly want The Outlast Trials routing profile.

## Why AWS is relevant

Amazon Web Services publicly documents Red Barrels as an AWS / Amazon GameLift customer and specifically states that Red Barrels used AWS to manage game servers for The Outlast Trials.

Sources:

- https://aws.amazon.com/blogs/gametech/aws-for-games-at-unreal-fest-2023/
- https://aws.amazon.com/gamelift/servers/

A community troubleshooting case for The Outlast Trials Asia also reports that adding missing Amazon AWS IP ranges fixed connectivity to Korea/Singapore servers:

- https://forums.mudfish.net/t/please-add-this-new-item-the-outlast-trials-asia-thank-you-very-much/69198

Historical player reports list multiple regions including US West/East, Europe Central, Asia Pacific Northeast/Southeast, Middle East South and Oceania:

- https://steamcommunity.com/app/1304930/discussions/0/3832045251559480937/

These sources support the use of multi-region AWS infrastructure, but they do not independently prove every individual CIDR below. The exact profile contents are maintainer-supplied routing candidates intended for field testing.

## Domains

The profile contains:

- `rbg-services.com`
- `cloudfront.net`
- `amazonaws.com`
- `akamaitechnologies.com`

`rbg-services.com` is retained as the game-specific candidate supplied by the maintainer.

The other three are broad provider roots and must not be interpreted as Outlast-exclusive infrastructure.

## AWS / cloud CIDRs

Maintainer-supplied candidate ranges:

- `3.24.0.0/14`
- `3.38.0.0/15`
- `3.80.0.0/12`
- `3.120.0.0/14`
- `13.228.0.0/15`
- `18.192.0.0/13`
- `18.228.0.0/14`
- `23.20.0.0/14`
- `35.156.0.0/14`
- `35.160.0.0/13`
- `52.4.0.0/14`
- `52.28.0.0/14`
- `54.64.0.0/11`
- `54.93.0.0/16`
- `54.96.0.0/12`
- `54.112.0.0/12`
- `92.122.0.0/16`
- `104.16.0.0/12`
- `184.72.0.0/15`

The duplicate `3.120.0.0/14` from the supplied list is stored only once.

## Shared CDN ranges

### 104.16.0.0/12

This is allocated to Cloudflare. Cloudflare currently publishes narrower operational IPv4 prefixes inside this allocation, so the `/12` is deliberately treated as a broad routing candidate rather than a precise current Cloudflare service-prefix list.

Sources:

- https://www.cloudflare.com/ips/
- https://www.whois.com/whois/104.16.0.0

### 92.122.0.0/16

This space is associated with Akamai infrastructure and is similarly shared across many unrelated services.

Sources:

- https://ipinfo.io/ips/92.122.0.0/16
- https://techdocs.akamai.com/origin-ip-acl/docs/update-your-origin-server

## Safety / false-positive policy

This profile intentionally trades precision for coverage. It must remain isolated from global aggregates.

If field reports later identify exact server IPs or narrower GameLift/AWS prefixes, those should be preferred and the profile can be reduced accordingly.
