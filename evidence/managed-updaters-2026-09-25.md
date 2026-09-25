# Managed profile updaters — 2026-09-25

This document defines the evidence and update policy for the prioritized automated game/service profiles.

## Source hierarchy

The updater uses three trust levels:

1. **Authoritative replace** — an official provider feed or first-party ASN/BGP data can replace the dynamic IP portion.
2. **Manifest-derived** — a stable official launcher/config endpoint can replace or extend game-specific download/CDN hosts.
3. **Conservative discovery** — official first-party pages are scanned only for approved first-party/game-specific hostnames. Existing evidence-backed entries are retained; arbitrary third-party hosts are not promoted automatically.

The list itself remains action-neutral. Automation describes infrastructure association; it does not decide whether the entry should be bypassed, proxied, blocked, or excluded.

---

## 1. Cloudflare_AWS

Mode: **authoritative replace**

Sources:

- Cloudflare IPv4: https://www.cloudflare.com/ips-v4/
- Cloudflare IPv6: https://www.cloudflare.com/ips-v6/
- AWS: https://ip-ranges.amazonaws.com/ip-ranges.json

AWS dynamic networks are selected when service is:

- `CLOUDFRONT`
- `GLOBALACCELERATOR`

The existing evidence-backed service domains are retained.

This profile stays excluded from both global aggregates because it is intentionally broad shared infrastructure.

---

## 2. Steam

Mode: **authoritative replace for IP/CIDR**

Valve operates AS32590. PeeringDB identifies it as Valve Corporation / Steam and publishes the verified IRR as-set `RADB::AS-VALVE`.

Source:

- https://www.peeringdb.com/net?asn=32590

Current originated routes are retrieved from RIPE RIS/RIPEstat BGP state:

- https://stat.ripe.net/data/bgp-state/data.json?resource=AS32590

Stable Steam/Valve domains remain curated. The IP/CIDR portion is replaced with currently observed AS32590-originated prefixes.

---

## 3. Riot Games: League of Legends and Valorant

Mode: **authoritative BGP-community replace**

Riot officially documents AS6507 purpose communities:

- `6507:8001` — League of Legends
- `6507:8002` — Valorant
- `6507:8003` — Wild Rift

Source:

- https://www.riotgames.com/en/peering-information

RIPEstat BGP state exposes community attributes:

- https://stat.ripe.net/data/bgp-state/data.json?resource=AS6507

The updater selects only AS6507-originated prefixes carrying the relevant purpose community.

Domain cleanup is intentionally conservative:

- obvious `lol.*`, `lolesports.*` and `*.lol.pvp.net` endpoints are removed from the Valorant profile;
- explicit `valorant.*` and `wildrift.*` endpoints are removed from the League profile;
- shared Riot auth/client/CDN/backend endpoints may remain in both.

There is no fallback to "all AS6507 prefixes in both files". If community-aware data disappears, the updater fails instead of broadening the profiles.

---

## 4. Roblox

Mode: **authoritative replace for IP/CIDR**

Roblox operates AS22697 and publishes the verified IRR as-set `AS-ROBLOX`.

Source:

- https://www.peeringdb.com/asn/22697

Current originated routes:

- https://stat.ripe.net/data/bgp-state/data.json?resource=AS22697

The large existing domain set is retained; the network portion is replaced from current AS22697 routing state.

---

## 5. Battle.net / Blizzard

Mode: **authoritative replace for IP/CIDR**

Blizzard operates AS57976 and PeeringDB identifies the verified IRR as-set `RADB::AS-BLIZZARD`. The network description explicitly covers Battle.net and Blizzard game services.

Source:

- https://www.peeringdb.com/net/5886

Current originated routes:

- https://stat.ripe.net/data/bgp-state/data.json?resource=AS57976

Battle.net/Blizzard domains remain curated; current AS57976 prefixes are maintained automatically.

---

## 6. Wuthering Waves

Mode: **manifest-derived**

Stable official Kuro launcher/config endpoint:

- https://prod-alicdn-gamestarter.kurogame.com/launcher/game/G153/50004_obOHXFrFanqsaIEOmuKroCcbZkQRBC7c/index.json

A second known official launcher path is used as a fallback:

- https://prod-alicdn-gamestarter.kurogame.com/pcstarter/prod/game/G153/50004_obOHXFrFanqsaIEOmuKroCcbZkQRBC7c/index.json

The endpoint is used by the official launcher and exposes current download/CDN URLs. Public reverse-engineering references documenting the launcher endpoint include:

- https://gist.github.com/DynamiByte/d839bf9f671c975b6666d0f6e6634641
- https://gist.github.com/DiceTsuki/770b229126354e5167e45ae0d5de3d0c

Only hosts under approved game-specific suffixes are promoted:

- `kurogame.com`
- `kurogames.com`
- `aki-game.net`
- `kurogame-service.com`

Generic provider roots are not imported.

---

## 7. Warframe

Mode: **conservative discovery**

Official sources:

- https://www.warframe.com/download
- https://www.warframe.com/

The updater only discovers first-party hosts under:

- `warframe.com`
- `digitalextremes.com`

Existing evidence-backed `warframe-web-assets.nyc3.cdn.digitaloceanspaces.com` and `wrfr.me` are retained.

Warframe's official Public Export also remains hosted under `content.warframe.com`; this pass does not infer DigitalOcean/Akamai/provider address ranges from it.

---

## 8. Magic: The Gathering Arena

Mode: **conservative discovery**

Official sources:

- https://magic.wizards.com/en/mtgarena/getting-started
- https://mtgarena-support.wizards.com/

The official standalone installer is distributed under:

- `mtgarena.downloads.wizards.com`

Current 2026 client interoperability research identifies the first-party account/auth API:

- `api.platform.wizards.com`
- https://github.com/Ikreb1/mtg-arena-collection-export/blob/main/docs/PROTOCOL.md

Only Wizards/MTGA first-party suffixes are automatically accepted. Azure/shared cloud ranges are not imported.

---

## 9. Blue Archive

Mode: **conservative discovery / verified static set**

Official surfaces:

- https://bluearchive.nexon.com/
- https://forum.nexon.com/bluearchive-en/main

Operational Russian reports in 2026 continue to identify:

- `x-update.ngs.nexon.com`
- `x-init.ngs.nexon.com`
- `public.api.nexon.com`

Source:

- https://github.com/Flowseal/zapret-discord-youtube/discussions/14851

Current-client reverse engineering identifies the game-specific server-config host:

- `d2vaidpni345rp.cloudfront.net`
- https://github.com/cc004/BlueArchiveAPI

The automation uses an explicit allowlist and does not promote arbitrary Nexon/CloudFront hosts found on web pages.

---

## 10. Arknights

Mode: **conservative discovery**

In 2026 Hypergryph introduced an official Arknights PC client using its launcher. Official references:

- https://ak.hypergryph.com/news/0717
- https://ak.hypergryph.com/download

The profile therefore explicitly includes:

- `ak.hypergryph.com`
- `launcher.hypergryph.com`

Discovery is restricted to Hypergryph/Gryphline first-party suffixes already associated with the Arknights ecosystem:

- `hypergryph.com`
- `hg-cdn.com`
- `gryphline.com`

No Bilibili, Tencent ACE, or other third-party provider ranges are generated automatically.

---

## Global aggregates

After the managed profiles are refreshed, `scripts/rebuild_aggregates.py` deterministically rebuilds:

- `medvedeff-game-list-all.txt` from game domains, excluding only the broad auxiliary `Cloudflare_AWS.txt`;
- `medvedeff-game-ipset.txt` from normal game IP/CIDR entries.

The following broad shared/regional AWS profiles are excluded from the global IP aggregate:

- `Cloudflare_AWS.txt`
- `Darktide.txt`
- `Fallout76_AWS.txt`

First-party networks such as Valve AS32590, Riot AS6507 purpose-tagged routes, Roblox AS22697, and Blizzard AS57976 remain eligible for the global IP aggregate.
