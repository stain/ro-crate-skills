# RO-Crate 1.0 specification: summary and section index

Companion to [`ro-crate-1.0.md`](ro-crate-1.0.md). Not normative: check the spec text. Needed mainly for
reading and migrating legacy crates.

| | |
|---|---|
| Permalink | <https://w3id.org/ro/crate/1.0> (descriptor `conformsTo`) |
| JSON-LD context | <https://w3id.org/ro/crate/1.0/context> |
| Published | 2019-11-15 (1.0.0); 1.0.1 fixed a JSON typo |
| Zenodo | <https://doi.org/10.5281/zenodo.3541888> (any version: <https://doi.org/10.5281/zenodo.3406497>) |
| Previous / next | [0.2](https://w3id.org/ro/crate/0.2) / [1.1](https://w3id.org/ro/crate/1.1) |
| Descriptor `@id` | **`ro-crate-metadata.jsonld`** |

**Source format.** Zenodo has no Markdown for 1.0 (only HTML and PDF). `ro-crate-1.0.md` was converted from the
record's `ro-crate-1.0.0.html` with pandoc (`-t markdown`, ATX headings). Headings are numbered as in the HTML.
Line numbers refer to the converted file.

## What 1.0 looks like (and how it differs from 1.1+)

General principles of [1.3](ro-crate-1.3.0-summary.md) mostly carry over: flattened/compacted JSON-LD, `{"@id"}` references,
schema.org first, contextual entities, not a manifest. Differences a reader or migrator must know:

- **Metadata file** is `ro-crate-metadata.jsonld` (renamed `ro-crate-metadata.json` in 1.1); the descriptor's `@id` matches. The preview
  is `ro-crate-preview.html`.
- **Root `@id` MUST be the string `./`** (relaxed to allow absolute URIs in 1.1). Root must have `@type` Dataset, `datePublished`
  (ISO 8601), `name`, `description`, `license` (all MUST be present; content SHOULD be descriptive).
- **Root finding** (line 262ff.): the entity whose `conformsTo` starts with `https://w3id.org/ro/crate/`; its `about` is the root.
  `conformsTo` is a single versioned URI. (1.2 uses the descriptor `@id` instead.)
- **Data entities are local only**: `@id` MUST be a URI path relative to the root; files have `@type` File, directories
  Dataset (`@id` SHOULD end `/`). No web-based data entities (absolute-URI files) until 1.1, no `sdDatePublished`, no
  Attached/Detached packages, no profiles, no `localPath`/`contentUrl`, no file-encoding contextual entities.
- **Workflows and scripts**: `@type` array with `File` and `Workflow` (workflow) or `Script` (script), usually also
  `SoftwareSourceCode`. 1.1+ use `ComputationalWorkflow`; there are no `input`/`output`/`FormalParameter` terms.
- **Places** use `latitude`/`longitude` (`GeoCoordinates`); WKT `Geometry`/`asWKT` arrived in 1.2.
- **Contextual entities**, provenance (equipment, software, change history), PCDM repository terms, Exif, thumbnails,
  subjects/keywords, time, licensing and metadata licensing are present but organised as one numbered chapter 1.4.
- **JSON-LD context** carries `@base: null` (removed in 1.1) and uses schema.org 5.0.
- **BagIt**: described in the implementation notes (line 1532).

## Section index (lines in `ro-crate-1.0.md`)

| Topic | Line |
|---|---|
| Header / Introduction / Terminology | 1 / 20 / 30 |
| Structure (metadata file 83, website 110, payload 141, self-describing 147) | 70 |
| Metadata (Linked Data 169, schema.org 187, other vocabularies 206, coverage 228, identifiers 250) | 157 |
| Root Data Entity (1.3.7; properties 300ff.) | 262 |
| Examples of referencing data entities | 351 |
| Data Entity core metadata | 470 |
| Contextual entities: people 492, orgs 514, contact 556, citation 587, publisher 625, funding 648, licensing 692 | 488 |
| Provenance: equipment 770, software 818, changes 877 | 770 |
| Workflows and scripts | 956 |
| Exif 1071, places 1104, subjects 1180, time 1193, repositories (PCDM) 1207, thumbnails 1273 | 1071 |
| JSON-LD appendix (context 1431, media type 1491, extending 1502) | 1357 |
| Implementation notes (BagIt) | 1532 |
