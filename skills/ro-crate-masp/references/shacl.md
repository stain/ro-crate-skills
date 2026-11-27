# MASP and SHACL: one Profile Crate for both validators

`masp-validate` reads MASP rules; [rocrate-validator](https://github.com/crs4/rocrate-validator)
(`ro-crate-validator`) reads SHACL shapes in its own profile folders. A Profile Crate can
serve both: keep the MASP rules as the single source and generate the SHACL from them.
Tested 2026-11-27 with roc-validator 0.14.0 (pySHACL 0.40.2) and `scripts/masp_to_shacl.py`
on the upstream example profiles.

## Contents
- How rocrate-validator profiles are written
- Converting MASP rules
- Where MASP and SHACL disagree
- Shipping both in the Profile Crate

## How rocrate-validator profiles are written

From its guide, [Writing a new profile](https://rocrate-validator.readthedocs.io/en/latest/11_writing_a_profile/):

- A profile is a **folder** `<token>/<version>/` with `profile.ttl` (a `prof:Profile` with
  `rdfs:label`, `prof:hasToken`, `prof:isProfileOf` and `prof:isTransitiveProfileOf`, and
  `prof:hasResource` descriptors) and any number of SHACL `.ttl` files and Python checks,
  optionally in `must/`, `should/`, `may/` (REQUIRED, RECOMMENDED, OPTIONAL) or with
  `sh:severity`. An optional `ontology.ttl` is merged into the data graph (slow on big crates).
- Each `sh:NodeShape`/`sh:PropertyShape` is one check, identified by `(sh:name, severity)`.
  A child profile can override a parent's check by using the same identity, deactivate it
  (`sh:deactivated true`), or present the parent's checks as its own (`validator:isRuleOverlayOf`).
- `prof:isProfileOf` the RO-Crate version makes the RO-Crate checks run too. List the whole
  chain in `prof:isTransitiveProfileOf`: on 1.3, both `https://w3id.org/ro/crate/1.3` and
  `.../1.2` (the 1.3 profile reuses the 1.2 checks; with 1.3 alone validation stops with
  "Invalid check dependency in profile 'ro-crate-1.3'").
- The folder's version must match a version in the profile IRI ("Inconsistent versions found").
- Use your own folder without changing the package:
  `rocrate-validator validate --extra-profiles-path <dir> -p <token>-<version> <crate>`; a
  profile with the URI of a bundled one replaces it. `rocrate-validator profiles check <id>`
  reports duplicate check identities.
- **Finding the root.** The RO-Crate profile has a hidden shape whose SPARQL target selects
  the `Dataset` the descriptor is `about`, and a `sh:TripleRule` that types it
  `https://github.com/crs4/rocrate-validator/profiles/ro-crate-1.2/RootDataEntity`
  (the 1.3 profile adds `.../ro-crate-1.3/RootDataEntity` as equivalent;
  1.1: `.../profiles/ro-crate/RootDataEntity`). A child profile targets the root with
  `sh:targetClass` on that class: this layered approach solves the hard part of converting
  MASP (a `Dataset` target would hit every folder). Prefer Core targets; SPARQL targets are
  slow on large graphs (see the guide's *Optimizing SHACL target selection*).

## Converting MASP rules

```bash
curl -sL -H 'Accept: application/ld+json' https://w3id.org/ro/crate/1.3/context -o context.jsonld
python scripts/masp_to_shacl.py profile-crate/ro-crate-metadata.json shacl --context context.jsonld [--base 1.3] [--token NAME]
rocrate-validator validate --extra-profiles-path shacl -p <token>-<version> -m <crate>
```

| MASP | SHACL generated |
|---|---|
| class rule | `sh:NodeShape`, `sh:targetClass` the specialised type; several types, or an `@id` rule, → `sh:SPARQLTarget` (all types; `@id` regex or literal matched on the last path segment) |
| the root rule (descriptor `about`) | `sh:targetClass` the validator's `RootDataEntity` class; several alternative root rules → `sh:or` of their shapes |
| the descriptor's own rules | left to the RO-Crate profile |
| property rule | property shape: `sh:path` from `prov:specializationOf` (else `rdfs:label` through the context), `sh:minCount`, `sh:maxCount`, `sh:name` "Class: property" |
| `rangeIncludes` | `sh:or` of: class rule → `sh:class`; Text/Date → `sh:nodeKind sh:Literal`; Number → numeric `sh:datatype`s; Boolean → `xsd:boolean`; URL → `sh:IRIOrLiteral`; `PropertyValue` → `sh:hasValue` or `sh:pattern` + `sh:flags`; `ItemList` → `sh:in` |
| class `sh:minCount`/`sh:maxCount` | `sh:SPARQLConstraint` on the root counting entities (`$this` must appear in the pattern: a query with only a sub-select never reports in pySHACL) |

All shapes go in `must/` (REQUIRED). The script prints what it could not convert; review the
Turtle as you would any generated code. Results on the upstream examples: all six profiles
convert and load; the SHACL found what `masp-validate` found (a missing main workflow) plus
property problems it hides (a README whose `about` is the string `"./"`, 1357 `RepositoryObject`s
without `conformsTo` in the LDAC `cooee` example).

## Where MASP and SHACL disagree

- **Strictness.** `masp-validate` counts an entity as an instance only if it passes its property
  rules, and reports only class counts: a `Person` lacking a required `name` is silent unless
  that makes a count fail (directly or through references from the root). SHACL, wpsld-cli,
  and the MASP documentation's wording check every entity of the class. Decide which you mean
  and say so in the profile text; the stricter reading is the safer default.
- **Types.** Both require all `prov:specializationOf` types and do no subclass reasoning (the
  validator's `ontology.ttl` could add it).
- **Literals vs references.** SHACL distinguishes `"./"` from `{"@id": "./"}`; `masp-validate` does not.
- **Not converted:** `@id` rules other than selecting entities, `DefinedTermSet` documentation,
  Crate-O layout. Several `@id` rules on one class: only the first becomes the filter.

## Shipping both in the Profile Crate

Keep the MASP rules in the crate (role `schema`); add the generated folder as data with role
`validation`, as the RO-Crate 1.3 profiles section recommends for SHACL:

```json
{"@id": "#hasValidation", "@type": "ResourceDescriptor", "name": "SHACL shapes for rocrate-validator",
 "hasRole": {"@id": "http://www.w3.org/ns/dx/prof/role/validation"},
 "hasArtifact": {"@id": "rocrate-validator/"}},
{"@id": "rocrate-validator/", "@type": "Dataset", "name": "rocrate-validator profile folder",
 "description": "Generated from the MASP rules with masp_to_shacl.py; use with rocrate-validator --extra-profiles-path.",
 "hasPart": [{"@id": "rocrate-validator/lab-profile/0.1/profile.ttl"},
             {"@id": "rocrate-validator/lab-profile/0.1/must/0_masp_rules.ttl"}]},
{"@id": "rocrate-validator/lab-profile/0.1/must/0_masp_rules.ttl", "@type": "File",
 "encodingFormat": ["text/turtle", {"@id": "https://www.nationalarchives.gov.uk/PRONOM/fmt/874"}],
 "conformsTo": {"@id": "https://www.w3.org/TR/shacl/"}, "isBasedOn": {"@id": "#hasSpecializedSchema"}}
```
List the folder and files in the root's `hasPart` too, describe `https://www.w3.org/TR/shacl/`
as a `Profile` entity, regenerate the SHACL whenever the rules change, and validate an example
crate with both tools before publishing. Users then run
`rocrate-validator validate --extra-profiles-path <profile-crate>/rocrate-validator -p lab-profile-0.1 <crate>`.
To bundle the profile with rocrate-validator itself, contribute the folder with tests (its guide).
