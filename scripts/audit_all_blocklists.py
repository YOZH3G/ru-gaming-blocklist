from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from rebuild_aggregates import (  # noqa: E402
    COH2_DOMAIN_AGGREGATE_EXCLUDE,
    COH2_IP_AGGREGATE_EXCLUDE,
    DOMAIN_AUX_EXCLUDE,
    IP_AGGREGATE_EXCLUDE,
)
from updaters.common import split_entries  # noqa: E402
from validate_blocklists import validate_file  # noqa: E402

GAMES = ROOT / "games"

# Every entry here has a source-specific updater/verification path in
# scripts/update_priority_profiles.py. Other files are evidence-reviewed.
MANAGED = {
    "Cloudflare_AWS", "Steam", "RiotGames_Valorant", "LeagueOfLegends",
    "Roblox", "BattleNet", "WutheringWaves", "Warframe",
    "MagicTheGathering", "BlueArchive", "Arknights", "StreetFighter6",
    "CallOfDuty", "CompanyOfHeroes2", "Wardogs", "MortalKombat11",
}


def entries(path: Path) -> list[str]:
    return [
        s for line in path.read_text(encoding="utf-8").splitlines()
        if (s := line.strip()) and not s.startswith("#")
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", default="audit-report.md")
    args = parser.parse_args()

    files = sorted(GAMES.glob("*.txt"))
    config = json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))
    mapped = set(config.get("game_map", {}))
    present = {p.stem for p in files}
    errors: list[str] = []
    review_only: list[str] = []
    details: list[str] = []
    all_domains: set[str] = set()
    all_ips: set[str] = set()
    total_domains = total_ips = 0

    missing = sorted(present - mapped)
    stale = sorted(mapped - present)
    if missing:
        errors.append("Missing game_map mappings: " + ", ".join(missing))
    if stale:
        errors.append("Mappings without a game file: " + ", ".join(stale))

    for path in files:
        domains, ips = split_entries(path)
        total_domains += len(domains)
        total_ips += len(ips)
        if not (domains or ips):
            errors.append("Empty list: " + path.name)
        errors.extend(validate_file(path, "mixed"))
        duplicates = [v for v, n in Counter(entries(path)).items() if n > 1]
        if duplicates:
            errors.append(path.name + " has duplicates: " + ", ".join(duplicates))
        if path.stem not in MANAGED:
            review_only.append(path.stem)
        details.append(
            f"| {path.stem} | {len(domains)} | {len(ips)} | "
            f"{'managed' if path.stem in MANAGED else 'review'} |"
        )

        if path.name == "CompanyOfHeroes2.txt":
            domains = set(domains) - COH2_DOMAIN_AGGREGATE_EXCLUDE
            ips = set(ips) - COH2_IP_AGGREGATE_EXCLUDE
        if path.name not in DOMAIN_AUX_EXCLUDE:
            all_domains.update(domains)
        if path.name not in IP_AGGREGATE_EXCLUDE:
            all_ips.update(ips)

    domain_path = ROOT / "medvedeff-game-list-all.txt"
    ip_path = ROOT / "medvedeff-game-ipset.txt"
    for path, expected in ((domain_path, all_domains), (ip_path, all_ips)):
        actual_lines = entries(path)
        actual = set(actual_lines)
        errors.extend(validate_file(path, "domains" if path == domain_path else "ips"))
        if len(actual_lines) != len(actual):
            errors.append("Duplicate entries in " + path.name)
        if missing := sorted(expected - actual):
            errors.append(f"{path.name}: {len(missing)} entries missing: " + ", ".join(missing[:10]))
        if extra := sorted(actual - expected):
            errors.append(f"{path.name}: {len(extra)} unexpected entries: " + ", ".join(extra[:10]))

    report = [
        "# Full gaming blocklist audit", "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}", "",
        f"Game files: **{len(files)}**; game_map: **{len(mapped)}**",
        f"Source-managed profiles: **{len(present & MANAGED)}**",
        f"Evidence-reviewed profiles: **{len(review_only)}**",
        f"All game-file entries: **{total_domains}** domains and **{total_ips}** IP/CIDR (across profiles)",
        f"Expected global aggregate: **{len(all_domains)}** domains and **{len(all_ips)}** IP/CIDR",
        f"Audit errors: **{len(errors)}**", "",
        "## Each game profile", "",
        "| Game file | Domains | IP/CIDR | Update mode |",
        "| --- | ---: | ---: | --- |",
        *details, "",
        "## Validation and aggregate integrity", "",
        *([f"- ERROR: {e}" for e in errors] or ["- No structural inconsistencies found."]),
        "", "## Review-only profiles", "",
        *([f"- {name}" for name in review_only] or ["- None."]), "",
        "## Scope and limitations", "",
        "- Validity and deterministic aggregates are checked for EVERY game file.",
        "- This does not assert that all current game-service endpoints are known.",
        "- Unmanaged profiles need game-specific evidence; never automatically import shared AWS/CDN address space.",
        "- Domain DNS failures or transient endpoint changes do not justify automatic removal.",
        "- Dedicated AWS, Riot BGP, provider-feed and game-manifest jobs retain their existing source-specific update policies.",
        "- Global Cloudflare/Outlast and regional AWS/CoH2 exceptions follow rebuild_aggregates.py.",
        "- This command does not change production lists; verified changes require reviewed diffs.", "",
    ]
    text = "\n".join(report)
    Path(args.report).write_text(text, encoding="utf-8")
    print(text)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
