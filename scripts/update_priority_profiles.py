from __future__ import annotations

import ipaddress
import json
import re
import socket
from pathlib import Path

from updaters.common import (
    ROOT,
    allowed_host,
    announced_prefixes,
    community_prefixes,
    extract_hosts,
    fetch_json,
    fetch_text,
    split_entries,
    write_mixed,
)

AWS_RANGES = "https://ip-ranges.amazonaws.com/ip-ranges.json"
CF_V4 = "https://www.cloudflare.com/ips-v4/"
CF_V6 = "https://www.cloudflare.com/ips-v6/"

RIOT_VALORANT_EXCLUDES = {
    "euw-red.lol.sgp.pvp.net",
    "euw-red.lol.sgp.pvp.net.cdn.cloudflare.net",
    "euw.red.lol.sgp.pvp.net",
    "feapp.euw1.lol.pvp.net",
    "legacy.lolesports.com",
    "lol.riotgames.com",
    "lol.secure.dyn.riotcdn.net",
    "lolesports.com",
    "lolstatic-a.akamaihd.net",
}
RIOT_LOL_EXCLUDES = {
    "valorant.scd.riotcdn.net",
    "valorant.secure.dyn.riotcdn.net",
    "wildrift.secure.dyn.riotcdn.net",
}
RIOT_LOL_FORCE = {
    "legacy.lolesports.com",
    "lolesports.com",
}

WUWA_INDEXES = (
    "https://prod-alicdn-gamestarter.kurogame.com/launcher/game/G153/50004_obOHXFrFanqsaIEOmuKroCcbZkQRBC7c/index.json",
    "https://prod-alicdn-gamestarter.kurogame.com/pcstarter/prod/game/G153/50004_obOHXFrFanqsaIEOmuKroCcbZkQRBC7c/index.json",
)
WUWA_STATIC = {
    "kurogame-service.com",
    "kurogames.com",
    "mc.kurogames.com",
    "prod-alicdn-gamestarter.kurogame.com",
    "wutheringwaves.kurogames.com",
}
WUWA_SUFFIXES = ("kurogame.com", "kurogames.com", "aki-game.net", "kurogame-service.com")

WARFRAME_SOURCES = (
    "https://www.warframe.com/download",
    "https://www.warframe.com/",
)
WARFRAME_SUFFIXES = ("warframe.com", "digitalextremes.com")
WARFRAME_EXTRA_ALLOWED = {"warframe-web-assets.nyc3.cdn.digitaloceanspaces.com", "wrfr.me"}

MTGA_SOURCES = (
    "https://magic.wizards.com/en/mtgarena/getting-started",
    "https://mtgarena-support.wizards.com/",
)
MTGA_ALLOWED = {
    "api.platform.wizards.com",
    "magic-the-gathering-arena.com",
    "magic.wizards.com",
    "mtgarena-support.wizards.com",
    "mtgarena.com",
    "mtgarena.downloads.wizards.com",
    "wizards.com",
}

BLUE_ARCHIVE_SOURCES = (
    "https://bluearchive.nexon.com/",
    "https://forum.nexon.com/bluearchive-en/main",
)
BLUE_ARCHIVE_ALLOWED = {
    "bluearchive.com",
    "bluearchive.jp",
    "bluearchive.nexon.com",
    "nexon.com",
    "nxm-clw-cdn.dn.nexoncdn.co.kr",
    "public.api.nexon.com",
    "x-init.ngs.nexon.com",
    "x-update.ngs.nexon.com",
    "d2vaidpni345rp.cloudfront.net",
}

ARKNIGHTS_SOURCES = (
    "https://ak.hypergryph.com/download",
    "https://ak.hypergryph.com/news/0717",
)
ARKNIGHTS_SUFFIXES = ("hypergryph.com", "hg-cdn.com", "gryphline.com")

SF6_SOURCES = (
    "https://www.streetfighter.com/6/",
    "https://c.cid.capcom.com/info/servicelist/en/",
    "https://cid.capcom.com/en/guide/game/connect/",
)
SF6_ALLOWED = {
    "auth.cid.capcom.com",
    "c.cid.capcom.com",
    "cid.capcom.com",
    "streetfighter.com",
    "www.streetfighter.com",
}

COH2_SUPPORT_API = "https://help.relic.com/api/v2/help_center/en-us/articles/36080656057363.json"
COH2_STATIC_DOMAINS = {
    "coh2-api.reliclink.com",
    "coh2-lobby.reliclink.com",
    "coh2.lobby.reliclink.com",
    "companyofheroes.com",
    "compute-1.amazonaws.com",
    "eu-central-1.compute.amazonaws.com",
    "garry.sgaas.net",
    "ingame.companyofheroes.com",
    "sso.relic.com",
}

COH2_BROAD_EXTRA_DOMAINS = {"amazonaws.com"}
COH2_BROAD_EXTRA_NETWORKS = {
    "3.70.251.0/24",
    "3.73.152.0/24",
    "3.91.171.0/24",
    "3.227.250.0/24",
    "3.230.230.0/24",
    "18.207.66.0/24",
    "44.220.67.0/24",
    "54.237.64.0/24",
    "146.66.152.0/24",
}

WARDOGS_OBSERVED_AWS_EU_WEST_1 = {
    "52.50.63.173",
    "52.209.230.193",
    "52.215.132.236",
    "54.73.85.151",
    "54.75.198.69",
    "54.247.140.91",
    "99.80.68.196",
    "108.133.35.6",
}
WARDOGS_STATIC_NETWORKS = {
    "54.115.0.0/16",
    "85.236.96.0/21",
}
WARDOGS_CLOUDFLARE_HOST = "api.epicgames.dev"


def update_cloudflare_aws() -> str:
    path = ROOT / "games" / "Cloudflare_AWS.txt"
    domains, _ = split_entries(path)

    networks = set(fetch_text(CF_V4).split()) | set(fetch_text(CF_V6).split())
    aws = fetch_json(AWS_RANGES)
    for item in aws.get("prefixes", []):
        if item.get("service") in {"CLOUDFRONT", "GLOBALACCELERATOR"} and item.get("ip_prefix"):
            networks.add(item["ip_prefix"])
    for item in aws.get("ipv6_prefixes", []):
        if item.get("service") in {"CLOUDFRONT", "GLOBALACCELERATOR"} and item.get("ipv6_prefix"):
            networks.add(item["ipv6_prefix"])

    changed = write_mixed(path, domains, networks)
    return f"Cloudflare_AWS: {len(domains)} domains + {len(networks)} networks ({'changed' if changed else 'current'})"


def update_asn_profile(filename: str, asn: int) -> str:
    path = ROOT / "games" / filename
    domains, _ = split_entries(path)
    networks = announced_prefixes(asn)
    changed = write_mixed(path, domains, networks)
    return f"{filename}: AS{asn}, {len(domains)} domains + {len(networks)} prefixes ({'changed' if changed else 'current'})"


def update_riot() -> list[str]:
    valorant_path = ROOT / "games" / "RiotGames_Valorant.txt"
    lol_path = ROOT / "games" / "LeagueOfLegends.txt"

    valorant_domains, _ = split_entries(valorant_path)
    lol_domains, _ = split_entries(lol_path)

    valorant_domains = [d for d in valorant_domains if d not in RIOT_VALORANT_EXCLUDES]
    lol_domains = [d for d in lol_domains if d not in RIOT_LOL_EXCLUDES]
    lol_domains = sorted(set(lol_domains) | RIOT_LOL_FORCE)

    valorant_prefixes = community_prefixes(6507, "6507:8002")
    lol_prefixes = community_prefixes(6507, "6507:8001")

    v_changed = write_mixed(valorant_path, valorant_domains, valorant_prefixes)
    l_changed = write_mixed(lol_path, lol_domains, lol_prefixes)

    return [
        f"RiotGames_Valorant: community 6507:8002, {len(valorant_domains)} domains + {len(valorant_prefixes)} prefixes ({'changed' if v_changed else 'current'})",
        f"LeagueOfLegends: community 6507:8001, {len(lol_domains)} domains + {len(lol_prefixes)} prefixes ({'changed' if l_changed else 'current'})",
    ]


def update_wuthering_waves() -> str:
    path = ROOT / "games" / "WutheringWaves.txt"
    discovered = set()
    successes = 0
    for url in WUWA_INDEXES:
        try:
            payload = fetch_json(url)
        except Exception as exc:
            print(f"WARN: Wuthering Waves source failed: {url}: {exc}")
            continue
        successes += 1
        discovered |= {h for h in extract_hosts(payload) if allowed_host(h, WUWA_SUFFIXES)}

    if successes == 0:
        raise RuntimeError("All Wuthering Waves launcher endpoints failed")
    if not discovered:
        raise RuntimeError("Wuthering Waves launcher returned no approved hosts")

    domains = WUWA_STATIC | discovered
    changed = write_mixed(path, domains, [])
    return f"WutheringWaves: {len(domains)} manifest-derived/stable domains ({'changed' if changed else 'current'})"


def update_company_of_heroes_2() -> str:
    path = ROOT / "games" / "CompanyOfHeroes2.txt"
    payload = fetch_json(COH2_SUPPORT_API, timeout=20)
    article = payload.get("article") or {}
    text = article.get("body") or ""

    if not text:
        raise RuntimeError("Relic Help Center API returned no CoH2 article body")

    # Strip HTML tags/whitespace so the check is resilient to Zendesk markup.
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)

    match = re.search(
        r"BattleServer\s+IP[^0-9]*((?:\d{1,3}\.){3}\d{1,3})",
        text,
        flags=re.IGNORECASE,
    )
    if not match:
        raise RuntimeError("Relic support page did not expose a CoH2 BattleServer IP")

    ip = match.group(1)
    try:
        address = ipaddress.ip_address(ip)
    except ValueError as exc:
        raise RuntimeError(f"Invalid CoH2 BattleServer IP from Relic support: {ip}") from exc

    if address.version != 4 or not address.is_global:
        raise RuntimeError(f"Unsafe CoH2 BattleServer IP from Relic support: {ip}")

    if "coh2-lobby.reliclink.com" not in text:
        raise RuntimeError("Relic support page no longer references coh2-lobby.reliclink.com")

    networks = {f"{ip}/32"}
    changed = write_mixed(path, COH2_STATIC_DOMAINS, networks)
    broad_changed = write_mixed(
        ROOT / "games" / "CompanyOfHeroes2_Broad.txt",
        COH2_STATIC_DOMAINS | COH2_BROAD_EXTRA_DOMAINS,
        networks | COH2_BROAD_EXTRA_NETWORKS,
    )
    return (
        f"CompanyOfHeroes2: {len(COH2_STATIC_DOMAINS)} domains + "
        f"{len(networks)} Relic-published BattleServer IP ({'changed' if changed else 'current'}); "
        f"broad profile {'changed' if broad_changed else 'current'}"
    )


def update_wardogs() -> str:
    path = ROOT / "games" / "Wardogs.txt"
    domains, _ = split_entries(path)

    aws = fetch_json(AWS_RANGES)
    aws_prefixes = [
        ipaddress.ip_network(item["ip_prefix"], strict=False)
        for item in aws.get("prefixes", [])
        if item.get("service") == "EC2"
        and item.get("region") == "eu-west-1"
        and item.get("ip_prefix")
    ]

    if not aws_prefixes:
        raise RuntimeError("AWS feed returned no eu-west-1 EC2 prefixes for WARDOGS validation")

    observed_networks = set()
    for value in sorted(WARDOGS_OBSERVED_AWS_EU_WEST_1):
        address = ipaddress.ip_address(value)
        if not any(address in prefix for prefix in aws_prefixes):
            raise RuntimeError(
                f"Observed WARDOGS endpoint {value} is no longer in AWS EC2 eu-west-1"
            )
        observed_networks.add(f"{value}/32")

    cf_prefixes = [
        ipaddress.ip_network(value, strict=False)
        for value in fetch_text(CF_V4).split()
    ]

    resolved = {
        item[4][0]
        for item in socket.getaddrinfo(
            WARDOGS_CLOUDFLARE_HOST,
            443,
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
        )
    }
    if not resolved:
        raise RuntimeError(f"DNS returned no IPv4 addresses for {WARDOGS_CLOUDFLARE_HOST}")

    cloudflare_networks = set()
    for value in resolved:
        address = ipaddress.ip_address(value)
        if not address.is_global or not any(address in prefix for prefix in cf_prefixes):
            raise RuntimeError(
                f"{WARDOGS_CLOUDFLARE_HOST} resolved outside official Cloudflare IPv4 space: {value}"
            )
        cloudflare_networks.add(f"{value}/32")

    networks = WARDOGS_STATIC_NETWORKS | observed_networks | cloudflare_networks
    changed = write_mixed(path, domains, networks)
    return (
        f"Wardogs: {len(domains)} domains + {len(networks)} networks "
        f"({len(observed_networks)} observed AWS eu-west-1 /32 + "
        f"{len(cloudflare_networks)} live Epic API Cloudflare /32) "
        f"({'changed' if changed else 'current'})"
    )


def update_conservative_domains(
    filename: str,
    urls: tuple[str, ...],
    suffixes: tuple[str, ...] = (),
    exact_allowed: set[str] | None = None,
    always_add: set[str] | None = None,
) -> str:
    path = ROOT / "games" / filename
    domains, networks = split_entries(path)
    result = set(domains)
    result |= always_add or set()

    successes = 0
    for url in urls:
        try:
            text = fetch_text(url, timeout=15)
        except Exception as exc:
            print(f"WARN: {filename} source failed: {url}: {exc}")
            continue
        successes += 1
        for host in extract_hosts(text):
            if exact_allowed is not None and host in exact_allowed:
                result.add(host)
            elif suffixes and allowed_host(host, suffixes):
                result.add(host)

    if successes == 0:
        raise RuntimeError(f"All authoritative/discovery sources failed for {filename}")

    changed = write_mixed(path, result, networks)
    return f"{filename}: {len(result)} conservative domains ({'changed' if changed else 'current'})"


def main() -> int:
    status = []

    # 1. Broad provider profile: authoritative provider feeds.
    status.append(update_cloudflare_aws())

    # 2. Valve-owned routing space.
    status.append(update_asn_profile("Steam.txt", 32590))

    # 3. Riot purpose communities: League and Valorant stay separate.
    status.extend(update_riot())

    # 4. Roblox-owned routing space.
    status.append(update_asn_profile("Roblox.txt", 22697))

    # 5. Blizzard-owned routing space.
    status.append(update_asn_profile("BattleNet.txt", 57976))

    # 6. Official launcher manifests.
    status.append(update_wuthering_waves())

    # 7. Warframe: official first-party pages only; no broad CDN/ASN guessing.
    status.append(update_conservative_domains(
        "Warframe.txt",
        WARFRAME_SOURCES,
        suffixes=WARFRAME_SUFFIXES,
        always_add=WARFRAME_EXTRA_ALLOWED,
    ))

    # 8. MTGA: official Wizards surfaces + a current first-party platform API host.
    status.append(update_conservative_domains(
        "MagicTheGathering.txt",
        MTGA_SOURCES,
        exact_allowed=MTGA_ALLOWED,
        always_add=MTGA_ALLOWED,
    ))

    # 9. Blue Archive: retain the verified NGS/Nexon set and one game-specific config CDN.
    status.append(update_conservative_domains(
        "BlueArchive.txt",
        BLUE_ARCHIVE_SOURCES,
        exact_allowed=BLUE_ARCHIVE_ALLOWED,
        always_add=BLUE_ARCHIVE_ALLOWED,
    ))

    # 10. Arknights: follow official Hypergryph PC launcher surfaces conservatively.
    status.append(update_conservative_domains(
        "Arknights.txt",
        ARKNIGHTS_SOURCES,
        suffixes=ARKNIGHTS_SUFFIXES,
        always_add={"ak.hypergryph.com", "launcher.hypergryph.com"},
    ))

    # Street Fighter 6: first-party control-plane only. No broad Capcom/cloud IP inference.
    status.append(update_conservative_domains(
        "StreetFighter6.txt",
        SF6_SOURCES,
        exact_allowed=SF6_ALLOWED,
        always_add=SF6_ALLOWED,
    ))

    # Call of Duty: Demonware is Activision's first-party online backend.
    # Keep curated CoD domains and replace the dynamic IP portion with current AS60229 routes.
    status.append(update_asn_profile("CallOfDuty.txt", 60229))

    # Company of Heroes 2: official Relic support publishes a mutable BattleServer IP.
    # Refresh exactly that /32 and keep only first-party RelicLink/Relic Account domains.
    status.append(update_company_of_heroes_2())

    # WARDOGS: retain narrow observed server endpoints.
    # Validate reported AWS addresses against the official eu-west-1 EC2 feed and
    # refresh api.epicgames.dev's current Cloudflare A records daily.
    status.append(update_wardogs())

    print("\n".join(status))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())