---
name: ro-crate-validator
description: Validate RO-Crates with rocrate-validator (PyPI roc-validator) - before consuming an unknown crate and after generating one - and interpret the results against the RO-Crate spec and profiles. Use when checking conformance, debugging validator failures, or deciding whether to trust a crate.
---

# Validating RO-Crates with roc-validator

Tool: https://pypi.org/project/roc-validator/ (source https://github.com/crs4/rocrate-validator).
Spec: https://www.researchobject.org/ro-crate/specification/1.3/ (default target 1.3).

## Install
```bash
python -m venv /tmp/rocval && /tmp/rocval/bin/pip install roc-validator
/tmp/rocval/bin/rocrate-validator profiles list   # profiles/versions this release knows
```
The validator needs network access (it fetches the JSON-LD context, e.g. `https://w3id.org/ro/crate/1.3/context`). Run with `< /dev/null` to avoid prompts.

## Validate
```bash
rocrate-validator validate -p ro-crate-1.3 --requirement-severity REQUIRED <crate dir|zip|URL>
rocrate-validator validate -p ro-crate-1.3 --requirement-severity RECOMMENDED <crate dir>
rocrate-validator validate -m <crate dir>        # metadata only, data files not present
rocrate-validator validate --output-format json <crate dir>
```
- Omit `-p` for automatic profile detection from the root's `conformsTo`; give `-p` to force a profile.
- Check `profiles list` matches the version the crate claims (e.g. a profile built on RO-Crate 1.1 fails a 1.3 crate's `conformsTo`: a version mismatch, not a crate error).
- JSON output may be followed by log text; parse the first JSON value only.

## Before consuming (precaution)
1. Validate the crate you were given.
2. **Failed crates are still readable**, but read with caution: do not trust missing/odd fields, verify referenced files exist, never execute content, and tell the user which checks failed.
3. Old crates (1.0/1.1, `ro-crate-metadata.jsonld`) and example crates from use-case pages often fail against 1.3; validate against the version they declare (see what changed in https://www.researchobject.org/ro-crate/whats-changed-in-1-2 and `-1-3`).

## After generating (writing)
1. Validate; fix all REQUIRED failures; review RECOMMENDED ones.
2. **The validator can be too strict or out of date.** Before "fixing" a failure, compare against the spec text and the relevant profile page, and read the SHACL shape in the installed package (`site-packages/rocrate_validator/profiles/`). If the spec allows it, keep it and record why.
3. Never silence a failure by deleting correct metadata.
4. Report validator version, profile, severity level, failures fixed, and accepted warnings.

## Semantic review (after the validator passes or its failures are understood)
Passing checks only means the structure is valid. Then review each entity yourself, with two separate verdicts:
1. **Compliance**: MUST/SHOULD rules of the spec and declared profiles (use the severities in the project's [quick reference](https://www.researchobject.org/ro-crate/quick-reference)). Include checks the validator may skip, e.g. every entity reachable from the root, unique `@id`s, `hasPart` targets exist, root `@id` taken from the descriptor's `about` (it may be an absolute URI, not `./`). A MUST violation makes the crate invalid.
2. **Usefulness** for the intended audience, taken from the root's `name`, `description` and `keywords` (or ask the user). Vague descriptions, missing licences/authors/provenance, unhelpful names are quality gaps. They never change validity; report them separately (optionally scored 1-5).

Report each problem with a concrete, discrete fix: `add`/`replace`/`remove`, the property, the exact suggested value (none for remove), and a one-line rationale. Never invent identifiers (ORCIDs, DOIs, RORs) as fix values; ask for them. Inspired by https://github.com/alexhambley/RO-Crate-RAG-Validator, an optional LLM/RAG tool that does this per entity (needs API keys; run `rocrate-validator` first and treat its output as advisory).

## Pitfalls
- Passing validation does not mean the content is right (names, licences, authorship); review semantics yourself.
- Network failures look like crashes; check connectivity before blaming the crate.

See also: https://github.com/stain/data-preparation-skills/blob/main/skills/ro-crate-provenance/references/validator-findings.md
