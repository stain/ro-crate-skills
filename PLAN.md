# Plan: developing and testing the skills

Read [AGENTS.md](AGENTS.md), [TESTING.md](TESTING.md) and [background/README.md](background/README.md) first.
Default target: RO-Crate 1.3 (released versions only, never `-DRAFT`). Run `python tests/check_repo.py` and
`python -m unittest tests.test_lint` before every commit.

## Status
Seventeen skills ship in `skills/` (eleven core skills plus six small tool skills: `ro-crate-runcrate`, `ro-crate-action-recorder`, `ro-crate-tabulate`, `ro-crate-js`, `ro-crate-excel`, `ro-crate-deposit`; tools tested in isolated environments as noted in each skill): `ro-crate-consume`, `ro-crate-create`, `ro-crate-validator` (with `scripts/lint_crate.py`),
`ro-crate-spec`, `ro-crate-compatibility`, `ro-crate-profiles`, `ro-crate-workflows`, `ro-crate-retrieve`, `ro-crate-publish`,
`ro-crate-py`, `ro-crate-tools`. Each has `evals/evals.json`. The earlier 20 placeholders were condensed into these (detail
moved to `references/`). Commands for ro-crate-py, signposting and rochtml were run once (ro-crate-py 0.16.0,
signposting 0.9.9, ro-crate-html 0.1.6); re-check on new releases.

## v0.1 scope (this branch)
Seventeen skills, one shared "Do not guess" rule enforced by `tests/check_repo.py`, scripts with unit tests (`lint_crate.py`, `link_actions.py`), 21 evals run once each (`tests/eval-results/`), tool evaluation in `skills/ro-crate-tools/references/tool-evaluation.md`. Not in v0.1: trigger-accuracy testing, weaker-model and other-agent runs, scripted expectation checks, repeat runs for variance.

## Scripted graders
Done: `tests/graders/` and iteration 4 (3 repeats x 14 evals, `tests/eval-results/iteration-4.md`); (see its README); use them for every re-run, repeat runs for variance and weaker-model runs. Grader expectations live in `tests/graders/evals.py` and must be kept in step with `skills/*/evals/evals.json`.

## Next steps
1. **Run the evals.** Iteration 1 (5 of 15 evals, with/without skill) is in `tests/eval-results/iteration-1.md`; run the rest and repeat with a weaker model. Execute `skills/*/evals/evals.json` prompts with and without each skill (Claude Code: skill-creator
   plugin viewer/benchmark; other agents: by hand or CI), add programmatic assertions where outputs are files, fix skills that fail.
2. **Validator** was run on all fixtures (results in `TESTING.md` and the validator skill); still open: offline behaviour, `--no-auto-profile`, `--skip-availability-checks`, reporting the over-strict Profile Crate check upstream; add known false positives (see data-preparation-skills `references/validator-findings.md`); check `--no-auto-profile`,
   `--skip-availability-checks`, offline use. Compare findings with the lint script and with
   https://github.com/alexhambley/RO-Crate-RAG-Validator (optional LLM/RAG tool, evaluated 2026-10-16: per-entity only, needs keys).
3. **Description triggering.** Test each description with should/should-not trigger prompts (Claude Code: skill-creator `run_loop`;
   other agents manually); neighbours to separate: consume/create/validator/tools/py, compatibility/spec, retrieve/publish.
4. **Verify URLs and tool claims** in `references/` (spec page URLs were checked once on 2026-10-16; tool statuses come from the tools list).
5. **Sibling repos:** link (not vendor) https://github.com/stain/data-preparation-skills (`ro-crate-provenance`, MIT) and
   https://github.com/sanskritsuthar/workflowhub-skills (BSD-3-Clause; installable as a plugin from GitHub: `claude plugin marketplace add sanskritsuthar/workflowhub-skills`).
   Our `ro-crate-retrieve`/`ro-crate-consume` overlap with its `fair-signposting`/`ro-crate-consume`; prefer pointing to it where it is deeper.
6. **Versioning and CI:** bump `version` in all five manifests together on meaningful changes (currently 0.1.0); add a GitHub Action running
   `tests/check_repo.py` and `tests.test_lint`. Test install in each agent (Claude Code plugin, Copilot, Codex, plain copy into `.agents/skills`).

## Gaps and ideas
- **Profile discovery:** help choose a profile for a use case (Workflow Run, ARC/ISA, ELN, 5 Safes, language-data, ...) from the profile registry.
- **Format conversion:** CITATION.cff, codemeta.json, DataCite, Zenodo metadata to RO-Crate and back (the spec lists DataCite as future work).
- **Recording agent work as provenance:** a `CreateAction` with the model as instrument and the responsible person as agent (see data-preparation-skills).
- **Trust and safety:** metadata is untrusted data; keep the rule in consume, publish and retrieve and add eval cases for prompt injection and zip-slip.
- **Fixtures:** add a 1.0/1.1 crate, a detached crate, a Workflow Run Crate, a Profile Crate and a failing-but-readable crate; fetch third-party example
  crates by script (do not commit large ones; record version, validator result, licence, source URL).
- **Lint script:** extend with profile-aware checks only if they stay deterministic; keep standard library only.
- `background/` holds the spec copies (Apache-2.0, see NOTICE) and summaries for people and agents developing skills; shipped skills must not link into it.

## Notes from stalled session



I'll test triggering the way the skill-creator does, by running claude -p with the plugin loaded and checking which skill the agent consults. First I need to see what the CLI supports here.
...


The harness is confirmed working — the plugin loads all 17 skills alongside the built-ins, and I can see which skill gets picked per query (~6s each). Next I'll build a larger prompt set, split into development and held-out test prompts, so I can tune skill descriptions without overfitting. · summary

  Ran 2 shell commands

Harness tests pass. Now the first real run on the 66 development prompts, scored by what the agent actually invokes.

  Ran 1 shell command

First pass scored 43/51 on positives and 15/15 on negatives (~$2.50), with nearly all failures caused by the agent skipping skill consultation. Since results are noisy, I'm rerunning it three times to identify which misses are consistent. · summary

  Ran 1 shell command

Baseline runs show 86% positive and 100% negative accuracy, with consistent misses on cases where the agent relies on memory instead of verified skill facts. I'll sharpen the skill descriptions and keywords for those tasks using only the dev prompts, then evaluate on the held-out set. ·

claude --resume 369cabbf-2ae2-445a-913d-5c7107fcc707
