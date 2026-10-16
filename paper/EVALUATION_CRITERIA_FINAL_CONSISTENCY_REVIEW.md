# EVALUATION_CRITERIA_FINAL_CONSISTENCY_REVIEW

**Methodological review — pending advisor approval.**

> **ADDENDUM — RESOLUTION STATUS.** The two blocking findings below (§4.1/§8 item 1: E7's S1–S4/S6 overlap with E1–E4; §8 item 2: the two documents' disagreeing slot lists) have since been addressed by direct edits to `EVALUATION_CRITERIA_OPTION_A_DESIGN.md` (§4 E6/E7, §9) and `PROFILE_FACT_SLOT_SPECIFICATION.md` (§1, §3–§15), which now agree on a single, narrowed E6/E7 slot set (`injury_limitations` only, Category A; `easy_run_pace` tracked as Category C, not adopted; all other originally proposed slots reclassified Category B and explicitly excluded, or Category D and dropped). The analysis below is left unmodified as the record of what was found and why; it should be read together with the two revised documents, not as superseded information.

---

> This document is read-only analysis. It does not modify `EVALUATION_CRITERIA_OPTION_A_DESIGN.md`, `PROFILE_FACT_SLOT_SPECIFICATION.md`, `EVALUATION_CRITERIA_RECONCILIATION.md`, or any other file. No application code, database, or experiment was inspected, run, or assumed. No Gemini output was generated. No git command was run. "Inputs read (read-only)": `EVALUATION_CRITERIA_OPTION_A_DESIGN.md` (full), `PROFILE_FACT_SLOT_SPECIFICATION.md` (full), `EVALUATION_CRITERIA_RECONCILIATION.md` (full, as background the two target documents themselves build on).

---

## 0. Summary of What Was Reviewed

Two documents, read together as one proposed methodology:

- **`EVALUATION_CRITERIA_OPTION_A_DESIGN.md`** ("Doc A") — defines E1–E8, the baseline/Gemini comparability matrix, RQ2 mapping, threats, and statistical-readiness inputs.
- **`PROFILE_FACT_SLOT_SPECIFICATION.md`** ("Doc B") — a follow-on document that operationalizes E6/E7 specifically, by auditing Doc A's 9-item `SLOTS` list against what is actually traceable in the documentation, and proposing a corrected 7-slot (S1–S7) set.

Doc B is explicitly scoped as a refinement of one open item in Doc A (§9 item 2 of Doc A: "the nine-slot list... needs advisor sign-off"). That relationship is coherent in principle. The main finding of this review is that the refinement was not round-tripped back into Doc A, so **the two documents currently disagree on what E6/E7's slot set even is**, and one specific construct-validity risk that Doc B itself discovered for one slot (S5) was not generalized to the four/five other slots where the identical risk applies. Both issues are fixable without redesigning the framework.

---

## 1. Criterion Boundary Check (E1–E8)

For each criterion: construct, RQ2 contribution, measures/does-not-measure, inputs, expected output, automation, expert-judgment need, overlap.

### E1 — Pace/Intensity Fidelity
- **Construct:** exact/near-exact preservation of per-workout `pace_target`/`intensity_zone` against the deterministic baseline, plus text-quoted pace/zone mentions matching the baseline's zone table.
- **RQ2 contribution:** operationalizes the "maintaining predefined training constraints" clause for effort-level.
- **Measures:** numeric/categorical equality on a per-workout basis.
- **Does not measure:** whether the effort-level target is itself appropriate for the runner (that is the baseline's job, assumed correct for this purpose); does not measure volume or day-arrangement.
- **Input:** baseline + Gemini `pace_target`/`intensity_zone` per workout (24 baseline, 72 Gemini); free text.
- **Output:** proportion matching ∈[0,1]; mismatch count ∈ℤ≥0.
- **Automated:** yes. **Expert judgment:** none required.
- **Overlap:** none with E2/E3 by construct (effort-level vs volume vs arrangement are separable failure modes, correctly argued in Doc A §4 E1 item 10). **New overlap found with E6/E7 — see §4 below**, because E6's S3 and E7's S3 both re-check pace against the same baseline-derived value E1 already checks.

### E2 — Volume Fidelity
- **Construct:** numeric preservation of distance/mileage against baseline, within a fixed tolerance.
- **RQ2 contribution:** the "volume" half of constraint preservation.
- **Measures:** per-day distance and per-week mileage deviation; internal sum-consistency; text-number matches.
- **Does not measure:** day-arrangement (E3) or pace (E1).
- **Input/Output/Automation:** as E1, with a continuous deviation metric rather than a pure binary.
- **Expert judgment:** none.
- **Overlap:** none with E1/E3 by construct. **New overlap found with E6/E7 S4 — see §4.**

### E3 — Structure Fidelity
- **Construct:** preservation of day-set, workout type, and rest/training-day counts.
- **RQ2 contribution:** schedule-level constraint preservation (distinct failure mode from E1/E2 — a plan can hold total volume and pace constant while moving a long run to the wrong day).
- **Measures:** four sub-checks per week, reported separately (not collapsed).
- **Does not measure:** whether the *type label itself* is semantically equivalent across a renamed vocabulary (flagged as an open scoring-convention decision, Doc A §9 item 4 — correctly left open, not silently resolved).
- **Automated:** yes, given a fixed type vocabulary. **Expert judgment:** none.
- **Overlap: already disclosed and accepted** — Doc B §13 explicitly states S5 (which reuses E3's day-set detector) "is not independent of E3." This is the one place the documents already do what §4 below asks them to do more broadly.

### E4 — Multi-Week Trajectory Fidelity
- **Construct:** week-over-week volume *shape* (build/cutback/taper), as distinct from any single week's numbers.
- **RQ2 contribution:** required because the locked design confirms multi-week scope; without it, a plan could pass every individual week (E1–E3) while flattening a taper.
- **Measures:** per-phase deviation from baseline schedule; text-contradiction count on progression statements, reported separately.
- **Does not measure:** whether the baseline's own trajectory is itself training-science-valid (explicitly out of scope, and explicitly why it is blocked — see below).
- **Automated:** yes, once gated.
- **Expert judgment:** none, once gated.
- **Status: BLOCKED, correctly and explicitly, not silently dropped.** Doc A §4 E4 item 11 ties E4's scorability to resolution of T7 (`RESEARCH_METHODOLOGY_LOCK.md`'s recorded baseline rule-engine issue: ~+25% post-cutback rebound, taper anchored to starting rather than peak volume). This review **confirms the block is correctly carried forward and not quietly removed**, satisfying the explicit instruction in the task brief to preserve this issue. It is not a defect in the document; it is a correctly surfaced open dependency.

### E5 — Output Validity & Completeness
- **Construct:** usability of the output as evidence (parses, schema-valid, required fields non-empty), independent of content correctness.
- **RQ2 contribution:** precondition criterion — without it, unparseable generations would be silently dropped (sample bias) or scored 0 (conflating "unusable" with "wrong").
- **Measures:** parse/schema pass; per-field non-empty rate; truncation, reported as its own category.
- **Does not measure:** quality of field content (explicitly deferred to E6/E7, and the document is explicit that a high completeness ratio must not be misread as good writing — Doc A §4 E5 item 11).
- **Automated:** yes. **Expert judgment:** none.
- **Overlap:** none — the only criterion that gates whether the others can even be computed.

### E6 — Profile-Grounded Personalization Coverage
- **Construct:** breadth of *applicable* profile facts verifiably and non-contradictorily reflected in the plan.
- **RQ2 contribution:** the "did Gemini use what it was given" half of the personalization clause.
- **Measures:** proportion of applicable slots referenced; excludes non-applicable (null) slots from the denominator (correct — avoids penalizing profiles that simply have no injury, no distinct preferred-days, etc.).
- **Does not measure:** depth/specificity of the reference (that is E7 — correctly deferred, not conflated).
- **Automated:** yes, in principle, per slot (see §4 for the reservation on S1–S4/S6).
- **Expert judgment:** none claimed; see §4 for why this claim needs qualification, not expert judgment.
- **Overlap:** with E1–E4, on S1–S4/S6 — see §4 (this is the central finding of this review).

### E7 — Profile-Grounded Personalization Specificity
- **Construct:** given a coverage hit, whether the plan reproduces the runner's own instance value (e.g., literal goal time) versus a generic class-level restatement.
- **RQ2 contribution:** the second half of the personalization clause — distinguishes "mentioned" from "materially used."
- **Measures:** template-vs-instance match, conditional on E6 hit; never scored independent of E6 (correct dependency, explicitly surfaced, Doc A §4 E7 item 10).
- **Does not measure:** rhetorical/coaching quality (explicitly and repeatedly disclaimed, Doc A §4 E7 item 11 — this is the single clearest piece of self-aware scoping in either document).
- **Automated:** yes for S1–S5 per Doc B; S7 requires a small pre-registered lexicon (disclosed, bounded).
- **Expert judgment:** none required for the automated path; a one-time codebook-curation step for S7 is required, correctly distinguished from per-sample expert judgment (Doc B §12, §13).
- **Overlap:** **with E1–E4, severely, on S1–S4/S6 — see §4.** This is more serious for E7 than for E6, because E7's specificity test *is*, for those slots, numerically closer to a duplicate of E1–E4's own check than Doc A/B currently acknowledge.

### E8 — Cross-Repetition Stability
- **Construct:** agreement/spread of E1–E7's *outcomes* across the 3 Gemini repetitions for the same profile — not the raw existence of 3 samples.
- **RQ2 contribution:** operationalizes the "reproducibility" dimension the repetition design was built to support.
- **Measures:** binary-criterion agreement (E1/E3/E5); continuous-criterion spread (E2/E4/E6/E7).
- **Does not measure:** API-process metrics (latency, HTTP errors, token cost) — explicitly and correctly excluded from E8 and left to reproducibility bookkeeping, avoiding the "engineering log glued to a research construct" failure mode the reconciliation document already flagged for the superseded C7.
- **Does not require identical plans across repetitions** — confirmed: the agreement/spread formulation (Doc A §4 E8 item 5) treats partial agreement (e.g., 2-of-3) and small continuous spread as normal, descriptive outcomes, not failures. Nothing in the algorithm forces or rewards identity.
- **Automated:** yes — pure aggregation of already-computed E1–E7 outputs. **Expert judgment:** none.
- **Overlap:** none with E1–E7 by construct (it consumes their outputs rather than duplicating their measurement), though it is downstream of whatever overlap exists inside E1–E7 themselves (see §4 — if E6/E7's numeric slots are not independent of E1–E4, then E8's "stability of E6/E7" is partly re-reporting stability already visible in E8's "stability of E1–E4").

### E6 vs E7 — explicit check requested by the brief
**Verdict: E6 = coverage, E7 = specificity, and the two are correctly kept non-identical by construction** (E7 only evaluates E6's hit set, and a plan can score high on one and low on the other in both directions for most slots). This separation is sound and should not be collapsed. The problem found in this review is not that E6 and E7 collapse into *each other* — it is that **both**, on 5 of their 6–7 common slots, collapse substantially into **E1–E4** (see §4). That is a different and more consequential finding than the E6-vs-E7 question as posed.

### E7 vs genericness — explicit check requested by the brief
Doc B's design genuinely avoids an externally authored "genericness keyword list" for every slot except S7, by anchoring the template-vs-instance test to the runner's *own* stored field value (Doc B §6.1, §6.4) rather than to a researcher-authored list of "generic-sounding" words. This satisfies the brief's objection. The one disclosed exception (S7's action lexicon and contradiction codebook, Doc B §6.4/§7) is bounded, pre-registered, and explicitly flagged as the "one place a small, disclosed curation step is unavoidable" (Doc B §15) — this is an honest, scoped exception, not a backdoor reintroduction of an arbitrary wordlist. No further action is required on this specific question beyond what Doc B already does.

### E8 — explicit check requested by the brief
Confirmed above: E8 measures agreement/spread, not identity, and this is unambiguous in the algorithm (Doc A §4 E8 item 5, item 9). No revision needed on this specific point.

---

## 2. Baseline vs Gemini Comparability Matrix

| Criterion | Baseline measurable? | Gemini measurable? | Directly comparable? | Gemini-only acceptable? | Reason |
|---|---|---|---|---|---|
| E1 | Yes, trivially (=1.0 by construction) | Yes | Degenerate — comparable only as "distance from a reference," not as two independent scores | N/A (not Gemini-only; baseline score is real but uninformative) | Baseline IS the reference values; scoring it against itself cannot fail. Documents correctly label this "reference point," not evidence. |
| E2 | Same as E1 | Yes | Degenerate, same reasoning | N/A | Same reasoning. |
| E3 | Same as E1 | Yes | Degenerate, same reasoning | N/A | Same reasoning. |
| E4 | Same as E1, **and currently blocked** | Yes once gated | Degenerate, and blocked until T7 resolved | N/A | Baseline trajectory itself may contain an unresolved engineering artifact (T7); scoring Gemini's "fidelity" to it before that is resolved would measure fidelity to a bug. Correctly gated, not silently scored. |
| E5 | Partially (parse/schema yes; text-completeness no, baseline has no optional text fields) | Yes, both sub-parts | Partially — parse/schema side only | Yes, for the text-completeness sub-check | Baseline genuinely has no analogue for "non-empty narrative field," so forcing a baseline score there would be fabricated, not measured. |
| E6 | **No** | Yes | No | **Yes** | Baseline produces no free text to check coverage of; a forced 0 would misleadingly read as "baseline contradicts the profile" rather than "baseline makes no textual claims." Both documents already state this correctly and explicitly refuse to force a 0. |
| E7 | **No** | Yes | No | **Yes** | Same reasoning as E6. |
| E8 | **No** (not repeated by design) | Yes | No | **Yes** | The baseline is deterministic and generated once per profile — not an oversight, a confirmed design fact. Forcing repetition on the baseline to "compare" would contradict the locked design (baseline = controlled reference, not a second stochastic condition). |

**Does the asymmetry create a methodological problem under Option A?** No, provided it is reported as designed. Option A's own premise (§CURRENT LOCKED RESEARCH DIRECTION) states the baseline is "a controlled reference for predefined training constraints, NOT ground truth," not a second generative condition symmetric to Gemini. A framework that forced symmetric two-sided scoring onto E6–E8 would either fabricate a baseline personalization/stability score that does not exist, or discard E6–E8 entirely to preserve symmetry — both worse than honest asymmetry. The one place this needs tightening is presentation discipline: the paper must visibly tag every reported number as "two-sided comparison" vs "Gemini-only descriptive statistic" (both documents already say this is required — Doc A §8 last bullet — this review confirms that instruction is sufficient and should simply be enforced at write-up time, not re-litigated).

---

## 3. RQ2 Traceability

RQ2: *"How does Gemini-based personalization differ from a deterministic baseline in generating personalized multi-week running training plans while maintaining predefined training constraints?"*

| RQ2 component | Criteria | Operationalized? |
|---|---|---|
| Constraint-preservation ("maintaining predefined training constraints") | E1, E2, E3, E4 | Yes — four independently falsifiable sub-dimensions (effort-level, volume, arrangement, trajectory), correctly argued as non-redundant in Doc A §3/§4. |
| Personalization ("Gemini-based personalization... differ... in generating personalized... plans") | E6, E7 | Partially — see §4. Coverage (E6) is well-operationalized. Specificity (E7) is well-operationalized only for the subset of its evidence that is not already implied by E1–E4 (chiefly S7, and the exact-day-set form of S5); for S1–S4/S6 it substantially re-measures constraint preservation under a different name. |
| Stability/reproducibility (implicit in "how does it differ" requiring a trustworthy single reading, and in the locked 3-repetition design) | E8 | Yes, operationalized as cross-repetition agreement/spread on E1–E7, correctly scoped away from API bookkeeping. |
| Output usability (implicit precondition for any of the above to mean anything) | E5 | Yes — not itself part of RQ2's wording, but required infrastructure for all other mappings to be meaningful, and correctly treated as precondition rather than forced into one of the three substantive clauses. |

**Unoperationalized part of RQ2:** none of RQ2's explicit clauses is left entirely uncovered. The one qualification is that the "personalization" clause is covered *more thinly* than Doc A's narrative claims, because part of E7's intended independent contribution collapses into the constraint-preservation clause for several slots (§4). This is a weakening of the *margin* by which E6+E7 answer the personalization clause, not a complete gap — E6 alone, plus E7's S7 and exact-day-set evidence, still provide real, non-redundant personalization evidence; it is E7's S1–S4/S6 contribution specifically that is overstated.

---

## 4. Personalization Validity (most important section)

### 4.1 The central finding: E7's (and to a lesser extent E6's) numeric slots are not independent of E1–E4

Doc B defines E7's specificity test for S1 (experience level), S2 (race distance), S3 (goal time/pace), S4 (weekly mileage), and S6 (plan duration) as: *does the plan's numeric/categorical value match the value the deterministic baseline computed specifically for this runner's stored input, rather than a generic/default value* (Doc B §5, §6.1). Mechanically, this is: `|plan_value − baseline_derived_expected_value| ≤ tolerance`.

Compare this to E1's definition (pace/zone equality to baseline), E2's definition (volume equality to baseline within tolerance), and E3's definition (day-set/type equality to baseline) — all three are, mechanically: `plan_value == baseline_value` (or within the same kind of tolerance).

Because the deterministic baseline is itself already a per-runner-personalized computation (it is derived *from* the profile's `experience_level`, `target_race_distance`, `target_race_time`, `current_weekly_mileage_km`, etc. — this is explicit in Doc B §2a: these fields are "rule-engine input"), **"matches the baseline's per-runner value" and "is specific to this runner, not generic" are, for these fields, the same test applied twice under two different names.** A Gemini plan that simply copies the baseline's numeric outputs verbatim will score ≈1.0 on E1/E2/E3 *and* ≈1.0 on E7's S1/S2/S3/S4 specificity test, for the identical underlying reason (both measure distance from the same baseline-derived number). A Gemini plan that deviates from the baseline's numbers will tend to fail both simultaneously as well.

This was **already discovered once by Doc B, but only for one slot.** Doc B §13 explicitly states: *"S5 double-counting with E3: Because S5 reuses the existing day-of-week detector, E6/E7 are not independent of E3 for that one slot."* This review finds the identical structural issue applies, with equal or greater force, to S1 (vs. E1's intensity-structure check, which also derives from `experience_level`), S2 (vs. E1/E3's long-run-distance/type checks, which also derive from `target_race_distance`), S3 (vs. E1's pace-fidelity check directly), S4 (vs. E2's volume-fidelity check directly), and S6 (vs. the week-count dimension of E3/E5's structural checks). Doc B's own disclosure pattern (flag the issue when found, don't force symmetry) is the right instinct; it was simply not applied exhaustively.

**Consequence for the headline claim.** Both documents assert, correctly for E6 in general and for E7's S7/S5-exactness in particular, that E6/E7 are "the primary, defensible proxy for personalization" (Doc A §4 E6 item 2) precisely *because* they are checkable independent of E1–E4. For S1–S4/S6, that independence claim does not hold: a plan's E7 score on those slots is largely a re-encoding of its E1/E2/E3 score, computed from the same baseline-derived ground truth. This does not make E7 *wrong* — it makes roughly 5 of its 6–7 slots a weak, redundant echo of constraint-fidelity rather than new evidence about personalization specifically. The genuinely new personalization evidence in the current slot set is concentrated in: (a) S7 (injury text — the baseline has no analogue at all, since `injury_limitations` is explicitly "not a numeric rule input," Doc B §2a), and (b) the *exact-day-set* form of S5 (E3 only checks day-count/type patterns per Doc A, not necessarily the exact preferred-day identities — Doc B's S5 does add the stricter "exact stored day-set, not just any permutation satisfying count" test, which is new evidence beyond E3's own check, see Doc B §11 S5 example). Everything else in E7's numeric slot set is better described as "cross-validation of E1–E4," not as independent personalization evidence.

### 4.2 Construct validity
E6's construct ("breadth of applicable profile facts reflected") is reasonably valid as a lower bound on personalization — it cannot register a false "used the profile" claim for a fact never touched. E7's construct ("specificity of what is reflected") is valid as *stated*, but the current slot-to-construct mapping over-attributes evidentiary weight to numeric slots that are confounded with constraint fidelity, per §4.1. Construct validity would be materially improved (without changing E6/E7's definitions) by re-weighting or re-labeling: report S1–S4/S6 explicitly as "numeric alignment with baseline-personalized values (overlaps E1–E4)" and report S5(exact-set)/S7 as "incremental personalization evidence (independent of E1–E4)," rather than pooling all slots into one undifferentiated E6/E7 proportion that implies uniform independent evidentiary value per slot.

### 4.3 Content validity
The slot list (post Doc B correction) is traceable to documented profile fields and avoids inventing facts, which is good content validity relative to what the system actually stores. Content validity is weaker in one respect flagged by Doc B itself: `plan_duration_weeks` (S6) is "low diagnostic value for personalization specifically" (Doc B §3) even before considering the E1–E4 overlap — it is a cardinality match any correctly-functioning system would trivially satisfy, contributing little information either way.

### 4.4 Automation feasibility
High for S1–S6 (deterministic numeric/categorical/scheduling comparisons against values the researcher already has, per Doc B §12). S7 requires a one-time, disclosed codebook (action lexicon, contradiction mapping) — correctly scoped as upfront curation, not per-sample judgment, and therefore does not reintroduce expert evaluation through the back door. This is sound.

### 4.5 False positive risk
Two concrete mechanisms, both already partially named in the source documents:
- **Baseline/default-band overlap (Doc B §11, S4 example):** if a generic default volume happens to fall inside the same numeric tolerance band as the mileage-specific baseline value, E7 would score "specific" when the plan may in fact be using a default. Doc B argues this "does not arise" because the baseline computation is mileage-specific by construction — this argument is sound *only if* the baseline's floor/cap function is strictly monotonic/injective enough that no two distinct profiles' bands overlap; that property is asserted, not verified (no code was read, per Doc B's own repository caveat), so this is a residual risk, not a resolved one.
- **The §4.1 circularity itself is a structural false-positive mechanism for "personalization": a plan can score high on E7's numeric slots for a reason (faithful constraint copying) that has nothing to do with "personalizing," inflating the apparent personalization signal.**

### 4.6 False negative risk
Fact-extraction recall limits are already disclosed (Doc A §4 E6 item 11: paraphrased goal times like "sub-50 10K" vs stored "49:30" may be missed). This is a conventional, acceptable, disclosed limitation, mitigated by reporting extractor recall on a held-out hand-checked sample — adequate as proposed.

### 4.7 Can profile facts be detected from the structured plan, or only from text?
This is handled well by the design, and is worth stating explicitly because it is a genuine strength: for S1, S2, S4, S5, and S6, detection is defined primarily over the **structured plan JSON** (intensity bands, long-run distance, Week-1 total, day assignment, week count), not over free-text narration. Only S3 (pace, when not in a structured field) and S7 (injury) depend on free-text scanning. This matters directly for the next question.

### 4.8 Should textual explanation count as evidence, and should plan behavior outweigh it?
Yes to both, and the current design already leans this way, correctly: the majority of E6/E7's slots are behavioral (does the plan's actual schedule/numbers reflect the fact) rather than rhetorical (does the plan's prose claim to have personalized). This is the right default, because a plan can narrate "I've tailored this to your goal" (rhetorical) while the actual schedule is a generic template (behavioral failure) — the reconciliation document's own earlier draft (C8, `EVALUATION_CRITERIA_RECONCILIATION.md` §6 C8 item 2) risked exactly this failure mode by proposing to count "specific-fact mentions" and "genericness markers" in text; Doc A/B's correction to structural/numeric comparison for S1–S6 is a direct and appropriate fix for that risk. Textual evidence should remain admissible (it is the only channel available for S7), but should be weighted as secondary where structured/behavioral evidence exists, which the current design already does by preferring structured fields over text wherever both exist (Doc B §12 S3 note: "if paces only appear in free text... adequate," i.e., text is a fallback, not the primary channel).

### 4.9 Overall verdict on §4
E6+E7 are a defensible objective proxy for the *coverage* half of personalization and for a *narrow but real* specificity signal (S7, and the exact-day-set reading of S5). They are **not currently a defensible proxy for personalization-specificity on S1–S4/S6**, because the test applied there is extensionally equivalent to constraint-fidelity (E1–E4) and should not be presented as additional, independent evidence that Gemini "personalized" beyond what preserving the baseline's numbers already shows. This is fixable by re-scoping §9's open item 2 (Doc A) to require, as part of advisor sign-off, an explicit statement of which E6/E7 slots are independent of E1–E4 and which are corroborating/redundant — not by discarding E6/E7 or redesigning the framework.

---

## 5. Three-Repetition Design (E8 sufficiency)

24 profiles × 3 Gemini repetitions = 72 outputs is treated correctly as a **within-profile stability design**, not a between-group comparison requiring statistical power. No power claim is made anywhere in either document, consistent with the task's instruction.

- **Unit of analysis:** profile (24 blocks), with 3 nested, non-independent replicates per block for the Gemini condition, and exactly 1 non-repeated observation per block for the baseline condition. This is stated explicitly and correctly in Doc A §6, and is consistent with `RESEARCH_METHODOLOGY_LOCK.md §10.2`'s instruction (quoted in Doc A) that "the 72 Gemini outputs must not be treated as 72 independent participants."
- **Non-independence is handled, not ignored:** E8 is explicitly defined to consume the nesting (per-profile agreement/spread, then pooled across 24 profiles — Doc A §4 E8 item 5), rather than pooling all 72 as flat independent samples. E1–E7's own primary reporting is also instructed to go "per-profile-then-pooled," not naively pooled (Doc A §6 item 2) — this is a correct and consistent convention across the whole document, not stated once and ignored elsewhere.
- **Sufficiency for E8 specifically:** 3 repetitions give only 3 possible per-profile agreement states for a binary criterion (3/3, 2/3, 1/3-all-disagree-is-impossible-with-3... actually with 3 reps the only partitions are 3-0 and 2-1, i.e., two possible agreement levels). This is explicitly and correctly flagged as a precision limitation in Doc A §4 E8 item 11 ("a 2-of-3 split is the finest resolution possible... do not claim a stability rate with a false sense of precision from n=3"). Given the explicit choice to report pooled-across-24-profiles distributions as the primary evidence rather than per-profile rates, 3 reps is adequate for *descriptive* stability reporting at the design's stated ambition level, and inadequate (and not claimed to be adequate) for any inferential claim about stability. This matches the task's instruction not to make unjustified statistical-power claims.
- **Baseline is correctly excluded from the repetition dimension** — it is deterministic, not stochastic, so "repeating" it would not test anything E8 is designed to test (model consistency). This is a design fact, not a gap.

**No revision needed in this section.**

---

## 6. Statistical-Analysis Readiness

Per the task's instruction, no test is chosen here; only the inputs are catalogued, cross-checking Doc A §8 against the detailed per-criterion outputs in §4 of Doc A and §4–5 of Doc B.

| Criterion | Data type produced | Likely unit of analysis | Pairing/nesting | Primarily descriptive only? |
|---|---|---|---|---|
| E1 | Binary pass/fail per workout + count data (text mismatches) | Workout, rolled to profile×generation | Nested: workout-in-week-in-profile; Gemini reps nested in profile | No — candidate for paired/matched analysis vs baseline |
| E2 | Continuous (deviation, km) + binary pass-rate | Day/week, rolled to profile×generation | Same nesting as E1 | No |
| E3 | Binary per sub-check per week | Week, rolled to profile×generation | Same nesting | No |
| E4 | Continuous per-phase deviation (%) + count (contradictions) | Week-within-phase, rolled to profile×generation | Same nesting; additionally phase-stratified | No — but **blocked** until T7 resolved, so no data exists to analyze yet |
| E5 | Binary (parse/schema) + continuous (completeness ratio) + binary (truncation) | Generation | Generation nested in profile | Partially — completeness ratio is descriptive by default |
| E6 | Continuous proportion (coverage, per generation) | Generation, strata by profile | Reps nested in profile | No, but see §4 — interpret jointly with E1–E4, not as an independent axis for S1–S4/S6 |
| E7 | Continuous proportion (specificity, conditional on E6 hits; may be N/A at 0 hits) | Generation | Same nesting; additional missing-data structure (N/A when hits=0) requires explicit handling before any test is chosen | No, same caveat as E6 |
| E8 | Agreement (categorical, 2 levels given n=3) + spread (continuous, max−min or CV) | **Profile** (this is the one criterion whose unit of analysis is the profile itself, not the generation) | By definition nested/repeated-measures derived | Yes — explicitly descriptive only, per Doc A §4 E8 item 11 |

**Assumptions that must be checked before any test is selected** (consistent with, and slightly more explicit than, Doc A §8): (a) whether E2/E4's continuous deviations are normally distributed per phase/profile stratum (plausible candidate: non-parametric paired tests, as Doc A already lists, but not yet chosen); (b) whether E6/E7's proportions are bounded-at-0/1 in a way that violates standard parametric assumptions (beta-regression or rank-based methods would need consideration, not decided here); (c) whether the N/A cases in E7 (zero E6 hits) need to be modeled as structural missingness rather than dropped, since dropping them would bias the specificity distribution toward higher-coverage generations; (d) multiplicity policy across 8 criteria × multiple sub-checks, explicitly deferred in both documents and here.

**Everything in this section remains TBD / advisor approval**, as instructed. No test is recommended.

---

## 7. Threats to Validity

| Threat | Mitigation already present | This review's addition |
|---|---|---|
| Deterministic baseline is not ground truth | Explicitly and repeatedly stated in both documents and the locked design | None needed — already sound. |
| E6/E7 are operational proxies for personalization, not quality judgments | Explicitly disclaimed, esp. E7 item 11 | Extend the disclaimer: for S1–S4/S6, state plainly that the proxy substantially overlaps E1–E4 and should not be read as incremental evidence (§4.1). |
| LLM stochasticity | Addressed by the 3-repetition design and E8 | None needed. |
| Profile selection (24 synthetic vignettes) | Stratified design mentioned in the reconciliation doc (experience × distance × injury × edge cases) | Not re-litigated here (out of scope — the task asked about these two documents, not profile sampling design). |
| Prompt/model version changes | Mitigated by the locked requirement to run all calls in one recorded window (Doc A §7, §9 item 9) | None needed. |
| Evaluator implementation bias | Partially addressed via fixed, pre-registered vocabularies/tolerances (Doc A §9 items 4–6; Doc B §14 items 3–4) | Flag that the tolerance values (§6.1 of Doc B, §5 item 11 of Doc A) are still open numbers, not yet frozen — already listed as an open decision, correctly not resolved here. |
| Field alias ambiguity | Explicitly found and resolved-by-convention in Doc B §2c (`goal_distance`/`goal_time` → `target_race_distance`/`target_race_time`), pending advisor confirmation | None needed beyond closing the loop in §9 below (push the resolved alias back into Doc A so only one slot vocabulary exists). |
| E4/T7 blocking issue | Explicitly preserved, not silently dropped, per this review's §1/§2 confirmation | None needed — this is handled correctly. |
| Dependence among E1–E8 | **Only partially addressed** — S5-vs-E3 dependence is disclosed (Doc B §13); S1/S2/S3/S4/S6-vs-E1/E2/E3 dependence is not | **This is the main actionable addition of this review — see §4.1.** Recommend an explicit "E6/E7 slots independent of E1–E4" vs "E6/E7 slots corroborating E1–E4" split before advisor sign-off. |
| Circularity if the evaluator uses the same rules that generated the baseline | Disclosed for E1–E3 ("compliance with the validator's own instructions," Doc A §7 table, row 1) | **Extend explicitly to E7's S1–S4/S6**, which compare against "the baseline's own published constants" (Doc B §6.1) — i.e., the same circularity concern applies to the personalization criteria, not only to the constraint criteria, and should be named as such rather than left implicit. |

---

## 8. Final Verdict

### REQUIRES METHODOLOGICAL REVISION

This is not a judgment that the framework is unsound or needs to be redesigned — E1–E5 and E8 are coherent, well-bounded, and internally consistent across both documents, and E6/E7's *coverage* construct and *S7/exact-day-set specificity* construct are defensible as proposed. The revision needed is narrow and does not require inventing new criteria, new experiments, or new data:

**Blocking issues (must be resolved, or explicitly re-framed, before advisor review proceeds on E6/E7's full claim):**

1. **E7's (and partially E6's) numeric slots S1–S4 and S6 are not independent of E1–E4** (§4.1, §7). Both documents currently present E6/E7 as the framework's defensible, independent personalization evidence; for most of E7's slots this is overstated, because the specificity test and the constraint-fidelity test resolve to the same comparison against the same baseline-derived number. **Required fix (editorial, not structural):** revise Doc A §4 (E6/E7 definitions) and/or Doc B §4–5 to explicitly classify each slot as either "independent personalization evidence" (S7; S5's exact-day-set form) or "corroborating evidence, overlapping E1–E4" (S1, S2, S3, S4, S6), and adjust the framing in Doc A §1/§9/§10 (which currently claims E6/E7 "resolve" the personalization-definition problem without this caveat) accordingly. This does not require dropping any slot or re-running anything — it requires the documents to say, honestly, how much new information each slot actually contributes.

2. **The two documents currently specify two different E6/E7 slot sets** (Doc A's original 9-item `SLOTS` list, including `vdot_band` and `stated_preference`, which Doc B finds have no traceable backing field, §2c/§9; and Doc B's corrected 7-item S1–S7 list). Doc A has not been updated to reflect Doc B's correction. **Required fix:** before advisor review, reconcile into a single authoritative slot list (adopting Doc B's corrected S1–S7, dropping `vdot_band`/`stated_preference` per Doc B's own recommendation, §15) so the advisor reviews one proposal, not two documents that silently disagree on E6/E7's definition. This is a low-effort edit, already fully specified by Doc B — it only needs to be applied back to Doc A (or Doc A needs to explicitly defer to Doc B as the superseding definition).

**Not blocking, but must stay visibly open (already correctly flagged, carry forward unchanged):**
- T7 (baseline cutback-rebound/taper-anchoring) blocking E4 — already correctly gated at the time this review was written, not silently resolved. **STATUS UPDATE (since this review): RESOLVED in a later session** — the rebound was fixed in `generate_weekly_progression_summary`, and taper anchoring was confirmed correct and left unchanged, per `paper/CODE_AUDIT_EASY_RUN_PACE_AND_T7.md`. E4 is no longer blocked by an unresolved engineering decision; this line is retained as the historical record of this review's original finding.
- The S7 action-lexicon/contradiction-codebook curation step — already correctly scoped as a disclosed, bounded, pre-registered exception; no change needed.
- Numeric tolerances (E2/E4/E6/E7) and E8's spread convention (max−min vs CV) — already correctly left as open advisor decisions; no change needed.
- The statistical test — correctly left TBD; no change needed.

### Remaining advisor decisions, once the above two blocking items are addressed editorially
- Confirm the corrected S1–S7 slot list (dropping `vdot_band`, `stated_preference`) and the `goal_distance`/`goal_time` → `target_race_distance`/`target_race_time` alias resolution.
- Confirm whether the "independent vs corroborating" slot classification proposed in §4.1/§8 item 1 is acceptable, or whether the advisor prefers dropping S1–S4/S6 from E7 entirely and relying on S5(exact)/S7 alone for specificity (a stricter but more defensible alternative).
- T7 resolution (fix-or-document the baseline rule engine) before any E4 data collection.
- Tolerance values, E3's type-vocabulary synonym handling, E8's spread convention, and the statistical test — all already correctly deferred.

---

## Required Final Summary Table

| ID | Criterion | Simple Question | Construct | Automated? | Expert Needed? | Baseline Comparable? | Role in RQ2 |
|----|-----------|------------------|-----------|------------|-----------------|------------------------|-------------|
| E1 | Pace/Intensity Fidelity | Did the plan keep the right effort level? | Numeric/categorical preservation of baseline effort-level targets | Yes | No | Degenerate-yes (reference only) | Constraint preservation |
| E2 | Volume Fidelity | Did the plan keep the right mileage? | Numeric preservation of baseline volume | Yes | No | Degenerate-yes (reference only) | Constraint preservation |
| E3 | Structure Fidelity | Did the plan keep the right days/types? | Preservation of baseline day-arrangement | Yes | No | Degenerate-yes (reference only) | Constraint preservation |
| E4 | Multi-Week Trajectory Fidelity | Did the plan keep the right build/cutback/taper shape? | Cross-week volume-trajectory preservation | Yes | No | Degenerate-yes, **T7 RESOLVED since this review** (historical note: blocked at time of writing) | Constraint preservation |
| E5 | Output Validity & Completeness | Is the output usable at all? | Structural/schema validity and field completeness | Yes | No | Partially (parse/schema yes; text-completeness no) | Precondition for all other criteria |
| E6 | Personalization Coverage | Was the runner profile actually used? | Breadth of applicable profile facts reflected, correctly | Yes | No | No (Gemini-only) | Personalization — partly overlaps constraint preservation on numeric slots (§4) |
| E7 | Personalization Specificity | Was the profile used specifically, or only generically? | Instance-value vs generic-category instantiation of E6 hits | Yes (S1–S6); S7 needs a one-time curated lexicon | No (curation ≠ per-sample judgment) | No (Gemini-only) | Personalization — **materially overlaps E1–E4 for S1–S4/S6; independent only for S7 and S5's exact-day-set test (§4.1)** |
| E8 | Cross-Repetition Stability | Does Gemini stay reasonably consistent across 3 runs on the same profile? | Agreement/spread of E1–E7 outcomes across repetitions | Yes | No | No (baseline not repeated, by design) | Reproducibility/stability |

### Accuracy check on the requested plain-language interpretation

> **E6 = profile dipakai**
> **E7 = profile dipakai secara spesifik, bukan sekadar generic**
> **E8 = hasil tetap relatif konsisten ketika Gemini dijalankan 3 kali pada profile yang sama**

- **E6 = profile dipakai: accurate**, with the standard proxy caveat already disclosed in both documents (it measures verifiable textual/structural reference, not a deeper notion of "use").
- **E7 = profile dipakai secara spesifik, bukan sekadar generic: accurate as a description of intent, but currently overstated as a description of what the slot set actually delivers.** For S7 and the exact-day-set reading of S5, the interpretation is accurate and the evidence is independent. For S1–S4 and S6, what is actually being measured is closer to "does the plan match the baseline's already-personalized number" — which is largely the same fact E1–E4 already establish — so calling it evidence of Gemini's *own* specific use of the profile, beyond constraint preservation, is not yet accurate for those slots until the §4.1/§8 fix is applied.
- **E8 = hasil tetap relatif konsisten ketika Gemini dijalankan 3 kali pada profile yang sama: accurate**, including the correct nuance that "relatif konsisten" (relatively consistent) does not mean identical — the agreement/spread formulation already captures exactly this relative/descriptive framing.
