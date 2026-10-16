# D6: Which responses are eligible for S2/S3 coding

**Status: PENDING OWNER DECISION: READY FOR OWNER.** Prepared 2026-10-15T03:30:47Z. The owner makes this decision; nothing here is adopted. Dependencies: none beyond those named below.

## 1. Why a decision is needed
The population coded after the main run must be fixed before coding (and is reported beside every table).

## 2-3. Authoritative sources and verbatim quotations
Quotations are exact text from the files and lines named (excerpts are marked). Interpretation is confined to sections 5-8.

**`results_package_2026-10-13/ADVISOR_DECISION_BRIEF.md` lines 47-53**

> ## D6. Which responses are eligible for coding  (before coding)
> - **Reference:** §16 "only parseable responses"; TH16; 12.31; Policy 2 package §7 and D-10; `step10/s12_coding.py` (provisional).
> - **Problem:** "parseable" is undefined for an SF3 call whose truncated text still contains a valid verdict.
> - **Options:** (a) non-SF calls with a parseable verdict (current provisional rule); (b) include SF3-partial calls as a separate stratum; (c) all calls with a parseable verdict.
> - **Consequences:** (a) consistent with SF-first precedence; (b) adds a stratum and tables; (c) contradicts SF-first.
> - **Recommendation:** (a).
> - **Decision:** ________________  **Date:** ________

**`results_package_2026-10-13/MASTER_PROPOSED_DECISION_RECORD.md` lines 151-151**

> - **Coding eligibility (clarification):** "Coded: recorded calls with no SF flag and a verdict that parses. UNP, SF and SF3-with-verdict calls are counted beside every table with D_P(c)."


## 4. Original options (labels and order as in the sources)
Options (a), (b), (c) as quoted in ADV D6.

## 5. Consequences
- Source-defined: see the Consequences line of ADV D6 (quoted).
- Reasoned: (a) matches the current `s12_coding.py` (per MASTER_PREPILOT_RESOLUTION D6).

## 6. Recommendation: NOT ADOPTED
Source recommendation (NOT ADOPTED): ADV D6: '(a)'.

## 7. Record cross-check
Decision record cross-check (read-only search of `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` for `eligib`, `D_P`): lines [602, 689, 765, 839, 873]. Hits are mentions only. Entries 12.40-12.45 were read for this check: they either do not mention this item or state it as not decided (12.43, 12.44).

## 8. Dependencies
See the dependencies named in the header of this brief; no further source-backed content.

## 9. Information still missing
- None found for the options.

## 10. Owner response (unfilled)
- [ ] (a)
- [ ] (b)
- [ ] (c)
- [ ] other: ______
- Owner: ______    Date: ______    Conditions: ______

## 11. Recording instruction
Do not record any outcome until the owner explicitly adopts it. The recording is a new entry in the owner decision record written under the owner's authority; this brief and its recommendation are not an entry and not a decision.
