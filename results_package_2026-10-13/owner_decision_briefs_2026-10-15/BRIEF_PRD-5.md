# PRD-5: Unit-token sets of the blind-check worksheet (MD-05 part 1)

**Status: PENDING OWNER DECISION: READY FOR OWNER.** Prepared 2026-10-15T03:30:47Z. The owner makes this decision; nothing here is adopted. Dependencies: none beyond those named below.

## 1. Why a decision is needed
The evaluator `s9_blindcheck.py` must know which unit sets are accepted before any blind-check evaluation is read as final (H1).

## 2-3. Authoritative sources and verbatim quotations
Quotations are exact text from the files and lines named (excerpts are marked). Interpretation is confined to sections 5-8.

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 32-32**

> | 1 | **PRD-5:** adopt the field-specific unit sets printed in spec 11.2 step 3? | YES: no change | the older global list: change `s9_blindcheck.py`, rerun its tests, before any evaluation | no (Step 9 file is not manifest-bound) | | | | |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 47-47**

> | 1 | PRD-5 (MD-05 pt 1) | PENDING | adopt the printed unit sets (spec 699) or the older list | `step9/s9_blindcheck.py` (already the printed sets) | none | none (older list: a change to `s9_blindcheck.py`) | `test_blindcheck.py` if changed | - | x (before the first evaluation) | - | - |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 116-120**

> ## MD-05 (part 1) PRD-5 unit sets of the blind-check worksheet — decide first
> - **Decision/recommendation:** adopt the field-specific unit-token sets printed in spec §11.2 step 3 (line 699). Requires formal approval (reading of a frozen clause).
> - **Consequences:** a foreign unit gives CHECKER ERROR (logged); no effect on the registry or the primary analysis. **Alternative rejected:** the older global unit list.
> - **Affects:** `step9/s9_blindcheck.py` `UNITS`/`normalize` (already implement the printed sets); spec lines 699, 1131. **Prerequisite:** none. **Ambiguity:** none.
> - `[ ] APPROVE  [ ] REJECT  [ ] AMEND: ______  | Owner: ______  | Date: ______`

**`results_package_2026-10-13/ADVISOR_DECISION_BRIEF.md` lines 55-61**

> ## D7. PRD-5: unit-token normalization of the human check  (before the human blind check is evaluated)
> - **Reference:** §11.2 step 3 (field-specific sets, marked "PENDING RESEARCHER DECISION PRD-5"), §19.3; `step9/s9_blindcheck.py` (`UNITS`).
> - **Problem:** the field sets are printed in the text but the decision is still marked pending.
> - **Options:** (a) adopt the printed field-specific sets; (b) return to the older global list (accepts more representations, absorbs wrong units).
> - **Consequences:** (a) stricter; a human who writes a foreign unit gets a transcription CHECKER ERROR (logged, member kept); (b) is not the text of v2.7.
> - **Recommendation:** (a).
> - **Decision:** ________________  **Date:** ________

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 96-96**

> | PRD-5 | the trust in any blind-check evaluation | the older global unit list would need a change to `s9_blindcheck.py` and a re-verification before H1 is evaluated |


## 4. Original options (labels and order as in the sources)
Options exactly as the sources state them: (a) adopt the printed field-specific sets; (b) return to the older global list (ADVISOR_DECISION_BRIEF D7); in OWNER_APPROVAL_PACKAGE: YES (printed sets) / the older global list.

## 5. Consequences
- Source-defined: (b) 'would need a change to `s9_blindcheck.py` and a re-verification before H1 is evaluated' (OAP consequence table, line 96); 'Step 9 file is not manifest-bound'.
- Reasoned: the code already contains the printed sets (OAP closure matrix), so (a) changes nothing; (b) changes a Step 9 file that is not in the 31-file P13 list unless it is `step9/s9_blindcheck.py` (it IS in that list), so a (b) change would move its hash.

## 6. Recommendation: NOT ADOPTED
Source recommendation (NOT ADOPTED): ADVISOR_DECISION_BRIEF D7: '(a)'. No separate assistant recommendation.

## 7. Record cross-check
Decision record cross-check (read-only search of `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` for `PRD-5`): lines [526, 587, 608, 654, 695, 720, 777]. Hits are mentions only. Entries 12.40-12.45 were read for this check: they either do not mention this item or state it as not decided (12.43, 12.44).

## 8. Dependencies
See the dependencies named in the header of this brief; no further source-backed content.

## 9. Information still missing
- None found for the options themselves.

## 10. Owner response (unfilled)
- [ ] (a) adopt the printed field-specific unit sets
- [ ] (b) return to the older global list
- [ ] other: ______
- Owner: ______    Date: ______    Conditions: ______

## 11. Recording instruction
Do not record any outcome until the owner explicitly adopts it. The recording is a new entry in the owner decision record written under the owner's authority; this brief and its recommendation are not an entry and not a decision.
