#!/usr/bin/env python3
"""Sync rule lists with the upstream sources they were built from.

Each upstream source has a snapshot in sync/upstream/. On every run the
script diffs the current upstream against its snapshot and only applies
that delta to our .list: entries upstream added are appended (unless
excluded or already covered), entries upstream removed are dropped.
Personal additions and deliberate removals are therefore left alone.
The .yaml files are regenerated from the .list files, and a Markdown
summary of the changes is written to $SYNC_SUMMARY.
"""

import ipaddress
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT_DIR = ROOT / "sync" / "upstream"
SUMMARY = Path(os.environ.get("SYNC_SUMMARY", "/tmp/sync-summary.md"))

BM7 = "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule"
V2FLY = "https://raw.githubusercontent.com/v2fly/domain-list-community/master/data"
ACC = "https://raw.githubusercontent.com/Accademia/Additional_Rule_For_Clash/main"
META = "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta"

RULES = {
    "X": {
        "list": "X/X.list",
        "sources": [
            ("blackmatrix7-Twitter", f"{BM7}/Loon/Twitter/Twitter.list", "surge"),
            ("v2fly-xai", f"{V2FLY}/xai", "v2fly"),
            ("accademia-Grok", f"{ACC}/Grok/Grok_No_Resolve.yaml", "clash"),
            ("AS13414", f"{META}/asn/AS13414.list", "cidr"),
        ],
        # Statsig CDN shared by many apps, and an Apple IP.
        "exclude": ["DOMAIN-SUFFIX,featureassets.org", "IP-CIDR,17.253.4.125/32,no-resolve"],
    },
    "US_Bank": {
        "list": "US_Bank/US_Bank.list",
        "sources": [("accademia-BankUS", f"{ACC}/Bank/BankUS.yaml", "clash")],
        # eastwest.com is East West Hospitality; the Zelle keywords match
        # unrelated domains; gobankrewards.com is unverified; the DOMAIN rule
        # duplicates DOMAIN-SUFFIX,us.hsbc.com.
        "exclude": [
            "DOMAIN-SUFFIX,eastwest.com",
            "DOMAIN-KEYWORD,zelle",
            "DOMAIN-KEYWORD,zellepay",
            "DOMAIN-SUFFIX,gobankrewards.com",
            "DOMAIN,us.hsbc.com",
        ],
    },
    "HK_Bank": {
        "list": "HK_Bank/HK_Bank.list",
        "sources": [("accademia-BankHK", f"{ACC}/Bank/BankHK.yaml", "clash")],
        "exclude": [],
    },
    "Apple_AI": {
        "list": "Apple_AI/Apple_AI.list",
        "sources": [
            ("accademia-AppleAI", f"{ACC}/AppleAI/AppleAI.yaml", "clash"),
            ("v2fly-apple-intelligence", f"{V2FLY}/apple-intelligence", "v2fly"),
        ],
        "exclude": [],
    },
    "PikPak": {
        "list": "PikPak/pikpak.list",
        "sources": [("v2fly-pikpak", f"{V2FLY}/pikpak", "v2fly")],
        "exclude": [],
    },
}

YAML_HEADER = "# Clash rule-provider: behavior: classical\npayload:\n"
IP_TYPES = ("IP-CIDR", "IP-CIDR6")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "personal-rule-sync"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8")


def ip_rule(cidr):
    net = ipaddress.ip_network(cidr.strip(), strict=False)
    return f"{'IP-CIDR' if net.version == 4 else 'IP-CIDR6'},{net},no-resolve"


def normalize(line):
    """Canonical form of one Surge/Loon/Clash classical rule, or None."""
    parts = [p.strip() for p in line.split(",") if p.strip()]
    if len(parts) < 2:
        return None
    kind, value = parts[0].upper(), parts[1]
    if kind in IP_TYPES:
        return ip_rule(value)
    if kind in ("DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD"):
        return f"{kind},{value.lower().lstrip('.')}"
    return None


def parse(text, fmt):
    rules = set()
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if fmt == "clash":
            if not line.startswith("-"):
                continue
            line = line.lstrip("-").strip().strip("'\"")
            rule = normalize(line) if "," in line else None
        elif fmt == "surge":
            rule = normalize(line)
        elif fmt == "cidr":
            rule = ip_rule(line)
        elif fmt == "v2fly":
            if "@ads" in line.split() or line.startswith(("include:", "regexp:")):
                continue
            value = line.split()[0]
            if value.startswith("full:"):
                rule = f"DOMAIN,{value[5:]}"
            elif value.startswith("keyword:"):
                rule = f"DOMAIN-KEYWORD,{value[8:]}"
            else:
                rule = f"DOMAIN-SUFFIX,{value.removeprefix('domain:')}"
        else:
            raise ValueError(fmt)
        if rule:
            rules.add(rule)
    return rules


def covered(rule, existing):
    """True if an existing rule already matches everything `rule` matches."""
    kind, value = rule.split(",")[:2]
    for other in existing:
        okind, ovalue = other.split(",")[:2]
        if kind in IP_TYPES and okind in IP_TYPES:
            a, b = ipaddress.ip_network(value), ipaddress.ip_network(ovalue)
            if a.version == b.version and a.subnet_of(b):
                return True
        elif kind in ("DOMAIN", "DOMAIN-SUFFIX") and okind == "DOMAIN-SUFFIX":
            if value == ovalue or value.endswith("." + ovalue):
                return True
        elif kind == "DOMAIN" and okind == "DOMAIN" and value == ovalue:
            return True
        elif kind == okind == "DOMAIN-KEYWORD" and ovalue in value:
            return True
        elif kind in ("DOMAIN", "DOMAIN-SUFFIX") and okind == "DOMAIN-KEYWORD" and ovalue in value:
            return True
    return False


def same_rule(a, b):
    return normalize(a) == normalize(b)


def main():
    report = []
    for name, cfg in RULES.items():
        list_path = ROOT / cfg["list"]
        lines = list_path.read_text().splitlines()
        exclude = {normalize(e) or e for e in cfg["exclude"]}
        added, removed, skipped = [], [], []

        for source_id, url, fmt in cfg["sources"]:
            upstream = parse(fetch(url), fmt)
            if not upstream:
                sys.exit(f"{source_id}: upstream parsed to nothing, refusing to sync")
            snap_path = SNAPSHOT_DIR / f"{source_id}.txt"
            previous = set(snap_path.read_text().splitlines()) if snap_path.exists() else set()
            snap_path.parent.mkdir(parents=True, exist_ok=True)
            snap_path.write_text("".join(f"{r}\n" for r in sorted(upstream)))
            if not previous:
                continue  # first run only records the snapshot

            for rule in sorted(previous - upstream):
                keep = [l for l in lines if not same_rule(l, rule)]
                if len(keep) != len(lines):
                    lines = keep
                    removed.append((rule, source_id))
            for rule in sorted(upstream - previous):
                if rule in exclude:
                    skipped.append((rule, source_id, "排除清单"))
                elif covered(rule, [normalize(l) for l in lines if normalize(l)]):
                    skipped.append((rule, source_id, "已被现有规则覆盖"))
                else:
                    first_ip = next((i for i, l in enumerate(lines) if l.startswith(IP_TYPES)), len(lines))
                    lines.insert(len(lines) if rule.startswith(IP_TYPES) else first_ip, rule)
                    added.append((rule, source_id))

        list_path.write_text("".join(f"{l}\n" for l in lines))
        list_path.with_suffix(".yaml").write_text(YAML_HEADER + "".join(f"  - {l}\n" for l in lines))

        if added or removed or skipped:
            report.append(f"### {name}\n")
            report += [f"- 新增 `{r}`（{s}）" for r, s in added]
            report += [f"- 删除 `{r}`（上游 {s} 已移除）" for r, s in removed]
            report += [f"- 跳过 `{r}`（{s}，{why}）" for r, s, why in skipped]
            report.append("")

    SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY.write_text("\n".join(report) if report else "上游没有影响规则内容的变化，仅更新了快照。\n")
    print(SUMMARY.read_text())


if __name__ == "__main__":
    main()
