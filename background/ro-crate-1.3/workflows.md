# Workflows and Scripts {#workflows}









Scientific workflows and scripts that were used (or can be used) to analyze or generate files contained in an RO-Crate MAY be embedded in an RO-Crate. See also the Provenance section on [Software Used to Create Files](provenance.md#software-used-to-create-files).

*Workflows* and *scripts* SHOULD be described using [data entities](introduction.md#data-entities) of type [SoftwareSourceCode](http://schema.org/SoftwareSourceCode).

The distinction between [SoftwareSourceCode](http://schema.org/SoftwareSourceCode) and [SoftwareApplication](http://schema.org/SoftwareApplication) for [software](provenance.md#software-used-to-create-files) is fluid, and comes down to availability and understandability. For instance, office spreadsheet applications are generally available and do not need further explanation (`SoftwareApplication`); while a Python script that is customized for a particular data analysis might be important to understand deeper and should therefore be included as `SoftwareSourceCode` in the RO-Crate dataset.

## Describing scripts and workflows

A script is a *Data Entity* which MUST have the following properties:

-   `@type` is an array with at least `File` and `SoftwareSourceCode` as values
-   `@id` is a File URI linking to the executable script
-   `name`: a human-readable [name](http://schema.org/name) for the script.

A workflow is a *Data Entity* which MUST have the following properties:

-   `@type` is an array with at least `File`, `SoftwareSourceCode` and `ComputationalWorkflow` as values
-   `@id` is a File URI linking to the workflow entry-point.
-   `name`: a human-readable [name](http://schema.org/name) for the workflow.

Short example describing a *script*:

``` json
{
  "@id": "scripts/analyse_csv.py",
  "@type": ["File", "SoftwareSourceCode"],
  "name": "Analyze CSV files",
  "programmingLanguage": {"@id": "https://www.python.org/downloads/release/python-380/"}
}
```

Short example describing a *workflow*:

``` json
{
    "@id": "workflow/retropath.knime",  
    "@type": ["File", "SoftwareSourceCode", "ComputationalWorkflow"],
    "author": {"@id": "#thomas"},
    "name": "RetroPath Knime workflow",
    "description": "Retrosynthesis workflow calculating chemical reactions",
    "license": { "@id": "https://spdx.org/licenses/CC-BY-NC-SA-4.0"},
    "programmingLanguage": {"@id": "#knime"}
}
```

There is no strong distinction between a *script* and a *workflow*; many computational workflows are written in script-like languages, and many scripts perform a *pipeline* of steps.

Here are some indicators for when a script should be considered a *workflow*:

-   It performs a series of steps (*pipeline*)
-   The executed steps are mainly external tools or services
-   The main work is performed by the steps (script is not algorithmic)
-   The steps exchange data in a *dataflow*, typically file inputs/outputs
-   The script has well-defined *inputs* and *outputs*, e.g. file arguments

Here are some counter-indicators for when a script might **not** be a workflow:

-   The script contains mainly algorithms or logic
-   Data is exchanged with services outside of the system, e.g. a SQL database
-   The script relies on a particular state of the system (e.g. appends existing files)
-   An interactive user interface that controls the actions

## Workflow Runtime and Programming Language

Scripts written in a *programming language*, as well as workflows, generally need a *runtime*; in RO-Crate the runtime SHOULD be indicated using a liberal interpretation of [programmingLanguage](http://schema.org/programmingLanguage).

Note that the language and its runtime MAY differ (e.g. different C++ compilers), but for scripts and workflows, frequently the language and runtime are essentially the same, and thus the `programmingLanguage`, implied to be a [ComputerLanguage](http://schema.org/ComputerLanguage), can also be described as an executable [SoftwareApplication](http://schema.org/SoftwareApplication):

``` json
{
  "@id": "scripts/analyse_csv.py",
  "@type": ["File", "SoftwareSourceCode"],
  "name": "Analyze CSV files",
  "programmingLanguage": {"@id": "https://www.python.org/downloads/release/python-380/"}
},
{
  "@id": "https://www.python.org/downloads/release/python-380/",
  "@type": ["ComputerLanguage", "SoftwareApplication"],
  "name": "Python 3.8.0",
  "version": "3.8.0"
}
```

A *contextual entity* representing a [ComputerLanguage](http://schema.org/ComputerLanguage) and/or [SoftwareApplication](http://schema.org/SoftwareApplication) MUST have a [name](http://schema.org/name), [url](http://schema.org/url) and [version](http://schema.org/version), which should indicate a known version the workflow/script was developed or tested with. [alternateName](http://schema.org/alternateName) MAY be provided if there is a shorter colloquial name, for instance *"R"* instead of *"The R Project for Statistical Computing"*.

It is possible to indicate *steps* that are executed as part of an `ComputationalWorkflow` or `Script`, by using [hasPart](http://schema.org/hasPart) to relate additional `SoftwareApplication` or nested `SoftwareSourceCode` contextual entities:

``` json
{
    "@id": "workflow/analyze.cwl",  
    "@type": ["File", "SoftwareSourceCode", "ComputationalWorkflow"],
    "name": "CWL workflow to analyze CSV and make PNG",
    "programmingLanguage": {"@id": "https://w3id.org/cwl/v1.1/"},
    "hasPart": [
      {"@id": "scripts/analyse_csv.py"},
      {"@id": "https://www.imagemagick.org/"}
    ]
}
```

## Workflow diagram/sketch

It can be beneficial to show a diagram or sketch to explain the script/workflow. This may have been generated from a workflow management system, or drawn manually as a diagram. This diagram MAY be included from the `SoftwareSourceCode` data entity by using `image`, pointing to an [ImageObject](http://schema.org/ImageObject) data entity which is [about](http://schema.org/about) the `SoftwareSourceCode`:

``` json
{
  "@id": "workflow/workflow.knime",  
  "@type": ["File", "SoftwareSourceCode", "ComputationalWorkflow"],
  "name": "RetroPath2.0 workflow",
  "image": {"@id": "workflow/workflow.svg" } 
},
{
  "@id": "workflow/workflow.svg",
  "@type": ["File", "ImageObject"],
  "encodingFormat":  "image/svg+xml",
  "name": "Diagram of RetroPath2.0 workflow",
  "about": {"@id": "workflow/workflow.knime"}
}
```

The image file format SHOULD be indicated with [encodingFormat](http://schema.org/encodingFormat) using an IANA registered [media type](https://www.iana.org/assignments/media-types) like `image/svg+xml` or `image/png`. Additionally a reference to a [Pronom](https://www.nationalarchives.gov.uk/PRONOM/Default.aspx) identifier SHOULD be provided, which MAY be described as an additional contextual entity to give human-readable name to the format:

``` json
{
  "@id": "workflow/workflow.svg",
  "@type": ["File", "ImageObject"],
  "encodingFormat":  ["image/svg+xml", {"@id": "https://www.nationalarchives.gov.uk/PRONOM/fmt/92"}],
  "name": "Diagram of RetroPath2.0 workflow",
  "about": {"@id": "workflow/workflow.knime"}
},
,
{
  "@id": "https://www.nationalarchives.gov.uk/PRONOM/fmt/92",
  "name": "Scalable Vector Graphics",
  "@type": ["WebPage", "Standard"]
}
```

A workflow diagram may still be provided even if there is no programmatic `SoftwareSourceCode` that can be executed (e.g. because the workflow was done by hand). In this case the sketch itself is a proxy for the workflow and SHOULD have an `about` property referring to the *Root Data Entity* as a whole (assuming the RO-Crate represents the outcome of a single workflow), or to other [Data Entities](introduction.md#data-entities) otherwise:

``` json
{
  "@id": "workflow/workflow.svg",
  "@type": ["File", "ImageObject"],
  "encodingFormat":  ["image/svg+xml"],
  "name": "Diagram of an ad hoc workflow",
  "about": {"@id": "./"}
}
```

## Complying with Bioschemas Computational Workflow profile

Data entities representing *workflows* (`@type: ComputationalWorkflow`) SHOULD comply with the Bioschemas [ComputationalWorkflow profile](https://bioschemas.org/profiles/ComputationalWorkflow/1.0-RELEASE), where possible.

When complying with this profile, the workflow data entities MUST describe these properties and their related contextual entities: [name](http://schema.org/name), [programmingLanguage](http://schema.org/programmingLanguage), [creator](http://schema.org/creator), [dateCreated](http://schema.org/dateCreated), [license](http://schema.org/license), [sdPublisher](http://schema.org/sdPublisher), [url](http://schema.org/url), [version](http://schema.org/version).

The [ComputationalWorkflow profile](https://bioschemas.org/profiles/ComputationalWorkflow/1.0-RELEASE) explains the above and lists additional properties that a compliant [ComputationalWorkflow](https://bioschemas.org/types/ComputationalWorkflow/1.0-RELEASE) data entity SHOULD include: [citation](http://schema.org/citation), [contributor](http://schema.org/contributor), [creativeWorkStatus](http://schema.org/creativeWorkStatus), [description](http://schema.org/description), [funding](https://github.com/schemaorg/schemaorg/pull/2618), [hasPart](http://schema.org/hasPart), [isBasedOn](http://schema.org/isBasedOn), [keywords](http://schema.org/keywords), [maintainer](http://schema.org/maintainer), [producer](http://schema.org/producer), [publisher](http://schema.org/publisher), [runtimePlatform](http://schema.org/runtimePlatform), [softwareRequirements](http://schema.org/softwareRequirements), [targetProduct](http://schema.org/targetProduct)

A data entity conforming to the [ComputationalWorkflow profile](https://bioschemas.org/profiles/ComputationalWorkflow/1.0-RELEASE) SHOULD declare the versioned profile URI using the [conformsTo](http://purl.org/dc/terms/conformsTo) property [^1]:

``` json
{ "@id": "workflow/alignment.knime",  
  "@type": ["File", "SoftwareSourceCode", "ComputationalWorkflow"],
  "conformsTo": 
    {"@id": "https://bioschemas.org/profiles/ComputationalWorkflow/1.0-RELEASE"},
  "..": ""
}
```

### Describing inputs and outputs

The input and output *parameters* for a workflow or script can be given with `input` and `output` to [FormalParameter](https://bioschemas.org/types/FormalParameter/1.0-RELEASE) contextual entities. Note that this entity type usually represents a *potential* input/output value in a reusable workflow, much like [function parameter definitions](https://en.wikipedia.org/wiki/Parameter_(computer_programming)) in general programming.

If complying with the Bioschemas [FormalParameter profile](https://bioschemas.org/profiles/FormalParameter/1.0-RELEASE), the *contextual entities* for [FormalParameter](https://bioschemas.org/types/FormalParameter/1.0-RELEASE), referenced by `input` or `output`, MUST describe [name](http://schema.org/name).

The Bioschemas [FormalParameter profile](https://bioschemas.org/profiles/FormalParameter/1.0-RELEASE) explains the above and lists additional properties that can be used, including [description](http://schema.org/description), [valueRequired](http://schema.org/valueRequired), [defaultValue](http://schema.org/defaultValue) and [identifier](http://schema.org/identifier).

A contextual entity conforming to the [FormalParameter profile](https://bioschemas.org/profiles/FormalParameter/1.0-RELEASE) SHOULD declare the versioned profile URI using `conformsTo` e.g.:

``` json
{
  "@id": "#36aadbd4-4a2d-4e33-83b4-0cbf6a6a8c5b",
  "@type": "FormalParameter",
  "conformsTo": 
    {"@id": "https://bioschemas.org/profiles/FormalParameter/1.0-RELEASE"},
  "..": ""
}
```

**Note**: `input`, `output` and `FormalParameter` are at time of writing proposed by Bioschemas and not yet integrated in Schema.org.

## Complete Workflow Example

The below is an example of an RO-Crate complying with the Bioschemas [ComputationalWorkflow profile 1.0](https://bioschemas.org/profiles/ComputationalWorkflow/1.0-RELEASE):

``` json
{ "@context": "https://w3id.org/ro/crate/1.3/context", 
  "@graph": [
    {
      "@type": "CreativeWork",
      "@id": "ro-crate-metadata.json",
      "conformsTo": {"@id": "https://w3id.org/ro/crate/1.3"},
      "about": {"@id": "./"}
    },
    {
      "@id": "./",
      "@type": "Dataset",
      "hasPart": [
          { "@id": "workflow/alignment.knime" }
      ]
    },
    {
      "@id": "workflow/alignment.knime",  
      "@type": ["File", "SoftwareSourceCode", "ComputationalWorkflow"],
      "conformsTo": {
        "@id": "https://bioschemas.org/profiles/ComputationalWorkflow/1.0-RELEASE"
      },
      "name": "Sequence alignment workflow",
      "programmingLanguage": {"@id": "#knime"},
      "creator": {"@id": "#alice"},
      "dateCreated": "2020-05-23",
      "license": { "@id": "https://spdx.org/licenses/CC-BY-NC-SA-4.0"},
      "input": [
        { "@id": "#36aadbd4-4a2d-4e33-83b4-0cbf6a6a8c5b"}
      ],
      "output": [
        { "@id": "#6c703fee-6af7-4fdb-a57d-9e8bc4486044"},
        { "@id": "#2f32b861-e43c-401f-8c42-04fd84273bdf"}
      ],
      "sdPublisher": {"@id": "#workflow-repo"},
      "url": "http://example.com/workflows/alignment",
      "version": "0.5.0"
    },
    {
      "@id": "#36aadbd4-4a2d-4e33-83b4-0cbf6a6a8c5b",
      "@type": "FormalParameter",
      "conformsTo": {
        "@id": "https://bioschemas.org/profiles/FormalParameter/1.0-RELEASE"
      },
      "name": "genome_sequence",
      "valueRequired": true,
      "additionalType": {"@id": "http://edamontology.org/data_2977"},
      "format": {"@id": "http://edamontology.org/format_1929"}
    },
    {
      "@id": "#6c703fee-6af7-4fdb-a57d-9e8bc4486044",
      "@type": "FormalParameter",
      "conformsTo": {
        "@id": "https://bioschemas.org/profiles/FormalParameter/1.0-RELEASE"
      },
      "name": "cleaned_sequence",
      "additionalType": {"@id": "http://edamontology.org/data_2977"},
      "encodingFormat": {"@id": "http://edamontology.org/format_2572"}
    },
    {
      "@id": "#2f32b861-e43c-401f-8c42-04fd84273bdf",
      "@type": "FormalParameter",
      "conformsTo": {
        "@id": "https://bioschemas.org/profiles/FormalParameter/1.0-RELEASE"
      },
      "name": "sequence_alignment",
      "additionalType": {"@id": "http://edamontology.org/data_1383"},
      "encodingFormat": {"@id": "http://edamontology.org/format_1982"}
    },
    {
      "@id": "https://spdx.org/licenses/CC-BY-NC-SA-4.0",
      "@type": "CreativeWork",
      "name": "Creative Commons Attribution Non Commercial Share Alike 4.0 International",
      "alternateName": "CC-BY-NC-SA-4.0"
    },
    {
      "@id": "#knime",
      "@type": "ComputerLanguage",
      "name": "KNIME Analytics Platform",
      "alternateName": "KNIME",
      "url": "https://www.knime.com/whats-new-in-knime-41",
      "version": "4.1.3"
    },
    {
      "@id": "#alice",
      "@type": "Person",
      "name": "Alice Brown"
    },
    {
      "@id": "#workflow-repo",
      "@type": "Organization",
      "name": "Example Workflow repository",
      "url":"http://example.com/workflows/"
    },
    {
      "@id": "http://edamontology.org/format_1929",
      "@type": "DefinedTerm",
      "name": "FASTA sequence format"
    },
    {
      "@id": "http://edamontology.org/format_1982",
      "@type": "DefinedTerm",
      "name": "ClustalW alignment format"
    },
    {
      "@id": "http://edamontology.org/format_2572",
      "@type": "DefinedTerm",
      "name": "BAM format"
    },
    {
      "@id": "http://edamontology.org/data_2977",
      "@type": "DefinedTerm",
      "name": "Nucleic acid sequence"
    },
    {
      "@id": "http://edamontology.org/data_1383",
      "@type": "DefinedTerm",
      "name": "Nucleic acid sequence alignment"
    }
  ]
}
```



```{=html}
<!--
   Copyright 2019-2020 University of Technology Sydney
   Copyright 2019-2020 The University of Manchester UK 
   Copyright 2019-2020 RO-Crate contributors <https://github.com/ResearchObject/ro-crate/graphs/contributors>

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
