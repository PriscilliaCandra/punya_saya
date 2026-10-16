# EVALUATION_CRITERIA_OPTION_A_DESIGN

> **REVISION NOTE (post-`EVALUATION_CRITERIA_FINAL_CONSISTENCY_REVIEW.md`).** The original §4 definitions of E6 and E7 below used a 9-slot `SLOTS` list that included two fields with no traceable backing field (`vdot_band`, `stated_preference`) and treated several baseline-input fields (`experience_level`, `target_race_distance`/`target_race_time`, `current_weekly_mileage_km`, `training_days_per_week`/`preferred_days`, `plan_duration_weeks`) as independent personalization evidence. The consistency review found that because those fields are themselves inputs the deterministic baseline already uses to compute its own output, a plan's "specificity" on those fields is mechanically the same comparison as E1–E4's constraint-fidelity check against the same baseline-derived number — i.e., not independent evidence, a point `PROFILE_FACT_SLOT_SPECIFICATION.md` §13 had already found for one slot (S5 vs. E3) but had not generalized. E6 and E7's definitions below have been revised accordingly: they now operate over a smaller, baseline-independent slot set (currently: `injury_limitations` only, as Category A; `easy_run_pace` flagged but not adopted, as Category C pending repository confirmation). E1–E8's names, the 8-criterion count, the group structure, and E1–E5/E8 themselves are unchanged. See `PROFILE_FACT_SLOT_SPECIFICATION.md` (also revised) for the full slot classification and `EVALUATION_CRITERIA_FINAL_CONSISTENCY_REVIEW.md` for the review that produced this revision.
>
> **STATUS: METHODOLOGICAL PROPOSAL — PENDING ADVISOR APPROVAL. NOT A LOCKED METHODOLOGY.**
> This document is a design-review deliverable only. It does not edit, supersede, or override `RESEARCH_METHODOLOGY_LOCK.md`, `RESEARCH_METHODOLOGY_COMPARATIVE_PROPOSAL.md`, `PAPER_DRAFT.md`, `EVALUATION_CRITERIA_RECONCILIATION.md`, or any other existing file, all of which were read-only inputs. No code, database, or application file was touched. No git command was run by this task. No experiment was run and no experimental data was generated or fabricated anywhere below — all "expected output" ranges are specification-level, not measured results.

**Inputs read (read-only):** `EVALUATION_CRITERIA_RECONCILIATION.md` (candidate-8 list and its known problems), `RESEARCH_METHODOLOGY_LOCK.md` (§§1–14, the Gemini-only Advisor Decision Update, and the §5 draft rubric), `RESEARCH_METHODOLOGY_COMPARATIVE_PROPOSAL.md` (superseded 16-item list §16, architecture discussion, Table/threats sections), `PAPER_DRAFT.md` (Table IV, the 5-item list: Format validity / Constraint consistency / Structural consistency / Personalization quality ["Expert rubric score"] / Efficiency). `ADVISOR_DECISION_SHEET_COMPARATIVE.md`, `ADVISOR_METHODOLOGY_QA.md`, `RESEARCH_READINESS_AUDIT.md`, and `ADVISOR_REVIEW_PACKAGE.md` were treated as already summarized inside `EVALUATION_CRITERIA_RECONCILIATION.md` §2.4 (all four restate one naming list with no attached operational definitions, and all four flag the list as unreconciled) — their content is incorporated by reference, not re-quoted at length, since the reconciliation document already performed that extraction.

---

## 1. Executive Recommendation

Adopt **8 criteria organized into 4 purpose-tagged groups** (not a forced A/B/C/D taxonomy copied from the brief, but a 2×2 structure that falls out naturally once "what does this measure" and "what does this compare" are separated — see §3):

| ID | Final Name |
|---|---|
| E1 | Constraint Preservation — Pace/Intensity |
| E2 | Constraint Preservation — Volume |
| E3 | Constraint Preservation — Structure |
| E4 | Multi-Week Trajectory Fidelity |
| E5 | Output Validity & Completeness |
| E6 | Profile-Grounded Personalization Coverage |
| E7 | Profile-Grounded Personalization Specificity |
| E8 | Cross-Repetition Stability |

This keeps the candidate-8's core compliance checks (C2–C6 of the reconciliation doc) nearly unchanged — they were already well-specified and are kept as E1–E5 with one structural correction (E4 is explicitly phase-tagged and gated on a baseline decision, not silently scored) — but **replaces the single "Personalization Depth/Specificity" slot with two narrower, independently-defensible criteria (E6, E7)** built only from data already present in the runner profile, and **reframes "Reliability & Stability" (E8) to measure only what the 3-repetition design cannot measure about itself for free** (see §6 and §9 below for why this is not double-counting the repetition design).

Net effect versus the candidate-8: same count (8), same "no composite, no ranking" posture, but the personalization slot is split in two (so the 1-of-8 imbalance the reconciliation doc flagged becomes 2-of-8, matching C1's degree of attention rather than less), and process-level reliability is narrowed so it is not accidentally restating the repetition design as if it were a ninth independent finding.

---

## 2. RQ2 Implication

RQ2 (locked wording, `RESEARCH_METHODOLOGY_LOCK.md` §2): *"How does Gemini-based personalization differ from a deterministic baseline in generating personalized multi-week running training plans while maintaining predefined training constraints?"*

This wording has two clauses that this framework must serve without collapsing into one:
1. **"differ ... in generating personalized ... plans"** → requires criteria that can detect personalization as something distinguishable from mere constraint echoing (E6, E7).
2. **"while maintaining predefined training constraints"** → requires criteria that can detect constraint drift (E1–E4), plus criteria confirming the output is even usable as evidence (E5) and stable enough to trust a single reading (E8).

No single criterion can answer RQ2 alone; the 8-criterion profile is the answer, reported criterion-by-criterion, never averaged into one number that would imply the two clauses trade off against each other (which they do not — they are different constructs measured on different evidence).

---

## 3. Evaluation Framework

The brief suggests a possible A. Constraint Preservation / B. Objective Personalization / C. Output Validity / D. Generation Stability structure. That structure is **adopted**, with one amendment: personalization (B) is split into two criteria rather than one, because "does the plan use the runner's facts at all" (coverage) and "does the plan go beyond templated defaults given those same facts" (specificity/elaboration) are genuinely different failure modes — a plan can mention every profile fact once in a boilerplate sentence (high coverage, low specificity) or build a detailed, fact-dense paragraph around only one fact (low coverage, high specificity). Collapsing them back into one criterion would recreate exactly the "lacks an objective operational definition" problem flagged in the task brief, because a single score could not report which of the two things failed.

| Group | Criteria | Governing question |
|---|---|---|
| A. Constraint Preservation | E1, E2, E3, E4 | Did Gemini preserve the deterministic engine's numeric/structural output? |
| B. Objective Personalization | E6, E7 | Did Gemini visibly use the runner's own profile/goal data, and how richly? |
| C. Output Validity | E5 | Is the output even usable as a plan (parseable, complete)? |
| D. Generation Stability | E8 | Is Gemini's behavior consistent across repeated calls on the same input? |

This is a 2+2+1+1 count rather than 2+2+2+2, by design: group A legitimately needs 4 slots because pace, volume, structure and multi-week trajectory are independently falsifiable (§3(d)/(e) of the reconciliation doc already established this for 3 of the 4; E4 is the 4th and is independently falsifiable from E1–E3 because a plan can preserve every single week's numbers while still violating the *trajectory* across weeks, e.g. flattening a taper). Group C and D each need only 1 slot because, once defined correctly, "is it usable" and "is it stable" are each a single well-posed question, not a family of sub-constructs.

---

## 4. Detailed Definition of the 8 Criteria

### E1 — Constraint Preservation: Pace/Intensity Fidelity
*(= candidate C2, retained essentially unchanged)*

1. **Construct:** Numeric/categorical preservation of the effort-level target (pace, intensity zone) computed by the deterministic engine.
2. **Why necessary for RQ2:** Directly operationalizes "maintaining predefined training constraints" for the one physiological variable (effort level) that the deterministic rules, not Gemini, are authorized to set.
3. **Measurable definition:** For every workout in the plan, `pace_target` and `intensity_zone` equal the baseline's values for that workout; every pace/zone name quoted in free text matches the baseline's zone table for that day.
4. **Inputs:** Baseline `pace_target`/`intensity_zone` per workout (24 baseline plans); Gemini-plan equivalents (72 generations); free-text fields for number/zone extraction.
5. **Algorithm (pseudocode):**
   ```
   for each profile p, each generation g in {baseline, gemini_rep1..3}:
     for each workout w in g.plan:
       struct_match[w] = (g.pace_target[w] == baseline.pace_target[w]) AND
                          (g.intensity_zone[w] == baseline.intensity_zone[w])
       text_values = extract_pace_and_zone_mentions(g.text_fields[w])
       text_mismatch[w] = count(v in text_values where v not in baseline.zone_table)
   report: proportion(struct_match) per generation; sum(text_mismatch) per generation
   ```
6. **Expected output/range:** Proportion matching ∈ [0,1]; mismatch count ∈ ℤ≥0. No score is "good" or "bad" a priori — reported descriptively per §10.2 of the lock.
7. **Type:** Baseline-reference criterion (the baseline defines the reference values Gemini is measured against).
8. **Comparable:** (a) Baseline vs Gemini — yes, but the baseline is compared to itself and is 1.0 by construction (not informative on its own; the informative content is Gemini's deviation from it). (b) Gemini rep1 vs rep2 vs rep3 — yes, directly, since each repetition is scored independently against the same baseline.
9. **Violation/failure:** Any struct_match = false, or any text_mismatch > 0.
10. **Non-redundancy:** Distinct from E2/E3 because effort-level (pace/zone) can diverge independently of mileage (E2) or day-arrangement (E3) — the reconciliation doc §3(d)/(e) already establishes volume and structure are separable from each other; the same logic separates effort-level from both (a plan can state the right distance on the right day but the wrong pace, e.g. prescribing a long run's mileage correctly at threshold pace instead of easy pace).
11. **Potential weakness/threat to validity:** The validator's tolerance-free "exact match" treats a phrasing paraphrase of the same zone (e.g., "steady effort" vs "Threshold") as a mismatch unless the extraction vocabulary anticipates every synonym the LLM might use — recall of the text-extraction step is a validity threat, not just a nuisance; report extraction-vocabulary coverage as a documented limitation alongside this criterion's numbers, not merged into the score.
12. **Fully automatable:** Yes — string/number equality plus regex/keyword extraction, no judgment calls at scoring time (the only judgment required is upfront vocabulary construction, done once, before data collection, not per-output).

### E2 — Constraint Preservation: Volume Fidelity
*(= candidate C3, retained essentially unchanged)*

1. **Construct:** Numeric preservation of prescribed training volume (daily distance, weekly mileage) against the deterministic baseline.
2. **Why necessary for RQ2:** Volume is the other half of "predefined training constraints" the engine, not Gemini, computes (injury/overtraining risk tracks volume more than effort-level).
3. **Measurable definition:** `distance_km` per workout and `weekly_mileage_km` per week equal the baseline within the validator's existing tolerance (±0.05 km distance, ±0.15 km weekly mileage, per `RESEARCH_METHODOLOGY_LOCK.md` §5 item 3/T9); per-week day distances sum to the stated weekly mileage; any distance quoted in free text matches the corresponding plan value.
4. **Inputs:** Baseline and Gemini `distance_km` per day and `weekly_mileage_km` per week, for all weeks (not Week 1 only, per the confirmed multi-week scope); free-text distance mentions.
5. **Algorithm:**
   ```
   for each profile p, each generation g, each week k, each day d:
     dev_distance[k,d] = |g.distance_km[k,d] - baseline.distance_km[k,d]|
     pass_distance[k,d] = dev_distance[k,d] <= 0.05
   for each week k:
     dev_mileage[k] = |g.weekly_mileage_km[k] - baseline.weekly_mileage_km[k]|
     pass_mileage[k] = dev_mileage[k] <= 0.15
     sum_check[k] = |sum(g.distance_km[k,:]) - g.weekly_mileage_km[k]| <= 0.15
   text_mismatch = count(number in g.text_fields not matching any plan value ±tolerance)
   report: median/range of dev_distance and dev_mileage; pass-rate at tolerance;
           pass-rate at exact equality (sensitivity analysis, §9 open item 6 of reconciliation doc)
   ```
6. **Expected output/range:** Deviation in km (continuous, ≥0); pass-rate ∈ [0,1] at two thresholds (tolerance and exact).
7. **Type:** Baseline-reference criterion.
8. **Comparable:** (a) Baseline vs Gemini — yes, baseline trivially 1.0 (same caveat as E1). (b) rep1/2/3 — yes, directly.
9. **Violation:** `pass_distance`/`pass_mileage`/`sum_check` false for any week; text number outside tolerance of any plan value.
10. **Non-redundancy:** A plan can preserve exact mileage totals while silently moving distance between days (caught by E3, not E2) or hold both mileage and day-arrangement correct while using the wrong pace (caught by E1, not E2) — three independently failable dimensions per the reconciliation doc §3(d).
11. **Weakness:** The 0.05/0.15 km tolerances are themselves an un-validated design choice inherited from the production validator, not derived from any training-science source — reporting at exact equality alongside the tolerance (step 5 above) is the mitigation already flagged as needed in `RESEARCH_METHODOLOGY_LOCK.md` §5.1; this document does not resolve that threshold choice, it only operationalizes the sensitivity check the lock already calls for.
12. **Fully automatable:** Yes.

### E3 — Constraint Preservation: Structure Fidelity
*(= candidate C4, retained essentially unchanged)*

1. **Construct:** Preservation of the day-by-day arrangement (which days train, which rest, what type each training day is) against the baseline.
2. **Why necessary for RQ2:** Arrangement failures are invisible to E1/E2 (same total volume and pace vocabulary, wrong day) and directly test "maintaining predefined training constraints" at the schedule level, which matters for runners with fixed availability (`training_days_per_week`, `preferred_days`).
3. **Measurable definition:** For every week, the set of training/rest days, the workout type per day (easy/long/quality/rest), the rest-day count, and the training-day count all equal the baseline.
4. **Inputs:** Baseline and Gemini per-week day list, workout type per day, rest/training-day counts, all weeks; profile's `training_days_per_week`/`preferred_days` for a secondary face-validity check.
5. **Algorithm:**
   ```
   for each profile p, each generation g, each week k:
     day_set_match[k]   = (g.days[k] == baseline.days[k])
     type_match[k]      = all(g.type[k,d] == baseline.type[k,d] for d in week)
     rest_count_match[k] = g.rest_days[k] == baseline.rest_days[k]
     train_count_match[k] = g.train_days[k] == baseline.train_days[k]
   report: proportion of weeks fully matching all 4 sub-checks; per-sub-check violation counts
           (never collapsed into one undifferentiated pass/fail, so which sub-check failed is visible)
   ```
6. **Expected output/range:** Proportion ∈ [0,1] per sub-check and overall; violation counts by category.
7. **Type:** Baseline-reference criterion.
8. **Comparable:** (a) yes, baseline trivially 1.0. (b) yes, directly.
9. **Violation:** Any sub-check false for any week.
10. **Non-redundancy:** See E1/E2 items 10 — arrangement is a distinct failure mode from both effort-level and total-volume preservation.
11. **Weakness:** "Workout type" is a closed small vocabulary (easy/long/quality/rest) extracted or structurally compared, which is low-risk, but if Gemini introduces a *new* type label not in the baseline's vocabulary (e.g., renames "quality" to "tempo"), this needs an explicit decision — treat as a type mismatch (conservative) or normalize synonyms first. Flagged as an open scoring-convention decision in §9.
12. **Fully automatable:** Yes, provided the type vocabulary is fixed in advance (no live judgment).

### E4 — Multi-Week Trajectory Fidelity
*(= candidate C6, retained with an explicit gating condition added)*

1. **Construct:** Preservation of the *week-over-week volume trajectory* (build progression, cutback dips, taper) across the full plan duration — a construct that exists only once multi-week scope is in play, and is not reducible to any single week's E1–E3 checks.
2. **Why necessary for RQ2:** The locked design confirms Gemini receives multi-week context and may personalize across weeks; without this criterion, a plan that preserves every individual week's numbers (passing E1–E3 every week) could still flatten a taper or omit a cutback dip, which E1–E3 cannot detect because they check within-week fidelity, not the cross-week shape.
3. **Measurable definition:** For every week 1..N, the week's volume deviation from the baseline's *scheduled* volume for that week, computed and reported **separately per phase** (build / cutback / taper), so that a cutback-week or taper-week failure is distinguishable from a build-week failure; plus a rule-based contradiction check on any free-text statement about progression, load, or taper against that same per-week schedule.
4. **Inputs:** Per-week baseline volume and a phase label (build/cutback/taper) for every week 1..N; per-week Gemini volume; free-text progression/taper statements.
5. **Algorithm:**
   ```
   for each profile p, each generation g:
     for each week k with phase label φ(k) in {build, cutback, taper}:
       dev[k] = (g.weekly_mileage_km[k] - baseline.weekly_mileage_km[k]) / baseline.weekly_mileage_km[k]
       pass[k] = |dev[k]| <= tolerance   # same tolerance convention as E2
     group dev[] and pass[] by φ(k); report per-phase distributions, not one pooled number
     contradiction_count = rule_check(g.text_progression_statements, schedule=baseline.phase_schedule)
   ```
6. **Expected output/range:** Per-phase deviation distribution (%, continuous); per-phase pass-rate ∈ [0,1]; contradiction count ∈ ℤ≥0, reported separately, never averaged into the numeric deviation.
7. **Type:** Baseline-reference criterion. **No longer blocked** — see item 11: the prior open decision has been resolved (rebound fixed in code; taper confirmed correct).
8. **Comparable:** (a) Baseline vs Gemini — trivially yes in the same degenerate sense as E1–E3 (the baseline IS the schedule). (b) rep1/2/3 — yes, directly.
9. **Violation:** `pass[k]` false for any week, flagged by its phase; any `contradiction_count` > 0.
10. **Non-redundancy:** E1–E3 check within-week fidelity; E4 checks the across-week shape, which is a different construct (a plan can pass every week individually and still fail E4, e.g. by applying the *same* cutback-week reduction to a build week one week early).
11. **RESOLVED (historical weakness, no longer open):** `RESEARCH_METHODOLOGY_LOCK.md` §3 T7 recorded two known deterministic rule-engine properties — post-cutback rebound of ~+25% vs the cutback week, and taper anchored to starting volume rather than peak volume — and called for a fix-or-document decision "before the baseline is frozen." **That decision has been made and implemented:** the rebound is fixed in `generate_weekly_progression_summary` (the cutback week's own reduced volume now carries forward as the progression reference), verified by `backend/tests/test_t7_progression_fix.py` and a 201/201 full-suite pass; the taper's starting-mileage anchoring was reviewed and confirmed to already match the documented methodology (`PAPER_DRAFT.md` Table II) and was left unchanged. E4 can therefore be scored against a settled, non-bugged baseline trajectory once the 24 baseline plans are generated against this fixed rule-engine version (baseline generation itself has not yet been done — that is a separate, later step, outside the scope of this fix). See `paper/CODE_AUDIT_EASY_RUN_PACE_AND_T7.md` for the full audit and fix record. This item was Open Decision #1 in §9 below; it is now resolved there too.
12. **Fully automatable:** Yes — phase labels are already produced by the generator, and the algorithm itself requires no judgment calls.

### E5 — Output Validity & Completeness
*(= candidate C5, retained essentially unchanged)*

1. **Construct:** Whether the output is usable as evidence at all, independent of whether its content is correct — a precondition for every other criterion.
2. **Why necessary for RQ2:** A plan that fails to parse or is missing required fields cannot be scored on E1–E4/E6–E8 at all; without E5, an unparseable output would either be silently dropped (biasing the sample toward "easy" generations) or forced into a 0 that conflates "wrong" with "unusable."
3. **Measurable definition:** Output parses as valid JSON and conforms to the `AIPersonalizedPlan` schema; every required text field is present and non-empty for each non-rest day (`warmup_cooldown`, `workout_execution`, `recovery_instruction`, `purpose`) and at the plan level (`coach_overview`, `personalized_insights`, `ai_personalization_summary`, `why_this_plan_was_generated`); truncation is flagged as its own sub-category.
4. **Inputs:** Raw HTTP response body; parsed JSON; the `AIPersonalizedPlan` schema; per-field presence/length; `truncated` flag from the harness (`RESEARCH_METHODOLOGY_LOCK.md` §9.3).
5. **Algorithm:**
   ```
   for each generation g:
     parse_ok = try_parse_json(g.raw_response)
     schema_ok = parse_ok AND validates_against_schema(g.parsed_json, AIPersonalizedPlan)
     if schema_ok:
       field_presence = [non_empty(f) for f in required_fields(g.parsed_json)]
       completeness_ratio = mean(field_presence)
     truncated = g.truncated_flag
   report: parse/schema pass-rate; completeness_ratio distribution; truncation rate, reported separately
   ```
6. **Expected output/range:** Parse/schema pass ∈ {0,1} per generation, rate ∈ [0,1] pooled; completeness_ratio ∈ [0,1]; truncation rate ∈ [0,1].
7. **Type:** Partially baseline-reference (parse/schema side), partially Gemini-only (text-completeness side — the baseline has no optional personalization text fields to leave empty).
8. **Comparable:** (a) Baseline vs Gemini — yes for parse/schema validity (both sides produce JSON); not meaningful for the completeness-of-text sub-check (baseline has none). (b) rep1/2/3 — yes, both sub-checks.
9. **Violation:** `parse_ok` or `schema_ok` false; any required field empty; `truncated` true.
10. **Non-redundancy:** The only criterion addressing usability as opposed to correctness; E1–E4/E6–E7 all presuppose a schema-valid, complete output to even run their checks on.
11. **Weakness:** "Non-empty" is a weak completeness bar (a one-word field counts as present) — it deliberately does not grade *quality* of the field's content (that is E6/E7's job), but a reader could mistakenly read a high completeness_ratio as evidence of good writing; the write-up must state this boundary explicitly.
12. **Fully automatable:** Yes.

### E6 — Profile-Grounded Personalization Coverage
*(revised per `EVALUATION_CRITERIA_FINAL_CONSISTENCY_REVIEW.md` — see the Revision Note at the top of this document; full slot-by-slot reasoning lives in `PROFILE_FACT_SLOT_SPECIFICATION.md`)*

1. **Construct:** The breadth of **baseline-independent** runner-specific profile facts — i.e., facts the deterministic rule engine does not itself consume to compute the baseline plan — that are verifiably and specifically reflected in the Gemini plan's text, out of the facts that are actually available to be reflected for that runner.
2. **Why necessary for RQ2, and why "baseline-independent" is the operative word:** A fact that *is* a rule-engine input (e.g. `target_race_time`) already has a single correct, baseline-computed instantiation; checking whether Gemini's plan matches that instantiation is indistinguishable from checking constraint preservation, which E1–E4 already do. E6 is scoped specifically to the complementary set of facts — those the baseline makes no claim about at all — because only there can "Gemini used this" mean something E1–E4 cannot already show. This directly answers the RQ2 personalization clause without re-measuring the constraint-preservation clause under a different name.
3. **Measurable definition:** For the fixed, enumerable slot set `SLOTS = [injury_limitations]` (see item 3a below for why this list is currently this short, and item 3b for the one conditionally-excluded candidate), the proportion of **applicable** slots (non-null for that profile) for which the plan's text contains an explicit, specific modification or reference tied to the stored value, per the detection rule in `PROFILE_FACT_SLOT_SPECIFICATION.md` §6.4 (token-overlap with the runner's own stored text, gated on a pre-registered, narrow action/modification lexicon — not a generic "mentioned it" check and not an externally authored genericness list).
   - **3a. Why the slot list is this short.** `experience_level`, `target_race_distance`, `target_race_time`, `current_weekly_mileage_km`, `training_days_per_week`/`preferred_days`, and `plan_duration_weeks` are all documented rule-engine inputs (`RESEARCH_METHODOLOGY_LOCK.md` §9.1, reproduced in `PROFILE_FACT_SLOT_SPECIFICATION.md` §2a) — the baseline's own schedule already is the per-runner-specific instantiation of each of these facts. Checking a Gemini plan against that same baseline-derived value is E1 (pace/time), E2 (mileage), E3 (day structure/count), or the structural side of E5/E4 (duration/week count) — not new evidence about personalization. These fields are therefore explicitly **excluded from E6**, not merely de-weighted (full reasoning and per-field classification: `PROFILE_FACT_SLOT_SPECIFICATION.md` §3–§4). `vdot_band` and `stated_preference` are additionally excluded because no backing field for either is traceable in any design document (`PROFILE_FACT_SLOT_SPECIFICATION.md` §2c) — they are not presented anywhere in this document as implemented fields.
   - **3b. `easy_run_pace`** is a stored, prompt-fed field that the deterministic baseline does *not* consume — structurally it is a candidate for independent personalization evidence. It is **not** included in the current slot list because the available documentation does not establish that its value is distinct from the pace derivable from `pb_5k`/VDOT by the same formula the baseline uses; if it is simply a restatement of that formula, scoring it would silently reintroduce the same E1-overlap problem this revision removes. This is carried forward as an open item (§9) pending confirmation against the real application schema, not silently dropped and not silently included.
   - **3c. Why this does not collapse E6 into "did the plan avoid an unsafe workout":** a weaker, rejected alternative definition would have scored E6 as "no workout contradicts the stated injury," which is a safety-constraint check (closer in kind to E3) rather than personalization evidence, since the baseline's absence of any injury-aware modification means "doing nothing" would trivially pass such a check. The adopted definition instead requires a *specific, referenced, active modification* (per §6.4's modification-verb gate) — a plan that is merely silent about the injury scores as NOT REFERENCED (a miss, not a pass), which is the behavior that keeps this a personalization measure rather than a disguised constraint check.
4. **Inputs:** `runner_profile.injury_limitations` (free text, optional); parsed Gemini text fields (`coach_overview`, `personalized_insights`, `ai_personalization_summary`, `why_this_plan_was_generated`, per-day `purpose`/`recovery_instruction`/`workout_execution`).
5. **Algorithm:**
   ```
   SLOTS = [injury_limitations]   # see item 3 for why; easy_run_pace tracked separately, not scored (§9)
   for each profile p, each generation g:
     applicable = [s in SLOTS where profile[p][s] is not null/empty]
     referenced = []
     for s in applicable:
       hit = injury_reference_detector(g.text_fields, profile[p][s])
            # per PROFILE_FACT_SLOT_SPECIFICATION.md §6.4: token-overlap(stored text, sentence) >= 1
            # AND sentence contains a verb from the pre-registered modification lexicon
       referenced.append(hit)
     coverage[g] = count(referenced) / count(applicable)   # undefined/NA if count(applicable) == 0
   report: coverage distribution per generation, pooled and per profile stratum;
           report the NOT-APPLICABLE rate (profiles with no injury_limitations) as its own number,
           since it determines how much of the 24-profile sample E6/E7 can speak to at all
   ```
6. **Expected output/range:** coverage ∈ [0,1], defined only over profiles where `injury_limitations` is non-empty; report the applicable-profile count/rate explicitly alongside the coverage distribution.
7. **Type:** Gemini-only criterion.
8. **Comparable:** (a) Baseline vs Gemini — **no**, baseline produces no free text and, independent of that, has no injury-aware modification mechanism at all (not forced to a 0). (b) rep1/2/3 — yes, directly; one of the two criteria feeding E8.
9. **Violation/failure:** Reported as a distribution, not thresholded, consistent with the lock's "no pass thresholds are invented" rule (§10.2).
10. **Non-redundancy vs E1–E5:** By construction — the slot list retains only facts the baseline does not consume, so an E6 hit cannot be produced by a plan that merely reproduces baseline output (the baseline has nothing to reproduce here). This is the direct fix for the overlap the consistency review identified.
11. **Weakness — stated plainly, not minimized:** With the slot list reduced to one field, E6's "breadth of coverage" framing is largely vestigial for any single profile (coverage is 0/1 or 1/1, not a graded proportion across many facts); the originally intended richer coverage construct only becomes meaningful again if `easy_run_pace` (§3b) or another presently-undocumented baseline-independent field is confirmed and added. The stratified profile design (`experience level × target distance × injury presence`, per `EVALUATION_CRITERIA_RECONCILIATION.md` §1) is what keeps this slot non-trivial at the sample level — a meaningful fraction of the 24 profiles are expected to have `injury_limitations` populated by design — but the per-profile construct is thin, and the paper must say so rather than imply a multi-fact coverage score where only one fact is actually being checked.
12. **Fully automatable:** Yes — the slot list and detection rule are fixed in advance; no live subjective judgment at scoring time (the modification lexicon is curated once, in advance, per `PROFILE_FACT_SLOT_SPECIFICATION.md` §6.4/§7).

### E7 — Profile-Grounded Personalization Specificity
*(revised per `EVALUATION_CRITERIA_FINAL_CONSISTENCY_REVIEW.md` — see the Revision Note at the top of this document)*

1. **Construct:** Given that a **baseline-independent** fact is referenced (E6 = hit), whether the reference instantiates the runner's own stored context (a specific condition/body-part token drawn from `injury_limitations` itself) rather than a generic, condition-agnostic statement that would apply to any runner regardless of what was stored.
2. **E7 explicitly does NOT mean "did Gemini copy the profile's numeric value."** That test — matching a plan's number to the baseline-derived expected value for `experience_level`, `target_race_distance`, `target_race_time`, `current_weekly_mileage_km`, `training_days_per_week`/`preferred_days`, or `plan_duration_weeks` — is now understood to be constraint-fidelity evidence (E1–E4), not personalization evidence, because the baseline already computes the one "correct" per-runner value for each of those fields; matching it is indistinguishable from preserving the constraint. Those fields are excluded from E7 for the same reason they are excluded from E6 (§4 E6 item 3a) — they are Category B ("constraint-derived evidence") in `PROFILE_FACT_SLOT_SPECIFICATION.md`'s slot classification, not Category A.
3. **Why necessary for RQ2:** Among the facts that remain (currently: `injury_limitations` only), E6 alone cannot distinguish "acknowledged the injury in a boilerplate caution" from "modified a specific session using the runner's own stated condition" — both would be an E6 hit under a looser definition, so E7 adds the instantiation test on top of E6's presence test, for the one fact where the baseline makes no competing claim.
4. **Measurable definition — the objective proxy:** For the subset of generations where E6 = hit on `injury_limitations`, specificity is a structural, not lexical, test: of the token(s) shared between the plan's referencing sentence and the runner's own stored `injury_limitations` text, is at least one token specific to the *stored condition itself* (e.g. "knee," "shin," "achilles" — drawn from what the runner actually typed) rather than limited to domain-generic running vocabulary ("run," "pace," "week," "mile")? This is a **template-vs-instance** test anchored to the runner's own stored text (per `PROFILE_FACT_SLOT_SPECIFICATION.md` §6.4 step 4), not an externally authored genericness wordlist — the comparison target is always that runner's own field value, never a researcher-authored list of "generic" words.
5. **Inputs:** Same profile record and text fields as E6; the E6 hit/miss outcome per generation (E7 is computed only over E6 hits).
6. **Algorithm:**
   ```
   for each profile p, each generation g:
     hit = E6.referenced[p][g]                    # on injury_limitations only
     if NOT hit: specificity[g] = NA               # never coded as 0; never silently dropped
     else:
       T_profile = tokenize(profile[p].injury_limitations)     # stored text, lowercase, stopwords stripped
       T_sentence = tokenize(the referencing sentence(s) in g.text_fields)
       overlap = T_profile ∩ T_sentence
       specific = EXISTS t in overlap where t NOT IN domain_generic_running_terms
                  # domain_generic_running_terms is a small, fixed, pre-registered closed list of
                  # running-process words (run, pace, week, mile, session, ...), used only to exclude
                  # trivially shared vocabulary -- it is not a genericness-of-personalization wordlist,
                  # it is the stopword-equivalent needed to make token overlap mean something
       specificity[g] = 1 if specific else 0
   report: specificity distribution conditional on E6 = hit; report the "no hit" (NA) rate separately
   ```
7. **Expected output/range:** specificity ∈ {0,1} per generation (binary at the current single-slot scale; would become a proportion again if a second slot, e.g. a confirmed `easy_run_pace`, is added per §9), conditional on E6 = hit; report the NA rate as its own number.
8. **Type:** Gemini-only criterion.
9. **Comparable:** (a) Baseline vs Gemini — no (baseline has no injury-aware text at all, by construction). (b) rep1/2/3 — yes, directly.
10. **Violation/failure:** Reported as a distribution/rate, not thresholded; a "failure" is specificity = 0 given E6 = hit (the injury is acknowledged only in generic terms).
11. **Non-redundancy vs E1–E5 (the problem this revision fixes) and vs E6:** E7 is computed only on `injury_limitations`, a field the deterministic baseline never consumes — there is no baseline-derived "correct" modification for E7 to covertly re-check, which is what makes it structurally different from E1–E4 (see item 2). It remains non-redundant with E6 by the same dependency logic as before (you cannot be "specific" about a fact never referenced; E6=0 implies E7=NA, never implies E7=0 by default).
12. **Weakness — stated plainly:** (a) The same instantiation-vs-quality gap flagged in the prior version remains: a plan can use the exact condition-specific token in a bland sentence and still score specific=1; E7 measures *instantiation*, not *coaching quality*, and the paper must say so. (b) At a single slot, E7 is a binary per generation, not a graded score, which is a real loss of resolution relative to the originally intended multi-slot design — this is the direct, disclosed cost of removing the slots that were overlapping E1–E4, not a free improvement. (c) The `domain_generic_running_terms` exclusion list (item 6) and the modification-verb lexicon it depends on (E6 item 3, item 5) are small, closed, pre-registered curation steps — bounded and disclosed, consistent with how `PROFILE_FACT_SLOT_SPECIFICATION.md` already treats this exception for S7, but still a human-authored list, not a purely data-driven derivation, and this must be stated in the limitations section rather than claimed as fully keyword-free from first principles.
13. **Fully automatable:** Yes — the stored field supplies the comparison target, and the only upfront human input is the small pre-registered action/exclusion lexicon, decided once before scoring, not per-sample.

### E8 — Cross-Repetition Stability
*(= candidate C7, narrowed — see §6/§9 on the repetition-overlap question)*

1. **Construct:** Whether Gemini's behavior is consistent enough across the 3 repetitions per profile that a single reading of any one repetition would have led to the same qualitative conclusion (pass/fail pattern) as the other two — i.e., *agreement*, not merely *the existence of 3 samples*.
2. **Why necessary for RQ2:** The 3-repetition design (locked) generates the data needed to measure stability, but generating 3 samples is not itself a finding — E8 is the criterion that actually consumes the repetition design to produce a reportable number; without a dedicated criterion, "stability" would either go unreported (wasting 2/3 of the Gemini generations as mere variance padding) or be smuggled into E1–E7 as an unstated side effect.
3. **Measurable definition:** For each profile, the rate of agreement across its 3 Gemini repetitions on (a) each of E1/E3/E5's binary pass/fail outcomes, and (b) the magnitude spread (max − min, or coefficient of variation) of each of E2/E4/E6/E7's continuous outcomes. This is explicitly scoped to **cross-repetition agreement on the other 7 criteria's outcomes**, not to API-layer process metrics (latency, HTTP errors, token cost), which are reproducibility/engineering bookkeeping (already specified for storage in `RESEARCH_METHODOLOGY_LOCK.md` §9.3/§13) rather than a research construct and are therefore **excluded from E8** to avoid conflating "did the call fail" with "did the model behave inconsistently when it succeeded."
4. **Inputs:** Per-repetition outcomes for E1, E2, E3, E4, E5, E6, E7, grouped by profile.
5. **Algorithm:**
   ```
   for each profile p:
     for each binary criterion c in {E1, E3, E5}:
       agreement[p,c] = (all 3 reps agree on pass/fail) ? 1 : fraction_in_majority
     for each continuous criterion c in {E2, E4, E6, E7}:
       spread[p,c] = max(reps) - min(reps)     # or CV = stdev/mean, pick one convention, pre-registered
   report: agreement distribution per criterion, pooled across 24 profiles; spread distribution per criterion
   ```
6. **Expected output/range:** agreement ∈ [0,1] (or {1/3, 2/3, 1} for 3 reps); spread ≥ 0 in the same units as the underlying criterion.
7. **Type:** Repetition/stability criterion (explicitly its own type, distinct from "baseline-reference" and "Gemini-only content" — see §9 for why this is kept as a separate type rather than folded into "Gemini-only").
8. **Comparable:** (a) Baseline vs Gemini — no, the baseline is not repeated (confirmed design fact) and has no agreement/spread to compute. (b) "Gemini rep1 vs rep2 vs rep3" — this criterion **is** that comparison, by definition, for the other 7 criteria; it does not have its own further repetition dimension.
9. **Violation/failure:** Low agreement (e.g., 1 of 3 reps disagreeing with the other 2 on a binary criterion) or high relative spread on a continuous criterion, reported descriptively, not thresholded.
10. **Non-redundancy vs the repetition design itself:** This is the resolution of the brief's flagged overlap concern (see §9 critical discussion) — the 3 repetitions are the *method* (data-generation design); E8 is the *measurement* computed from that method's output. Removing E8 would not remove the repetitions (they are locked at 3 regardless), it would just mean 72 generations exist but no criterion ever reports what the extra 2 repetitions per profile revealed.
11. **Weakness:** With only 3 repetitions per profile, agreement/spread estimates per profile are low-precision (a 2-of-3 split is the finest resolution possible); report pooled-across-24-profiles distributions as the primary evidence, not per-profile agreement rates in isolation, and do not claim a stability "rate" with a false sense of precision from n=3.
12. **Fully automatable:** Yes — it is a deterministic aggregation of E1–E7's already-computed per-repetition outputs, no new extraction or judgment step.

---

## 5. Baseline vs Gemini Comparability Matrix

| ID | Criterion | Baseline-evaluable? | Why / treatment |
|---|---|---|---|
| E1 | Pace/Intensity Fidelity | Trivially yes, but **uninformative** (baseline scored against itself = 1.0 by construction) | Retained as the reference point; real information is in Gemini's deviation from it |
| E2 | Volume Fidelity | Trivially yes, but uninformative (same reasoning) | Same treatment |
| E3 | Structure Fidelity | Trivially yes, but uninformative (same reasoning) | Same treatment |
| E4 | Multi-Week Trajectory Fidelity | Trivially yes, but uninformative. **T7 RESOLVED** (rebound fixed; taper confirmed correct) — no longer blocked on a pending decision | Baseline IS the schedule being compared against; not a scored participant; score is entirely about Gemini's fidelity to it. Scoring can proceed once the 24 baseline plans are generated against the fixed rule engine (not yet done) |
| E5 | Output Validity & Completeness | **Partially** — parse/schema validity meaningfully comparable (both sides produce JSON); text-completeness sub-check not meaningful for baseline (no optional text fields) | Report parse/schema for both sides; completeness-of-text as Gemini-only |
| E6 | Personalization Coverage | **No** — baseline has no free text | Gemini-only secondary outcome; reported as "not applicable," never as a baseline score of 0 (a 0 would misleadingly imply the baseline contradicts the profile, when it simply makes no textual claims) |
| E7 | Personalization Specificity | **No** — same reason as E6 | Gemini-only secondary outcome |
| E8 | Cross-Repetition Stability | **No** — the baseline is deterministic and generated once per profile (confirmed design fact, not an oversight) | Gemini-only by design; this is an accepted, explicitly justified asymmetry (§9), not a gap to fix |

**Why it is acceptable, under Option A, that half the criteria (E5 partially, E6, E7, E8) are not symmetrically baseline-scored:** the locked design states the baseline is "a controlled reference for predefined training constraints," not ground truth for overall plan quality, and the baseline by construction produces no free text and is not repeated. A framework that forced every criterion into a symmetric two-sided score would either (a) invent a fictitious baseline text-quality score where none exists, or (b) artificially suppress criteria that only make sense for the generative, stochastic side of the comparison. Reporting "not applicable to baseline" honestly for E6/E7/E8, and "reference value by construction, not independent evidence" for E1–E4, is the more defensible choice and matches the posture already adopted in `EVALUATION_CRITERIA_RECONCILIATION.md` §7.

---

## 6. Repetition/72-Generation Analysis

The 72 Gemini generations (24 profiles × 3 repetitions) serve two distinct purposes that must not be conflated:

1. **As the sampling unit for E1–E7**: each of the 72 generations contributes one observation to each of E1–E7's pooled distributions (e.g., E2's "deviation distribution" is computed across all 72 generations, or stratified by profile, not just 24). This is where most of the 72 generations' statistical value comes from — more observations per criterion, better-characterized distributions.
2. **As the direct input to E8**: E8 is the only criterion that uses the *nesting structure* (3 reps within 1 profile) as its unit of analysis, rather than treating the 72 as 72 independent data points. This matches `RESEARCH_METHODOLOGY_LOCK.md` §10.2's explicit instruction that "the 72 Gemini outputs must not be treated as 72 independent participants" — E8 is exactly the criterion that respects the nesting, and E1–E7's *primary* descriptive reporting (medians, ranges) should also be reported per-profile-then-pooled, not naively pooled across all 72 as if profile were not a blocking factor, consistent with the lock's own analysis plan.

**On the brief's flagged concern — "Reliability/Stability may overlap with the 3-repetition design itself (repetition is the method, not necessarily a separate construct)":** resolved by treating repetition as the *data-generation method* and E8 as the *measurement* that method enables (see E8 item 10 above). E8 is kept as a separate criterion, but its scope is deliberately narrowed to cross-repetition agreement on E1–E7's outcomes, explicitly excluding API-process metrics (latency, errors, tokens), which belong in reproducibility bookkeeping (`RESEARCH_METHODOLOGY_LOCK.md` §9.3/§13), not in the 8-criterion research rubric — this prevents E8 from being partly "a research construct" and partly "an engineering log" glued together, which was the failure mode the reconciliation doc already flagged for the superseded C7/L8.

---

## 7. Threats to Validity

| Threat | Where it applies | Mitigation / how documented |
|---|---|---|
| Circularity with the production validator | E1, E2, E3 reuse `ai/validator.py`'s own logic as the measurement instrument | Report explicitly as "compliance with the validator's own instructions," per `RESEARCH_METHODOLOGY_LOCK.md` §5.1; not claimed as independent evidence of plan quality |
| Baseline engineering artifacts treated as ground truth | E4 specifically; T7's rebound/taper-anchoring behaviors | **RESOLVED**: T7's rebound bug is fixed in code (no longer an artifact to treat as ground truth); taper-anchoring is confirmed intentional, matching the documented methodology, not an artifact at all (item 11 under E4). E4 is no longer gated/blocked by this item; remaining prerequisite is generating/freezing the 24 baseline plans against the fixed rule engine (not yet done) |
| Extraction/recall limits of rule-based text parsing | E1 (text-quoted pace/zone), E2 (text-quoted distances), E6, E7 | Report extractor recall on a held-out hand-checked sample as a documented limitation alongside each criterion's numbers; do not fold recall error into the criterion's own score |
| Proxy ceiling on personalization measurement | E6, E7 — both are automated proxies for a construct (genuine personalization quality/insight) that would ordinarily need expert judgment | Stated explicitly in E7 item 11; the paper must not claim E6/E7 measure "quality," only coverage and instantiation |
| Low-precision stability estimates at n=3 | E8 | Report pooled-across-24-profiles distributions as primary evidence; do not report per-profile stability rates as if precise |
| Vocabulary/synonym mismatches at scoring time (e.g., Gemini renaming a workout type, or paraphrasing a zone name) | E1, E3 | Fixed vocabulary decided in advance (§9 open item); flagged, not resolved, as a scoring-convention decision |
| Multiplicity across 8 criteria × multiple sub-checks | All | No significance testing is promised by this document (consistent with the lock, §10.2); if any inferential test is later added, a multiplicity policy must be fixed beforehand, out of scope here |
| Researcher-defined slot list for E6/E7 | E6, E7 | The 9-slot list (step 3/item 3 under E6) is a design choice, not a literature-validated instrument; flagged for advisor review in §9 |
| Model/prompt drift between repetitions if not run in one window | E8 | Already covered by the lock's requirement to run all Gemini calls within one recorded window (§4.3); E8's results are only interpretable under that condition, which this document assumes but does not itself enforce |

---

## 8. Recommended Statistical Analysis Inputs

**No statistical test is chosen here.** Consistent with `RESEARCH_METHODOLOGY_LOCK.md` §10.2 ("the final statistical procedure will be selected based on the measurement scale, pairing structure, repeated-generation design, and distributional characteristics of the collected outcomes... PROPOSED methodology only"), this section lists inputs and considerations for that future, separate decision:

- **Measurement scales produced by E1–E8:** binary pass/fail (E1 struct-match, E3 sub-checks, E5 parse/schema), continuous/ratio (E2 deviation km, E4 per-phase deviation %, E6/E7 proportions), and count data (E1/E2 text-mismatch counts, E4 contradiction counts). Any candidate test must accommodate this mix, or criteria must be analyzed separately by scale type rather than forced into one test.
- **Nesting/pairing structure that any test must respect:** profile is the blocking/sampling unit (24 profiles); within each profile, 3 Gemini repetitions are nested replicates (not independent); the baseline has exactly 1 observation per profile, not repeated. The 72 Gemini outputs must not be treated as 72 independent samples (lock §10.2, restated here as a binding constraint on any future test, not a new decision).
- **Candidate families consistent with that structure (not chosen, listed only as the lock already does):** paired/matched non-parametric tests (e.g., Wilcoxon signed-rank on profile-level baseline-vs-Gemini-mean deviations), mixed-effects models with profile as a random effect and repetition nested within profile, or Friedman-type tests if more than two conditions are ever compared. Selection, assumptions-checking, and multiplicity policy remain [ADVISOR/METHOD REVIEW REQUIRED], unchanged from the lock.
- **No composite score and no ranking:** every candidate above is a per-criterion analysis; nothing in this document proposes combining E1–E8 into one index or declaring Gemini "better" or "worse" than the baseline — that framing is explicitly out of scope under the locked design and is not reintroduced here.
- **Reporting convention implied by §5–6 above:** any future statistical write-up must separately label which criteria are two-sided (E1–E4 partially, E5 partially) vs Gemini-only (E6, E7, E8, and the completeness sub-check of E5), so a reader cannot misread a Gemini-only descriptive statistic as a baseline-vs-Gemini comparison.

---

## 9. Open Decisions That Still Require Advisor Approval

1. **RESOLVED — E4 is no longer blocked on the baseline rule-engine fix-or-document decision (T7).** Post-cutback rebound (~+25%) has been fixed in code; taper-anchored-to-starting-mileage was reviewed and confirmed correct (matches the documented methodology) and left unchanged. This was carried forward unresolved from the reconciliation doc's own open item #4; it is resolved now, in a separate, later task that was explicitly authorized to modify the rule engine (this document's own original read-only/no-rule-engine-edit constraint applied only at the time this document was first written). Remaining prerequisite before E4 produces data: generate and freeze the 24 baseline plans against the fixed rule-engine version (not yet done).
2. **RESOLVED (superseded item, kept for traceability):** the original nine-slot `SLOTS` list has been replaced by the baseline-independence classification in `PROFILE_FACT_SLOT_SPECIFICATION.md` (§3–§5, Category A/B/C/D table). `vdot_band` and `stated_preference` are dropped (no traceable backing field); `experience_level`, `target_race_distance`, `target_race_time`, `current_weekly_mileage_km`, `training_days_per_week`/`preferred_days`, and `plan_duration_weeks` are reclassified Category B (constraint-derived, excluded from E6/E7, already measured by E1–E4); only `injury_limitations` remains Category A. This is no longer open — it is the current definition in §4's E6/E7 above. What remains open: whether the advisor wants to attempt instrumenting additional Category-C fields (item 2a below) once the real application schema is available.
   - **2a. Open:** `easy_run_pace` is a candidate second slot (Category C — potentially independent, pending confirmation) but is not currently scored, because it is not confirmed to be distinct from the VDOT-derived pace the baseline already uses (§4 E6 item 3b). Confirming or refuting this requires reading the real `app/models.py`/`app/rules/generator.py`, which is outside this repository's documentation. Advisor decision needed on whether to (a) proceed to data collection with the single-slot E6/E7 as specified, or (b) delay until the real schema is checked for `easy_run_pace` and any other undocumented baseline-independent field.
3. **RESOLVED (superseded item, kept for traceability):** the "verbatim or recognized numeric-equivalent form" test previously proposed for E7's now-removed numeric slots is no longer part of E7's definition (those slots are excluded — item 2 above). E7's current, sole equivalence judgment surface is the small `domain_generic_running_terms` exclusion list and the modification-verb lexicon (§4 E6 item 3 / E7 item 6), both already scoped as bounded, pre-registered, one-time curation per `PROFILE_FACT_SLOT_SPECIFICATION.md` §6.4/§7 — advisor sign-off on the exact contents of that lexicon remains open (see `PROFILE_FACT_SLOT_SPECIFICATION.md` §14 item 3).
4. **Workout-type/zone-vocabulary synonym handling for E1/E3 (flagged under each criterion's item 11)** — decide whether a renamed-but-equivalent label (e.g., "tempo" for "quality") counts as a match or a mismatch before scoring begins.
5. **Tolerance sensitivity analysis for E2 (and by extension E4's per-phase tolerance)** — whether the exact-equality sensitivity check is folded into this rubric's primary reporting or treated as a wholly separate analysis step; carried forward from the reconciliation doc's open item #6, not newly introduced here.
6. **Whether E8's continuous-criterion spread convention (max−min vs coefficient of variation) is pre-registered as one or the other**, so the choice is not made post hoc after seeing the data.
7. **Whether the 2-personalization-criteria / 4-constraint-criteria / 1-validity / 1-stability (2+4+1+1) distribution across groups A–D (§3) is the right balance, or whether the advisor prefers reallocating one constraint-preservation slot (E1–E4) toward a third personalization-facing criterion** — this document argues 4 constraint-preservation criteria are each independently falsifiable and therefore earn their slots (§3), but the balance itself is a judgment call open to the advisor's reweighing of RQ2's two clauses (§2).
8. **Whether `PAPER_DRAFT.md` Table IV's "Personalization quality = Expert rubric score" wording should be corrected in a future, separately authorized edit to match E6/E7's automated definitions** — this document does not edit `PAPER_DRAFT.md` (read-only per task constraints) and only flags the conflict, consistent with how `EVALUATION_CRITERIA_RECONCILIATION.md` §9 item 3 already flagged it for C8.

---

## 10. Final Recommendation

> **This Section 10, and this entire document, is a methodological proposal PENDING ADVISOR APPROVAL. It is not a locked methodology and does not amend `RESEARCH_METHODOLOGY_LOCK.md` or any other file.**

Recommend the advisor review the 8-criterion framework in §4 (E1–E8) as a candidate replacement for the "candidate 8" in `EVALUATION_CRITERIA_RECONCILIATION.md` §5, on the grounds that:
- E1–E5 preserve the reconciliation doc's already-sound constraint/validity criteria essentially unchanged, so no previously-agreed ground is relitigated unnecessarily;
- E6/E7 resolve the "Personalization Depth/Specificity lacks an objective operational definition" problem, and the subsequently-identified overlap with E1–E4, by scoping both measures to the single confirmed baseline-independent profile fact (`injury_limitations`) and deriving the coverage/specificity tests directly from that field's own stored text, with no invented keyword/genericness wordlist beyond the small, disclosed, pre-registered modification/exclusion lexicon (§4 E6–E7, §9 items 2–3; full classification in `PROFILE_FACT_SLOT_SPECIFICATION.md`);
- E8 resolves the "Reliability/Stability may overlap with the repetition design" concern by explicitly scoping stability to cross-repetition agreement on E1–E7's outcomes, separating it from API-process bookkeeping that belongs elsewhere (§6);
- E4 explicitly surfaced, rather than silently inherited, the T7 baseline-engine decision that previously blocked it — that decision is now resolved (§4 E4 item 11, §9 item 1);
- the baseline-vs-Gemini asymmetry already present in the reconciliation doc (3 Gemini-only criteria there) is preserved and extended with explicit justification rather than papered over (§5);
- no composite score, ranking, or "Gemini is better/superior" framing is introduced anywhere in this document, consistent with the locked design.

If approved (with or without amendment on the §9 open items), the next steps — out of scope for this document — would be: (a) advisor resolution of §9 items, especially T7 (item 1) and the slot/equivalence lists (items 2–3); (b) extension of `ai/validator.py` and the not-yet-built experiment harness to compute E1–E8 across the full multi-week context; (c) a separate, explicitly authorized correction of `PAPER_DRAFT.md` Table IV's wording if the advisor agrees (§9 item 8); (d) the statistical-test decision (§8), still open.

---

## Summary Table

| ID | Criterion | Construct | Automated? | Baseline Comparable? | Gemini Repetition Comparable? | Primary Purpose |
|---|---|---|---|---|---|---|
| E1 | Pace/Intensity Fidelity | Effort-level constraint preservation | Yes | Yes (trivial/reference only) | Yes | Constraint Preservation |
| E2 | Volume Fidelity | Mileage/distance constraint preservation | Yes | Yes (trivial/reference only) | Yes | Constraint Preservation |
| E3 | Structure Fidelity | Day/type arrangement constraint preservation | Yes | Yes (trivial/reference only) | Yes | Constraint Preservation |
| E4 | Multi-Week Trajectory Fidelity | Cross-week progression/cutback/taper shape preservation | Yes | Yes (trivial/reference only; **T7 RESOLVED — pending baseline generation/freeze, not pending any decision**) | Yes | Constraint Preservation |
| E5 | Output Validity & Completeness | Structural usability of the output | Yes | Partially (parse/schema yes; text-completeness no) | Yes | Output Validity |
| E6 | Personalization Coverage | Reference to the stored `injury_limitations` fact (the one confirmed baseline-independent slot) | Yes | No | Yes | Objective Personalization |
| E7 | Personalization Specificity | Condition-specific (vs. generic) instantiation of that same reference | Yes | No | Yes | Objective Personalization |
| E8 | Cross-Repetition Stability | Agreement of E1–E7 outcomes across the 3 Gemini repetitions | Yes | No (baseline not repeated) | N/A — this criterion IS the repetition comparison | Generation Stability |

**Candidate framework only — PENDING ADVISOR APPROVAL. Not locked.**
