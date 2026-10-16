# MD-08 gap resolution, pre-pilot blocker matrix and gate assessment (2026-10-15)

Status words: COMPLETED / VERIFIED (a command ran and its result is quoted) / PROPOSED — NOT ADOPTED / BLOCKED / NOT RUN. Owner decisions are in `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` entry 12.40; this file adds none. Nothing here is an approval. No advisor answer exists. The gate is CLOSED.

## 1. Gap 1: HTTP transient-status list (12.40 row 2)
Facts. Spec 13.4 defines SF1 as "HTTP/API error or timeout"; 13.8 says only that a transport-only halt (SF1) "may resume only under the identical FZ version". No file in the repository (spec v2.7, FZ-v1, parameter justification record, decision records 12.1-12.40, Step 7 manifest) names any HTTP status as transient. The list 408/429/500/502/503/504 appeared only as an illustration in `MD08_DECISION_PACKAGE_2026-10-14.md` and is not adopted. `s10_runner.py` has no retry on HTTP statuses that could be read as a policy (spec versioning rule: any retry-count change is a new FZ version).
Impact. A halt caused by any HTTP status cannot be resumed (the code refuses on `http_status is not None`). Under a real provider, 429/503 are the likeliest transient failures, so an unresolved list means such a halt ends the main run as incomplete.
Implemented (VERIFIED): HTTP statuses never qualify in code; additionally every resume after a halt is closed while `TRANSPORT_ALLOWLIST_RATIFIED = False`, because the exception allow-list `TRANSPORT_ERROR_CLASSES` is also unratified.

**PROPOSED — NOT ADOPTED (decision needed from the owner, ideally with the advisor).** Options for the status list: (a) empty: no HTTP status is transient, only exceptions (timeouts, connection/SSL errors) resume; safest, may lose runs to 429/503. (b) an explicit closed list written by the owner, each status with a one-line reason (candidates the owner may consider: 408, 429, 500, 502, 503, 504; this is a menu, not a recommendation). (c) like (b) but with a bound on how many consecutive such calls the halt may contain. Also required: ratify or edit `TRANSPORT_ERROR_CLASSES` (14 names). Risk of a wide list: resuming over a systematic fault (e.g. quota). Whichever is chosen must be fixed before the pilot (it is a halt-handling rule and belongs to the code freeze). To apply after the decision: add the list as a constant, replace the `http_status is None` condition in `is_transport_only`, set the ratified flag, extend the tests.

## 2. Gap 2: persistent evidence for a resume after a killed process (12.40 row 3)
Facts. Existing persistence: hash-chained `ledger.jsonl` (events start/intent/raw/classified/resume/reconcile), `calls.jsonl`, `raw/NNNNN.json` records (error class, http status, flags), status markers `RUN_COMPLETE`/`RUN_INCOMPLETE`, `run.lock`. A killed process leaves no marker and no record of why it died; the only durable trace of a transport failure is a persisted raw record with SF1 and a transport error class (for completed calls). A call with an intent but no raw record has no evidence at all (row 1: closed). No specification text defines "sufficient evidence".
Implemented (VERIFIED): resume without a halt marker and without a holding halt rule is refused (`PROCESS_INTERRUPTION_EVIDENCE_ADOPTED = False`), including with the owner acknowledgement; the reconcile/chain machinery is unchanged and tested as mechanics.

**PROPOSED — NOT ADOPTED: evidence contract.** A resume after a stop without marker is allowed only if all hold: (1) the ledger chain, calls.jsonl and raw files verify (existing `inspect_run`); (2) the last persisted completed call(s) are SF1-only with no response text, no HTTP status and an error class on the ratified allow-list, and the consecutive count of these is at least 1 and the failure is the cause named by the owner in the resume authorization; (3) no intent without raw record (row 1); (4) no `RUN_COMPLETE` marker, no cost-stop marker, no second marker; (5) the run lock is free; (6) the resume authorization names the ledger head. Negative cases that must be refused: no trailing SF1 record; trailing success; trailing SF1 with an HTTP status; unlisted exception class; mixed SF flags; marker contradicting ledger; corrupt or missing raw file; duplicate resume with a stale head. Honest limitation: a kill during a call leaves an intent without a record, so this contract only covers a process that died AFTER a persisted transport failure (for example during the delay); it does not cover a crash mid-call. Owner decision needed: adopt, amend or refuse (refusing means a killed process always ends the run).

## 3. Gap 3: H1-H4 at resume (12.40 row 5)
Authoritative definitions: spec v2.7 section 13.6 (H1 executable code only, no frozen-layer item; H2 byte-identical request bytes, parsed verdicts, UNP flags, scores on the frozen synthetic regression suite; H3 agreement with the frozen reference grammar checker on the triggering stored record; H4 log of code hash before and after, regression result, reason class crash/hang/logging/I/O, harness code hash in the run manifest).

| Criterion | Enforced in code now | Left to the owner's attestation |
|---|---|---|
| H1 | no | `h1_executable_code_only` (the tool cannot tell executable code from a frozen layer) |
| H2 | no (the tool does not run the regression suite) | `h2_regression_byte_identical` + `h2_regression_result_ref` |
| H3 | no (the tool does not run the reference checker) | `h3_reference_checker_agreement` + `h3_triggering_call_index` |
| H4 | yes: before hashes must equal the last segment's, after hashes the files now, reason class in the list, reason text present; the resume entry records the harness code hashes and the evidence SHA-256 | `h4_logged` |
| owner sign-off | yes: `authorized_by = owner` and `owner_signoff = true`, run id must match | the signature itself |

Implemented (VERIFIED): `_check_h1_h4` in `s10_resume.py`; any change in `s10_runner.py`/`s10_integrity.py`/`s10_resume.py` since the last segment refuses the resume unless a valid owner-signed evidence file is given (`--h1-h4-evidence`); `s10_scoring.py` change is still refused outright. Limits stated honestly: the tool hashes only the four files in `RN.code_hashes()`; the provider adapter inside `s10_runner.py` is covered, `s10_report.py`, `s11_pilot.py` and the other Step 10 files are not. Whether the owner wants those four H1-H3 attestations to be machine-checked later (run the regression suite and reference checker from the tool) is an owner decision (not proposed as adopted).

## 4. Other semantics checked
Cost stop is its own halt text (`cost stop: ...`), never counted as SF1, and a cost-stopped run is not resumable (existing `TestCostStop`, passes). Intent without record is never repeated (existing test). The advisor is not an authorizing party: `authorized_by = advisor` is refused (new test). A second resume with the same authorization is refused (new test).

## 5. Code changes (authorization: owner decisions 12.40 rows 2, 3, 5 and the owner's instruction of 2026-10-15 to implement what is authorized; no frozen artifact touched)
| File | Change | Backup |
|---|---|---|
| `research_design/step10/s10_resume.py` | two closed policy gates, `_check_h1_h4`, owner marker and H1-H4 hash in the resume entry, CLI option | `_backup/md08_impl_20261015/s10_resume.py` |
| `research_design/step10/test_resume.py` | mechanics tests run with the gates patched open; new `TestPolicyGatesClosed` (6 tests) and `TestH1H4AtResume` (4 tests incl. 13 subtests) | `_backup/md08_impl_20261015/test_resume.py` |
`s10_runner.py`, `s10_integrity.py`, `s10_scoring.py` unchanged. Note: the three Step 10 code hashes recorded for any earlier run are unaffected (no run exists). The change of `s10_resume.py` is code that P13 hashes in the final freeze list; hashes must be re-recorded at the code freeze.

## 6. Advisor notification draft (NOT SENT; for the owner to review and send)
"Subject: MD-08 owner decisions for information. The owner decided on 2026-10-15 (record 12.40): (1) a call with an intent and no stored result is never resumed or repeated; (2) resume only after a transport-only halt defined by a ratified list of transient HTTP statuses and transport exceptions (list still to be fixed); (3) no resume after a killed process without persistent evidence of a transport failure (contract still to be fixed); (4) the owner authorises each resume, the advisor is informed in the run report; (5) only pure implementation fixes meeting H1-H4 at resume; (6) a US$100 cost stop is a separate halt cause (not SF1), which spec 13.8 does not list. This message asks for no approval; if you have objections, please state them in writing."

## 7. Blocker, dependency and evidence matrix
Sources: `HUMAN_TASKS_H1_H7_OPERATIONAL_CHECKLIST.md`, `PRE_PILOT_ACTION_CHECKLIST_2026-10-14.md`, spec 13 and FZ-v1 row 19. "Blocks": CF = code freeze, PA = pilot authorization / gate.
| ID | Definition | Status | Evidence present | Missing | Depends on | Actor | Next action | Safe without authorization? | Blocks |
|---|---|---|---|---|---|---|---|---|---|
| MD-08 rows 1-6 | owner choices | AWAITING_OWNER for 3 sub-details | 12.40 | status list, evidence contract, allow-list ratification (section 1-2) | owner | owner | decide proposals | no | CF, PA |
| Advisor notice/answers | advisor Q1-Q5, notice rows 4, 6 | OPEN | draft in section 6 | sending; any answer | owner sends | owner / advisor | send | no (assistant never sends) | PA (H4 stop rule, 12.38 PG3 review) |
| R1 | true time the researcher stopped viewing registry content | OPEN | none (`human_evidence/clock/` does not exist) | the file written by the researcher | none | researcher | write it at the true time; never backdate | no | PA |
| H1 | blind check of 624 files | OPEN | blank worksheet in `step9_blind_check_kit/` | filled worksheet, evaluation.json | R1, PRD-5/PG3 ratified (12.38 done, advisor review pending) | researcher | do it | no (researcher only) | PA |
| 7-day wait | completion >= R1 + 7 days (FZ-v1 row 19) | NOT STARTED | none | R1 | R1 | time | none | no | PA |
| H3 | `step9_evidence.json` | BLOCKED | evaluator tests pass | H1, wait, H4 stop-rule clearance, owner confirmation, rebuild if artefacts change | R1, H1, wait | researcher + owner | wait | no | PA |
| H4 rehearsal | codebook rehearsal | IN_PROGRESS | `human_evidence/rehearsal/` incl. comparison.json | researcher classification, stop-rule answer (12.38/12.39) | advisor | researcher / owner | answer open items | partly | PA |
| Code freeze | no Step 10 change after this point (checklist row 10) | OPEN | none | owner declaration | MD-08 definitions, P13 entry, full check | owner | declare after the items below | no | CF, PA |
| P13 record entry | Step 11 list entry in the owner record | OPEN | applied and tested 2026-10-15 | record entry | owner | owner | write entry | no | CF |
| PRD-6 / H7 | write-once store and anchoring of the pilot decision record | OPEN | none | owner declaration | MD-09 | owner | declare | no | main run, decision script (not the pilot itself per checklist) |
| Price re-read (B7/H6) | prices and model id on run date | OPEN | none | dated note | pilot day | researcher/owner | do on the day | no | PA |
| MD-02 / C-32 | `max_input_characters` 1,016, token assumption | working decision | package text | owner confirmation | owner | owner | confirm | no | PA |
| Pilot authorization (H5) | new file from template, `authorized_by = owner`, 18 calls, ceiling 100 | OPEN | template | the file | MD-02, H3 for the gate | owner | write | no | PA |
| API key / environment | key in the terminal environment | OPEN | none | owner action | PA | owner | do last | no | PA |
| Other manifest-bound items | MD-03 (K2), PG11b scope, D3, D5, MD-10 | OPEN | none | owner/advisor entries; rebuild if any artefact changes | advisor | owner | decide | no | CF |
| Final freeze manifest | tool refuses unless `final_decision = PASS` | NOT RUN, impossible now | tool + 31-file list | PASS record after the pilot | pilot | assistant after PASS | none now | no | main run |

## 8. Code-freeze readiness: NOT READY
Reasons: row-2 list and row-3 contract undecided (they change `s10_resume.py` again); P13 entry not written; other manifest-bound owner items open; no declaration. Once those are settled the freeze needs: full `run_all_checks` (including the slow Step 8 suite), new hashes of the 31 listed files recorded, then the owner's dated declaration.

## 9. Pilot-gate assessment: CLOSED
The runner's own gate (checked by `run_all_checks`, exit 2) reports missing Step 9 evidence and missing owner authorization. Beyond that: R1, H1, 7-day wait, H3, advisor items, code freeze, PRD-6/H7, price re-read and the explicit start instruction are unmet. A passing implementation does not change this.

## 10. Owner decisions needed (in dependency order)
1. HTTP status list option (a/b/c) and ratification of `TRANSPORT_ERROR_CLASSES`.
2. Adopt, amend or refuse the persistent-evidence contract for a killed process.
3. Whether H1-H3 attestations stay manual.
4. P13 record entry; other manifest-bound items (MD-03, PG11b, D3, D5, MD-10).
5. Send the advisor notice (section 6); advisor answers to Q1-Q5.
6. Code-freeze declaration, PRD-6/H7, MD-02, H5 authorization.

---
# UPDATE 2026-10-15 (third round; decision record entry 12.42). Supersedes the statuses of sections 1, 2, 3, 5, 7-10 above where they differ.

## U1. Status vocabulary, per item
| Item | Owner instruction received | Policy recorded | Technical spec adopted | Class ratified | Code implemented | Tests passed |
|---|---|---|---|---|---|---|
| HTTP status allow-list empty (Option A) | yes | yes (12.42 A1) | yes | n/a | yes (`HTTP_STATUS_ALLOWLIST = frozenset()`, `is_transport_only`) | yes: `TestHttpAndClassPolicy` (every status 0-599 sample rejected, mixed flags, response text, unratified class, ratified non-candidate ignored) and the existing 429/503 end-to-end tests |
| Process-death evidence contract | yes | yes (12.42 A2) | yes (conditions 1-8 in 12.42, limited to a death AFTER a persisted transport failure) | n/a | yes (`_process_death_contract`, authorization fields `failure_cause`, `trailing_transport_failures`) | machinery yes (`TestProcessDeathContract`, 14 tests incl. subtests with a TEST-ONLY class). Policy-level positive: NOT POSSIBLE, no class is ratified |
| H1-H3 manual attestation | yes | yes (12.42 A3) | yes | n/a | yes (`_check_h1_h4`, unchanged this round) | yes (`TestH1H4AtResume`); the attestations' truth is NOT checked by the tool |
| 14 exception classes | yes (audit) | audit recorded (12.42 A4) | n/a | **none of 14 ratified** | deny-by-default (`RATIFIED_TRANSPORT_ERROR_CLASSES = frozenset()`) | yes: nothing is transport-only while empty |

Effect: no resume (after a halt, or after a stop without marker) is possible until the owner ratifies at least one class. The contract is ADOPTED and IMPLEMENTED; it is VERIFIED only as machinery. Its production-level positive path cannot be shown honestly until a class is ratified (then the same tests run with the real set).

## U2. Honest limits of what was tested
- Mechanics tests (`Base`) run with a TEST-ONLY ratified set `{"TimeoutError"}` and the contract check switched off, to exercise reconcile/chain/counter/lock code; they verify no policy. `ProductionPolicyBase` tests run with the shipped constants (contract enforced, nothing ratified) and use the TEST-ONLY set only where a positive path needs one (declared in the test names and docstrings). The production constants in the module were never edited to make a check pass.
- Active run lock: covered by the existing `test_a_resume_started_while_the_run_is_alive_is_refused` (adversarial file), not re-tested in the new class. Cost stop: covered by `TestCostStop` (cost-stopped run not resumable; its halt text is not SF1). Intent without a raw record: covered by the existing test and re-tested under the production configuration. Duplicate authorization: re-tested under the contract.
- H2/H3 evidence is a reference string and an index; the tool does not open the referenced regression result.

## U3. Manifest-bound items and P13 (F1, F2)
| Item | Authoritative source | What exists | What is missing | Needs |
|---|---|---|---|---|
| P13 (Step 11 list 24 -> 31) | `STEP11_FILE_LIST_PROPOSAL_2026-10-14.md`; applied 2026-10-15 on the owner's chat instruction | patch applied, guard test passes; `s10_resume.py` is in the 31-file list, so its hash must be re-recorded after the final code change | an entry in the owner record. It is an owner approval of a list, not a record of work, so I did NOT write it as completed. Draft: "12.4x Step 11 file list. The owner approves the 31-file list of P13 (proposal of 2026-10-14), applied on 2026-10-15; hash of the tool before bbcbf153076a7232, after 7395140c...10eb." | `AWAITING_OWNER` |
| MD-03 / K2 | `OWNER_APPROVAL_PACKAGE.md` row 2 | choice K1 (no code) or K2 (Step 7 re-freeze R-7, Step 8 rebuild) | owner answer | `AWAITING_OWNER`; K2 triggers a rebuild |
| PG11b scope | same package row 4 | default: keep the literal scan | owner answer | `AWAITING_OWNER`; narrowing = new methodology version |
| D3 (SF/UNP policy, MPR 3 D3, conflict C-08) | `MASTER_CONFLICT_INDEX.md` C-08 | interim rule | owner decision before the FZ hash | `AWAITING_OWNER` / advisor |
| D5 (re-code values, C-09) | `MASTER_CONFLICT_INDEX.md` C-09 | delegated reading | decision before the FZ hash | `AWAITING_OWNER` |
| MD-10 | package row 6 | confirm PC-2, I-6, P-3, F-3, PRD-8, Step 8 choices | owner confirmation and advisor review | `AWAITING_OWNER`, `AWAITING_ADVISOR` |
| MD-09 / PRD-6 / H7 | package row 17 | none | write-once store + anchoring declaration | `AWAITING_OWNER` |
No frozen artifact was touched and no record was invented for any of these.

## U4. Advisor (F3)
The draft in section 6 is still accurate except that rows 1-3 now read: HTTP statuses: none qualifies; process-death: contract adopted (evidence = persisted transport failure on a ratified class); exception classes: audited, none ratified yet. It is **NOT SENT** and **no advisor response exists**. Advisor-dependent: Q1-Q5 of `H4_ADVISOR_DECISION_REQUEST_READY_2026-10-14.md` (reading of "used", `s2_arith` without a prompt, sufficiency of the rehearsal, role in 12.39, PG3 review), the H4 stop-rule clearance, and the notice for the cost stop (a halt cause not listed in spec 13.8). No answer is assumed from silence.

## U5. Human evidence and clock (F4, F5, F7)
`human_evidence/clock/` does not exist: **R1 NOT RECORDED**, seven-day wait **NOT STARTED** (FZ-v1 row 19: completion >= R1 + 7 full days; no earliest date can be computed). A template is at `templates/R1_clock_note_TEMPLATE.md` (not evidence; awaiting the researcher). H1: blank worksheet exists, no filled worksheet, no `evaluation.json`. H3 `step9_evidence.json`: not created (needs H1, the wait, H4 stop-rule clearance and the owner's written confirmation). H4 rehearsal: files exist under `human_evidence/rehearsal/`; the researcher's classification and the advisor items stay open. Offline checks already pass (evaluator tests, `run_all_checks`, gate exit 2).

## U6. PRD-6, H7, MD-02, H5, price, environment (F6) - none satisfied
PRD-6/H7/MD-09: not declared (`AWAITING_OWNER`). MD-02 (`max_input_characters` 1,016, `input_tokens_per_call_assumed`): working decision only, owner confirmation missing. H5 pilot authorization: no file; template `templates/owner_authorization_TEMPLATE.json` is invalid while empty; I created none. Price/model re-read (B7/H6): due on the day of the first paid call, not done. Environment: the API key must be set by the owner in the terminal that runs the pilot, never in a repository file; `.env` does not exist and was not created. Pilot start instruction: not given.

## U7. Updated blocker table (additions/changes to section 7)
| ID | Status | Owner / actor | Next action |
|---|---|---|---|
| Exception-class ratification | AWAITING_OWNER (14 of 14 unratified) | owner | rule on the draft entry in `MD08_EXCEPTION_AUDIT_2026-10-15.md`; without it no resume exists |
| URLError reason not stored | OPEN (NEEDS_EVIDENCE for 5 classes) | owner decides whether to change the stored record (code freeze scope) | decide |
| H1-H3 evidence for any actual fix | not applicable until a fix is made | owner | produce when needed |
| P13 record entry | AWAITING_OWNER | owner | enter |
| Advisor notice / answers | AWAITING_ADVISOR (notice unsent) | owner sends | send, wait |
| R1 / H1 / wait / H3 | OPEN / OPEN / NOT STARTED / BLOCKED | researcher | R1 first |
| Code freeze | NOT READY | owner | after ratification, P13 entry, manifest-bound items, then full `run_all_checks` |
| PRD-6/H7, MD-02, H5, price, key | OPEN | owner / researcher | see U6 |

## U8. Gate: CLOSED. Code freeze: not declared. Final freeze manifest: not created (impossible before a PASS record).

