#!/usr/bin/env python3
"""Summarise several graded iterations (repeats) of the same evals.

Usage: python tests/graders/summarize.py <iteration dir> [<iteration dir> ...] [--variant with_skill]

Prints passed/total per eval for each repeat and the expectations that failed in any repeat, with the
repeats they failed in. Standard library only.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent))

from tests.graders.run import GRADERS, grade_run  # noqa: E402


def main(argv):
    variant = "with_skill"
    if "--variant" in argv:
        variant = argv[argv.index("--variant") + 1]
    dirs = [Path(a) for a in argv if not a.startswith("--") and a != variant]
    repo = HERE.parent.parent
    names = sorted({d.name[5:] for it in dirs for d in it.glob("eval-*") if d.name[5:] in GRADERS})
    cells, fails = {}, {}
    for n in names:
        for i, it in enumerate(dirs, 1):
            out = it / f"eval-{n}" / variant / "outputs"
            if not out.exists():
                continue
            res = grade_run(n, out, repo)
            cells[(n, i)] = (sum(r["passed"] for r in res), len(res))
            for r in res:
                if not r["passed"]:
                    fails.setdefault((n, r["text"]), []).append((i, r["evidence"]))
    print(f"{'eval':24s} " + " ".join(f"{'r' + str(i):>8s}" for i in range(1, len(dirs) + 1)))
    tot = [0, 0]
    for n in names:
        row = []
        for i in range(1, len(dirs) + 1):
            c = cells.get((n, i))
            row.append(f"{c[0]:>4d}/{c[1]:<3d}" if c else f"{'-':>8s}")
            if c:
                tot[0] += c[0]; tot[1] += c[1]
        print(f"{n:24s} " + " ".join(row))
    print(f"{'TOTAL':24s} {tot[0]}/{tot[1]}")
    if fails:
        print("\nExpectations that failed in at least one repeat:")
        for (n, text), items in sorted(fails.items()):
            print(f"- {n}: {text}  [repeats {[i for i, _ in items]}]")
            print(f"    e.g. {items[0][1][:150]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
