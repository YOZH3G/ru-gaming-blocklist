# Mortal Kombat 11 IP-only profile — 2026-10-02

Game: **Mortal Kombat 11** (NetherRealm Studios / Warner Bros. Games).

## Production candidate set

This profile is intentionally IP-only and currently contains five exact IPv4 endpoints:

- `35.170.104.108/32`
- `52.216.163.77/32`
- `72.21.91.29/32`
- `104.18.20.226/32`
- `188.121.36.239/32`

The list is experimental: the first two addresses have direct historical MK11 network observations, while the last three were observed alongside MK11 certificate-validation traffic and are included for field testing after maintainer request.

## Confirmed MK11 backend context

Public MK11 tooling and captured game configuration identify:

- `mk11-api.wbagora.com` — MK11 Hydra/backend API used for authentication, account/game configuration, progression, Krypt/items, store and related online functions.
- `us-east-1-mk11-realtime-1.wbagora.com` — realtime endpoint associated with online fights.

Sources:

- https://github.com/thethiny/Mortal-Kombat-11-Tools
- https://github.com/einyx/pfsense-pihole-blocklist/blob/098df94a42eed5c9b062a78c2e3836130174b1a6/gaming.txt
- https://steamcommunity.com/app/976310/discussions/0/3557193237098000319/

## 35.170.104.108/32

A historical MK11 traffic observation lists this address in the same MK11 network block as WB Insights / WB Agora activity.

The address belongs to Amazon AS14618 and has EC2 reverse-DNS form:
`ec2-35-170-104-108.compute-1.amazonaws.com`.

Sources:

- https://steamcommunity.com/app/976310/discussions/0/3557193237098000319/
- https://ipinfo.io/ips/35.170.104.0/24

Confidence: **higher** among the current IP-only candidates.

## 52.216.163.77/32

The same historical MK11 observation records this address beside the MK11 WB backend/analytics traffic.

`52.216.0.0/16` is Amazon S3 infrastructure and the old MK11 notes explicitly reference `s3.amazonaws.com` for game/EULA-related traffic.

Sources:

- https://steamcommunity.com/app/976310/discussions/0/3557193237098000319/
- https://en.ntunhs.net/IPInfo/EN/52/216.htm

Confidence: **higher**, but the address is shared AWS/S3 infrastructure rather than a WB-owned range.

## Experimental certificate/CDN endpoints

The following three addresses were listed immediately beside the MK11 network block as certificate-related connections. They are not treated as dedicated MK11 servers; they are included because the maintainer wants to test whether routing them together improves reliability.

### 72.21.91.29/32

Current registry data places the address in Edgecast `72.21.80.0/20`. Public reputation/WHOIS sources identify it with legacy certificate revocation infrastructure.

Sources:

- https://www.whois.com/whois/72.21.91.29
- https://www.abuseipdb.com/check/72.21.91.29

Confidence for MK11-specificity: **low**.

### 104.18.20.226/32

Cloudflare AS13335 address. Public reverse-host associations include GlobalSign OCSP/CRL infrastructure, consistent with the certificate-validation context in which it was observed.

Sources:

- https://www.ipaddress.com/ipv4/104.18.20.226
- https://www.whois.com/whois/104.18.20.226

Confidence for MK11-specificity: **low**.

### 188.121.36.239/32

Historically associated with `ocsp.godaddy.com` / Go Daddy Netherlands infrastructure and therefore consistent with an OCSP/certificate check rather than a game backend.

Sources:

- https://superuser.com/questions/121901/is-there-a-way-to-determine-which-service-in-svchost-exe-does-an-outgoing-conn
- https://www.hybrid-analysis.com/search?query=188.121.36.239

Confidence for MK11-specificity: **low**.

## Why no broad CIDR expansion

The realtime hostname contains `us-east-1`, and several observed addresses are AWS-hosted, but that is not enough evidence to add all AWS EC2/S3 space in N. Virginia.

The production candidate therefore keeps exact `/32` entries only. Broad AWS, Cloudflare and Edgecast ranges are deliberately not promoted.

## Field-testing rule

If users report that MK11 works with the first two entries but not without one or more of the certificate/CDN addresses, the corresponding exact `/32` can be promoted from experimental to field-confirmed.

If the last three do not affect connectivity, they should be the first entries removed because they are generic shared certificate/CDN infrastructure.
