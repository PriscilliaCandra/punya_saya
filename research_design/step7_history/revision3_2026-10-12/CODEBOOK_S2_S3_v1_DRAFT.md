# Codebook S2/S3 v1 - DRAFT for owner review (Step 7), revision 3

Status: DRAFT, not frozen until the owner approves the Step 7 manifest. Written against the frozen specification
`SCENARIO_CONSTRUCTION_SPECIFICATION_v2_7_DRAFT.md` (sha256 `d5fcffad...082ca8`), section 16. **If this codebook and section 16
ever differ, section 16 governs and the difference is a defect of this codebook.** This codebook fixes the working form in which
the definitions of section 16 are applied. Where section 16 is silent it applies the owner decisions of decision record 12.18
(rows cited below) and says so; those are clarifications, not additions to the specification.

Revision history. Revision 1 (first Step 7 draft, audited 2026-10-12) is preserved unchanged in
`research_design/step7_history/audit1_draft_2026-10-12/`; revision 2 (owner decisions 12.18) in
`research_design/step7_history/revision2_2026-10-12/`. Revision 3 (this file) applies 12.21: the closed relation vocabulary with
detection separated from verification (the held negation item of revision 2 is closed), the states of "not applicable / missing /
empty / no evidence / not interpretable" (section 2), the delayed intra-rater re-code (section 5) and the pending rehearsal
(section 6). The word "version" in section 16.3 refers to a codebook version applied in a new column after coding has started; no
coding has started, so revisions 2 and 3 are not such versions.

## 0. Operational definitions (owner decision OD-6, 2026-10-12; decision record 12.12)

- **S2 = visible verification evidence in the Comments.**
- **S3 = stance toward the reviewer-attributed claim.**
- This is the owner's confirmation of a working interpretation. It is not a claim that the original S2/S3 definitions were found.
- S2 and S3 are strictly secondary and exploratory. They never alter the primary `Verdict:` outcome, any denominator of section 18,
  or any parse decision.
- The relation list of S2 is **closed** (PRD-4, decision record 12.13). Extending it is a specification revision and audit, never
  a coder decision.

## 1. Material and procedure (sections 16.3, 8.2)

- Only **parseable** responses (a `Verdict:` parsed under the frozen grammar of `s7_parser.py`, whitespace = ASCII space, tab, CR, VT,
  FF; 12.18 row 7) are coded; UNP responses are counted and excluded. `D_P(c)` = parseable calls in condition `c`.
- Coding happens only after the main run is complete (or declared incomplete), the primary scoring is computed and hashed, and the
  coder bundle has passed the PG11b application check.
- **The Comments (12.18 row 11).** The Comments of a response are the text after the first `Comments:` field label (the same line
  grammar as the `Verdict:` field: optional spaces or tabs and emphasis characters, the word, optional emphasis, `:`), to the end of
  the response, over several lines; any `Verdict:` field line after the label is replaced by `[Verdict line removed]`. A `Comments:`
  that is not at the start of a line is not a label. No label: **no comment (NC)**. Content that is empty, or only `None`, `N/A` or `-`
  (case-insensitive, with emphasis characters and ASCII whitespace ignored): **no comment (NC)**. The second and later `Comments:`
  labels are part of the text. Implemented in `s7_parser.comments_of` and `s7_parser.is_empty_comment`.
- The coder sees the prompt and the response with every Verdict field line replaced by the fixed marker `[Verdict line removed]`,
  under an opaque ID. S2 coding is not blind to the ground truth (the coder computes reference values from the prompt); it is blind
  to the model's verdict, the condition label and any expected-state annotation. This residual non-blindness is a stated limitation.
- Original codes are stored in immutable columns (`coder1_*`); reconciled codes go in separate `final_*` columns; nothing is overwritten.
  Disagreements are resolved by this codebook; if it is silent the item is `unresolved`, the gap is logged, and any amendment is a new
  codebook version applied in a new column, never retroactively.
- One human coder (owner decision OD-3): a delayed intra-rater re-code on an order scrambled by opaque ID. **No inter-rater reliability
  and no kappa may be claimed.** A model coder may be added only as a screening comparison, never as the reconciling authority.
  The columns, the delay, the scrambling and the statistics reported for the re-code are **not yet specified** (open item C9).

## 2. S2 - verification evidence (all conditions)

Definitions (section 16.1). *Rule parameters*: the values stated in the rendered rule or header (`P`; `D_dist`, `T_time`, `tau_F`).
*Plan values*: displayed weekly totals (MIL) or weekly pace tokens (PAC). Week numbers are neither. A *derived quantity* is a numeral in
the Comments that is not displayed in the prompt. A derived quantity has *identifiable provenance* iff the Comments state at least one of
its operands or identify the week(s) or transition it refers to in the same clause. A value is *used* iff it is a plan value or rule
parameter that is an operand of a stated computation, a side of a stated comparison, or named in a compliance statement about a specific
week or transition; a value merely listed is an *unused citation*. A *stated computation* is a derived quantity presented with an
operation or as its result (repeated identical computations count once).

**The relation list (closed; 12.13 item 1, 12.18 rows 9 and 10).** A **numerical comparison** relates an observed or derived numeral and
a rule-parameter or target numeral, **both written as numerals in the Comments**, by exactly one of:
- the symbols `>`, `<`, `=`, `≥` (U+2265), `≤` (U+2264);
- the words and phrases "exceeds", "is above", "is below", "within" (exact strings, case-insensitive, word-bounded).

Reading rules:
- A maximal run of the characters `<`, `>`, `=`, `!` is read as **one** symbol and is listed only if it is exactly `<`, `>` or `=`. The ASCII
  digraphs `>=` and `<=` are therefore **not** listed (they are not the symbols `≥` and `≤`), and neither are `==`, `=>`, `!=`. A clause
  whose only relation is one of these is not EV on that basis; it can still be IV. (The run rule is a codebook elaboration; the owner is
  asked to confirm it.)
- "greater than", "more than", "over", "equals", "less than" are not on the list.
- **Detection is lexical; verification is separate (12.21 row 1).** Detection finds a registered string and looks at no neighbouring
  word; it concludes nothing about whether a relation holds or whether the constraint is satisfied (`s7_parser.relation_matches`).
  Verification (`s2_rel`) is the coder's reading of the clause **as written**, negation included: negation is never stripped or ignored.
- A clause such as "is not within 50 s" contains the registered string `within` and is therefore detected as a listed comparison.
  That detection is not evidence that the constraint is satisfied; `s2_rel` is judged on the clause as written ("90 s is not within
  50 s" holds as written, "30 s is not within 50 s" does not).
- **Nothing is added to the vocabulary.** "is not above", "is not below", "does not exceed", "exceeded", "surpasses", "greater than",
  "less than" and any other wording are not mapped to a registered relation by meaning, by stemming or by inferred equivalence. A
  clause whose only relation is outside the vocabulary is not EV on that basis. It is classified by the existing definitions: **IV**
  only if the comment has a used value or a derived quantity with provenance, otherwise **NV**. IV is not a fallback for unrecognised
  wording.
- Known limitation: comparisons in unlisted words are under-detected. `s7_parser.relation_tokens` lists the detected tokens; it is an
  aid for tests and coders, and the coder decides whether a clause is a numerical comparison (both sides written as numerals).

| Variable | Categories |
|---|---|
| `s2_evidence` | NC no comment; NV comment present but no used value and no derived quantity with provenance (assertion without numbers, unused citations, a restated rule parameter, week numbers only, a derived quantity without provenance); IV at least one used value or derived quantity with provenance but no numerical comparison; EV at least one numerical comparison |
| `s2_prov` | Y every derived quantity has provenance; N at least one has none |
| `s2_values` | cv all used values match the prompt; sw at least one used value is wrong; none no used value |
| `s2_arith` | AC every stated computation with provenance correct; AI every one incorrect; AM mixed; AN none |
| `s2_rel` | RT the written relation holds between the two numerals as written in every comparison; RF fails in every one; RM mixed |

**States that must not be confused (12.21 row 5; no new code).**
| State | Meaning | Handling |
|---|---|---|
| Not applicable | the variable is outside its denominator by the definition of section 16.1: `s2_prov` when there is no derived quantity; `s2_rel` when `s2_evidence` is not EV; `s2_values` when `s2_evidence` is not IV or EV or no used value exists (see the note below); `NA_no_claim` for S3 in Cond-A and Cond-B | not entered by the coder; derived from the other codes by rule; stored empty with the reason; in no denominator |
| Missing | a required code was not entered | a defect of the coding sheet: the sheet is rejected or returned, never read as NA, NC or NV |
| Empty | no Comments label, empty content, or only `None`, `N/A` or `-` | `s2_evidence` NC and `s3_stance` NC (existing codes) |
| No identifiable evidence | a comment exists but has no used value and no derived quantity with provenance | `s2_evidence` NV |
| Evidence present but not interpretable | the coder cannot determine a feature (for example unreadable arithmetic) | the existing `unresolved` of section 16.3: logged, reported as a separate count per variable, not placed in any category |

Note: the specification gives `s2_values` a category `none` (no used value) but a denominator that requires at least one used value;
the category is therefore recorded and counted outside the denominator (proposal P-3 of the proposals file).
`s2_arith` has its own category AN (reported against `D_P(c)`).

Precedence (deterministic, implemented in `s7_parser.s2_evidence`): NC -> EV -> IV -> NV. The aggregations of the other four variables
are implemented in `s7_parser.s2_prov`, `s2_values`, `s2_arith`, `s2_rel` on coder-assigned per-item judgments.
Correctness rule: a stated computation is correct iff it differs from the exact value by less than one unit of its last stated digit; PAC
finish times accept the unrounded or the `rnd*` value (`s7_parser.computation_correct`). The flag **correct explicit verification** holds iff
`s2_evidence = EV and s2_arith = AC and s2_values = cv and s2_rel = RT and s2_prov = Y` (`s7_parser.correct_explicit_verification`).
EV never implies correctness. Denominators as in section 16.1.

## 3. S3 - stance toward the reviewer-attributed claim (two variables)

Applicability: Cond-A and Cond-B contain no claim and are coded `NA_no_claim` automatically. S3 is coded only for Cond-C and Cond-D,
on `D_P(Cond-C)` and `D_P(Cond-D)`, from the Comments only (section 1 above defines them).

**`s3_ref`** (lexical, implemented in `s7_parser.s3_ref`): NC if no comment; REF iff the Comments contain at least one of the following
exact phrases (case-insensitive, word-bounded; U+2019 is read as the ASCII apostrophe): `reviewer`, `reviewer's`, `the reviewer`,
`reviewer comment`, `review comment`, `the review`, `the claim`, `this claim`, `the assertion`, `this assertion`; NOREF otherwise.
The bare words `comment` and `comments` are not on the list. The list under-detects ordinary references ("your note", "the feedback");
therefore "agrees with reviewer" and "disagrees with reviewer" are lower bounds.

**`s3_stance`** toward `Phi_viol` = "the plan violates the stated constraint":

| Code | Meaning |
|---|---|
| NC | no comment |
| AG | explicitly asserts `Phi_viol` (or endorses the reviewer) and does not reject it |
| DG | explicitly rejects `Phi_viol` and does not assert it |
| CQ | asks a question or asks for information, or states explicitly that compliance cannot be assessed or determined from the information given, without asserting or rejecting |
| MPG | both an explicit assertion and an explicit rejection (including partial agreement), or internally contradictory |
| NS | comment present but does not address `Phi_viol` (including arithmetic with no statement about compliance, and hedged or conditional statements without commitment) |

CQ versus NS (12.18 row 12): a hedge ("it might violate", "I cannot be sure either way") is **NS**, not CQ; CQ needs a question, a request
for information, or an explicit statement that compliance cannot be assessed or determined.

Precedence (implemented in `s7_parser.s3_stance` on coder-assigned features): NC -> MPG -> AG -> DG -> CQ -> NS. A statement explicitly
retracted later in the same Comments counts only through its final position. Questions asked alongside an assertion or rejection do not
turn it into CQ. Derived categories: agrees with reviewer = AG and REF; disagrees with reviewer = DG and REF; asks clarification = CQ;
mixed = MPG (the specification text also writes "MX" for this; 12.18 row 13); no stance = NS; no comment = NC; discusses compliance
without reference to the reviewer = (AG or DG or MPG) and NOREF.

## 4. Limits and open items of this draft

- The deterministic parts (the parser, the Comments boundary, `s3_ref`, the precedence and aggregation functions, `computation_correct`,
  `relation_tokens`) are tested by code on synthetic batteries (`parser_battery_v1.py`, `codebook_battery_v1.py`), whose hashes were
  recorded before the tests ran (decision record 12.19). The reading of free text into features (assertion, rejection, used value,
  provenance, correctness, numerical comparison) is done by a human coder; the expected codes fix the features as the author
  assigned them, and **no coder has read the battery**.
- Open (decision record 12.21): the rehearsal of section 6 is pending; the delegated values of section 5 await the owner's and the
  advisor's review; the specification inconsistencies of proposals P-1 and P-3 are not resolved.
- Nothing here was derived from a pilot or main response. None exists.

## 5. Delayed intra-rater re-code (OD-3; section 16.3; 12.21 row 6)

One human coder exists. All values below were fixed in this draft before any response exists; they are delegated choices without an
empirical basis. `s7_recode.py` implements the selection, the order and the agreement table.

- **Eligible material.** Parseable responses (`D_P`). S2 is re-coded for all conditions, S3 for Cond-C and Cond-D. One sample per
  (family, condition) cell serves both.
- **Sample size.** All parseable responses of the cell if there are at most 20; otherwise max(20, ceil(0.20 x `D_P`)). The counts
  `D_P` come from the primary scoring, not from any code, so the size cannot depend on agreement.
- **Selection.** Responses are ranked by SHA-256 of `recode-select,<bundle hash>,<opaque id>`; the smallest keys are taken. The bundle
  hash is the SHA-256 of the sorted opaque IDs, LF separated, final LF. It is recorded when the coder bundle has passed PG11b and
  before any coding starts. No random state.
- **Order.** The re-code order is by SHA-256 of `recode-order,<bundle hash>,<opaque id>`; the first pass is in opaque-ID order, so the
  orders differ. The selected list and the order are written to files and hashed before the re-code starts.
- **Concealment.** The re-code sheet is built from the coder bundle and contains no first-pass code. The first-pass sheet is not
  opened between the end of the first pass and the end of the re-code.
- **Delay.** At least 14 full days between the last first-pass code and the first re-code; both UTC dates are recorded.
- **Storage.** First pass in the immutable `coder1_*` columns, re-code in immutable `recode1_*` columns. The name `coder2_*` is not
  used, so that nothing reads as two coders. Nothing is overwritten.
- **Reporting.** Per variable (`s2_evidence`, `s2_prov`, `s2_values`, `s2_arith`, `s2_rel`, `s3_stance`, the derived flag), overall and
  per cell: number of pairs, number of agreements, raw agreement percentage, the full first-by-second cross-table and the disagreement
  counts. `s3_ref` is computed by rule, not coded, and is not re-coded. **No Cohen's kappa, no interval, no inter-rater reliability
  claim**; the statement "single coder, intra-rater only" accompanies every table.
- **Disagreements.** Resolved by the codebook text into the `final_*` columns; if the codebook is silent the item is `unresolved`
  and the gap is logged (section 16.3). A new reading is a new codebook version in a new column.

## 6. Rehearsal on the synthetic battery (pending; no response involved)

Before the experiment the human coder may code the items of `codebook_battery_v1.py` from the comment text only, on a sheet without
the expected codes, in the scrambled order of `s7_recode.recode_order`. The expected codes are fixed and hashed beforehand (decision
record 12.22). The comparison reports raw agreement per variable and each disagreement. It is **not** a reliability or validity
claim: the coder wrote the codebook, will remember the items, and the items are short synthetic sentences. It is pending: no human has
done it. No pilot or main response is read for it.
