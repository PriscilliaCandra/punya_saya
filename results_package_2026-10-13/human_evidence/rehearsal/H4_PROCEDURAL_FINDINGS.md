# H4 procedural findings (state of 2026-10-14; H4 is NOT complete and the coding is NOT independent)

Companion of `H4_ADJUDICATION_REQUEST.md` (the questions and the cited rules). Paths relative to `D:\research s2\results_package_2026-10-13\human_evidence\rehearsal\` unless stated. Files referenced: `rehearsal_ai_coded_working.csv` (sha256 `f54db16191a52a73`), `rehearsal_ai_coded_working_REPORT.md` (`242455bf7b848030`), `rehearsal_filled.csv` (the pasted AI labels, `57936647a71f2d9b`, unchanged), `../../codebook_rehearsal_kit/rehearsal_sheet_BLANK.csv` (`19db7b40ac239c97`, unchanged).

## 1. CSV format problems found and fixed
| Problem | Evidence | Fix |
|---|---|---|
| The working copy `rehearsal_filled.csv` was overwritten (08:06, 1,660 bytes instead of 3,389) by the pasted AI labels | file size and header; the template survives in the kit | not repaired in place; the original file is untouched; a NEW file was created |
| Every line was one quoted field (`"b7721cb9eafab528,EV,Y,cv,AM,RM,NS"`), so the file had one column | parsed row width 1 for 40 rows | `rehearsal_ai_coded_working.csv` has seven real columns (width 7 in 40 rows), LF endings, UTF-8 without BOM |
| 47 cells `N/A` (20 in `s2_prov`, 27 in `s2_rel`) | the format check; codebook line 99 stores not-applicable states empty; `precheck_human_sheets.py` accepts only empty there | emptied in the working file |
| The pasted file had no `comment_text` | header | not needed in the 7-column file; IDs match the kit (40/40, same order). The existing pre-check requires the 8-column kit header, so it was run on a temporary 8-column derivative outside the project (result `rows: 40; not filled: 0; problems: 0`, exit 0), deleted afterwards |
Remaining format risks: none known. `compare_rehearsal.py` has not been run.

## 2. Limits of the rehearsal design (the prompt is not included)
- The 40 items are synthetic sentences ("Numbers are placeholders", battery module docstring). The kit has no prompt, no input data (targets, caps, weekly values) and no condition label; no file maps `opaque_id` to a prompt or to Cond-A..D (searched in the project: not found). `opaque_id` is only a hash of the battery item id.
- Codebook lines 217-223 and the kit README say the items are coded "from the comment text only", but `s2_values` (spec 941; codebook line 92) is defined against the prompt and arithmetic correctness (spec 947) against "displayed values and rule parameters". These two variables are therefore not assessable for most rows; `s2_evidence`, `s2_prov`, `s2_rel` and `s3_stance` are determinable from the text.
- Registry or prompt files of the experiment must not be consulted to fill the gap (viewing them affects the blind-check clock and they are not the source of these items).
- Spec 942 (explicit) versus codebook line 93 (omits the exclusion of computations without provenance): the codebook states that section 16 governs (codebook lines 4-5); the omission is a defect of the codebook, not a decision.

## 3. Labels that still need adjudication
| Row / `opaque_id` | Variable | Candidate | What the written rules say | Status |
|---|---|---|---|---|
| 20 `d614cbb672fe000e` | `s2_arith` | AC | spec 942 excludes computations without provenance, so AN | rule explicit; the candidate conflicts with it; owner confirmation (A-1) and codebook handling (A-2) |
| 25 `fe7db0c0524f62b4` | `s3_stance` | NS | referent and limit direction unknown | rules insufficient (B-1) |
| 28 `8a34b8db3f040423` | `s3_stance` | NS | spec 982 leans DG, not conclusive | adjudication (C-1) |
| 29 `22fb1725b563cd91` | `s3_stance` | NS | spec 984 and 991 lean AG, not conclusive | adjudication (D-1) |
| 35 `8a694865d0c4617d` | `s3_stance` | NS | as row 29 | adjudication (E-1) |
| 05 `00ceeab4df7002aa` | `s2_prov` | N (applied) | spec 931, 932, 956 explicit | confirmation only (F-1) |
| all rows with a used value or bare-result computation | `s2_values`, `s2_arith` | cv / AC, AM, AI | need the prompt | design limit (G-1) |
Scope warning: the stance question is a principle; adopting reading A for the cap/limit rows would also apply to 16 more candidate-NS rows listed in `H4_ADJUDICATION_REQUEST.md` section E.
Corrected earlier statement: `rehearsal_ai_coded_working_REPORT.md` sections 2.2 and 2.3 call the `s2_prov`/`s2_arith` points an "assumption" and "unresolved"; spec lines 931, 942 and 956 resolve them (see section F and A of the adjudication request). That report was not edited.

## 4. Status of the AI-assisted coding
- The labels were produced with AI assistance and pasted by the researcher; a model then compared them with the written rules and made the two corrections that the rules determine (row 01 EV -> IV and `s2_rel` emptied; row 05 `s2_prov` N) plus the `N/A` normalisation. Nothing else differs.
- OD-3 (`research_design/STEP2_OWNER_DECISIONS_RECORD.md`, row "Operational implications", line 44): "One human coder only ... No inter-rater reliability and no Cohen's κ may be claimed. A model coder, if used at all, is a screening comparison only, never the reconciling authority." Codebook lines 49-50 repeat it. Consequence: these labels are a screening input; they are not the human rehearsal required by spec 13.5 / codebook section 6, and they must not be reported as such, as independent coding, or as reliability.
- H4 status: NOT DONE. The researcher's own coding (the human rehearsal) has not been performed; no comparison was run; no finding exists from a human coder.

## 5. What waits for the owner/advisor (nothing below was done)
1. Answers A-1 to G-1 of `H4_ADJUDICATION_REQUEST.md`; until then no candidate label is changed.
2. If the codebook is to be revised (for example to add the exclusion sentence of spec 942, or a stance clarification): the codebook is a Step 7 freeze-set file hashed by the Step 8 build manifest, so box R-7, the rebuild sequence of `OWNER_APPROVAL_PACKAGE.md` and a decision BEFORE the evidence file H3 are required. If the codebook stays unchanged and the spec governs, nothing bound into H3 changes.
3. A decision on what H4 means given the AI assistance: for example the researcher codes the 40 rows independently from the blank kit and the AI labels serve only as a screening comparison (OD-3); the assistant has not made this choice.
4. Only after the researcher's own coding is complete and the owner agrees: the one-time `compare_rehearsal.py` run (it opens the expected codes).
Not blocked by these items: R1, H1 (subject to the PG3 question), H5-H7 and the other owner decisions.
