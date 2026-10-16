# PG11b: PG11b scan scope

**Status: PENDING OWNER DECISION: BLOCKED — SOURCE TEXT REQUIRED (partial: see section 9).** Prepared 2026-10-15T03:30:47Z. The owner makes this decision; nothing here is adopted. Dependencies: none beyond those named below.

## 1. Why a decision is needed
The post-run bundle check scans model-written text for forbidden patterns; ordinary words can reject a bundle and block secondary S2/S3 coding (primary results unaffected).

## 2-3. Authoritative sources and verbatim quotations
Quotations are exact text from the files and lines named (excerpts are marked). Interpretation is confined to sections 5-8.

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 35-35**

> | 4 | **MD-05 PG11b:** keep the literal scan (risk stated)? | YES | narrowing = protocol change, new methodology version, `s7_bundle.py` and spec 8.2 change | narrowing only | | | | |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 50-50**

> | 4 | MD-05 PG11b | PENDING | keep literal, or narrow (PROTOCOL) | `s7_bundle.py`, spec 8.2 if narrowed | none | none if kept | none if kept | - | (x) | (x) | - |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 109-109**

> | MD-05, MD-07, MD-10 | the FZ hash | each is a prerequisite of the official hash; a rejected item is reopened first |

**`results_package_2026-10-13/ADVISOR_DECISION_BRIEF.md` lines 15-21**

> ## D2. PG11b scan scope  (before FZ hash: the bundle builder is an FZ item, 12.14)
> - **Reference:** §8.2 rows PG11a/PG11b ("no pattern PT1, PT3-PT8b occurs in any file name, file body or directory name"); §21.2 row 6; 12.26 item 2 (owner kept the literal text); `step7/s7_bundle.py` lines 30, 64-98; `test_step7.py` `test_D1_pt4_is_in_the_pg11_scan`.
> - **Problem:** the post-run application check scans model-written text. In an in-memory test with synthetic strings, ordinary words such as "CLEAR", "PAC", "(valid)", "class = A" were rejected, and rebuilding cannot help. The effect would be to block the secondary S2/S3 coding; primary results are unaffected.
> - **Options:** (a) keep literal (current); (b) amend to scan names, directory names, skeleton and prompt part only; (c) amend to scan response text only for machine-form patterns; (d) mask matches in the builder (changes what coders see).
> - **Consequences:** (a) risk of blocked coding, no cost now; (b), (c), (d) need a new methodology version and a Step 7 re-freeze before the FZ hash; (d) alters coder material and is the hardest to defend.
> - **Recommendation:** (a) for the first run if the timeline matters, accepting the risk in writing; (c) if the advisor wants S2/S3 coding protected. The choice should be made before the FZ hash because a later change is an FZ change.
> - **Decision:** ________________  **Date:** ________

**`results_package_2026-10-13/MASTER_PROPOSED_DECISION_RECORD.md` lines 149-149**

> - **PG11b (class: keep = no change; narrowing = PROTOCOL):** "The literal text of 8.2 stands. Known risk: ordinary words in model comments can block secondary coding." Alternative text if narrowed: ______.


## 4. Original options (labels and order as in the sources)
Options as in ADVISOR_DECISION_BRIEF D2, labels (a), (b), (c), (d) preserved in the quoted section; OAP: 'keep the literal scan (risk stated)' / narrowing.

## 5. Consequences
- Source-defined: narrowing = 'protocol change, new methodology version, `s7_bundle.py` and spec 8.2 change'.
- Reasoned: (b)-(d) change a Step 7 file (`s7_bundle.py` is in the Step 7 freeze set) so a Step 7 re-freeze and Step 8 rebuild would follow; the 31-file list would change at those lines.

## 6. Recommendation: NOT ADOPTED
Source recommendation (NOT ADOPTED): ADV D2: '(a) for the first run if the timeline matters, accepting the risk in writing; (c) if the advisor wants S2/S3 coding protected.'

## 7. Record cross-check
Decision record cross-check (read-only search of `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` for `PG11b`): lines [432, 434, 449, 453, 456, 462, 464, 479] .... Hits are mentions only. Entries 12.40-12.45 were read for this check: they either do not mention this item or state it as not decided (12.43, 12.44).

## 8. Dependencies
See the dependencies named in the header of this brief; no further source-backed content.

## 9. Information still missing
- The wording of (b), (c), (d): MPDR leaves 'Alternative text if narrowed: ______' blank (BLOCKED — SOURCE TEXT REQUIRED).
- Advisor choice requested by the brief: not obtained.

## 10. Owner response (unfilled)
- [ ] (a) keep the literal text of 8.2
- [ ] (b) narrow, with wording ______
- [ ] (c) narrow, with wording ______
- [ ] (d) narrow/mask, with wording ______
- [ ] other: ______
- Owner: ______    Date: ______    Conditions: ______

## 11. Recording instruction
Do not record any outcome until the owner explicitly adopts it. The recording is a new entry in the owner decision record written under the owner's authority; this brief and its recommendation are not an entry and not a decision.
