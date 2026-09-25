from __future__ import annotations

import ipaddress
import json
import re
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
UA = "ru-gaming-blocklist-updater/1.0"


def fetch_bytes(url: str, timeout: int = 45) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read()


def fetch_text(url: str, timeout: int = 45) -> str:
    return fetch_bytes(url, timeout).decode("utf-8", errors="replace")


def fetch_json(url: str, timeout: int = 45):
    return json.loads(fetch_text(url, timeout))


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


def write_mixed(path: Path, domains, networks) -> bool:
    values = sorted(set(domains)) + sorted(set(networks), key=network_sort_key)
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
    result = set()
    for route in bgp_state(asn):
        path = route.get("path") or []
        prefix = route.get("target_prefix")
        if prefix and path and int(path[-1]) == asn:
            result.add(str(ipaddress.ip_network(prefix, strict=False)))
    if not result:
        raise RuntimeError(f"No current originated prefixes found for AS{asn}")
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


def community_prefixes(asn: int, community: str) -> set[str]:
    result = set()
    for route in bgp_state(asn):
        path = route.get("path") or []
        if not path or int(path[-1]) != asn:
            continue
        communities = set(flatten_strings(route.get("community") or []))
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
        hosts.add(host.lower())
    return hosts


def allowed_host(host: str, suffixes: tuple[str, ...]) -> bool:
    return any(host == suffix or host.endswith("." + suffix) for suffix in suffixes)
