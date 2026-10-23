Root Data Entity
================



Table of contents
-----------------





The **Root Data Entity** is a [Dataset](http://schema.org/Dataset) that represents the RO-Crate as a whole; a *Research Object* that includes the *Data Entities* and the related *Contextual Entities*.

RO-Crate Metadata Descriptor
----------------------------

The *RO-Crate Metadata Document* MUST contain a self-describing **RO-Crate Metadata Descriptor** with the `@id` value `ro-crate-metadata.json` (or `ro-crate-metadata.jsonld` in legacy crates for RO-Crate 1.0 or older) and `@type` [CreativeWork](http://schema.org/CreativeWork). This descriptor MUST have an [about](http://schema.org/about) property referencing the *Root Data Entity*'s `@id`.

``` {.json}
{ "@context": "https://w3id.org/ro/crate/1.2/context", 
  "@graph": [
    {
        "@type": "CreativeWork",
        "@id": "ro-crate-metadata.json",
        "about": {"@id": "./"},
        "conformsTo": {"@id": "https://w3id.org/ro/crate/1.2"}
    },
    
    {
      "@id": "./",
      "@type": "Dataset",
      ...
    }
  ]
}
```

**Note**: Even in [Detached RO-Crate Packages](structure.md#detached-ro-crate-package), where the *RO-Crate Metadata File* may be absent or named with a [prefix](structure.md#types-of-ro-crate), the identifier `ro-crate-metadata.json` MUST be used within the *RO-Crate JSON-LD*.

The [conformsTo](http://purl.org/dc/terms/conformsTo) of the *RO-Crate Metadata Descriptor* SHOULD have a single value which is a versioned permalink URI of the RO-Crate specification that the *RO-Crate JSON-LD* conforms to. The URI SHOULD start with `https://w3id.org/ro/crate/`.

**Note**: In RO-Crates conforming to version 1.1 and earlier, `conformsTo` MAY be an array and can include [RO-Crate profiles](profiles.md#profiles) in addition to the base specification. In version 1.2, it is now recommended that profile declarations are included on the *Root Data Entity* instead (see [Direct Properties of the Root Data Entity](#direct-properties-of-the-root-data-entity)).

### Finding the Root Data Entity

Consumers processing the RO-Crate as a JSON-LD graph can find the *Root Data Entity* by following this algorithm:

1.  For each entity in `@graph` array
2.  .. if the `@id` is `ro-crate-metadata.json`
3.  .... from this entity's `about` object, keep the `@id` URI as variable *root*
4.  .. if the `@id` is `ro-crate-metadata.jsonld`
5.  .... from this entity's `about` object, keep the `@id` URI as variable *legacyroot*
6.  For each entity in `@graph` array
7.  .. if the entity has an `@id` URI that matches a non-null *root* return it
8.  For each entity in `@graph` array
9.  .. if the entity has an `@id` URI that matches a non-null *legacyroot* return it
10. Fail with unknown root data entity.

Note that the above can be implemented efficiently by first building a map (`entity_map`) of all entities using their `@id` as keys (which is typically also helpful for further processing) and then performing a series of lookups. Ignoring the legacy case for now, this lookup code could be:

``` {.javascript}
metadata_entity = entity_map["ro-crate-metadata.json"]
root_entity = entity_map[metadata_entity["about"]["@id"]]
```

See also the appendix on [finding RO-Crate Root in RDF triple stores](appendix/relative-uris.md#finding-ro-crate-root-in-rdf-triple-stores).

### Purpose of Metadata Document

To ensure a base-line interoperability between RO-Crates, a minimum set of metadata is required for the *Root Data Entity*. As [stated earlier](structure.md#self-describing-and-self-contained) the *RO-Crate Metadata Document* is not an exhaustive manifest or inventory, that is, it does not necessarily list or describe all files in the package. For this reason, there are no minimum metadata requirements in terms of describing [Data Entities](introduction.md#data-entities) (files and folders) other than the *Root Data Entity*. Extensions of RO-Crate dealing with specific types of dataset may apply further constraints or requirements of metadata beyond the Root Data Entity (see the appendix [Extending RO-Crate](appendix/jsonld.md#extending-ro-crate)).

The *RO-Crate Metadata Descriptor* MAY contain information such as licensing for the *RO-Crate Metadata Document* if metadata is licensed separately from the crate's Data entities.

The section below outlines the properties that the *Root Data Entity* MUST have.

Direct properties of the Root Data Entity
-----------------------------------------

The *Root Data Entity* MUST have all of the properties listed below. Each property also has requirements that apply to its value:

-   `@type`: MUST be [Dataset](http://schema.org/Dataset) or an array that contains `Dataset`
-   `@id`: SHOULD be the string `./` or an absolute URI (see [below](#root-data-entity-identifier))
-   `name`: SHOULD identify the dataset to humans well enough to disambiguate it from other RO-Crates
-   `description`: SHOULD further elaborate on the name to provide a summary of the context in which the dataset is important.
-   `datePublished`: MUST be a single string value in [ISO 8601 date format](http://schema.org/DateTime), SHOULD be specified to at least the precision of a day, and MAY be a timestamp down to the millisecond.
-   `license`: SHOULD link to a *Contextual Entity* or *Data Entity* in the *RO-Crate Metadata Document* with a name and description (see section on [licensing](contextual-entities.md#licensing-access-control-and-copyright)). MAY, if necessary, be a textual description of how the RO-Crate may be used.

**Note**: These requirements are stricter than those published for [Google Dataset Search](https://developers.google.com/search/docs/data-types/dataset) which requires a `Dataset` to have a `name` and `description`.

**Warning** :The properties above are not sufficient to generate a [DataCite](https://www.datacite.org/) citation. Advice on integrating with [DataCite](https://www.datacite.org/) will be provided in a future version of this specification, or as an implementation guide.

Additional properties of *schema.org* types [Dataset](http://schema.org/Dataset) and [CreativeWork](http://schema.org/CreativeWork) MAY be added to further describe the RO-Crate as a whole, e.g. [author](http://schema.org/author), [abstract](http://schema.org/abstract), [publisher](http://schema.org/publisher). See sections [contextual entities](introduction.md#contextual-entities) and [provenance](provenance.md#provenance) for further details.

If the RO-Crate conforms to one or more [profiles](profiles.md#profiles), this should be described following the guidance in the section [Declaring conformance of an RO-Crate profile](profiles.md#declaring-conformance-of-an-ro-crate-profile).

### Root Data Entity identifier

The *Root Data Entity*'s `@id` SHOULD be either `./` (indicating the directory of `ro-crate-metadata.json` is the [RO-Crate Root](structure.md#structure)), or an absolute URI.

**Note**: RO-Crates that have been assigned a *persistent identifier* (e.g. a DOI) MAY indicate this using [identifier](http://schema.org/identifier) on the *Root Data Entity* using the approach set out in the [Science On Schema.org guides](https://github.com/ESIPFed/science-on-schema.org/blob/1.3.1/guides/Dataset.md#identifier), that is through a `PropertyValue` or MAY use a full persistent URL as the `@id` for the *Root Data Entity*.

**Note**: RO-Crate 1.1 and earlier recommended `identifier` to be plain string URIs. Clients SHOULD be permissive of an RO-Crate `identifier` being a string (which MAY be a URI), or a `@id` reference, which SHOULD be represented as a `PropertyValue` entity which MUST have a human readable `value`, and SHOULD have a `url` if the identifier is Web-resolvable. A citable representation of this persistent identifier MAY be given as a `description` of the `PropertyValue`, but as there are more than 10.000 known [citation styles](https://citationstyles.org/), no attempt should be made to parse this string.

#### Resolvable persistent identifiers and citation text

It is RECOMMENDED that resolving the `identifier` programmatically returns the *RO-Crate Metadata Document* or an archive (e.g. ZIP) that contains the *RO-Crate Metadata File*, using [content negotiation](data-entities.md#retrieving-an-ro-crate) and/or [Signposting](https://signposting.org/). With an RO-Crate identifier that is persistent and resolvable in this way from a URI, the *Root Data Entity* SHOULD indicate this using the `cite-as` property according to [RFC8574](https://www.iana.org/go/rfc8574). Likewise, an HTTP/HTTPS server of the resolved RO-Crate Metadata Document or archive (possibly after redirection) SHOULD indicate that persistent identifier in its [Signposting](https://signposting.org/) headers using `Link rel="cite-as"`.

**Tip**: The above `cite-as` MAY go to a repository landing page, and MAY require authentication, but MUST ultimately have the RO-Crate as a downloadable item, which SHOULD be programmatically accessible through content negotiation or [Signposting](https://signposting.org/) (`Link rel=\"describedby\"` for an *RO-Crate Metadata Document*, or `Link rel=\"item\"` for an archive). To rather associate a textual scholarly citation for a crate (e.g. journal article), indicate instead a [publication via `citation` property](contextual-entities.md#publications-via-citation-property).

Any entity which is a subclass of [CreativeWork](http://schema.org/CreativeWork), including [Dataset](http://schema.org/Dataset)s like the *Root Data Entity*, MAY have a `creditText` property which provides a textual citation for the entity.

Minimal example of RO-Crate
---------------------------

The following *RO-Crate Metadata Document* represents a minimal description of an *RO-Crate* that also follows the identifier recommendations above for use in an *Attached RO-Crate Package*.

``` {.json}
{ "@context": "https://w3id.org/ro/crate/1.2/context", 
  "@graph": [

 {
    "@id": "ro-crate-metadata.json",
    "@type": "CreativeWork",
    "about": {"@id": "./"},
    "conformsTo": {"@id": "https://w3id.org/ro/crate/1.2"}
 },  
 {
    "@id": "./",
    "@type": "Dataset",
    "identifier": {"@id": "https://doi.org/10.4225/59/59672c09f4a4b"},
    "cite-as": "https://doi.org/10.4225/59/59672c09f4a4b",
    "datePublished": "2017",
    "name": "Data files associated with the manuscript:Effects of facilitated family case conferencing for ...",
    "description": "Palliative care planning for nursing home residents with advanced dementia ...",
    "license": {"@id": "https://creativecommons.org/licenses/by-nc-sa/3.0/au/"},
    "creditText": "Agar, M. et al., 2017. Data supporting \"Effects of facilitated family case conferencing for advanced dementia: A cluster randomised clinical trial\". https://doi.org/10.4225/59/59672c09f4a4b"
 },
 {
    "@id": "https://creativecommons.org/licenses/by-nc-sa/3.0/au/",
    "@type": "CreativeWork",
    "description": "This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Australia License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/au/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.",
    "identifier": "https://creativecommons.org/licenses/by-nc-sa/3.0/au/",
    "name": "Attribution-NonCommercial-ShareAlike 3.0 Australia (CC BY-NC-SA 3.0 AU)"
 },
 {
    "@id": "https://doi.org/10.4225/59/59672c09f4a4b",
    "@type": "PropertyValue",
    "propertyID": "https://registry.identifiers.org/registry/doi",
    "value": "doi:10.4225/59/59672c09f4a4b",
    "url": "https://doi.org/10.4225/59/59672c09f4a4b"
  }
 ]
}
```

Alternatively the following is also valid, this time using the DOI as the `@id` of the *Root Data Entity*:

``` {.json}
 {
    "@id": "ro-crate-metadata.json",
    "@type": "CreativeWork",
    "about": {"@id": "https://doi.org/10.4225/59/59672c09f4a4b"},
    "conformsTo": {"@id": "https://w3id.org/ro/crate/1.2"}
 },  
{
    "@id": "https://doi.org/10.4225/59/59672c09f4a4b",
    "@type": "Dataset",
    "cite-as": "https://doi.org/10.4225/59/59672c09f4a4b",
    "datePublished": "2017",
    "name": "Data files associated with the manuscript:Effects of facilitated family case conferencing for ...",
    "description": "Palliative care planning for nursing home residents with advanced dementia ...",
    "license": {"@id": "https://creativecommons.org/licenses/by-nc-sa/3.0/au/"},
    "creditText": "Agar, M. et al., 2017. Data supporting \"Effects of facilitated family case conferencing for advanced dementia: A cluster randomised clinical trial\". https://doi.org/10.4225/59/59672c09f4a4b"
 }
```



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
