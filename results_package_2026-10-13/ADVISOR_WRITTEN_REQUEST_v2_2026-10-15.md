# Written advisor request, version 2 (prepared 2026-10-15T03:32:40Z)

**DELIVERY STATUS: NOT SENT, BLOCKED (no verified advisor recipient or channel; see part E).** This is the finalized content. The earlier draft `ADVISOR_WRITTEN_REQUEST_DRAFT_2026-10-15.md` is preserved unchanged (sha256 `9f677451cc9b391d34ae8a98a8de0b88d88b6cf21e6c26e6ecae13d523af26a7`). In this version every quotation is extracted by script from the file and lines named, so it is exact; the earlier draft's quotations were re-checked mechanically and 2 of them were not verbatim (the PG3 sentence of 12.38 row 5, which had its quotation marks changed and was shortened with an ellipsis, and the joined cells of the 'I-6 ...' row), which is why this version replaces them.

**Proposed subject line:** "Written input requested: pre-pilot decisions of the scenario-construction study (specification v2.7)".

**Suggested cover note (the owner edits and sends):** "Dear <advisor>, part B lists the points on which a written answer from you is needed before the pilot can proceed; each item quotes the project's own text and says what is asked. Part A is for information only. Part C lists matters that the owner decides and that are not put to you. No decision in this message has been taken on your behalf, and no draft or recommendation quoted here is adopted. Please reply item by item; silence will not be read as agreement."

**Note for the reader:** some quoted project sections (the advisor brief D1-D5) contain the project assistant's own "Recommendation" lines and blank "Decision" lines. They are quoted unchanged because they are part of the source text; they are NOT adopted, NOT endorsed by the owner, and you are not asked to confirm them: please state your own view.

## A. For information (no answer requested)
Owner decisions recorded on 2026-10-15 in `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md`, entries 12.40-12.45: resume after interruption or halt (a call with an intent and no stored result is never resumed or repeated; no HTTP status qualifies; no exception class is ratified now; resume after a killed process only on persisted evidence of a transport failure with the whole run free of other structural failures; the owner alone authorises a resume and the advisor is informed through the run report, which is notification and not approval; only pure implementation fixes meeting H1-H4; the US$100 cost stop is a distinct halt cause that spec 13.8 does not list); a coarse failure category is recorded for exception failures; the 31-file list of the final-freeze tool was approved by the owner; for a change made after the code freeze, raw-record fields are not counted among the outputs observed by H2 (a limited decision, not an H2 attestation). Nothing in part A asks for approval.

## B. Questions that need the advisor's written answer
For each: the question, the verbatim source text, where it is, why the advisor's input is needed, the answer requested, and the related owner decision (which the advisor is not asked to override).

### B1. PG3 review
**Question to answer:** Do you concur with reading "contiguous" in PG3 as one changed span with every differing position inside the target token's span, or do you object?
*Source:* `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` lines 815-815

> | 5 | PG3 before H1 | **Ratified:** "contiguous" (spec 8.1 PG3, line 461) is read as one changed span, with every differing position inside the target token's span (spec 8.2 line 525 "a single changed span"; line 550 "only the target numeral may differ"); the shared decimal point inside the token does not break the span. The strict reading (consecutive positions) is not adopted. | The textual basis was checked: spec lines 461, 525 and 550, the implementation `research_design/step8/s8_gates.py` lines 94-100 and record 12.28 support the reading; no frozen provision was found that contradicts it. | No artifact is changed and no rebuild is needed (the Step 8 build was made under this reading). The text of record 12.28 ("clarification, advisor review pending") is unchanged: advisor review of PG3 remains pending and is not marked done. H1 is not opened by this entry: it still needs the other prerequisites (the researcher's R1, the open decisions listed in the owner package that can change a manifest-bound artifact). |

*Source:* `results_package_2026-10-13/ADVISOR_DECISION_BRIEF.md` lines 7-13

> ## D1. PG3: "contiguous" changed span  (before pilot: yes, it decides whether the built registry stands)
> - **Reference:** §8.1 row PG3 ("the set of differing character positions is contiguous and inside the target token's span"); §8.2 "a single changed span"; 12.28 (clarification taken, advisor review pending); `step8/s8_gates.py` (`pair_problems`); `main/gate_report.json` field `PG3_strict_nonconsecutive_pairs_informational` = 180 pairs.
> - **Problem:** read as consecutive character positions, 90 of the 104 MIL templates fail because the decimal point is shared (21.5 vs 22.4 differ in two non-adjacent characters). PAC never fails.
> - **Options:** (a) ratify the single-span reading as a clarification (record entry); (b) keep the strict reading: the build is rejected, which returns to step 3 or 7 (§21.2) with new MIL parameters or wording, and Steps 3 to 9 repeat; (c) amend the text of PG3 in a new methodology version.
> - **Consequences:** (a) none for the built artefacts; (b) invalidates the registry, the Step 8 output and Implementation B's agreement, and costs days; (c) as (a) but formal and slower.
> - **Recommendation:** (a), because §8.2 states the intent ("single changed span"), and (b) would reject the frozen design for a property of the decimal point rather than of leakage.
> - **Decision (advisor/owner):** ________________  **Date:** ________

**Why the advisor:** the record states that advisor review of PG3 remains pending (quoted above); `MASTER_PROPOSED_DECISION_RECORD.md` assigns MD-05 to "owner + advisor". **Answer requested:** concur / object (an objection returns to the strict reading, with the consequences in the quoted D1) / other. **Related owner decision:** ratified by the owner in 12.38 row 5; the advisor is asked to review, not to be bound by it.

### B2. The reading of "used" (12.39 row 1)
**Question to answer:** Do you concur with the owner's provisional working interpretation of "used" for `s2_values`, or do you read it differently?
*Source:* `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` lines 825-825

> | 1 | Meaning of "used" for `s2_values` (spec 16.1, line 933(b)) | **Option A, broad reading, as a provisional working interpretation.** A numeral on the rule-parameter side of a comparison-like clause counts as a used value (933(b) "a side of a stated comparison") even when the clause's relation is outside the closed relation list. | Basis: 933(b) says "stated comparison", a term the specification does not define; it defines only "stated computation" (934) and "numerical comparison" (935). The closure of the list (935, codebook lines 62-85) is stated for "numerical comparison" and its stated reason concerns the evidence category; codebook lines 80-83 classify a clause with an unlisted relation as IV only through a used value or a derived quantity with provenance, which neither includes nor excludes such a numeral. 933(c) independently covers B37 ("the cap of 10% in week 3"). The battery's `used_ok` flags are consistent with this reading. Limits: it is a reading, not a codebook rule or amendment; the codebook, the battery, the expected codes, the registry and the Step 8 artifacts are unchanged; it does not decide `cv` versus `sw` (that needs the prompt) nor whether an unlabelled numeral such as "10%" is a rule parameter (also prompt-dependent); no sheet cell is changed and the classification of the sheet cells stays with the researcher. For coding of real responses the codebook text governs; any formal clarification needs a separate decision (codebook version). | Advisor review NOT obtained and not claimed. Possible tension to be reported: codebook line 46 and spec line 1001 say that where the codebook is silent a disagreement item is `unresolved`; the owner's working reading treats the point as resolvable by 933. If the advisor reads 933(b) narrowly, the six expected `cv` cells (B09, B20, B23, B32, B35, B38) become a battery question for the advisor (checklist step 8, answer (iii)), which would be a separate decision. |

*Source:* `results_package_2026-10-13/human_evidence/rehearsal/H4_STATUS_AND_BLOCKERS_2026-10-14.md` lines 1-12

> # H4 status and blockers (2026-10-14)
>
> Status note (not an official record). H4 comparison and findings: DONE as documents (`comparison.json`, `rehearsal_findings.md`). H4 is NOT cleared for H3: the stop rule (checklist step 8) holds because class B cells exist and two `SW` cells are unclassified. `NEXT_ACTIONS.md` row B5 ("comparison done, disagreements noted for the advisor") is superseded by this note; that file was not edited.
>
> ## Unmet H4 prerequisites
> | Item | Blocker | Who can clear it |
> |---|---|---|
> | Owner/advisor answer to the findings (checklist step 8: (i) limitation, (ii) codebook revision, (iii) battery question) | no written answer exists | owner and advisor |
> | Advisor input on the reading of "used" (12.39 row 1) and on sufficiency without a prompt (12.39 row 3) | not requested; no message sent | owner sends; advisor answers |
> | Whether the advisor must also decide 12.39 row 2 | authority unconfirmed (12.38 row 3 names no decider) | owner |
> | Basis of `SW` on B10 and B36 | not recoverable from records | researcher (only if they can state it) |
> | Advisor review of PG3 (record 12.28) | pending; owner ratified the reading in 12.38 row 5 | advisor |

**Why the advisor:** `H4_STATUS_AND_BLOCKERS_2026-10-14.md` lists "Advisor input on the reading of 'used' (12.39 row 1)" as an unmet H4 prerequisite (quoted above, table row). **Answer requested:** concur / other reading. **Related owner decision:** provisional working interpretation, recorded in 12.39 row 1.

### B3. Sufficiency of the rehearsal (12.39 row 3)
**Question to answer:** Does a rehearsal that cannot assess `s2_values` and `s2_arith` from the comment text satisfy the requirement that a human rehearsal be completed before the coding procedure is declared validated?
*Source:* `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` lines 827-827

> | 3 | Whether the `s2_values` and `s2_arith` comparisons are usable in a rehearsal without a prompt | **Option A.** Their interpretation is limited and the limitation is documented. | The raw agreement figures (`s2_values` 31/40 = 77.5%, `s2_arith` 24/40 = 60.0%) are kept as raw descriptive results only. They are not a measure of validity or reliability (OD-3: one human coder, no kappa; AI-exposed rehearsal; synthetic comments; the expected `cv`, `AC` and `AI` are fixed by item-level flags of the battery, not derived from the comment text). The rehearsal is not redesigned; the battery and the expected codes are unchanged. | Remains an OPEN QUESTION FOR THE ADVISOR: whether a rehearsal that cannot assess these two variables from text satisfies 12.38 row 4 (human rehearsal required before the coding procedure is declared validated). The human rehearsal remains an open advisor item of the Step 7 manifest; this entry does not mark it closed. |

**Why the advisor:** the record itself labels it "an OPEN QUESTION FOR THE ADVISOR". **Answer requested:** satisfies / does not satisfy / satisfies with the limitation stated. **Related owner decision:** 12.39 row 3 (Option A, limitation documented); 12.38 row 4 (rehearsal required).

### B4. The H4 stop rule
**Question to answer (the project's own wording is quoted; select one):**
*Source:* `results_package_2026-10-13/HUMAN_TASKS_H1_H7_OPERATIONAL_CHECKLIST.md` lines 91-91

> 8. **Stop rule before H3.** If any finding is class B or C, or you are unsure, do NOT create H3. Send the findings file to the owner and the advisor with this question: "(i) no change, the point is recorded as a limitation; (ii) a codebook revision (new Step 7 version, box R-7, rebuild sequence in `OWNER_APPROVAL_PACKAGE.md`); (iii) a question on the battery for the advisor." Nobody, including the assistant, edits the codebook or any manifest-bound file on the basis of the findings without that written decision. If there are no class B or C findings, H4 does not block H3. H1 does not depend on H4.

*Source:* `results_package_2026-10-13/human_evidence/rehearsal/rehearsal_findings.md` lines 93-96

> ## 7. Open items and stop rule
>
> - **Stop rule (checklist step 8) applies.** Class B cells exist and two cells are unclassified. H3 is not created. The findings go to the owner and the advisor with the question: (i) no change, recorded as a limitation; (ii) a codebook revision (new Step 7 version, box R-7, rebuild sequence of `OWNER_APPROVAL_PACKAGE.md`); (iii) a question on the battery for the advisor.
> - **Advisor input not yet requested and not claimed:** the reading of "used" (12.39 row 1; tension with codebook line 46 and spec 1001, where a silent codebook leads to `unresolved`); whether a rehearsal that cannot assess `s2_values`/`s2_arith` from text satisfies 12.38 row 4; whether the advisor must also be involved in 12.39 row 2 (unconfirmed). The human rehearsal remains an open advisor item of the Step 7 manifest.

**Why the advisor:** the checklist directs the question to "the owner and the advisor" and H3 may not be created while the rule holds. **Answer requested:** (i), (ii) or (iii), with the battery question if (iii). **Related owner decision:** none yet (`OWNER_APPROVAL_PACKAGE.md` row 7: owner choice pending). **Missing input, not the advisor's:** the researcher's classification of the open `SW` cells.

### B5. The four open advisor items of the Step 7 manifest
**Question to answer:** For each of the four items, which of the options described in the project documents do you advise?
*Source:* `research_design/step7/STEP7_PROMPT_SPECIFICATION_FREEZE_MANIFEST_v1.json` lines 213-218

>  "open_advisor_items": [
>   "SF/UNP main-run policy (Policy 1 / Policy 2 / interim = v2.7 as written)",
>   "PG11b scan scope (literal text may reject ordinary response words; post-run only)",
>   "delegated re-code values and the section 16.3 departures (codebook 5.3)",
>   "human rehearsal of the codebook battery (section 13.5, before the pilot; not done)"
>  ],

Options and evidence per item: SF/UNP policy *Source:* `results_package_2026-10-13/ADVISOR_DECISION_BRIEF.md` lines 23-29

> ## D3. Structural failures and UNP in the main run  (before main run; before FZ hash because §18 is in FZ)
> - **Reference:** §13.4 (SF1-SF5, UNP), §13.6, §13.8, §18.2 (four proportions over all `n_calls`, "sum to 1"), §22 item 6; 12.18 row 1 (pilot rule); 12.24 decision 1 (Policy 1 proposed); 12.26 item 1 (owner kept v2.7 as written); `PROPOSED_AMENDMENT_18_2_DRAFT_v1.md`; `POLICY_2_METHODOLOGY_DECISION_PACKAGE_DRAFT_v1.md`.
> - **Problem:** under the literal text SF2 and SF3 without a verdict also meet the UNP definition; 12.18 row 1 fixes SF-first precedence for the pilot only. With an SF call in a main cell the four proportions cannot sum to 1.
> - **Options:** (L) literal text, overlap unresolved; (C) v2.7 plus the SF-first sentence, SF reported beside the four proportions (current interim rule); (P1) evaluable-call denominators plus a separate SF rate; (P2) SF as a fifth class over planned calls; (PF) parse-first.
> - **Consequences:** L and PF contradict 12.18 row 1. C needs no amendment but leaves "sum to 1" false when an SF occurs. P1 contradicts §12 ("over all R calls") and leaves cluster means undefined. P2 keeps §12 intact, sums to 1, matches the halting monitor, and needs an amendment, a call ledger and a counting sentence.
> - **Recommendation:** C for the pilot and the first main run (it needs nothing); P2 if the advisor wants a clean "sums to 1" statement, adopted before the FZ hash.
> - **Decision:** ________________  **Date:** ________

PG11b *Source:* `results_package_2026-10-13/ADVISOR_DECISION_BRIEF.md` lines 15-21

> ## D2. PG11b scan scope  (before FZ hash: the bundle builder is an FZ item, 12.14)
> - **Reference:** §8.2 rows PG11a/PG11b ("no pattern PT1, PT3-PT8b occurs in any file name, file body or directory name"); §21.2 row 6; 12.26 item 2 (owner kept the literal text); `step7/s7_bundle.py` lines 30, 64-98; `test_step7.py` `test_D1_pt4_is_in_the_pg11_scan`.
> - **Problem:** the post-run application check scans model-written text. In an in-memory test with synthetic strings, ordinary words such as "CLEAR", "PAC", "(valid)", "class = A" were rejected, and rebuilding cannot help. The effect would be to block the secondary S2/S3 coding; primary results are unaffected.
> - **Options:** (a) keep literal (current); (b) amend to scan names, directory names, skeleton and prompt part only; (c) amend to scan response text only for machine-form patterns; (d) mask matches in the builder (changes what coders see).
> - **Consequences:** (a) risk of blocked coding, no cost now; (b), (c), (d) need a new methodology version and a Step 7 re-freeze before the FZ hash; (d) alters coder material and is the hardest to defend.
> - **Recommendation:** (a) for the first run if the timeline matters, accepting the risk in writing; (c) if the advisor wants S2/S3 coding protected. The choice should be made before the FZ hash because a later change is an FZ change.
> - **Decision:** ________________  **Date:** ________

Re-code values and 16.3 departures *Source:* `results_package_2026-10-13/ADVISOR_DECISION_BRIEF.md` lines 39-45

> ## D5. Re-code values and the departures from §16.3  (before FZ hash: the codebook is an FZ item; before S2/S3 coding at the latest)
> - **Reference:** §16.3 lines 997-1003; OD-3 (`STEP2_OWNER_DECISIONS_RECORD.md`: one coder, no inter-rater reliability or kappa claim); 12.21 row 6; 12.24 decision 2; 12.26 item 3; codebook revision 5 section 5.3; `step7/s7_recode.py`.
> - **Problem:** the delegated procedure uses a 20 % sample (floor 20), 14 days, `recode1_*` columns and no kappa; §16.3 states no sample, no delay, names `coder1_*`/`coder2_*` and says kappa is reported.
> - **Options:** (a) approve the delegated values and record the departures; (b) re-code every coded response and report kappa labelled "intra-rater consistency, no reliability claim"; (c) other values.
> - **Consequences:** (a) fastest, weakest evidence; (b) closest to the literal text and OD-3's wording (OD-3 forbids claims, not computation), larger workload and a change to `s7_recode.py`; the owner chose (a) on 2026-10-13 pending the advisor.
> - **Recommendation:** (a), with the advisor's explicit approval of the 14-day delay and the sample.
> - **Decision:** ________________  **Date:** ________

**Why the advisor:** the manifest lists them as open advisor items (quoted); the briefs name the advisor. The fourth (human rehearsal) is addressed by B3/B4. **Answer requested:** one choice per item among the options quoted; where the project documents lack wording for an option (K3 threshold, K4 wording, PG11b alternatives (b)-(d), final P2/PF wording, alternative re-code values) the option cannot be chosen until it is written: `SOURCE TEXT REQUIRED` (see the owner briefs `owner_decision_briefs_2026-10-15/`). **Related owner decisions:** none taken on these items; they remain with the owner and the advisor jointly.

### B6. MD-10: review of the Step 8 choices of record 12.28
**Question to answer:** Do you confirm, or do you want amended, each item named in the quoted text?
*Source:* `results_package_2026-10-13/MASTER_PROPOSED_DECISION_RECORD.md` lines 186-189

> ### MD-10 Confirmations of earlier choices (C-20, C-21, C-22, C-24, C-25, C-28)
> Text: "(PC-2) the pilot registry is built and gated at step 8; (I-6) informational diagnostic, gate counts stay 30 and 14; (P-3 item 1) `s2_values` 'none' is reported as a count outside its denominator; (F-3) closed; (PRD-8) unchanged; the Step 8 choices of record 12.28 (F-4 architecture, PG4 test, PG11a projection bundle of 624 files, A6b actor) are confirmed / amended: ______."
>
> - **Owner decision: PENDING | Advisor decision: PENDING | Date: PENDING | Option chosen: PENDING**

*Source:* `results_package_2026-10-13/ADVISOR_DECISION_BRIEF.md` lines 79-80

> | PC-2: step at which the pilot registry is first built | §19.3; 12.23 table; 12.28 (reading taken) | confirm the reading |
> | I-6 six-reading check; F-3; PRD-8 | 12.23 table; 12.28 | confirm "informational" / current handling |

**Why the advisor:** the text asks for "an advisor review of them before the FZ hash". **Answer requested:** confirm / amend per item (amendment wording must come with the answer, since none is written). **Related owner decision:** none.

### B7. Conditional: the C-31/C-32 questions
Send this item only if the owner confirms that the advisor is to be asked (Q6 below is the owner's to settle first); if the owner decides alone, withdraw B7.
*Source:* `results_package_2026-10-13/C31_C32_OWNER_DECISION_BRIEF.md` lines 88-96

> ## 8. Explicit questions for the owner / advisor
> - **Q1.** Which reading of §13.4 line 810 versus §13.6 lines 830-831 is intended for a call that is an HTTP error, a timeout or a block **and** has an empty body? **B/A2c** (the error or block explains the empty body: SF1/SF4 only), **A2a**, or **A1**.
> - **Q2.** Is `f_S` a count of calls (working decision) or of flags? (Only matters for SF1+SF4 on one call.)
> - **Q3.** Is the whitespace set D2 accepted, or is a Unicode definition wanted? (A U+00A0-only body is today UNP, not SF2.)
> - **Q4.** Should a record with no HTTP status and no error marker stop the run for review (MD-06) or be classified by D1/D3?
> - **Q5.** Should the adapter store a candidate indicator so that "no candidate" and "candidate without text and without finish reason" can be told apart (D6)? An adapter change needing its own acceptance tests.
> - **Q6.** Who decides: owner only, or owner and advisor? (MD-01 in `MASTER_PROPOSED_DECISION_RECORD.md` names both.)
>
> Decision fields: **Owner: PENDING | Advisor: PENDING | Date: PENDING | Option chosen: PENDING | Edits: PENDING**.

**Why the advisor:** `MASTER_PROPOSED_DECISION_RECORD.md` MD-01 names both owner and advisor. **Answer requested:** Q1-Q5 as worded. **Note:** these are the only numbered "Q1-Q5" questions found in the repository for the owner/advisor; whether the checklist's "Q1-Q5" means these or the five topics B1-B3 was not verifiable.

## C. Reserved for the owner (not put to the advisor)
Class ratification (deferred by the owner, 12.44), the P13 list (approved, 12.44), X-4b (12.45), PRD-6/H7, MD-02, the H5 authorization, the code-freeze declaration, the pilot start, and whether the advisor must also be involved in 12.39 row 2 ("whether the advisor must also be involved is NOT confirmed"). Briefs for the owner's pending decisions: `owner_decision_briefs_2026-10-15/INDEX.md`.

## D. Source recovery for the missing request text
- `H4_ADVISOR_DECISION_REQUEST_READY_2026-10-14.md`: searched again by name in the whole repository on 2026-10-15T03:32:40Z: **not present**. Its text and the original numbering of the checklist's "Q1-Q5" are therefore `SOURCE TEXT REQUIRED`; the content above is rebuilt from primary sources only (the record, the Step 7 manifest, the checklist, the briefs). The five topics the checklist names ("reading of 'used', `s2_arith` without a prompt, sufficiency of the rehearsal, role in 12.39, PG3 review") map to B2, 12.39 row 2 (owner decided Option A; see C), B3, 12.39 row 2 authority (C) and B1.
- Nothing else is marked `SOURCE TEXT REQUIRED` in parts A-C.

## E. Delivery
Recipient and channel: **NOT VERIFIED.** The repository names no advisor and no contact (`paper/PAPER_DRAFT.md` line 13: "[CO-AUTHOR / SUPERVISOR NAMES — TO BE COMPLETED]"; `paper/PAPER_GAPS.md` line 52 lists the supervisor and e-mail as missing). The tools available to the assistant in this session are Apollo (a sales-outreach product, not a project channel) and session messaging; no project communication integration is configured. Sending was therefore NOT attempted. Human input needed: the advisor's name and the official channel.
