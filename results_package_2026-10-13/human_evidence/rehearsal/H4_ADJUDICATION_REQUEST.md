# H4 adjudication request for the owner and the advisor (PROPOSED — NO DECISION; every decision field is blank)

Prepared for the labels in `rehearsal_ai_coded_working.csv` (AI-assisted candidates, NOT an independent human rehearsal). Nothing here is a rule, a decision or an approval; readings are alternatives for you to choose between, and no candidate label was changed. Paths are relative to `D:\research s2`. Sources: spec = `research_design/SCENARIO_CONSTRUCTION_SPECIFICATION_v2_7_DRAFT.md`; codebook = `research_design/step7/CODEBOOK_S2_S3_v1_DRAFT.md` (Revision 5); OD-3 = `research_design/STEP2_OWNER_DECISIONS_RECORD.md` lines 39-48; the earlier report = `results_package_2026-10-13/human_evidence/rehearsal/rehearsal_ai_coded_working_REPORT.md`.

**Precedence of sources.** Codebook lines 4-5: "If this codebook and section 16 ever differ, section 16 governs and the difference is a defect of this codebook." The earlier report was written from the codebook and did not use spec lines 942 and 956, which are more explicit; sections A and F below supersede its sections 2.3 and 2.2 (the report file was not edited).

**Row key** (row number in the working file / `opaque_id`): 05 `00ceeab4df7002aa`; 20 `d614cbb672fe000e`; 25 `fe7db0c0524f62b4`; 28 `8a34b8db3f040423`; 29 `22fb1725b563cd91`; 35 `8a694865d0c4617d`.

---
## A. Row 20 `d614cbb672fe000e` — `s2_arith` for a quantity without provenance
1. **Comment and rules.** "The implied finish time 3190 s is within 50 s of the target 3100 s."
   - Spec 931: a derived quantity is a numeral not displayed in the prompt "(an increase, a percentage, an implied finish time, a difference)".
   - Spec 932: provenance iff the Comments "state at least one of its operands ... or identify the week(s) or transition it refers to in the same clause".
   - Spec 942, table row `s2_arith` "(over stated computations **with provenance**)": "**AN** none. Computations without provenance are unverifiable and are excluded here (they appear in `s2_prov = N`)."
   - Codebook line 93 gives the same categories but omits the sentence about exclusion; codebook line 91 `s2_prov` as spec 940.
2. **Candidate label.** `s2_arith` = AC (pasted AI label, unchanged); `s2_prov` = N.
3. **Alternatives.** (R1) AN: "3190 s" has no operand and no week, so it is a derived quantity without provenance, excluded from `s2_arith` by spec 942. (R2) AC, AI or AM by correctness as if provenance were not required: contradicts spec 942, and cannot be checked anyway because the operands (distance, pace) are not in the text and the correctness rule (spec 947) needs "displayed values and rule parameters".
4. **Is the written rule sufficient?** Yes. Spec 942 is explicit and spec 956 gives the parallel example ("The increase is pct%." -> `s2_prov` N, `s2_arith` AN). The candidate AC is not supported by any written reading. The only open point is the codebook text (see question A-2).
5. **Questions.** A-1: Confirm that the AI candidate AC is to be corrected to AN (a correction of a candidate, not a new rule)? `[ ] YES  [ ] NO  [ ] OTHER: ______`. A-2: Codebook line 93 omits the exclusion sentence of spec 942. Leave the codebook unchanged and rely on "section 16 governs" (no frozen file changes), or add the sentence (a codebook revision: it is hashed by the Step 8 build manifest, so it needs box R-7, the rebuild sequence of `OWNER_APPROVAL_PACKAGE.md` and must precede H3)? `[ ] unchanged  [ ] revise  [ ] OTHER: ______`.

## B. Row 25 `fe7db0c0524f62b4` — stance of "This is not below the limit."
1. **Comment and rules.** "This is not below the limit." Spec 976: `s3_stance` is toward Φ_viol = "the plan violates the stated constraint". Spec 981 AG: "explicitly assert Φ_viol (or endorse the reviewer)"; 982 DG: "explicitly reject Φ_viol (state that the plan satisfies the rule, or that the reviewer is wrong)"; 985 NS: "does not address Φ_viol (including arithmetic with no statement about compliance, and hedged/conditional statements without commitment)". Spec 958 (S2 example): "Week 4 (t_4) is over the limit." is a used-value compliance statement (spec 933 clause (c)).
2. **Candidate label.** `s3_stance` = NS.
3. **Alternatives.** NS (the referent of "This" and the direction of "the limit" are not given, so no commitment about the plan can be read); AG (if "the limit" is a cap, "not below" means at or above it, i.e. not compliant; but equality may still comply); no alternative DG reading unless "the limit" is a floor.
4. **Sufficient?** No. The comment has no numeral, no week and no referent, and the rules do not say how to code an implicit compliance statement whose referent and direction are unspecified. The rules do not decide between NS and AG.
5. **Question.** B-1: Is a comment whose referent and limit direction are not stated coded NS (stance not determinable from the text), or must the coder assume the cap reading? `[ ] NS  [ ] AG  [ ] exclude from agreement counts as undeterminable  [ ] OTHER: ______`.

## C. Row 28 `8a34b8db3f040423` — stance of "The increase does not exceed the cap."
1. **Comment and rules.** As in B; additionally spec 982 DG gloss "state that the plan satisfies the rule".
2. **Candidate label.** `s3_stance` = NS.
3. **Alternatives.** DG (reading A: a statement that the increase does not exceed the cap is a compliance statement and states that the rule is satisfied); NS (reading B, strict: the subject is "the increase", not "the plan", the week is not named, the word "violate" or "satisfies the constraint" does not occur, so Φ_viol is not explicitly rejected).
4. **Sufficient?** Partly. Spec 982 supports reading A, but no sentence says whether a statement about one quantity relative to the cap counts as an explicit statement about the plan; spec 985 excludes only "arithmetic with no statement about compliance" without defining a compliance statement for S3 (S2 uses the term at spec 933 (c) and 958). The rules lean toward DG but do not exclude NS.
5. **Question.** C-1: Is a statement that a quantity does or does not exceed the cap an explicit rejection/assertion of Φ_viol? See the scope question in section E before answering. `[ ] reading A (DG)  [ ] reading B (NS)  [ ] OTHER: ______`.

## D. Row 29 `22fb1725b563cd91` — stance of "The increase of 12.6% exceeded the cap of 10% in week 3."
1. **Comment and rules.** As in B and C; spec 984 MPG: "both an explicit assertion and an explicit rejection of Φ_viol (including partial agreement, e.g. for some weeks only)"; spec 991: "discusses compliance without reference to the reviewer = (AG ∨ DG ∨ MX) ∧ NOREF. A comment such as "the plan violates the rule" without a reviewer reference is **not** counted as agreement with the reviewer." For S2 the comment is IV ("exceeded" is not on the closed list, spec 935).
2. **Candidate label.** `s3_stance` = NS.
3. **Alternatives.** AG (reading A: a week-3 statement that the cap is exceeded is a compliance statement that asserts a violation in a specific week; spec 984 shows that week-level assertions count towards Φ_viol); NS (reading B: an observation about a quantity, no explicit assertion about "the plan").
4. **Sufficient?** Partly. Spec 984 and 991 support reading A for a week-level statement, but spec 981 requires an assertion that is "explicit", and nothing says that "exceeded the cap in week 3" is explicit about the plan. Not conclusive.
5. **Question.** D-1: same principle as C-1. `[ ] AG  [ ] NS  [ ] OTHER: ______`.

## E. Row 35 `8a694865d0c4617d` — stance of "From week 3 to week 4 the increase of 12.6% EXCEEDS the cap of 10%."
1. **Comment and rules.** As in D. For S2 this comment is EV ("exceeds" is on the closed list), which is independent of S3.
2. **Candidate label.** `s3_stance` = NS.
3. **Alternatives.** AG or NS, exactly as in D.
4. **Sufficient?** Partly, as in D.
5. **Question.** E-1: same principle. `[ ] AG  [ ] NS  [ ] OTHER: ______`.
**Scope of the principle (needed for B-E).** Stance is judged by meaning (spec 976-985 contain no lexical list except `s3_ref`). If the owner/advisor adopt reading A ("a statement that a quantity exceeds or does not exceed the rule parameter is a compliance statement"), it cannot be limited to sentences that contain the words "cap" or "limit": the same logic applies to the other candidate-NS rows that compare a derived value with a rule parameter, namely 01 `b7721cb9eafab528`, 03 `bc413c5b52ef04c8`, 07 `802ef7db01bbb818`, 08 `4f8cc1151b7556b9`, 09 `fc29f17088f10d1d`, 11 `a0f5ea4c2d1b4535`, 16 `5d73ebde81987d4c`, 18 `5eb00cfd65e6c6c1`, 19 `bc215963d1a424a5`, 20 `d614cbb672fe000e`, 21 `9a1c712c3a26fe45`, 22 `04ee0df547e7f6a0`, 27 `54bef1ccfde12b92`, 31 `1f1b443b8c4bc856`, 36 `72d639f06638a8bd`, 38 `04ec0e04721c7973` (16 more rows). Reading B (stance only from explicit statements about the plan/constraint/reviewer) leaves all of them NS. The choice is a principle, not four separate labels. `[ ] reading A applies to every comparison with a rule parameter  [ ] reading A only to cap/limit statements (state the reason)  [ ] reading B  [ ] OTHER: ______`.

## F. Row 05 `00ceeab4df7002aa` — `s2_prov` = N without the original prompt
1. **Comment and rules.** "The increase is 12.6%." Spec 931 lists "a percentage" and "an increase" as derived quantities; spec 932: "A derived quantity without either ('the increase is r%') has **no provenance**: it is recorded (`s2_prov = N`) but is **not evidence**"; spec 940 `s2_prov` applies to "responses with ≥ 1 derived quantity"; spec 956 (synthetic example): "The increase is pct%." (weeks not identified) -> NV | N | AN. Codebook line 99: `s2_prov` is not applicable only "when there is no derived quantity".
2. **Candidate label.** `s2_prov` = N (the pasted AI label was `N/A`, corrected in the working file); `s2_evidence` NV, `s2_arith` AN.
3. **Alternatives.** Empty (not applicable) only if "12.6%" were not a derived quantity, for example displayed in the prompt; the rehearsal has no prompt, so that cannot be excluded by observation.
4. **Sufficient?** Yes for the label: the spec names a percentage as derived and gives a near-verbatim example with `s2_prov` N. Residual limit: the original prompt is not available to confirm the numeral is not displayed (displayed plan values are weekly totals or pace tokens, spec 930). The earlier report's "assumption" (its section 2.2) is therefore largely replaced by spec 931 and 956.
5. **Question.** F-1: Confirm `s2_prov` = N for this row? `[ ] YES  [ ] NO  [ ] OTHER: ______`.

## G. `s2_values` and `s2_arith` cannot be verified without the original prompt
1. **Rules.** Spec 941: "`s2_values` ... **cv** all used values match the prompt; **sw** at least one used value is wrong"; spec 947: a computation is correct iff it matches "the exact value of the quantity it identifies (from displayed values and rule parameters)"; spec 951-957: the examples depend on `t_3`, `t_4` and whether `pct` is "exact" or "wrong", i.e. on a prompt. Codebook line 92 as spec 941; codebook lines 217-223 (section 6): the human coder "may code the items ... from the comment text only, on a sheet without the expected codes". The battery's module docstring (`research_design/step7/codebook_battery_v1.py`, docstring only; no item, feature or expected code was read) states that "Numbers are placeholders" and that the features include "used_ok : per used value, does it match the prompt". Spec 13.5 (line 820) requires batteries "written without any pilot/main response"; no prompt is attached to the 40 items, and the rehearsal sheet has columns `opaque_id`, `comment_text` and the labels only.
2. **Candidate labels.** `s2_values` = cv in 19 rows and none in 21; `s2_arith` = AC 17, AM 2, AI 1, AN 20 (the AC of row 20 is addressed in A).
3. **Alternatives.** (a) Report `s2_values` and `s2_arith` as "not assessable" in the rehearsal where they depend on the prompt and compare only the variables that the text determines (`s2_evidence`, `s2_prov`, `s2_rel`, `s3_stance`, and `s2_arith` where operands and result are both in the text); (b) attach a stipulated prompt context to each item (new material for a pre-registered battery whose hash is fixed in record 12.22: changing it is a decision of its own); (c) accept `cv` as the default when no contradiction is visible in the text (not a rule in the codebook).
4. **Sufficient?** No. The rules define cv/sw and correctness against the prompt and the rehearsal provides none. Verifiable from the text: `s2_evidence` (spec 935 closed list), `s2_prov`, `s2_rel` (spec 947: "checked only on the written numerals"; spec 943: "independent of whether the numerals are the right values"), `s3_stance`. Arithmetic is self-contained and was checked in three rows only: 19 `bc215963d1a424a5` (AM), 27 `54bef1ccfde12b92` (AC), 38 `04ec0e04721c7973` (AC).
5. **Questions.** G-1: Which of (a), (b), (c) applies to the rehearsal, and may the comparison output for `s2_values` and `s2_arith` be read as an indication of the codebook? `[ ] (a)  [ ] (b)  [ ] (c)  [ ] OTHER: ______`.

---
## Decision log (to be completed by the owner/advisor; blank)
| Item | Choice | Approver | Date | Conditions / edits |
|---|---|---|---|---|
| A-1, A-2 | | | | |
| B-1 | | | | |
| C-1, D-1, E-1 and the scope principle | | | | |
| F-1 | | | | |
| G-1 | | | | |
Nothing in this file changes a label, a CSV, the codebook, the battery or any frozen artifact.
