# MD-10: Confirmations of earlier choices (PC-2, I-6, P-3 item 1, F-3, PRD-8, Step 8 choices of 12.28)

**Status: PENDING OWNER DECISION: BLOCKED — SOURCE TEXT REQUIRED (partial: see section 9).** Prepared 2026-10-15T03:30:47Z. The owner makes this decision; nothing here is adopted. Dependencies: none beyond those named below.

## 1. Why a decision is needed
These earlier readings and Step 8 choices were taken under working direction and need the owner's confirmation (and the advisor's review) before the FZ hash.

## 2-3. Authoritative sources and verbatim quotations
Quotations are exact text from the files and lines named (excerpts are marked). Interpretation is confined to sections 5-8.

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 37-37**

> | 6 | **MD-10:** confirm PC-2, I-6 informational (gate counts 30 and 14), P-3 item 1, F-3, PRD-8 and the Step 8 choices of 12.28 (F-4, PG4, PG11a bundle of 624 files, A6b)? Advisor review done? | YES | an amended Step 8 choice or I-6 as a gate changes `step8/s8_*.py` or the projection | amended only | | | | |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 52-52**

> | 6 | MD-10 | PENDING | confirm PC-2, I-6, P-3 item 1, F-3, PRD-8 and the Step 8 choices of 12.28; advisor review | none if confirmed; `step8/s8_*.py` / projection bundle if amended | advisor review | none | rebuild sequence if amended | - | x | x | - |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 109-109**

> | MD-05, MD-07, MD-10 | the FZ hash | each is a prerequisite of the official hash; a rejected item is reopened first |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 157-159**

> ## MD-10 Confirmations of earlier choices (C-20, C-21, C-22, C-24, C-25, C-28)
> - **Recommendation:** confirm PC-2, I-6 informational (gate counts 30 and 14), P-3 item 1, F-3 closed, PRD-8 unchanged, and the Step 8 choices of record 12.28 (F-4, PG4, PG11a bundle of 624 files, A6b actor), with an advisor review of the Step 8 choices before the FZ hash. No code change. **Consequence if rejected/amended:** the rejected Step 8 choice is reopened before the FZ hash and may require a Step 8 rebuild (steps 3-9 repeat for a rejected PG3-type choice) and a new evidence file.
> - `[ ] APPROVE  [ ] REJECT  [ ] AMEND: ______  | Owner: ______  | Advisor: ______  | Date: ______`

**`results_package_2026-10-13/MASTER_PROPOSED_DECISION_RECORD.md` lines 186-187**

> ### MD-10 Confirmations of earlier choices (C-20, C-21, C-22, C-24, C-25, C-28)
> Text: "(PC-2) the pilot registry is built and gated at step 8; (I-6) informational diagnostic, gate counts stay 30 and 14; (P-3 item 1) `s2_values` 'none' is reported as a count outside its denominator; (F-3) closed; (PRD-8) unchanged; the Step 8 choices of record 12.28 (F-4 architecture, PG4 test, PG11a projection bundle of 624 files, A6b actor) are confirmed / amended: ______."

**`results_package_2026-10-13/ADVISOR_DECISION_BRIEF.md` lines 72-81**

> ## Other open items found while reading the record (not in the list you gave)
> | Item | Reference | Needed |
> |---|---|---|
> | PRD-6: anchoring of the decision record in a write-once store | §10, §19.3; 12.23 table; `research_design/` is untracked, FZ-v1 declares none | before the final pilot decision is written (Step 11): owner declares the store |
> | P-2: FZ hash contract | 12.21 row 7; decision script records the hash as "researcher-supplied, unverified" | before Step 11 (or accept "unverified" in writing) |
> | P-4 / OD-10: input size is a character bound, not measured | 12.18 row 6 ("for Step 7"); PJR J-9 (re-verify model, prices, cost at the freeze) | before the first paid call: re-accept the bound or authorize a measurement |
> | Round-1 FAIL-S action and the multi-type case | §13.6 actions; 12.18 row 5, 12.21 row 3 | when it occurs; researcher decision, logged |
> | PC-2: step at which the pilot registry is first built | §19.3; 12.23 table; 12.28 (reading taken) | confirm the reading |
> | I-6 six-reading check; F-3; PRD-8 | 12.23 table; 12.28 | confirm "informational" / current handling |
> | P-3: text inconsistencies (`s2_values`, MX, kappa, 13.4 versus SF2/SF3) | 12.21 row 5 | before coding |

**`research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` lines 743-745**

> ### 12.28 Step 8: decisions taken under the owner's instruction of 2026-10-13, and results (not an amendment of the specification)
>
> Choices (smallest coherent; each recorded here, none advisor approved): **F-4** Architecture 1 - independent construction in `step8/s8_construct.py`; Implementation A's gates are imported unmodified and applied to the generator's templates (section 21.1: step 8 gates by A); equivalence E-ID, E-PAR, E-GATE, E-PROMPT against A's builders, any difference rejects the build. **Registry**: canonical JSON (sorted keys, compact separators, ensure_ascii=False, UTF-8, one final LF), hash = SHA-256 of the file bytes; provenance and templates only (no prompts, no gate results). **Prompt hash**: SHA-256 of the ASCII bytes. **Artifacts**: `step8_output/step8_build_<12 hex of main registry hash>/` with main/ and pilot/ (registry.json, prompt_table.json, prompts/, checker_bundle/, checker_mapping_HELD_SEPARATELY.json, gate_report.json), pilot/pilot_calls.txt, manifest.json (no self hash), build_log.json (interpreter, UTC time; outside the deterministic inventory). **Pilot**: built and gated at step 8 by the same code (PC-2 reading: informational at step 4, hard at step 8); 18 calls by the section 13.3 rule. **IDs**: same canonical IDs in both registries, distinguished by registry_kind and registry hash. **Output scope**: registry, prompts, hashes, gate report, checker bundle, manifest; the call list is only cross-checked (IDs equal expected_template_ids, 2,496 slots, hash recorded); no request envelope. **I-6**: informational count only. **A6b**: computed at step 8 from rendered numerals (exact fractions); repeated with decimal arithmetic by the verifier; Implementation B (step 9) is not written. **PG4**: prompt equals the frozen segments around the registry plan block and no frozen text carries a numeral. **PG11a**: 624 projections (rule and plan block of Cond-A and Cond-B, no claim, task or format). **PG11b builder test**: 75 items of the section 13.5 batteries assigned to registry call keys. **PG3 reading (clarification, advisor review pending)**: \"contiguous\" is read as one changed span with every differing position inside the target token (section 8.2: \"a single changed span\"); the strict reading (consecutive positions) would reject 90 of 104 MIL templates because the decimal point is shared (180 pairs in the main registry are non-consecutive and are counted in gate_report.json, not rejected). **Failure log**: separate folder `step8_failures/`, nothing published. **Interpreter**: recorded (CPython 3.11.9), not enforced.


## 4. Original options (labels and order as in the sources)
Options in the sources: 'confirmed / amended: ______' (MPDR) and OAP: YES / an amended Step 8 choice or I-6 as a gate.

## 5. Consequences
- Source-defined: 'an amended Step 8 choice or I-6 as a gate changes `step8/s8_*.py` or the projection' (OAP row 6); 'rebuild sequence if amended'.
- Reasoned: an amendment would rebuild the Step 8 output; H1 may be void if the registry changes.

## 6. Recommendation: NOT ADOPTED
Source recommendation (NOT ADOPTED): OAP: confirm, 'with an advisor review of the Step 8 choices before the FZ hash'.

## 7. Record cross-check
Decision record cross-check (read-only search of `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` for `MD-10`, `PC-2`, `I-6`): lines [97, 239, 286, 299, 331, 361, 374, 526] .... Hits are mentions only. Entries 12.40-12.45 were read for this check: they either do not mention this item or state it as not decided (12.43, 12.44).

## 8. Dependencies
See the dependencies named in the header of this brief; no further source-backed content.

## 9. Information still missing
- Amendment wording: the blank '______' is not filled in any source (BLOCKED — SOURCE TEXT REQUIRED for any amendment).
- Advisor review: not obtained. P-3 items other than item 1 are covered by brief P-3.

## 10. Owner response (unfilled)
- [ ] confirm all items as written
- [ ] amend (name the item and give the wording): ______
- Owner: ______    Date: ______    Conditions: ______

## 11. Recording instruction
Do not record any outcome until the owner explicitly adopts it. The recording is a new entry in the owner decision record written under the owner's authority; this brief and its recommendation are not an entry and not a decision.
