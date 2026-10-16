# ro-crate-skills
Agentic skills for RO-Crate

## Skills

| Skill | Purpose |
|---|---|
| [`ro-crate-consume`](skills/ro-crate-consume/SKILL.md) | Read and interpret an existing RO-Crate |
| [`ro-crate-create`](skills/ro-crate-create/SKILL.md) | Create/edit `ro-crate-metadata.json` per RO-Crate 1.3 |
| [`ro-crate-tools`](skills/ro-crate-tools/SKILL.md) | Pick and use common RO-Crate tools and validators |
| [`ro-crate-validator`](skills/ro-crate-validator/SKILL.md) | Validate with rocrate-validator before consuming and after generating |

### Planned (not yet installed)

Drafts live in [`skills-wip/`](skills-wip/) so that agents do not load unfinished skills; they move to `skills/` when written and tested (several will be merged first, see [PLAN.md](PLAN.md)).

| Skill | Purpose |
|---|---|
| [`ro-crate-compatibility`](skills-wip/ro-crate-compatibility/SKILL.md) | Differences between RO-Crate versions (default 1.3) |
| [`ro-crate-profile`](skills-wip/ro-crate-profile/SKILL.md) | Understand and create profiles |
| [`ro-crate-profile-crate`](skills-wip/ro-crate-profile-crate/SKILL.md) | Profile Crate specifics |
| [`ro-crate-data-entities`](skills-wip/ro-crate-data-entities/SKILL.md) | Data entities and root data entity |
| [`ro-crate-contextual-entities`](skills-wip/ro-crate-contextual-entities/SKILL.md) | People, orgs, licenses, places etc. |
| [`ro-crate-provenance`](skills-wip/ro-crate-provenance/SKILL.md) | Provenance and actions |
| [`ro-crate-workflows`](skills-wip/ro-crate-workflows/SKILL.md) | Workflow and run crates |
| [`ro-crate-jsonld`](skills-wip/ro-crate-jsonld/SKILL.md) | JSON-LD, context, relative URIs |
| [`ro-crate-packaging`](skills-wip/ro-crate-packaging/SKILL.md) | Packaging, distribution, publishing |
| [`ro-crate-py`](skills-wip/ro-crate-py/SKILL.md) | Use ro-crate-py instead of writing code |
| [`ro-crate-preview`](skills-wip/ro-crate-preview/SKILL.md) | Generate HTML previews |
| [`ro-crate-js`](skills-wip/ro-crate-js/SKILL.md) | JavaScript tooling |
| [`ro-crate-editors`](skills-wip/ro-crate-editors/SKILL.md) | Describo, Crate-O |
| [`ro-crate-repositories`](skills-wip/ro-crate-repositories/SKILL.md) | WorkflowHub, Zenodo, Dataverse |
| [`ro-crate-retrieve`](skills-wip/ro-crate-retrieve/SKILL.md) | Retrieve referenced RO-Crates |
| [`fair-signposting`](skills-wip/fair-signposting/SKILL.md) | FAIR Signposting discovery/publishing |

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
