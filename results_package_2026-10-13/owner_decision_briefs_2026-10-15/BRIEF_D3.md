# D3: Structural failures and UNP in the main run (SF/UNP policy)

**Status: PENDING OWNER DECISION: BLOCKED — SOURCE TEXT REQUIRED (partial: see section 9).** Prepared 2026-10-15T03:30:47Z. The owner makes this decision; nothing here is adopted. Dependencies: none beyond those named below.

## 1. Why a decision is needed
Under the literal text SF2/SF3 calls without a verdict also meet the UNP definition and the four proportions of 18.2 cannot sum to 1 when an SF occurs; 12.18 row 1 fixes SF-first precedence for the pilot only. Decision needed before the FZ hash (section 18 is an FZ item).

## 2-3. Authoritative sources and verbatim quotations
Quotations are exact text from the files and lines named (excerpts are marked). Interpretation is confined to sections 5-8.

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 36-36**

> | 5 | **MD-05 SF/UNP and parse-first:** keep the interim policy (an SF call is SF only; 18.2 as written; counts reported beside)? Parse-first, Policy 1 and Policy 2 are not adopted? | YES | any other policy = spec 18.2 amendment | other policy only | | | | |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 51-51**

> | 5 | MD-05 SF/UNP policy, eligibility | PENDING | interim as built, or Policy 1/2/parse-first (PROTOCOL) | none if interim; spec 18.2 otherwise | MD-01 | none | none if interim | - | (x) | x | - |

**`results_package_2026-10-13/MASTER_PROPOSED_DECISION_RECORD.md` lines 150-150**

> - **SF/UNP policy (class: interim = clarification; Policy 1/2/parse-first = PROTOCOL):** "A call that meets any SF definition is classified SF only. Main-run reporting follows §18.2 as written: SF calls stay in `n_calls`, the SF count and rate are reported beside the four proportions, no proportion is rescaled."

**`results_package_2026-10-13/ADVISOR_DECISION_BRIEF.md` lines 23-29**

> ## D3. Structural failures and UNP in the main run  (before main run; before FZ hash because §18 is in FZ)
> - **Reference:** §13.4 (SF1-SF5, UNP), §13.6, §13.8, §18.2 (four proportions over all `n_calls`, "sum to 1"), §22 item 6; 12.18 row 1 (pilot rule); 12.24 decision 1 (Policy 1 proposed); 12.26 item 1 (owner kept v2.7 as written); `PROPOSED_AMENDMENT_18_2_DRAFT_v1.md`; `POLICY_2_METHODOLOGY_DECISION_PACKAGE_DRAFT_v1.md`.
> - **Problem:** under the literal text SF2 and SF3 without a verdict also meet the UNP definition; 12.18 row 1 fixes SF-first precedence for the pilot only. With an SF call in a main cell the four proportions cannot sum to 1.
> - **Options:** (L) literal text, overlap unresolved; (C) v2.7 plus the SF-first sentence, SF reported beside the four proportions (current interim rule); (P1) evaluable-call denominators plus a separate SF rate; (P2) SF as a fifth class over planned calls; (PF) parse-first.
> - **Consequences:** L and PF contradict 12.18 row 1. C needs no amendment but leaves "sum to 1" false when an SF occurs. P1 contradicts §12 ("over all R calls") and leaves cluster means undefined. P2 keeps §12 intact, sums to 1, matches the halting monitor, and needs an amendment, a call ledger and a counting sentence.
> - **Recommendation:** C for the pilot and the first main run (it needs nothing); P2 if the advisor wants a clean "sums to 1" statement, adopted before the FZ hash.
> - **Decision:** ________________  **Date:** ________

**`research_design/step7/PROPOSED_AMENDMENT_18_2_DRAFT_v1.md` lines 1-14**

> # Proposed amendment of section 18.2 - DRAFT v1 (outcome denominators and structural failures)
>
> Status: **PROPOSED AMENDMENT. NOT APPLIED. NOT ADOPTED.** Specification v2.7 (sha256 `d5fcffad...082ca8`) is unchanged and remains the
> text in force. This file records the owner's delegated decision of 2026-10-12 (decision record 12.24, decision 1) as a proposal for a
> future methodology version (13.2, 21.2). It supersedes proposal P-1 (alternative A1) of `PROPOSED_CLARIFICATIONS_AND_AMENDMENTS_DRAFT_v1.md`.
> The draft code that expresses it (`s7_outcomes.py`) is conditional on adoption. The author of this proposal, the code and the tests is the same.
>
> ## 1. The proposed policy
>
> 1. The four primary outcome proportions (satisfied, violated, unclear, unparseable) use the number of **evaluable responses** of the cell as denominator.
> 2. Evaluable responses = the actual calls of the cell excluding the calls classified as structural failures (SF1 to SF5).
> 3. The four proportions sum to 1 (exact rational arithmetic, 3.1).
> 4. The **structural-failure rate** is reported separately over the protocol-defined total number of calls of the cell.
> 5. Pilot UNP share = UNP calls / all actual calls of the round (as implemented in `s7_decision.py`; unchanged).

**`research_design/step7/POLICY_2_METHODOLOGY_DECISION_PACKAGE_DRAFT_v1.md` lines 120-146**

>
> ### 4.1 Candidate
> Any call with a flag SF1-SF5 is `structural failure` in the primary classification: SF2, SF3 (also with a parseable partial verdict), SF5, SF1
> and SF4 alike. This is **SF-only precedence**.
>
> ### 4.2 Comparison with the alternatives
> | | SF-only (candidate) | Parse-first | Flags + explicit class table |
> |---|---|---|---|
> | SF2 (empty) | structural failure | unparseable (zero matches) | per table |
> | SF3, no verdict | structural failure | unparseable | per table |
> | SF3 with a parseable verdict | structural failure | the parsed class | per table |
> | SF5 | structural failure | structural failure when parsing did not run, else parsed class | per table |
> | Class "structural failure" equals the calls counted by the 13.8 monitor | **yes** | no (SF2/SF3 become flags only) | depends |
> | Same rule can serve pilot and main run | **yes** | no | depends |
>
> ### 4.3 Compatibility with the frozen pilot rules
> FROZEN 13.6: PASS needs "no SF2, no SF3, no SF5; SF1 + SF4 <= f_S; UNP share <= theta_unp"; FAIL-S is any SF2, SF3, SF5 or `SF1 + SF4 > f_S`;
> FAIL-U is "UNP share > theta_unp" and means STOP-U, with "no re-pilot of the unchanged protocol". The frozen text does not say whether an empty or
> truncated response counts toward the UNP share; the owner clarification 12.18 row 1 (not specification text) says it does not.
>
> **The choice changes a frozen outcome.** Example: a pilot round of 18 calls with 10 empty responses (SF2). If empty responses were also UNP
> (literal reading of "zero Verdict matches"), the UNP share is 10/18 = 5/9 > 1/2 and the round is FAIL-U, hence STOP-U. Under SF-only precedence the
> UNP share is 0 and the round is FAIL-S, the recoverable branch (SF2: a pure implementation fix, H1-H4). SF-only precedence is therefore
> **consequential for the pilot**, and it must be written into the specification (section 11, A-1) for the pilot and the main run alike. The
> candidate matches the clarification already applied by `s7_decision.py` (disjoint counts) and the halting monitor of 13.8, which counts SF1-SF5
> per call. Parse-first would make the main run and the pilot differ, and would turn some pilot FAIL-S cases into FAIL-U.
>


## 4. Original options (labels and order as in the sources)
Options exactly as in ADVISOR_DECISION_BRIEF D3: L, C, P1, P2, PF (quoted section). Draft texts: P1 = PROPOSED_AMENDMENT_18_2_DRAFT_v1.md (complete draft); P2 = POLICY_2_METHODOLOGY_DECISION_PACKAGE_DRAFT_v1.md (candidate level).

## 5. Consequences
- Source-defined: see the Consequences line of ADV D3 (quoted): L and PF contradict 12.18 row 1; C needs no amendment; P1 contradicts section 12; P2 needs an amendment, a call ledger and a counting sentence.
- Reasoned: P1/P2 are amendments of the frozen specification (new methodology version) and would change `s10_scoring.py`/the decision script/report, listed files of the 31-file list.

## 6. Recommendation: NOT ADOPTED
Source recommendation (NOT ADOPTED): ADV D3: 'C for the pilot and the first main run (it needs nothing); P2 if the advisor wants a clean "sums to 1" statement, adopted before the FZ hash.'

## 7. Record cross-check
Decision record cross-check (read-only search of `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` for `SF/UNP`, `Policy 2`, `18.2`): lines [506, 522, 587, 598, 608, 659, 667, 676] .... Hits are mentions only. Entries 12.40-12.45 were read for this check: they either do not mention this item or state it as not decided (12.43, 12.44).

## 8. Dependencies
See the dependencies named in the header of this brief; no further source-backed content.

## 9. Information still missing
- Final amendment wording of P2 (the Policy 2 package is a candidate-level draft and states its originating request was cut off) and of PF (described in the comparison table, no amendment wording): BLOCKED — SOURCE TEXT REQUIRED.
- Advisor choice: not obtained.

## 10. Owner response (unfilled)
- [ ] L
- [ ] C (interim as built)
- [ ] P1
- [ ] P2 (wording to be supplied)
- [ ] PF (wording to be supplied)
- [ ] other: ______
- Owner: ______    Date: ______    Conditions: ______

## 11. Recording instruction
Do not record any outcome until the owner explicitly adopts it. The recording is a new entry in the owner decision record written under the owner's authority; this brief and its recommendation are not an entry and not a decision.
