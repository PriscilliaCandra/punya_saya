# ADVISOR REVIEW PACKAGE

**Project:** AI-based personalized running training recommendation (S2 thesis prototype, BINUS University)
**STATUS AS OF 2 OCTOBER 2026 (LATER SAME DAY): the "2 LLM" design referenced below is `SUPERSEDED`.** New FINAL LOCKED design: 1 LLM only (Gemini) vs the deterministic baseline; 24 profiles CONFIRMED; 3 Gemini repetitions (72 generations) + 24 baseline plans (not repeated); exactly 8 automated criteria (definitions OPEN); multi-week scope CONFIRMED. See "Advisor Decision Update — 2 October 2026 (Gemini-only design)" at the end of this document and the STATUS SUMMARY that follows it.

**Package status:** for supervisor review — **methodology NOT YET APPROVED, except where marked APPROVED/CONFIRMED (CURRENT: 1 LLM — Gemini; 3 Gemini repetitions per profile, 72 generations; 24 baseline plans, not repeated; 24 profiles CONFIRMED; exactly 8 criteria locked; multi-week scope CONFIRMED; expert evaluation excluded entirely — see "Advisor Decision Update — 2 October 2026 (Gemini-only design)" at the end) · data collection NOT STARTED · RQ2 experiment NOT STARTED**
**Source documents:** `RESEARCH_METHODOLOGY_LOCK.md`, `RESEARCH_READINESS_AUDIT.md`, `PAPER_DRAFT.md`, `EVIDENCE_MAP.md`, `PAPER_GAPS.md`, `QUESTIONNAIRE_TRACEABILITY.md`, `REFERENCES_VERIFICATION.md`, `CITATION_AUDIT.md`, the phase design/report documents and the repository code. This package summarizes them; it adds no new evidence and takes no methodological decision. Nothing here is a research result.

Markers used: **[ADVISOR DECISION]** = needs the supervisor's decision; **[BINUS CHECK]** = must be confirmed with BINUS/the supervisor; **[NOT IMPLEMENTED]** = missing in the repository today.

---

## 1. Research title

- **English:** "Design and Evaluation of an AI-Based Personalized Running Training Recommendation System" (identical in the README and the manuscript title).
- **Indonesian:** "Perancangan dan Evaluasi Sistem Rekomendasi Latihan Lari Personal Berbasis AI" (appears in the manuscript as an Indonesian working title).
- **Wording difference found:** the software's internal project name (`PROJECT_NAME` in `backend/app/config.py`) is "AI Running Training Recommendation System (Academic Prototype)". It is not the research title; no change was made.

---

## 2. Research problem

Recreational runners usually follow generic training plans that do not reflect their current fitness, available training days, goal distance or injuries; personalizing a plan normally requires coaching expertise. Large language models (LLMs) can write fluent, individualized plans, and studies have begun to evaluate ChatGPT-generated running plans with coaching experts (Düking et al., 2024, rated sub-optimal and better with more input information), but the literature reviewed also reports variability between models and prompts, low-rigor evaluation designs and safety concerns for LLM-generated exercise plans. A distance, pace or weekly volume that an LLM alters silently can make a plan inconsistent with the runner's profile.

The approach studied here limits what the LLM is allowed to do. Deterministic running-domain calculations (a VDOT-based fitness index and training paces) and training constraints (weekly progression, long-run share, cutback weeks, taper) first produce a baseline plan; the LLM then personalizes the *wording* of the first week; a server-side validator rejects any output that changes the computed numbers or the plan structure, and a deterministic fallback is used if validation fails. The motivation is to keep numerical and structural content under programmatic control while still using an LLM for natural-language personalization. The rule constants are engineering design constraints of this system, not established scientific thresholds.

This work does not train a machine-learning model, does not claim that the system improves athletic performance or prevents injury, and has no clinical validity. The literature search supporting the research gap is not yet documented as a protocol, so no novelty claim beyond the cited literature is made.

---

## 3. Research objective (from the methodology lock)

| Element | Objective |
|---|---|
| **System/design objective** | To explore a hybrid recommendation design in which deterministic running-domain calculations and training constraints establish a baseline plan, an LLM personalizes it, and server-side validation is applied after personalization. The software prototype is the **research artifact**; feature count is not a contribution. |
| **Technical validation objective** | To verify, with explicit pass/fail criteria (T1–T14), that the implemented artifact conforms to its own specification. This makes no claim about training effectiveness. |
| **LLM comparison objective** | **UPDATED (Gemini-only, CONFIRMED):** to compare **Gemini-personalized output vs the deterministic baseline** under identical/controlled conditions (same runner profile, same deterministic multi-week baseline given to Gemini as context, same prompt and schema), using the 8 locked automated/objective evaluation criteria (expert evaluation excluded). ~~Compare 2 LLMs (APPROVED/CONFIRMED)~~ superseded. [EXPERIMENT REQUIRED] |
| **User evaluation objective** | To study how runners perceive the generated plans in terms of personalization, usefulness, clarity and confidence, using a study-specific, currently unvalidated questionnaire. [DATA REQUIRED] |

Out of scope: performance or injury outcomes, clinical validity, longitudinal adherence, comparison of complete applications.

---

## 4. Research questions (exact wording from the methodology lock)

**RQ1:** How can a hybrid AI-based system generate personalized multi-week running training plans by combining deterministic training constraints with LLM-based personalization?

**RQ2 — `SUPERSEDED` (2-LLM wording, audit trail only):** How do different large language models, given the same runner profile and the same deterministic baseline plan, differ in personalizing the plan while remaining consistent with the runner profile and predefined training constraints? RQ2 compared exactly 2 LLMs ("LLM A", "LLM B") using automated/objective evaluation criteria only.

**RQ2 — CURRENT (Gemini-only, LOCKED):** How does Gemini-based personalization differ from a deterministic baseline in generating personalized multi-week running training plans while maintaining predefined training constraints? (Indonesian: "Bagaimana personalisasi berbasis Gemini berbeda dari deterministic baseline dalam menghasilkan rencana latihan lari multi-minggu yang dipersonalisasi dengan tetap mempertahankan constraint latihan yang telah ditentukan?"). RQ2 compares Gemini-personalized output vs the deterministic baseline using the 8 locked automated/objective evaluation criteria only, and must never conclude with an overall ranking, "best," or "winner," nor claim Gemini is "better"/"improves"/"superior" without statistical support.

**RQ3:** How do users perceive the generated training plans in terms of personalization, usefulness, clarity, and confidence?

| | What is being studied | Evidence required | Current status |
|---|---|---|---|
| **RQ1** | Whether the implemented hybrid pipeline (rule engine → LLM personalization → server-side validation → fallback → scheduling) behaves according to its specification | Pass/fail results for T1–T14 on a frozen commit with a recorded environment | Prototype implemented; 194 tests pass; 12 of 14 criteria not fully covered (Section 7) |
| **RQ2** | How different LLMs behave as the personalization layer when only the model varies | Raw outputs, validator verdicts, run metadata, automated/objective metrics under an approved protocol (expert ratings excluded, see Section 11) | Not started; infrastructure missing (Section 9); protocol undecided |
| **RQ3** | Runners' perceived personalization, usefulness, clarity and confidence | Anonymous questionnaire responses under approved consent/ethics, from a validated-as-approved instrument | Not started; instrument unvalidated; application not ready |

---

## 5. Proposed research architecture

**CURRENT (Gemini-only, LOCKED):**
```
Runner Profile → Validation → Physiological Calculation → Deterministic Rule-Based Multi-Week Baseline
      → Gemini Personalization → Server-Side Validation → Gemini-Personalized Multi-Week Plan
      → Automated Evaluation → Baseline vs Gemini Comparison
```
`SUPERSEDED` generic diagram (audit trail only):
```
Runner Profile → Validation → Physiological Calculation → Rule-Based Baseline Plan
      → LLM Personalization → Server-Side Validation → AI-Personalized Plan → Evaluation
```

| Stage | Function |
|---|---|
| Runner profile | Age, gender, experience, 5K (and optional 10K) personal best, target race and time, weekly mileage, training days and preferred days, plan duration, optional injury note, easy-run pace |
| Validation | Schema checks (formats, ranges); invalid input is rejected |
| Physiological calculation | VDOT from the 5K personal best; training pace zones (easy, marathon, threshold, interval, repetition); target race pace; feasibility class |
| Rule-based baseline | Multi-week plan (4–24 weeks): weekly volume progression, cutback weeks, taper, long run, quality session, easy runs, rest days, day placement |
| Gemini personalization | Gemini receives the profile, VDOT, zones and **sufficient multi-week baseline context (CONFIRMED, supersedes Week-1-only)**, and may rewrite explanatory text (warm-up, execution cues, injury-related notes, rationale) across weeks |
| Server-side validation | Rejects output that changes workout type, distance, pace, intensity zone, weekly mileage, day set, or training/rest-day counts; on failure, or if no key/API error/malformed JSON, a deterministic template fallback is used |
| Gemini-personalized plan | Validated multi-week plan with personalized text (supersedes the earlier "Week 1 only, Weeks 2+ have no LLM text" scope) |
| Evaluation | Technical validation, LLM comparison, user evaluation |

Principles: the deterministic rules constrain the physiological and training logic; the LLM is used for personalization and natural-language generation and does **not** independently determine physiological rules; the server-side validator checks the generated output. The validator checks numbers and structure, **not** the safety or accuracy of free-text advice.

---

## 6. Current system implementation (repository facts)

| Item | Status |
|---|---|
| Repository state | HEAD `224d910`. No tracked file is modified; the research/audit documents and the Word generator are **untracked** (so the working tree is not literally "clean") |
| Tests | `pytest`: **194 passed** (re-run during the readiness audit); frontend production build succeeds |
| Backend | Python 3.11, FastAPI, Pydantic, SQLAlchemy on SQLite, Alembic (3 migrations), `httpx` for LLM calls, `slowapi` rate limiting |
| Frontend | React 19, Vite, Tailwind CSS |
| Database | Tables for users, profiles, sessions, reset tokens, runner profiles, training plans (rule-based and AI plan stored as JSON), plan evaluations, planned workouts (7 rows per week), workout logs |
| Authentication/security | Argon2 password hashing; hashed session tokens in an HttpOnly cookie (SameSite=Lax); Origin/Referer CSRF check; owner-only plan access (404 otherwise); configurable rate limits; no email provider (reset links are logged) |
| Workout logging | Create/list/read/update/soft-delete logs; optional link to a planned workout (owner-only) |
| Multi-week plans | 4–24 weeks; all weeks scheduled for authenticated users; dates derived from the start date; LLM receives and returns every baseline week (per-week validation); effectiveness of that multi-week personalization not yet evaluated |
| Deterministic progress insights | Weekly totals and at most two template sentences comparing recent weeks; no LLM and no scores |
| Research mode | Anonymous plan generation, baseline vs. AI-personalized view, four single 1–5 ratings (one per construct) with optional comment, descriptive statistics page |
| LLM providers | Gemini and OpenAI only (defaults `gemini-1.5-flash`, `gpt-4o-mini`, temperature 0.4); these defaults are placeholders, not chosen models |
| Data | The development database holds test rows only (19 plans, 11 evaluations, all plans produced by the fallback). **No experiment or participant data have been collected** |

---

## 7. RQ1 — technical validation (T1–T14)

**Not complete.** Status from `RESEARCH_READINESS_AUDIT.md`: **2 criteria fully covered · 9 partially covered · 2 not ready · 1 requires an advisor decision.**

| Criterion | Purpose | Current status | Evidence gap |
|---|---|---|---|
| T1 Input validation | Invalid profiles are rejected (HTTP 422), valid ones accepted | PARTIALLY READY | No tests for age bounds, target-time format, race distance, duration limits, mileage limits, empty preferred days |
| T2 VDOT | VDOT matches an independent recomputation; deterministic | PARTIALLY READY | Only a range test (37–40); no independent oracle; reference source not chosen |
| T3 Pace zones | Zones follow the inversion formula and are ordered | NOT READY | Test only checks that keys exist; zone fractions not verified against the published source |
| T4 Number of weeks | Plan length equals requested duration (4–24) | PARTIALLY READY | 5 of 21 durations tested (4, 8, 12, 16, 24) |
| T5 Weekly structure | 7 days Mon–Sun; training-day count as requested | PARTIALLY READY | Not asserted for every week × every day count |
| T6 Rule conformance | Distances equal the documented formulas | PARTIALLY READY | `test_t7_progression_fix.py` (new) now covers cutback/taper values and the post-cutback build step; no test yet for caps, floors, quality share |
| T7 Known rule-engine properties | Fix or document rebound and taper behavior | **RESOLVED** | Rebound fixed in code; taper anchoring confirmed correct and unchanged. See `paper/CODE_AUDIT_EASY_RUN_PACE_AND_T7.md` |
| T8 Prompt construction | Prompt contains profile, VDOT, zones, Week 1 baseline and preservation instruction | NOT READY | No test; no prompt version |
| T9 Server-side validation | Each violation class is rejected; valid plan passes | PARTIALLY READY | Not tested: workout type, intensity zone, unknown/duplicate day, rest-day and training-day counts |
| T10 Fallback | Baseline-identical fallback on any failure, label recorded | PARTIALLY READY | Not tested: HTTP error/timeout, OpenAI path, `auto` order, stored fallback label |
| T11 Scheduling | 7 × weeks rows; dates correct | PARTIALLY READY | Rows tested for 4, 8, 24 weeks only |
| T12 Planned/actual integration | Derived status, owner-only linking, soft delete | READY | Covered by 28 + 11 + 28 tests and week-tracking tests |
| T13 Authorization/security | Non-owner 404, CSRF, authentication | READY | Rate limiting has only 2 tests (outside the criterion wording) |
| T14 Whole suite on a frozen commit | All tests pass on a designated freeze commit in a recorded environment | PARTIALLY READY | Suite passes today; no freeze tag; environment not recorded; dependencies unpinned |

Technical validation reports pass/fail only; it makes no statement about plan quality or effectiveness.

---

## 8. RQ2 — controlled LLM comparison (conceptual design; values undecided)

- **Comparison condition (CURRENT):** deterministic multi-week baseline vs Gemini-personalized output. ~~**SUPERSEDED independent variable:** the LLM (provider + model + version) used for personalization, compared across 2 LLMs.~~ Complete applications are not compared.
- **Potential controlled variables:** runner profile; deterministic baseline; prompt; system instruction; output schema; generation parameters; validator version and tolerances; rule-engine version (also time window, retry policy, timeout).
- **Potential dependent variables:** validator compliance (JSON/schema validity, first-attempt pass, failure category, numerical deviation); completeness, latency, token usage, between-repetition variability (Gemini's 3 repetitions). Measured against the 8 locked automated criteria. **Expert-evaluation criteria remain removed from the study (unchanged).**
- **Scope fact (UPDATED):** Gemini sees and personalizes **sufficient multi-week context (CONFIRMED)**. ~~Week 1 only~~ superseded. ~~OPEN METHODOLOGICAL DECISION…~~ RESOLVED.
- **Baseline is now the primary comparator**, not merely an optional additional control; the deterministic template fallback remains an optional additional control.

**CONFIRMED (2 October 2026, Gemini-only design — supersedes the same-day 2-LLM resolution):** 1 LLM (Gemini); 24 runner profiles; 3 Gemini repetitions per profile (72 generations); 24 baseline plans (not repeated); exactly 8 automated criteria locked; multi-week scope confirmed; expert evaluation excluded entirely.
**Not yet decided [ADVISOR DECISION]:** exact Gemini model/version and pinning policy; exact 8-criteria operational definitions (conflict flagged — see Section 11); profile demographic composition detail; temperature value, token limit, seed policy; time window and call order.

---

## 9. RQ2 — experimental infrastructure gap

The repository's LLM code serves web requests, not experiments. Today it does **not** have:

- experiment ID or run ID **[NOT IMPLEMENTED]**;
- prompt version or prompt hash **[NOT IMPLEMENTED]**;
- captured model version (only the configured alias is stored per plan) **[NOT IMPLEMENTED]**;
- raw output storage (the raw response is discarded after parsing) **[NOT IMPLEMENTED]**;
- validator verdict storage (only a log line) **[NOT IMPLEMENTED]**;
- error storage (only the exception type name is logged) **[NOT IMPLEMENTED]**;
- a reproducible experiment harness: the model is a global setting, a silent fallback can mask failures, and neither per-call timestamps, latency, token usage nor the git commit are recorded **[NOT IMPLEMENTED]**.

Also: `requirements.txt` uses `>=` ranges and no environment is recorded.

> **RQ2 should not be executed until the experimental protocol and required infrastructure are approved.**

---

## 10. RQ2 confounders (from the readiness audit)

| # | Issue | Possible impact | Proposed handling (not implemented) | Advisor decision? |
|---|---|---|---|---|
| 1 | ~~Gemini receives the system prompt concatenated into one user message; OpenAI receives a separate system message~~ | **MOOT under the Gemini-only design** (no second provider) | Document Gemini's own system-instruction delivery mechanism for reproducibility | No (resolved by design) |
| 2 | Rubric criteria 2–4 (pace, volume, distribution) overlap with what the validator already enforces | Compliance is read as quality; three "independent" criteria are one family; the validator is both gate and outcome (circularity) | Report them as compliance, with failure categories; do not interpret as subjective quality | Yes |
| 3 | ~~The LLM sees Week 1 only, so progression consistency cannot be measured automatically~~ | **RESOLVED**: multi-week scope is CONFIRMED (Section 8); progression consistency is now measurable via automated rule checks across the confirmed multi-week context | Automated rule check for invented/contradictory statements (`SUPERSEDED`: expert check removed) | No (resolved by design) |
| 4 | The validator accepts empty text fields (text fields default to `""`) | A plan with no personalization text can "pass" | Check text completeness separately; do not infer completeness from validator pass | Yes (completeness definition) |
| 5 | Different JSON-enforcement mechanisms and default safety filters between providers | Output format/refusal behavior differs | Record settings; document differences | Yes |
| 6 | Models differ in output length (verbosity) | Expert ratings may favor longer text | Blinding and length-normalized presentation where feasible; report length | Yes |
| 7 | Stochastic sampling at temperature 0.4, no seed, repetitions undecided | Run-to-run variation | Repetitions; record variability | Yes |
| 8 | Provider alias drift, model retirement (the default `gemini-1.5-flash` may not stay available) | Results tied to a moving target | Pin identifiers; record returned version; run in one time window | Yes |
| 9 | Time-of-day, rate limits, call order | Latency/error effects | Interleave order; log HTTP status and timing | Minor |
| 10 | Silent fallback and `auto` provider mode | Template text could be counted as LLM output | No silent fallback in experiments; flag fallback runs | Yes |
| 11 | Researcher wrote the prompt, baseline, validator and rubric | Researcher bias | Fix protocol before data; blinded rating; report all runs; consider preregistration | Yes |
| 12 | Free-text injury notes may affect models differently | Sensitivity to profile content | Include profiles with and without injury notes | Yes |
| 13 | Baseline rule decisions taken after data generation | Stored baselines would not match results | Freeze baseline first (Section 14) | Yes |
| 14 | ~~Expert-rater subjectivity, no consensus on plan criteria, fatigue/order effects~~ | `SUPERSEDED` (2 October 2026) — expert evaluation removed from the study; no raters | n/a | Resolved |

---

## 11. Expert evaluation — `SUPERSEDED`: REMOVED FROM THE STUDY (Advisor Decision, 2 October 2026)

**Expert evaluation is excluded entirely from this study.** No coach/expert rating, expert rubric, inter-rater agreement, expert recruitment, or blinded expert assessment will be used. RQ2 relies solely on automated/objective evaluation criteria — **count now LOCKED at exactly 8** (2 October 2026, Gemini-only design). **OPEN SUB-DECISION, flagged not resolved:** the exact operational definitions of these 8 criteria are not reconciled across `RESEARCH_METHODOLOGY_LOCK.md` §5 (its own 8), `RESEARCH_METHODOLOGY_COMPARATIVE_PROPOSAL.md` §16 (superseded 16-item draft), and `PAPER_DRAFT.md` Table IV (5 criteria).

The previous proposal below is kept for audit-trail purposes only and no longer applies:
- ~~Rubric (candidate): (1) runner-profile consistency, (2) pace consistency, (3) weekly-volume consistency, (4) workout-distribution consistency, (5) progression consistency, (6) output completeness, (7) personalization quality, (8) reliability/efficiency~~
- ~~Blinding, number of experts, recruitment, inter-rater reliability method~~

Progression consistency (criterion 5) is now evaluated via automated rule checks only (e.g., no invented/contradictory statements), or marked N/A given the Week-1-only scope — see the OPEN METHODOLOGICAL DECISION in Section 8.
No composite score and no weights are proposed; an unweighted, criterion-by-criterion profile remains recommended.

---

## 12. RQ3 — user study (design not chosen)

- **Target population (proposal):** recreational runners able to provide a 5K personal best and weekly mileage.
- **Adult-only requirement (proposal):** adults only. The application currently accepts ages 12–99, so this must be enforced or approved otherwise **[BINUS CHECK]**.
- **Constructs:** Perceived Personalization (PP), Perceived Usefulness (PU), Perceived Clarity (PC), Recommendation Confidence (RC), four items each, planned 5-point agreement scale.
- **Questionnaire status:** study-specific and currently unvalidated (Section 13).
- **Known confounding:** the rule-based baseline contains little warm-up/execution text, while the personalized plan adds it by design. Differences in perceived clarity or personalization therefore reflect added text **plus** LLM use, not LLM use alone.
- **Template-text control (proposal):** include the deterministic template fallback as a comparison so that "more text" can be separated from "LLM text" **[ADVISOR DECISION]**.
- **Also open:** which LLM and prompt version supplies the "AI" plan; Week 1 vs. full plan; participant's own profile vs. vignette; the AI arm must use live LLM output (all stored development plans used the fallback).

**Not chosen here — advisor decisions:** within-subject vs. between-subject vs. single-arm design · sample size (approaches only: pilot-based, precision-based, power-based with an assumed effect size, reliability-based) · recruitment method.

---

## 13. Questionnaire

**The questionnaire is study-specific and currently unvalidated.** No item is adapted from a validated scale; no validation step has been performed. Items must not be called validated.

| Construct | Planned items | Conceptual basis |
|---|---|---|
| PP — Perceived Personalization | PP1–PP4 | No established scale identified; loosely related to perceived recommendation quality in user-centric frameworks |
| PU — Perceived Usefulness | PU1–PU4 | Usefulness is among qualities addressed by the ResQue framework (Pu et al., 2011) |
| PC — Perceived Clarity | PC1–PC4 | Study-specific; link to explanation/transparency unconfirmed |
| RC — Recommendation Confidence | RC1–RC4 | Study-specific; link to confidence/trust unconfirmed |

Item wording is a proposal in `QUESTIONNAIRE_TRACEABILITY.md` (not in the repository or the paper; wording not reproduced or changed here).

**Identified issues (from the readiness audit):**
- **PC4** is double-barrelled (warm-up and recovery); the baseline plan also has no warm-up field.
- **PP4** (contrastive wording) and **PC3** ("each type" universal quantifier) have wording concerns.
- **Mildly leading:** PP1, PP3, PP4, RC2.
- **Overlap:** PP1/PP4; PU1/PU3/PU4; PC1/PC4; RC1/RC3.
- **Construct-fit doubts:** PP2, PU2, PC3, RC1, RC3; **PP3** needs a "not applicable" option for runners without injuries; PC1/PC4 are not equivalent across the two plan types.
- **Scale mismatch:** the current application uses non-agreement anchors (e.g., "1 - Very Generic … 5 - Highly Personalized"), pre-filled sliders (5/5/5/4), visible plan labels, no participant code, and one single rating per construct, not 16 items.

**Validation path (proposed):** construct literature review → item review → expert/content review → pilot test → wording revision → final questionnaire → main data collection. None started.

---

## 14. Baseline freeze

**RESOLVED.** Both issues below have been decided and implemented (rebound fixed; taper confirmed correct as-is). The baseline (24 profiles) has **not yet been generated/frozen** — that remains a separate, later step, now unblocked by this resolution. Existing stored plans would not change if the rules were changed (plans are stored as JSON); newly generated plans do differ for the rebound fix.

| Issue | Prior behavior (historical) | Current behavior (post-fix) | Resolution |
|---|---|---|---|
| **25% post-cutback rebound** | A cutback week was 0.85 × the running volume, which was not reset, so the next build week was about +25% above the cutback week. Example: 25.3 km → 31.6 km | The cutback week's own reduced volume now becomes the reference for the next build step: 25.3 km → 26.8 km (≈ +6%, a normal build step) | **FIXED** in `generate_weekly_progression_summary` (`current = vol` after a cutback); verified by `backend/tests/test_t7_progression_fix.py` and a 201/201 full-suite pass |
| **Taper tied to starting mileage** | Second-to-last week 0.85 × and last week 0.55 × the starting mileage, not the peak; code comment incorrectly said "~75% of peak" | Unchanged — same formula, anchored to starting mileage. Comment corrected to describe the actual, correct behavior | **CONFIRMED CORRECT, documented as-is** — matches `PAPER_DRAFT.md` Table II ("times the base (starting) mileage"); not changed to peak-anchored |

Other freeze-relevant observations (reported, undecided): Week 1 volume is current × 1.06/1.08, while the explainability text says it "matches current capacity"; minimum-distance floors can make realized weekly distance differ slightly from the target; age, gender, 10K PB and easy-run pace do not change any number (and `easy_run_pace` has been confirmed, in a separate decision, excluded from E6/E7).

---

## 15. Ethics / BINUS requirements

Ethics/research-review requirements have not yet been confirmed and should be checked with the supervisor/BINUS before participant recruitment or collection of health-adjacent information.

Points to bring to that check (no position is taken on whether review is required):
- **Adult participants:** the application currently accepts ages 12–99; minors would need explicit handling.
- **Injury/health-adjacent notes:** the profile includes a free-text injury field.
- **External LLM API transmission:** profile data, including the injury text, are sent to third-party providers (Google, OpenAI) when a live LLM is used.
- **Informed consent and data disclosure:** the application has no consent flow; information sheet, withdrawal, retention and storage rules are undefined.
- ~~**Experts** who rate plans are also human participants.~~ `SUPERSEDED` (2 October 2026) — expert evaluation removed from the study; no expert raters.
- Existing database rows are development data and must not be mixed with study data.

---

## 16. Current research status

**READY FOR ADVISOR REVIEW**

- Prototype implemented (rule engine, LLM personalization with validation and fallback, multi-week scheduling, planned/actual logging, research evaluation page).
- Preliminary technical validation exists: 194 tests pass; 12 of 14 technical criteria are not yet fully covered.
- Methodology is not yet approved.
- RQ2 experiment not started; infrastructure missing.
- RQ3 data collection not started; instrument unvalidated; application not ready.
- No empirical performance claims. The project is **not** ready for experiment or data collection.

---

## 17. Decisions required from the supervisor

| Priority | Decision | Why it matters |
|---|---|---|
| 1 | ~~Scope of RQ2: Week-1 personalization only, or multi-week LLM content~~ | **RESOLVED (2 October 2026): multi-week scope CONFIRMED.** Changes the progression criterion, the prompt and the harness accordingly. |
| 2 | RQ2 model identity (which specific Gemini version) | Count **RESOLVED (2 October 2026, Gemini-only): 1 LLM (Gemini)** — supersedes the same-day 2-LLM resolution; default in code is only a placeholder for the exact version |
| 3 | Model/version control (pinning, prompt delivery parity, prompt freeze, generation parameters) | Without it, results are not attributable to the model and cannot be reproduced |
| 4 | ~~Baseline rule-engine freeze/fix (rebound, taper, Week-1 factor)~~ — **RESOLVED** (rebound fixed; taper confirmed correct; Week-1 factor was never in question) | Baselines and stored results must correspond to one rule-engine version; later changes invalidate them. The 24-profile baseline generation/freeze step itself is still pending (separate from this resolved decision) |
| 5 | Composition detail of the 24 runner profiles | Count **RESOLVED: 24 CONFIRMED**; exact demographic composition within the 24 remains an open sub-decision |
| 6 | ~~Repetitions per model~~ | **RESOLVED (2 October 2026, Gemini-only): 3 Gemini repetitions per profile (72 total); 24 baseline plans, not repeated** |
| 7 | Rubric methodology (kept criteria; unweighted vs. composite; treatment of validator-derived and progression criteria) | Prevents compliance being reported as quality; criteria count not final |
| 8 | ~~Expert definition and count; blinding; reliability method~~ | **RESOLVED (2 October 2026): expert evaluation excluded entirely from the study** |
| 9 | Ethics/research-review requirement and consent/data-protection rules (BINUS) | Gates any participant or expert data collection |
| 10 | RQ3 study design (within, between, single-arm) and which plan is shown | Fixes analysis, sample needs and conclusions |
| 11 | Sample-size approach and pilot size | Determines feasibility and what can be claimed |
| 12 | Template-text control (yes/no) | Without it, text amount is confounded with LLM use |
| 13 | Questionnaire validation process (panel, pilot, adaptation from ResQue, scale and "not applicable") | Instrument cannot be called validated otherwise |
| 14 | Participant eligibility, recruitment, external-API transmission of participant data | Privacy and ethics consequences |
| 15 | Analysis approach (descriptive only vs. inferential; preregistration) | Must be fixed before seeing data |

---

## 18. Advisor meeting questions (from `RESEARCH_READINESS_AUDIT.md` §13, wording preserved)

1. ~~**Scope of RQ2:** is evaluating the LLM on Week-1 personalization only acceptable, or must the LLM handle multi-week content?~~ — **RESOLVED: multi-week scope CONFIRMED.** Remaining: are technical-validation criteria T1–T14 sufficient evidence for RQ1 under the extended multi-week pipeline?
2. ~~**Which LLMs** (number, exact versions, access/cost)~~ — **RESOLVED: 1 LLM (Gemini).** Remaining: exact version, access/cost, version-pinning policy?
3. **Prompt parity:** accept provider-specific delivery (Gemini concatenation vs OpenAI system role; different JSON modes) or require alignment? Freeze the prompt before the run? Run a prompt-sensitivity check?
4. **Generation conditions:** temperature value, token limit, seed policy, retry policy (none today), time window.
5. ~~**Stimulus set:** how many runner profiles, which strata?~~ — **RESOLVED: 24 profiles; 3 Gemini repetitions per profile (72 total); 24 baseline plans, not repeated.** Remaining: exact strata/demographic composition.
6. **Baseline freeze:** ~~fix or document the post-cutback rebound and the starting-mileage-anchored taper~~ — **RESOLVED** (rebound fixed; taper confirmed correct). Who approves the baseline version, and when the commit is tagged before generating the 24 profiles' baselines, remain open.
7. **Rubric:** which criteria are kept; unweighted profile or composite (and how weights would be justified); is validator-derived "consistency" acceptable as an outcome given its circularity; how to treat the progression criterion that cannot be measured from Week 1?
8. ~~**Expert evaluation:** number and qualifications of experts, blinding method, rubric source ([11]), reliability statistic, workload~~ — **RESOLVED: expert evaluation excluded entirely.** Still open: include baseline-only and template controls?
9. **RQ3 design:** within-subject, between-subject or single-arm; Week 1 or full plan; participant's own profile or vignettes; which "AI" plan (which model/prompt) is shown?
10. **Sample size and pilot:** which approach to justify the main-study sample, the pilot sample, and the minimum for reliability estimation?
11. **Eligibility and recruitment:** adults only? exclusions? channels? (The application currently accepts ages 12–99.)
12. **Ethics:** which review route or exemption applies at BINUS; required consent, information sheet, withdrawal and retention rules.
13. **External LLM transmission:** may participant profiles (including injury text) be sent to third-party LLM APIs; if not, redaction or vignettes?
14. **Questionnaire:** accept the 16 study-specific items with the validation path (panel size, pilot size)? May items be adapted from ResQue after reading its item list? Scale format and "not applicable" option?
15. **Analysis:** descriptive only, or inferential tests (which, with what multiplicity control)? Preregistration of the protocol?

*Clarification added to question 1:* it contains two questions — (a) Week-1-only vs. multi-week LLM scope, and (b) whether T1–T14 are sufficient evidence for RQ1; please answer both.
*Clarification added to question 6:* "Week-1 ×1.06 behavior" means that Week 1 volume is current weekly mileage × 1.06 (or × 1.08), not equal to the current mileage.

---

## 19. Recommended decision sequence

```
Advisor methodology approval
        ↓
Freeze research protocol
        ↓
Resolve/freeze baseline rules
        ↓
Finalize questionnaire
        ↓
Confirm ethics requirements
        ↓
Implement RQ1 missing tests
        ↓
Implement RQ2 experiment harness
        ↓
Run controlled RQ2 experiment
        ↓
Finalize RQ3 study protocol
        ↓
Pilot/content validation as approved
        ↓
Collect participant data
        ↓
Analyze results
        ↓
Update paper
        ↓
Final manuscript
```

Dependencies and flexibility (this is not a strict order where the methodology document says otherwise):
- The **baseline freeze** must come before any RQ2 generation or RQ3 data collection (a baseline change invalidates stored results).
- The **prompt freeze and model selection** must come before the RQ2 run; the harness depends on the parameters decided in the protocol.
- **Ethics confirmation** is required before any participant or expert data collection; it can proceed in parallel with RQ1 tests and harness work.
- **RQ1 missing tests** can run in parallel with ethics work, but the T6 oracle depends on the baseline decision and T14 on the freeze commit.
- **Questionnaire finalization** (content validation, pilot) should precede the main RQ3 data collection; the RQ3 protocol depends on the chosen RQ3 design and on which LLM/prompt supplies the AI plan, so it may follow the RQ2 run as listed, or run in parallel if the supervisor decides the model choice earlier.
- The **paper** is updated only after results exist; methodology and evaluation sections will need reconciliation with the approved protocol.

---

## 20. Do not do yet

- Do not run RQ2.
- Do not recruit participants.
- Do not collect questionnaire responses.
- Do not call the questionnaire validated.
- Do not claim technical validation is complete.
- Do not claim LLM performance improvement (or athletic-performance or injury-prevention benefit).
- Do not change baseline rules without a protocol decision.
- Do not select final LLMs without an advisor decision.
- Do not add arbitrary rubric weights.
- Do not rewrite paper results that do not exist.
- Do not mix development database rows with study data.

---

## 21. Executive summary (one page)

**1. What is the research?** An S2 study of a hybrid running-training recommender: deterministic running-domain calculations (VDOT-based paces and rule-based multi-week progression) create a multi-week baseline plan; Gemini personalizes the wording across sufficient multi-week context (CONFIRMED, supersedes the earlier Week-1-only scope); server-side validation rejects outputs that change the computed numbers or structure; a deterministic fallback applies on failure. The research questions ask how such a system can be built (RQ1), how Gemini-personalized output differs from the deterministic baseline under identical/controlled conditions (RQ2 — updated to a single-LLM-vs-baseline design, superseding the earlier 2-LLM "LLM A vs LLM B" framing), and how users perceive the plans in terms of personalization, usefulness, clarity and confidence (RQ3). It does not claim improved athletic performance, injury prevention, or clinical validity.

**2. What has been built?** A working prototype (FastAPI/SQLite backend, React frontend) with the rule engine, Gemini/OpenAI integration with validation and fallback, 4–24-week plans with scheduling, workout logging linked to planned workouts, deterministic progress insights, authentication/security, and an anonymous research mode with baseline-vs-AI comparison and four single ratings. A draft IEEE-style manuscript (33 references, DOI-checked; Google Scholar confirmed for 9 of the retained original references) and a methodology proposal exist.

**3. What has been validated?** The prototype has 194 passing automated tests at commit `224d910`. Against the 14 proposed technical-validation criteria, 2 are fully covered, 9 partially, 2 not ready and 1 awaits a decision, so technical validation is **not complete**. No LLM comparison, user data or quality/performance result exists; the database contains development test rows only.

**4. What remains?** RQ1 test gaps; an RQ2 experiment harness (raw outputs, validator verdicts, errors, run/prompt/model-version records are not stored today); a frozen baseline; a finalized automated-criteria rubric (expert protocol no longer needed — excluded 2 October 2026); the 16-item questionnaire (study-specific, unvalidated, with wording issues) and its validation; an evaluation application with consent, participant codes, neutral defaults and blinding; ethics/BINUS clarification; the user-study design and data collection; analysis; and the paper's results sections.

**5. What decisions are needed?** From the supervisor: exact Gemini model/version and version control (count resolved: 1 — Gemini only), Gemini configuration/reproducibility details, profile demographic composition (count resolved: 24), exact 8-criteria operational definitions (count resolved, definitions conflict across documents — flagged, not resolved), the RQ3 design, sample-size approach, template-text control, questionnaire validation process, and the statistical test accounting for 72 Gemini outputs nested within 24 profiles. Multi-week scope and repetition counts are now CONFIRMED and need no further decision. **Fix-or-document for the two rule-engine behaviors (a ~25% rebound after cutback weeks and a taper tied to starting mileage) is RESOLVED**: the rebound is fixed in code; the taper's tie to starting mileage is confirmed correct and unchanged. From BINUS: the ethics/research-review requirements, adult-only rule, consent and data-protection rules, and whether participant profiles (including injury notes) may be sent to external LLM APIs.

**6. What should happen next?** Review this package with the supervisor and record the decisions; freeze the protocol and the baseline; confirm ethics requirements; then close the RQ1 test gaps and build the RQ2 harness. RQ2, participant recruitment and data collection should not start until the protocol and infrastructure are approved.

**Status: READY FOR ADVISOR REVIEW — not ready for experiment or data collection.**

---

## Advisor Decision Update — 2 October 2026 — `SUPERSEDED` (2-LLM design; kept for audit trail only)

~~- **2 LLM design approved:** RQ2 compares exactly 2 LLMs ("LLM A", "LLM B") — Sections 4, 8, 17.~~
~~- **3 repetitions approved:** 3 repetitions per (runner profile × LLM) combination; replicates, not independent runners — Sections 8, 17.~~
- **Expert evaluation excluded from the study design:** no coach/expert rating, expert rubric, inter-rater agreement, expert recruitment, or blinded expert assessment — Sections 8, 10, 11, 15, 17. *(Not superseded — still current.)*
- ~~Not resolved by this update (preserved): specific LLM identities and versions; the 24-profile count…~~ — see the next section for current status.

## Advisor Decision Update — 2 October 2026 (Gemini-only design)

**This is the current, authoritative design, superseding the 2-LLM design recorded in the update above (issued earlier the same day).**

- **1 LLM (Gemini) CONFIRMED** — Sections 4, 8, 17; supersedes the same-day 2-LLM resolution.
- **24 runner profiles CONFIRMED** — Section 17; previously PROPOSED/unconfirmed.
- **3 Gemini repetitions per profile CONFIRMED → 72 Gemini generations; 24 baseline plans, generated once, NOT repeated** — Sections 8, 17.
- **Exactly 8 automated criteria LOCKED** — Section 11; exact operational definitions remain an OPEN SUB-DECISION, explicitly flagged (conflict across the lock's own 8, the superseded comparative proposal's 16, and the paper's Table IV 5 — not resolved here).
- **Multi-week scope CONFIRMED** — resolves the former Sections 8/17 OPEN METHODOLOGICAL DECISION. Pipeline: Runner Profile → Validation → Physiological Calculation → Deterministic Rule-Based Multi-Week Baseline → Gemini Personalization → Server-Side Validation → Gemini-Personalized Multi-Week Plan → Automated Evaluation → Baseline vs Gemini Comparison.
- **Expert evaluation still excluded** (unchanged) — Sections 8, 10, 11, 15, 17.
- **No ranking/winner framing**: results per criterion, baseline vs Gemini; no composite/overall score; Gemini never declared "better" without statistical support.
- **Not resolved by this update** (still open/unresolved): exact Gemini model/version; exact 8-criteria operational definitions (Section 11); the exact statistical test (must account for 72 Gemini outputs nested within 24 profiles); prompt-delivery/Gemini-configuration details; RQ3 design, sample size, ethics/BINUS requirements; questionnaire validation; profile demographic composition detail. **Resolved since this update: baseline rule-engine rebound/taper issues** — rebound fixed, taper confirmed correct as-is.

---

## STATUS SUMMARY

**CONFIRMED:** 24 runner profiles; Gemini as the only LLM; 3 Gemini repetitions per profile; 24 baseline plans; 72 Gemini generations; no expert evaluation; exactly 8 automated criteria (count locked); multi-week personalization; baseline vs Gemini comparison.

**OPEN:** exact Gemini model/version; exact 8-criteria definitions/thresholds (explicit conflict between the methodology lock's 8, the superseded comparative proposal's 16, and the paper's Table IV 5 — not resolved here); statistical test; RQ3 sample size; ethics/BINUS requirements; questionnaire validation/pilot; prompt implementation/reproducibility details; profile demographic composition.
