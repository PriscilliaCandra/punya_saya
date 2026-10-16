# MD-01: SF counting for the pilot decision and the unit of f_S

**Status: PENDING OWNER DECISION: READY FOR OWNER.** Prepared 2026-10-15T03:30:47Z. The owner makes this decision; nothing here is adopted. Dependencies: none beyond those named below.

## 1. Why a decision is needed
A WORKING DECISION (option B, D1-D8, per-call unit) is in force in the code; a formal owner entry is still needed.

## 2-3. Authoritative sources and verbatim quotations
Quotations are exact text from the files and lines named (excerpts are marked). Interpretation is confined to sections 5-8.

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 55-55**

> | 9 | MD-01 (+ unit of `f_S`) | WORKING DECISION | adopt option B + D1-D8 + per-call unit | `s10_scoring.py`, tests (none bound in H3) | none | none (A1 diff only if A1) | `test_sf2_*`, `test_sf_matrix_literal` (already run) | - | - | x | x |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 97-97**

> | MD-01 | the counting/SF2 rule in force | the working decision must be replaced by your choice (A1/A2a diff or another rule) and the tests rewritten; the FZ hash waits |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 122-127**

> ## MD-01 SF counting for the pilot decision (C-04, C-05, C-31) — WORKING DECISION, formal entry needed
> - **Decision/recommendation:** keep all flags; a call meeting SF2, SF3 or SF5 is one hard count; any other call meeting SF1 or SF4 is one soft call; `f_S` counts calls; **option B**: SF1/SF4 take precedence over SF2 (an empty body explained by an HTTP/transport error or by a block/no candidate is not also SF2); definitions D1-D8 (brief section 6.1); no new outcome label. Owner + advisor.
> - **Consequences:** a 503/timeout/block with empty body is soft (tolerated up to `f_S` = 1); an empty body of a received non-error response stays SF2 (FAIL-S); hard flags are never hidden. **Alternatives rejected:** A1 (voids the `f_S` tolerance for adapter records, re-routes the round-1 action to the SF2 remedy), A2a (every empty block hard), A2b (hole for status-less records), per-flag `f_S` (protocol change).
> - **Affects:** spec §13.4 (810), §13.6 (830-831, 838); `s10_scoring.py`, `s11_pilot.py`, `test_sf2_detection.py` (19), `test_sf_matrix_literal.py` (14), `test_sf2_variants.py` (11). **Prerequisite:** none.
> - **Unresolved:** Q5 (candidate without text and finish reason vs no candidate; brief section 16) is NOT decided by this approval; it has its own box **Q5** in the Quick sign sheet; live provider behaviour is unknown.
> - `[ ] APPROVE  [ ] REJECT  [ ] AMEND: ______  | Owner: ______  | Advisor: ______  | Date: ______`

**`results_package_2026-10-13/MASTER_PROPOSED_DECISION_RECORD.md` lines 96-114**

> ### MD-01 SF counting for the pilot decision (C-04, C-05)
> - **Class:** record entry (counting convention) + code after adoption; no protocol change.
> - **Rule quoted:** spec §13.6: PASS needs "no SF2, no SF3, no SF5; SF1 + SF4 <= f_S"; FAIL-S is "any SF2, SF3, SF5, or SF1 + SF4 > f_S". Record 12.18 row 1: SF and UNP counts disjoint.
> - **STATUS OF THIS TEXT (read first):** WORKING TECHNICAL DECISION directed by the project owner on 2026-10-13 for P1/P3 preparation. It is NOT an approval by the advisor and NOT an institutional/formal owner approval: the approval block below stays PENDING and no verifiable approval evidence exists. Code patch P1 implements it under that label; if the owner/advisor reject or amend it, P1 is reverted from `_backup/p1_p3/` (or amended) and nothing downstream may rely on it.
> - **Proposed text (working decision, items 1-7 as directed):** (1) "All SF flags met by a call are retained in the data and in every report. (2) The primary classification is for recording only; it never hides another flag that determines the pilot outcome. (3) A call that meets the protocol definition of SF2, SF3 or SF5 contributes to FAIL-S even if it also meets SF1 or SF4. (4) `f_S` is compared with the number of CALLS that meet the soft-failure definition (SF1 or SF4); several soft flags on one call do not count that call more than once. (5) SF1 + SF4 on one call is one soft-failure call. (6) No flag definition, threshold or denominator is changed. (7) If a reading conflicts with the explicit text of the protocol, the affected implementation stops and the conflict is recorded for ratification." The number of multi-flag calls is reported. The recording primary order (provisional SF1 > SF4 > SF3 > SF2 > SF5, unchanged) has no role in the outcome.
> - **Source check (against `SCENARIO_CONSTRUCTION_SPECIFICATION_v2_7_DRAFT.md`):** §13.4 lines 805-813 (definitions SF1-SF5); §13.6 lines 828-834: PASS = "no SF2, no SF3, no SF5; `SF1 + SF4 ≤ f_S`; UNP share `≤ θ_unp`", FAIL-S = "any SF2, SF3, SF5, or `SF1 + SF4 > f_S`" -> item 3 follows the literal text ("any SF2, SF3, SF5"); §13.7 line 869 (counts only); record 12.18 row 1 (SF and UNP counts disjoint; unchanged). Items 1, 2, 4, 5 are consistent with the text but ARE an interpretation: §13.6 writes `SF1 + SF4` without stating whether the unit is calls or flags; the working decision reads it as calls (an arithmetic sum of the SF1 and SF4 counts would give 2 for one call carrying both flags). This is the unit question of MPR section 2 and is the part that needs ratification (alternative S4, per-flag, is a PROTOCOL change).
> - **SF2 detection conflict (open; NOT changed in code; three separate statements, do not merge them):**
>   1. **Explicit protocol rule (verified, no interpretation needed).** Spec v2.7 §13.4 line 810: "SF2 | Empty response: no non-whitespace character."; line 816: "Structural failures are SF1–SF5."; §13.6 line 830: PASS needs "no SF2, no SF3, no SF5; `SF1 + SF4 ≤ f_S`"; line 831: FAIL-S is "any SF2, SF3, SF5, or `SF1 + SF4 > f_S`". So every call that meets SF2 makes the round FAIL-S, whatever other flag it carries. §13.4 states no exception for SF2 when SF1 or SF4 is also met, and no order of precedence between flags.
>   2. **Independent detection of all flags: measured consequence (2026-10-13, in-memory only, nothing written to the code).** Detecting SF2 on every response without a non-whitespace character (variant A1: no exception for SF1/SF4) was applied by monkeypatch to the existing suites. Result: the adapter returns text "" for every HTTP error, timeout and transport exception (`GeminiProvider.generate`), and "no candidate" is empty by construction, so under A1 EVERY such call becomes SF1+SF2 or SF4+SF2, i.e. a hard failure and FAIL-S. The soft allowance of §13.6 (`SF1 + SF4 ≤ f_S`, `f_S` = 1; PJR J-10 "tolerates one transport or block failure in 18 calls") would then be unreachable for every call the adapter can produce. 10 tests flip (8 in older suites: `test_provider_response` 4, `test_step10` 3, `test_sf_matrix_literal` 1; plus 2 pinned tests in `test_sf2_detection`) and the 4 marked tests succeed. Therefore the literal reading and the evident purpose of `f_S` conflict; this is a genuine rule ambiguity, not a code slip, and the earlier recommendation "detect every flag independently" is WITHDRAWN as stated. Options for the owner/advisor (none adopted): **A1** literal independent detection (the soft allowance becomes vacuous for adapter-made records; changes the meaning of FZ-v1 `f_S`; PROTOCOL-level consequence); **A2** independent detection of the five flags where SF2 is met only by a response that was received (HTTP 2xx) with no non-whitespace character, so a 503 or a timeout is SF1 only and an empty 200 is SF2 (a definitional clarification of "empty response"; needs a record entry); **B** keep the current precedence (SF1/SF4 over SF2) and write it into the record (no code change; the marked tests are rewritten to the ratified rule). Assistant's reading, not a decision: B (equivalently A2c, see 2b) respects both lines of §13.4/§13.6; A1 does not respect §13.6's own allowance; A2a/A2b are refined in 2b. Statement 1 (the explicit rule) is unaffected: whatever is ratified, a call that IS an SF2 under the ratified definition makes the round FAIL-S. The inactive patch for A1 is `deferred_patches/P1b_sf2_independent_detection.diff.INACTIVE`.
>   2b. **Analysis of 2026-10-13 (details and the full case table: `C31_C32_OWNER_DECISION_BRIEF.md`; reproducible with `step10/sf2_variants_analysis.py`, pinned by `test_sf2_variants.py`).** The current code equals variant B on 20 cases; variant A2c (SF2 when the text is empty and the call is neither SF1 nor SF4) equals B on an exhaustive 384-record grid, so A2 as first described (A2a strict 2xx; A2b with a block exception) is either harder than B for empty-bodied blocks (A2a) or leaves a hole for status-less empty records (A2b) and, with the hole closed, is B written as a definition. Recommendation (not adopted): do not ratify A1; if tolerance for SF1/SF4 is intended, ratify B as definitions D1-D8 of the brief (whitespace set, received response, invalid body, error/metadata, no candidate, soft unit, recording). Questions Q1-Q6 are in the brief.
>   3. **Interpretation still awaiting ratification: `f_S` per call.** §13.6 writes `SF1 + SF4 ≤ f_S` without stating the unit; the working decision reads it as calls (SF1+SF4 on one call = 1). Independent of statements 1-2.
>   **Current implementation (pre-existing, unchanged):** `s10_scoring.sf_flags` suppresses SF2 when the call also has SF1 or SF4 (line 59 condition `"SF4" not in flags and "SF1" not in flags`, and `not rec.get("error")`). There is no record-entry or decision that adopts this suppression (searched 12.18, 12.30, 12.36, 12.37). Consequence under the CURRENT code: all seven empty-body cases in the acceptance tests (HTTP 503 + empty, 503 without error marker, timeout + no body, transport error + whitespace body, SAFETY finish + empty, prompt block + empty, no candidate) yield a single soft flag and the round can PASS within `f_S` = 1; under the literal text each has SF2 and must FAIL-S. Not covered by items 3-5 of the working decision, because those act on detected flags and SF2 is not detected here. Stop for owner review before any pilot call: the live pilot outcome could depend on this point.
>   **Impact of changing it (documented before any change, as directed):** code `s10_scoring.sf_flags` only (one condition); `decision_type`/`pilot_counts` unchanged; tests: the four `expectedFailure` markers in `test_sf2_detection.py` are removed and the pinned-behaviour tests in the same file are rewritten; no change to flag definitions in the spec, denominators or thresholds; main-run `call_table`/`classify` outputs gain SF2 in `flags` for those calls (recording only). Alternatives A1, A2 and B are defined in statement 2; A1/A2 change `sf_flags` (one condition) and flip the tests listed there, B changes no code. Every alternative needs the approval block below.
>   **Acceptance tests:** `step10/test_sf2_detection.py` (14 tests, mock records): 10 pass today (pinned current behaviour, whitespace-only, empty, `None` text, NBSP not whitespace, valid text with transport error = SF1 only and soft, SF3 + empty, SF1 + SF4 independent, clean); 4 are `expectedFailure` and encode the literal text (SF1/SF4 + empty body must also carry SF2; every empty-body case must be FAIL-S; SF1+SF2 must be counted hard while all flags are kept). Checked without the markers: the 4 fail by AssertionError for the stated reason (SF2 absent from the flag list, outcome PASS instead of FAIL-S).
> - **Reason/impact:** closes the false-pass rows (SF1/SF4 combined with SF3/SF5); `counts` (decision vector) is disjoint, one entry per failed call; `primary_counts` (recording) and `flag_totals` (all flags, non-exclusive) are reported beside it; per-type table may sum to more than the failure total and is labelled. Code: `s10_scoring.decision_type`, `decision_counts`, `pilot_counts`; `s11_pilot.report` statement. The ledger `classified` entry and `classify()` output are unchanged. No data/analysis/cost impact; no stop path (a stop is MD-06/P2, not part of this working decision: the earlier draft clause "stops the workflow for owner review" is withdrawn from MD-01).
>   **Update 2026-10-13 (researcher's direction, option B):** the four expected-failure tests that encoded A1 were replaced; `test_sf2_detection.py` now has 19 tests that encode option B and definitions D1-D8 (including the real adapter path with a patched `urlopen`) and no expected failure; the A1 and A2a consequences stay analysed in `test_sf2_variants.py`. Working decision only; see the Direction record.
> - **Acceptance (met by `test_sf_matrix_literal.py`, 14 tests, all ordinary tests; the six former `expectedFailure` rows now expect FAIL-S):** outcomes equal hand-derived values for all 31 non-empty subsets of {SF1..SF5}: any subset containing SF2/SF3/SF5 -> FAIL-S, any subset of {SF1, SF4} -> one soft call; SF1+SF4 on one call -> `f_S` unit 1, both flags kept in `flag_totals`; two such calls with `f_S` = 1 -> FAIL-S; recording primary unchanged.
>
> - **Owner decision: PENDING | Advisor decision: PENDING | Date: PENDING | Option chosen: PENDING**

**`results_package_2026-10-13/C31_C32_OWNER_DECISION_BRIEF.md` lines 88-96**

> ## 8. Explicit questions for the owner / advisor
> - **Q1.** Which reading of §13.4 line 810 versus §13.6 lines 830-831 is intended for a call that is an HTTP error, a timeout or a block **and** has an empty body? **B/A2c** (the error or block explains the empty body: SF1/SF4 only), **A2a**, or **A1**.
> - **Q2.** Is `f_S` a count of calls (working decision) or of flags? (Only matters for SF1+SF4 on one call.)
> - **Q3.** Is the whitespace set D2 accepted, or is a Unicode definition wanted? (A U+00A0-only body is today UNP, not SF2.)
> - **Q4.** Should a record with no HTTP status and no error marker stop the run for review (MD-06) or be classified by D1/D3?
> - **Q5.** Should the adapter store a candidate indicator so that "no candidate" and "candidate without text and without finish reason" can be told apart (D6)? An adapter change needing its own acceptance tests.
> - **Q6.** Who decides: owner only, or owner and advisor? (MD-01 in `MASTER_PROPOSED_DECISION_RECORD.md` names both.)
>
> Decision fields: **Owner: PENDING | Advisor: PENDING | Date: PENDING | Option chosen: PENDING | Edits: PENDING**.

**`results_package_2026-10-13/C31_C32_OWNER_DECISION_BRIEF.md` lines 81-86**

> ## 7. Recommendation (not a decision)
> - **R1.** Do not ratify A1: it contradicts the tolerance written in the same section (§13.6 lines 830-831) for the records the adapter produces, and it re-routes the round-1 action (section 5 item 2).
> - **R2.** If the owner/advisor read §13.6 as intending tolerance for SF1/SF4, ratify **B, expressed as definitions D1-D8 (A2c)**, as a record entry (clarification of an undefined precedence). No scoring change is needed except rewriting the marked tests and a comment; `sf_flags` already implements it.
> - **R3.** If they read the text literally and accept the consequence, A1 is a PROTOCOL-level consequence for the meaning of `f_S` (it makes `f_S` irrelevant for adapter records) and should be decided together with `f_S` and the FZ-v1 value, not as a counting detail.
> - **R4.** A2a only if the owner wants empty blocks to be hard failures; state that this removes the soft treatment of a typical block.
> - Either way, ratify the `f_S` per-call unit (D7) in the same entry, and keep the SF3/SF5 rules as they are.


## 4. Original options (labels and order as in the sources)
Options as in C31_C32_OWNER_DECISION_BRIEF sections 7-8 (A1, A2a, A2c = B, etc.; labels preserved in the quoted text).

## 5. Consequences
- Source-defined: OAP: if rejected, 'the working decision must be replaced by your choice (A1/A2a diff or another rule) and the tests rewritten; the FZ hash waits'.
- Reasoned: the choice lives in `s10_scoring.py` (a listed file).

## 6. Recommendation: NOT ADOPTED
Source recommendation (NOT ADOPTED): the quoted C31 section 7 ('Recommendation (not a decision)').

## 7. Record cross-check
Decision record cross-check (read-only search of `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` for `MD-01`, `C-31`, `f_S`): lines [82, 263, 801]. Hits are mentions only. Entries 12.40-12.45 were read for this check: they either do not mention this item or state it as not decided (12.43, 12.44).

## 8. Dependencies
See the dependencies named in the header of this brief; no further source-backed content.

## 9. Information still missing
- Definitions D1-D8 'still need approval' (C31 section 14); advisor involvement for C-31 is named in MASTER_EXECUTION_REPORT.

## 10. Owner response (unfilled)
- [ ] APPROVE option B + D1-D8 + per-call unit as the working decision stands
- [ ] REJECT / AMEND: ______
- Owner: ______    Date: ______    Conditions: ______

## 11. Recording instruction
Do not record any outcome until the owner explicitly adopts it. The recording is a new entry in the owner decision record written under the owner's authority; this brief and its recommendation are not an entry and not a decision.
