# ADVISOR METHODOLOGY Q&A — Comparative LLM Evaluation

**STATUS AS OF 2 OCTOBER 2026 (LATER SAME DAY): the "2 LLM" design (LLM A vs LLM B) described throughout most of this document is `SUPERSEDED`.** The advisor's new FINAL LOCKED design is **1 LLM only (Gemini) vs the deterministic baseline**, 24 profiles CONFIRMED, 3 Gemini repetitions (72 generations) + 24 baseline plans, exactly 8 automated criteria (definitions still OPEN — see OI-2 below, now expanded), multi-week scope CONFIRMED. See **"Advisor Decision Update — 2 October 2026 (Gemini-only design)"** at the end of this document for the authoritative design and the STATUS SUMMARY that follows it. References below to "LLM A vs LLM B" / 2 LLMs / "16 criteria" describe the superseded design and are kept for audit-trail purposes only.

**Status: PROPOSED — SUBJECT TO ADVISOR APPROVAL**, except where marked APPROVED/CONFIRMED (see "Advisor Decision Update — 2 October 2026", itself `SUPERSEDED` by the Gemini-only update that follows it). Prepared from `RESEARCH_METHODOLOGY_COMPARATIVE_PROPOSAL.md` and the earlier methodology documents. Answers state what is defensible *now*; nothing here is a decision unless tagged APPROVED/CONFIRMED. Tags: `READY FOR ADVISOR REVIEW` (consistent across the documents), `OPEN ISSUE` (a problem found in this audit), `[ADVISOR DECISION REQUIRED]`, `APPROVED/CONFIRMED`, `SUPERSEDED`. **CURRENT (Gemini-only): 1 LLM; 3 Gemini repetitions per profile (72 generations); 24 baseline plans; 24 profiles CONFIRMED; exactly 8 automated criteria locked (definitions open); multi-week scope CONFIRMED.** **SUPERSEDED: the 2-LLM design, and the earlier "16 criteria" draft count.** Expert evaluation remains excluded from the study entirely. Reference numbers [n] follow the current manuscript.

---

## A. Why this design?

**1. Why compare LLMs?** `READY FOR ADVISOR REVIEW`
The personalization layer is where model-dependent behavior enters the system. Prior work reports that the quality of LLM-generated exercise plans varies with the input information given [11] and between models even when repeated prompts are reproducible [12], and that safety and rigor concerns exist [13], [14]. In a hybrid system the LLM is a replaceable component, so knowing how different models behave under identical constraints is design-relevant evidence. The aim is to characterize behavior in this task, **not** to declare the best AI model; results hold only for the tested versions, prompt, profiles and date.

**2. Why is the LLM the independent variable?**
RQ2 asks how models differ. Manipulating only the model while holding profile, baseline, prompt, schema, validator and generation settings constant allows differences to be attributed to the model (within the limits of provider differences, Q10). Other factors (prompt, temperature) are held constant and could be studied later as sensitivity analyses. `READY FOR ADVISOR REVIEW`

**3. Why is a deterministic baseline necessary?**
Physiological and training numbers should not depend on an LLM, which can generate plausible but nonfactual content [16]. The baseline (VDOT-based paces and rule-based progression) gives every model the same reproducible input, supplies the constraints the LLM must keep, and serves as the reference for compliance checks. Limits: the rules are engineering design constraints, not scientific thresholds. Two behaviors were previously undecided (≈25% rebound after a cutback week; taper tied to starting mileage) — **RESOLVED**: the rebound was fixed in code (`generate_weekly_progression_summary`); the taper's tie to starting mileage was confirmed correct and intentional (matches `PAPER_DRAFT.md` Table II) and left unchanged. `READY FOR ADVISOR REVIEW`.

**4. Why is the baseline not a comparator?**
`SUPERSEDED` framing (audit trail): under the 2-LLM design, RQ2 compared LLM A vs LLM B, each receiving the same baseline, and the baseline was a controlled input rather than a comparator. **CURRENT (Gemini-only):** the comparison is now explicitly **deterministic baseline vs Gemini-personalized output**, so the baseline is a direct condition in the comparison — but it is still never treated as "ground truth" for overall plan quality; it remains the controlled reference/constraint source that Gemini is instructed to preserve numerically. Numeric compliance against the baseline is a **fidelity/consistency measure against predefined constraints**, not a quality measure. A rule-only comparator is no longer a separate optional add-on — it is now the primary comparator by design.

---

## B. Profiles, repetitions and size

**5. Why several runner profiles?**
One profile cannot separate model differences from profile-specific behavior; models may behave differently by experience level, injury note, distance or training days. The profile is the sampling unit for generalizing across runners. Limit: profiles are synthetic and not representative of a population. `READY FOR ADVISOR REVIEW`

**6. Why repeated runs?**
Output is stochastic at nonzero temperature; repeated runs separate a model's typical behavior from sampling luck and make stability (e.g., how often a model passes validation across repeats) a measured result. Temperature 0 is **not** assumed deterministic: hosted services can vary through batching, backend or version changes, and some models restrict temperature `[VERIFY per model]`. Repeats are replicates within a cell, not independent runners. `READY FOR ADVISOR REVIEW`; count `[ADVISOR DECISION REQUIRED]`.

**7. Why 24 profiles?** — **24 synthetic runner profiles: CONFIRMED (updated 2 October 2026, Gemini-only design)**
Built for coverage, not derived from a power calculation: 3 experience levels × 3 target distances × injury present/absent = 18 core profiles, plus 6 edge cases (e.g., 1 and 7 training days, shortest and longest plan, aggressive and conservative goal), with a separate pilot set for prompt development. Fewer profiles (about 8–12) would be easier to cover but weakly representative; more (36+) would increase workload without a power rationale. Demographic composition detail within the 24 remains an OPEN SUB-DECISION if not already finalized elsewhere.
`OPEN ISSUE`: the proposal does not yet assign plan durations, 5K bands and mileage bands to the 18 core profiles; durations must allow cutback weeks (a cutback occurs only in plans of at least 6 weeks), which matters now that multi-week scope is confirmed.

**8. Why 3 Gemini repetitions, and why is the baseline not repeated?** — **CONFIRMED (Gemini-only design): 3 Gemini repetitions per profile (→ 72 Gemini generations); the deterministic baseline is generated once per profile (→ 24 baseline plans), never repeated 3×, because it is deterministic and would produce identical output each time.**
Rationale for 3 Gemini repetitions: two repetitions yield a single pairwise difference, three give the smallest practical basis for a within-cell variability estimate, and the total workload stays manageable. **Total outputs for comparison: 24 baseline + 72 Gemini.** This must never be called "96 independent experimental generations" (the baseline and Gemini repetitions are different unit types — one deterministic, one stochastic/repeated) and must never be called "144 generations" or "216 generations" (those were workload estimates under the now-superseded 2-LLM/3-LLM designs). Repetition count is not power-derived; a pilot should inform further tuning.
`OPEN ISSUE`: the exact workload/token-cost implications of the confirmed multi-week context (vs the earlier Week-1-only estimate) are not quantified in the comparative proposal, which still carries the superseded 144/720 Week-1-only figures.

---

## C. Fairness and infrastructure

**9. How is fairness between LLMs ensured?**
Identical profile, baseline, prompt text, JSON schema, validator and tolerances; the same explicitly set generation parameters; model-specific settings documented; exact request payload stored for every call; no model-specific prompt tuning (prompt developed on a pilot set and frozen); no retries; randomized/interleaved run order; comparable access tier; model version and date recorded. Equal numeric settings do not guarantee equal behavior across providers; this is reported. `READY FOR ADVISOR REVIEW`

**10. How are API differences handled?** `SUPERSEDED` cross-provider framing — kept for audit trail only
This question previously concerned a cross-provider fairness issue (Gemini receiving the system prompt concatenated into one user message vs OpenAI receiving a separate system message). **Under the Gemini-only design, there is no second provider, so this specific cross-provider parity question is moot.** What remains relevant: Gemini's own system-instruction delivery mechanism, its JSON-mode mechanism, default safety filters, default sampling parameters and output limits must still be documented and fixed/frozen for reproducibility. Exact Gemini configuration details `[ADVISOR DECISION REQUIRED]`.

**11. How are model/version changes handled?**
Pin dated model snapshots where offered; record the requested and returned model identifier and the timestamp of each call; execute in one short window; store raw outputs; define a contingency (if a model is retired or visibly changed during the study, report it and repeat the affected runs). Silent provider-side changes cannot be excluded and are reported as a limitation. `READY FOR ADVISOR REVIEW`; open-weight/local models as an option `[ADVISOR DECISION REQUIRED]`.

**12. Why must raw output be stored?**
It is the primary evidence: it allows re-scoring with revised criteria, auditing of validator verdicts, and analysis of failures (non-JSON, truncation, refusal). Because generation cannot be reproduced exactly, stored raw output is what makes the *analysis* reproducible. The current code discards the raw response after parsing. `READY FOR ADVISOR REVIEW`

**13. Why must fallback not replace experimental output?**
The production fallback substitutes a deterministic template when output is invalid; that template is identical for every model, so it would hide exactly the differences under study and is not LLM output. The experiment evaluates the raw model output before any fallback, and fallback occurrence is reported separately as a system behavior. This requires an experiment mode that does not use the production dispatcher (implementation only after approval). `READY FOR ADVISOR REVIEW`

---

## D. Measurement

**14. How is personalization measured?**
Not by one number. (a) Objective, rule-based: correct use of profile facts (goal, time, days, injury) and absence of contradictions; (b) users' perceived personalization (PP) in RQ3, kept separate. **Expert ratings of personalization remain excluded from the study** — RQ2 relies solely on automated/objective criteria. Because the numbers are copied from the baseline, personalization in RQ2 is mainly textual. Age, gender, 10K personal best and easy pace do not change any number. The definition of "personalization requirements" and any text-extraction rules `[ADVISOR DECISION REQUIRED]`.

**15. How is constraint compliance measured?** — **UPDATED: exactly 8 automated evaluation criteria, LOCKED (not 16)**
By exactly **8 locked automated evaluation criteria**: profile consistency, goal consistency, physiological/pace consistency, weekly volume/mileage consistency, workout structure, intensity constraints, progression/recovery constraints, and completeness/constraint violations. Output: pass/fail per run, aggregated per profile × condition (baseline/Gemini) cell, with failure categories. Primary indicator: first-attempt validator pass on raw output. Acceptability thresholds `[ADVISOR DECISION REQUIRED]`.
`OPEN ISSUE` (unresolved by this update, flagged not silently picked): the count is now locked at 8, but **exact operational definitions conflict across documents** — `RESEARCH_METHODOLOGY_LOCK.md`'s 8-criterion list, the (superseded) comparative proposal's 16-item draft list, and `PAPER_DRAFT.md` Table IV's 5-criterion list define overlapping but non-identical criteria and groupings. This document does not pick one; reconciling which exact 8 definitions apply is an explicit OPEN SUB-DECISION for the advisor (see OI-2 below).

**16. Why is compliance not training quality?**
Compliance means the output satisfies a specification; here the specification is the system's own engineering design constraints, and numeric compliance is largely enforced by the validator. A plan can comply and still be poorly written, unsuitable or unsafe in its free text; the validator does not check text safety, and it accepts empty text fields. Quality requires judgment (experts) and, for effectiveness, longitudinal evidence the study does not collect. No physiological-optimality or performance claim is made. `READY FOR ADVISOR REVIEW`

**17. How is the multi-week plan evaluated?** — **RESOLVED/CONFIRMED: multi-week scope confirmed; Week-1-only is superseded**
`SUPERSEDED` framing (audit trail): previously, the LLM personalized only Week 1 and Weeks 2+ were identical across models, so multi-week criteria would have described the deterministic engine, not model differences; several options were weighed. **CURRENT:** Gemini now receives sufficient multi-week context via the confirmed pipeline (Runner Profile → Validation → Physiological Calculation → Deterministic Rule-Based Multi-Week Baseline → Gemini Personalization → Server-Side Validation → Gemini-Personalized Multi-Week Plan → Automated Evaluation → Baseline vs Gemini Comparison). For Gemini, which must not change numbers, "progression/cutback/taper consistency" means numeric fidelity to the baseline plus correctness of what the text says about it.
~~`OPEN ISSUE`: RQ1 says multi-week while the current LLM scope is Week 1~~ — RESOLVED: scope is now multi-week, consistent with RQ1's wording.
~~**OPEN METHODOLOGICAL DECISION: The relationship between the multi-week research scope and the specific weeks/context presented to the LLM must be finalized before the comparative experiment.**~~ — RESOLVED by the confirmed pipeline above.

**18. Why use expert evaluation — or why not?** `SUPERSEDED`
**Expert evaluation has been removed entirely from the study** (advisor decision, 2 October 2026): no coach/expert rating, expert rubric, inter-rater agreement, expert recruitment, or blinded expert assessment. RQ2 now relies solely on automated/objective evaluation criteria (Q15). The reasoning previously recorded for and against expert evaluation — automated checks cannot judge appropriateness, practicality, clarity for people or safety of advice; but workload, subjectivity, low inter-rater agreement (reported in [11]) and recruitment burden were significant costs — is kept here for audit-trail purposes only and no longer applies to this study's design.

**19. How does RQ2 differ from RQ3?**
RQ2 evaluates LLM outputs on controlled synthetic profiles, with automated/objective checks only (expert ratings excluded, see Q18); its unit is the profile × LLM cell. RQ3 measures runners' perceptions (PP, PU, PC, RC) with a study-specific, unvalidated questionnaire; its unit is the participant. Expert evaluation is not part of RQ3 and the questionnaire is not an expert questionnaire. The two are never merged into one score; RQ2's automated metrics and perceived clarity (PC) in RQ3 may disagree and are reported separately. How RQ3 relates to the model comparison (one configured model, blinded multi-model exposure, or random assignment) `[ADVISOR DECISION REQUIRED]`. `OPEN ISSUE`: if RQ3 uses one model, the selection rule is undefined.

---

## E. Statistics and validity

**20. How will the statistical test be chosen?**
The test follows the design: paired within profile, with the profile as block and aggregated cells as data. Candidates: Wilcoxon signed-rank or McNemar-type analysis for two models; Friedman or Cochran's Q with post hoc pairwise tests for three or more; mixed-effects models (profile and rater as random effects) if methodological support exists; small samples favor nonparametric/exact methods. Report effect sizes and confidence intervals, pre-specify a small set of primary outcomes, and correct for multiple comparisons. No test or sample size is fixed here; if compliance is near 100% for all models, report it descriptively. `[ADVISOR/METHOD REVIEW REQUIRED]`

**21. What is the unit of analysis?** — **UPDATED for the Gemini-only design**
Primary: the **profile × condition (baseline/Gemini) cell** (repetitions aggregated), replacing the superseded "profile × LLM cell" wording. The runner profile is the primary sampling/block unit; the 3 Gemini repetitions are replicates nested within a profile, not additional independent runners; the single baseline per profile is a deterministic reference, not a replicate. In RQ3 the participant is the unit. `READY FOR ADVISOR REVIEW`
`OPEN ISSUE (contradiction, still present)`: `RESEARCH_METHODOLOGY_LOCK.md` §4.1 and the readiness audit define one generation (profile, model, repetition) as the unit of analysis; this must be updated to the cell-level, profile-blocked definition above to avoid pseudo-replication — and the 72 Gemini outputs must not be treated as 72 independent participants.

**22. What are the main threats to validity?**
Construct: compliance ≠ quality; criteria derived from the system's own rules (circularity); unvalidated questionnaire. Internal: unequal prompt delivery/parameters, fallback mixed with LLM output, order and drift effects, prompt tuned on one model, rater bias. External: synthetic profiles, models at one date, one prompt, Week-1 or sampled-week scope. Statistical: small number of profiles, multiple comparisons, clustering, ceiling effects. Also researcher bias (the designer evaluates the system), rater subjectivity and API drift. Handling: Section 22–25 of the proposal. `READY FOR ADVISOR REVIEW`

**23. What are the limitations of hosted LLM APIs?**
Provider-side model changes can occur under an unchanged model name; outputs vary between calls even with fixed settings; models may be deprecated mid-study; safety filters and rate limits can alter outputs; settings differ by provider; the provider processes the data sent. Mitigation: pinned snapshots where offered, a short execution window, stored raw outputs, recorded returned identifiers, reporting dates; reproducibility of *generation* remains limited. `READY FOR ADVISOR REVIEW`

**24. How is external LLM data processing handled ethically?**
RQ2 uses synthetic profiles and therefore sends no personal data (provided no real person's data are used); provider terms on data use and retention still need to be checked. RQ3 may send participants' own profile data, including free-text injury notes, to external providers: this requires disclosure and informed consent, data minimization (vignettes, coarse injury categories, optional free text), adult-only participation (the application currently accepts ages 12–99), withdrawal and retention rules. Whether ethics review is required has not been confirmed. `[CHECK BINUS REQUIREMENTS]` `[ADVISOR DECISION REQUIRED]`

---

## F. Additional questions an examiner may ask

**25. Which model will be used?** — **UPDATED: CONFIRMED — Gemini only, exact version not yet finalized**
**CONFIRMED (Gemini-only design): 1 LLM — Gemini.** Exact model/version is to be finalized and recorded before experimental data collection `[ADVISOR DECISION REQUIRED]` for the identity string. Selection/configuration criteria (unchanged in spirit): publicly documented version, API access through the study period, deprecation schedule covering it, structured-output ability, comparable generation controls.

**26. Does the study show that Gemini is the best LLM / better than other LLMs?** No — there is no cross-LLM comparison in this design at all (that was the superseded 2-LLM design). The only comparison is Gemini-personalized output vs the deterministic baseline, reported per criterion (8 locked criteria) with no overall ranking, "best," or "winner" framing, and no claim that Gemini "improves" or is "superior" to the baseline unless supported by the (not-yet-chosen) statistical analysis.

**27. Does the system improve running performance?** No such claim: there is no longitudinal outcome measurement. Findings are about compliance, expert-rated quality (if used) and user perception.

**28. Is the literature gap novel?** The proposal does not claim that no one has compared LLMs for exercise or running plans: studies exist on ChatGPT running plans [11] and on GPT-4 vs Gemini hypertrophy plans [12]. The defensible gap is the specific hybrid architecture (deterministic baseline + LLM personalization + server-side validation) evaluated with a controlled same-profile comparison and multi-week constraint evaluation. A documented search protocol and full-text reading of [11], [12], [24] are still required. `[LITERATURE VERIFICATION REQUIRED]`

**29. Why not let the LLM adjust the numbers within bounds?** It would put the LLM into physiological decision-making, contradicting the system principle; it could be a future extension but is not proposed.

**30. Is the current implementation ready?** No: no experiment/run IDs, prompt version, captured model version, raw-output/verdict/error storage or harness; model set by global configuration; silent fallback; different system-prompt delivery; validator accepts empty text. Implementation starts after approval.

---

## OPEN ISSUES found during this audit (consolidated)

| ID | Issue |
|---|---|
| OI-1 | Unit of analysis: lock/readiness audit use the generation; this document now uses the profile × condition (baseline/Gemini) cell (Q21) — still needs updating in the lock/audit files |
| OI-2 | **NOT RESOLVED — flagged explicitly, not silently picked.** Criteria count is now locked at 8, but exact operational definitions conflict: `RESEARCH_METHODOLOGY_LOCK.md`'s 8-criterion list, the superseded comparative proposal's 16-item draft list, and `PAPER_DRAFT.md` Table IV's 5-criterion list define overlapping but non-identical criteria (Q15). Reconciling the exact 8 definitions is an advisor decision. |
| OI-3 | ~~Workload of the recommended multi-week option is not quantified~~ — superseded premise (the old "Week-1-only vs multi-week" option set no longer applies; multi-week is confirmed). Current workload is 24 baseline + 72 Gemini generations under confirmed multi-week scope; exact token/cost implications of multi-week generation are not quantified (Q8) |
| OI-4 | Core profile specification incomplete (durations, 5K bands, mileage bands) — unchanged (Q7) |
| OI-5 | ~~Prompt-delivery parity: no single primary option named; provider documentation unchecked~~ — RESOLVED/moot for cross-provider parity (only Gemini remains); Gemini's own system-instruction/JSON-mode configuration still needs documenting (Q10) |
| OI-6 | ~~RQ1 says multi-week, current LLM scope is Week 1~~ — RESOLVED: multi-week scope confirmed, consistent with RQ1 (Q17) |
| OI-7 | ~~Expert-rating sampling scheme (which runs are rated) undefined (Q18)~~ — RESOLVED/moot: expert evaluation removed from the study (2 October 2026) |
| OI-8 | Relation between RQ3 and the model comparison, and selection of the RQ3 model, undefined — unchanged (Q19) |
| OI-9 | `RESEARCH_METHODOLOGY_NON_COMPARATIVE_PROPOSAL.md` is superseded but carries no notice; risk of confusion — unchanged; also now true of the 2-LLM comparative design itself, which this update addresses |
| OI-10 | The comparative proposal's baseline-freeze section omits the Week-1 ×1.06 vs "matches current capacity" inconsistency noted in earlier audits — unchanged |
| OI-11 | Cross-reference error: §3.3 of the comparative proposal points to "Section 28" for the list of files to modify; that list is in the Appendix — unchanged |
| OI-12 | Pilot phase: size, stopping rule and amendment procedure undefined — unchanged |
| OI-13 | Experiment mode requires bypassing the production dispatcher (fallback, `auto`) — a system change — unchanged |
| OI-14 | ~~Model tier policy undecided; code defaults (`gemini-1.5-flash`, `gpt-4o-mini`) are small/cost tier and may be unavailable~~ — narrows to Gemini only; exact Gemini model/version string still undecided |

## Items marked READY FOR ADVISOR REVIEW
Research title and RQ1/RQ3 wording; the architecture and the role of the baseline (input, constraint source, oracle; not comparator); the LLM-as-independent-variable logic; fairness principles; raw-output and no-fallback rationale; compliance vs quality distinction; unit-of-analysis logic; confounder list; threats to validity; hosted-API limitations; reproducibility record fields; ethics points to check.

## Advisor Decision Update — 2 October 2026 — `SUPERSEDED` (2-LLM design; kept for audit trail only)

~~- **2 LLM design approved**: RQ2 compares LLM A vs LLM B only (Q4, Q25).~~
~~- **3 repetitions approved**: 3 repetitions per (runner profile × LLM) combination; replicates, not independent runners; runner profile remains the block/sampling unit (Q8).~~
- **Expert evaluation excluded from study design**: no coach/expert rating, rubric, inter-rater agreement, recruitment, or blinding (Q14, Q18, Q19; OI-7 resolved as moot). *(Not superseded — still current.)*
- ~~Remaining open/unresolved items preserved from this audit: 24-profile count (Q7, PROPOSED/not confirmed), exact automated-criteria count (Q15, OI-2), exact statistical test (Q20), Week-1-only vs multi-week LLM context (Q17, OI-6), prompt-delivery parity (Q10, OI-5), baseline rule-engine issues, RQ3–RQ2 relation (Q19, OI-8).~~ — see the next section for current status.

## Advisor Decision Update — 2 October 2026 (Gemini-only design)

**This is the current, authoritative design, superseding the 2-LLM comparative design recorded in the update above.**

- **1 LLM (Gemini) CONFIRMED** (Q25); exact model/version to be finalized and recorded before data collection.
- **24 runner profiles CONFIRMED** (Q7) — previously PROPOSED/unconfirmed.
- **3 Gemini repetitions per profile CONFIRMED → 72 Gemini generations** (Q8).
- **Deterministic baseline = 24 plans, generated once per profile, NOT repeated** (Q4, Q8).
- **Exactly 8 automated criteria LOCKED** (Q15) — operational definitions remain OPEN and conflicting across documents (OI-2, not resolved by this update).
- **Multi-week scope CONFIRMED** (Q17, OI-6) via the pipeline: Runner Profile → Validation → Physiological Calculation → Deterministic Rule-Based Multi-Week Baseline → Gemini Personalization → Server-Side Validation → Gemini-Personalized Multi-Week Plan → Automated Evaluation → Baseline vs Gemini Comparison.
- **Expert evaluation still excluded** (unchanged, Q14, Q18, Q19).
- **No ranking/winner framing** (Q26): results are reported per criterion; Gemini is never declared "better" without statistical support.
- **Unit of analysis updated**: profile × condition (baseline/Gemini) cell; profile is the primary block/sampling unit; the 72 Gemini outputs are not 72 independent participants (Q21).
- **Not resolved by this update** (still open/unresolved): exact Gemini model/version; exact 8-criteria operational definitions/thresholds (OI-2 — explicitly flagged, not resolved); exact statistical test (Q20); RQ3 sample size/design/relation to RQ2 (Q19, OI-8); ethics/BINUS requirements (Q24); questionnaire validation/pilot; prompt implementation/reproducibility details (Gemini-specific configuration, OI-5); profile demographic composition detail (OI-4); baseline rule-engine rebound/taper fix-or-document decision.

---

## STATUS SUMMARY

**CONFIRMED:** 24 runner profiles; Gemini as the only LLM; 3 Gemini repetitions per profile; 24 baseline plans; 72 Gemini generations; no expert evaluation; exactly 8 automated criteria (count locked); multi-week personalization; baseline vs Gemini comparison.

**OPEN:** exact Gemini model/version; exact 8-criteria definitions/thresholds (OI-2 — explicit conflict between the lock's 8, the superseded comparative proposal's 16, and the paper's Table IV 5, not resolved here); statistical test; RQ3 sample size; ethics/BINUS requirements; questionnaire validation/pilot; prompt implementation/reproducibility details.
