# Terminology

*RO-Crate*: A dataset, which is described in a JSON-LD *RO-Crate Metadata Document*.

*RO-Crate Metadata Document*: A JSON-LD document that describes the *RO-Crate* with structured data in form of *RO-Crate JSON-LD*. This may be stored in a file-system as an *RO-Crate Metadata File*, served via web site or via an API.

*RO-Crate Metadata File*: An *RO-Crate Metadata Document* stored in a file named `ro-crate-metadata.json` in the *RO-Crate Root* of an *Attached RO-Crate Package*. See section [RO-Crate Metadata Document](structure.md#ro-crate-metadata-document-ro-crate-metadatajson).

*Attached RO-Crate Package*: A file system directory which functions as a packaged dataset, indicated by the presence of the *RO-Crate Metadata File*. An *Attached RO-Crate Package* carries a payload of zero or more files. See section [Types of RO-Crate](structure.md#types-of-ro-crate).

*Detached RO-Crate Package*: A stand-alone *RO-Crate Metadata Document* which defines a virtual data package by referencing online materials. A *Detached RO-Crate Package* does not have a payload. See section [Types of RO-Crate](structure.md#types-of-ro-crate).

*Detached RO-Crate Metadata File*: An *RO-Crate Metadata Document* stored in a file named `${prefix}-ro-crate-metadata.json` or `ro-crate-metadata.json` where `${prefix}`, if present, is a file-system safe version identifier or name for the RO-Crate.

*RO-Crate Root*: The top-level directory of an *RO-Crate Package*. See section [RO-Crate structure](structure.md#structure).

*RO-Crate Metadata Descriptor*: A *Contextual Entity* of type [CreativeWork](http://schema.org/CreativeWork), which describes the *RO-Crate Metadata Document* and links it to the *Root Data Entity*. See section [RO-Crate Metadata Descriptor](introduction.md#ro-crate-metadata-descriptor)

*RO-Crate Website*: Human-readable HTML pages which describe the RO-Crate (i.e. the *Root Data Entity*, its *Data Entities* and *Context Entities*), with a home-page at `ro-crate-preview.html`. See section [RO-Crate Website](structure.md#ro-crate-website-ro-crate-previewhtml-and-ro-crate-preview_files-for-packages).

*Type*: A classification of objects or their descriptions. The type (or "class") is given as a short-hand *key*, mapped by the *RO-Crate JSON-LD Context* to a *URI* that has the type definition. See appendix [RO-Crate JSON-LD](appendix/jsonld.md#jsonld).

*Data Entity*: A JSON-LD representation (in the *RO-Crate Metadata Document*) of a directory, file, or other Web resource which is considered *contained* by the *RO-Crate*. See section [Data entities](introduction.md#data-entities).

*Property*: A relationship from one *entity* to another entity, or to a *value*. The type of relationship is identified by a *URI*, mapped to a *key* by *JSON-LD*. See appendix [RO-Crate JSON-LD](appendix/jsonld.md#jsonld).

*Root Data Entity*: A *Data Entity* of *type* [Dataset](http://schema.org/Dataset), representing the RO-Crate as a whole. See section [Root Data Entity](root-data-entity.md#root-data-entity).

*JSON-LD*: A JSON-based file format for storing *Linked Data*. This document assumes [JSON-LD 1.0](https://www.w3.org/TR/2014/REC-json-ld-20140116/). JSON-LD use a *context* to map from JSON keys to *URIs*. See appendix [RO-Crate JSON-LD](appendix/jsonld.md#jsonld).

*JSON*: The *JavaScript Object Notation (JSON) Data Interchange Format* as defined by [RFC 7159](https://tools.ietf.org/html/rfc7159); a structured text file format that can be programmatically consumed and generated in a wide range of programming languages. The main JSON structures are *objects* (`{}`) indexed by *keys*, sequential *arrays* (`[]`) and literal *values* (`""`).

*Contextual Entity*: A JSON-LD representation of an entity associated with another *Entity*, in order to adequately describe it. For example, a [Person](http://schema.org/Person), [Organization](http://schema.org/Organization) (including research projects), item of equipment ([IndividualProduct](http://schema.org/IndividualProduct)), [license](http://schema.org/license) or any other *thing* or *event* that forms part of the metadata for a *Data Entity*. *Properties* of contextual entities may refer to further entities. See section [Contextual Entities](introduction.md#contextual-entities).

*Linked Data*: A data structure where properties, types and resources are identified with *URIs*, which if retrieved over the Web, further describe or provide the identified property/type/resource.

*URI*: A *Uniform Resource Identifier* as defined in [RFC 3986](https://tools.ietf.org/html/rfc3986), for example `http://example.com/path/file.html` - commonly known as *URL*. In this document the term *URI* includes *IRI*, which also permit international Unicode characters. The URI identifies a downloadable resource (e.g. an image) or a concept (e.g. a *type* definition).

*URI Path*: The relative *path* element of an *URI* as defined in [RFC3986 section 3.3](https://tools.ietf.org/html/rfc3986#section-3.3), e.g. `path/file.html`

*RO-Crate JSON-LD Context*: A JSON-LD [context](https://www.w3.org/TR/json-ld/#the-context) that provides Linked Data mapping for RO-Crate metadata to vocabularies like [Schema.org](http://schema.org). This mapping assigns meaning to the JSON keys, see appendix [RO-Crate JSON-LD](appendix/jsonld.md#jsonld).

*RO-Crate JSON-LD*: JSON-LD that use the *RO-Crate JSON-LD Context* and contain RO-Crate metadata, written as if [flattened](https://www.w3.org/TR/json-ld/#flattened-document-form) and then [compacted](https://www.w3.org/TR/json-ld/#compacted-document-form) according to the rules in JSON-LD 1.0. The *RO-Crate JSON-LD* for an *RO-Crate* is stored or transmitted in the \_RO-Crate Metadata Document.

## Linked Data conventions

Throughout this specification, RDF terms (*properties*, *types*) are referred to using the *keys* defined in the *RO-Crate JSON-LD Context*.

Following [Schema.org](http://schema.org) practice, `property` names start with lowercase letters and `Type` names start with uppercase letters.

In the *RO-Crate Metadata Document* the RDF terms use their RO-Crate JSON-LD names as defined in the *RO-Crate JSON-LD Context*, which is available at <https://w3id.org/ro/crate/1.3/context>



```{=html}
<!--
   Copyright 2019-2020 University of Technology Sydney
   Copyright 2019-2023 The University of Manchester UK 
   Copyright 2019-2023 RO-Crate contributors <https://github.com/ResearchObject/ro-crate/graphs/contributors>

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
