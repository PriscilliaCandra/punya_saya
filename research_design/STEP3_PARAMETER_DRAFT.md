# Step 3 Parameter Draft (recommendations only)

**Prepared:** 2026-10-09, under the project owner's written authorization of this file (a new administrative file; the frozen v2.7 protocol does not specify its location or format).
**Baseline:** `SCENARIO_CONSTRUCTION_SPECIFICATION_v2_7_DRAFT.md` (sha256 `d5fcffad…82ca8`), frozen; `STEP2_OWNER_DECISIONS_RECORD.md` (OD-2, OD-3, OD-4 recorded).

## 0. Status of this file (read first)

- **This file is not the Parameter Justification Record (PJR)** and is not final. The PJR is finalized at step 5.
- **No candidate below is approved.** A value is a parameter of the study only after explicit written owner approval.
- This file **does not amend v2.7** and creates no methodology version.
- No model output, pilot content or Stage 1/2 response content was used. The only Stage 1/2 material read is `pilot_clarification/scenario_registry_stage2_v1.json` (design parameters), to find coincidences that §13.1 requires the PJR to flag.
- No registry, template, prompt or gate (`M*`, `Q*`, `PG*`, `A1`–`A7`) was built or run. The arithmetic in §4 uses only closed-form formulas of §12.1 and screening aids of §4–§5.5, on candidate values. This is not the step-4 dry run.
- Labels: **PROPOSED** (candidate with a protocol-based reason; still needs approval) · **OWNER DECISION REQUIRED** (substantive choice that I cannot justify from the protocol) · **DEFERRED** (the protocol assigns it to a later step, or it is computed from other values).
- None of the numbers has a literature source. Where a number rests on judgment, that is stated. Sources, if any, are for the owner to supply in the PJR.

## 0.1 Revision note (2026-10-11, owner-approved expository corrections)

Four mathematical-exposition corrections were applied on the owner's limited approval: (1) row 8 and §3 now separate the screening bound `m*` from the actual deviation `M`; (2) `M = 9` and the theoretical bound `60 − 2M = 42` are recorded with prerequisites, as candidate-specific, not global; (3) with `G_max = 349` enumeration gives 41 elements and, `L_P` being even, an operational limit of 40; 42 needs `G_max ≥ 350` and is a sensitivity analysis, not a decision; (4) §4 and §4.1 were updated, including the `hw*` feasibility statements. No candidate value was changed (`G_max`, `P`, `D_dist`, `τ_F`, `R_cap`, `N` unchanged) and nothing was approved. The `hw*` row now lists 0.20 and 0.25 as candidates awaiting final owner approval. OD-1 to OD-4 are untouched.

## 1. Four kinds of open item (kept apart)

| Kind | Items |
|---|---|
| **A. Methodology decisions for the owner** | OD-5 (shared vs per-family windows); whether to accept a PAC base list that is necessarily tight (§3); which distance `D_dist` the rule is about; the cap value `P` (familiarity threat); the model and settings (row 17); whether the budget `C_max` justifies the precision target. |
| **B. Numeric parameters to choose** | `P`, `N`, `ρ_NT`, windows, `D_dist`, `τ_F`, `S_list`, `G_list`, `X_min/X_max`, plausibility bounds, `C_max`, `R_min`, `R_cap`, `z`, level, `hw*`, `n_cells`, `n_boot`, `L_small`, pilot thresholds, blind-check coverage and delay. |
| **C. Values that exist only after calculation** | `n_M^req`, `n_P^req`, `C_req`, `L_M`, `L_P`, `R`, `N_tpl`, the DP6 mode outcome, `Xprev_max`, the coverage tier, the screening interval `[τ_lo, τ_hi)`, `𝒢_adm`. |
| **D. Deferred by the protocol** | Wording (row 20, step 7); seeds (row 16, step 11); DP9; OD-6; OD-7; PRD-4/5/6/8/10, PC-1/2 (still pending, §19.3). Step 6 freezes the final numbers. |

## 2. Candidate register (§17 rows)

Notation: "Freeze" is the step at which the protocol freezes the value. Step 3 selects drafts only.

| # | Parameter and protocol definition | Domain (protocol) | Step 3 or later | Candidate or range | Reasoning and effect | Depends on | Evidence still needed | Status |
|---|---|---|---|---|---|---|---|---|
| FX1/2 | `N` weeks (FIXED rule; value is researcher choice). `K = N−1` target positions `{2…N}`. | `N` odd, `N ≥ 5` (A2, OD-1 resolved); `N ≥ 2` for the DP6 divisor | Draft at 3, freeze 6 | **5** (alternative 7) | Calls `= 8·K·R·(n_M+2n_P)` grow linearly in `K` and `K` does not enter the worst-case precision bound (§12.2). `N = 5` is the cheapest admissible value (`K = 4`). The audit table of §9.3 reports zero measured interaction correlation at `L = 2K` (`L ≥ 8` for `K = 4`): finite check only. `N = 7` costs 1.5× and gives 6 target positions. | `K` enters cost | Owner's view of how many weeks is credible for the construct | **PROPOSED** (N = 5) |
| 1 | `P` mileage cap, integer percent | integer ≥ 1 (A5); cite a source; flag familiarity threat if a famous value (TH15) | 3 / 6 | **10** (famous; coincides with Stage 1/2) or another integer | `P = 10` is the best-known weekly increase rule: ecological, but a model may pattern-match instead of computing (TH15) and it coincides with the Stage 1/2 cap, which §13.1 requires to be flagged. A non-famous value (for example 12) avoids the cue but I can supply no source. `P` sets `U_M = P·S_min/100`, which controls MIL window reach. | `S_min`, windows | A citable source for the chosen cap; owner's stance on TH15 | **OWNER DECISION REQUIRED** |
| 3 | `ρ_NT`: normalized margin of non-target steps | rational `> 0` (A5(a)); two decimals by PJR convention; `ρ_NT < v_lo` is a screening aid only | 3 / 6 | **0.40** | Must give `m_NT ≥ 1` (RC-P4: `ρ_NT·τ_F ≥ D_dist + ½`) and `ρ_NT·U_M ≥ 1` (RC-M4). 0.40 satisfies both under the §4 candidates and lies below `v_lo`. It equals the arbitrary scratch value used in the spec's Appendix C, which proposed nothing; no other basis than feasibility and judgment. | windows, `τ_F`, `D_dist`, `P` | step-4 exact gates | **PROPOSED** |
| 4 | Windows `W_V, W_MILD, W_CLEAR` (shared or per family: OD-5) | positive rationals, `0 < lo ≤ hi`; for every declared set `v_hi < 1 < mi_lo` and `mi_hi < c_lo` (A5(c)); two decimals by PJR convention | 3 / 6 | Shared set: `W_V = [0.60, 0.90]`, `W_MILD = [1.10, 1.30]`, `W_CLEAR = [1.50, 2.00]` | Meaning: a valid target uses 60–90% of the allowed margin; MILD exceeds it by 10–30%; CLEAR by 50–100%. Satisfies A5(c) with gaps (0.90 < 1 < 1.10, 1.30 < 1.50). Satisfies the MIL and PAC guards and reach screens at the §4 candidates. Widths are chosen so the coarse PAC finish-time lattice (step `D_dist`) can reach them. Window placement is a researcher degree of freedom (§20): this choice rests on feasibility and domain meaning, not on any output. | OD-5, `τ_F`, `D_dist`, `P` | step-4 exact gates M2, M3, Q3, Q4 | **PROPOSED** (conditional on OD-5 = shared) |
| 5 | `D_dist` race distance (km) | positive rational with finite decimal expansion; `D_dist ≥ 3/2` screen | 3 / 6 | **10** (alternatives 5; 7.5; 21.0975) | `D_dist` is a construct choice (only this distance is studied, I-17). An integer makes `r = 0` and `rnd*` the identity, so the half-second rounding stage is not exercised in the data (the guard proofs still cover it). A non-integer exercises it. 21.0975 coincides with the Stage 2 half-marathon and gives lattice step 21 s, requiring `τ_F ≥ 105` at the §4 window widths. The lattice step `D_dist` also sets how finely PAC windows are realized. | `τ_F`, windows | Owner's choice of distance and whether rounding should be exercised | **OWNER DECISION REQUIRED** |
| 6 | `τ_F` finish-time tolerance (s) | positive integer (A4); screening interval `[τ_lo, τ_hi)` | 3 / 6 | **50** if `D_dist = 10` | Screening interval at the §4 candidates is `[50, 149]` (`τ_lo = D/ω_min = 50`). 50 is its lower end: it keeps the same-minute band widest (see row 8). Larger `τ_F` raises `m*` and shrinks the band. Must be recomputed if `D_dist` or the windows change. | `D_dist`, windows, `ρ_NT` | step-4 gates A4, Q2–Q6 | **PROPOSED** (conditional on `D_dist = 10`) |
| 7 | `S_list`: MIL start values, tenths of km, arithmetic progression of length `L_M = 2n_M` | positive progression (A3, A5(a)) | form at 3, values at 6 | `S_0 = 200` (20.0 km), `step_S = 10` (1.0 km) | Spacing is 5% of `S_min` and 2.5% across the list, so neighbouring bases are less alike than PAC bases. `S_max = 200 + 10(L_M−1)` must keep `Xprev_max·(1 + c_hi·P/100) ≤ X_max` (RC-M7). `L_M` is not known until DP4. | `n_M`, `P`, `X_max` | `L_M` from DP4; PJR spacing report (§17) | **PROPOSED** (form); values **DEFERRED** |
| 8 | `G_list`: PAC reference paces, s/km, progression of length `L_P = 2n_P` | positive progression; every element must pass all `Q*` (A3) | form at 3, values at 6 | `G_0 = 310` (5:10/km), `step_G = 1` | **Binding limit (candidate-specific; see §3).** The exact same-minute rule (Q7) uses the actual largest token deviation `M`, not the screening bound `m*`: every base is used in both directions, so `G mod 60 ∈ [M, 59−M]`. At the §4 candidates `M = 9`, giving a theoretical `L_P ≤ 60 − 2M = 42` for `0 < step_G < 60`. With the recorded candidate `G_max = 349` the enumerated list has 41 admissible elements; `L_P = 2n_P` must be even, so the operational limit is `L_P ≤ 40` (`n_P ≤ 20`). 42 could be considered only if `G_max ≥ 350` is chosen and passes all plausibility bounds and the feasibility gates (sensitivity, not a decision). Not a global limit. A larger step shortens the list. Relative spacing is `1/310 = 0.3%`, so **neighbouring bases are nearly identical and the effective number of independent clusters may be far below `L_P`** (§2.3); the PJR must report this and no effective size may be asserted. | `τ_F`, `D_dist`, windows | PJR spacing discussion; owner acceptance of the limitation (§3) | **OWNER DECISION REQUIRED** |
| 9 | `X_min, X_max` (tenths of km) | `X_min ≤ X_max`; RC-M5 single digit-width band | 3 / 6 | **100 and 999** (10.0–99.9 km) | Gate M7 forbids a pair crossing 9.9→10.0 or 99.9→100.0, and the band 10.0–99.9 km is one width. RC-M6 holds (`X_min ≥ 1/γ = 25`; tail `S_min·(1−γ)^{N−2} ≈ 177 ≥ 100`). **Coverage tier:** because `Xprev_max·(1 + c_hi·P/100) ≤ X_max = 999`, `Xprev_max < 1000` tenths, so the floor, ceiling and nearest 0.1 pp readings are **covered** (§6.1); whole-percent readings stay NOT COVERED. The PJR states the tier. | `S_list`, `P`, windows | `Xprev_max` from the final list | **PROPOSED** |
| 10 | Plausibility: `G_min, G_max, p_min, p_max, Tm_min, Tm_max` | A5 ordering and representational limits; Q11; "construction gates, not physiological truth" | 3 / 6 | `G_min = 300`, `G_max = 349`, `p_min = 270`, `p_max = 420`, `Tm_min = 2700`, `Tm_max = 4200` (conditional on `D_dist = 10`) | `G` band is the residue band 10–49 within minute 5 (§4). Pace range 4:30–7:00/km and time 45:00–70:00 for 10 km are broad recreational ranges. **Judgment only, no source.** | `G_list`, `D_dist` | owner confirmation; step-4 gate Q11 | **PROPOSED** (conditional) |
| 11 | `n_M, n_P` → `L_M, L_P`, `N_tpl` | by DP4–DP6 | 3 / 6 | – | Computed, not chosen. | rows 13–15 | approved inputs | **DEFERRED** |
| 12 | `R` | `R ≥ R_min ≥ 2`, by DP6 | 3 / 6 | – | Computed. | rows 13 | approved inputs | **DEFERRED** |
| 13a | `R_min` | integer ≥ 2 (A5(b)) | 3 / 6 | **2** | The minimum the protocol allows. `R ≥ 2` makes within-template consistency observable (DP7). Under the worst-case bound repetitions buy no precision, only cost (§12.2). | – | – | **PROPOSED** |
| 13b | `R_cap` | integer ≥ `R_min` | 3 / 6 | **2** (alternative 3) | Equal to `R_min`: surplus budget is not spent on repeats, which do not enter the bound. A higher cap only raises cost. `R_cap = 5` would coincide with the Stage 2 repetition count and must be flagged. | `R_min` | – | **PROPOSED** |
| 13c | `C_max` maximum calls | positive integer (A5(b)) | 3 / 6 | **no candidate** | A budget, not a methodological quantity. See the cost table (§4.1). It fixes whether precision mode is feasible (DP6). | model price, owner budget | provider cost per call, token counts, owner's ceiling | **OWNER DECISION REQUIRED** |
| 14a | Level and `z` | `z > 0`; level in (0,1) | 3 / 6 | **95%, `z = 1.96`** (alternative 90%, `z = 1.645`) | Conventional two-sided normal value, used in the §12.1 planning bound with DP2(i) (no multiplicity correction, per OD-4). It is a convention, not a derived value. | – | – | **PROPOSED** |
| 14b | `hw*` target half-width, single cell | `hw* > 0` | 3 / 6 | **0.20 or 0.25** (two candidates, neither selected; 0.15 and 0.10 not feasible at the current candidates) | Drives cost: `n^req = ⌈⌈(z/2hw*)²⌉ / 2⌉`. See §4.1. At 95%: `hw* = 0.20` gives `C_req = 25`, `n = 13`, `L = 26`; `0.25` gives `C_req = 16`, `n = 8`, `L = 16`; `0.15` gives `L = 44`, which exceeds the PAC limit of row 8 (40, or 42 if `G_max ≥ 350`); `0.10` gives `L = 98`, infeasible. Nominal only (worst case, independent clusters; optimistic under base similarity, §12.1, TH12). | `z`, row 8, `C_max` | owner's precision need | **OWNER DECISION REQUIRED** |
| 14c | `hw*` for contrasts | `hw* > 0` only if contrasts are designated | – | not applicable | OD-4: contrasts are exploratory, so no contrast `hw*` is needed. | OD-4 | – | **DEFERRED** (not applicable) |
| 14d | `n_cells` | declared under DP2(i) | 3 / 6 | **12** | The 12 primary cells (OD-4). | OD-4 | – | **PROPOSED** |
| 15a | `n_boot` | positive integer; "with citation" | 3 / 6 | **10,000** | A conventional order of magnitude. **I cannot supply a verified citation**; the PJR needs one. | – | citation | **PROPOSED** (citation missing) |
| 15b | `L_small` | positive integer | 3 / 6 | **10** | Below this many clusters, only counts and per-cluster proportions are reported (DP8). Judgment; the candidates give `L ≥ 26`, so it would not trigger. | – | owner view | **PROPOSED** |
| 16 | Execution-order and bootstrap seeds | from the decision record (§10) | step 11 | – | Rule is fixed; value is created by the decision script after the pilot. | – | – | **DEFERRED** |
| 17 | Model ID/version, system prompt, decoding, max tokens, timeout, delay, retries | researcher choice; no key in any artifact | 3 / 6 | – | Determines per-call cost and thus `C_max`. May inherit the Stage 2 provider-setting policy (not read here). | `C_max` | owner's model choice | **OWNER DECISION REQUIRED** |
| 18 | Pilot: `L_pilot` (even, ≥ 2, default 2); `f_S, θ_unp, c_stop, θ_main, calls_min_main`; `S_pilot, G_pilot` | `0 < θ_unp < 1`, `0 < θ_main < 1`, `c_stop ≥ 1`, `f_S ≥ 0`; pilot lists disjoint from the main lists | 3 / 6 | `L_pilot = 2`; for the thresholds an illustration only: `f_S = 1`, `θ_unp = 0.50`, `c_stop = 5`, `θ_main = 0.10`, `calls_min_main = 100` | These are catastrophe thresholds (§13.6). I have no basis for the numbers; they are placeholders for the owner to replace. `S_pilot`/`G_pilot` can be fixed only after the main lists, so they are open. | main lists | owner view | **OWNER DECISION REQUIRED** (thresholds); **DEFERRED** (pilot lists) |
| 19 | Blind-check coverage fraction and minimum delay | declared duration with the §11 criterion (no viewing of registry content or expected states in the interval) | 3 / 6 | coverage **100%** (default); delay: none proposed | OD-3 applies the delayed self-check. A duration of the order of days is typical, but I can give no justified number. | OD-3 | owner's duration | **PROPOSED** (coverage); **OWNER DECISION REQUIRED** (delay) |
| 20 | Wording, anti-cue list, parser normalizations, trigger list, claim insertion | content constraints | step 7 | – | Not a step-3 item. | – | – | **DEFERRED** |

## 3. Consequence of the PAC base-list limit (needs owner awareness)

For PAC, A3 plus the same-minute rule (Q7) bound the list. Two quantities must be kept apart:

- `m* = max(m_NT, ⌊(c_hi·τ_F + ½)/D_dist⌋)` is the **screening bound** of §5.5 (sufficient, possibly conservative; not a gate). At the candidates `m* = 10`.
- `M` is the **actual largest token deviation** (s/km) over the templates of the build; the exact Q7 condition is `sec_G ≥ M` and `59 − sec_G ≥ M`. With the construction rule `m_q = nearest(mid(W_q)·τ_F / D_dist)` (spec §9) the candidates give `m_V = 4`, `m_MILD = 6`, `m_CLEAR = nearest(8.75) = 9`, `m_NT = 1`, hence **`M = 9`** (realized ρ = 0.8, 1.2, 1.8, all inside their windows).

With `0 < step_G < 60` and all elements in one minute band, the theoretical bound is `L_P ≤ 60 − 2M = 42` (residues 9–50). Prerequisites: `D_dist = 10` (integer), `τ_F = 50`, the shared windows of row 4, `ρ_NT = 0.40`, each base used in both directions, and `M` computed from the construction rule above. If any of these change, `M` and the bound change; this is **not a global limit** for all parameter sets. Two independent computations (closed-form residue count; enumeration of every `G` in 300–349 over both directions and both classes) were run on scratch, outside the repository.

With the recorded candidate `G_max = 349`, enumeration gives 41 admissible elements (`G = 309…349`); the residue-50 value `G = 350` is excluded only by `G_max`. Because `L_P = 2n_P` is even, the **operational limit is `L_P ≤ 40`** (`n_P ≤ 20`). A limit of 42 could be considered only if `G_max ≥ 350` were chosen and passed all plausibility bounds and the step-4 feasibility gates. `G_max` is kept at 349 here; 40 versus 42 is a sensitivity analysis, not a decision. Larger `τ_F`, larger `c_hi` or smaller `D_dist` shrink the band (through `M`). The progression must also stay inside minute-width bands of 1 s/km spacing, so PAC bases are necessarily tightly spaced. Effects:

1. At the candidates, precision targets above `L = 40` are infeasible for PAC with `G_max = 349`, and above `L = 42` even with `G_max ≥ 350`, whatever the budget.
2. Even a feasible `L_P` has fewer effective independent clusters than `L_P` (§2.3, TH5); the nominal `hw*` is therefore optimistic for PAC in particular.
3. DP6 is evaluated on the required counts; it does not know about this limit. A request for `n_P^req > 20` would be rejected later by gate A3 (step 4), returning to step 3 with a logged rejected set (§21.2). Choosing `hw*` with this in view avoids that return.

## 4. Screening arithmetic on the candidates (not gates, not a dry run)

All values below are hypothetical inputs to closed-form formulas. They assume `P = 10` (placeholder, OWNER DECISION), `D_dist = 10`, `τ_F = 50`, `ρ_NT = 0.40`, the windows of row 4, `N = 5`.

- **PAC lattice:** `ω_min = 0.20`; `τ_lo = max(D/ω_min = 50, 1/(1−0.90) = 10, 1/(1.10−1) = 10, (D+½)/ρ_NT = 26.25, 1/0.60 = 1.67) = 50`; `τ_hi = (30·10 − ½)/2.0 = 149.75`. Integer interval `[50, 149]`; `τ_F = 50` inside.
- `m_NT = ⌊(0.4·50 − ½)/10⌋ = 1`; screening bound `m* = max(1, ⌊(2.0·50 + ½)/10⌋) = 10` (conservative residue band 10–49, width 40). Actual deviations: `m_V = 4`, `m_MILD = 6`, `m_CLEAR = nearest(1.75·50/10) = 9`, so `M = 9` and the exact band is 9–50, width 42 (see §3). The lattice value 100 s (`m = 10`) lies in `W_CLEAR` but is not selected by the midpoint rule.
- **Lattice points inside the windows** (`|x| = 10m`): valid {30, 40}; MILD {60}; CLEAR {80, 90, 100}. RC-P2 holds with equality for MILD (`(hi−lo)·τ_F = 10 = D_dist`): MILD has exactly one lattice value, a thin margin that step 4 will decide.
- **MIL:** `U_M = 20` tenths; reach `(hi−lo)·U_M = 6, 4, 10 ≥ 1`; guards `v_hi = 0.90 ≤ 0.95` and `mi_lo = 1.10 ≥ 1.05`; `ρ_NT·U_M = 8 ≥ 1`; `γ = 0.04`; tail `S_min·0.8847 ≈ 177 ≥ X_min = 100`.
- **A5(c)** on the shared set: `v_hi = 0.90 < 1 < mi_lo = 1.10`; `mi_hi = 1.30 < c_lo = 1.50`. This is an input check of the draft windows only.

### 4.1 Cost sensitivity (DP4 formula on hypothetical `hw*`; not a DP4–DP6 evaluation)

`L ≥ (z/(2hw*))²`, `n^req = ⌈C_req/2⌉`, `Calls = 8·K·R·(n_M + 2n_P)` with `n_M = n_P = n` and `R = R_min = 2`.

| Level / `z` | `hw*` | `C_req` | `n^req` | `L` | Calls, `N = 5` | Calls, `N = 7` | Within PAC limit (`L_P ≤ 40`; conditional, §3) |
|---|---|---|---|---|---|---|---|
| 95% / 1.96 | 0.10 | 96.04 → 97 | 49 | 98 | 9,408 | 14,112 | no |
| 95% / 1.96 | 0.15 | 42.68 → 43 | 22 | 44 | 4,224 | 6,336 | no |
| 95% / 1.96 | 0.20 | 24.01 → 25 | 13 | 26 | 2,496 | 3,744 | yes |
| 95% / 1.96 | 0.25 | 15.37 → 16 | 8 | 16 | 1,536 | 2,304 | yes |
| 90% / 1.645 | 0.10 | 67.65 → 68 | 34 | 68 | 6,528 | 9,792 | no |
| 90% / 1.645 | 0.15 | 30.07 → 31 | 16 | 32 | 3,072 | 4,608 | yes |
| 90% / 1.645 | 0.20 | 16.91 → 17 | 9 | 18 | 1,728 | 2,592 | yes |
| 90% / 1.645 | 0.25 | 10.82 → 11 | 6 | 12 | 1,152 | 1,728 | yes |

At 95%, with the recorded candidate `G_max = 349` (operational `L_P ≤ 40`, §3), the smallest `hw*` inside the PAC limit is about 0.155 (`C_req ≤ 40`). If `G_max ≥ 350` were chosen and passed all gates (sensitivity only; `L_P ≤ 42`), it would be about 0.1512. In both cases `hw* = 0.15` (`C_req = 43`, `n = 22`, `L = 44`) is **not feasible for the current candidate parameters**, and `hw* = 0.10` (`L = 98`) is not either. `hw* = 0.20` (`L = 26`) and `hw* = 0.25` (`L = 16`) are inside the limit and are the **two precision candidates awaiting the owner's final approval**; neither is selected. Because `L = 2n` can exceed `C_req`, the nominal half-width at the realized `L` is 0.1922 (`hw* = 0.20`) and 0.2450 (`hw* = 0.25`).

Counts are different things: *clusters* = bases `L` per family (the only quantity in the bound); *items* = templates (`N_tpl,MIL = 2K·n_M`, `N_tpl,PAC = 4K·n_P`; distinct prompts `= 4·N_tpl`); *model calls* = prompts × `R`; *observations* = one verdict per call, not independent units. The nominal half-width is a worst-case planning figure, not an achieved precision, coverage or power. No cost in currency is computed: model, provider, prices, token counts and `C_max` are not decided; `C_max`, `n_M` and `n_P` stay non-final.

## 5. OD-5: shared or per-family windows

Protocol basis: §2.4 and §6.2 make shared windows the default; per-family windows are used only if "a family cannot realize them", and are then "a recorded degree of freedom". OD-5 is due at step 3 and depends on the dry run (step 4). `A5(c)` applies to each declared set separately and does not decide OD-5.

| | Shared windows (initial preference) | Per-family windows |
|---|---|---|
| Comparability across families | Same ρ intervals for MIL and PAC, so the class labels MILD/CLEAR mean the same normalized margin. §3.5 still says equal ρ does not imply equal difficulty, and no primary analysis compares classes across families (TH8). | MILD/CLEAR mean different ρ ranges per family; the labels are less comparable, but no cross-family comparison is planned. |
| `A5(c)` | Checked once. | Checked twice, once per set. No condition relates the two sets. |
| Mathematical feasibility | Must satisfy both families' realizability simultaneously: MIL reach `(hi−lo)·P·S_min/100 ≥ 1` and guards `v_hi ≤ 1 − 1/U_M`; PAC reach `(hi−lo)·τ_F ≥ D_dist` and `v_hi ≤ 1 − 1/τ_F`, `τ_F < (30·D_dist − ½)/c_hi`. A joint solution exists iff an integer `τ_F` lies in `[τ_lo, τ_hi)`, which needs roughly `ω_min > c_hi/30` (0.067 for `c_hi = 2`). At the candidates it does (§4). | Lets PAC use wider windows to cope with the lattice while MIL keeps narrow ones; useful only if shared sets fail the step-4 gates. |
| Interpretation risk | Windows tuned to PAC's coarse lattice are also applied to MIL, where they are finer than necessary. | More researcher degrees of freedom (§20): the windows differ by family and could be (or look) tuned to feasibility; the PJR must justify each. |
| What is still needed | The step-4 numeric gates (M2, M3, M11, Q3, Q4, Q12) on the actual register: only they decide admissibility. The thin MILD lattice (one value at `D_dist = 10`, `τ_F = 50`) is the likeliest failure point. | The same, per family. |

Recommendation (not a decision): select shared windows now, as the protocol's default, and state in advance that a step-4 failure returns to step 3 under §21.2 and is **not** answered by switching automatically. Switching to per-family windows would then be a new owner decision, recorded with the failing gate.

## 6. A5(b) domain precheck on the candidate draft (§21.1 step 3, item (i))

The check uses the candidates of §2; it is **conditional**, not an evaluation of the approved register.

| Quantity | Candidate | Domain | Result |
|---|---|---|---|
| `N` (denominator precheck, `K = N−1 ≥ 1`) | 5 → `K = 4` | integer ≥ 2 | pass |
| `z` | 1.96 | `> 0` | pass |
| level | 0.95 | in (0,1) | pass |
| `hw*` (single) | 0.20 (OWNER DECISION) | `> 0` | pass if chosen; no value approved |
| `C_max` | none | positive integer | **cannot be evaluated** |
| `R_min`, `R_cap` | 2, 2 | `R_min ≥ 2`, `R_cap ≥ R_min` | pass |
| `n_boot`, `L_small` | 10,000; 10 | positive integers | pass |
| contrast `hw*` | not applicable (OD-4) | – | not needed |

`A5(b)` is therefore **incomplete** because `C_max` has no value. As the protocol orders `A5(b)` before DP4, **DP4–DP6 were not evaluated and no claim is made that they are satisfied**. No value was substituted. The numeric-stage `A5(a)` and `A5(c)` are step-4 checks and were not run, other than the input observation in §4.

## 7. PJR flags noted so far (§13.1)

Candidate or option values that coincide with Stage 1/Stage 2: `P = 10`; `D_dist = 21.0975` (if chosen); `R_cap = 5` (if chosen). `ρ_NT = 0.40` coincides with the arbitrary scratch value in the spec's Appendix C, not with a Stage 1/2 value. `P = 10` also carries the familiarity threat of TH15.

## 8. What the owner must decide, in this order

1. `C_max`, with the model choice (row 17), since cost per call is needed.
2. `hw*` (and level), with §3 and §4.1 in view.
3. `D_dist`, then `τ_F` (recomputed if `D_dist` changes).
4. `P` (cap value and the TH15 stance).
5. OD-5.
6. Acceptance of the PAC base-list limitation (§3).
7. Pilot thresholds and the blind-check delay.
8. Approval, in writing, of each candidate marked PROPOSED.

Nothing here has been frozen or approved. Step 4 has not been run.
