**Methodological proposal pending advisor approval**

# Profile-Fact Slot Specification for E6 (Personalization Coverage) and E7 (Personalization Specificity)

> **REVISION NOTE (post-`EVALUATION_CRITERIA_FINAL_CONSISTENCY_REVIEW.md`).** The original version of this document corrected `EVALUATION_CRITERIA_OPTION_A_DESIGN.md`'s 9-slot list down to a 7-slot traceable set (S1–S7) on *traceability* grounds alone — i.e., it asked only "does this field exist in the documented schema?" The consistency review asked a second, independent question — "even if the field exists, is checking it actually evidence of *personalization*, or is it just a restatement of *constraint preservation* (E1–E4) under a different name?" — and found that S1–S6 fail that second test: each is a documented rule-engine input, so the deterministic baseline already computes the one "correct" per-runner value for it, and checking a Gemini plan against that same value is indistinguishable from E1/E2/E3/E4/E5's own checks. Only S7 (`injury_limitations`) survives both tests. This revision adds that second classification pass (§3, §4, §5 below) on top of the original traceability pass, narrows the recommended E6/E7 slot set to S7 alone, and carries the traceability findings (drop `vdot_band`/`stated_preference`; treat `goal_distance`/`goal_time` as aliases, not silently merged) forward unchanged. See `EVALUATION_CRITERIA_OPTION_A_DESIGN.md`'s Revision Note and §4 (E6/E7) for the corresponding update there.
>
> **Methodological proposal pending advisor approval.** Nothing in this document is implemented. It does not modify the existing 8-criterion framework; it specifies the slot set and detection rules needed to make E6/E7 objectively computable AND independent of E1–E4, as requested after reviewing `EVALUATION_CRITERIA_OPTION_A_DESIGN.md` and `EVALUATION_CRITERIA_FINAL_CONSISTENCY_REVIEW.md`.

> **Repository caveat (read before using the tables below).** This repository (`D:\research s2\paper`) contains only thesis documentation — no application source code (no `backend/`, `frontend/`, `.py`/`.ts` model files). The application code (`app/models.py`, `app/schemas.py`, `app/rules/generator.py`, frontend pages) lives in a separate repository not present at this path. Every "implemented" claim below is therefore sourced from **documentation's description of the code** — primarily `RESEARCH_METHODOLOGY_LOCK.md` §9.1 (lines 248–257) and `EVALUATION_CRITERIA_OPTION_A_DESIGN.md` (lines 117–119, 197–198) — not from reading the code directly. **Before implementation, the actual schema files must be inspected in the real application repository to confirm field names, types, and validator ranges.** Where documents disagree with each other, that disagreement is flagged explicitly rather than silently resolved.

---

## 1. Executive Summary

E6 and E7 are supposed to answer two different questions:

- **E6 (Coverage):** Did the generated plan correctly incorporate the applicable runner-profile facts?
- **E7 (Specificity):** When a fact is incorporated, does the plan instantiate the actual stored value/context, rather than making a generic statement that would be true for any runner?

Both questions presuppose a prior one that this revision makes explicit: **incorporate it relative to what?** For a fact the deterministic baseline already uses to compute its own output (e.g. `target_race_time` → the baseline's pace targets), "did Gemini incorporate it" and "did Gemini preserve the baseline's constraint" collapse into the same check — E1–E4 already answer it. E6/E7 can only contribute *new* information for facts the baseline does not itself consume.

The existing draft `SLOTS` list (`EVALUATION_CRITERIA_OPTION_A_DESIGN.md`, pre-revision) named nine slots. This document applies two independent screens to that list, in sequence:

1. **Traceability screen (original scope of this document):** is the field actually documented as an implemented profile/rule-engine field? This alone already removes `vdot_band` and `stated_preference` (no backing field anywhere) and resolves `goal_distance`/`goal_time` as aliases of `target_race_distance`/`target_race_time` (Section 2).
2. **Baseline-independence screen (added per `EVALUATION_CRITERIA_FINAL_CONSISTENCY_REVIEW.md`):** of the fields that survive screen 1, which are *rule-engine inputs* the baseline already consumes to compute its own output, and are therefore constraint-derived evidence (Category B, excluded from E6/E7, already measured by E1–E5) rather than personalization evidence (Category A)? This screen removes `experience_level`, `target_race_distance`, `target_race_time`, `current_weekly_mileage_km`, `training_days_per_week`/`preferred_days`, and `plan_duration_weeks` — i.e., everything that survived screen 1 except `injury_limitations` (Section 3).

**Headline recommendation (revised):** of the original nine slots, **one (`injury_limitations`) is both traceable and baseline-independent, and is the recommended E6/E7 slot.** `easy_run_pace` is traceable and plausibly baseline-independent but not confirmed as such (Category C, not adopted pending real-schema confirmation). `vdot_band`, `stated_preference`, `pb_10k`, `age`, and `gender` are dropped (Category D — no traceable field, or no definable detection rule). `experience_level`, `target_race_distance`, `target_race_time`, `current_weekly_mileage_km`, `training_days_per_week`/`preferred_days`, and `plan_duration_weeks` are reclassified **Category B and explicitly excluded from E6/E7** — not because they are untraceable (they are well-documented), but because scoring them under E6/E7 would silently duplicate E1–E5. This is a deliberately narrow result: it trades slot count for construct validity, which the task that requested this revision explicitly allows.

---

## 2. Actual Implemented Runner Profile Fields

Because no source code is present in this repository, "implemented" here means: named as a `RunnerProfile`/`UserProfile` field or rule-engine input in at least one design/lock document, with a stated type. This is a **documentation-sourced inventory**, flagged as such throughout — it is not a code read.

### 2a. Fields documented as implemented AND used by the deterministic rule engine

| Field (canonical name used in this spec) | Type | Rule-engine input? | Source |
|---|---|---|---|
| `experience_level` | enum | Yes | `RESEARCH_METHODOLOGY_LOCK.md:250` |
| `pb_5k` | string `MM:SS` | Yes (VDOT basis) | `RESEARCH_METHODOLOGY_LOCK.md:251` |
| `pb_10k` | string `MM:SS` | Documented as stored; **not** used numerically per Threats-to-Validity note ("10K PB ... not used numerically", `RESEARCH_METHODOLOGY_LOCK.md:363`) | `RESEARCH_METHODOLOGY_LOCK.md:251,363` |
| `target_race_distance` | enum | Yes | `RESEARCH_METHODOLOGY_LOCK.md:252` |
| `target_race_time` | string | Yes | `RESEARCH_METHODOLOGY_LOCK.md:252` |
| `current_weekly_mileage_km` | float | Yes | `RESEARCH_METHODOLOGY_LOCK.md:253` |
| `training_days_per_week` | int | Yes | `RESEARCH_METHODOLOGY_LOCK.md:254`; also E3 schedule check, `EVALUATION_CRITERIA_OPTION_A_DESIGN.md:117,119` |
| `preferred_days` | list of weekday | Yes (paired with the above) | same as above |
| `plan_duration_weeks` | int, validated range 4–24 | Yes | `RESEARCH_METHODOLOGY_LOCK.md:255`; range from `PHASE_5_DISCOVERY.md:90` |
| `injury_limitations` | text, optional | **Not** a numeric rule input — "Text personalization" only, i.e. it is meant to surface in LLM-authored narrative text, not in the deterministic baseline's numeric schedule | `RESEARCH_METHODOLOGY_LOCK.md:256` |

### 2b. Fields documented as implemented but NOT used by the rule engine (profile metadata only)

| Field | Type | Status | Source |
|---|---|---|---|
| `age` | int | Stored; not used numerically ("age ... not used numerically", `RESEARCH_METHODOLOGY_LOCK.md:363`); validated 12–99 at input (`RESEARCH_METHODOLOGY_LOCK.md:191`) | `RESEARCH_METHODOLOGY_LOCK.md:248,363` |
| `gender` | string | Stored; explicitly "not used in numeric rules" | `RESEARCH_METHODOLOGY_LOCK.md:249` |
| `easy_run_pace` | string | "Prompt only" — fed to the LLM prompt, not to the deterministic engine | `RESEARCH_METHODOLOGY_LOCK.md:257` |

### 2c. Fields DOCUMENTED but not traceable to any concrete schema definition

| Field named in a document | Where named | Problem |
|---|---|---|
| `vdot_band` | `EVALUATION_CRITERIA_OPTION_A_DESIGN.md:198` | VDOT is described elsewhere as a *computed, plan-level* value stored per-plan (`training_plans.baseline_json`, `PHASE_2_DESIGN.md:177`), not a profile field, and no binning ("band") logic is described anywhere. |
| `stated_preference` | `EVALUATION_CRITERIA_OPTION_A_DESIGN.md:198` | No definition anywhere else. No corresponding schema field, form field, or rule input is named in any other document. |
| `goal_distance`, `goal_time` | `EVALUATION_CRITERIA_OPTION_A_DESIGN.md:197` | Not a naming inconsistency to fix silently — these appear to be informal aliases for `target_race_distance`/`target_race_time` (§2a), but no document confirms this is the same underlying field rather than a distinct one. **Resolved in this spec by using the canonical names from `RESEARCH_METHODOLOGY_LOCK.md` and treating the SLOTS-list names as aliases**, pending advisor confirmation. |

### 2d. Fields/concepts mentioned only conceptually (no field name anywhere)

| Concept | Where | Note |
|---|---|---|
| Structured injury type/severity/body part | General framing around "injury history" | Only one concrete field exists (`injury_limitations`, free text); no structured sub-fields. |
| General "preferences" | `EVALUATION_CRITERIA_RECONCILIATION.md`, as the rationale for `stated_preference` | No concrete field backs this term. |
| Height / weight / BMI | Not found in any document | Entirely absent — not implemented, documented, or conceptual. |
| Heart-rate training zones as a profile input | `avg_heart_rate`/`max_heart_rate` exist only as **workout-log** fields (a logging feature, `PHASE_2_DESIGN.md:46-47,138`), not as runner-profile inputs to plan generation | Different subsystem; must not be conflated with E6/E7 profile facts. |
| Running-history depth ("years running") | Not found | `experience_level` (enum) is the only proxy. |

---

## 3. Candidate Personalization Facts

Starting from §2a/§2b (the only fields with a traceable implementation claim), each field is now screened through **two** independent tests, applied in order:

- **Screen 1 (traceability):** does a backing field actually exist in the documented schema? (This is the original scope of this document.)
- **Screen 2 (baseline-independence — added in this revision):** for fields that pass Screen 1, is the field a documented *rule-engine input*, i.e. does the deterministic baseline already consume it to compute the baseline plan's own numeric/structural output? If yes, the baseline already supplies the single "correct" per-runner instantiation of that fact, and checking a Gemini plan against it is constraint-fidelity evidence (already owned by E1–E5), not personalization evidence. A field must pass **both** screens, and specifically must be baseline-**independent**, to be eligible for E6/E7.

Each field below is classified **A** (independent personalization evidence — eligible for E6/E7), **B** (constraint-derived evidence — passes Screen 1 but fails Screen 2, excluded from E6/E7), **C** (potentially useful but requires an additional methodological condition not currently satisfied), or **D** (excluded — no field, or no definable detection rule).

| Field | Class | Reason |
|---|---|---|
| `experience_level` | **B** | Rule-engine input (`RESEARCH_METHODOLOGY_LOCK.md:250`) — the baseline's intensity/ramp structure is already the per-level-specific instantiation of this fact. A plan matching that structure is passing E1 (effort-level fidelity); a plan not matching it is failing E1. There is no third outcome ("matches a different, more personalized value") for E6/E7 to detect. |
| `target_race_distance` | **B** | Rule-engine input (`RESEARCH_METHODOLOGY_LOCK.md:252`) — determines the baseline's long-run distance/race-pace workout deterministically; checking a plan against that value is E1/E3, not new evidence. |
| `target_race_time` | **B** | Rule-engine input (`RESEARCH_METHODOLOGY_LOCK.md:252`) — determines the baseline's pace targets; checking a plan's printed pace against it is exactly E1's own check. |
| `current_weekly_mileage_km` | **B** | Rule-engine input (`RESEARCH_METHODOLOGY_LOCK.md:253`) — determines Week 1 volume via the baseline's documented floor/cap rule; checking a plan's Week 1 total against it is exactly E2's own check. |
| `training_days_per_week` + `preferred_days` | **B** | Both are rule-engine inputs (`RESEARCH_METHODOLOGY_LOCK.md:254`) — the baseline's own day arrangement is already placed on `preferred_days`. Checking a plan's day-set against the baseline's day-set (E3) is therefore already checking it against `preferred_days`; there is no additional "was it placed on the *stored* days" fact left for E6/E7 to detect once E3 has run. (This generalizes the overlap the pre-revision version of this document already found for this one field, §13 below.) |
| `plan_duration_weeks` | **B** | Rule-engine input (`RESEARCH_METHODOLOGY_LOCK.md:255`) — determines the number of week-blocks the baseline itself produces; a week-count match is a structural/completeness check (E5/E3 territory), not personalization evidence. |
| `injury_limitations` | **A** | The deterministic baseline does **not** consume this field numerically at all — it is documented as "Text personalization" only (§2a). There is therefore no baseline-computed "correct" modification for a plan to be checked against; any plan-level reference to it is necessarily something Gemini itself produced, not a restatement of a rule-engine output. This is the one field that passes both screens. Detection rule: §6.4 (content-matching against the runner's own stored text, not an external keyword list). |
| `pb_10k` | **D** | Documented as not used numerically anywhere downstream; no plan field is defined to derive from it independently of `pb_5k`. No detection rule can be written without inventing an unstated mapping. |
| `age` | **D** | Not used numerically by the rule engine; no plan-level artifact is defined as "the age-correct value." A check would require inventing an age→output mapping the system does not have. |
| `gender` | **D** | Same reasoning as `age` — explicitly not used in numeric rules, no textual slot defined either. |
| `easy_run_pace` | **C** | Passes Screen 1 (documented, "Prompt only") and is *plausibly* baseline-independent, since the deterministic engine's own paces are computed from `pb_5k`, not from this field. However, documentation does not establish that `easy_run_pace`'s stored value is actually distinct from the `pb_5k`/VDOT-derived pace — if the two coincide by formula, scoring this slot would silently reintroduce the same E1-overlap problem this revision exists to remove. **Not adopted** until the real application schema confirms the two values can diverge for at least some profiles. |
| `vdot_band` | **D** | No backing field exists (§2c) — fails Screen 1. Cannot specify a detection rule for a fact that is not confirmed to be stored. |
| `stated_preference` | **D** | No backing field exists (§2c) — fails Screen 1. Same reasoning. |

**Net effect:** of 13 candidate fields/field-pairs screened, 1 is Category A (`injury_limitations`), 1 is Category C (`easy_run_pace`, not currently adopted), 6 are Category B (excluded from E6/E7 specifically *because* they are well-measured elsewhere, by E1–E5), and 5 are Category D (excluded for lack of a traceable field or detection rule).

---

## 4. Recommended E6 Slot Set (Coverage)

E6 asks: *for each applicable, baseline-independent fact, did the plan's content reflect it at all* (binary presence check per slot, then aggregated as a coverage ratio: applicable-and-reflected ÷ applicable).

**S1–S6 (the slots keyed to `experience_level`, `target_race_distance`, `target_race_time`, `current_weekly_mileage_km`, `training_days_per_week`/`preferred_days`, and `plan_duration_weeks`) are retired from E6**, per the Category-B classification in §3: each would ask "does the plan match the baseline-derived value for this field," which is already E1, E2, E3, E4, or E5's own question. Retaining them under E6 would double-count the same evidence under a second name, which is exactly the overlap `EVALUATION_CRITERIA_FINAL_CONSISTENCY_REVIEW.md` flagged as a blocking issue. Their slot IDs (S1–S6) are kept here, struck through, only so the traceability trail from the pre-revision version of this document is not silently erased:

| Slot ID | Field | Status |
|---|---|---|
| ~~S1~~ | ~~`experience_level`~~ | **Retired — Category B, see §3.** Already measured by E1. |
| ~~S2~~ | ~~`target_race_distance`~~ | **Retired — Category B, see §3.** Already measured by E1/E3. |
| ~~S3~~ | ~~`target_race_time`~~ | **Retired — Category B, see §3.** Already measured by E1. |
| ~~S4~~ | ~~`current_weekly_mileage_km`~~ | **Retired — Category B, see §3.** Already measured by E2. |
| ~~S5~~ | ~~`training_days_per_week` + `preferred_days`~~ | **Retired — Category B, see §3.** Already measured by E3. |
| ~~S6~~ | ~~`plan_duration_weeks`~~ | **Retired — Category B, see §3.** Already measured by E3/E5. |

**The current, recommended E6 slot set:**

| Slot ID | Field | Class | E6 question | Evidence type |
|---|---|---|---|---|
| **S7** | `injury_limitations` (only when non-empty) | **A** | Does the plan's free text contain a specific modification, substitution, or caution tied to the body part/limitation named in the field, via an explicit action verb (not mere silence, and not a generic caution that would apply regardless of what was stored)? | textual |

**Not adopted (Category C, open):** `easy_run_pace` would be a second E6 slot ("does the plan's prescribed easy-run pace match the stored `easy_run_pace` value specifically, rather than the VDOT-derived pace") if and only if the real schema confirms this field can diverge from the `pb_5k`-derived pace for at least some profiles. Pending that confirmation (§14), it is not scored.

**Excluded from E6 for lack of a field/detection rule (Category D):** `pb_10k`, `age`, `gender`, `vdot_band`, `stated_preference` (§3).

---

## 5. Recommended E7 Slot Set (Specificity)

E7 asks, **only for the slot that passed E6 for a given generation**: did the plan instantiate the runner's own *stored context*, not just a generic statement that would be true of any runner? Per §3's Category-B finding, E7's previously proposed numeric/categorical specificity tests for S1–S4/S6 ("does the plan's value match the baseline-computed value for this runner, not a generic default") are now understood to be a restatement of E1–E4's own fidelity tests — the baseline-derived value *is* the per-runner-specific value for those fields, so "matches it" and "preserves the constraint" are the same event. Retaining those tests under E7 would not measure *Gemini's* personalization; it would measure whether Gemini copied the baseline, which E1–E4 already report. **E7 therefore does not mean "did Gemini copy the profile's numeric value"** — that question belongs to E1–E4.

**S1–S6 are retired from E7** for the identical reason they are retired from E6 (§4), including S5: the pre-revision version of this document had already flagged that S5's exact-day-set test "is not independent of E3" (§13 below); this revision generalizes that same finding to S1–S4 and S6.

**The current, recommended E7 slot set:**

| Slot ID | E7 question | Specificity test |
|---|---|---|
| **S7** | Does the text name or clearly reference the specific limitation stored (e.g. a body part or condition token drawn from the field's own text), rather than a generic caution that would apply regardless of what was stored? | See §6.4 — token-overlap/reference check against the *stored field's own content*, not a generic external keyword list. |

This test is independent of E1–E5 precisely because the baseline makes no claim about `injury_limitations` at all (§3) — unlike S1–S4/S6, there is no baseline-derived "expected value" that a token-overlap match could be covertly re-deriving.

**Not adopted (Category C, open):** `easy_run_pace`, same condition as §4.

---

## 6. Exact Detection Rules

> **Note on scope:** §6.1–6.3 below describe the detection rules that applied to S1–S6 in the pre-revision version of this document. They are kept here, explicitly marked retired, only as a traceability record of what E6/E7 used to check — per §3/§4/§5, S1–S6 are now excluded from E6/E7 because those checks duplicate E1–E5. **§6.4 (S7, textual) is the only detection rule currently active for E6/E7.**

**6.1 — RETIRED. Numeric slots (previously S3, S4, S6; the numeric half of S1/S2):**
`detected = |plan_value − expected_value| ≤ tolerance_t`, where `expected_value` and `tolerance_t` were to be read from the deterministic baseline's own published constants. This is no longer an E6/E7 rule — it is, mechanically, E1/E2's own tolerance check (`EVALUATION_CRITERIA_OPTION_A_DESIGN.md` §4 E1/E2), which is why these slots were retired.

**6.2 — RETIRED. Categorical slots (previously S2's distance type, S5's day set):**
`detected = (plan_set == stored_set)` / `detected = (plan_category == profile_category)`. No longer an E6/E7 rule — equivalent to E3's structure check.

**6.3 — RETIRED. Scheduling slot (previously S5):**
Comparing the plan's day assignment to `preferred_days`. No longer an E6/E7 rule — equivalent to E3's day-set check, since the baseline's own day-set is already built from `preferred_days`.

**6.4 Textual slot (S7, injury) — the active E6/E7 rule — avoiding a keyword list:**
Per the task's explicit prohibition on an "arbitrary genericness keyword list," the detection rule here uses **the stored field's own text as the comparison target**, not an externally authored list:
1. Tokenize `injury_limitations` (lowercase, strip stopwords) into a token set `T_profile`.
2. Tokenize each sentence of the plan's free-text notes into `T_sentence`.
3. `detected (E6) = ∃ sentence where |T_profile ∩ T_sentence| ≥ 1` AND that sentence contains a modification verb from a closed, domain-defined (not "genericness") action lexicon fixed in advance by the research design — e.g. {substitute, reduce, avoid, replace, modify, swap, lower-impact} — used only to confirm an *action* is present, not to judge whether the language is "generic." This lexicon is about detecting *the presence of a prescribed modification*, structurally different from a genericness filter: it is checking for an instruction, not scoring prose quality.
4. `specific (E7) = detected(E6)` AND the overlapping token(s) are **not** limited to domain-generic running terms (run, pace, week, mile) — i.e., at least one overlapping token is specific to the *stored condition* itself (e.g. "knee", "shin", "achilles" — drawn from what the runner actually typed, never from an externally authored list).

This keeps the check anchored to *that runner's own stored text*, satisfying "no arbitrary genericness keyword list" while still being deterministic and reproducible.

---

## 7. Contradiction Rules

A slot is marked **CONTRADICTED** (a stricter, separate flag from "not detected") when the plan's value is present but inconsistent with the stored fact. As in §6, the S1–S4/S5/S6 rules below are **retired** (kept for traceability only — these are now subsumed by E1–E4's own violation checks, `EVALUATION_CRITERIA_OPTION_A_DESIGN.md` §4); **only the S7 rule is active for E6/E7**:

- **RETIRED — previously S1–S4, S6:** `contradicted = detected_value_exists AND |plan_value − expected_value| > contradiction_threshold`. Now covered by E1/E2's own violation definitions.
- **RETIRED — previously S5:** `contradicted = a training day is scheduled on a day NOT in preferred_days`. Now covered by E3's own violation definition.
- **S7 (active):** `contradicted = the plan text recommends an action on record as unsafe given the stored limitation` — this is the one slot where a closed, pre-registered mapping (e.g. "high-impact plyometrics" flagged against a stored "stress fracture") is unavoidable, and must be scoped narrowly and listed explicitly in the study's codebook, reviewed by the advisor, not invented ad hoc by the evaluator at run time.

Contradiction is reported separately from the E6 coverage ratio (it is a safety/quality signal, not a coverage count) to avoid silently folding it into a single composite score, per the task's constraint against composite metrics.

---

## 8. Missing-Evidence Rules

- If `injury_limitations` is null/empty for a given profile, S7 is marked **NOT APPLICABLE** for that profile, not "failed." A NOT APPLICABLE profile is excluded from both the numerator and denominator of E6's coverage ratio for that profile (see §9) — this is why the NOT-APPLICABLE rate must be reported alongside the coverage distribution (`EVALUATION_CRITERIA_OPTION_A_DESIGN.md` §4 E6 item 5/6/11): it determines how much of the 24-profile sample E6/E7 can speak to at all.
- If `injury_limitations` is non-empty but the plan's text contains no corresponding modification/reference at all, S7 is marked **MISSING** — counted in the denominator (applicable), not detected in the numerator. This is different from NOT APPLICABLE and different from CONTRADICTED.
- E7 is only evaluated when S7 is E6-detected; a MISSING or NOT APPLICABLE profile has no E7 value for that generation (reported as blank/NA, never defaulted to zero, to avoid silently penalizing twice).

---

## 9. Applicability Rules

A field is **excluded from E6/E7 entirely, for all 24 profiles** (not merely scored low on some) when it is classified Category B, C, or D in §3:
1. **Category D** (`pb_10k`, `age`, `gender`, `vdot_band`, `stated_preference`) — no traceable field or no definable detection rule.
2. **Category B** (`experience_level`, `target_race_distance`, `target_race_time`, `current_weekly_mileage_km`, `training_days_per_week`/`preferred_days`, `plan_duration_weeks`) — traceable, but constraint-derived; already measured by E1–E5, so scoring them under E6/E7 would double-count rather than add evidence.
3. **Category C** (`easy_run_pace`) — traceable and plausibly independent, but not adopted pending confirmation it is distinct from the baseline's VDOT-derived pace (§14).

Within the one surviving Category-A field (`injury_limitations`), a **per-profile** applicability rule still applies: a profile is excluded from S7's numerator/denominator when the field is null/empty for that specific profile (§8) — this is a per-profile exclusion, not a field-level exclusion, and is the only applicability check E6/E7 still perform at the profile level.

This two-level structure is how the specification satisfies "do not force every profile field into the metric": Category B/C/D fields are never scored for any profile, by construction (field-level exclusion, decided once in §3); Category A's one field is scored for every profile where it has data, and honestly marked NOT APPLICABLE where it does not (profile-level exclusion, §8).

---

## 10. Example Profile → Expected Evidence Mapping

> **Note on scope:** the S1–S6 rows below are retained from the pre-revision version of this document to show *why* those facts are now Category B — each row's "expected evidence" is, on inspection, exactly what E1–E5 already check (see the right-hand annotations added in this revision). **Only the S7 row is live E6/E7 evidence.** A fuller worked example demonstrating E7's independence from E1–E5 end-to-end is in `EVALUATION_CRITERIA_FINAL_CONSISTENCY_REVIEW.md`'s companion report and is reproduced in abbreviated form at the end of this section.

Using the worked example from the task prompt:

```
experience_level = intermediate
preferred_days = [Monday, Wednesday, Saturday]
training_days_per_week = 3
target_race_distance = 5K
target_race_time = 23:00 (sub-23)
current_weekly_mileage_km = 30
injury_limitations = "" (empty)
```

| Slot | Status | What this evidence is now (post-revision) |
|---|---|---|
| ~~S1~~ | Retired from E6/E7 | "Plan's intensity structure matches 'intermediate' band" is E1's own check. |
| ~~S2~~ | Retired from E6/E7 | "A long-run consistent with 5K training" is E1/E3's own check. |
| ~~S3~~ | Retired from E6/E7 | "Pace matches the value derived from 23:00/5K" is E1's own check. |
| ~~S4~~ | Retired from E6/E7 | "Week 1 total within floor/cap of 30 km" is E2's own check. |
| ~~S5~~ | Retired from E6/E7 | "3 days, exactly Mon/Wed/Sat" is E3's own check (the baseline's own day-set is already built from `preferred_days`). |
| ~~S6~~ | Retired from E6/E7 | "Plan has the requested number of weeks" is E3/E5's own check. |
| **S7** | **Active — the only E6/E7 slot** | In this particular example, `injury_limitations = ""`, so S7 is **NOT APPLICABLE** for this profile — E6/E7 report no value for it, not a 0. A second profile with `injury_limitations = "mild left knee pain"` is worked through in full in §11.1 below, including the E6/E7 outcome and a side-by-side of what E1–E5 do and do not see. |

This table is retained specifically to make the point concrete: five of the six retired slots would have reported a value that an E1–E5 reader already has, under a different criterion name, for the identical runner.

---

## 11. Example Positive/Negative Cases

### 11.1 Full worked example — why E7 is not duplicating E2/E3 (added in this revision)

**Profile:** `experience_level = intermediate`; `target_race_distance = 10K`; `target_race_time = 48:00`; `current_weekly_mileage_km = 35`; `training_days_per_week = 4`; `preferred_days = [Mon, Tue, Thu, Sat]`; `plan_duration_weeks = 8`; `injury_limitations = "mild left knee pain, aggravated by downhill running and speed work"`.

**Deterministic baseline:** Week 1 = 35 km across 4 sessions on Mon/Tue/Thu/Sat; Tuesday is the baseline's "quality" day (type label only — the baseline's rule engine does not read `injury_limitations`, so it schedules a generic hill-repeat/speed session on Tuesday regardless of the stored knee note).

**Gemini output (one repetition):** Numerically and structurally identical to the baseline — same 4 sessions, same days, same weekly mileage, same paces. Tuesday's `workout_type` field is still labeled `"quality"`. But Tuesday's `workout_execution` text reads: *"Given your history of left knee discomfort aggravated by downhill running and speed work, today's quality session is a flat tempo effort rather than hill repeats; total volume is unchanged."*

| Criterion | What it sees | Outcome |
|---|---|---|
| E1 (Pace/Intensity) | Pace targets for every session match baseline | Pass — nothing here reveals the substitution, since the *pace* didn't change |
| E2 (Volume) | Day and week distances match baseline exactly | Pass — nothing here reveals the substitution, since *volume* didn't change |
| E3 (Structure) | Day-set, rest/training counts, and **workout-type label** (`"quality"`) all match baseline | Pass — critically, E3's type vocabulary (easy/long/quality/rest) is too coarse to distinguish "hill repeats" from "tempo," both of which are `"quality"`; **the substitution is invisible to E3** |
| E4 (Trajectory) | Weekly volumes match baseline's phase schedule | Pass — unaffected |
| E5 (Validity) | Output parses, required fields non-empty | Pass — unaffected |
| **E6 (Coverage, S7)** | `injury_limitations` is non-empty; Tuesday's text shares token "knee" with the stored field and contains an action verb ("rather than" / substitution framing) | **Hit** — this is the first criterion in the whole framework that registers anything happened on Tuesday beyond "a quality session occurred" |
| **E7 (Specificity, S7)** | The overlapping token ("knee") is condition-specific, not a domain-generic running term | **Specific** |

This demonstrates the required property directly: **E1–E5 all pass this generation identically whether or not the Tuesday substitution happened**, because none of them inspect workout content below the type-label/numeric level. E6/E7 are the only criteria in the framework that detect the substitution at all, and they detect it using a fact (`injury_limitations`) the baseline never touches — which is exactly why they are not a restatement of E2 (volume, unchanged) or E3 (structure/type, unchanged) for this generation.

### 11.2 S7 positive/negative cases (retained from the pre-revision version, still active)

**S7 — E6 positive, E7 positive:** `injury_limitations = "mild left knee pain"`; plan text says "given your knee discomfort, swap Tuesday's hill repeats for a flat tempo run." Overlap token "knee"; action verb "swap" present.

**S7 — E6 positive, E7 negative:** Same profile; plan text says "listen to your body and modify sessions if anything feels off." Action verb present ("modify"), but no token overlap with "knee" — this is exactly the generic/specific distinction E7 is designed to catch, using the runner's own stored text as the bar, not an external keyword list.

**S7 — NOT APPLICABLE:** `injury_limitations = ""` — slot excluded entirely, not scored as a failure.

### 11.3 Retired examples (S1–S6, kept for traceability only — these are now E1–E5 outcomes, not E6/E7)

**~~S5~~ — retired:** "Plan places 3 workouts/week on Mon/Wed/Sat" (or fails to) is now read as an E3 outcome.

**~~S4~~ — retired:** "Week 1 distance = 32 km, within tolerance of the baseline's 30-km-derived value" (or outside it) is now read as an E2 outcome. The prior version of this document's concern about a generic-default/mileage-specific-band overlap producing an E7 false positive (§13) is moot once S4 is removed from E7 — but is retained as a general cautionary note about tolerance-band design for E2 itself.

---

## 12. Automation Feasibility

| Slot | E6/E7 status | Fully automatable? | Notes |
|---|---|---|---|
| ~~S1~~–~~S6~~ | **Retired from E6/E7** (Category B, §3) | Yes, but as E1–E5, not E6/E7 | Each was indeed mechanically automatable (as the pre-revision version of this document correctly found), which is precisely how the overlap with E1–E5 was discovered: an automatable check against "the baseline's own published constants" is, by definition, the same computation E1–E5 already perform. Automatability was never the problem with these slots; independence was. |
| **S7** | **Active — the only E6/E7 slot** | Partially automatable | Tokenization/overlap/action-lexicon check is mechanical, but the pre-registered contradiction mapping (§7) requires one-time manual curation by the research team *before* the study runs — this curation is a fixed codebook, not a per-plan expert judgment, and does not reintroduce "expert evaluation" as a per-sample step. This is the one slot where full automation requires an upfront, disclosed design decision rather than a purely mechanical derivation. |
| `easy_run_pace` | Category C, not adopted | Would be yes, mechanically, if adopted | Blocked on confirming the field is distinct from the VDOT-derived pace (§3, §14), not on automation feasibility. |

**Fields excluded from automation entirely** (because no detection rule can be written without inventing unstated mappings): `pb_10k`, `age`, `gender`, `vdot_band`, `stated_preference` — consistent with §3 and §9.

---

## 13. Threats to Validity

- **Reconstructed-from-docs risk:** Every "implemented" claim in §2 is sourced from documentation describing a separate codebase, not from reading that codebase directly. If the real schema differs (renamed fields, an `injury_limitations` that turns out to *also* feed the rule engine, a `vdot_band` that does in fact exist in code), this entire slot set — now narrowed to one field — must be re-verified against the actual `app/models.py`/`app/schemas.py`/`app/rules/*.py` before implementation. **This risk is now higher-stakes than in the pre-revision version**, precisely because E6/E7 rest on a single slot: if `injury_limitations` turns out to be a rule-engine input after all, E6/E7 would have zero remaining independent slots.
- **Baseline-as-reference, not ground truth:** unchanged in spirit, but now narrower in scope — it applies to E1–E5's tolerances, which are the only criteria still comparing against baseline-derived numeric values. E6/E7 no longer compare against any baseline-derived value at all (by design, §3/§4/§5), so this threat no longer applies to E6/E7 directly.
- **S7's closed action lexicon and contradiction codebook (§6.4, §7)** remain the specification's one residual judgment surface, and are now its *only* residual judgment surface (previously one of several). They are fixed in advance and narrow in scope, but they are still human-authored category lists, not purely data-driven. This is disclosed rather than hidden, and carries more weight now that it is the sole mechanism E6/E7 run on.
- **RESOLVED — S1–S6 double-counting with E1–E4:** the pre-revision version of this document found this for S5 vs. E3 only; `EVALUATION_CRITERIA_FINAL_CONSISTENCY_REVIEW.md` generalized it to S1–S4 and S6, and this revision resolves it by retiring all six slots from E6/E7 (§3–§5), rather than merely disclosing the overlap and keeping the slots.
- **Single-slot construct thinness (new):** With E6/E7 reduced to `injury_limitations`, the "coverage breadth" and "specificity" framing in their names is wider than what is actually measured — both become, in effect, a single conditional binary check per generation (NA / miss / hit-generic / hit-specific), not a graded multi-fact score. This is the direct, disclosed cost of removing the overlapping slots (also stated in `EVALUATION_CRITERIA_OPTION_A_DESIGN.md` §4 E6 item 11 / E7 item 12) and must be stated in the paper's limitations section, not minimized.
- **Sample coverage of the one remaining slot:** E6/E7's informativeness now depends entirely on how many of the 24 profiles have `injury_limitations` populated. The reconciliation document's stratification plan (experience × distance × injury presence) is designed to ensure this is non-trivial, but the exact count is not knowable from this repository's documentation and should be confirmed before data collection, not assumed.
- **Tolerance-band sensitivity — retained for E2, no longer relevant to E7:** All numeric baseline-comparison criteria (E1, E2, E4) still depend on tolerance width. This was previously also a risk for E7's now-retired numeric slots; it is no longer an E7 concern, since E7 has no numeric tolerance test left.

---

## 14. Open Advisor Decisions

1. Confirm `vdot_band` and `stated_preference` either (a) do not exist in the real schema and should be dropped from the slot list permanently, or (b) exist under different names and should be re-added with a corrected detection rule (and, per the baseline-independence screen in §3, would still need to pass Screen 2 before being added to E6/E7, not merely Screen 1).
2. Confirm the alias mapping `goal_distance`/`goal_time` → `target_race_distance`/`target_race_time` is correct (same field, different name across documents) rather than two genuinely distinct concepts. (This mapping now matters chiefly for documentation consistency and for E1/E2's own field references, since both aliased fields are Category B and excluded from E6/E7 regardless of which name is canonical.)
3. Approve or revise the closed action lexicon and contradiction codebook for S7 (§6.4, §7) before any evaluation run — this is the one place a small, disclosed curation step is unavoidable, and it now carries more weight since it is the only mechanism E6/E7 run on.
4. **New — confirm whether `easy_run_pace` is a genuinely distinct stored value from the `pb_5k`/VDOT-derived pace the baseline computes**, by reading the real `app/models.py`/`app/rules/generator.py`. If confirmed distinct for at least some profiles, `easy_run_pace` can be added as a second E6/E7 slot (Category A) using the same template-vs-instance logic as S7, restoring a graded (not purely binary) E6/E7 score. If not confirmed, it remains excluded (Category C → D) and E6/E7 remain scoped to `injury_limitations` alone.
5. Confirm whether `pb_10k`, `age`, and `gender` should remain permanently excluded from E6/E7 (this spec's recommendation, unchanged) or whether the advisor wants a documented rationale added to the paper's Limitations section instead.
6. **New — confirm the single-slot scope of E6/E7 is acceptable to the advisor as the price of removing the E1–E4 overlap.** The alternative — keeping S1–S6 in E6/E7 for a richer-looking score at the cost of construct validity — is explicitly not recommended by this document (§15), but is named here as the decision the advisor is actually being asked to make, not assumed.

---

## 15. Final Recommendation (revised)

**E6 and E7 are sufficiently objective to proceed to implementation, now scoped to the single confirmed baseline-independent slot, S7 (`injury_limitations`).** The detection rule (§6.4) reduces to a mechanical token-overlap-plus-action-verb comparison against the runner's own stored text — no expert rating, no externally authored genericness keyword list, and no reliance on Gemini's self-reported reasoning. This is a deliberately narrower recommendation than the pre-revision version of this document (which recommended 6 of 9 slots): the narrowing is the direct, intended consequence of applying the baseline-independence screen added in §3, not a retreat from automatability (every retired slot was, and remains, mechanically automatable — see §12 — it was never an automation problem).

**`easy_run_pace` is the one slot with a plausible path back to a second E6/E7 slot** (§3, §14 item 4), conditional on confirming it is not simply a restatement of the baseline's VDOT-derived pace. This is the single highest-value open item for restoring a graded, multi-fact E6/E7 score rather than a single binary check.

**S7's specificity test (§6.4) still requires a small, disclosed, pre-registered curation step** (the action lexicon and contradiction codebook) and should be flagged in the paper as a narrow, bounded exception rather than claimed as fully keyword-free from first principles — this is unchanged from the pre-revision recommendation and is now the only such exception in the framework (previously one among several numeric-tolerance decisions, §13).

**Before implementation:** the repository caveat in the preamble must still be resolved — the actual application repository must be located and its schema/rule-engine code read directly — both to confirm `injury_limitations` is genuinely not consumed by the rule engine (the premise this whole revision rests on) and to resolve the `easy_run_pace` question (§14 item 4). Pending that confirmation and the open advisor decisions in §14, this document should be treated as a proposal, not a finalized methodology.

---

## Required Final Table (revised)

| Slot ID | Profile Fact | Class | E6 Coverage Rule | E7 Specificity Rule | Automatically Detectable? | Evidence Source | Main Risk |
|---|---|---|---|---|---|---|---|
| ~~S1~~ | `experience_level` | **B — excluded from E6/E7** | *(retired — now E1's own check)* | *(retired — now E1's own check)* | Yes, as E1 | Baseline constant table | Already measured by E1; scoring again under E6/E7 would double-count |
| ~~S2~~ | `target_race_distance` | **B — excluded from E6/E7** | *(retired — now E1/E3's own check)* | *(retired — now E1/E3's own check)* | Yes, as E1/E3 | Structured plan workout list | Same as above |
| ~~S3~~ | `target_race_time` | **B — excluded from E6/E7** | *(retired — now E1's own check)* | *(retired — now E1's own check)* | Yes, as E1 | Structured pace field | Same as above |
| ~~S4~~ | `current_weekly_mileage_km` | **B — excluded from E6/E7** | *(retired — now E2's own check)* | *(retired — now E2's own check)* | Yes, as E2 | Sum of per-day distances, Week 1 | Same as above |
| ~~S5~~ | `training_days_per_week` + `preferred_days` | **B — excluded from E6/E7** | *(retired — now E3's own check)* | *(retired — now E3's own check)* | Yes, as E3 | Per-week day assignment | Same as above |
| ~~S6~~ | `plan_duration_weeks` | **B — excluded from E6/E7** | *(retired — now E3/E5's own check)* | *(retired — excluded from E7 even before this revision)* | Yes, as E3/E5 | Count of week-blocks | Same as above |
| **S7** | `injury_limitations` | **A — the only active E6/E7 slot** | Plan text contains a specific, action-verbed modification addressing a token from the stored text (if non-empty) | Overlap token is condition-specific, not a generic running term | Partially | Free-text scan + pre-registered action lexicon | Requires a small, disclosed curation step (lexicon + contradiction codebook); E6/E7 now depend entirely on this one slot |
| — | `easy_run_pace` | **C — not adopted** | *(would mirror S7's logic if adopted)* | *(would mirror S7's logic if adopted)* | Yes, if adopted | Structured/prompt pace field | Not confirmed distinct from the baseline's VDOT-derived pace — adopting it unconfirmed risks reintroducing the E1-overlap problem |
| — | `pb_10k`, `age`, `gender`, `vdot_band`, `stated_preference` | **D — excluded** | **Excluded from E6/E7** | **Excluded from E6/E7** | N/A | N/A | No traceable detection rule without inventing an unstated mapping |
