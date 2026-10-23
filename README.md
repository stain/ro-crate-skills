# RO-Crate Skills

Agent skills for working with [RO-Crate](https://w3id.org/ro/crate) (Research Object Crate), the community standard
for packaging research data, software and workflows with their metadata as `ro-crate-metadata.json` (JSON-LD
using schema.org). With these skills, Claude and other agents can create a crate for a folder of data, read and
summarise an existing crate, validate it, find the crate behind a DOI, and package or deposit it in a repository.

The skills follow the [RO-Crate 1.3 specification](https://www.researchobject.org/ro-crate/specification/1.3/) and
also read crates of versions 1.0 to 1.2. They ask you for facts about you and your project (authors, licence,
ORCIDs, funders) rather than guessing them, and never invent identifiers.

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

## What the skills run and connect to

The plugin contains only skills (instructions, reference notes and small standard-library Python scripts). It has
no hooks or MCP servers, collects no data and sends nothing anywhere by itself. When a task needs it, a skill tells
Claude to:

- install open-source RO-Crate tools from PyPI or npm (for example `rocrate`, `roc-validator`, `runcrate`,
  `signposting`, `ro-crate-html`, `ro-crate-excel`);
- fetch public web resources: DOIs, landing pages and their FAIR Signposting links, crates you point it to, and the
  RO-Crate, schema.org and Bioschemas JSON-LD contexts;
- upload a crate to Zenodo or an InvenioRDM repository with `rocrate-zenodo` / `rocrate-inveniordm`, only after you
  ask for it and confirm, starting with the sandbox. The tool reads your API token from your own configuration
  (`~/.config/zenodo.ini` for Zenodo, the `INVENIORDM_API_KEY` environment variable for InvenioRDM) and sends it
  only to that repository.

In claude.ai chat, skills that install tools or run scripts need code execution and network access; the reference
material works without them.

## Related projects

- [RO-Crate tools](https://www.researchobject.org/ro-crate/tools) listed by the RO-Crate community.
- [stain/data-preparation-skills](https://github.com/stain/data-preparation-skills): skills for reproducible data preparation, including RO-Crate provenance for data files.
- [sanskritsuthar/workflowhub-skills](https://github.com/sanskritsuthar/workflowhub-skills): skills for finding, inspecting and citing workflows in WorkflowHub.

## Layout and installation

Skills follow the open Agent Skills layout (`skills/<name>/SKILL.md`), shared by all agents. Plugin manifests live in `.claude-plugin/`, `.codex-plugin/` and `.github/plugin/`.

> The commands below follow each agent's documented conventions but have not yet been tested against this repository (see [PLAN.md](PLAN.md)); agent CLIs change, so check their docs if a command fails.

### Claude (claude.ai, Cowork and Claude Code)
Add **RO-Crate Skills** from the directory under **Customize > Plugins** on claude.ai, once it is listed there. It then also loads in Claude Code.

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

## Development and testing

See [AGENTS.md](AGENTS.md) for how to work on the skills, [TESTING.md](TESTING.md) for the checks and evals, and [PLAN.md](PLAN.md) for status and remaining work. Tool runs are recorded in `tests/eval-results/` and [tool-evaluation.md](skills/ro-crate-tools/references/tool-evaluation.md). Issues and suggestions: <https://github.com/stain/ro-crate-skills/issues>.

## License

Apache-2.0, see [LICENSE](LICENSE) and [NOTICE](NOTICE). This repository derives from the RO-Crate specification (Apache-2.0).
