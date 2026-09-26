from __future__ import annotations

import ipaddress
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOMAIN_RE = re.compile(r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$")
BAD_SUFFIXES = {
    ".exe", ".dll", ".sys", ".msc", ".bin", ".zip", ".rar", ".7z", ".log",
    ".ini", ".cfg", ".lua", ".php", ".aspx", ".js", ".dat", ".tmp",
}
GENERIC_ROOT_ALLOWED_FILES = {"Cloudflare_AWS.txt", "CompanyOfHeroes2_Broad.txt"}
BROAD_IP_ALLOWED_FILES = {
    "Cloudflare_AWS.txt",
    "Darktide.txt",
    "Fallout76_AWS.txt",
    "Steam.txt",
    "Roblox.txt",
    "BattleNet.txt",
    "LeagueOfLegends.txt",
    "RiotGames_Valorant.txt",
}

GENERIC_ROOTS = {
    "google.com", "googleapis.com", "gstatic.com", "youtube.com",
    "github.com", "githubusercontent.com",
    "cloudflare.com", "cloudflare.net", "cloudfront.net",
    "amazonaws.com", "s3.amazonaws.com",
    "akamaihd.net", "akamaized.net",
    "discord.com", "discord.gg", "discord.media", "discordapp.com", "discordapp.net",
    "one.one", "windows.net", "blob.core.windows.net", "azureedge.net", "azurefd.net",
}


def is_bare_generic_domain(domain: str) -> bool:
    return domain in GENERIC_ROOTS


def validate_domain(value: str, allow_generic_root: bool = False) -> str | None:
    if value != value.lower():
        return "domain must be lowercase"
    if any(value.endswith(suffix) for suffix in BAD_SUFFIXES):
        return "looks like a filename/pseudo-domain"
    # A recurring scraper artifact is an URL-encoded slash (%2F) with the percent
    # sign stripped, e.g. 2fapi-ar-game.bistudio.com.
    if value.startswith("2f") and value[2:].count(".") >= 2 and DOMAIN_RE.fullmatch(value[2:]):
        return "looks like a stripped %2F URL-encoding artifact"
    if not DOMAIN_RE.fullmatch(value):
        return "invalid domain syntax"
    if not allow_generic_root and is_bare_generic_domain(value):
        return "bare generic infrastructure root is not allowed in production"
    return None


def validate_ip(value: str, allow_broad: bool = False) -> str | None:
    try:
        net = ipaddress.ip_network(value, strict=False)
    except ValueError:
        return "invalid IP/CIDR"
    if not net.is_global:
        return "non-global/reserved/private network"
    if not allow_broad and net.version == 4 and net.prefixlen < 16:
        return "IPv4 prefix is too broad (< /16)"
    if not allow_broad and net.version == 6 and net.prefixlen < 32:
        return "IPv6 prefix is too broad (< /32)"
    return None


def validate_file(path: Path, kind: str) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    allow_generic_root = path.name in GENERIC_ROOT_ALLOWED_FILES
    allow_broad_ip = path.name in BROAD_IP_ALLOWED_FILES
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        value = raw.strip()
        if not value or value.startswith("#"):
            continue
        if value in seen:
            errors.append(f"{path.relative_to(ROOT)}:{number}: duplicate: {value}")
            continue
        seen.add(value)

        domain_error = validate_domain(value, allow_generic_root=allow_generic_root)
        ip_error = validate_ip(value, allow_broad=allow_broad_ip)

        if kind == "domains":
            if domain_error:
                errors.append(f"{path.relative_to(ROOT)}:{number}: {domain_error}: {value}")
        elif kind == "ips":
            if ip_error:
                errors.append(f"{path.relative_to(ROOT)}:{number}: {ip_error}: {value}")
        else:
            if domain_error and ip_error:
                errors.append(f"{path.relative_to(ROOT)}:{number}: neither valid domain nor safe IP/CIDR: {value}")
    return errors


def main() -> int:
    errors: list[str] = []
    errors.extend(validate_file(ROOT / "medvedeff-game-list-all.txt", "domains"))
    errors.extend(validate_file(ROOT / "medvedeff-game-ipset.txt", "ips"))
    for path in sorted((ROOT / "games").glob("*.txt")):
        errors.extend(validate_file(path, "mixed"))

    if errors:
        print("\n".join(errors), file=sys.stderr)
        print(f"FAILED: {len(errors)} validation error(s)", file=sys.stderr)
        return 1

    print("OK: production blocklists passed validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())