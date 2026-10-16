# EVALUATOR_SPECIFICATION_AUDIT

**Status: Specification aligned with the CURRENT implementation. No evaluator (E1–E8) has been implemented. No baseline plans or Gemini outputs have been generated for the study. No experiment has been run. No methodology, E1–E8 definition, profile count, or repetition count was changed. Nothing has been committed.**

Labels: `LOCKED` (fixed by the methodology or by existing, tested code), `OPEN METHODOLOGY DECISION` (needs an advisor/researcher choice), `NOT YET IMPLEMENTED` (specified here, not built), `NOT AUTOMATICALLY MEASURABLE` (no defensible automated procedure exists).

---

## 1. Executive Summary

The application now implements the locked multi-week design end to end:

1. The deterministic rule engine produces a multi-week baseline (`rule_plan["weeks"]`, 4–24 weeks, each with `week_number`, `phase`, `weekly_mileage_km`, `workouts`).
2. Gemini receives the **complete** baseline schedule (`rule_based_baseline_plan`), not only Week 1, and must return a `weeks` array with one entry per baseline week.
3. The server validates **every week** against the corresponding baseline week (week count, week number, phase, per-workout fields, weekly mileage, rest/training-day counts).
4. The research path (`generate_gemini_result`) reports the true outcome of each Gemini generation with no deterministic fallback. Its statuses are `GEMINI_SUCCESS`, `GEMINI_VALIDATION_FAILED`, and `GEMINI_API_ERROR`.
5. The production path (`get_personalized_ai_plan` and `get_personalized_ai_plan_with_status`) may substitute the deterministic fallback and marks that substitution structurally as `GEMINI_FALLBACK`. Its external contract (`(plan, model_used)`, the `ai_model_used` label, and the frontend fields) is unchanged.

Consequence for the evaluator: E4 (Multi-Week Trajectory Fidelity) is **no longer blocked by missing Gemini output**, because Gemini now produces `weeks[]` with `phase` and per-week mileage. E4 remains a defined criterion that is not yet implemented. The research experiment must call the research path directly; calling the production endpoint would hide validation failures behind fallback text.

Remaining work before any evaluator or experiment: implement the E1–E8 evaluator (out of scope here), build the research harness that calls `generate_gemini_result` and holds the `profile_id` / `generation_id` bookkeeping, and freeze the open methodology decisions listed in §9.

---

## 2. Current Architecture and Source Mapping

### 2.1 End-to-end flow

```
RunnerProfileCreate (app/schemas.py)
  → generate_rule_based_plan (app/rules/generator.py)
      → rule_plan["weeks"]: N weeks (generate_weekly_progression_summary + distribute_workouts_across_week)
  → build_user_prompt (app/ai/prompts.py)
      → payload["rule_based_baseline_plan"] = rule_plan["weeks"]   (all weeks)
  → Gemini call (app/ai/llm_service.py: generate_gemini_plan)
      → JSON text → clean_json_response; malformed text → GeminiMalformedJSON(raw_text, key-redacted)
  → validate_ai_plan (app/ai/validator.py)
      → AIPersonalizedPlan.model_validate (app/ai/schemas.py)   [schema check]
      → _validate_week for each week                             [constraint check, week-prefixed errors]
      → weekly_mileage_km / workouts mirror = weeks[0]
  → research result: GeminiGenerationResult (llm_service.py)
  → production: get_personalized_ai_plan_with_status → ProductionAIOutcome
  → persistence (app/routes/plan_routes.py): rule_based_plan_json, ai_plan_json, ai_model_used
```

### 2.2 Where each step lives

| Step | Location | Notes |
|---|---|---|
| Week count and week selection | `generate_rule_based_plan` (`rules/generator.py`), `plan_duration_weeks` from the profile | 4–24 weeks |
| Baseline multi-week representation | `rule_plan["weeks"]` entries: `week_number`, `phase`, `focus_note`, `weekly_mileage_km`, `workouts` | `week_1_plan` also exists (keys: `week_number`, `weekly_mileage_km`, `focus`, `workouts`) |
| Gemini output schema | `AIWorkoutItem`, `AIWeekPlan`, `AIPersonalizedPlan` in `app/ai/schemas.py` | `AIPersonalizedPlan.weeks: List[AIWeekPlan]` is required |
| Flat week-1 mirror | `AIPersonalizedPlan.weekly_mileage_km` and `.workouts` in `app/ai/schemas.py`; set from `weeks[0]` by `validate_ai_plan` | Kept for existing frontend readers (`PlanResultPage.jsx`, `PlanDetailConsumerPage.jsx`) |
| Gemini prompt | `build_user_prompt` and `SYSTEM_PROMPT` in `app/ai/prompts.py` | Sends `rule_based_baseline_plan` (all weeks); instructs one `weeks` entry per baseline week |
| Validation | `validate_ai_plan` and `_validate_week` in `app/ai/validator.py` | Constants `DISTANCE_TOLERANCE_KM = 0.05`, `MILEAGE_TOLERANCE_KM = 0.15`; exception `AIPlanValidationError` |
| Schema validation | `AIPersonalizedPlan.model_validate` inside `validate_ai_plan` | Error message begins `schema validation failed` |
| Week-specific errors | `_validate_week` prefixes every message with `week N:` | e.g. `week 5: weekly_mileage_km changed: ...` |
| Research path | `generate_gemini_result` in `app/ai/llm_service.py` | Returns `GeminiGenerationResult`; never falls back |
| Status enum | `GenerationStatus` (`GEMINI_SUCCESS`, `GEMINI_VALIDATION_FAILED`, `GEMINI_API_ERROR`, `GEMINI_FALLBACK`) in `app/ai/llm_service.py` | `GEMINI_FALLBACK` is produced only by the production dispatcher |
| Malformed JSON handling | `generate_gemini_plan` catches `json.JSONDecodeError` and raises `GeminiMalformedJSON(raw_text)` with `GEMINI_API_KEY` replaced by `[REDACTED]` (`_redact_secrets`) | `generate_gemini_result` returns `raw_text`, `error_category="MALFORMED_JSON"` |
| Production dispatcher | `get_personalized_ai_plan_with_status` (returns `ProductionAIOutcome`), wrapped by `get_personalized_ai_plan` (returns `(plan, model_used)`) | Fallback: `generate_offline_ai_plan`, status `GEMINI_FALLBACK` |
| Offline fallback | `generate_offline_ai_plan` in `app/ai/llm_service.py` | Covers every baseline week; adds the same week-1 mirror |
| Persistence | `TrainingPlan.rule_based_plan_json`, `.ai_plan_json`, `.ai_model_used` (`app/models.py`), written in `generate_plan` (`app/routes/plan_routes.py`) | Production stores only the production outcome; the research path does not write to the database |
| Consumer materialization | `materialize_training_plan_workouts` (`app/workouts/service.py`) → `TrainingPlanWorkout` (`app/models.py`) | All weeks, 7 rows per week, from the **baseline** only; anonymous research plans get zero rows |

### 2.3 Output status contract (research path)

| Status | When | Fields populated |
|---|---|---|
| `GEMINI_SUCCESS` | Gemini returned valid JSON that passed schema and per-week constraint validation | `validated_plan` (multi-week), `raw_output` (parsed JSON as returned) |
| `GEMINI_VALIDATION_FAILED` | Malformed JSON, schema failure, or constraint failure | Malformed JSON: `raw_text` (key-redacted), `error_category="MALFORMED_JSON"`. Schema/constraint: `raw_output`, `error_category="SCHEMA_OR_CONSTRAINT"`, `error` (message with `week N:` prefix where applicable) |
| `GEMINI_API_ERROR` | HTTP/network/other exception, or missing key | `error_category="API_CALL_FAILED"` with `error` = exception type name, or `error_category="CONFIG_MISSING_KEY"` |

Research rule: no status above is ever replaced by a deterministic fallback. Secrets never appear in `error`, `raw_text`, or logs.

### 2.4 Production behavior (unchanged external contract)

`get_personalized_ai_plan` returns `(plan, model_used)`. Gemini is tried first (`LLM_PROVIDER` gemini or auto), then OpenAI (if configured), then the deterministic fallback. The internal `ProductionAIOutcome.status` is `GEMINI_SUCCESS` for an accepted Gemini plan, `GEMINI_FALLBACK` for the deterministic fallback, and `None` for an accepted OpenAI plan (the enum covers Gemini only). `model_used` labels are unchanged (`Gemini (...)`, `OpenAI (...)`, `AI Synthesis Engine (Rule-Constrained Academic Fallback)`).

---

## 3. Output Structure Comparability (baseline vs Gemini)

| Information | Baseline (`rule_plan`) | Gemini (`AIPersonalizedPlan` / `raw_output`) | Comparable? |
|---|---|---|---|
| Week number | `weeks[i].week_number` | `weeks[i].week_number` | Yes, 1:1 for every week |
| Phase | `weeks[i].phase` | `weeks[i].phase` | Yes, 1:1 for every week (validated) |
| Weekly volume | `weeks[i].weekly_mileage_km` | `weeks[i].weekly_mileage_km` | Yes, every week |
| Day | `weeks[i].workouts[j].day` | `weeks[i].workouts[j].day` | Yes |
| Workout type | `...workout_type` (free string) | `...workout_type` (free string) | Yes; validator enforces case-insensitive literal equality |
| Distance | `...distance_km` | `...distance_km` | Yes |
| Pace | `...pace_target` (string) | `...pace_target` (string) | Yes; validator enforces exact string equality |
| Intensity | `...intensity_zone` (string) | `...intensity_zone` (string) | Yes; validator enforces exact string equality |
| Rest day | `workout_type == "Rest & Recovery"`, `distance_km == 0.0` | same convention | Yes |
| Narrative | `purpose`, `recovery_instruction` only | `purpose`, `recovery_instruction`, plus `warmup_cooldown`, `workout_execution`; plan-level `coach_overview`, `personalized_insights`, `ai_personalization_summary`, `why_this_plan_was_generated` | Gemini-only (by design; the baseline makes no textual claim) |
| Profile information | `RunnerProfile` row; `explainability.runner_inputs_utilized` | Sent in the prompt (`runner_profile`); not echoed structurally | Read from the stored profile, not from AI output |
| Injury limitations | `RunnerProfile.injury_limitations`; not a numeric rule input | Candidate evidence fields listed in §6 | Gemini-only evidence |

---

## 4. E1–E8 Mapping (current implementation)

| Criterion | What it measures | Required input | Actual source (current) | Automatically measurable? | Notes / open decisions |
|---|---|---|---|---|---|
| E1 | Pace/intensity preservation | Per-workout `pace_target`, `intensity_zone`, per relevant week | Baseline `rule_plan["weeks"][i].workouts[j]`; Gemini `raw_output["weeks"][i]["workouts"][j]` (or `validated_plan`) | **YES** per relevant week and workout | Exact-string comparison per the existing validator. Text-quoted pace mismatch is not implemented (OPEN, §9) |
| E2 | Volume preservation | `weekly_mileage_km` per week; per-workout `distance_km` | Baseline `weeks[i].weekly_mileage_km`, `workouts[j].distance_km`; Gemini equivalents | **YES** against weekly volume | Tolerances `0.05` km and `0.15` km from `validator.py`; the research tolerance choice is OPEN (§9) |
| E3 | Weekly workout and rest structure | Day set, workout types, rest/training-day counts per week | Baseline and Gemini `workouts` per week | **YES** per week | Validator already enforces these literally, so validated outputs are tautologically compliant; informative evidence comes from `raw_output` of `GEMINI_VALIDATION_FAILED` results (§5) |
| E4 | Multi-week trajectory fidelity | `phase` and `weekly_mileage_km` for every week, in order | Baseline `weeks[i].phase`, `.weekly_mileage_km`; Gemini `weeks[i].phase`, `.weekly_mileage_km` | **YES** in principle (data now exists for all weeks); evaluator not yet implemented | Trajectory comparison and phase grouping follow `EVALUATION_CRITERIA_OPTION_A_DESIGN.md` §4 E4 without change |
| E5 | Output validity and completeness | Parse, schema, required weeks and workouts, non-empty required text | `AIPersonalizedPlan` (schema); `len(weeks)` vs baseline; text fields in `AIWorkoutItem`/`AIPersonalizedPlan` | **PARTIAL**: schema and week/workout count are automatic; non-empty text check is not implemented | Schema vs constraint failures share `error_category="SCHEMA_OR_CONSTRAINT"`; distinguish them by the `schema validation failed` message prefix or add a category (OPEN, §9) |
| E6 | Gemini uses the stored `injury_limitations` (profile-grounded personalization coverage) | `RunnerProfile.injury_limitations` (optional text) and Gemini text fields | `RunnerProfile.injury_limitations`; `personalized_insights.injury_prevention_note`, `ai_personalization_summary`, `why_this_plan_was_generated.ai_personalization_additions`, `coach_overview`, per-workout `recovery_instruction`/`workout_execution`/`warmup_cooldown` | **YES** (token-overlap plus action-verb rule) once the lexicon is frozen | OPEN: action-verb lexicon and contradiction codebook (§9) |
| E7 | Specificity of that personalization | Same as E6, conditional on an E6 hit | Same as E6 | **YES** conditional on E6, once the exclusion list is frozen | OPEN: `domain_generic_running_terms` exclusion list (§9) |
| E8 | Cross-repetition stability | E1–E7 outcomes for 3 Gemini generations per profile | Requires harness bookkeeping (`profile_id`, repetition index); not stored by the application | **NOT YET**: bookkeeping is a harness requirement | OPEN: agreement/spread formula; fallback-repetition handling (§9) |

Methodology definitions of E1–E8 are unchanged. This table only records where each already-defined input now lives.

---

## 5. Per-Criterion Operational Notes

**E1–E3 (structural and numeric fidelity, per week).** The validator's per-week comparison is the operational procedure. For research analysis, compute E1–E3 from `raw_output` whenever it is present (`GEMINI_SUCCESS` and `GEMINI_VALIDATION_FAILED`), not from `validated_plan`. Validated plans already passed these checks, so their E1–E3 results are constant by construction; the informative variation is in the raw outputs that failed. A `GEMINI_VALIDATION_FAILED` result with a schema failure has no per-week structure to evaluate; record it as an E5 failure.

**E4 (trajectory).** Compare `weeks[i].phase` and `weeks[i].weekly_mileage_km` in order against the baseline, group deviations by phase, and report phase mismatches separately, as specified in `EVALUATION_CRITERIA_OPTION_A_DESIGN.md`. The validator already rejects phase and mileage mismatches per week (tolerance 0.15 km), so the same caveat applies: use `raw_output` for informative results.

**E5 (validity).** Schema validity is `AIPersonalizedPlan.model_validate` (already used). Week-count and workout-count checks are in the validator. The "non-empty required text" sub-check is not implemented: the Pydantic defaults for text fields are `""`, which pass schema validation. Implementing it is new code, and is not done here.

**E6/E7 (injury personalization).** Field locations and detection rules are in §6. E6 and E7 remain injury-only, as locked.

**E8 (stability).** Unit of analysis is the profile. Agreement and spread are computed over E1–E7 outcomes of the three generations. The application does not record which generations belong to the same profile. The harness must (a) build the same profile payload for all three generations, (b) record `repetition_index`, and (c) treat `GEMINI_API_ERROR` and `GEMINI_VALIDATION_FAILED` as outcomes of that repetition rather than dropping them silently.

---

## 6. E6/E7 Injury-Specific Design (unchanged definitions)

- **Input:** `RunnerProfile.injury_limitations` (optional text). Sent to Gemini in `runner_profile.injury_limitations`; the prompt uses the literal `"None reported"` when the field is empty (`prompts.py`).
- **Applicability:** a profile with null or empty `injury_limitations` is NOT APPLICABLE for E6/E7 (excluded from numerator and denominator). The `"None reported"` string must not be treated as a stored injury.
- **Candidate evidence fields (Gemini output):** `personalized_insights.injury_prevention_note`, `ai_personalization_summary[]`, `why_this_plan_was_generated.ai_personalization_additions`, `coach_overview`, and per workout `recovery_instruction`, `workout_execution`, `warmup_cooldown`, across every week (`weeks[i].workouts[j]`). Multi-week output means the workout-level fields now exist for all weeks; E6 is still computed per plan (not per week) as defined.
- **E6 hit:** at least one sentence in those fields shares a non-stopword token with the stored text AND contains a verb from a pre-registered modification lexicon. Example: "Because your left knee pain is aggravated by downhill running, the plan avoids downhill repetitions" (hit).
- **E6 generic caution (miss, not hit):** action wording with no token overlap with the stored injury text, e.g. "Listen to your body and adjust training if needed", is an E6 **miss**. A hit requires token overlap with the stored text plus an action verb (`PROFILE_FACT_SLOT_SPECIFICATION.md` §6.4). See `FINAL_EVALUATION_SPECIFICATION_REVIEW.md` C6.
- **E6 hit with only generic running tokens (E7 = not specific):** overlap that consists only of domain-generic running terms gives E6 hit and E7 not specific.
- **E6 miss:** none of the fields share a token with the stored text.
- **E7:** conditional on E6 hit; at least one overlapping token must be specific to the stored condition, not in the `domain_generic_running_terms` exclusion list.
- **Frozen before data collection (OPEN, §9):** the lexicon, the exclusion list, and the contradiction codebook.

---

## 7. E8 Repeated-Generation Design (unchanged definition)

- Unit of analysis: profile (24 profiles, 3 generations each, 72 total). Baseline is generated once per profile and is not repeated.
- Compared quantities: E1–E7 outcomes per generation (agreement for binary criteria, spread for continuous ones).
- Agreement/spread formula: OPEN (§9).
- Bookkeeping: harness-level; the application has no generation identifier and creates a new `RunnerProfile` row per call. Identical profile payloads must be used for the three generations.

---

## 8. Potential Confounders and Controls

| # | Confounder | Current status | Control |
|---|---|---|---|
| 1 | Production fallback masks failures | Production endpoint substitutes fallback before persistence (`GEMINI_FALLBACK`) | Experiment must call `generate_gemini_result` directly; never use `/api/plans/generate` for data collection |
| 2 | Validated outputs are tautologically compliant | By construction of the validator | Analyze `raw_output` of failed generations for informative variation; report validated-success rates separately |
| 3 | No repetition tracking in the application | Confirmed; each call creates a new profile row | Harness bookkeeping outside the production database |
| 4 | Two week-1 representations (`week_1_plan` vs `weeks[0]`) with different keys | Still present in `generate_rule_based_plan` | Use `weeks[i]` for phase and focus; document once in evaluator code |
| 5 | Workout type is free text | Enforced literally by the validator | No synonym mapping; literal equality is the locked rule |
| 6 | Production tolerances (0.05 km, 0.15 km) as research sensitivity thresholds | Inherited constants | OPEN sensitivity analysis (exact equality) |
| 7 | `"None reported"` echoed into output | Prompt substitution | E6 applicability uses stored value; the phrase is not an injury |
| 8 | Units differ: JSON blobs use km; `TrainingPlanWorkout.distance_meters` uses meters | Stored schema | Research evaluation reads JSON blobs only |
| 9 | Stored plans are JSON text | `rule_based_plan_json`, `ai_plan_json` | Re-parse with `AIPersonalizedPlan` |
| 10 | 72 generations are not 72 independent observations | Locked design | Analyze nested by profile |
| 11 | Plan lengths 4–24 weeks | Varies by profile | Phase boundaries come from the `phase` field; do not hard-code week numbers |
| 12 | Gemini output token size grows with plan length | Full schedule is sent in the prompt; `max output tokens` not set | Record prompt and response sizes; OPEN (§9) |
| 13 | Schema vs constraint failures share one category | `error_category="SCHEMA_OR_CONSTRAINT"` | Use the message prefix or add a category before E5 analysis |

---

## 9. Open Methodology Decisions

1. Frozen E6/E7 lexicons: the action-verb lexicon, the `domain_generic_running_terms` exclusion list, and the S7 contradiction codebook. Must be versioned and pre-registered before the 72 generations.
2. E8 agreement/spread formula (max−min vs coefficient of variation) and the rule for handling `GEMINI_API_ERROR` / `GEMINI_VALIDATION_FAILED` repetitions.
3. Tolerance for the research analysis: keep the production 0.05 km / 0.15 km, add an exact-equality sensitivity analysis, or both.
4. Whether E1 includes a text-quoted pace/zone sub-check (no extractor exists); default is structured fields only.
5. Whether E5 reports schema failures separately from constraint failures (a new error category or a parsed-message rule).
6. Whether E5's non-empty text check is part of E5 or reported as a separate completeness statistic.
7. Token-cost and prompt-size reporting for 24-week plans, and whether to set a max output token limit (locked as an open item in `RESEARCH_METHODOLOGY_LOCK.md`).
8. Harness design for repetition bookkeeping (not a methodology question; an engineering design task before data collection).

---

## 10. Proposed Evaluator Input/Output Contract (specification only, not implemented)

```text
Input (harness-level, outside the production DB)
  - profile_id, repetition_index (1..3), profile payload used for the generation
  - Research result: GeminiGenerationResult (status, raw_output or raw_text, validated_plan, error_category, error)
  - Baseline: rule_plan from generate_rule_based_plan (one per profile, generated once)
↓
Normalization
  - Use raw_output for E1–E5 when present; validated_plan only as a cross-check
  - Read phase and week_number from weeks[i]; never from week_1_plan
↓
Per-criterion evaluation (E1–E8, as defined in EVALUATION_CRITERIA_OPTION_A_DESIGN.md)
↓
Output row (proposed shape)
  profile_id | repetition_index | criterion | scope (week_k / plan) | raw_value | normalized_value |
  status (HIT/MISS/NA/PASS/FAIL/BLOCKED) | evidence | generation_status | error_category | notes
```

This is a specification for the future evaluator's working data. It is not a database migration and has not been implemented.

---

## 11. Recommended Implementation Order (next steps, not undertaken here)

1. Freeze the open methodology decisions in §9 (items 1–3 at minimum), before any generation.
2. Build the research harness: calls `generate_gemini_result`, records statuses and raw outputs, and holds profile and repetition bookkeeping outside the production database.
3. Implement the evaluator E1–E8, reusing the validator's comparison logic where it applies and adding only the new sub-checks listed in §4–§5.
4. Only then generate 24 baselines and 72 Gemini generations, and run the evaluator.

---

## 12. Historical Record (pre-implementation finding, preserved)

Before the multi-week Gemini implementation, this document stated that `AIPersonalizedPlan` was flat and single-week, that the prompt sent only `rule_plan["week_1_plan"]`, and that E4 could not be computed because Gemini produced no multi-week output. Those statements were accurate for the code at that time and are superseded by §1–§4. They are kept here as the record of why the implementation changed.

---

## 13. Confirmation

This documentation update changed no backend logic, database, schema, frontend, methodology, or experiment data. Only comments and docstrings in backend source were corrected (see the accompanying report). No evaluator was implemented. No baseline or Gemini plan was generated for the study. Nothing has been committed.
