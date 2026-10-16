#!/usr/bin/env python3
"""Structural checks: manifests parse and agree, skills follow the Agent Skills layout,
evals are well formed, no placeholders or -DRAFT URIs, relative links resolve."""
import json, pathlib, re, sys

root = pathlib.Path(__file__).resolve().parent.parent
errors = []

# --- manifests -----------------------------------------------------------
versions = {}
licenses = {}
for m in [".claude-plugin/plugin.json", ".claude-plugin/marketplace.json",
          ".codex-plugin/plugin.json", ".github/plugin/plugin.json",
          ".github/plugin/marketplace.json"]:
    try:
        d = json.loads((root / m).read_text())
    except Exception as e:
        errors.append(f"{m}: {e}")
        continue
    versions[m] = d.get("version") or d["plugins"][0]["version"]
    if "license" in d:
        licenses[m] = d["license"]
if len(set(versions.values())) > 1:
    errors.append(f"manifest versions differ: {versions}")
if set(licenses.values()) - {"Apache-2.0"}:
    errors.append(f"manifest license is not Apache-2.0: {licenses}")

# --- skills --------------------------------------------------------------
ALLOWED_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
readme = (root / "README.md").read_text()
skills = sorted((root / "skills").glob("*/SKILL.md"))
for s in skills:
    d = s.parent
    name = d.name
    text = s.read_text()
    fm = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not fm:
        errors.append(f"{name}: missing frontmatter")
        continue
    fields = dict(l.split(": ", 1) for l in fm.group(1).splitlines() if re.match(r"^[a-z-]+: ", l))
    if fields.get("name") != name:
        errors.append(f"{name}: frontmatter name {fields.get('name')!r} != directory")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
        errors.append(f"{name}: name must be lowercase-hyphenated, at most 64 characters")
    desc = fields.get("description", "")
    if not desc:
        errors.append(f"{name}: missing description")
    elif len(desc) > 1024:
        errors.append(f"{name}: description longer than 1024 characters")
    extra = set(fields) - ALLOWED_KEYS
    if extra:
        errors.append(f"{name}: non-portable frontmatter keys {sorted(extra)}")
    if f"skills/{name}/SKILL.md" not in readme:
        errors.append(f"{name}: not listed in README")
    if text.count("\n") > 500:
        errors.append(f"{name}: SKILL.md longer than 500 lines; move detail to references/")
    for f in d.rglob("*"):
        if f.is_file() and f.suffix in {".md", ".json", ".py"}:
            body = f.read_text()
            rel = f.relative_to(root)
            if re.search(r"\d-DRAFT", body):
                errors.append(f"{rel}: uses a -DRAFT specification/profile URI")
            if "placeholder" in body.lower() and f.name == "SKILL.md":
                errors.append(f"{rel}: placeholder text in a shipped skill")
            if f.suffix == ".md":
                for link in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", body):
                    if not re.match(r"[a-z]+:", link) and not (f.parent / link).exists():
                        errors.append(f"{rel}: broken relative link {link}")
        if f.suffix == ".py":
            try:
                compile(f.read_text(), str(f), "exec")
            except SyntaxError as e:
                errors.append(f"{f.relative_to(root)}: {e}")
    ev = d / "evals" / "evals.json"
    if ev.exists():
        try:
            data = json.loads(ev.read_text())
            if data.get("skill_name") != name:
                errors.append(f"{name}: evals skill_name mismatch")
            ids = [e.get("id") for e in data.get("evals", [])]
            if not ids or len(ids) != len(set(ids)):
                errors.append(f"{name}: evals ids missing or not unique")
            for e in data["evals"]:
                if not e.get("prompt") or not e.get("expectations"):
                    errors.append(f"{name}: eval {e.get('id')} lacks prompt or expectations")
        except Exception as e:
            errors.append(f"{name}: evals.json: {e}")
    else:
        errors.append(f"{name}: no evals/evals.json")

print(f"checked {len(skills)} skills")
for e in errors:
    print("ERROR:", e)
sys.exit(1 if errors else 0)
