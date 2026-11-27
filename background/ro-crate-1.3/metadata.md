# RO-Crate Metadata {#metadata}









RO-Crate aims to capture and describe the [Research Object](https://www.researchobject.org/) using structured *metadata*. Specifically, an RO-Crate is described using *JSON-LD* by an *RO-Crate Metadata Document*. As explained in section [RO-Crate Structure](structure.md#structure) this may be stored in an *RO-Crate Metadata File*.

The *RO-Crate Metadata Document* contains the metadata that describes the RO-Crate and its content, in particular:

-   [Root Data Entity](root-data-entity.md#root-data-entity) - the RO-Crate `Dataset` itself, a gathering of data
-   [Data Entities](introduction.md#data-entities) - the *data* payload, in the form of files and folders
-   [Contextual Entities](introduction.md#contextual-entities) - related things in the world (e.g. people, organizations, places), providing provenance for the data entities and the RO-Crate.

This machine-readable metadata can also be represented for human consumption in the *RO-Crate Website*, linking to data and Web resources.

## RO-Crate uses Linked Data principles

RO-Crate makes use of the [Linked Data principles](https://5stardata.info/en/) for its description. In particular:

1.  (Meta)data should be made available as **Open Data** on the web.
2.  (Meta)data should be **machine-readable** in a structured format.
3.  (Meta)data should *not* require proprietary software packages.
4.  (Meta)data should use [open standards from W3C](https://www.w3.org/standards/), such as RDF and SPARQL.
5.  (Meta)data should **link** to other people's data to provide context, using *URIs* as global identifiers

RO-Crate realizes these principles using a particular set of technologies and best practices:

1.  The *RO-Crate Metadata Document* can be stored in an *RO-Crate Metadata File*. The *RO-Crate Metadata File* and an *RO-Crate Website* can be directly published on the web together with the RO-Crate payload. In addition, a data package (e.g. BagIt Zip archive) that contains the RO-Crate can also be published on the web.
2.  The *RO-Crate Metadata Document* is based on the structured data format [JSON-LD](https://json-ld.org/).
3.  Multiple open source tools/libraries are available [for JSON](http://json.org/) and [for JSON-LD](https://json-ld.org/).
4.  The *RO-Crate Website* is [HTML 5](https://www.w3.org/TR/html52/), and the *RO-Crate Metadata Document* is [JSON-LD](https://json-ld.org/), one of the [W3C RDF 1.1 formats](https://www.w3.org/TR/rdf11-primer/).
5.  The *RO-Crate Metadata Document* reuses common vocabularies like [Schema.org](http://schema.org), and this specification [recommends identifiers](#recommended-identifiers) it should link to.

## Common principles for RO-Crate entities

For all entities listed in an *RO-Crate Metadata Document* the following principles apply:

1.  The entity MUST have an `@id` (see [Describing entities in JSON-LD](appendix/jsonld.md#describing-entities-in-json-ld)).
2.  The entity MUST have a `@type`, which MAY be an array.
3.  The `@type` SHOULD include at least one [Schema.org](http://schema.org) type that accurately describes the entity. [Thing](http://schema.org/Thing) or [CreativeWork](http://schema.org/CreativeWork) are valid fallbacks if no alternative external or ad-hoc term is found (see [Extending RO-Crate](appendix/jsonld.md#extending-ro-crate)).
4.  The entity SHOULD have a human-readable `name`, in particular if its `@id` does not go to a human-readable Web page.
5.  The properties used on the entity SHOULD be applicable to the `@type` (or superclass) according to their definitions. For instance, the property [publisher](http://schema.org/publisher) can be used on a [Dataset](http://schema.org/Dataset) as it applies to its superclass [CreativeWork](http://schema.org/CreativeWork).
6.  Property references to other entities (e.g. `author` property to a `Person` entity) MUST use the `{ "@id": "..."}` object form (see [JSON-LD appendix](appendix/jsonld.md#jsonld)).
7.  The entity SHOULD be ultimately referenceable from the root data entity (possibly through another reachable [data entity](introduction.md#data-entities) or [contextual entity](introduction.md#contextual-entities)).

## Base metadata standard: Schema.org

[Schema.org](http://schema.org) is the base metadata standard for RO-Crate. Schema.org was chosen because it is widely used on the World Wide Web and supported by search engines, on the assumption that discovery is likely to be maximized if search engines index the content.

**Note**: As far as we know there is no alternative, well-maintained linked-data schema for research data with the coverage needed for this project - i.e. a single standard for expressing all the examples presented in this specification.

RO-Crate relies heavily on [Schema.org](http://schema.org), using a constrained subset of [JSON-LD](https://json-ld.org/), and this specification gives opinionated recommendations on how to represent the metadata using existing [linked data](https://en.wikipedia.org/wiki/Linked_data) best practices.

**Tip**: The main principle of RO-Crate is to use a [Schema.org](http://schema.org) term whenever possible, even if its official definition may seem broad or related to every day objects. For instance, [IndividualProduct](http://schema.org/IndividualProduct) can describe scientific equipment and instruments (see [Provenance of entities](provenance.md#provenance)). RO-Crate implementers are free to use additional properties and types beyond this specification (see also appendix [Extending RO-Crate](appendix/jsonld.md#extending-ro-crate)).

### Differences from Schema.org

Generally, the standard *type* and *property* names (*terms*) from [Schema.org](http://schema.org) should be used. However, RO-Crate uses variant names for some elements, specifically:

-   `File` is mapped to <http://schema.org/MediaObject> which was chosen as a compromise as it has many of the properties that are needed to describe a generic file. Future versions of Schema.org or a research data extension may re-define `File`.
-   `Journal` is mapped to <http://schema.org/Periodical>.

**Warning** :JSON-LD examples given on the [Schema.org](http://schema.org) website might not be in *flattened* form, but *RO-Crate JSON-LD* is flattened; any nested entities in *RO-Crate JSON-LD* MUST be described as separate contextual entities in the flat `@graph` list.

To simplify processing and avoid confusion with string values, the *RO-Crate JSON-LD Context* requires URIs and entity references to be given in the form `"author": {"@id": "http://example.com/alice"}`, even where [Schema.org](http://schema.org) for some properties otherwise permit shorter forms like `"author": "http://example.com/alice"`.

See the appendix [RO-Crate JSON-LD](appendix/jsonld.md#jsonld) for details.

## Additional metadata standards

RO-Crate also uses the *Portland Common Data Model* ([PCDM](https://github.com/duraspace/pcdm/wiki) version <https://pcdm.org/2016/04/18/models>) to describe repositories or collections of digital objects and imports these terms:

-   `RepositoryObject` mapped to <http://pcdm.org/models#Object>
-   `RepositoryCollection` mapped to <http://pcdm.org/models#Collection>
-   `RepositoryFile` mapped to <http://pcdm.org/models#File>
-   `hasMember` mapped to <http://pcdm.org/models#hasMember>
-   `hasFile` mapped to <http://pcdm.org/models#hasFile>

**Note**: The terms `RepositoryObject` and `RepositoryCollection` are renamed to avoid collision between other vocabularies and the PCDM terms `Collection` and `Object`. The term `RepositoryFile` is renamed to avoid clash with RO-Crate's `File` mapping to <http://schema.org/MediaObject>.

RO-Crate uses the [Profiles Vocabulary](https://www.w3.org/TR/2019/NOTE-dx-prof-20191218/) to describe [profiles](profiles.md#profiles) using these terms and definitions:

-   `ResourceDescriptor` mapped to <http://www.w3.org/ns/dx/prof/ResourceDescriptor> ([definition](https://www.w3.org/TR/2019/NOTE-dx-prof-20191218/#Class:ResourceDescriptor))
-   `ResourceRole` mapped to <http://www.w3.org/ns/dx/prof/ResourceRole> ([definition](https://www.w3.org/TR/2019/NOTE-dx-prof-20191218/#Class:ResourceRole))
-   `Profile` mapped to <http://www.w3.org/ns/dx/prof/Profile> ([definition](https://www.w3.org/TR/2019/NOTE-dx-prof-20191218/#Class:Profile))
-   `hasArtifact` mapped to <http://www.w3.org/ns/dx/prof/hasArtifact> ([definition](https://www.w3.org/TR/2019/NOTE-dx-prof-20191218/#Property:hasArtifact))
-   `hasResource` mapped to <http://www.w3.org/ns/dx/prof/hasResource> ([definition](https://www.w3.org/TR/2019/NOTE-dx-prof-20191218/#Property:hasResource))
-   `hasRole` mapped to <http://www.w3.org/ns/dx/prof/hasRole> ([definition](https://www.w3.org/TR/2019/NOTE-dx-prof-20191218/#Property:hasRole))

From [Dublin Core Terms](http://purl.org/dc/terms/) RO-Crate uses:

-   `conformsTo` mapped to <http://purl.org/dc/terms/conformsTo>
-   `Standard` mapped to <http://purl.org/dc/terms/Standard>

From the [IANA link relations](https://www.iana.org/assignments/link-relations/) registry:

-   `cite-as` mapped to <http://www.iana.org/assignments/relation/cite-as> (defined by [RFC8574](https://www.iana.org/go/rfc8574))

These terms are being proposed by [Bioschemas profile ComputationalWorkflow 1.0-RELEASE](https://bioschemas.org/profiles/ComputationalWorkflow/1.0-RELEASE) and [FormalParameter 1.0-RELEASE](https://bioschemas.org/profiles/FormalParameter/1.0-RELEASE) to be integrated into Schema.org:

-   `ComputationalWorkflow` mapped to <https://bioschemas.org/terms/ComputationalWorkflow>
-   `FormalParameter` mapped to <https://bioschemas.org/terms/FormalParameter>
-   `input` mapped to <https://bioschemas.org/terms/input>
-   `output` mapped to <https://bioschemas.org/terms/output>

**Note**: In version 1.3 of this specification the proposed Bioschemas terms use the <https://bioschemas.org/terms/> namespace; previous versions 1.1 and 1.2 used the temporary <https://bioschemas.org/> namespace. Future releases of RO-Crate may reflect mapping to the <http://schema.org/> namespace.

To support geometry in [Places](contextual-entities.md#places), these terms from the [GeoSPARQL ontology](https://opengeospatial.github.io/ogc-geosparql/geosparql11/):

-   `Geometry` mapped to <http://www.opengis.net/ont/geosparql#Geometry>
-   `asWKT` mapped to <http://www.opengis.net/ont/geosparql#asWKT>

From [CodeMeta 3.0](https://w3id.org/codemeta/3.0):

-   `buildInstructions` mapped to <https://codemeta.github.io/terms/buildInstructions>
-   `developmentStatus` mapped to <https://codemeta.github.io/terms/developmentStatus>
-   `continuousIntegration` mapped to <https://codemeta.github.io/terms/continuousIntegration>
-   `embargoEndDate` mapped to <https://codemeta.github.io/terms/embargoEndDate>
-   `hasSourceCode` mapped to <https://codemeta.github.io/terms/hasSourceCode>
-   `isSourceCodeOf` mapped to <https://codemeta.github.io/terms/isSourceCodeOf>
-   `issueTracker` mapped to <https://codemeta.github.io/terms/issueTracker>
-   `readme` mapped to <https://codemeta.github.io/terms/readme>
-   `referencePublication` mapped to <https://codemeta.github.io/terms/referencePublication>
-   `softwareSuggestions` mapped to <https://codemeta.github.io/terms/softwareSuggestions>

**Warning** :As of 2025-01-09, the CodeMeta URIs do not resolve correctly, but are used here to match the Codemeta JSON-LD context <https://w3id.org/codemeta/3.0> (issue [#275](https://github.com/ResearchObject/ro-crate/issues/275)). The CodeMeta terms `maintainer` and `funding` are not mapped, as these are already defined by schema.org.

## Custom RO-Crate terms

The RO-Crate community maintains a [common namespace](https://github.com/ResearchObject/ro-terms/tree/master) for terms not covered by other vocabularies. This is mainly used by [RO-Crate profiles](profiles.md#profiles), but the following term is included in the core RO-Crate context:

-   `localPath` mapped to <https://w3id.org/ro/terms#localPath>

## Summary of Coverage

RO-Crate is simply a way to make metadata assertions about a set of files and folders that make up a *Dataset*. These assertions can be made at two levels:

-   Assertions at the RO-Crate level: for an RO-Crate to be useful, some metadata should be provided about the dataset as a whole (see minimum requirements for different use-cases below). In the *RO-Crate Metadata Document*, we distinguish the *Root Data Entity*, which represents the RO-Crate as a whole, from other *Data Entities* (files and folders contained in the RO-Crate) and *Contextual Entities*, e.g. a person, organisation, place related to an RO-Crate *Data Entity*.
-   Assertions about files and folders contained in the RO-Crate: in addition to providing metadata about the RO-Crate as a whole, RO-Crate allows metadata assertions to be made about any other *Data Entity*.

This document has guidelines for ways to represent common requirements for describing data in a research context, e.g.:

-   Contact information for a data set.
-   Descriptive information for a dataset and the files within it and their contexts such as an abstract, spatial and temporal coverage.
-   Associated publications.
-   Funding relationships.
-   Provenance information of various kinds; who (people and organizations) and what (instruments and computer programs) created or contributed to the data set and individual files within it.
-   Workflows that operate on the data using standard workflow descriptions, including 'single step workflows,' executable files, or environments such as Singularity containers or Jupyter notebooks.

However, as RO-Crate uses the [Linked Data principles](https://5stardata.info/en/), adopters of RO-Crate are free to supplement RO-Crate using [Schema.org](http://schema.org) metadata and/or assertions using other *Linked Data* vocabularies (see [Extending RO-Crate](appendix/jsonld.md#extending-ro-crate)).

## Future coverage

A future version of this specification will aim to cater for variable-level assertions: in some cases, e.g. for tabular data, additional metadata may be provided about the structure and variables within a given file. See the use case [Describe a tabular data file directly in RO-Crate metadata](https://github.com/ResearchObject/ro-crate/issues/27) for work-in-progress.

## Recommended Identifiers

*RO-Crate JSON-LD* SHOULD use the following IDs where possible:

-   For a *Root Data Entity*, an `identifier` which is RECOMMENDED to be a <https://doi.org/> URI.
-   For a [Person](http://schema.org/Person) participating in the research process: [ORCID](https://orcid.org) identifiers, e.g. <https://orcid.org/0000-0002-1825-0097>
-   For [Organization](http://schema.org/Organization)s including [funder](http://schema.org/funder)s, [Research Organization Registry URIs](https://ror.org/), e.g. <https://ror.org/0384j8v12>
-   For entities of type [Place](http://schema.org/Place), a [geonames](https://www.geonames.org/) URL, e.g. <http://sws.geonames.org/8152662/>
-   For file formats, a [Pronom](https://www.nationalarchives.gov.uk/PRONOM/Default.aspx) URL, for example <https://www.nationalarchives.gov.uk/PRONOM/fmt/831>.

In the absence of the above, RO-Crates SHOULD contain stable persistent URIs to identify all entities wherever possible.



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
