> Status: PRE-EXPERIMENT RESEARCH READINESS AUDIT
> **ADDENDUM (implementation update, 4 October 2026).** Statements in this audit that the LLM receives or personalizes Week 1 only describe the implementation at the time of the audit. Current implementation: the LLM receives the full deterministic multi-week schedule (`rule_based_baseline_plan`), returns a `weeks[]` plan, and is validated week by week; the research path (`generate_gemini_result`) reports `GEMINI_SUCCESS`, `GEMINI_VALIDATION_FAILED`, or `GEMINI_API_ERROR` without fallback. Effectiveness of multi-week personalization has not been evaluated. The T7 status updates below remain accurate.
> **STATUS AS OF 2 OCTOBER 2026 (LATER SAME DAY): the "2 LLM" design below is `SUPERSEDED`.** New FINAL LOCKED design: 1 LLM only (Gemini) vs the deterministic baseline; 24 profiles CONFIRMED; 3 Gemini repetitions (72 generations) + 24 baseline plans (not repeated); exactly 8 automated criteria (definitions OPEN); multi-week scope CONFIRMED. See "Advisor Decision Update — 2 October 2026 (Gemini-only design)" at the end of this document and the STATUS SUMMARY that follows it.
> Methodology approval status: NOT YET APPROVED, except where marked APPROVED/CONFIRMED (see "Advisor Decision Update — 2 October 2026" at the end of this document, itself `SUPERSEDED` by the Gemini-only update): ~~2 LLMs; 3 repetitions per (runner profile × LLM)~~ — superseded by 1 LLM (Gemini); 3 Gemini repetitions per profile (72 generations); 24 baseline plans (not repeated). Expert evaluation excluded from the study entirely (unchanged).
> Data collection status: NOT STARTED
> RQ2 experiment status: NOT STARTED

**Scope of this file.** Audit only. No code, paper, or other research file was changed; no RQ2 experiment was run; no participant data were collected; no methodological decision was taken on behalf of the researcher or advisor. Items marked `[ADVISOR DECISION REQUIRED]`, `[TO BE DECIDED WITH ADVISOR]`, `[ADVISOR/METHOD REVIEW REQUIRED]`, `[CHECK BINUS REQUIREMENTS]` in `RESEARCH_METHODOLOGY_LOCK.md` are reported as open here.

**Evidence base (read for this audit):** `RESEARCH_METHODOLOGY_LOCK.md`, `PAPER_DRAFT.md` (and the regenerated `PAPER_IEEE.docx`, readable with python-docx), `EVIDENCE_MAP.md`, `PAPER_GAPS.md`, `QUESTIONNAIRE_TRACEABILITY.md`, `REFERENCES_VERIFICATION.md`, `CITATION_AUDIT.md`, the phase documents (`PHASE_*_DESIGN.md`, `PHASE_*_REPORT.md`, `PRODUCT_READINESS_AUDIT.md`, `README.md`), the backend source (`backend/app/**`), the frontend evaluation page, and the test suite.
**Checks executed during this audit:** `git rev-parse` → HEAD `224d910`, no modified tracked files; `pytest` (isolated temporary database) → **194 passed in 66.94 s** (19 deprecation warnings), re-run today; code search for versioning/experiment/seed/token-limit/usage handling in `backend/app`; reading of the test bodies relevant to each criterion. Reference numbers [n] follow the current manuscript.

Status vocabulary: READY / PARTIALLY READY / NOT READY / ADVISOR DECISION REQUIRED.

---

## 1. RQ1 readiness — the 14 technical-validation criteria (T1–T14)

"Oracle available" = the expected result is stated explicitly in the code/spec such that a test can be written without further decisions. "Test exists" = an automated test covering the criterion already exists in the suite. "Run" = executed in today's `pytest` run (194 passed).

| # | Criterion | Explicit oracle | Oracle available? | Automated test exists? | Run? | Evidence | Status |
|---|---|---|---|---|---|---|---|
| T1 | Input validation rejects out-of-range/malformed fields; valid accepted | Pydantic constraints in `schemas.py` (age 12–99, MM:SS pattern, race distance set, mileage 0<x≤200, days 1–7, duration 4–24) | Yes (constraints are explicit in code) | Partial: invalid 5K PB, invalid 10K PB, valid/missing 10K PB, `training_days_per_week=8` → 422 (`test_api.py`); invalid pace on profile endpoint (`test_profile.py`) | Yes | Not covered: age bounds, target time format, race-distance enum, duration 4/24 and out-of-range, mileage ≤0/>200, empty preferred days | PARTIALLY READY |
| T2 | VDOT equals an independent recomputation; deterministic | Independent implementation of Eqs. (1)–(3) or published VDOT table values | **No**: no independent implementation exists; source table for reference values is not chosen (book [27] not consulted) | Weak: `test_vdot_formula_matches_known_reference_value` asserts only 37 ≤ VDOT ≤ 40 for 24:56 | Yes | Observed value 38.43; determinism not explicitly tested (generator uses no randomness) | PARTIALLY READY |
| T3 | Pace zones = inversion of Eq. (1) at implemented fractions; ordered/monotonic | Formula and fractions are explicit in `vdot.py` | Partially: recomputation oracle possible; correctness of the fractions vs the published zones is unverified (literature check pending) | Minimal: asserts keys `easy`, `threshold`, `interval` exist | Yes | No value or ordering assertion | NOT READY |
| T4 | Number of weeks = requested duration for all durations 4–24 | Duration field | Yes | Partial: engine for 4, 8, 12, 16, 24 (`test_rule_engine_generates_all_weeks`) | Yes | 16 of 21 valid durations untested | PARTIALLY READY |
| T5 | 7 entries Mon–Sun every week; training-day count = requested | Day list; profile field | Yes | Partial: Mon–Sun and 7 entries for every week (but only for the 4-day profile); active/rest counts asserted for Week 1 across 1–7 days only | Yes | Not asserted for all weeks × all day counts | PARTIALLY READY |
| T6 | Every workout distance equals the documented formula (long run, quality, easy, caps, floors, progression, cutback, taper) | Formulas explicit in `generator.py` | Yes as *conformance to the implemented rules* | Partial: long run ≤30%+0.1 at one mid-volume case; build-week ≤10%; Week 1 within ±2 km of current mileage; week 4 < week 3. **Since this audit:** `test_t7_progression_fix.py` (new) adds cutback-exactness, post-cutback build-step, and taper/race-week anchoring assertions | Yes | No test yet for caps, floors, quality share | PARTIALLY READY |
| T7 | Known rule-engine properties are documented or fixed | Decision on fix vs document | **RESOLVED** — post-cutback rebound fixed in code; taper anchoring confirmed correct and left unchanged | `backend/tests/test_t7_progression_fix.py` (7 tests); full suite 201/201 passing | By test (`test_t7_progression_fix.py`), not ad hoc | `paper/CODE_AUDIT_EASY_RUN_PACE_AND_T7.md` (fix record); Section 7 below (historical finding, now resolved) | RESOLVED |
| T8 | Prompt contains profile, VDOT, zones, Week 1 baseline and numeric-preservation instruction | Prompt template in `ai/prompts.py` | Yes (template text) | **None** | — | No prompt snapshot test; no prompt version | NOT READY |
| T9 | Each validator violation class is rejected; valid plan passes | Validator rules and tolerances in `validator.py` | Yes | Partial: valid payload passes; offline synthesizer passes; distance, pace, weekly mileage, workout count, missing field rejected | Yes | Not covered: workout type, intensity zone, unknown day, duplicate day, rest-day count, training-day count; Mon–Sun reordering | PARTIALLY READY |
| T10 | Fallback returns a baseline-identical, schema-valid plan and records the fallback label on no key / API error / malformed JSON / validation failure | Dispatcher behavior in `llm_service.py` | Yes | Partial: no key, invalid plan (and key never logged), malformed JSON (all via the Gemini path with monkeypatched provider function) | Yes | Not covered: HTTP error/timeout path, OpenAI path, `auto` provider order, assertion that `ai_model_used` carries the fallback label | PARTIALLY READY |
| T11 | 7 × weeks scheduled rows; calendar dates correct | `materialize_training_plan_workouts`, `scheduled_date_for` | Yes | Yes for dates (start on Monday/mid-week/Sunday, all seven weekdays, multi-week offsets); rows for 4, 8, 24 weeks | Yes | Rows for other durations untested | PARTIALLY READY |
| T12 | Planned/actual integration: derived status, owner-only linking, soft delete, dashboard week logic | Phase 3/5 design documents | Yes | Yes: `test_workout_linking.py` (28), `test_dashboard.py` (11), `test_progress.py` (28), `test_multi_week_plans.py` week-tracking tests | Yes | Covers completed/missed/scheduled, rest days, cross-user link rejection, archived-plan links, deleted logs | READY |
| T13 | Authorization/security (non-owner 404, CSRF Origin, auth) | Phase 1 design | Yes | Yes: `test_authorization.py` (5), `test_csrf.py` (4), `test_auth.py` (13), `test_password_reset.py` (7) | Yes | Rate limiting has only 2 tests (login only plus config sourcing) — outside the T13 wording | READY |
| T14 | Whole suite passes on a *frozen* commit in a clean, recorded environment | A designated freeze commit and environment record | **No**: no freeze commit/tag exists; environment not recorded; `requirements.txt` uses `>=` pins | Suite exists (194 tests) | Yes: 194 passed at HEAD `224d910` (tracked tree unmodified; documentation files untracked) | Passing today ≠ frozen-state evidence | PARTIALLY READY |

**Separation (no tests were created at the time this audit was originally written):**
- *Tests that already exist:* T7 (fully, since this audit — see below), T12, T13 (fully), plus partial coverage for T1, T2, T3 (minimal), T4, T5, T6, T9, T10, T11.
- *Tests that still have to be written:* T1 boundary cases; T2 exact oracle; T3 value/ordering; T4/T5/T11 all-duration × all-day-count parametrization; T6 caps/floors/quality (cutback/taper/post-cutback progression now covered by `test_t7_progression_fix.py`); T8 prompt snapshot; T9 missing violation classes; T10 HTTP-error/OpenAI/`auto`/label assertions.
- *Needs a methodological decision:* T2 (which published values are authoritative; whether the zone fractions are accepted), T14 (which commit/tag is the freeze commit). **T6/T7's fix-or-document decision is RESOLVED** (rebound fixed; taper confirmed correct), so the T6 oracle is no longer awaiting that decision.

Counts for this table (14 criteria): READY 2 · PARTIALLY READY 9 · NOT READY 2 · ADVISOR DECISION REQUIRED 1.
---

## 2. RQ2 experiment readiness — what the repository can do today

The current pipeline lives in `backend/app/ai/llm_service.py::get_personalized_ai_plan` and is built for the web request, not for an experiment. Findings below come from reading that code and searching `backend/app` for versioning, experiment, seed, token-limit and usage handling (no matches except the FastAPI app version string).

| Requirement | Current implementation | Evidence | Status | Required action |
|---|---|---|---|---|
| Model/provider identification | Provider chosen by environment (`LLM_PROVIDER` = gemini/openai/auto) and the model name by `GEMINI_MODEL`/`OPENAI_MODEL` from a global settings object; the string `ai_model_used` ("Gemini (name)", "OpenAI (name)" or a fallback label) is stored per plan | `config.py`, `llm_service.py:215,227,237`, `models.py` | PARTIALLY READY | Provider/model must become an explicit per-run input; record the identifier requested |
| Exact model version | Only the configured alias is stored; nothing returned by the API (model field, system fingerprint) is captured | `generate_gemini_plan`, `generate_openai_plan` return only the parsed dict | NOT READY | Capture the returned model identifier; decide pinning policy [ADVISOR DECISION REQUIRED] |
| Prompt versioning | None. `SYSTEM_PROMPT` and `build_user_prompt` are source code only; no version tag, no hash stored | `ai/prompts.py`; grep for "version" finds only `app.version="1.1.0"` in `main.py` | NOT READY | Define a prompt version/hash scheme; freeze the prompt for the experiment |
| Deterministic runner-profile input | Profiles are validated Pydantic objects (`RunnerProfileCreate`); test factories can build them; there is no stimulus-profile file/format and no fixed stimulus set | `schemas.py`, `tests/factories.py` | PARTIALLY READY | Define the stimulus set and its storage format [ADVISOR DECISION REQUIRED on size/composition] |
| Deterministic baseline generation | `generate_rule_based_plan` is a pure function of the profile (no randomness, no clock use) | `rules/generator.py`, `rules/vdot.py` (no `random`/date use in the rules) | PARTIALLY READY | Record baseline version (commit + hash); decide the open rule-engine issues first (Section 7) |
| Identical input across models | Both providers receive the same `build_user_prompt(profile, rule_plan)` text, **but** the system prompt is delivered differently: Gemini concatenates `SYSTEM_PROMPT` and the user prompt into one user message; OpenAI sends a separate system message | `llm_service.py:149` vs `:179` | PARTIALLY READY | Decide whether this delivery difference is accepted as an unavoidable provider difference or must be aligned [ADVISOR DECISION REQUIRED] |
| Generation parameters | `temperature` = 0.4 hard-coded in both calls; JSON mode via different mechanisms (`responseMimeType` vs `response_format`); timeout 30 s; no retries; no top-p/top-k/seed | `llm_service.py:152-155,182-183,158,186` | PARTIALLY READY | Make parameters explicit per run and recorded; values beyond what exists are advisor decisions |
| Temperature | Fixed constant, same for both providers; not configurable per run | same | PARTIALLY READY | Make recordable/configurable; the value to use [ADVISOR DECISION REQUIRED] |
| Token/output limit | Not set (provider default) | no `max_tokens`/`maxOutputTokens` anywhere | ADVISOR DECISION REQUIRED | Decide whether to set one; truncation must be detectable |
| Raw output preservation | **Not preserved**: `raw_text` is a local variable, parsed and discarded; on JSON failure it is lost | `llm_service.py:162-163,190-191` | NOT READY | Preserve verbatim response body per run |
| Parsed output preservation | Only a *validated* plan is persisted (`ai_plan_json`, after `model_dump`, with workouts re-ordered); rejected parsed outputs are discarded | `llm_service.py:214-215`, `validator.py:106-107` | PARTIALLY READY | Preserve parsed output regardless of validator outcome |
| Validator verdict preservation | Only `logger.warning(...)` with the exception text; no stored verdict, no category field | `llm_service.py:216-217,228-229` | NOT READY | Store pass/fail, failure category, message, deviations |
| Exception/error preservation | Only the exception *type name* is logged for API errors; HTTP status/body, timeout, rate limit are not stored | `llm_service.py:220-221,232-233` | NOT READY | Preserve error type, HTTP status, body |
| Experiment ID / run ID | None. Only per-request UUIDs for `runner_profiles` and `training_plans` exist | `models.py` | NOT READY | Define experiment and run identifiers |
| Timestamp | `training_plans.created_at` (naive UTC) per web request; no per-call timestamp, no latency | `models.py` | PARTIALLY READY | Per-call UTC timestamps and latency |
| Token usage / cost | Not captured from provider responses | no `usage` handling | NOT READY | Capture if the protocol requires efficiency metrics |
| Reproducibility / ability to repeat the experiment | Baseline is deterministic; LLM calls are stochastic at 0.4 with no seed; no artifacts saved; nothing links a plan to a commit | see above | NOT READY | Requires the preservation items above plus a freeze procedure |
| Compare models without changing the baseline | The model is a global setting; a dispatcher with silent fallback hides failures; `auto` tries Gemini then OpenAI. The provider functions can be called directly with a prompt, but their model name is not a parameter | `llm_service.py:194-237`, `config.py` | PARTIALLY READY | Needs a separate run path with explicit model input and no silent fallback (not implemented here) |
| Fallback contamination control | The fallback label is stored at plan level; `ai_model_used` is not asserted in any test | grep of tests | PARTIALLY READY | Ensure fallback outputs are never counted as LLM outputs |
| API-key handling | Gemini key is sent in the URL query string; the tests assert the key is not logged | `llm_service.py:143`, `test_llm_validation.py` | PARTIALLY READY | Sanitize stored URLs/logs |
| Git commit recorded with results | Not recorded anywhere | — | NOT READY | Record at run time |

Counts for this table (21 requirements): READY 0 · PARTIALLY READY 11 · NOT READY 9 · ADVISOR DECISION REQUIRED 1.
---

## 3. RQ2 controlled-variable audit

### 3.1 Independent variable
- The language model used for personalization (provider + model identifier + version). Nothing else may differ between conditions.

### 3.2 Controlled variables (must be identical across models) and current repository status
| Variable | Must be | Current status in the repository |
|---|---|---|
| Runner profile | Same stimulus profile for every model | Controllable (Pydantic objects); no stimulus store |
| Deterministic baseline | Same baseline JSON per profile for every model | Deterministic function; not stored/hashed |
| Input schema | Same structure sent to every model (`runner_profile`, `physiological_parameters`, `rule_based_baseline_week`) | Same function `build_user_prompt` |
| User prompt/instructions | Same text | Same function |
| System instruction | Same text | Same constant, **delivered differently** by provider |
| Output schema | Same JSON schema description in prompt and same Pydantic model | Same |
| Temperature | Same value | Same constant (value is an open decision) |
| Token limit | Same | Not set; decision open |
| Other sampling settings (top-p/top-k/seed) | Same or provider defaults, recorded | Not set; not recorded |
| Number of repetitions | Gemini: same for every profile; baseline: not repeated | **CONFIRMED (2 October 2026, Gemini-only): 3 Gemini repetitions per profile (72 total); 24 baseline plans, not repeated** — supersedes the same-day 2-LLM resolution |
| Model version | Pinned and recorded | Alias only (Gemini) |
| Validator version/tolerances | Same code and tolerances (0.05 km, 0.15 km) | Fixed constants; no version tag |
| Rule-engine version | Same for all runs | Git commit only; no version field |
| Provider safety/content-filter settings | Same or recorded | Not set; provider defaults; not recorded |
| Time window | Same short window, interleaved order | Not defined |
| Retry/fallback policy | None, identical | Dispatcher falls back silently; no retries |
| Timeout | Same | 30 s constant |
| Language/locale of prompt | Same | English |

### 3.3 Dependent variables (to be measured)
Format validity (JSON/schema), first-attempt validator pass and failure category, deviation from baseline in distance/pace/mileage, structural consistency (now across the confirmed multi-week scope, not Week 1 only), text completeness, text-number mismatches, injury-related content, latency, token usage, error/timeout rates, between-repetition variability (Gemini's 3 repetitions per profile). Measured against the 8 locked automated criteria. **SUPERSEDED (2 October 2026): expert ratings per criterion, safety flags scored by experts, and inter-rater agreement are removed** — expert evaluation is excluded from the study; RQ2 relies solely on automated/objective criteria.

### 3.4 Potential confounders (not yet controlled or not controllable)
1. ~~Different system-prompt delivery (Gemini concatenation vs OpenAI system message).~~ **MOOT under the Gemini-only design** (no second provider); Gemini's own system-instruction delivery mechanism should still be documented and frozen.
2. JSON-enforcement mechanism (Gemini only now) and default safety filters.
3. Gemini's output length/verbosity could still vary across repetitions and across baseline vs Gemini text amount; no cross-model verbosity comparison applies now.
4. Stochastic sampling; no seed; **3 Gemini repetitions per profile CONFIRMED** (72 total).
5. Provider alias drift between calls/dates; model retirement (the default `gemini-1.5-flash` may not remain available [VERIFY]).
6. Time-of-day/rate-limit effects; call order.
7. Silent fallback and `auto` mode masking failures.
8. The validator is both a quality gate and an outcome measure (circularity for consistency metrics).
9. Researcher authored the prompt, the baseline, the validator and the rubric (researcher bias).
10. ~~The LLM sees only Week 1, so outcomes generalize only to Week 1 personalization.~~ **RESOLVED/SUPERSEDED**: multi-week scope is now CONFIRMED; Gemini receives sufficient multi-week context.
11. Free-text injury notes in the profile may behave differently across models.
12. Rule-engine decisions (Section 7) change baselines if taken after data are generated.
13. ~~Expert rating confounds: rater familiarity with model styles, non-blindable formatting, rater fatigue/order.~~ `SUPERSEDED` — expert evaluation removed from the study (2 October 2026); no raters.
No values for any of these are chosen here, except the APPROVED/CONFIRMED items noted in the Advisor Decision Update at the end of this document.

---

## 4. RQ2 rubric audit

Source: `RESEARCH_METHODOLOGY_LOCK.md` §5. "Overlap" = overlap with the production validator.

| # | Criterion | Definition (as proposed) | Measurement | Auto / expert | Overlaps validator? | Quality or compliance? | Issues flagged |
|---|---|---|---|---|---|---|---|
| 1 | Runner-profile consistency | No contradiction with profile facts; injury addressed | (a) structural identity; (b) fact-mention checklist; (c) injury content present | Mixed | (a) yes | (a) compliance; (b) compliance/accuracy; (c) presence only | Three different constructs in one criterion; "contradiction" has no operational extraction method; presence of injury text ≠ appropriate advice; should be split before scoring |
| 2 | Pace consistency | Paces equal baseline; text paces match zones | Exact string match; number extraction | Auto | Yes (pace/zone strings) | Compliance | Text-number extraction rules (formats, units, tolerance) undefined; no meaning for quality |
| 3 | Weekly-volume consistency | Distances/mileage equal baseline within tolerance | Validator + extraction | Auto | Yes (distance ±0.05, mileage ±0.15) | Compliance | Tolerances are the validator's own; sensitivity analysis proposed but undecided; validator does not check that distances sum to the weekly mileage |
| 4 | Workout-distribution consistency | Same day set/types/rest-day count | Validator sub-checks | Auto | Yes | Compliance | Duplicates criterion 1(a) |
| 5 | Progression consistency | Text consistent with baseline progression | Rule-based check (`SUPERSEDED`: expert check removed) | Auto only | No | Would be quality | **Now measurable**: multi-week scope is CONFIRMED (supersedes the earlier Week-1-only limitation and the OPEN METHODOLOGICAL DECISION on multi-week LLM context, now resolved); the validator must be extended to examine progression across the confirmed multi-week context |
| 6 | Output completeness | Required text fields present and non-empty | Field check | Auto | Partial (schema validity; but `AIPersonalizedPlan` text fields default to `""`, so an empty-text plan **passes** the validator) | Compliance | Requirements for rest days unspecified; "non-empty" ≠ informative |
| 7 | Personalization (automated proxy) | Specific, profile-relevant text, assessed by automated/rule-based checks only | Rule-based extraction | Auto only (`SUPERSEDED`: blinded expert rubric removed from the study, 2 October 2026) | No | Compliance/proxy, not perceived quality | Automated criteria cannot assess "specific, useful, safe" text the way an expert rubric would; this is a known, accepted limitation of excluding expert evaluation |
| 8 | Reliability/efficiency | Errors, latency, tokens, repetition variability | Run logs | Auto | No | Operational, not quality | Latency/tokens are not captured today |

Cross-cutting findings:
- **Criteria 2, 3, 4 (and part of 1 and 6) measure compliance with the instructions the validator already enforces.** They answer "did the model obey the numerical-preservation instruction", not "is the plan good". Reporting them as three independent criteria overstates independent evidence; they are one family.
- **First-attempt validator pass rate** is a single binary outcome that hides which criterion failed; failure categories must accompany it.
- **Criterion 7 (and parts of 1 and 5) no longer relies on expert judgment** — expert evaluation has been removed from the study (2 October 2026); only automated/rule-based proxies remain, with the accepted limitation that this cannot fully capture perceived quality.
- **Composite score:** none is defined (the lock recommends unweighted reporting). **No weights exist**, so there is no unsupported weight in the current text; any composite remains `[WEIGHTS REQUIRE LITERATURE/EXPERT JUSTIFICATION]` and `[ADVISOR DECISION REQUIRED]`.
- **Criteria count is now LOCKED at exactly 8** under the Gemini-only design (2 October 2026). **OPEN SUB-DECISION, flagged not resolved:** this audit's 8-row rubric table above, the methodology lock's own 8-criterion list, the (superseded) comparative proposal's 16-item draft, and the paper's Table IV 5-criterion list are not identical in wording/grouping and must be reconciled before the rubric is finalized.
- **Literature support** is design inspiration only ([10]–[13], [15], [30]); the 22 criteria of [11] have not been read in full.
- **LLM-as-judge** is not part of the current design (no expert baseline exists to validate it against, since expert evaluation was removed).

---

## 5. RQ3 user-study readiness — open decisions and questions

| Topic | Current state | Open decision / required answer | Owner |
|---|---|---|---|
| Study design | Three options described (within-subject counterbalanced, between-subject, single-arm descriptive); none chosen | Which design? What constitutes the compared conditions (rule-based vs one AI plan)? | Advisor |
| Plan content shown | Rule-based baseline has little warm-up/execution text; AI plan adds text by design (confound) | Week 1 only or full plan? Include a template-text control? | Advisor |
| Which "AI" plan | Dispatcher may silently fall back to templated text; all 19 stored dev plans used fallback | Which LLM/prompt version is used in RQ3? How are fallback plans excluded? | Advisor |
| Profile source | Participant's own profile vs vignette | Which? (own profile is needed for personalization perception but increases privacy burden) | Advisor |
| Inclusion/exclusion | Not defined; app accepts ages 12–99 | Criteria; exclusion of medical conditions | Advisor / BINUS |
| Adult-only requirement | Not enforced in the application (minimum age 12) | Adults only? If minors, special approval | BINUS |
| Sample size | Not defined; approaches listed only | Approach and number | Advisor / method reviewer |
| Recruitment | Not defined | Channels, incentives, voluntariness | Advisor / BINUS |
| Consent | **No consent flow in the application** | Consent text, version, storage | BINUS / Researcher |
| Health/injury information | Free-text injury field is stored and sent to the LLM | Collect at all? Coarse category instead of free text? Redaction? | Advisor / BINUS |
| External LLM data transmission | Profiles (including injury text) are sent to Google/OpenAI endpoints | Is transmission of participant data permitted? Disclosure wording? Vignettes instead? | BINUS / Advisor |
| Questionnaire administration | App collects 4 single ratings with pre-filled defaults (5/5/5/4), visible plan labels, no participant ID, endpoints unauthenticated | 16-item form, neutral defaults, blinding, participant code, access control | Researcher after design decisions |
| Content validation | Not started | Expert panel size and composition; method | Advisor |
| Pilot testing | Not started | Pilot sample size; criteria for revising items | Advisor / method reviewer |
| Data storage | SQLite development database containing test rows; no separate study store; no retention policy | Storage location, access control, retention | BINUS / Researcher |
| Anonymization | Planned: anonymous code, separate consent log; not implemented | Linkage policy; de-identification of free text | BINUS / Researcher |
| Withdrawal | Not implemented | Procedure and its data consequences | BINUS |
| Ethics/BINUS requirements | Not checked | Whether review/exemption applies; documents required | BINUS |

### Questions that must be answered by the advisor/institution
1. Is ethics committee review required, and by whom (`[CHECK BINUS REQUIREMENTS]`)?
2. Which RQ3 design and which plan conditions are used?
3. Which participants are eligible; are minors excluded?
4. How is the sample size to be justified, and what is the pilot sample?
5. May participant profiles (including injury text) be sent to external LLM providers?
6. What information sheet/consent/withdrawal procedure is required?
7. Where may the data be stored, and for how long?
8. Who is on the questionnaire content-validity panel?

---

## 6. Questionnaire audit — 16 proposed items

Source of wording: `QUESTIONNAIRE_TRACEABILITY.md` §3 (a **proposal**, not in the repository, wording unchanged here). **No item may be called a validated questionnaire item until the validation process in the methodology (literature review → item review → expert/content review → pilot → revision → final version) is completed. None of the steps has been started; all 16 items are study-specific.**

Planned response scale (all items): 5-point agreement (1 strongly disagree … 5 strongly agree). Fit: declarative statements → agreement scale is appropriate for all 16. *Implementation mismatch:* the current app uses non-agreement anchors (e.g., "1 - Very Generic … 5 - Highly Personalized"); no "not applicable" option exists.

| Item | Construct | Wording (unchanged) | Single-barrelled? | Leading? | Scale fit | Redundancy | Measures its construct? | Content-validation status |
|---|---|---|---|---|---|---|---|---|
| PP1 | PP | This plan takes my personal running profile (for example my current fitness and goal) into account. | Mostly; two examples in parentheses | Mildly (asserts the plan "takes into account") | Fits | Overlaps PP4 | Yes (core meaning) | Not started |
| PP2 | PP | This plan fits the number of days I can train each week. | Yes | No | Fits | Distinct | Questionable: closer to schedule feasibility than personalization | Not started |
| PP3 | PP | This plan takes my reported injuries or physical limitations into account. | Yes | Mildly | Needs "not applicable" for respondents without injury | Distinct | Yes, but depends on injury report; rule-based plan changes text only | Not started |
| PP4 | PP | This plan feels written for me rather than for runners in general. | Contrastive (two-part comparison) | Mildly leading | Fits | Overlaps PP1 | Yes (holistic) | Not started |
| PU1 | PU | This plan would help me prepare for my target race. | Yes | No | Fits | Overlaps PU4 | Yes | Not started |
| PU2 | PU | The weekly schedule is practical to follow in my daily routine. | Yes | No | Fits | Distinct | Questionable: practicality/feasibility vs usefulness | Not started |
| PU3 | PU | Following this plan would help me organize my running training. | Yes | No | Fits | Overlaps PU1/PU4 | Yes | Not started |
| PU4 | PU | I find this plan useful. | Yes | No | Fits | Overlaps PU1, PU3 | Yes (global) | Not started |
| PC1 | PC | The workout descriptions in this plan are easy to understand. | Yes | No | Fits | Distinct | Yes; but the rule-based plan contains less descriptive text by design, so conditions are not equivalent | Not started |
| PC2 | PC | The pace targets in this plan are clearly stated. | Yes | No | Fits | Distinct | Yes (numeric clarity; same data in both plans) | Not started |
| PC3 | PC | I understand why each type of workout is included in this plan. | "each type" is a universal quantifier | No | Fits | Distinct | Partly: understanding of rationale (explanation) rather than clarity of text | Not started |
| PC4 | PC | The warm-up and recovery instructions in this plan are clear. | **No** (warm-up and recovery) | No | Fits | Overlaps PC1 | Yes, but the baseline has no warm-up field | Not started |
| RC1 | RC | I am confident that I could follow this plan. | Yes | No | Fits | Overlaps RC3 | Partly: self-efficacy for adherence rather than confidence in the recommendation | Not started |
| RC2 | RC | I trust the training load in this plan to be appropriate for me. | Yes ("trust" and "appropriate") | Mildly | Fits | Distinct | Yes (trust), but respondents may lack expertise to judge load | Not started |
| RC3 | RC | I would feel comfortable using this plan to guide my training. | Yes | No | Fits | Overlaps RC1 | Partly: "comfortable" is ambiguous | Not started |
| RC4 | RC | I am confident that the pace targets match my current ability. | Yes | No | Fits | Distinct (numeric); related to PC2 | Yes | Not started |

Summary of flags (no wording changed): one clearly double-barrelled item (PC4); contrastive/universal-quantifier wording (PP4, PC3); mild leading wording (PP1, PP3, PP4, RC2); redundancy pairs (PP1/PP4; PU1/PU3/PU4; PC1/PC4; RC1/RC3); construct-fit doubts (PP2, PU2, PC3, RC1, RC3); an applicability gap (PP3 for respondents without injuries); a condition-equivalence problem (PC1, PC4); the implemented scale anchors differ from the planned agreement scale. Constructs PC and RC have only a weak, unconfirmed conceptual link to prior frameworks [3]; PP has none verified; PU has a general link to usefulness as a quality in [3].

---

## 7. Baseline-freeze audit (rule-engine issues — not fixed)

Both issues are in `generate_weekly_progression_summary` (`backend/app/rules/generator.py`), reproduced earlier by running the generator (canonical profile; 8, 12 and 16 weeks).

### 7.1 Post-cutback rebound (~+25%) — RESOLVED, fixed in code
- **Prior behavior (historical record — no longer current):** the running volume `current` was updated only in build weeks. A cutback week was computed as `current × 0.85` without updating `current`, so the next build week was `current × (1.06 or 1.08)` and was ≈ +24.9% above the cutback week (≈ +6% above the last build week). Canonical examples (pre-fix): week 4 = 25.3 km → week 5 = 31.6 km.
- **Current behavior (post-fix):** the cutback branch now sets `current = vol` (the cutback week's own reduced volume) before returning, so the next build week is a normal `current × (1.06 or 1.08)` step off the actual post-cutback mileage. Canonical examples (post-fix): week 4 = 25.3 km → week 5 = 26.8 km (≈ +6%, matching the "capped at ≤8–10%" claim relative to the immediately preceding week, including across a cutback). Verified by `backend/tests/test_t7_progression_fix.py` (7 tests) and a full-suite regression run (201/201 passing).
- **Why it mattered for the baseline:** it determined the weekly volume (and hence all workout distances) of every build week that followed a cutback, i.e., weeks ≥ 5 in plans of at least 8 weeks.
- **Did it affect RQ2?** At the time of this audit the LLM received Week 1 only, so the rebound did not reach the LLM. The LLM now receives and returns every baseline week (see the addendum at the top of this document), so the post-cutback step is part of the LLM's input.
- **Did it affect RQ1/RQ3?** Yes: the T6/T7 oracles (what counts as "conformant") and any user study showing the whole plan — now resolved for both.
- **Effect of the fix on existing plans:** no baseline plans for the 24-profile experiment have been generated yet (per the study's gating), so there is nothing stored to invalidate. Any future baseline generation will use the fixed rule engine.
- **Freeze status:** the fix-or-document decision has been made and implemented (fixed). The baseline should still be frozen (commit tagged) before any RQ2 generation or RQ3 data collection, per Section 13 — that freeze step itself has not yet happened.
- **Decisions previously required, now resolved:** fix was chosen over document, consistent with there being no literature source to anchor an alternative progression semantics to (`PAPER_GAPS.md` §5b); the advisor approved the fix before implementation. See `paper/CODE_AUDIT_EASY_RUN_PACE_AND_T7.md` for the audit trail.

### 7.2 Taper anchored to starting mileage — CONFIRMED CORRECT, not a defect
- **Behavior (unchanged by the T7 fix):** the second-to-last week is `base_mileage × 0.85` and the last week `base_mileage × 0.55`, independent of the peak. Canonical examples: 8 weeks: 33.5 → 21.2 → 13.8 km; 12 weeks: 39.8 → 21.2 → 13.8; 16 weeks: 47.5 → 21.2 → 13.8 (drops of 37–55% into the first taper week). The code comment previously said "~75% of peak", which did not match the code; **the comment has been corrected, the formula was not changed.**
- **Why this is intentional, not a bug:** `PAPER_DRAFT.md` Table II documents the taper as "times the base (starting) mileage," not the peak — the implementation already matched the documented, citation-reviewed methodology. The code comment was the only thing wrong.
- **Why it can affect the baseline:** taper volumes are identical for any plan length with the same starting mileage, so the taper's relative size depends on how far the build phase climbed — this is a known, accepted property of the base-anchored design, not an error to correct.
- **Did it affect RQ2?** At the time of this audit, not directly (the LLM saw Week 1 only). The LLM now receives the full schedule, including the final two taper weeks.
- **Did it affect RQ1/RQ3?** The formula itself needed no correction; T6/T7 oracles can now reference it as a settled rule.
- **Resolution:** DOCUMENT AS-IS. No code change was needed to the formula; only the inline comment was corrected.
- **Freeze recommendation:** same as 7.1.
- **Decisions still required (advisor):** fix or document; anchor choice; justification source (none identified).

### 7.3 Additional observations relevant to the freeze (reported, no decision taken)
- Week 1 volume is `current × 1.06/1.08`, whereas the explainability text states that Week 1 "matches current capacity"; the test tolerates ±2 km.
- Minimum floors (4/3.5/3 km) are applied after percentages, so realized weekly distance can differ slightly from the target.
- Age, gender, 10K PB and easy-run pace do not influence any number.
- Documentation (`README.md`) describes the progression/80-20 rules in terms the manuscript now qualifies as engineering design constraints.

---

## 8. Research data model audit (conceptual only)

No migration, schema or code is proposed. Existing development tables (`runner_profiles`, `training_plans`, `plan_evaluations`) lack participant IDs, raw LLM output, rater data and consent links and contain development test rows (19 plans, 11 evaluations, all plans from the fallback); they must not be mixed with study data.

| Research question | What must be stored (conceptual) |
|---|---|
| **RQ1** technical validation | Freeze commit hash and tag; environment record (Python version, installed package versions); criteria list T1–T14 with version of each oracle; test identifiers and outcomes with run timestamp; warnings; fixture profiles and the baseline hash each oracle uses; list of known limitations and open decisions at the time of the run |
| **RQ2** LLM comparison | Protocol version; experiment ID and time window; stimulus profiles and their rationale; baseline snapshot (JSON + hash) per profile; prompt version/hash (system and user, as rendered); model registry (provider, requested identifier, returned identifier, access date) for **2 LLMs**; generation parameters; per-run record (run ID, profile, LLM, repetition [**3 per cell, APPROVED/CONFIRMED**], call start time, latency, HTTP status, error type, raw body, parsed JSON, token usage, truncation flag); validator verdict (pass/fail, category, message, deviations); automatic metrics; analysis script version. **SUPERSEDED: blinded expert materials, the blinding key, rater registry, rubric version, ratings, comments, presentation order and agreement statistics are removed — expert evaluation is excluded from this study.** |
| **RQ3** participant evaluation | Participant code; eligibility screening result; consent record and version (separate store); coarse demographics if needed; profile inputs (minimal; free-text injury treated as sensitive); plan exposure record (plan ID, true condition, blinded label, order, model and prompt version, fallback flag); questionnaire version; item responses; optional comments; withdrawal flag/date; session metadata; instrument-validation records (item review notes, expert-panel ratings, pilot data) kept separate from main-study data |

Privacy principles carried over from the lock: no name/email in research tables; consent log separate; free-text injury optional or coarsened; raw LLM outputs derived from participant text are sensitive.

---

## 9. Reproducibility audit

| Component | Can the repository record it today? | Evidence | Missing |
|---|---|---|---|
| Git commit/hash | No (not stored with any plan or result) | grep of `backend/app`; models | Record at run time; clean-tree requirement; freeze tag |
| Rule-engine version | No explicit version (only the commit; `app.version="1.1.0"` is the API version) | `main.py` | Version identifier tied to the baseline |
| Prompt version | No | `prompts.py` | Version tag/hash of rendered prompts |
| Model/version | Partially (configured alias in `ai_model_used`); no returned version | `llm_service.py` | Requested and returned identifiers |
| Generation parameters | Hard-coded constants in code; not stored with results | `llm_service.py` | Persist per run |
| Profile input | Yes for web-generated plans (`runner_profiles` row) | `plan_routes.py` | Dedicated stimulus store; separation from dev data |
| Baseline output | Yes (`rule_based_plan_json`) | `models.py` | Hash/version |
| LLM output | Only the validated plan or the fallback (`ai_plan_json`); raw and rejected outputs are lost | `llm_service.py` | Raw and parsed outputs for all runs |
| Validator result | No (log lines only) | `llm_service.py` | Persisted verdicts |
| Evaluation result | Partially (`plan_evaluations`: four scores, comment, plan type; no participant ID, no instrument version, no model/prompt version) | `models.py` | Study-grade response store |
| Experiment metadata | No | — | Experiment/run IDs, protocol version, time window |
| Environment/dependencies | No lock file; `requirements.txt` uses `>=` ranges; Python version not pinned; tests ran on Python 3.11, pytest 9.1.1 | `requirements.txt` | Pinned or recorded versions |
| Randomness | Rule engine has none; LLM sampling has no seed | code | Document sampling nondeterminism; seed only if offered by the provider [VERIFY] |
| Analysis scripts | None exist | — | Versioned analysis code reading raw data |

Conclusion: the deterministic part (rules, schedule, planned/actual logic) is reproducible from the commit; **the LLM experiment is not reproducible with the current repository**, because nothing needed to re-run or audit it is recorded.

---

## 10. Paper alignment audit (no rewrite performed)

| Check | Finding | Aligned? |
|---|---|---|
| RQ1 wording | Identical in paper (I) and lock (§2) | Yes |
| RQ2 wording | Identical; marked `[EXPERIMENT REQUIRED FOR RQ2]` in paper | Yes |
| RQ3 wording | Identical; marked `[DATA REQUIRED]` in paper | Yes |
| Terminology | "personalization layer", "deterministic baseline", "server-side validation" used consistently | Yes |
| Evaluation criteria | Paper Table IV lists five criteria (format validity, constraint consistency, structural consistency, personalization quality, efficiency); the lock defines eight (runner-profile, pace, weekly-volume, workout-distribution, progression, completeness, personalization quality, reliability/efficiency) with different names and granularity | **No — reconcile after the advisor approves the rubric** |
| Control conditions | The lock proposes optional baseline-only and template-fallback controls; the paper does not mention them | Not aligned (paper pending decisions) |
| Questionnaire constructs | PP, PU, PC, RC and four items each in both; Table V includes the conceptual-basis column consistent with the traceability file | Yes |
| Questionnaire described as validated? | Paper says the items are "contextualized for this study and are not an established validated questionnaire" and require pilot testing | Yes (no such claim) |
| Technical-validation status | Paper (III-A) says the artifact "and its technical validation are complete in the repository"; the lock and this audit show 12 of 14 criteria not fully ready | **No — overstated relative to the lock** |
| Claims of unavailable results | None; results sections carry placeholders; the 194-test result is real and was reproduced today | Yes |
| Final model choice | Paper mentions the default models only as supported providers whose availability must be verified; no model is declared as the choice | Yes |
| Novelty claim | Paper states that no novelty is claimed beyond the cited literature; the gap statement acknowledges Düking et al. [11] | Yes (search protocol still pending) |
| Performance claims | None; paper states effectiveness is not assumed and cites the systematic review [14] | Yes |
| Methodological decisions presented as settled | Paper lists profile set, models, repetitions, rubric and weights as undefined; consistent with the lock | Yes |
| Prompt delivery difference between providers | Not mentioned in the paper | Gap (to be documented once decided) |
| Word manuscript = Markdown | Regenerated from the Markdown; text matches apart from math rendering | Yes |

---

## 11. Final research readiness matrix

| Area | Status | Blocking? | Why | Next action | Decision owner |
|---|---|---|---|---|---|
| Research objective and RQ text | 🔵 ADVISOR DECISION REQUIRED | Yes | Wording is consistent across documents, but nothing is approved | Advisor review of objective and scope (Week-1-only LLM scope) | Advisor |
| RQ1 test suite (194 tests) | 🟡 PARTIALLY READY | No (for starting RQ2/RQ3); Yes for claiming RQ1 complete | Suite passes; 12 of 14 criteria not fully ready (9 partially, 2 not ready, 1 awaiting a decision) | Close the listed test gaps (Section 1) | Researcher |
| RQ1 VDOT/zone oracle (T2, T3) | 🔴 NOT READY | No | No independent oracle; zone fractions unverified against the source | Select authoritative reference values; verify fractions with [27] | Researcher / Advisor |
| Rule-engine freeze (T7) | 🔵 ADVISOR DECISION REQUIRED | Yes | Two known behaviors undecided; baseline cannot be frozen | Decide fix vs document | Advisor |
| Freeze commit/environment (T14) | 🟡 PARTIALLY READY | Yes | Suite passes today; no freeze tag or environment record | Define freeze point after decisions | Researcher |
| RQ2 experiment harness | 🔴 NOT READY | Yes | Raw output, verdicts, errors, IDs, timestamps not preserved; model not a parameter | Build after protocol approval (not now) | Researcher |
| RQ2 number of models | 🟢 RESOLVED (2 October 2026, Gemini-only; supersedes same-day 2-LLM resolution) | No | **CONFIRMED: 1 LLM (Gemini)** | Exact version still to choose | Advisor |
| RQ2 model identity and version | 🔵 ADVISOR DECISION REQUIRED | Yes | Not chosen; default is a placeholder; availability unverified | Choose Gemini version and pinning policy | Advisor |
| Prompt versioning and freeze | 🔴 NOT READY | Yes | No version/hash; prompt not frozen | Define scheme and freeze after approval | Researcher / Advisor |
| Prompt delivery parity | 🔵 ADVISOR DECISION REQUIRED | Yes | Gemini concatenates system prompt, OpenAI uses a system message | Accept or align | Advisor |
| Generation parameters (tokens, seed, temperature value) | 🔵 ADVISOR DECISION REQUIRED | Yes | Token limit/seed undecided; temperature fixed constant | Decide values and recording | Advisor |
| Stimulus profiles (count) | 🟢 RESOLVED (2 October 2026, Gemini-only) | No | **CONFIRMED: 24 profiles**; demographic composition detail still an open sub-decision | Finalize composition | Advisor |
| Repetitions per profile (Gemini) / baseline count | 🟢 RESOLVED (2 October 2026, Gemini-only) | No | **CONFIRMED: 3 Gemini repetitions per profile (72 total); 24 baseline plans, not repeated** | — | Advisor |
| RQ2 rubric | 🟡 PARTIALLY READY | Yes | Criteria count now LOCKED at exactly 8; progression now measurable under confirmed multi-week scope; exact definitions not reconciled across documents (flagged conflict) | Resolve reconciliation in Section 4 | Advisor |
| Expert evaluation design | 🟢 RESOLVED (2 October 2026) | No | **Excluded entirely from the study** — no coach/expert rating, rubric, inter-rater agreement, recruitment, or blinding | — | Advisor |
| RQ3 study design and plan exposure | 🔵 ADVISOR DECISION REQUIRED | Yes | Three options, none chosen; confounds identified | Decide | Advisor |
| Participants, recruitment, sample size | 🔵 ADVISOR DECISION REQUIRED | Yes | Not defined | Decide with method review | Advisor |
| Ethics and consent | 🔵 ADVISOR DECISION REQUIRED | Yes | Requirement unknown; no consent flow in the application | Ask BINUS; prepare documents after answer | BINUS/Institution |
| External LLM data transmission | 🔵 ADVISOR DECISION REQUIRED | Yes (for participant data) | Profiles incl. injury text go to third-party APIs | Decide permission/redaction/vignettes | BINUS/Institution |
| Evaluation application readiness | 🔴 NOT READY | Yes | 4 single ratings, pre-filled defaults, visible labels, no participant ID, no consent screen, unauthenticated endpoints | Implement after design decisions | Researcher |
| Questionnaire items and validation | 🔴 NOT READY | Yes | 16 study-specific proposals; 0 validation steps done; wording issues flagged | Run validation process | Researcher / Advisor |
| Research data model and storage | 🔴 NOT READY | Yes | No study-grade storage exists | Finalize conceptual model, then implement | Researcher |
| Reproducibility recording | 🔴 NOT READY | Yes | Commit, prompt, model version, parameters, raw output, verdicts not recorded | Implement per protocol | Researcher |
| Dependency/environment record | 🟡 PARTIALLY READY | No | Unpinned requirements; can be recorded at run time | Record environment | Researcher |
| Statistical analysis plan | 🔵 ADVISOR DECISION REQUIRED | Yes | Descriptive proposed; inference/multiplicity undecided | Decide | Advisor |
| Paper alignment | 🟡 PARTIALLY READY | No | Two inconsistencies (rubric naming; "technical validation complete") | Reconcile after approval | Researcher |
| Paper honesty (results, validation, novelty, performance) | 🟢 READY | No | No unsupported claims found | Keep placeholders | Researcher |
| Literature checks (search protocol, Scholar, full texts) | 🟡 PARTIALLY READY | No | Pending items listed in `PAPER_GAPS.md` | Complete manually | Researcher |

---

## 12. CAN DO NOW vs MUST WAIT

These lists describe what is safe in the future; none of it was done in this audit.

### CAN DO NOW (does not pre-empt any advisor decision)
1. Run and report the existing test suite on the working tree (done today: 194 passed).
2. Record the environment (Python version, installed package versions) and the current commit.
3. Write the missing technical-validation tests that only check implemented behavior (T1 boundaries, T3 values/ordering, T4/T5/T11 all durations, T8 prompt snapshot, T9 missing violation classes, T10 error/OpenAI/`auto` paths) — implementation not requested in this task.
4. Consult the published VDOT source ([27]) to establish an authoritative oracle for T2/T3.
5. Read in full [11], [12], [24] (post-generation validation; rater details; kappa) and the ResQue paper [3] (item list).
6. Draft a documented literature-search protocol for the gap statement; complete the manual Google Scholar checks and the pending volume/page checks.
7. Complete steps 1–2 of questionnaire validation (construct literature review; item review notes).
8. Ask BINUS what ethics/consent/data-protection requirements apply and collect the answer.
9. Prepare *drafts* (not final) of the participant information sheet, rater guide and anonymization policy.
10. Prepare the advisor meeting material (Section 13).
11. Keep development data separate from future study data (use a fresh store later).

### MUST WAIT (needs advisor/institution decision first)
1. Choosing the final Gemini model identity/version (count resolved: 1, Gemini-only).
2. Finalizing stimulus profile demographic composition detail (count resolved: 24), token limit, seed policy, temperature value (repetition count resolved: 3 Gemini repetitions per profile; baseline count resolved: 24, not repeated).
3. ~~Choosing the number and qualifications of experts, the rating rubric, the reliability statistic~~ — RESOLVED: expert evaluation excluded from the study.
4. Choosing the RQ3 design, plan exposure, participant eligibility, recruitment and sample size.
5. ~~Changing the baseline rules (post-cutback rebound, taper anchoring)~~ — **RESOLVED: rebound fixed, taper confirmed correct and unchanged.** Freezing the baseline (commit tag + generating/storing the 24 profiles' baselines) is still a separate, not-yet-done step.
6. Freezing the prompt (P1) and the freeze commit.
7. Building the experiment harness and the study-grade data store (their parameters depend on 1–3).
8. Changing the evaluation application (16 items, anonymous code, blinding) — its content depends on the questionnaire and design decisions.
9. Pilot testing the questionnaire and collecting any participant data.
10. Running RQ2 as the final experiment; any inferential test choice; any composite score or weights.
11. Updating the paper's methodology/evaluation sections to the approved design.

---

## 13. Advisor meeting checklist (most invalidating questions first; 15 maximum)

1. ~~**Scope of RQ2:** is evaluating the LLM on Week-1 personalization only acceptable, or must the LLM handle multi-week content?~~ — **RESOLVED (2 October 2026): multi-week scope CONFIRMED.** Remaining question: are technical-validation criteria T1–T14 sufficient evidence for RQ1, now extended to the multi-week pipeline?
2. ~~**Which LLMs** (number, exact versions, access/cost)~~ — **RESOLVED: 1 LLM (Gemini).** Remaining question: exact version/pinning policy?
3. **Prompt parity:** accept provider-specific delivery (Gemini concatenation vs OpenAI system role; different JSON modes) or require alignment? Freeze the prompt before the run? Run a prompt-sensitivity check?
4. **Generation conditions:** temperature value, token limit, seed policy, retry policy (none today), time window.
5. ~~**Stimulus set and repetitions:** how many runner profiles, which strata, how many repetitions per model?~~ — **RESOLVED: 24 profiles; 3 Gemini repetitions per profile (72 total); baseline 24, not repeated.** Remaining question: strata/demographic composition detail within the 24.
6. **Baseline freeze:** ~~fix or document the post-cutback rebound and the starting-mileage-anchored taper~~ — **RESOLVED** (rebound fixed; taper confirmed correct, Week-1 ×1.06 behavior was never in question). Who approves the baseline version, and when is the commit tagged, remain open steps ahead of generating the 24 profiles' baselines.
7. **Rubric:** which criteria are kept; unweighted profile or composite (and how weights would be justified); is validator-derived "consistency" acceptable as an outcome given its circularity; how to treat the progression criterion that cannot be measured from Week 1?
8. ~~**Expert evaluation:** number and qualifications of experts, blinding method, rubric source ([11]), reliability statistic, workload~~ — **RESOLVED (2 October 2026): expert evaluation excluded entirely from the study.** Remaining open question: include baseline-only and template controls?
9. **RQ3 design:** within-subject, between-subject or single-arm; Week 1 or full plan; participant's own profile or vignettes; which "AI" plan (which model/prompt) is shown?
10. **Sample size and pilot:** which approach to justify the main-study sample, the pilot sample, and the minimum for reliability estimation?
11. **Eligibility and recruitment:** adults only? exclusions? channels? (The application currently accepts ages 12–99.)
12. **Ethics:** which review route or exemption applies at BINUS; required consent, information sheet, withdrawal and retention rules.
13. **External LLM transmission:** may participant profiles (including injury text) be sent to third-party LLM APIs; if not, redaction or vignettes?
14. **Questionnaire:** accept the 16 study-specific items with the validation path (panel size, pilot size)? May items be adapted from ResQue after reading its item list? Scale format and "not applicable" option?
15. **Analysis:** descriptive only, or inferential tests (which, with what multiplicity control)? Preregistration of the protocol?

---

## 14. Audit conclusions

### Evidence-based observations (summary)
- The deterministic pipeline, scheduling, planned/actual integration and security layers are implemented and covered by 194 passing tests; this supports RQ1 only partially under the lock's own 14 criteria.
- The repository **cannot run the controlled LLM comparison**: it does not preserve raw outputs, validator verdicts, errors, run/experiment IDs, model versions or prompt versions, and it takes the model from global settings.
- The user-study application does not implement the 16-item questionnaire, neutral defaults, blinding, participant codes or consent.
- Many methodology items are legitimately open and require advisor/BINUS decisions; none was decided here.
- The paper contains no unsupported results, validity, novelty or performance claims, with two alignment items to reconcile after approval.

### Overall status
**READY FOR ADVISOR REVIEW** — the methodology proposal, the evidence and the list of open decisions are complete enough to take to the supervisor. The project is **NOT ready for experiment or data collection**: it has not reached "READY FOR EXPERIMENT AFTER ADVISOR APPROVAL", because implementation prerequisites (harness, prompt versioning, study data store, evaluation application, consent flow) and rule-engine freeze decisions are missing.

### Count summary
| Table | READY / 🟢 | PARTIALLY READY / 🟡 | NOT READY / 🔴 | ADVISOR DECISION REQUIRED / 🔵 | Total |
|---|---|---|---|---|---|
| RQ1 criteria T1–T14 (Section 1) | 2 | 9 | 2 | 1 | 14 |
| RQ2 requirements (Section 2) | 0 | 11 | 9 | 1 | 21 |
| Final readiness matrix (Section 11) | 1 | 6 | 7 | 12 | 26 |

**Blocking items in the final matrix (Section 11): 20 of 26** (rows whose "Blocking?" starts with "Yes"); 2 rows resolved by the 2 October 2026 update (model count, expert evaluation).

---

## Advisor Decision Update — 2 October 2026 — `SUPERSEDED` (2-LLM design; kept for audit trail only)

~~- **2 LLM design approved:** RQ2 compares exactly 2 LLMs ("LLM A", "LLM B") — Sections 3.2, 11.~~
~~- **3 repetitions approved:** 3 repetitions per (runner profile × LLM) combination; replicates, not independent runners; runner profile remains the sampling/block unit — Sections 3.2, 11.~~
- **Expert evaluation excluded from the study design:** no coach/expert rating, expert rubric, inter-rater agreement, expert recruitment, or blinded expert assessment — Sections 3.3, 3.4, 4, 8, 11, 13. *(Not superseded — still current.)*
- ~~Not resolved by this update (preserved): specific LLM identities and versions; the 24-profile count…~~ — see the next section for current status.

## Advisor Decision Update — 2 October 2026 (Gemini-only design)

**This is the current, authoritative design, superseding the 2-LLM design recorded in the update above (issued earlier the same day).**

- **1 LLM (Gemini) CONFIRMED** — Sections 3.2, 11; supersedes the earlier same-day 2-LLM resolution.
- **24 runner profiles CONFIRMED** — Section 11; previously PROPOSED/unconfirmed.
- **3 Gemini repetitions per profile CONFIRMED → 72 Gemini generations; 24 baseline plans, not repeated** — Sections 3.2, 11.
- **Exactly 8 automated criteria LOCKED** — Section 4; exact operational definitions remain an OPEN SUB-DECISION, explicitly flagged (conflict with the lock's own list, the superseded comparative proposal's 16, and the paper's Table IV 5).
- **Multi-week scope CONFIRMED** — resolves the former Section 13 item 1 "Scope of RQ2" open methodological decision. Pipeline: Runner Profile → Validation → Physiological Calculation → Deterministic Rule-Based Multi-Week Baseline → Gemini Personalization → Server-Side Validation → Gemini-Personalized Multi-Week Plan → Automated Evaluation → Baseline vs Gemini Comparison.
- **Expert evaluation still excluded** (unchanged) — Sections 3.3, 3.4, 4, 8, 11, 13.
- **No ranking/winner framing**: results per criterion, baseline vs Gemini; no composite/overall score.
- **Not resolved by this update** (still open/unresolved): exact Gemini model/version and pinning policy; exact 8-criteria operational definitions (Section 4); the exact statistical/inference method (must account for 72 Gemini outputs nested within 24 profiles); RQ3 design, participants, ethics and consent (Section 5); reproducibility harness implementation (Section 9); profile demographic composition detail. **Resolved since this update: baseline rule-engine rebound/taper issues (Section 7)** — rebound fixed in code, taper confirmed correct as-is.

---

## STATUS SUMMARY

**CONFIRMED:** 24 runner profiles; Gemini as the only LLM; 3 Gemini repetitions per profile; 24 baseline plans; 72 Gemini generations; no expert evaluation; exactly 8 automated criteria (count locked); multi-week personalization; baseline vs Gemini comparison.

**OPEN:** exact Gemini model/version; exact 8-criteria definitions/thresholds (explicit conflict between this audit's own rubric table, the methodology lock's 8, the superseded comparative proposal's 16, and the paper's Table IV 5 — not resolved here); statistical test; RQ3 sample size; ethics/BINUS requirements; questionnaire validation/pilot; prompt implementation/reproducibility details; profile demographic composition.

