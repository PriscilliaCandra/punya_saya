# Master implementation plan (IMPLEMENTATION PLAN — nothing may be done before the decision it names is adopted)

Status: PROPOSED — NOT ADOPTED. No code was changed to produce this plan. Decision IDs MD-xx are in `MASTER_PROPOSED_DECISION_RECORD.md`; conflict IDs C-xx in `MASTER_CONFLICT_INDEX.md`. Files are in `research_design/step10/` unless stated.

## 0. Rules for every patch
- Precondition: the named MD entry exists in the official record with an approval block filled by the owner (and the advisor where the entry says so). Without it, do not start.
- Before editing: `git status`, hash list of the files to touch, copy to `results_package_2026-10-13/_backup/<patch id>/` (existing practice). Frozen files are never edited: the specification, the FZ-v1 file, `step7/` freeze-set files, `step8_output/`, `implementation_a/`, Stage 1/2 folders, the official record (append only, by the owner's instruction).
- Acceptance criteria are written from the adopted rule (hand-derived expected values), never from what the code currently returns.
- Tests: mock providers and synthetic data only; `python -B -I -W error::ResourceWarning`. Re-run only the suites named in the patch plus `run_all_checks.py --quick` at the end.
- Rollback: restore the backup copies; remove only the new files created by the patch; the official record is not rolled back (append a correcting entry instead).
- Forbidden until the checklist (`MASTER_PILOT_READINESS_CHECKLIST.md`) is complete: running the pilot or the main run, any live call.

## 1. Order of patches
| Order | Patch | Needs | Files touched | New tests (acceptance) |
|---|---|---|---|---|
| 1 | **P1 SF counting from flag sets** (acceptance tests for the hard-flag rows already exist as `test_sf_matrix_literal.py`, derived from the text of §13.6, six rows marked expectedFailure: remove the markers when P1 is applied) | MD-01 | `s10_scoring.py` (`pilot_counts`, helpers), `s11_pilot.py` (report fields), docs | `test_sf_matrix.py`: all 31 non-empty subsets of {SF1..SF5} that `sf_flags` can emit (plus the ones forced via crafted records): the outcome equals the value from a hand table derived from §13.6 under the adopted unit; no subset with SF2/SF3/SF5 passes; single-flag outcomes unchanged; multi-flag calls reported; ledger `classified` entry unchanged; `s7_decision` untouched |
| 2 | **P2 Provider safe-stop policy** | MD-06 (and MD-01 for the hard+soft stop) | `s10_scoring.py` (lists, unlisted handling), `s10_runner.py` (stop path, status marker `RUN_INCOMPLETE` with reason), `s10_integrity.py` | mock cases: model mismatch, unlisted reason, missing status, hard+soft multi-flag each stop after recording the call, raw stored before the stop, hash chain valid, no further call made, retries 0; blocked names list per MD-06; nothing scored as valid after a stop |
| 3 | **P3 Input-size gate** | MD-02 | `s10_runner.py` (`check_gates`), `s10_integrity.py` | authorization with assumed tokens below the longest prompt length (read from `prompt_table.json`) is refused; with a stated measured basis accepted; hard-cap cost unchanged; no other gate behaviour changes |
| 4 | **P4 Kappa / re-code reporting** | MD-03 | `step7/s7_recode.py` and codebook sections 5.1/5.3 are FREEZE-SET files: a change returns to Step 7 (new version, new freeze manifest, before the FZ hash). If K1 is adopted: no code change, record only | for K2/K3: kappa hand-computed on small tables incl. undefined cases; label text present; no chance-corrected claim; `test_step7.py` updated knowingly |
| 5 | **P5 FZ index tool and enforcement** | MD-04 | new `fz_index.py` (writes the index, new file only), `s7_decision.py` is a freeze-set file (check there = Step 7 change; alternative: check in the runner and in `s11_pilot.py decide` before calling the decision script), `s10_runner.py` (`check_gates`), `s11_final_freeze_manifest.py` | tool output equals a hand computation on a small fixture; a one-byte change of a listed file changes the hash; the gate refuses a missing or mismatching hash; the final freeze manifest still includes the record hash and is not the FZ hash |
| 6 | **P6 Timeout total deadline (only if MD-07 chooses it)** | MD-07 | `s10_runner.py` (`GeminiProvider.generate`) | mock server-less test: a provider that blocks longer than the deadline yields SF1 without a second call; summary states the semantics; frozen value 180 unchanged; since this changes the behaviour of a frozen setting it needs the FZ decision first |
| 7 | **P7 PRD-6 anchor check** | MD-09 | `s10_runner.py` (main scope), new small verifier | main run refuses if the recomputed hash of the decision record differs from the anchored value or no anchor is recorded |
| 8 | **P8 Resume tool (only if MD-08 adopted)** | MD-08, MD-01, MD-06 | new `s10_resume.py`, `s10_runner.py` (shared ledger writer), `s10_integrity.py` | local simulations: (a) halt at `c_stop` then resume appends to the same chain and never repeats an index; (b) interrupt after `intent` without `raw`: resume refuses until a recorded disposition exists, then continues at the next index without repeating that key; (c) counters carry over; (d) settings or FZ hash differ: refused; (e) no authorization: refused; (f) retries stay 0 (every key at most once in `calls.jsonl`); (g) `s10_integrity` passes on the resumed folder |
| 9 | **P9 Report tooling for the above** | patches done | `s10_report.py`, docs | outputs state counts, flags, stops, basis of cost |
| 10 | Documentation sync | all | `NEXT_ACTIONS.md`, `OPERATIONS_RUNBOOK.md` (new files with a new name or a dated section; do not rewrite old reports) | commands re-verified with `--help` |

Patches 1-3 are the minimum code for the pilot; 4-5 belong to the FZ hash; 6-8 only if the corresponding decisions are adopted; none changes the build or the registry.

## 2. Risks to control
- P1 and P2 alter what the ledger `classified` event contains only by adding fields; the order intent → raw → classified must stay (tested in `test_pilot_flow.py`, rerun after the patch).
- P4/P5 touch freeze-set files: do not touch them silently; a new Step 7 freeze manifest version and a record entry are required.
- No patch may weaken `check_gates`; a patch that changes a gate is itself a decision item.

## 3. Final regression (after all adopted patches)
`python -B -I results_package_2026-10-13/reproduce/run_all_checks.py` (including the slow Step 8 suite once), the new suites, git status comparison, hash comparison of the frozen files. Expected: all as before, gate status still CLOSED until the human evidence and the authorization exist.
