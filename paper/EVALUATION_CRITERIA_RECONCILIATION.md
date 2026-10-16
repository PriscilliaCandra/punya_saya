# EVALUATION_CRITERIA_RECONCILIATION

**Purpose:** reconcile the non-aligned evaluation-criteria lists currently scattered across `RESEARCH_METHODOLOGY_LOCK.md` (§5), `RESEARCH_METHODOLOGY_COMPARATIVE_PROPOSAL.md` (§16, superseded 16-item draft), `PAPER_DRAFT.md` (Table IV, 5 items), and the advisor-facing summary documents, into one candidate 8-criterion rubric for advisor review.

**Status of this document: ANALYSIS AND PROPOSAL ONLY. Nothing in Section 5/6 is advisor-approved.** This file does not edit, supersede, or lock any other document. `PAPER_DRAFT.md` and `PAPER_IEEE.docx` were read only, not modified. No source code, database, or git state was touched.

**Locked design facts assumed as given (not re-decided here):** 24 synthetic runner profiles; 1 LLM (Gemini); 3 Gemini repetitions per profile → 72 Gemini generations; 24 deterministic baseline plans (generated once, not repeated); comparison = deterministic multi-week baseline vs Gemini-personalized multi-week plan; no expert evaluation; exactly 8 automated/objective evaluation criteria (count locked, definitions open); multi-week personalization scope (Gemini receives sufficient multi-week context, not Week-1-only).

---

## 1. Current Study Design

| Element | Value |
|---|---|
| Profiles | 24 synthetic vignettes (stratified: experience level × target distance × injury presence, plus edge-case coverage) |
| Conditions | Deterministic baseline (24, generated once) vs Gemini-personalized (72 = 24 × 3 repetitions) |
| Unit of analysis | Profile × condition cell; profile is the block/sampling unit; Gemini repetitions are nested replicates, not independent samples |
| Scope | Multi-week (confirmed); Gemini receives sufficient multi-week context, not just Week 1 |
| Expert evaluation | Excluded entirely from the study |
| Criteria count | Locked at exactly 8; **definitions not yet reconciled — this is the open problem this document addresses** |
| Reporting | Per-criterion only; no composite score; no weights; no ranking/"winner" framing; Gemini must never be declared "better"/"superior"/"improves" without a chosen statistical test |
| Statistical test | Not yet chosen (out of scope for this document) |

---

## 2. Existing Criteria Across Documents

### 2.1 `RESEARCH_METHODOLOGY_LOCK.md` §5 (8-item draft rubric)

| # | Name | Definition (as stated) | Automatable? | Baseline-applicable? | Gemini-applicable? | Category |
|---|---|---|---|---|---|---|
| L1 | Runner-profile consistency | Text doesn't contradict profile (goal, experience, days, injury); injury content present when reported | Mostly (string/number extraction); "contradiction" check partly heuristic | N (baseline has no personalization text) | Y | A |
| L2 | Pace consistency | `pace_target`/`intensity_zone` equal baseline; text-quoted paces equal zone table | Y | N (trivially identical to itself) | Y | B |
| L3 | Weekly-volume consistency | `weekly_mileage_km`/`distance_km` equal baseline within tolerance; text numbers match | Y | N (trivial) | Y | B |
| L4 | Workout-distribution consistency | Same day set, workout types, rest/training-day counts as baseline | Y | N (trivial) | Y | B |
| L5 | Progression consistency | Text statements about progression/load/taper consistent with baseline multi-week progression | Y (rule-based, now that multi-week is confirmed) | N (baseline has no text) | Y | D |
| L6 | Output completeness | All schema text fields present & non-empty per day; plan-level fields non-empty | Y | N (baseline has no text fields to check) / Y if redefined structurally | Y | C |
| L7 | Personalization (automated proxy) | Degree of specific profile-fact use in text, via rule-based checks only | Y (proxy only) | N | Y | A |
| L8 | Reliability/efficiency | HTTP errors, timeouts, invalid JSON, latency, tokens, cross-repetition variability | Y | N (baseline is not an API call) | Y (Gemini only) | E |

### 2.2 `RESEARCH_METHODOLOGY_COMPARATIVE_PROPOSAL.md` §16 (superseded 16-item draft, kept as source material)

| # | Name | Category (mapped) |
|---|---|---|
| P1 | Output schema compliance | C |
| P2 | Required-field completeness | C |
| P3 | Runner-profile consistency | A |
| P4 | Goal consistency | A |
| P5 | Workout-type consistency | B |
| P6 | Intensity-zone consistency | B |
| P7 | Pace consistency | B |
| P8 | Distance consistency | B |
| P9 | Weekly-mileage consistency | B |
| P10 | Rest-day consistency | B |
| P11 | Long-run constraint | B |
| P12 | Progression consistency | D |
| P13 | Cutback-week consistency | D |
| P14 | Taper consistency | D |
| P15 | Absence of duplicate/conflicting workouts | C |
| P16 | Safety/constraint violations | C/E (aggregation of B-violations + flagged-content checks) |

### 2.3 `PAPER_DRAFT.md` Table IV (5-item draft, READ ONLY, not edited)

| # | Name | Category (mapped) |
|---|---|---|
| D1 | Format validity | C |
| D2 | Constraint consistency | B |
| D3 | Structural consistency | B/C |
| D4 | Personalization quality | A (currently defined as "expert rubric score" — contradicts the no-expert-evaluation decision; flagged, not fixed, per the read-only constraint on this file) |
| D5 | Efficiency | E |

### 2.4 Advisor-facing summary documents (`ADVISOR_DECISION_SHEET_COMPARATIVE.md`, `ADVISOR_METHODOLOGY_QA.md`, `RESEARCH_READINESS_AUDIT.md`, `ADVISOR_REVIEW_PACKAGE.md`)

All four restate the same candidate 8-name list (introduced in the Advisor Decision Update, 2 Oct 2026): **profile consistency, goal consistency, physiological/pace consistency, weekly volume/mileage consistency, workout structure, intensity constraints, progression/recovery constraints, completeness/constraint violations.** All four explicitly flag this list as *not yet reconciled* against the lock's own §5 list and the paper's Table IV, and treat it as a naming convention, not an operational definition — no measurement method, data fields, or scoring rule is attached to it in any of the four documents. `RESEARCH_READINESS_AUDIT.md` additionally restates the lock's 8-item rubric verbatim with added critique columns (reused as Section 2.1 above) and contributes the key cross-cutting finding that **criteria 2–4 in the lock's list (and the validator-overlap items in the 16-item draft) measure compliance with the validator's own instructions, not independent evidence of plan quality** — i.e., several "distinct" criteria are one family wearing different names. `PAPER_GAPS.md` does not define criteria itself; it only flags that Table IV's count (5) does not match the locked count (8) and that this is unresolved.

---

## 3. Overlap and Redundancy Analysis

For each candidate merge, the conceptual distinction is stated first; a merge is proposed only where no surviving distinction remains.

**(a) Profile consistency vs personalization (L1/L7, P3, "profile consistency" in the advisor list).**
*Distinction considered:* "profile consistency" could mean non-contradiction of hard facts (goal race, experience, days, injury) — a correctness check; "personalization" could mean the depth/specificity of the use of those facts — a richness/engagement check.
*Verdict:* in the current design both are operationalized identically (rule-based extraction of profile facts from text, checked against the profile record) because no expert judge exists to assess "richness" independently of fact use. There is no second, independently measurable construct behind "personalization" once expert evaluation is excluded — recommend **merging into one criterion** (named "Profile/Goal Alignment" below), while explicitly scoping it to fact non-contradiction + fact-coverage count, and stating that it is a proxy, not a quality judgment.

**(b) Goal consistency vs profile consistency (P4 vs L1/P3).**
*Distinction considered:* goal consistency (race distance/time/pace stated correctly) is a strict subset of profile facts; profile consistency as drafted already lists "goal race, goal time" as one of the facts it checks.
*Verdict:* goal consistency is not conceptually separate from profile consistency — it is one category of profile fact. **Merge into the same criterion as (a)** rather than keeping as a sibling criterion; this also frees a criterion slot.

**(c) Pace consistency vs intensity-zone/intensity constraints (L2, P6/P7, "physiological/pace consistency" and "intensity constraints" in the advisor list).**
*Distinction considered:* pace (a numeric target, e.g. min/km) and intensity zone (a categorical label, e.g. "Threshold") are different data types describing the same physiological construct — the workout's targeted effort level — and in the implemented schema they are emitted together per workout (`pace_target`, `intensity_zone`).
*Verdict:* they are two fields of one underlying construct (target effort level), checked by the same mechanism (string/number equality against the baseline). **Merge into one criterion** ("Pace/Intensity Fidelity") rather than keeping two line items that would always move together (any case that breaks pace equality is overwhelmingly likely to break zone equality too, since both derive from the same baseline computation) — keeping them separate would overstate independent evidence.

**(d) Mileage/volume consistency vs workout structure/distribution (L3/L4, P8/P9/P10, "weekly volume/mileage consistency" and "workout structure" in the advisor list).**
*Distinction considered:* mileage consistency checks *quantities* (distance_km, weekly_mileage_km numeric equality); workout structure/distribution checks *qualitative arrangement* (which days are training vs rest, workout type per day, day-count by type). A plan could preserve total mileage while rearranging which day carries which distance, or vice versa — these are genuinely separable failure modes (e.g., Gemini could swap a long run to the wrong day while keeping total mileage identical).
*Verdict:* **keep as two distinct criteria** — this is not a naming duplicate, it is two different constructs that can fail independently. This matches the audit's observation that they are "one family" only in the weaker sense of "both validator-derived," not in the sense of being the same measurement.

**(e) Workout-type consistency vs workout-structure consistency (P5 vs L4/P10).**
*Distinction considered:* "workout type" (easy/long/quality/rest) per day and "structure" (day set, rest-day count, training-day count) are both checked by the same validator sub-routine and almost always co-vary (a day-type mismatch is usually also a day-set mismatch).
*Verdict:* **merge** workout-type and day-set/rest-day/training-day-count checks into a single "Workout Structure & Type Fidelity" criterion (distinct from mileage, per (d) above).

**(f) Progression consistency vs cutback/taper consistency vs "progression/recovery constraints" (L5, P12/P13/P14).**
*Distinction considered:* progression (week-over-week volume trend), cutback weeks (scheduled recovery dips), and taper (pre-race volume reduction) are phase-specific instances of the same underlying construct — adherence of the multi-week volume *trajectory* to the baseline's documented schedule — not three independent constructs. All three are measured the same way (per-week deviation from the baseline schedule) once multi-week scope is confirmed.
*Verdict:* **merge into one multi-week criterion** ("Multi-Week Progression Fidelity") that explicitly enumerates build/cutback/taper weeks as sub-checks within it, rather than three separate top-level criteria — this avoids triple-counting the same underlying trajectory-fidelity construct while still requiring the operationalization to check all three phases (see Section 7).

**(g) Output completeness vs constraint-violation aggregation (L6/P2 vs P16/"completeness/constraint violations" combined advisor name).**
*Distinction considered:* completeness (are required fields present/non-empty) is a structural-validity check; constraint-violation aggregation (count of criterion 2–for failures) is a rollup of other criteria's failures, not an independent construct.
*Verdict:* the advisor list's own naming ("completeness/constraint violations") already acknowledges these are two things glued together. **Split them**: keep completeness as its own criterion (construct C); do not create a separate "constraint violations" criterion, since it would simply recount failures already captured by the mileage/structure/pace criteria above and would risk double-counting in any later statistical analysis. This also directly addresses the audit's warning against "reporting as independent evidence" what the validator already enforces once.

**(h) Reliability/efficiency (L8, D5) vs everything else.**
*Distinction considered:* this is the only criterion that is inherently about the Gemini *process* (API behavior, latency, token cost, cross-repetition variability) rather than the *content* of a plan.
*Verdict:* **keep as its own criterion** but flag explicitly (Section 7) that it is Gemini-only — the deterministic baseline has no API call to measure.

**(i) Safety/constraint-violation flags (P16b, free-text safety keyword detection).**
*Distinction considered:* flagged unsafe advice (e.g., "run through sharp pain") is conceptually different from numeric constraint fidelity, but was explicitly tied to expert review in the superseded 16-item draft (P16 required "(b) rule list plus expert review").
*Verdict:* since expert evaluation is excluded from the study, and keyword-based safety detection has "low recall" per the proposal's own caveat, this is **not included** as one of the 8 — recommend flagging it as an unresolved safety limitation in the paper's limitations section rather than forcing it into an automated criterion that cannot do the job it was designed for.

---

## 4. Personalization vs Constraint Coverage

Mapping the surviving candidate criteria (Section 5) against the four coverage buckets from the task brief:

| Coverage bucket | Candidate criteria that cover it | Observation |
|---|---|---|
| (A) Personalization — does Gemini reflect profile/goal | Profile/Goal Alignment (C1) | **Only 1 of 8** criteria addresses this directly |
| (B) Constraint fidelity — does Gemini preserve deterministic constraints | Pace/Intensity Fidelity (C2), Weekly-Volume/Mileage Fidelity (C3), Workout Structure & Type Fidelity (C4) | **3 of 8** |
| (C) Output validity — structurally complete/parseable | Schema & Completeness Validity (C5) | 1 of 8 |
| (D) Multi-week behavior | Multi-Week Progression Fidelity (C6) | 1 of 8 |
| (E) Other / process | Reliability & Stability (C7) | 1 of 8 |
| (A, revisited) | Personalization Depth/Specificity (C8) | 1 of 8 |

**Imbalance flagged explicitly (per Task 3):** of the 8 criteria, **4 (C2–C5, roughly half) are direct restatements or close derivatives of what `ai/validator.py` already enforces as a production gate** (pace, mileage, structure, schema). Only **2 criteria (C1, C8)** address personalization quality/profile reflection, and both are automated proxies rather than true quality judgments, since expert evaluation is excluded. This mirrors the cross-cutting finding already flagged in `RESEARCH_READINESS_AUDIT.md` §4: the rubric as drafted across all source documents is **weighted toward constraint compliance, not toward personalization**, because compliance is cheap to automate and personalization quality is not, in the absence of an expert judge. This imbalance is not fixed by the candidate set below — it is a structural consequence of "automated/objective criteria only, no expert evaluation" — but the candidate set deliberately keeps 2 of 8 slots on personalization rather than letting compliance sub-checks crowd out all 8, which several of the source drafts (particularly the superseded 16-item list) effectively did.

---

## 5. Candidate 8-Criteria Framework

**CANDIDATE ONLY — NOT ADVISOR-APPROVED.**

| # | Name | Construct category |
|---|---|---|
| C1 | Profile/Goal Alignment | A |
| C2 | Pace/Intensity Fidelity | B |
| C3 | Weekly-Volume/Mileage Fidelity | B |
| C4 | Workout Structure & Type Fidelity | B |
| C5 | Schema & Completeness Validity | C |
| C6 | Multi-Week Progression Fidelity | D |
| C7 | Reliability & Stability | E (Gemini-only, see Section 7) |
| C8 | Personalization Depth/Specificity | A |

No composite score. No weights. Each reported as a separate outcome per the locked design.

---

## 6. Criterion Operationalization Table

### C1 — Profile/Goal Alignment
1. **Definition:** The personalized text does not contradict any profile fact (goal race distance, goal time, experience level, training days/preferred days, injury/limitation note) and references the injury note when one exists.
2. **What is measured:** Count of contradictions between text-stated facts and the stored profile record; presence/absence of injury-relevant content when `injury_limitations` is non-empty.
3. **Unit:** Count of contradictions (integer); presence flag (bool) for injury content.
4. **Scoring:** Pass/fail per fact category + contradiction count; not a composite score with C8.
5. **Required data fields:** `runner_profile` record (goal_race_distance, goal_race_time, experience_level, training_days_per_week, preferred_days, injury_limitations); parsed Gemini text fields (`coach_overview`, `personalized_insights`, `ai_personalization_summary`, `why_this_plan_was_generated`, per-day `purpose`/`recovery_instruction`).
6. **Baseline evaluation:** N/A as free text (baseline has no personalization text) — report as "not applicable, baseline produces no natural-language profile reference" rather than a forced score (see Section 7).
7. **Gemini evaluation:** Rule-based extraction (regex/keyword + numeric comparison) of fact mentions in text vs. the profile record.
8. **Why it belongs:** Directly answers construct (A) — the one personalization-facing criterion with a defensible automated oracle (the profile record itself).
9. **Replaces/merges:** L1 (lock), P3+P4 (proposal's "profile consistency" + "goal consistency" — merged per Section 3(a)/(b)), part of the advisor list's "profile consistency" + "goal consistency" names.

### C2 — Pace/Intensity Fidelity
1. **Definition:** `pace_target` and `intensity_zone` fields for every workout equal the deterministic baseline's values exactly; any pace or zone name quoted in free text matches the baseline's zone table.
2. **What is measured:** Exact-match rate on structured fields; count of text-quoted paces/zones not found in the baseline zone table.
3. **Unit:** Proportion of workouts matching (0–1); count of text mismatches.
4. **Scoring:** Pass/fail per workout for structured fields; mismatch count for free text.
5. **Required data fields:** Baseline `pace_target`/`intensity_zone` per workout; Gemini-plan equivalents; free text fields for number/zone extraction.
6. **Baseline evaluation:** Trivially 1.0 (baseline compared to itself) — report as a reference point ("100% by construction"), not a meaningful baseline score; stated explicitly to avoid misreading it as evidence.
7. **Gemini evaluation:** String/number equality check against baseline, per repetition, aggregated per profile cell.
8. **Why it belongs:** Core constraint-fidelity measure (construct B); directly reuses the existing validator logic, so it is cheap and well-defined.
9. **Replaces/merges:** L2 (lock); P6+P7 (proposal's "intensity-zone consistency" + "pace consistency" — merged per Section 3(c)); advisor list's "physiological/pace consistency" + "intensity constraints" (merged).

### C3 — Weekly-Volume/Mileage Fidelity
1. **Definition:** `distance_km` per workout and `weekly_mileage_km` per week equal the baseline within the validator's tolerance (±0.05 km distance, ±0.15 km weekly mileage); per-week distances sum to the stated weekly mileage; any distance quoted in free text matches the corresponding plan value.
2. **What is measured:** Absolute deviation per field; sum-consistency check (not currently in the validator per the audit's note); text-number mismatch count.
3. **Unit:** Deviation in km (continuous); pass/fail at the tolerance threshold.
4. **Scoring:** Deviation distribution (median, range) + pass/fail rate at the frozen tolerance; sensitivity check at exact equality is a secondary analysis, not part of the primary score.
5. **Required data fields:** Baseline and Gemini `distance_km` per day, `weekly_mileage_km` per week; free-text distance mentions.
6. **Baseline evaluation:** Trivially 1.0 by construction (same caveat as C2).
7. **Gemini evaluation:** Per-repetition deviation computation, aggregated per profile cell across all weeks (not Week 1 only).
8. **Why it belongs:** Core constraint-fidelity measure (construct B); distinct failure mode from C4 (quantity vs. arrangement — see Section 3(d)).
9. **Replaces/merges:** L3 (lock); P8+P9 (proposal's "distance consistency" + "weekly-mileage consistency"); advisor list's "weekly volume/mileage consistency."

### C4 — Workout Structure & Type Fidelity
1. **Definition:** The set of training/rest days, the workout type assigned to each day (easy/long/quality/rest), the rest-day count, and the training-day count all equal the baseline, for every week.
2. **What is measured:** Day-set match; per-day workout-type match; rest/training-day count match.
3. **Unit:** Pass/fail per sub-check, per week; proportion of weeks fully matching.
4. **Scoring:** Pass/fail per sub-check + violation-category counts (which sub-check failed), never collapsed into one undifferentiated pass/fail.
5. **Required data fields:** Baseline and Gemini per-week day list, workout type per day, rest-day/training-day counts; profile's `training_days_per_week`.
6. **Baseline evaluation:** Trivially 1.0 by construction (same caveat as C2/C3).
7. **Gemini evaluation:** Validator sub-check logic extended to run across all weeks, aggregated per profile cell.
8. **Why it belongs:** Constraint-fidelity measure (construct B) capturing arrangement failures that C3's numeric check cannot catch (Section 3(d)).
9. **Replaces/merges:** L4 (lock); P5+P10 (proposal's "workout-type consistency" + "rest-day consistency" — merged per Section 3(e)); advisor list's "workout structure."

### C5 — Schema & Completeness Validity
1. **Definition:** Output parses as valid JSON and conforms to the `AIPersonalizedPlan` schema; every required text field is present and non-empty for each non-rest day (`warmup_cooldown`, `workout_execution`, `recovery_instruction`, `purpose`) and at the plan level (`coach_overview`, `personalized_insights`, `ai_personalization_summary`, `why_this_plan_was_generated`).
2. **What is measured:** Parse success; schema-validation success; per-field non-empty rate.
3. **Unit:** Pass/fail (parse/schema); proportion of required fields non-empty (0–1).
4. **Scoring:** Pass/fail for parse/schema; proportion for completeness; truncation flagged separately as a sub-category, not merged into the proportion.
5. **Required data fields:** Raw HTTP response body; parsed JSON; schema definition; per-field presence/length.
6. **Baseline evaluation:** Applicable in modified form — the baseline is schema-valid JSON by construction and has no optional text fields to leave empty, so it scores as "structurally valid, text-completeness not applicable" (see Section 7) rather than a forced numeric completeness score.
7. **Gemini evaluation:** Parse + schema check per repetition; field-level non-empty check per repetition.
8. **Why it belongs:** Construct (C) — the only criterion addressing whether the output is even usable, independent of whether its content is correct.
9. **Replaces/merges:** L6 (lock); P1+P2 (proposal's "output schema compliance" + "required-field completeness" — merged, since in this design a non-parsing/non-schema-valid output and an incomplete one are both captured by one "is this plan usable" criterion rather than two); D1 (paper's "format validity"); advisor list's "completeness" (the "constraint violations" half of that name is intentionally dropped per Section 3(g)).

### C6 — Multi-Week Progression Fidelity
1. **Definition:** Across the full multi-week plan, weekly training volumes follow the baseline's progression schedule (build weeks, cutback weeks, taper/race week), and any textual statement about progression/load/taper does not contradict that schedule.
2. **What is measured:** Per-week numeric deviation from the baseline's scheduled volume, computed separately within each phase (build/cutback/taper) so a cutback-week or taper-week failure is distinguishable from a build-week failure; a rule-based contradiction check on progression-related text statements.
3. **Unit:** Per-week deviation (continuous, km or %); phase-tagged pass/fail; contradiction count for text.
4. **Scoring:** Deviation distribution per phase + pass/fail rate per phase; text-contradiction count reported separately, never averaged into one number that hides which phase or which repetition failed.
5. **Required data fields:** Per-week baseline volume and phase label (build/cutback/taper) for every week 1..N; per-week Gemini volume; free-text progression/taper statements.
6. **Baseline evaluation:** Trivially 1.0 by construction (same caveat as C2–C4). **RESOLVED (originally an open item):** the baseline's post-cutback rebound (≈+25%) has been fixed in code and no longer applies to freshly generated baselines; taper anchored to starting mileage rather than peak is confirmed to be the intended, documented methodology (`PAPER_DRAFT.md` Table II), not an engineering limitation requiring a decision. The fix-or-document decision in the lock (§3, T7) has been made (fix the rebound; document the taper as-is) — this criterion can be scored against the fixed baseline once the baseline plans are generated.
7. **Gemini evaluation:** Per-repetition, per-week, per-phase deviation and contradiction check, aggregated per profile cell; explicitly spans the entire plan duration, not Week 1.
8. **Why it belongs:** The only criterion addressing construct (D), multi-week coherence — required because the study's locked design confirms multi-week scope, and this criterion is "now measurable" (per all four advisor documents) precisely because of that confirmation.
9. **Replaces/merges:** L5 (lock); P12+P13+P14 (proposal's "progression consistency" + "cutback-week consistency" + "taper consistency" — merged per Section 3(f), with phase tagging preserved as sub-checks rather than three top-level criteria); advisor list's "progression/recovery constraints."

### C7 — Reliability & Stability
1. **Definition:** The rate and nature of generation failures (HTTP errors, timeouts, malformed/non-JSON output, truncation) and the run-to-run variability of Gemini's output across the 3 repetitions per profile.
2. **What is measured:** Failure counts by category; latency; token usage; agreement of validator outcome across repetitions; variability of numeric deviations and text-number mismatches across repetitions.
3. **Unit:** Counts (errors, timeouts); ms (latency); token counts; proportion of repetitions agreeing on pass/fail.
4. **Scoring:** Counts/medians per category; no pass/fail threshold invented.
5. **Required data fields:** HTTP status, error type, latency_ms, tokens_in/out, truncated flag per call; per-repetition validator verdicts within a profile cell.
6. **Baseline evaluation:** **Not applicable** — the deterministic baseline is not an API call and is not repeated, so it has no failure/latency/variability distribution to measure. This is the one criterion that is explicitly Gemini-only (see Section 7).
7. **Gemini evaluation:** Aggregated across the 3 repetitions per profile, and across all 24 profiles for pooled reporting.
8. **Why it belongs:** Construct (E); captures the operational/process dimension that no content-focused criterion covers, and directly operationalizes the locked design's requirement to report "stability: agreement across the 3 Gemini repetitions per profile."
9. **Replaces/merges:** L8 (lock); D5 (paper's "efficiency"); not present by this name in the proposal's 16-item list (closest analogue is the general reliability discussion in §18 Family G of the proposal, reused here as a top-level criterion rather than a metrics appendix).

### C8 — Personalization Depth/Specificity
1. **Definition:** The degree to which the personalized text goes beyond generic phrasing to use the runner's specific, concrete profile facts (named goal race, named injury, specific weekly-mileage context) in a way that is internally non-contradictory (reuses the C1 contradiction check as a gate) — measured by automated/rule-based proxy only, since no expert judge is used.
2. **What is measured:** Count/rate of specific-fact mentions per text field; ratio of specific vs. generic phrasing markers (e.g., presence of the runner's actual race distance/injury term vs. templated boilerplate); this is explicitly a **coverage/specificity proxy**, not a quality judgment.
3. **Unit:** Count of specific-fact mentions (integer); proportion of eligible fact slots mentioned (0–1).
4. **Scoring:** Proportion of profile-fact slots referenced in text, reported per text field and pooled; no attempt to score "good" vs. "bad" personalization, only "specific" vs. "generic."
5. **Required data fields:** Profile record (same fields as C1); parsed Gemini text fields; a fixed list of "genericness" markers / boilerplate phrases to exclude from the count (to be defined before scoring, since this list does not yet exist in any source document).
6. **Baseline evaluation:** **Not applicable** — the deterministic baseline has no free text to be specific or generic about; report explicitly as "not applicable, Gemini-only secondary outcome" (see Section 7) rather than scoring it 0.
7. **Gemini evaluation:** Rule-based extraction per repetition, aggregated per profile cell.
8. **Why it belongs:** The second of only two personalization-facing criteria (construct A); included specifically to prevent the rubric from collapsing entirely into constraint-compliance checks (see Section 4's imbalance finding), even though it is acknowledged to be a weak proxy for genuine personalization quality in the absence of expert evaluation.
9. **Replaces/merges:** L7 (lock, "personalization (automated proxy)"); D4 (paper's "personalization quality" — note: D4 as currently worded in `PAPER_DRAFT.md` calls for an "expert rubric score," which directly conflicts with the locked exclusion of expert evaluation; this conflict is flagged here, not resolved, since `PAPER_DRAFT.md` is read-only in this task); advisor list's residual "personalization" framing (the advisor list itself has no explicit 8th-named slot for this — it is implied by "profile consistency" doing double duty, which Section 3(a) argues should be split back out as its own criterion rather than conflated with C1).

---

## 7. Baseline vs Gemini Comparability

Explicit answer to "can this be meaningfully evaluated for BOTH sides?" for each of the 8:

| # | Criterion | Baseline-evaluable? | Treatment |
|---|---|---|---|
| C1 | Profile/Goal Alignment | **No** — baseline produces no free text to check for contradiction/injury mention | Gemini-only secondary outcome. Report explicitly as "not applicable to baseline" rather than scoring the baseline 0 or 1 by default, since a 0 would misleadingly read as "the baseline contradicts the profile" when in fact it makes no textual claims at all. |
| C2 | Pace/Intensity Fidelity | **Trivially yes, but uninformative** — the baseline is compared to itself and will always score 1.0 by construction | Retain for comparability (it IS one of the two "sides" of RQ2), but document explicitly that the baseline's score is a reference point, not independent evidence; the comparison's informative content is entirely in Gemini's deviation from it. |
| C3 | Weekly-Volume/Mileage Fidelity | **Trivially yes, but uninformative** (same reasoning as C2) | Same treatment as C2. |
| C4 | Workout Structure & Type Fidelity | **Trivially yes, but uninformative** (same reasoning as C2) | Same treatment as C2. |
| C5 | Schema & Completeness Validity | **Partially** — JSON/schema validity is meaningfully comparable (both sides produce JSON); the "required text field non-empty" sub-check is not meaningful for the baseline, which has no personalization text fields to populate | Report parse/schema validity for both sides; report completeness-of-text-fields as Gemini-only. |
| C6 | Multi-Week Progression Fidelity | **Trivially yes, but uninformative** — the baseline's progression IS the schedule being compared against, so it is tautologically "compliant" with itself; what is comparable and informative is whether Gemini's *stated* progression text is consistent with that schedule | Treat the baseline side as the reference schedule, not a scored participant; score Gemini's numeric and textual fidelity to it. |
| C7 | Reliability & Stability | **No** — the baseline is not an API call and is not repeated | Gemini-only secondary outcome (explicitly flagged in Section 6.C7 item 6). |
| C8 | Personalization Depth/Specificity | **No** — the baseline has no free text | Gemini-only secondary outcome, same treatment as C1. |

**Summary:** of the 8, only **C5** offers a genuinely informative baseline-vs-Gemini comparison on both a trivial and a non-trivial sub-check; **C2/C3/C4/C6** are "comparable" only in the degenerate sense that the baseline always scores at the reference value, so the real comparison is "how far does Gemini deviate from this known reference," which is still useful and intended; **C1, C7, C8 are Gemini-only** and should be reported as such rather than forced into a two-sided comparison that would misrepresent what the baseline does and does not do. This is consistent with the locked design's own statement that the baseline is "a controlled reference/input condition... never ground truth for overall plan quality" — several criteria are structured around measuring Gemini's distance from that reference, not around giving the baseline an independent score.

---

## 8. Traceability to Existing Documents

| Candidate | Source document(s) | Original criterion name(s) | Disposition | Rationale |
|---|---|---|---|---|
| C1 Profile/Goal Alignment | Lock §5 (L1); Proposal §16 (P3, P4); Table IV (none directly); Advisor docs ("profile consistency", "goal consistency") | Runner-profile consistency; Goal consistency | Merged + renamed | Section 3(a)/(b): goal facts are a subset of profile facts; both measured by the same fact-extraction mechanism |
| C2 Pace/Intensity Fidelity | Lock §5 (L2); Proposal §16 (P6, P7); Advisor docs ("physiological/pace consistency", "intensity constraints") | Pace consistency; Intensity-zone consistency | Merged + renamed | Section 3(c): two fields of one effort-level construct |
| C3 Weekly-Volume/Mileage Fidelity | Lock §5 (L3); Proposal §16 (P8, P9); Table IV ("constraint consistency", partial); Advisor docs ("weekly volume/mileage consistency") | Weekly-volume consistency; Distance consistency; Weekly-mileage consistency | Merged + renamed | Numeric quantity checks on the same measurement family |
| C4 Workout Structure & Type Fidelity | Lock §5 (L4); Proposal §16 (P5, P10); Table IV ("structural consistency"); Advisor docs ("workout structure") | Workout-distribution consistency; Workout-type consistency; Rest-day consistency | Merged + renamed | Section 3(e): arrangement checks sharing one validator sub-routine |
| C5 Schema & Completeness Validity | Lock §5 (L6); Proposal §16 (P1, P2); Table IV ("format validity") | Output completeness; Output schema compliance; Required-field completeness | Merged + renamed | Section 3(g): structural usability of the output |
| C6 Multi-Week Progression Fidelity | Lock §5 (L5); Proposal §16 (P12, P13, P14); Advisor docs ("progression/recovery constraints") | Progression consistency; Cutback-week consistency; Taper consistency | Merged + renamed | Section 3(f): phase-specific instances of one trajectory-fidelity construct |
| C7 Reliability & Stability | Lock §5 (L8); Table IV ("efficiency") | Reliability/efficiency; Efficiency | Retained + renamed | No conceptual overlap found; kept as the sole process-level criterion |
| C8 Personalization Depth/Specificity | Lock §5 (L7); Table IV ("personalization quality", conflicting expert-rubric wording not carried over) | Personalization (automated proxy); Personalization quality | Retained + reformulated | The only slot left for construct (A) beyond C1; reformulated to explicitly drop Table IV's expert-rubric definition, which contradicts the locked no-expert-evaluation decision |

**Not carried forward into the candidate 8** (with reasons): Proposal P11 (long-run constraint) — folded conceptually into C4/C6 rather than kept separate, since it is one more instance of the same rule-conformance check already covered there; Proposal P15 (absence of duplicate/conflicting workouts) — folded into C4 as a sub-check rather than a top-level criterion; Proposal P16 (safety/constraint-violation flags) — explicitly excluded per Section 3(i), since it depended on expert review that is no longer part of the design and automated keyword detection was already flagged by its own source document as having low recall.

**Literature support:** none of the 8 candidates above currently cites literature for its specific operationalization; the lock and proposal documents note that literature citations attached to the superseded lists were "context/design inspiration only, not proof of validity of these specific measures." Per the task constraint against inventing citations, every candidate's literature basis is marked **[LITERATURE SUPPORT TO VERIFY]**.

---

## 9. Remaining Questions for Advisor Approval

1. Is the merge logic in Section 3 acceptable, particularly (f) — collapsing progression/cutback/taper into one criterion with internal phase sub-checks, rather than three separate top-level criteria (as the superseded 16-item draft and some advisor-summary phrasing might imply)?
2. Is it acceptable that 3 of the 8 criteria (C1, C7, C8) are Gemini-only with no baseline-side score, and that 4 more (C2, C3, C4, C6) are "comparable" only in the degenerate sense that the baseline scores at the reference value by construction? Section 7 proposes this is unavoidable given what the deterministic baseline actually produces (no free text, no repeated API calls) — but it is an explicit methodological choice that needs sign-off, since it affects how "8 criteria, baseline vs Gemini" can honestly be described in the paper.
3. `PAPER_DRAFT.md` Table IV's "Personalization quality" criterion currently specifies "Expert rubric score" as its measure (read-only; not edited by this document) — this directly conflicts with the locked exclusion of expert evaluation. The candidate C8 in this document replaces that definition with an automated proxy. Does the advisor want Table IV's wording corrected in a future, separate edit (out of scope here), and does the automated proxy in C8 adequately substitute for what Table IV originally intended?
4. **RESOLVED:** the post-cutback rebound (~+25%) and taper-anchored-to-starting-mileage behaviors of the baseline rule engine were an open "fix or document" decision (lock §3, T7); the rebound has been fixed in code, and the taper anchoring has been confirmed correct and left unchanged. C6 (Multi-Week Progression Fidelity) — superseded by E4 in the later Option-A design — can now be scored once baselines are generated, since the rule engine is no longer subject to change before the freeze on this point.
5. Does C5's partial baseline/Gemini split (parse/schema shared, completeness Gemini-only) need a more formal "comparable sub-score vs. not-comparable sub-score" reporting convention across all 8 criteria, so the paper does not imply a symmetric 8-criteria-both-sides comparison where none exists for several criteria?
6. Thresholds/tolerances for C2/C3 (currently inherited from the existing validator: ±0.05 km distance, ±0.15 km weekly mileage) were themselves flagged in the lock as "a design choice" requiring a sensitivity analysis at exact equality — should that sensitivity analysis be folded into this rubric's scoring convention, or treated as a separate analysis step?
7. Should the "genericness marker list" required to operationalize C8 (Section 6.C8 item 5) be developed by the researcher alone, or does it need advisor/content review given it directly shapes what counts as "specific" personalization?

---

## 10. Recommended Advisor Decision

This document recommends that the advisor review and either approve, amend, or reject the candidate 8-criteria framework in Section 5/6 as the operational definitions for the already-locked count of exactly 8 automated/objective evaluation criteria. If approved, the next steps (out of scope for this document) would be: (a) correct `PAPER_DRAFT.md` Table IV's wording in a separate, explicitly authorized edit; (b) extend `ai/validator.py` and the (not-yet-built) experiment harness to compute C1–C8 across the full multi-week context; (c) resolve the Section 9 open questions, particularly the baseline rule-engine fix-or-document decision that blocks C6.

**Candidate framework only — not yet advisor-approved.**
