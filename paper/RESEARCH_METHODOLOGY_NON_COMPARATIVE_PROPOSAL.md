STATUS: PROPOSED — NOT YET APPROVED BY ADVISOR
Research focus: System Design and Evaluation
LLM comparison: NOT PART OF THE RESEARCH OBJECTIVE

# RESEARCH METHODOLOGY — NON-COMPARATIVE PROPOSAL

**Purpose.** Redesign of the methodology after the researcher's decision **not** to compare LLMs (no Gemini-vs-OpenAI comparison, no model ranking, no model "winner", no composite score for choosing a model). The research evaluates the **proposed hybrid running-training recommendation system and the plans it generates**, not which LLM is better.

**What this file is.** A proposal for advisor review. It supersedes the LLM-comparison parts of `RESEARCH_METHODOLOGY_LOCK.md`, `RESEARCH_READINESS_AUDIT.md` and `ADVISOR_REVIEW_PACKAGE.md` only once the advisor approves it. Nothing here is approved. No code, paper, data or experiment was touched or produced. Every open choice is marked `[ADVISOR DECISION REQUIRED]` (or `[CHECK BINUS REQUIREMENTS]`).

**Evidence base:** the documents listed above plus `PAPER_DRAFT.md`, `PAPER_GAPS.md`, `EVIDENCE_MAP.md`, `QUESTIONNAIRE_TRACEABILITY.md`, the phase design/report documents, and the repository code (HEAD `224d910`; 194 tests passed in the last audit run). Reference numbers [n] follow the current manuscript.

---

## 1. New research direction

The research title ("Design and Evaluation of an AI-Based Personalized Running Training Recommendation System") is read as three linked parts: **design** of the hybrid system (RQ1), **evaluation of the recommendations it produces** (RQ2), and **evaluation by users** (RQ3).

### 1.1 Proposed research questions

| | Proposed wording | Relation to existing wording |
|---|---|---|
| **RQ1 — System design** | **Keep existing wording:** "How can a hybrid AI-based system generate personalized multi-week running training plans by combining deterministic training constraints with LLM-based personalization?" | The alternative you proposed ("…combine deterministic running-training constraints with LLM-based personalization to generate personalized multi-week running training plans?") has the same meaning. There is no methodological reason to change the wording, and the existing text is already used in the manuscript, the lock, the audit and the advisor package. Choosing between the two is `[ADVISOR DECISION REQUIRED]` (final RQ wording). |
| **RQ2 — System/recommendation evaluation** | "To what extent does the proposed system generate personalized running training plans that satisfy predefined training constraints and personalization requirements?" | **Replaces** the old LLM-comparison RQ2. Two terms must be defined before the RQ is answerable: *predefined training constraints* (Section 5) and *personalization requirements* (Section 5.3). No acceptability threshold is invented (Section 5.6). |
| **RQ3 — User evaluation** | **Keep existing wording:** "How do users perceive the generated training plans in terms of personalization, usefulness, clarity, and confidence?" | Identical in meaning to your proposed direction (it was already the working RQ3). Kept because it names the four constructs measured and matches the manuscript. |

### 1.2 What is evaluated
- **Evaluated:** the generated personalized training plan produced by the proposed hybrid system — the output of the *whole pipeline* (Week 1 personalized text from the LLM, Weeks 2+ from the rule engine, after server-side validation and, if triggered, deterministic fallback).
- **Not evaluated:** the superiority of one LLM over another; athletic-performance improvement; injury prevention; clinical validity; longitudinal adherence. The study has no longitudinal performance intervention, so **no performance claim can be made**.

### 1.3 Title consistency
With this direction the methodology maps directly onto the title (design → RQ1, evaluation of recommendations → RQ2, user evaluation → RQ3). The earlier methodology had a model-comparison arm that the title does not mention.

---

## 2. Role of the LLM

The LLM is a **component of the system**, not the independent variable and not a research question.

```
Runner Profile → Validation → Physiological Calculation → Deterministic Rule-Based Baseline
   → LLM Personalization → Server-Side Validation → Final Personalized Training Plan → Evaluation
```

| Stage | Role |
|---|---|
| Validation | Rejects malformed profiles |
| Physiological calculation | VDOT from the 5K personal best; pace zones; target pace; feasibility class |
| Deterministic baseline | Weekly volumes, workout types, distances, paces, days (all weeks) from engineering design constraints |
| LLM personalization | Rewrites explanatory text for Week 1 (warm-up, execution cues, injury-related notes, rationale) from the profile and the baseline |
| Server-side validation | Guardrail: rejects output that changes workout type, distance, pace, intensity zone, weekly mileage, day set, or training/rest-day counts; deterministic fallback on failure |
| Evaluation | Evidence about the final plan (Sections 5–10) |

- The deterministic engine handles physiological/training logic; the LLM handles personalization and natural-language generation and **may not freely change the calculations**; the validator provides guardrails (numbers and structure only — it does not check the safety or accuracy of free text); the **final output evaluated is the result of the whole pipeline**.
- **Consequence for interpretation:** the study cannot attribute any finding to "the LLM" as opposed to the rest of the pipeline, and cannot say whether the LLM adds value over the rule-only output unless an approved reference condition is used (Section 11).

---

## 3. LLM model selection

- Model selection is an **implementation detail / experimental configuration**, **not a research question**. No LLM comparison, number of LLMs, repetitions per LLM, ranking, or winner is part of this methodology.
- The model actually used must be reported in the study (provider, requested identifier, returned version if the API provides it, access date, generation settings, prompt version).
- **LLM implementation choice: `[ADVISOR DECISION REQUIRED]`.** The code supports Gemini and OpenAI; its defaults (`gemini-1.5-flash`, `gpt-4o-mini`, temperature 0.4) are placeholders whose availability must be verified. If one model is used, the experiment evaluates the system **under that configuration only**; results are not claimed to hold for other models.
- Implementation note (observation only, no change made): the dispatcher's default `auto` mode tries Gemini then OpenAI and falls back silently; a single configured provider avoids ambiguity about which model produced a given plan. Whether to fix the provider to one is part of the advisor's configuration decision.
- If the chosen model is retired or changes during the study, the evaluation must be re-run or the limitation reported (alias drift, Section 12).

---

## 4. Old comparison infrastructure — what is removed or reframed

Tags: **REMOVE FROM METHODOLOGY**, **REFRAME** (kept in a different form), **KEEP**. No file or code is deleted; only the methodology is redesigned.

| Old component (source) | Disposition | New form |
|---|---|---|
| Independent variable = LLM/model (Lock §4.1; Audit §3.1) | **REMOVE FROM METHODOLOGY** | There is no independent variable manipulation in RQ2; the unit of analysis is a (runner profile → final plan) record |
| "Controlled comparison": same profile across several models (Lock §4.1) | **REMOVE FROM METHODOLOGY** | Profiles are inputs to the one configured system |
| Candidate models table (Lock §4.2) | **REFRAME** | A single documented LLM configuration `[ADVISOR DECISION REQUIRED]` |
| Repetitions per (profile, model) (Lock §4.3) | **REFRAME** | Repeated generation per profile is optional, only to characterize how stable the pipeline's output (validator pass, fallback occurrence, text content) is; count `[ADVISOR DECISION REQUIRED]`; not a model comparison |
| Interleaved call order across models; one time window to limit cross-model drift (Lock §4.3) | **REMOVE FROM METHODOLOGY** | Record dates and the model version; keep runs reasonably contiguous |
| Prompt-delivery parity between Gemini and OpenAI (Audit §2/§3.4, Package §10 #1) | **REMOVE FROM METHODOLOGY** as a confounder | Not relevant with one provider; the actual delivery method is documented as part of the configuration |
| Different JSON modes/safety filters between providers; output-length (verbosity) differences between models (Audit §3.4) | **REMOVE FROM METHODOLOGY** | Document the single provider's settings |
| Model ranking, winner/loser, per-model comparative tables, cross-model reproducibility (Lock §10.2) | **REMOVE FROM METHODOLOGY** | Not used |
| Comparative statistical analysis and multiplicity policy across models (Lock §10.2) | **REMOVE FROM METHODOLOGY** | Descriptive analysis of the single system (Section 9) |
| Composite score / weighting to choose a model (Lock §5.2) | **REMOVE FROM METHODOLOGY** | No composite score; no weights |
| LLM-as-judge for model screening (Lock §5.3) | **REMOVE FROM METHODOLOGY** (as a model-ranking tool) | If used at all it would be a secondary text-screening aid, `[ADVISOR DECISION REQUIRED]`; not needed by this design |
| Blinding of model labels for experts (Lock §6) | **REMOVE FROM METHODOLOGY** | Blinding only matters if the advisor adopts a reference condition (Section 11) |
| Control conditions C0/C1 (Lock §4.5) | **REFRAME** | Becomes the baseline/reference-plan role decision (Section 11) |
| Rubric criteria 2–4 as "consistency across models" (Lock §5) | **REFRAME** | Constraint compliance of the final plan (Section 5.1) |
| Progression consistency from Week 1 (Lock §5, criterion 5; Audit §4) | **REFRAME** | Evaluated on the full multi-week plan against the rule specification, not as an LLM property (Section 6) |
| Rubric 7 (personalization quality) | **KEEP** | Becomes expert/profile-alignment evidence (Sections 5.3, 8) |
| Rubric 8 (reliability/efficiency) | **REFRAME** | Fallback rate, validator pass rate, errors, latency of the configured system; not compared across models |
| Stimulus profile set (Lock §4.4) | **KEEP** | Coverage of the system's input space; size `[ADVISOR DECISION REQUIRED]` |
| Experiment harness for evidence recording (Lock §4.6; Audit §2) | **KEEP, reduced** | Still needed to store raw output, validator verdicts, errors, run metadata; the multi-model parameterization is no longer required |
| Model-version drift, prompt sensitivity, API variability, researcher bias, expert subjectivity (Lock §11) | **KEEP** | Still apply to a single configuration |
| Gate item "LLM models selected"; "controlled LLM comparison" (Lock §14) | **REFRAME** | "LLM configuration documented"; "controlled evaluation of generated personalized training plans" (Section 13) |

---

## 5. RQ2 — system/recommendation evaluation design

### 5.1 Evaluation dimensions (conceptual; no weights, no composite)

**A. Constraint Compliance** — does the generated plan satisfy the predefined deterministic training constraints?
Candidate constraints (all drawn from the implemented design; they are **engineering design constraints used in the proposed system**, not scientific thresholds — see `PAPER_GAPS.md` §5b): valid training-day count and Mon–Sun structure; rest days; workout type; intensity zone; pace target within the computed zone; long-run constraint (30% share, caps, floor); weekly-mileage progression; cutback weeks; taper; structured-output requirements (schema, required fields).

**B. Profile/Goal Alignment** — does the plan fit the runner's ability, goal, available frequency, baseline performance, training history and other profile inputs *that the system actually uses*? Inputs used numerically: experience level, 5K personal best, target race distance and time, current weekly mileage, training days and preferred days, plan duration. Used only in text/explainability: age, gender, 10K personal best, easy-run pace; injury note affects text only.

**C. Personalization** — does the output actually use the runner's profile information rather than being a generic running plan? (Definition of "personalization requirements" in 5.3.)

**D. Training-plan Quality** — expert judgment of appropriateness, internal consistency, structure, progression, practicality (Section 8). No weights or composite.

**E. Clarity / Explainability** — can workout instructions and the rationale be understood? Two *different* evidence types are kept separate:
| | Objective/expert evaluation (RQ2) | Subjective/user evaluation (RQ3, construct PC) |
|---|---|---|
| Who judges | Domain experts and/or rule checks | Runners who receive the plan |
| Question | Is the explanation accurate, internally consistent with the plan, and understandable in principle? | Do I (the runner) find it easy to understand? |
| Can disagree? | Yes: a plan may be technically clear to experts but not to novices, or the reverse | — |
| Reporting | Separately; never merged into one clarity score | Separately |

### 5.2 Unit of evaluation
One record = (runner profile, final plan produced by the configured pipeline, path flag). The path flag records whether Week 1 text came from a validated LLM output or from the deterministic fallback. Handling of fallback plans in the evaluation (excluded, analysed separately, or counted as a system outcome) is `[ADVISOR DECISION REQUIRED]`; the fallback rate is itself a system-reliability measure.

### 5.3 Defining "personalization requirements" `[ADVISOR DECISION REQUIRED]`
Candidate definitions, from most to least objective:
1. *Profile sensitivity (objective):* plans for profiles that differ in one used input differ in the expected plan fields (numbers by construction; text by inspection).
2. *Profile-fact use in text (objective, requires an extraction rule):* the text states the runner's goal race/time, training days, experience-appropriate content and the reported injury correctly.
3. *Non-genericness (needs a reference):* the text is more specific to the profile than a generic plan. Claims of this kind need a defined reference text; whether to introduce one is part of the baseline/reference-plan decision (Section 11).
4. *Expert judgment of personalization (subjective).*

Because age, gender, 10K personal best and easy-run pace do not change any number, personalization must be defined relative to what the system uses; this limitation must be stated.

### 5.4 Evidence sources
1. **Automated validator** (existing `validate_ai_plan`: schema and the checks in manuscript Table III).
2. **Deterministic rule checks** (independent oracle code that recomputes the specification for every week — to be written only after the baseline decision, Section 12).
3. **Expert evaluation** (Section 8), if the advisor approves it.
4. **Structured output inspection** (field completeness; numbers quoted in text vs plan; profile-fact mentions).

### 5.5 Evaluation protocol (conceptual)

```
Runner profile → deterministic baseline → LLM personalization → server-side validation
   → evaluation criteria → recorded evidence
```

1. Fix the protocol, the baseline version, the prompt version and the LLM configuration before generating any evaluation plan.
2. Prepare the stimulus profiles (vignettes) `[ADVISOR DECISION REQUIRED: number and composition]`.
3. Run the pipeline once per profile (or repeatedly if approved), recording the full evidence set (Section 10).
4. Apply automated and deterministic checks to every record.
5. If approved, present final plans to experts for rating (Section 8).
6. Report descriptive results per criterion and per evidence type; keep compliance and quality separate.

### 5.6 Reporting rule
"To what extent" is answered descriptively (proportions of plans meeting each criterion, violation categories, expert rating distributions). **No acceptability threshold is invented**; any threshold such as a required compliance rate is `[ADVISOR DECISION REQUIRED]`.

---

## 6. Automated evaluation — what can be tested objectively

### 6.1 Objective compliance (machine-checkable)
| Check | What is tested | Existing validator? | Notes |
|---|---|---|---|
| Schema validity | JSON parses to `AIPersonalizedPlan` | Yes | |
| Required fields / completeness | Text fields present **and non-empty** | **Partly** (schema accepts empty strings, so empty text passes the validator) | Needs a separate completeness check |
| Workout-day validity | 7 days Mon–Sun, no unknown/duplicate days | Yes (Week 1) | Rule checks needed for every week |
| Rest-day validity | Rest days = 7 − training days | Yes (Week 1) | |
| Workout type | Type equals baseline; type belongs to the allowed set | Equality: yes | Allowed-set check not present |
| Intensity zone | Zone string equals baseline; zone suits workout type | Equality: yes | Suitability rule not present |
| Pace consistency | `pace_target` equals zone table; paces quoted in text match | Equality: yes | Text-number extraction rule undefined |
| Weekly volume | Weekly mileage and distances equal baseline; distances sum to weekly mileage | Equality: yes; sum: no | Tolerances 0.05 km/0.15 km |
| Progression | Week-to-week volumes follow the specified progression | No | Rule-engine decision RESOLVED (rebound fixed); still no check in the production validator itself |
| Cutback | Cutback weeks follow the specification | No | Same resolution; same validator gap |
| Taper | Taper weeks follow the specification | No | Taper confirmed correct as-is; still no check in the production validator itself |
| Long-run constraint | Long run ≤ min(30% of weekly volume, race-distance cap) with floor | No | Floors can make realized shares exceed 30% at low volume |
| Profile consistency | Text does not contradict goal, time, days, injury note | No | Extraction rule undefined |

### 6.2 What these checks mean — and do not mean
- **Objective compliance** shows conformance to the system's *own specification* (and to the numerical values the validator copies from the baseline). Because the validator forces Week 1 numbers to equal the baseline, numeric compliance of Week 1 is largely **by construction**; the informative cases are (a) how often LLM output is rejected, (b) the text content the validator does not examine, and (c) the multi-week rules that no LLM touches.
- **Subjective quality** (appropriateness, practicality, safety of advice, clarity for people) requires judgment and cannot be inferred from compliance.
- **Automated compliance is not evidence that a plan is physiologically optimal, safe, or effective.** The constraints are engineering design constraints; the criteria are derived from the system's own rules (circularity, Section 12).
- **RESOLVED:** the two rule-engine issues referenced below (Section 12) have been decided — the post-cutback rebound is fixed in code, and the taper's starting-mileage anchoring is confirmed correct and unchanged. Progression, cutback and taper checks can now be built against a settled rule: a criterion "≤10% week-on-week increase" now also holds for the post-cutback week (the real step is ~6-8%, not the previously observed ~25%), so no special-case exclusion is needed for weeks following a cutback.

---

## 7. RQ2 evidence recording (retained requirement)

Evidence recording remains necessary even without model comparison, to make the evaluation auditable and reproducible. Still required (all currently **[NOT IMPLEMENTED]** per the readiness audit): run/evaluation ID, prompt version/hash, captured model version, raw LLM output, parsed output, validator verdict and failure category, error type/HTTP status, per-call timestamp, git commit, environment record. **No longer required:** model-as-parameter harness for multiple providers, cross-model call ordering, cross-model reproducibility records. The harness is not to be built before the protocol is approved.

---

## 8. Expert evaluation (if approved) `[ADVISOR DECISION REQUIRED]`

Whether expert evaluation is used at all is an advisor decision; automated and rule-based evidence alone cannot answer plan-quality questions.

- **Object rated:** the final personalized plan (profile + plan), not a model identity.
- **Candidate dimensions (no weights, no composite score):** personalization; training appropriateness; internal consistency; workout structure; progression; practicality; clarity. Methodological precedent for expert rating of plans on literature-derived criteria with a 5-point scale: [11] (ChatGPT running plans) and [12]; these precedents rated unconstrained LLM output, not a constrained hybrid pipeline, and the 22 criteria of [11] are not yet read in full.
- **Open decisions:** whether experts are used; inclusion criteria and qualifications; number of experts; recruitment; rating scale and anchors; rubric items; whether experts see the baseline numbers and the profile; whether they know the plan is AI-generated (disclosure may bias ratings); training/calibration; inter-rater reliability method if more than one expert; handling of disagreement; ethics treatment of experts as participants `[CHECK BINUS REQUIREMENTS]`.
- Not specified here: expert count, qualifications, weights, composite score.

---

## 9. Statistical analysis (no results implied)

- **RQ1:** pass/fail per technical criterion; counts of failed assertions.
- **RQ2:** descriptive only — proportion of plans meeting each compliance criterion; violation categories and counts; validator first-attempt pass rate; fallback rate; expert rating distributions and agreement if applicable; per-criterion reporting; **no composite score; no model comparison; no significance testing promised.** Whether any inferential analysis is justified depends on the design and sample `[ADVISOR DECISION REQUIRED]`.
- **RQ3:** item- and construct-level descriptive statistics, response distributions; Cronbach's alpha only if appropriate and with enough respondents; comparisons between plan types only if the advisor adopts a reference condition (Section 11) and then with a design-appropriate ordinal analysis.

---

## 10. Conceptual data to record (no schema/code)

| For | Data to record |
|---|---|
| **RQ1** | Freeze commit; environment; criteria list with oracle version; test outcomes and timestamps; fixture profiles and baseline hashes; limitations and open decisions at run time |
| **RQ2** | Protocol version; stimulus profiles and rationale; baseline JSON and hash; prompt version/hash (rendered system and user prompts); LLM configuration (provider, requested/returned identifier, access date, parameters); per-run record (ID, profile, repetition if any, timestamp, latency, HTTP status, error type, raw response, parsed output, truncation flag); validator verdict/category/message/deviations; path flag (LLM vs fallback); automatic rule-check results; text-completeness and number-consistency results; expert materials, rater registry (pseudonymous), rubric version, ratings, comments (if experts are used) |
| **RQ3** | Participant code; consent record and version (separate store); eligibility; minimal profile inputs; plan exposure record (plan ID, condition, order, LLM configuration, path flag); questionnaire version; item responses; comments; withdrawal flag; validation-process records (kept separate) |

Privacy: no names/emails in research tables; consent separate; free-text injury notes sensitive; development database rows are test data and must not be mixed with study data.

---

## 11. Baseline vs personalized plan — role of the baseline `[ADVISOR DECISION REQUIRED]`

The earlier concern was that the rule-based baseline contains little descriptive text while the AI plan adds warm-up, execution and explanation. With no LLM comparison the question becomes: **is a baseline/reference plan needed as a reference condition at all?**

| Option | Description | What it allows | What it costs / risks |
|---|---|---|---|
| **A. Internal pipeline stage only (not a comparator)** | RQ2 and RQ3 evaluate only the final personalized plan; the baseline is the deterministic input to the LLM stage | Evaluates constraint compliance, alignment and perceptions of the system's output without a confound from text amount; simplest | No claim that the LLM stage or the pipeline adds anything over rule-only output; "personalization" judged against requirements, not against a reference |
| **B. Baseline as reference condition** | Add the rule-only plan (and possibly the template-fallback plan) as a comparison in RQ2 expert rating and/or RQ3 | Allows relative statements (e.g., perceived clarity/personalization of personalized vs. rule-only output) | Text-richness confound (more text by design); requires a within/between design, blinding and comparative analysis; template-fallback control needed to separate "text" from "LLM text"; larger sample needs |
| **C. Reference only for RQ3** | Use a reference only in the user study, not in RQ2 | Perception comparison without expert burden | Same confound as B for RQ3 |

- The choice must **not** be made automatically. If Option A is chosen, the baseline is *not* an experimental control and must not be described as one in the paper.
- The current research mode of the application shows both plans and collects ratings per plan type; Option A would use only the AI-personalized plan type. No change has been made.

---

## 12. Rule-engine issues and their effect on system evaluation — RESOLVED

| Issue | Prior behavior (historical) | Current behavior (post-fix) | Is Week 1 / the LLM affected? |
|---|---|---|---|
| **25% post-cutback rebound** | After a cutback week (0.85 × running volume) the running volume was not reset, so the next build week was ≈ +25% above the cutback week; e.g., 25.3 → 31.6 km | **FIXED**: the cutback week's own reduced volume is now carried forward as the progression reference, so the next build week is ≈ +6-8% above the cutback week, e.g., 25.3 → 26.8 km. The "weekly mileage progression" and "cutback" criteria can now be defined unambiguously: a ≤10%-week-on-week criterion now also holds across a cutback. Verified by `backend/tests/test_t7_progression_fix.py` | No (Week 1 is never a cutback or its successor) |
| **Taper tied to starting mileage** | Second-to-last week 0.85 ×, last week 0.55 × the starting mileage, not the peak; e.g., 33.5 → 21.2 → 13.8 km (8 weeks), 47.5 → 21.2 → 13.8 km (16 weeks); code comment said "~75% of peak" | **CONFIRMED CORRECT, unchanged** — this anchoring matches `PAPER_DRAFT.md` Table II ("times the base (starting) mileage"); the relative taper size still depends on how far the build climbed, which is the intended, accepted design, not an ambiguity to resolve. Only the inline code comment was corrected | No |

Also observed (not decided): Week 1 volume is current × 1.06/1.08 while the explainability text says it "matches current capacity"; minimum floors can make realized volume differ from target; age, gender, 10K PB and easy pace do not influence any number (`easy_run_pace` separately confirmed excluded from E6/E7).

**Advisor question — RESOLVED:** *Should these rules be corrected before the deterministic baseline is frozen, or documented as engineering limitations?*
- Rebound: **corrected**. The rule-engine fix changes newly generated plans for durations ≥ 8 weeks; no plans for the 24-profile experiment have been generated yet, so nothing stored needs to change.
- Taper: **documented as the intended design**, not corrected — it was already consistent with the published methodology; only the misleading comment was fixed.
- The baseline must still be frozen (commit tagged, 24 profiles generated and stored) before any evaluation plan is generated — that step has not yet happened and is unaffected by this resolution beyond now using the fixed rule-engine version. Because Week 1 is the only LLM-personalized week, these issues affected RQ2 only through the *multi-week deterministic* criteria (E4) and RQ3 if participants see the whole plan — both now unblocked on this specific point.

---

## 13. RQ3 — user evaluation

- **Unchanged focus:** perceived personalization (PP), perceived usefulness (PU), perceived clarity (PC), recommendation confidence (RC).
- **The questionnaire is study-specific and currently unvalidated.** No item is adapted from a validated scale; content review and pilot testing are required as the advisor decides; it must not be called a validated instrument (`QUESTIONNAIRE_TRACEABILITY.md`). Known item issues (PC4 double-barrelled, PP4/PC3 wording, mildly leading items, overlaps, scale-anchor mismatch with the application) remain.
- **Study design, sample size and recruitment are not chosen here** `[ADVISOR DECISION REQUIRED]`. Which design is meaningful depends on the Section 11 decision (single plan type descriptive study vs. a reference condition).
- **Objective vs subjective clarity:** PC is the runners' perception; the expert/rule evidence on explanation quality in RQ2 is separate (Section 5.1 E).
- Adults only (proposal); the application currently accepts ages 12–99 `[CHECK BINUS REQUIREMENTS]`.
- Privacy/disclosure: if participants' own profiles (including injury text) are used, they are sent to the configured external LLM provider; this must be disclosed `[CHECK BINUS REQUIREMENTS]`.

---

## 14. Revised methodology gates

Status vocabulary: READY / OPEN / ADVISOR DECISION REQUIRED / EXPERIMENT REQUIRED. "Ready" is claimed only where the evidence already exists.

| Gate | Status | Notes / dependency |
|---|---|---|
| RQ wording approved (RQ1–RQ3) | ADVISOR DECISION REQUIRED | Section 1.1 |
| LLM configuration documented (model, version, parameters; not a comparison) | ADVISOR DECISION REQUIRED | Section 3 |
| RQ1 technical validation (T1–T14) | OPEN | From the readiness audit: 2 criteria fully covered, 9 partial, 2 not ready, 1 awaiting a decision; **not complete**; T7 depends on the baseline decision |
| Baseline freeze (rule-engine fix vs document) | ADVISOR DECISION REQUIRED | Section 12; precedes any evaluation generation |
| RQ2 system-evaluation protocol approved | ADVISOR DECISION REQUIRED | Sections 5–7 |
| RQ2 evaluation criteria and definitions (incl. "personalization requirements") | OPEN | Sections 5.1, 5.3, 6; no thresholds, weights or composite |
| Automated vs expert evaluation; expert evaluation if approved | ADVISOR DECISION REQUIRED | Section 8 |
| Baseline/reference-plan role | ADVISOR DECISION REQUIRED | Section 11 |
| Stimulus profile set (and optional repeated runs) | ADVISOR DECISION REQUIRED | Number/composition not chosen |
| Evidence-recording infrastructure | OPEN | Section 7; not implemented; build after approval |
| RQ3 user-evaluation design, sample-size approach, recruitment | ADVISOR DECISION REQUIRED | Section 13 |
| Questionnaire validation/content review/pilot | EXPERIMENT REQUIRED | Not started; process as approved |
| Evaluation application readiness (16 items, neutral defaults, participant code, consent screen) | OPEN | Depends on questionnaire and design decisions |
| Ethics/BINUS requirements and data privacy | ADVISOR DECISION REQUIRED | `[CHECK BINUS REQUIREMENTS]`; external API disclosure |
| Reproducibility procedure (commit, prompt, model version, parameters, raw outputs, verdicts, analysis scripts) | OPEN | Section 10; not implemented |
| Analysis plan | ADVISOR DECISION REQUIRED | Section 9 |

No gate is currently READY for starting evaluation or data collection.

---

## 15. Advisor decisions required (updated list)

None of these asks which LLM is better.

| # | Decision |
|---|---|
| 1 | Final RQ wording (keep existing RQ1/RQ3; adopt the new RQ2; accept the alternative RQ1 phrasing or not) |
| 2 | LLM implementation choice for the study configuration (one model; version pinning; parameters) — an implementation detail, not a research question |
| 3 | RQ2 evaluation criteria: which of A–E are used; definition of "predefined training constraints" and "personalization requirements"; whether any acceptability threshold is needed |
| 4 | Automated/rule-based evidence only, or also expert evaluation |
| 5 | If experts are used: inclusion criteria, number, rating procedure, reliability method, disclosure of AI authorship |
| 6 | Role of the baseline/reference plan (Option A, B or C) and whether a template-text control is used |
| 7 | Rule-engine issues: correct before the baseline freeze, or document as engineering limitations |
| 8 | RQ3 study design (and which plan(s) participants see) |
| 9 | Participant sample-size approach, pilot size, recruitment |
| 10 | Questionnaire validation process (content-review panel, pilot, possible adaptation from ResQue, response scale, "not applicable" option) |
| 11 | Ethics/research-review requirements, consent, withdrawal, retention, adult-only rule |
| 12 | Data privacy and disclosure of external LLM API transmission (use of own profiles/injury text vs vignettes) |
| 13 | Stimulus profile set (number/composition) and whether repeated generation per profile is used to characterize pipeline stability |
| 14 | Treatment of fallback plans in the evaluation (exclude, analyse separately, or count as a system outcome) |
| 15 | Scope of LLM personalization (Week 1 only, as implemented, or multi-week) and whether technical-validation criteria T1–T14 are sufficient evidence for RQ1 |

---

## 16. PAPER CHANGES REQUIRED AFTER METHODOLOGY APPROVAL

No paper change is made now. After approval, the following will need to be reconciled (location in `PAPER_DRAFT.md` → needed change):

| Location | Current content | Required change |
|---|---|---|
| Abstract | Mentions a controlled LLM comparison placeholder | Replace with the approved evaluation of generated plans; keep results placeholders |
| I, paragraph 3 (gap statement) | Gap includes "different LLMs are compared on the same runner profile and the same baseline plan" | Reformulate the gap around hybrid design + post-generation validation + system evaluation; drop the multi-LLM comparison element |
| I, RQ list and objectives | RQ2 = LLM comparison; objective "controlled comparison of LLMs" | New RQ2 wording; new objective |
| I, contributions (item 4) | "A methodology for comparing LLM personalization under the same runner profile and baseline plan" | Replace with a system-evaluation protocol contribution; keep conservative language |
| II-C, differences paragraph ("third, the planned RQ2 comparison varies the LLM…") | Contrasts RQ2 with the multi-LLM design of [12] | Remove/reframe; [12] remains as a related study |
| II-F (research gap) | "…will compare different LLMs using the same runner profile and the same deterministic baseline" | Remove the comparison; keep hybrid design, validation, system evaluation, user perception |
| III-A (research design) | Experiments: (2) "controlled LLM comparison (RQ2), if conducted"; also states technical validation is complete | Replace with system evaluation; correct the "complete" statement (T1–T14 only partly covered) |
| III-I (experimental design), Table IV | "LLM comparison (RQ2)", independent models, repetitions per model; Table IV "Planned LLM comparison criteria" (5 criteria) | Rewrite as RQ2 system-evaluation protocol; replace Table IV with the evaluation dimensions A–E and evidence sources; no weights |
| III-J, III-K | Plan-type comparison in analysis | Adjust to the approved RQ3 design and the baseline role |
| III-F | Describes provider options and defaults | Report the single LLM configuration used, as an implementation detail |
| IV (implementation) | Provider support | State that evaluation uses one configured provider |
| V-C heading "LLM Comparison" | Placeholder for model comparison | Rename and rewrite as "Evaluation of Generated Plans" (placeholders only until data exist) |
| V-E (discussion) and limitations | RQ2 discussed as model performance | Add limitations: single model/configuration; circularity of rule-derived criteria; compliance ≠ quality; LLM multi-week personalization implemented but not yet evaluated; baseline decision; fallback handling |
| VI (conclusion) and future work | "building an LLM comparison harness", RQ2 about model differences | Replace with evidence-recording infrastructure and system evaluation; optional future work: LLM comparison (as future work only) |
| Table V, constructs | Unchanged | Keep; confirm after questionnaire process |
| References | [12] used as multi-LLM precedent | Keep as related work; re-check wording |
| Supporting documents | Lock, readiness audit, advisor package, `PAPER_GAPS.md`, `EVIDENCE_MAP.md`, literature matrix | Update to the approved methodology (they still describe the comparison) |

---

## 17. Validity threats (updated for the non-comparative design)

| Threat | Description | Handling |
|---|---|---|
| Circularity | Compliance criteria are derived from the system's own rules, so "compliance" shows conformance to the specification, not scientific validity | State explicitly; add expert appropriateness judgment if approved |
| Construct validity | Compliance vs quality; "personalization" defined relative to used inputs; questionnaire unvalidated | Separate evidence types; define terms before data |
| Internal validity | Fallback plans may be mistaken for LLM output; expectation effects; non-neutral rating defaults; text-amount confound if a reference condition is used | Path flag; neutral defaults; Section 11 decision |
| External validity | One model/configuration; one prompt; vignette profiles or volunteers; LLM personalization over the full multi-week schedule as implemented (effectiveness not yet evaluated); three race distances | Limit claims to the evaluated configuration |
| Researcher bias | The researcher designed the system, rules, criteria and rubric and evaluates it | Fix protocol first; report all runs including failures; independent expert review if approved |
| Model-version drift | The single model may change or be retired | Pin identifier; record returned version and date |
| Prompt sensitivity | Results depend on the single frozen prompt | Freeze and report the prompt |
| API variability | Errors, timeouts, nondeterminism | Record statuses and fallback occurrences |
| Expert subjectivity | No consensus criteria; low agreement is possible | Calibration; report agreement |
| Questionnaire/sample limits | Self-report; small convenience sample | Descriptive claims only |
| Rule-engine limitations | Two known behaviors; constants are engineering design constraints | Section 12 |

---

## 18. Ethics

Ethics/research-review requirements have not yet been confirmed and should be checked with the supervisor/BINUS before participant recruitment or collection of health-adjacent information. Points to bring: adult participants (the application accepts ages 12–99); free-text injury notes; transmission of profile data to the external LLM provider; informed consent, information sheet, withdrawal, retention; experts as human participants; development database rows must not be reused. `[CHECK BINUS REQUIREMENTS]`

---

## 19. Do not do yet

Do not run any evaluation, recruit participants or collect responses; do not call the questionnaire validated; do not claim technical validation is complete; do not claim LLM or athletic-performance improvement; do not rank or compare LLMs; do not change the rule engine or freeze the baseline without the protocol decision; do not choose the final model, profile count, repetitions, expert count or sample size without the advisor; do not add weights or a composite score; do not modify the paper until the methodology is approved.

---

## 20. Summary of this proposal

- **Direction:** system design and evaluation; LLM comparison is not part of the research objective.
- **RQ1** (existing wording kept): system design. **RQ2** (new): to what extent the proposed system generates personalized plans that satisfy predefined constraints and personalization requirements. **RQ3** (existing wording kept): users' perceptions of personalization, usefulness, clarity and confidence.
- **Evaluated object:** the final plan from the whole pipeline; not model superiority, not performance.
- **Key methodological point:** compliance is partly by construction (the validator forces numerical identity with the baseline) and derived from the system's own rules, so it must be reported as conformance, not quality; quality requires expert judgment if approved.
- **Open for the advisor:** the items in Section 15, notably the LLM configuration, evaluation criteria and definitions, expert evaluation, the baseline's role, the rule-engine fix-or-document decision, the RQ3 design, ethics and data privacy.
