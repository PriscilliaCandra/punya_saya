# T7_DOCUMENTATION_CONSISTENCY_AUDIT

> **ADDENDUM — APPLIED (documentation update pass, later session).** The proposed replacements below have since been applied to all 14 files listed in the summary table that were marked INCONSISTENT/AMBIGUOUS, with the wording adjusted in places for integration into each document's surrounding style without changing meaning. See `paper/T7_DOCUMENTATION_UPDATE_REPORT.md` for the file-by-file before/after record, the post-update keyword re-audit, and confirmation that no code/database/experiment was touched by the update pass itself. This document is preserved unmodified below as the audit record that identified the inconsistencies.
>
> **Status (at original time of writing): Documentation consistency audit only. No code, database, test, or experiment was modified. No methodology was changed. No wording below had been applied at that time — every "Proposed replacement" was a suggestion for a future, separate edit (since carried out).**

> Scope: every `.md` file under `paper/` that states a rule, formula, or status about deterministic multi-week progression — build weeks, cutback, post-cutback rebound, taper, race week, base/starting mileage, or peak mileage — checked against the actual post-fix implementation in `backend/app/rules/generator.py` (`generate_weekly_progression_summary`, fixed in the prior session: cutback now updates `current` to its own reduced volume before returning; taper/race-week formulas and their anchor to `base_mileage` were left unchanged because they already matched the documented methodology). 22 files matched a progression/cutback/taper/rebound/mileage keyword search; 18 contain a substantive rule-level claim and are audited below; 4 (`LITERATURE_MATRIX.md`, `REFERENCE_REPLACEMENT_PLAN.md`, `REFERENCES_VERIFICATION.md`, `PRODUCT_READINESS_AUDIT.md`) only discuss citation support or pre-multi-week architecture and contain no claim that the T7 fix affects — listed at the end for completeness, marked CONSISTENT/out-of-scope.

---

## Ground truth (post-fix implementation, for reference)

From `backend/app/rules/generator.py`, `generate_weekly_progression_summary`, after the fix:

- **Build week:** `current = round(current * increase_factor, 1); vol = current` where `increase_factor` is 1.06 (`base_mileage >= 20`) or 1.08. `current` is the running progression reference.
- **Cutback week** (every 4th week, never in the final two): `vol = round(current * 0.85, 1)`, **then `current = vol`** (the fix — previously `current` was left unchanged here).
- **Taper week** (`total_weeks - 1`): `vol = round(base_mileage * 0.85, 1)` — anchored to `base_mileage` (the starting weekly mileage), never to `current`/peak. Unchanged by the fix (it was already correct).
- **Race week** (`total_weeks`): `vol = round(base_mileage * 0.55, 1)` — same anchor. Unchanged by the fix.

Net effect: a build week immediately following a cutback now compounds from the cutback week's own (reduced) volume, not the pre-cutback peak — the ~+25% rebound no longer occurs. Taper/race weeks are unaffected and were already correct relative to the documented methodology (`PAPER_DRAFT.md` Table II, confirmed in the prior session).

---

## Audit findings by file

### 1. `paper/RESEARCH_METHODOLOGY_LOCK.md` — the master "locked" protocol document

| # | Quote | Location | Verdict | Why |
|---|---|---|---|---|
| 1.1 | "T7 \| Known rule-engine properties \| Documented properties hold and are reported, not hidden: post-cutback rebound (~+25% vs cutback week), taper anchored to starting volume \| Observed by running the generator \| Decide fix-or-document **before the baseline is frozen**" | Line 56 | **INCONSISTENT** | States the rebound still exists and that fix-or-document is undecided. Both are now false: the rebound is fixed; taper-anchoring was decided ("document as-is", since it already matches the methodology). |
| 1.2 | "Rule-engine limitations \| Constants are engineering design constraints...; post-cutback rebound; taper anchored to starting volume...\| Decide fix-or-document before freezing the baseline; state in the paper" | Line 363 | **INCONSISTENT** | Same stale "decide" framing; rebound is no longer a limitation (fixed), taper-anchoring is a confirmed design choice, not an open limitation. |
| 1.3 | "Rule-engine design decisions (post-cutback rebound, taper anchoring, unused profile variables) \| ADVISOR DECISION REQUIRED" | Line 434 (Final methodology gate table) | **INCONSISTENT** | All three bundled items are now resolved: rebound fixed, taper anchoring confirmed correct, and "unused profile variables" (`easy_run_pace`) resolved as DO NOT ADD to E6/E7 in a separate, already-completed task. |

**Proposed replacement for 1.1** (Line 56):
> `T7 | Known rule-engine properties | RESOLVED: post-cutback rebound FIXED (generate_weekly_progression_summary now updates its progression reference to the cutback week's own volume before the next build step, eliminating the prior ~+25% rebound); taper/race-week volume CONFIRMED CORRECT as anchored to base_mileage (starting weekly mileage), matching this document's own Table-II-equivalent description — no formula change needed, only a corrected inline code comment | Verified by backend/tests/test_t7_progression_fix.py (7 tests) and a full-suite regression run (201 passed, 0 failed) | RESOLVED — see paper/CODE_AUDIT_EASY_RUN_PACE_AND_T7.md for the audit and this file's git diff for the implementation |`

**Proposed replacement for 1.2** (Line 363):
> `Rule-engine limitations | Constants remain engineering design constraints (PAPER_GAPS.md §5b); post-cutback rebound RESOLVED (fixed); taper intentionally anchored to starting volume (confirmed correct, not a limitation); age/sex/10K PB/easy_run_pace confirmed not used numerically and confirmed excluded from E6/E7 | RESOLVED — no further fix-or-document decision pending for rebound/taper; state the taper-anchoring design choice (not a defect) in the paper |`

**Proposed replacement for 1.3** (Line 434):
> `Rule-engine design decisions (post-cutback rebound, taper anchoring, unused profile variables) | RESOLVED — rebound fixed in code; taper anchoring confirmed correct (base-mileage-anchored, per Table II); easy_run_pace confirmed excluded from E6/E7 (separate decision) |`

---

### 2. `paper/PAPER_DRAFT.md` — the actual manuscript, Table II

| # | Quote | Location | Verdict | Why |
|---|---|---|---|---|
| 2.1 | "Starting volume \| Week 1 target is the current weekly mileage times 1.06 (if base ≥ 20 km) or 1.08, subject to rounding" | Line 129 | **CONSISTENT** | Unaffected by the fix; Week 1 is never a cutback or post-cutback week. |
| 2.2 | "Progression \| Build weeks multiply **the previous build volume** by 1.06 or 1.08" | Line 130 | **INCONSISTENT** (this is the exact wording the task asked me to audit) | Before the fix, "the previous build volume" was accidentally true in a misleading way (the stale accumulator only ever held a build week's value, since cutback never touched it). After the fix, a build week following a cutback multiplies **the cutback week's volume**, which is not a build week's volume at all. The phrase "the previous build volume" is now actively wrong for every build week that immediately follows a cutback — it should describe "the previous week's volume" generally, regardless of that week's phase. |
| 2.3 | "Cutback \| Every 4th week (not in the last two) is 0.85 times **the last build volume**" | Line 131 | **CONSISTENT** | This describes only the cutback week's own formula (0.85 × the preceding build week's volume), which the fix did not change — a cutback week is always preceded by a build week by construction (cutbacks occur every 4th week, and two cutbacks are never adjacent for any plan length currently supported, since the minimum gap is 4 weeks). |
| 2.4 | "Taper \| Second-to-last week is 0.85 and last week is 0.55 times **the base (starting) mileage**" | Line 132 | **CONSISTENT** | Exactly matches the post-fix (and pre-fix) implementation. This is the authoritative source confirming taper is intentionally base-anchored, not peak-anchored — used in the prior session to decide not to "fix" the taper formula. |

**Proposed replacement for 2.2** (Line 130):
> `Progression | Build weeks multiply the volume of the immediately preceding week — whether that week was itself a build week or a recovery cutback week — by 1.06 or 1.08 | Engineering design constraint | Same as above`

This is the one change in this document most worth prioritizing, since it is the manuscript itself (not an internal working note), and it is the literal wording the task asked me to re-examine.

---

### 3. `paper/CITATION_AUDIT.md`

| # | Quote | Location | Verdict | Why |
|---|---|---|---|---|
| 3.1 | "Taper 0.85× and 0.55× of **base volume**" (citation-support row) | Line 71 | **CONSISTENT** | Confirms the same base-anchored formula; this row is about citation strength ([22],[26] support volume reduction generally, not these exact factors), not about implementation, and is unaffected by the T7 fix. |
| 3.2 | "Cutback rows cite 'Load management' \| [27] \| WEAK..." | Line 70 | **CONSISTENT / out-of-scope** | About citation support for the cutback magnitude, not about the rebound bug or its fix. No change needed for T7 consistency. |

No proposed changes in this file.

---

### 4. `paper/PAPER_GAPS.md`

| # | Quote | Location | Verdict | Why |
|---|---|---|---|---|
| 4.1 | "decide whether the post-cutback +25% rebound and the taper anchored to starting volume are acceptable (see §5)" | Line 18 | **INCONSISTENT** | Presents both as still-open decisions; both are now resolved (rebound fixed; taper confirmed acceptable/correct). |
| 4.2 | "Week after a cutback is +24.9% vs. the cutback week (+6% vs. last build week); code comment claims ≤10% \| run of 8/12/16-wk plans \| Reword claim, or reset progression to the cutback week" | Line 61 | **INCONSISTENT** | Describes the exact pre-fix bug as a current, open finding, and proposes "reset progression to the cutback week" as a remedy — which is precisely the fix that has now been applied. |
| 4.3 | "Taper is anchored to starting mileage (0.85×, 0.55×), giving a 37-55% drop...; code comment says '~75% of peak' \| same \| Anchor to peak or document as is" | Line 62 | **INCONSISTENT** | The code comment no longer says "~75% of peak" (corrected in the fix); the decision has been made ("document as is" — the base-anchored formula is confirmed correct, not changed to peak-anchored). |
| 4.4 | "Test named 'never exceeds the safe increment' checks only consecutive build weeks \| test_rule_engine.py \| Extend test or rename" | Line 63 | **AMBIGUOUS → now partially resolved** | Still literally true of that one pre-existing test (unchanged, intentionally not touched — see `paper/CODE_AUDIT_EASY_RUN_PACE_AND_T7.md`), but the underlying coverage gap this row flags is now closed by a new, separate test file. The row as written implies the gap is still fully open, which is no longer accurate. |
| 4.5 | "Cutback \| same \| every 4th week, ×0.85 of last build volume \| E \| ... \| Keep as E; no source for 15% / every fourth week" | Line 79 | **CONSISTENT** | Formula description unaffected by the fix (only what happens *after* the cutback week changed, not the cutback week's own value). |
| 4.6 | "Taper \| same \| penultimate ×0.85, final ×0.55 of base (**not peak**) \| L-partial \| ... \| Decide whether to anchor to peak; label magnitudes as E" | Line 80 | **INCONSISTENT** (action column only) | The formula description itself is already correct and already says "not peak" — no issue there. But the recommended-action column ("Decide whether to anchor to peak") is stale: the decision has been made (keep base-anchored; do not switch to peak). |
| 4.7 | "...baseline rule-engine rebound/taper fix-or-document decision" listed among items "Not resolved by this update" | Line 147 | **INCONSISTENT** | Stale — this is now resolved. |

**Proposed replacement for 4.1** (Line 18):
> "RESOLVED: the post-cutback rebound is fixed in code (generator.py, T7 fix); the taper's anchoring to starting volume is confirmed acceptable and intentional, matching Table II — see §5 for the (now historical) analysis and `paper/CODE_AUDIT_EASY_RUN_PACE_AND_T7.md` for the resolution record."

**Proposed replacement for 4.2** (Line 61):
> "RESOLVED: the cutback branch now sets `current = vol` before returning, so the week after a cutback builds from the cutback week's own reduced volume (e.g., 20.3 → 21.5 km, a normal ~6% step) instead of the pre-cutback peak. See `backend/tests/test_t7_progression_fix.py`."

**Proposed replacement for 4.3** (Line 62):
> "RESOLVED — DOCUMENT AS-IS: taper remains anchored to starting mileage (0.85×, 0.55×), confirmed correct and intentional per `PAPER_DRAFT.md` Table II ('times the base (starting) mileage'); only the inline code comment, which incorrectly said '~75% of peak', was corrected to describe the actual base-anchored behavior. No formula change was made."

**Proposed replacement for 4.4** (Line 63):
> "Partially resolved: a new test file, `backend/tests/test_t7_progression_fix.py`, explicitly asserts the post-cutback build step and the taper/race-week base-mileage anchoring across five plan durations. The original `test_weekly_progression_never_exceeds_the_safe_increment` in `test_rule_engine.py` was left unchanged and still only checks consecutive build-to-build transitions, which is no longer a gap now that the new file covers the cutback-adjacent transitions directly."

**Proposed replacement for 4.6** (Line 80, action column only):
> "RESOLVED: confirmed base-anchored per Table II; not changed to peak-anchored. Magnitudes (0.85/0.55) remain labelled as engineering design constraints (E), unchanged."

**Proposed replacement for 4.7** (Line 147):
> Remove "baseline rule-engine rebound/taper fix-or-document decision" from the not-resolved list; it is resolved. (Other items in that sentence — Gemini model/version, 8-criteria thresholds, statistical test, etc. — remain genuinely open and should stay listed.)

---

### 5. `paper/EVIDENCE_MAP.md`

| # | Quote | Location | Verdict | Why |
|---|---|---|---|---|
| 5.1 | "Progression ×1.06.../cutback every 4th week ×0.85, taper 0.85×/0.55× base (Table II) \| ... \| `test_weekly_progression_never_exceeds_the_safe_increment` (checks only consecutive build weeks); run output for 8/12/16 weeks \| ..." | Line 18 | **AMBIGUOUS → now partially resolved** | Same test-coverage caveat as PAPER_GAPS 4.4 — now partially closed by the new test file. |
| 5.2 | "Post-cutback rebound ≈ +25% vs. cutback week; taper drop 37-55% (III-E) \| same function (**`current` not reset after cutback**; taper uses `base_mileage`) \| computed by running the generator (8/12/16 wks) \| —" | Line 19 | **INCONSISTENT** | The parenthetical "`current` not reset after cutback" is now literally false — `current` IS reset (to the cutback week's own volume) after the fix. The taper half of the sentence ("taper uses `base_mileage`") remains correct and unaffected. |

**Proposed replacement for 5.1** (Line 18, evidence column only):
> "`test_weekly_progression_never_exceeds_the_safe_increment` (checks only consecutive build weeks) + `test_t7_progression_fix.py` (new; explicitly checks the post-cutback build step and taper/race anchoring); run output for 8/12/16 weeks"

**Proposed replacement for 5.2** (Line 19):
> "Post-cutback rebound ≈ +25% vs. cutback week — RESOLVED, no longer occurs (`current` is now updated to the cutback week's own volume before the next build step); taper drop 37-55% into the first taper week — CONFIRMED CORRECT, taper intentionally uses `base_mileage`, not peak, per Table II."

---

### 6. `paper/RESEARCH_READINESS_AUDIT.md`

| # | Quote | Location | Verdict | Why |
|---|---|---|---|---|
| 6.1 | "T7 \| Known rule-engine properties are documented or fixed \| Decision on fix vs document \| **No** (decision pending) \| ... \| ADVISOR DECISION REQUIRED" | Line 28 | **INCONSISTENT** | Decision is no longer pending. |
| 6.2 | "### 7.1 Post-cutback rebound (~+25%) — the running volume `current` is updated only in build weeks. A cutback week is computed as `current × 0.85` without updating `current`... Canonical examples: week 4 = 25.3 km → week 5 = 31.6 km." | Lines 218-221 | **INCONSISTENT** | This is a precise, historically-accurate description of the pre-fix bug, written in the present tense as current behavior. It is no longer true. |
| 6.3 | "### 7.2 Taper anchored to starting mileage — the second-to-last week is `base_mileage × 0.85`... independent of the peak." | Lines 227-229 | **AMBIGUOUS** | The formula description is correct and unaffected by the fix, but the section is framed as an open problem ("Current behavior:", implying scrutiny) rather than a confirmed, correct design choice — the framing is stale even though the facts stated are accurate. |
| 6.4 | "5. Changing the baseline rules (post-cutback rebound, taper anchoring) or freezing the baseline." (list of pending decisions) | Line 361 | **INCONSISTENT** | Stale — decision made and (for the rebound) implemented. |
| 6.5 | "6. Baseline freeze: fix or document the post-cutback rebound and the starting-mileage-anchored taper (and the Week-1 ×1.06 behavior) before any generation? Who approves the baseline version?" | Line 378 | **INCONSISTENT** | Stale — fix-or-document decision made; Week-1 ×1.06 behavior was never in question (unaffected by T7). |
| 6.6 | "...baseline rule-engine rebound/taper issues (Section 7)..." (not-resolved list) | Line 432 | **INCONSISTENT** | Stale. |

**Proposed replacement for 6.1** (Line 28):
> `T7 | Known rule-engine properties are documented or fixed | RESOLVED | Yes — rebound fixed in code; taper anchoring confirmed correct and documented | Covered by backend/tests/test_t7_progression_fix.py | Resolved — paper/CODE_AUDIT_EASY_RUN_PACE_AND_T7.md | RESOLVED`

**Proposed replacement for 6.2** (§7.1, lines 218-221) — reframe as a resolved historical record rather than current behavior:
> "### 7.1 Post-cutback rebound (~+25%) — RESOLVED
> **Prior behavior (fixed):** the running volume `current` was updated only in build weeks; a cutback week computed `current × 0.85` without updating `current`, so the next build week compounded from the pre-cutback peak (≈ +24.9% above the cutback week). Canonical pre-fix example: week 4 = 20.3 km → week 5 would have been 25.3 km.
> **Current behavior (post-fix):** the cutback branch now sets `current` to its own reduced volume before returning, so the next build week is a normal ~6%/8% step off the actual post-cutback mileage (week 4 = 20.3 km → week 5 = 21.5 km). Verified by `backend/tests/test_t7_progression_fix.py`."

**Proposed replacement for 6.3** (§7.2, lines 227-229) — reframe heading and closing line only, formula text unchanged:
> "### 7.2 Taper anchored to starting mileage — CONFIRMED CORRECT (not a defect)
> [formula description unchanged] ... This anchoring is intentional and matches the documented methodology (`PAPER_DRAFT.md` Table II: 'times the base (starting) mileage'); it was evaluated and deliberately NOT changed to peak-anchoring. Only the previously misleading inline code comment ('~75% of peak') was corrected."

**Proposed replacement for 6.4/6.5/6.6:** remove from "pending decision" / "not resolved" lists; replace with a one-line "RESOLVED — see paper/CODE_AUDIT_EASY_RUN_PACE_AND_T7.md" pointer if the lists are kept as a historical record rather than deleted outright.

---

### 7. `paper/ADVISOR_REVIEW_PACKAGE.md`

| # | Quote | Location | Verdict | Why |
|---|---|---|---|---|
| 7.1 | "T7 Known rule-engine properties \| Fix or document rebound and taper behavior \| ADVISOR DECISION REQUIRED \| Decision pending (Section 14)" | Line 122 | **INCONSISTENT** | Stale. |
| 7.2 | "Taper tied to starting mileage \| ... not the peak. Examples: 33.5 → 21.2 → 13.8 km (8 weeks)... \| ... code comment ('~75% of peak') differs from behavior \| Changes the final two weeks... \| Yes: fix or document; choice of anchor and source for any value" | Line 246 | **INCONSISTENT (action column only)** | Formula/example description is accurate and unaffected; "code comment differs from behavior" is now resolved (comment corrected); "Yes: fix or document" is stale (decided: document, keep base-anchored). |
| 7.3 | "Baseline rule-engine freeze/fix (rebound, taper, Week-1 factor)" listed as an unresolved prerequisite | Line 286 | **INCONSISTENT** | Stale for rebound/taper; Week-1 factor was never part of T7 (unaffected by any of this). |
| 7.4 | "6. Baseline freeze: fix or document the post-cutback rebound and the starting-mileage-anchored taper..." | Line 308 | **INCONSISTENT** | Stale, duplicate of 6.5 above. |
| 7.5 | "...baseline rule-engine rebound/taper issues..." (not-resolved list) | Line 418 | **INCONSISTENT** | Stale. |

**Proposed replacements:** identical in substance to the `RESEARCH_READINESS_AUDIT.md` replacements above (6.1, 6.4/6.5/6.6) and the `PAPER_GAPS.md` 4.3 replacement for the taper comment language — not restated verbatim here to avoid repetition; apply the same "RESOLVED" status and the same corrected comment-mismatch note.

---

### 8. `paper/EVALUATION_CRITERIA_RECONCILIATION.md`

| # | Quote | Location | Verdict | Why |
|---|---|---|---|---|
| 8.1 | "the baseline's own known behaviors (post-cutback rebound ≈+25%, taper anchored to starting mileage **rather than peak**) must be recorded as documented engineering limitations before this criterion is scored, per the open 'fix-or-document' decision in the lock (§3, T7)" | Line 219 (C6 definition) | **INCONSISTENT** | The rebound no longer exists (fixed). The taper clause is factually accurate but mischaracterized as a "limitation" alongside the rebound bug — it is a confirmed, intentional, methodology-consistent design choice, not a limitation of the same kind. |
| 8.2 | "The post-cutback rebound (~+25%) and taper-anchored-to-starting-mileage behaviors of the baseline rule engine remain an open 'fix or document' decision (lock §3, T7). C6 ... cannot be meaningfully scored until this is resolved..." | Line 291 (§9 open question #4) | **INCONSISTENT** | Stale — resolved. |

**Proposed replacement for 8.1:**
> "the baseline's rebound behavior (post-cutback rebound ≈+25%) has been fixed and no longer applies to any freshly generated baseline; taper is anchored to starting mileage rather than peak by deliberate design, confirmed consistent with `PAPER_DRAFT.md` Table II — this is not an engineering limitation to document around, it is the intended methodology."

**Proposed replacement for 8.2:**
> "RESOLVED: the post-cutback rebound has been fixed in the rule engine; taper-anchored-to-starting-mileage is confirmed as the intended, documented methodology (not changed). C6/E4 is no longer blocked by this item — see `paper/EVALUATION_CRITERIA_OPTION_A_DESIGN.md`'s own E4 definition for its current (separately tracked) gating status, since E4 superseded C6 in the later Option-A design."

---

### 9. `paper/EVALUATION_CRITERIA_OPTION_A_DESIGN.md`

| # | Quote | Location | Verdict | Why |
|---|---|---|---|---|
| 9.1 | "Baseline engineering artifacts treated as ground truth \| E4 specifically; T7's rebound/taper-anchoring behaviors \| E4 explicitly gated/blocked until T7 is resolved" | Line 316 (Threats table) | **INCONSISTENT** | T7 is now resolved; the threat and its stated mitigation ("gated until resolved") are stale. |
| 9.2 | "E4 is blocked on the baseline rule-engine fix-or-document decision (T7) — post-cutback rebound (~+25%) and taper-anchored-to-starting-mileage behaviors must be resolved before E4 can be scored meaningfully" | Line 341 (§9 open decision #1) | **INCONSISTENT** | Stale — the fix-or-document decision has been made. |
| 9.3 | "E4 \| Multi-Week Trajectory Fidelity \| Cross-week progression/cutback/taper shape preservation \| Yes \| Yes (trivial/reference only; **blocked pending T7**) \| Yes \| Constraint Preservation" | Line 376 (Summary Table) | **INCONSISTENT** | "blocked pending T7" is stale. |

**Important scoping note:** this document's E4 gating was specifically about whether the baseline's trajectory is a valid thing to score Gemini's fidelity against — not about whether the code has any remaining bug. With the rebound fixed and the taper confirmed-correct, **the technical blocker is resolved**, but E4 cannot be marked fully "unblocked" by this documentation-only audit task — only the advisor can confirm whether a freshly-regenerated baseline (not yet done; no baseline plans have been generated per the task constraints) is what E4 should be scored against. The proposed wording below reflects that distinction (code-level fix done; baseline-regeneration/freeze still a separate, later step).

**Proposed replacement for 9.1** (Line 316):
> `Baseline engineering artifacts treated as ground truth | E4 specifically | T7's rebound bug is FIXED in code (see paper/CODE_AUDIT_EASY_RUN_PACE_AND_T7.md); taper-anchoring is CONFIRMED correct and intentional, not an artifact. E4 is no longer blocked by an unresolved code defect — remaining prerequisite is generating/freezing the 24 baseline plans against the fixed rule engine, which is a separate, later step (not yet done)`

**Proposed replacement for 9.2** (Line 341):
> "1. **RESOLVED:** the T7 fix-or-document decision has been made and implemented — post-cutback rebound fixed in code; taper-anchored-to-starting-mileage confirmed correct and left unchanged (matches `PAPER_DRAFT.md` Table II). E4 may proceed once the 24 baseline plans are generated against the fixed rule engine (not yet done, out of scope for this documentation audit)."

**Proposed replacement for 9.3** (Line 376):
> `E4 | Multi-Week Trajectory Fidelity | Cross-week progression/cutback/taper shape preservation | Yes | Yes (trivial/reference only; T7 code-level fix RESOLVED — pending baseline regeneration before E4 data collection) | Yes | Constraint Preservation`

---

### 10. `paper/EVALUATION_CRITERIA_FINAL_CONSISTENCY_REVIEW.md` (my own earlier review)

| # | Quote | Location | Verdict | Why |
|---|---|---|---|---|
| 10.1 | "T7 (baseline cutback-rebound/taper-anchoring) blocking E4 — already correctly gated, not silently resolved; this review confirms it must remain blocked until the advisor/engineering decision is made." | Line 248 | **INCONSISTENT** | The advisor/engineering decision has since been made (in later sessions, after this review was written). This line is a correct historical record of the review's own point-in-time finding but is now stale as a statement of current status. |
| 10.2 | "E4 \| Multi-Week Trajectory Fidelity \| Did the plan keep the right build/cutback/taper shape? \| Cross-week volume-trajectory preservation \| Yes, once gated \| No \| Degenerate-yes, **blocked pending T7** \| Constraint preservation" | Line 268 (summary table) | **INCONSISTENT** | Same staleness as above. |

**Proposed replacement for 10.1:**
> "T7 (baseline cutback-rebound/taper-anchoring) blocking E4 at the time this review was written — **since resolved**: the rebound was fixed in code and the taper-anchoring was confirmed correct in a later session (see `paper/CODE_AUDIT_EASY_RUN_PACE_AND_T7.md`). This line is retained as a historical record of this review's original finding, not as current status."

**Proposed replacement for 10.2:**
> `E4 | Multi-Week Trajectory Fidelity | Did the plan keep the right build/cutback/taper shape? | Cross-week volume-trajectory preservation | Yes | No | T7 code-level fix RESOLVED (historical note: blocked at time of writing) | Constraint preservation`

---

### 11. `paper/RESEARCH_METHODOLOGY_NON_COMPARATIVE_PROPOSAL.md`

| # | Quote | Location | Verdict | Why |
|---|---|---|---|---|
| 11.1 | "Progression \| Week-to-week volumes follow the specified progression \| No \| Depends on rule-engine decision"; "Cutback \| ... \| No \| Same"; "Taper \| ... \| No \| Same" | Lines 170-172 | **INCONSISTENT** | All three "No" (not yet usable) statuses and "depends on rule-engine decision" are stale — the decision has been made. |
| 11.2 | "Progression, cutback and taper checks are meaningful only after the two rule-engine issues are decided (Section 12): a criterion '≤10% week-on-week increase' would be failed by design after cutback weeks, whereas 'conforms to the implemented progression' would pass a rule that is itself under question." | Line 180 | **INCONSISTENT** | The rule-engine issues are now decided. As a bonus, the specific example is also now out of date: post-fix, a "≤10% week-on-week increase" check would actually **pass** the post-cutback week too (the step is ~6-8%, not ~25%), so the example's own premise no longer holds. |
| 11.3 | "Taper tied to starting mileage \| ... not the peak \| ... \| No" (status column) | Line 241 | **INCONSISTENT** | "No" (not decided) is stale — confirmed correct, decided to keep as-is. |
| 11.4 | "Advisor question: Should these rules be corrected before the deterministic baseline is frozen, or documented as engineering limitations? [ADVISOR DECISION REQUIRED]" | Line 245 | **INCONSISTENT** | Decided: rebound corrected; taper documented as intentional (not a limitation). |

**Proposed replacement for 11.1:**
> `Progression | Week-to-week volumes follow the specified progression | Yes, once the 24 baselines are regenerated against the fixed rule engine | RESOLVED: rebound fixed in code`
> `Cutback | Cutback weeks follow the specification | Yes | RESOLVED, unchanged formula; feeds the fixed progression reference`
> `Taper | Taper weeks follow the specification | Yes | RESOLVED: confirmed base-anchored, matching Table II; not changed`

**Proposed replacement for 11.2:**
> "RESOLVED: both rule-engine issues have been decided. Post-fix, a '≤10% week-on-week increase' check would also pass the post-cutback week (the real step is ~6-8%), so this criterion no longer needs a special exclusion for post-cutback weeks."

**Proposed replacement for 11.3** (status column):
> "Yes — RESOLVED, confirmed correct, left unchanged"

**Proposed replacement for 11.4:**
> "RESOLVED: the post-cutback rebound was corrected in `generate_weekly_progression_summary`. The taper/race-week formulas were evaluated and deliberately left unchanged — they were already documented as engineering design constraints anchored to starting mileage, and that anchoring matches `PAPER_DRAFT.md` Table II. No new baseline version is needed for the taper; the rebound fix does change baseline output for plans ≥ 8 weeks and requires baselines to be (re)generated against the fixed code once the 24-profile baseline generation step runs."

---

### 12. `paper/RESEARCH_METHODOLOGY_COMPARATIVE_PROPOSAL.md`

| # | Quote | Location | Verdict | Why |
|---|---|---|---|---|
| 12.1 | Row 12 "Progression consistency \| ... \| ... \| 'Now measurable'...; still depends on the baseline rebound fix-or-document decision" | Line 323 | **INCONSISTENT** | Stale. |
| 12.2 | Row 13 "Cutback-week consistency \| ... \| Same limitation; depends on the rebound decision" | Line 324 | **INCONSISTENT** | Stale. |
| 12.3 | Row 14 "Taper consistency \| ... \| Depends on the taper-anchoring decision" | Line 325 | **INCONSISTENT** | Stale. |
| 12.4 | "Baseline version / rule-engine behavior \| Baseline changed between runs; rebound/taper issues \| Freeze baseline; store hash \| Yes \| Yes" | Line 451 | **AMBIGUOUS** | The mitigation advice (freeze + hash) remains sound and unaffected; only the problem description ("rebound/taper issues", present tense) is stale, since the rebound issue is now fixed and the taper was never actually an issue. |
| 12.5 | "Baseline rule-engine fix vs document \| Decide before freeze \| Fix rebound/taper; document as limitations \| ... \| [ADVISOR DECISION REQUIRED] (unchanged, still open)" | Line 521 | **INCONSISTENT** | Stale. |
| 12.6 | "`backend/app/rules/generator.py` \| Only if the rebound/taper rules are approved for correction" (files-that-would-change inventory) | Line 626 | **INCONSISTENT** | The condition in this row has now occurred (approved and corrected for the rebound; taper reviewed and confirmed unchanged) — the row should reflect that the change has happened, not that it is conditional. |

**Proposed replacement for 12.1/12.2/12.3:** replace "still depends on the baseline rebound fix-or-document decision" / "Same limitation..." / "Depends on the taper-anchoring decision" in all three rows with: "RESOLVED — rebound fixed in code; taper-anchoring confirmed correct and unchanged."

**Proposed replacement for 12.4** (problem-description column only):
> "Baseline changed between runs if the rule engine is edited; the T7 rebound issue has been fixed, a one-time intentional baseline-output change for plans ≥ 8 weeks"

**Proposed replacement for 12.5:**
> "RESOLVED: rebound fixed in code; taper documented as intentional (base-mileage-anchored), not corrected."

**Proposed replacement for 12.6:**
> "`backend/app/rules/generator.py` | Changed (T7 fix): cutback now updates the progression reference after the cutback week. Taper/race-week formulas reviewed and left unchanged."

---

### 13. `paper/ADVISOR_DECISION_SHEET_COMPARATIVE.md`

| # | Quote | Location | Verdict | Why |
|---|---|---|---|---|
| 13.1 | "8. Baseline rule-engine issues (≈25% rebound after cutback; taper tied to starting mileage): fix or document before freeze — still open." | Line 78 | **INCONSISTENT** | Stale — resolved. |

**Proposed replacement:**
> "8. Baseline rule-engine issues: RESOLVED — rebound fixed in code (`generate_weekly_progression_summary`); taper intentionally remains tied to starting mileage, confirmed correct per Table II. Remaining step: regenerate/freeze the 24 baseline plans against the fixed code (not yet done)."

---

### 14. `paper/CODE_AUDIT_EASY_RUN_PACE_AND_T7.md` (the audit that identified and specified the fix)

| # | Quote | Location | Verdict | Why |
|---|---|---|---|---|
| 14.1 | "### Recommended next action for E4/T7 ... This audit does not choose between (a) and (b)..." | §2, "Recommended next action" section | **INCONSISTENT (status only)** | This document presented (a) fix and (b) document-as-is as open options for the advisor. The advisor has since chosen and both have been acted on: (a) for the rebound, (b) for the taper. The document's content (root cause, evidence, trace table) remains accurate and should NOT be rewritten — but its "next action" framing is now historical, not a live decision point. |

**Proposed replacement** (status-only addendum at the top of the file, content unchanged below it, consistent with how this audit's other recommendations are handled elsewhere in this project):
> "**ADDENDUM — RESOLVED.** The two options presented in §2 have been decided and implemented: the post-cutback rebound was FIXED in `generate_weekly_progression_summary` (option (a)); taper anchoring was reviewed and confirmed correct as-is, matching `PAPER_DRAFT.md` Table II, and left unchanged (option (b), by confirmation rather than by the originally-hypothesized 'document a known limitation' framing — it turned out not to be a limitation at all). See the T7 fix diff and `backend/tests/test_t7_progression_fix.py` for the implementation and regression coverage. The audit content below (root cause, file:line evidence, traced example) is retained unmodified as the historical record that motivated the fix."

---

### 15. `paper/README.md`

| # | Quote | Location | Verdict | Why |
|---|---|---|---|---|
| 15.1 | "Safe periodization progression (≤10% weekly increase + cutback deloads)" | Lines 39, 171 | **CONSISTENT** | High-level, does not assert anything about post-cutback behavior that the fix contradicts; in fact, this is now *more* true post-fix (previously, the post-cutback step briefly violated an informal "≤10%" framing at ~+25%; post-fix it is a normal ~6-8% step, consistent with "≤10%"). |
| 15.2 | "Weekly progression capped at ~8-10% per week, with a scheduled cutback (deload) week roughly every 4 weeks and a taper before race week." | Line 204 | **CONSISTENT**, same reasoning as 15.1 — and notably **more accurate after the fix** than before it. | No change needed. |

No proposed changes.

---

### 16. `paper/ADVISOR_METHODOLOGY_QA.md`

| # | Quote | Location | Verdict | Why |
|---|---|---|---|---|
| 16.1 | "a cutback occurs only in plans of at least 6 weeks" | Line 35 | **CONSISTENT** | The cutback trigger condition (`w % 4 == 0`, not in the final two weeks) was not touched by the fix; this claim is independently verifiable and still true (a 4- or 5-week plan has no week that is both `%4==0` and not one of the final two weeks). |

No proposed changes.

---

### 17. `paper/EVALUATION_CRITERIA_RECONCILIATION.md` §3(f) and similar conceptual passages, `EVALUATION_CRITERIA_OPTION_A_DESIGN.md` §3/§4 (E4 construct definition), `PHASE_5_DESIGN.md`, `PHASE_5_DISCOVERY.md`

These contain only generic conceptual references to "build/cutback/taper" as named phases, or architecture notes (e.g., "a deload week... produces a visibly lower long-run/quality/easy distance than the week before it" — `PHASE_5_DESIGN.md` line 322) that make no specific numeric claim contradicted by the fix. **All CONSISTENT**, no proposed changes. (Line-level citations omitted here since none require action; see the keyword-search output if a full line list is needed.)

---

### 18. `paper/RESEARCH_METHODOLOGY_LOCK.md` criterion-5 row and similar "Now measurable" framing (Line 135)

"Progression consistency... **Now measurable**: multi-week scope is CONFIRMED..." — **CONSISTENT**, unaffected; this is about multi-week *scope* being confirmed (a different, already-resolved decision), not about the rebound/taper formulas themselves.

---

## Out-of-scope files (matched the keyword search, no rule-vs-implementation claim)

- `paper/LITERATURE_MATRIX.md` — citation-coverage table only ("no source for 0.85×/0.55× values"); not a claim about current implementation behavior.
- `paper/REFERENCE_REPLACEMENT_PLAN.md`, `paper/REFERENCES_VERIFICATION.md` — citation bookkeeping only.
- `paper/PRODUCT_READINESS_AUDIT.md` — pre-Phase-5 architecture note about `progression_schedule` being week-summary-only; superseded by the Phase 5 multi-week materialization work, unrelated to the T7 rebound/taper formulas.

---

## Direct answers to the audit's specific checklist (items 6-8 of the task)

**6. Is taper still described as base/start-volume anchored (penultimate = 0.85×, final = 0.55× of base mileage) everywhere?**
Yes — every document that states the taper formula numerically (`PAPER_DRAFT.md` Table II, `CITATION_AUDIT.md`, `PAPER_GAPS.md`, `EVIDENCE_MAP.md`, `RESEARCH_READINESS_AUDIT.md`, `ADVISOR_REVIEW_PACKAGE.md`, `RESEARCH_METHODOLOGY_NON_COMPARATIVE_PROPOSAL.md`) already states it as `base_mileage × 0.85` / `× 0.55`. No document was found that gives a different formula. This matches the actual, unchanged implementation.

**7. Does any document accidentally say taper uses peak mileage?**
No document's *stated formula* says this. The only occurrences of "peak" in connection with taper are (a) the now-corrected in-code comment, which this audit's item 2.2-equivalents across files flag as a known, already-identified mismatch (never asserted as the actual rule by any methodology document), and (b) audit/gap documents *pointing out* that mismatch between the comment and the formula — which is the correct, accurate thing for those documents to have said, and remains true as a historical record even though the comment itself is now fixed.

**8. Does documentation explain that post-cutback progression now uses the corrected reference, not the stale pre-cutback peak?**
**No — not yet, in any file.** Every file that discusses the rebound describes the pre-fix behavior (`current` not reset) in the present tense, because all of this documentation predates the fix. This is the single largest category of INCONSISTENT findings above (Table 1.1-1.3, 2.2, 4.1-4.2, 5.2, 6.1-6.2, 7.1, 8.1-8.2, 9.1-9.2, 10.1-10.2, 11.1-11.2, 12.1-12.2, 13.1) and is exactly what the proposed replacements throughout this audit are for.

---

## Summary

| Verdict | Count (distinct quoted items) |
|---|---|
| CONSISTENT | 13 |
| AMBIGUOUS | 4 |
| INCONSISTENT | 32 |

The single highest-priority item is **2.2** (`PAPER_DRAFT.md` Table II, the actual manuscript, "Build weeks multiply the previous build volume") — this is the exact wording flagged in the task, it is now demonstrably inconsistent with the fixed implementation, and it is the only INCONSISTENT item that lives in the manuscript itself rather than an internal working/audit document. Every other INCONSISTENT item is in internal methodology/audit documents (`RESEARCH_METHODOLOGY_LOCK.md`, `PAPER_GAPS.md`, `EVIDENCE_MAP.md`, `RESEARCH_READINESS_AUDIT.md`, `ADVISOR_REVIEW_PACKAGE.md`, the `EVALUATION_CRITERIA_*` family, the two `RESEARCH_METHODOLOGY_*_PROPOSAL.md` files, `ADVISOR_DECISION_SHEET_COMPARATIVE.md`, and this session's own `CODE_AUDIT_EASY_RUN_PACE_AND_T7.md`) and follows the same pattern: a "fix-or-document, advisor decision pending" status that is now resolved, and (for the rebound specifically) a description of `current`-not-being-reset that is no longer true of the code.

**No wording has been changed by this audit.** All replacements above are proposals for you to apply (or amend) in a separate, explicit editing pass.
