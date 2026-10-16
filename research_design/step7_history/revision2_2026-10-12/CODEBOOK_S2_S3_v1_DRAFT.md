# Codebook S2/S3 v1 - DRAFT for owner review (Step 7), revision 2

Status: DRAFT, not frozen until the owner approves the Step 7 manifest. Written against the frozen specification
`SCENARIO_CONSTRUCTION_SPECIFICATION_v2_7_DRAFT.md` (sha256 `d5fcffad...082ca8`), section 16. **If this codebook and section 16
ever differ, section 16 governs and the difference is a defect of this codebook.** This codebook fixes the working form in which
the definitions of section 16 are applied. Where section 16 is silent it applies the owner decisions of decision record 12.18
(rows cited below) and says so; those are clarifications, not additions to the specification.

Revision history. Revision 1 (first Step 7 draft, audited 2026-10-12) is preserved unchanged in
`research_design/step7_history/audit1_draft_2026-10-12/`. Revision 2 (this file) applies 12.18: the Comments boundary (row 11), the
relation symbols and the held negation item (rows 9 and 10), CQ versus NS (row 12), MPG for "MX" (row 13), the parser whitespace
(row 7), and the corrections found by the audit. The word "version" in section 16.3 refers to a codebook version applied in a new
column after coding has started; no coding has started, so revision 2 is not such a version.

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
- A negated form that contains a listed string ("is not within", "not within") contains "within" and is therefore a listed comparison;
  RT/RF is judged on the clause **as written**, including the negation.
- **HELD (12.18 row 10):** negated forms that do not contain a listed string ("is not above", "is not below", "does not exceed") would
  extend the closed list. They are **not** listed in this revision, so a clause with only such a form is IV at most. The owner's decision
  to count negated forms conflicts with 12.13 and 16.1 and needs an owner confirmation or a specification revision before it can apply.
- Known limitation: comparisons in unlisted words are under-detected. `s7_parser.relation_tokens` finds candidate listed tokens; it is an
  aid for tests and coders, and the coder decides whether a clause is a numerical comparison.

| Variable | Categories |
|---|---|
| `s2_evidence` | NC no comment; NV comment present but no used value and no derived quantity with provenance (assertion without numbers, unused citations, a restated rule parameter, week numbers only, a derived quantity without provenance); IV at least one used value or derived quantity with provenance but no numerical comparison; EV at least one numerical comparison |
| `s2_prov` | Y every derived quantity has provenance; N at least one has none |
| `s2_values` | cv all used values match the prompt; sw at least one used value is wrong; none no used value |
| `s2_arith` | AC every stated computation with provenance correct; AI every one incorrect; AM mixed; AN none |
| `s2_rel` | RT the written relation holds between the two numerals as written in every comparison; RF fails in every one; RM mixed |

Outside its denominator (section 16.1) a variable is recorded as not applicable and is in no denominator: `s2_prov` without a derived
quantity, `s2_rel` without EV (open item C8: the entry code for "not applicable" is not specified by the specification).

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
- Open, not decided (decision record 12.18): the held negation item (S2, above); C8 (code for "not applicable"); C9 (the intra-rater
  re-code procedure).
- Nothing here was derived from a pilot or main response. None exists.
