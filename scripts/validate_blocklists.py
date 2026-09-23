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


def validate_domain(value: str) -> str | None:
    if value != value.lower():
        return "domain must be lowercase"
    if any(value.endswith(suffix) for suffix in BAD_SUFFIXES):
        return "looks like a filename/pseudo-domain"
    if not DOMAIN_RE.fullmatch(value):
        return "invalid domain syntax"
    if is_bare_generic_domain(value):
        return "bare generic infrastructure root is not allowed in production"
    return None


def validate_ip(value: str) -> str | None:
    try:
        net = ipaddress.ip_network(value, strict=False)
    except ValueError:
        return "invalid IP/CIDR"
    if not net.is_global:
        return "non-global/reserved/private network"
    if net.version == 4 and net.prefixlen < 16:
        return "IPv4 prefix is too broad (< /16)"
    if net.version == 6 and net.prefixlen < 32:
        return "IPv6 prefix is too broad (< /32)"
    return None


def validate_file(path: Path, kind: str) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        value = raw.strip()
        if not value or value.startswith("#"):
            continue
        if value in seen:
            errors.append(f"{path.relative_to(ROOT)}:{number}: duplicate: {value}")
            continue
        seen.add(value)

        domain_error = validate_domain(value)
        ip_error = validate_ip(value)

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