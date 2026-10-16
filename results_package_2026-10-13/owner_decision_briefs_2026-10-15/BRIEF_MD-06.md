# MD-06: Provider response safe-stop policy (with B-1)

**Status: PENDING OWNER DECISION: BLOCKED — SOURCE TEXT REQUIRED (partial: see section 9).** Prepared 2026-10-15T03:30:47Z. The owner makes this decision; nothing here is adopted. Dependencies: none beyond those named below.

## 1. Why a decision is needed
No stop path exists in the runner for anomalies of a real response (model ID, finish reasons, missing status).

## 2-3. Authoritative sources and verbatim quotations
Quotations are exact text from the files and lines named (excerpts are marked). Interpretation is confined to sections 5-8.

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 59-59**

> | 13 | MD-06 + B-1 | PENDING | adopt the safe-stop and choose (a)/(b)/(c) | `s10_runner.py`, `s10_integrity.py`, 5 legacy tests | none | P2 | P2 suites, `--quick` | - | - | - | x |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 102-102**

> | MD-06 / B-1 (c) | P2 | anomalies are only counted and reported; no round question |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 141-145**

> ## MD-06 Provider response safe-stop policy (C-12..C-15) — formal approval needed (details in Appendix B)
> - **Decision/recommendation:** after the record is stored, stop for owner review on: (1) returned model ID missing or not exactly the requested ID; (2) finish reason not STOP, not token limit, not a documented block name; (4) record without HTTP status and without error marker; (5) error marker or non-2xx remains SF1. SF4 only for structural signals (no candidate; a block-reason field); block NAMES only after an authorized observation. Owner + advisor.
> - **Consequence you must accept:** a stop ends the run as RUN_INCOMPLETE with no PASS/FAIL-S outcome, and `s11_pilot` refuses it; what that means for round accounting and the lineage depends on your answer to **B-1** ((a) it counts as a round, (b) it is void and re-run under the identical FZ, (c) MD-06 is not adopted); the options and their consequences are in Appendix B and the assistant does not choose. **Alternatives rejected:** record only (today); automatic SF classification of new names (protocol change).
> - **Affects:** `s10_runner.py`, `s10_integrity.py`, 5 legacy tests; inactive P2 diff + 7 tests. **Prerequisite:** your answer to B-1.
> - `[ ] APPROVE  [ ] REJECT  [ ] AMEND: ______  | B-1 answered: [ ] (a)  [ ] (b)  [ ] (c)  [ ] other: ______  | Owner: ______  | Advisor: ______  | Date: ______`

**`results_package_2026-10-13/MASTER_PROPOSED_DECISION_RECORD.md` lines 157-164**

> ### MD-06 Provider response safe-stop policy (C-12, C-13, C-14, C-15)
> - **Class:** record entry (a stop is not a classification); automatic SF classification of new names would be PROTOCOL.
> - **Rule quoted:** FZ-v1 row 17 (returned model ID "recorded for every call"); spec §13.4 SF1, SF3, SF4; record 12.36.
> - **Proposed text:** "(1) A response whose returned model ID is missing or not exactly the requested ID is recorded and stops the workflow for owner review before the next call. (2) A finish reason that is not STOP and not the token limit and not a documented block signal stops the workflow for owner review; the response is kept as recorded and not replaced. (3) SF4 is assigned only to: no candidate returned; a prompt block reason; and finish reasons ______ [names, each with its source after the first live observation]. (4) A record without an HTTP status stops the workflow for owner review. (5) An error marker or an HTTP status outside 2xx is SF1 even if text is present. A stop leaves the run marked INCOMPLETE with the reason."
> - **Impact:** needs a stop path in the runner (none today); retries stay 0.
> - **Acceptance:** mock tests for every clause; no stop case is scored as a valid response.
>
> - **Owner decision: PENDING | Advisor decision: PENDING | Date: PENDING | Option chosen: PENDING**

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 227-236**

> ## Appendix B. MD-06 / P2 explained
> - **Exact behaviour change.** After each call the record, the raw file and the ledger `raw`/`classified` entries are written as today. Then the runner checks the stored record: status absent and no error marker; returned model ID missing or different from `gemini-3.5-flash-lite` (for a 2xx record); finish reason not in the known sets. On a hit it stops, writes `RUN_INCOMPLETE` with the reason, makes no further call. Records with an error marker or a non-2xx status are not anomalies (they are SF1 and the run continues). Classification and scoring are unchanged.
> - **Legacy tests affected (5, exact reason).** Three are fixtures that return a 200 response without `model_returned`: `test_step10.TestRunner.test_pilot_records_failures_without_retry` (call 2), `test_pilot_flow.TestPilotGlue.test_round_one_fail_s_is_not_final`, `test_pilot_flow.TestPilotGlue.test_round_two_fail_s_stops_and_fail_u_is_stop_u`; the fix is giving those mock responses the requested model ID (the draft already changes the shared `good()` fixture). Two encode the opposite policy on purpose and must be rewritten to the adopted rule: `test_provider_response.TestRunLevel.test_returned_model_difference_does_not_stop_or_reclassify` and `test_mixed_responses_run_keeps_ledger_hashes_retries_and_marks_failures` (it feeds a different model ID and an unlisted finish reason and expects the run to continue).
> - **B-1 What happens to a pilot round after a safe-stop anomaly (the assistant does not choose).**
>   - *Facts.* Spec 13.6: "at most 2 pilot rounds in total for the whole main experiment"; round 2 is the follow-up of a round-1 FAIL-S with one whitelisted change (new FZ version); the lineage records every pilot round ever run; the spec says nothing about a round that stops without an outcome. Tooling: `pilot_round_1`/`pilot_round_2` are only scope labels in the authorization; the runner keeps NO round counter and refuses only an existing output folder; a preflight failure creates nothing and consumes nothing; a stopped run leaves its folder with `RUN_INCOMPLETE`, a `halt` reason, the ledger and raw files intact; `s11_pilot report/decide` refuse an incomplete run (exit 2, nothing written), so no outcome, PASS or FAIL-S, exists for it.
>   - *Option (a), the stopped run counts as a pilot round.* Consequence: it has no outcome, so the spec defines no next action; a follow-up round needs your (and the advisor's) rule, because round 2 is defined only after FAIL-S. Record: a disposition entry "pilot attempt of scope S, folder F, ledger final hash H, recorded calls N, halt reason R: counted as round __; next step: ______".
>   - *Option (b), the stopped run is declared void (not a round).* Consequence: after the cause is understood the same scope is run again under the identical FZ (a new authorization and a new output folder; no code change is needed to do so); this effectively raises the number of attempts above the cap of 2 unless the advisor accepts that a void run is not a round; if fixing the cause changes executable code it must satisfy H1-H4, otherwise it is a new FZ version that counts toward the cap. Record: the same disposition entry with "void" and the advisor's acceptance; the folder is kept and listed in the lineage.
>   - *Option (c), MD-06 is not adopted (record and report only, as today).* Consequence: no stop, no round question; anomalies are counted and reported (`provider_checks`) and the pilot decision proceeds on counts; a returned-model or finish-reason problem would be seen only after the round.
>   - *In every option* the stopped folder is never deleted or edited, and the owner writes the disposition in the official record before any further run. Sentence templates: "B-1 = (a): a safe-stop run counts as a pilot round; next step: ______." / "B-1 = (b): a safe-stop run is void; the advisor accepted on ______; the folder is kept in the lineage." / "B-1 = (c): MD-06 is not adopted."
> - **Acceptance criteria before activation:** MD-06 and B-1 recorded; the 5 tests rewritten to the adopted policy (not weakened); the 7 new tests pass; single-flag outcomes unchanged; block-name lists unchanged until L3; `run_all_checks.py --quick` OK; gate still CLOSED; mock-only.

**`results_package_2026-10-13/deferred_patches/DEFERRED_PATCHES.md` lines 28-33**

> ## P2 Provider safe-stop (MD-06; C-12..C-15)
> - **Source.** FZ-v1 row 17 (returned model ID recorded for every call); spec 805-816 (silent on unlisted reasons), 809 (SF1); record 12.36 (line 793); MPR section 3 Q-P1..Q-P4.
> - **Current behaviour (pinned by `test_provider_response.py`, unchanged):** a returned-model difference, an unlisted finish reason and a record without HTTP status are recorded and reported by `s10_integrity`/`pilot_counts`; the run does NOT stop. `BLOCK_REASONS` (eight names) comes from memory of the public API and is UNVERIFIED (MPR Q-P3); it was not extended.
> - **Design for after adoption.** Add `StopForReview` in `s10_runner.run`: after the call record, raw file and ledger `raw` entry are written (raw before the stop), evaluate (1) returned model missing or not exactly the requested ID, (2) finish reason not STOP, not token-limit, not a documented block name, (3) record without HTTP status; on a hit write `RUN_INCOMPLETE` with `halt = "provider anomaly: <reason class>"`, make no further call, keep the chain valid. `classify` unchanged; SF4 names changed only by the owner after a live observation. `s10_integrity` gets a `halt_reason` check.
> - **Acceptance (mock):** each of the three triggers stops after recording; raw exists; hash chain valid; provider call count equals the index of the trigger; retries 0; no stopped run scored as valid; a normal run unchanged; block names list per MD-06.
> - **Blocked by:** MD-06 adoption; the name list needs L1-L3 (live verification, D).

**`results_package_2026-10-13/ADVISOR_DECISION_BRIEF.md` lines 63-70**

> ## D8. Provider-response handling  (before pilot; none can be settled by a test)
> - **Reference:** FZ-v1 row 17 ("returned model ID recorded for every call"); §13.4 (SF3, SF4); `PROVIDER_RESPONSE_VALIDATION_REPORT.md`; 12.36; `step10/s10_scoring.py`.
> - **Problem:** the protocol records the returned model ID but gives no consequence; it is silent on unlisted finish reasons; it does not list which provider names mean "blocked"; it does not say how to treat a record without HTTP status.
> - **Q-P1 (returned model differs):** (a) record only (current); (b) flag to the owner in the pilot report; (c) stop. Recommendation: (b), (c) only with a written rule.
> - **Q-P2 (unlisted finish reason):** (a) parse decides, reported (current); (b) structural failure; (c) owner reviews the printed counts before the decision. Recommendation: (c).
> - **Q-P3 (names counted as blocked):** current list SAFETY, BLOCKLIST, PROHIBITED_CONTENT, SPII, IMAGE_SAFETY (protocol-like) plus RECITATION, OTHER, LANGUAGE (implementation choice). Options: keep, or restrict to the first five. Recommendation: keep until the first live observation shows which names occur.
> - **Q-P4 (no HTTP status, no error):** (a) not classified, reported (current); (b) SF1. Recommendation: (b) once the live adapter is known to always set the status.
> - **Decision (advisor/owner):** ________________  **Date:** ________


## 4. Original options (labels and order as in the sources)
Options B-1 (a), (b), (c) with the sentence template of Appendix B; Q-P1..Q-P4 options in ADV D8.

## 5. Consequences
- Source-defined: OAP: if (c): 'anomalies are only counted and reported; no round question'.
- Reasoned: P2 rewrites 5 legacy tests and changes `s10_runner.py`/`s10_integrity.py`.

## 6. Recommendation: NOT ADOPTED
Source recommendation (NOT ADOPTED): ADV D8 recommendations per question (quoted).

## 7. Record cross-check
Decision record cross-check: no mention of `MD-06`, `safe-stop` in the record.

## 8. Dependencies
See the dependencies named in the header of this brief; no further source-backed content.

## 9. Information still missing
- Finish-reason / block names for SF4 'each with its source after the first live observation' (MPDR text): BLOCKED — SOURCE TEXT REQUIRED.

## 10. Owner response (unfilled)
- [ ] B-1 = (a)
- [ ] B-1 = (b)
- [ ] B-1 = (c)
- [ ] Q-P1..Q-P4 as: ______
- [ ] REJECT / AMEND: ______
- Owner: ______    Date: ______    Conditions: ______

## 11. Recording instruction
Do not record any outcome until the owner explicitly adopts it. The recording is a new entry in the owner decision record written under the owner's authority; this brief and its recommendation are not an entry and not a decision.
