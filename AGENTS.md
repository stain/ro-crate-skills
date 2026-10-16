# Agent instructions

This repository holds agent skills for RO-Crate. Each skill lives in `skills/<skill-name>/SKILL.md`
(YAML frontmatter with `name` matching the directory and a `description`). Keep skills concise and
accurate to the RO-Crate 1.3 specification. Plugin manifests: `.claude-plugin/`, `.codex-plugin/`,
`.github/plugin/` — keep versions in sync when changing them.

## Working on this repository

- Before writing or revising a skill, read [background/ro-crate-1.3.0-summary.md](background/ro-crate-1.3.0-summary.md) (principles, section index, which spec lines each skill needs), then the relevant ranges of `background/ro-crate-1.3.0.md`. For older versions or migration see [background/ro-crate-version-differences.md](background/ro-crate-version-differences.md) and the 1.0/1.1/1.2 summaries beside it.

- **Never use unreleased `-DRAFT` specifications, contexts or `conformsTo` values** in skills, examples, fixtures or generated crates: no `https://w3id.org/ro/crate/1.x-DRAFT[/context]`, no `...-DRAFT` profile URIs (e.g. Bioschemas `0.5-DRAFT-2020_07_21`; use the `1.0-RELEASE` profiles), and no draft/unreleased versions of any profile. Use released versions only (RO-Crate 1.0-1.3, default 1.3). When *reading* a crate that declares a draft, report it as unreleased and do not copy it into new output. Some spec tables still show `1.2-DRAFT` leftovers; do not copy them.
- Add a skill: create `skills/<skill-name>/SKILL.md` (lowercase-hyphenated name equal to the directory; `description` says what it does and when to use it). Then list it in the README skills table.
- Keep skills short, procedural and spec-accurate; link to https://www.researchobject.org/ro-crate/specification/1.3/ rather than copying it. Never invent identifiers (ORCIDs, DOIs) in examples that look real.
- Bump `version` identically in `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json`, `.github/plugin/plugin.json` and `.github/plugin/marketplace.json`.
- Validate: every manifest must parse (`python -m json.tool <file>`), and each `SKILL.md` must have frontmatter `name` and `description`.
- Run `python tests/check_repo.py` before committing; see [TESTING.md](TESTING.md).
- License is Apache-2.0 (the repository derives from the Apache-2.0 RO-Crate specification; see NOTICE); do not add content you cannot license that way.
