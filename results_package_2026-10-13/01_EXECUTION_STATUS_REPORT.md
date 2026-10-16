# Execution status report (updated 2026-10-13, after write access was authorized)

## 1. Two separate studies

| | Pilot clarification (Stage 1 / Stage 2) | Scenario-construction experiment (specification v2.7) |
|---|---|---|
| Model | `gemini-3.1-flash-lite` | frozen: `gemini-3.5-flash-lite`, thinking minimal, 8192 output tokens, 0 retries, 180 s, 1 s delay, concurrency 1 (verified in the register and checked by the Step 8 build) |
| Model responses | 30 (Stage 1) + 40 (Stage 2) ok; 30 error records from a failed first attempt | **none** |
| Status | complete, analysed (`03_EXPERIMENTAL_RESULTS.md`) | Steps 1 to 8 complete; Step 9 and later blocked by a human action |

## 2. Pilot clarification: complete, not repeated
Stage 1 (30/30 ok, INVESTIGATE) and Stage 2 (40/40 ok, CONTINUE) were not rerun or overwritten. 60 hashes re-verified, 0 mismatches; headline counts independently recomputed. Evidence: `05_REPRODUCIBILITY.md`.

## 3. v2.7 experiment, step by step

| Step | Status | Evidence |
|---|---|---|
| 1 to 6 | complete | spec `d5fcffad...`; FZ-v1 register `c7d50e11...` recomputed |
| 4 numeric dry run (Implementation A) | complete | 30/30 gates, main and pilot; 123 tests OK (re-run) |
| **7 prompt-specification freeze** | **done on the owner's instruction (2026-10-13); advisor items open** | `research_design/step7/STEP7_PROMPT_SPECIFICATION_FREEZE_MANIFEST_v1.json` (status FROZEN_ON_OWNER_INSTRUCTION, 11 freeze-set files, proposals excluded); decision entries 12.26, 12.27; snapshot `step7_history/revision4_2026-10-13/`; codebook revision 5; 150 Step 7 tests OK |
| **8 registry generation** | **done, all acceptance checks pass** | `research_design/step8_output/step8_build_7a6bbe465c66/`: main 312 templates / 1,248 prompts (sha256 `7a6bbe46...`), pilot 24 / 96 (`2b77d718...`), 30/30 numeric gates on the generator's data, equivalence with Implementation A's builders, 14 rendering-stage gate identifiers on every prompt, two byte-identical builds, independent verifier clean, 30 Step 8 tests OK; decision entry 12.28 |
| 9 independent validation | **Implementation B done; human blind check pending (blocks completion)** | `research_design/step9/impl_b.py`: AGREE on 312 + 24 templates (strict parse, decimal recomputation, PG1-3, PG5-10, PG11a, PG12, A1b, A6b, A7, guard); 10 mutation tests OK; entry 12.29. The **human blind check** needs you and a minimum **7-day** delay (FZ-v1 row 19). Kit: `step9_blind_check_kit/`; codebook rehearsal kit: `codebook_rehearsal_kit/` |
| 10 pilot (18 calls) | **not started, not permitted yet** | section 21.1: no pilot before step 9 |
| 11 final pilot decision, 12 main run (2,496 calls) | not started | depend on 10 |

No model call, network call or token count was made at any step.

## 4. Open approvals and risks (none represented as approved)
1. Advisor: main-run SF/UNP policy (kept as v2.7 text), PG11b scan scope (kept literal; ordinary words such as "CLEAR" can be rejected post-run), delegated re-code values and section 16.3 departures, **PG3 reading** (single changed span; the strict reading would reject 90 of 104 MIL templates), human rehearsal of the codebook battery (pre-pilot).
2. Same-author limit: generator, gates, verifier and tests share one author; the verifier is not Implementation B.
3. A change to a freeze-set file before the FZ hash returns to Step 7.

## 5. Single next action
Do the human blind check (or tell me who does) and start the 7-day clock; also do the codebook rehearsal. Everything else eligible is complete. Bring the advisor items above to the meeting.

## 6. Harness notes
Writes into `research_design/` were first denied by the auto-mode classifier; after you authorized the scope in chat, the same plain commands were accepted. The empty folder created during the first denied attempt is now the revision-4 snapshot folder.
