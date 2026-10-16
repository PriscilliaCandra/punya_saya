# MD-03: Kappa and the re-code reporting (K1-K4)

**Status: PENDING OWNER DECISION: BLOCKED — SOURCE TEXT REQUIRED (partial: see section 9).** Prepared 2026-10-15T03:30:47Z. The owner makes this decision; nothing here is adopted. Dependencies: none beyond those named below.

## 1. Why a decision is needed
Spec 16.3 line 1002 says agreement is 'reported per variable (percent agreement and Cohen's kappa)'; OD-3 says no kappa may be claimed; `s7_recode.py` reports raw agreement only. The reading must be fixed before the FZ hash because `s7_recode.py` and the codebook are Step 7 freeze-set files.

## 2-3. Authoritative sources and verbatim quotations
Quotations are exact text from the files and lines named (excerpts are marked). Interpretation is confined to sections 5-8.

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 33-33**

> | 2 | **MD-03:** K1 (raw agreement only, recorded departure from spec line 1002) or K2 (kappa labelled intra-rater, literal text)? | K1: no code, no re-freeze | K2: Step 7 re-freeze (R-7), Step 8 rebuild, new manifest | K2 only | | | | |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 48-48**

> | 2 | MD-03 K1/K2 | PENDING | K1 or K2 + values; box R-7 for K2 | `s7_recode.py`, codebook 5.1/5.3, Step 7 and Step 8 manifests (K2) | none | P4 (K2 + R-7) | Step 7 tests, rebuild sequence above, inventory identity | - | x | x | - |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 99-99**

> | MD-03 K2 rejected (K1 chosen) | P4 | no code; the departure from spec line 1002 is recorded |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 147-151**

> ## MD-03 Kappa and the re-code procedure (C-02, C-09) — formal approval; touches frozen Step 7 files
> - **Decision/recommendation:** K2: raw agreement + cross-tables per variable and Cohen's kappa labelled "intra-rater consistency; no inter-rater reliability claim"; "undefined" with counts for degenerate tables; sample = all if at most 20 else max(20, ceil 20 %); delay at least 14 days; concealed first-pass codes; columns `recode1_*`. Fallback K1 (raw only; a recorded departure from the literal spec line 1002). Owner + advisor.
> - **Consequences:** K2 changes `step7/s7_recode.py` and codebook 5.1/5.3 = a Step 7 re-freeze before the FZ hash; K1 changes nothing. **Alternatives rejected:** K3 (needs a threshold no source gives), K4 (amends §16.3: protocol change).
> - **Affects:** spec 1000-1003, OD-3, record 12.21 row 6, 12.24. **Timing consequence (verified in the code):** `step7/s7_recode.py` and the codebook are hashed by the Step 8 build manifest (`generator_code_sha256`), and the Step 9 evidence file names that manifest's SHA-256 (`s10_runner` gate line 139). K2 therefore means: Step 7 re-freeze (box **R-7**), a regenerated Step 8 manifest with a new hash, re-verification that the registry and checker bundle are byte-identical, and an evidence file created AFTER that. **Decide MD-03 before H3 is created**; a K2 chosen later makes the evidence file invalid and it must be recreated (a blind check on unchanged bundle bytes need not be redone only if those bytes are verified identical). K1 has no such effect. **Prerequisite:** decide before the FZ list is finalized and before H3.
> - `[ ] APPROVE K2  [ ] APPROVE K1  [ ] REJECT  [ ] AMEND: ______  | Owner: ______  | Advisor: ______  | Date: ______`

**`results_package_2026-10-13/CONFLICT_RESOLUTION_BRIEF.md` lines 52-61**

> | Option | What is reported | Class | Consequence for reliability reporting |
> |---|---|---|---|
> | K1 | Raw agreement and cross-tables only; kappa neither computed nor shown (current implementation) | RECORD ONLY (decides the reading of line 1002) | no chance-corrected figure; a reader cannot judge agreement beyond raw counts; departs from the literal line 1002 |
> | K2 | Also compute kappa per variable (with the cross-table) and print it with the label "intra-rater consistency; no inter-rater reliability claim" | RECORD ONLY + CODE (add kappa to `agreement_table`, tests, codebook 5.1/5.3 wording) | satisfies line 1002 and OD-3 together; kappa is unstable for small or skewed tables and can be undefined (all one category) — rules for that case would be needed |
> | K3 | Report kappa only for variables where each category has at least a stated number of items; otherwise raw only | RECORD ONLY + CODE | a threshold that is not in the protocol must be chosen and justified |
> | K4 | Amend §16.3 to remove the kappa phrase | PROTOCOL | only needed if the advisor wants the text to match K1 |
>
> ### RECOMMENDATION (PROPOSED — NOT ADOPTED)
> K2 with an explicit rule for undefined or unstable cases (report "undefined" with the counts), because it needs no protocol change, satisfies both texts, and gives the reader more information; K1 if the advisor judges kappa unsuitable for this design. Since the codebook is an FZ item and the FZ hash precedes the first pilot call (spec §13.2 line 797), the decision is needed before the FZ hash; it does not change any pilot call.
> ### OWNER/ADVISOR DECISION: PENDING

**`results_package_2026-10-13/MASTER_PROPOSED_DECISION_RECORD.md` lines 129-136**

> ### MD-03 Kappa and the re-code procedure (C-02, C-09)
> - **Class:** record entry (K1-K3) / PROTOCOL (K4 amends §16.3).
> - **Rule quoted:** spec §16.3 line 1002 "Agreement is reported per variable (percent agreement and Cohen's κ)"; line 1003 single-coder fallback; OD-3 "No inter-rater reliability and no Cohen's κ may be claimed"; 12.21 row 6; 12.24 decision 2.
> - **Proposed text (choose one sentence):** (K1) "Agreement is reported as raw agreement and cross-tables; kappa is not computed; this departs from the literal text of line 1002 and is recorded as a departure." (K2) "Agreement is reported as raw agreement and cross-tables and, per variable, Cohen's kappa labelled 'intra-rater consistency; no inter-rater reliability claim'; a variable with a degenerate table reports 'undefined' with its counts." (K3) as K2 for variables meeting ______.
>   Values: sample = all responses if at most 20, otherwise max(20, ceil(20 %)); delay at least 14 full days; concealed first-pass codes; columns `recode1_*`. The verbs computed / reported / claimed are stated separately.
> - **Acceptance:** codebook section 5.3 and `s7_recode` match the chosen sentence; decided before the FZ hash.
>
> - **Owner decision: PENDING | Advisor decision: PENDING | Date: PENDING | Option chosen: PENDING**

**`research_design/SCENARIO_CONSTRUCTION_SPECIFICATION_v2_7_DRAFT.md` lines 1002-1003**

> - Agreement is reported per variable (percent agreement and Cohen's κ).
> - **If no second human coder exists:** a delayed intra-rater re-code on an order scrambled by opaque ID (limitation: no inter-rater reliability). A model coder may be added only as a screening comparison, never as the reconciling authority and never described as inter-rater reliability.


## 4. Original options (labels and order as in the sources)
Options exactly as in CONFLICT_RESOLUTION_BRIEF (labels and order K1, K2, K3, K4 preserved in the quoted table); the proposed sentences for K1-K3 are in MPDR MD-03.

## 5. Consequences
- Source-defined: K1 'no code, no re-freeze'; K2 'Step 7 re-freeze (R-7), Step 8 rebuild, new manifest' (OAP row 2 and closure matrix); K3 'a threshold that is not in the protocol must be chosen and justified'; K4 PROTOCOL.
- Reasoned: K2 changes `s7_recode.py` and codebook 5.1/5.3, hence the Step 7 manifest and the Step 8 build manifest, hence 4 lines of the approved 31-file list and the evidence H3 names; K1 changes none.

## 6. Recommendation: NOT ADOPTED
Source recommendation (NOT ADOPTED): CRB: 'K2 with an explicit rule for undefined or unstable cases ... K1 if the advisor judges kappa unsuitable for this design.'

## 7. Record cross-check
Decision record cross-check (read-only search of `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` for `MD-03`, `kappa`, `K2`): lines [602, 689, 691, 726, 732, 765, 827, 877] .... Hits are mentions only. Entries 12.40-12.45 were read for this check: they either do not mention this item or state it as not decided (12.43, 12.44).

## 8. Dependencies
See the dependencies named in the header of this brief; no further source-backed content.

## 9. Information still missing
- K3: the number in 'at least a stated number of items' is stated nowhere (BLOCKED — SOURCE TEXT REQUIRED).
- K4: only the intent ('Amend section 16.3 to remove the kappa phrase') exists; no amendment wording is drafted (BLOCKED — SOURCE TEXT REQUIRED for the wording).
- Authority: MPDR register says 'owner + advisor'; no advisor answer exists.

## 10. Owner response (unfilled)
- [ ] K1
- [ ] K2 (with the undefined-case rule of MPDR MD-03)
- [ ] K3 with threshold ______ (threshold must be supplied)
- [ ] K4 with wording ______ (wording must be supplied)
- [ ] other: ______
- Owner: ______    Date: ______    Conditions: ______

## 11. Recording instruction
Do not record any outcome until the owner explicitly adopts it. The recording is a new entry in the owner decision record written under the owner's authority; this brief and its recommendation are not an entry and not a decision.
