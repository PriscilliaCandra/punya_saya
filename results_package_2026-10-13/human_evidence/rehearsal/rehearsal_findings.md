# H4 codebook rehearsal: findings (researcher's classification, 2026-10-14)

**What this file is.** The findings file required by `HUMAN_TASKS_H1_H7_OPERATIONAL_CHECKLIST.md` step 7. The A/B/C classification of every differing cell is the researcher's decision, stated in the working conversation of 2026-10-14; the assistant prepared the text and the textual basis. No advisor has been asked or has approved anything. No second coder exists (OD-3). Nothing in this file changes a label, an expected code, the codebook, the battery, the specification, a manifest, a registry or a script. Decisions of the owner referred to below are in `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` entries 12.38 and 12.39.

## 1. Evidence of the comparison

| Item | Value |
|---|---|
| Coded sheet (the researcher's own coding, AI-exposed) | `human_evidence/rehearsal/rehearsal_human_AI_exposed_working.csv`, SHA-256 `1c4424ee7c08177a02a7d85c2b0160bc3680d6e3c231cb048ee2dfc3a8352b6e` (has a UTF-8 BOM) |
| Comparison input actually read by the script | a BOM-less temporary copy (the original minus the 3 BOM bytes), SHA-256 `1528cee10d30c507cfce3e30a132b3307ca7ce4c82e8ffe2df64ce692152707f`, because `compare_rehearsal.py` decodes with `utf-8` and fails on a BOM; the script was not edited |
| Comparison output | `human_evidence/rehearsal/comparison.json`, SHA-256 `3e868fd5dcb5eb631d0b95d16b0afdc2c3c5b1c4742f3b036ffc176cccb5c7bd` |
| Script run | `reproduce/compare_rehearsal.py`, SHA-256 `226bd628aef91d9e0305b4cf97f6a65e0aa62b6ff34fda9dbca87974478a6869`, exit code 0, run once |
| Expected codes | `research_design/step7/codebook_battery_v1.py`, SHA-256 `8200cfea41e23255242576ace494fa039ce28880d1a443a2326d6900e0107d49` (pre-registered, record 12.22) |
| Format pre-check before the comparison | `rows: 40; not filled: 0; problems: 0` (format only; see section 5) |

## 2. Raw descriptive agreement (40 items)

| Variable | Agree | Raw agreement |
|---|---|---|
| `s2_evidence` | 39/40 | 97.5% |
| `s2_prov` | 39/40 | 97.5% |
| `s2_rel` | 39/40 | 97.5% |
| `s3_stance` | 39/40 | 97.5% |
| `s2_values` | 31/40 | 77.5% |
| `s2_arith` | 24/40 | 60.0% |

These are raw descriptive figures from one comparison. They are **not** evidence of validity or of reliability: one human coder, no inter-rater comparison and no kappa (OD-3); the coder had seen AI-assisted labels (AI-exposed rehearsal, not independent coding); the 40 comments are short synthetic sentences; the coder wrote the codebook (codebook section 6); and for `s2_values` and `s2_arith` the expected codes are fixed by item-level flags of the battery, not derived from the comment text, while the rehearsal gives no prompt (section 4). `comparison.json` states: "rehearsal on synthetic comments; not a reliability or validity claim; no kappa".

## 3. Classification of the 29 differing cells

Classes (checklist step 7): **A** the researcher's slip or misreading; **B** the codebook wording allows two defensible readings, or a methodological decision is unresolved; **C** the pre-registered expected code looks wrong. Confidence is the assistant's estimate of the textual basis, not a measurement. "G-1" = the observability limitation of section 4.

| item | variable | my code | expected | class | one-sentence reason |
|---|---|---|---|---|---|
| B03 | `s3_stance` | NS | MPG | A (high) | The comment endorses the reviewer for week 4 and rejects it for week 3, which spec 984 names as MPG ("partial agreement, e.g. for some weeks only"). |
| B17 | `s2_evidence` | NV | IV | A (high) | "From week 3 to week 4 the increase is 20.0 percent" identifies the transition, so the derived quantity has provenance (spec 932) and the spec's own example (line 957) is IV. |
| B17 | `s2_prov` | N | Y | A (high) | Same clause: the weeks are identified in the same clause, so provenance holds (spec 932, example 957). |
| B17 | `s2_arith` | AN | AI | B (G-1) | Once the quantity has provenance a stated computation exists, but whether 20.0 is correct needs the plan values, which are not in the comment. |
| B36 | `s2_rel` | (empty) | RT | A (high) | The item is EV ("EXCEEDS" is a listed relation, and my `s2_evidence` is EV), so `s2_rel` is required (spec 943; codebook line 100 "Missing") and "12.6% exceeds 10%" holds as written. |
| B37 | `s2_values` | none | cv | A (medium) | "the cap of 10% in week 3" names a rule parameter in a compliance statement about a specific week, which makes it used under spec 933(c); `cv` versus `sw` still needs the prompt. |
| B09 | `s2_values` | none | cv | B | Whether the numeral 10 percent beside "less than" is a used value depends on the undefined "stated comparison" of spec 933(b); the broad reading was chosen by the owner only after the coding (12.39 row 1). |
| B20 | `s2_values` | none | cv | B | Same as B09 (relation `>=` is outside the closed list). |
| B23 | `s2_values` | none | cv | B | Same as B09 ("greater than" is outside the closed list). |
| B32 | `s2_values` | none | cv | B | Same as B09 ("is not above" is outside the closed list). |
| B35 | `s2_values` | none | cv | B | Same as B09 ("surpasses" is outside the closed list). |
| B38 | `s2_values` | none | cv | B | Same as B09 (relation `<=` is outside the closed list). |
| B10 | `s2_values` | SW | cv | not classified | The basis of `SW` cannot be recovered from the records (section 6). |
| B36 | `s2_values` | SW | cv | not classified | The basis of `SW` cannot be recovered from the records (section 6). |
| B09 | `s2_arith` | AN | AC | B (G-1) | Derived quantities with provenance are stated but their operands are not in the comment, so correctness cannot be assessed from the text. |
| B12 | `s2_arith` | AN | AC | B (G-1) | Same as B09 (12.5% for week 3 to week 4, no operands). |
| B20 | `s2_arith` | AN | AC | B (G-1) | Same as B09. |
| B21 | `s2_arith` | AN | AC | B (G-1) | Same as B09. |
| B22 | `s2_arith` | AN | AC | B (G-1) | Same as B09. |
| B23 | `s2_arith` | AN | AC | B (G-1) | Same as B09. |
| B24 | `s2_arith` | AN | AC | B (G-1) | Same as B09 (a difference of 90 s for week 3, no operands). |
| B31 | `s2_arith` | AN | AC | B (G-1) | Same as B24 (30 s). |
| B32 | `s2_arith` | AN | AC | B (G-1) | Same as B09. |
| B35 | `s2_arith` | AN | AC | B (G-1) | Same as B09. |
| B36 | `s2_arith` | AN | AC | B (G-1) | Same as B09. |
| B37 | `s2_arith` | AN | AC | B (G-1) | Same as B09. |
| B38 | `s2_arith` | AN | AC | B (G-1) | Same as B09. |
| B39 | `s2_arith` | AN | AC | B (G-1) | Same as B09. |
| B40 | `s2_arith` | AN | AC | B (G-1) | Same as B24 (90 s for week 3). |

**Summary.** A = 5 cells (B03 `s3_stance`; B17 `s2_evidence`, `s2_prov`; B36 `s2_rel`; B37 `s2_values`). B = 22 cells (6 `s2_values`; 16 `s2_arith`, of which 15 plus B17). Not classified = 2 cells (the `SW` cells of B10 and B36). C = 0. Total 29. The classification is the researcher's and provisional until the decisions listed in section 7 exist.

No class C was assigned because no expected code contradicts an explicit written rule for a comment that can be assessed from its text. This is "no contradiction found", not "expected codes proven correct": the expected `cv`, `AC` and `AI` are stipulated by the battery's flags and cannot be tested in a rehearsal without a prompt.

## 4. Limitation G-1 (owner decision 12.39 row 2) and the limit of `s2_values`/`s2_arith` (row 3)

`cv`/`sw` and arithmetic correctness are defined against the displayed values and rule parameters of the prompt (spec 941, 947). The real coding sees the prompt (codebook lines 42-44); the rehearsal gives the comment text only (codebook lines 219-223). Arithmetic assessment that needs the prompt cannot be validly assessed from the visible comment alone.

- The 16 `s2_arith` differences (15 with expected AC plus B17 with expected AI) are a limitation of observability. They are **not** shown to be coder errors. The `AN` labels were not changed, no `unresolved` category was added, and no second comparison was run.
- Where a rule determines the code from the text, the cell is classified separately (the class A rows).
- The `s2_values` reading of "used" is the owner's provisional broad reading of spec 933(b) (12.39 row 1); it is not a codebook rule, it has no advisor approval, and it does not decide `cv` versus `sw`.

## 5. Three validation layers (owner decision 12.39 row 5)

1. **Format** (`precheck_human_sheets.py`, advisory): header, ids, unchanged `comment_text`, allowed codes, non-empty required cells (`s2_prov` and `s2_rel` optional). A pass means the format satisfies the current checking rules; it does not show that every substantively required label is filled or that any label is correct.
2. **Applicability of labels** (for example `s2_rel` required when `s2_evidence` = EV; codebook lines 99-100): no tool checks this; none was added by decision.
3. **Agreement with the expected codes** (`compare_rehearsal.py`, run once): raw descriptive agreement only.

Known limitation: B36 (`s2_evidence` = EV with `s2_rel` empty) passed layer 1 and appears as a difference in layer 3. The sheet was not changed to remove it.

## 6. Cells whose basis cannot be recovered (B10 and B36, `s2_values` = SW)

- B10: `From week 3 to week 4: (34.9 - 31.0) / 31.0 = 12.6% > 10%.` Manual SW; expected cv; AI-assisted candidate cv.
- B36: `From week 3 to week 4 the increase of 12.6% EXCEEDS the cap of 10%.` Manual SW; expected cv; AI-assisted candidate cv.
- Evidence that exists: `s2_values` was blank for these rows in all three timestamped backups of the sheet (the last is `…before_s2_rel_clear_20261014T093409`), so SW was entered afterwards. The sheet has no notes column and `comment_text` was not altered. No written rationale for SW exists in the records read.
- Spec 941 defines `sw` against the prompt, which the rehearsal does not provide; owner decision 12.38 row 3 asks not to guess correctness against a missing prompt. For B10 the internal arithmetic is consistent ((34.9 - 31.0) / 31.0 = 12.58%, written 12.6%).
- Statement: the basis for these two SW labels **cannot be recovered from the available records**. No reason is inferred and no class A, B or C is assigned. Because a basis is unknown, the checklist's "unsure" condition applies (step 8).

## 7. Open items and stop rule

- **Stop rule (checklist step 8) applies.** Class B cells exist and two cells are unclassified. H3 is not created. The findings go to the owner and the advisor with the question: (i) no change, recorded as a limitation; (ii) a codebook revision (new Step 7 version, box R-7, rebuild sequence of `OWNER_APPROVAL_PACKAGE.md`); (iii) a question on the battery for the advisor.
- **Advisor input not yet requested and not claimed:** the reading of "used" (12.39 row 1; tension with codebook line 46 and spec 1001, where a silent codebook leads to `unresolved`); whether a rehearsal that cannot assess `s2_values`/`s2_arith` from text satisfies 12.38 row 4; whether the advisor must also be involved in 12.39 row 2 (unconfirmed). The human rehearsal remains an open advisor item of the Step 7 manifest.
- **Reporting format for "not assessable" values:** undecided (12.38 row 3, 12.39 row 2).
- **Not done here:** no second comparison, no sheet change, no R1, no H1/H2/H3, no message to the advisor.

Supporting documents (working, non-official): `H4_LIMITATIONS_AND_LAYERS_2026-10-14.md` (this folder); in the scratch directory `H4_DIAGNOSTIC_REPORT_2026-10-14.md`, `H4_OWNER_ADVISOR_ISSUES_DRAFT_2026-10-14.md`, `H4_FOLLOWUP_INTEGRITY_AND_DECISION_REQUEST_2026-10-14.md`.
