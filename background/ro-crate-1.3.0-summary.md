# RO-Crate 1.3 specification: summary and section index

Companion to [`ro-crate-1.3/`](ro-crate-1.3/), the specification with one Markdown file per chapter, split from
the all-in-one Markdown (https://doi.org/10.5281/zenodo.20720080, published 2026-06-22). Written for agents creating or
reviewing skills in this repository. This is a navigation aid, **not normative**: check the spec text before quoting a
MUST/SHOULD. Line numbers refer to the chapter file named in each row (read with `offset`/`limit`).
To find a requirement by entity type, start from [`quick-reference.md`](ro-crate-1.3/quick-reference.md), whose
links lead to the section in the chapter files.
Rendered pages: https://www.researchobject.org/ro-crate/specification/1.3/ (permalink https://w3id.org/ro/crate/1.3).
See [README.md](README.md) for licence and provenance. Version differences: [ro-crate-version-differences.md](../skills/ro-crate-compatibility/references/version-differences.md).

## General principles

1. **A crate is a Dataset described by one JSON-LD file.** `ro-crate-metadata.json` (the *RO-Crate Metadata
   Document*) describes the *RO-Crate Root*. Any folder becomes a crate by adding it. JSON-LD tooling is optional.
2. **Flattened and compacted JSON-LD.** `@graph` is a flat array of entities, order insignificant, no nesting.
   `@context` is `https://w3id.org/ro/crate/1.3/context` (by reference; extra terms via an `@context` array).
   Single-element arrays are unpacked. No duplicate `@id`s.
3. **References are objects.** Link entities with `{"@id": "..."}`, never bare strings, e.g.
   `"author": {"@id": "https://orcid.org/..."}`. Values may be a scalar *or* a reference *or* an array: code defensively.
4. **Every entity** has `@id` and `@type` (may be an array); SHOULD have a human-readable `name`; SHOULD use a
   schema.org type and applicable properties; SHOULD be reachable from the root (via `hasPart` or another property).
5. **Required graph members:** the Metadata Descriptor, the Root Data Entity, zero or more Data Entities, zero or
   more Contextual Entities. Referenced contextual entities SHOULD be described in the same file.
6. **Data vs contextual entities.** Data entities (`File`, `Dataset`) are the payload, linked via `hasPart` from the
   root (directly or indirectly). Contextual entities (Person, Organization, Place, licence, ...) describe
   context, linked via other properties. An entity can be both (use a `@type` array). `#local` `File`/`Dataset`
   entities are *not* data entities.
7. **Not a manifest.** There is no requirement to list every file. Use a `Dataset` with a `description` for undescribed
   directories. Pair with BagIt/OCFL when checksums or completeness are needed.
8. **schema.org first.** Prefer an existing schema.org term, even with a liberal reading (`IndividualProduct` for
   equipment, `HowTo` for a script). RO-Crate aliases: `File` = `MediaObject`, `Journal` = `Periodical`. Other
   vocabularies in the core context: PCDM, DC Terms (`conformsTo`), Profiles vocabulary, GeoSPARQL, CodeMeta,
   Bioschemas (`ComputationalWorkflow`, `FormalParameter`, `input`, `output`; namespace `bioschemas.org/terms/` in 1.3), `localPath`.
9. **Identifiers.** Prefer persistent absolute URIs: ORCID (people), ROR (organisations), GeoNames (places), PRONOM
   (file formats), DOI (root `identifier`). Otherwise `#local-id` for named entities and `_:blank` for unnamed
   (display inline). Relative `@id`s are URI references: use `/`, percent-encode space (`%20`) and `%`; UTF-8
   characters are preferred over `%`-escaping. Do not climb out of the root with `../`.
10. **Never invent identifiers.** Use the identifiers the user supplies; do not fabricate ORCIDs, DOIs, ROR ids.
11. **Self-describing and self-contained** (attached crates): include enough metadata for humans (`ro-crate-preview.html`)
    and machines to understand the crate without external lookups.
12. **Versions via `conformsTo`.** Detect the spec version from the descriptor's `conformsTo`, not from `@context`.
    Only use *released* versions: never write `-DRAFT` specs, contexts, `conformsTo` or profile URIs (see [AGENTS.md](../AGENTS.md)).
13. **Profiles = duck typing.** Domain conventions are layered via profiles declared on the *root* (`conformsTo`),
    optionally formalised as a machine-readable Profile Crate. Profiles are conventions, not strict inheritance.
14. **Be permissive on read, strict on write.** Accept older forms (string `identifier`, `.jsonld` descriptor,
    string `license`); generate the 1.3 recommended forms.
15. **Extend openly.** Add terms by mapping them in `@context` and defining them (`DefinedTerm`, `rdf:Property`,
    `rdfs:Class`); group repeated extensions into a profile.

## Structure of the crate

| Concept | Rule (section) |
|---|---|
| Attached crate | Directory (or ZIP root) containing `ro-crate-metadata.json`; payload files + web-based entities |
| Detached crate | Stand-alone document; all data entities are absolute URIs; file may be named `<prefix>-ro-crate-metadata.json`; the descriptor `@id` is still `ro-crate-metadata.json` |
| Metadata Descriptor | `@id` `ro-crate-metadata.json` (`.jsonld` = legacy 1.0), `@type` CreativeWork, `about` the root, `conformsTo` a single versioned `https://w3id.org/ro/crate/1.3` |
| Root Data Entity | `@type` includes `Dataset`; `@id` `./` or absolute URI; `name`, `description`, `datePublished` (ISO 8601, single string), `license` MUST be present (see the [quick reference](ro-crate-quick-reference-1.2-1.3.md)); `name`/`description` SHOULD disambiguate/summarise; `license` SHOULD link to an entity, or text; `identifier` string or `PropertyValue`; `cite-as` for a resolvable PID; `creditText` for citation text |
| Finding the root | `entity_map["ro-crate-metadata.json"].about["@id"]` (legacy fallback `.jsonld`) |
| Preview | Optional `ro-crate-preview.html` + `ro-crate-preview_files/`; MUST NOT be in `hasPart` |
| Metadata licence | Put `license` on the descriptor if it differs from the root |

## Section index (chapter files in [`ro-crate-1.3/`](ro-crate-1.3/), line ranges within each file)

| Topic | File | Lines | Notes |
|---|---|---|---|
| Front matter, permalinks, licence | [index.md](ro-crate-1.3/index.md) | 1-50 | Apache-2.0; examples/context CC0 |
| Introduction and running example | [introduction.md](ro-crate-1.3/introduction.md) | 1-217 | Best 5-minute orientation; walkthrough of descriptor/root/data/contextual |
| Terminology | [terminology.md](ro-crate-1.3/terminology.md) | 1-44 | Defines Attached/Detached, Root, Descriptor, entities |
| Structure: types, descriptor, attached, detached | [structure.md](ro-crate-1.3/structure.md) | 1-188 | Preview rules 103-157; self-contained 158-171 |
| Metadata: Linked Data, entity principles, schema.org, other vocabularies | [metadata.md](ro-crate-1.3/metadata.md) | 1-172 | Common principles 39-49; vocabularies 74-138; recommended identifiers 161-171 |
| Root Data Entity, descriptor, finding root, identifier | [root-data-entity.md](ro-crate-1.3/root-data-entity.md) | 1-109 | Minimal example 110-172 |
| Data entities: files, dirs, web-based, distributions | [data-entities.md](ro-crate-1.3/data-entities.md) | 1-349 | File 119; Dataset 150; web 191; landing pages 274; DataDownload 304 |
| File encodings and file-format profiles | [data-entities.md](ro-crate-1.3/data-entities.md) | 350-430 | PRONOM, `Standard`, `WebPageElement` |
| Referencing other RO-Crates | [data-entities.md](ro-crate-1.3/data-entities.md) | 431-565 | Persistent id 437; id selection 457; `subjectOf` 468; profiles 489 |
| **Retrieving an RO-Crate** (Signposting, content negotiation, ZIP, BagIt) | [data-entities.md](ro-crate-1.3/data-entities.md) | 511-543 | Algorithm for `ro-crate-retrieve` / `fair-signposting` |
| Contextual entities: people, orgs, contact, citation, publisher, funding, licence, Exif, places, subjects, time, thumbnails | [contextual-entities.md](ro-crate-1.3/contextual-entities.md) | 1-558 | Licence 307; metadata licence 352; places (WKT) 417 |
| Focus: `mainEntity`, `mentions` | [crate-focus.md](ro-crate-1.3/crate-focus.md) | 1-187 | |
| Provenance: equipment, software, change history, PCDM repositories | [provenance.md](ro-crate-1.3/provenance.md) | 1-270 | Actions 59/122; repositories 201 |
| **Profiles**: publishing, declaring conformance | [profiles.md](ro-crate-1.3/profiles.md) | 1-65 | |
| **Profile Crate** and its parts (roles, schema table, vocab, context, multiple profiles) | [profiles.md](ro-crate-1.3/profiles.md) | 66-599 | `ResourceDescriptor` 173; schema types table 347; context rules 497; multiple 541 |
| Workflows and scripts (types, runtime, diagram, Bioschemas, I/O, full example) | [workflows.md](ro-crate-1.3/workflows.md) | 1-327 | Required types 19-29; example 202 |
| Implementation notes: programming with JSON-LD, ELN, BagIt | [appendix/implementation-notes.md](ro-crate-1.3/appendix/implementation-notes.md) | 1-174 | BagIt layout 39; manifest 61; `fetch.txt` 104; wrapping 149 |
| Repository-specific identifiers | [appendix/implementation-notes.md](ro-crate-1.3/appendix/implementation-notes.md) | 175-199 | |
| JSON-LD appendix: structure, ids, context, media type, extending, ad hoc terms, profile grouping | [appendix/jsonld.md](ro-crate-1.3/appendix/jsonld.md) | 1-357 | Context 89; media type 150; extending 193; ad hoc terms 224 |
| Relative URIs: attached/detached conversion, flatten/expand, base URIs, arcp, relativize | [appendix/relative-uris.md](ro-crate-1.3/appendix/relative-uris.md) | 1-673 | Attached to detached 13; detached to attached 118; `@base: null` 250; arcp 516 |
| Changelog 1.0 to 1.3 | [appendix/changelog.md](ro-crate-1.3/appendix/changelog.md) | 1-124 | Source for `ro-crate-compatibility` |
| Reference link list | [references.md](ro-crate-1.3/references.md) | 1-464 | Ignore |
| All requirements by entity type (quick reference) | [quick-reference.md](ro-crate-1.3/quick-reference.md) | | Links go to the chapter files |

## Which skill should read which sections

| Skill | Read |
|---|---|
| `ro-crate-consume` | `structure.md` 33-57, `root-data-entity.md` 1-109, `data-entities.md` 117-349, `data-entities.md` 431-565, `appendix/implementation-notes.md` 11-19, `appendix/relative-uris.md` 352-407 |
| `ro-crate-create` | `introduction.md` 1-197, `metadata.md` 39-49, `metadata.md` 161-171, `root-data-entity.md` 1-194, `data-entities.md` 42-47, `data-entities.md` 117-235, `appendix/jsonld.md` 71-87 |
| `ro-crate-data-entities` | `data-entities.md` 1-430 |
| `ro-crate-contextual-entities` | `contextual-entities.md` 1-558, `metadata.md` 161-171 |
| `ro-crate-provenance` | `provenance.md` 1-200 |
| `ro-crate-workflows` | `crate-focus.md` 1-187 (mainEntity), `workflows.md` 1-327 |
| `ro-crate-profile`, `ro-crate-profile-crate` | `profiles.md` 1-599, `appendix/jsonld.md` 306-357 |
| `ro-crate-jsonld` | `appendix/jsonld.md` 1-357, `appendix/relative-uris.md` 1-673 |
| `ro-crate-compatibility` | `appendix/changelog.md` 1-124, `root-data-entity.md` 13-42 (descriptor), `root-data-entity.md` 75-109 (root), `appendix/jsonld.md` 89-148 (context/version) |
| `ro-crate-packaging` | `structure.md` 59-188, `appendix/implementation-notes.md` 21-174, `appendix/relative-uris.md` 13-155 |
| `ro-crate-retrieve`, `fair-signposting` | `root-data-entity.md` 94-108 (`cite-as`), `data-entities.md` 431-565, `profiles.md` 131-136 |
| `ro-crate-preview` | `introduction.md` 198-217, `structure.md` 103-157 |
| `ro-crate-repositories` | `provenance.md` 201-270, `appendix/implementation-notes.md` 175-199, `data-entities.md` 304-348 |
| `ro-crate-validator`, `ro-crate-tools` | Use the checklist below; tools are not covered by the spec |

## Checklist: what a valid, good 1.3 crate has

- [ ] `@context` `https://w3id.org/ro/crate/1.3/context`; `@graph` flat; unique `@id`s; references as `{"@id": ...}`.
- [ ] Descriptor: `@id` `ro-crate-metadata.json`, CreativeWork, `about` root, `conformsTo` `https://w3id.org/ro/crate/1.3`.
- [ ] Root: `@type` Dataset; `@id` `./` or absolute URI; `datePublished`, `name`, `description`, `license` all present.
- [ ] Data entities reachable via `hasPart`; files exist (attached) or are downloadable (web-based); directories end in `/`.
- [ ] Files carry `name`, `encodingFormat`, `contentSize` where known; web-based files carry `sdDatePublished`.
- [ ] Contextual entities described for every referenced person/org/licence/place; persistent identifiers where real.
- [ ] Profile conformance on the root, each profile a contextual entity with `@type` `Profile`.
- [ ] Extension terms mapped in `@context` and defined; schema.org terms use `http://` in `@id`s.

## Spec quirks to be aware of (do not copy blindly)

- Section "Direct properties of the Root Data Entity" says the root MUST have all listed properties, while the
  bullets use SHOULD for what the value should be (`name`, `description`, `license`, `@id`). Read it as: the
  properties MUST be present, values SHOULD meet the stated quality bar (the project's quick reference lists
  them as "Must be present" for `name`, `description`, `datePublished`, `license`).
- Several spec examples are abbreviated or not valid JSON (trailing commas, `...` placeholders, string `license`/`author` values,
  a workflow example without `datePublished`). Take patterns from the prose; do not paste examples unchanged.
- The Retrieving algorithm's heuristic fallback (`./ro-crate-metadata.json`) is optional and only for URIs that end in a
  crate-like path; see `data-entities.md` line 465 for when relative-root resolution is not recommended.
- The spec still calls JSON-LD 1.0 the baseline; the `@base` handling sections apply 1.1-style behaviour in tools.
- The BagIt example in the implementation notes writes `BagIt-version: 1.0`; the BagIt spec (RFC 8493) and `bagit-python` require `BagIt-Version`.
- The spec says to use `contentUrl` (not `url`) for direct download links of files on the web (changed in 1.2).
