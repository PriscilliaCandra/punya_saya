# FINAL_EVALUATION_SPECIFICATION_REVIEW

**Status: specification review only. No evaluator code, experiment harness, baseline generation, Gemini generation, database change, production change, methodology change, or git commit was performed. Every criterion below is either fully specified from locked methodology and existing code, or marked NEEDS_DECISION / BLOCKED with the exact open question. Nothing has been filled in by assumption.**

Source of truth used: `RESEARCH_METHODOLOGY_LOCK.md` §5 and the E1–E8 definitions in `EVALUATION_CRITERIA_OPTION_A_DESIGN.md` (the E1–E8 names and roles the user has fixed); `EVALUATION_CRITERIA_RECONCILIATION.md`; `EVALUATION_CRITERIA_FINAL_CONSISTENCY_REVIEW.md`; `PROFILE_FACT_SLOT_SPECIFICATION.md` (E6/E7 detection rules); current code in `backend/app/ai/{schemas,prompts,validator,llm_service}.py`, `backend/app/rules/generator.py`, and `backend/tests/test_llm_validation.py`, `test_multi_week_gemini.py`.

---

## 0. Corrections found during this review (read first)

These are factual corrections to premises or to earlier documentation. None changes a locked methodology decision.

| # | Finding | Evidence | Consequence |
|---|---|---|---|
| C1 | **There is no pace tolerance.** The `0.15 km` tolerance applies only to weekly mileage. Pace and intensity zone are compared by exact string equality after `.strip()`. The `0.05 km` tolerance applies to each workout's `distance_km`. | `validator.py`: `DISTANCE_TOLERANCE_KM = 0.05` (line 10), `MILEAGE_TOLERANCE_KM = 0.15` (line 11), `pace_target` and `intensity_zone` exact compare (lines 72–79) | E1 uses exact equality. The task premise "0.15 km pace" is not implemented and is not in the lock. |
| C2 | **The validator is fail-fast.** It raises on the first violation, so one generation yields at most one error message. | `validate_ai_plan` raises inside the loops (`_validate_week`) | Violation counts per generation cannot be read from `error`. The evaluator must recompute each criterion from `raw_output` rather than parse the message. |
| C3 | **The validator reorders workouts.** `validated_plan` lists workouts in baseline Monday–Sunday order. `raw_output` keeps Gemini's order. | `validator.py` lines 106–109 (`by_day` reorder) | Match workouts by `day`, never by list index, on `raw_output`. |
| C4 | **E6 applicability is inconsistent in code.** The prompt sends the stored injury string verbatim, or the literal `"None reported"` when empty. The generator and the offline fallback treat `none`, `no`, `n/a`, `-` as "no injury". | `prompts.py` line 32; `generator.py` line 97/162 (`not in ["none","no","n/a","-"]`); `llm_service.py` `has_injury` | Applicability needs an explicit decision (§E6). |
| C5 | **E4 tolerance wording is inconsistent in the design doc.** `EVALUATION_CRITERIA_OPTION_A_DESIGN.md` E4 says "same tolerance convention as E2" (absolute km, 0.15) but its algorithm uses a relative percentage deviation. | OPTION_A E4 item 5 (`dev[k] = (g − b) / b`) vs E2 item 5 (`|g − b| ≤ 0.15`) | E4 tolerance is NEEDS_DECISION. Option A text was not changed. |
| C6 | **Earlier audit mislabeled a generic caution.** `EVALUATOR_SPECIFICATION_AUDIT.md` §6 called "Listen to your body and adjust training if needed" an E6 hit. Under `PROFILE_FACT_SLOT_SPECIFICATION.md` §6.4 an E6 hit requires token overlap with the stored injury text, so that sentence is an E6 **miss**. | `PROFILE_FACT_SLOT_SPECIFICATION.md` §6.4 items 3–4 | Corrected in this review (§E6). The earlier audit line is corrected in place (see §10). |
| C7 | **Lock §5 lists 8 draft criteria that differ in naming from the adopted E1–E8.** The lock says the count is locked at 8 but the definitions must be reconciled. The reconciled E1–E8 are the Option A definitions, which the user has fixed. | `RESEARCH_METHODOLOGY_LOCK.md` §5 vs `EVALUATION_CRITERIA_OPTION_A_DESIGN.md` §1 | This review uses the Option A E1–E8 definitions. The lock's draft list is not used as an operational source. |
| C8 | **Gemini truncation is not detected.** `generate_gemini_plan` does not read `finishReason`, and `generationConfig` sets no `maxOutputTokens`. A cut-off JSON is reported as `MALFORMED_JSON`, indistinguishable from other malformed output. | `llm_service.py` `generate_gemini_plan` payload and return path | E5 truncation sub-category requires a small code change (§E5, §Prerequisites). |

---

## 1. E1 — Pace/Intensity Fidelity

| # | Field | Specification |
|---|---|---|
| 1 | Criterion ID | E1 |
| 2 | Name | Pace/Intensity Fidelity |
| 3 | Research question | Did Gemini keep each workout's deterministic pace and intensity-zone target, as the deterministic baseline defines them? (Constraint fidelity / reference comparison — not baseline quality.) |
| 4 | Input data | Per generation: `raw_output["weeks"][i]["workouts"][j]`, fields `day`, `pace_target`, `intensity_zone`. Per baseline: `rule_plan["weeks"][i]["workouts"][j]`, same fields. |
| 5 | Source | Gemini: `GeminiGenerationResult.raw_output` (research path). Baseline: `generate_rule_based_plan(profile)["weeks"]`, deterministic and stored once per profile. Never `validated_plan`. |
| 6 | Unit of analysis | Workout (week k, day d). Each workout yields one match value per field. |
| 7 | Operational rule | Match `(week_number, day)`. For each field in {`pace_target`, `intensity_zone`}: match ⇔ `gemini.strip() == baseline.strip()`, case-sensitive. **No numeric tolerance** (C1). Rest days are included because the validator compares them too (`pace_target` = `"N/A"`, zone = `"Rest (Zone 1 or Complete Rest)"` in the baseline). Rest-day inclusion is listed as a decision in §12 item E1-b. |
| 8 | Output | Per workout: `pace_match` (bool), `zone_match` (bool). Per week: count of matched workouts / total workouts. Per generation: count of matched workouts / total workouts (all weeks). |
| 9 | Aggregation | Report per workout, per week, and per generation. Profile-level aggregation is not specified by the lock and is left to E8 and the analysis plan (NEEDS_DECISION, §12). |
| 10 | Repeated generations | Each generation is evaluated independently. Stability across the three generations is E8, not E1. |
| 11 | Missing / invalid data | (a) `GEMINI_SUCCESS` or `GEMINI_VALIDATION_FAILED` with a `raw_output` that parses into `AIPersonalizedPlan`: evaluate all workouts. (b) `raw_output` absent (malformed JSON, API error): E1 = NA for that generation. (c) `raw_output` present but a required field missing or of the wrong type: the schema fails, so the generation is NA for E1 (a per-field partial parse would be a new rule — NEEDS_DECISION §12 E1-c). A missing `day` in Gemini output is a mismatch on every field of that workout, not NA. |
| 12 | Example PASS | Baseline week 3, Tuesday: `pace_target "05:15 - 05:30 /km"`, zone `"Zone 4 (Threshold)"`. Gemini week 3, Tuesday: same two strings. Both match. |
| 13 | Example FAIL | Same baseline. Gemini: `pace_target "05:00 - 05:15 /km"`. `pace_match = false`, `zone_match` depends on the zone string. |
| 14 | Potential confounders | Free-text pace mentions are not checked (no extractor exists; C-list §12 E1-a). Whitespace only is normalized, so `"05:15–05:30"` (en dash) fails. Rest-day copies inflate the match rate if included. |
| 15 | Overlap | E1 vs E2 (none: pace/zone vs distance). E1 vs E3 (low: zone correlates with workout type, but E1 compares strings, E3 compares types). E1 vs E4 (none). |
| 16 | Readiness | **NEEDS_DECISION** — one blocking item: §12 E1-a (text-quoted paces in or out) and E1-c (partial-field handling). The structured exact-match rule itself is READY. |

---

## 2. E2 — Volume Fidelity

| # | Field | Specification |
|---|---|---|
| 1 | Criterion ID | E2 |
| 2 | Name | Volume Fidelity |
| 3 | Research question | Did Gemini keep the deterministic weekly volume and per-workout distance in every week? |
| 4 | Input data | Per generation: `raw_output["weeks"][i]["weekly_mileage_km"]`, `raw_output["weeks"][i]["workouts"][j]["distance_km"]`. Per baseline: `rule_plan["weeks"][i]["weekly_mileage_km"]`, `workouts[j]["distance_km"]`. |
| 5 | Source | As E1. Baseline `weekly_mileage_km` is `round(sum(distance_km), 1)` (`generator.py`). |
| 6 | Unit of analysis | Week (weekly mileage) and workout (distance). |
| 7 | Operational rule | Week k: `pass_mileage[k] ⇔ |g_k − b_k| ≤ 0.15` (validator constant `MILEAGE_TOLERANCE_KM`, lock §5 item 3). Workout: `pass_distance ⇔ |g − b| ≤ 0.05` (`DISTANCE_TOLERANCE_KM`). Comparison is always to the **same week number** of the baseline. Cutback and taper weeks are compared to their own baseline week, so a deliberate −15% cutback or taper volume is not a violation, because the baseline defines that week's volume. Phase is not used to excuse a deviation. |
| 8 | Output | Per week: `dev_mileage_km` (signed), `pass_mileage`. Per workout: `dev_distance_km`, `pass_distance`. Per generation: count of passing weeks; count of passing workouts. |
| 9 | Aggregation | Per week; across all weeks per generation (count and max |dev|). Profile-level via E8. |
| 10 | Repeated generations | Independent per generation; spread across generations is E8. |
| 11 | Missing / invalid data | As E1. Missing `weekly_mileage_km` or `distance_km` fails schema (NA). Rounding: values are compared as floats; no extra rounding is applied beyond the tolerance. |
| 12 | Example PASS | Baseline week 5 mileage 26.8 km; Gemini 26.9 km. |0.1| ≤ 0.15 → pass. |
| 13 | Example FAIL | Baseline week 5 mileage 26.8 km; Gemini 27.2 km → 0.4 > 0.15 → fail. |
| 14 | Potential confounders | Comparing to Week 1 or to peak instead of the same week would falsely flag cutback and taper weeks (avoided by the same-week rule). The 0.05/0.15 km tolerances are production constants, not a research-validated threshold (lock §5 item 3; sensitivity analysis is a decision, §12 E2-a). |
| 15 | Overlap | E2 vs E4: E4 must not repeat magnitude comparison (see §E4). E2 vs E3: none (E3 counts days, not kilometres). |
| 16 | Readiness | **READY** for the primary rule. The exact-equality sensitivity analysis is NEEDS_DECISION but is **not blocking**. |

---

## 3. E3 — Structure Fidelity

| # | Field | Specification |
|---|---|---|
| 1 | Criterion ID | E3 |
| 2 | Name | Structure Fidelity |
| 3 | Research question | Did Gemini keep each week's schedule structure: which days are training or rest, the workout type of each day, and the number of sessions? |
| 4 | Input data | Per generation and week: set of `day` values; per day `workout_type`; count of non-rest days. Per baseline week: same. |
| 5 | Source | As E1. |
| 6 | Unit of analysis | Week. Sub-checks are reported separately (per the Option A design: never collapsed into one pass/fail). |
| 7 | Operational rule | Per week k, four sub-checks: (a) **day set**: the set of days in `raw_output` equals the baseline's set of 7 days, no duplicates, no unknown day; (b) **workout type**: for each day, `workout_type.strip().lower()` equals the baseline's (case-insensitive, validator rule `validator.py` line 64); (c) **rest-day count**: count of `workout_type == "rest & recovery"` (case-insensitive) equals `7 − training_days_per_week` (the same as the baseline's rest count); (d) **training-day count**: non-rest count equals `training_days_per_week`. Workout order in the list is not evaluated (not part of the methodology; C3). |
| 8 | Output | Per week: four booleans. Per generation: count of weeks passing each sub-check. |
| 9 | Aggregation | Per week; per generation across weeks. Reported per sub-check, not as one combined pass. |
| 10 | Repeated generations | Independent per generation (E8 for spread). |
| 11 | Missing / invalid data | Missing or duplicate day: sub-check (a) fails for that week. Missing week: E3 NA for the missing weeks, and the generation's week count fails (reported under E5). |
| 12 | Example PASS | Baseline week 2: Mon Easy, Tue Interval, Wed Rest, Thu Easy, Fri Rest, Sat Long, Sun Rest. Gemini week 2 has the same day set, same types (case-insensitive), 3 rest days, 4 training days. |
| 13 | Example FAIL | Gemini week 2 renames `"Interval Training"` to `"Threshold Run"`: sub-check (b) fails for Tuesday. |
| 14 | Potential confounders | Literal-string rule means synonym labels fail. This is the locked rule. Do not add a synonym map (the validator never allowed one; a mapping would hide violations). Rest-day label `"Rest & Recovery"` is a hard-coded literal in `validator.py` line 92. |
| 15 | Overlap | E3 vs E1: low (types vs strings; a type change usually also changes zone, which E1 then also records; accepted as a shared consequence, not double counting in the same sub-check). E3 vs E4: E4 uses phase, not day structure; no overlap. |
| 16 | Readiness | **READY**. All rules are decided by the locked methodology and the existing validator. Implementation requires fail-fast avoidance (C2): evaluate from `raw_output`, not from the first error. |

---

## 4. E4 — Multi-Week Trajectory Fidelity

| # | Field | Specification |
|---|---|---|
| 1 | Criterion ID | E4 |
| 2 | Name | Multi-Week Trajectory Fidelity |
| 3 | Research question | Did Gemini's multi-week plan follow the deterministic trajectory's phase pattern (build → cutback → build → taper → race), so that the plan's shape across weeks matches the baseline? |
| 4 | Input data | `raw_output["weeks"]` and `rule_plan["weeks"]`, each entry `week_number`, `phase`, `weekly_mileage_km`. |
| 5 | Source | As E1. |
| 6 | Unit of analysis | Plan (the full ordered sequence of weeks) for the trajectory outcome; week for per-week reporting. |
| 7 | Operational rule | **Alignment:** require `len(gemini.weeks) == len(baseline.weeks)` and `gemini.weeks[k].week_number == baseline.weeks[k].week_number` for all k. If either fails, E4 = NA with reason "week alignment" (the validator also rejects this, reported under E5). **Phase alignment:** `gemini.weeks[k].phase.strip() == baseline.weeks[k].phase.strip()` (case-sensitive; validator line equivalent). **Trajectory shape:** the phase sequence must match exactly. The transition type is then fixed by the baseline phases. **Volume trajectory:** NEEDS_DECISION (§12 E4-a) — the Option A algorithm uses relative deviation, which overlaps E2 (C5). |
| 8 | Output | Per week: `phase_match`. Per plan: `phase_sequence_match` (bool) and `phase_mismatch_count`. If volume trajectory is decided later: per phase group, the deviation distribution as specified in OPTION_A §4 E4. |
| 9 | Aggregation | Plan-level for the sequence outcome. Per phase group (build, cutback, taper, race) for any volume component. Never averaged into one number with other criteria. |
| 10 | Repeated generations | Independent per generation; across generations via E8. |
| 11 | Missing / invalid data | Week alignment failure → NA (not 0). Missing `phase` → schema failure → NA. A phase label that differs in spelling counts as a mismatch. |
| 12 | Example PASS | Baseline phases (8 weeks): Build, Build, Build, Cutback, Build, Build, Taper, Race. Gemini has the same eight labels in the same order. |
| 13 | Example FAIL | Gemini labels week 4 `"Progressive Build Phase"` instead of `"Recovery Cutback Week"`. `phase_sequence_match = false`, mismatch at week 4. |
| 14 | Potential confounders | Phase labels are produced by the deterministic engine and copied by Gemini. Because the validator already enforces phase per week, validated outputs pass E4 by construction; informative E4 data come from `raw_output` of `GEMINI_VALIDATION_FAILED` results. A phase-only E4 is largely equivalent to the validator's per-week phase check aggregated over the plan. |
| 15 | Overlap | **E4 vs E2 (the central risk):** E2 compares magnitude per week; E4 must not repeat magnitude. If the volume component of E4 is kept, it duplicates E2 in every week, so this component needs a decision (§12 E4-a). Phase-sequence component: independent of E2 (no kilometres). E3 vs E4: day structure vs phase labels; distinct. |
| 16 | Readiness | **NEEDS_DECISION** — E4-a: keep a volume-trajectory component (and if so its distinct rule, tolerance, and whether it duplicates E2) or restrict E4 to the phase-sequence check. The phase-sequence check itself is READY. |

---

## 5. E5 — Output Validity & Completeness

E5 is split into four categories, each with its own result. The current code does **not** distinguish them: `error_category` is `SCHEMA_OR_CONSTRAINT` for both schema and constraint failures (`llm_service.py`).

| Sub-category | Definition | Current code | Status |
|---|---|---|---|
| 5a. Schema validity | `raw_output` parses into `AIPersonalizedPlan` (all required fields present and correctly typed) | `AIPersonalizedPlan.model_validate` inside `validate_ai_plan`; message begins `schema validation failed` | Implemented, but not separated from constraint failures in `error_category` |
| 5b. Structural completeness | Week count equals baseline; each week has the same week number; each week has the same number of workouts as the baseline (7) | Week count check (`week count mismatch`), week-number and workout-count checks in `_validate_week` | Implemented; fail-fast (C2) |
| 5c. Required text / field completeness | Non-empty required text (defined below) | **Not implemented** | NEEDS_DECISION (definition §5.1) |
| 5d. Constraint violation | Any E1–E4 failure, or any validator constraint failure (distance, pace, zone, mileage, type, rest/training count, phase) | `validate_ai_plan` constraint checks | Implemented, but not separated from 5a |

**Truncation** (lock §E5 mentions truncation): not detected (C8). A cut-off JSON becomes `MALFORMED_JSON`. Decision needed on capturing `finishReason` (§12 E5-b).

### 5.1 What "required text is not empty" means

Taken from the lock's criterion 6 text, applied to the actual schema:

- **Per non-rest day** (rest days are defined by the **baseline**, not by Gemini, so Gemini cannot change which days need text): `warmup_cooldown`, `workout_execution`, `recovery_instruction`, `purpose` each has `strip() != ""`.
- **Plan-level**: `coach_overview` non-empty; `ai_personalization_summary` is a non-empty list; `personalized_insights` and `why_this_plan_was_generated` present with their sub-fields.
- **Sub-field granularity is not defined by the lock.** The schema defaults sub-fields to `""` or `[]`, which pass schema validation. Whether all three `personalized_insights` sub-fields, or both `why_this_plan_was_generated` sub-fields, must be non-empty is **NEEDS_DECISION** (§12 E5-c). Nothing is assumed here.
- "Non-empty" means non-whitespace. Length thresholds are not part of the lock and are not used.

### 5 — per-criterion table

| # | Field | Specification |
|---|---|---|
| 1 | Criterion ID | E5 |
| 2 | Name | Output Validity & Completeness |
| 3 | Research question | Is each generation a usable, complete multi-week plan (schema-valid, structurally complete, with the required text), separately from whether its numbers respect the constraints? |
| 4 | Input data | `raw_output` (or `raw_text` when JSON is malformed); the `AIPersonalizedPlan` schema; the baseline day/rest structure; `generation status`. |
| 5 | Source | Research path result (`GeminiGenerationResult`). |
| 6 | Unit of analysis | Generation. |
| 7 | Operational rule | Report 5a, 5b, 5c, 5d as four separate booleans (or counts). Not a composite. Truncation is a separate sub-count once captured. |
| 8 | Output | Per generation: `schema_valid`, `structure_complete`, `text_complete` (once §12 E5-c decided), `constraint_violations` (count and category list). Per profile and across profiles: proportions. |
| 9 | Aggregation | Per generation; proportion of generations per profile (E8 unit). |
| 10 | Repeated generations | Each of the three generations is counted as one attempt. An attempt that errors counts as an attempt with status `GEMINI_API_ERROR`. |
| 11 | Missing / invalid data | `GEMINI_API_ERROR`: 5a–5d = NA, status reported. `MALFORMED_JSON`: 5a = fail (not parseable); 5b–5d = NA. Production fallback output is never counted (§Research data flow). |
| 12 | Example PASS | Valid JSON, 8 `weeks`, 7 workouts each, all required text non-empty on the 6 non-rest days. |
| 13 | Example FAIL | `weeks` has 7 entries for an 8-week baseline: 5b fails; 5a passes if the rest of the schema is valid. |
| 14 | Potential confounders | Pydantic defaults make empty strings schema-valid, so 5a alone overstates completeness (hence 5c). Truncation looks like malformed JSON. The validator's fail-fast behavior hides multiple structural defects behind one message (C2). |
| 15 | Overlap | E5 vs E1–E4: 5d repeats constraint checks by design; 5a and 5b are separate from E1–E4 and must stay separate. E5 vs E6: 5c text completeness could mask E6 (empty text cannot reference anything), so E6 must report NA for empty text rather than miss. |
| 16 | Readiness | **NEEDS_DECISION** — E5-a: whether 5a/5b/5c/5d are separate outputs (recommended by this review, consistent with the request) and the separate category fields (minimum change in §Prerequisites); E5-b: capture `finishReason` to detect truncation; E5-c: sub-field granularity for non-empty. |

---

## 6. E6 — Profile-Grounded Personalization Coverage

Locked slot: `injury_limitations` only. No new slot is added.

| # | Field | Specification |
|---|---|---|
| 1 | Criterion ID | E6 |
| 2 | Name | Profile-Grounded Personalization Coverage |
| 3 | Research question | Does Gemini's generated plan actually use the runner's stored injury limitation? |
| 4 | Input data | `profile.injury_limitations` (stored value); Gemini text fields (§6 field list below). |
| 5 | Source | Stored: `RunnerProfile.injury_limitations` (the profile used to generate the plan). Gemini: `raw_output` text fields. |
| 6 | Unit of analysis | Generation (per plan, across all weeks). |
| 7 | Operational rule | **Applicability:** the slot applies when the stored value is non-null and `strip() != ""`. **Sentinel values** `none`, `no`, `n/a`, `-` (case-insensitive) — NEEDS_DECISION (§12 E6-a; C4). **Searched fields:** `coach_overview`; `personalized_insights.{pacing_strategy, injury_prevention_note, nutrition_and_recovery_advice}`; `ai_personalization_summary[]`; `why_this_plan_was_generated.{key_influencing_factors[], ai_personalization_additions}`; for every week and every non-rest workout: `warmup_cooldown`, `workout_execution`, `recovery_instruction`, `purpose`. **Hit:** at least one sentence in a searched field shares at least one content token with the stored text (after lowercasing and removing stop words) **and** contains a verb from the action lexicon. **Miss:** no such sentence. **Generic caution** (action verb, no token overlap) is a **miss** for E6 (C6). It is recorded separately as a count of "action sentences without overlap", not as a hit. |
| 8 | Output | Per generation: `applicable` (bool), `hit` (bool), `hit_sentence_count`, and the matched token and verb for auditability. |
| 9 | Aggregation | Proportion of applicable generations with hit, per profile and overall. Profiles without the slot are excluded from the denominator (NA), never counted as misses. |
| 10 | Repeated generations | Each generation independently. Coverage consistency across the three is E8. |
| 11 | Missing / invalid data | Non-applicable profile: NA. Malformed JSON or API error: NA (no text to search). Schema-valid output with empty text: hit = false (miss), and 5c fails in E5, so the reader sees both. The literal `"None reported"` produced by the prompt is never a stored injury and must not match. |
| 12 | Example PASS | Stored: `"mild left knee pain, aggravated by downhill running"`. Gemini `personalized_insights.injury_prevention_note`: "Because your left knee pain is aggravated by downhill running, the plan avoids downhill repetitions." Tokens `knee`, `downhill` overlap; `avoids` is an action verb. Hit. |
| 13 | Example FAIL | Same stored value. Gemini: "Listen to your body and adjust training if needed." No overlap. Miss (generic caution). |
| 14 | Potential confounders | Stop-word and action-lexicon choice (§12 E6-b). Stored-text tokens that are generic running words ("running") can create a false hit: E6 counts them, E7 excludes them. Prompt echo of the stored value (the text is in the prompt, so it may be copied verbatim: a copied injury phrase counts as a hit). Whether verbatim copying counts as "use" is a decision (§12 E6-c). |
| 15 | Overlap | E6 vs E7: E7 is conditional on E6 hit (see E7). E6 vs E1–E5: none; E6 uses text, the others use structure. E6 vs E5c: empty text makes E6 miss, which the design accepts (§5 row 15). |
| 16 | Readiness | **NEEDS_DECISION** — E6-a (sentinel handling), E6-b (freeze of the stop-word list and action lexicon), E6-c (is verbatim copy a use). No expert judgment is needed for any of them; each is a frozen list or a rule. |

---

## 7. E7 — Profile-Grounded Personalization Specificity

| # | Field | Specification |
|---|---|---|
| 1 | Criterion ID | E7 |
| 2 | Name | Profile-Grounded Personalization Specificity |
| 3 | Research question | When Gemini references the stored injury limitation, does the reference rely on a token specific to the runner's own condition, rather than generic running vocabulary? |
| 4 | Input data | E6 result for the generation; the hit sentence and its overlapping tokens; the stored injury text. |
| 5 | Source | As E6. |
| 6 | Unit of analysis | Generation, conditional on E6 hit. |
| 7 | Operational rule | Conditional: evaluated only when E6 = hit. Among the overlapping tokens (from the hit sentence and the stored text), **specific** ⇔ at least one token is not in the frozen exclusion list of domain-generic running terms (NEEDS_DECISION §12 E7-a). **Generic** ⇔ all overlapping tokens are in that list. The stored text is the only comparison target; no external wordlist defines "generic personalization". |
| 8 | Output | Per generation with E6 hit: `specific` (bool), overlapping token list. E6 miss: NA. |
| 9 | Aggregation | Proportion of E6-hit generations that are specific, per profile and overall. Profiles with no hit are excluded and their count is reported. |
| 10 | Repeated generations | Each generation independently; specificity consistency across the three is E8. |
| 11 | Missing / invalid data | E6 NA or miss → E7 NA (never 0). Stored injury with only stop-words (no content token): E7 = NA, reported. |
| 12 | Example PASS | Overlap: `knee` (not a running term) → specific. |
| 13 | Example FAIL | Hit sentence: "Keep your running easy this week, with lower volume." Stored text "knee pain, aggravated by running". Overlap: `running` only → generic. |
| 14 | Potential confounders | The exclusion list decides the result; a short list keeps E7 narrow, a long list can make a specific token look generic. Verbatim copy of the stored phrase is specific by construction (ties to E6-c). Contradiction/safety checks are **not** part of E7 (see below). |
| 15 | Overlap | E7 vs E6: E7 cannot occur without E6 hit (by design). Not a duplicate: E6 is presence, E7 is which tokens carry the reference. |
| 16 | Readiness | **NEEDS_DECISION** — E7-a: exclusion list content (frozen, versioned, documented before experiment); E7-b: contradiction codebook is **out of scope** unless the advisor decides otherwise (see below). |

### 7.1 Codebooks: frozen, versioned, documented?

- **Action-verb lexicon (E6), stop-word list (E6), domain-generic running-term exclusion list (E7):** these are finite, rule-based lists. They must be **frozen before experiment**, **versioned** (for example `v1`), and **documented** in an appendix with the exact contents. Their contents are not written here because the user asked that no codebook be invented without a decision.
- **Contradiction codebook** (what Gemini text would be unsafe given the stored limitation): this review recommends it is **not** part of E6/E7. It would require deciding which advice is unsafe, a judgment step that the study design otherwise excludes (no expert evaluation). If the advisor wants it, it becomes a separate criterion or a separately documented, frozen rule, and it must be decided before experiment. Until then E6/E7 measure use and specificity only, and the paper states that safety of text is not evaluated (`PAPER_DRAFT.md` §V limitation 2).

---

## 8. E8 — Cross-Repetition Stability

| # | Field | Specification |
|---|---|---|
| 1 | Criterion ID | E8 |
| 2 | Name | Cross-Repetition Stability |
| 3 | Research question | For the same runner profile, are the evaluated characteristics of the three Gemini generations consistent with each other? |
| 4 | Input data | Per profile: the three generation results (status, E1–E7 outcomes). |
| 5 | Source | Harness bookkeeping (`profile_id`, `repetition_index` 1–3) joined to the per-generation evaluations. The application does not store this (confirmed earlier: no `generation_id`). |
| 6 | Unit of analysis | Profile (one profile with three generations). |
| 7 | Operational rule | **Compared quantities:** the E1–E7 *outcomes* of each generation (not text, not extracted wording). **Binary outcomes** (E1 match per workout summarized as a rate or pass per week, E3 sub-checks, E4 phase-sequence match, E5 sub-checks, E6 hit, E7 specific): agreement is measured across the successful generations. **Continuous outcomes** (E1 match rate, E2 deviations, E4 volume if kept): spread across generations. **Formula: NEEDS_DECISION** (§12 E8-a: max−min vs coefficient of variation; per-criterion agreement rule). Identical outputs are not required; the criterion measures consistency of evaluated characteristics. |
| 8 | Output | Per profile and criterion: `n_success`, agreement or spread value, reported as a distribution across profiles. No pass/fail threshold. |
| 9 | Aggregation | Across the 24 profiles, distribution per criterion. Descriptive only (no inference in this review). |
| 10 | Repeated generations | This criterion is the handling of repetitions. Failed generations: see 11. |
| 11 | Missing / invalid data | **Failed attempts** (`GEMINI_API_ERROR`, `GEMINI_VALIDATION_FAILED`): counted in `n_attempted`; excluded from the agreement/spread of criteria where they are NA; **the minimum number of successful generations required to compute E8 is NEEDS_DECISION** (§12 E8-b). **Missing generation** (harness did not run it): NEEDS_DECISION, because the protocol does not say whether to re-run. Production fallback output is never a generation for E8. |
| 12 | Example PASS | Three generations, all with E6 hit: agreement 3/3 for E6. |
| 13 | Example FAIL (instability) | E1 match rate per generation: 0.98, 0.62, 0.97 — spread 0.36 (value of the spread rule depends on E8-a). |
| 14 | Potential confounders | A fallback repetition would look more stable than real Gemini variation, so it must never be counted (production path is excluded). A wording change that keeps the same E1–E7 outcomes is consistency, not instability, by definition. Repetitions made from different profile payloads (harness error) would appear as instability: the harness must guarantee identical payloads. |
| 15 | Overlap | E8 vs E1–E7: E8 consumes their outputs and does not measure the workout content itself, so it is not a duplicate in construct, but its numbers are derived from E1–E7 outcomes. |
| 16 | Readiness | **NEEDS_DECISION** — E8-a (formula per outcome type), E8-b (minimum successes), E8-c (rule for missing generations). The "consistency of characteristics, not identity" principle is decided. |

---

## 9. Cross-criterion overlap check

| Pair | Overlap risk | Why still distinct | Do the rules separate them? |
|---|---|---|---|
| E1 vs E2 | Low | Pace/zone strings vs distances | Yes: different fields, different rules |
| E1 vs E3 | Low–moderate | A workout-type change usually also changes its zone | Yes: E1 compares strings for each field; E3 compares type labels and counts. A type change is recorded in both, which is a consequence, not a duplicate check |
| E1 vs E4 | None | E4 uses phase labels and (if kept) volume | Yes |
| E2 vs E4 | **High if E4 keeps a volume component** | Both compare weekly mileage | **Not yet**: E4 volume component is NEEDS_DECISION (E4-a). Phase-sequence component is separate. |
| E3 vs E4 | Low | Day/type structure vs phase labels | Yes |
| E5 vs E1–E4 | Moderate by design | 5d repeats constraint checks; 5a and 5b are structural and must be kept separate | Yes, once §5 separation is implemented |
| E6 vs E1–E5 | Low | E6 uses text and the stored injury; others use structure | Yes. E5c text emptiness can make E6 miss; the design accepts this and reports both |
| E7 vs E6 | By design | E7 is conditional on E6 hit | Yes |
| E8 vs E1–E7 | Derived, not duplicated | E8 measures agreement across generations, not the content | Yes, once E8-a is decided |

---

## 10. Research data flow

```
PROFILE (stored injury_limitations, stored numeric fields)
  ↓
DETERMINISTIC BASELINE  (generate_rule_based_plan; once per profile; deterministic)
  ↓
GEMINI GENERATION × 3   (generate_gemini_result, research path only; attempts 1..3)
  ↓
RAW GEMINI OUTPUT + STATUS  (GEMINI_SUCCESS | GEMINI_VALIDATION_FAILED | GEMINI_API_ERROR)
  ↓
E1–E7 PER GENERATION   (computed from raw_output; NA where raw_output is absent)
  ↓
E8 ACROSS GENERATIONS  (per profile; on successful generations)
  ↓
FINAL DATASET          (harness-level, outside the production database)
```

- `GEMINI_SUCCESS`: evaluated normally from `raw_output`. Its E1–E4 results are constant by construction (the validator already passed them), so the research value of these outputs is the E5 and E6/E7 content and the success rate.
- `GEMINI_VALIDATION_FAILED`: evaluated from `raw_output` where it exists, so the deviations are visible. It must never be counted as a successful Gemini output, and it must keep its status in every table.
- `GEMINI_API_ERROR`: tracked separately, with its error category. It is an attempt with no output.
- Production fallback outputs are not Gemini outputs for analysis. The research experiment must call `generate_gemini_result` directly, never `/plans/generate`.

---

## 11. Experimental unit

- **Experimental subject / input unit: the profile** (24 profiles, the deterministic baseline and the prompt input are defined by the profile).
- **Repeated observation: one Gemini generation** (3 per profile; 72 attempted generations in total).
- **Baseline: 24 deterministic plans**, one per profile, never repeated.
- The 72 generations are **not** 72 independent runner profiles. They are nested within 24 profiles, and analyses must respect that nesting (lock §10.2; `EVALUATION_CRITERIA_OPTION_A_DESIGN.md` §6).

---

## 12. Decisions (open items, by criterion)

- **E1-a.** Are paces and zones quoted in free text (for example `workout_execution`) evaluated? No extractor exists. Default if undecided: structured fields only.
- **E1-b.** Are rest days included in the E1 match rate? The validator compares them. Decide whether to report with and without rest days.
- **E1-c.** Partial-field handling: whether a generation with a single bad field gets a per-field result or NA for all of E1.
- **E2-a.** Exact-equality sensitivity analysis: in scope (lock §5.1 asks for it) or not. Non-blocking for the primary rule.
- **E4-a.** Keep a volume-trajectory component in E4 (with its own rule, tolerance, and an explicit statement of how it differs from E2), or restrict E4 to the phase-sequence check. The Option A algorithm uses relative deviation with an E2 tolerance reference (C5): this must be resolved, not assumed.
- **E5-a.** Separate output fields for 5a, 5b, 5c, 5d (recommended; see Prerequisites).
- **E5-b.** Capture `finishReason` so that truncation is reported separately.
- **E5-c.** Sub-field granularity for non-empty (all three `personalized_insights` fields? both `why_this_plan_was_generated` fields?).
- **E6-a.** Sentinel handling for the stored value (`none`, `no`, `n/a`, `-`). Current code treats these as no injury in two places and sends them literally in another (C4).
- **E6-b.** Freeze stop-word list and action-verb lexicon, versioned and documented.
- **E6-c.** Does verbatim copying of the stored injury phrase count as use?
- **E7-a.** Freeze the domain-generic running-term exclusion list, versioned and documented.
- **E7-b.** Contradiction codebook: in scope or out of scope for E6/E7.
- **E8-a.** Agreement/spread formula per outcome type (binary and continuous).
- **E8-b.** Minimum successful generations for E8 to be computed.
- **E8-c.** Rule for a generation that was never run.

---

## 13. Pre-experiment engineering checks

| # | Check | Status now | Action before experiment |
|---|---|---|---|
| 1 | 24-week prompt size and token feasibility | Not measured. Full schedule is sent in the prompt (all weeks, 7 workouts each). | Measure prompt size for 4- and 24-week profiles on the real provider. No estimate is given here. |
| 2 | Gemini output token feasibility | `generationConfig` sets no `maxOutputTokens` (C8) | Decide whether to set a limit (locked as open in lock §4.3), and capture `finishReason` |
| 3 | Parsing of full `weeks[]` | Tested with a 12-week fake response and 8-week multi-week payloads (`test_multi_week_gemini.py`). Not tested against a real provider. | Run the parse check on a small, non-study set of outputs |
| 4 | Research status handling | Implemented and tested: `generate_gemini_result` returns SUCCESS / VALIDATION_FAILED / API_ERROR with no fallback (`test_multi_week_gemini.py`) | None beyond E5 error-category separation |
| 5 | Raw output preservation | `raw_output` and `raw_text` are returned in memory. Nothing persists them. | Harness writes them to a file outside the production database, per attempt |
| 6 | Evaluator reproducibility | No evaluator exists | Evaluator must be deterministic given the raw files and the frozen lists |
| 7 | Deterministic baseline reproducibility | Verified in code: no `random`, no clock dependency in `rules/` (grep); output depends only on the profile. Stored once per profile. | Store each baseline JSON with a hash of the profile payload and the code commit |

Minimum code changes required (not implemented here; they change research traceability, not production behavior):
- Separate `error_category` values: `SCHEMA_INVALID`, `CONSTRAINT_VIOLATION`, `MALFORMED_JSON`, `TRUNCATED` (from `finishReason`), `API_CALL_FAILED`, `CONFIG_MISSING_KEY`. Current: `SCHEMA_OR_CONSTRAINT` covers two of these.
- Capture `finishReason` in the research result.
- Optionally, a non-fail-fast research check that returns every violation (C2), or the evaluator recomputes violations itself from `raw_output`.

---

## 14. Final decision table

| Criterion | Status | Blocking decision |
|---|---|---|
| E1 | NEEDS_DECISION | E1-a (free-text pace scope) and E1-c (partial-field handling). Exact structured rule is READY. |
| E2 | READY | None blocking. E2-a (sensitivity analysis) is non-blocking. |
| E3 | READY | None. Requires evaluating from `raw_output` (C2). |
| E4 | NEEDS_DECISION | E4-a: volume component and its relation to E2. Phase-sequence component is READY. |
| E5 | NEEDS_DECISION | E5-a (separate categories), E5-b (truncation), E5-c (non-empty granularity). Minimum code change in §13. |
| E6 | NEEDS_DECISION | E6-a (sentinels), E6-b (frozen lexicon), E6-c (verbatim copy). |
| E7 | NEEDS_DECISION | E7-a (frozen exclusion list); E7-b (contradiction codebook scope). |
| E8 | NEEDS_DECISION | E8-a (formula), E8-b (minimum n), E8-c (missing generations). |

No criterion is BLOCKED by missing code or missing methodology. Every NEEDS_DECISION item has a stated question and is decidable without changing the locked design.

### MUST DECIDE BEFORE CODING
1. E4-a: whether E4 keeps a volume-trajectory component, and if so its rule and tolerance (resolves the E2 overlap).
2. E5-a / E5-b / E5-c: separate categories, truncation capture, non-empty granularity.
3. E6-a / E6-b / E6-c: sentinel handling, frozen lexicon, verbatim-copy rule.
4. E7-a / E7-b: exclusion list, contradiction codebook scope.
5. E8-a / E8-b / E8-c: formula, minimum n, missing generations.
6. E1-a / E1-b / E1-c: free-text pace scope, rest-day inclusion, partial-field handling.
7. E2-a: whether the exact-equality sensitivity analysis is in scope (non-blocking).

### SAFE TO IMPLEMENT NOW
- E2 primary rule (per-week same-week comparison, 0.15 km and 0.05 km, as in the validator).
- E3 four sub-checks (day set, case-insensitive type, rest count, training count), evaluated from `raw_output`.
- E4 phase-sequence check (alignment and exact phase equality), since it does not depend on E4-a.
- E5 5a and 5b (schema and structure), once the error categories are separated.
- The research data flow, the status contract, and the harness-side raw-file capture.
- E1 structured exact-match rule, excluding free text and the rest-day question.

### DO NOT CHANGE (locked methodology)
- Profile count (24), generations per profile (3), total attempted generations (72), baseline count (24, one per profile, deterministic and not repeated).
- E1–E8 names and roles; the injury-only E6/E7 slot.
- E8 as a stability criterion over generations, not identity of outputs.
- Gemini as the only LLM in the study; research status categories; no deterministic fallback in the research path.
- Tolerances from the validator as the primary analysis rule (0.05 km per workout, 0.15 km per week); exact equality for pace and zone.
- No expert evaluation.
- No composite score, no ranking, no winner framing.

---

## 15. Corrections applied elsewhere

- `paper/EVALUATOR_SPECIFICATION_AUDIT.md` §6, the "E6 generic (hit without E7)" example, is corrected so that "Listen to your body and adjust training if needed" is an E6 miss, as in C6.

No commit. No code change. Stop here.

---

## Correction pass (later session, codebook v2)

The labels C1–C8 above are from the earlier specification review. The correction pass that follows uses DECISION 1–4 and the cleanup items; they are not renumbered here.

- **E6 and E7 are two logical stages.** E6 = 1 requires an explicit injury-related plan adaptation in one sentence: an injury reference term, an adaptation action term, and a plan-object term. E6 does not require a runner-specific anchor. E7 is conditional on E6 = 1 and checks for a non-generic token from the stored injury text. The example "Reduce intensity and listen to your body." is an E6 miss, so E7 = N/A. It is not E7 = 0.
- **E5 is N/A when no provider output exists** (API failure). `api_error` is no longer an E5 category. Failed attempts are recorded in `generation_failure` and are not evaluable repetitions for E8.
- **finishReason is preserved** for successful parses, validation failures, and malformed JSON. It is carried on the parsed object returned by `generate_gemini_plan` and in `GeminiGenerationResult.finish_reason`.
- **E1** trims structured values before exact comparison. **E3** normalizes `workout_type` with trim and case-fold. Free text is never normalized.
- The codebook is `v2` (`app/research/criteria_config.py`). Any change requires a new version.

---

## Final specification freeze (codebook v2)

The evaluator specification is now frozen and must not be changed based on future experimental outputs. Codebook version: `v2` (`backend/app/research/criteria_config.py`). No experiment data has been generated under any version.

- **E1**: applicable structured fields only. Rest days are excluded from the numerator and denominator. Values are trimmed, then compared exactly. A rest-only plan gives N/A.
- **E5**: schema-required fields only, plus structural and truncation checks. Explanatory text fields with schema defaults are not required.
- **E6**: an explicit injury-related plan adaptation, with an injury reference, an adaptation action, and a plan object in the same sentence. No runner-specific anchor required.
- **E7**: conditional on E6 = 1. Requires a body-part, condition, or trigger/activity anchor from the stored injury text (codebook `E7_ANCHOR_CODEBOOK_V2`). Generic running vocabulary is never an anchor.
- **E8**, **E2**, **E3**, **E4**, and finishReason handling are unchanged.
