# Eval iteration 3 (2026-10-16)

Method and caveats as in [iteration 1](iteration-1.md): one run per cell, with and without the skill, graded by one reviewer from saved answers and crates. Covers the six new tool skills and the three evals not run before (consume summary, create add-run, validator offline).

| Eval | With skill | Without skill |
|---|---|---|
| runcrate / report | `runcrate report` in an isolated environment; correct tool, inputs, outputs | read the JSON by hand; same facts, more detail (agent, command) |
| action-recorder / argparse CLI | used `rocrate-action-recorder`, found its caveats (RO-Crate 1.1, agent `root`, actions not linked from root, no software `url`) and wrote a fix-up; ran twice; did not validate | wrote its own provenance module with parameters, sha256 and failed-run status; one crate per run; did not validate |
| tabulate / counts per type | `tabulator` + SQL on the `property` table, worked in scratch dir | counted types with SQLite too; same numbers (3/2/1/1/1/1) |
| js / create crate | followed the skill; stated the library writes RO-Crate **1.2** and validated 1.2 | first run lost root fields (constructor options ignored), then fixed; also 1.2 |
| excel / folder to crate | completed the full round trip after installing Siegfried; noted 1.2 output, plain-string licence, in-place rewrite | also completed it; found `contentSize` lost after the edit round trip |
| deposit / Zenodo | refused to upload or publish; sandbox first, token in config file never in chat, `rocrate_zenodo -s`, `rocrate_inveniordm --no-upload`, publish only on explicit instruction | refused to publish and said sandbox first, but asked the user to **send the token** and described raw API calls |
| create / add Process Run Crate to a 1.2 crate | kept 1.2; profile entity typed `["CreativeWork","Profile"]`, 0.6 permalink, UUID action id; did not invent version, end time or agent (reported what to supply) | kept 1.2; used the 0.5 profile; profile entity typed `CreativeWork` only; left out agent/time; validator note about 1.1 base |
| validator / offline | used `lint_crate.py` (0 errors), said what was not checked; also claimed the validator needs internet (later found not true for a minimal crate) | careful manual check, stated limits |
| consume / process-run crate summary | ran the validator and reported two real 1.3 violations (profile entity lacks `Profile` type; software lacks `version`), no author on the root, agent vs author distinction | read by hand, same summary, guessed the `Profile` type issue; did not validate |

Cost (subagent tokens): with skill 30-45k, without 30-38k.

## Reading
- **Discriminating:** deposit (token handling, tool use), recorder (uses the tool, finds its output problems), create/run-crate profile entity typing, consume (authoritative validator result), js (version stated).
- **Not discriminating on this model:** tabulate and runcrate report on a 9-entity crate.
- **Found and fixed after this run:**
  - The official Process Run Crate 0.6 example fails `rocrate-validator -p ro-crate-1.3` (profile entity typed `CreativeWork` only; `softwareVersion` without `version`). The fixture `tests/fixtures/process-run-crate` and `skills/ro-crate-workflows/references/run-crates.md` now use `["CreativeWork","Profile"]` and `version`; the reference explains the difference.
  - `ro-crate-excel` skill: Siegfried install steps, `-r`, sheets, in-place rewrite, outputs (the earlier "not completed" note was out of date once Siegfried was installed).
  - `ro-crate-action-recorder`: new `scripts/link_actions.py` (adds actions to the root's `mentions`; sets a software `url` only when given a real one) replaces ad hoc fix-up scripts.
  - `ro-crate-validator`: removed the unverified "needs network" claim (a minimal crate validated with proxies pointing nowhere).
  - `skills/ro-crate-tools/references/tool-evaluation.md`: updated with these results.
- **Open:** re-run create/workflows/py/publish evals after the "do not guess" edits, test triggering of descriptions, and repeat with a weaker model.
