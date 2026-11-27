#!/usr/bin/env python3
"""Trigger tests: does an agent pick the right skill from the descriptions alone?

Runs each prompt in tests/triggers/triggers.json through `claude -p` with this repository loaded as a
plugin (all skills present at once, next to Claude Code's own skills) and reads which skill the agent
invoked first (the `Skill` tool call). Standard library only; needs the `claude` CLI and a login.

Usage: python tests/triggers/run.py [--split dev|test|all] [--repeats N] [--workers N] [--model M]
                                    [--only SKILL] [--out results.json]

positive prompts pass when the first Skill call is one of `accept`; negatives pass when no ro-crate-*
skill is called. Prompts are single-turn (`--max-turns 1`): only the first decision is observed.
"""
import json
import os
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
PLUGIN_PREFIX = "ro-crate-skills:"


def parse_stream(text):
    """Return (skill or None, first_tool or None, cost_usd) from `claude -p --output-format stream-json` output."""
    skill, first_tool, cost = None, None, 0.0
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if e.get("type") == "assistant":
            for c in e.get("message", {}).get("content", []):
                if c.get("type") == "tool_use":
                    first_tool = first_tool or c.get("name")
                    if c.get("name") == "Skill" and skill is None:
                        skill = str(c.get("input", {}).get("skill", "")).removeprefix(PLUGIN_PREFIX)
        elif e.get("type") == "result":
            cost = e.get("total_cost_usd") or 0.0
    return skill, first_tool, cost


def run_one(query, model=None, timeout=180, attempts=2):
    cwd = tempfile.mkdtemp(prefix="trigger-")
    cmd = ["claude", "-p", query, "--plugin-dir", str(REPO), "--setting-sources", "project",
           "--output-format", "stream-json", "--verbose", "--max-turns", "1", "--no-session-persistence"]
    if model:
        cmd += ["--model", model]
    for _ in range(attempts):
        try:
            p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, stdin=subprocess.DEVNULL)
        except subprocess.TimeoutExpired:
            continue
        skill, tool, cost = parse_stream(p.stdout)
        if p.stdout.strip():
            return {"skill": skill, "first_tool": tool, "cost": cost}
    return {"skill": None, "first_tool": None, "cost": 0.0, "error": "no output"}


def passed(item, skill):
    if item["kind"] == "positive":
        return skill in item["accept"]
    return not (skill or "").startswith("ro-crate-")


def main(argv):
    def opt(name, default=None):
        return argv[argv.index(name) + 1] if name in argv else default
    split, repeats, workers = opt("--split", "dev"), int(opt("--repeats", "1")), int(opt("--workers", "6"))
    model, only, out = opt("--model"), opt("--only"), opt("--out")
    items = json.loads((HERE / "triggers.json").read_text())
    items = [i for i in items if (split == "all" or i["split"] == split) and (not only or i.get("skill") == only)]
    jobs = [(i, r) for i in items for r in range(repeats)]
    with ThreadPoolExecutor(workers) as ex:
        results = list(ex.map(lambda j: run_one(j[0]["query"], model), jobs))
    rows = []
    for (item, r), res in zip(jobs, results):
        got = res["skill"]
        got = got if got is None or got.startswith("ro-crate-") else f"(other) {got}"
        rows.append({"id": item["id"], "repeat": r, "expected": item["accept"] if item["kind"] == "positive" else None,
                     "got": got, "pass": passed(item, res["skill"]), "first_tool": res["first_tool"],
                     "cost": res["cost"], "split": item["split"], "kind": item["kind"], "skill": item.get("skill"),
                     "query": item["query"]})
    if out:
        Path(out).write_text(json.dumps(rows, indent=1) + "\n")
    summarize(rows)
    return 0


def summarize(rows):
    by_skill = {}
    for r in rows:
        by_skill.setdefault(r["skill"] or "(negatives)", []).append(r)
    print(f"{'skill':30s} pass/total")
    for s, rs in sorted(by_skill.items(), key=lambda kv: kv[0]):
        print(f"{s:30s} {sum(r['pass'] for r in rs):>3d}/{len(rs):<3d}")
    tp = [r for r in rows if r["kind"] == "positive"]
    ng = [r for r in rows if r["kind"] == "negative"]
    print(f"\npositives {sum(r['pass'] for r in tp)}/{len(tp)}   negatives (no ro-crate skill) {sum(r['pass'] for r in ng)}/{len(ng)}   cost ${sum(r['cost'] for r in rows):.2f}")
    bad = [r for r in rows if not r["pass"]]
    if bad:
        print("\nfailures:")
        for r in bad:
            exp = ",".join(x.replace("ro-crate-", "") for x in r["expected"]) if r["expected"] else "none"
            got = (r["got"] or "none").replace("ro-crate-", "")
            print(f"- {r['id']} [{r['split']}] expected {exp}, got {got}: {r['query'][:95]}")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
