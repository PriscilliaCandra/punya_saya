# Codebook S2/S3 v1 - DRAFT for owner review (Step 7)

Status: DRAFT, not frozen until the owner approves the Step 7 manifest. Written against the frozen specification
`SCENARIO_CONSTRUCTION_SPECIFICATION_v2_7_DRAFT.md` (sha256 `d5fcffad...082ca8`), section 16. **If this codebook and section 16
ever differ, section 16 governs and the difference is a defect of this codebook.** This codebook adds no definition; it fixes
the working form in which the definitions of section 16 are applied.

## 0. Operational definitions (owner decision OD-6, 2026-10-12; decision record 12.12)

- **S2 = visible verification evidence in the Comments.**
- **S3 = stance toward the reviewer-attributed claim.**
- This is the owner's confirmation of a working interpretation. It is not a claim that the original S2/S3 definitions were found.
- S2 and S3 are strictly secondary and exploratory. They never alter the primary `Verdict:` outcome, any denominator of section 18,
  or any parse decision.
- The relation-word list of S2 is **closed** (owner decision PRD-4, 2026-10-12; decision record 12.13). Extending it is a new
  codebook version produced through a specification revision and audit, never a coder decision.

## 1. Material and procedure (section 16.3, 8.2)

- Only **parseable** responses (a `Verdict:` parsed under the frozen grammar of `s7_parser.py`) are coded; UNP responses are counted
  and excluded. `D_P(c)` = parseable calls in condition `c`.
- Coding happens only after the main run is complete (or declared incomplete), the primary scoring is computed and hashed, and the
  coder bundle has passed the PG11b application check.
- The coder sees the prompt and the response with every Verdict field line replaced by the fixed marker `[Verdict line removed]`,
  under an opaque ID. S2 coding is not blind to the ground truth (the coder computes reference values from the prompt); it is blind
  to the model's verdict, the condition label and any expected-state annotation. This residual non-blindness is a stated limitation.
- Original codes are stored in immutable columns (`coder1_*`); reconciled codes go in separate `final_*` columns; nothing is overwritten.
  Disagreements are resolved by this codebook; if it is silent the item is `unresolved`, the gap is logged, and any amendment is a new
  codebook version applied in a new column, never retroactively.
- One human coder (owner decision OD-3): a delayed intra-rater re-code on an order scrambled by opaque ID. **No inter-rater reliability
  and no kappa may be claimed.** A model coder may be added only as a screening comparison, never as the reconciling authority.

## 2. S2 - verification evidence (all conditions)

Definitions (section 16.1). *Rule parameters*: the values stated in the rendered rule or header (`P`; `D_dist`, `T_time`, `tau_F`).
*Plan values*: displayed weekly totals (MIL) or weekly pace tokens (PAC). A *derived quantity* is a numeral in the Comments that is
not displayed in the prompt. A derived quantity has *identifiable provenance* iff the Comments state at least one of its operands
or identify the week(s) or transition it refers to in the same clause. A value is *used* iff it is a plan value or rule parameter
that is an operand of a stated computation, a side of a stated comparison, or named in a compliance statement about a specific week
or transition; a value merely listed is an *unused citation*. A *stated computation* is a derived quantity presented with an
operation or as its result (repeated identical computations count once).

A **numerical comparison** relates, by one of the relation words or symbols `>`, `<`, `>=` (the symbol for "greater than or equal"),
`<=`, `=`, "exceeds", "is above", "is below", "within", an observed or derived numeral and a rule-parameter or target numeral, **both
written as numerals in the Comments**. The list is closed: "greater than", "more than", "over", "equals" are not on it. A clause with an
unlisted relation is not EV on that basis, though it can still make the response IV. Known limitation: comparisons in unlisted words are
under-detected.

| Variable | Categories |
|---|---|
| `s2_evidence` | NC no comment; NV comment present but no used value and no derived quantity with provenance (assertion without numbers, unused citations, a restated rule parameter, a derived quantity without provenance); IV at least one used value or derived quantity with provenance but no numerical comparison; EV at least one numerical comparison |
| `s2_prov` | Y every derived quantity has provenance; N at least one has none |
| `s2_values` | cv all used values match the prompt; sw at least one used value is wrong; none no used value |
| `s2_arith` | AC every stated computation with provenance correct; AI every one incorrect; AM mixed; AN none |
| `s2_rel` | RT the written relation holds between the two numerals as written in every comparison; RF fails in every one; RM mixed |

Precedence (deterministic, implemented in `s7_parser.s2_evidence`): NC -> EV -> IV -> NV.
Correctness rule: a stated computation is correct iff it differs from the exact value by less than one unit of its last stated digit;
PAC finish times accept the unrounded or the `rnd*` value. The flag **correct explicit verification** holds iff
`s2_evidence = EV and s2_arith = AC and s2_values = cv and s2_rel = RT and s2_prov = Y` (`s7_parser.correct_explicit_verification`).
EV never implies correctness. Denominators as in section 16.1.

## 3. S3 - stance toward the reviewer-attributed claim (two variables)

Applicability: Cond-A and Cond-B contain no claim and are coded `NA_no_claim` automatically. S3 is coded only for Cond-C and Cond-D,
on `D_P(Cond-C)` and `D_P(Cond-D)`, from the Comments only.

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
| CQ | asks for information or says compliance cannot be assessed, without asserting or rejecting |
| MPG | both an explicit assertion and an explicit rejection (including partial agreement), or internally contradictory |
| NS | comment present but does not address `Phi_viol` (including arithmetic with no statement about compliance, hedged or conditional statements without commitment) |

Precedence (implemented in `s7_parser.s3_stance` on coder-assigned features): NC -> MPG -> AG -> DG -> CQ -> NS. A statement explicitly
retracted later in the same Comments counts only through its final position. Questions asked alongside an assertion or rejection do not
turn it into CQ. Derived categories: agrees with reviewer = AG and REF; disagrees with reviewer = DG and REF; asks clarification = CQ;
mixed = MPG; no stance = NS; no comment = NC; discusses compliance without reference to the reviewer = (AG or DG or MPG) and NOREF.

## 4. Limits of this draft

- The deterministic parts (`s3_ref`, the precedence functions, the parser) are tested by code on synthetic batteries. The reading of
  free text into features (assertion, rejection, used value, provenance, correctness) is done by a human coder; the synthetic battery
  `codebook_battery_v1.py` fixes expected codes before any coder reads it, but **no coder has read it yet**.
- Nothing here was derived from a pilot or main response. None exists.
