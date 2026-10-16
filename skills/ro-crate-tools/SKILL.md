---
name: ro-crate-tools
description: Choose and use RO-Crate tools: libraries for Python, JavaScript, Java, R and others; editors (Describo, Crate-O, NovaCrate); HTML preview generators (rochtml); workflow-run exporters (Nextflow, Galaxy); repository uploaders. Use when the user asks which tool fits, how to preview or edit a crate in a GUI, or how to convert, export or deposit crates with existing tooling instead of writing code. For Python scripting see ro-crate-py; for validation see ro-crate-validator.
---

# RO-Crate tools

Authoritative, changing list with status labels: https://www.researchobject.org/ro-crate/tools . Check it before recommending a tool; most are alpha/beta. Install tools in a virtualenv/`npm` prefix and confirm commands with `--help`.

| Task | Tool (status on the tools list) |
|---|---|
| Create/read/modify crates, Python | `ro-crate-py` (beta): see the `ro-crate-py` skill |
| Validate against spec and profiles | `rocrate-validator` / `roc-validator` (beta): see the `ro-crate-validator` skill |
| JavaScript / other languages | `ro-crate-js` (`npm install ro-crate`, beta), ro-crate-java, rocrateR, ro-crate-ruby, ro-crate-rs: [references/js-and-editors.md](references/js-and-editors.md) |
| Interactive editing | Describo (production), NovaCrate (production), Crate-O (beta), RO-Crate Playground: [references/js-and-editors.md](references/js-and-editors.md) |
| HTML preview | `rochtml` from `npm install ro-crate-html`; `rocrate init --gen-preview`: [references/preview.md](references/preview.md) |
| Spreadsheets to crates | `ro-crate-excel` (beta), RO-Crates-and-Excel profile |
| Workflow crates and run provenance | `nf-core` RO-Crate tool and `nf-prov` (Nextflow, production), `galaxy2cwl` (alpha), PyCOMPSs CLI `inspect`, `rocrate-action-recorder` (record CLI calls from Python, beta) |
| Resolve a PID to its crate (Signposting) | `signposting` (PyPI, beta): `signposting <url>` prints CiteAs/DescribedBy/Item links; see `ro-crate-retrieve` |
| Deposit to repositories | `ro-crate-zenodo` (alpha), `ro-crate-inveniordm` (alpha); WorkflowHub accepts Workflow RO-Crates (`*.crate.zip`) |
| Browse/search | Bowerbird (offline), Oni UI, RO-Crate Explorer, `ro-crate-tabulator` (crate to tables) |
| Profiles | RO-Crate Profile Portal https://profiles.ro-crate.org/ , Profile Crate Creator (ROCratePCC, beta) |

## Guidance
- Prefer an existing tool over new code, then **review its output**: tools often emit crates that lack `name`, `description`, `license` or authors.
- Always validate after any generation or edit and report failures verbatim. Without network: `python -m json.tool ro-crate-metadata.json` is only a syntax check.
- Deprecated per the tools list: CheckMyCrate, ro-crate-validator-py; inactive: ro-crates-deposit (use ro-crate-inveniordm).
- If no listed tool fits, follow the `ro-crate-create` skill and write the JSON-LD directly.
