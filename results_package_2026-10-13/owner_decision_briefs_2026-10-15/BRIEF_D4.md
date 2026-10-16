# D4: Priority when several SF flags occur on one call

**Status: PENDING OWNER DECISION: READY FOR OWNER.** Prepared 2026-10-15T03:30:47Z. The owner makes this decision; nothing here is adopted. Dependencies: none beyond those named below.

## 1. Why a decision is needed
The decision script needs disjoint counts; the order only decides the per-type table (ADV D4).

## 2-3. Authoritative sources and verbatim quotations
Quotations are exact text from the files and lines named (excerpts are marked). Interpretation is confined to sections 5-8.

**`results_package_2026-10-13/ADVISOR_DECISION_BRIEF.md` lines 31-37**

> ## D4. Priority when several SF flags occur on one call  (before pilot: it fixes the count vector)
> - **Reference:** §13.4 states none; `step10/s10_scoring.py` `PRIMARY_ORDER` (SF1 > SF4 > SF3 > SF2 > SF5, provisional); Policy 2 package §4.5 and D-4; 12.30.
> - **Problem:** the decision script needs disjoint counts. By reading `sf_flags`, the only realistic co-occurrence is SF3 with SF2 (empty text at the token limit); both are "hard" in 13.6, so the pilot outcome does not depend on the order. The order only decides the per-type table.
> - **Options:** (a) flags-only reporting, the order used only to build the pilot count vector; (b) freeze an exclusive order (the provisional one); (c) another order.
> - **Consequences:** pilot outcome is unaffected under (a) and (b) for the realistic case; (b) adds a rule that the text lacks.
> - **Recommendation:** (a), with the provisional order recorded as a counting convention.
> - **Decision:** ________________  **Date:** ________


## 4. Original options (labels and order as in the sources)
Options (a), (b), (c) as quoted.

## 5. Consequences
- Source-defined: see the Consequences line (quoted): pilot outcome unaffected under (a) and (b) for the realistic case.
- Reasoned: (b) adds a rule that the specification text lacks.

## 6. Recommendation: NOT ADOPTED
Source recommendation (NOT ADOPTED): ADV D4: '(a), with the provisional order recorded as a counting convention.'

## 7. Record cross-check
Decision record cross-check: no mention of `PRIMARY_ORDER`, `priority` in the record.

## 8. Dependencies
See the dependencies named in the header of this brief; no further source-backed content.

## 9. Information still missing
- None found.

## 10. Owner response (unfilled)
- [ ] (a)
- [ ] (b)
- [ ] (c) another order: ______
- Owner: ______    Date: ______    Conditions: ______

## 11. Recording instruction
Do not record any outcome until the owner explicitly adopts it. The recording is a new entry in the owner decision record written under the owner's authority; this brief and its recommendation are not an entry and not a decision.
