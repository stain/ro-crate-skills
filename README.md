# ro-crate-skills
Agentic skills for RO-Crate

## Skills

| Skill | Purpose |
|---|---|
| [`ro-crate-consume`](skills/ro-crate-consume/SKILL.md) | Read, summarise and check an existing crate (any version), safely |
| [`ro-crate-create`](skills/ro-crate-create/SKILL.md) | Create/edit `ro-crate-metadata.json` (1.3 default); references for data/contextual entities, JSON-LD, provenance |
| [`ro-crate-validator`](skills/ro-crate-validator/SKILL.md) | Validate: offline lint script, `rocrate-validator`, semantic review |
| [`ro-crate-spec`](skills/ro-crate-spec/SKILL.md) | Answer questions about the specification; principles and where to look |
| [`ro-crate-compatibility`](skills/ro-crate-compatibility/SKILL.md) | Differences between 1.0-1.3 and upgrade steps |
| [`ro-crate-profiles`](skills/ro-crate-profiles/SKILL.md) | Find, declare and author profiles and Profile Crates |
| [`ro-crate-workflows`](skills/ro-crate-workflows/SKILL.md) | Workflow RO-Crate and Workflow/Process/Provenance Run Crates |
| [`ro-crate-bioschemas`](skills/ro-crate-bioschemas/SKILL.md) | Bioschemas profiles and types in crates: released profiles, `conformsTo`, terms missing from the context |
| [`ro-crate-retrieve`](skills/ro-crate-retrieve/SKILL.md) | Resolve a DOI/URL (Signposting) to a crate; follow referenced crates |
| [`ro-crate-publish`](skills/ro-crate-publish/SKILL.md) | Zip/BagIt/.eln, attached vs detached, serving, PIDs, deposit |
| [`ro-crate-py`](skills/ro-crate-py/SKILL.md) | Use `rocrate` (ro-crate-py) CLI and library |
| [`ro-crate-tools`](skills/ro-crate-tools/SKILL.md) | Pick tools: libraries, editors, preview, exporters, uploaders |
| [`ro-crate-runcrate`](skills/ro-crate-runcrate/SKILL.md) | Report on, replay or convert Workflow Run Crates with `runcrate` |
| [`ro-crate-action-recorder`](skills/ro-crate-action-recorder/SKILL.md) | Record Python CLI runs as Process Run Crate provenance |
| [`ro-crate-tabulate`](skills/ro-crate-tabulate/SKILL.md) | Crate to SQLite/CSV with `rocrate-tabular` |
| [`ro-crate-js`](skills/ro-crate-js/SKILL.md) | `ro-crate` npm library for Node.js |
| [`ro-crate-excel`](skills/ro-crate-excel/SKILL.md) | Folder or spreadsheet to crate with `rocxl` (needs Siegfried) |
| [`ro-crate-deposit`](skills/ro-crate-deposit/SKILL.md) | Deposit to Zenodo/InvenioRDM with `rocrate-zenodo` / `rocrate-inveniordm` |

Each skill folder holds `SKILL.md` (frontmatter `name` and `description` only, so any Agent Skills reader works), optional `references/` (read on demand), optional `scripts/` (standard-library Python) and `evals/evals.json` (test prompts with expectations). Ideas for further skills (profile discovery, format conversion, recording agent work as provenance) are in [PLAN.md](PLAN.md).

## Status (v0.1)
Seventeen skills; tools were run and results recorded in `tests/eval-results/` and `skills/ro-crate-tools/references/tool-evaluation.md`. Evals are single runs graded by hand; trigger accuracy of the descriptions, other agents and weaker models are untested. All skills share one rule, [`tests/do_not_guess.txt`](tests/do_not_guess.txt): ask rather than guess facts about the user or project, never invent identifiers, use `TODO:` for unavoidable gaps.

## Related skill repositories

Existing drafts to link to or align with rather than duplicate:

- [stain/data-preparation-skills](https://github.com/stain/data-preparation-skills): `ro-crate-provenance` (RO-Crate 1.3 + Process Run Crate for data files; fuller than our placeholder, so our `ro-crate-provenance` should link to it), `reproducible-data-preparation`, `data-license-investigation`, `snakemake-data-pipeline`.
- [sanskritsuthar/workflowhub-skills](https://github.com/sanskritsuthar/workflowhub-skills): `ro-crate-consume`, `workflowhub-find`, `workflowhub-inspect`, `workflowhub-explain`, `workflowhub-evaluate`, `workflowhub-cite`, `fair-signposting`. Overlaps with our `ro-crate-consume`, `ro-crate-workflows` and `ro-crate-repositories`.
- [alexhambley/RO-Crate-RAG-Validator](https://github.com/alexhambley/RO-Crate-RAG-Validator) (BSD-3-Clause): experimental Streamlit/CLI tool that validates each entity against profile Markdown using RAG and an LLM (needs your own chat and embeddings API keys). Optional and not a dependency: it checks entities one at a time and gives non-deterministic results, so run `rocrate-validator` first. Its ideas (compliance vs usefulness, fixes as add/replace/remove operations, audience from the root) are used in `ro-crate-validator`.

Open question: whether to depend on, vendor, or only link to the first two.

Based on the [RO-Crate 1.3 specification](https://www.researchobject.org/ro-crate/specification/1.3/) and the [tools list](https://www.researchobject.org/ro-crate/tools).

## Layout and installation

Skills follow the open Agent Skills layout (`skills/<name>/SKILL.md`), shared by all agents. Plugin manifests live in `.claude-plugin/`, `.codex-plugin/` and `.github/plugin/`.

> The commands below follow each agent's documented conventions but have not yet been tested against this repository (see [PLAN.md](PLAN.md)); agent CLIs change, so check their docs if a command fails.

### Claude Code
```text
/plugin marketplace add stain/ro-crate-skills
/plugin install ro-crate-skills@ro-crate-skills
```
Or, without the plugin, copy a skill folder into `~/.claude/skills/` (all projects) or `.claude/skills/` (one project).

### GitHub Copilot (CLI and VS Code)
```text
copilot plugin marketplace add stain/ro-crate-skills
copilot plugin install ro-crate-skills@ro-crate-skills
```
Or copy skill folders into `.github/skills/` in your repository (or `~/.copilot/skills/` for personal use).

### OpenAI Codex
Install via the plugin manifest in `.codex-plugin/`, or copy skill folders into `.agents/skills/` in your repository (or `~/.agents/skills/` for personal use).

### Other agents
Any agent supporting Agent Skills can use the folders in `skills/` directly: copy or symlink them into that agent's skills directory.

### Using the skills
Skills are picked up automatically when your request matches a skill's `description`, e.g. "validate this RO-Crate" or "create an RO-Crate for this folder". You can also name a skill explicitly in your prompt, for example "use the ro-crate-validator skill".

## Testing

See [TESTING.md](TESTING.md). Remaining work: see [PLAN.md](PLAN.md).

## License

Apache-2.0, see [LICENSE](LICENSE) and [NOTICE](NOTICE). This repository derives from the RO-Crate specification (Apache-2.0).
