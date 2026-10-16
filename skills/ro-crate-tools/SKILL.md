---
name: ro-crate-tools
description: Choose and use common RO-Crate tools (ro-crate-py, ro-crate-js/Describo, ro-crate-java, crate-o, rocrate-validator, WorkflowHub, Galaxy, runcrate) to create, validate, convert, or preview RO-Crates. Use when asked how to validate an RO-Crate or which tooling fits a task.
---

# RO-Crate tools

Catalogue: https://www.researchobject.org/ro-crate/tools — check it for the current list.

| Task | Tool |
|---|---|
| Create/read/modify crates in Python | `ro-crate-py` (`pip install rocrate`; CLI `rocrate init`, `rocrate add ...`) |
| Validate against spec & profiles | `rocrate-validator` (`pip install roc-validator`; `rocrate-validator validate <path>`) |
| JavaScript/TypeScript libraries | `ro-crate-js` (`npm install ro-crate`), `ro-crate-html-js` for previews |
| Interactive editing / desktop | Describo, Crate-O (browser editor, schema-driven) |
| Java | `ro-crate-java` |
| Workflow provenance | `runcrate`, `autosubmit`, Galaxy and Nextflow/Snakemake/cwltool exports (Workflow Run Crate) |
| Registry / publishing | WorkflowHub, Zenodo (RO-Crate import), Dataverse |

## Guidance
- Prefer a validator over hand-checking; run it after any generation or edit and report failures verbatim.
- Install tools in a virtualenv; confirm command names with `--help` since CLIs change.
- Use `rocrate init` to bootstrap metadata from an existing directory, then enrich by hand.
- Always parse generated JSON (`python -m json.tool ro-crate-metadata.json`) as a basic sanity check when no validator is available.

## Tool-specific skills
Prefer these over writing new code: `ro-crate-py`, `ro-crate-validator`, `ro-crate-preview`, `ro-crate-js`, `ro-crate-editors`, `ro-crate-repositories`.
Related external skills: https://github.com/stain/data-preparation-skills (ro-crate-provenance), https://github.com/sanskritsuthar/workflowhub-skills (workflowhub-*, ro-crate-consume).
