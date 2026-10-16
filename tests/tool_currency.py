#!/usr/bin/env python3
"""Print release and maintenance data for the RO-Crate tools evaluated in
skills/ro-crate-tools/references/tool-evaluation.md (needs network and git).

Usage: python tests/tool_currency.py [--today YYYY-MM-DD]
Releases come from PyPI and npm; the last commit on the repository's default branch comes from a
shallow `git clone` (no GitHub API, so there is no rate limit). Standard library plus git.
Classes: active = release or last commit within 6 months; slow = 6-24 months; stale = over 24 months.
"""
import json
import subprocess
import sys
import tempfile
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


def last_commit(repo):
    """(default branch, date of its last commit) via git; (None, None) if git or the clone fails."""
    url = f"https://github.com/{repo}"
    env = {"GIT_TERMINAL_PROMPT": "0", "PATH": __import__("os").environ.get("PATH", "")}
    try:
        out = subprocess.run(["git", "ls-remote", "--symref", url, "HEAD"], capture_output=True, text=True,
                             timeout=60, env=env).stdout
        branch = next(l.split()[1].replace("refs/heads/", "") for l in out.splitlines() if l.startswith("ref:"))
        with tempfile.TemporaryDirectory() as d:
            subprocess.run(["git", "clone", "-q", "--depth", "1", "--branch", branch, "--single-branch", url, d],
                           check=True, capture_output=True, timeout=180, env=env)
            day = subprocess.run(["git", "-C", d, "log", "-1", "--format=%cs"], capture_output=True, text=True).stdout.strip()
        return branch, date.fromisoformat(day)
    except (subprocess.SubprocessError, StopIteration, ValueError, OSError):
        return None, None


def months(d, today):
    return (today.year - d.year) * 12 + today.month - d.month


def klass(m):
    return "active" if m <= 6 else ("slow" if m <= 24 else "stale")


def main(argv):
    today = date.fromisoformat(argv[argv.index("--today") + 1]) if "--today" in argv else date.today()
    print(f"as of {today}")
    print("| Tool | Latest release | Last commit (default branch) | Class |")
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
        branch, commit = last_commit(gh)
        newest = max([x for x in ((rel[1] if rel else None), commit) if x], default=None)
        cls = klass(months(newest, today)) if newest else "unknown"
        print(f"| {name} | {f'{rel[0]} ({rel[1]})' if rel else '-'} | {f'{commit} ({branch})' if commit else '-'} | {cls} |")


if __name__ == "__main__":
    main(sys.argv[1:])
