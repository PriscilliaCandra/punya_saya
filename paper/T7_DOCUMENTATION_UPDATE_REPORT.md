# T7_DOCUMENTATION_UPDATE_REPORT

**Status: Documentation update pass only. No backend code, database, schema, or experiment was modified in this pass. No E1–E8 definitions were changed. No methodology was changed substantively — only wording was corrected to match the already-fixed, already-tested implementation and the already-published `PAPER_DRAFT.md` Table II. Nothing has been committed.**

> Source of truth used: (1) the fixed implementation in `backend/app/rules/generator.py`; (2) the passing regression suite `backend/tests/test_t7_progression_fix.py` (7 tests) plus a full-suite run (201/201 passing); (3) the one clarified progression rule requested — "Build weeks multiply the volume of the immediately preceding week — whether that week was itself a build week or a recovery cutback week — by 1.06 or 1.08."

---

## 1. Files changed

| # | File | Priority tier |
|---|---|---|
| 1 | `paper/PAPER_DRAFT.md` | Required (manuscript, Table II) |
| 2 | `paper/RESEARCH_METHODOLOGY_LOCK.md` | Required |
| 3 | `paper/PAPER_GAPS.md` | Required |
| 4 | `paper/RESEARCH_READINESS_AUDIT.md` | Required |
| 5 | `paper/ADVISOR_REVIEW_PACKAGE.md` | Required |
| 6 | `paper/RESEARCH_METHODOLOGY_NON_COMPARATIVE_PROPOSAL.md` | Required |
| 7 | `paper/RESEARCH_METHODOLOGY_COMPARATIVE_PROPOSAL.md` | Required |
| 8 | `paper/EVALUATION_CRITERIA_OPTION_A_DESIGN.md` | Required (E4-blocked wording) |
| 9 | `paper/EVALUATION_CRITERIA_RECONCILIATION.md` | Required (E4-blocked wording) |
| 10 | `paper/EVALUATION_CRITERIA_FINAL_CONSISTENCY_REVIEW.md` | Required (E4-blocked wording; historical, addendum-style) |
| 11 | `paper/ADVISOR_DECISION_SHEET_COMPARATIVE.md` | Found in the original audit, not in the priority list |
| 12 | `paper/EVIDENCE_MAP.md` | Found in the original audit, not in the priority list |
| 13 | `paper/ADVISOR_METHODOLOGY_QA.md` | **Found only during the final re-audit pass** (missed in the original 18-file audit) |
| 14 | `paper/CODE_AUDIT_EASY_RUN_PACE_AND_T7.md` | Historical audit document — addendum added, findings preserved unmodified |
| 15 | `paper/T7_DOCUMENTATION_CONSISTENCY_AUDIT.md` | Historical audit document — addendum added, findings preserved unmodified |
| 16 | `paper/T7_DOCUMENTATION_UPDATE_REPORT.md` | **New** — this report |

No other files were touched. `backend/app/rules/generator.py` and `backend/tests/test_t7_progression_fix.py` are unchanged from the prior (code-fix) session — this pass did not re-open them.

---

## 2. Sections changed (by file)

- **`PAPER_DRAFT.md`**: Table II "Progression" row (the exact ambiguous wording); the body paragraph immediately after Table II (the "two properties" sentence); the "Multi-Week Plan Generation" results paragraph (the canonical-profile numeric example and its closing sentence).
- **`RESEARCH_METHODOLOGY_LOCK.md`**: the T7 row in the technical-validation table; the T6 row (test-coverage note); the "Rule-engine limitations" threats-to-validity row; the "Technical validation T1–T14" and "Rule-engine design decisions" rows in the Section-13 freeze-readiness table.
- **`PAPER_GAPS.md`**: item 4 of the open-items list; the §5 "Findings about the rule engine to decide on" table (all three rows); the §5b rule-constant traceability table (Cutback and Taper rows); the "Not resolved by this update" closing sentence.
- **`RESEARCH_READINESS_AUDIT.md`**: T6 and T7 rows in the main criteria table; the "Separation" summary bullets; §7.1 and §7.2 (fully reframed as resolved/confirmed, formulas and canonical examples preserved); the pending-decisions list items 5 and 6; the final "Not resolved by this update" sentence.
- **`ADVISOR_REVIEW_PACKAGE.md`**: T6/T7 summary-table rows; the detailed rebound/taper issue table (reframed as "prior vs current behavior"); item 4 of the prerequisites table; question 6 of the decisions list; question 5's answer; the final "Not resolved by this update" sentence.
- **`RESEARCH_METHODOLOGY_NON_COMPARATIVE_PROPOSAL.md`**: the §6.1 objective-compliance table (Progression/Cutback/Taper rows); the §6.2 closing bullet; §12's entire rebound/taper table and advisor-question block.
- **`RESEARCH_METHODOLOGY_COMPARATIVE_PROPOSAL.md`**: rule-table rows 12–14 (Progression/Cutback/Taper consistency); the threats-to-validity row; the open-decisions row; the files-that-would-change inventory row; the §4-area paragraph introducing the two rule-engine behaviors.
- **`EVALUATION_CRITERIA_OPTION_A_DESIGN.md`**: E4's item 7, 8, 11, 12 (definition section); the §5 comparability-matrix E4 row; the §7 threats-to-validity row; §9 open decision #1; the §10 final-recommendation bullet; the closing summary table's E4 row.
- **`EVALUATION_CRITERIA_RECONCILIATION.md`**: C6's "Baseline evaluation" item; §9 open question #4.
- **`EVALUATION_CRITERIA_FINAL_CONSISTENCY_REVIEW.md`**: the "not blocking" T7 bullet (status-update style, original text preserved alongside); the E4 summary-table row.
- **`ADVISOR_DECISION_SHEET_COMPARATIVE.md`**: decision item 8.
- **`EVIDENCE_MAP.md`**: the progression/cutback/taper evidence row and the rebound/taper-drop row.
- **`ADVISOR_METHODOLOGY_QA.md`**: Q3's answer paragraph (caught only in the final re-audit — see §7 below).
- **`CODE_AUDIT_EASY_RUN_PACE_AND_T7.md`**: a new addendum block at the top; one added resolution line after the original "does not choose between (a) and (b)" sentence. The audit's root-cause table and traced example are unmodified.
- **`T7_DOCUMENTATION_CONSISTENCY_AUDIT.md`**: a new addendum block at the top. The audit's 32 findings and proposed wordings are unmodified (they are now the historical record of what this pass applied).

---

## 3. Before → after wording for the important methodology changes

### 3.1 The flagged progression wording (`PAPER_DRAFT.md` Table II — the manuscript itself)

**Before:**
> "Progression | Build weeks multiply the previous build volume by 1.06 or 1.08"

**After:**
> "Progression | Build weeks multiply the volume of the immediately preceding week — whether that week was itself a build week or a recovery cutback week — by 1.06 or 1.08"

This is the exact clarification requested, applied verbatim to the manuscript's Table II with no change in meaning beyond resolving the ambiguity.

### 3.2 The canonical-profile numeric example (`PAPER_DRAFT.md`, §V-B)

**Before:** "For an 8-week plan the realized weekly distances are 26.6, 28.2, 29.9, 25.3, **31.6, 33.5**, 21.2, and 13.8 km; for 12 weeks ... 26.6, 28.2, 29.9, 25.3, **31.6, 33.5, 35.6, 30.1, 37.6, 39.8**, 21.2, and 13.8 km ... They also show the properties described in Section III-E (post-cutback rebound and anchored taper)."

**After:** "For an 8-week plan the realized weekly distances are 26.6, 28.2, 29.9, 25.3, **26.8, 28.4**, 21.2, and 13.8 km; for 12 weeks ... 26.6, 28.2, 29.9, 25.3, **26.8, 28.4, 30.2, 25.6, 27.1, 28.7**, 21.2, and 13.8 km ... They also show the anchored-taper property described in Section III-E; the build weeks that follow a cutback ... step up by the normal ~6% relative to the cutback week, reflecting the post-cutback progression fix described there, not the ~25% rise shown in an earlier version of this example."

These replacement numbers were not invented — they were obtained by running the actual fixed `generate_rule_based_plan` against the exact canonical test-factory profile already cited in the manuscript (age 21, 5K PB 24:56, target 5K 23:00, 25 km/week, 4 days/week), confirming VDOT (38.43) and pace zones are unchanged and only the post-cutback weeks (5–6 in the 8-week plan; 5, 6, 9, 10 in the 12-week plan) differ from the pre-fix numbers.

### 3.3 T7 status (`RESEARCH_METHODOLOGY_LOCK.md`, the master "locked" document)

**Before:** "T7 | Known rule-engine properties | Documented properties hold and are reported, not hidden: post-cutback rebound (~+25% vs cutback week), taper anchored to starting volume | Observed by running the generator | Decide fix-or-document **before the baseline is frozen**"

**After:** "T7 | Known rule-engine properties | **RESOLVED**: post-cutback rebound FIXED ...; taper/race-week volume CONFIRMED CORRECT as anchored to `base_mileage` ... | `backend/tests/test_t7_progression_fix.py` (7 tests); full suite 201/201 passing | RESOLVED — ... Remaining step before the baseline is frozen: generate/freeze the 24 baseline plans against this fixed rule-engine version (not yet done)"

### 3.4 Taper — confirmed NOT changed to peak-anchored (every file)

No file's taper *formula* was altered. Every update preserves: penultimate week = `base_mileage × 0.85`, race week = `base_mileage × 0.55`. The only textual change applied to taper descriptions, everywhere it appeared, was removing "decide whether to anchor to peak" / "fix or document" framing and replacing it with "CONFIRMED CORRECT, anchored to base/starting mileage, not changed" — consistent with the constraint that taper must remain base-anchored.

---

## 4. T7 status after update

**RESOLVED** across every document surveyed, with a consistent three-part statement used throughout:
1. Post-cutback rebound (~+25%) — **FIXED in code** (`generate_weekly_progression_summary`, `current = vol` added to the cutback branch).
2. Taper/race-week anchoring to `base_mileage` — **CONFIRMED CORRECT and left unchanged**, matching `PAPER_DRAFT.md` Table II; only the previously-wrong inline code comment was corrected.
3. **Remaining, explicitly separate, NOT yet done**: generating and freezing the 24 baseline plans against this fixed rule-engine version. No document claims this has happened.

---

## 5. E4 status after update

- E4 ("Multi-Week Trajectory Fidelity") is **no longer described as blocked by T7** in `EVALUATION_CRITERIA_OPTION_A_DESIGN.md`, `EVALUATION_CRITERIA_RECONCILIATION.md` (its predecessor C6), or `EVALUATION_CRITERIA_FINAL_CONSISTENCY_REVIEW.md` (updated as a status note on a historical finding).
- E4 **remains one of the 8 locked evaluation criteria** — its definition, algorithm, inputs, and non-redundancy argument in `EVALUATION_CRITERIA_OPTION_A_DESIGN.md` §4 were not changed, only its blocking status.
- E4 **can now proceed to evaluator implementation**, subject to the normal, separate evaluator design/testing work (not part of this pass) — this pass did not build, modify, or test any evaluator.
- **No document claims the 24 baseline plans have been generated.** Every updated passage that mentions "generate/freeze the 24 baseline plans" explicitly marks it as a separate, not-yet-done step.
- **No document claims the 24×3 Gemini experiment has been run.** This was not touched by this pass and no wording anywhere implies otherwise.

---

## 6. Historical audit documents preserved

- **`CODE_AUDIT_EASY_RUN_PACE_AND_T7.md`**: root-cause analysis, file:line evidence table, and the traced pre-fix example (`[21.2, 22.5, 23.9, 20.3(cutback), 25.3, 26.8, 17.0(taper), 11.0(race)]`) are byte-for-byte unmodified below the new addendum. The addendum explicitly states the finding describes pre-fix behavior and points to the fix.
- **`T7_DOCUMENTATION_CONSISTENCY_AUDIT.md`**: all 32 INCONSISTENT / 4 AMBIGUOUS / 13 CONSISTENT findings and their quoted original wordings are unmodified. A new addendum at the top states the proposed replacements have since been applied and points to this report.
- **`EVALUATION_CRITERIA_FINAL_CONSISTENCY_REVIEW.md`**: the original finding ("T7 ... blocking E4 — already correctly gated ... must remain blocked until the advisor/engineering decision is made") is kept in place, with a "STATUS UPDATE (since this review): RESOLVED in a later session" sentence appended immediately after it — the original sentence was not deleted or rewritten.

No historical evidence was erased or rewritten as if the bug had never existed; every "before" state is either kept verbatim (in the two audit documents) or restated explicitly as "prior behavior (historical record)" alongside the current behavior (in the working methodology documents, where keeping both in one place is more useful than a separate addendum).

---

## 7. Final consistency-audit results (re-run after the edits)

| Keyword/phrase searched | Remaining occurrences | Classification |
|---|---|---|
| `"previous build volume"` | 2, both in `T7_DOCUMENTATION_CONSISTENCY_AUDIT.md`, quoting the old `PAPER_DRAFT.md` wording for the audit record | **HISTORICAL/AUDIT RECORD** |
| `"pre-cutback peak"` | `CODE_AUDIT_EASY_RUN_PACE_AND_T7.md` (2, in the preserved root-cause table); `T7_DOCUMENTATION_CONSISTENCY_AUDIT.md` (4, in its findings/proposed-wording text); `RESEARCH_METHODOLOGY_LOCK.md` (1, in the T7 row's own "RESOLVED" description, correctly describing what the fix moved *away from*) | **HISTORICAL/AUDIT RECORD** (first two files); **CURRENT RULE** (the lock-document occurrence correctly describes the resolved state) |
| `"stale accumulator"` / `"stale pre-cutback"` | 2, both in `T7_DOCUMENTATION_CONSISTENCY_AUDIT.md` | **HISTORICAL/AUDIT RECORD** |
| `"rebound ~25%"` (and the `+25%`/`≈+25%` variants) | Present in `CODE_AUDIT_EASY_RUN_PACE_AND_T7.md` and `T7_DOCUMENTATION_CONSISTENCY_AUDIT.md` (historical records); present in `RESEARCH_METHODOLOGY_LOCK.md`, `PAPER_GAPS.md`, `EVIDENCE_MAP.md`, `RESEARCH_READINESS_AUDIT.md`, `ADVISOR_REVIEW_PACKAGE.md`, `ADVISOR_METHODOLOGY_QA.md`, `ADVISOR_DECISION_SHEET_COMPARATIVE.md`, `RESEARCH_METHODOLOGY_COMPARATIVE_PROPOSAL.md` (all now stating the figure as the magnitude of a **resolved/fixed** issue, not a live one) | **HISTORICAL/AUDIT RECORD** (first two); **CURRENT RULE, correctly described as resolved** (the rest) |
| `"T7 unresolved"` / `"T7 pending"` | 0 | — |
| `"E4 blocked"` | 1, in `T7_DOCUMENTATION_CONSISTENCY_AUDIT.md`, quoting a now-superseded line from `EVALUATION_CRITERIA_OPTION_A_DESIGN.md` for the audit record | **HISTORICAL/AUDIT RECORD** |
| `"taper peak"` (taper described as peak-anchored, in either order) | 0 outside historical/audit records; the only "taper...peak" co-occurrences are (a) the two preserved audit documents correctly describing the *prior, incorrect comment*, (b) `RESEARCH_METHODOLOGY_LOCK.md`'s T7 row correctly stating the current formula is *not* peak-anchored, and (c) this report's and the consistency audit's own section headers asking the question | **HISTORICAL/AUDIT RECORD** or **CURRENT RULE** (correctly negating peak-anchoring) — never an affirmative, current claim that taper uses peak |
| `"taper base"` | Present throughout every updated document, consistently describing `base_mileage × 0.85` / `× 0.55` | **CURRENT RULE** — unchanged formula, confirmed correct, matches `PAPER_DRAFT.md` Table II |
| `"0.85"` | Widespread — cutback formula (`current × 0.85`) and taper formula (`base_mileage × 0.85`) throughout | **CURRENT RULE** in every occurrence checked; no stale usage found |
| `"0.55"` | Widespread — race-week taper formula (`base_mileage × 0.55`) throughout | **CURRENT RULE** in every occurrence checked; no stale usage found |

**Three additional INCONSISTENT items were found only during this final re-audit pass** (not in the original 32-item audit) and were corrected in this update:
- `paper/ADVISOR_METHODOLOGY_QA.md` Q3's answer ("two behaviors are undecided ... [ADVISOR DECISION REQUIRED]").
- `paper/ADVISOR_REVIEW_PACKAGE.md` §"What decisions are needed?" (listed fix-or-document as a still-needed decision).
- `paper/RESEARCH_METHODOLOGY_COMPARATIVE_PROPOSAL.md`'s paragraph introducing the two rule-engine behaviors (said "must be decided" / "`[ADVISOR DECISION REQUIRED]`").

No occurrence of any searched phrase was blindly replaced: every edit either (a) restated the fact in the resolved present tense while keeping the formula/magnitude accurate, or (b) was left untouched because it was already a historical/audit record correctly describing pre-fix behavior for the record.

---

## 8. Confirmation

- No backend application code was modified in this pass (`backend/app/rules/generator.py` is unchanged from the prior fix session — verified by `git diff --stat`, which shows only the prior session's 20 insertions/3 deletions, nothing new).
- No database file was modified (`running_research.db` and its backups do not appear in `git status`).
- No schema (Pydantic or ORM) was modified.
- No baseline plans were generated.
- No Gemini experiment was run.
- No evaluator was implemented.
- No E1–E8 definitions were changed (E4's *blocking status* changed; its construct, algorithm, inputs, and non-redundancy argument did not).
- `easy_run_pace` was not added to E6/E7 — confirmed by `Grep` on every edited file: the only mentions of `easy_run_pace` are in already-settled "DO NOT ADD" / "confirmed excluded" statements carried over or added for consistency, never as an active slot.
- Taper was not changed from base-anchored to peak-anchored anywhere — confirmed in §7 above.
- A full backend test run after this documentation pass still shows **201 passed, 0 failed** (re-run to confirm the documentation edits touched nothing executable).

---

## 9. Git diff summary

```
backend/app/rules/generator.py | 23 ++++++++++++++++++++---   (unchanged from the prior session — not touched in this pass)
backend/tests/test_t7_progression_fix.py                        (new in the prior session — not touched in this pass)
paper/                                                           (untracked directory; 16 files edited/created in this pass,
                                                                   listed in §1 above — no git diff is available for untracked
                                                                   files; `git status` shows the whole directory as `??`)
```

`git status --porcelain` confirms exactly two paths outside `paper/` are touched in the whole working tree (`backend/app/rules/generator.py`, modified; `backend/tests/test_t7_progression_fix.py`, new) — both from the prior session, neither touched by this documentation pass. **Nothing has been committed.**
