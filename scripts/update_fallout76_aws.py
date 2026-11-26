from __future__ import annotations

import ipaddress
import json
import urllib.request
from pathlib import Path

AWS_IP_RANGES_URL = "https://ip-ranges.amazonaws.com/ip-ranges.json"
TARGET_REGIONS = {"ap-southeast-2", "eu-central-1", "eu-west-1", "us-east-1", "us-east-2"}
TARGET_SERVICE = "EC2"
STATIC_DOMAINS = [
    "api.bethesda.net",
    "bethesda.net",
    "fallout.bethesda.net",
    "p76prod.systems",
    "ap-southeast-2-prod-prodpc01-reg-httpping.p76prod.systems",
    "eu-central-1-prod-prodpc01-reg-httpping.p76prod.systems",
    "eu-west-1-prod-prodpc01-reg-httpping.p76prod.systems",
    "us-east-1-prod-prodpc01-reg-httpping.p76prod.systems",
    "us-east-2-prod-prodpc01-glb-bps-bigateway.p76prod.systems",
    "us-east-2-prod-prodpc01-glb-bps-gateway.p76prod.systems",
    "us-east-2-prod-prodpc01-glb-bps-pushy.p76prod.systems",
]

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "games" / "Fallout76_AWS.txt"


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
        headers={"User-Agent": "ru-gaming-blocklist-fallout76-updater/1.0"},
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        return json.load(response)


def build_list(payload: dict) -> tuple[list[str], str | None]:
    networks = set()
    regions = set()
    for item in payload.get("prefixes", []):
        region = item.get("region")
        if region in TARGET_REGIONS and item.get("service") == TARGET_SERVICE and item.get("ip_prefix"):
            networks.add(item["ip_prefix"])
            regions.add(region)

    missing = TARGET_REGIONS - regions
    if missing:
        raise ValueError(f"Missing EC2 prefixes for regions: {sorted(missing)}")

    return STATIC_DOMAINS + sort_networks(networks), payload.get("createDate")


def main() -> int:
    payload = fetch_aws_ranges()
    entries, create_date = build_list(payload)
    OUTPUT.write_text("\n".join(entries) + "\n", encoding="utf-8")

    print(
        f"Updated {OUTPUT.relative_to(ROOT)}: "
        f"{len(STATIC_DOMAINS)} domains + {len(entries) - len(STATIC_DOMAINS)} CIDRs "
        f"(AWS createDate={create_date or 'unknown'})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
