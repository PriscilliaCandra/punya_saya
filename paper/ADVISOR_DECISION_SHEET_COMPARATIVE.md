# ADVISOR DECISION SHEET — Comparative LLM Evaluation

**STATUS AS OF 2 OCTOBER 2026 (LATER SAME DAY): the "2 LLM comparative" design described in most of this document is `SUPERSEDED`.** The advisor has issued a NEW FINAL LOCKED design: **1 LLM only (Gemini) vs the deterministic baseline**, 24 profiles CONFIRMED, 3 Gemini repetitions (72 generations) + 24 baseline plans (not repeated), exactly 8 automated criteria, multi-week scope CONFIRMED. See **"Advisor Decision Update — 2 October 2026 (Gemini-only design)"** near the end of this document for the authoritative current design, and the **STATUS SUMMARY** at the very end. Everything below this notice that describes "LLM A vs LLM B" / 2-LLM comparison is kept visible for audit-trail purposes only and no longer describes the approved design.

**Status: PROPOSED — SUBJECT TO ADVISOR APPROVAL**, except where marked APPROVED/CONFIRMED below (see "Advisor Decision Update — 2 October 2026", itself now `SUPERSEDED` by the Gemini-only update that follows it). Numbers marked ◆ are starting proposals, not decisions, unless confirmed. Full detail: `RESEARCH_METHODOLOGY_COMPARATIVE_PROPOSAL.md`. No experiment has been run and no data collected.

**1. Title.** "Design and Evaluation of an AI-Based Personalized Running Training Recommendation System" / "Perancangan dan Evaluasi Sistem Rekomendasi Latihan Lari Personal Berbasis AI".

**2. Problem.** Generic running plans ignore an individual runner's fitness, schedule and limitations. LLMs can write individualized plans, but studies report variability across inputs and models and safety concerns, and an LLM may silently alter a distance, pace or volume. The proposed hybrid system fixes the physiological and training numbers with deterministic rules and uses an LLM only to personalize the plan text; a server-side validator checks the output. The study makes no claim about athletic performance, injury prevention or clinical validity.

**3. Research questions**
- **RQ1:** How can a hybrid AI-based system generate personalized multi-week running training plans by combining deterministic training constraints with LLM-based personalization?
- **RQ2 — `SUPERSEDED` (2-LLM wording, kept for audit trail only):** "How do different large language models, given the same runner profile and the same deterministic baseline plan, differ in personalizing the plan while remaining consistent with the runner profile and predefined training constraints?" RQ2 compared LLM A vs LLM B only, using automated/objective evaluation criteria; it never concludes with an overall ranking, "best LLM," or "winner."
- **RQ2 — CURRENT (Gemini-only design, locked):** "How does Gemini-based personalization differ from a deterministic baseline in generating personalized multi-week running training plans while maintaining predefined training constraints?" (Indonesian: "Bagaimana personalisasi berbasis Gemini berbeda dari deterministic baseline dalam menghasilkan rencana latihan lari multi-minggu yang dipersonalisasi dengan tetap mempertahankan constraint latihan yang telah ditentukan?"). RQ2 now compares Gemini-personalized output vs the deterministic baseline, using the 8 locked automated/objective criteria, reported individually; it never concludes with an overall ranking, "best," or "winner," and does not claim Gemini is superior unless supported by the (not-yet-chosen) statistical analysis.
- **RQ3:** How do users perceive the generated training plans in terms of personalization, usefulness, clarity, and confidence?

**4. Design**

`SUPERSEDED` (2-LLM diagram, audit trail only):
```
Runner Profile → Deterministic Baseline → LLM A / LLM B → Validation → Evaluation
                      (identical for both models: profile, baseline, prompt, schema, validator)
```
*(SUPERSEDED: earlier versions of this diagram showed LLM A / LLM B / LLM C, then LLM A / LLM B. APPROVED/CONFIRMED CURRENT DESIGN: 1 LLM — Gemini — vs the deterministic baseline — see "Advisor Decision Update — 2 October 2026 (Gemini-only design)" below.)*

**CURRENT (Gemini-only) pipeline, locked:**
```
Runner Profile → Validation → Physiological Calculation → Deterministic Rule-Based Multi-Week Baseline
   → Gemini Personalization → Server-Side Validation → Gemini-Personalized Multi-Week Plan
   → Automated Evaluation → Baseline vs Gemini Comparison
```

**5. What is compared.** `SUPERSEDED` wording: only the LLM (the independent variable) across LLM A vs LLM B, given identical inputs. **CURRENT:** the deterministic rule-based multi-week baseline vs Gemini-personalized multi-week output, given the same profile and baseline as controlled context for Gemini. The baseline is a **controlled reference/input condition, not "ground truth" for overall plan quality**. No overall "best"/"winner" is sought; results apply to the tested Gemini version, prompt and date.

**6. Automated evaluation criteria — LOCKED AT EXACTLY 8** (not 16, not any other count)
- Candidate criteria (8 total): profile consistency, goal consistency, physiological/pace consistency, weekly volume/mileage consistency, workout structure, intensity constraints, progression/recovery constraints, completeness/constraint violations.
- **OPEN SUB-DECISION:** the exact operational definitions of these 8 criteria are not yet reconciled across documents — `RESEARCH_METHODOLOGY_LOCK.md`'s 8-criterion list, the (now superseded) comparative proposal's 16-item list, and `PAPER_DRAFT.md` Table IV's 5-criterion list define overlapping but non-identical criteria. This conflict is flagged, not resolved, by this update.
- *Stability:* agreement across the 3 Gemini repetitions per profile.
- **Compliance is not training-plan quality and not physiological optimality.**
- **Expert evaluation remains excluded from the study** (unchanged from the 2 October 2026 decision; see below). RQ2 relies solely on the 8 locked automated/objective criteria.

**7. Experimental design — CURRENT (Gemini-only), supersedes the 2-LLM table below**
| Element | Value | Status |
|---|---|---|
| LLM | **Gemini only** — exact model/version to be finalized and recorded before experimental data collection | CONFIRMED (1 LLM) |
| Runner profiles | **24 synthetic runner profiles — CONFIRMED** | CONFIRMED; demographic composition detail is an OPEN SUB-DECISION if not already finalized elsewhere |
| Baseline plans | **24** — one deterministic baseline per profile, generated once (NOT repeated 3×, since it is deterministic) | CONFIRMED |
| Gemini repetitions | **3 per profile** → 24 × 3 = **72 Gemini generations** | CONFIRMED |
| Total outputs | **24 baseline + 72 Gemini** (never call this "96 independent experimental generations" — baseline and Gemini reps are different unit types; never "144" or "216" — those were 2-LLM/3-LLM-design totals) | CONFIRMED |
| Unit of analysis | Runner profile = primary sampling/block unit; "profile × condition (baseline/Gemini) cell" replaces the old "profile × LLM cell" wording | CONFIRMED |
| Automated criteria | Exactly 8, locked (Section 6) | CONFIRMED count; definitions OPEN |
| Expert evaluation | Excluded (unchanged) | CONFIRMED |
| Statistics | Not finalized — selected later based on measurement scale, pairing, repeated-generation design and distributional characteristics; candidates (Wilcoxon, Friedman, mixed models) are PROPOSED only; the 72 Gemini outputs must NOT be treated as 72 independent participants — they are nested within 24 profiles | OPEN |

`SUPERSEDED` 2-LLM table (audit trail only, no longer the approved design):
| Element | Proposal ◆ | Rationale / limit |
|---|---|---|
| LLMs | ~~APPROVED/CONFIRMED: 2 LLMs ("LLM A" and "LLM B")~~ | Superseded 2 October 2026 (Gemini-only) |
| Runner profiles | ~~24 synthetic runner profiles — PROPOSED~~ | Superseded by CONFIRMED 24 above |
| Repetitions | ~~3 repetitions per (runner profile × LLM)~~ | Superseded by 3 Gemini repetitions above |
| Generations | ~~24 × 2 × 3 = 144 generations for Week-1-only; ~720 if five phase-weeks~~ | Superseded — see 24 baseline + 72 Gemini above |
| Unit of analysis | ~~Profile × LLM cell~~ | Superseded by profile × condition (baseline/Gemini) cell |

**8. Multi-week scope — RESOLVED/CONFIRMED (supersedes the "Multi-week scope issue" below).** The Gemini-only design confirms multi-week scope: Gemini receives sufficient multi-week context (not Week-1-only) via the pipeline in Section 4. This resolves the open methodological decision previously recorded here.

`SUPERSEDED` text (audit trail only): RQ1 says multi-week, but the LLM personalizes only Week 1 (Weeks 2+ are deterministic and identical across models), so progression, cutback and taper criteria would not distinguish models. Options: Week 1 only (restrict RQ wording); full plan in one call (long outputs, truncation, extended validator); Week 1 plus read-only whole-plan context; phase-stratified weeks (Week 1, cutback, last build, taper, race week); per-week generation. ~~OPEN METHODOLOGICAL DECISION: The relationship between the multi-week research scope and the specific weeks/context presented to the LLM must be finalized before the comparative experiment.~~ — RESOLVED by the Gemini-only pipeline above.

**9. RQ3 user evaluation.** Perceived Personalization, Usefulness, Clarity and Recommendation Confidence (PP, PU, PC, RC), four items each, 5-point agreement scale. The questionnaire is **study-specific and currently unvalidated**; wording issues are documented (e.g., PC4 double-barrelled). Design, sample size and recruitment are not chosen; participants should be adults; ethics/BINUS requirements are not yet confirmed; profile data (including injury notes) would be sent to external LLM providers.

**10. Decisions requiring supervisor approval** `[ADVISOR DECISION REQUIRED]` unless noted (updated for the Gemini-only design)
1. Final RQ2 wording — **RESOLVED/LOCKED (Gemini-only wording, Section 3)**.
2. ~~Number of LLMs and which ones~~ — **RESOLVED: 1 LLM (Gemini)**; exact model/version string still to be finalized and recorded before data collection.
3. ~~Number of profiles~~ — **RESOLVED: 24 profiles CONFIRMED**; demographic composition detail is an OPEN sub-decision if not finalized elsewhere.
4. ~~Repetitions~~ — **RESOLVED: 3 Gemini repetitions per profile (72 generations); 24 baseline plans (not repeated)**; temperature policy still open.
5. Prompt delivery / Gemini configuration details — still open.
6. Baseline role — **RESOLVED: controlled reference/deterministic comparison condition** (baseline vs Gemini is now the explicit comparison; baseline is never "ground truth" for overall plan quality).
7. ~~LLM scope: Week 1 only vs multi-week~~ — **RESOLVED/CONFIRMED: multi-week scope confirmed**, per the pipeline in Section 4.
8. ~~Baseline rule-engine issues (≈25% rebound after cutback; taper tied to starting mileage): fix or document before freeze~~ — **RESOLVED**: rebound fixed in code (`generate_weekly_progression_summary`); taper confirmed correct as intentionally tied to starting mileage, matching `PAPER_DRAFT.md` Table II, and left unchanged. See `paper/CODE_AUDIT_EASY_RUN_PACE_AND_T7.md`. The baseline freeze itself (generating/storing the 24 profiles' plans) remains a separate, not-yet-done step.
9. Automated criteria — **RESOLVED: exactly 8, locked**; exact operational definitions remain an OPEN SUB-DECISION (conflicting definitions across documents — see Section 6).
10. ~~Expert evaluation: yes/no, count, qualifications, blinding, agreement statistic.~~ — **RESOLVED: expert evaluation excluded from the study** (unchanged).
11. Statistical method `[ADVISOR/METHOD REVIEW REQUIRED]` — still open; must account for 72 Gemini outputs nested within 24 profiles (not 72 independent participants).
12. Questionnaire revision and validation process — still open.
13. RQ3 design, relation to RQ2, participant sample-size approach `[ADVISOR/METHOD REVIEW REQUIRED]` — still open, unchanged by this update.
14. Ethics/BINUS requirements and disclosure of external LLM data processing `[CHECK BINUS REQUIREMENTS]` — still open.
15. Literature-gap wording (needs search protocol) `[LITERATURE VERIFICATION REQUIRED]` — still open.

*Current implementation is not yet able to run the experiment (no run IDs, prompt version, captured model version, raw-output/verdict/error storage, or harness); implementation starts only after approval.*

## Advisor Decision Update — 2 October 2026 — `SUPERSEDED` (2-LLM design; kept visible for audit trail only)

~~- **2 LLM design APPROVED/CONFIRMED** ("LLM A" and "LLM B"); no third LLM.~~
~~- **3 repetitions per (runner profile × LLM) combination APPROVED/CONFIRMED**; repetitions are replicates, not additional independent runners; the runner profile remains the sampling/block unit.~~
- **Expert evaluation EXCLUDED from the study design** (no coach/expert rating, expert rubric, inter-rater agreement, expert recruitment, or blinded expert assessment). RQ2 now relies solely on automated/objective evaluation criteria. *(This item is NOT superseded — it remains the current decision; only the 2-LLM items above are superseded.)*
- ~~Still open / unresolved: 24-profile count (PROPOSED, not confirmed), exact automated evaluation criteria count, exact statistical test, Week-1-only vs multi-week LLM context, baseline rule-engine issues, ethics/BINUS requirements.~~ — see the next section for the current status of each.

## Advisor Decision Update — 2 October 2026 (Gemini-only design)

**This is the current, authoritative experimental design, superseding the 2-LLM comparative design above.**

- **1 LLM (Gemini) CONFIRMED** as the sole personalization model; exact model/version to be finalized and recorded before experimental data collection. No second or third LLM.
- **24 runner profiles CONFIRMED** (previously PROPOSED/unconfirmed under the 2-LLM design).
- **3 Gemini repetitions per profile CONFIRMED → 72 Gemini generations.**
- **Deterministic baseline = 24 plans CONFIRMED** (one per profile, generated once — not repeated 3×, since the baseline is deterministic).
- **Comparison = deterministic multi-week baseline vs Gemini-personalized multi-week plan** (same profile/baseline as controlled context for Gemini); never "LLM A vs LLM B."
- **Exactly 8 automated criteria LOCKED** (profile consistency, goal consistency, physiological/pace consistency, weekly volume/mileage consistency, workout structure, intensity constraints, progression/recovery constraints, completeness/constraint violations). Exact operational definitions are an OPEN SUB-DECISION — see the conflict flagged in Section 6.
- **Multi-week scope CONFIRMED**: Gemini receives sufficient multi-week context (resolving the former Week-1-only open issue). Pipeline: Runner Profile → Validation → Physiological Calculation → Deterministic Rule-Based Multi-Week Baseline → Gemini Personalization → Server-Side Validation → Gemini-Personalized Multi-Week Plan → Automated Evaluation → Baseline vs Gemini Comparison.
- **Expert evaluation still excluded** (unchanged from the 2 October 2026 decision).
- **No ranking/winner framing**: results report differences across the 8 criteria individually; Gemini is never claimed "better" without statistical support, and no composite/overall score is used.
- **Not resolved by this update** (still open): exact Gemini model/version string; exact 8-criteria operational definitions/thresholds (flagged conflict with the lock's 8, the now-superseded comparative proposal's 16, and the paper's Table IV 5); the statistical test (to be chosen later, accounting for repeated Gemini generations nested within profiles); RQ3 sample size/design; ethics/BINUS requirements; questionnaire validation/pilot; prompt implementation/reproducibility details; profile demographic composition detail; baseline rule-engine rebound/taper issues.

---

## STATUS SUMMARY

**CONFIRMED:** 24 runner profiles; Gemini as the only LLM; 3 Gemini repetitions per profile; 24 baseline plans; 72 Gemini generations; no expert evaluation; exactly 8 automated criteria; multi-week personalization; baseline vs Gemini comparison (never "LLM A vs LLM B", never 2-LLM/3-LLM framing).

**OPEN:** exact Gemini model/version; exact 8-criteria definitions/thresholds (conflict with the lock's 8 and the paper's Table IV 5 criteria — not resolved here); statistical test; RQ3 sample size; ethics/BINUS requirements; questionnaire validation/pilot; prompt implementation/reproducibility details; profile demographic composition detail; baseline rule-engine rebound/taper fix-or-document decision.
