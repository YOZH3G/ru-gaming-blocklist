from __future__ import annotations

import ipaddress
import json
import urllib.request
from updaters.common import ROOT, profile_domains

AWS_IP_RANGES_URL = "https://ip-ranges.amazonaws.com/ip-ranges.json"
TARGET_REGIONS = {"eu-central-1", "eu-north-1", "eu-west-2"}
TARGET_SERVICE = "EC2"
STATIC_DOMAINS = ["fatshark.se", "playdarktide.com"]

OUTPUT = ROOT / "games" / "Darktide.txt"


def sort_networks(values: set[str]) -> list[str]:
    return sorted(
        values,
        key=lambda value: (
            ipaddress.ip_network(value).version,
            int(ipaddress.ip_network(value).network_address),
            ipaddress.ip_network(value).prefixlen,
        ),
    )


def fetch_aws_ranges() -> dict:
    request = urllib.request.Request(
        AWS_IP_RANGES_URL,
        headers={"User-Agent": "ru-gaming-blocklist-darktide-updater/1.0"},
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        return json.load(response)


def build_list(payload: dict) -> tuple[list[str], str | None]:
    networks = {
        item["ip_prefix"]
        for item in payload.get("prefixes", [])
        if item.get("region") in TARGET_REGIONS
        and item.get("service") == TARGET_SERVICE
        and item.get("ip_prefix")
    }

    if not networks:
        raise RuntimeError("AWS feed returned no matching Darktide EC2 prefixes")

    networks.update(
        item["ipv6_prefix"]
        for item in payload.get("ipv6_prefixes", [])
        if item.get("region") in TARGET_REGIONS
        and item.get("service") == TARGET_SERVICE
        and item.get("ipv6_prefix")
    )
    return profile_domains(OUTPUT, STATIC_DOMAINS) + sort_networks(networks), payload.get("createDate")


def main() -> int:
    payload = fetch_aws_ranges()
    entries, create_date = build_list(payload)
    OUTPUT.write_text("\n".join(entries) + "\n", encoding="utf-8")

    domain_count = len(profile_domains(OUTPUT, STATIC_DOMAINS))
    print(
        f"Updated {OUTPUT.relative_to(ROOT)}: "
        f"{domain_count} domains + {len(entries) - domain_count} CIDRs "
        f"(AWS createDate={create_date or 'unknown'})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
