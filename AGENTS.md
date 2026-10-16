# Agent instructions

This repository holds agent skills for RO-Crate. Each skill lives in `skills/<skill-name>/SKILL.md`
(YAML frontmatter with `name` matching the directory and a `description`). Keep skills concise and
accurate to the RO-Crate 1.3 specification. Plugin manifests: `.claude-plugin/`, `.codex-plugin/`,
`.github/plugin/` — keep versions in sync when changing them.

## Working on this repository

- Add a skill: create `skills/<skill-name>/SKILL.md` (lowercase-hyphenated name equal to the directory; `description` says what it does and when to use it). Then list it in the README skills table.
- Keep YAML frontmatter valid: quote scalar values when needed, especially descriptions containing a colon followed by a space (for example, `description: "Placeholder: ..."`).
- Keep skills short, procedural and spec-accurate; link to https://www.researchobject.org/ro-crate/specification/1.3/ rather than copying it. Never invent identifiers (ORCIDs, DOIs) in examples that look real.
- Bump `version` identically in `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json`, `.github/plugin/plugin.json` and `.github/plugin/marketplace.json`.
- Validate: every manifest must parse (`python -m json.tool <file>`), and each `SKILL.md` must have frontmatter `name` and `description`.
- Run `python tests/check_repo.py` before committing; see [TESTING.md](TESTING.md).
- License is MIT; do not add content you cannot license that way.
