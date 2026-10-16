# H4 rehearsal: limitation statement and three validation layers (2026-10-14)

**Status:** supporting text for the researcher. This is NOT `rehearsal_findings.md`, contains no final A/B/C classification, and does not create H3. It records the owner decisions of 2026-10-14 (decision record entry 12.39) as text the researcher may carry into the findings file. No advisor approval exists or is claimed. Nothing here changes a sheet, label, expected code, battery, codebook, specification, manifest, registry or script. The stop rule of `HUMAN_TASKS_H1_H7_OPERATIONAL_CHECKLIST.md` step 8 stays in force.

## 1. Nature of the comparison
One human coder (OD-3), AI-exposed (the coder had seen AI-assisted labels), 40 synthetic comments, coded from comment text only (codebook lines 219-223), compared once with the pre-registered expected codes (battery hash recorded in 12.22). `comparison.json` reports raw agreement and the 29 differing cells; it states "not a reliability or validity claim; no kappa". The figures below are raw descriptive results.

| Variable | Agree | Raw agreement |
|---|---|---|
| `s2_evidence` | 39/40 | 97.5% |
| `s2_prov` | 39/40 | 97.5% |
| `s2_rel` | 39/40 | 97.5% |
| `s3_stance` | 39/40 | 97.5% |
| `s2_values` | 31/40 | 77.5% |
| `s2_arith` | 24/40 | 60.0% |

## 2. Limitation G-1 (decision 12.39 row 2)
Arithmetic assessment that needs the prompt (plan values or rule parameters behind a stated computation) cannot be validly assessed from the visible comment alone. In the rehearsal, 15 comments (B09, B12, B20, B21, B22, B23, B24, B31, B32, B35, B36, B37, B38, B39, B40) contain a derived quantity with provenance, but the operands are not in the text; the sheet carries `AN` and the expected code is `AC`. B17 (expected `AI`) shares this limitation for its `s2_arith` cell. These `s2_arith` differences are a limitation of observability, not shown coder errors. The `AN` labels are unchanged, no `unresolved` category was added, and no second comparison was run.

Differences that the written rules determine from the comment text are a different category and are for the researcher to classify (candidates named in the diagnostic: B03 `s3_stance`; B17 `s2_evidence` and `s2_prov`; B36 `s2_rel`; B37 `s2_values` "none").

## 3. Limitation of `s2_values` and `s2_arith` without a prompt (decision 12.39 row 3)
`cv`/`sw` and arithmetic correctness are defined against the prompt (spec 941, 947); the real coding sees the prompt (codebook lines 42-44) and the rehearsal does not. The expected `cv`, `AC` and `AI` are set by item-level flags of the battery, not derived from the comment. Therefore 77.5% and 60.0% must not be read as validity or reliability. Whether this satisfies 12.38 row 4 is an open question for the advisor.

`s2_values` reading of "used" (decision 12.39 row 1): provisional broad reading of spec 933(b), owner's working interpretation, advisor review not obtained; it does not decide `cv` versus `sw`. The basis of `SW` on B10 and B36 is not documented in the files read; the researcher records the basis or states that it cannot be recovered (issue 4).

## 4. Three validation layers (decision 12.39 row 5)
| Layer | What it checks | Tool | What a pass means |
|---|---|---|---|
| 1. Format | header, ids, unchanged `comment_text`, allowed codes, non-empty required cells (`s2_prov` and `s2_rel` optional) | `precheck_human_sheets.py` (advisory) | The format satisfies the current checking rules. It does not show that every substantively required label is filled, nor that any label is correct. |
| 2. Applicability of labels | whether a cell is required or empty given other codes (for example `s2_rel` required when `s2_evidence` = EV; codebook lines 99-100; EV excludes `s2_values` = none, spec 949) | none at present (not added by decision) | Not checked by any tool; a missing required code is "Missing" by codebook line 100. |
| 3. Agreement with expected codes | cell-by-cell comparison with the pre-registered expected codes | `compare_rehearsal.py`, run once | Raw descriptive agreement only. |

Known limitation: B36 (`s2_evidence` = EV, `s2_rel` empty) passed layer 1 and appears as a difference in layer 3. The sheet is not changed to remove it.

## 5. Still open
- Issue 4: the researcher classifies A/B/C in `rehearsal_findings.md`, including the basis of `SW` on B10 and B36 or a statement that it cannot be recovered.
- Advisor input (not requested yet): the reading of "used" (12.39 row 1) and whether the rehearsal suffices without a prompt (row 3). Whether the advisor must also be involved in row 2 is unconfirmed.
- Reporting format for "not assessable" values: undecided.
- H3 is not created; R1 is not recorded.
