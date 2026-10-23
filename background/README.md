# Background material

Reference material for people and agents *developing* the skills. It is not itself a skill, and no skill links to it
(it is copied with the plugin because the plugin is the whole repository). Start from the summaries, then read only
the relevant line ranges of the full text.

## Specification versions

| Version | Permalink | Full text | Summary | Zenodo |
|---|---|---|---|---|
| 1.3 | <https://w3id.org/ro/crate/1.3> | [ro-crate-1.3/](ro-crate-1.3/) (one file per chapter; [index.md](ro-crate-1.3/index.md), [quick-reference.md](ro-crate-1.3/quick-reference.md)) | [ro-crate-1.3.0-summary.md](ro-crate-1.3.0-summary.md) (**start here**: general principles, section index, per-skill reading list, checklist) | <https://doi.org/10.5281/zenodo.20720080> |
| 1.2 | <https://w3id.org/ro/crate/1.2> | [ro-crate-1.2/](ro-crate-1.2/) (one file per chapter; [index.md](ro-crate-1.2/index.md), [quick-reference.md](ro-crate-1.2/quick-reference.md)) | [ro-crate-1.2.0-summary.md](ro-crate-1.2.0-summary.md) | <https://doi.org/10.5281/zenodo.13751027> |
| 1.1 | <https://w3id.org/ro/crate/1.1> | [ro-crate-1.1.md](ro-crate-1.1.md) | [ro-crate-1.1-summary.md](ro-crate-1.1-summary.md) | <https://doi.org/10.5281/zenodo.7867028> |
| 1.0 | <https://w3id.org/ro/crate/1.0> | [ro-crate-1.0.md](ro-crate-1.0.md) | [ro-crate-1.0-summary.md](ro-crate-1.0-summary.md) | <https://doi.org/10.5281/zenodo.3541888> |

Permalinks are the values used in a crate's `conformsTo` (and as base for `@context`: `<permalink>/context`). All versions:
<https://doi.org/10.5281/zenodo.3406497>.

How the full texts were obtained:
- 1.3 and 1.2: the project's all-in-one Markdown (`ro-crate-1.3.0.md`, `ro-crate-1.2.0.md`), downloaded unmodified from Zenodo,
  then split into one file per chapter by [split_spec.py](split_spec.py), with the file names the specification uses on
  GitHub (`docs/_specification/<version>/`). The text is unchanged except that links to a section in another chapter
  point at that chapter's file (`](data-entities.md#web-based-data-entities)`); line N of a chapter is line
  (chapter start + N - 1) of the all-in-one file. Each folder also has `quick-reference.md`, the
  [quick reference](ro-crate-quick-reference-1.2-1.3.md) with its links rewritten to the chapter files. The chapter files
  are what agents read; the script and the all-in-one files are only needed again for a new specification version:
  download the all-in-one Markdown into this folder (it is in `.gitignore`), then run
  `python split_spec.py ro-crate-X.Y.Z.md ro-crate-X.Y/ ro-crate-quick-reference-1.2-1.3.md`. The split keeps every file
  under 256 KiB, the limit above which Anthropic's plugin directory holds a plugin version for a reviewer.
- 1.1 and 1.0: Zenodo has no Markdown; converted from the record's single-page HTML (`ro-crate-1.1.2.html`, `ro-crate-1.0.0.html`)
  with pandoc (see the notes in each summary). The 1.1 record is version 1.1.3 but its HTML carries the 1.1.2 text.

## Differences between versions

| File | What |
|---|---|
| [ro-crate-version-differences.md](../skills/ro-crate-compatibility/references/version-differences.md) | Permalinks, comparison table 1.0 → 1.3, migration checklists |
| [ro-crate-whats-changed-in-1.2.md](ro-crate-whats-changed-in-1.2.md) | Project guide, https://www.researchobject.org/ro-crate/whats-changed-in-1-2 |
| [ro-crate-whats-changed-in-1.3.md](ro-crate-whats-changed-in-1.3.md) | Project guide, https://www.researchobject.org/ro-crate/whats-changed-in-1-3 |
| [ro-crate-quick-reference-1.2-1.3.md](ro-crate-quick-reference-1.2-1.3.md) | All explicit requirements with severities, https://www.researchobject.org/ro-crate/quick-reference |

## Licence

The specification texts are Copyright 2017-2025 University of Technology Sydney, The University of Manchester UK and the
RO-Crate contributors, licensed under the Apache License 2.0 (<http://www.apache.org/licenses/LICENSE-2.0>); their JSON-LD
contexts and examples are CC0. The website pages are from the Apache-2.0 repository <https://github.com/ResearchObject/ro-crate>.
The copies here are unmodified apart from format conversion and stay under those terms. This repository is also Apache-2.0
(see [../NOTICE](../NOTICE)). The summaries and the differences file are original text. Skills should link to the spec rather
than copy it (see [../AGENTS.md](../AGENTS.md)).
