# Scripted graders for the skill evals

Programs that check what an eval run produced, so results can be scored and compared without reading every answer.

- **Standard library only** (`json`, `re`, `zipfile`, `hashlib`). No RO-Crate libraries, no JSON-LD library, and no code from the skills' own lint script: a crate is read as plain JSON (`@graph`, `@id`, `about`), so the graders are an independent second opinion.
- **Separate from the skills**: nothing here ships in `skills/`.

## Layout of a run
```
<iteration>/eval-<name>/{with_skill,without_skill}/outputs/
    answer.md        the agent's final answer, verbatim
    commands.md      the commands it ran
    crate/ ...       any crate or zip it produced (location per eval: see crate_hint in evals.py)
```
`<name>` is a key of `GRADERS` in `evals.py` (for example `create-basic`, `deposit-zenodo`). Input crates the agent was given are copied from `tests/fixtures/` into `outputs/crate`.

## Run
```bash
python tests/graders/run.py <iteration dir> [--verbose] [--json] [--no-write]
python tests/graders/run.py <iteration dir>/eval-create-basic
python tests/graders/summarize.py <iter-r1> <iter-r2> <iter-r3>   # repeats side by side + failed expectations
python -m unittest tests.test_graders      # tests of the graders themselves
```
It prints passed/total per eval for each variant and, unless `--no-write`, writes `grading.json` (fields `text`, `passed`, `evidence`, `kind`) next to each `outputs/`, the format the skill-creator viewer reads.

`crate_hint` in `evals.py` is a subdirectory of `outputs/`, or `zip:<name>.zip` to grade the crate inside a zip. A missing `answer.md` is reported as a failed expectation.

## What is checked
- **Crate checks** (`checks.py`): crate found (also inside a zip), root properties, declared version, single descriptor `conformsTo`, profiles on the root typed `Profile`, no `-DRAFT`, no ORCID other than the fictional example, license given by the user or an explicit `TODO:`, author local/absent, no software version without evidence in `commands.md`, `TODO:` values reported in the answer, workflow `mainEntity`, action completeness, actions mentioned by the root, input crate not modified.
- **Bag checks**: BagIt zip with a complete manifest that lists the metadata file and matches checksums; `bag-info.txt` has no details the user did not give.
- **Text and command checks**: regular expressions on `answer.md` / `commands.md` (named things mentioned, unwanted things absent, no request to send a token, tool used).
Expectations with `kind: "tool"` check that the skill's recommended tool was used; the baseline without the skill may fail them by design.

## Limits
- Text checks are regular expressions: they catch missing facts, not wrong reasoning. Expectations about the quality of an explanation still need a person.
- `input_crate_unchanged` compares file sets and non-metadata files with the fixture (fixtures evolve; the metadata file is not compared).
- Graders encode what each eval's prompt asked; update `evals.py` together with `skills/*/evals/evals.json`.

## Calibration
Run against iterations 1-3 they agree with the hand grading in `tests/eval-results/` (see `tests/eval-results/graders-calibration.md`).
