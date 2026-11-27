# MASP crate format

How a MASP profile or schema crate is put together, as the reference validator
(`@crate-works/ro-crate-masp-validator` 0.1.0) reads it. Checked against
[ro-crate-masp](https://github.com/Language-Research-Technology/ro-crate-masp) at commit
`f8cc225` (2026-11-27) and the implementation notes of the Java editor wpsld
([MASP.md](https://github.com/stain/wpsld/blob/main/MASP.md)). MASP is a prototype:
re-check the [MASP profile documentation](https://github.com/Language-Research-Technology/ro-crate-masp/blob/main/profiles/ro-crate-masp/profile-crate/profile-documentation.md)
before relying on details.

## Contents
- Root and resources
- Class rules
- Property rules
- Value constraints
- Finding the root data entity
- How the validator matches
- Minimal profile crate
- Pitfalls seen in real profiles
- Mapping to SHACL (see shacl.md)

## Root and resources

The root is `["Dataset", "Profile"]` (an RO-Crate Profile Crate, see `ro-crate-profiles`)
with `isProfileOf` the RO-Crate version, `license`, `name`, and `conformsTo` the MASP
profile, `https://language-research-technology.github.io/ro-crate-masp/profiles/ro-crate-masp/profile-crate/#profile`
(described as a `["CreativeWork", "Profile"]` entity). Its `hasResource` lists
`ResourceDescriptor`s; the validator only looks at those linked from the root.

| `hasRole` | `hasArtifact` / `hasPart` |
|---|---|
| `http://www.w3.org/ns/dx/prof/role/schema` (conventionally `#hasSpecializedSchema`) | `hasPart`: **every rule**. Entities not listed here are not rules |
| `http://www.w3.org/ns/dx/prof/role/specification` | `index.html` |
| `http://www.w3.org/ns/dx/prof/role/guidance` | `profile-documentation.md` (generated) |
| `http://www.w3.org/ns/dx/prof/role/example` | example entities or crates |
| `http://www.w3.org/ns/dx/prof/role/vocabulary` | enumeration values (schema crates) |
| `https://w3id.org/ro/mode` | `crate-o-mode.json`, Crate-O layout (field groups, order) |
| `https://w3id.org/ro/conformance-indicators` | an `ItemList` whose `itemListElement` are the `@id`s a crate may put in its root `conformsTo` to claim this profile |

The conformance indicators matter because many profile crates have root `./` or a
GitHub Pages folder as `@id`: tools look a profile up by these identifiers, not the
root's `@id` (e.g. LDAC: `https://w3id.org/ldac/profile#Collection`).

## Class rules

```json
{"@id": "#class_ScholarlyArticle", "@type": "rdfs:Class",
 "prov:specializationOf": {"@id": "http://schema.org/ScholarlyArticle"},
 "rdfs:label": "ScholarlyArticle", "name": "Scholarly article",
 "rdfs:comment": "An article reviewed by peers, as this profile uses it.",
 "sh:minCount": 1, "sh:maxCount": 1}
```
- `prov:specializationOf`: the vocabulary class(es), resolved through the profile crate's
  own context; an entity matches when its context-resolved `@type`s include **all** of them
  (exact IRIs, no subclass reasoning). Without it, the rule's own `@id` is the type (as for
  `ldac:CollectionEvent`-style rules with absolute or compact ids).
- `sh:minCount`/`sh:maxCount` on a class: how many such entities the **whole crate**
  must/may have.
- `rdfs:subClassOf` another class rule: the subclass inherits its property rules.
- `rdfs:label` is the term as written in a crate (`ScholarlyArticle`); `name` is the
  human-readable name for documentation. This is the reverse of RO-Crate's ad hoc
  terms, where `name` is the human form: MASP follows schema.org.

## Property rules

One per property **per class**: `name` on the root and `name` on a `Person` are two rules.

```json
{"@id": "#prop_author_ScholarlyArticle", "@type": "rdf:Property",
 "prov:specializationOf": {"@id": "http://schema.org/author"},
 "rdfs:label": "author", "rdfs:comment": "Who wrote the article.",
 "domainIncludes": {"@id": "#class_ScholarlyArticle"},
 "rangeIncludes": [{"@id": "#class_Person"}, {"@id": "#class_Organization"}],
 "sh:minCount": 1}
```
- `rdfs:label`: the JSON key in the target crate (`author`, or `@id` for the identifier).
- `domainIncludes`: **class rules** (local ids), not vocabulary classes. Write the plain
  key `domainIncludes`/`rangeIncludes`, never `schema:domainIncludes`: the validator
  matches keys as written.
- `sh:minCount`/`sh:maxCount` on a property: values per matching entity. Omit for 0..*.
  `sh:minCount` ≥ 1 is what editors show as required; property rules without it are
  shown as suggested.
- `rangeIncludes`: class rules (values are references to entities, checked recursively
  against that rule), primitive types (`Text`, `Number`, `Boolean`, `Date`, `URL`),
  `PropertyValue` constraints, or an `ItemList` of allowed values.

## Value constraints

Never put `value` on the property rule. Reference a constraint from `rangeIncludes`:

```json
{"@id": "#prop_license_Root", "@type": "rdf:Property", "rdfs:label": "license",
 "prov:specializationOf": {"@id": "http://schema.org/license"},
 "domainIncludes": {"@id": "#class_Root"}, "rangeIncludes": {"@id": "#licenses"},
 "sh:minCount": 1, "sh:maxCount": 1},
{"@id": "#licenses", "@type": "ItemList", "name": "Allowed licences",
 "itemListElement": [{"@id": "https://spdx.org/licenses/CC-BY-4.0"},
                     {"@id": "https://spdx.org/licenses/CC0-1.0"}]},
{"@id": "#readme_id", "@type": "PropertyValue", "name": "README file name",
 "value": "/^readme\\.md$/i"}
```
- `PropertyValue` `value`: an exact literal, an `{"@id": ...}` to match a reference, or a
  JavaScript-style `/regex/flags` string (proposal to use `sh:pattern` instead:
  ro-crate-masp issue #47).
- `ItemList`: the value must be one of the `itemListElement` `@id`s; list items may carry
  properties the value must also match. List both the `ItemList` and `PropertyValue`
  entities in the schema descriptor's `hasPart`.
- `DefinedTermSet`/`DefinedTerm`: documented terms; the validator passes them through.

## Finding the root data entity

RO-Crate types cannot tell the root from other `Dataset`s, so a profile of whole crates
needs this pattern (copy it, renaming ids as you like):

```json
{"@id": "#class_MetadataDescriptor", "@type": "rdfs:Class",
 "prov:specializationOf": {"@id": "http://schema.org/CreativeWork"}, "sh:minCount": 1, "sh:maxCount": 1},
{"@id": "#prop_id_MetadataDescriptor", "@type": "rdf:Property", "rdfs:label": "@id",
 "domainIncludes": {"@id": "#class_MetadataDescriptor"},
 "rangeIncludes": {"@id": "#value_metadata_id"}, "sh:minCount": 1, "sh:maxCount": 1},
{"@id": "#value_metadata_id", "@type": "PropertyValue", "value": "ro-crate-metadata.json", "sh:minCount": 1},
{"@id": "#prop_about_MetadataDescriptor", "@type": "rdf:Property", "rdfs:label": "about",
 "prov:specializationOf": {"@id": "http://schema.org/about"},
 "domainIncludes": {"@id": "#class_MetadataDescriptor"},
 "rangeIncludes": {"@id": "#class_Root"}, "sh:minCount": 1, "sh:maxCount": 1}
```
The `PropertyValue` needs `"sh:minCount": 1`: without it the validator does not enforce the
value, and every `CreativeWork` counts as a candidate descriptor. The root's rules then hang off `#class_Root` (`prov:specializationOf` `Dataset`) and apply
to the root only. A schema crate (general vocabulary) does not need this.

## How the validator matches

1. Root's `hasResource` → descriptor with role `schema` → its `hasPart` = the rules.
2. `rdfs:Class` → class rule, `rdf:Property` → property rule, `ItemList`, `PropertyValue`,
   `DefinedTermSet` → constraints.
3. Root detection by the pattern above.
4. Each class rule: target entities whose resolved `@type`s include all of `prov:specializationOf`;
   check instance counts and the property rules whose `domainIncludes` is that class
   rule (or an ancestor by `rdfs:subClassOf`).
5. Each property: counts, `PropertyValue`/`ItemList` constraints, primitive ranges, and
   references validated against the class rules in the range.

Output: only class counts become `[ERROR]`s. An entity failing a property rule is simply not a
valid instance; that matters only if a count then fails (directly, or because a reference from
the root no longer reaches a valid entity). `--json` has the per-entity property results.

## Minimal profile crate

A profile of RO-Crate 1.3 that requires a root `name` and one `author` who is a `Person`.
Replace the example identifiers; the upstream examples use the RO-Crate 1.2 context and
`isProfileOf` 1.2, which works the same way.

```json
{"@context": ["https://w3id.org/ro/crate/1.3/context",
              {"@vocab": "http://schema.org/", "sh": "http://www.w3.org/ns/shacl#"}],
 "@graph": [
  {"@id": "ro-crate-metadata.json", "@type": "CreativeWork",
   "conformsTo": {"@id": "https://w3id.org/ro/crate/1.3"}, "about": {"@id": "https://example.org/profiles/lab/0.1"}},
  {"@id": "https://example.org/profiles/lab/0.1", "@type": ["Dataset", "Profile"],
   "name": "Example lab profile", "description": "Crates from the example lab.", "version": "0.1.0",
   "license": {"@id": "https://spdx.org/licenses/Apache-2.0"},
   "isProfileOf": {"@id": "https://w3id.org/ro/crate/1.3"},
   "conformsTo": {"@id": "https://language-research-technology.github.io/ro-crate-masp/profiles/ro-crate-masp/profile-crate/#profile"},
   "hasPart": [{"@id": "profile-documentation.md"}],
   "hasResource": [{"@id": "#hasSpecializedSchema"}, {"@id": "#hasGuidance"}, {"@id": "#hasConformanceIndicators"}]},
  {"@id": "https://w3id.org/ro/crate/1.3", "@type": ["CreativeWork", "Profile"], "name": "RO-Crate 1.3"},
  {"@id": "https://language-research-technology.github.io/ro-crate-masp/profiles/ro-crate-masp/profile-crate/#profile",
   "@type": ["CreativeWork", "Profile"], "name": "RO-Crate MASP Profile"},
  {"@id": "https://spdx.org/licenses/Apache-2.0", "@type": "CreativeWork", "name": "Apache License 2.0"},
  {"@id": "profile-documentation.md", "@type": "File", "name": "Profile documentation", "encodingFormat": "text/markdown"},
  {"@id": "#hasGuidance", "@type": "ResourceDescriptor",
   "hasRole": {"@id": "http://www.w3.org/ns/dx/prof/role/guidance"}, "hasArtifact": {"@id": "profile-documentation.md"}},
  {"@id": "#hasConformanceIndicators", "@type": "ResourceDescriptor",
   "hasRole": {"@id": "https://w3id.org/ro/conformance-indicators"}, "hasArtifact": {"@id": "#indicators"}},
  {"@id": "#indicators", "@type": "ItemList", "name": "Supported conformsTo identifiers",
   "itemListElement": [{"@id": "https://example.org/profiles/lab/0.1"}]},
  {"@id": "#hasSpecializedSchema", "@type": "ResourceDescriptor", "name": "Specialized Schema Terms",
   "hasRole": {"@id": "http://www.w3.org/ns/dx/prof/role/schema"},
   "hasPart": [{"@id": "#class_MetadataDescriptor"}, {"@id": "#prop_id_MetadataDescriptor"},
               {"@id": "#value_metadata_id"}, {"@id": "#prop_about_MetadataDescriptor"},
               {"@id": "#class_Root"}, {"@id": "#prop_name_Root"}, {"@id": "#prop_author_Root"},
               {"@id": "#class_Person"}, {"@id": "#prop_name_Person"}]},
  "... the four root-detection entities from the section above ...",
  {"@id": "#class_Root", "@type": "rdfs:Class", "rdfs:label": "Dataset", "name": "Root data entity",
   "prov:specializationOf": {"@id": "http://schema.org/Dataset"}, "sh:maxCount": 1},
  {"@id": "#prop_name_Root", "@type": "rdf:Property", "rdfs:label": "name",
   "prov:specializationOf": {"@id": "http://schema.org/name"}, "domainIncludes": {"@id": "#class_Root"},
   "rangeIncludes": {"@id": "http://schema.org/Text"}, "sh:minCount": 1, "sh:maxCount": 1},
  {"@id": "#prop_author_Root", "@type": "rdf:Property", "rdfs:label": "author",
   "prov:specializationOf": {"@id": "http://schema.org/author"}, "domainIncludes": {"@id": "#class_Root"},
   "rangeIncludes": {"@id": "#class_Person"}, "sh:minCount": 1},
  {"@id": "#class_Person", "@type": "rdfs:Class", "rdfs:label": "Person",
   "prov:specializationOf": {"@id": "http://schema.org/Person"}},
  {"@id": "#prop_name_Person", "@type": "rdf:Property", "rdfs:label": "name",
   "prov:specializationOf": {"@id": "http://schema.org/name"}, "domainIncludes": {"@id": "#class_Person"},
   "rangeIncludes": {"@id": "http://schema.org/Text"}, "sh:minCount": 1}
 ]}
```
The string line stands for the four root-detection entities: replace it with them.

## Pitfalls seen in real profiles

- **`sh:` prefix.** Older MASP crates use `sh:minCount` without defining `sh` in the
  context, so in JSON-LD they are not SHACL terms. Define `"sh": "http://www.w3.org/ns/shacl#"`
  in new crates and keep writing the key `sh:minCount` (the validator reads the key).
- **Loose literals.** Counts appear as numbers, strings (`"1"`) and even `[]`; write integers.
- **Rule `@id`s** may be local (`#class_X`), compact (`ldac:AccessTypes`) or absolute; refer
  to them consistently, as tools compare expanded ids.
- **Ranges written as words** (`{"@id": "Text"}`) are relative IRIs in JSON-LD but meant as
  schema.org types; prefer `http://schema.org/Text`.
- **`http` versus `https` schema.org.** RO-Crate contexts and most profiles use
  `http://schema.org/`; MASP's schema.org schema crate uses `https://`. Use `http://`.
- **Bioschemas IRIs changed in RO-Crate 1.3**: `ComputationalWorkflow` is
  `https://bioschemas.org/terms/ComputationalWorkflow` (1.1/1.2: `https://bioschemas.org/ComputationalWorkflow`).
  The upstream Workflow profile uses the 1.2 form, so 1.3 workflow crates may not match
  its class rule; say so rather than downgrading the crate.
- **Same identifier, different profiles.** The LDAC profile in the MASP examples and the
  one `https://w3id.org/ldac/profile` redirects to differ (99 versus 101 property rules).
  Note which copy, commit or checksum you used.
- **Profiles without MASP rules.** Many registered profiles (e.g. FAIRSCAPE) are Profile
  Crates whose `schema` resource is JSON Schema or SHACL, not MASP rules; MASP tools
  refuse them. Use the profile's own validator.
- **Schema crates not linked from the root.** A frozen LDAC schema crate has its schema
  descriptor in the graph but not in the root's `hasResource`, so the validator finds no
  rules. `scripts/masp_rules.py` reports this.

## Mapping to SHACL

See [shacl.md](shacl.md): `scripts/masp_to_shacl.py` converts the rules to a rocrate-validator
profile folder, targeting the root through the validator's own `RootDataEntity` class (the
layered approach) and class counts as SPARQL constraints.
