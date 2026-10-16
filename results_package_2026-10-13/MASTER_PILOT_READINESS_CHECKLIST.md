# Master pilot readiness checklist

Status words: DONE (evidence file named), OPEN (no evidence), HUMAN (only a person can do it), WAITING (decision pending), BLOCKED (depends on an open item), NOT_STARTED (technical work after a decision). Statuses are taken from the artefacts as of 2026-10-13, not assumed. **Overall: pilot gate CLOSED. Nothing below may be marked DONE without the evidence named in its last column.** Decisions: `MASTER_PROPOSED_DECISION_RECORD.md` (MD-xx); conflicts: `MASTER_CONFLICT_INDEX.md` (C-xx).

## 1. Technical and local verification
| # | Item | Status | Evidence needed / present |
|---|---|---|---|
| T1 | Frozen inputs unchanged (spec, FZ-v1, Step 7 freeze manifest, Step 8 build) | DONE (checked repeatedly by hash) | hashes: spec `d5fcffad...`, freeze manifest `202979de...`, build manifest `09eed00e...`, FZ-v1 file `14944571...`; `run_all_checks.py --quick` |
| T2 | Step 8 build verified (30 numeric gates, rendering gates, repeat build, verifier) | DONE | `step8_output/step8_build_7a6bbe465c66/`, 30 tests |
| T3 | Implementation B agrees on the build | DONE | `step9/impl_b.py` output "AGREE", 10 tests |
| T4 | Runner, scoring, integrity, pilot glue, coding prep tested with mocks | DONE | `step10/` suites (18, 11, 8, 11, 16 tests) |
| T5 | SF counting from flag sets (MD-01) | LOCAL TEST DONE for the working decision; NOT ADOPTED. SF2-with-SF1/SF4 (C-31): WORKING DECISION option B | `test_sf_matrix_literal.py` 14 tests OK, no expectedFailure; `test_sf2_detection.py` 19 tests OK, no expected failure; adopted entry still needed |
| T6 | Provider safe-stop policy (MD-06) | WAITING, then NOT_STARTED | adopted entry; patch P2 and tests |
| T7 | Input-size gate (MD-02) | LOCAL TEST DONE for the working decision (character limit); NOT ADOPTED. Assumed-tokens gate and token-measurement method OPEN | `test_input_limit.py` 10 tests OK; adopted entry still needed; the limit is a control, not a token measurement or a cost guarantee |
| T8 | FZ index tool and enforcement (MD-04) | WAITING, then NOT_STARTED | adopted entry; patch P5 and tests |
| T9 | Anchor check (MD-09) | WAITING | adopted entry; patch P7 |
| T10 | Gate check without `--live` prints "gates open" for the right reasons | OPEN (currently CLOSED: no evidence file, no valid authorization) | command output |
| T12 | Interrupted-run and damaged-ledger behaviour characterized (no resume exists) | DONE (local, mock) | `test_ledger_resilience.py` 11 tests OK |
| T13 | C-31 / C-32 analysis package for the owner (decision table, definitions D1-D8, questions Q1-Q9) | DONE (analysis only; decisions PENDING) | `C31_C32_OWNER_DECISION_BRIEF.md`; `test_sf2_variants.py` 11 tests OK |
| T11 | Same-author limitation recorded | DONE (recorded) | a second reviewer or a second implementation would be needed to remove it; not required by the text |

## 2. Methodological decisions (adopted entries with names and dates)
The approve/reject form for every row below is `OWNER_APPROVAL_PACKAGE.md`.
Status vocabulary (2026-10-13): PROPOSED, WORKING DECISION (applied in code on the project owner's direction; not an official entry, not approved by the advisor), PENDING OWNER, APPROVED (real approval only). Today no M-item is APPROVED; M1 and M2 are WORKING DECISIONS with the open parts listed in `C31_C32_OWNER_DECISION_BRIEF.md`; the per-decision register is in `MASTER_PROPOSED_DECISION_RECORD.md`.
| # | Decision | Needed before | Status |
|---|---|---|---|
| M1 | SF counting convention and `f_S` unit (MD-01; C-04, C-05) and SF2 detection (C-31) | pilot | WAITING (working decision applied in code; not ratified) |
| M2 | OD-10 input-size basis for paid pilot calls (MD-02; C-01) | pilot | WAITING (working decision applied in code; not ratified; owner writes `max_input_characters` in the authorization) |
| M3 | PG3 reading (MD-05; C-06) | pilot | WAITING |
| M4 | PRD-5 (MD-05; C-11) | evaluating the blind check | WAITING |
| M5 | Provider safe-stop policy (MD-06; C-12..C-15) | pilot | WAITING |
| M6 | FZ hash contract (MD-04; C-03) | FZ hash = before the first pilot call | WAITING |
| M7 | Kappa and re-code values (MD-03; C-02, C-09) | FZ hash | WAITING |
| M8 | PG11b scope (MD-05; C-07) | FZ hash | WAITING |
| M9 | §18.2 policy (MD-05; C-08) | FZ hash | WAITING |
| M10 | Timeout meaning (MD-07; C-16) | FZ hash | WAITING |
| M11 | Confirmation of Step 8 design choices (MD-10; C-28) | FZ hash | WAITING |
| M12 | Resume (MD-08; C-17), PRD-6 (MD-09; C-18), coding eligibility (C-10), P-3 item 1 (C-22), token measurement (C-23) | main run / step 11 / coding | WAITING |
Evidence to mark any M-item DONE: an entry in the official record naming the option chosen, the approver and the date. A draft, a recommendation or a report is not evidence.

## 3. Human tasks
Operational detail for each row (procedure, inputs, evidence, acceptance, location): `HUMAN_TASKS_H1_H7_OPERATIONAL_CHECKLIST.md`. Every row below is still NOT DONE.
| # | Task | Status | Evidence | Rules |
|---|---|---|---|---|
| H1 | Blind check of 624 files (`HUMAN_TASK_GUIDE.md` part 1) | HUMAN, not done | filled worksheet; evaluator output "NO REJECT", coverage 100 % | opaque-ID files only; calculator allowed; never edit rows after the evaluation |
| H2 | Seven-day delay | BLOCKED by H1's start | completion date at least 7 days after the last viewing of rendered registry content or expected states (FZ-v1 row 19) | the person supplies both dates; they are not invented or backdated; the clock is not running now |
| H3 | Step 9 evidence file | BLOCKED by H1, H2, M4 | `s9_blindcheck.py ... --evidence-out` output; the runner gate reads it | the tool refuses on any REJECT |
| H4 | Codebook rehearsal, 40 rows | HUMAN, not done | filled sheet and `compare_rehearsal.py` output | before the pilot (spec 13.5); do not open the battery before finishing |
| H5 | Owner authorization (pilot round 1) | HUMAN, not done | file with `authorized_by` = owner, scope `pilot_round_1`, `max_calls` 18, `cost_ceiling_usd` 100, input-size basis | the template is empty and is rejected |
| H6 | Re-read prices and model terms (PJR J-9) | HUMAN, not done | dated note | on the day of the paid call |
| H7 | Declare the write-once store (PRD-6) | HUMAN, not done | record entry | before the decision script runs |
| H8 | Sequence respected | rule | H1 → H2 → (M4 decided) → H3; H4; M-items; H5 last, after the cost basis is chosen | do not do H5 before M2, H3 before M4, or the pilot before the FZ hash |

## 4. Provider verification
Procedures, evidence and PASS/FAIL/INCONCLUSIVE criteria for each row: `PROVIDER_VERIFICATION_MATRIX.md` (prepared; nothing run). (all need separate written owner authorization; none done)
| # | Item | Status | Criteria to allow one live connection test |
|---|---|---|---|
| L1 | Request field names accepted | OPEN | authorization file for scope "connection test", `max_calls` 1, cost ceiling stated; a neutral prompt that is not a registry prompt and not experiment content; the response is handled as non-experimental metadata and its text is not used for any protocol decision; the key is present; MD-06 adopted so that anomalies stop the workflow |
| L2 | Returned model ID form (alias or suffix) | OPEN | same test |
| L3 | Finish-reason vocabulary; block signals (names, `promptFeedback`) | OPEN | same test shows only what one call returns; further names may appear later (hence MD-06 safe-stop) |
| L4 | Usage fields (`thoughtsTokenCount`, `totalTokenCount`) | OPEN | same test |
| L5 | Timeout behaviour | OPEN | cannot be settled by one call; decided by MD-07 |
| L6 | Token count of the 1,248 + 96 prompts | OPEN | separate authorization (MD-02 option O2) |
Do not open L1 merely to see whether the adapter works; open it when the criteria hold and the owner has authorized it in writing.

## 5. Pilot prerequisites (round 1)
Frozen state T1-T3 DONE; T5-T7 and T10 done; M1, M2, M3, M5 adopted; M4 if the blind check is evaluated; M6-M11 adopted (FZ hash exists and is enforced); H1-H5 done with evidence; H6 on the day; provider anomalies stop the run (T6); API key present (checked by the preflight); gate check without `--live` prints "gates open". Round 2 only after a whitelisted change as a new FZ version and a new authorization.

## 6. Main-run prerequisites
Final pilot decision record PASS, anchored (H7, T9); final freeze manifest written after the record; authorization with scope `main`, 2,496 calls, input-size basis for 1,248 prompts (M2, O2/O4); M12 items for coding adopted before coding; resume policy adopted or the decision to forbid resume recorded; prices re-read.

## 7. Final readiness criteria
Every row of sections 1-3 DONE with its named evidence (T5-T9 only where the corresponding decision requires code), sections 4-5 satisfied, no gate opened by assumption, and the outcome of the gate check itself. Until then the status is: **not ready for the pilot**.
