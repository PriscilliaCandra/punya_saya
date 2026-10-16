# CODE_AUDIT_EASY_RUN_PACE_AND_T7

> **ADDENDUM — T7 RESOLVED (added in a later session; the audit below is preserved unmodified as the historical record that motivated the fix).** The two options presented in §2 ("Recommended next action for E4/T7") have been decided and implemented: the post-cutback rebound was **FIXED** in `generate_weekly_progression_summary` (`backend/app/rules/generator.py`) — the cutback week's own reduced volume now carries forward as the progression reference for the next build step, eliminating the ~+25% rebound documented below. Taper anchoring was reviewed and **CONFIRMED CORRECT as-is** — it already matched the documented methodology (`PAPER_DRAFT.md` Table II: "times the base (starting) mileage"), so it was left unchanged; only the misleading inline code comment ("~75% of peak") was corrected. The fix is covered by a new regression suite, `backend/tests/test_t7_progression_fix.py` (7 tests), and the full backend suite passes at 201/201. **No baseline plans for the 24-profile experiment have been generated**, and no Gemini experiment has been run — this resolution is a code-level fix only. The root-cause analysis, file:line evidence, and traced pre-fix example below remain accurate as a description of what the implementation *was* before the fix and are not rewritten.
>
> **Status: Read-only source-code audit. No code, database, or experiment was modified or run (at the time this audit was originally written).**

> Scope: `D:\research s2\backend` (the actual FastAPI application — `app/`, `alembic/`, `tests/`). This supersedes the documentation-only caveats in `paper/PROFILE_FACT_SLOT_SPECIFICATION.md` (which stated the real repository was unavailable) — it is now available and was read directly. Only Read/Grep/Glob and read-only shell commands were used; no file was written, no migration run, no server started, no plan generated.

---

## 1. `easy_run_pace` Audit

### A. Existence and definition (file:line evidence)
The field exists, literally named `easy_run_pace`, in every layer:

| Layer | Location |
|---|---|
| Anonymous-research API schema | `app/schemas.py:39` — `easy_run_pace: str = Field(..., description="Current average easy-run pace in MM:SS /km (e.g. 05:45)")`; format-validated at `:41-50` |
| Consumer/auth profile schema | `app/auth/schemas.py:91` (update, optional), `:114` (response), validated at `:93` |
| DB model, research flow | `app/models.py:109` — `RunnerProfile.easy_run_pace = Column(String(10), nullable=False)` |
| DB model, consumer flow | `app/models.py:55` — `UserProfile.easy_run_pace = Column(String(10), nullable=True)` |
| Migrations | `alembic/versions/0001_baseline_research_schema.py:44`; `alembic/versions/0002_add_auth_and_ownership.py:52` |
| Route wiring | `app/routes/plan_routes.py:69` — copied verbatim from request onto the persisted `RunnerProfile` row |
| Rule-engine explainability block | `app/rules/generator.py:305` — included in `runner_inputs_utilized` |
| Gemini prompt payload | `app/ai/prompts.py:33` |
| Test factory | `tests/factories.py:46` — `easy_run_pace="05:45"` |

No frontend tree exists under the audited path (`backend/` only), so no frontend form evidence is available from this audit.

### B. Value source
**(a) Directly user-provided free text.** Validated only for `MM:SS` format (`app/schemas.py:41-50`, regex `^\d{1,2}:\d{2}$`). It is **never computed** from VDOT, `pb_5k`, or anything else — no function assigns it the output of `calculate_training_paces()` or any derivation. A grep of the full `app/` tree for `easy_run_pace` finds only schema declarations, the DB columns, the route copy, and the two read-only usages in (C)/(D) below.

By contrast, the engine's own VDOT-derived easy pace is a **separate, independently computed value** — `app/rules/vdot.py:51-108`, `calculate_training_paces()`:
```python
v_easy_slow = velocity_from_vo2(vdot * 0.65)
v_easy_fast = velocity_from_vo2(vdot * 0.74)
...
"easy": {"pace_range": f"{format_seconds_to_pace(sec_easy_fast)} - {format_seconds_to_pace(sec_easy_slow)} /km", ...}
```
Keyed `paces["easy"]` — a distinct value from `profile.easy_run_pace`, never reconciled or cross-checked against it anywhere in the codebase.

### C. Baseline usage
**No.** `generate_rule_based_plan` and `distribute_workouts_across_week` (`app/rules/generator.py:109-221`) compute every workout's `pace_target` from the VDOT-derived `paces` dict only. `profile.easy_run_pace` appears in `generator.py` exactly once — line 305, copied into the display-only `runner_inputs_utilized` explainability block — never as a computational input to any workout's pace.

### D. Gemini/prompt exposure
**Yes.** `app/ai/prompts.py:18-34`, `build_user_prompt`:
```python
"runner_profile": {
    ...
    "easy_run_pace": profile.easy_run_pace
},
```
This sits in the same prompt payload as `physiological_parameters.training_pace_zones` (the VDOT `paces` dict) and `rule_based_baseline_week` (week-1 baseline with its own VDOT-derived `pace_target`s) — Gemini receives both numbers side by side, with nothing in the prompt telling it which one is authoritative.

### E. Distinguishability from E1/E2
`easy_run_pace` is formulaically distinct from the VDOT pace (confirmed — no shared derivation). The existing validator, `validate_ai_plan` (`app/ai/validator.py:72-75`), already enforces exact-match `pace_target` fidelity against the baseline's VDOT-derived value for every structured workout field — this is E1's own mechanism. It never inspects free-text fields (`coach_overview`, `workout_execution`, `pacing_strategy`, etc.) for pace mentions at all.

So, structurally:
- Checking whether Gemini's **structured** `pace_target` matches `easy_run_pace` would duplicate E1 exactly (and would almost always fail, since the baseline's structured pace is VDOT-derived, not `easy_run_pace`-derived) — not useful.
- Checking whether Gemini's **free text** specifically echoes/uses the raw `easy_run_pace` string would not duplicate any existing check (the validator never touches free text) — structurally available, in the same sense `injury_limitations` is.

**However**, this is where the audit surfaces a problem the earlier documentation-only review could not see: a presence check on `easy_run_pace` in free text would not cleanly indicate "personalization" the way the `injury_limitations` check does. For injury, *any* structured reference necessarily reflects something Gemini generated on its own initiative, because the baseline provides zero scaffolding for it — the detection rule's action-verb gate (`substitute`, `reduce`, `swap`, …) specifically distinguishes an adaptive response from passive mention. For `easy_run_pace`, there is no equivalent "adaptation" to detect: the prompt hands Gemini this exact string already (`app/ai/prompts.py:33`), so a plan could trivially state "your reported easy pace is 05:45" by simple verbatim copy, with zero interpretive or adaptive act involved — it would look identical to genuine personalization under any simple presence/specificity test, and there is no clean way to define an "action/modification" analogue for a bare pace number without inventing new, ad hoc detection logic the task explicitly asked not to introduce without strong methodological justification.

### Recommended decision: **DO NOT ADD**

`easy_run_pace` passes the baseline-independence screen (it is not a rule-engine input, unlike the fields already excluded in `PROFILE_FACT_SLOT_SPECIFICATION.md`) — on that narrow test alone it looks eligible. But it fails a second, newly-surfaced test that `injury_limitations` passes: there is no way to distinguish genuine instantiation from incidental verbatim repetition of a value the prompt already hands Gemini outright, because unlike injury there is no "do nothing" baseline state to adapt away from — the value is just sitting in the prompt, ready to be echoed. Scoring its presence would risk crediting simple string-copying as "personalization," which is a construct-validity problem of a different and arguably worse kind than the overlap problem this field was being considered to avoid. No new field is added to E6/E7; the current single-slot (`injury_limitations`) design is unchanged.

---

## 2. E4 / T7 Baseline Audit

All evidence from `app/rules/generator.py`, function `generate_weekly_progression_summary` (lines 13–58).

| Component | Intended Methodology (documented / implied by code comments) | Actual Implementation (traced from code) | Match? | Issue |
|---|---|---|---|---|
| **Build-phase progression** | Comment at the top of the build branch states "Safe 5–8% increase capped at 10%" (a range, with a ceiling) | `increase_factor = 1.06 if base_mileage >= 20 else 1.08` — a **flat, single constant** (6% or 8% depending on starting mileage tier), applied every build week with no range and no cap logic of any kind (`generator.py:43-49`) | **No** | The code comment describes behavior the code does not implement — there is no "capped at 10%" anywhere; it is an unconditional fixed multiplier. Not dangerous, but the documentation-vs-code mismatch should be corrected (either the comment or the formula). |
| **Cutback week** | Periodic recovery reduction, roughly −15%, approximately every 4 weeks (per the T7 record carried in prior documentation) | Exactly `vol = current * 0.85` (−15%), triggered every 4th week (`w % 4 == 0`) (`generator.py:38-42`) | **Yes** | Matches as documented, in isolation. The problem is downstream (next row). |
| **Post-cutback rebound** | A cutback week should produce a genuine, lasting reduction that the following week's progression builds from — not be erased the next week | `current` (the compounding accumulator) is **never reassigned** in the cutback branch — only the displayed `vol` for that one week is reduced. The following week resumes compounding from the pre-cutback `current`, so it **exceeds the pre-cutback peak**. Traced example (`base_mileage=20.0`, 8 weeks, 6% factor): `[21.2, 22.5, 23.9, 20.3(cutback), 25.3, 26.8, 17.0(taper), 11.0(race)]`. Week 5 (25.3) is already higher than week 3's pre-cutback peak (23.9); rebound ratio week4→week5 = 25.3/20.3 ≈ **+24.6%**, closely matching the previously-recorded "~+25% rebound" issue (T7). | **No — confirms T7** | The cutback is cosmetic: it changes nothing about subsequent weeks' volume, so it provides no actual recovery stimulus in the trajectory the runner experiences from week to week — it only looks like a dip in a single week's displayed number, then a sharp, undocumented jump past the prior peak the very next week. |
| **Taper anchoring** | Comment states pre-race taper is "~75% of peak" (i.e., relative to the highest volume reached) | Both taper weeks are flat percentages of `base_mileage` — the **starting** input value, never reassigned — not of `current` (the actual peak): `vol = base_mileage * 0.85` (week `total_weeks-1`) and `vol = base_mileage * 0.55` (final week) (`generator.py:28-37`). In the traced example, the true peak is 26.8 km/week, but the taper computes 17.0 and 11.0 as fractions of the original 20.0 km/week — not 75%/55% of the 26.8 peak. | **No — confirms T7** | The code's own comment ("~75% of peak") is factually wrong relative to its own formula ("85% of starting mileage") — this is not just a documentation gap, it suggests the implementation may not match even its author's stated intent. The taper's depth relative to the *actual* peak becomes inconsistent and plan-dependent rather than a fixed, predictable percentage-of-peak reduction, which is the training-science property a taper is supposed to have. |
| **Phase tagging** | A structured per-week phase label, usable for trajectory analysis | A `phase` string ("Progressive Build Phase," "Recovery Cutback Week," "Taper Phase," "Race Week & Taper") is generated per week (`generator.py:31,36,41,48`) and included in each week's dict — but it is serialized **only inside the unstructured `rule_based_plan_json` text blob** (`app/models.py:140`). The materialized `TrainingPlanWorkout` table that consumer-facing endpoints actually serve has **no `phase` column** (confirmed by direct read of `app/models.py:189-198`) and, per its own docstring, only materializes week 1 at all — weeks 2+ exist solely inside the JSON blob. | **Partial** | Phase exists and is named, but is not queryable structured data for weeks beyond week 1. Any E4 evaluation tooling will need to parse `rule_based_plan_json` directly to recover per-week phase and volume for the full multi-week trajectory, rather than reading a workouts table. |

### Recommended next action for E4/T7

This is confirmed to be a real, precisely characterized, reproducible property of the current rule engine — not a documentation ambiguity and not something that depends on how Gemini behaves. Two options are consistent with the already-locked stance that the baseline is a controlled reference, not ground truth, and that any fix must be justified by methodology, not by making Gemini "look better":

- **(a) Fix the rule engine before generating the 24 baseline plans.** Concretely: track the actual peak separately from (or reset) the `current` accumulator after a cutback week so subsequent weeks build from the reduced value, not the pre-cutback peak; and change the taper's reference from `base_mileage` to the tracked peak. This is a small, localized change confined to one function (`generate_weekly_progression_summary`). Because no baseline plans or Gemini generations exist yet, now is the cheapest point in the project to make this change — doing it later would mean regenerating all 24 baselines and all 72 Gemini generations.
- **(b) Document the behavior as-is and score E4 against it.** Keep the current formulas, explicitly state in the methodology and paper that "trajectory fidelity" means fidelity to this specific deterministic rule (including its rebound/taper characteristics), not to an idealized periodization model, and unblock E4 on that documented basis.

This audit does not choose between (a) and (b) — that is an advisor/methodology decision, not a code-reading one, per your own framing that any baseline fix must be grounded in methodology rather than in how it affects Gemini's relative appearance. It does, however, narrow the decision from "a suspected issue described only in prose" to a precisely quantified, four-line root cause with an exact numeric example, which should make that decision easier to make and defend.

**RESOLVED (see addendum at the top of this document):** the advisor chose (a) for the rebound and, in effect, (b) for the taper — fix the rebound in code; keep the taper's formula as-is and correct only the comment, since the formula was already correct.

---

## 3. Files that would need to change later, if a fix is approved (none changed now)

- `backend/app/rules/generator.py` — `generate_weekly_progression_summary` (the only function implicated in the T7 fix, if option (a) is chosen).
- Optionally, `backend/app/models.py` (`TrainingPlanWorkout`) plus a new Alembic migration — only if the advisor additionally wants `phase` exposed as a structured, queryable column rather than parsed out of the JSON blob for evaluation convenience. This is a separate, optional improvement, not required to fix the T7 rebound/taper issue itself.
- No files require changes as a result of the `easy_run_pace` decision (DO NOT ADD) — E6/E7's methodology and slot set are unchanged.

---

## 4. Confirmation

No application code, database file, or configuration was modified. No migration was run. No server was started. No training plan was generated or regenerated. No evaluator was built or run. No E6/E7 methodology was changed. No T7 fix was applied. All findings above were obtained by reading source files only (`Read`/`Grep`/`Glob` and read-only shell listing), inside a sub-agent explicitly instructed not to modify anything, and cross-checked against the file paths and line numbers cited.
