# Master closeout report (local pre-pilot batch, 2026-10-13)

**The research is NOT pilot-ready. The pilot gate is CLOSED, as expected.** (See the addendum at the end of this file for the final pre-pilot preparation batch.) This report states what was actually done and verified in the closeout batch; it makes no claim about decisions that have not been made. Status vocabulary: PROPOSED, WORKING DECISION (applied in code on the project owner's direction; not an official entry; not approved by the advisor), PENDING OWNER, APPROVED (real approval only). **Nothing is APPROVED.** The official record (`STEP3_OWNER_DECISIONS_RECORD_DRAFT.md`) was not edited.

## 1. Work completed, with evidence
| Item | Evidence |
|---|---|
| Baseline validated before editing: no unexpected change since the previous batch; relevant suites passed | `test_sf2_variants` OK, `test_sf2_detection` OK (4 expected failures), `test_sf_matrix_literal` OK, `test_ledger_resilience` OK, `test_provider_response` OK, `test_input_limit` OK |
| Docstrings of `s10_scoring.py` (module) and `s11_pilot.py` (line 5) corrected so that they describe the behaviour in force as a working decision | edit script asserts the code AST (docstring excluded) is identical before and after; backups `_backup/master_exec/s10_scoring.py.before_docstring`, `s11_pilot.py.before_docstring`; `test_sf_matrix_literal`, `test_pilot_flow`, `test_sf2_detection`, `test_sf2_variants` re-run OK; `test_step10` and all others in the regression below |
| Inactive P1b diff regenerated for the new `s10_scoring.py` base (CRLF-preserving) | applied with `patch -p1 --binary` to a scratch copy: clean, result byte-equal to the intended patched copy; the real file was not touched |
| Decision status register (MD-01 to MD-10) added to `MASTER_PROPOSED_DECISION_RECORD.md`; per-patch register (P1 to P10) added to `deferred_patches/DEFERRED_PATCHES.md` | both state "no entry is APPROVED"; B for C-31 stays a RECOMMENDATION in the brief and in MD-01 item 2b |
| Cross-document reconciliation: checklist, `NEXT_ACTIONS.md` (D4 row, label collision between advisor-brief D1-D8 and brief definitions D1-D8), `00_INDEX.md`, conflict index (C-33 wording), execution report (hash correction), `PROPOSED_RECORD_CORRECTION_12_37.md` (factual basis, impact, approvals) | greps: register headings present once; C-31/C-32/C-33 rows present |
| Reproduction package checked: `run_all_checks.py` registers the SF acceptance, SF2 detection, SF2 variant, ledger, provider-response and input-limit suites | `--quick` run: every check OK, slow Step 8 suite SKIPPED (not affected by this batch), gate check exit 2 = CLOSED (expected) |
The 384-record grid and the 20-case analysis were not repeated; their results are pinned by `test_sf2_variants.py` (11 tests, OK) and were used as the baseline.

## 2. Files changed in this batch and why
- `research_design/step10/s10_scoring.py`, `s11_pilot.py` — docstring text only (stale statements 5 and 6 of the correction audit). Hashes now `67b85b183fab...`, `68fc807f85a7...`; `s10_runner.py` `86954f14c790...` and `s10_integrity.py` `17c1ec621b23...` unchanged.
- `deferred_patches/P1b_sf2_independent_detection.diff.INACTIVE` — regenerated for the new base; still inactive.
- `deferred_patches/DEFERRED_PATCHES.md` — base hash reference; status register with files, dependencies, acceptance tests, owner and the explicit condition to continue.
- `MASTER_PROPOSED_DECISION_RECORD.md` — status register at the top.
- `MASTER_PILOT_READINESS_CHECKLIST.md` — status vocabulary note in section 2.
- `NEXT_ACTIONS.md` — D4 row reconciled, reconciliation note.
- `00_INDEX.md` — closeout report row.
- `MASTER_CONFLICT_INDEX.md` — C-33 wording.
- `PROPOSED_RECORD_CORRECTION_12_37.md` — rows 5-6 marked corrected; section 5 (evidence, impact if corrected or not, approvals).
- `MASTER_EXECUTION_REPORT.md` — addendum 2 (hash correction).
- New: this report. Backups of every edited file: `_backup/master_exec/*.before_closeout`, `*.before_docstring`. Rollback: copy the backup over the file; delete this report.

## 3. Owner / advisor decisions still PENDING
C-31 (Q1-Q6: SF2 with SF1/SF4; recommendation B written as definitions D1-D8, not adopted; unit of `f_S`; whitespace set; status-less record; candidate indicator); C-32 (Q7-Q9: assumed-token gate, main-run token method, form of a "measured basis"); C-33 (whether and how to append a status entry to the official record; draft text in `PROPOSED_RECORD_CORRECTION_12_37.md`); MD-03 kappa/re-code; MD-04 FZ hash contract and file list; MD-05 PG3, PG11b, SF/UNP policy, eligibility, PRD-5; MD-06 provider safe-stop and block names; MD-07 timeout; MD-08 resume; MD-09 anchor and authorization content; MD-10 confirmations of Step 8 choices. Ratification of the working decisions MD-01 and MD-02 is also PENDING.

## 4. Human tasks not done (no evidence created)
H1 blind check of 624 files; H2 seven-day delay after the last viewing (clock not running); H3 Step 9 evidence file; H4 codebook rehearsal (40 rows); H5 owner authorization (with `max_input_characters` and `input_tokens_per_call_assumed` >= 1,016 written by the owner); H6 price and model re-read on the day of the paid call; H7 declaration of the write-once store (PRD-6).

## 5. Provider verification not authorized, not done
L1 request field names, L2 returned model ID form, L3 finish-reason vocabulary and block names, L4 usage fields, L5 timeout behaviour, L6 token count of the 1,344 prompts. Each needs separate written owner authorization (`MASTER_PILOT_READINESS_CHECKLIST.md` section 4). The Gemini adapter and `BLOCK_REASONS` remain UNVERIFIED against the live API; mock tests do not prove compatibility.

## 6. Patches held and their dependencies
| Patch | Status | Depends on / explicit condition to continue |
|---|---|---|
| P1 | DONE as working decision | ratification of MD-01 unit |
| P1b | READY FOR OWNER APPROVAL | answers Q1-Q6; if B/A2c, no scoring change |
| P2 | READY FOR OWNER APPROVAL (stop clauses) + BLOCKED BY PROVIDER VERIFICATION (names) | MD-06, L1-L3 |
| P3 | DONE as working decision | ratification of MD-02 |
| P3b | READY FOR OWNER APPROVAL; O2 BLOCKED BY PROVIDER VERIFICATION | Q7-Q9 |
| P4 | DEFERRED | MD-03; Step 7 freeze-set files |
| P5 | DEFERRED | MD-04 with the file list |
| P6 | DEFERRED | MD-07, L5 |
| P7 | BLOCKED BY HUMAN TASK + DEFERRED | H7, MD-09 |
| P8 | DEFERRED | MD-08, P2, MD-01, MD-06 |
| P9 | PARTLY DONE | P2, P5, P7, P8 |
| P10 | DONE for this batch | repeat after any decision |
Full table with files, acceptance tests and owners: `deferred_patches/DEFERRED_PATCHES.md`, end of file. No held patch was applied to raise a completion figure.

## 7. Integrity check results
| Check | Result |
|---|---|
| Spec v2.7 | sha256 `d5fcffadd104...` as recorded in the checklist |
| Step 7 freeze manifest | `202979de2a88...` as recorded |
| Step 8 build manifest | `09eed00eeb79...` as recorded; Step 8 verifier and Implementation B OK |
| FZ-v1 | `149445715a82...` as recorded |
| Official decision record | `5a7ff7687850...`, last modified 10:31, before the first batch; unchanged (12.30, 12.37 not edited) |
| Stage 1/2 | `verify_stage_evidence.py` OK; Stage 2 headline recomputation OK; no file under `pilot_clarification` changed |
| Registries, Step 7, Step 8 folders | no file changed since 10:00 |
| `.env` / credentials | no `.env` file exists in the repository root; none read or written |
| Git | no commit, push, reset, stash or other operation |
| Human evidence / authorization | none created; no timestamp invented |

## 8. Pilot gate status
**CLOSED.** Gate check exit 2. Reasons: (1) no Step 9 evidence file (no human blind check); (2) no valid owner authorization (the template is empty and rejected). In addition the readiness checklist lists open decisions that must be recorded before the pilot (M1 to M11) and the open provider verification. Passing tests opened nothing and cannot open it. Main-run gate: CLOSED (needs a PASS pilot record, anchor, final freeze manifest and an authorization for 2,496 calls).

## 9. Next actions in dependency order
1. **Owner/advisor:** answer Q1-Q9 of `C31_C32_OWNER_DECISION_BRIEF.md`; decide on the correction entry for the record (C-33). Then the assistant rewrites the four marked tests from the ratified rule (no scoring change if B/A2c).
2. **Owner/advisor, before the FZ hash:** MD-03, MD-04 (file list), MD-05, MD-07, MD-10; then the FZ index (P5) and any Step 7 re-freeze (P4). The FZ hash precedes the first pilot call.
3. **Owner/advisor, before the pilot:** MD-06 (safe-stop) and, if wanted, a written authorization for a single connection test (L1-L5) once its criteria hold; then P2.
4. **Researcher (human):** decide the viewing-stop date (B1) -> H1 blind check (after PRD-5 is decided) -> wait at least 7 days -> H3 evidence file; H4 rehearsal; H5 authorization after M2/C-32 is settled; H6 on the day.
5. **Gate check** without `--live` (must print "gates open" for the right reasons) -> pilot round 1 only on the owner's explicit instruction -> `s10_integrity` -> `s11_pilot report` -> `decide`.
6. **After the pilot:** H7 and MD-09 (anchor, P7), final freeze manifest, main-run token method (Q8), MD-08/P8 if resume is wanted, coding preparation.

## 10. Confirmation
No live provider call, pilot, main run, credit use, token count by a provider, `.env` or credential access, human evidence, authorization file, or Git operation was made in this batch. The batch stops here.

---

# Addendum: final pre-pilot preparation batch (2026-10-13)

**Status after this batch: local pre-pilot preparation is exhausted for everything that does not need an owner/advisor decision, a human, or provider authorization. The research is NOT pilot-ready; the pilot gate is CLOSED.** Nothing below is an approval. Baseline recorded before the batch: relevant suites OK (SF2 detection OK with 4 expected failures, SF2 variants, SF matrix, ledger resilience, provider response, input limit); gate check exit 2; frozen hashes and official record unchanged since the previous batch (listed in A7).

## A1. What was actually done
1. Inventory of the actual status of MD-01..MD-10, C-31..C-33, P1..P10, H1..H7, L1..L6 from the files (no item was upgraded).
2. Owner/advisor package completed: `C31_C32_OWNER_DECISION_BRIEF.md` now also holds (section 13) the consequence of each option by failure class (SF1..SF5, PASS/FAIL-S, `f_S` tolerance, round-1 action route), (section 14) the inventory of definitions still needing approval (empty response, whitespace, no candidate, unknown status, non-JSON body, unlisted finish reason, timeout, transport exception, metadata error), and (section 15) the separation of character limit, assumed tokens, measured tokens, output cap, cost cap and observed cost with the evidence each needs. Recommendation B stays a RECOMMENDATION.
3. C-33: `PROPOSED_RECORD_CORRECTION_12_37.md` section 6 gives, for entries 12.37, 12.30 and 12.32, the old text, current facts, proposed replacement, reason, impact and approval needed. The record itself was not edited.
4. MD register extended with decision owner, dependencies, affected files, acceptance tests and the action after a decision (`MASTER_PROPOSED_DECISION_RECORD.md`, "Register details"). No status was changed.
5. New `HUMAN_TASKS_H1_H7_OPERATIONAL_CHECKLIST.md` (purpose, procedure, responsible person, inputs, evidence, acceptance, dependencies, expected location, actual status for H1..H7; all NOT DONE; no date, hash or sheet filled).
6. New `PROVIDER_VERIFICATION_MATRIX.md` (L1..L6: question, reason, minimal check, authorization, cost bound, evidence allowed, protection, PASS/FAIL/INCONCLUSIVE, impact if unverified; unknown API facts marked UNKNOWN; a connection-test tool is identified as missing and proposed as P11, not written).
7. Patches: none applied and none re-applied; reasons are in the register below. The four expected-failure tests in `test_sf2_detection.py` were kept.
8. Index, checklist, next actions and deferred-patch register updated for consistency.

## A2. Files changed in this batch and why
New: `HUMAN_TASKS_H1_H7_OPERATIONAL_CHECKLIST.md`, `PROVIDER_VERIFICATION_MATRIX.md` (Phases 3-4). Edited (all documents; backups `_backup/master_exec/*.before_final_prep`): `C31_C32_OWNER_DECISION_BRIEF.md` (sections 13-15), `PROPOSED_RECORD_CORRECTION_12_37.md` (section 6), `MASTER_PROPOSED_DECISION_RECORD.md` (register details), `MASTER_PILOT_READINESS_CHECKLIST.md` (pointers), `NEXT_ACTIONS.md`, `00_INDEX.md`, `deferred_patches/DEFERRED_PATCHES.md` (P11), this report. No code, test, scoring, adapter, template or gate file was changed in this batch. Rollback: copy a backup over the file; delete the two new files.

## A3. Tests and commands actually run (all mock/local; no network)
| Command | Exit | Result |
|---|---|---|
| `python -B -I -W error::ResourceWarning -m unittest discover -s research_design/step10 -p test_sf2_detection.py` | 0 | OK, 14 tests, 4 expected failures (the open C-31 conflict) |
| same, `test_sf2_variants.py` | 0 | OK, 11 tests |
| same, `test_sf_matrix_literal.py` | 0 | OK, 14 tests |
| same, `test_ledger_resilience.py` | 0 | OK, 11 tests |
| same, `test_provider_response.py` | 0 | OK, 16 tests |
| same, `test_input_limit.py` | 0 | OK, 10 tests |
| `python -B -I results_package_2026-10-13/reproduce/run_all_checks.py --quick` | 0 | "ALL CHECKS AS EXPECTED": 18 checks OK with exit 0, the slow Step 8 suite SKIPPED (unaffected), and the gate check returned exit 2 = CLOSED, which is the expected result (counted as OK by the script) |
| `python -B -I research_design/step8/s8_verify.py <build>` | 0 | OK |
| `python -B -I results_package_2026-10-13/reproduce/verify_stage_evidence.py` | 0 | OK |
| gate check without `--live` (template authorization, no evidence file) | 2 | GATE CLOSED, reasons printed: Step 9 evidence missing; authorization does not match the scope and call count; `max_input_characters` missing |
Expected failures and a closed gate are the intended outcome and are not test failures.

## A4. Decisions: evidence status
APPROVED with evidence: **none**. WORKING DECISION (applied in code, not an official entry, not approved by the advisor): MD-01 (hard flags, per-call decision vector), MD-02 (owner-stated character limit). PROPOSED / PENDING OWNER: MD-03..MD-10, the `f_S` unit and C-31 (recommendation B, not adopted), C-32 (Q7-Q9), C-33 (correction entry). Details and owners: register in `MASTER_PROPOSED_DECISION_RECORD.md`.

## A5. Status of P1..P11, H1..H7, L1..L6
| Item | Status |
|---|---|
| P1 / P3 | DONE as working decisions (ratification pending) |
| P1b / P2 / P3b | READY FOR OWNER APPROVAL (P2 names and P3b O2 also BLOCKED BY PROVIDER VERIFICATION) |
| P4 / P5 / P6 / P8 | DEFERRED (decisions; P4 touches frozen Step 7 files) |
| P7 | BLOCKED BY HUMAN TASK (H7) and DEFERRED |
| P9 | PARTLY DONE |
| P10 | DONE |
| P11 (connection-test tool, new) | DEFERRED / BLOCKED BY PROVIDER VERIFICATION authorization |
| H1-H7 | all NOT DONE (procedures in `HUMAN_TASKS_H1_H7_OPERATIONAL_CHECKLIST.md`) |
| L1-L6 | all NOT DONE and UNKNOWN (procedures in `PROVIDER_VERIFICATION_MATRIX.md`) |

## A6. Blockers
- **Methodological (owner/advisor):** C-31 Q1-Q6; `f_S` unit; C-32 Q7-Q9; MD-03 kappa; MD-04 FZ hash contract and file list; MD-05 (PG3, PG11b, SF/UNP policy, eligibility, PRD-5); MD-06 safe-stop; MD-07 timeout; MD-08 resume; MD-09 anchor; MD-10 confirmations; C-33 record correction.
- **Technical:** no connection-test tool (P11); no resume tool (P8); no FZ index tool (P5); no stop path for provider anomalies (P2); assumed-token gate absent (P3b).
- **Human:** H1-H7; the seven-day delay (H2) alone adds at least 7 days after the true last-viewing date, which has not been set.
- **Provider:** L1-L6, each needs separate written owner authorization.

## A7. Integrity check (hash and content, not only timestamps)
| Artifact | Check | Result |
|---|---|---|
| Spec v2.7 | sha256 | `d5fcffadd104...` = checklist value |
| Step 7 freeze manifest | sha256 | `202979de2a88...` = checklist value |
| Step 8 build manifest | sha256; `s8_verify.py` exit 0 | `09eed00eeb79...` = checklist value |
| FZ-v1 | sha256 | `149445715a82...` = checklist value |
| Official decision record | sha256 | `5a7ff7687850...`, same as at the start of the batch; 12.30, 12.32, 12.37 untouched |
| Stage 1/2 results | `verify_stage_evidence.py` exit 0 | OK |
| Registries, Step 7, Step 8, Step 8 output, `pilot_clarification` | files modified after 10:00 | 0 |
| Code | sha256 | `s10_scoring.py` `67b85b183fab`, `s11_pilot.py` `68fc807f85a7`, `s10_runner.py` `86954f14c790`, `s10_integrity.py` `17c1ec621b23`, `test_sf2_detection.py` `1419450cbc41`: unchanged in this batch |
| `.env` / credentials | existence | no `.env` in the repository root; none read or written |
| Git | operations | none (no commit, push, reset, stash) |

## A8. Pilot gate: CLOSED, exact reasons
(1) No Step 9 evidence file: the human blind check (H1, H2, H3) has not been done and no stop-viewing date has been set. (2) No valid owner authorization: only the empty template exists (H5), which also lacks `max_input_characters`. Separately, the readiness checklist requires adopted entries for M1-M11 and the unresolved provider verification before the pilot; tests passing opens no gate. The main-run gate is also CLOSED (needs a PASS pilot record, anchor, final freeze manifest, authorization for 2,496 calls).

## A9. Main action list (in dependency order)
| # | Who | What | Evidence required | Depends on | Done when | Allowed afterwards |
|---|---|---|---|---|---|---|
| 1 | Owner (+ advisor) | Answer Q1-Q6 (C-31) and Q7-Q9 (C-32); decide on the correction entry (C-33) | official record entries naming option, approver, date | none | entries exist | assistant rewrites the 4 marked tests from the ratified rule; implements P1b/P3b if chosen |
| 2 | Owner (+ advisor) | Decide MD-03, MD-04 (with file list), MD-05, MD-07, MD-10 | entries | 1 for MD-05 SF/UNP item | entries exist | P4/P5/P6 as chosen; Step 7 re-freeze if needed; FZ hash computed once before the first pilot call |
| 3 | Researcher | B1: write the true date/time of stopping viewing registry content | own dated note | PRD-5 decided (MD-05) before the evaluation is trusted | note exists, clock starts | H1 |
| 4 | Researcher | H1 blind check of 624 texts | filled worksheet, `evaluation.json`, worksheet hash | 3 | coverage 100 %, NO REJECT | H3 after H2 |
| 5 | Researcher | H2 wait at least 7 days from the true last-viewing date | calendar | 3, 4 started | difference >= 7 days | H3 |
| 6 | Researcher | H3 evidence file via the evaluator | `step9_evidence.json` | 4, 5 | gate reason 1 gone | gate check |
| 7 | Researcher | H4 codebook rehearsal | filled sheet, `comparison.json`, disagreement list | none | comparison produced | pilot (spec 13.5); codebook version if needed before the FZ hash |
| 8 | Owner (+ advisor) | MD-06 safe-stop; optionally authorize one connection test (L1-L5) in writing | entry; authorization file | none | adopted | P2 (and P11 + the test only if authorized) |
| 9 | Owner | H5 authorization (`authorized_by`, scope, 18 calls, ceiling 100, assumed tokens, `max_input_characters`) | saved file and hash | 1 (C-32) | gate reason 2 gone | gate check |
| 10 | Researcher / owner | H6 price and model re-read on the day of the paid call | dated note | 9 | note exists, prices consistent with FZ-v1 | pilot |
| 11 | Assistant (after 1-10) | Gate check without `--live`; must print "gates open" for the right reasons | command output | 2, 6, 7, 9, 10 | prints gates open | pilot round 1 only on the owner's explicit instruction |
| 12 | Owner | H7 declare the write-once store; MD-09 | record entry | before the decision script | entry exists | decision record anchor, P7 |
| 13 | Owner (+ advisor) | After the pilot: decision, final freeze manifest, main-run token method (Q8), MD-08 if resume is wanted | entries, manifest | pilot PASS | recorded | main run authorization |

## A10. Progress estimate (qualitative; no single percentage is given because the categories are not commensurable and the critical path is not engineering)
| Category | Counts | Reading |
|---|---|---|
| Local engineering that needs no decision | P1, P3, P10 done; P9 partial; reproducibility package: 18 checks OK plus the gate check closed as expected | exhausted: what remains is blocked, not undone |
| Local engineering that needs a decision | 7 patch items (P1b, P2, P3b, P4-P8) plus P11 | prepared (diffs/plans/acceptance criteria) but 0 applied |
| Owner/advisor decisions | 0 of 10 MD entries approved; 2 working decisions applied; 9 questions ready to answer | not started in the formal sense; the package is ready for them |
| Human tasks | 0 of 7 done; instructions ready | not started; contains an unavoidable >= 7-day wait |
| Provider verification | 0 of 6 done; procedures ready; one tool missing (P11) | not started; needs written authorization |
Weighting: the pilot opens only when every row of the checklist sections 1-3 has its evidence, so progress is limited by the slowest category, which is human tasks and owner decisions, not code. Preparation work (documents, tests, procedures) is substantially complete; gate-relevant evidence is 0 of the required items.

## A11. Confirmation
No live provider call, no pilot or main run, no credit use, no token count by a provider, no network call, no change to frozen artifacts, Stage 1/2 results, registries, the official record, `.env` or credentials, no invented human evidence, approval or timestamp, and no Git operation.

---

# Addendum B: execution of the researcher's direction (2026-10-13)

**Gate: CLOSED (unchanged). Not pilot-ready.** The researcher agreed with the recommended direction; effect: C-31 option B and the C-32 proposals became WORKING DECISIONS where they could be applied inside the existing authorization; every other entry has a recorded recommendation and a specific approval request. **No entry is APPROVED** (no official record entry, no advisor review). The per-entry reasoning, alternatives rejected, consequences and approval requests are in the "Direction record" of `MASTER_PROPOSED_DECISION_RECORD.md` (not repeated here).

## B1. Decisions MD-01..MD-10 (actual titles)
| Entry | Title | Recommended choice | Status | Unresolved approval |
|---|---|---|---|---|
| MD-01 | SF counting for the pilot decision (C-04, C-05, C-31) | hard flags -> FAIL-S; one decision count per call; `f_S` per call; option B (SF1/SF4 over SF2) with D1-D8 | WORKING DECISION (applied) | official entry; Q5 open (candidate vs no candidate) |
| MD-02 | OD-10 scope of the input-size basis (C-01, C-23, C-32) | 1,016-character preflight maximum (pre-filled in the template), refuse before any call, no truncation; assumption not measurement; C32-1 for the pilot; O4 first for the main run | WORKING DECISION (character limit) | official entry; Q8 main-run method |
| MD-03 | Kappa and the re-code procedure | K2 (kappa labelled intra-rater; K1 as fallback) | PENDING OWNER | K1/K2 and values; touches Step 7 freeze-set files |
| MD-04 | FZ hash contract | canonical index of the listed FZ files, once before the first pilot call | PENDING OWNER | adopt and supply the file list |
| MD-05 | PG3, PG11b, SF/UNP policy, coding eligibility, PRD-5 | all five as built | PENDING OWNER | one entry; PRD-5 before the blind check is evaluated |
| MD-06 | Provider response safe-stop policy | stop for review on clauses 1, 2, 4, 5; SF4 structural signals only | PENDING OWNER | adopt, accepting that an anomaly consumes a pilot round |
| MD-07 | Timeout meaning | keep per-socket-operation; no code | PENDING OWNER | record entry |
| MD-08 | Resume after a transport halt | adopt text; implement nothing for the pilot | PENDING OWNER | adopt; build P8 after a pilot PASS |
| MD-09 | Anchoring, authorization content, order of runs | owner's own commit of the decision record | PENDING OWNER | H7 declaration |
| MD-10 | Confirmations of earlier choices | confirm; advisor review of Step 8 choices (C-28) | PENDING OWNER | confirmation / advisor review |

## B2. Changes implemented and why each was authorized
| Change | Authorization basis |
|---|---|
| `test_sf2_detection.py` rewritten: 19 tests encode option B and D1-D7, including the real adapter path with patched `urlopen`; the four A1 expected-failure tests removed (backup `*.before_optionB`; A1/A2a analysis stays in `test_sf2_variants.py`) | the researcher's direction on C-31 (working decision); class B dependency resolved; no scoring logic changed |
| `s10_scoring.py` comment lines on `sf_flags` | comment only; AST verified identical to the backup |
| `templates/owner_authorization_TEMPLATE.json`: `max_input_characters` pre-filled with 1016, note rewritten | the researcher's direction on C-32; the template stays INVALID (`authorized_by` empty, `input_tokens_per_call_assumed` 0); gate output unchanged in kind |
| `reproduce/run_all_checks.py` label | wording only |
| Documents updated in place: decision record (status register rows, Direction record, MD-01 update), brief (status update), correction file (section 7 adoption draft, 12.38 wording), `DEFERRED_PATCHES.md` (classification A-F), index, conflict index, checklist, plan, `NEXT_ACTIONS.md` | consistency with the above; no new master report was created |
| Prepared INACTIVE, verified only in scratch copies (deleted afterwards): `P2_safe_stop.diff.INACTIVE` + `P2_test_safe_stop.py.INACTIVE` (7 tests pass; 5 old tests need updating on activation (3 fixtures without `model_returned`, 2 tests encoding the run-through policy; see `OWNER_APPROVAL_PACKAGE.md` Appendix B)), `P5_fz_index.py.INACTIVE` + `P5_test_fz_index.py.INACTIVE` (7 tests pass), A1 diff regenerated (applies cleanly in scratch) | "prepare small isolated patches, do not activate" |
Not implemented, with reason: P2, P3b, P4, P5, P6, P7, P8, P11 (class C/D/E/F in `DEFERRED_PATCHES.md`: they need an official decision, human evidence, provider authorization, or touch frozen files). Existing backups and scratch patches were kept.

## B3. Tests actually run (exit code, result)
| Command | Exit | Result |
|---|---|---|
| unittest discover `test_sf2_detection.py` | 0 | OK, 19 tests |
| `test_sf2_variants.py` | 0 | OK, 11 tests |
| `test_sf_matrix_literal.py` | 0 | OK, 14 tests |
| `test_ledger_resilience.py` | 0 | OK, 11 tests |
| `test_provider_response.py` | 0 | OK, 16 tests |
| `test_input_limit.py` | 0 | OK, 10 tests |
| `test_step10.py` (also inside the quick suite) | 0 | OK |
| `run_all_checks.py --quick` | 0 | "ALL CHECKS AS EXPECTED": 19 lines OK (18 checks plus the gate check, which returned exit 2 = CLOSED as expected); slow Step 8 suite SKIPPED |
| `s8_verify.py` / `verify_stage_evidence.py` | 0 / 0 | OK |
| gate check without `--live` (template authorization) | 2 | GATE CLOSED: Step 9 evidence missing; authorization does not match the scope and call count |
| scratch only: P2 tests, P5 tests, A1 and P2 diffs applied with `patch --binary` | n/a | 7/7, 7/7, clean |

## B4. Hashes before/after (sha256 prefix)
Unchanged: spec v2.7 `d5fcffadd104`, Step 7 freeze manifest `202979de2a88`, Step 8 build manifest `09eed00eeb79`, FZ-v1 `149445715a82`, official decision record `5a7ff7687850`, `s11_pilot.py` `68fc807f85a7`, `s10_runner.py` `86954f14c790`, `s10_integrity.py` `17c1ec621b23`. No file under registries, Step 7, Step 8, Step 8 output or `pilot_clarification` changed (0 modified since 10:00); no `.env` exists. Changed as intended: `s10_scoring.py` `67b85b183fab` -> `8c0e6b9fecb5` (comments only), `test_sf2_detection.py` `1419450cbc41` -> `691597f95ec2`, authorization template `7ea941f62fb3` -> `9a17d5c575b7`. No discrepancy.

## B5. Remaining items and exact next action
| Item | Next action | Prerequisite |
|---|---|---|
| Official entries | owner signs one combined entry: draft 12.39 (MD-01, MD-02) and the other MD decisions; optionally appends the 12.38 status note (C-33) | none; advisor where an entry says so |
| MD-03/04/05/06/07/08/09/10 | owner answers the approval request in the Direction record | MD-04 needs the file list; MD-06 consequence accepted |
| H1-H3 blind check and 7-day delay | researcher states the true stop-viewing date/time and starts H1 | PRD-5 (MD-05) adopted before the evaluation is trusted |
| H4 rehearsal | researcher codes 40 rows and runs the comparator | none |
| H5 authorization | owner writes `authorized_by`, assumed tokens, confirms 1016, saves as a new file | MD-02 entry |
| H6 price re-read | on the day of the first paid call | H5 |
| H7 write-once store | owner declares it | MD-09 (needed before the decision script, not the pilot) |
| L1-L6 provider verification | optional; owner authorizes in writing; P11 tool must be written first | none for the pilot; MD-06 is the protection |

## B6. Pilot gate
CLOSED. Factual reasons: no Step 9 evidence file (blind check H1-H3 not done; no stop-viewing date exists, so the 7-day clock has not started); no valid owner authorization (the template is not an authorization). Decisions not yet formally recorded are additional checklist prerequisites.

## B7. Shortest valid critical path to the next authorized milestone (a pilot round 1 that the gate would allow)
Elapsed time is driven by the 7-day delay; everything else fits inside it if done in parallel. (1) Researcher writes the true time at which they stop viewing registry content; this starts the clock and cannot be set in advance. (2) Same day, owner signs the official entries (MD-05 PRD-5 first; then MD-01/02/04/06/03/07/10) and supplies the FZ file list; assistant activates P5 (and P2 if MD-06 is adopted, updating its 5 tests) and computes the FZ hash once. (3) Researcher does H4 at any time and H1 (the guide requires only that the COMPLETION date is at least 7 days after the last viewing; finishing late is recommended; no registry content may be viewed in between). (4) On or after day 7 from the true last viewing: H3 evidence file. (5) Owner writes H5; H6 on the day. (6) Gate check without `--live` must print "gates open"; only then may the owner instruct a pilot. No step can be shortened by assumption.

## B8. Not safely resolved
Q5 (distinguishing "no candidate" from "candidate without text and without finishReason": needs an adapter change and the live shape, unknown); block names and returned-model-ID form (live facts); the main-run token measurement (O4 needs pilot data; O2 needs spending authorization); the file list for the FZ index (owner); whether the advisor accepts the working decisions; the 5 existing tests that P2 would flip (3 fixtures, 2 policy tests; decision on MD-06 and question B-1 first).

## B9. Confirmation
No live provider call, pilot, main run, credit use, token count by a provider, network call, change to frozen artifacts or the official record, `.env`/credentials access, invented evidence/approval/timestamp, or Git operation.

---

# Addendum C: owner package and human-task start (2026-10-13, directive "shortest safe path")
Nothing was approved, signed, computed or activated. Added: `OWNER_APPROVAL_PACKAGE.md` (the consolidated approve/reject form for MD-01..MD-10 in critical-path order, with Appendix A: FZ index request and file-list options L-A/L-B/L-C, the open question whether `s10_scoring.py` and `s10_analysis.py` belong to the FZ set, and Appendix B: MD-06/P2 explanation, the exact five legacy tests, question B-1 on a stopped round, acceptance criteria); `HUMAN_TASKS_H1_H7_OPERATIONAL_CHECKLIST.md` "START HERE" (R1-R4, O1-O5, H6, independent vs chained, evidence folders; R1 is the only start of the 7-day clock and only the researcher can create it); brief sections 16 (Q5 contract) and 17 (O4-after-pilot path); matrix cross-links. Correction of an earlier statement: the five legacy tests affected by P2 are 3 fixtures without `model_returned` plus 2 tests that encode the run-through policy (not "4 fixtures plus 1"). Status of the 7-day clock: NOT STARTED (no `last_registry_view_utc.txt` exists). Pilot gate: CLOSED (rerun output below in section C1).

## C1. Verification of this directive (actual output)
No code or test file changed, so no suite was re-run except the inactive P5 tests in a scratch copy (7 tests, OK, scratch deleted). Protected and code hashes are identical to the end of the previous batch (spec `d5fcffadd104`, Step 7 manifest `202979de2a88`, Step 8 manifest `09eed00eeb79`, FZ-v1 `149445715a82`, official record `5a7ff7687850`, `s10_scoring.py` `8c0e6b9fecb5`, `s11_pilot.py` `68fc807f85a7`, `s10_runner.py` `86954f14c790`, `s10_integrity.py` `17c1ec621b23`, `test_sf2_detection.py` `691597f95ec2`, template `9a17d5c575b7`); `s8_verify.py` exit 0; `verify_stage_evidence.py` exit 0; 0 files modified after 10:00 under registries, Step 7, Step 8, Step 8 output, pilot_clarification; no `.env`; `human_evidence/` does not exist (the researcher creates it). Hashes of the inactive artifacts, to prove at activation that the file equals the verified draft: `P1b...diff.INACTIVE` `394201ea0b25`, `P2_safe_stop.diff.INACTIVE` `d8f351ef7d19`, `P2_test_safe_stop.py.INACTIVE` `aec106ab8f8d`, `P5_fz_index.py.INACTIVE` `816978c0df0a`, `P5_test_fz_index.py.INACTIVE` `13eebf277266`. Non-live gate check output (exit 2): "GATE CLOSED: Step 9 evidence file missing (human blind check not documented); authorization does not match the scope and the planned number of calls".

---

# Addendum D: independent preparation and owner package v2 (2026-10-13, directive "next stage")
No approval, R1 timestamp or authorization exists, so Phases 3-5 (activation, the seven-day tracking, readiness validation) were not executed. Done: (1) kits checked read-only: the blank H1 worksheet has 624 rows, 0 filled cells, ids equal to the `checker_bundle` file names (directory listing only), sha256 `3f85ff147f96`; the blank H4 sheet has 40 rows, 0 coding cells, sha256 `19db7b40ac23`; (2) new `reproduce/precheck_human_sheets.py` (+ 12 synthetic tests): a format-only pre-check that opens only the researcher's sheet and the blank kit, never the bundle, mapping, registry or expected codes, and prints ids and column names only; (3) `OWNER_APPROVAL_PACKAGE.md` now starts with a Quick sign sheet, shows exact answers for MD-04 and B-1, maps each approval to the patch it authorizes (P5, official FZ computation, E-1 gate enforcement, P2, Q5, P3b, P4/R-7, P7, P8, P11, new P12 for the O4 reader), and has copy-paste, existence-verified lists L-A (4), L-B (19), L-C (21) with a comparison; (4) **correction:** the earlier recommendation of L-C is replaced by L-B, because spec 13.6 protects executable code by H1-H4 (a pure fix creates no new FZ version) and a list that binds `s10_scoring.py`/`s10_analysis.py` would need a supplement rule; (5) B-1 is presented as options (a) counts as a round, (b) void and re-run, (c) MD-06 not adopted, with the verified facts (spec 13.6 cap and lineage; no round counter in the runner; incomplete runs are refused by `s11_pilot`) and the record to write, and no option is chosen; (6) brief section 18 reviews Q5/O4 completeness (new approval slots Q5 and P12); (7) START HERE wording on H1 timing no longer recommends delay for convenience: completion cannot be earlier than R1 + 7 days, starting is allowed once R1 exists, independence is the researcher's and the advisor's judgment.
Verification actually run: `precheck` tests 12/12 OK; `run_all_checks.py --quick` exit 0, 20 OK lines (19 checks plus the expected CLOSED gate), Step 8 slow suite SKIPPED; `s8_verify.py` exit 0; `verify_stage_evidence.py` exit 0; protected and code hashes identical to the previous batch; 0 modified files under registries, Step 7/8, `pilot_clarification`; no `.env`; `human_evidence/` does not exist; gate exit 2: "GATE CLOSED: Step 9 evidence file missing (human blind check not documented); authorization does not match the scope and the planned number of calls". Nothing approved, nothing activated, no live call.

---

# Addendum E: final owner handoff and consistency pass (2026-10-13)
**Gate CLOSED; nothing approved, activated, computed or created by automation.** Final consistency pass of `OWNER_APPROVAL_PACKAGE.md` against the decision register, the spec and the code. **Real discrepancies found and fixed:** (1) MD-06 stated as a fact that one anomaly consumes a pilot round, while B-1 is an open choice: now stated as dependent on B-1 (a)/(b)/(c); (2) MD-04 said the FZ hash is "enforced by the gates" although enforcement needs its own box: now box E-1; (3) the dependency note said Q5/MD-01 touch listed files, true only for L-C: now precise per list; (4) **MD-03 K2 timing (new, verified in the code):** `s7_recode.py` and the codebook are hashed by the Step 8 build manifest, and the Step 9 evidence names that manifest's SHA-256 (gate, `s10_runner.py` line 139); K2 therefore must be decided BEFORE the evidence file H3 is created (also for a PG11b narrowing under MD-05); the critical path, the MD-03/MD-05 blocks, the decision record and START HERE R4 now say so; (5) MD-07..MD-10 lacked explicit consequences: added; (6) boxes E-1, Q5, Q9, R-7, P7, P11, P12 are now referenced individually in the blocks that need them; (7) the H1 worksheet column `family_read_from_text` was undocumented (optional, read by nothing) and the H4 stance code is `MPG`, not the spec's `MX`: documented in `HUMAN_TASK_GUIDE.md`. L-B is stated as a RECOMMENDATION, L-C needs the explicit supplement rule (draft wording in Appendix A). The package now has a Response guide (what the owner must return: decisions with conditions, FZ list + A-2, B-1, the individual boxes, the H5 authorization fields, provider-related permissions that the gate does not read, and what stops if something is rejected or conditioned; silence is not consent).
**Patch activation and rollback procedures** (prerequisite, steps, tests, rollback/recovery, recorded hashes of the inactive artefacts and of the base files) were added for P5, E-1, P2, Q5, P3b, P4, P7, P8, P11, P12 and the A1 diff at the end of `deferred_patches/DEFERRED_PATCHES.md`; all stay inactive.
**Verification actually run:** `test_precheck_human_sheets.py` 12/12 OK; the blank H1 sheet reports `rows: 624; not filled: 624; problems: 0` (exit 1) and the blank H4 sheet `rows: 40; not filled: 40; problems: 0` (exit 1), the expected states; the pre-check imports only `argparse, csv, os, re, sys` and the spy test shows it opens only the researcher's sheet and the blank kit (never the bundle, mapping, registry, prompts, gate report or the answer key); no Python file writes `human_evidence/` or an R1 file, and `human_evidence/` does not exist; `s8_verify.py` exit 0; `verify_stage_evidence.py` exit 0; protected and code hashes identical to the previous batch; the five inactive artefacts keep their recorded hashes; 0 files modified under registries, Step 7/8, Step 8 output and `pilot_clarification`; no `.env`. No suite was re-run beyond these because no code or test changed. Non-live gate output (exit 2): "GATE CLOSED: Step 9 evidence file missing (human blind check not documented); authorization does not match the scope and the planned number of calls".

---

# Addendum F: H3 dependency chain and decision closure matrix (2026-10-13)
No approval, R1 timestamp or authorization arrived; therefore nothing was activated, rebuilt or modified in any frozen artifact. Documents only. **Chain verified in the code and manifests:** H3 names `build_manifest_sha256` (gate, `s10_runner.py` line 139); the Step 8 manifest binds the spec hash, the FZ-v1 register canonical hash, the Step 7 manifest hash, 15 generator-code files and 2,026 published files; `step9/*`, `step10/*`, the template and the official record are not bound (the Step 7 manifest names the record only by path and entry numbers). The 15 generator-code hashes in the manifest equal the current files (no drift; `s8_verify.py` exit 0). **Decisions that can invalidate H3 (documented, placed before H3 in the critical path):** MD-03 K2; a codebook revision after the H4 findings (new: H4 and the advisor's decision on its disagreements precede H3); MD-05 PG11b narrowing, SF/UNP Policy 1/2/parse-first; MD-10 amendment of a Step 8 choice or I-6 as a gate; MD-07 only if a register value changes; any decision implemented as an edit of the spec or the FZ-v1 register instead of a record entry; PRD-5 must be settled before the first evaluation run. **MD-05 PG3 strict** would rebuild the registry and void H1 itself, so it precedes the START of H1. MD-01, MD-02, MD-04, MD-06, MD-08, MD-09, E-1, Q5, Q9, P7, P11, P12 cannot change H3. The authorized rebuild/reverification sequence and the hashes to record (old Step 7 manifest `202979de2a88`, Step 8 manifest `09eed00eeb79`, `s7_recode.py` `ec8f948e6209`, codebook `25a74353be54`, `s7_bundle.py` `10567178b209`, spec `d5fcffadd104`, register `c7d50e115b08`, and the 2,026-file inventory comparison) are in `OWNER_APPROVAL_PACKAGE.md` ("What is bound into H3"); a rebuild needs a new `--out` folder because the build folder is named by the registry hash and the tool refuses an existing target. The package now also has the 20-row **closure matrix** (status, exact decision, files, dependencies, patch authorized, verification, and which of H1/H3/FZ/H5 the item must precede; nothing needs to precede R1). `START HERE` R3 and R4, the decision register and the P4 procedure were aligned.
**Verification actually run (no code or test changed, so no suite was re-run):** protected and code hashes identical to the previous batch; generator-code drift check `[]`; `s8_verify.py` exit 0; `verify_stage_evidence.py` exit 0; 0 modified files under registries, Step 7/8, Step 8 output, `pilot_clarification`; no `.env`; `human_evidence/` absent (no R1); the five inactive artefacts keep their recorded hashes; non-live gate output (exit 2): "GATE CLOSED: Step 9 evidence file missing (human blind check not documented); authorization does not match the scope and the planned number of calls".

---

# Addendum G: H4 support and the H1/H3-blocking decision log (2026-10-13)
**Concrete progress is documentation only; no human result, owner decision or R1 exists.** H4 status: NOT DONE (no `human_evidence/` folder, no filled sheet, no comparison, no findings). Owner decisions received: **none** (the blocking-decision log in `OWNER_APPROVAL_PACKAGE.md` is blank). Rebuild: **not required and not authorized today**; it becomes necessary only for the non-default answers (K2, strict PG3, narrowed PG11b, another SF/UNP policy, an amended Step 8 choice or I-6 as a gate, a codebook revision from H4, a changed register value). Added: (1) in `HUMAN_TASKS_H1_H7_OPERATIONAL_CHECKLIST.md`, "H4 step by step": exact PowerShell commands, the expected output of the pre-check on the blank copy (`rows: 40; not filled: 40; problems: 0`, `NOT FILLED (first 5 ids): ...`, `FORMAT PRE-CHECK: NOT COMPLETE`, exit 1) and on a complete sheet (`rows: 40; not filled: 0; problems: 0`, `FORMAT PRE-CHECK OK ...`, exit 0), the blank sheet's sha256, the one-time comparison and the shape of its output, and a findings protocol (class A slip / B codebook ambiguity / C battery question) with a blank template and a stop rule before H3; verified by running the pre-check on an unedited copy of the blank (identical hash, identical output) and on a synthetic complete copy that was deleted afterwards (not a human result); the comparator was NOT run because it opens the expected codes; (2) in `OWNER_APPROVAL_PACKAGE.md`, "Blocking decisions for H1/H3": eight exact questions (PRD-5, MD-03 K1/K2, PG3, PG11b, SF/UNP and parse-first, MD-10, H4 findings, MD-07), default answer versus non-default, whether a rebuild follows, and blank columns for choice, approver, date and conditions, plus a neutral K1/K2 cost comparison. If H4 shows a discrepancy of class B or C the researcher stops before H3 and the owner/advisor decide; nobody edits the codebook or any manifest-bound file in the meantime.
Verification actually run (no code or test changed): protected and code hashes identical to the previous batch; `s8_verify.py` exit 0; `verify_stage_evidence.py` exit 0; `test_precheck_human_sheets.py` 12/12 OK; the blank H1 and H4 sheets keep `3f85ff147f96` and `19db7b40ac23`; 0 modified files under registries, Step 7/8, Step 8 output, `pilot_clarification`; no `.env`; non-live gate exit 2: "GATE CLOSED: Step 9 evidence file missing (human blind check not documented); authorization does not match the scope and the planned number of calls". Next valid action: the researcher starts H4 (steps 1-2 take a minute) and records R1 when they truly stop viewing registry contents; the owner returns the blocking-decision log.
