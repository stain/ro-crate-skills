---
name: ro-crate-masp
description: "Read, write and validate against RO-Crate MASP (Machine Actionable Schemas and Profiles): profile and schema crates whose rules (rdfs:Class and rdf:Property with prov:specializationOf, domainIncludes, rangeIncludes, sh:minCount/sh:maxCount, PropertyValue and ItemList constraints) drive validation with masp-validate and editor forms in Crate-O, NovaCrate and wpsld. Use when a profile crate has a ResourceDescriptor with the dx-prof schema role, when a crate's conformsTo names a MASP or LDAC profile, when making a profile machine-actionable, or when asked to check a crate against such a profile. For profiles in general and Profile Crates see ro-crate-profiles."
---

# RO-Crate MASP profiles and schemas

[RO-Crate MASP](https://github.com/Language-Research-Technology/ro-crate-masp) packages a **profile** (rules for a purpose) or a **schema** (a general vocabulary) as an RO-Crate. The rules are contextual entities in schema.org's own shape (`rdfs:Class`, `rdf:Property`, `domainIncludes`, `rangeIncludes`) plus `prov:specializationOf` and SHACL-style counts. One crate drives validation, generated documentation and editor forms. Format details, a minimal profile and pitfalls: [references/masp-format.md](references/masp-format.md). Tested usage of every MASP tool and of wpsld-cli: [references/tools.md](references/tools.md). Converting the rules to SHACL for rocrate-validator: [references/shacl.md](references/shacl.md).

**Status (checked 2026-11-27):** a prototype. The MASP profile is version 0.1.0 with no release; the validator and tools are npm 0.1.0; profiles are identified by GitHub Pages URLs and pinned by commit. Say so when recommending it, record the commit or SHA-256 of any profile crate you use, and re-check the upstream README before quoting paths. A MASP check complements `rocrate-validator` (`ro-crate-validator`); it does not replace it.

## Where things are
The ro-crate-masp repository was split on 2026-11-25; it now holds only the MASP profile (the format's own definition) and points to the rest:

| What | Where |
|---|---|
| Format definition (the self-describing MASP profile) | [ro-crate-masp](https://github.com/Language-Research-Technology/ro-crate-masp), [profile documentation](https://github.com/Language-Research-Technology/ro-crate-masp/blob/main/profiles/ro-crate-masp/profile-crate/profile-documentation.md) |
| Validator, CLI `masp-validate` | [crate-works/ro-crate-masp-validator](https://github.com/crate-works/ro-crate-masp-validator), npm `@crate-works/ro-crate-masp-validator` |
| Tools: `generate-masp-docs`, `generate-mode-file`, `mode-to-masp`, `generate-schema-org-crate`, `owl-to-masp.py` | [crate-works/ro-crate-masp-tools](https://github.com/crate-works/ro-crate-masp-tools), npm `@crate-works/ro-crate-masp-tools` |
| Schema template and guide | [masp-templates](https://github.com/Language-Research-Technology/masp-templates) (`schema/`, `schema-user-guide.md`; no profile template yet) |
| Example profiles and schemas, `catalogue.json` | [ro-crate-masp-examples](https://github.com/Language-Research-Technology/ro-crate-masp-examples), site https://language-research-technology.github.io/ro-crate-masp-examples/ |

Old `language-research-technology.github.io/ro-crate-masp/profiles/...` pages redirect to the examples site and their `ro-crate-metadata.json` files stay as frozen copies; prefer the new addresses, but keep identifiers a profile already declares (the MASP profile's own `#profile` identifier is still under `/ro-crate-masp/`).

## Do not guess
Ask the user for facts about them and their project: authors, publisher, organisation, affiliation, ORCID/ROR/DOI, licence, funders, dates of events, and software or tool versions. Do not infer them from the user's email address, username, git config or machine, and never invent identifiers. You may derive what you can observe: file sizes and media types from the files, `tool --version` output, titles and descriptions from the content (say that you did).
If you cannot ask: leave optional properties out. For what the root data entity must have (`license`, `name`, `description`, `datePublished`) and for any other property the specification, a profile or the validator requires (for example `version` on a `SoftwareApplication` or `ComputerLanguage` you could not run), use an obviously temporary value that starts with `TODO:` (for example `"license": "TODO: choose a licence"`; today's date is fine for the `datePublished` of a draft), and list every `TODO:` value in your answer. The lint script (`ro-crate-validator`) warns about `TODO:` values. Never publish, deposit or hand over a crate that still contains one.

## Recognise a MASP crate
- Root `["Dataset", "Profile"]` whose `hasResource` has a `ResourceDescriptor` with `hasRole` `http://www.w3.org/ns/dx/prof/role/schema`; its `hasPart` lists the rules. Only those entities are rules.
- Usually `conformsTo` `https://language-research-technology.github.io/ro-crate-masp/profiles/ro-crate-masp/profile-crate/#profile`, and an `ItemList` of **conformance indicators** (role `https://w3id.org/ro/conformance-indicators`): the identifiers a crate puts in its root `conformsTo` to claim the profile. Match a crate's `conformsTo` against these, not only the root `@id` (often `./`).
- A Profile Crate whose `schema` resource is JSON Schema, SHACL or Turtle (e.g. FAIRSCAPE) is not MASP: use its own tools.

Summarise one (identifiers, class rules with their properties, counts and ranges, and authoring problems), standard library only:
```bash
python scripts/masp_rules.py path/to/profile-crate/ro-crate-metadata.json   # --json for machine output
```

## Find a profile
- Examples site and its `catalogue.json` (above): core RO-Crate, LDAC collection, Workflow RO-Crate port, photo collections, software, and schemas such as schema.org and LDAC terms.
- Registry: https://profiles.ro-crate.org/ (few entries have MASP rules; LDAC does).
- Retrieve a profile crate from its identifier as any crate (`ro-crate-retrieve`): the Pages folders link `ro-crate-metadata.json` with `<link rel="describedby">`; w3id identifiers redirect there. Work from a local copy of the JSON.

## Validate a crate against a profile
```bash
npm install @crate-works/ro-crate-masp-validator     # 0.1.0 on 2026-11-27; check `npm ls` for yours
npx masp-validate [--json] target/ro-crate-metadata.json profile-crate/ro-crate-metadata.json
```
In JavaScript: `new MaspValidator(profileCrate).validateCrate(targetCrate)` with both loaded by `ro-crate` (`ro-crate-js`) as `new ROCrate(json, {array: true, link: true})`.
Both arguments are local files. Exit 0 = passes, 2 = rule errors, 1 = unreadable input. **Only class counts become errors**: an entity that fails its property rules just does not count, so a root without `license` shows up as "Expected at least 1 instances of RO-Crate Metadata Descriptor ... found 0", and a stray entity failing its rules is not reported at all. In 0.1.0 that is all the error says: find the cause in `--json` (`rules.<rule>.<entity>.property-errors`). Releases with [PR #4](https://github.com/crate-works/ro-crate-masp-validator/pull/4) add "; not counted because they fail the rules: ..." with the reasons, innermost `[...]` first, and keep `--json` stdout pure JSON. Both behaviours and a `jq` recipe that works with either: [references/tools.md](references/tools.md). For plainer, stricter messages run `wpsld-cli check` (it reads the crate's MASP profiles from `conformsTo`) or the SHACL conversion below. Before changing the crate, read the rule (`masp_rules.py`) and check the error against the profile's documentation and the RO-Crate spec: example profiles have bugs (see the pitfalls in the reference), and a profile written for RO-Crate 1.2 can disagree with a correct 1.3 crate. Report such mismatches instead of degrading the crate. Then run `ro-crate-validator` for the RO-Crate rules themselves.

## Validate with rocrate-validator too (SHACL)
`python scripts/masp_to_shacl.py <profile-crate>/ro-crate-metadata.json shacl --context context.jsonld` writes a rocrate-validator profile folder (class rules as node shapes, the root targeted through the validator's own `RootDataEntity` class, property rules with counts and ranges, class counts as SPARQL constraints); then `rocrate-validator validate --extra-profiles-path shacl -p <token>-<version> -m <crate>`. Tested on all upstream example profiles. It checks every entity of a class (stricter than `masp-validate`). Ship the generated folder in the Profile Crate with role `validation` so one crate serves both validators: [references/shacl.md](references/shacl.md).

## Write or change a profile
1. Reuse first: an existing profile or schema from the examples; for new vocabulary terms start a schema crate from masp-templates, or convert an OWL/RDFS ontology with `owl-to-masp.py` (ro-crate-masp-tools); a profile can start from an existing Crate-O mode file with `mode-to-masp`. Ask the user for the profile's name, identifier (a permalink they control, e.g. w3id), version, licence and authors.
2. Root as a Profile Crate (`ro-crate-profiles`): `["Dataset", "Profile"]`, `name`, `description`, `version`, `license`, `isProfileOf` the RO-Crate version, `conformsTo` the MASP profile, `hasResource` with the schema, guidance and conformance-indicator descriptors.
3. For each type the profile constrains, a class rule (`rdfs:Class`, `prov:specializationOf` the vocabulary IRI, `rdfs:label` the term as written, `name`/`rdfs:comment` for humans, optional crate-wide `sh:minCount`/`sh:maxCount`).
4. For each property of each class rule, a property rule (`rdf:Property`, `rdfs:label` the JSON key, `prov:specializationOf`, `domainIncludes` the class rule, `rangeIncludes`, `sh:minCount` 1 if required, `sh:maxCount` 1 if single). Fixed values and patterns as `PropertyValue`, choices as `ItemList`, both referenced from `rangeIncludes`, never `value` on the property rule.
5. For a profile of whole crates, the root-detection rules (descriptor `@id` = `ro-crate-metadata.json`, `about` → root class rule); copy them from the reference.
6. List every rule, `PropertyValue` and `ItemList` in the schema descriptor's `hasPart`. Use plain `domainIncludes`/`rangeIncludes` keys, integer counts, `http://schema.org/` IRIs, and define the `sh` prefix in `@context`.
7. Check: `python scripts/masp_rules.py` until no ERROR; validate the profile crate against the MASP profile itself with `masp-validate`; validate an example conforming crate (and a broken one) against the new profile with `masp-validate` and, after `masp_to_shacl.py`, with rocrate-validator. Decide whether property rules apply to every entity of a class (SHACL, wpsld) or only make entities count (`masp-validate`), and say so in the profile text.
8. Documentation: write a `profile-text.md` with `${rules.all}` (and `${rules.allItemLists}`, `${rules.allDefinedTermSets}`) and generate `profile-documentation.md` with `npx generate-masp-docs -x <crate>/ro-crate-metadata.json profile-text.md <crate>/profile-documentation.md` from [ro-crate-masp-tools](https://github.com/crate-works/ro-crate-masp-tools) (`-x` also syncs the spreadsheet copy `ro-crate-metadata.xlsx`, newer file wins: commit before running). It also writes `index.html`. `generate-mode-file --output <crate>/crate-o-mode.json --update-profile <crate>/ro-crate-metadata.json` writes a Crate-O mode file and adds it to the profile crate. Optionally add the SHACL folder (role `validation`). Publish as in `ro-crate-profiles` / `ro-crate-publish`.

## Editors that read MASP
Crate-O (beta, uses the JS validator and `crate-o-mode.json`), NovaCrate (since v1.14, profiles named in `conformsTo`), and wpsld (Java desktop editor: required, suggested and other schema.org properties per type, profiles from a file, URL or registry). Editors show `sh:minCount` ≥ 1 as required and other property rules as suggested, so a profile shapes the forms people fill in; keep required rules to what is truly required.

## Pitfalls
- `rdfs:label` is the term as written (`datePublished`), `name` the human label ("Date published"): the reverse of RO-Crate's ad hoc terms.
- `sh:minCount`/`sh:maxCount` on a class count entities in the whole crate; on a property, values per entity.
- One property rule per property **per class**; a rule without `domainIncludes` applies nowhere, and a class rule with a local `@id` and no `prov:specializationOf` matches nothing.
- An `@id` property rule with a `PropertyValue` (e.g. `/^readme\.md$/i`) selects which entities a class rule is about (the README among the `File`s).
- Several class rules in the descriptor's `about` range = alternative kinds of root (rocphotos); the root must match one.
- Matching uses context-resolved types, exactly: an entity must have **every** type in the class rule's `prov:specializationOf` (two values = both types, not either), and a subtype (`ScholarlyArticle` for a `CreativeWork` rule) does not match. Without `prov:specializationOf`, the rule's own `@id` is the type.
- No `-DRAFT` RO-Crate versions in `isProfileOf` or contexts.
