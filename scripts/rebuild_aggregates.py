from __future__ import annotations

from pathlib import Path

from updaters.common import ROOT, split_entries

GAMES = ROOT / "games"
DOMAIN_AUX_EXCLUDE = {"Cloudflare_AWS.txt", "CompanyOfHeroes2_Broad.txt"}
IP_AGGREGATE_EXCLUDE = {"Cloudflare_AWS.txt", "CompanyOfHeroes2_Broad.txt", "Darktide.txt", "Fallout76_AWS.txt"}


def main() -> int:
    domains: set[str] = set()
    networks: set[str] = set()

    for path in sorted(GAMES.glob("*.txt")):
        file_domains, file_networks = split_entries(path)
        if path.name not in DOMAIN_AUX_EXCLUDE:
            domains.update(file_domains)
        if path.name not in IP_AGGREGATE_EXCLUDE:
            networks.update(file_networks)

    domains_file = ROOT / "medvedeff-game-list-all.txt"
    ips_file = ROOT / "medvedeff-game-ipset.txt"

    domains_file.write_text("\n".join(sorted(domains)) + "\n", encoding="utf-8")

    import ipaddress
    ordered_networks = sorted(
        networks,
        key=lambda value: (
            ipaddress.ip_network(value, strict=False).version,
            int(ipaddress.ip_network(value, strict=False).network_address),
            ipaddress.ip_network(value, strict=False).prefixlen,
        ),
    )
    ips_file.write_text("\n".join(ordered_networks) + "\n", encoding="utf-8")

    print(f"Rebuilt aggregates: {len(domains)} domains, {len(networks)} IP/CIDR entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
