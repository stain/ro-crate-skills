---
name: ro-crate-workflows
description: Describe workflows, scripts and their executions in RO-Crate: ComputationalWorkflow entities, Workflow RO-Crate (WorkflowHub), Workflow Testing RO-Crate, and Process/Workflow/Provenance Run Crates with CreateAction provenance. Use when packaging a workflow or script, recording how tools or a workflow produced files (provenance), or reading a workflow or run crate from WorkflowHub, Nextflow, Galaxy or CWL.
---

# Workflows, scripts and run provenance in RO-Crate

Spec: https://www.researchobject.org/ro-crate/specification/1.3/workflows (and `/provenance`). Run provenance profiles: https://www.researchobject.org/workflow-run-crate/ . Never use `-DRAFT` profile URIs.

## Describing a script or workflow (data entities)
- Script: `@type` `["File", "SoftwareSourceCode"]`, `name`, `programmingLanguage`.
- Workflow: `["File", "SoftwareSourceCode", "ComputationalWorkflow"]`, `@id` the entry-point file, `name`; add `author`/`creator`, `license`, `description`, `version`, `dateCreated`, `url`, `sdPublisher` as known.
- `programmingLanguage` → a `ComputerLanguage` (usually also `SoftwareApplication`) entity with `name`, `url`, `version`. Steps: `hasPart` to `SoftwareApplication`/nested `SoftwareSourceCode`.
- Diagram: `image` → `["File", "ImageObject"]` with `encodingFormat` and `about` the workflow (or the root for a hand-run workflow).
- Inputs/outputs: `input`/`output` → `FormalParameter` entities (`name`, `valueRequired`, `additionalType`, `encodingFormat`). Bioschemas profiles: `conformsTo` the **1.0-RELEASE** ComputationalWorkflow/FormalParameter profile URIs; the 1.3 context maps these terms to `https://bioschemas.org/terms/`.
- Script vs workflow: pipeline of tool steps with dataflow and defined inputs/outputs is a workflow; mostly logic/algorithms or interactive scripts are not.

## Workflow RO-Crate (WorkflowHub)
Profile https://w3id.org/workflowhub/workflow-ro-crate/ : at least one `ComputationalWorkflow` data entity which is also the root's `mainEntity`; `programmingLanguage` required; recommended `README.md`, `test/`, diagram; serialised as ZIP named `*.crate.zip`. Workflow Testing RO-Crate (https://lifemonitor.eu/workflow_testing_ro_crate) adds `TestSuite`/`TestInstance`/`TestDefinition` linked from the root with `mentions`.

## Run provenance: Workflow Run Crate profiles (version 0.6, on RO-Crate 1.3)
Pick by how much you can say; all add the context `https://w3id.org/ro/terms/workflow-run/context` and declare conformance on the root with versioned permalinks:
- **Process Run Crate** https://w3id.org/ro/wfrun/process/0.6 : tool executions without a workflow.
- **Workflow Run Crate** https://w3id.org/ro/wfrun/workflow/0.6 : a workflow drove the tools (also conform to Process Run Crate and Workflow RO-Crate).
- **Provenance Run Crate** https://w3id.org/ro/wfrun/provenance/0.6 : adds per-step detail (`HowToStep`, `ControlAction`, `OrganizeAction`).
Details and requirement tables: [references/run-crates.md](references/run-crates.md). Examples in the spec's older text show profile version 0.4: use the current profile page's version.

Related skill repo with fuller tested recipes for data files: https://github.com/stain/data-preparation-skills (`ro-crate-provenance`, Process Run Crate).

## Tools
Report on, replay or convert run crates: `runcrate` (`ro-crate-runcrate` skill). Record runs of your own Python CLIs: `ro-crate-action-recorder`. `nf-core` RO-Crate tool and `nf-prov` (Nextflow), `galaxy2cwl`, PyCOMPSs CLI, `rocrate-action-recorder` (see `ro-crate-tools`); `ro-crate-py` can add workflows (`rocrate add workflow`). Review generated crates for missing root `name`/`description`/`license`.
