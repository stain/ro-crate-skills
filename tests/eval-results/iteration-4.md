# Eval iteration 4: repeats of the "do not guess" evals (2026-10-16)

14 evals x 3 repeats, **with the skill only** (baselines for these evals are in iterations 1-3), 42 runs, scored by `tests/graders` (`python tests/graders/summarize.py iteration-4-r1 iteration-4-r2 iteration-4-r3`). Prompts were identical across repeats (task files, not retyped). Repeats 1 and 2 ran against the skills as they were before the fixes below; repeat 3 ran after them. Two py-zip runs were repeated because the shared virtualenv had a downgraded `rocrate` (0.15.0, from installing `rocrate-action-recorder` into it); their first results were discarded.

## Result: 234/241 expectations
| Eval | r1 | r2 | r3 |
|---|---|---|---|
| create-basic | 11/11 | 11/11 | 11/11 |
| create-add-run | 9/10 | 9/10 | 10/10 |
| py-zip | 8/8 | 8/8 | 7/8 |
| workflows-snakemake | 7/8 | 7/8 | 7/9 |
| publish-bagit | 4/4 | 4/4 | 4/4 |
| profiles-declare, profiles-create | 6/6, 7/7 | 6/6, 7/7 | 6/6, 7/7 |
| js-create, excel-folder, recorder-argparse, runcrate-report, deposit-zenodo | all pass | all pass | all pass |
| validator-invalid, validator-offline | 3/3 | 3/3 | 3/3 |

## What the failures were
1. **Required properties left out (r1, r2: create-add-run, workflows).** The agents omitted the `version` of a software/language entity that the validator requires, following the then-current rule (omit what you cannot know). The rule was refined (use a `TODO:` value for anything the spec, a profile or the validator requires). **r3 did this correctly in both evals** (`TODO: ImageMagick version...`, `TODO: Snakemake version used`) and passed the validator.
2. **Bare `rocrate init` metadata left in the source folder (r3 py-zip).** The zip held a complete crate, but the folder kept an incomplete one. `ro-crate-py` skill now says to complete the folder's own metadata and zip that; the grader checks the leftover.
3. **Harness failure (r3 workflows): `answer.md` was not written** although the agent said it was. The graders now flag a missing `answer.md` explicitly.

## Stability of the behaviour that matters
Across the 42 runs: no invented ORCID, no guessed licence (a licence appears only where the prompt gave it, otherwise `TODO:`), no software version without evidence, no upload or publish, no token requested, profiles always on the root with released 0.6 permalinks and a `Profile` type, declared version kept when editing a 1.2 crate. The guessed licence and Snakemake version seen in iteration 2 (before the rule) did not recur.

## What the runs found in the skills (all fixed)
- `ro-crate-publish`: the BagIt tag is `BagIt-Version` (the RO-Crate spec's own example misspells it as `BagIt-version`; `bagit-python` rejects that); skill now recommends `bagit-python` (`python -m bagit --sha512 <copy>`, `--validate`), explains `Payload-Oxum`, and notes the tool writes version 0.97.
- `ro-crate-validator`: the lint script could not read zips; it now can.
- `ro-crate-excel`: folder ids come out without a trailing `/`; `contentSize` was kept in some round trips and dropped in others; Siegfried's signature file location varies.
- `ro-crate-js`: `roccheck` looks for the old `ro-crate-metadata.jsonld` filename.
- Shared "Do not guess" rule refined (above); `tests/do_not_guess.txt` is checked verbatim in ten skills.

## Limits
Three repeats of one model on small fixtures; repeats 1-2 predate the fixes; one reviewer wrote both skills and graders (the graders were calibrated against hand grading in `graders-calibration.md`); no weaker-model or other-agent runs; triggering from descriptions untested.
