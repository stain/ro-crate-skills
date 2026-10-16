# Testing the skills

Skills are prose for agents, so testing has three layers.

## 1. Structural checks (automated)
```bash
python tests/check_repo.py
```
Checks that manifests parse and share one version, and that each `skills/*/SKILL.md` has portable frontmatter (`name` equal to its directory, `description` up to 1024 characters, no Claude-only keys), is listed in the README, has no placeholder text, stays under 500 lines, has working relative links and a valid `evals/evals.json`, and that no skill file uses a `-DRAFT` spec/profile URI. Unit tests for the lint script: `python -m unittest tests.test_lint`.

## 2. Fixtures
`tests/fixtures/` holds tiny crates:
- `minimal-crate/`: should pass `rocrate-validator validate -p ro-crate-1.3` at REQUIRED level.
- `invalid-crate/`: lacks `description`, `datePublished`, `license` and links a missing file; the validator should report REQUIRED failures.

Confirmed with roc-validator 0.12.2 (2026-10-16): `rocrate-validator validate -p ro-crate-1.3 --requirement-severity REQUIRED tests/fixtures/minimal-crate` exits 0 (63 checks passed, 3 skipped); the same on `invalid-crate` exits 1 with three REQUIRED failures (description, license, datePublished). It does not report the missing `missing.txt`; `skills/ro-crate-validator/scripts/lint_crate.py` does. Whether the validator works without network access is not yet confirmed.

## 3. Evals (per skill)
Each skill has `evals/evals.json` (prompts with `expectations`, the format used by the skill-creator plugin). Any agent can run the prompts by hand or in CI and compare the answer with the expectations; Claude Code users can also use the skill-creator plugin's viewer, benchmark and description optimiser (these need Claude Code). Prompts that name `tests/fixtures/...` expect to run from the repository root.

## 4. Behavioural tests with example crates
Give an agent a prompt with the skill installed, then check the answer against the crate (consume skills) or validate the output (create skills). Suggested prompts:
- Consume: "Summarise this crate: title, authors, license, files, and which profiles it conforms to." Compare with the metadata.
- Consume a failing crate: the agent must validate first and report failures and cautions.
- Create: "Package this directory as an RO-Crate" then run `rocrate-validator`; the agent must also check the result against the spec, not only the validator.
- Compatibility: give a 1.0/1.1 crate and ask what to change for 1.3.
- Retrieve: give a DOI/landing-page URL and ask for the crate (signposting).

### Example crate sources
- Workflow Run RO-Crate examples: https://www.researchobject.org/workflow-run-crate/ (Process/Workflow/Provenance Run Crate; verify the links on that page)
- Use cases and published crates: https://www.researchobject.org/ro-crate/use_cases
- Specification examples: https://www.researchobject.org/ro-crate/specification/1.3/
- WorkflowHub: https://workflowhub.eu/
- Related skill repos with their own tests: https://github.com/sanskritsuthar/workflowhub-skills (`TESTING.md`), https://github.com/stain/data-preparation-skills

**Caveat:** crates from use-case pages may use older spec versions or be non-compliant. Record the spec version and validator result for each example you adopt; do not treat the validator as the sole oracle.

Do not commit large third-party crates; reference them by URL or download in a script, and check their licences.
