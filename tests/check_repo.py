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

readme = (root / "README.md").read_text()


def check_skills(directory, shipped):
    paths = sorted((root / directory).glob("*/SKILL.md"))
    for s in paths:
        name = s.parent.name
        text = s.read_text()
        fm = re.match(r"---\n(.*?)\n---\n", text, re.S)
        if not fm:
            errors.append(f"{directory}/{name}: missing frontmatter")
            continue
        fields = dict(l.split(": ", 1) for l in fm.group(1).splitlines() if ": " in l)
        if fields.get("name") != name:
            errors.append(f"{directory}/{name}: frontmatter name {fields.get('name')!r} != directory")
        if not fields.get("description"):
            errors.append(f"{directory}/{name}: missing description")
        if f"{directory}/{name}/SKILL.md" not in readme:
            errors.append(f"{directory}/{name}: not listed in README")
        if shipped and "placeholder" in text.lower():
            errors.append(f"{directory}/{name}: placeholder text in a shipped skill (move to skills-wip/)")
        if re.search(r"\d-DRAFT", text):
            errors.append(f"{directory}/{name}: uses a -DRAFT specification/profile URI")
    return paths


skills = check_skills("skills", shipped=True)
wip = check_skills("skills-wip", shipped=False)
for name in {p.parent.name for p in skills} & {p.parent.name for p in wip}:
    errors.append(f"{name}: exists in both skills/ and skills-wip/")

print(f"checked {len(skills)} skills, {len(wip)} planned (skills-wip)")
for e in errors:
    print("ERROR:", e)
sys.exit(1 if errors else 0)
