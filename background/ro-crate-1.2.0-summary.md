# RO-Crate 1.2 specification: summary and section index

Companion to [`ro-crate-1.2/`](ro-crate-1.2/), the specification of RO-Crate 1.2.0 (published 2025-06-04)
with one Markdown file per chapter, split from the all-in-one Markdown on Zenodo. Not normative: check the
spec text. Line numbers refer to the chapter files (Setext-style headings; each chapter has a "Table of
contents" stub that can be ignored). [`quick-reference.md`](ro-crate-1.2/quick-reference.md) lists every
requirement by entity type, linked to the chapters.

| | |
|---|---|
| Permalink | <https://w3id.org/ro/crate/1.2> (descriptor `conformsTo`) |
| JSON-LD context | <https://w3id.org/ro/crate/1.2/context> |
| Zenodo (this version) | <https://doi.org/10.5281/zenodo.13751027> (any version: <https://doi.org/10.5281/zenodo.3406497>) |
| Previous / next | [1.1](https://w3id.org/ro/crate/1.1) / [1.3](https://w3id.org/ro/crate/1.3) |
| Descriptor `@id` | `ro-crate-metadata.json` (`.jsonld` only in legacy 1.0 crates) |

**1.2 is structurally almost identical to [1.3](ro-crate-1.3.0-summary.md).** Read that summary for the general
principles; this file records only what differs. 1.3's changelog ([`ro-crate-1.3/appendix/changelog.md`](ro-crate-1.3/appendix/changelog.md), lines 1-56) lists 1.2's changes;
the 1.3 text also folds in minor fixes listed there as "applied to the web version of 1.2".

## Differences from 1.3

- **Context and version URIs** use `1.2` (`https://w3id.org/ro/crate/1.2[/context]`).
- **Bioschemas namespace.** 1.2 maps `ComputationalWorkflow`, `FormalParameter` to `https://bioschemas.org/...` and
  `input`/`output` to `https://bioschemas.org/properties/...`. 1.3 moved all four to `https://bioschemas.org/terms/`.
  Crates still validate by term name; only the expanded IRIs differ.
- **schema.org** snapshot is 22.0 (1.3: 30.0). Terms removed in 22.0 relative to 1.1's snapshot: `AuthenticContent`,
  `MissingContext`, `constrainingProperty`, `measuredValue`, `observedNode`.
- **Minor errata fixed in 1.3** (descriptor must be `ro-crate-metadata.json` and not made absolute when converting
  attached to detached; typos/links; extra `rdfs:` properties in the core Profile Crate).
- Prose, sections and examples otherwise match; section order is the same.

## What 1.2 introduced (vs 1.1)

- **Attached vs Detached RO-Crate Package**; "RO-Crate Metadata Document" vs "Metadata File" terminology.
- **Profiles and Profile Crates**: profile conformance declared with `conformsTo` on the *root*; `Profile`,
  `ResourceDescriptor`, `hasResource`/`hasArtifact`/`hasRole`, `isProfileOf`.
- **Root finding** via `ro-crate-metadata.json` `about` (legacy `.jsonld` fallback), replacing the 1.0/1.1
  `conformsTo`-prefix algorithm.
- **Root `@id`** is `./` or an absolute URI; `identifier` as `PropertyValue`; `cite-as` and Signposting recommendations.
- **Web-based entities**: `contentUrl` is the direct-download property (1.1 used `url`); `localPath`; `sdDatePublished`;
  `DataDownload` distributions; referencing other RO-Crates and **Retrieving an RO-Crate** (`data-entities.md` line 520).
- **File encodings and file-format profiles** (`Standard`, PRONOM, `Profile` via `conformsTo`).
- **`mainEntity` / `mentions`** ("The focus of an RO-Crate"), "Common principles for RO-Crate entities", GeoSPARQL
  `Geometry`/`asWKT` for places, running example in the introduction, Attached/Detached conversion appendices.

## Section index (chapter files in [`ro-crate-1.2/`](ro-crate-1.2/), lines within each file)

| Topic | File | Line |
|---|---|---|
| Front matter | [index.md](ro-crate-1.2/index.md) | 1 |
| Introduction / running example | [introduction.md](ro-crate-1.2/introduction.md) | 1 / 10 |
| Terminology | [terminology.md](ro-crate-1.2/terminology.md) | 1 |
| Structure (types, document, attached, detached) | [structure.md](ro-crate-1.2/structure.md) | 1 (13, 36, 63, 177) |
| Metadata: principles, entity principles, schema.org, other vocabularies, identifiers | [metadata.md](ro-crate-1.2/metadata.md) | 1 (23, 42, 55, 79, 170) |
| Root Data Entity (descriptor 15, properties 77, minimal example 113) | [root-data-entity.md](ro-crate-1.2/root-data-entity.md) | 1 |
| Data Entities (files 122, encodings 356, format profiles 416, other crates 439, retrieving 520) | [data-entities.md](ro-crate-1.2/data-entities.md) | 1 |
| Contextual Entities | [contextual-entities.md](ro-crate-1.2/contextual-entities.md) | 1 |
| Focus of a crate | [crate-focus.md](ro-crate-1.2/crate-focus.md) | 1 |
| Provenance | [provenance.md](ro-crate-1.2/provenance.md) | 1 |
| Profiles (publishing 10, conformance 31, Profile Crate 69) | [profiles.md](ro-crate-1.2/profiles.md) | 1 |
| Workflows and Scripts | [workflows.md](ro-crate-1.2/workflows.md) | 1 |
| Implementation notes (BagIt 24) | [appendix/implementation-notes.md](ro-crate-1.2/appendix/implementation-notes.md) | 1 |
| RO-Crate JSON-LD appendix (context 92, media type 154, extending 198, profile grouping 313) | [appendix/jsonld.md](ro-crate-1.2/appendix/jsonld.md) | 1 |
| Relative URIs appendix | [appendix/relative-uris.md](ro-crate-1.2/appendix/relative-uris.md) | 1 |
| Changelog | [appendix/changelog.md](ro-crate-1.2/appendix/changelog.md) | 1 |
| Requirements by entity type, linked to the chapters | [quick-reference.md](ro-crate-1.2/quick-reference.md) | |
