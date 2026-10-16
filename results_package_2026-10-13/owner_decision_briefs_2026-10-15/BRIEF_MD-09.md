# MD-09: Anchoring of the decision record (PRD-6 / H7 / P7)

**Status: PENDING OWNER DECISION: READY FOR OWNER.** Prepared 2026-10-15T03:30:47Z. The owner makes this decision; nothing here is adopted. Dependencies: none beyond those named below.

## 1. Why a decision is needed
The decision record must be anchored in a write-once store before an order is generated; the store is not declared (PRD-6, H7).

## 2-3. Authoritative sources and verbatim quotations
Quotations are exact text from the files and lines named (excerpts are marked). Interpretation is confined to sections 5-8.

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 63-63**

> | 17 | MD-09, box P7, H7 | PENDING | anchor store; runner anchor check | `s10_runner.py` (P7), decision record anchoring | pilot done | P7 | P7 tests | - | - | - | after the pilot, before the decision script |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 21-21**

> | P7 anchor check | MD-09 + H7 declaration + box **P7** | the decision script |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 106-106**

> | P7 | the runner's anchor check | the anchor is a manual procedure |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 165-167**

> ## MD-09 Anchoring, authorization content, order of runs (C-18) — needed after the pilot, before the decision script
> - **Recommendation:** anchor the decision record by your own commit (commit ID recorded in the final freeze manifest and run manifests; committing is your act, not the assistant's); authorization content as in H5 of `HUMAN_TASKS_H1_H7_OPERATIONAL_CHECKLIST.md`; order pilot -> integrity -> decision -> record anchored -> final freeze manifest -> main. Alternative: external timestamped copy of the record's SHA-256. Affects spec 662, 1132. **Consequence if not decided:** the decision script must not be run (the record must be anchored before an order is generated), so the main run cannot start; the pilot is not affected. Box **P7** below (anchor check) is only needed if you want the runner to verify the anchor.
> - `[ ] APPROVE  [ ] REJECT  [ ] AMEND: ______  | Store chosen: ______  | Owner: ______  | Date: ______`

**`results_package_2026-10-13/MASTER_PROPOSED_DECISION_RECORD.md` lines 180-184**

> ### MD-09 Anchoring of the decision record, authorization content, order of runs (C-18)
> - **Class:** record entry.
> - **Proposed text:** "The decision record is anchored by ______ (own commit with ID recorded in the final freeze manifest and run manifests / external timestamped copy of its SHA-256), declared on ______ [date], before the decision script is run. The owner authorization for a run is a file with `authorized_by` = owner, the scope, the exact number of calls, the cost ceiling 100 and the input-size basis of MD-02. Order: pilot round 1 → report and integrity check → decision → [round 2 only after a whitelisted change as a new FZ version] → decision record anchored → final freeze manifest → main run."
>
> - **Owner decision: PENDING | Advisor decision: PENDING | Date: PENDING | Option chosen: PENDING**

**`results_package_2026-10-13/HUMAN_TASKS_H1_H7_OPERATIONAL_CHECKLIST.md` lines 109-115**

> ## H7 Declare the write-once store (PRD-6)
> - **Purpose.** Spec 10 line 662 and 19.3 line 1132: the decision record must be anchored in a write-once store before an order is generated; the runner verifies the anchor for the main run (patch P7, MD-09).
> - **Procedure.** The owner chooses and declares the store (own commit whose ID is recorded, or an external timestamped copy of the record's SHA-256), as an official record entry, before the decision script runs. Committing is the owner's permission; the assistant does not commit.
> - **Evidence.** The record entry (approver, date, store type and location).
> - **Acceptance.** Entry exists before the decision script is run; later the recomputed record hash matches the anchored value.
> - **Status.** NOT DONE.
>

**`results_package_2026-10-13/deferred_patches/DEFERRED_PATCHES.md` lines 56-59**

> ## P7 Anchor check (MD-09; C-18)
> - **Source.** spec 662 (anchoring "PENDING RESEARCHER DECISION PRD-6"), 1132; record 655.
> - **Why held.** The write-once store is not declared (human task H7), `research_design/` is untracked, and the spec requires the runner to verify the anchor, which cannot be built without the declared store type. Nothing is invented.
> - **Design after adoption.** Main-scope gate: recompute the SHA-256 of the decision record, compare with the anchored value read from the declared store; refuse if missing or different. **Acceptance:** positive (match), negative (one byte changed), boundary (anchor absent, anchor of another record, empty store).


## 4. Original options (labels and order as in the sources)
Store options in H7: 'own commit whose ID is recorded, or an external timestamped copy of the record's SHA-256'; boxes MD-09 and P7 APPROVE/REJECT.

## 5. Consequences
- Source-defined: OAP: 'MD-08, MD-09 | P8, the decision script | no resume; no decision script, hence no main run'; P7 rejected: 'the anchor is a manual procedure'.
- Reasoned: needed after the pilot and before the decision script (OAP heading), not before the pilot call; a commit is the owner's act (the assistant does not commit).

## 6. Recommendation: NOT ADOPTED
Source recommendation (NOT ADOPTED): H7 text: 'own commit ... is the recommended store'.

## 7. Record cross-check
Decision record cross-check (read-only search of `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` for `anchor`, `write-once`, `PRD-6`): lines [526, 587, 608, 655, 695, 720, 877, 897] .... Hits are mentions only. Entries 12.40-12.45 were read for this check: they either do not mention this item or state it as not decided (12.43, 12.44).

## 8. Dependencies
See the dependencies named in the header of this brief; no further source-backed content.

## 9. Information still missing
- The store type and the declaration date are the owner's to write (blanks in the MPDR text).

## 10. Owner response (unfilled)
- [ ] store = own commit (ID to be recorded) 
- [ ] store = external timestamped copy of the record SHA-256
- [ ] P7 APPROVE
- [ ] P7 REJECT
- [ ] other: ______
- Owner: ______    Date: ______    Conditions: ______

## 11. Recording instruction
Do not record any outcome until the owner explicitly adopts it. The recording is a new entry in the owner decision record written under the owner's authority; this brief and its recommendation are not an entry and not a decision.
