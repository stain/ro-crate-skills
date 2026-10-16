#!/usr/bin/env python3
"""Structural checks: manifests parse, versions match, SKILL.md frontmatter is valid."""
import json, pathlib, re, sys

root = pathlib.Path(__file__).resolve().parent.parent
errors = []

versions = {}
for m in [".claude-plugin/plugin.json", ".claude-plugin/marketplace.json",
          ".codex-plugin/plugin.json", ".github/plugin/plugin.json",
          ".github/plugin/marketplace.json"]:
    try:
        d = json.loads((root / m).read_text())
    except Exception as e:
        errors.append(f"{m}: {e}")
        continue
    versions[m] = d.get("version") or d["plugins"][0]["version"]
if len(set(versions.values())) > 1:
    errors.append(f"manifest versions differ: {versions}")

skills = sorted((root / "skills").glob("*/SKILL.md"))
readme = (root / "README.md").read_text()
for s in skills:
    name = s.parent.name
    fm = re.match(r"---\n(.*?)\n---\n", s.read_text(), re.S)
    if not fm:
        errors.append(f"{name}: missing frontmatter")
        continue
    fields = dict(l.split(": ", 1) for l in fm.group(1).splitlines() if ": " in l)
    if fields.get("name") != name:
        errors.append(f"{name}: frontmatter name {fields.get('name')!r} != directory")
    if not fields.get("description"):
        errors.append(f"{name}: missing description")
    if f"skills/{name}/SKILL.md" not in readme:
        errors.append(f"{name}: not listed in README")

print(f"checked {len(skills)} skills")
for e in errors:
    print("ERROR:", e)
sys.exit(1 if errors else 0)
