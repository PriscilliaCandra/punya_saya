**STATUS AS OF 2 OCTOBER 2026 (LATER SAME DAY): the "2 LLM" design (LLM A vs LLM B) below is `SUPERSEDED`.** The advisor's new FINAL LOCKED design is **1 LLM only (Gemini) vs the deterministic baseline**: 24 profiles CONFIRMED, 3 Gemini repetitions (72 generations) + 24 baseline plans (not repeated), exactly 8 automated criteria (definitions OPEN), multi-week scope CONFIRMED. See "Advisor Decision Update — 2 October 2026 (Gemini-only design)" at the end of this document and the STATUS SUMMARY that follows it. Everything below that references "LLM A vs LLM B" or a 2-LLM/3-LLM design is kept visible for audit-trail purposes only.

STATUS: PROPOSED — NOT YET APPROVED BY ADVISOR, except where marked APPROVED/CONFIRMED (see "Advisor Decision Update — 2 October 2026" at the end of this document, itself `SUPERSEDED` by the Gemini-only update that follows it): ~~2 LLMs (LLM A, LLM B); 3 repetitions per (runner profile × LLM)~~ — **superseded by: 1 LLM (Gemini); 3 Gemini repetitions per profile (72 generations); 24 baseline plans (not repeated); expert evaluation excluded from the study (unchanged).**

Research focus: System design and **comparative evaluation of multiple LLMs** as the personalization layer of a hybrid running-training recommender.
Supersedes: `RESEARCH_METHODOLOGY_NON_COMPARATIVE_PROPOSAL.md` (researcher decision reversed). Builds on `RESEARCH_METHODOLOGY_LOCK.md`, `RESEARCH_READINESS_AUDIT.md` and `ADVISOR_REVIEW_PACKAGE.md`; earlier findings are kept and re-evaluated, not dropped.
Constraints of this document: analysis and documentation only. No source code, database, paper, experiment or participant data was touched or produced. Every undecided choice is marked `[ADVISOR DECISION REQUIRED]`; literature that still has to be checked is marked `[LITERATURE VERIFICATION REQUIRED]`. Numbers proposed below (models, profiles, repetitions) are **starting proposals for discussion, not decisions**.
Reference numbers [n] follow the current manuscript (`PAPER_DRAFT.md`). Repository facts refer to commit `224d910`.

---

## 1. Research focus

The study evaluates how different LLMs behave **when used as the personalization stage of one fixed hybrid system**, given an identical runner profile and an identical deterministic baseline. It does **not** try to establish which LLM is the best AI model in general, and it makes no statement about athletic performance, injury prevention or clinical validity.

What the comparison asks is narrow: given the same inputs and the same task ("personalize this plan without changing the computed numbers and stay consistent with the profile"), how do the models differ in (a) complying with the constraints, (b) staying consistent with the profile, (c) the quality of the personalization they add, and (d) the stability of their behavior across repeated runs. Results apply only to the tested model versions, on the tested date, with the tested prompt, profiles and tasks.

Changes from the non-comparative proposal (summary): the LLM is again the independent variable; model selection, profile design, repeated runs, prompt standardization, multi-week evaluation, statistical design for repeated blocks and the confounder checklist are re-introduced and expanded; the baseline is a **controlled input and constraint source**, not a comparator, unless the advisor approves an additional condition.

---

## 2. Research title

English: "Design and Evaluation of an AI-Based Personalized Running Training Recommendation System" (the title used in the README and the manuscript).
Indonesian: "Perancangan dan Evaluasi Sistem Rekomendasi Latihan Lari Personal Berbasis AI" (Indonesian working title in the manuscript).
Consistency: the comparative evaluation sits inside "Evaluation"; the title does not need to change. The software's internal name ("AI Running Training Recommendation System (Academic Prototype)") is not the research title.

---

## 3. Research questions

### 3.1 Working wording (kept)
- **RQ1 (updated wording, Gemini-only design):** How can a hybrid AI-based system generate personalized multi-week running training plans by combining deterministic training constraints with Gemini-based personalization? (Previously worded generically as "LLM-based personalization"; reworded because the locked design uses a single named model, Gemini, not an unspecified/multiple-LLM component. The hybrid architecture itself — deterministic rules + physiological calculation + multi-week baseline + Gemini personalization + validation/guardrails — is otherwise unchanged.)
- **RQ2 — `SUPERSEDED` (2-LLM wording, audit trail only):** "How do different large language models, given the same runner profile and the same deterministic baseline plan, differ in personalizing the plan while remaining consistent with the runner profile and predefined training constraints?" RQ2 compared exactly **LLM A vs LLM B** using **automated/objective evaluation criteria only**; it must never conclude with an overall ranking, "best LLM," or "winner."
- **RQ2 — CURRENT (Gemini-only, LOCKED):** "How does Gemini-based personalization differ from a deterministic baseline in generating personalized multi-week running training plans while maintaining predefined training constraints?" (Indonesian: "Bagaimana personalisasi berbasis Gemini berbeda dari deterministic baseline dalam menghasilkan rencana latihan lari multi-minggu yang dipersonalisasi dengan tetap mempertahankan constraint latihan yang telah ditentukan?"). RQ2 now compares Gemini-personalized output vs the deterministic baseline using the 8 locked automated/objective criteria, reported individually; it must never conclude with an overall ranking, "best," or "winner," and must not claim Gemini is "better"/"superior" unless later supported by actual statistical analysis.
- **RQ3:** How do users perceive the generated training plans in terms of personalization, usefulness, clarity, and confidence?

### 3.2 Audit of RQ1 and RQ3
RQ1 and RQ3 are precise enough and unchanged. One consequence for RQ1: it says *multi-week*, but the implementation personalizes only Week 1 with the LLM (Section 15). Either the implementation scope or the RQ1 claim must match; this is `[ADVISOR DECISION REQUIRED]`.

### 3.3 Audit of RQ2 — is the wording precise enough for a comparative study?

| Issue in the current wording | Why it matters |
|---|---|
| "perform" is undefined | It does not say which characteristics are compared (compliance, consistency, quality, stability). "Perform" invites a single "best model" reading, which the study does not want |
| "different" large language models | The set is unspecified; fine as an RQ, but the methodology must define it |
| No statement of the controlled conditions | The comparison is only meaningful if profile, baseline, prompt and task are identical; the RQ should make this explicit |
| "a deterministic running training plan" (singular) | Scope is ambiguous: one plan, one week, or the whole multi-week plan |
| "personalizing … while maintaining consistency" | Personalization quality and constraint consistency are two different constructs; both are named but not separated |
| No mention of stability | Hosted LLMs are stochastic; repeated-run behavior is part of what is compared |

| | Wording |
|---|---|
| **Current** | How do different large language models perform in personalizing a deterministic running training plan while maintaining consistency with the runner profile and predefined training constraints? |
| **Proposed (small change)** | How do different large language models, given the same runner profile and the same deterministic baseline plan, differ in personalizing the plan while remaining consistent with the runner profile and the predefined training constraints? |
| **Optional extension** `[ADVISOR DECISION REQUIRED]` | "…differ in the consistency, quality and stability of the personalization they produce…" |

**Academic reasons.** (1) "differ" states a comparative question without presupposing a winner. (2) "given the same runner profile and the same deterministic baseline plan" states the controlled design in the question itself. (3) "remaining consistent" keeps the compliance construct but separates it from "personalizing". (4) Scope of "plan" (Week 1 vs full plan) is resolved by the methodology decision in Section 15.
**Consequences for the methodology.** The dependent variables must be named separately (compliance, profile consistency, personalization quality, stability); the design is a repeated-measures design with the profile as block (Sections 10, 19); the paper's RQ2 wording would change slightly and Table IV would be replaced (see Section 28 / the list of files to modify after approval). The paper is not changed now.

---

## 4. Research objectives

| Objective | Statement |
|---|---|
| **System/design** | Design and implement a hybrid architecture in which deterministic running-domain calculations and constraints produce a baseline plan, an LLM personalizes it, and server-side validation checks the generated output |
| **Technical validation** | Verify with explicit pass/fail criteria (T1–T14 of the methodology lock) that the implemented system conforms to its specification (no claim about training effectiveness) |
| **LLM comparison** | Compare several LLMs as the personalization layer under identical, documented conditions (same profile, same baseline, equivalent instructions and schema), reporting differences in compliance, profile consistency, personalization quality and stability; no overall ranking |
| **User evaluation** | Describe how runners perceive the generated plans in terms of personalization, usefulness, clarity and confidence, using a study-specific, currently unvalidated questionnaire |

---

## 5. Research contribution (conservative)

1. A hybrid architecture for personalized running-training recommendation (deterministic baseline + LLM personalization + server-side validation).
2. Integration of deterministic running-domain constraints (each classified as literature-informed or an engineering design constraint) with LLM-based personalization.
3. A server-side validation mechanism that constrains generated output against the baseline (implemented for Week 1).
4. A controlled same-profile, same-baseline comparison protocol for LLM personalization, **if executed**, with explicit fairness and traceability requirements.
5. A framework for constraint-compliance evaluation across a multi-week plan, kept separate from quality evaluation.
6. A user-centered evaluation design for perceived personalization, usefulness, clarity and confidence.

Not claimed: novelty beyond the literature; best model; improved performance; safe training; physiological optimality.

---

## 6. System architecture

**CURRENT (Gemini-only, LOCKED) pipeline:**
```
Runner Profile → Validation → Physiological Calculation → Deterministic Rule-Based Multi-Week Baseline
   → Gemini Personalization → Server-Side Validation → Gemini-Personalized Multi-Week Plan
   → Automated Evaluation → Baseline vs Gemini Comparison
```

`SUPERSEDED` generic/2-LLM diagram (audit trail only):
```
Runner Profile → Validation → Physiological Calculation → Deterministic Rule-Based Baseline Plan
   → LLM-Based Personalization → Server-Side Validation → Personalized Training Plan → Evaluation
```

| Stage | Function (as implemented) |
|---|---|
| Runner profile | Age, gender, experience, 5K (optional 10K) personal best, target race and time, weekly mileage, training days and preferred days, plan duration, optional injury note, easy-run pace |
| Validation | Pydantic constraints; invalid input rejected |
| Physiological calculation | VDOT from the 5K personal best; pace zones; target pace; feasibility class |
| Deterministic baseline | Weekly progression, cutback weeks, taper, long run, quality session, easy runs, rest days for all weeks (4–24) |
| LLM personalization | Receives profile, VDOT, zones and the **Week 1** baseline; returns text fields in a fixed JSON schema |
| Server-side validation | Checks schema, workout/day structure, type, distance (±0.05 km), pace and zone strings, weekly mileage (±0.15 km), rest/training-day counts; deterministic fallback on failure |
| Evaluation | Technical validation (RQ1), LLM comparison (RQ2), user evaluation (RQ3) |

---

## 7. Role of the deterministic baseline

The baseline plays three roles that must not be confused:
1. **Controlled input** — identical for every model and run (it is part of what is held constant).
2. **Source of physiological/training constraints** — the task tells the LLM to preserve its numbers.
3. **Oracle for compliance checks** — numeric compliance is measured *against* the baseline, so it is a measure of **fidelity to the baseline (copy-fidelity)**, not of plan quality.

**UPDATED (Gemini-only design):** the primary comparison IS now the baseline itself vs Gemini — **deterministic baseline vs Gemini-personalized output, same profile and baseline given to Gemini as controlled context.** This supersedes the earlier "LLM A vs LLM B with the same baseline" framing (APPROVED/CONFIRMED 2 October 2026, itself now superseded by the Gemini-only locked design the same day). The deterministic baseline is consistently a **controlled reference/input condition**, used to evaluate consistency/fidelity to predefined constraints — it is **never "ground truth" for overall plan quality**, even though it is now a named side of the comparison.

Two known baseline behaviors (reported in earlier audits) needed a decision before the baseline is frozen: the ≈+25% rebound after a cutback week (the running volume was not reset) and the taper anchored to the starting mileage (0.85× and 0.55× of the base, not the peak). **RESOLVED**: the rebound was fixed (the running volume is now reset to the cutback week's own value); the taper anchoring was confirmed correct and intentional, matching `PAPER_DRAFT.md` Table II, and left unchanged. They do not affect Week 1, but they define the constraints against which progression, cutback and taper compliance will be judged once the baseline is generated. Existing stored plans would not change if the rules changed (they are stored as JSON, and none for the 24-profile experiment have been generated yet); newly generated plans use the fixed rule engine.

---

## 8. Role of the LLM (Gemini-only, LOCKED — supersedes "Role of the LLMs" plural framing)

- Gemini is the **personalization layer**, not a source of physiological values. All numbers it receives are computed deterministically, and the task instructs it to keep them unchanged.
- In this study Gemini-vs-baseline is the **comparison condition of RQ2**; in RQ1 and RQ3 Gemini is a component of the system.
- Gemini adds natural-language content: warm-up/cool-down, execution cues, injury-related adaptation, rationale and overview. The validator checks numbers and structure; it does **not** check the safety or accuracy of the text, and it accepts empty text fields (text fields default to `""`).
- Gemini is evaluated *as configured in this system* (prompt, schema, validator, parameters); conclusions do not generalize to Gemini in other tasks, nor to any other LLM.
- `SUPERSEDED`: the earlier plural "Role of the LLMs" framing (multiple models as the independent variable of RQ2) no longer applies — there is only one LLM in the locked design.

---

## 9. Comparative experimental design — CURRENT (Gemini-only, LOCKED)

```
Same Runner Profile → Same Deterministic Multi-Week Baseline
      ↓                           ↓
  Baseline (24, not repeated)   Gemini (3 repetitions per profile → 72)
      ↓                           ↓
            raw Gemini output captured BEFORE any fallback
      ↓                           ↓
      Server-side validation (same validator version)
      ↓                           ↓
      Automated evaluation (8 locked criteria) → Baseline vs Gemini comparison → recorded evidence
```
*(CONFIRMED: 1 LLM — Gemini — only, vs the deterministic baseline. Expert evaluation remains excluded from this design.)*

`SUPERSEDED` 2-LLM diagram (audit trail only):
```
Same Runner Profile → Same Deterministic Baseline
      ↓                    ↓
    LLM A               LLM B                (same prompt, same schema, same settings where possible)
      ↓                    ↓
          raw output captured BEFORE any fallback
      ↓                    ↓
  Server-side validation  (same validator version)
      ↓                    ↓
   Automated/objective evaluation → recorded evidence
```

- **Design:** repeated-measures / block design. **Factor (CURRENT):** condition (deterministic baseline vs Gemini), within-profile. ~~**Factor (SUPERSEDED):** LLM (LLM A vs LLM B), within-profile.~~ **Block:** runner profile. **Replicates:** 3 Gemini repetitions per profile; the baseline is generated once per profile (not replicated, since it is deterministic).
- **Primary outcome stream:** the **raw model output**, evaluated *before* the production fallback is applied. The production dispatcher returns the fallback template when output is invalid; the final plan would then be identical across models and would hide exactly the differences under study. The experiment must therefore not use the fallback-substituted plan as the outcome, and a fallback must never be counted as LLM output.
- **Held constant:** profile, baseline version, prompt text, output schema, validator version and tolerances, generation settings, time window, rule-engine version.
- **Varied (CURRENT):** condition — deterministic baseline vs Gemini-personalized output. ~~**Varied (SUPERSEDED):** model (provider, model identifier, version) across LLM A vs LLM B.~~
- **Not compared:** complete applications, user interface, other pipeline components; no cross-LLM comparison (no second or third model exists in this design).
- **Baseline-only is no longer "additional/optional"** — it is now the primary comparator by design. Template fallback remains an optional additional control `[ADVISOR DECISION REQUIRED]`.
- **No composite score, no overall ranking, no "winner".** Results are a profile of metrics per criterion (8 locked criteria), reported for baseline and Gemini separately; a statement such as "Gemini had fewer constraint violations than the baseline on these profiles under this configuration" is the strongest allowed form. Gemini must not be declared "better"/"improves"/"superior" to the baseline without statistical support.
- **Pilot vs final:** prompt and rubric are developed on a separate pilot set of profiles and frozen before the final run (Section 13), so the prompt is not tuned on the evaluation profiles.

---

## 10. Experimental unit

| Level | Definition | Used for |
|---|---|---|
| **Run** | One Gemini API call: (profile, repetition) → one raw output and one validator verdict; the baseline has no "run" concept (generated once, deterministically) | Observation; replicate (Gemini only) |
| **Cell** | (profile, condition): baseline (1 observation) or Gemini (3 repetitions aggregated) — replaces the superseded "(profile, model)" cell | Aggregate (e.g., proportion of Gemini repetitions passing); the unit of **primary analysis** |
| **Profile (block)** | One synthetic runner profile, with its baseline and its 3 Gemini repetitions | Primary sampling/block unit; the profile, not the run, is the unit of replication for generalizing across runners |
| **Participant** | One runner in RQ3 | Unit of analysis for RQ3 |

~~**SUPERSEDED (2-LLM wording):** "(profile, model)" cell, "run through every model" — replaced by the baseline-vs-Gemini cell above.~~

*(SUPERSEDED: a "Rating" level — one expert's score per (profile, model, run) — previously appeared here. Expert evaluation has been removed from the study; see "Advisor Decision Update — 2 October 2026.")*

Repetitions are replicates for estimating within-cell variability; they are **not** independent samples of runners. Analyzing all runs as independent would inflate the effective sample (pseudo-replication).

---

## 11. Runner profiles

### 11.1 Construction principles
- Profiles are **synthetic vignettes** created from documented rules, not real participants; they are therefore not representative of a population, which must be stated.
- Several profiles are needed, not one; a single profile confounds model differences with profile-specific behavior.
- Stratify on the factors that change the baseline or the text: ability level (5K performance/VDOT band), running experience level (beginner → tempo session; others → interval session), current weekly mileage, target distance (5K, 10K, half marathon), training availability (training days, preferred days), goal feasibility (conservative to aggressive pace delta), injury note (none vs. several kinds), plan duration (short, medium, long; cutback weeks exist only if the plan has at least 6 weeks, taper in every plan).
- Enforce plausibility constraints (e.g., 5K time consistent with experience and mileage); document every profile and the rule that generated it; if any random sampling is used, record the seed.
- Keep a separate **pilot profile set** for prompt/rubric development; do not tune on the final profiles.
- Source of realistic ranges: consult coaches and/or published running statistics `[LITERATURE VERIFICATION REQUIRED]`.

### 11.2 Size — **24 synthetic runner profiles: CONFIRMED** (updated 2 October 2026, Gemini-only design; supersedes the earlier PROPOSED/unconfirmed status)
**24 final profiles, CONFIRMED** = 18 core (3 experience levels × 3 target distances × injury none/present) + 6 edge/coverage profiles (e.g., 1 training day, 7 training days, shortest plan, longest plan, aggressive goal, conservative goal), plus a smaller separate pilot set. Demographic composition detail within the 24 (exact 5K/mileage bands assigned to each) remains an OPEN SUB-DECISION if not already finalized elsewhere.

| Option | Profiles | Advantages | Disadvantages |
|---|---|---|---|
| Few | about 8–12 | Low workload; easy expert rating | Weak coverage; one odd profile dominates; little power for paired tests; results anecdotal |
| Moderate (proposal) | about 24 | Covers the main strata and edge cases; usable for nonparametric paired analysis | Needs a rating subset for experts; still a convenience set |
| Many | 36 or more | Better coverage and precision | Expert workload grows with profiles × models; cost; diminishing returns without a power rationale |

**UPDATED workload (Gemini-only, CONFIRMED; supersedes the 144/720 Week-1-only estimate below):** 24 CONFIRMED profiles × 1 baseline each = **24 baseline plans** (not repeated, since deterministic); 24 profiles × 3 Gemini repetitions = **72 Gemini generations**. **Total outputs for comparison: 24 baseline + 72 Gemini.** Do **not** call this "96 independent experimental generations" (baseline and Gemini repetitions are different unit types) and do **not** reuse the superseded "144 generations" (2-LLM, Week-1-only) or "216 generations" (3-LLM) figures below. Expert evaluation remains excluded from the study (Section 17), so there is no expert-rating subset to plan.

`SUPERSEDED` workload illustration (2-LLM, Week-1-only; audit trail only): with **2 LLMs** and **3 repetitions**, 24 profiles gave 24×2×3 = ~~144 generations~~ for Week-1-only; about 720 if five phase-weeks were personalized. This estimate no longer applies.

---

## 12. LLM selection

### 12.1 Selection criteria (not popularity)
1. Publicly documented model name and version/snapshot.
2. API accessibility to the researcher during the whole study period.
3. Availability and stated deprecation schedule covering the study period (the code default `gemini-1.5-flash` may no longer be available `[VERIFY]`).
4. Ability to follow structured-output instructions and return the required JSON.
5. Comparable access conditions (paid tier/rate limits, no special privileges).
6. Comparable capability/cost tier, or an explicit and justified decision to compare across tiers (otherwise provider is confounded with model size).
7. Support for the same minimum generation controls (temperature, output limit) or a documented deviation.
8. Terms of use permitting the use of the data sent.
9. Relevance to LLM-based text generation in applied use.

### 12.2 Number and candidates — **UPDATED (Gemini-only, CONFIRMED)**
- **Number of LLMs: CONFIRMED — 1 LLM (Gemini)**, advisor decision 2 October 2026 (later same day), superseding the earlier 2-LLM decision (itself superseding the original 3-LLM starting proposal).
- **Model: Gemini** — exact model/version to be finalized and recorded before experimental data collection `[ADVISOR DECISION REQUIRED]` for the identity string. ~~Candidate classes: a Google Gemini-family model and an OpenAI GPT-family model~~ — OpenAI is no longer part of the design; the repository's OpenAI provider path is not used for this study.
- No overall ranking, "best," or "winner" is produced; the comparison is Gemini vs the deterministic baseline, not Gemini vs another model.

---

## 13. Prompt and input standardization

### 13.1 What must be identical
Runner profile; deterministic baseline JSON; the user instructions text; the system instruction text; the JSON output template; the constraint statements; the language; the rendering of the input payload (the same serialization string); the validator and tolerances.

### 13.2 System/user prompt delivery — `SUPERSEDED`: cross-provider fairness problem no longer applies (Gemini-only design)
The cross-provider fairness issue described below (Gemini's concatenated system prompt vs OpenAI's separate system message) is moot now that OpenAI is not part of the design — there is only Gemini. What remains relevant is documenting and freezing Gemini's own system-instruction delivery mechanism for reproducibility. The original text is kept for audit-trail context: in the current code, Gemini receives `SYSTEM_PROMPT` concatenated with the user prompt in a **single user message**, whereas OpenAI (not used in this study) receives them as a **system message plus a user message**. Options (none implemented, and only the Gemini-relevant ones remain applicable):

| Option | Description | Comment |
|---|---|---|
| (i) Common-denominator delivery | Put system and user text in one user message for every provider | Identical position; deviates from the usual system-role practice for some models |
| (ii) Native system role for every provider | Use each provider's dedicated system-instruction mechanism with identical text | Closest to the intended semantics; relies on each provider's implementation (for Gemini, a system-instruction field exists `[VERIFY in current provider documentation]`) |
| (iii) Both as a sensitivity analysis | Primary (ii) or (i); secondary run with the other | More workload; reveals sensitivity |

The choice is `[ADVISOR DECISION REQUIRED]`; whichever is chosen must be documented and the **exact request payload of every call must be stored** so that no model can have received additional text unnoticed (for example, provider-added wrappers).

### 13.3 Other standardization points
- **JSON enforcement:** the code uses provider JSON modes (`responseMimeType` vs `response_format`). Stricter native schema enforcement on one provider and not another would give unequal help; the proposal is JSON-mode plus the schema described in the prompt for all models, with native schema enforcement only if available and used equivalently for all `[ADVISOR DECISION REQUIRED]`. Some JSON modes require instruction wording (e.g., mention of JSON) `[VERIFY]`.
- **Generation parameters:** same temperature value across models (the system's production value is 0.4; choice of value `[ADVISOR DECISION REQUIRED]`); identical explicit output-token cap, set generously above the expected length and checked for truncation; other sampling parameters (top-p/top-k, penalties) left at provider defaults and **recorded**, or fixed equal where supported; no extended-reasoning/"thinking" mode unless allowed for all models and recorded; models that do not accept a given parameter are documented as exceptions. Equal numeric settings do not guarantee equal behavior across providers.
- **No model-specific prompt tuning.** If tuning is allowed at all, it must be applied equally on a pilot set and the prompt frozen before the final run (prompt version P1).
- **Retries:** none; each generation is one attempt; failures are outcomes.
- **Fallback:** disabled in experiment mode for outcome capture; the dispatcher's silent fallback and `auto` provider order must not be used.
- **Model/version/date captured** for each call, including the identifier returned by the API where available.

---

## 14. Repeated runs

Question: does each LLM have to be run more than once per profile? **Yes, recommended**, for these reasons:
- **Stochasticity:** at a temperature above zero, outputs vary run to run; a single run per cell cannot separate a model's typical behavior from sampling luck.
- **Temperature = 0 does not guarantee determinism.** Hosted services can differ across calls because of provider-side batching, hardware or floating-point effects, backend or version changes, and, for some models, fixed or unsupported temperature settings `[VERIFY per model]`. Repeated runs are therefore still needed at temperature 0 to **verify** stability rather than assume it.
- **Reproducibility:** repeated runs measure the run-to-run variability that any later re-run will exhibit.
- **Stability is a result**, not only a nuisance: e.g., how often a model's output passes validation across repeats of the same profile.

Minimum practical repetitions: no value is derived from a power calculation here. **CONFIRMED (2 October 2026, Gemini-only design): 3 repetitions** per runner profile for Gemini (→ 72 Gemini generations across 24 profiles) — the smallest number that yields a within-cell variability estimate beyond a single pair. The deterministic baseline is **not** repeated (generated once per profile → 24 baseline plans), since it is deterministic and repeating it would add no information. Repetitions are replicates, not additional independent runners; the runner profile remains the sampling/block unit. 5 would give a more stable estimate at higher cost but is not the approved figure.

Temperature policy options `[ADVISOR DECISION REQUIRED]`: (a) one common setting equal to the system's production value as the primary condition; (b) temperature 0 or the provider's minimum as a secondary sensitivity condition; (c) provider defaults (not recommended: unequal conditions).

How consistency/stability would be evaluated: per (profile, model) cell — proportion of repetitions that pass validation, agreement of failure categories across repetitions, variation in numeric deviations, completeness across repetitions, a similarity measure between repetition texts (measure to be chosen and justified `[ADVISOR DECISION REQUIRED]`), and, if experts rate several repetitions, the variability of ratings across repetitions. Run order should be randomized/interleaved across models and profiles.

---

## 15. Multi-week evaluation — **RESOLVED/CONFIRMED (Gemini-only design, 2 October 2026): multi-week scope is confirmed**

~~**OPEN METHODOLOGICAL DECISION: The relationship between the multi-week research scope and the specific weeks/context presented to the LLM must be finalized before the comparative experiment.**~~ — **RESOLVED.** Gemini now receives sufficient multi-week context (not Week-1-only) per the confirmed pipeline in Section 6: Runner Profile → Validation → Physiological Calculation → Deterministic Rule-Based Multi-Week Baseline → Gemini Personalization → Server-Side Validation → Gemini-Personalized Multi-Week Plan → Automated Evaluation → Baseline vs Gemini Comparison. This resolves the previously open "Week-1-only vs multi-week" decision; progression, cutback, taper and weekly-volume criteria across weeks can now carry information about Gemini's behavior, not only about the deterministic engine.

The options analysis below is kept for audit-trail/implementation-reference purposes (it informed the confirmed design), but the decision itself is no longer open:

`SUPERSEDED` framing (audit trail only): RQ1 claims multi-week plans, but **the LLM currently receives and personalizes only Week 1**; Weeks 2+ are deterministic and identical across models. Consequently, under the old design, progression, cutback, taper and weekly-volume criteria across weeks carried **no information about differences between models**; they described the deterministic engine (RQ1) only. The design options were:

| Option | LLM context/task | Scientific consequences | Costs/risks |
|---|---|---|---|
| **1. Week 1 only (current)** | Baseline Week 1 | Clean, comparable, low cost; RQ2 conclusions restricted to Week-1 personalization; multi-week criteria evaluate the rule engine, not the models; the RQ1 "multi-week personalized" wording should then say "first-week personalization" | Cannot test how models handle phase changes (cutback, taper); weakest match to the RQ wording |
| **2. Full multi-week baseline in one call** | All weeks, all days | Directly tests whole-plan consistency (progression, cutback, taper, long-run, rest structure) across models; matches the "multi-week" claim | Long input and output (up to 24 weeks × 7 days); output limits or truncation may differ by model; more malformed-JSON and omission failures; token cost; the validator and schema must be extended; output length becomes a confound (though partly a legitimate model characteristic); changes the system under study |
| **3. Week 1 with plan-level context** | Week 1 baseline to personalize + a read-only compact schedule of all weeks (phase, target volume) | Lets models write rationale consistent with the whole progression; permits checking that text does not contradict the schedule; low cost | Still personalizes only Week 1; checks progression only through *statements about it* |
| **4. Phase-stratified week-level personalization** | Separate calls for representative weeks (e.g., Week 1, a cutback week, the last build week, a taper week, the race week), each with that week's baseline and plan-level context | Tests constraint handling in each phase at bounded cost; model differences visible for cutback/taper; each call is short | More calls (representative weeks × profiles × models × repetitions); profiles must be long enough to contain cutback weeks (about 6 weeks or more); requires prompt/schema/validator generalization to any week; weeks are personalized independently, so cross-week text coherence is untested |
| **5. Per-week generation of every week** | Each week separately | Full coverage | Highest cost; independent calls give no cross-week coherence; impractical for 24-week plans |

What "progression, cutback, taper consistency" means for an LLM that must **not** alter numbers: (a) numeric fidelity of each week to the baseline (compliance), and (b) correctness of statements the model makes about progression/cutback/taper (explanation consistency). It is **not** a measure of how good the progression is. A variant in which the LLM may *adjust* volumes within deterministic bounds would test personalization of the load itself but would put the LLM into physiological decision-making and contradict the system's stated principle; it is not proposed.

**RESOLVED:** the advisor has confirmed multi-week scope (a design in the spirit of Option 4/3 combined — sufficient multi-week context given to Gemini, with server-side validation). ~~Recommendation (most defensible, for discussion): Option 4 combined with Option 3's plan-level context…Option 1 is acceptable only if RQ1/RQ2 wording is restricted to first-week personalization. `[ADVISOR DECISION REQUIRED]`~~ Any implementation beyond the previous Week-1-only system requires the corresponding system changes (Appendix), which are now authorized by this confirmation.

---

## 16. Proposed automated evaluation criteria

**Status: UPDATED — the criteria COUNT is now LOCKED AT EXACTLY 8** (not 16; the 16-item draft list below is `SUPERSEDED` and kept only as source material). **OPEN SUB-DECISION, explicitly flagged and NOT resolved here:** the exact operational definitions of the 8 locked criteria differ across documents — `RESEARCH_METHODOLOGY_LOCK.md`'s own 8-criterion list, this document's 16-item draft below, and `PAPER_DRAFT.md` Table IV's 5-criterion list are not identical in grouping or wording. The 8 candidate criteria per the advisor's locked design are: profile consistency, goal consistency, physiological/pace consistency, weekly volume/mileage consistency, workout structure, intensity constraints, progression/recovery constraints, and completeness/constraint violations — these must be mapped against the 16-item list below and against the lock's own list before the rubric is finalized.

Since expert evaluation has been removed from the study, RQ2 relies solely on automated/objective criteria. Principles: automated results are **objective compliance with a specification**, not training-plan quality and not physiological optimality; the baseline is a **controlled reference/input**, used to evaluate consistency/fidelity to predefined constraints — **never "ground truth" for overall plan quality**; criteria use the **raw Gemini output** (pre-fallback). "Existing validator" notes what `validate_ai_plan` already checks. Multi-week scope is now confirmed, so these criteria apply across the full multi-week context, not Week 1 only.

`SUPERSEDED` 16-item draft list (kept as source material for the 8-criterion mapping above, not as the final rubric):

| # | Criterion | Construct | Operational definition | Measurement | Pass/fail or continuous | Data source | Oracle / reference | Limitation |
|---|---|---|---|---|---|---|---|---|
| 1 | Output schema compliance | Format validity | Output parses as JSON and conforms to the plan schema | Parse + schema validation; record failure type (non-JSON, truncated, wrong types) | Pass/fail | Raw output, parsed output | Plan schema | Existing validator covers this; truncation/refusals need separate flags |
| 2 | Required-field completeness | Completeness | Every required text field is present **and non-empty** for each non-rest day; plan-level fields non-empty | Field-level count of present/non-empty fields | Continuous (proportion) and pass/fail | Parsed output | Field list from schema and task | Existing validator **accepts empty strings**; "non-empty" is not "informative" |
| 3 | Runner-profile consistency | Fidelity to profile facts | Text does not contradict profile facts (goal distance/time, experience level, training days, injury note) | Rule-based fact checks plus expert confirmation; count of contradictions | Count / pass-fail | Parsed text, profile | Profile record | Requires extraction rules; incomplete automatic detection |
| 4 | Goal consistency | Goal alignment | Race distance, target time and target pace stated in text equal the profile/baseline | Extract and compare numbers/names | Pass/fail per statement | Parsed text, baseline | Baseline target pace/time | Number extraction is heuristic; paraphrases missed |
| 5 | Workout-type consistency | Structural fidelity | Each day's workout type equals the baseline's | Day-by-day comparison | Pass/fail per day; proportion | Parsed plan | Baseline | Existing validator checks (Week 1) |
| 6 | Intensity-zone consistency | Structural fidelity | Intensity-zone string equals baseline; zone is appropriate to the workout type | String equality; rule table | Pass/fail | Parsed plan | Baseline; zone/type rule table | Equality exists; "appropriate to type" rule is new |
| 7 | Pace consistency | Numeric fidelity | `pace_target` equals baseline; paces quoted in free text belong to the computed zone table | String equality; extract paces from text | Pass/fail; count of unmatched text paces | Parsed plan, baseline zones | Baseline pace table | Text extraction heuristic |
| 8 | Distance consistency | Numeric fidelity | Each `distance_km` equals baseline within the validator tolerance; distances in text equal the plan | Absolute deviation per day | Continuous (km) and pass/fail | Parsed plan, baseline | Baseline | Tolerance (0.05 km) is itself a design choice; sensitivity analysis with exact equality `[ADVISOR DECISION REQUIRED]` |
| 9 | Weekly-mileage consistency | Numeric fidelity | `weekly_mileage_km` equals baseline within tolerance and equals the sum of distances | Deviation; sum check | Continuous / pass-fail | Parsed plan, baseline | Baseline | Existing validator does not check the sum |
| 10 | Rest-day consistency | Structural fidelity | Rest days equal baseline; number of training days equals the profile | Count and day-set comparison | Pass/fail | Parsed plan, profile | Baseline; profile | Existing validator checks (Week 1) |
| 11 | Long-run constraint | Rule conformance | Long run distance equals baseline and baseline respects its rule (30% share, caps, floor) | Compare to baseline; recompute rule | Pass/fail | Parsed plan, baseline | Rule specification | Constraint is an engineering design constraint; floors may exceed 30% at low volume |
| 12 | Progression consistency | Rule conformance across weeks | Weekly volumes across weeks equal the baseline progression; text statements about progression do not contradict the schedule | Per-week deviation; statement check | Continuous / pass-fail | Parsed multi-week output | Baseline schedule | **Now measurable**: multi-week scope is CONFIRMED under the Gemini-only design (superseding the earlier Week-1-only limitation). **RESOLVED**: the baseline rebound fix-or-document decision is made and implemented (fixed) — this criterion can be scored against a settled rule once baselines are generated |
| 13 | Cutback-week consistency | Rule conformance across weeks | Cutback weeks have the baseline volume and are described as recovery weeks | Per-week comparison | Pass/fail | Parsed output, baseline | Baseline cutback rule | **RESOLVED** — rebound fixed; cutback's own formula was already correct and unaffected |
| 14 | Taper consistency | Rule conformance across weeks | Taper/race-week volumes equal baseline and are described consistently | Per-week comparison | Pass/fail | Parsed output, baseline | Baseline taper rule | **RESOLVED** — taper-anchoring confirmed correct (base-mileage-anchored, per Table II) and left unchanged |
| 15 | Absence of duplicate/conflicting workouts | Internal consistency | No duplicate days, no two sessions contradicting each other (e.g., hard session adjacent to long run contrary to baseline, text contradicting the plan on the same day) | Duplicate-day check; conflict rules | Count / pass-fail | Parsed plan | Baseline; conflict rules | Existing validator checks duplicate days only; text-level conflicts need rules or experts |
| 16 | Safety/constraint violations | Constraint safety | (a) any hard-constraint violation from criteria 5–14; (b) text flags: advice that contradicts the plan or profile limits (extra hard sessions, extra mileage, "run through sharp pain") or specific medical/supplement dosing | (a) automatic aggregation; (b) rule list plus expert review | Count of violations | Parsed text, rules | Flag list `[ADVISOR DECISION REQUIRED]` | Absence of flags is not evidence of safety; keyword detection has low recall |

Reporting rule: each criterion is reported separately; there is no composite score. Criteria 5–10 largely restate what the validator enforces and will probably approach a ceiling; a pilot should check for ceiling effects (if every model complies fully, the comparison is uninformative on compliance and the weight of the study falls on personalization quality and stability).

---

## 17. Expert evaluation — `SUPERSEDED`: REMOVED FROM THE STUDY (Advisor Decision, 2 October 2026)

**Expert evaluation is excluded entirely from this study.** No coach/expert rating, expert rubric, inter-rater agreement, expert recruitment, or blinded expert assessment will be used. RQ2 relies solely on the automated/objective evaluation criteria of Section 16.

The table below (the previous proposal) is kept for audit-trail purposes only and no longer applies:

| Aspect | Previous proposal (no longer applicable) |
|---|---|
| Use of experts | ~~Yes/no `[ADVISOR DECISION REQUIRED]`~~ — resolved: no experts; objective evaluation only (Section 16) |
| Expert background | ~~Running coach, exercise scientist, sports-science professional, qualified endurance-training practitioner~~ |
| Number of experts | ~~More than one needed for inter-rater agreement~~ |
| Criteria (no weights) | ~~Personalization, training appropriateness, internal consistency, workout structure, progression/phase explanation, practicality, clarity, safety flags~~ |
| Inter-rater agreement | ~~Krippendorff's alpha, weighted kappa, ICC~~ |
| Ethics | ~~Experts are human participants `[CHECK BINUS REQUIREMENTS]`~~ — no longer applicable |

**Current design:** objective/automated evaluation only (Section 16), extended where useful with rule-based text checks (profile-fact use, number consistency, flagged-advice lists) and stability metrics across repetitions. Claims about personalization quality are limited to what automated criteria can establish; no LLM-as-judge or human expert judge is used as evidence in this study.

---

## 18. RQ2 metrics

Metric families, reported separately (no composite, no ranking):

| Family | Metrics | Source |
|---|---|---|
| A. Format validity | JSON-parse rate; schema-valid rate; truncation rate; refusal rate | Raw output |
| B. Constraint compliance (objective) | First-attempt validator pass rate; failure-category counts; per-field numeric deviations; rest/training-day match; for multi-week designs: per-week/phase compliance | Validator + rule checks |
| C. Profile consistency (objective) | Contradiction counts; goal-statement correctness; injury content present and consistent | Rule checks |
| D. Completeness | Proportion of non-empty required fields | Parsed output |
| E. Personalization (objective proxy only) | Rule-based use of profile facts (Section 16, criterion 3); no expert rating — see `SUPERSEDED` Section 17 | Rule checks |
| F. Stability | Within-cell pass proportion; agreement of failure categories; variability of deviations and text similarity | Repeated runs |
| G. Operational | HTTP errors, timeouts, latency, token usage/cost, retries (none) | Run logs |

Distinguish *first-attempt* metrics on raw output (primary) from *final-plan* metrics after fallback (trivial; reported only as system behavior).

---

## 19. Statistical analysis

**Principle:** the analysis follows the design (Section 10); no test is claimed as mandatory before the number of profiles, repetitions and raters is decided `[ADVISOR DECISION REQUIRED]`.

1. **Unit of analysis:** the cell (profile × condition, i.e., baseline or Gemini) for compliance, completeness and stability outcomes (aggregate the 3 Gemini repetitions within the cell; the baseline cell has one observation); the profile is the sampling unit. Do not treat the 72 Gemini generations as 72 independent profiles or participants — they are nested within the 24 profiles.
2. **Descriptive first:** per model, proportions with confidence intervals (e.g., intervals obtained by bootstrapping over profiles, since repetitions are clustered), failure-category tables, distributions of deviations, per-stratum results.
3. **Paired comparison, baseline vs Gemini:** the same profile has both a baseline and (aggregated) Gemini repetitions, so the comparison is paired within profile.
   - No specific test is finalized. **The final statistical procedure will be selected based on the measurement scale, pairing structure, repeated-generation design, and distributional characteristics of the collected outcomes.** Candidate approaches (PROPOSED only): a paired nonparametric test on per-profile aggregates (e.g., Wilcoxon signed-rank); mixed-effects / hierarchical models with profile as a random effect and the 3 Gemini repetitions nested within profile (e.g., Friedman-type extensions for repeated designs); logistic models for pass/fail outcomes. The 72 Gemini outputs must **not** be treated as 72 independent participants/samples — they must be modeled as repeated observations nested within the 24 profiles.
   - Small N (24 profiles) favors nonparametric or exact/permutation methods; asymptotic results may be unreliable.
4. **Multiple comparisons:** many criteria (8 locked) create multiplicity; pre-specify a small set of primary outcomes (e.g., first-attempt validator pass rate), treat the rest as exploratory, and use a stated correction (e.g., Holm) for pairwise tests.
5. **Effect sizes and uncertainty:** report effect sizes (paired differences in proportions; matched-pairs rank-biserial correlation) with confidence intervals, not only p-values, where appropriate.
6. **Ceiling/floor effects:** if compliance is near 100% for both the baseline and Gemini, report that and avoid forcing a test.
7. ~~Expert ratings~~ — not applicable; expert evaluation is removed from the study (Section 17).
8. **No composite score and no single ranking.** A "best LLM"/"winner" statement is not an allowed output; results are reported per metric, per stratum, with uncertainty.
9. **Sample-size:** not determined here; planning approaches (precision-based for proportions, simulation-based power for the paired design with an assumed effect size, or a pilot to estimate variance) are `[ADVISOR/METHOD REVIEW REQUIRED]`.
10. **Preregistration** of outcomes and analysis `[ADVISOR DECISION REQUIRED]`.

---

## 20. RQ3 user evaluation

- **Retained as a separate study of perception**, not of LLM ranking. Constructs: **Perceived Personalization (PP), Perceived Usefulness (PU), Perceived Clarity (PC), Recommendation Confidence (RC)**, each with four proposed items on a 5-point agreement scale: 1 Strongly Disagree, 2 Disagree, 3 Neither Agree nor Disagree, 4 Agree, 5 Strongly Agree.
- **Questionnaire status:** study-specific and currently unvalidated; no formal validation exists; no item may be called validated.
- **Relation to RQ2:** options `[ADVISOR DECISION REQUIRED]`: (a) participants evaluate plans from one configured model only (RQ3 stays independent of the model comparison); (b) participants see plans from several models for the same profile, blinded, which would also give perception evidence per model but multiplies workload and requires a within-subject design; (c) participants are randomly assigned one model. The "AI" plan must come from live LLM output, never from the fallback.
- **Reference/baseline plans and a template-text control** are optional additional conditions, subject to the text-amount confound `[ADVISOR DECISION REQUIRED]`.
- **Objective vs subjective:** automated criteria (Section 16) and user perceptions (this section) are two separate evidence streams and are never merged into one score. Expert evaluation is excluded from the study (Section 17, `SUPERSEDED`) and is not part of RQ3; the questionnaire is a user/participant instrument, not an expert questionnaire.
- **Design, sample size, recruitment, eligibility:** not chosen. Sample-size approaches: pilot-based, precision-based for descriptive statistics, power-based for a paired ordinal comparison with an assumed effect size, and reliability-based (minimum respondents for Cronbach's alpha) `[ADVISOR/METHOD REVIEW REQUIRED]`. Proposed eligibility: adult recreational runners able to provide a 5K personal best and weekly mileage; the application currently accepts ages 12–99 `[CHECK BINUS REQUIREMENTS]`.
- **Application readiness:** the current application collects four single ratings with pre-filled defaults, visible plan labels, no participant code and no consent screen; it does not implement the 16 items.

---

## 21. Questionnaire audit

Wording below is the proposal in `QUESTIONNAIRE_TRACEABILITY.md` (not in the application or the paper). **The questionnaire is study-specific and currently unvalidated.** Revision suggestions are proposals only; the questionnaire file is not changed.

| Item | Wording (current proposal) | Flags | Proposed revision (not applied) |
|---|---|---|---|
| PP1 | This plan takes my personal running profile (for example my current fitness and goal) into account. | Overlaps PP4; two examples in brackets (mildly multi-barrelled); mildly leading | Remove the bracketed examples or split by aspect; keep one global item |
| PP2 | This plan fits the number of days I can train each week. | Construct-fit doubt (feasibility rather than personalization) | Keep as availability-fit; consider moving to PU (practicality) |
| PP3 | This plan takes my reported injuries or physical limitations into account. | Mildly leading; not applicable for runners without injury | Add a "not applicable" option |
| PP4 | This plan feels written for me rather than for runners in general. | Contrastive two-part wording; mildly leading; overlaps PP1; vague ("feels") | Reword without the contrast or drop in favor of PP1 |
| PU1 | This plan would help me prepare for my target race. | Overlaps PU4; hypothetical ("would") | Keep; ensure respondents all have a target race |
| PU2 | The weekly schedule is practical to follow in my daily routine. | Construct-fit doubt (feasibility vs usefulness) | Keep as practicality or move out of PU |
| PU3 | Following this plan would help me organize my running training. | Overlaps PU1/PU4; vague ("organize") | Merge with PU4 or sharpen |
| PU4 | I find this plan useful. | Global; overlaps PU1/PU3 | Keep one global usefulness item |
| PC1 | The workout descriptions in this plan are easy to understand. | Plans differ in text amount if a reference/baseline plan is used | Keep; interpret carefully across conditions |
| PC2 | The pace targets in this plan are clearly stated. | None major | Keep |
| PC3 | I understand why each type of workout is included in this plan. | Universal quantifier ("each type") — hard to agree; explanation rather than clarity | "I understand the purpose of the workouts in this plan." |
| PC4 | The warm-up and recovery instructions in this plan are clear. | **Double-barrelled**; overlaps PC1; baseline plans have no warm-up field | Split into two items or choose one |
| RC1 | I am confident that I could follow this plan. | Overlaps RC3; self-efficacy rather than confidence in the recommendation | Keep as adherence confidence; relabel construct aspect |
| RC2 | I trust the training load in this plan to be appropriate for me. | Mildly leading; respondents may lack expertise; "trust" and "appropriate" together | "I believe the weekly training load in this plan is suitable for my current fitness." |
| RC3 | I would feel comfortable using this plan to guide my training. | Vague ("comfortable"); overlaps RC1 | Merge with RC1 or sharpen |
| RC4 | I am confident that the pace targets match my current ability. | Difficult to judge for respondents; related to PC2 | Keep if participants know their pace; otherwise reconsider |

Other issues: the application's current scale anchors differ from the planned agreement scale (e.g., "1 - Very Generic … 5 - Highly Personalized"); sliders are pre-filled (5/5/5/4); no participant code; no consent. All items are study-specific; validation path (proposal): construct literature review → item review → expert/content review → pilot → wording revision → final version → main data collection (`[ADVISOR DECISION REQUIRED]` for panel and pilot sizes). Possible adaptation from the ResQue framework [3] only after its item list has been read `[LITERATURE VERIFICATION REQUIRED]`. If participants rate plans from different models, item wording must not refer to "AI" in a way that reveals the source.

---

## 22. Confounding factors

"Controllable?": Yes = can be made identical by design; Partly = reducible but not eliminated; No = outside the researcher's control. "Must report?": whether it must appear in the paper.

| Factor | Risk | Mitigation | Fully controllable? | Must report? |
|---|---|---|---|---|
| Prompt differences between models | One model effectively receives different instructions | Identical text; store exact request payloads | Yes | Yes |
| Prompt tuned on one model | Prompt favors the model it was developed on | Pilot set; freeze prompt before final run | Partly | Yes |
| System/user message formatting (Gemini concatenation vs OpenAI system role) | Different instruction following due to role placement | Choose a common delivery or native system role for all; optional sensitivity run | Partly | Yes |
| Model version differences | Results tied to a version; alias may move | Pin dated snapshots; record returned identifier | Partly | Yes |
| Capability/cost tier differences | Provider confounded with model size | Declared tier policy | Yes (by selection) | Yes |
| Temperature and sampling parameters | Unequal randomness; equal values ≠ equal behavior | Same explicit settings; record defaults | Partly | Yes |
| Token/output limits | Truncation differs; length differences | Same generous explicit cap; flag truncation | Partly | Yes |
| Context length / input size | Longer multi-week context changes behavior | Same input; record token counts | Partly | Yes |
| Reasoning/thinking modes | Hidden reasoning tokens change behavior and latency | Same policy for all; record | Partly | Yes |
| JSON enforcement mode | Unequal help to produce valid JSON | Same enforcement tier | Partly | Yes |
| Provider safety filters/refusals | Output blocked or altered | Record settings; count refusals as outcomes | Partly | Yes |
| API changes / deprecations | Model removed or changed mid-study | One short window; record dates; contingency plan | No | Yes |
| Hidden provider-side changes | Same name, different behavior over time | Time window; store raw outputs; state limitation | No | Yes |
| Fallback behavior | Template output mistaken for LLM output; hides failures | No fallback in experiment mode; flag any substitution | Yes | Yes |
| Malformed JSON / retries | Retry policy changes outcomes | No retries; count failures | Yes | Yes |
| Validator differences / tolerances | Different checks or tolerance across models/time | One validator version for all; tolerance sensitivity analysis | Yes | Yes |
| Validator as both gate and outcome | Circular measurement of "consistency" | Report as compliance with failure categories | Partly | Yes |
| Baseline version / rule-engine behavior | Baseline changed between runs if the rule engine is edited; the rebound issue was fixed (a one-time, intentional change to newly generated output for plans ≥ 8 weeks), taper confirmed unchanged | Freeze baseline; store hash | Yes | Yes |
| Profile distribution | Results depend on which profiles were sampled | Documented stratified design; report per stratum | Partly | Yes |
| Synthetic profiles | Not representative of real runners | State; optional coach review of plausibility | No | Yes |
| Order effects in execution | Time-of-day, rate limits, drift favor early/late calls | Randomize/interleave order | Yes | Yes |
| Repeated runs | Clustering inflates significance | Analyze at profile level; report repetition design | Yes | Yes |
| Time/date of execution | Version drift, load-dependent latency | Record UTC timestamps; short window | Partly | Yes |
| Network/region/endpoint | Latency/availability differences | Record endpoint/region | Partly | Optional |
| Output length (verbosity) | Experts favor longer text | Report length; blinding does not remove length cues | No | Yes |
| ~~Expert evaluation order~~ | `SUPERSEDED` — expert evaluation removed from the study | n/a | n/a | n/a |
| ~~Rater knowledge of model/AI origin~~ | `SUPERSEDED` — no raters in this design | n/a | n/a | n/a |
| ~~Rater subjectivity / no consensus criteria~~ | `SUPERSEDED` — no raters in this design | n/a | n/a | n/a |
| Model knowledge cutoff / training data | Different domain knowledge | Report model dates | No | Optional |
| Researcher bias | Designer is evaluator | Fix protocol first; blinded rating; report all runs | Partly | Yes |
| Ceiling/floor effects | Compliance near 100% for all | Pilot to check; focus on discriminating metrics | Partly | Yes |
| Rule-engine limitations | Constraints are engineering design constraints, two known behaviors | Document or fix before freeze | Yes | Yes |

---

## 23. Reproducibility

### 23.1 Traceability record per run (methodology only; not implemented)
`experiment_id`, `run_id`, `profile_id`, `repetition_index`, `model_name` (requested), `model_version` (returned/pinned), `provider`, `endpoint`, `timestamp_utc` (start/end), `latency`, `prompt_version` and prompt hash, exact request payload (system/user text and placement), `deterministic_baseline_version` (code commit + hash of baseline JSON), `validator_version` (commit) and tolerances, `rule_engine_version` (commit), generation parameters (temperature, output cap, other sampling, JSON mode, reasoning mode), HTTP status and errors, token usage, `raw_output` (verbatim), `parsed_output`, validation result and violation list, evaluation metrics, expert ratings with rater codes and rubric version (if used), analysis script version, environment (language and package versions).

### 23.2 Also to store
Profile files and the rule that generated them; baseline JSON; the protocol version and approval date; deviations log; read-only archive with checksums; analysis scripts that regenerate every table.

### 23.3 Limitations that remain
Hosted LLM APIs can change **even when the model name is unchanged** (silent updates, alias changes, infrastructure changes), and outputs can vary run to run even with fixed settings; a later re-run may not reproduce the same text. Mitigations: pinned dated snapshots where offered, a short execution window, storage of raw outputs (so analysis, not generation, is exactly reproducible), reporting returned model identifiers and dates; open-weight models on pinned local or hosted checkpoints are an option with better reproducibility but more infrastructure `[ADVISOR DECISION REQUIRED]`. Current repository limitations (no experiment/run IDs, prompt version, captured model version, raw-output/verdict/error storage, git commit; `requirements.txt` with `>=` ranges) are listed in the readiness audit.

---

## 24. Ethics and data privacy

- Ethics/research-review requirements have not yet been confirmed and should be checked with the supervisor/BINUS before participant recruitment or collection of health-adjacent information `[CHECK BINUS REQUIREMENTS]`.
- **RQ2 with synthetic profiles** involves no human participants (expert evaluation, which would have involved human raters, has been removed from the study). Synthetic profiles may be sent to external LLM providers without personal-data concerns, provided they contain no real person's data.
- **RQ3** collects questionnaire responses and, if participants enter their own profiles, health-adjacent information (injury notes) that would be sent to external LLM providers: disclosure, consent, minimization (vignettes or coarse injury categories), adult-only participation (the application accepts ages 12–99), withdrawal, retention and storage rules must be decided.
- No names or contact data in research tables; consent log separate; development database rows are test data and must not be mixed with study data.
- Provider terms for data use and retention must be checked for every API used `[CHECK BINUS REQUIREMENTS]`.

---

## 25. Threats to validity

| Type | Threat | Handling |
|---|---|---|
| Construct | Compliance ≠ quality; compliance is measured against the system's own baseline and rules (circularity); "performance" of a model is multi-dimensional; questionnaire unvalidated | Separate evidence streams; report as compliance; no composite; validation process for the instrument |
| Internal | Unequal prompt delivery/parameters; fallback mixed with LLM output; order and drift effects; prompt tuned on one model; rater bias | Standardization (Section 13); raw-output capture; randomization; pilot/freeze; blinding |
| External | Synthetic profiles; limited strata; models and versions at one date; one prompt; LLM scope limited to Week 1 or sampled weeks; results do not transfer to other tasks or models | State scope; no generalization to "best LLM" |
| Conclusion (statistical) | Small number of profiles; multiple comparisons; clustering; ceiling effects; ordinal data | Profile-level analysis, nonparametric/exact methods, primary outcomes pre-specified, effect sizes and CIs |
| Reproducibility | API drift, nondeterminism | Section 23 |
| Researcher bias | Designer evaluates own system | Fixed protocol, blinded raters, full reporting, optional independent review |
| Rater | Subjectivity, low agreement, length bias | Calibration; report agreement |
| Questionnaire/sample (RQ3) | Self-report; convenience sample | Descriptive claims only |
| Validity of constraints | Rules are engineering design constraints; two known behaviors | Documented limitation or fix before freeze |

---

## 26. Advisor decisions required

| Decision | Proposed Option | Alternatives | Why It Matters | Advisor Decision |
|---|---|---|---|---|
| Final RQ2 wording | **RESOLVED/LOCKED (Gemini-only wording, Section 3)** | ~~LLM A vs LLM B wording~~ superseded | Defines the construct and scope of the comparison | **RESOLVED (2 October 2026, Gemini-only)** |
| Number of LLMs | **CONFIRMED: 1 (Gemini)** | ~~2 ("LLM A","LLM B"); 3; 4 or more~~ superseded | Workload, multiple comparisons, breadth | **RESOLVED (2 October 2026, Gemini-only — supersedes the same-day 2-LLM resolution)** |
| Selected LLM | Gemini; exact model/version to be finalized and recorded before data collection | — | Defines the comparison condition; availability | `[ADVISOR DECISION REQUIRED]` (exact version string only; model and count resolved) |
| Number of runner profiles | **CONFIRMED: 24 final (18 core + 6 edge)** plus a separate pilot set | 8–12; 36+ | Representativeness, workload, analysis | **RESOLVED (2 October 2026, Gemini-only)** — demographic composition detail remains an open sub-decision |
| Repeated generations | **CONFIRMED: 3 Gemini repetitions per profile (72 total); 24 baseline plans, not repeated** | ~~1; 5; also at temperature 0~~ superseded as the count | Separates Gemini's behavior from sampling variation; baseline needs no replicate (deterministic) | **RESOLVED (2 October 2026, Gemini-only)** |
| Temperature/generation policy | Common value equal to production setting (value to decide) | Temperature 0 as sensitivity; provider defaults | Fairness and stability | `[ADVISOR DECISION REQUIRED]` |
| Prompt delivery | Native system role for all, or one common message (Section 13.2) | Sensitivity run with both | Unequal instruction placement is a confound | `[ADVISOR DECISION REQUIRED]` |
| Baseline: comparator or controlled reference | **RESOLVED/UPDATED: the baseline IS now the primary comparator** (baseline vs Gemini), while still being a controlled reference/input and never "ground truth" for overall quality | — | Determines what can be claimed | **RESOLVED (2 October 2026, Gemini-only)** |
| Full-plan vs Week-1 LLM context | **RESOLVED/CONFIRMED: multi-week scope confirmed** per the pipeline in Section 6 | — | Determines whether multi-week criteria discriminate Gemini from the baseline | **RESOLVED (2 October 2026, Gemini-only)** |
| Baseline rule-engine fix vs document | Decide before freeze | Fixed rebound in code; documented taper as the intended, already-correct design | Alters baselines (rebound) and settles compliance oracles | **RESOLVED** — see `paper/CODE_AUDIT_EASY_RUN_PACE_AND_T7.md` |
| Automated evaluation criteria — count | **RESOLVED: exactly 8, locked** | — | Defines the primary outcome | **RESOLVED (2 October 2026, Gemini-only)** |
| Automated evaluation criteria — exact definitions | **OPEN SUB-DECISION, explicitly flagged:** the lock's 8, this document's 16-item draft, and the paper's Table IV 5 are not identical | Reconcile into one definitive 8-item rubric | Defines what exactly each of the 8 criteria measures | `[ADVISOR DECISION REQUIRED]` — NOT resolved by this update |
| Acceptability thresholds | None proposed (descriptive reporting) | Advisor-set thresholds | Avoids invented cutoffs | `[ADVISOR DECISION REQUIRED]` |
| Expert evaluation | **RESOLVED (2 October 2026): excluded entirely from the study** | ~~Yes, on a subset, blinded to model~~ superseded | RQ2 relies solely on automated/objective criteria | **RESOLVED** |
| Statistical method | PROPOSED methodology only: profile-level paired comparison, profile as block/sampling unit, repeated generations as replicates, appropriate non-parametric analysis if parametric assumptions fail, effect sizes/CIs where appropriate; mixed models if supported | Descriptive only | Must match the design; no specific test declared final | `[ADVISOR/METHOD REVIEW REQUIRED]` |
| Fallback handling | Disabled in experiment mode; raw outputs evaluated | Count fallback as a system outcome in a separate analysis | Prevents masking differences | `[ADVISOR DECISION REQUIRED]` |
| Questionnaire revision | Apply the proposals in Section 21, then validation process | Keep wording; adapt from ResQue after review | Instrument cannot be called validated otherwise | `[ADVISOR DECISION REQUIRED]` |
| RQ3 design and relation to RQ2 | One configured model (RQ3 independent of comparison) | Blinded multi-model exposure; random assignment | Workload and interpretation | `[ADVISOR DECISION REQUIRED]` |
| Participant sample size | No number proposed; approaches listed (Section 20) | Pilot-based, precision-based, power-based, reliability-based | Feasibility and claims | `[ADVISOR/METHOD REVIEW REQUIRED]` |
| Ethics/BINUS approval | To be confirmed | Exemption if the committee grants it | Gates participant/expert data | `[CHECK BINUS REQUIREMENTS]` |
| External LLM data disclosure | Disclose; use vignettes or coarse categories for participant data | Exclude free-text injury | Privacy and consent | `[CHECK BINUS REQUIREMENTS]` |
| Literature gap wording | Defensible gap (Section 28b) after literature verification | — | Avoids unsupported novelty claims | `[LITERATURE VERIFICATION REQUIRED]` |

---

## 27. Recommended decision sequence

```
Advisor methodology approval (RQ wording, design choices)
        ↓
Freeze research protocol (models, profiles, repetitions, scope, criteria)
        ↓
Resolve/freeze baseline rules (fix vs document) ──→ then freeze baseline version
        ↓
Select and document LLM configurations; pilot profiles; freeze prompt P1
        ↓
Confirm ethics/BINUS requirements (can run in parallel from the start)
        ↓
Implement missing RQ1 tests (T6 oracle depends on the baseline decision; T14 on the freeze commit)
        ↓
Implement RQ2 experiment infrastructure (only after protocol approval)
        ↓
Pilot run → check ceiling effects, failures, rubric; amend protocol if needed (documented)
        ↓
Run the final RQ2 experiment → automated/objective evaluation (expert evaluation excluded from this study)
        ↓
Finalize questionnaire (content review, pilot) and RQ3 protocol (in parallel with RQ2 where possible)
        ↓
Collect participant data (after ethics approval)
        ↓
Analyze → update paper → final manuscript
```
Dependencies: baseline freeze precedes any final generation; the prompt freeze precedes the final run; the multi-week scope decision changes the prompt, schema and validator; ethics approval precedes any expert or participant data; questionnaire validation precedes the main RQ3 collection.

---

## 28. What must NOT be implemented yet

Not before advisor approval of this proposal: any change to prompts, provider code, validator, schema, rule engine, application, database or Alembic migrations; the experiment harness and any data-capture schema; multi-week LLM context; additional providers; the 16-item evaluation form, participant codes, consent screen; study data stores; any experiment or pilot run beyond what the advisor permits; any recruitment or data collection; any paper change.

### 28b. Literature gap (defensible formulation) `[LITERATURE VERIFICATION REQUIRED]`
Existing studies evaluate LLM-generated exercise and running plans by expert rating of directly generated text (e.g., ChatGPT six-week running plans [11]), compare two LLMs and their reproducibility on resistance-training plans [12], and propose knowledge-grounded generation [24] and non-LLM running recommenders [26]. The gap addressed here is the investigation of a **specific hybrid architecture** in which a **deterministic baseline plus LLM personalization** is followed by **server-side validation**, evaluated with a **controlled same-profile, same-baseline comparison of several LLMs** and with **constraint-compliance evaluation across a multi-week running plan**, alongside user perception. This is *not* the claim that no previous work compares LLMs for exercise or running plans: [12] compares LLMs on exercise plans, and whether any study compares several LLMs on running plans is unverified. Before any novelty statement: complete a documented search protocol; read [11], [12] and [24] in full (including whether they describe any post-generation validation and which ChatGPT version(s) were used); update the related-work comparison paragraph accordingly.

---

## Advisor Decision Update — 2 October 2026 — `SUPERSEDED` (2-LLM design; kept for audit trail only)

~~- **2 LLM design approved:** RQ2 compares exactly LLM A vs LLM B (Sections 3.3, 9, 12.2, 26). The earlier 3-LLM starting proposal is superseded.~~
~~- **3 repetitions approved:** 3 repetitions per (runner profile × LLM) combination; repetitions are replicates, not additional independent runners; the runner profile remains the sampling/block unit (Sections 10, 14, 26).~~
- **Expert evaluation excluded from the study design:** no coach/expert rating, expert rubric, inter-rater agreement, expert recruitment, or blinded expert assessment (Sections 16–18, 20, 22, 24, 26). RQ2 now relies solely on automated/objective evaluation criteria. *(Not superseded — still current.)*
- ~~Not resolved by this update (still open/unresolved, preserved from the original proposal): the 24-profile count…the exact statistical test…the Week-1-only vs multi-week LLM-context decision…~~ — see the next section for current status of each item.

## Advisor Decision Update — 2 October 2026 (Gemini-only design)

**This is the current, authoritative design, superseding the 2-LLM comparative design recorded in the update above (issued earlier the same day).**

- **1 LLM (Gemini) CONFIRMED** as the sole personalization model (Sections 8, 12.2, 26); exact model/version to be finalized and recorded before experimental data collection.
- **24 runner profiles CONFIRMED** (Section 11.2, 26) — previously PROPOSED/unconfirmed.
- **3 Gemini repetitions per profile CONFIRMED → 72 Gemini generations** (Sections 9, 10, 14, 26).
- **Deterministic baseline = 24 plans, generated once per profile, NOT repeated** (Sections 9, 14, 26).
- **Total outputs for comparison: 24 baseline + 72 Gemini** — never "96 independent experimental generations," never the superseded "144" or "216" generation figures (Section 11.2).
- **Comparison = deterministic multi-week baseline vs Gemini-personalized multi-week plan** (Sections 6, 7, 9).
- **Exactly 8 automated criteria LOCKED** (Section 16, 26); exact operational definitions remain an OPEN SUB-DECISION — the lock's 8, this document's 16-item draft, and the paper's Table IV 5 are not identical and are not reconciled by this update.
- **Multi-week scope CONFIRMED** (Section 15), resolving the former "Week-1-only vs multi-week" open methodological decision. Pipeline: Runner Profile → Validation → Physiological Calculation → Deterministic Rule-Based Multi-Week Baseline → Gemini Personalization → Server-Side Validation → Gemini-Personalized Multi-Week Plan → Automated Evaluation → Baseline vs Gemini Comparison.
- **Expert evaluation still excluded** (unchanged from the earlier 2 October 2026 decision).
- **No ranking/winner framing:** results report differences across the 8 criteria individually; Gemini is never claimed "better"/"improves"/"superior" without statistical support, and no composite/overall score is used unless explicitly approved (it is not).
- **RQ1 updated** to "Gemini-based personalization" wording (Section 3); RQ3 unchanged.
- **Not resolved by this update** (still open/unresolved): exact Gemini model/version (Section 12.2); exact 8-criteria operational definitions/thresholds (Section 16 — explicitly flagged conflict, not resolved); the exact statistical test (Section 19 — candidates remain PROPOSED only; must account for 72 Gemini outputs nested within 24 profiles); prompt-delivery/Gemini-configuration details (Section 13.2); the baseline rule-engine rebound/taper issues (Section 7); RQ3 design and its relation to RQ2 (Section 20); ethics/BINUS requirements (Section 24); the literature-gap wording (Section 28b); profile demographic composition detail (Section 11.2).

---

## STATUS SUMMARY

**CONFIRMED:** 24 runner profiles; Gemini as the only LLM; 3 Gemini repetitions per profile; 24 baseline plans; 72 Gemini generations; no expert evaluation; exactly 8 automated criteria (count locked); multi-week personalization; baseline vs Gemini comparison.

**OPEN:** exact Gemini model/version; exact 8-criteria definitions/thresholds (explicit conflict between the lock's 8, this document's superseded 16-item draft, and the paper's Table IV 5 — not resolved here); the statistical test; RQ3 sample size; ethics/BINUS requirements; questionnaire validation/pilot; prompt implementation/reproducibility details; profile demographic composition.

---

## Research positioning (restated)

The study draws conclusions only from evidence actually collected. It does not claim that an LLM improves athletic performance, that AI is better than coaches, that any model produces optimal or guaranteed-safe plans, or that any model is the best. Constraint compliance is not physiological optimality; user satisfaction is not athletic effectiveness; expert preference is not objective correctness.

---

## Appendix — Files that would need modification AFTER advisor approval (none modified now)

| File | Why |
|---|---|
| `backend/app/ai/prompts.py` | Prompt versioning/hash; identical delivery of system and user text across providers; optional plan-level context or week-level prompts (Section 15) |
| `backend/app/ai/llm_service.py` | Per-call explicit provider/model; delivery parity (Gemini concatenation vs OpenAI system role); capture of raw response, returned model identifier, usage, timing, errors; experiment mode without silent fallback or `auto`; explicit output cap and other parameters; keep the API key out of stored URLs |
| `backend/app/ai/validator.py` | Non-empty text check; sum-of-distances check; per-week/phase validation if the scope changes; validator version |
| `backend/app/ai/schemas.py` | Week-level or multi-week output schema if the scope changes |
| `backend/app/config.py` | Explicit generation parameters |
| `backend/app/rules/generator.py` | **Changed** (T7 fix, approved and implemented): cutback now updates the progression reference for subsequent build weeks; taper/race-week formulas reviewed and left unchanged |
| `backend/app/routes/plan_routes.py` | Only if production personalization changes (week-level calls) |
| New experiment harness, profile files, analysis scripts (new files) | Run orchestration, evidence capture, reproducible analysis |
| `backend/app/models.py` and a new file in `backend/alembic/versions/` | Only if experiment/evaluation data are stored in the application database (a separate store is an alternative) |
| `backend/app/schemas.py`, `backend/app/routes/evaluation_routes.py`, `frontend/src/pages/EvaluationPage.jsx`, `EvaluationStatsPage.jsx`, `ResearchApp.jsx`, `frontend/src/api.js` | 16 items, agreement scale, participant code, consent screen, neutral defaults, blinding, access control |
| `backend/tests/*` (new tests; e.g., `test_rule_engine.py`, `test_llm_validation.py`, `test_api.py`, `test_multi_week_plans.py`) | Close RQ1 test gaps; prompt snapshot; new validator checks |
| `backend/requirements.txt` (or a lock file) | Pinned environment |
| `PAPER_DRAFT.md`, then regenerate `PAPER_IEEE.docx` with `build_docx.py` | RQ2 wording, III-A, III-I, Table IV, V-C, II-C difference paragraph, II-F gap, abstract, contributions, discussion, limitations, conclusion |
| `RESEARCH_METHODOLOGY_LOCK.md`, `RESEARCH_READINESS_AUDIT.md`, `ADVISOR_REVIEW_PACKAGE.md`, `PAPER_GAPS.md`, `EVIDENCE_MAP.md`, `QUESTIONNAIRE_TRACEABILITY.md`, `LITERATURE_MATRIX.md` (and the reference documents if references change) | Align with the approved methodology |
