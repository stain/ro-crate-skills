# Graders vs hand grading (iterations 1-3)

`python tests/graders/run.py <iteration>` on the 21 evals, with and without the skill:

| Iteration | with skill | without skill |
|---|---|---|
| 1 | 26/26 | 25/26 |
| 2 | 35/37 | 26/37 |
| 3 | 41/41 | 34/41 |

Every failure matches a finding made by hand: baselines writing 1.1 crates or 0.5 profile permalinks, a `CreativeWork`-only profile entity, a guessed licence (also by two with-skill runs from before the "do not guess" rule), `Source-Organization` in a bag, a request to send a token, claiming the licence is only a SHOULD, tools not used (runcrate, tabulator, recorder, lint script, rocrate_zenodo).

Bugs found in the graders by this comparison, now fixed: a crate that exists only inside a zip was not found; the token check flagged "never paste the token"; the unchanged-input check broke when fixtures changed after the runs; per-run crates under `runs/` were skipped.
