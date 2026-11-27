# MASP tools: tested usage

Run on 2026-11-27 with `@crate-works/ro-crate-masp-validator` 0.1.0, `@crate-works/ro-crate-masp-tools`
0.1.0 (Node 22) and wpsld-cli 0.8.0, on the upstream examples and this repository's fixtures.
Install the npm tools in a project or scratch folder (`npm install --save-dev ...`), not globally.

## Contents
- masp-validate
- generate-masp-docs
- generate-mode-file
- mode-to-masp
- generate-schema-org-crate
- owl-to-masp.py
- wpsld-cli

## masp-validate
```bash
npm install @crate-works/ro-crate-masp-validator@0.1.0
npx masp-validate [--json] target/ro-crate-metadata.json profile-crate/ro-crate-metadata.json
```
- Local files only (fetch a profile first, `ro-crate-retrieve`). Exit 0 pass, 2 errors, 1 unreadable.
- **Errors are class counts only.** Property rules decide whether an entity counts as a valid
  instance, so a missing root `license` is reported as
  `Expected at least 1 instances of RO-Crate Metadata Descriptor ... found 0` (the descriptor's
  `about` no longer reaches a valid root). The cause is only in `--json`, under
  `rules.<rule>.<entity>.property-errors`. A stray entity failing its rules is not reported at all.
- `--json` prints the JSON and then the `[ERROR]` lines on stdout; strip them before `jq`:
  ```bash
  npx masp-validate --json crate.json profile.json | sed '/^\[ERROR\]/d' \
    | jq -r '.rules[][]["property-errors"][]?.message'
  ```
  This also lists failures of entities that merely share a type (e.g. a licence `CreativeWork`
  failing the descriptor rule's `about`): read the ones on entities that matter.
- The MASP profile validates itself, and the minimal profile in `masp-format.md` passes it.

## generate-masp-docs
```bash
npx generate-masp-docs [-x] [--multi-page] <crate>/ro-crate-metadata.json profile-text.md [out.md]
```
Writes `profile-documentation.md` (default, next to the crate) **and** `index.html`. The template
needs `${rules.all}` (also `${rules.allItemLists}`, `${rules.allDefinedTermSets}`). Outside a git
repository it prints `fatal: not a git repository` but still succeeds (provenance links are left
out). `-x` creates or syncs `ro-crate-metadata.xlsx`; the newer of JSON and spreadsheet wins, so
commit before running it. The JSON was unchanged when it was newer.

## generate-mode-file
```bash
npx generate-mode-file --output <crate>/crate-o-mode.json --update-profile <crate>/ro-crate-metadata.json [--input full-mode.json]
```
Writes a minimal Crate-O mode file (metadata, groups, lookups, enabled classes) and **edits the
profile crate**: adds `crate-o-mode.json` as a `File`, a `#hasEditorMode` `ResourceDescriptor`
(role `https://w3id.org/ro/mode`) and the role's `DefinedTerm`. The profile still passed the MASP profile.

## mode-to-masp
```bash
npx mode-to-masp -m full-mode.json -p <profile>/profile-crate [-n https://example.org/terms#]
```
Converts a full Crate-O mode file into a profile crate, and also writes `output/mode-masp/`
in the current folder. A first draft only: from the LDAC mode file it used the deprecated
`value` on a property rule and left ranges to class rules it did not create
(`scripts/masp_rules.py` reported 13 errors). Fix before use.

## generate-schema-org-crate
```bash
npx generate-schema-org-crate --output schemas/schema-org/schema-crate/ro-crate-metadata.json
```
Downloads the **current** schema.org release (not the 30.0 that RO-Crate 1.3 uses) and writes a
1.7 MB schema crate (939 classes, 1538 properties, 546 enumeration values). `--help` is ignored:
it runs the conversion into `schemas/schema-org/...` of the current folder.

## owl-to-masp.py
```bash
uv run node_modules/@crate-works/ro-crate-masp-tools/scripts/owl-to-masp.py \
  -i ontology.ttl -o schemas/my-schema -n https://example.org/ns# --name "My ontology"
```
Needs `uv` (installs rdflib itself). Writes `schema-crate/ro-crate-metadata.json`, a copy of the
ontology and `schema-text.md`. Rules keep the ontology IRIs as `@id`s and have no
`prov:specializationOf` (they match their own `@id`); anonymous `owl:Restriction` superclasses are
skipped with a warning. A schema crate has no root rules: write a profile on top of it.

## wpsld-cli
The command-line part of the [wpsld](https://github.com/stain/wpsld) editor, in every release zip
(`wpsld/bin/wpsld-cli`, `wpsld\wpsld-cli.exe`, `wpsld.app/Contents/MacOS/wpsld-cli`; the portable
zip needs Java 25 only). Verify the zip with the release's `SHA256SUMS`.
```bash
wpsld-cli check [--json] [--offline] CRATE    # CRATE: folder or metadata file; exit 0/1/2
wpsld-cli repair --dry-run CRATE             # then without --dry-run (in place) or -o out.json
wpsld-cli preview [-o page.html] CRATE       # ro-crate-preview.html
```
- `check` applies the MASP profiles named in the root's `conformsTo` (bundled, kept by the
  editor, or fetched; `--offline` uses only bundled or kept ones), else the bundled core RO-Crate
  MASP profile, plus RO-Crate requirements and the folder's files. It checks every entity
  (stricter than `masp-validate`) and names the problem plainly ("The root data entity must have
  a license"). `--json` follows rocrate-validator's JSON report.
- A declared profile without MASP rules (Workflow RO-Crate, Process Run Crate) is reported as
  "Profile not found ... no rules" and the crate is checked against the core profile only: a pass
  then says nothing about that profile; use rocrate-validator for it.
- Passed the repository's 1.0 (`.jsonld`, with a warning), 1.1, detached and Profile Crate
  fixtures; failed the invalid one with its four problems. A folder holding only a detached
  `*-ro-crate-metadata.json` needs the file path.
- `repair` (offline) links SPDX licences and PRONOM formats, normalises ORCID/ROR/DOI forms, and
  adds entities that are referred to but missing **as `Thing` placeholders**, and links unlinked
  entities from the root's `mentions`: review with `--dry-run` and name and type what it adds.
- `preview` will not overwrite another tool's preview without `--replace-other` (moves it to
  `ro-crate-preview_files/`); `--describe` also adds the preview to the metadata.
