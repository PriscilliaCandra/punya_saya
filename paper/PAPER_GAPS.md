# PAPER_GAPS — what is still required before the paper is complete

Format per item: **Missing → Why → How to obtain → Where it goes.**

**STATUS AS OF 2 OCTOBER 2026 (LATER SAME DAY): the "2 LLM" design referenced in the update below is `SUPERSEDED`.** New FINAL LOCKED design: 1 LLM only (Gemini) vs the deterministic baseline; 24 profiles CONFIRMED; 3 Gemini repetitions (72 generations) + 24 baseline plans (not repeated); exactly 8 automated criteria (definitions OPEN, flagged conflict — see item 3 under "Experiments"); multi-week scope CONFIRMED. See "Advisor Decision Update — 2 October 2026 (Gemini-only design)" at the end of this document and the STATUS SUMMARY that follows it. None of this touches `PAPER_DRAFT.md` itself, which remains out of scope for this update (per the task constraints, `PAPER_DRAFT.md` and `PAPER_IEEE.docx` are not edited here — they are only flagged as containing obsolete terminology where relevant).

**Advisor Decision Update — 2 October 2026 — `SUPERSEDED` (2-LLM design; kept for audit trail only):** ~~2 LLM design approved (item 1 under "Experiments" below reflected 2 LLMs, "LLM A"/"LLM B"); 3 repetitions per (runner profile × LLM) approved~~ — superseded by the Gemini-only design (1 LLM; 3 Gemini repetitions per profile = 72 generations; 24 baseline plans, not repeated). Expert evaluation (rubric, coach rater, rater agreement) remains excluded entirely from the study — see item 3 under "Experiments" (unchanged, not superseded).

## 1. Experiments

1. **Baseline-vs-Gemini comparison harness (RQ2)** — **UPDATED (Gemini-only, CONFIRMED)**
   - Missing: no code runs Gemini on the confirmed multi-week baseline and stores both sides of the comparison; `get_personalized_ai_plan` returns only the final (possibly fallback) plan and discards raw output and failure reasons; no live Gemini output is stored anywhere.
   - Why: RQ2 cannot be answered; without raw outputs, validator pass rate and failure types cannot be measured.
   - How: write a script (outside the web path) that, for 24 CONFIRMED profiles, generates 1 deterministic baseline each (24 total, not repeated) and calls the Gemini provider function 3 times per profile (72 total), stores raw JSON, validator verdict and reason, latency, tokens/cost, and model id with date. Multi-week scope is CONFIRMED, so the baseline and prompt must cover sufficient multi-week context, not Week 1 only. Fix the profile set and the 8-criterion automated rubric (definitions still to be reconciled, see item 3) before running.
   - Where: III-I, Table IV, V-C.
2. **Choose and justify the Gemini model/version**: confirm the exact Gemini model/version to use and that it still exists on the experiment date [VERIFY]; record the exact version string. ~~Count resolved: 2 LLMs ("LLM A", "LLM B")~~ — **superseded: count resolved at 1 LLM (Gemini only)**; the OpenAI provider path is not used for this study.
3. **Rubric for Gemini-vs-baseline comparison**: the criteria **count is now LOCKED at exactly 8** (2 October 2026, Gemini-only design), with no composite/weights [no composite is approved]. **OPEN SUB-DECISION, explicitly flagged and NOT resolved here:** the exact operational definitions of the 8 criteria conflict across documents — `RESEARCH_METHODOLOGY_LOCK.md`'s own 8-criterion list, `RESEARCH_METHODOLOGY_COMPARATIVE_PROPOSAL.md`'s (superseded) 16-item draft list, and `PAPER_DRAFT.md` Table IV's 5-criterion list define overlapping but non-identical criteria; these must be reconciled by the advisor before the rubric is finalized. `SUPERSEDED` (2 October 2026): expert rubric, recruiting a running coach as rater, and rater agreement remain not applicable — expert evaluation is excluded from the study entirely; RQ2 relies solely on the 8 locked automated/objective evaluation criteria.
4. **Deterministic-engine checks not yet done**: cross-check the zone fractions and VDOT output against published tables in [27]; add property tests over all durations 4–24 and all day counts (currently durations 4/8/12/16/24 and 4/8/24 only). **UPDATE 2026-10-14: property tests added (`backend/tests/test_rule_engine_properties.py`); structure, phase schedule and formulas hold on 6,615 combinations; two design claims do not hold in general (section 5). The cross-check of VDOT zones against published tables [27] remains open.** **RESOLVED (see §5): the post-cutback +25% rebound has been fixed in code; the taper anchored to starting volume was reviewed and confirmed acceptable (intentional, matches Table II) and left unchanged.**

## 2. Data

1. **User-study data (RQ3)**: participants, recruitment, inclusion criteria, sample size rationale, responses, comments. None exists; stored DB rows are development artifacts. Obtain by running the study after the fixes in §3. Goes in V-D, Table VI [DATA REQUIRED].
2. **Questionnaire reliability**: Cronbach's alpha requires the 16-item instrument and enough respondents (rule-of-thumb sample size [VERIFY]). Goes in III-K, V-D.
3. **Ethics and consent**: ethical clearance/waiver from the institution and an informed-consent screen; the app has no consent flow. Goes in III-J.
4. **Real-user data policy**: runner profiles include health-adjacent free text (injury); state storage, anonymization and retention [TO BE COMPLETED].

## 3. Implementation changes required for valid evaluation

- Replace the four single sliders with the 16 items (PP1–PP4, PU1–PU4, PC1–PC4, RC1–RC4); write item wording and document its source or pilot it [NOT IMPLEMENTED]. Items must be traceable to literature (e.g., [2], [3]) or piloted.
- Neutral (unset) defaults for ratings: **DONE 2026-10-14 (owner-approved scope).** `EvaluationPage.jsx` and the new blinded page start with no answer selected (null, shown as "Not rated yet"); submit is disabled until all four answers exist; nothing is sent for an unanswered item. The previous defaults (5/5/5/4 and 3/4/5/4) are gone. The four criteria and the 1-5 scale are unchanged; no item, scale or criterion was added (`src/constants/likertCriteria.js` holds the existing four).
- Blinding/order randomization: **PARTIALLY DONE 2026-10-14 (labels and field names only).** New page `/research/blind/:planId` shows the two plans as "Plan A" and "Plan B"; the server maps the label to the internal condition (`backend/app/research/blinding.py`, hash-based per plan, stored as `evaluated_plan_type`) and never sends the mapping; model name, plan-type keys and generation meta-text are not shown, and the tab title is neutral. Checked by 25 backend tests and one browser run on a temporary database (rendered text contains no condition words; no answer pre-selected; submit blocked until complete; stored row mapped as expected). **Not solved:** (1) content still differs (the personalized plan carries extra text such as an overview and per-workout cues, so a participant may guess the source; in the browser run the two plans visibly differ in structure); (2) the label assignment is a reproducible hash, not a secret; (3) how participants obtain a plan id without seeing the unblinded result page, how many plans each rates and in what order are study-procedure decisions NOT made here; (4) the original unblinded pages (`/research`) are unchanged and still show the labels; (5) no claim that blinding succeeds is made before a human-perception check.
- Participant identifier (anonymous code) so ratings of the same person can be paired and alpha computed: **DONE for the blinded endpoint 2026-10-14 (not applied to the real database).** `plan_evaluations.participant_code` (nullable) holds a random token `P-XXXXXXXX` generated in the browser (sessionStorage) and validated server-side so that names, e-mail addresses or phone numbers cannot be entered as a code. Alembic revision `0004_participant_code` was tested up and down on a COPY of `running_research.db` and has NOT been applied to the real file; **until `alembic upgrade head` is run (after backing the file up), the backend code cannot read the real `plan_evaluations` table.** **Not anonymous in the strict sense:** free-text comments and the runner profile's injury text may contain identifying details; the database, server logs and timestamps remain; consumer-owned plans are excluded from the blinded endpoints, but a plan linked to an account would link to an e-mail through `training_plans.user_id`. Withdrawal, retention and consent procedures are ethics decisions and are not implemented.
- Ensure the "AI" arm used live LLM output: if no key is set the arm is template text (all 19 stored plans). Record `ai_model_used` for every evaluated plan and exclude or separate fallback plans.
- ~~Decide whether evaluation should compare Week 1 only (the only week with LLM text) or the whole plan.~~ — **RESOLVED (2 October 2026): multi-week scope CONFIRMED.** Evaluation and the application must cover the whole plan, not Week 1 only.
- Optional: validate free-text safety content, add retry on validation failure, personalize later weeks — only if the paper's contribution claims require them.

## 4. Literature (after the reference audit and manuscript update)

Done in this update: gap statement rewritten around Düking et al. 2024; Düking, Havers, He T., Feely and Issurin added; Norman 2010 replaced Sullivan & Artino; former [2], [13], [15] removed (relevance/redundancy, not because of Google Scholar); weak [28] (Gabbett) citations removed from the cutback row and from V-E; [15] (Akrimi) reworded as one exploratory study; the "closed-loop validator" wording for He Z. removed. The reference list now has 33 entries.

Still open:
1. Documented search protocol (databases, keywords, dates) to support any novelty or gap statement; the manuscript currently makes none.
2. Google Scholar: 10 references directly confirmed; the rest are "not verified due to access limitation" (CAPTCHA), not "not found". Check manually, including the 6 added references.
3. Read in full: He Z. et al. [24] (does it validate outputs after generation?), Düking [11] and Havers [12] (confirm that no post-generation validation is described; confirm the number of experts, ChatGPT version).
4. Confirm volume/issue/pages for Havers 2025 [12] (OpenAlex: vol. 42(2), pp. 289–329) and He T. 2026 [14] (OpenAlex: vol. 43, pp. 949–961; no issue).
5. Decide on the 1979 Daniels–Gilbert source (pre-2001) [APPROVAL REQUIRED]; confirm Daniels book edition/year [27] and the zone fractions against it.
6. See `REFERENCES_VERIFICATION.md` for every item still marked VERIFY MANUALLY.
7. Find sources, or keep as explicitly engineering design constraints, for the rules in the table in Section 5b.

## 4b. Paper-text items still open

- Author block: co-authors/supervisor, affiliations, e-mail.
- Figures (architecture, LLM personalization pipeline, multi-week workflow, interaction flow) (Fig. 1–4 in the manuscript) must be drawn from the real implementation; the Word file contains labelled placeholders only. Tables I–VI are populated; Table VII waits for data.
- Convert to the BINUS/IEEE two-column template (the existing `Paper.docx` shows the template format).
- Re-count abstract after results are inserted (currently ≈218 words with placeholders).

## 5. Findings about the rule engine to decide on (research validity)

| Finding (historical — describes the pre-fix implementation) | Evidence | Resolution |
|---|---|---|
| Week after a cutback is +24.9% vs. the cutback week (+6% vs. last build week); code comment claims ≤10% | run of 8/12/16-wk plans, pre-fix | **RESOLVED — fixed.** `generate_weekly_progression_summary` now carries the cutback week's own reduced volume into the next build step (`current = vol` in the cutback branch), so the week after a cutback is now the normal ~6%/8% step relative to the cutback week, consistent with the ≤10% claim. Verified by `backend/tests/test_t7_progression_fix.py`. |
| Taper is anchored to starting mileage (0.85×, 0.55×), giving a 37–55% drop from the preceding week in 8/12/16-wk plans; code comment said "~75% of peak" | same, pre-fix | **RESOLVED — documented as-is, not changed.** The base-mileage anchoring is intentional and matches `PAPER_DRAFT.md` Table II ("times the base (starting) mileage"); it was reviewed and deliberately not switched to peak-anchoring. Only the misleading inline comment ("~75% of peak") was corrected. |
| Test named "never exceeds the safe increment" checks only consecutive build weeks | `test_rule_engine.py` | **Partially resolved.** `backend/tests/test_t7_progression_fix.py` (new) explicitly covers the post-cutback build step and the taper/race-week anchoring; the original test was left unchanged and still checks only consecutive build-to-build transitions, which is no longer a coverage gap given the new file. |
| Weeks 2+ repeat Week 1's structure and have no LLM text | `generator.py`, Phase 5 design | State clearly (done) or extend LLM to weeks 2+ |
| Realized weekly distance departs from the progression target, and the long-run share can exceed 30% | generator; `backend/tests/test_rule_engine_properties.py` | **MEASURED 2026-10-14 (6,615 combinations).** 2 training days: realized volume 50-70% below target in every week, long-run share up to ~60%. Low base mileage with many days: realized volume up to several times the target (per-session floors). 24 synthetic dry-run profiles: 20/288 weeks over 30% (max 36%), 4/288 weeks outside ±10% (max 50%); final study profiles not yet determined. **Owner decision (Option A, 2026-10-14): engine unchanged; claims in the explainability text, UI and paper softened.** |
| Age, sex, 10K PB, easy pace not used in computation | generator | Use them or state it (done) |

## 5b. Rule-constant traceability

Classification: **L** = directly supported by literature, **L-partial** = direction supported, numerical value not, **E** = engineering design constraint of the proposed system, **H** = implementation heuristic. Manuscript wording: E and H items are described as "an engineering design constraint used in the proposed system" (never as scientific thresholds).

| Rule | Code location | Current value | Classification | Literature support | Action |
|---|---|---|---|---|---|
| VDOT equations (1)–(3) | `rules/vdot.py: calculate_vdot_from_race` | −4.60 + 0.182258 v + 0.000104 v²; 0.8 + 0.1894393 e^(−0.012778 t) + 0.2989558 e^(−0.1932605 t) | L (Daniels–Gilbert) | Original 1979 source (pre-2001, not cited) ; [27] book covers VDOT | Decide on 1979 citation; verify constants against [27] |
| Zone fractions of VDOT | `rules/vdot.py: calculate_training_paces` | easy 0.65–0.74, marathon 0.80, threshold 0.88, interval 0.98, repetition 1.05 | L-partial (Daniels-style zones) | [27] (not yet checked) | Compare with book; if different, label as implementation choice |
| Velocity floor / fallbacks | `rules/vdot.py: velocity_from_vo2` | 60 m/min floor, 150 m/min fallback | H | None | Document |
| Feasibility thresholds | `rules/generator.py: generate_rule_based_plan` | 0%, 3.5%, 6.5% pace improvement | E | None | Justify or label as design constraint (done in text) |
| Week-1/progression factor | `rules/generator.py: generate_weekly_progression_summary` | ×1.06 if base ≥ 20 km else ×1.08 | E | 10% rule is contested [17], [18] | Keep as E; note the base-20 km switch is unsupported |
| Cutback | same | every 4th week, ×0.85 of the current progression reference (the last build week's volume, or the previous cutback week's reduced volume if a build week has not intervened since) | E | Periodization concept only [29] | Keep as E; no source for 15% / every fourth week. The resulting reduced volume now carries forward as the reference for the next build week (RESOLVED, previously it did not) |
| Taper | same | penultimate ×0.85, final ×0.55 of base (not peak) | L-partial | [22], [23] support reducing volume while keeping intensity | **RESOLVED: confirmed base-anchored, not peak-anchored; not changed.** Magnitudes remain labelled E |
| Long-run share and caps | `rules/generator.py: distribute_workouts_across_week` | 30%; caps 12/16/21 km; floor 4 km | E | None found | Keep as E or find a source; the realized share can exceed 30% (section 5) |
| Quality share | same | 20%, floor 3.5 km; tempo (beginner) / interval | H (loosely motivated by [19], [20]) | [19], [20] describe session shares, not distance | Keep wording "approximate" |
| Easy-run floor | same | 3.0 km | H | None | Document |
| Day placement | same | long run Sunday/Saturday; quality Tue/Wed/Thu | H | None | Document |
| LLM tolerances | `ai/validator.py` | ±0.05 km distance, ±0.15 km weekly mileage | H (rounding tolerance) | None | Document |

## 5c. Questionnaire

The 16 items do not exist in the repository (only four single ratings are implemented). Provenance, adaptation status and validation needs are documented in `QUESTIONNAIRE_TRACEABILITY.md`; every item remains study-specific until validated.

## 6. Claims that must NOT be made yet

- That the system improves performance, prevents injury, or is clinically/medically validated.
- Any statement about which LLM is better, any model ranking, any LLM-vs-baseline user-preference result.
- That the "AI-personalized" plans in the database came from an LLM (all used the fallback).
- That the questionnaire is validated, reliable, or derived from [2]/[3].
- ~~That the whole multi-week plan is LLM-personalized (Week 1 only).~~ — **NOTE: this claim restriction is now partially superseded.** Under the Gemini-only CONFIRMED design, multi-week personalization is the intended scope going forward; the implementation now extends Gemini personalization to every baseline week (`weeks[]`, per-week validation), so the paper may describe multi-week personalization as *implemented*; it must still not claim that multi-week personalization has been *evaluated* until the harness and experiment are run.
- That the baseline's long run is always ≤30% of weekly volume, or that realized weekly distance always follows the progression target (measured otherwise, section 5).
- That the 10% progression rule or the 80/20 split is an established law (evidence is mixed/contextual).
- That validation guarantees safety of the generated text (it checks numbers only).
- Any novelty claim, including "first", "only", or "never done": the manuscript now states that running-plan generation by LLMs has been studied [11] and that no novelty beyond the cited literature is claimed.

## 7. Suggested order of work

1. Decide §5 rule-engine questions; fix or document.
2. Fix evaluation instrument and UI (§3), then pilot with a few runners.
3. Build the LLM harness and run RQ2 with stored raw outputs.
4. Obtain ethics clearance; run the user study.
5. Fill results (V-C, V-D, Table VII), rewrite abstract/conclusion, draw figures.
6. Final reference check (manual Google Scholar, abstracts), then template conversion.

## 8. Word manuscript (`PAPER_IEEE.docx`) — formatting differences from the official IEEE/BINUS template

Generated by `build_docx.py` from `PAPER_DRAFT.md` (the Markdown file is the source of truth; re-run `python build_docx.py` after editing it; requires `python-docx`). Content check (re-run after this update): the word sets of the two files differ only in rendered math notation.

- Implemented: A4, two-column body (title/authors single column), 14.5 mm side margins, Times New Roman 10 pt, justified text, small-caps section headings, italic subsection headings, editable Word tables with shaded header rows, bordered figure placeholders with captions, page numbers, hanging-indent numbered references.
- Differences: section/subsection numbers are typed text (not Word auto-numbering); headings use the built-in Heading 1/2 styles recoloured black; equations are typeset as formatted text with tab-aligned numbers, **not** Word equation objects (OMML), and Eq. (2) may wrap in a single column; the author block is a simple centered paragraph, not the IEEE three-column author grid; table column widths are estimated from text length and may need manual adjustment; no widow/orphan, column-balancing or hyphenation tuning; no running header; bottom margin 25 mm rather than the template's.
- Not verified: the file was checked structurally (reopens with python-docx, 11 tables, 2 sections, 2-column section present, 31 references all cited, no Markdown residue) but **not** rendered, because no Word/LibreOffice was available. Open it in Word and check pagination, table widths and Eq. (2).
- Best next step: paste the content into the official BINUS/IEEE `.dotx` template (like the existing `Paper.docx`) so styles match exactly.


## 9. Update log (reference-audit revision)

- Gap statement rewritten; Düking 2024 added and compared methodologically; contributions rewritten conservatively; artifact-versus-experiment distinction added to III-A; Table II now classifies each rule; Table V adds a conceptual-basis column; V-E limitations updated.
- RQ1-RQ3 unchanged; RQ2 remains [EXPERIMENT REQUIRED]; no results were added.
- Status: **Draft ready for advisor/literature review.** It is not a complete paper: experiments, participant data, figures, author block and several [VERIFY] items remain.
- `PAPER_DRAFT.md` has NOT been edited by the 2 October 2026 updates (2-LLM or Gemini-only). It still uses "different large language models" / generic multi-LLM wording in RQ2 and Table IV criteria counts that do not match the now-locked 8. This is flagged here, not fixed, per the task constraint that `PAPER_DRAFT.md` and `PAPER_IEEE.docx` are out of scope for methodology-document edits.

---

## Advisor Decision Update — 2 October 2026 — `SUPERSEDED` (2-LLM design; kept for audit trail only)

~~2 LLM design approved (item 1 under "Experiments" reflected 2 LLMs, "LLM A"/"LLM B"); 3 repetitions per (runner profile × LLM) approved~~ — superseded, see below.
- Expert evaluation excluded entirely from the study (item 3 under "Experiments") — *not superseded, still current.*

## Advisor Decision Update — 2 October 2026 (Gemini-only design)

**This is the current, authoritative design, superseding the 2-LLM design recorded in the update above (issued earlier the same day).**

- **1 LLM (Gemini) CONFIRMED** (item 2 under "Experiments"); exact model/version to be finalized and recorded before data collection.
- **24 runner profiles CONFIRMED.**
- **3 Gemini repetitions per profile CONFIRMED → 72 Gemini generations; 24 baseline plans, generated once, NOT repeated.** Total outputs for comparison: 24 baseline + 72 Gemini — never "96 independent experimental generations," never the superseded "144"/"216" generation figures from earlier 2-LLM/3-LLM drafts.
- **Exactly 8 automated criteria LOCKED** (item 3 under "Experiments"); exact operational definitions remain an OPEN SUB-DECISION, explicitly flagged — conflict between the methodology lock's own 8, the superseded comparative proposal's 16-item draft, and `PAPER_DRAFT.md` Table IV's 5 criteria. Not resolved by this update.
- **Multi-week scope CONFIRMED**: Gemini must receive sufficient multi-week context, not Week 1 only. Pipeline: Runner Profile → Validation → Physiological Calculation → Deterministic Rule-Based Multi-Week Baseline → Gemini Personalization → Server-Side Validation → Gemini-Personalized Multi-Week Plan → Automated Evaluation → Baseline vs Gemini Comparison.
- **Expert evaluation still excluded** (unchanged).
- **No ranking/winner framing**: results per criterion, Gemini vs baseline; no composite/overall score; Gemini never declared "better"/"improves"/"superior" without statistical support.
- **These decisions do not touch `PAPER_DRAFT.md` or `PAPER_IEEE.docx` content** — both remain out of scope for this update and are only flagged (see the update log above) as containing obsolete 2-LLM/generic-LLM wording and a mismatched criteria count.
- **Not resolved by this update** (still open/unresolved): exact Gemini model/version; exact 8-criteria operational definitions/thresholds; the statistical test (must account for 72 Gemini outputs nested within 24 profiles); RQ3 sample size/design; ethics/BINUS requirements; questionnaire validation/pilot; prompt implementation/reproducibility details; profile demographic composition detail. **Resolved since this update: the baseline rule-engine rebound/taper fix-or-document decision** (rebound fixed; taper confirmed correct as-is; see `paper/CODE_AUDIT_EASY_RUN_PACE_AND_T7.md`).

---

## STATUS SUMMARY

**CONFIRMED:** 24 runner profiles; Gemini as the only LLM; 3 Gemini repetitions per profile; 24 baseline plans; 72 Gemini generations; no expert evaluation; exactly 8 automated criteria (count locked); multi-week personalization (as the locked design target); baseline vs Gemini comparison.

**OPEN:** exact Gemini model/version; exact 8-criteria definitions/thresholds (explicit conflict between the lock's 8, the superseded comparative proposal's 16, and the paper's Table IV 5 — not resolved here); statistical test; RQ3 sample size; ethics/BINUS requirements; questionnaire validation/pilot; prompt implementation/reproducibility details; profile demographic composition; `PAPER_DRAFT.md`/`PAPER_IEEE.docx` alignment (flagged, not edited).
