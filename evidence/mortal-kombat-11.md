# Mortal Kombat 11 routing profile — updated 2026-10-06

Game: **Mortal Kombat 11** (NetherRealm Studios / Warner Bros. Games).

## Current policy

The original five-IP test profile was not sufficient for some users. MK11 uses WB Hydra / Agora / Insights services by hostname, and those services are cloud-hosted and may rotate addresses.

The profile is therefore now **mixed domain + IP**:

- stable WB/MK11 service domains are kept explicitly;
- the five historical test `/32` addresses are retained;
- the managed updater resolves the current IPv4 A records for the strongest backend hostnames and writes them as exact `/32` entries on every managed refresh.

This avoids promoting all AWS `us-east-1`, Cloudflare or other shared provider ranges.

## MK11-specific backend

Strong MK11 evidence identifies:

- `mk11-api.wbagora.com` — Hydra API: authentication, configuration, account/progression, Krypt/items, store and other online functions;
- `us-east-1-mk11-realtime-1.wbagora.com` — online-fight realtime endpoint;
- `event.wbinsights.com` — WB Insights event/heartbeat service;
- `int-api.wbagora.com`;
- `next-api.wbagora.com`.

Historical MK11 traffic source:

- https://steamcommunity.com/app/976310/discussions/0/3557193237098000319/

Independent MK11 tooling continues to use `mk11-api.wbagora.com` as the service base URL:

- https://github.com/thethiny/Mortal-Kombat-11-Tools
- https://www.mksecrets.net/forums/eng/viewtopic.php?t=47278

## WB account/control-plane additions

The profile also includes the current WB control-plane family used by Mortal Kombat / WB titles:

- `account.wbgames.com`
- `api.wbgames.com`
- `wb-hydra.wbgames.com`
- `prod-network-api.wbagora.com`
- `telemetry.wbgames.com`
- `cdn.wbgames.com`
- `wbagora.com`
- `wbinsights.com`
- `wbgames.com`
- `warnerbrosgames.com`
- `mortalkombat.com`
- `mk11.mortalkombat.com`

Why this is justified:

- multiple MK11 users reported that creating/linking a WB Games account through `account.wbgames.com` or the MK11 Mortal Kombat site restored online/store functionality;
- modern WB routing work for MK1 uses the same WB Agora/WB Games control-plane family, including `prod-network-api.wbagora.com`, `account.wbgames.com`, `api.wbgames.com`, `wb-hydra.wbgames.com`, `telemetry.wbgames.com` and `cdn.wbgames.com`.

Sources:

- https://steamcommunity.com/app/976310/discussions/0/3801650156490708364/
- https://steamcommunity.com/app/976310/discussions/0/3801650561758093134/
- https://forums.gamemag.ru/topic/132893-%D0%BE%D0%B1%D1%85%D0%BE%D0%B4-%D0%B1%D0%BB%D0%BE%D0%BA%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D0%B8-%D1%81%D0%B5%D1%80%D1%8B%D1%85-xbox-%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%BE%D0%B2-mk1-%D0%B8-%D0%BD%D0%B5-%D1%82%D0%BE%D0%BB%D1%8C%D0%BA%D0%BE/

## event.wbinsights.com is not safely optional

A 2026 false-positive report against a DNS blocklist found that blocking `event.wbinsights.com` broke events, rewards, purchases and in some cases startup behavior in several WB games. The report was accepted as an allow-list case.

Source:

- https://github.com/hagezi/dns-blocklists/issues/9755

For MK11 this strengthens the older observation that `event.wbinsights.com` should be routed with the WB backend instead of treated as disposable analytics.

## Managed current-IP refresh

The updater resolves these exact hosts daily:

- `event.wbinsights.com`
- `int-api.wbagora.com`
- `mk11-api.wbagora.com`
- `next-api.wbagora.com`
- `prod-network-api.wbagora.com`
- `us-east-1-mk11-realtime-1.wbagora.com`

Only global IPv4 A records are accepted and written as exact `/32` entries.

`account.wbgames.com` is deliberately **domain-only**: repeated CI runs returned different CloudFront edge pools (`18.238.109.*` and then `13.226.251.*`). Pinning those shared CDN A-records would create noisy churn and route unrelated CloudFront traffic.

The six managed backend hosts were stable across repeated test runs. On 2026-10-06 they resolved to:

- `event.wbinsights.com` → `35.169.33.137/32`, `44.213.188.14/32`, `100.51.63.52/32`
- `int-api.wbagora.com` → `52.207.74.15/32`, `98.88.126.132/32`
- `mk11-api.wbagora.com` → `54.237.169.75/32`, `100.49.182.94/32`
- `next-api.wbagora.com` → `98.85.83.96/32`, `98.91.61.235/32`
- `prod-network-api.wbagora.com` → `32.196.168.103/32`, `184.195.76.76/32`
- `us-east-1-mk11-realtime-1.wbagora.com` → `18.205.98.8/32`

DNS failure for one hostname is tolerated because individual WB hosts may be retired or temporarily unavailable. The updater fails closed only if none of the managed hosts resolves.

## Historical pinned addresses

The earlier field-test addresses are retained:

- `35.170.104.108/32`
- `52.216.163.77/32`
- `72.21.91.29/32`
- `104.18.20.226/32`
- `188.121.36.239/32`

The first two were observed directly around MK11 WB traffic. The last three were certificate/CDN/OCSP-side candidates and remain lower-confidence.

## Why no full AWS region

The realtime hostname explicitly contains `us-east-1`, but routing all EC2/S3 in that region would capture a very large amount of unrelated traffic.

The managed exact-host resolution provides current cloud IPs without promoting the entire AWS region.

## Important non-routing failure mode

Not every MK11 "server connection" error is a routing problem.

Several 2024–2025 reports indicate that repairing the Windows root certificate store restored MK11 online access even when VPN/account-linking changes did not. If the expanded routing profile still fails on a Windows PC, certificate-store health should be checked before adding progressively broader cloud ranges.

Sources:

- https://steamcommunity.com/app/976310/discussions/0/3821909708334611396/
- https://steamcommunity.com/app/976310/discussions/0/597414091753083517/
