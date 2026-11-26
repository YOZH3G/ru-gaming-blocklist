from __future__ import annotations

import gzip
import ipaddress
import json
import re
import urllib.request
from datetime import datetime, timedelta, timezone
from urllib.parse import quote
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
UA = "ru-gaming-blocklist-updater/1.0"


# Reviewed zones and backend names whose descendants belong in each profile.
WILDCARD_ZONES = {
    "ApexLegends_RocketLeague": "apexlegends.com playapex.com ea.com rocketleague.com",
    "Arknights": "gryphline.com hg-cdn.com biligame.com",
    "ArmaReforger": "armaplatform.com armareforgerplatform.com bistudio.com",
    "BattleNet": "battle.net battlenet.com blizzard.com blizzard.cn blzstatic.cn",
    "Battlefield6": "battlefield.com battlefield6.com ea.com dice.se",
    "BlueArchive": "bluearchive.com bluearchive.jp nexon.com",
    "CallOfDuty": "callofduty.com demonware.net activision.com",
    "Cloudflare_AWS": "amazonaws.com amazonaws.cn awsglobalaccelerator.com cloudfront.net elasticloadbalancing.com on.aws cloudflare.com cloudflare.net cloudflareclient.com trycloudflare.com workers.dev pages.dev",
    "CompanyOfHeroes2": "companyofheroes.com",
    "Darktide": "fatshark.se playdarktide.com",
    "DeadByDaylight": "bhvrdbd.com bhvrdbd.net deadbydaylight.com",
    "EA_Origin": "ea.app ea.com origin.com",
    "EpicGames_Fortnite": "epicgames.com epicgames.dev epicgames.net epicgamescdn.com fortnite.com",
    "Fallout76_AWS": "bethesda.net p76prod.systems",
    "GearsOfWar": "gearsofwar.com xboxlive.com",
    "GooseGooseDuck": "gaggle.fun",
    "LeagueOfLegends": "leagueoflegends.com lolesports.com lolstatic.com",
    "MagicTheGathering": "mtgarena.com magic-the-gathering-arena.com mtgarena.downloads.wizards.com",
    "Minecraft_Extra": "minecraft.net minecraftservices.com mojang.com hypixel.net",
    "MortalKombat1": "mortalkombat.com",
    "MortalKombat11": "mortalkombat.com wbagora.com wbinsights.com",
    "OutlastTrials": "rbg-services.com",
    "PhotonEngine": "photonengine.io exitgames.com",
    "RiotGames_Valorant": "playvalorant.com valorant.com valorant.scd.riotcdn.net valorant.secure.dyn.riotcdn.net",
    "Roblox": "roblox.com rbxcdn.com rbxinfra.net robloxcdn.com",
    "Steam": "steamcommunity.com steamcontent.com steampowered.com steamserver.net steamstatic.com",
    "StreetFighter6": "streetfighter.com",
    "Ubisoft_Rainbow_Six_Siege": "rainbow6.com r6s.com ubisoft.com ubi.com uplay.com",
    "VRChat": "vrchat.com vrchat.net vrchat.cloud vrchatassets.com vrcdn.cloud",
    "Wardogs": "wardogs.com live.wardogs.bulkhead.pragmaengine.com",
    "Warframe": "warframe.com digitalextremes.com wrfr.me",
    "WutheringWaves": "kurogame-service.com kurogames.com",
}


def fetch_bytes(url: str, timeout: int = 45) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read()


def fetch_text(url: str, timeout: int = 45) -> str:
    return fetch_bytes(url, timeout).decode("utf-8", errors="replace")


def fetch_json(url: str, timeout: int = 45):
    data = fetch_bytes(url, timeout)
    if data.startswith(b"\x1f\x8b"):
        data = gzip.decompress(data)
    return json.loads(data.decode("utf-8-sig", errors="strict"))


def is_network(value: str) -> bool:
    try:
        ipaddress.ip_network(value, strict=False)
        return True
    except ValueError:
        return False


def split_entries(path: Path) -> tuple[list[str], list[str]]:
    domains, networks = [], []
    if not path.exists():
        return domains, networks
    for raw in path.read_text(encoding="utf-8").splitlines():
        value = raw.strip()
        if not value or value.startswith("#"):
            continue
        (networks if is_network(value) else domains).append(value)
    return domains, networks


def network_sort_key(value: str):
    net = ipaddress.ip_network(value, strict=False)
    return (net.version, int(net.network_address), net.prefixlen)


def profile_domains(path: Path, domains) -> list[str]:
    exact = {domain for domain in domains if not domain.startswith("*.")}
    zones = set(WILDCARD_ZONES.get(path.stem, "").split())
    return sorted(exact | {f"*.{domain}" for domain in exact & zones})


def write_mixed(path: Path, domains, networks) -> bool:
    values = profile_domains(path, domains) + sorted(set(networks), key=network_sort_key)
    content = "\n".join(values) + "\n"
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if old == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def bgp_state(asn: int) -> list[dict]:
    url = f"https://stat.ripe.net/data/bgp-state/data.json?resource=AS{asn}"
    payload = fetch_json(url)
    routes = payload.get("data", {}).get("bgp_state", [])
    if not routes:
        raise RuntimeError(f"RIPEstat returned no BGP state for AS{asn}")
    return routes


def announced_prefixes(asn: int) -> set[str]:
    # The dedicated RIPEstat endpoint is far lighter than requesting the full
    # BGP state for large content ASNs. A short recent window plus the default
    # visibility threshold keeps this focused on globally visible routes.
    start = (datetime.now(timezone.utc) - timedelta(hours=6)).replace(microsecond=0).isoformat()
    url = (
        "https://stat.ripe.net/data/announced-prefixes/data.json"
        f"?resource=AS{asn}&starttime={quote(start)}&min_peers_seeing=10"
    )
    payload = fetch_json(url)
    result = {
        str(ipaddress.ip_network(item["prefix"], strict=False))
        for item in payload.get("data", {}).get("prefixes", [])
        if item.get("prefix")
    }
    if not result:
        raise RuntimeError(f"No recent globally visible prefixes found for AS{asn}")
    return result


def flatten_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from flatten_strings(item)
    elif isinstance(value, (list, tuple, set)):
        for item in value:
            yield from flatten_strings(item)


def flatten_communities(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from flatten_communities(item)
    elif isinstance(value, (list, tuple, set)):
        seq = list(value)
        if len(seq) == 2 and all(isinstance(x, int) or (isinstance(x, str) and x.isdigit()) for x in seq):
            yield f"{seq[0]}:{seq[1]}"
        else:
            for item in seq:
                yield from flatten_communities(item)


def community_prefixes(asn: int, community: str) -> set[str]:
    result = set()
    for route in bgp_state(asn):
        path = route.get("path") or []
        if not path or int(path[-1]) != asn:
            continue
        communities = set(flatten_communities(route.get("community") or []))
        if community in communities:
            prefix = route.get("target_prefix")
            if prefix:
                result.add(str(ipaddress.ip_network(prefix, strict=False)))
    if not result:
        raise RuntimeError(f"No AS{asn} prefixes found with BGP community {community}")
    return result


URL_RE = re.compile(r"https?://[^\s\"'<>]+", re.I)
HOST_RE = re.compile(r"(?<![a-z0-9-])(?:[a-z0-9-]+\.)+[a-z]{2,63}(?![a-z0-9-])", re.I)


def extract_hosts(value) -> set[str]:
    text = "\n".join(flatten_strings(value)) if not isinstance(value, str) else value
    hosts = set()
    for match in URL_RE.findall(text):
        host = urlparse(match.rstrip(").,]}")).hostname
        if host:
            hosts.add(host.lower())
    for host in HOST_RE.findall(text):
        host = host.lower()
        if host.startswith("u002f"):
            continue
        hosts.add(host)
    return hosts


def allowed_host(host: str, suffixes: tuple[str, ...]) -> bool:
    return any(host == suffix or host.endswith("." + suffix) for suffix in suffixes)