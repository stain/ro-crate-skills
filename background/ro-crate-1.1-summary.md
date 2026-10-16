# RO-Crate 1.1 specification: summary and section index

Companion to [`ro-crate-1.1.md`](ro-crate-1.1.md). Not normative: check the spec text.

| | |
|---|---|
| Permalink | <https://w3id.org/ro/crate/1.1> (descriptor `conformsTo`) |
| JSON-LD context | <https://w3id.org/ro/crate/1.1/context> |
| Published | 2022-01-19 (1.1.0); patch releases 1.1.1-1.1.3 |
| Zenodo | <https://doi.org/10.5281/zenodo.7867028> (record version 1.1.3, 2023-04-26); the text in the record's HTML is the 1.1.2 release (<https://doi.org/10.5281/zenodo.5841615>); any version: <https://doi.org/10.5281/zenodo.3406497> |
| Previous / next | [1.0](https://w3id.org/ro/crate/1.0) / [1.2](https://w3id.org/ro/crate/1.2) |
| Descriptor `@id` | `ro-crate-metadata.json` (legacy `ro-crate-metadata.jsonld` still accepted when reading) |

**Source format.** Zenodo has no Markdown for 1.1 (only HTML and PDF). `ro-crate-1.1.md` was converted from the
record's `ro-crate-1.1.2.html` with pandoc (`-t markdown`, ATX headings; the leading table of contents was removed).
Headings are numbered as in the HTML; code fences use `{.sourceCode .json}` attributes. Line numbers refer to the
converted file. The patch releases are errata only; see the changelog (line 1582).

## What 1.1 is

The general principles of [1.3](ro-crate-1.3.0-summary.md) (flattened/compacted JSON-LD, `{"@id"}` references,
schema.org first, data vs contextual entities, not a manifest) already apply. 1.1 is a **single-kind crate**: a directory
(the root) with a metadata file. There are no Detached packages, profiles or Profile Crates, `mainEntity` focus
section, retrieval algorithm or `cite-as`.

- **Metadata file** `ro-crate-metadata.json` (renamed from `.jsonld` in 1.1 to ease JSON editors); readers should
  still accept `ro-crate-metadata.jsonld` from 1.0 crates and rename it when updating.
- **Descriptor** `CreativeWork`, `about` the root, `conformsTo` a versioned `https://w3id.org/ro/crate/1.1`; in 1.1 `conformsTo` MAY be an
  array that also lists profiles (1.2 moved profile declarations to the root).
- **Finding the root** (line 322): the entity whose `conformsTo` starts with `https://w3id.org/ro/crate/`
  gives the root via `about` (replaced by the descriptor-`@id` lookup in 1.2).
- **Root Data Entity** (line 342): `@type` Dataset; `@id` MUST end with `/`, SHOULD be `./`; `datePublished`
  (ISO 8601), `name`, `description`, `license` (all MUST be present; content SHOULD be descriptive). The root MAY now be an absolute URI (a 1.1 change).
- **Data entities** (line 391): files, directories, **web resources** (new: absolute-URI `File`/`Dataset`, and
  online databases as `CreativeWork`); `hasPart` from root; `sdDatePublished` for web files; `url`/`identifier`/
  `subjectOf`/`mainEntityOfPage` for entities also on the web (1.2 prefers `contentUrl` for downloads). Paths must be
  percent-encoded.
- **Contextual entities** (line 675), **provenance** (line 1012), **workflows** (line 1275): workflows use
  `@type` `File`, `SoftwareSourceCode`, `ComputationalWorkflow` (1.0 used `Workflow`/`Script`) and align with the
  Bioschemas ComputationalWorkflow 0.5-DRAFT / FormalParameter 0.1-DRAFT profiles (1.2+ use 1.0-RELEASE).
- **JSON-LD context** no longer sets `@base: null`; the relative-URI appendix (line 2105) explains `@base` handling.
- Appendices: BagIt (line 1674), repository identifiers (1810), JSON-LD / context / media type / extending (1838),
  relative URIs (2105).

## Section index (lines in `ro-crate-1.1.md`)

| Topic | Line |
|---|---|
| Header / Introduction / Terminology | 1 / 29 / 39 |
| Structure (metadata file 100, website 128, payload 160, self-describing 166) | 85 |
| Metadata (principles 192, schema.org 210, other vocabularies 231, identifiers 279) | 180 |
| Root Data Entity (descriptor 297, finding root 322, properties 342, minimal example 357) | 291 |
| Data Entities (encodings 469, web-based 552, also-on-web 619, distributions 649) | 391 |
| Contextual Entities (people 705, licence 934, metadata licence 982) | 675 |
| Provenance (equipment 1014, software 1062, changes 1125, repositories 1204) | 1012 |
| Workflows and Scripts (Bioschemas 1421, example 1462) | 1275 |
| Changelog | 1582 |
| Implementation notes (BagIt 1674) | 1652 |
| RO-Crate JSON-LD (context 1914, media type 1976, extending 2019, ad hoc terms 2049) | 1838 |
| Relative URI references (ZIP base 2474, relativizing 2542) | 2105 |
