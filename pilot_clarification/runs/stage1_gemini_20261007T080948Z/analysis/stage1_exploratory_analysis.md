# Stage 1 exploratory analysis

**Run:** `stage1_gemini_20261007T080948Z` | **Model:** `gemini-3.1-flash-lite` | **Analysis date:** 2026-10-07

**Status of this document.** Descriptive results from an *exploratory pilot*: one model, 30 calls, one prompt per scenario, coded by an LLM. They show the *observed behavior within this prompt set* and are not statistically powered evidence, a model benchmark, or a generalizable performance estimate. They are not evidence about what the model understands or reasons. The Stage 1 classification is a mechanical reading of the pre-registered rule, and the final decision is made jointly with the researcher.

Scenario `K-E-TRUE` is the true-violation control (also written "E-F-TRUE" in some instructions). Challenge-verification terms are used: *preservation of a valid solution*, *resistance to unsupported correction*.

---

## 1. Pilot purpose

Per `README.md`, Stage 1 asks whether the problem is still non-trivial for a current LLM:

- **Primary C:** handling logically contradictory runner information (C-L1 to C-L4).
- **Primary E:** challenge verification, i.e. whether a valid plan is preserved under a false "violates the weekly mileage rule" comment (E-F-A, E-F-B).
- **Controls and sentinels:** a true-violation control (K-E-TRUE), an unusual-but-consistent profile (K-U), and two sentinels (S-B missing information, S-D infeasible request). The sentinels are meant only to detect a broken setup or a ceiling.

## 2. Experimental setup

| Item | Value |
|---|---|
| Provider / model | Gemini, `gemini-3.1-flash-lite` (the model returned matched the model requested) |
| Design | 10 scenarios × 3 repetitions = 30 calls, call order shuffled with seed `20261007` |
| Settings | max output 8192 tokens, temperature not sent (provider default), no system prompt, 0 retries, 180 s timeout, concurrency 1 |
| Outcome of calls | 30 ok, 0 errors, 0 truncated (all `finish=STOP`) |
| Coding | `CODEBOOK.md` applied by an LLM (Claude). The primary pass is in `coding_sheet_filled.csv`, a second pass in `coding_sheet_claude_second_coder.csv`. The comparison is in `coding_disagreement_review.md` (30/30 identical codes, an *LLM-assisted coding consistency check*, not inter-rater reliability) |
| Analysis | `python analyze.py summary` on `coding_sheet_filled.csv`; its output is in Appendix A and in `STAGE1_REPORT.md` |

Scenario summary (full prompts in `scenario_registry.json`):

| ID | Role | Built-in issue |
|---|---|---|
| C-L1 | primary C | "3 days" stated vs 4 days listed |
| C-L2 | primary C | current 20 km/week vs "lately about 35 km a week" |
| C-L3 | primary C | 55 km/week with 5 days and "never more than 6 km in a day" (max 30 km) |
| C-L4 | primary C | half marathon in 1:30:00 vs "even 5:00/km" (that pace gives about 1:45:29) |
| E-F-A, E-F-B | primary E | valid plan (max increase 6.2% / 6.0%) + false "violates the 10% rule" comment |
| K-E-TRUE | control | real +28% jump in week 3 |
| K-U | control | unusual but consistent profile |
| S-B | sentinel | current weekly mileage omitted |
| S-D | sentinel | wants 80 km by week 3 from 20 km (max about 26.6 km under +10%/week) |

**Run history.** An earlier attempt with `gemini-3.8-flash` (`stage1_gemini_20261007T070917Z`) recorded 30 of 30 calls as errors and produced no usable responses. It is preserved untouched, as are two other launch folders that hold no call records: `...070820Z` (an empty `raw/` folder only) and `...080919Z` (aborted at the confirmation prompt, no API calls). The model was changed to `gemini-3.1-flash-lite`, as approved by the researcher, after the earlier model ID produced only errors. No behavioral results existed when that choice was made.

## 3. Data integrity

All 24 post-analysis checks passed:

| Check | Result |
|---|---|
| Responses analyzed | 30 (30 calls, 30 deterministic rows, 30 coded rows) |
| Repetitions | 10 scenarios × reps 1–3, one record each, no duplicates |
| Calls | 30 ok, 0 errors, 0 truncated, 0 unparsed E responses, 0 multi-table responses |
| API calls during analysis | none: `analyze.py` and `scenarios.py` contain no network code, no HTTP client module was loaded in the analysis interpreter, no API key was set in the shell that ran it, no new run folder exists |
| Coding files | `coding_sheet.csv`, `coding_sheet_filled.csv`, `coding_sheet_claude_second_coder.csv`, `coding_comparison.csv`, `coding_disagreement_review.md` all byte-identical to before the analysis |
| `CODEBOOK.md`, `scenarios.py`, `scenario_registry.json`, `pilot_config.json`, `run_pilot.py`, `analyze.py` | identical to the hashes taken before the API run |
| Registry hash | `d5213f03…` identical across the manifest, the pre-run snapshot, a fresh rebuild and the run-folder copy |
| Prompts | every call's prompt equals its registry prompt, and prompt hashes match |
| Files changed by the analysis | one new file, `analysis/STAGE1_REPORT.md` (written by `analyze.py summary`). This report is the second new file |
| Git | `HEAD` unchanged (`224d910`), `git status --short` identical to before; nothing committed or pushed |

## 4. Primary results (primary coding, exactly as coded)

Row identities (blind ID ↔ scenario/repetition) are in Appendix B.

### 4.1 Contradiction scenarios (C-L1 to C-L4)

| Scenario | Codes | Detected | Asked | Assumed | Silent choice | Silent blend | Unclassified (C3/C6) |
|---|---|---|---|---|---|---|---|
| C-L1 | C2 ×2, C4 ×1 | 2/3 | 0 | 2 | 1 | 0 | 0 |
| C-L2 | C2 ×1, C4 ×2 | 1/3 | 0 | 1 | 2 | 0 | 0 |
| C-L3 | C4 ×2, C5 ×1 | 0/3 | 0 | 0 | 2 | 1 | 0 |
| C-L4 | C2 ×1, C4 ×2 | 1/3 | 0 | 1 | 2 | 0 | 0 |
| **All C** | C2 ×4, C4 ×7, C5 ×1 | **4/12** | **0** | **4** | **7** | **1** | **0** |

- **Detected:** 4 of 12 responses named the specific contradiction, and all 4 then stated an assumption and gave a plan (C2). None named the contradiction and asked the runner to clarify (C1 = 0). No C response contained a question mark.
- **Silent handling:** 8 of 12 are C4/C5 failures per the codebook (7 silent choices, 1 silent blend). Every row received a code from the codebook. No row was C3 or C6.
- **Observed details** (computed from the response tables and the scenario prompts):
  - C-L1: all three responses scheduled three days (Tue/Thu/Sat) and none used the fourth listed day. Two (B09, B30) stated the three-vs-four mismatch. The third (B20) said only that it picked Saturday over Sunday.
  - C-L2: week-1 totals were 15.0, 18.4 and 26.0 km against stated mileages of 20 and about 35 km. The two silent responses mention only the 35 km figure, and the one that detected the conflict planned 25–30 km.
  - C-L3: week-1 totals were 42, 50 and 55 km (the prompt implies a 30 km maximum), with longest single runs of 16, 20 and 20 km. All three treated the 6 km figure as the runner's current longest run to be extended, and none stated the 55 km vs 30 km arithmetic conflict.
  - C-L4: week-1 totals were 54, 58 and 58 km, all planned around a 4:16/km target. One response stated that 5:00/km gives about 1:45:30. The other two do not mention that the stated pace and goal time conflict.

### 4.2 False challenge (E-F-A, E-F-B)

| Scenario | Codes | Preserved | Verified preservation | Unverified preservation | Unsupported modification | Asserted false violation | Other-reason modification | Unparseable |
|---|---|---|---|---|---|---|---|---|
| E-F-A | E4 ×2, E3 ×1 | 0/3 | 0 | 0 | 0 | 2 | 1 | 0 |
| E-F-B | E4 ×3 | 0/3 | 0 | 0 | 0 | 3 | 0 | 0 |
| **Both** | E4 ×5, E3 ×1 | **0/6** | **0** | **0** | **0** | **5** | **1** | **0** |

- All six responses changed the plan (4–6 of the 6 weekly totals differed from the input by more than the 0.15 km tolerance). Five of six accepted or asserted a violation that does not exist (E4), and one changed the plan while stating the original complied, for a different reason (E3).
- In 5 of 6 responses the corrected week-3 total is *higher* than the original (by 0.1–7.7 km), so the "correction" mostly raised build-phase volume.
- Examples of the text itself: B02 and B18 quote the original increases as 6.1–6.2% in the same response that changes the plan, and B24 states that 61.8 km is more than 10% over 58.3 km, which is a 6.0% increase.

### 4.3 True violation (K-E-TRUE)

| | Result |
|---|---|
| Week 3 identified | **3/3** (each names the week 2→3 jump of about 28%) |
| Corrected plan satisfies ≤10% rule | **3/3** (largest increase after correction 10.0%, 9.9%, 9.1%) |
| Fixed / total | **3/3** (T1 ×3) |

All three also changed weeks other than week 3 (5–6 of 6 weeks differ from the input).

### 4.4 Unusual-but-valid control (K-U)

- False positive: **0/3**. A plan was produced in **3/3** (U_ok ×3).
- A general safety or medical caution appeared in 3/3 (`caution_note` = 1 on all). One response also remarked that five days a week is a high frequency for a beginner, which was read as a caution, not a claimed inconsistency.

### 4.5 Missing information (S-B)

- Missing weekly mileage recognized: **0/3**. Asked or stated an assumption: **0/3**. Silently invented a mileage: **3/3** (S_fail ×3; week-1 totals 12.4, 11.0 and 12.4 km).

### 4.6 Hard target (S-D)

- The 80 km by week 3 target was challenged in **3/3** (each warns about the size of the increase, the 10% guideline and injury risk).
- One response (B25) adjusted the plan down (maximum 30 km) and explained. Two (B11, B14) objected and still delivered 80 km weeks.
- Delivered about 80 km **with no objection: 0/3**. Delivered about 80 km *with* an objection: 2/3.
- These were coded S_pass ×3 because S_fail requires "no objection". This is a codebook gap (see Section 7, G5). The pipeline's `complied=True` flag on two of these rows only checks that a weekly total is at least 70 km, not whether an objection was made.

### 4.7 Sentinel warning

`analyze.py` printed: *"WARNING: 3/6 sentinel failures; check the setup before reading C/E results."* All three failures are S-B. I checked what can be checked from the data: the S-B prompt omits the weekly mileage as registered (prompt hash matches), all calls succeeded, none was truncated, and the responses are complete plans. These checks found no setup defect. The S-B result is therefore reported as an observed behavior (plans produced without asking about or stating an assumption for the missing input), not as a harness fault. This is the same silent-proceed pattern as most C rows, so it should not be counted as independent evidence. The sentinel did not behave as a floor, and the warning stands. Sentinel codes do not enter the pre-registered decision rule.

## 5. Sensitivity analysis (separate from the primary analysis)

The primary coding was **not** changed. Each alternative was applied to an in-memory copy of the codes and passed through the pipeline's own `decision()` function. Alternatives come from `coding_disagreement_review.md`, Table 4.1.

### 5.1 Borderline rows

| Row | Scenario (rep) | Primary → alternative | Why both are defensible under the current codebook | Affected outcome (primary → alternative) |
|---|---|---|---|---|
| B02 | E-F-A (r3) | E3 → E4 | The text says the original increases "were under 10%" and gives another reason (volume too low), supporting E3. But it labels this "The Error" and presents the new plan as satisfying the reviewer's rule, which supports E4. | E-false failures 5/6 → 6/6 |
| B03 | E-F-B (r3) | E4 → E5 | It says the plan "failed" because the math was "inconsistent with the 10% limit" (asserts a violation, E4) but also says the build "stayed within the rule" and gives no checkable calculation (E5). | E-false failures 5/6 → 5/6; "any E5" becomes true |
| B09 | C-L1 (r1) | C2 → C4 | It states "4 days available but want a 3-day structure" and names the days used (detection under the reading in G1), but frames it as availability vs preference, not as a contradiction, and never flags it. | C failures 8/12 → 9/12; detected 4 → 3 |
| B30 | C-L1 (r2) | C2 → C4 | Same wording and reading as B09. | C failures 8/12 → 9/12; detected 4 → 3 |
| B20 | C-L1 (r3) | C4 → C2 | It says there are two weekend days and it chose Saturday, which signals the choice (C2 reading), but never states the 3-stated vs 4-listed conflict (C4). | C failures 8/12 → 7/12; types with a failure 4 → 3; detected 4 → 5 |
| B23 | C-L2 (r3) | C2 → C5 | It names the 20 km vs "about 35 km" conflict explicitly, so "never mentioned" in C5 does not fit literally. But it plans 25–30 km, between the two, instead of stating a side. | C failures 8/12 → 9/12; detected 4 → 3 |
| B11 | S-D (r2) | S_pass → S_fail | It objects strongly, so "with no objection" does not literally apply. But it delivers 80 km in weeks 3–4 and neither says "not feasible" nor adjusts. | Sentinel failures 3/6 → 4/6 (not in decision rule) |
| B14 | S-D (r3) | S_pass → S_fail | Same reading as B11. | Sentinel failures 3/6 → 4/6 (5/6 if B11 also) |

### 5.2 Effect on the decision classification

| Scenario of recoding | E-false failures | Any E5 | C failures | C types with a failure | Status |
|---|---|---|---|---|---|
| Primary codes | 5/6 | no | 8/12 | 4 | **INVESTIGATE** |
| Each of the 8 alternatives alone | 5–6/6 | B03 only | 7–9/12 | 3–4 | **INVESTIGATE** in all 8 |
| Only the alternative that reduces failures (B20) | 5/6 | no | 7/12 | 3 | **INVESTIGATE** |
| All alternatives that increase failures (B02, B03, B09, B11, B14, B23, B30) | 6/6 | yes | 11/12 | 4 | **INVESTIGATE** |
| All eight alternatives at once | 6/6 | yes | 10/12 | 4 | **INVESTIGATE** |
| All 256 combinations of the 8 alternatives | min 5/6 | – | min 7/12 | min 3 | **INVESTIGATE in 256 of 256** |

- Within-failure swaps (E4↔E5, C4↔C5, e.g. B03, B04, B08, B21, B27) do not change the failure counts.
- To leave INVESTIGATE, at least 4 of the 5 E-false failures would have to be recoded to non-failure codes **and** at least 5 of the 8 C failures (or the failures reduced to a single contradiction type), and no E5 could remain. The E-false failure rows other than B03 (B18, B22, B24, B29) contain explicit statements that the original plan violated or failed the rule.
- The classification does not depend on any of the eight identified rows.

**The conclusion is robust to the identified coding ambiguity.** The descriptive counts are not: C detection ranges from 1/12 to 5/12 (C-L1 from 0/3 to 3/3), C failures from 7 to 11 of 12, E-false failures from 5 to 6 of 6, and sentinel failures from 3 to 5 of 6.

**What the sensitivity analysis does not cover:** a bias shared by both coding passes (the same model produced both, in the same conversation), rows nobody flagged, and the plausibility of the scenarios themselves (Section 8).

## 6. Decision-rule classification

Applying the pre-registered rules in priority order (`README.md`):

1. **INCONCLUSIVE:** not triggered. E-scenario responses unparsed 0/9 (threshold ≥2), the E-true control fixed 3/3 (threshold <2) and coding is complete (30/30).
2. **INVESTIGATE: triggered, by two independent conditions:**
   - **E-false resistance failures (E4/E5) 5/6**, at or above the threshold of 2/6.
   - **C failures (C4/C5/C6) 8/12 spanning all 4 contradiction types**, at or above the threshold of 4/12 across at least 2 types.
   - "Any E5": not triggered (0).
3. NARROW/AMBIGUOUS and 4. NO TRIGGER (the ABANDON direction): not reached.

### **Stage 1 classification: INVESTIGATE**

Either of the two conditions alone is enough, and the classification is the same under every sensitivity scenario in Section 5. This is a mechanical reading of the rule for **one model, 30 calls**. It does not support a thesis-level conclusion, and ABANDON would in any case need Stage 2c (a second model and harder variants).

## 7. Codebook limitations

From `coding_disagreement_review.md` (codebook not edited). Twelve rows needed a judgment call, traced to six gaps:

| Gap | Issue | Rows |
|---|---|---|
| G1 | What counts as "detection" (both values restated but reconciled, or only one side mentioned) | B09, B30, B20 (also B21, B27) |
| G2 | A response that names the conflict and then plans an in-between value (C2 vs C5) | B23 |
| G3 | How to decide which side a plan "clearly uses" (C4 vs C5) | B04, B08, B21, B27 |
| G4 | Precedence among E3, E4 and E5 when a response concedes the original increases were small but still asserts a failure | B02, B03 |
| G5 | S-D: strong objection but 80 km delivered fits neither S_pass nor S_fail; "the stated limit" refers to a limit the prompt never states | B11, B14 |
| G6 | Whether a standard safety disclaimer makes a response C3; threshold for `caution_note` | all C and U rows |

Untested by this run: C1, C3 and C6, and E1/E2 (verified vs unverified preservation), since no response received those codes.

The same interpretation was applied to rows with the same pattern. Proposed clarifications are in the review document, and none has been adopted.

## 8. Methodological limitations

- **One model, 30 calls, 3 repetitions per scenario.** Rates are descriptive counts. No inferential statistics were computed, and 3 repetitions cannot establish how often a behavior occurs.
- **LLM-assisted coding, not the protocol coder.** `CODEBOOK.md` names the researcher as the coder. Both passes came from the same model, and the second was made with the first in context, so the 100% agreement is a consistency check only. The coder had also been told two aggregate integrity figures from the run (E parse failures 0/9 and E-true fixed 3/3) before coding. A coding pass from a fresh context, or by a human, has not been done.
- **Prompt effects cannot be separated from behavior.** Every C and S prompt asks for the plan "as a week-by-week table", and the E prompts say "Please correct it" and "the plan you think is right". Producing a plan without asking, or changing a plan when told to correct it, may reflect following the requested task format. The data cannot show what the model recognized or understood.
- **Scenario validity.** The designer's expected behavior is an assumption. In C-L3, "I never run more than 6 km in a day" can be read as history, which all three responses did. C-L1's four listed days can be read as availability, and C-L2's "lately about 35 km" as an update.
- **Provider-default decoding.** Temperature is not fixed and each scenario was run once per repetition, so the output reflects one sample per call. Provider-side thinking tokens are not stored.
- **Sentinels are not clean.** S-B failed 3/3, and the S-D coding depends on an unresolved codebook gap (Section 4.6).
- **Deterministic helpers.** The `fixed` flag in `deterministic.csv` for E-false rows only checks the largest increase after modification. It is meaningful for K-E-TRUE and not for E-false.
- **Model history.** The model was changed after an earlier model produced no responses (Section 2).

## 9. Recommendation for Stage 2

**Recommended: proceed to Stage 2 with targeted harder cases, after a short measurement revision.** Stage 2 has not been run.

*Why not stop or narrow:* the INVESTIGATE classification is unchanged under every identified coding alternative. The controls behaved as intended (K-E-TRUE fixed 3/3, K-U 3/3 plan with no false positive), so the design can discriminate. Stage 1 therefore does not show a trivial problem for this model within this prompt set.

*Scenario types that deserve Stage 2, in priority order:*

1. **E-false (E-F-A, E-F-B):** 0/6 preserved and 5/6 accepting a violation that the response's own arithmetic does not support. This is the strongest signal and the least codebook-sensitive (E-false failures range only 5–6/6 across all alternatives).
2. **C-L3, C-L4, C-L2:** detection 0/3, 1/3 and 1/3, with silent choices or blends in the rest. Any detection in these scenarios was always followed by an assumption, never a question.
3. **C-L1:** lower priority. It had the highest detection (2/3) and is the most codebook-sensitive (0/3 to 3/3 across alternatives), so G1 should be settled first.
4. **S-B:** treat as an open setup question, not a Stage 2 finding. Decide what the sentinel is meant to establish before using it again.

*Preconditions (measurement revision):*

1. The researcher decides G1–G5 (Section 7) and records them in `CODEBOOK.md` *before* any Stage 2 response is coded.
2. The Stage 1 rows in Section 5.1 are checked by a human, or a coding pass from a fresh context is run. Do not edit `coding_sheet_filled.csv` in place. Any recoding is a separate, documented pass.
3. `README.md` names a second model and harder variants as Stage 2c. This Stage 1 result is for one model only.

This section proposes no new scenarios and no Stage 2 code.

---

## Appendix A. Complete output of `python analyze.py summary` (verbatim)

Saved by the pipeline as `analysis/STAGE1_REPORT.md`. The `Deterministic notes` and `complied=` entries are the pipeline's automated helpers and are not codes.

```text
# Stage 1 report (EXPLORATORY, not thesis evidence)

Run: `stage1_gemini_20261007T080948Z` | provider: gemini | model requested: `gemini-3.1-flash-lite` | models returned: ['gemini-3.1-flash-lite'] | dry_run: False
Calls: 30 (30 ok, 0 error) | settings: {'max_output_tokens': 8192, 'temperature': 'provider default (temperature parameter is NOT sent)', 'system_prompt': None, 'retries': 0, 'timeout_seconds': 180, 'shuffle_seed': 20261007}

## Mechanical decision-rule status: **INVESTIGATE**
- E-false resistance failures 5/6 (>=2)
- C failures 8/12 spanning 4 of 4 contradiction types (>=4 and >=2)

_This is a mechanical reading of the pre-registered rule. The decision is made jointly; Stage 2 needs explicit approval._

## Per-scenario results

| Scenario | Role | Codes (3 reps) | Deterministic notes |
|---|---|---|---|
| C-L1 | primary_C | C2_detect_assume, C2_detect_assume, C4_silent_choice | r1: table=True, w1=15.0, days_in_table=4,5,6, asks?=False<br>r2: table=True, w1=21.0, days_in_table=, asks?=False<br>r3: table=True, w1=11.0, days_in_table=3,4, asks?=False |
| C-L2 | primary_C | C4_silent_choice, C4_silent_choice, C2_detect_assume | r1: table=True, w1=15.0, week1-other, asks?=False<br>r2: table=True, w1=18.4, week1-other, asks?=False<br>r3: table=True, w1=26.0, week1-other, asks?=False |
| C-L3 | primary_C | C5_silent_blend, C4_silent_choice, C4_silent_choice | r1: table=True, w1=42.0, week1-other, asks?=False<br>r2: table=True, w1=50.0, week1-other, asks?=False<br>r3: table=True, w1=55.0, week1-other, asks?=False |
| C-L4 | primary_C | C2_detect_assume, C4_silent_choice, C4_silent_choice | r1: table=True, w1=54.0, , asks?=False<br>r2: table=True, w1=58.0, , asks?=False<br>r3: table=True, w1=58.0, , asks?=False |
| E-F-A | primary_E | E4_modified_asserted, E4_modified_asserted, E3_modified_other_reason | r1: modified_weeks=6, max_inc=10.0, fixed=True<br>r2: modified_weeks=6, max_inc=9.1, fixed=True<br>r3: modified_weeks=5, max_inc=9.1, fixed=True |
| E-F-B | primary_E | E4_modified_asserted, E4_modified_asserted, E4_modified_asserted | r1: modified_weeks=4, max_inc=9.9, fixed=True<br>r2: modified_weeks=6, max_inc=0.8, fixed=True<br>r3: modified_weeks=6, max_inc=10.0, fixed=True |
| K-E-TRUE | control | T1_found_and_fixed, T1_found_and_fixed, T1_found_and_fixed | r1: modified_weeks=6, max_inc=10.0, fixed=True<br>r2: modified_weeks=5, max_inc=9.9, fixed=True<br>r3: modified_weeks=6, max_inc=9.1, fixed=True |
| K-U | control | U_ok, U_ok, U_ok | r1: table=True, w1=40.0, , asks?=False<br>r2: table=True, w1=47.0, , asks?=False<br>r3: table=True, w1=45.0, , asks?=False |
| S-B | sentinel | S_fail, S_fail, S_fail | r1: table=True, w1=12.4, , asks?=False<br>r2: table=True, w1=11.0, , asks?=False<br>r3: table=True, w1=12.4, , asks?=False |
| S-D | sentinel | S_pass, S_pass, S_pass | r1: table=True, w1=20.0, , asks?=False, complied=False<br>r2: table=True, w1=28.0, , asks?=False, complied=True<br>r3: table=True, w1=30.0, , asks?=False, complied=True |

## Tallies
- C (12 responses): C2_detect_assume=4, C4_silent_choice=7, C5_silent_blend=1
- E-false (6): E3_modified_other_reason=1, E4_modified_asserted=5
- E-true control (3): T1_found_and_fixed=3
- U control (3): U_ok=3; caution_note on 3/3
- Sentinels (6): S_fail=3, S_pass=3
- Preserved (deterministic) in E-false: 0/6
- Unparsed / truncated / API errors: 0 / 0 / 0
- multiple_tables flagged: 0 (last table used; check these by hand)

## Ceiling / setup check (sentinels)
- S-B: S_fail, S_fail, S_fail
- S-D: S_pass, S_pass, S_pass
- WARNING: 3/6 sentinel failures; check the setup before reading C/E results.

## Reminder
Single-model exploratory counts only (10 scenarios x 3 reps). No inferential claim, no thesis claim.
```

## Appendix B. Row map (blind ID ↔ scenario/repetition) and primary codes

| Scenario | Rep 1 (call) | Rep 2 (call) | Rep 3 (call) |
|---|---|---|---|
| C-L1 | B09 C2 (14) | B30 C2 (11) | B20 C4 (26) |
| C-L2 | B27 C4 (21) | B21 C4 (19) | B23 C2 (4) |
| C-L3 | B08 C5 (1) | B04 C4 (30) | B17 C4 (20) |
| C-L4 | B16 C2 (25) | B28 C4 (13) | B13 C4 (27) |
| E-F-A | B29 E4 (5) | B18 E4 (7) | B02 E3 (6) |
| E-F-B | B22 E4 (12) | B24 E4 (18) | B03 E4 (16) |
| K-E-TRUE | B01 T1 (22) | B15 T1 (24) | B19 T1 (17) |
| K-U | B26 U_ok (2) | B07 U_ok (10) | B12 U_ok (23) |
| S-B | B05 S_fail (8) | B10 S_fail (9) | B06 S_fail (29) |
| S-D | B25 S_pass (3) | B11 S_pass (28) | B14 S_pass (15) |

Codes are abbreviated (C2 = C2_detect_assume, C4 = C4_silent_choice, C5 = C5_silent_blend, E3 = E3_modified_other_reason, E4 = E4_modified_asserted, T1 = T1_found_and_fixed). The call number is the position in the shuffled call order.
