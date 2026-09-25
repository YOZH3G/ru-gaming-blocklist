# Street Fighter 6 and Call of Duty profiles — 2026-09-25

Both profiles follow the repository's evidence-based, action-neutral policy, but they use different update models because their publicly observable infrastructure differs substantially.

## Street Fighter 6

File:

- `games/StreetFighter6.txt`

Mode:

- conservative first-party domain profile;
- no generated IP/CIDR ranges.

Production entries:

- `auth.cid.capcom.com`
- `c.cid.capcom.com`
- `cid.capcom.com`
- `streetfighter.com`
- `www.streetfighter.com`

### Evidence

CAPCOM's own CAPCOM ID service list identifies **Street Fighter 6** as a CAPCOM ID-compatible service for online play and identifies **Buckler's Boot Camp** as its linked web/game service:

- https://c.cid.capcom.com/info/servicelist/en/

The official Street Fighter 6 manual states that a Fighter Account is required for exclusive online content and that creating it requires linking CAPCOM ID to the player's platform account:

- https://game.capcom.com/manual/SF6/en/ps5/page/1/1

The official CAPCOM ID guide uses Street Fighter 6 as its in-game account-linking example:

- https://cid.capcom.com/en/guide/game/connect/

Buckler is hosted on the first-party Street Fighter domain:

- https://www.streetfighter.com/6/buckler/

Public Buckler client tooling observes the CAPCOM authentication hand-off through `auth.cid.capcom.com` before returning to the first-party Buckler service:

- https://github.com/Uncle-Ma11/SF6-Scout/blob/main/docs/live-scout-implementation-plan.md

### Why there are no IP ranges

The available evidence strongly identifies the first-party account/matchmaking/control-plane domains, but does not establish a stable Street Fighter 6-specific ASN or provider range.

Online fights also involve direct player connectivity/matchmaking behavior, so importing generic Capcom/cloud/CDN address space would create false positives without describing a stable SF6 server pool.

Therefore this profile remains domain-only until stronger game-specific network evidence appears.

---

## Call of Duty

File:

- `games/CallOfDuty.txt`

Mode:

- curated first-party/game-specific domains;
- automatically maintained current Demonware AS60229 originated prefixes.

Static domains:

- `activision.com`
- `callofduty.com`
- `cod-assets.cdn.callofduty.com`
- `codm.activision.com`
- `datax.activision.com`
- `demonware.net`
- `prod.demonware.net`
- `s.activision.com`

### Demonware evidence

Activision acquired Demonware specifically for online multiplayer technology and stated that it had already used Demonware in Call of Duty titles:

- https://investor.activision.com/news-releases/news-release-details/activision-set-acquire-demonware

Activision later described Demonware as an integral part of Call of Duty online infrastructure, providing networking, matchmaking, storage and other online services:

- https://blog.activision.com/call-of-duty/archives/a-look-inside-demonware-the-unsung-heroes-powering-your-online-gaming-experience

Demonware's current site describes itself as providing and hosting Activision online services:

- https://www.demonware.net/about

Demonware operates:

- ASN: `AS60229`
- verified IRR as-set: `AS-DEMONWARE`

Source:

- https://www.peeringdb.com/net/20632

The updater replaces the IP/CIDR portion of `CallOfDuty.txt` with the currently visible prefixes originated by AS60229 using RIPEstat, while preserving the curated domains.

### Current Call of Duty domains

Activision currently operates the Call of Duty account/login service at:

- https://s.activision.com/cod/

The game-specific texture/content streaming hostname `cod-assets.cdn.callofduty.com` is independently observed as active Call of Duty infrastructure and is backed by Akamai:

- https://www.netify.ai/resources/hostnames/cod-assets.cdn.callofduty.com
- https://github.com/uklans/cache-domains/blob/master/cod.txt

A Russian Zapret/OpenWrt report also identified `demonware.net`, `prod.demonware.net`, `activision.com`, `datax.activision.com`, and `callofduty.com` as part of the working Call of Duty/Warzone connection set:

- https://github.com/remittor/zapret-openwrt/issues/154

### Scope limitation

AS60229 is Demonware's first-party backend network, but it is **not claimed to be the complete Call of Duty dedicated match-server pool**. Demonware supports multiple Activision titles, and Call of Duty can use third-party hosting/CDN infrastructure.

The profile deliberately does **not** import:

- generic Akamai roots or Akamai address ranges;
- generic CloudFront/AWS/GCP/Azure ranges;
- community-collected Vultr/Choopa/other hosting networks without sufficiently strong game-specific provenance;
- obsolete `codonline.com` infrastructure from the discontinued Call of Duty Online service.

This keeps the list useful and maintainable without turning it into a generic hosting-provider list.

## Aggregates

Street Fighter 6 domains are eligible for `medvedeff-game-list-all.txt`.

Call of Duty domains and current Demonware AS60229 prefixes are eligible for the normal global aggregates because Demonware is first-party Activision gaming infrastructure rather than an arbitrary shared public-cloud region.
