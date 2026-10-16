# RO-Crate 1.3 specification: summary and section index

Companion to [`ro-crate-1.3.0.md`](ro-crate-1.3.0.md), the all-in-one Markdown of the specification
(https://doi.org/10.5281/zenodo.20720080, published 2026-06-22). Written for agents creating or reviewing
skills in this repository. This is a navigation aid, **not normative**: check the spec text before quoting a
MUST/SHOULD. Line numbers refer to `ro-crate-1.3.0.md` (read with `offset`/`limit`; the file is ~5500 lines).
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

## Section index (line ranges in `ro-crate-1.3.0.md`)

| Topic | Lines | Notes |
|---|---|---|
| Front matter, permalinks, licence | 1-50 | Apache-2.0; examples/context CC0 |
| Introduction and running example | 51-267 | Best 5-minute orientation; walkthrough of descriptor/root/data/contextual |
| Terminology | 308-351 | Defines Attached/Detached, Root, Descriptor, entities |
| Structure: types, descriptor, attached, detached | 381-568 | Preview rules 483-537; self-contained 538-551 |
| Metadata: Linked Data, entity principles, schema.org, other vocabularies | 589-760 | Common principles 627-637; vocabularies 662-726; recommended identifiers 749-759 |
| Root Data Entity, descriptor, finding root, identifier | 782-890 | Minimal example 891-953 |
| Data entities: files, dirs, web-based, distributions | 976-1324 | File 1094; Dataset 1125; web 1166; landing pages 1249; DataDownload 1279 |
| File encodings and file-format profiles | 1325-1405 | PRONOM, `Standard`, `WebPageElement` |
| Referencing other RO-Crates | 1406-1540 | Persistent id 1412; id selection 1432; `subjectOf` 1443; profiles 1464 |
| **Retrieving an RO-Crate** (Signposting, content negotiation, ZIP, BagIt) | 1486-1518 | Algorithm for `ro-crate-retrieve` / `fair-signposting` |
| Contextual entities: people, orgs, contact, citation, publisher, funding, licence, Exif, places, subjects, time, thumbnails | 1541-2098 | Licence 1847; metadata licence 1892; places (WKT) 1957 |
| Focus: `mainEntity`, `mentions` | 2120-2306 | |
| Provenance: equipment, software, change history, PCDM repositories | 2329-2598 | Actions 2387/2450; repositories 2529 |
| **Profiles**: publishing, declaring conformance | 2620-2684 | |
| **Profile Crate** and its parts (roles, schema table, vocab, context, multiple profiles) | 2685-3218 | `ResourceDescriptor` 2792; schema types table 2966; context rules 3116; multiple 3160 |
| Workflows and scripts (types, runtime, diagram, Bioschemas, I/O, full example) | 3241-3567 | Required types 3259-3269; example 3442 |
| Implementation notes: programming with JSON-LD, ELN, BagIt | 3618-3791 | BagIt layout 3656; manifest 3678; `fetch.txt` 3721; wrapping 3766 |
| Repository-specific identifiers | 3792-3816 | |
| JSON-LD appendix: structure, ids, context, media type, extending, ad hoc terms, profile grouping | 3839-4195 | Context 3927; media type 3988; extending 4031; ad hoc terms 4062 |
| Relative URIs: attached/detached conversion, flatten/expand, base URIs, arcp, relativize | 4218-4890 | Attached to detached 4230; detached to attached 4335; `@base: null` 4467; arcp 4733 |
| Changelog 1.0 to 1.3 | 4911-5034 | Source for `ro-crate-compatibility` |
| Reference link list | 5054-5517 | Ignore |

## Which skill should read which sections

| Skill | Read |
|---|---|
| `ro-crate-consume` | 413-437, 782-890, 1092-1324, 1406-1540, 3628-3636, 4569-4624 |
| `ro-crate-create` | 51-247, 627-637, 749-759, 782-975, 1017-1022, 1092-1210, 3909-3925 |
| `ro-crate-data-entities` | 976-1405 |
| `ro-crate-contextual-entities` | 1541-2098, 749-759 |
| `ro-crate-provenance` | 2329-2528 |
| `ro-crate-workflows` | 2120-2306 (mainEntity), 3241-3567 |
| `ro-crate-profile`, `ro-crate-profile-crate` | 2620-3218, 4144-4195 |
| `ro-crate-jsonld` | 3839-4195, 4218-4890 |
| `ro-crate-compatibility` | 4911-5034, 794-823 (descriptor), 856-890 (root), 3927-3986 (context/version) |
| `ro-crate-packaging` | 439-568, 3638-3791, 4230-4372 |
| `ro-crate-retrieve`, `fair-signposting` | 875-889 (`cite-as`), 1406-1540, 2750-2755 |
| `ro-crate-preview` | 248-267, 483-537 |
| `ro-crate-repositories` | 2529-2598, 3792-3816, 1279-1323 |
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
  crate-like path; see 1440 for when relative-root resolution is not recommended.
- The spec still calls JSON-LD 1.0 the baseline; the `@base` handling sections apply 1.1-style behaviour in tools.
- The BagIt example in the implementation notes writes `BagIt-version: 1.0`; the BagIt spec (RFC 8493) and `bagit-python` require `BagIt-Version`.
- The spec says to use `contentUrl` (not `url`) for direct download links of files on the web (changed in 1.2).
