---
name: ro-crate-publish
description: Package, distribute and publish an RO-Crate: zip, BagIt, .eln, attached versus detached crates and converting between them, serving ro-crate-metadata.json with the right media type, persistent identifiers with Signposting, and depositing to WorkflowHub, Zenodo or InvenioRDM. Use when the user wants to share, archive, upload, host, cite or hand over a finished crate.
---

# Packaging and publishing RO-Crates

Spec: https://www.researchobject.org/ro-crate/specification/1.3/structure and `/appendix/implementation-notes`, `/appendix/relative-uris`.

Before publishing: validate (`ro-crate-validator`), check there is no private or unlicensed content, that `license`, `author` and `datePublished` are real, and that no identifier (DOI, ORCID) was invented. Publishing is hard to undo, so confirm the destination with the user before uploading anything.

## Package forms
- **Attached crate** = a directory whose root holds `ro-crate-metadata.json` (+ optional `ro-crate-preview.html`, `ro-crate-preview_files/`, payload). Zip it with the crate files at the **zip root** (or in one top-level folder): `rocrate write-zip -c <dir> out.zip` (ro-crate-py) or `zip -r`.
- **Detached crate** = a stand-alone metadata document; every data entity is a web URL; file name may be `<prefix>-ro-crate-metadata.json`, but the descriptor `@id` stays `ro-crate-metadata.json`.
- **`.eln`** (electronic lab notebooks): a zip containing one folder that is the crate root.
- **Workflow RO-Crate** for WorkflowHub: a ZIP named `*.crate.zip`.

## BagIt (checksummed transfer)
Put the crate root in the bag's payload: `bag/{bagit.txt, bag-info.txt, manifest-sha512.txt, data/ro-crate-metadata.json, data/...}`. The manifest must list **every** payload file including `data/ro-crate-metadata.json`; `bagit.txt` = `BagIt-version: 1.0` + `Tag-File-Character-Encoding: UTF-8`. Without a bag tool: `find data -type f -print0 | xargs -0 sha512sum > manifest-sha512.txt`; verify with `sha512sum --quiet -c manifest-sha512.txt`. Add `External-Identifier: urn:uuid:<fresh uuid>` to `bag-info.txt` for a stable base URI. `fetch.txt` can name big external files (also give them a `url`/`contentUrl` in the crate). Checksums detect accidents, not tampering.

## Attached to detached (and back)
- Attached to detached: choose public URLs for each data file, make every data entity's `@id` absolute, list nested directories' content in `hasPart` or give a `distribution`, keep the descriptor `@id` `ro-crate-metadata.json` (put its URL in `contentUrl`); if the crate is already online, rewrite with JSON-LD flattening and a new `@base` (relative-URI appendix).
- Detached to attached: first look for a root `distribution` download; for a snapshot create a folder, save the metadata as `ro-crate-metadata.json`, copy the absolute root `@id` into `identifier`, optionally make the root `./`. To also download web files: use `localPath` (else derive from the parent dataset), check `contentSize`, record the old URL as `contentUrl`, make the `@id` relative (encode paths). Treat the result as a **fork** if anything could not be fetched: remove the old `identifier`, add `isBasedOn`, add yourself as `author`/`contributor`, fix `datePublished`/`publisher`, record a change action.

## Serving on the web
Serve `ro-crate-metadata.json` as `application/ld+json; profile="http://www.w3.org/ns/json-ld#flattened http://www.w3.org/ns/json-ld#compacted https://w3id.org/ro/crate"` (Apache `ForceType`, nginx `default_type`; or a `.jsonld` alias on static hosts), with CORS if browsers read it. Do not put real data behind a server that cannot enforce access rules.

## Persistent identifiers and discovery
Root `identifier` (`PropertyValue` for a DOI; or use the DOI URL as root `@id`) and `cite-as`; the landing page or archive response should repeat it as `Link: <pid>; rel="cite-as"` and advertise the crate with `rel="describedby"` (metadata) or `rel="item"` (archive, `profile="https://w3id.org/ro/crate"`). See `ro-crate-retrieve` for how consumers resolve this. Only mint or claim identifiers you actually hold.

## Repositories and tools (check the tools list for status)
- WorkflowHub accepts Workflow RO-Crates (`*.crate.zip`) and serves one per workflow with Signposting.
- `ro-crate-zenodo` (alpha): upload to Zenodo and fill its metadata from the crate. `ro-crate-inveniordm` (alpha): InvenioRDM. `ro-crates-deposit` is inactive.
- Static sites: `ro-crate-preview` GitHub Action, `rocrate-to-pages`.
Details and current status: https://www.researchobject.org/ro-crate/tools . Run a tool against a test/sandbox record first when one exists.
