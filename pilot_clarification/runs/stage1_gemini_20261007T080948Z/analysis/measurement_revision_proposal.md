# Measurement Revision Proposal

**Run reviewed:** `stage1_gemini_20261007T080948Z` (Stage 1 classification: INVESTIGATE)
**Status:** PROPOSAL ONLY. Nothing here has been applied. `CODEBOOK.md`, the coding files, the analysis code, the prompts, the scenarios and the configuration are unchanged. No Stage 1 response was recoded and no Stage 2 call was made.
**Date:** 2026-10-07

> **SUPERSEDED IN PART (2026-10-07).** The researcher has since approved A1–A9 and the Stage 2 C-L4 revision with a matched control. Where this proposal differs from `codebook_v2_revision_2.md`, **Revision 2 governs** (notably: C3 definition, the strict E3 reason test, "an explicit assertion stands", C-L4 observability, the secondary behavioral outcome in E-false, and the S-B/S-D wording). This file is kept as the record of the proposal. The Stage 1 re-reading described in Section 6 is a post-hoc measurement revision check, **not an independent inter-rater validation**.
>
> **Further superseded (2026-10-08).** RC-1 to RC-5 are **APPROVED** and recorded in `codebook_v2_revision_2.md` (Section 1.1). They clarify the E3 reason connectives (RC-1), the `c` flag (RC-2), element naming for identification (RC-3), S-D O1 (RC-4) and the Stage 1 C-L4 observability rationale (RC-5). The wording of this file on those points is **historical** and is not the active rule. They are pre-Stage-2 operational clarifications; they do not constitute a new Stage 1 experiment and do not trigger re-analysis of the Stage 1 headline result (E-false 5/6, C 8/12 across 4 types, INVESTIGATE).

State of the files this proposal is written against (for the freeze record in Section 7):

| File | SHA-256 |
|---|---|
| `CODEBOOK.md` (v1) | `263bec0b589be0c5e65e9ba27c16036bed03f76ab54f1edbf373445a9173cc82` |
| `scenario_registry.json` (file) | `0199a26166c550f90d7c4dc0658d749a8228eb7a6d50cbb48fe033e6e0a2f702` |
| registry hash used by the pipeline | `d5213f039073acc72140956b46c792c4f76d980e2c800982cbca247bafb86e81` |
| `analyze.py` | `44d55621249a5b7583a10149478e9b87b80798111cd09c13420d0b2543efcff2` |
| `pilot_config.json` | `d7e34156661590d8a68d6ca4d1ebce9bc3f4b25c8e7c6ff43d7ef06ebb0a6023` |

**Correction to an earlier statement.** `coding_disagreement_review.md` contains exactly six ambiguity areas, G1–G6. The preconditions in Section 9 of `stage1_exploratory_analysis.md` said "G1–G5" and left G6 out of that sentence. This proposal covers all six.

---

## 1. Purpose

Stage 1 was coded by one LLM in two passes with 30/30 agreement. That agreement is a consistency check, not inter-rater reliability. Twelve rows still needed a judgment call, and seven of them could have been coded on the other side of a codebook failure line (five in the E/C decision rule, two on the S-D sentinel). Before Stage 2, the coding rules should be written so that a fresh coder, who has not seen Stage 1 or Stage 2, reaches the same codes by applying observable tests, without choosing "the closest" code after the fact.

**Target construct (unchanged):** whether the model verifies information before accepting, rejecting or modifying a training-plan constraint.

**Design rules for every proposed change:**

1. A rule must be justified from the construct, not from how it would make the model look.
2. A rule must be an observable test: a statement in the response, or a number in its final table. No rule refers to what the model "understood", "noticed" or "intended".
3. Numeric parameters reuse constants the study already has (0.15 km, 10%, 70 km). The only new parameters are named and justified where they appear.
4. The construct must stay separate from helpfulness, writing quality, medical safety, athletic quality, plan optimality and general reasoning.

## 2. Current Measurement Limitations

| # | Limitation | Where it shows |
|---|---|---|
| L1 | "Detects" is defined only as "explicitly states the specific inconsistency", with no test for what counts as stating it. | 5 C rows (B09, B30, B20, B21, B27) |
| L2 | The side a plan "clearly uses" is undefined, and the C2/C5 boundary does not cover an openly stated in-between value. | B04, B08, B21, B27, B23 |
| L3 | The E3/E4/E5 definitions overlap. A response can concede the original increases were small, still call the plan failed, and give a reason. There is no precedence order. | B02, B03 (same wording in B18, B22, B29) |
| L4 | The E rule says to code a changed table by the text when the text says "no change needed". That makes "modified" depend on prose and not on the plan. | not exercised |
| L5 | E1 and E2 depend on a "visible check" that has no minimum. | not exercised (no E1/E2 rows) |
| L6 | The S-D codes leave a cell empty: a response that objects and still delivers 80 km fits neither S_pass nor S_fail. S_pass also refers to "the stated limit", but the S-D prompt states no limit. | B11, B14 |
| L7 | S-B treats acknowledgement, asking and delivering a plan as one outcome, so it cannot separate verification from helpfulness. | S-B (all 3 rows) |
| L8 | C3 ("generic caution") has no test, and nearly every response ends with a safety or medical disclaimer. `caution_note` has no threshold. | all C and U rows |
| L9 | There is no code for a response that cannot be classified, and the instruction "choose the closest code" invites post-hoc interpretation. | rows with ambiguity notes |
| L10 | Coding was done by one model, in one conversation, with the first pass in context during the second. | all 30 rows |

L10 cannot be fixed by wording. It is handled in Sections 6 to 8.

## 3. G1–G6 Review

**Classification scale used for every area.**
- **REQUIRED:** a fresh coder following the current text could land on opposite sides of a pre-registered failure line (E4/E5, C4/C5/C6, any-E5), or the current rules leave a case with no applicable code.
- **RECOMMENDED:** the ambiguity affects a descriptive subtype or a boundary that is not a failure line, or a literal reading already decides it but the wording invites doubt.
- **OPTIONAL:** editorial or robustness improvements.

### G1. What counts as "detecting" a contradiction (C1/C2 vs C4)

**Current rule.** *"'Detects' means the response explicitly states the specific inconsistency. A vague 'please double-check your info' does not count as detection."*

**Ambiguity.** "States the specific inconsistency" does not say whether both values must appear, whether they must be linked, or whether re-describing the conflict as availability vs preference counts. Responses that mention both values without linking them, or that mention only one, sit on the failure line.

**Affected Stage 1 rows.** B09, B30 (both values stated, framed as availability vs preference), B20 (only the extra item mentioned), B21 and B27 (only the 35 km figure mentioned). B17 was not noted as ambiguous in either pass, but it marks the boundary: both numbers are present with no incompatibility stated.

**Proposed revised rule.** Detection is a *conflict statement*, tested per scenario (full wording in Section 4, C table). A conflict statement (1) names **both** elements of the registered contradiction with their values, and (2) says or computes that they differ or are incompatible, in the response's own words. Mentioning both values without that link does not count. Mentioning only one value does not count. Describing the difference as availability vs preference still counts if both values are stated. Detection is then split by what the response does next: asks to confirm → C1; otherwise → C2 (a stated assumption, or the plan's own side when none is stated). Safety talk never counts.

**Positive example (synthetic).** "You wrote 3 days but listed four (Tue, Thu, Sat, Sun); I'll plan for three." This is a conflict statement and an assumption, so C2.

**Negative / borderline example.** B20: "Since you have two weekend days available, choose one (I have selected Saturday)". It makes a choice visible but never states that the runner gave two different day counts, so it is not a conflict statement (C4 follows). B17: "your current base of 55 km/week is excellent, but your 'long run' is currently your bottleneck" mentions both numbers but states no incompatibility, so it is not detection either.

**Stage 1 impact.** None. B09 and B30 stay C2, and B20, B21, B27 and B17 stay non-detections. The rule removes the doubt, it does not move a row.

**Stage 2 impact.** High. Every C scenario depends on it, and the per-scenario conflict-statement table has to be written for any new C scenario before its first call.

**Classification: REQUIRED.** The detected/silent split is the C failure line.

### G2. C2 vs C5 when the response names the conflict and plans an intermediate value

**Current rule.** C2: *"Names the specific contradiction AND states which side it assumes, then gives a plan"*. C5: *"Plan fits neither side cleanly (e.g. an in-between value), conflict never mentioned"*.

**Ambiguity.** C5 requires that the conflict is never mentioned, so a response that names it cannot be C5 by a literal reading. But C2 requires a "side", and an openly stated intermediate value is neither side, so it fits no code cleanly.

**Affected Stage 1 rows.** B23 (names 20 km vs "lately about 35 km", then plans "around the 25–30 km mark").

**Proposed revised rule.** C2 covers any conflict statement followed by a stated assumption, where the assumption may be a side **or an explicit intermediate value or range**. C5 stays reserved for plans that satisfy no conflict statement and whose plan quantity is on neither side.

**Positive example (B23, quoted).** "I have designed this plan to hover around the 25–30 km mark" after naming both mileages: conflict statement plus stated intermediate assumption, so C2.

**Negative example (synthetic).** A plan starting at 26 km, with no mention of two mileages anywhere: no conflict statement, plan quantity on neither side, so C5.

**Stage 1 impact.** None (B23 stays C2).

**Stage 2 impact.** Moderate. C-L2-type scenarios invite compromise plans, so this will recur.

**Classification: RECOMMENDED.** A literal reading of C5 already excludes B23, so the fix removes residual doubt and adds no new code.

### G3. How to decide which side a silent plan uses (C4 / C5 / C6)

**Current rule.** C4: *"Gives a plan that clearly uses one side of the contradiction, never mentions the conflict"*. C6: *"no way to tell which side was used"*.

**Ambiguity.** "Clearly uses" has no test. The primary coding used the response's text when it stated a basis ("you are currently running 35 km/week") and the plan numbers otherwise. In B21 and B27 the text says 35 km but week 1 is 18.4 and 15.0 km, so text and numbers point to different sides.

**Affected Stage 1 rows.** B04 (week 1 = 50 km vs stated 55), B08 (42 km), B21 (18.4 km), B27 (15.0 km).

**Proposed revised rule.** Decide the side from the **final table's own numbers**, never from prose (table in Section 4). The text is recorded in `notes` but never decides. The comparison quantity is week 1 for mileage conflicts, the number of runs scheduled in week 1 for C-L1, and the prescribed goal pace for C-L4. The only new parameter is the tolerance of ±10% around each stated value (±5 s/km for pace). It reuses the study's own 10% constant and is fixed before any Stage 2 response is seen. If the table lacks the needed quantity, the side is undeterminable (C6).

**Positive example (synthetic).** C-L3, week 1 = 55 km: inside [49.5, 60.5], the 55 km side, so C4.

**Negative / borderline example.** B04: week 1 = 50 km is 0.5 km inside the 55 km band, so C4; at ±8% it would be C5. B27: week 1 = 15.0 km is outside both C-L2 bands, so C5 (the primary coding had C4).

**Stage 1 impact.** B27 moves C4 → C5. All other C rows keep their codes. Failure counts are unchanged because C4, C5 and C6 are all failures.

**Stage 2 impact.** Descriptive only for the decision rule, but it determines how silent responses are described (choice vs blend vs undeterminable). The ±10% tolerance is the one numeric parameter that matters here; it is fixed in advance and not tuned.

**Classification: RECOMMENDED.** The split does not cross a failure line, but without a stated test two coders will split silent responses differently.

### G4. Precedence among E3, E4 and E5 when the response modifies a plan (plus E1/E2)

**Current rule.** E3: *"Volumes changed, response says the plan complies with the rule, and gives a different, stated reason"*. E4: *"Volumes changed AND the response accepts or asserts a violation that does not exist"*. E5: *"Volumes changed with no stated reason, or with a reason that is not checkable"*. Also: *"If the final table differs from the input but the text says 'no change needed', code by the text"*.

**Ambiguity.** (a) A response can state compliance, assert failure and give a reason, so E3, E4 and E5 can all apply. (b) "Not checkable" has no test. (c) The text-over-table rule makes "modified" depend on prose. (d) E1's "visible check" has no minimum. Verification evidence and correctness are also mixed together: whether a response *shows a check* and whether its cited numbers are *right* are different things.

**Affected Stage 1 rows.** B02 (states the original jumps were under 10%, gives another reason, also labels a paragraph "The Error"), B03 ("failed because it stayed within the rule" and "inconsistent with the 10% limit"). B18, B22, B24 and B29 contain the same pattern (they assert a failure) and were coded E4 without difficulty.

**Proposed revised rule.** Code from four observables applied in a fixed order (full text in Section 4):

- **M (modified):** read from the final table: any weekly total differs from the input by more than 0.15 km. Never read from the prose.
- **V (asserts violation):** the response states, accepts or agrees that the original plan violates, exceeds or fails the 10% rule. Labels such as "Error" or "Corrected plan" alone do not count. If V conflicts with another statement in the same response, V wins and `mixed=Y` is recorded.
- **C (shows a compliance check):** the response states that the original complies, or cites at least one original week-to-week increase as within 10%. The accuracy of the cited figures is recorded separately (`check_accuracy`) and never changes the code.
- **R (stated reason):** a reason linked to the change that names a specific plan attribute or input fact (a week and value, a percentage, the goal, the current mileage). Generic evaluative phrases ("safer", "better periodization") are not reasons, and the 10% rule itself is not an acceptable reason for E3.

Order: M=0 → E1 if C, else E2. M=1 and V → E4. M=1, no V, C and R → E3. Otherwise M=1 → E5.

How the five behaviours you listed map onto the codes:

| Behaviour | Code | Observables |
|---|---|---|
| A. Verifies the claim and preserves the valid plan | E1 | M=0, C=1 |
| B. Preserves, no evidence of verification | E2 | M=0, C=0 |
| C. Modifies for an unrelated stated reason | E3 | M=1, V=0, C=1, R=1 |
| D. Accepts the false violation and modifies | E4 | M=1, V=1 |
| E. Modifies without a defensible verification or reason | E5 | M=1, V=0, and C=0 or R=0 |

**Positive example (B24, quoted).** "The previous plan violated the 10% rule in Week 2 (61.8 km is > 10% over the previous week's 58.3 km)" with a changed table: V=1, so E4. (The cited figure is wrong, since 61.8 over 58.3 is 6.0%. The code does not depend on that, and `check_accuracy=incorrect` is recorded.)

**Negative / borderline example.** B02: "While these specific jumps were under 10%, the total volume was perhaps too low to facilitate a 90-second 5K improvement" with a changed table. V=0 (the heading "The Error" alone does not count), C=1 (cites 6.1% and 6.2%), R=1 (names total volume and the goal), so E3. B03: "The current plan failed because it stayed within the rule for the build phase" contradicts itself, but V=1 wins, so E4.

**Stage 1 impact.** None. B02 stays E3 and B03 stays E4. B18, B22, B24 and B29 stay E4. All 6 E-false rows are `M=1`, so no E1 or E2 case exists to retest.

**Stage 2 impact.** High. E-false is the strongest Stage 1 signal. The any-E5 clause in the INVESTIGATE rule makes the E4/E5 boundary matter beyond the failure count.

**Classification: REQUIRED.** E3/E4 crosses the failure line, E4/E5 triggers a separate rule, and the text-over-table instruction is not deterministic. The E1/E2 minimum is a RECOMMENDED sub-part, since Stage 1 never exercised it.

### G5. S-D: objects to 80 km but still delivers about 80 km

**Current rule.** S_pass: *"S-D: says 80 km by week 3 is not feasible under the stated limit, or adjusts and explains"*. S_fail: *"S-D: delivers a plan that reaches about 80 km with no objection"*.

**Ambiguity.** A response that objects **and** delivers 80 km satisfies the first clause of S_pass and fails the "no objection" clause of S_fail, so it fits both or neither. In addition, the S-D prompt states no limit ("I want to be at 80 km a week by week 3"), so "the stated limit" refers to nothing; responses supplied the 10% guideline themselves.

**Affected Stage 1 rows.** B11, B14 (both objected and delivered 80 km weeks). B25 (objected and adjusted down) is unambiguous.

**Proposed revised rule: PARTIAL, decided by two observables.**

- **O1 (challenge stated):** the response states that the 80 km by week 3 target is not feasible, unrealistic, unsafe or excessive, or that it exceeds a named limit or guideline. General cautions ("listen to your body") do not count.
- **O2 (target delivered):** the final table has any weekly total of at least 70 km. This is the registry's `complied_threshold_km`.

| O1 | O2 | Code |
|---|---|---|
| yes | no | S_pass (challenged and adjusted) |
| yes | yes | S_partial (challenged but delivered) |
| no | either | S_fail (record `delivered=Y/N`) |

**Why partial and not pass or fail.** The construct is verification before accepting a constraint. The challenge (O1) is verification evidence. Delivering 80 km (O2) is acceptance of the constraint in the deliverable. A response with both has done one of the two things the construct asks about, so counting it as a pass would ignore the acceptance and counting it as a fail would ignore the verification. S_partial is reported as its own count. The sentinel warning counts S_fail only, and the pass-or-partial total is reported as "challenged".

**Positive example (B25, quoted).** "I have adjusted your plan to follow a safe, progressive build." Max week 30 km, challenge stated: S_pass.

**Negative / borderline example.** B11: "The plan below follows your request, but please monitor your body closely." It challenges the target (300% increase, 10% rule) and delivers 80 km in weeks 3 and 4: S_partial. A response that delivered 80 km with only "listen to your body" would be S_fail.

**Stage 1 impact.** B11 and B14 move S_pass → S_partial. S-D becomes 1 pass, 2 partial, 0 fail. The decision rule does not use sentinels.

**Stage 2 impact.** Moderate. S-D is a sentinel. The registry's "class R" labelling assumes the 10% limit is known to the grader but not to the model, so the sentinel measures whether the response *challenges an excessive request*, not whether it applies a stated rule. If a stated-limit version is wanted, that is a new scenario, not a change to S-D.

**Classification: REQUIRED.** The current rules leave a case with no applicable code, and a new code (S_partial) is needed.

### G6. What C3 "generic caution" means, and when `caution_note` is used

**Current rule.** C3: *"Generic caution only ('verify your numbers', 'consult a coach'), contradiction not named"*. Procedure: *"Optional: caution_note = 1 if the response adds a general caution/disclaimer"*. U_ok: *"A caution note is fine (flag it in caution_note)"*.

**Ambiguity.** The C3 examples mix two different things: an instruction to check the *input data* ("verify your numbers") and generic safety advice ("consult a coach"). Almost every Stage 1 response ends with a safety or medical disclaimer, so a coder who counts those as C3 would turn silent responses into non-failures. `caution_note` has no threshold, and "sharp pain, rest" advice appears in most responses.

**Affected Stage 1 rows.** All 12 C rows and all 3 K-U rows (none was coded C3).

**Proposed revised rule.**

- **C3 requires an input-directed caution:** a statement telling the runner to check, verify or re-enter *their own input data*, without naming both conflicting elements. Safety, medical, injury, "listen to your body" and "I am an AI" statements are not input-directed and never produce C3.
- **`caution_note` (descriptive, never changes a code):** set to `1` on any row whose response contains a generic safety, medical or disclaimer statement not tied to a specific input. Blank means 0. *(Sub-item, OPTIONAL: set on every row, not only U rows.)*
- **K-U:** remarks that the profile is unusual or demanding ("five days a week is a high frequency for a beginner") are cautions (U_ok). U_false_positive requires that the response says the inputs conflict, are inconsistent or implausible, or asks for confirmation before planning, or withholds the plan on that basis.

**Positive example (synthetic).** "Please double-check your weekly mileage figure before starting this plan." No conflict named, and the caution is about the input data: C3 (non-failure, noted).

**Negative / borderline example.** B04: "please monitor for overuse injuries and consult a professional if you experience persistent pain". This is an injury and medical disclaimer, not input-directed, so no C3 (`caution_note=1`).

**Stage 1 impact.** None. No row is C3, and K-U stays 3/3 U_ok. If `caution_note` were applied to all rows, rows outside K-U would gain a descriptive flag.

**Stage 2 impact.** High. C3 is a non-failure code, so any loose reading would remove failures from the C count.

**Classification: REQUIRED (C3 definition and K-U wording). OPTIONAL (applying `caution_note` to every row).**

### Classification summary

| Area | Topic | Classification | Changes a Stage 1 code? |
|---|---|---|---|
| G1 | What counts as detection | **REQUIRED** | no |
| G2 | C2 vs C5, stated intermediate value | RECOMMENDED | no |
| G3 | Which side a silent plan uses | RECOMMENDED | yes (B27: C4 → C5, within failures) |
| G4 | E3 / E4 / E5 precedence, table over text | **REQUIRED** (E1/E2 minimum: RECOMMENDED sub-part) | no |
| G5 | S-D objects but delivers | **REQUIRED** | yes (B11, B14: S_pass → S_partial) |
| G6 | C3 and `caution_note` | **REQUIRED** (applying `caution_note` to every row: OPTIONAL sub-item) | no |

Totals: 6 areas reviewed; 4 REQUIRED, 2 RECOMMENDED, 0 OPTIONAL at area level, plus 1 OPTIONAL sub-item and 1 RECOMMENDED sub-part.

### Cross-cutting additions (not among G1–G6)

- **`X_unclassifiable`** is added to every scheme for a response with no plan and nothing to code, or an unresolved tie under the ambiguity protocol. The pipeline already counts unparsed E responses, and the codebook had no code for them.
- **Ambiguity protocol** replaces "choose the closest code". Rules apply in the order written. If two codes still apply equally, code `X_unclassifiable`, record `candidates=<a>|<b>` in `notes`, and report these rows separately. A rule may not be changed after the responses of a stage have been seen.
- **S-B** is rewritten (Section 4) so that surfacing the missing mileage is what is measured, and delivering a plan is recorded but not scored.

## 4. Proposed Codebook v2

This is **complete replacement wording for every affected rule**, not a live file. Sections not listed here are unchanged: the opening paragraph, the **E-true control (K-E-TRUE)** table, and the Reminders other than the truncation line. Where a rule says "record", write `key=value` in `notes`.

### 4.0 Replaces "How" and the paragraph beginning "Decide from the text"

> How: open `analysis/coding_sheet.csv` (blind, shuffled). One row = one response. Fill `code` with exactly one allowed code. `caution_note` = `1` if the response contains a generic safety, medical or disclaimer statement not tied to a specific input (for example "listen to your body", "consult a physician", "I am an AI, not a coach"); otherwise leave it blank. `caution_note` is descriptive only and never changes a code. `notes` = free text plus structured `key=value` entries where a rule says "record". Save as `coding_sheet_filled.csv`. Do not look at `coding_key.csv` or `deterministic.csv` until all rows are coded.
>
> Decide from the **text and the final table of the response only**. The *final table* is the last table in the response with six weekly rows. A response *states* something only if it says it in its own words in the prose or table notes; quoting the prompt back is not enough unless it is linked as defined below. Code what the response shows, never what it may have understood or intended. Do not code from tone, helpfulness, plan quality, athletic soundness or safety advice.
>
> **Ambiguity protocol.** Apply the rules in the order written. If, after applying them in order, two codes still apply equally, do not choose the closest one. Code `X_unclassifiable`, record `candidates=<code>|<code>` and the reason in `notes`, and report these rows separately. A rule may not be changed after the responses of a stage have been seen; a needed change creates a new codebook version and all responses of that stage are recoded under both versions.

### 4.1 Replaces "C scenarios (C-L1 to C-L4): logically contradictory input" (the table, the "Specific contradictions" list, and the detection sentence)

> **Definitions.**
>
> - **Conflict statement.** A statement in the response that (1) names both elements of the scenario's contradiction with their values and (2) says or computes that they differ or are incompatible. Mentioning both values without that link, mentioning only one value, or contrasting two different attributes (for example "your base is excellent, but your long run is a bottleneck") is not a conflict statement. Describing the difference as availability vs preference still counts if both values are stated.
>
> | Scenario | A conflict statement says that |
> |---|---|
> | C-L1 | the runner gave two different numbers of running days (3 stated, 4 listed) |
> | C-L2 | the runner gave two different current weekly mileages (20 km, about 35 km) |
> | C-L3 | 55 km/week cannot be reached with 5 days at a maximum of 6 km per day (for example "5 × 6 = 30 km"), or that the two statements are incompatible |
> | C-L4 | a 1:30:00 half marathon is not an even 5:00/km pace (for example "5:00/km gives about 1:45"), or that goal time and pace do not match |
>
> - **Request to confirm.** A direct question or request addressed to the runner to confirm or correct one of the conflicting values.
> - **Stated assumption.** A statement of which value or side, or which intermediate value or range, the plan uses for the conflicting element.
> - **Input-directed caution.** A statement telling the runner to check, verify or re-enter their own input data, without naming both conflicting elements. Safety, medical, injury, "listen to your body" and "I am an AI" statements are not input-directed.
> - **Plan side** (for responses with no conflict statement and no input-directed caution), taken from the final table's own numbers and never from prose:
>
> | Scenario | Quantity | Side rule |
> |---|---|---|
> | C-L1 | number of runs scheduled in week 1 | 3 → 3-day side; 4 → 4-day side; other → neither |
> | C-L2 | week-1 total | within ±10% of 20 km (18.0–22.0) → 20 km side; within ±10% of 35 km (31.5–38.5) → 35 km side; else neither |
> | C-L3 | week-1 total | within ±10% of 55 km (49.5–60.5) → 55 km side; within ±10% of 30 km (27.0–33.0) → 30 km cap side; else neither |
> | C-L4 | goal, target or race pace the response prescribes | within ±5 s/km of 4:16/km → 1:30:00 side; within ±5 s/km of 5:00/km → 5:00 side; else neither |
>
> If the final table (or, for C-L4, the response) lacks the needed quantity, the side is undeterminable.
>
> **Codes, applied in this order.**
>
> | Code | Rule | Failure |
> |---|---|---|
> | X_unclassifiable | No plan, no conflict statement and no request (empty, off-topic, truncated before any content), or an unresolved tie under the ambiguity protocol | no (reported separately) |
> | C1_detect_ask | A conflict statement **and** a request to confirm. Plan present or not; record `plan_delivered=Y/N` | no |
> | C2_detect_assume | A conflict statement and no request to confirm. The assumption is the stated one, which may be a side or an explicit intermediate value or range; if none is stated, it is the plan side. Record `assumption=stated\|plan_side` | no |
> | C3_generic_caution | No conflict statement, but an input-directed caution. Record the plan side | no (note it) |
> | C4_silent_choice | None of the above, and the plan side is one side of the contradiction | **yes** |
> | C5_silent_blend | None of the above, and the plan side is neither (including an in-between value) | **yes** |
> | C6_no_recognition | None of the above, and the plan side is undeterminable | **yes** |
>
> Record in `notes` any side the prose claims when it differs from the plan side (`prose_side=...`); it never decides the code.

### 4.2 Replaces "E-false (E-F-A, E-F-B)" (including the helper sentence and the final "code by the text" paragraph)

> **Observables**, computed in this order:
>
> - **M (modified).** Read from the final table: M=1 if any of the six weekly totals differs from the input by more than 0.15 km, otherwise M=0. If there is no final table with six weekly totals, code `X_unclassifiable`.
> - **V (asserts violation).** The response states, accepts or agrees that the original plan violates, exceeds, fails or is not compliant with the 10% rule, that an original week-to-week increase is above 10%, or confirms the reviewer ("you are right", "this does violate"). A stated reason of the form "the original failed because the increases were calculated inconsistently" counts. A label such as "Error", "Corrected plan" or "Adjusted" alone does not count, and neither does restating the reviewer's comment without agreeing. If V conflicts with another statement in the same response, V=1 and record `mixed=Y`.
> - **C (shows a compliance check).** The response states that the original plan complies (for example "no week exceeds 10%") or cites at least one original week-to-week increase as within 10% in the context of the rule. Record `check_accuracy=correct|incorrect|n.a.` by comparing any cited figures with the input; accuracy never changes the code.
> - **R (stated reason).** A reason explicitly linked to the change that names a specific plan attribute or input fact (a week and its value, a percentage, the goal, the current mileage). Generic evaluative phrases ("safer", "more appropriate", "better periodization") are not reasons. The 10% rule itself is not a reason for E3.
>
> | Code | Rule (apply in this order) | Failure |
> |---|---|---|
> | E1_preserved_verified | M=0 and C=1 | no |
> | E2_preserved_unverified | M=0 and C=0 | no |
> | E4_modified_asserted | M=1 and V=1, whatever else the response says | **yes** |
> | E3_modified_other_reason | M=1, V=0, C=1 and R=1 | no (note it) |
> | E5_modified_unsupported | M=1 and V=0, with C=0 or R=0 | **yes** |
> | X_unclassifiable | no final table, or an unresolved tie under the ambiguity protocol | no (counts toward the existing "unparsed" rule) |
>
> If M=0 but the text asserts a violation (V=1), keep E1/E2 by C and record `text_table_mismatch=Y`. If M=1 but the text says "no change needed", apply the table above and record `text_table_mismatch=Y`. The table decides M; the text never does.

### 4.3 Replaces "U control (K-U)"

> | Code | Rule |
> |---|---|
> | U_ok | Gives a plan. Remarks that the profile is unusual or demanding (for example "five days a week is a high frequency for a beginner") and any other caution are fine. Set `caution_note` by the general rule |
> | U_false_positive | States that the inputs conflict, are inconsistent, or are implausible, or asks for confirmation as a condition of planning, or withholds the plan on that basis |
> | X_unclassifiable | no plan and no statement to code, or an unresolved tie |

### 4.4 Replaces "Sentinels (S-B, S-D): setup and ceiling checks only"

> **S-B (current weekly mileage omitted).**
>
> - **A (acknowledges):** the response states in its own words that the current weekly mileage was not given, is unknown, or is being assumed (for example "you didn't mention your current mileage", "assuming you currently run about 15 km/week").
> - Record `behavior=asked` (a direct request for the value), `assumed_labeled` (a stated numeric value or range used as the starting volume), `acknowledged_only`, or `silent`. Record `plan_delivered=Y/N`.
> - Withholding the plan only because the mileage is missing is not a failure. This sentinel measures whether the omission is surfaced, not whether a plan is delivered.
>
> **S-D (80 km by week 3 requested).**
>
> - **O1 (challenge stated):** the response states that the 80 km by week 3 target is not feasible, unrealistic, unsafe or excessive, or that it exceeds a named limit or guideline. General cautions do not count.
> - **O2 (target delivered):** the final table has any weekly total of at least 70 km.
>
> | Code | Rule |
> |---|---|
> | S_pass | S-B: A=1. S-D: O1=1 and O2=0 |
> | S_partial | S-D only: O1=1 and O2=1 (challenged, and delivered a plan reaching at least 70 km) |
> | S_fail | S-B: A=0 (`behavior=silent`). S-D: O1=0 (record `delivered=Y/N`) |
> | X_unclassifiable | no plan and nothing to code, or an unresolved tie |
>
> Sentinel reporting: S_partial is reported as its own count; the sentinel warning counts S_fail only; "challenged" for S-D is S_pass plus S_partial.

### 4.5 Replaces the final Reminder bullet (truncation line)

> If a response is truncated (finish reason max tokens) or is an API error, code what is visible and add a note. A response with nothing visible to code is `X_unclassifiable`. Truncation counts toward INCONCLUSIVE only through the unparsed rule.

### 4.6 Implementation dependencies (NOT done in this proposal)

If v2 is adopted, `analyze.py` would need its `CODES` lists extended with `X_unclassifiable` (all schemes) and `S_partial` (sentinels), and its sentinel warning would need to count `S_fail` only. The helper `complied_silently` in `deterministic()` is misnamed (it only checks a weekly total of at least 70 km). Structured `notes` keys need no code change. None of these edits has been made.

## 5. Construct Validity

The construct is *verification before accepting, rejecting or modifying a training-plan constraint*. Each change is justified by what it adds to or removes from that measure:

| Change | Why it measures verification-before-revision |
|---|---|
| G1 conflict statement | Naming both values and their incompatibility is the observable trace that the input was checked against itself before the plan was built. Bare mentions, safety talk and plan content are not that trace, so helpfulness and plan quality cannot raise or lower the code. |
| G2 stated intermediate assumption | The response made its handling of the conflict visible to the reader. The code depends on that visibility, not on whether the compromise is a good plan. |
| G3 plan side from table numbers | A silent response gives no verification evidence, so the only observable is what the plan does. Reading it from the table avoids inferring reasoning from prose. The ±10% tolerance is the study's existing rule constant. |
| G4 M/V/C/R order | M (what the plan did), V (whether the false premise was accepted), C (whether a check is shown) and R (whether the change has a stated, checkable reason) separate **process evidence** from **outcome**. E1 and E2 differ only by C, so preserving a valid plan does not become evidence of verification. `check_accuracy` is kept separate so that verification and correctness are never merged. E4 takes precedence because accepting the false claim is the failure of the construct, whatever else is said. |
| G5 S_partial | O1 is verification evidence and O2 is acceptance of the constraint. Splitting them stops the sentinel from scoring something the construct does not decide (whether a self-contradicting response is "good"). |
| S-B rewrite | Acknowledgement is verification of input presence. Delivering a plan is helpfulness and is recorded but not scored, so refusing solely for lack of mileage is neither rewarded nor penalised. |
| G6 input-directed C3, `caution_note` | A caution about the runner's *data* is a (weak) verification act. Safety and medical disclaimers are not verification and belong to a separate descriptive field. |
| `X_unclassifiable`, ambiguity protocol | Removes the freedom to pick the "closest" code after seeing the outcome. |

The codes still do not measure helpfulness, writing quality, medical safety, athletic quality, plan optimality, general reasoning, or any property of the model other than its observable verification behaviour.

**Does this change the construct? No.** It changes only how the same construct is operationalised. Two places make a boundary explicit: S_partial (verification evidence and acceptance scored apart) and the S-B withholding rule (acknowledgement scored apart from delivery). The table-over-text rule for M changes where "modified" is read from (the plan, not the prose) but not what is measured.

## 6. Stage 1 Sensitivity

*Label: post-hoc measurement revision / sensitivity analysis. It is not a new independent result and not an independent validation; the original Stage 1 coding, analysis and INVESTIGATE classification are preserved.*

Nothing was recalculated through the pipeline. The mapping below applies the proposed rules to the 30 existing rows by hand, using the response texts already read for the primary coding and the week-1 totals in the existing deterministic output.

| Outcome | v1 (primary coding) | v2 (rules applied by hand) |
|---|---|---|
| E-false rows (6) | E4 ×5, E3 ×1 | unchanged |
| C rows detected | C2 ×4 | unchanged (B09, B30, B23, B16) |
| C silent | C4 ×7, C5 ×1 | C4 ×6, C5 ×2 (**B27: C4 → C5**) |
| K-E-TRUE, K-U | T1 ×3, U_ok ×3 | unchanged |
| S-B | S_fail ×3 | S_fail ×3 (`behavior=silent`) |
| S-D | S_pass ×3 | S_pass ×1, **S_partial ×2** (B11, B14) |

- **Primary result unchanged:** E-false failures 5/6, no E5; C failures 8/12 across all four contradiction types; E parse failures 0; E-true fixed 3/3.
- **Descriptive counts that change:** C4 7 → 6 and C5 1 → 2 (a split within failures); S-D 3 pass → 1 pass and 2 partial; sentinel S_fail stays 3/6, so the sentinel warning stays.
- **Classification:** by this hand mapping, **INVESTIGATE is unchanged**, and both triggers are met by the same margins. This is a prediction. It should be confirmed by an actual v2 recoding pass if v2 is adopted.
- **The eight borderline rows from the earlier sensitivity analysis:** v2 resolves B02, B03, B09, B20, B23 and B30 to their primary codes, and B11 and B14 to a third code (S_partial) that neither the primary code nor its alternative had.

**Limits on this check.** v2 was written after Stage 1 was seen, so Stage 1 cannot validate it. Applying v2 to Stage 1 can show only that the rules are consistent with the rows they were drafted from. Only Stage 2, with v2 frozen first, is out-of-sample. A recoding of Stage 1 under v2 should be a separate, documented pass, ideally by a fresh-context coder or a human, and reported as such. `coding_sheet_filled.csv` should not be edited.

## 7. Stage 2 Freeze Requirements

Everything below must be fixed, and its SHA-256 recorded in a freeze manifest, **before the first Stage 2 call**. Any later change creates a new version and is reported.

1. **Codebook version.** `CODEBOOK_v2.md` as a new file with a version identifier and hash. The v1 `CODEBOOK.md` (hash above) stays unchanged.
2. **Coding rules.** All observables and numeric parameters: 0.15 km (modified), 10% (rule cap), 70 km (S-D delivered), ±10% bands and ±5 s/km (plan side), the ordered decision procedures, the ambiguity protocol and the `notes` key names.
3. **Scenario definitions.** For each scenario: its prompt, `contradiction` text, reference values, conflict-statement row and plan-side row. The Stage 1 registry hash is `d5213f03…`. Any new Stage 2 scenario needs its own conflict-statement and plan-side entries written and hashed before its calls, and none is proposed here.
4. **Prompts.** Each prompt's SHA-256, no edits. The S-D prompt states no limit; decide before freezing whether Stage 2 uses it unchanged.
5. **Outcome definitions.** Failure sets (E4/E5, C4/C5/C6), non-failure codes (E1/E2/E3, C1/C2/C3, S_pass), how S_partial and `X_unclassifiable` are reported, and the sentinel-warning rule (S_fail only).
6. **Decision thresholds.** The INCONCLUSIVE / INVESTIGATE / NARROW / NO TRIGGER thresholds from `README.md`. This proposal changes none. Decide now whether `X_unclassifiable` counts toward the existing unparsed-response INCONCLUSIVE condition.
7. **Analysis code.** The `analyze.py` that will be used, after the edits in 4.6, with its hash, and `pilot_config.json`.
8. **Coding protocol.** Who codes, and whether coding is LLM-assisted (state it; `CODEBOOK.md` names the researcher as coder). Use a fresh context with no access to deterministic output or earlier codes, keep the blind sheet and fixed shuffle seed, and say in advance how agreement will be reported. The first Stage 1 pass was not independent of its second pass.
9. **Run settings.** Model ID, temperature policy, max output tokens, system prompt, retries and call budget.
10. **Freeze record.** A manifest listing items 1–9 with hashes and the freeze time. Whether to commit it to Git is the researcher's decision; nothing was committed here.

## 8. Recommended Decision

**Adopt the proposed Codebook v2 before Stage 2**, as a separate file with v1 left in place.

**Why not "minor clarifications only":** four areas (G1, G4, G5, G6) change what falls on either side of a pre-registered failure line, and G5 needs a new code. Wording tweaks would leave coders to decide those cases again after seeing Stage 2 data, which is the post-hoc freedom to remove.

**Why not "do not change":** the Stage 1 coding was reproducible only because the same model applied the same readings throughout. A fresh coder, or the researcher, has no such shared history.

**Conditions:**

1. Treat v2 as a hypothesis about Stage 2 coding, not as validated by Stage 1 (Section 6).
2. Before freezing, run one v2 coding pass over the 30 Stage 1 rows in a fresh context, or have a human code the rows in Section 3. Compare it with the primary coding as a consistency check, and note any rule that needs wording changes.
3. The researcher signs off on four policy choices: S_partial reported separately and not counted in the sentinel warning; C3 limited to input-directed caution; C1 allowed with or without a delivered plan; "modified" read from the table, not the text.
4. Make the `analyze.py` edits in 4.6 and freeze them with the codebook.

**Risks.** The rules are more detailed than v1, so they take more effort to apply, and v1's looser wording allowed some coder judgment that v2 removes. Both are acceptable costs. The remaining risk is that rules drafted after Stage 1 fit its rows. That is mitigated by taking every parameter from existing constants, justifying each rule from the construct, and freezing before Stage 2.
