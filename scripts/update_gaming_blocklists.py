from __future__ import annotations

import argparse
import dataclasses
import ipaddress
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from collections import OrderedDict, defaultdict
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATH = ROOT / "sources.json"

DOMAIN_RE = re.compile(
    r"(?<![A-Za-z0-9_-])"
    r"(?:\*\.)?"
    r"((?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+"
    r"[A-Za-z]{2,63})"
    r"(?![A-Za-z0-9_-])"
)

URL_HOST_RE = re.compile(r"https?://([^/\s'\"<>]+)", re.IGNORECASE)
IPV4_CIDR_RE = re.compile(r"(?<![0-9A-Fa-f:.])(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?(?![0-9A-Fa-f:.])")
IPV6_CANDIDATE_RE = re.compile(r"(?<![0-9A-Fa-f:])(?:[0-9A-Fa-f]{0,4}:){2,7}[0-9A-Fa-f]{0,4}(?:/\d{1,3})?(?![0-9A-Fa-f:])")

COMMON_FALSE_DOMAIN_SUFFIXES = {"example.com", "example.org", "example.net", "test.com", "localhost.localdomain"}
COMMON_NON_GAME_DOMAINS = {
    "github.com", "raw.githubusercontent.com", "api.github.com", "docs.github.com",
    "youtube.com", "youtu.be", "google.com", "gstatic.com", "discord.com",
    "discord.gg", "telegram.org", "t.me", "whatsapp.com", "openwrt.org",
}

BLOCKED_DOMAIN_KEYWORDS = {
    "porn", "porno", "xxx", "sex", "adult", "camgirl", "escort",
    "casino", "bet", "betting", "poker", "gambling", "slots",
    "weed", "cannabis", "marijuana", "cocaine", "drug", "drugs",
    "pharmacy", "viagra",
}

BLOCKED_GAME_NAMES = {
    "zapret", "youtube", "discord", "youtube_discord", "youtubediscord",
    "github", "raw", "general", "hostlist", "ipset", "blocklist",
    "domainlist", "iplist", "issue", "issues", "readme", "hosts",
}

# If this is the only game detected from an issue, we send it to review instead of games/Other_Games.txt.
GENERIC_REVIEW_ONLY_GAMES = {"Other_Games"}

BINARY_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip", ".7z", ".rar",
    ".exe", ".dll", ".bin", ".dat", ".pak", ".mp4", ".mp3", ".wav", ".ttf", ".otf",
}


def log(message: str) -> None:
    print(message, flush=True)


def warn(message: str) -> None:
    print(f"WARNING: {message}", file=sys.stderr, flush=True)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    return [line.rstrip("\n\r") for line in path.read_text(encoding="utf-8", errors="replace").splitlines()]


def normalize_existing_key(line: str) -> str:
    return line.strip().lower()


def append_unique(path: Path, new_items: Iterable[str], dry_run: bool = False) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing_lines = read_lines(path)
    existing_keys = {normalize_existing_key(x) for x in existing_lines if normalize_existing_key(x)}
    to_add: list[str] = []
    for item in new_items:
        item = item.strip()
        if not item:
            continue
        key = normalize_existing_key(item)
        if key in existing_keys:
            continue
        existing_keys.add(key)
        to_add.append(item)
    if not to_add:
        return 0
    if dry_run:
        log(f"[dry-run] Would append {len(to_add)} line(s) to {path.relative_to(ROOT)}")
        return len(to_add)
    with path.open("a", encoding="utf-8", newline="\n") as f:
        if existing_lines and existing_lines[-1] != "":
            f.write("\n")
        for item in to_add:
            f.write(item + "\n")
    return len(to_add)


def strip_comments(line: str) -> str:
    line = re.sub(r"(?<!:)//.*$", "", line)
    line = line.split("#", 1)[0]
    return line.strip()


def clean_possible_domain(raw: str) -> str | None:
    token = raw.strip().lower()
    token = token.strip("`'\"<>[](){}|,;!")
    token = token.removeprefix("||").removeprefix("*.").removeprefix("address=/").strip("/^")
    if token.startswith(("http://", "https://")):
        token = urllib.parse.urlsplit(token).netloc
    if "@" in token:
        return None
    token = token.split("/", 1)[0].split(":", 1)[0].strip(".")
    if not token or token in COMMON_FALSE_DOMAIN_SUFFIXES or token in COMMON_NON_GAME_DOMAINS:
        return None
    if "_" in token or len(token) > 253:
        return None

    # GitHub issue/config text frequently contains URL-encoded paths. DOMAIN_RE can
    # otherwise start matching immediately after '%' in "%2Fapi.example.com" and
    # produce the fake hostname "2fapi.example.com".
    if token.startswith("2f") and token[2:].count(".") >= 2 and DOMAIN_RE.fullmatch(token[2:]):
        return None
    labels = token.split(".")
    if len(labels) < 2:
        return None
    for label in labels:
        if not label or len(label) > 63 or label.startswith("-") or label.endswith("-"):
            return None
        if not re.fullmatch(r"[a-z0-9-]+", label):
            return None
    if not re.fullmatch(r"[a-z]{2,63}", labels[-1]):
        return None
    if token.endswith((".md", ".txt", ".bat", ".cmd", ".json", ".yaml", ".yml", ".png", ".jpg")):
        return None

    token_for_filter = token.replace("-", " ").replace(".", " ")
    for bad_word in BLOCKED_DOMAIN_KEYWORDS:
        if re.search(rf"(?<![a-z0-9]){re.escape(bad_word)}(?![a-z0-9])", token_for_filter):
            return None

    return token


def normalize_ip(raw: str) -> str | None:
    token = raw.strip().strip("`'\"<>[](){}|,;!")
    if not token:
        return None
    try:
        if "/" in token:
            return str(ipaddress.ip_network(token, strict=False))
        return str(ipaddress.ip_address(token))
    except ValueError:
        return None


def extract_domains(text: str) -> set[str]:
    found: set[str] = set()
    for match in URL_HOST_RE.finditer(text):
        domain = clean_possible_domain(match.group(1))
        if domain:
            found.add(domain)
    for match in DOMAIN_RE.finditer(text):
        domain = clean_possible_domain(match.group(1))
        if domain:
            found.add(domain)
    for match in re.finditer(r"address=/([^/\s]+)/", text, re.IGNORECASE):
        domain = clean_possible_domain(match.group(1))
        if domain:
            found.add(domain)
    return found


def extract_ips(text: str) -> set[str]:
    found: set[str] = set()
    for match in IPV4_CIDR_RE.finditer(text):
        value = normalize_ip(match.group(0))
        if value:
            found.add(value)
    for match in IPV6_CANDIDATE_RE.finditer(text):
        value = normalize_ip(match.group(0))
        if value:
            found.add(value)
    return found


def normalize_text_for_match(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).lower()
    return text.replace("_", " ").replace("-", " ").replace("/", " ")


def normalize_game_key(text: str) -> str:
    return normalize_text_for_match(text).replace(" ", "_")


def slugify_game_name(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9А-Яа-яЁё]+", "_", name.strip()).strip("_")
    return (cleaned or "Other_Games") + ".txt"


def build_alias_index(game_map: dict[str, list[str]]) -> list[tuple[str, str, str]]:
    index: list[tuple[str, str, str]] = []
    for game, aliases in game_map.items():
        for alias in [game] + aliases:
            norm = normalize_text_for_match(alias)
            if norm:
                index.append((game, alias, norm))
    index.sort(key=lambda x: len(x[2]), reverse=True)
    return index


def filter_known_games(games: Iterable[str], known_game_names: set[str]) -> set[str]:
    out: set[str] = set()