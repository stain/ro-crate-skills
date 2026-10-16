# Testing the skills

Skills are prose for agents, so testing has three layers.

## 1. Structural checks (automated)
```bash
python tests/check_repo.py
```
Checks that manifests parse and share one version, and that each `skills/*/SKILL.md` has frontmatter `name` (equal to its directory) and `description`, and is listed in the README.

## 2. Fixtures
`tests/fixtures/` holds tiny crates:
- `minimal-crate/`: should pass `rocrate-validator validate -p ro-crate-1.3` at REQUIRED level.
- `invalid-crate/`: lacks `description`, `datePublished`, `license` and links a missing file; the validator should report REQUIRED failures.

(The validator needs network access to fetch the JSON-LD context. The expected results above are not yet confirmed by a run.)

## 3. Behavioural tests with example crates
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
