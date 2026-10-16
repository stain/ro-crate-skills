# Eval iteration 2 (2026-10-16)

Seven further evals (profiles x2, workflows, publish, spec, py, tools), each run once with the skill and once without, same method and caveats as [iteration 1](iteration-1.md): single runs, one reviewer grading from the saved answers and crates, skill read by the agent as files (triggering not tested).

| Eval | With skill | Without skill |
|---|---|---|
| profiles / declare (Workflow Run + Process Run on `minimal-crate`) | root `conformsTo` with released **0.6** permalinks and `Profile` entities; descriptor untouched; said conformance is only a claim without workflow data | same structure but 0.5 (the validator's older version); also refused to fabricate provenance |
| profiles / create a Profile Crate | 1.3 crate, root absolute `@id`, `["Dataset","Profile"]`, `isProfileOf`, `hasPart`, `ResourceDescriptor`; left the known over-strict validator failure alone; no invented ORCID | 1.1 crate; improvised `Profile`/requirement entities with its own modelling (no `ResourceDescriptor`), CC0 licence chosen without asking |
| workflows / Snakemake | 1.3 crate, `mainEntity`, three types, `programmingLanguage` entity, declared Workflow RO-Crate 1.0; but **assumed Snakemake version 8.25.0** and Apache-2.0 licence | 1.1 crate, `mainEntity`, `ComputationalWorkflow`; guessed MIT licence, validated only against the 1.1 base profile |
| publish / BagIt zip | `bag/` with `data/` crate, `manifest-sha512.txt` including the metadata file, `External-Identifier`, checksum verification; asked the user to confirm author/licence | `bag/` with sha256 manifest and tag manifest; added `Source-Organization: BioFAIR` **guessed from the user's email domain** |
| spec / is `license` required? | correct: the root MUST have the property, SHOULD link to an entity, MAY be text; separated MUST on presence from SHOULD on value; ORCID must be an entity reference | wrong: said `license` is only a SHOULD and that `name`/`description` are MUST; reference form for `author` correct |
| py / folder to crate zip | used the library after noting `rocrate init` leaves `name`, `description`, `license` unset; validated 1.3; placeholder name/description/licence flagged | also valid 1.3; flagged assumed licence and generic name |
| tools / HTML page and GUI | `rochtml`, `rocrate init --gen-preview`, Describo/NovaCrate/Crate-O/Playground with status labels from the tools list; "review tool output" | similar list but unverified (CalcyteJS, Describo as a preview renderer), said it had not checked versions |

Cost (subagent tokens): with skill 33-42k, without 30-37k (about 5-20% more).

## Reading
- **Discriminating:** spec (correct MUST/SHOULD reading), profiles (current permalinks, Profile Crate structure), publish (no guessed organisation, sha512 manifest incl. metadata), default RO-Crate version (1.3 vs 1.1 in create/workflows/profiles).
- **Weak:** py and tools, where the baseline was about as good.
- **Failures found in the skill runs and fixed after this iteration:** the workflows run guessed a Snakemake version and a licence; `py`/`workflows` runs chose licences. Changes: `ro-crate-workflows` ("Do not guess", plus the validator version-mismatch note), `ro-crate-create` ("Do not infer who the user is", ask for the licence), `ro-crate-publish` (no inferred organisation), `ro-crate-py` (ask for licence/author), `ro-crate-validator` (workflow profiles are built on 1.1). Re-run these evals to confirm.
- Both configurations declined to fabricate run provenance when asked to declare run-crate conformance on a crate with no runs.
