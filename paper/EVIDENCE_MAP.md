# EVIDENCE_MAP

Repository state: branch `master`, HEAD `224d910` ("Phase 5: add multi-week training plans"); 8 commits in history (`732f4b3` baseline research prototype → Phases 1–5). Untracked: `Paper.docx` (an unrelated earlier sign-language paper by the same author; used only to learn the BINUS IEEE format, no content reused).

Verified runs (2026-10-01): `pytest` in `backend/` → **194 passed in 55.12 s** (Python 3.11, pytest 9.1.1); `npm run build` in `frontend/` → success, 1923 modules; `npm run lint` → warnings only (unused variables, setState-in-effect), not triaged.

## A. System claims

| Paper claim (section) | Source code | Test / run evidence | Literature |
|---|---|---|---|
| Hybrid pipeline: validate → rules → LLM → validate → fallback (III, IV) | `routes/plan_routes.py:generate_plan` (calls `generate_rule_based_plan`, then `get_personalized_ai_plan`) | `tests/test_api.py`, `tests/test_plan_lifecycle.py` | — |
| No ML training; LLM only via API (I, IV-A) | no ML libs in `requirements.txt`; `ai/llm_service.py` uses `httpx` | — | — |
| Profile variables and bounds (Table I) | `schemas.py:RunnerProfileCreate` | `tests/test_profile.py`, `tests/test_api.py` | — |
| Age, gender, 10K PB, easy pace not used in numbers (III-B) | `rules/generator.py` (only in `explainability`), `ai/prompts.py` (in prompt) | grep of generator.py | — |
| VDOT equations (1)–(3) | `rules/vdot.py:calculate_vdot_from_race` | `test_rule_engine.py::test_vdot_formula_matches_known_reference_value` (asserts 37–40) ; run: VDOT 38.43 for 24:56 | [27]; original 1979 source [PRE-2001 — approval] |
| Pace inversion and zone fractions 0.65/0.74/0.80/0.88/0.98/1.05 | `rules/vdot.py:velocity_from_vo2, calculate_training_paces` | run output for canonical profile | [27] — fractions need cross-check |
| Feasibility thresholds 3.5%/6.5% | `rules/generator.py:generate_rule_based_plan` | — | none; engineering design constraint |
| Progression ×1.06 (≥20 km) / ×1.08, cutback every 4th week ×0.85, taper 0.85×/0.55× base (Table II) | `rules/generator.py:generate_weekly_progression_summary` | `test_weekly_progression_never_exceeds_the_safe_increment` (checks only consecutive build weeks) + `test_t7_progression_fix.py` (new; checks the post-cutback build step and taper/race-week anchoring across 5 durations); run output for 8/12/16 weeks | [17], [18] (progression debated); [22], [23] (taper); [29] (periodization concept only). Cutback factor and taper magnitudes: no direct source (engineering design constraints) |
| Post-cutback rebound ≈ +25% vs. cutback week — **RESOLVED, fixed in code**; taper drop 37–55% (III-E) — **CONFIRMED CORRECT, unchanged** | same function (`current` IS NOW updated to the cutback week's own volume after a cutback, per the T7 fix; taper uses `base_mileage`, confirmed intentional) | `test_t7_progression_fix.py`; full suite 201/201 passing | — |
| Long run 30%, caps 12/16/21 km, floor 4 km; quality 20%, floor 3.5; easy floor 3 | `rules/generator.py:distribute_workouts_across_week` | `test_long_run_respects_the_thirty_percent_design_heuristic` (canonical profile only), `test_rule_engine_properties.py` (all durations and day counts; the realized 30% share and target tracking are documented xfail findings, 2026-10-14), run output (quality share 0.199) | [20], [21] report shares of sessions (context only); 30%/20% shares and caps are engineering design constraints |
| Day placement; 1-day edge case | same function | `test_training_day_distribution_across_all_valid_day_counts` (1–7), `test_single_training_day_preserves_injury_guidance` | — |
| Beginner → tempo, others → interval | same function | — | — |
| LLM input: profile, VDOT, zones, **Week 1 baseline** (III-F) | `ai/prompts.py:build_user_prompt` | — | — |
| Providers: Gemini (default `gemini-1.5-flash`), OpenAI (`gpt-4o-mini`), temperature 0.4, JSON mode | `ai/llm_service.py`, `config.py`, `.env.example` | dispatcher tests (mocked) | — |
| Fallback synthesizer is non-LLM template | `ai/llm_service.py:generate_offline_ai_plan` | `test_dispatcher_falls_back_*`, `test_offline_synthesizer_output_also_passes_validation` | — |
| Validator checks (Table III) | `ai/validator.py:validate_ai_plan`; tolerances 0.05 km / 0.15 km | `tests/test_llm_validation.py` (11 tests: distance, pace, mileage, count, malformed JSON, missing field) | [16] |
| No retry, no text-safety check, no storage of rejected output (Table III) | absence in `llm_service.py`/`validator.py` (failures only `logger.warning`) | code reading | — |
| LLM receives and returns every baseline week (per-week validation) | `ai/prompts.py` (`rule_based_baseline_plan`), `ai/schemas.py` (`AIPersonalizedPlan.weeks`), `ai/validator.py` (`_validate_week`) | `test_multi_week_gemini.py`, `test_llm_validation.py` (multi-week and per-week tamper cases) | Effectiveness of multi-week personalization not yet evaluated. The earlier "Week 1 only" entry described the pre-implementation state (`PHASE_5_DESIGN.md` §5 is a historical design note) |
| Supported durations 4–24 | `schemas.py` (`ge=4, le=24`); UI offers 4, 6, 8, 12, 16, 20, 24 (`PHASE_5_DESIGN.md` §2) | tests parametrize 4, 8, 12, 16, 24 (generation) and 4, 8, 24 (materialization) | — |
| Materialization 7 rows/week, unique (plan, week, day) | `workouts/service.py:materialize_training_plan_workouts`; `models.py:TrainingPlanWorkout` | `test_consumer_plan_materializes_exact_row_count` | — |
| Scheduled date from start date, week, weekday | `workouts/service.py:scheduled_date_for` | `test_scheduled_date_for_*` | — |
| Completion status derived, not stored | `workouts/service.py:derive_completion_status` | `test_workout_linking.py` (28) | — |
| One active plan per user | `workouts/service.py:archive_previous_active_plans` | `test_plan_lifecycle.py` | — |
| Dashboard current week; progress observations (thresholds fixed, ≤2 sentences, no LLM) | `routes/dashboard_routes.py`, `workouts/service.py:generate_observations` | `test_dashboard.py` (11), `test_progress.py` (28) | — |
| Argon2, hashed session tokens, HttpOnly SameSite=Lax cookie | `auth/security.py`, `auth/routes.py` (set_cookie) | `test_auth.py` | — |
| Origin/Referer CSRF check, non-wildcard CORS | `core/csrf.py`, `main.py` | `test_csrf.py` (4) | — |
| Rate limits (login, register, reset, plan generation, workout writes) | `core/rate_limit.py`, `config.py`, route decorators | `test_rate_limiting.py` (2) — covers login only plus config sourcing | — |
| Ownership: plan 404 for non-owner; link only to own planned workout | `routes/plan_routes.py`, `routes/workout_routes.py:_resolve_owned_training_plan_workout` | `test_authorization.py` (5), `test_workout_linking.py` | — |
| Password reset (hashed single-use 30-min token; no email provider) | `auth/routes.py`, `auth/email_service.py`, `config.py` | `test_password_reset.py` (7) | — |
| Evaluation: 4 single ratings 1–5 + comment + plan type; per-group mean/median/SD (SD only n≥2) | `schemas.py:PlanEvaluationCreate`, `routes/evaluation_routes.py` | `test_evaluation.py` (9) | [32], [33] |
| Evaluation endpoints unauthenticated, no participant ID | `routes/evaluation_routes.py` (no auth dependency) | code reading | — |
| Sliders prefilled 5/5/5/4 (and 3/4/5/4 for the second plan) | `frontend/src/pages/EvaluationPage.jsx` (state init and "Now Rate" handler) | code reading | — |
| Stack: FastAPI, SQLAlchemy/SQLite, Alembic (3 migrations), React 19, Vite, Tailwind | `requirements.txt`, `frontend/package.json`, `alembic/versions/0001–0003` | build/test runs | — |

## B. Facts about stored data (do not report as results)

| Observation | Evidence |
|---|---|
| `running_research.db` has 19 runner profiles/plans, 11 evaluations (5 rule-based, 6 AI), 9 users, 11 workout logs, 56 planned-workout rows | read-only SQLite query, 2026-10-01 |
| All 19 stored plans have `ai_model_used` = "AI Synthesis Engine (Rule-Constrained Academic Fallback)" → no live LLM output has ever been stored | same query |
| These rows come from development/testing (earlier memory note: leftover test runs) and are not participant data | [VERIFY with author] |

## C. Literature claims (updated after the reference audit; numbering follows the current manuscript)

Reference list changes: removed former [2], [13], [15]; replaced former [30] (Sullivan & Artino) by Norman 2010 ([32]); added Düking 2024 ([11]), Havers 2025 ([12]), He T. 2026 ([14]), Feely 2020 ([26]), Issurin 2010 ([29]); all others renumbered by order of first citation. Old-to-new mapping is in `REFERENCES_VERIFICATION.md`.

| Paper claim | Source / evidence |
|---|---|
| ChatGPT-generated six-week running plans were rated sub-optimal by coaching experts and better with more input information (II-C) | [11] abstract (Düking et al., J. Sports Sci. Med. 23(1):56–72, 2024) |
| Number/qualification of experts (ten) and ChatGPT version in [11] | Not used in the manuscript text (obtained only from a fetched page summary; verify in full text) |
| GPT-4 vs Gemini reproducibility and ratings (II-C) | [12] abstract |
| Systematic review: 24 studies, safety flaws in 14, LLM plans inferior in 5 of 6 head-to-head trials (I, II-C, V-E) | [14] abstract |
| Feely et al.: case-based marathon recommender with explanations, offline evaluation | [26] abstract |
| "Abstracts of [11], [12], [24] do not describe post-generation validation" (II-C) | Abstract-level only; full texts not read [VERIFY] |
| Parametric methods argued robust for Likert data (II-E, III-K) | [32] abstract (Norman, 2010) |
| LLM-as-a-judge biases (II-E) | Abstract of the arXiv version of [31]; NeurIPS record not opened |
| Periodization divides programs into smaller periods; limitations of the traditional model (II-D) | [29] abstract |

See `REFERENCES_VERIFICATION.md` for each reference's checks.



## D. Claims deliberately NOT made

No improvement in performance or injury risk; no medical/clinical validity; no supervised/deep/reinforcement learning; no LLM determination of physiological parameters; no questionnaire validation; no LLM model ranking; no participant counts or scores.
