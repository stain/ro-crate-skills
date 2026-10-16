# Plan: developing and testing the skills

Status as of the initial scaffold. Read [AGENTS.md](AGENTS.md) and [TESTING.md](TESTING.md) first.
Default target: RO-Crate 1.3. Run `python tests/check_repo.py` before every commit.

## Cross-cutting first steps
1. **Verify every URL.** The authoring environment had no access to researchobject.org, w3id.org or PyPI. All spec URLs (pages use `.html`, e.g. `.../specification/1.3/profiles.html`) and tool URLs were written from memory. Fix wrong ones, and confirm the `#referencing-other-ro-crate` anchor.
2. **Run the validator.** The validator commands and the expected results for `tests/fixtures/` (minimal passes, invalid fails with REQUIRED errors) were never executed (no network). Run them and correct `skills/ro-crate-validator/SKILL.md` and `TESTING.md`.
3. **Decide the relationship to the sibling repos** (link / depend / vendor); check licences first:
   - https://github.com/stain/data-preparation-skills (`ro-crate-provenance`, MIT per frontmatter)
   - https://github.com/sanskritsuthar/workflowhub-skills (`ro-crate-consume`, `fair-signposting`, `workflowhub-*`; licence not checked)
4. **Overlap:** our `ro-crate-consume` and `ro-crate-provenance` overlap with the above. Prefer reuse over duplicate drafting.
5. **Versioning:** bump `version` in all five manifests together when skills change meaningfully (currently 0.1.0). Manifest fields and install commands in the README (Claude, Copilot, Codex) are unverified against current plugin specs; test installing in each.
6. **CI:** consider a GitHub Action running `tests/check_repo.py` (and the validator on fixtures).
7. **Add `.agents/skills` or similar only if** a target agent needs it; check each agent's current discovery rules.

## Skills drafted but need review/testing
| Skill | Needs |
|---|---|
| `ro-crate-consume` | Check against spec 1.3 text; test on real crates incl. detached, zipped, 1.0/1.1 (`.jsonld`) crates; add validation-first step (see validator skill) |
| `ro-crate-create` | Check minimal example against 1.3 (required properties, `conformsTo` form, licence handling); test: prompt to package a directory, then validate; add mention of ro-crate-py to avoid hand-writing |
| `ro-crate-tools` | Verify tool names, package names, CLI commands; refresh against https://www.researchobject.org/ro-crate/tools |
| `ro-crate-validator` | Run every command; document real output; add known false positives (see data-preparation-skills `references/validator-findings.md`); check `--no-auto-profile`, `--skip-availability-checks`, offline use |

## Placeholders to develop (suggested priority)
**High**
1. `ro-crate-profile` and `ro-crate-profile-crate`: understand/create profiles; Profile Crate per `specification/1.3/profiles.html` (Profile entity, `conformsTo`, resource descriptors, `hasResource`, role/`Profile` type, validation).
2. `ro-crate-compatibility`: diff 1.0 → 1.1 → 1.2 → 1.3 (context URLs, `.jsonld` vs `.json` name, `conformsTo`, terms, profile type); migration checklist; how to validate against the declared version.
3. `ro-crate-py`: tested recipes (`rocrate init`, `add`, library snippets) so agents do not write new crate code.
4. `ro-crate-retrieve` + `fair-signposting`: resolve a URL/DOI/identifier to an RO-Crate (signposting Link headers, linksets, content negotiation, subcrates per `data-entities.html#referencing-other-ro-crates`). Reuse Sanskrit's `fair-signposting` where possible. Test with real repositories.
5. `ro-crate-workflows`: Workflow Crate, Workflow Run Crate, Process Run Crate, Provenance Run Crate (profile versions at https://www.researchobject.org/workflow-run-crate/). Largely link to `ro-crate-provenance` in data-preparation-skills.

**Medium**
6. `ro-crate-data-entities`, `ro-crate-contextual-entities`, `ro-crate-jsonld`: reference skills distilled from spec pages; keep short, link to the spec.
7. `ro-crate-provenance`: align with or link to data-preparation-skills version.
8. `ro-crate-preview`: `ro-crate-html-lite` / `ro-crate-html-js`; pin versions.
9. `ro-crate-packaging`, `ro-crate-repositories`: zip/detached crates, WorkflowHub/Zenodo/Dataverse; link to `workflowhub-*` skills.

**Low**
10. `ro-crate-js`, `ro-crate-editors` (Describo, Crate-O).

## Other skills to consider
- `ro-crate-testing-evaluating`: run the behavioural prompts in TESTING.md and record results.
- `ro-crate-ro-crate-vs-bagit` / format conversion (BagIt, other formats), if requested.
- Skills for specific communities' profiles (e.g. 5 Safes, ELN, Schema.org-based), after profile skills exist.

## Testing plan (see TESTING.md)
- Build a corpus of example crates (Workflow Run Crate page, use-cases page, spec examples, WorkflowHub). For each record spec version, validator result, licence, source URL. Do not commit large third-party crates; fetch by script.
- Add fixtures beyond the two present: a 1.0/1.1 crate, a detached crate, a Workflow Run Crate, a Profile Crate, a failing-but-readable crate.
- Behavioural test prompts per skill (consume, create, compatibility, retrieve) with expected outcomes; run in Claude Code, Copilot and Codex.
- Key behaviours to test: validate before consuming; read failed crates cautiously and report failures; after writing, validate **and** compare against spec/profile (the validator can be too strict); never invent ORCIDs/DOIs.

## Definition of done for a skill
- Placeholder banner removed; frontmatter `description` states what and when.
- Procedures and commands verified by running them.
- Links verified; spec version stated.
- At least one test prompt and fixture/crate in TESTING.md.
- Listed in README; `python tests/check_repo.py` passes.
