# Provenance patterns (RO-Crate 1.2/1.3)

Spec: https://www.researchobject.org/ro-crate/specification/1.3/provenance and `/workflows`. For full run provenance use the Workflow Run Crate profiles (see ro-crate-workflows).

- **Software used:** `SoftwareApplication` (`name`, `url`, `version` such as `tool --version` output) and a `CreateAction`: `instrument` the software, `object` inputs, `result` outputs, `agent` a Person, `endTime` ISO 8601 (SHOULD), `startTime` (MAY), `name`, `description` (the command line; double-escape backslashes). Several tools in sequence: instrument a `SoftwareSourceCode` script/workflow instead.
- **Equipment:** `IndividualProduct` (serial number, manufacturer, a web page as `@id`); a `CreateAction` with `instrument` it.
- **Changes to the crate or its files:** a curation `CreateAction`/`UpdateAction` with at least one `object` (the root or a part), `name`, `endTime`, a human `agent`, optional `instrument`, `actionStatus` (`CompletedActionStatus`, `FailedActionStatus`, ...), `error`. `UpdateAction` only for whole-dataset state changes; for a changed file keep the old version and add a `CreateAction` with `object` old, `result` new.
- **Repository exports (PCDM):** `RepositoryObject`/`RepositoryCollection` with `hasMember`, `hasFile`.
- List actions from the root with `mentions` so they are reachable.
- Agents that are AI systems: record them honestly (a `SoftwareApplication` as `instrument`, the responsible person as `agent`). Do not invent versions or identifiers.
