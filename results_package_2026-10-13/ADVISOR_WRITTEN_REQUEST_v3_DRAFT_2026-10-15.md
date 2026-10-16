# Written advisor request, version 3 DRAFT (prepared 2026-10-15T04:49:23Z)

**DELIVERY STATUS: NOT SENT. Nothing was transmitted and no advisor answer exists.** This draft is for the owner's review; it is not an approval request to the advisor on the owner's behalf and records no advisor view. Versions v2 (`ADVISOR_WRITTEN_REQUEST_v2_2026-10-15.md`, sha256 `3b0d13ee426872cc3455bd48a17904b57a15ceffff725545b0ba8bab9d63dc2b`) and the first draft are preserved unchanged. v3 differs from v2 because the owner has since recorded decisions on several items that the sources assign to "owner + advisor": the advisor is now asked to CONCUR, OBJECT or advise otherwise on recorded owner choices, instead of choosing among options. All quotations are extracted from the files and lines named (record entries 12.46-12.49 are in `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md`).

**Recipient and channel: NOT VERIFIED.** The repository names no advisor and no contact (`paper/PAPER_DRAFT.md` line 13: "[CO-AUTHOR / SUPERVISOR NAMES — TO BE COMPLETED]"; `paper/PAPER_GAPS.md` line 52). Information the owner must supply: (1) the advisor's name and role; (2) the official channel and address or account; (3) whether the assistant may send through a named authorized tool or the owner sends; (4) approval of the final text. Priority when sending: B1 and B6, then Part B concurrences, then B2-B4, then B7.

Proposed subject: "Written input requested: pre-pilot decisions of the scenario-construction study (specification v2.7)".

## A. For information (no answer requested)
Recorded 2026-10-15: PRD-5 (printed unit sets), D4 (flags-only reporting, order as counting convention), D6 (non-SF calls with a parseable verdict) and MD-07 (180 s stays a per-socket-operation timeout) in entry 12.46; MD-02 (owner only) in 12.48; the resume policy and the P13 list in 12.40-12.45. Quoted project "Recommendation" lines in the extracts below are the project assistant's suggestions, are not adopted, and you are not asked to endorse them.

## B. Concurrence requests: owner choices recorded, advisor concurrence pending
The sources name "Owner + advisor" for MD-01, MD-03 and MD-04, and list PG11b, D3 and the re-code values as open advisor items of the Step 7 manifest. For each item the owner's recorded choice is quoted; **the answer requested is: concur / object (with reason) / advise another option among those the project documents describe / comment.** An objection does not change the record; the owner decides what follows.
**B-MD03. MD-03: K2 (kappa labelled) and the 12.49 clarification.** *Source:* `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` lines 935-935

> | 1 | MD-03 | `OWNER_APPROVAL_PACKAGE.md` line 33: "K1 (raw agreement only, recorded departure from spec line 1002) or K2 (kappa labelled intra-rater, literal text)"; K2 sentence (`MASTER_PROPOSED_DECISION_RECORD.md` MD-03): "Agreement is reported as raw agreement and cross-tables and, per variable, Cohen's kappa labelled 'intra-rater consistency; no inter-rater reliability claim'; a variable with a degenerate table reports 'undefined' with its counts." | **K2**, together with the values confirmed under D5 | The owner accepts the stated consequence: a Step 7 re-freeze (new Step 7 manifest, Step 8 build manifest regenerated and re-verified) and, after any change, the comparison of the new Step 8 manifest inventory (2,026 file hashes) with the old one; per the source, an inventory difference means the registry changed and H1 must be redone, an identical inventory leaves a blind check on the bundle valid, and H3 must be created against the NEW manifest. **Not authorized by this entry:** the re-freeze itself (box R-7 is a separate authorization and is not recorded as given), any edit of `s7_recode.py`, the codebook or any manifest. K3 and K4 are not chosen. K2 prospectively replaces the "no kappa" element of the delegated reading in 12.21 row 6 only once the codebook and `s7_recode.py` are changed under R-7. Advisor concurrence: NOT obtained. |

*Source:* `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` lines 962-982

> ### 12.49 Owner clarification of OD-3 and the K2 reporting decision for Cohen's kappa, 2026-10-15 (recorded 2026-10-15T04:45:14Z; records the owner's decisions; the author's interpretation of OD-3, NOT an amendment of OD-3; NO advisor concurrence; not an implementation of K2)
>
> Authority: the owner's written statements in the working conversation of 2026-10-15. The owner's name and signature are not part of this text. Entries 12.40-12.48 are unchanged, and this entry edits none of them. It changes no specification text, no codebook, no code (`s7_recode.py`, `agreement_table`), no test, no manifest and no evidence; no kappa value was calculated or displayed.
>
> **Sources checked before recording:** spec v2.7 16.3 ("Agreement is reported per variable (percent agreement and Cohen's κ)." and "(limitation: no inter-rater reliability) ... never described as inter-rater reliability"); OD-3, `STEP2_OWNER_DECISIONS_RECORD.md` ("**No inter-rater reliability and no Cohen's κ may be claimed.**"; status "Owner decision recorded. Not a specification amendment"); `CONFLICT_RESOLUTION_BRIEF.md` section 2 (K1 "kappa neither computed nor shown"; K2 "Also compute kappa per variable (with the cross-table) and print it with the label 'intra-rater consistency; no inter-rater reliability claim'"; and "A kappa can be computed and shown with an explicit 'not a reliability claim' label without violating OD-3", which also marks as unresolved whether OD-3 meant 'not computed' or 'not claimed'); `MASTER_PROPOSED_DECISION_RECORD.md` MD-03 (the K2 sentence); `MASTER_PREPILOT_RESOLUTION.md` D5 (acceptance: "record entry stating the verb ('computed' / 'reported' / 'claimed') separately"); `OWNER_APPROVAL_PACKAGE.md` (MD-03: "Owner + advisor."; box R-7). Entries 12.47 and 12.48 are in this record (not in `MASTER_PROPOSED_DECISION_RECORD.md`); the K2 sentence was checked in both places and is identical. No material discrepancy was found.
>
> **Owner decisions, stated separately (the three verbs):**
> | Verb | Decision |
> |---|---|
> | Cohen's kappa is **computed** | **YES** |
> | Cohen's kappa is **reported / displayed** | **YES** |
> | Cohen's kappa is **claimed** as evidence of reliability | **NO** |
>
> **Permitted description.** Only the existing K2 label is used: `intra-rater consistency; no inter-rater reliability claim`. The owner decided not to add an interpretation scale, a threshold or any new statistical rule; K3 (threshold) and K4 (amendment of 16.3) remain not chosen.
>
> **The author's interpretation of OD-3.** The owner is the author of OD-3 and clarifies that "no Cohen's κ may be claimed" means that kappa must not be claimed (in particular not as evidence of reliability), not that it must never be computed or displayed. This resolves, as the author's interpretation, the point that `CONFLICT_RESOLUTION_BRIEF.md` recorded as unresolved ("not computed" or "not claimed"). It is not an amendment of OD-3; OD-3 and its recorded text are unchanged.
>
> **K2 wording.** The K2 sentence recorded in entry 12.47 remains unchanged and is not replaced by this entry: "Agreement is reported as raw agreement and cross-tables and, per variable, Cohen's kappa labelled 'intra-rater consistency; no inter-rater reliability claim'; a variable with a degenerate table reports 'undefined' with its counts." The three verbs above are consistent with that sentence (computed and reported; no reliability claim).
>
> **Supersession of earlier language.** The "no kappa" language of the delegated readings in entry 12.21 (row 6) and entry 12.24 (decision 2) is superseded only after K2 has been formally applied through its authorized process (codebook and `s7_recode.py` changes under a Step 7 re-freeze). Until then those entries, the codebook and the code stand as they are; no historical entry is rewritten or deleted.
>

Specific advisor question (source: `CONFLICT_RESOLUTION_BRIEF.md`, "a statistical question for the advisor"): is Cohen's kappa meaningful for an intra-rater re-code of 20 % samples with several categories, where cells can be small or skewed? The owner decided not to add any interpretation scale, threshold or statistical rule. Implementation of K2 is blocked in any case by R-7, which the owner has not authorized.
**B-PG11b. PG11b: option (a), keep the literal text.** *Source:* `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` lines 936-936

> | 2 | PG11b | OAP line 35 "keep the literal scan (risk stated)"; ADV D2 option (a) | **(a) keep the literal text of spec 8.2** | The text stands as written: "The literal text of 8.2 stands. Known risk: ordinary words in model comments can block secondary coding." No spec or `s7_bundle.py` change. Advisor choice: NOT obtained (open advisor item). |

**B-D3. D3: option C.** *Source:* `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` lines 937-937

> | 3 | D3 | ADV D3: "(C) v2.7 plus the SF-first sentence, SF reported beside the four proportions (current interim rule)" | **C** (label and wording verified against the brief) | Text of the interim policy (MPDR MD-05): "A call that meets any SF definition is classified SF only. Main-run reporting follows §18.2 as written: SF calls stay in `n_calls`, the SF count and rate are reported beside the four proportions, no proportion is rescaled." Options L, P1, P2 and PF are not adopted. The source notes that C leaves "sum to 1" false when an SF occurs. No spec change. Advisor choice: NOT obtained. |

**B-D5. D5: re-code values.** *Source:* `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` lines 938-938

> | 4 | D5 | ADV D5; codebook section 5 | **Confirm the values as written:** sample 20 % with a floor of 20 per (family, condition) cell (all parseable responses if the cell has at most 20, otherwise max(20, ceil(0.20 x D_P))), delay of at least 14 full days, first-pass codes closed, columns `recode1_*` | Each value was verified against codebook section 5 (and against MPR D5 and record 12.21 row 6). One wording difference was found and judged equivalent: 12.21 row 6 says "fewer than 20" where the codebook says "at most 20"; at exactly 20 both give the same selection (all 20), so the rule is the same function. The codebook still reads as written; no value is changed. The values remain "delegated choices without an empirical basis" (codebook). Advisor approval of the values (recommended by the source): NOT obtained. |

**B-MD01. MD-01: SF2 = B/A2c, `f_S` per call, whitespace D2, Q6 = owner with advisor.** *Source:* `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` lines 939-939

> | 5 | MD-01 | OAP line 55: "adopt option B + D1-D8 + per-call unit" | **APPROVE**, namely: SF2 = option B / A2c (verified equal in the sources: C31 "proven equal to B"; MPDR: equal on an exhaustive 384-record grid; D1: SF2 when the call is not SF1 and not SF4 and the text contains no character outside the whitespace set of D2); **`f_S` per call** (D7: "`f_S` counts calls, not flags"); the whitespace set **D2** as written ("exactly space (U+0020), TAB, LF, VT, FF, CR"; U+00A0 and other Unicode spaces are content); **Q6 = owner together with advisor** | Options A1, A2a, A2b are not adopted; the per-flag `f_S` is not adopted. The owner's Q6 position is that the advisor takes part: the decision is therefore recorded as the owner's decision with **advisor concurrence PENDING**, not as final. Q5 (candidate indicator) is a separate box and is not decided here. No code change (`sf_flags` already implements B). |

**B-MD04. MD-04: procedure approved, list L-B, A-2 = exclude.** *Source:* `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` lines 955-955

> | 2 | MD-04, procedure box | **RECORDED: APPROVE procedure** by the owner; **advisor concurrence PENDING** (authority per source: "Owner + advisor.") | The source states that "its procedure can be approved now, but the official hash is computed only after the entries that change listed files are settled" and its box reads `[ ] APPROVE procedure  [ ] REJECT  [ ] AMEND: ______  | File list chosen ... | A-2 ...`. With the list L-B and A-2 = exclude (12.47) the owner's decision on MD-04 is now complete on the owner side; it is not final in the sense of the source until the advisor's concurrence exists. The procedure: the FZ hash = SHA-256 of a canonical index {path -> SHA-256} of the listed files, computed once before the first pilot call, stored as a new file, recorded in the decision record and every run manifest, recomputed by the tool (`verify`). **Not authorized by this approval:** computing or publishing the official FZ hash, activating `fz_index.py` (patch P5), gate enforcement (box E-1, pending), a freeze of any kind, a final freeze manifest, a pilot. **Outstanding dependencies for the official hash** (source: MD-01, MD-03, MD-05, MD-06, MD-07, MD-10): MD-01 owner-decided, advisor pending (12.47); MD-03 K2 chosen but not implemented, R-7 not authorized (row 4), verbs pending (row 3), advisor pending; PG11b (a) and D3 C owner-decided, advisor pending (12.47); MD-06 pending; MD-07 decided (12.46); MD-10 pending (row 5). |


## C. Review requests
**B1. PG3 review (before H1).** Do you concur with the owner's ratified reading of "contiguous" (one changed span), or do you object? *Source:* `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` lines 815-815

> | 5 | PG3 before H1 | **Ratified:** "contiguous" (spec 8.1 PG3, line 461) is read as one changed span, with every differing position inside the target token's span (spec 8.2 line 525 "a single changed span"; line 550 "only the target numeral may differ"); the shared decimal point inside the token does not break the span. The strict reading (consecutive positions) is not adopted. | The textual basis was checked: spec lines 461, 525 and 550, the implementation `research_design/step8/s8_gates.py` lines 94-100 and record 12.28 support the reading; no frozen provision was found that contradicts it. | No artifact is changed and no rebuild is needed (the Step 8 build was made under this reading). The text of record 12.28 ("clarification, advisor review pending") is unchanged: advisor review of PG3 remains pending and is not marked done. H1 is not opened by this entry: it still needs the other prerequisites (the researcher's R1, the open decisions listed in the owner package that can change a manifest-bound artifact). |

*Source:* `results_package_2026-10-13/ADVISOR_DECISION_BRIEF.md` lines 7-13

> ## D1. PG3: "contiguous" changed span  (before pilot: yes, it decides whether the built registry stands)
> - **Reference:** §8.1 row PG3 ("the set of differing character positions is contiguous and inside the target token's span"); §8.2 "a single changed span"; 12.28 (clarification taken, advisor review pending); `step8/s8_gates.py` (`pair_problems`); `main/gate_report.json` field `PG3_strict_nonconsecutive_pairs_informational` = 180 pairs.
> - **Problem:** read as consecutive character positions, 90 of the 104 MIL templates fail because the decimal point is shared (21.5 vs 22.4 differ in two non-adjacent characters). PAC never fails.
> - **Options:** (a) ratify the single-span reading as a clarification (record entry); (b) keep the strict reading: the build is rejected, which returns to step 3 or 7 (§21.2) with new MIL parameters or wording, and Steps 3 to 9 repeat; (c) amend the text of PG3 in a new methodology version.
> - **Consequences:** (a) none for the built artefacts; (b) invalidates the registry, the Step 8 output and Implementation B's agreement, and costs days; (c) as (a) but formal and slower.
> - **Recommendation:** (a), because §8.2 states the intent ("single changed span"), and (b) would reject the frozen design for a property of the decimal point rather than of leakage.
> - **Decision (advisor/owner):** ________________  **Date:** ________

Answer requested: concur / object (an objection returns to the strict reading with the consequences quoted: build rejected, steps 3-9 repeat, H1 void) / other. Why it matters: H1 should not be done on a build whose reading you may reject.
**B2. The reading of "used" (12.39 row 1).** Do you concur with the owner's provisional working interpretation? *Source:* `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` lines 825-825

> | 1 | Meaning of "used" for `s2_values` (spec 16.1, line 933(b)) | **Option A, broad reading, as a provisional working interpretation.** A numeral on the rule-parameter side of a comparison-like clause counts as a used value (933(b) "a side of a stated comparison") even when the clause's relation is outside the closed relation list. | Basis: 933(b) says "stated comparison", a term the specification does not define; it defines only "stated computation" (934) and "numerical comparison" (935). The closure of the list (935, codebook lines 62-85) is stated for "numerical comparison" and its stated reason concerns the evidence category; codebook lines 80-83 classify a clause with an unlisted relation as IV only through a used value or a derived quantity with provenance, which neither includes nor excludes such a numeral. 933(c) independently covers B37 ("the cap of 10% in week 3"). The battery's `used_ok` flags are consistent with this reading. Limits: it is a reading, not a codebook rule or amendment; the codebook, the battery, the expected codes, the registry and the Step 8 artifacts are unchanged; it does not decide `cv` versus `sw` (that needs the prompt) nor whether an unlabelled numeral such as "10%" is a rule parameter (also prompt-dependent); no sheet cell is changed and the classification of the sheet cells stays with the researcher. For coding of real responses the codebook text governs; any formal clarification needs a separate decision (codebook version). | Advisor review NOT obtained and not claimed. Possible tension to be reported: codebook line 46 and spec line 1001 say that where the codebook is silent a disagreement item is `unresolved`; the owner's working reading treats the point as resolvable by 933. If the advisor reads 933(b) narrowly, the six expected `cv` cells (B09, B20, B23, B32, B35, B38) become a battery question for the advisor (checklist step 8, answer (iii)), which would be a separate decision. |

**B3. Sufficiency of the rehearsal (12.39 row 3).** *Source:* `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` lines 827-827

> | 3 | Whether the `s2_values` and `s2_arith` comparisons are usable in a rehearsal without a prompt | **Option A.** Their interpretation is limited and the limitation is documented. | The raw agreement figures (`s2_values` 31/40 = 77.5%, `s2_arith` 24/40 = 60.0%) are kept as raw descriptive results only. They are not a measure of validity or reliability (OD-3: one human coder, no kappa; AI-exposed rehearsal; synthetic comments; the expected `cv`, `AC` and `AI` are fixed by item-level flags of the battery, not derived from the comment text). The rehearsal is not redesigned; the battery and the expected codes are unchanged. | Remains an OPEN QUESTION FOR THE ADVISOR: whether a rehearsal that cannot assess these two variables from text satisfies 12.38 row 4 (human rehearsal required before the coding procedure is declared validated). The human rehearsal remains an open advisor item of the Step 7 manifest; this entry does not mark it closed. |

Answer requested: satisfies / does not satisfy / satisfies with the limitation stated.
**B4. The H4 stop rule.** Choose (i), (ii) or (iii) (with the question for (iii)), together with the owner. *Source:* `results_package_2026-10-13/HUMAN_TASKS_H1_H7_OPERATIONAL_CHECKLIST.md` lines 91-91

> 8. **Stop rule before H3.** If any finding is class B or C, or you are unsure, do NOT create H3. Send the findings file to the owner and the advisor with this question: "(i) no change, the point is recorded as a limitation; (ii) a codebook revision (new Step 7 version, box R-7, rebuild sequence in `OWNER_APPROVAL_PACKAGE.md`); (iii) a question on the battery for the advisor." Nobody, including the assistant, edits the codebook or any manifest-bound file on the basis of the findings without that written decision. If there are no class B or C findings, H4 does not block H3. H1 does not depend on H4.

*Source:* `results_package_2026-10-13/human_evidence/rehearsal/rehearsal_findings.md` lines 93-96

> ## 7. Open items and stop rule
>
> - **Stop rule (checklist step 8) applies.** Class B cells exist and two cells are unclassified. H3 is not created. The findings go to the owner and the advisor with the question: (i) no change, recorded as a limitation; (ii) a codebook revision (new Step 7 version, box R-7, rebuild sequence of `OWNER_APPROVAL_PACKAGE.md`); (iii) a question on the battery for the advisor.
> - **Advisor input not yet requested and not claimed:** the reading of "used" (12.39 row 1; tension with codebook line 46 and spec 1001, where a silent codebook leads to `unresolved`); whether a rehearsal that cannot assess `s2_values`/`s2_arith` from text satisfies 12.38 row 4; whether the advisor must also be involved in 12.39 row 2 (unconfirmed). The human rehearsal remains an open advisor item of the Step 7 manifest.

The researcher's classification of the two `SW` cells (B10, B36) is not available yet and is not asked of you.
**B6. MD-10: review of the Step 8 choices of record 12.28.** The sentence in the project documents is: *Source:* `results_package_2026-10-13/MASTER_PROPOSED_DECISION_RECORD.md` lines 186-189

> ### MD-10 Confirmations of earlier choices (C-20, C-21, C-22, C-24, C-25, C-28)
> Text: "(PC-2) the pilot registry is built and gated at step 8; (I-6) informational diagnostic, gate counts stay 30 and 14; (P-3 item 1) `s2_values` 'none' is reported as a count outside its denominator; (F-3) closed; (PRD-8) unchanged; the Step 8 choices of record 12.28 (F-4 architecture, PG4 test, PG11a projection bundle of 624 files, A6b actor) are confirmed / amended: ______."
>
> - **Owner decision: PENDING | Advisor decision: PENDING | Date: PENDING | Option chosen: PENDING**

That sentence names a count "14" that no project source defines; the verified results in record 12.28 are "30 numeric gates" (main and pilot registers) and the rendering-stage gate list. **Owner-requested wording proposal (NOT adopted, NOT recorded, awaiting the owner's confirmation):** "(PC-2) the pilot registry is built and gated at step 8; (I-6) informational diagnostic, an informational count only (record 12.28), the gate results standing as reported in record 12.28 (30 numeric gates PASS on the generator's templates and on Implementation A's builders; PG1-PG10, PG11a, the PG11b builder test, PG12, A1b and A6b PASS on all 1,248 main and 96 pilot prompts); (P-3 item 1) `s2_values` 'none' is reported as a count outside its denominator; (F-3) closed; (PRD-8) unchanged; the Step 8 choices of record 12.28 (F-4 architecture, PG4 test, PG11a projection bundle of 624 files, A6b actor) are confirmed / amended: ______." Note: confirming would close F-3 (the record lists it as open) and leave PRD-8 unchanged; both are decisions, not findings. Answer requested: review of the Step 8 choices and of the wording; confirm / amend per item (amendment wording must come with the answer).
**B7. C-31/C-32 questions still open (Q6 answered by the owner: owner together with the advisor).** Q1-Q3 are covered by the recorded MD-01 choice in B-MD01. Open:
*Source:* `results_package_2026-10-13/C31_C32_OWNER_DECISION_BRIEF.md` lines 92-92

> - **Q4.** Should a record with no HTTP status and no error marker stop the run for review (MD-06) or be classified by D1/D3?

*Source:* `results_package_2026-10-13/C31_C32_OWNER_DECISION_BRIEF.md` lines 93-93

> - **Q5.** Should the adapter store a candidate indicator so that "no candidate" and "candidate without text and without finish reason" can be told apart (D6)? An adapter change needing its own acceptance tests.


## D. Reserved for the owner (not put to the advisor)
Class ratification (none now, 12.44), P13 (12.44), X-4b (12.45), MD-02 (12.48), PRD-6/H7 and MD-09 (deferred, 12.47), the H5 authorization, R-7 (not authorized, 12.48), the code-freeze declaration and the pilot start.

## E. Source recovery notes
`H4_ADVISOR_DECISION_REQUEST_READY_2026-10-14.md` does not exist in the repository; the original numbering of the checklist's "Q1-Q5" is `SOURCE TEXT REQUIRED`; every question above is rebuilt from the primary sources named.
