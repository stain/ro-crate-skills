#!/usr/bin/env python3
"""Print release and maintenance data for the RO-Crate tools evaluated in
skills/ro-crate-tools/references/tool-evaluation.md, from PyPI, npm and GitHub (needs network).

Usage: python tests/tool_currency.py [--today YYYY-MM-DD]
Standard library only. GitHub's unauthenticated API allows about 60 requests per hour.
Classes: active = release or push within 6 months; slow = 6-24 months; stale = over 24 months.
"""
import json
import sys
import urllib.request
from datetime import date

TOOLS = [  # (name, pypi, npm, github)
    ("ro-crate-py", "rocrate", None, "ResearchObject/ro-crate-py"),
    ("rocrate-validator", "roc-validator", None, "crs4/rocrate-validator"),
    ("signposting", "signposting", None, "stain/signposting"),
    ("ro-crate-html (rochtml)", None, "ro-crate-html", "Language-Research-Technology/ro-crate-html-js"),
    ("ro-crate-js", None, "ro-crate", "Language-Research-Technology/ro-crate-js"),
    ("ro-crate-excel", None, "ro-crate-excel", "Language-Research-Technology/ro-crate-excel"),
    ("rocrate-action-recorder", "rocrate-action-recorder", None, "i-VRESSE/rocrate-action-recorder"),
    ("runcrate", "runcrate", None, "ResearchObject/runcrate"),
    ("rocrate-tabular", None, None, "Sydney-Informatics-Hub/rocrate-tabular"),
    ("rocrate-zenodo", "rocrate-zenodo", None, "ResearchObject/ro-crate-zenodo"),
    ("rocrate-inveniordm", "rocrate-inveniordm", None, "ResearchObject/ro-crate-inveniordm"),
    ("bagit-python", "bagit", None, "LibraryOfCongress/bagit-python"),
    ("RO-Crate-RAG-Validator", None, None, "alexhambley/RO-Crate-RAG-Validator"),
    ("CheckMyCrate", None, None, "KockataEPich/CheckMyCrate"),
    ("ro-crate-validator-py", None, None, "ResearchObject/ro-crate-validator-py"),
    ("ro-crates-deposit", None, None, "beerphilipp/ro-crates-deposit"),
    ("Crate-O", None, None, "Language-Research-Technology/crate-o"),
    ("nf-prov", None, None, "nextflow-io/nf-prov"),
]


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "ro-crate-skills", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except Exception as e:  # network or rate limit: report, do not crash
        return {"_err": str(e)[:60]}


def months(d, today):
    return (today.year - d.year) * 12 + today.month - d.month


def klass(m):
    return "active" if m <= 6 else ("slow" if m <= 24 else "stale")


def main(argv):
    today = date.fromisoformat(argv[argv.index("--today") + 1]) if "--today" in argv else date.today()
    print(f"as of {today}")
    print("| Tool | Latest release | Last push | Class |")
    print("|---|---|---|---|")
    for name, pypi, npm, gh in TOOLS:
        rel = None
        if pypi:
            d = get(f"https://pypi.org/pypi/{pypi}/json")
            if "_err" not in d:
                files = d["releases"].get(d["info"]["version"], [])
                rel = (d["info"]["version"], date.fromisoformat(files[0]["upload_time"][:10])) if files else None
        elif npm:
            d = get(f"https://registry.npmjs.org/{npm}")
            if "_err" not in d:
                v = d["dist-tags"]["latest"]
                rel = (v, date.fromisoformat(d["time"][v][:10]))
        push = None
        g = get(f"https://api.github.com/repos/{gh}")
        if "_err" not in g and "pushed_at" in g:
            push = date.fromisoformat(g["pushed_at"][:10])
        newest = max([x for x in ((rel[1] if rel else None), push) if x], default=None)
        cls = klass(months(newest, today)) if newest else "unknown"
        if g.get("archived"):
            cls += " (archived)"
        print(f"| {name} | {f'{rel[0]} ({rel[1]})' if rel else '-'} | {push or '-'} | {cls} |")


if __name__ == "__main__":
    main(sys.argv[1:])
