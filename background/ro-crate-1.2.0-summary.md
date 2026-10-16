# RO-Crate 1.2 specification: summary and section index

Companion to [`ro-crate-1.2.0.md`](ro-crate-1.2.0.md), the all-in-one Markdown of RO-Crate 1.2.0
(published 2025-06-04). Not normative: check the spec text. Line numbers refer to `ro-crate-1.2.0.md`
(Setext-style headings; each chapter has a "Table of contents" stub that can be ignored).

| | |
|---|---|
| Permalink | <https://w3id.org/ro/crate/1.2> (descriptor `conformsTo`) |
| JSON-LD context | <https://w3id.org/ro/crate/1.2/context> |
| Zenodo (this version) | <https://doi.org/10.5281/zenodo.13751027> (any version: <https://doi.org/10.5281/zenodo.3406497>) |
| Previous / next | [1.1](https://w3id.org/ro/crate/1.1) / [1.3](https://w3id.org/ro/crate/1.3) |
| Descriptor `@id` | `ro-crate-metadata.json` (`.jsonld` only in legacy 1.0 crates) |

**1.2 is structurally almost identical to [1.3](ro-crate-1.3.0-summary.md).** Read that summary for the general
principles; this file records only what differs. 1.3's changelog (1.3.0 spec, lines 4911-4966) lists 1.2's changes;
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
  `DataDownload` distributions; referencing other RO-Crates and **Retrieving an RO-Crate** (line 1522).
- **File encodings and file-format profiles** (`Standard`, PRONOM, `Profile` via `conformsTo`).
- **`mainEntity` / `mentions`** ("The focus of an RO-Crate"), "Common principles for RO-Crate entities", GeoSPARQL
  `Geometry`/`asWKT` for places, running example in the introduction, Attached/Detached conversion appendices.

## Section index (lines in `ro-crate-1.2.0.md`)

| Topic | Line |
|---|---|
| Front matter / Introduction / running example | 1 / 52 / 61 |
| Terminology | 313 |
| Structure (types, document, attached, detached) | 388 (400, 423, 450, 564) |
| Metadata: principles, entity principles, schema.org, other vocabularies, identifiers | 602 (624, 643, 656, 680, 771) |
| Root Data Entity (descriptor 819, properties 881, minimal example 917) | 805 |
| Data Entities (files 1124, encodings 1358, format profiles 1418, other crates 1441, retrieving 1522) | 1003 |
| Contextual Entities | 1577 |
| Focus of a crate | 2172 |
| Provenance | 2384 |
| Profiles (publishing 2690, conformance 2711, Profile Crate 2749) | 2681 |
| Workflows and Scripts | 3306 |
| Implementation notes (BagIt 3715) | 3692 |
| RO-Crate JSON-LD appendix (context 4009, media type 4071, extending 4115, profile grouping 4230) | 3918 |
| Relative URIs appendix | 4305 |
