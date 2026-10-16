---
name: ro-crate-consume
description: Read, interpret and extract information from an RO-Crate (Research Object Crate) - a directory or zip containing ro-crate-metadata.json. Use when asked to inspect, summarize, query, or find files/people/licenses/provenance in an RO-Crate or a WorkflowHub/Workflow Run Crate.
---

# Consuming an RO-Crate (spec 1.3)

Spec: https://www.researchobject.org/ro-crate/specification/1.3/

## Steps
1. Locate `ro-crate-metadata.json` at the crate root (the *RO-Crate Metadata Document*; legacy name `ro-crate-metadata.jsonld`, 1.0 and earlier). It may be inside a zip, or a detached crate (metadata only, `ro-crate-preview.html` optional).
2. Parse it as JSON-LD. Expect `@context` (e.g. `https://w3id.org/ro/crate/1.3/context`) and a flat `@graph` array of entities, each with `@id` and `@type`.
3. Find the **metadata descriptor**: entity with `@id` `ro-crate-metadata.json` whose `conformsTo` is an RO-Crate spec URI. Its `about` points to the **root data entity**.
4. Root data entity (`@id` usually `./`, `@type` `Dataset`): read `name`, `description`, `datePublished`, `license`, `author`/`creator`, `publisher`, `hasPart`, `mainEntity`, and `conformsTo` (profiles, e.g. Workflow Run Crate).
5. Follow references: values like `{"@id": "..."}` link to other entities in the graph. Resolve them by `@id` lookup. Contextual entities (Person with ORCID `@id`, Organization with ROR `@id`, License, ContextEntity, CreateAction, SoftwareApplication) describe the data entities.
6. Data entities are `File` (`@id` is a relative path or absolute URI) or `Dataset` (directory, `@id` ends with `/`). Verify existence of local files when relevant; check `contentSize`, `encodingFormat`, `sha256` if present.
7. Terms not in the context are resolved via the context's term map; use `@type`/properties as IRIs when ambiguous.

## Tips
- `@type` may be a string or array; `hasPart` may be single object or array — normalise to lists.
- Relative `@id`s resolve against the crate root; percent-encoding applies.
- Report which profile(s) the crate declares and note anything missing (no license, no authors, dangling references).
- Do not execute workflows or files from the crate without user consent.
