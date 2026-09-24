# Cloudflare / AWS auxiliary profile — 2026-09-24

`games/Cloudflare_AWS.txt` is intentionally different from the normal per-game lists.

It is a **broad opt-in auxiliary infrastructure profile** for users whose game/service traffic is difficult to identify more narrowly. It may be useful as either an include or an exclude, depending on the consumer.

It is deliberately **not merged** into:

- `medvedeff-game-list-all.txt`
- `medvedeff-game-ipset.txt`

## Included

### Cloudflare

The profile includes the complete current Cloudflare IPv4 and IPv6 ranges published by Cloudflare:

- https://www.cloudflare.com/ips-v4/
- https://www.cloudflare.com/ips-v6/

It also includes provider/service domains used by Cloudflare DNS, WARP, R2, Stream, Tunnel, Workers, Pages and related edge services.

### AWS

AWS ranges are based on the official AWS feed:

- https://ip-ranges.amazonaws.com/ip-ranges.json
- feed createDate at review time: `2026-09-24-02-07-06`

The profile does **not** import all `AMAZON` or `EC2` prefixes. That would effectively route a very large fraction of unrelated Internet services.

Instead it includes:

- CloudFront global edge ranges from the official CloudFront list:
  https://d7uri8nf7uskq.cloudfront.net/tools/list-cloudfront-ips
- selected `GLOBALACCELERATOR` ranges whose region is `GLOBAL`;
- common AWS service domains relevant to game backends and downloads, including S3, EC2 DNS, ELB, API Gateway, Global Accelerator and GameLift.

## Explicitly excluded from the old file

The original upstream `Cloudflare_AWS.txt` mixed provider infrastructure with unrelated websites and scraper artifacts. The rebuilt file excludes, among other things:

- private, loopback, link-local and multicast ranges;
- public DNS addresses merely because they appeared in reports;
- arbitrary one-off EC2 instances;
- YouTube, GitHub, 4PDA, banks, marketplaces and unrelated Russian sites;
- Roblox/Riot/Steam/etc. domains that belong in their own game lists;
- pseudo-domains and filenames such as `winws.exe`, `services.msc`, `stun.bin`;
- stripped URL-encoding artifacts such as `2fcloudflare.com`;
- malformed concatenated hostnames.

## Maintenance rule

This auxiliary file may be broad, but every broad network block must come from an authoritative provider feed or have strong service-specific evidence.

Game-specific observations should normally go to the relevant game file. Shared provider infrastructure belongs here only when the broader profile is intentionally useful.
