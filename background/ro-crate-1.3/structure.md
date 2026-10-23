# RO-Crate Structure {#structure}









## Types of RO-Crate

An [*RO-Crate Metadata Document*](#ro-crate-metadata-document-ro-crate-metadatajson) is used to package data in one of two ways:

1.  An *Attached RO-Crate Package* that defines an on-disk collection of data:

-   It is defined within a file-system-like service as a directory (known as the *RO-Crate Root*) with the *RO-Crate Metadata Document* saved in a file-like entity with a file name of `ro-crate-metadata.json`.
-   References to files and directories in the *RO-Crate Metadata Document* are present in the RO-Crate or available online as [Web-based Data Entities](data-entities.md#web-based-data-entities).
-   Typically, software processing an *Attached RO-Crate Package* would be passed a path to a directory or a zip file.

2.  A *Detached RO-Crate Package*:
    -   Is defined by a stand-alone *RO-Crate Metadata Document* which may be stored in a file or distributed via an API.
    -   References to files and directories in the *RO-Crate Metadata Document* are all Web-based Data Entities.
    -   If stored in a file, known as a *Detached RO-Crate Metadata File*, the filename SHOULD be `${prefix}-ro-crate-metadata.json` rather than `ro-crate-metadata.json` where the variable `${prefix}` is a human readable version of the dataset's ID or name, to signal that on disk, the presence of the file does not indicate an *Attached RO-Crate Data Package*.
    -   Typically, software processing a *Detached RO-Crate Package* would be passed a path to a file, an absolute URI, or a JSON string or object, without a directory context.

RO-Crate Metadata Documents MAY also be processed in non-packaging contexts by tools such as website generators or crate visualizers, where data entities are not processed, or in applications which use RO-Crate conventions for representing context (such as a schema definition using Schema.org conventions).

**Note**: Client software may provide modes which force a particular packaging mode to be assumed. For example, if the software is passed a directory, then it would assume that is processing an *Attached RO-Crate Package*. If passed a path to a file, it could work in *Detached RO-Crate Package* mode, and possibly attempt to resolve *Web Based Data Entities*. It could also provide a mode to simply parse the document and process it without referencing or validating Data entities in any special way.

In all crates the metadata is completed with [contextual entities](introduction.md#contextual-entities) that further describe the relationships and context of the data to form a *Research Object*.

## RO-Crate Metadata Document (`ro-crate-metadata.json`)

[JSON-LD](https://json-ld.org/) is a structured form of [JSON](http://json.org/) that can represent a *Linked Data* graph.

-   The *RO-Crate Metadata Document* MUST be a document which is valid [JSON-LD 1.0](https://www.w3.org/TR/2014/REC-json-ld-20140116/) in [flattened](https://www.w3.org/TR/json-ld/#flattened-document-form) and [compacted](https://www.w3.org/TR/json-ld/#compacted-document-form) form.
-   The *RO-Crate JSON-LD* MUST use the *RO-Crate JSON-LD Context* <https://w3id.org/ro/crate/1.3/context> by reference.

The graph MUST describe:

1.  The [RO-Crate Metadata Descriptor](introduction.md#ro-crate-metadata-descriptor)
2.  The [Root Data Entity](root-data-entity.md#direct-properties-of-the-root-data-entity)
3.  Zero or more [Data Entities](introduction.md#data-entities)
4.  Zero or more [Contextual Entities](introduction.md#contextual-entities)

Any referenced *contextual entities* SHOULD also be described in the *RO-Crate Metadata Document* with the same identifier. Similarly any *contextual entity* in the *RO-Crate Metadata Document* SHOULD be linked to from at least one of the other entities using the same identifier.

The appendix [RO-Crate JSON-LD](appendix/jsonld.md#jsonld) details the general structure of the JSON-LD that is expected in the *RO-Crate Metadata Document*. In short, the rest of this specification describes the different types of entities that can be added as `{}` objects to the *RO-Crate JSON-LD* `@graph` array below:

``` json
{ "@context": "https://w3id.org/ro/crate/1.3/context",
  "@graph": [

  ]
}
```

## Attached RO-Crate Package

An **Attached RO-Crate Package** is used to contain and describe an optional *payload* of files and directories as well as web-based data entities along with their contextual information.

When processing an *Attached RO-Crate Package* the *RO-Crate Metadata Document* MUST be present in the *RO-Crate Root* and it MUST be named `ro-crate-metadata.json`.

An *Attached RO-Crate Package* can be stored and published in multiple ways depending on its use:

-   On a typical hierarchical *file system* (e.g. `/files/shared/crates/my-crate-01/`)
-   Exposed as a *Web resource* within a folder structure (e.g. <https://www.researchobject.org/2021-packaging-research-artefacts-with-ro-crate/>)
-   [*Packaged*](appendix/implementation-notes.md#combining-with-other-packaging-schemes) within a ZIP file, [BagIt](https://en.wikipedia.org/wiki/BagIt) archive or [OCFL](https://ocfl.io/) structure
-   *Archived* as a set of named files in other ways (e.g. Zenodo deposit)

A valuable feature of the *Attached RO-Crate Package* approach is that the metadata is preserved when a crate is transferred between these types of storage/publication systems.

The file path structure an *Attached RO-Crate Package* MUST follow is:

    <RO-Crate root directory>/
    |   ro-crate-metadata.json    # RO-Crate Metadata File containing the RO-Crate Metadata Document MUST be present 
    |   ro-crate-preview.html     # RO-Crate Website homepage MAY be present
    |   ro-crate-preview_files/   # MAY be present
    |    | [other RO-Crate Website files]
    |   [payload files and directories]  # 0 or more

The name of the *RO-Crate root* directory is not defined, but a root directory is identifiable by the presence of the *RO-Crate Metadata File*, `ro-crate-metadata.json`. For instance, if an *RO-Crate* is archived in a ZIP-file, the ZIP root directory is an *RO-Crate root* directory if it contains `ro-crate-metadata.json`.

The payload files and directories MAY be described within the *RO-Crate Metadata File* as [Data Entities](introduction.md#data-entities). Additional Web-based Data Entities MAY also be described, but are not considered part of the payload.

The `@id` of the *Root Data Entity* in an *Attached RO-Crate Package* MUST be either `./` or be a URI, such as a DOI URL or other persistent URL which is considered to be the main identifier of the *Attached RO-Crate Package*.

**Note**: Earlier versions of RO-Crate mandated an `@id` of `./` as a convention for identifying the *Root Data Entity*, but the use of the *RO-Crate Metadata Descriptor* means that this is no longer required, freeing-up the *Root Data Entity* `@id` to be used to indicate what should be considered the canonical URI for an RO-Crate Package. Other mechanisms for specifying the 'main identifier' involve multiple JSON-LD entities and may be ambiguous.

### Payload files and directories

These are the actual files and directories that make up the **payload** of the dataset being described in an *Attached RO-Crate Package*.

The base RO-Crate specification makes no assumptions about the presence of any specific files or folders beyond the reserved RO-Crate files described above.

Payload files may appear directly in the *RO-Crate Root* alongside the *RO-Crate Metadata File*, and/or appear in sub-directories of the *RO-Crate Root*. Each file and directory MAY be represented as [Data Entities](introduction.md#data-entities) in the *RO-Crate Metadata File*.

An RO-Crate may also contain Web-based Data Entities that are not present as part of the payload and referenced using absolute URIs. These may require additional preservation measures.

**Tip**: An RO-Crate [packaged with BagIt](appendix/implementation-notes.md#adding-ro-crate-to-bagit) may [reference external files](appendix/implementation-notes.md#referencing-external-files) which are not present in the *RO-Crate Root* hierarchy until the BagIt has been *completed*. This method for referencing external files can be used for files that are large, require authentication or otherwise inconvenient to transfer with the RO-Crate, but which should nevertheless still be considered part of the *payload*. RO-Crate has a similar mechanism for referencing such external files using both an `@id` to reference a local path and [contentUrl](http://schema.org/contentUrl) property to indicate a source for that data. See the section on [File Data Entities](data-entities.md#file-data-entity).

### RO-Crate Website (`ro-crate-preview.html` and `ro-crate-preview_files/`) for Packages

In addition to the machine-oriented *RO-Crate Metadata Document*, an *Attached RO-Crate Package* MAY include a human-readable HTML rendering of the same information, known as the *RO-Crate Website*. If present, the *RO-Crate Website* MUST be a file named `ro-crate-preview.html` in the root directory, which MAY serve as the entry point to other web-resources, which MUST be in `ro-crate-preview_files/` in the root directory.

If present in the root directory of an *Attached RO-Crate Package* as `ro-crate-preview.html` (or otherwise served in a *Detached RO-Crate Package*), the RO-Crate Website MUST:

-   Be a valid [HTML 5](https://www.w3.org/TR/html52/) document
-   Be useful to users of the RO-Crate - this will vary by community and intended use, but in general the aim is to assist users in reusing data by explaining what it is, how it was created, how it can be used and how to cite it. One simple approach to this is to expose *all* the metadata in the *RO-Crate Metadata Document*.

`ro-crate-preview.html` SHOULD:

-   Display at least the metadata relating to the *Root Data Entity* as static HTML without the need for scripting. It MAY contain extra features enabled by JavaScript.
-   When a *Data Entity* or *Contextual Entity* is referenced by its ID:
    -   If it has a [name](http://schema.org/name) property, provide a link to its HTML version.
    -   If it does not have a name (e.g. a [GeoCoordinates](http://schema.org/GeoCoordinates) location), show it embedded in the HTML for the entity.
    -   For external URI values, provide a link.
-   For keys that resolve in the `RO-Crate JSON-LD Context` to a URI, indicate this (the simplest way is to link the key to its definition).
-   If there are additional resources necessary to render the preview (e.g. CSS, JSON, HTML), link to them in a subdirectory `ro-crate-preview_files/`

**Note**: Previous versions of the Specification recommended that the *RO-Crate Website* should contain a redundant copy of the RO-Crate Metadata Document, but there is no evidence that this has been useful and it is no longer recommended.

The *RO-Crate Website* is not considered a part of the RO-Crate payload in an *Attached RO-Crate Package*, but serves as a way to make metadata available in a user-appropriate format. The `ro-crate-preview.html` file and the `ro-crate-preview_files/` directory and any contents SHOULD NOT be included in the `hasPart` property of the *Root Dataset* or any other `Dataset` entity within an RO-Crate.

Metadata about parts of the *RO-Crate Website* MAY be included in an RO-Crate as in the following example. Metadata such as an `author` property, `dateCreated` or other provenance can be included, including details about the software that created them, as described in [Software used to create files](provenance.md#software-used-to-create-files).

    {
          "@id": "ro-crate-preview.html",
          "@type": "CreativeWork",
          "about": {"@id": "./"}
    }

    {
          "@id": "https://www.npmjs.com/package/ro-crate-html-js",
          "@type": "SoftwareApplication",
          "url": "https://www.npmjs.com/package/ro-crate-html-js",
          "name": "ro-crate-html-js",
          "version": "1.4.19"
    }

    {
          "@id": "#ro-crate-preview-generation",
          "@type": "CreateAction",
          "name": "Create HTML summary",
          "endTime": "2022-10-019T17:01:07+10:00",
          "instrument": {
            "@id": "https://www.npmjs.com/package/ro-crate-html-js"
          },
          "object": {
            "@id": "ro-crate-metadata.json"
          },
          "result": {
            "@id": "ro-crate-preview.html"
          }
    }

### Self-describing and self-contained

*Attached RO-Crates Packages* SHOULD be self-describing and self-contained.

A minimal *Attached RO-Crate Package* is a directory containing a single *RO-Crate Metadata Document* stored as an [RO-Crate Metadata File](root-data-entity.md#root-data-entity) `ro-crate-metadata.json`.

At the basic level, an Attached RO-Crate Package is a collection of files and resources represented as a Schema.org [Dataset](http://schema.org/Dataset), that together form a meaningful unit for the purposes of communication, citation, distribution, preservation, etc. The *RO-Crate Metadata Document* describes the RO-Crate, and MUST be stored in the *RO-Crate Root*.

While RO-Crate is well catered for describing a *Dataset* as files and relevant metadata that are *contained* by the RO-Crate in the sense of living within the same root directory, RO-Crates can also reference external resources which are stored or accessed separately, via absolute URIs. This is particularly recommended where some resources cannot be co-hosted for practical or legal reasons, or if the RO-Crate itself is primarily web-based.

It is important to note that the *RO-Crate Metadata Document* is **not necessarily an exhaustive manifest** or inventory, that is, it is not required to list or describe all files in the package. Rather it is focused on providing sufficient amount of metadata to understand and use the content, and is designed to be compatible with existing and future approaches that *do* have full inventories / manifest and integrity checks, e.g. by using checksums, such as BagIt and Oxford Common File Layout [OCFL Objects](https://ocfl.io/1.0/spec/#object-spec).

The intention is that RO-Crates can work well with a variety of archive file formats, e.g. tar, zip, etc., and approaches to capturing file manifests and file fixity, such as BagIt, OCFL and [git](https://git-scm.com/) (see also appendix [Combining with other packaging schemes](appendix/implementation-notes.md#combining-with-other-packaging-schemes)). An RO-Crate can also be hosted on the web or mainly refer to web resources, although extra care to ensure persistence and consistency should be taken for archiving such RO-Crates.

## Detached RO-Crate Package

A *Detached RO-Crate Package* is an RO-Crate, defined in an *RO-Crate Metadata Document* without a defined root directory, where the *RO-Crate Metadata Document* content is accessed independently (e.g. as part of a programmatic API).

Unlike an *Attached RO-Crate Package*, a *Detached RO-Crate Package* is not processed in a file-system context and thus does not carry a data *payload* in the same sense, but may reference data deposited separately, or purely reference [contextual entities](introduction.md#contextual-entities).

In a *Detached RO-Crate Package* the [root data entity](root-data-entity.md#root-data-entity) SHOULD have an @id which is an absolute URL if it is available online. If it is not yet, or will never be available online then @id MAY be any valid URI - including `./`.

Any [data entities](introduction.md#data-entities) in a *Detached RO-Crate Package Package* MUST be Web-based Data Entities.

A Detached RO-Crate Package may still use `#`-based local identifiers for [contextual entities](introduction.md#contextual-entities).

The concept of an *RO-Crate Website* is undefined for a *Detached RO-Crate Package*.

To distribute a *Detached RO-Crate Package* and optionally to provide an RO-Crate Website, any *Detached RO-Crate Package* can be saved in a directory (and zipped or otherwise bundled) and will function as an *Attached RO-Crate Package* with no payload data. See the [appendix on converting from Detached to Attached RO-Crate Package](appendix/relative-uris.md#converting-from-detached-to-attached-ro-crate-package) for further guidance on this.



```{=html}
<!--
   Copyright 2019-2020 University of Technology Sydney
   Copyright 2019-2024 The University of Manchester UK 
   Copyright 2019-2024 RO-Crate contributors <https://github.com/ResearchObject/ro-crate/graphs/contributors>

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
-->
```
