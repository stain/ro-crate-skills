# ro-crate-skills
Agentic skills for RO-Crate

## Skills

| Skill | Purpose |
|---|---|
| [`ro-crate-consume`](skills/ro-crate-consume/SKILL.md) | Read and interpret an existing RO-Crate |
| [`ro-crate-create`](skills/ro-crate-create/SKILL.md) | Create/edit `ro-crate-metadata.json` per RO-Crate 1.3 |
| [`ro-crate-tools`](skills/ro-crate-tools/SKILL.md) | Pick and use common RO-Crate tools and validators |

Based on the [RO-Crate 1.3 specification](https://www.researchobject.org/ro-crate/specification/1.3/) and the [tools list](https://www.researchobject.org/ro-crate/tools).

## Layout and installation

Skills follow the open Agent Skills layout (`skills/<name>/SKILL.md`), shared by all agents:

- **Claude Code**: `/plugin marketplace add stain/ro-crate-skills` then `/plugin install ro-crate-skills@ro-crate-skills` (`.claude-plugin/`)
- **GitHub Copilot CLI**: `copilot plugin marketplace add stain/ro-crate-skills` (`.github/plugin/`), or copy `skills/` into `.github/skills/`
- **Codex**: plugin manifest in `.codex-plugin/`; or copy skills to `.agents/skills/`
