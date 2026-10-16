# JSON-LD essentials for RO-Crate

Spec appendix: https://www.researchobject.org/ro-crate/specification/1.3/appendix/jsonld (and `/appendix/relative-uris`).

- The document is **flattened and compacted** JSON-LD 1.0 style: `{"@context": ..., "@graph": [ {entity}, ... ]}`, no nesting, order irrelevant, single-element arrays unpacked.
- `@context` = `"https://w3id.org/ro/crate/1.3/context"` by reference (embedding a copy is allowed for archiving; consumers must not replace an embedded context by reference). The version to trust is the descriptor's `conformsTo`, not `@context`.
- **Extending:** `"@context": ["https://w3id.org/ro/crate/1.3/context", {"myTerm": "https://example.com/terms#myTerm"}]`. Every non-schema.org term used as a key or `@type` must be mapped. Define it in the graph:
  `{"@id": "https://example.com/terms#myTerm", "@type": "rdf:Property", "name": "my term", "description": "..."}` (`DefinedTerm` for concepts, `rdfs:Class` for types; add `rdfs:label`/`rdfs:comment`, `sameAs` to a human page if the IRI is an ontology file). Use `http://schema.org/...` (not https) in schema.org `@id`s.
- **Term URIs for ad hoc terms:** your own web page with `#anchors` (resolvable), or register a namespace under `https://w3id.org/ro/terms/` (https://github.com/ResearchObject/ro-terms). Repeated extensions belong in a profile (see ro-crate-profiles).
- **Relative references:** `@id` values like `data/a.csv`, `./`, `#alice` are URI references relative to the crate root. When expanding to RDF, set `@base` deliberately: `{"@base": null}` keeps relatives; `arcp://uuid,<uuid>/` for a zip with no URL; the retrieved URL for web crates. Never save `@base` in a crate you publish. Relativise absolute URIs inside the root before writing.
- **Programming tips:** build `entity_map[@id]`; values may be scalar, `{"@id"}`, list; do not assume strings; `@type` may be a list.
- Serve `ro-crate-metadata.json` as `application/ld+json` (profile `https://w3id.org/ro/crate`), with CORS if browsers read it.
