#!/usr/bin/env python3
"""Grade eval runs with scripted checks.

Usage: python tests/graders/run.py <iteration dir | eval dir> [--verbose] [--json] [--no-write] [--repo PATH]

The iteration directory holds eval-<name>/{with_skill,without_skill}/outputs/ (answer.md, commands.md,
crates). For each run it writes grading.json next to `outputs/` (fields text, passed, evidence, as the
skill-creator viewer expects) and prints a table. Standard library only.
"""
import inspect
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent))

from tests.graders.core import Run  # noqa: E402
from tests.graders.evals import GRADERS  # noqa: E402

VARIANTS = ("with_skill", "without_skill", "old_skill")


def grade_run(name, outputs, repo):
    spec = GRADERS[name]
    run = Run.open(outputs, repo)
    crate = run.find_crate(spec.get("crate_hint"))
    results = []
    for e in spec["expectations"]:
        params = inspect.signature(e.check).parameters
        args = [run] + ([crate] if "crate" in params else [])
        try:
            passed, evidence = e.check(*args, *e.args, **e.params)
        except Exception as ex:  # a grader bug or odd output must not stop the run
            passed, evidence = False, f"grader error: {type(ex).__name__}: {ex}"
        results.append({"text": e.text, "passed": bool(passed), "evidence": evidence, "kind": "tool" if e.tool else "script"})
    return results


def main(argv):
    flags = {a for a in argv if a.startswith("--") and "=" not in a}
    args = [a for a in argv if not a.startswith("--")]
    repo = HERE.parent.parent
    if "--repo" in argv:
        repo = Path(argv[argv.index("--repo") + 1])
        args = [a for a in args if a != str(repo)]
    if len(args) != 1:
        print(__doc__)
        return 2
    base = Path(args[0])
    eval_dirs = [base] if base.name.startswith("eval-") else sorted(p for p in base.glob("eval-*") if p.is_dir())
    summary = {}
    for d in eval_dirs:
        name = d.name[len("eval-"):]
        if name not in GRADERS:
            print(f"(no grader for {name})")
            continue
        for v in VARIANTS:
            outputs = d / v / "outputs"
            if not outputs.exists():
                continue
            res = grade_run(name, outputs, repo)
            summary.setdefault(name, {})[v] = res
            if "--no-write" not in flags:
                (d / v / "grading.json").write_text(json.dumps({"expectations": res}, indent=2) + "\n")
    if "--json" in flags:
        print(json.dumps(summary, indent=2))
        return 0
    total = {v: [0, 0] for v in VARIANTS}
    print(f"{'eval':24s} " + " ".join(f"{v:>14s}" for v in VARIANTS[:2]))
    for name, byv in summary.items():
        cells = []
        for v in VARIANTS[:2]:
            r = byv.get(v)
            if r is None:
                cells.append(f"{'-':>14s}")
                continue
            p = sum(x["passed"] for x in r)
            total[v][0] += p
            total[v][1] += len(r)
            cells.append(f"{p:>10d}/{len(r):<3d}")
        print(f"{name:24s} " + " ".join(cells))
        if "--verbose" in flags:
            for v, r in byv.items():
                for x in r:
                    if not x["passed"]:
                        print(f"    [{v}] FAIL {x['text']}: {x['evidence'][:140]}")
    print(f"{'TOTAL':24s} " + " ".join(f"{total[v][0]:>10d}/{total[v][1]:<3d}" for v in VARIANTS[:2]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
