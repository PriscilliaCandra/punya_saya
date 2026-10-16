# RESEARCH_METHODOLOGY_LOCK

**STATUS AS OF 2 OCTOBER 2026 (LATER SAME DAY): the "2 LLM" design (LLM A vs LLM B) below is `SUPERSEDED`.** The advisor's new FINAL LOCKED design is **1 LLM only (Gemini) vs the deterministic baseline**: 24 profiles CONFIRMED, 3 Gemini repetitions (72 generations) + 24 baseline plans (not repeated), exactly 8 automated criteria (definitions OPEN — see the conflict flagged below), multi-week scope CONFIRMED. See "Advisor Decision Update — 2 October 2026 (Gemini-only design)" at the end of this document and the STATUS SUMMARY that follows it.

**Status: PROPOSAL FOR SUPERVISOR REVIEW — nothing in this file is approved yet, except where marked APPROVED/CONFIRMED** (see "Advisor Decision Update — 2 October 2026" at the end of this document, itself `SUPERSEDED` by the Gemini-only update that follows it): ~~2 LLMs (LLM A, LLM B); 3 repetitions per (runner profile × LLM)~~ — **superseded by: 1 LLM (Gemini); 3 Gemini repetitions per profile (72 generations); 24 baseline plans (not repeated).** Expert evaluation excluded from the study entirely (unchanged). It specifies the methodology to be fixed *before* any experiment or participant data collection. Evidence base: `PAPER_DRAFT.md`, `PAPER_GAPS.md`, `LITERATURE_MATRIX.md`, `CITATION_AUDIT.md`, `QUESTIONNAIRE_TRACEABILITY.md`, `EVIDENCE_MAP.md`, and the source code at commit `224d910` (working tree has no tracked changes; documentation files are untracked). Reference numbers [n] follow the current manuscript.

Markers: `[TO BE DECIDED WITH ADVISOR]`, `[ADVISOR DECISION REQUIRED]`, `[ADVISOR/METHOD REVIEW REQUIRED]`, `[CHECK BINUS REQUIREMENTS]`, `[NOT IMPLEMENTED]` (code change needed), `[VERIFY]`.

---

## 1. Research objective

| Element | Definition | Status |
|---|---|---|
| **Research objective** | To explore a hybrid recommendation design for personalized running training plans in which deterministic running-domain calculations and training constraints establish a multi-week baseline plan, Gemini personalizes the baseline, and server-side validation is applied after personalization; and to evaluate (a) the technical behavior of the design, (b) how Gemini-personalized output differs from the deterministic baseline under identical conditions (UPDATED: Gemini-only, not "different LLMs" — see the Advisor Decision Update at the end), and (c) how users perceive the resulting plans. (Wording follows the manuscript: "explores", no novelty claim beyond the literature.) | Draft |
| **Research artifact** | The software prototype in this repository (FastAPI/SQLite/React): rule engine (`rules/`), LLM personalization and validation (`ai/`), scheduling and logging. It is the object being studied, not the scientific contribution. Feature count is not a contribution. | Exists |
| **Technical validation** | Pass/fail verification that the artifact implements its specification (Section 3). Answers RQ1. Makes no claim about training effectiveness. | Partly done (194 tests pass) |
| **LLM comparison** | Controlled experiment in which only the LLM used for personalization varies (Section 4–6). Answers RQ2. | [EXPERIMENT REQUIRED] |
| **User evaluation** | Study of runners' perceived personalization, usefulness, clarity and confidence (Section 7–8). Answers RQ3. | [DATA REQUIRED] |

Out of scope (must not be claimed): improved performance, injury prevention, clinical validity, longitudinal adherence, comparison of complete applications.

---

## 2. Research questions — specification summary

| | RQ1 | RQ2 | RQ3 |
|---|---|---|---|
| Text | How can a hybrid AI-based system generate personalized multi-week running training plans by combining deterministic training constraints with Gemini-based personalization? (updated wording: "Gemini-based", not generic "LLM-based" — single named model) | **CURRENT/LOCKED (Gemini-only, supersedes the 2-LLM direction below):** How does Gemini-based personalization differ from a deterministic baseline in generating personalized multi-week running training plans while maintaining predefined training constraints? ~~`SUPERSEDED`: How do different large language models, given the same runner profile and the same deterministic baseline plan, differ in personalizing the plan while remaining consistent with the runner profile and predefined training constraints?~~ | How do users perceive the generated training plans in terms of personalization, usefulness, clarity, and confidence? |
| **Input** | Validated runner profiles (`RunnerProfileCreate`), including edge cases | **CONFIRMED:** 24 runner profiles; the deterministic multi-week baseline for each (24 baseline plans, not repeated); fixed prompt; **CONFIRMED: 1 LLM (Gemini)**, exact version to be finalized ~~APPROVED/CONFIRMED: 2 LLMs ("LLM A", "LLM B")~~ superseded | Participants; plans generated for their (or vignette) profiles; the questionnaire |
| **Method** | Specification-based verification with automated tests and documented inspection | Controlled generation experiment (profile × condition [baseline/Gemini] × repetition — 3 Gemini repetitions per profile, baseline generated once), **automatic/objective metrics only (8 locked criteria) — expert rating excluded from the study** | Within- or between-subject exposure to rule-based and AI-personalized plans; questionnaire (Section 7) |
| **Output** | Pass/fail per criterion; list of constraint violations; documented limitations | Baseline vs Gemini counts of valid/invalid outputs, violation categories, deviations, per criterion (never an overall ranking/winner) | Item- and construct-level descriptive statistics, response distributions, comments |
| **Evidence required** | Test report with commit hash; explicit oracle for each criterion | Raw outputs, validator verdicts, run metadata (Section 13) | Anonymous responses, consent records, instrument version |
| **Analysis** | Pass/fail; violation counts (Section 10) | Descriptive comparison; automated criteria only (Section 10) | Descriptive statistics; alpha if appropriate; no inference promised (Section 10) |
| **Status** | Largely available | [EXPERIMENT REQUIRED] | [DATA REQUIRED] |

---

## 3. RQ1 — technical validation

### 3.1 What counts as evidence
RQ1 is answered by showing that the *implemented* design performs each stage of the pipeline correctly with respect to its own specification. "Correct" means conformance to the documented rule or schema, not scientific effectiveness. Only capabilities that exist in the code are listed.

### 3.2 Pass/fail criteria

Test column: existing automated test coverage at commit `224d910` (194 tests passed; verified run). "Gap" means no test currently covers the criterion and one must be added before the lock.

| # | Capability (implemented) | Pass criterion | Existing coverage | Gap / action |
|---|---|---|---|---|
| T1 | Input validation (`schemas.py`) | Out-of-range or malformed fields (age, times, race distance, duration 4–24, days 1–7) are rejected with HTTP 422; valid profile accepted | `test_profile.py`, `test_api.py` | Add table-driven boundary tests for every field |
| T2 | VDOT (`rules/vdot.py`) | VDOT computed from 5K PB equals an independent recomputation of Eqs. (1)–(3); same input → identical output | `test_vdot_formula_matches_known_reference_value` asserts only 37 ≤ VDOT ≤ 40 | Add exact-value oracle (independent implementation); cross-check against published VDOT table [27] [OPEN] |
| T3 | Pace zones | Each zone pace equals the inversion of Eq. (1) at the implemented fraction; easy range ordered fast→slow; zones monotonic (easy > marathon > threshold > interval > repetition in speed) | Presence checked only | Add monotonicity and recomputation tests |
| T4 | Multi-week generation | Number of weeks = requested duration for every duration 4–24 | Durations 4, 8, 12, 16, 24 | Parametrize all 21 durations |
| T5 | Weekly structure | Each week has exactly 7 entries Monday–Sunday; number of non-rest days = requested training days (days 1–7) | `test_training_day_distribution_across_all_valid_day_counts` (1–7) | Assert for all weeks, not only Week 1 |
| T6 | Rule conformance (Table II) | For every week and test profile, each workout distance equals the value given by the documented formula (long run = min(30%, cap) with floor; quality = 20% with floor; easy runs = remainder split with floor); progression, cutback and taper multipliers as documented | Partial (`long_run…`, `weekly_progression…` for build weeks only), plus `test_t7_progression_fix.py` (new) for cutback, post-cutback progression, and taper/race-week anchoring | Add oracle tests for caps/floors; **these assert conformance to the implemented design constraints, not scientific validity** |
| T7 | Known rule-engine properties | **RESOLVED.** Post-cutback rebound FIXED (`generate_weekly_progression_summary` now carries the cutback week's own reduced volume into the next build step instead of the pre-cutback peak); taper anchored to starting volume CONFIRMED CORRECT and left unchanged (matches Table II) | `backend/tests/test_t7_progression_fix.py` (7 tests); full suite 201/201 passing | Resolved — see `paper/CODE_AUDIT_EASY_RUN_PACE_AND_T7.md` for the audit and fix record. Remaining step before the baseline is frozen: generate/freeze the 24 baseline plans against this fixed rule-engine version (not yet done) |
| T8 | LLM prompt construction | Prompt contains profile, VDOT, zones, Week 1 baseline and the numeric-preservation instruction | None | Add snapshot test; introduce prompt version (Section 4.3) [NOT IMPLEMENTED] |
| T9 | Server-side validation (`ai/validator.py`) | Each violation class below is rejected: schema/missing field, workout count, unknown day, duplicate day, workout type, distance (>0.05 km), pace string, intensity-zone string, weekly mileage (>0.15 km), rest-day count, training-day count; a valid plan passes and is reordered Mon–Sun | Tests cover distance, pace, mileage, workout count, malformed JSON, missing field | Add tests for workout type, intensity zone, unknown/duplicate day, rest-day count, training-day count |
| T10 | Deterministic fallback | On no API key, API error, malformed JSON, or validation failure, a schema-valid plan identical to the baseline in all numeric fields is returned and the fallback label is stored | No key, invalid plan, malformed JSON covered | Add HTTP-exception/timeout path test |
| T11 | Scheduling | Each plan gets 7 × weeks scheduled rows; calendar dates derived from start date, week and weekday correctly (incl. mid-week start) | `test_multi_week_plans.py` (durations 4, 8, 24; date mapping) | Parametrize all durations |
| T12 | Planned/actual integration | Completion status derived (completed/missed/scheduled; none for rest days); a log can link only to the owner's planned workout; soft-deleted logs excluded | `test_workout_linking.py` (28), `test_dashboard.py`, `test_progress.py` | — |
| T13 | Authorization/security (support, not core to RQ1) | Non-owner receives 404 for another user's plan; CSRF Origin check; auth tests | `test_authorization.py`, `test_csrf.py`, `test_auth.py` | Rate-limit coverage is thin (2 tests) |
| T14 | Whole suite | All tests pass on the frozen commit in a clean environment | 194 passed (2026-10-01) | Re-run on the freeze commit; record environment (Section 13) |

**Reporting rule:** results are reported as counts of passed/failed criteria and of failed assertions, with the commit hash. No numeric "accuracy" or "quality" is attached to technical validation.

---

## 4. RQ2 — controlled LLM comparison

### 4.1 Design — **UPDATED (Gemini-only, LOCKED 2 October 2026)**
- **Comparison condition (CURRENT):** deterministic multi-week baseline vs Gemini-personalized multi-week output (one factor: condition, levels = baseline, Gemini). ~~**SUPERSEDED independent variable:** the LLM used for personalization (one factor, APPROVED/CONFIRMED levels = 2, "LLM A" and "LLM B").~~
- **Held constant:** runner profile, deterministic multi-week baseline, prompt text (system + user), output schema (`AIPersonalizedPlan`), validator, tolerances, generation settings.
- **Unit of analysis (UPDATED):** the cell = (profile, condition); for Gemini this aggregates 3 repetitions per profile (72 total); the baseline has one observation per profile (24 total), not a "generation" in the stochastic sense. ~~SUPERSEDED: one generation = (profile, model, repetition).~~
- **Scope:** the experiment compares the *personalization layer (Gemini) against the deterministic baseline*. It does not run the web application, user flows, or the fallback path (the fallback is recorded as a separate control condition, Section 4.5).
- **What the layer does now (CONFIRMED, supersedes Week-1-only):** Gemini receives and may rewrite **sufficient multi-week context**, not Week 1 only. Progression/periodization across weeks is now within Gemini's remit and can be evaluated (see Section 5, criterion 5, updated).
- ~~**OPEN METHODOLOGICAL DECISION: The relationship between the multi-week research scope and the specific weeks/context presented to the LLM must be finalized before the comparative experiment.**~~ — **RESOLVED/CONFIRMED**: multi-week scope is locked; pipeline: Runner Profile → Validation → Physiological Calculation → Deterministic Rule-Based Multi-Week Baseline → Gemini Personalization → Server-Side Validation → Gemini-Personalized Multi-Week Plan → Automated Evaluation → Baseline vs Gemini Comparison.

### 4.2 Candidate models — **UPDATED (Gemini-only, LOCKED 2 October 2026, later same day — supersedes the 2-LLM resolution below)**
| Item | Specification | Status |
|---|---|---|
| Providers used | Google Gemini REST (`generateContent`) only. The OpenAI adapter exists in the repository but is **not used** for this study | Fact |
| Number of models | **CONFIRMED: 1 (Gemini)** | Resolved |
| Identity of model | Gemini — exact model/version to be finalized and recorded before experimental data collection [TO BE DECIDED WITH ADVISOR]. Default in code (`gemini-1.5-flash`) is a placeholder and must be checked for availability on the experiment date [VERIFY] | Open (identity only; count resolved) |
| Exact model version string | Record the identifier sent *and* any version/fingerprint the API returns. If the alias moves between versions, prefer a dated/pinned identifier | [TO BE DECIDED WITH ADVISOR] |
| Adding a second/third model | **Not applicable** — the study uses exactly 1 LLM (Gemini); this supersedes the earlier 2 LLM ("LLM A"/"LLM B") resolution of the same day | Resolved: Gemini only |
| Selection rationale | Document why Gemini was chosen (access, cost, prior use in the literature [11], [12]) | To write |

### 4.3 Experimental conditions
| Parameter | Current code | Locked value |
|---|---|---|
| Temperature | 0.4 (hard-coded for Gemini) | Keep 0.4 unless the advisor decides otherwise; document that fixed temperature does not guarantee deterministic output |
| Max output tokens | Not set (provider default) | [TO BE DECIDED WITH ADVISOR]; if set, set identically and large enough to avoid truncation; record truncation events |
| Other sampling (top-p, top-k, seed) | Not set | Use provider defaults and record them; use a seed only if both providers support one [VERIFY] |
| JSON enforcement | Gemini: `responseMimeType: application/json` | Single-provider mechanism now; no cross-provider difference to equalize |
| Timeout | 30 s | Keep; record timeouts as failures, not as retries |
| Retries | None (single attempt) | None; each generation is one attempt, consistent with production behavior |
| System/user prompt | `ai/prompts.py` (`SYSTEM_PROMPT`, `build_user_prompt`) | **Freeze as prompt version `P1`** [NOT IMPLEMENTED: no version tag exists; store SHA-256 of the exact rendered prompt per run]. Any prompt change creates a new version and a new experiment |
| Output schema | `AIPersonalizedPlan` (extended for multi-week scope, per the confirmed pipeline) | Frozen with the code commit |
| Deterministic baseline | `generate_rule_based_plan` at the freeze commit | Frozen; baseline JSON stored per profile (24 baseline plans, generated once each, not repeated); decide rule-engine issues (T7) *before* freezing |
| Gemini repetitions per profile | — | **CONFIRMED: 3** per profile → 72 Gemini generations across 24 profiles. Replicates, not independent runners; needed because sampling is stochastic. The baseline is NOT repeated (deterministic) |
| Number and composition of profiles | — | **CONFIRMED: 24.** Demographic composition detail within the 24 is an open sub-decision if not finalized elsewhere; see 4.4 |
| Date/time | — | Run all Gemini calls within one short, recorded window (UTC timestamps per call) to limit drift; schedule [TO BE DECIDED WITH ADVISOR] |
| Order of calls | — | Randomize/interleave call order across profiles to avoid time-of-day confounds |

### 4.4 Profile set (stimuli)
Profiles are **vignettes created by the researcher** (no real participants needed for RQ2). The set should cover factors that change the deterministic baseline or the textual personalization, so the comparison is not dominated by one runner type. Candidate strata (proposal; counts [TO BE DECIDED WITH ADVISOR]):
- experience level (beginner → tempo session; intermediate/advanced → interval session);
- training days per week, including the 1-day edge case and 7 days;
- injury note present (several different limitations) vs absent;
- target race distance (5K, 10K, half marathon: affects long-run cap);
- weekly mileage regime (affects floors/caps);
- preferred-day patterns.
Because Week 1 volume does not depend on plan duration, duration need not vary for RQ2 (verified in code: Week 1 target = base × 1.06/1.08). Profile vignettes and their rationale are fixed and stored before generation.

### 4.5 Control conditions (optional, [ADVISOR DECISION REQUIRED])
- **C0 baseline-only:** the deterministic plan without personalized text (reference for numerical identity).
- **C1 deterministic fallback synthesizer:** the non-LLM template text (reference for "text richness without an LLM"); required if the user study compares it with LLM text, otherwise text amount is confounded with LLM use.

### 4.6 Required implementation before running [NOT IMPLEMENTED]
An experiment harness, separate from the web path, that: (1) loads a profile file; (2) builds the baseline and prompt; (3) calls the provider function with an explicit model name (today the model comes from global settings); (4) stores the raw HTTP response body, parsed JSON, model identifier returned, parameters, timestamps, latency, HTTP status, token usage; (5) runs `validate_ai_plan` and stores pass/fail and the exception reason; (6) never falls back silently. Secrets must not be logged (note: the Gemini call places the API key in the URL query string; logs and stored URLs must be sanitized).

---

## 5. Baseline-vs-Gemini comparison criteria (candidate rubric) — **UPDATED: count LOCKED AT EXACTLY 8, not the 8-ish items shown below as a draft list which must be reconciled**

**SUPERSEDED (2 October 2026): expert evaluation has been removed from the study entirely.** This section is retained for the automatic/objective criteria only; references to expert ratings below describe the previous design and no longer apply — RQ2 relies solely on automated/objective evaluation criteria. **The advisor's Gemini-only locked design fixes the criteria count at exactly 8** (profile consistency, goal consistency, physiological/pace consistency, weekly volume/mileage consistency, workout structure, intensity constraints, progression/recovery constraints, completeness/constraint violations). **OPEN SUB-DECISION, flagged not resolved:** this section's own 8-item table below does not use identical wording/grouping to that locked list, nor to the (superseded) comparative proposal's 16-item draft, nor to `PAPER_DRAFT.md` Table IV's 5-criterion list — all three must be reconciled into one definitive rubric. Principles: **automatic, objective checks only**; report each criterion separately; avoid a single composite score unless justified (see 5.2); criteria now apply across the confirmed multi-week scope, not Week 1 only. Literature citations below are kept for context/design inspiration only, not as proof of validity of these specific measures.

| # | Criterion | Operational definition | Measurable evidence | Scoring method | Literature support |
|---|---|---|---|---|---|
| 1 | Runner-profile consistency | Personalized text does not contradict the profile (goal race, goal time, experience, training days, injury note) and addresses reported limitations | (a) Structural fields identical to baseline (automatic); (b) checklist of profile facts mentioned correctly/incorrectly (automatic string/number extraction + expert confirmation); (c) injury-specific content present when an injury is reported | (a) pass/fail; (b) count of contradictions; (c) present/absent | Expert criteria in [11]; safety review [15] |
| 2 | Pace consistency | `pace_target` and `intensity_zone` equal the baseline; paces quoted in free text equal the baseline zones | Exact string match (validator); numbers extracted from text vs zone table | Rate of exact matches; count of text paces not in zone table | Numerical-preservation requirement in the design (internal); hallucination background [16] |
| 3 | Weekly-volume consistency | `weekly_mileage_km` and each `distance_km` equal the baseline within the validator tolerance; distances quoted in text equal the baseline | Validator result; absolute deviation per field; text-number extraction | Pass/fail; deviation distribution | Internal specification |
| 4 | Workout-distribution consistency | Same day set, workout types, rest-day count and training-day count as baseline | Validator result per sub-check | Pass/fail per sub-check; violation category counts | Internal specification |
| 5 | Progression consistency | Text statements about progression, load or taper are consistent with the baseline progression | **Now measurable**: multi-week scope is CONFIRMED (Section 4.1), so progression/cutback/taper criteria can discriminate Gemini's behavior across weeks, not only describe the deterministic engine. Rule-based contradiction checks; `SUPERSEDED`: expert rating is no longer used | Automated rule check | Progression/taper evidence [17], [18], [22], [23] only as context |
| 6 | Output completeness | All schema fields present and non-empty: for each non-rest day `warmup_cooldown`, `workout_execution`, `recovery_instruction`, `purpose`; plus `coach_overview`, `personalized_insights`, `ai_personalization_summary`, `why_this_plan_was_generated` | Field-level non-empty check; JSON validity; truncation | Proportion of required fields present | Completeness-oriented coding in [10] |
| 7 | Personalization (automated proxy) | Degree to which text uses the runner's specific profile facts, assessed by rule-based/automated checks only | Rule-based extraction and contradiction checks (profile facts, goal, injury content presence); `SUPERSEDED`: blinded expert ratings and safety flags are no longer used in this study | Automated pass/fail and counts | Design rationale only; no expert-rating citation applies |
| 8 | Reliability/efficiency (supporting) | Failure and variability of calls | HTTP errors, timeouts, invalid JSON, latency, tokens, cost; variability of outputs across repetitions | Counts, medians | Reproducibility focus of [12] |

### 5.1 Handling of the validator
Criteria 2–4 are partly the validator's own checks. Report **first-attempt validator pass rate** and **failure categories** per model, but state that this measures compliance with the instructions the validator enforces, not general quality. Because the validator is also the production safeguard, include a *sensitivity analysis*: pass rate under the current tolerances and under exact equality [ADVISOR DECISION REQUIRED].

### 5.2 Weighted vs unweighted
Recommendation: **unweighted, criterion-by-criterion reporting** (a profile of scores), no composite index. Reasons: no literature-derived weights exist for these dimensions; arbitrary weights would be an unjustified modelling choice; criteria differ in kind (hard constraints vs subjective quality). If the advisor requires a composite, the weights must be justified by one of: equal weights stated explicitly as a convention; expert-elicited weights (e.g., a structured expert survey/Delphi or pairwise-comparison method) with the elicitation documented [WEIGHTS REQUIRE LITERATURE/EXPERT JUSTIFICATION] [ADVISOR DECISION REQUIRED]. No weights are specified here.

### 5.3 Optional LLM-as-judge
An LLM judge could screen text at scale, but known biases (position, verbosity, self-enhancement) [31] and the risk of circularity (judging the same model family) argue against using it as primary evidence. Since expert evaluation is excluded from the study, there is no expert baseline to validate an LLM judge against; an LLM-as-judge is not part of the current design `[ADVISOR DECISION REQUIRED]` if proposed later.

---

## 6. Expert evaluation — `SUPERSEDED`: REMOVED FROM THE STUDY (Advisor Decision, 2 October 2026)

**Expert evaluation is excluded entirely from this study.** No coach/expert rating, expert rubric, inter-rater agreement, expert recruitment, or blinded expert assessment will be used. RQ2 relies solely on the automated/objective criteria of Section 5. The table below (the previous proposal) is kept for audit-trail purposes only and no longer applies.

| Aspect | Previous proposal (no longer applicable) | Status |
|---|---|---|
| Expert background | Practitioners with expertise in endurance/running training: running coach, exercise scientist, sports-science professional. Precedent: coaching experts rated plans in [11], [12], [15] | Fixed categories proposed |
| Inclusion criteria | Minimum qualification and years of endurance-coaching experience, and any certification | [ADVISOR DECISION REQUIRED] (no thresholds invented here) |
| Exclusion/conflict | Experts must not be involved in building the system; declare conflicts | Proposed |
| Number of experts | — | [ADVISOR DECISION REQUIRED]; more than one needed for inter-rater reliability |
| Recruitment | Professional networks, coaching associations | [ADVISOR DECISION REQUIRED] |
| Ethics | Experts are human participants (opinions, possibly identifiable) → consent and data handling | [CHECK BINUS REQUIREMENTS] |
| Materials per item | Runner profile; the deterministic baseline (numbers); one personalized output with the model identity **removed**; fixed presentation format | Proposed |
| Blinding | Model labels removed; formatting normalized (remove model-specific styling/length markers where possible); randomized presentation order; include repeated generations; optionally insert C0/C1 controls among items | Feasible; length differences cannot be fully blinded |
| Rubric | Items per criterion 1, 5, 6(optional), 7 and safety flags; 5-point ordinal scale with anchors; build from the literature-derived criteria of [11] after reading the full text; add running-specific items | [ADVISOR DECISION REQUIRED] |
| Calibration | Joint calibration session on a few non-study examples; written rater guide; independent rating afterwards | Proposed |
| Load | Number of outputs per expert must be feasible; consider incomplete block design if profiles × models × repetitions is large | [ADVISOR DECISION REQUIRED] |
| Inter-rater reliability | Ordinal agreement statistic suitable for ≥ 2 raters (e.g., weighted kappa for pairs, Fleiss' kappa, Krippendorff's alpha, or ICC) chosen before data collection; low agreement was reported in [11] (verify from full text) so report it honestly and do not hide disagreements | Method to be fixed [ADVISOR/METHOD REVIEW REQUIRED] |
| Disagreement | Report individual ratings and agreement; do not average away systematic disagreement without comment | Proposed |
| Data | Rater ID (pseudonymous), item ID, scores, comments, time | Section 9 |

---

## 7. RQ3 — user evaluation

### 7.1 Instrument status
The 16-item questionnaire (PP1–PP4, PU1–PU4, PC1–PC4, RC1–RC4) is **study-specific and currently unvalidated**. No item is adapted from a validated scale; proposed wording exists only in `QUESTIONNAIRE_TRACEABILITY.md` and is not final. The repository implements four single ratings, not the 16 items (Section 8). It must not be called a validated instrument in any document.

### 7.2 Design options for plan exposure [ADVISOR DECISION REQUIRED]
| Option | Description | Strength | Weakness |
|---|---|---|---|
| A. Within-subject, counterbalanced | Each participant rates both a rule-based baseline plan and an AI-personalized plan, order randomized, labels blinded | Paired comparison; fewer participants | Carry-over; participants may recognise richer text |
| B. Between-subject | Each participant sees one plan type | No carry-over | More participants; no paired analysis |
| C. Single-arm descriptive | Only the AI-personalized plan is rated | Simplest; descriptive | No comparison; cannot support "better" claims |

Confound to state in any option: the rule-based baseline contains little warm-up/execution text, whereas the personalized plan adds it by design. A difference in perceived clarity or personalization therefore reflects the combined effect of added text and LLM use, not LLM use alone. Control C1 (Section 4.5) can separate template text from LLM text.

### 7.3 Participants
| Item | Proposal | Status |
|---|---|---|
| Eligibility | Adults (≥ 18; the application accepts ages 12–99, so minors must be excluded explicitly or via ethics approval), current or recent recreational runners able to provide a 5K personal best and weekly mileage | [ADVISOR DECISION REQUIRED]; [CHECK BINUS REQUIREMENTS] |
| Exclusion | Medical conditions requiring supervised exercise; refusal of consent | [ADVISOR DECISION REQUIRED] |
| Recruitment | Running clubs/communities, university networks; voluntary, no coercion; recruitment channel recorded | [ADVISOR DECISION REQUIRED] |
| Sample size | Do not fix a number here. Candidate approaches: (i) feasibility/pilot sample to estimate item behavior and variance; (ii) precision-based planning for descriptive statistics (width of intervals for construct means); (iii) power analysis for a paired ordinal test requires an assumed effect size and is only valid with such an assumption; (iv) guidance on minimum respondents for reliability estimation (Cronbach's alpha) | [ADVISOR/METHOD REVIEW REQUIRED] |

### 7.4 Procedure (proposed)
1. Information sheet and informed consent (Section 12) before any data entry.
2. Participant receives an anonymous code (no name/email in the research tables).
3. Participant enters a runner profile (own data) **or** is shown a vignette profile [ADVISOR DECISION REQUIRED]. Own data raise privacy burden; vignettes limit personalization realism. Using the participant's own profile is needed for a meaningful "personalization" rating.
4. System generates plan(s) with the **LLM and prompt version fixed from RQ2** (decision on which model [ADVISOR DECISION REQUIRED]). The "AI" condition must use live LLM output, not fallback; plans whose `ai_model_used` indicates fallback are excluded from the AI arm and counted.
5. Participant views the plan(s) (Week 1 detail and multi-week overview) under blinded labels.
6. Participant completes the questionnaire; optional open comment.
7. Debrief: statement that the prototype is educational, not medical advice, and that following the plan was not part of the study.

### 7.5 Application changes required before data collection [NOT IMPLEMENTED]
16-item form with neutral (unset) defaults; agreement anchors consistent across items; anonymous participant code stored with each rating; neutral plan labels with randomized order; consent screen; recording of model name/version and prompt version with every evaluated plan; refusal to evaluate fallback plans as "AI"; restriction of evaluation endpoints (currently unauthenticated, accepts any existing plan ID) [VERIFY intended access control].

### 7.6 Privacy and anonymization
- Collect the minimum: coded profile variables needed to generate the plan; no name, email or contact data in research tables; keep consent records separate from responses.
- `injury_limitations` is free text and health-adjacent: make it optional, warn participants not to include identifying details, and consider storing it as a coarse category plus text kept only as long as needed [ADVISOR DECISION REQUIRED].
- Existing `runner_profiles` and evaluation rows in the development database are test data and must not be mixed into the study dataset; use a fresh database for data collection.
- Retention, access control, deletion/withdrawal procedure [CHECK BINUS REQUIREMENTS].

---

## 8. Questionnaire validation process (pre-study)

| Step | Activity | Output | Status |
|---|---|---|---|
| 1 | Literature review for construct definitions (PP, PU, PC, RC): targeted search for validated perceived-personalization, usefulness, clarity/transparency and trust/confidence scales; read the ResQue item list [3] and the framework of [2] | Construct definition document; list of candidate source items | OPEN |
| 2 | Item review: for every item, record origin (literature-derived / adapted / study-specific) and wording rationale; remove multi-barrelled and leading wording | Item table (see below) | OPEN |
| 3 | Expert/content review: panel of domain experts and a survey-methods reviewer rate relevance and clarity of each item | Content-validity record; revised items | [ADVISOR DECISION REQUIRED] (panel size) |
| 4 | Cognitive pretest with a few runners (think-aloud) | Wording problems list | OPEN |
| 5 | Pilot test with a sample [ADVISOR/METHOD REVIEW REQUIRED]: item distributions, missing responses, preliminary Cronbach's alpha per construct [33]; assess whether items within a construct behave consistently | Pilot report | EXPERIMENT REQUIRED |
| 6 | Wording revision based on 3–5; version the questionnaire (e.g., Q-v1 → Q-v2) | Final questionnaire | OPEN |
| 7 | Main data collection with the frozen questionnaire version | Dataset | DATA REQUIRED |

Item origin (current status — to be updated after steps 1–2):

| Items | Origin | Note |
|---|---|---|
| PP1–PP4, PU1–PU4, PC1–PC4, RC1–RC4 | **Study-specific** | None is literature-derived or adapted at present. An item may be reclassified as "adapted" only after its source item is identified, cited and the adaptation documented. Wording proposals: `QUESTIONNAIRE_TRACEABILITY.md` §3 |

Conceptual links only: usefulness and perceived quality of recommended items are among qualities addressed by [3]; PC and RC links are unconfirmed [VERIFY]. Claim to be used in the paper: "contextualized for this study; not an established validated questionnaire; pilot-tested only if step 5 is completed".

---

## 9. Data structure

Existing development tables (`runner_profiles`, `training_plans`, `plan_evaluations`) are **not** sufficient for the study (no participant ID, no raw LLM output, no rater data, no consent link). Research datasets should live in a separate store (database or files) created for the study [NOT IMPLEMENTED].

### 9.1 `stimulus_profiles` (RQ2 vignettes) and `participant_profiles` (RQ3)
| Variable | Type | Purpose | Privacy |
|---|---|---|---|
| profile_id | string (UUID) | Key | Pseudonymous |
| source | enum {vignette, participant} | Distinguish stimuli from human data | — |
| participant_code | string (random, no link to identity) | Join responses (participants only) | Linking table, if any, stored separately and access-restricted |
| age | int | Profile variable | Consider age bands for reporting |
| gender | string | Profile variable (not used in numeric rules) | Optional/self-described |
| experience_level | enum | Rule input | — |
| pb_5k, pb_10k | string MM:SS | Rule input | — |
| target_race_distance, target_race_time | enum, string | Rule input | — |
| current_weekly_mileage_km | float | Rule input | — |
| training_days_per_week, preferred_days | int, list | Rule input | — |
| plan_duration_weeks | int | Rule input | — |
| injury_limitations | text (optional) | Text personalization | **Sensitive**; optional; no identifying details; consider coarse category |
| easy_run_pace | string | Prompt only | — |
| created_at_utc | timestamp | Audit | — |

### 9.2 `baselines`
| Variable | Type | Purpose |
|---|---|---|
| baseline_id, profile_id | string | Keys |
| code_commit | string (git hash) | Reproducibility |
| baseline_json | JSON | Full deterministic output (VDOT, paces, weeks) |
| baseline_sha256 | string | Integrity check |

### 9.3 `llm_outputs` (RQ2)
| Variable | Type | Purpose |
|---|---|---|
| run_id | string | Key |
| profile_id, baseline_id | string | Links |
| model_provider, model_requested, model_returned | string | Version tracking |
| prompt_version, prompt_sha256 | string | Prompt identity |
| params_json | JSON | temperature, max tokens, JSON-mode settings, any defaults observed |
| repetition_index | int | Repeats |
| call_started_utc, latency_ms | timestamp, int | Drift and efficiency |
| http_status, error_type | int, string | API variability |
| raw_response | text | Verbatim response (unedited) |
| parsed_json | JSON/null | After `clean_json_response` |
| tokens_in, tokens_out | int | Cost |
| truncated | bool | Output limit effects |
Privacy: vignette profiles only → no personal data. For participant plans, raw output may repeat injury text → treat as sensitive.

### 9.4 `validation_results`
| Variable | Type | Purpose |
|---|---|---|
| run_id | string | Link |
| schema_valid, validator_pass | bool | First-attempt outcomes |
| failure_category | enum | One of the validator classes (schema, count, day, type, distance, pace, zone, mileage, rest-day, training-day) |
| failure_message | text | Validator exception text |
| max_distance_deviation_km, mileage_deviation_km | float | Deviation measures |
| text_completeness_ratio | float | Criterion 6 |
| text_number_mismatch_count | int | Criteria 2–3 (extracted numbers not in baseline) |
| injury_content_flag | bool | Criterion 1(c) |

### 9.5 `expert_evaluations` — `SUPERSEDED`: NOT NEEDED
Expert evaluation has been removed from the study (2 October 2026); this table is no longer required. Kept here for audit-trail purposes only.

| Variable | Type | Purpose | Privacy |
|---|---|---|---|
| ~~rating_id, run_id (or control id), rater_code~~ | string | ~~Keys~~ | ~~Rater identity stored separately~~ |
| ~~presentation_order~~ | int | ~~Order effects~~ | — |
| ~~item_id, score~~ | string, int (ordinal) | ~~Rubric ratings~~ | — |
| ~~safety_flag, flag_note~~ | bool, text | ~~Safety review~~ | — |
| ~~comment~~ | text | ~~Qualitative~~ | ~~May identify rater style~~ |
| ~~rated_at_utc, rubric_version~~ | timestamp, string | ~~Audit~~ | — |

### 9.6 `questionnaire_responses`
| Variable | Type | Purpose | Privacy |
|---|---|---|---|
| response_id, participant_code | string | Keys | No identity |
| plan_id, plan_condition (blinded label + true label stored) | string | Link to the plan exposed and its condition | — |
| model_returned, prompt_version, is_fallback | string, string, bool | Ensure AI arm = live LLM | — |
| presentation_order | int | Counterbalancing | — |
| item_id (PP1…RC4), response | string, int 1–5 | Data | — |
| questionnaire_version | string | Instrument version | — |
| comment | text (optional) | Qualitative | Warn: no personal details |
| submitted_at_utc | timestamp | Audit | — |

### 9.7 `consent_log` (separate store)
participant_code or consent token, consent version, timestamp, withdrawal flag. Kept apart from responses; access restricted [CHECK BINUS REQUIREMENTS].

---

## 10. Statistical analysis (no results implied)

### 10.1 Technical validation (RQ1)
Pass/fail per criterion T1–T14; counts of failed assertions; list of documented limitations. No inferential statistics.

### 10.2 LLM comparison (RQ2)
- **Descriptive first:** per model: counts and proportions of JSON-valid, schema-valid and first-attempt validator-pass outputs; frequency table of failure categories; distribution (median, range) of numerical deviations; completeness ratios; latency and token usage. Report results per profile stratum as well as pooled.
- **Variability:** agreement of outputs across repetitions (e.g., share of repetitions with the same validator outcome; variability of text-number mismatches).
- **Expert ratings:** `SUPERSEDED` — not collected; expert evaluation is excluded from this study.
- **Inter-rater reliability:** `SUPERSEDED` — not applicable; no raters in this design.
- **Inference:** no significance testing is promised. **The final statistical procedure will be selected based on the measurement scale, pairing structure, repeated-generation design, and distributional characteristics of the collected outcomes.** PROPOSED methodology only: the test must respect the non-independence of the 72 Gemini repetitions nested within the 24 profiles (profile as block/pairing unit) when comparing Gemini to the baseline; candidate approaches (Wilcoxon, Friedman, mixed models) are PROPOSED only [ADVISOR/METHOD REVIEW REQUIRED]. The 72 Gemini outputs must **not** be treated as 72 independent participants. Without a finalized test, claims are limited to descriptive differences in this sample of profiles.
- **Multiplicity:** if many criteria are tested, state the policy beforehand [ADVISOR/METHOD REVIEW REQUIRED].
- **No composite score** unless approved (Section 5.2). No pass thresholds are invented; any acceptability threshold would need a source or an explicit advisor decision.

### 10.3 Questionnaire (RQ3)
- Item level: N, response distribution, median, mean, SD.
- Construct level: mean/median/SD per construct per plan condition; handling of missing items fixed beforehand.
- Reliability: Cronbach's alpha per construct only if four items are collected from enough respondents [33] [ADVISOR/METHOD REVIEW REQUIRED for the minimum]; do not report alpha from the pilot as evidence of validity of the final instrument.
- Comparison between plan types, if the design is within-subject: paired, ordinal-appropriate analysis; if between-subject: independent-group analysis; choice and any significance testing only after the sample and design are fixed. Parametric analysis of Likert data is argued to be robust [32], but the decision remains [ADVISOR/METHOD REVIEW REQUIRED].
- Qualitative comments: coded descriptively (method [TO BE DECIDED WITH ADVISOR]).

---

## 11. Threats to validity

| Threat | Description | Mitigation / how documented |
|---|---|---|
| Construct validity | Questionnaire constructs unvalidated; PC and RC definitions unclear; "personalization" depends on text richness; rubric criteria are the researcher's choices; "consistency" measures partly equal the validator's own checks | Questionnaire process (Section 8); report validator-derived metrics as compliance, not quality; expert rubric reviewed by advisor |
| Internal validity | Order and carry-over effects; non-neutral slider defaults; visible plan labels; AI arm contaminated by fallback text; plan type confounded with text amount; unequal provider JSON mechanisms | Counterbalancing, blinding, neutral defaults, fallback exclusion, control C1, document provider differences |
| External validity | Vignette profiles; volunteer runners; single language/culture; one rule engine; one prompt; LLM personalization over the full multi-week schedule as implemented (effectiveness not yet evaluated); only three race distances | State scope; do not generalize beyond the sampled profiles and participants |
| Researcher bias | Researcher built the system, prompt, rubric and baseline, and may favor the hybrid design | Fix protocol before data; blinded expert rating; report all runs including failures; separate rubric authors from raters where possible; consider preregistration [ADVISOR DECISION REQUIRED] |
| Model-version drift | Provider models change or are retired; aliases may move | Pinned identifiers where possible; single time window; store returned model identifier and date; state that results apply to those versions |
| Prompt sensitivity | Results may change with small prompt changes | Freeze prompt version; report prompt text; optional prompt-sensitivity run as a separate, labelled experiment |
| API variability | Latency, rate limits, outages, nondeterminism at temperature 0.4, provider-specific JSON modes | Repetitions; log HTTP status and errors; count failures; no silent retries |
| ~~Expert-rater subjectivity~~ | `SUPERSEDED` — expert evaluation removed from the study (2 October 2026) | n/a |
| Questionnaire limitations | Self-report; acquiescence; single exposure; perception ≠ effectiveness; ceiling effects with positive text | Neutral defaults; item review; interpret as perception only |
| Sample limitations | Small, convenience sample; self-selection | Descriptive claims only; report demographics in coarse form |
| Rule-engine limitations | Constants are engineering design constraints (`PAPER_GAPS.md` §5b); post-cutback rebound **RESOLVED** (fixed in `generate_weekly_progression_summary`, verified by `backend/tests/test_t7_progression_fix.py`, 201/201 tests passing); taper anchored to starting volume **CONFIRMED CORRECT** (intentional, matches Table II, not changed); age/sex/10K PB not used numerically; `easy_run_pace` confirmed not used by the baseline and confirmed excluded from E6/E7 (separate decision) | State the taper-anchoring design choice and the rebound fix in the paper (Section III-E); no fix-or-document decision remains open |
| Safety | LLM text (nutrition, hydration, injury) is not validated | Expert safety flags; participants told it is not medical advice; no real-world training outcomes measured |

---

## 12. Ethics

| Question | Position | Status |
|---|---|---|
| Does the user study involve human participants? | Yes (runners complete a questionnaire and enter health-adjacent data such as injury notes). Expert raters are no longer part of the study — expert evaluation was removed (2 October 2026) | Yes |
| Is ethics committee / IRB review required? | Not assumed either way. It must be determined from BINUS (and, if applicable, national) requirements, including whether the study may qualify for an exemption — which only the committee can decide | [CHECK BINUS REQUIREMENTS] |
| Informed consent | Required in the design: participants and experts are told purpose, data collected, voluntariness, withdrawal, contacts. The application has no consent flow | [NOT IMPLEMENTED] [CHECK BINUS REQUIREMENTS] |
| Participant information sheet | Required; in the participants' language | To write |
| Data protection | Minimize PII; anonymous codes; separate consent store; secure storage; retention and deletion policy; Indonesian personal data protection law and institutional policy to be checked (this document gives no legal advice) | [CHECK BINUS REQUIREMENTS] |
| Minors | Exclude unless explicitly approved | [CHECK BINUS REQUIREMENTS] |
| Health risk | Plans are not followed as part of the study and are not medical advice; disclaimer shown; no clinical claims | Proposed |
| Third-party data processing | Profiles (incl. injury text) are sent to external LLM APIs (Google, OpenAI) → disclose in the information sheet; consider excluding free-text injury details from user-study prompts or using vignettes | [ADVISOR DECISION REQUIRED] [CHECK BINUS REQUIREMENTS] |
| ~~Experts~~ | `SUPERSEDED` — expert evaluation removed from the study; no expert raters | n/a |
| Use of development data | Existing database rows are test data, not participant data | Do not use |

---

## 13. Reproducibility

Store, for every experiment run and every analysis:

| Item | How |
|---|---|
| Code commit hash | `git rev-parse HEAD` at run time; require a clean working tree; tag the freeze commit (e.g., `method-lock-v1`) |
| Environment | Python version, `pip freeze`, OS; frontend not needed for RQ2 |
| Model name/version | Identifier requested and identifier/version returned by the API; provider and endpoint |
| Prompt version | Version tag + SHA-256 of the exact rendered system and user prompts [NOT IMPLEMENTED] |
| Generation parameters | Temperature, token limit, JSON mode, timeouts, any defaults |
| Experiment date/time | UTC start and end; per-call timestamps |
| Runner profiles | Stimulus profile files (versioned) |
| Deterministic baseline | Baseline JSON and hash per profile; rule-engine commit |
| Raw LLM output | Verbatim response bodies, unmodified |
| Validation result | Validator verdict, failure category, message, deviations |
| ~~Expert scores~~ | `SUPERSEDED` — not collected; expert evaluation removed from the study |
| Questionnaire data | Raw responses, questionnaire version, consent version, plan/condition mapping |
| Analysis script | Versioned script(s) that read the raw data and produce every table and figure; fixed random seeds where used |
| Data integrity | File checksums; read-only archive of raw data |
| Protocol record | This locked document with approval date and any later amendments listed with reasons; consider preregistration [ADVISOR DECISION REQUIRED] |
| Deviations log | Any departure from protocol recorded and reported |

Operational rule: **freeze order** = (1) approve protocol; (2) decide rule-engine fixes (T7); (3) finalize prompt P1; (4) tag commit; (5) generate baselines; (6) run experiment; (7) rate; (8) analyze. No edits to code, prompt, rubric or analysis plan after step 4 without a documented amendment.

---

## 14. Final methodology gate

| Item | Status | Reason / next action |
|---|---|---|
| [x] RQ approved | **RESOLVED (2 October 2026, Gemini-only): RQ2 wording LOCKED** (Section 2) | RQ1/RQ3 largely unchanged (RQ1 wording updated to "Gemini-based"); experiment itself still needed |
| [x] Number of LLMs | **RESOLVED (2 October 2026, Gemini-only): 1 (Gemini)** — supersedes the same-day earlier resolution of 2 | — |
| [ ] Specific LLM identities selected | ADVISOR DECISION REQUIRED | Defaults in code are placeholders; versions and availability to be checked |
| [ ] Experiment protocol approved | ADVISOR DECISION REQUIRED | Sections 4 and 13; harness not implemented |
| [ ] Evaluation rubric approved | OPEN | Section 5 automated-criteria rubric; count not final |
| [x] Expert evaluation | **RESOLVED (2 October 2026): excluded entirely from the study** | Section 6 |
| [ ] Questionnaire finalized | OPEN | Items are study-specific drafts; wording not final |
| [ ] Questionnaire reviewed/piloted | EXPERIMENT REQUIRED | Steps 3–5 of Section 8 |
| [ ] Participant criteria finalized | ADVISOR DECISION REQUIRED | Section 7.3; minors; vignette vs own profile |
| [ ] Ethics requirements checked | OPEN | [CHECK BINUS REQUIREMENTS]; consent flow not implemented |
| [ ] Data schema finalized | OPEN | Section 9 proposed; research tables not implemented |
| [ ] Analysis method finalized | ADVISOR DECISION REQUIRED | Section 10; sample-size approach and inferential tests undecided |
| [ ] Reproducibility procedure finalized | OPEN | Section 13 proposed; prompt versioning and harness not implemented |

Additional readiness items:
| Item | Status |
|---|---|
| Technical validation T1–T14 run on the frozen commit | READY for T7, T12–T14 (201 tests passing, including the new T7 regression suite); OPEN for the gaps listed in Section 3.2 |
| Rule-engine design decisions (post-cutback rebound, taper anchoring, unused profile variables) | **RESOLVED** — rebound fixed in code; taper anchoring confirmed correct and left unchanged; `easy_run_pace` confirmed excluded from E6/E7. Remaining step: generate/freeze the 24 baseline plans against the fixed rule-engine version (not yet done) |
| Evaluation UI fixes (neutral defaults, blinding, participant code, 16 items) | OPEN |
| Search protocol for the gap statement | OPEN |
| Pending reference checks (`PAPER_GAPS.md` §4) | OPEN |

Summary count of the 12 gate items: READY 0, OPEN 5, ADVISOR DECISION REQUIRED 6, EXPERIMENT REQUIRED 1 (2 items now RESOLVED per the 2 October 2026 update). **No data collection should begin until the gate items are READY or explicitly waived by the advisor.**

---

## Advisor Decision Update — 2 October 2026 — `SUPERSEDED` (2-LLM design; kept for audit trail only)

~~- **2 LLM design approved:** RQ2 compares exactly LLM A vs LLM B (Sections 2, 4.1, 4.2, 14). Any earlier reference to "3 LLMs" is superseded.~~
~~- **3 repetitions approved:** 3 repetitions per (runner profile × LLM) combination; repetitions are replicates, not additional independent runners; the runner profile remains the sampling/block unit (Section 4.3).~~
- **Expert evaluation excluded from the study design:** no coach/expert rating, expert rubric, inter-rater agreement, expert recruitment, or blinded expert assessment (Sections 5, 6, 9.5, 10.2, 11, 12, 13, 14). RQ2 now relies solely on automated/objective evaluation criteria. *(Not superseded — still current.)*
- ~~Not resolved by this update (preserved): specific LLM identities; the 24-profile count…~~ — see the next section for current status.

## Advisor Decision Update — 2 October 2026 (Gemini-only design)

**This is the current, authoritative design, superseding the 2-LLM design recorded in the update above (issued earlier the same day).**

- **1 LLM (Gemini) CONFIRMED** (Sections 2, 4.1, 4.2, 14). Any earlier reference to "2 LLMs" or "3 LLMs" is superseded.
- **24 runner profiles CONFIRMED** (Section 4.3) — previously undecided.
- **3 Gemini repetitions per profile CONFIRMED → 72 Gemini generations** (Section 4.3); **24 baseline plans, generated once per profile, NOT repeated.**
- **Exactly 8 automated criteria LOCKED** (Section 5); exact operational definitions remain an OPEN SUB-DECISION, explicitly flagged — this section's own list, the (superseded) comparative proposal's 16-item draft, and the paper's Table IV 5-criterion list are not reconciled by this update.
- **Multi-week scope CONFIRMED** (Section 4.1), resolving the former OPEN METHODOLOGICAL DECISION. Pipeline: Runner Profile → Validation → Physiological Calculation → Deterministic Rule-Based Multi-Week Baseline → Gemini Personalization → Server-Side Validation → Gemini-Personalized Multi-Week Plan → Automated Evaluation → Baseline vs Gemini Comparison.
- **Expert evaluation excluded from the study design** (unchanged, Sections 5, 6, 9.5, 10.2, 11, 12, 13, 14).
- **No ranking/winner framing:** RQ2 reports per-criterion differences between Gemini and the baseline; no composite score, no "best," no "winner."
- **Not resolved by this update** (still open/unresolved): exact Gemini model/version identity; the exact automated-criteria definitions (Section 5; must be reconciled with the comparative proposal's superseded 16 and the paper's Table IV 5); the exact statistical test (Section 10.2 — candidates PROPOSED only, must account for 72 Gemini outputs nested within 24 profiles); prompt-delivery/Gemini-configuration details; baseline rule-engine issues (T7); RQ3 design details; ethics/BINUS requirements.

---

## STATUS SUMMARY

**CONFIRMED:** 24 runner profiles; Gemini as the only LLM; 3 Gemini repetitions per profile; 24 baseline plans; 72 Gemini generations; no expert evaluation; exactly 8 automated criteria (count locked); multi-week personalization; baseline vs Gemini comparison.

**OPEN:** exact Gemini model/version; exact 8-criteria definitions/thresholds (explicit conflict between this document's own list, the superseded comparative proposal's 16, and the paper's Table IV 5 — not resolved here); statistical test; RQ3 sample size; ethics/BINUS requirements; questionnaire validation/pilot; prompt implementation/reproducibility details.
