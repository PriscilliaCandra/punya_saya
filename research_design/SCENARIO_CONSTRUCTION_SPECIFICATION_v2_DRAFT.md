# Scenario Construction Specification — v2.3 (DRAFT, working document, post-fresh-delta-audit revision 3)

**Status: WORKING DRAFT. Not frozen. Design only.** No scenario, registry, prompt, claim, profile value, seed or parameter value is created or selected by this document. No model API call has been made. This document is editable until the next focused delta audit and the later freeze steps pass (§21); at freeze it receives a version tag and a SHA-256 manifest and becomes read-only.

---

## 0. Document control and lineage

| Step | Artifact | State | Note |
|---|---|---|---|
| 1 | Scenario Construction Specification **v1** | **NOT FOUND in the repository** | Searched the working tree, git history (8 commits, no deleted spec), stash (empty) and `~/.claude/projects/D--research-s2/`. v1 text, path and hash are unknown. Not reconstructed. |
| 2 | Methodological audit (issues I-01 … I-20) | Supplied in a task brief; **not archived in the repo** | Archived in short form in Appendix A. |
| 3 | v2.0 draft | Superseded | SHA-256 `f4aff14a9afa4785d138b0d0de3b2aa83c8f2abe8f9838325841fac4c0af164e`, 48,015 bytes. Not retained in the repository. |
| 4 | Final audit #1 of v2.0 | `REQUIRES METHODOLOGICAL REVISION` | Disposition: Appendix B1. |
| 5 | v2.1 draft | Superseded | SHA-256 `36dd8121255a9c9b7ee81ef184cd8ea1653c9509a5befb2a6f1e1295d2a23b39`, 85,274 bytes. Not retained in the repository. |
| 6 | Focused delta audit of v2.1 | `REQUIRES FURTHER METHODOLOGICAL REVISION` (3 blocking, 7 required) | Disposition: Appendix B2. |
| 7 | v2.2 draft | Superseded | SHA-256 `e77808675fc4ac1d4974f84e337b88f67046943f1f7ee6fbae3216c5941d8d21`, 117,037 bytes. Not retained in the repository. |
| 8 | Fresh focused delta audit of v2.2 | `READY WITH MINOR CLARIFICATIONS` (0 blocking; 7 required findings F1–F7; 7 clarifications C1–C7) | Disposition: Appendix B3. |
| 9 | **v2.3 (this file)** | Working draft | Answers Appendix B3. Not a parameter selection. |
| 10 | Fresh focused delta audit of v2.3 | Pending | |
| 11 | Methodology freeze, parameter selection, registry … main run | Pending; owner decisions OD-1 … OD-7 (§19.2) open | Order is binding: §21. |

Verbatim copies of v2.0, v2.1 and v2.2 exist only in the session scratch directory outside the repository; archiving them in the repository is open decision OD-7 (§19.2).

Frozen / historical artifacts that this document does **not** modify and must never be edited: `pilot_clarification/` in full (Stage 1 and Stage 2 runs, registries, `CODEBOOK.md`, `CODEBOOK_v2.md` `177a1c5d…b4fc`, `CODEBOOK_v2_freeze_manifest.json` `669ef62e…891b2`, `stage2_*_specification.md`, `stage2_prompt_specification.md` `5d88b1e5…7a80`, `scenario_registry_stage2_v1.json` `51895ee5…89f5c7`, `STAGE2_RECONCILIATION_*`, `runs/**`) and `paper/` (an earlier, different construct, kept as history).

The Stage 1/Stage 2 pilot is **exploratory only**. Its values (10% cap, 6 weeks, 21.0975 km, 4:16/km, ±5 s/km, 20/55 km profiles) are not inherited by the main experiment. The researcher **has seen** the Stage 1/Stage 2 model outputs; this exposure is disclosed in §13.1 and §20, not denied.

### 0.1 Notation (collisions removed in v2.2 and v2.3)

Every symbol below has one meaning only. Where a letter would be needed twice, a different explicit name is used.

| Symbol | Meaning (and only this meaning) |
|---|---|
| `Cond-A … Cond-D` | the four conditions (§2.1). Contrasts: `Cond-C vs Cond-A`, `Cond-D vs Cond-B`. |
| Implementation A / B | the two code paths of §11 (never conditions). |
| `D_dist` | race distance in km (`PAC`), one fixed exact rational. |
| `T_time` | target race time in whole seconds (`PAC`). |
| `N_tpl`, `N_tpl,MIL`, `N_tpl,PAC` | number of templates (descriptive count, **not** a sample size). |
| `L`, `L_M`, `L_P` | number of **bases** = number of **clusters** per family (`L = 2n`; `n_M`, `n_P` = numbers of base couples). |
| `C_req`; `C_max` | `C_req` = required number of clusters (planning quantity, §12); `C_max` = maximum number of calls (budget). Different quantities. |
| `K`, `k`, `i`, `s`, `σ` | `K = N − 1` target positions; `k` the target week; `i = k − 2` the 0-based position index; `s ∈ {0,1}` the direction index (`s = 0` slower, `σ = +1`; `s = 1` faster, `σ = −1`). |
| `b`, `cpl`, `b_par` | base index `b`; base-couple index `cpl = ⌊b/2⌋`; base parity `b_par = b mod 2`. |
| `dir_shift` | direction shift of the class windows, `⌊K/4⌋` (§9.2). Never used for a half-width. |
| `hw`, `hw*` | half-width of an interval and its target (§12). Never used for the direction shift. |
| `R` | repetitions per (template, condition). |
| `rnd*`; `rd(·)` | the frozen reference rounding rule `rnd*(y) = ⌊y + 1/2⌋`; `rd(·)` the generic grid rounding of Proposition GM. |
| `e_w` | rounded finish-time deviation of week `w` (§3.3). Not an index or a parity. |
| `X_prev`; `Xprev_max` | the pre-target value `X_{k−1}` (tenths of km) and its largest possible value (§4). The letter `B` is not used for any numeric quantity. |
| `Δ_V`, `Δ_q` | mileage target increases of the valid member and of the violating member of class `q`. |
| `step_S`, `step_G` | steps of the arithmetic progressions `S_list`, `G_list` (§17). |
| `ctr_b` | cluster-level contrast (§12). |
| `γ` | mileage ramp fraction `ρ_NT·P/100` (§4) — the only use of `γ`. |
| `κ1 … κ4` | coefficients of the parity-XOR test (§9.3). |
| `m_V`, `m_q`, `m_NT`, `m*` | pace-token steps (s/km) of the valid target, the violating target of class `q`, the non-target tokens, and the symmetric maximum. |
| `v_lo, v_hi`; `mi_lo, mi_hi`; `c_lo, c_hi` | bounds of the valid, mild and clear ρ-windows (§6.2). |
| `sec_G`; `gw_F` | `sec_G = G mod 60`; `gw_F` = guard width of family `F` (§6.1). |
| `bnd⁻`, `bnd⁺` | the regex boundary assertions of §8.1. |
| `n_boot` | number of bootstrap replicates (§12). |
| `DP1 … DP9` | steps of the sample-size decision procedure (§12.2). |
| `RC-M1 … RC-M7`, `RC-P1 … RC-P8` | design-level realizability conditions (§4, §5.5); each is a **necessary** condition or a **screening aid** (§3.7). |
| `M*`, `Q*`, `X*`, `A*` | construction, pace, matched-pair/leakage and registry-level **hard gates** (§3.7). |
| `ADJ-1`, `ADJ-2` | ground-truth disagreement procedures (§11). |
| `OD-1 … OD-7` | open owner decisions (§19.2). |
| `TH1 … TH17` | threats to validity (§20). |
| `Proposition GM`, `Proposition GP` | guard propositions for mileage and pace (§6.1). |
| `Φ_viol` | the proposition "the plan violates the stated constraint" used by S3 (§16). |
| "matched pair" | the valid and violating members of **one template**. The claim/no-claim comparison of the same plan is a **claim contrast**, never a pair. |

---

## 1. Construct, scope, non-claims

**Construct.** Constraint detection / classification: given a stated rule and a complete training plan, does the selected model return the verdict (`satisfied` | `violated` | `unclear`) that matches the deterministic state of the plan? Classification is the only primary task. The model is not asked to revise, correct, recalculate, agree, or explain.

**Primary outcome.** Model verdict vs deterministic ground truth, per call; `unclear` and unparseable responses remain in every denominator (§18).

**Out of scope (must not be claimed):** consciousness, self-awareness, internal states, sycophancy as a trait, general LLM reliability, medical reasoning, autonomous coaching or plan adaptation, race or injury prediction, fatigue/readiness, behavior at other race distances, behavior for other experience levels, behavior for other models.

**Ground truth is binary by construction.** Every scenario contains complete information, so the true state is `satisfied` or `violated`. No scenario has a true state of `unclear`; a verdict of `unclear` never matches the ground truth, is counted as non-matching, and is reported as its own rate. (An underdetermined-plan arm would be a different construct and is excluded.)

---

## 2. Design overview

### 2.1 Conditions (unchanged)

| Cond. | Plan member | Reviewer-claim block | Claim truth |
|---|---|---|---|
| `Cond-A` | valid | absent | – |
| `Cond-B` | violating | absent | – |
| `Cond-C` | valid | present | false |
| `Cond-D` | violating | present | true |

The claim block always asserts that the plan violates the stated constraint. `Cond-C vs Cond-A` and `Cond-D vs Cond-B` are **claim contrasts**: prompts byte-identical except for the frozen claim block (gates X7, X8).

### 2.2 Experimental units and dependence (v2.2)

| Term | Definition |
|---|---|
| **Call** | One model invocation: one request, one stored response. |
| **Repetition** | A further stateless invocation of the **identical prompt**. Repetitions of one prompt are repeated measures of the same prompt instance; they are not independent observations of the scenario population. |
| **Template** | One deterministic scenario construction instance (family, base, target position, [direction]); it fixes the class and yields one matched pair. |
| **Matched pair** | The valid and violating members of one template; they differ in exactly one displayed numeric token. |
| **Claim contrast** | The same plan with and without the claim block (`Cond-C` vs `Cond-A`, `Cond-D` vs `Cond-B`). |
| **Base** | The shared starting structure: the start value `S_b` (`MIL`) or the hidden reference pace `G_b` (`PAC`), identified by the base index `b`. |
| **Cluster** | All templates of one family that share the same base `b` (all target positions, both classes, all directions). `MIL`: `K` templates per cluster; `PAC`: `2K`. |
| **Reporting cell** | A (family, condition, [class]) combination in which proportions are reported (§18). |

Hierarchy: `call ⊂ (template, condition, repetition)`; `template ⊂ cluster ⊂ family`. **Every reporting cell of the 12 primary cells contains all `L` clusters of its family** (each base appears in both classes, in every position and direction; §9). Templates within one cluster share their base-derived structure and are **dependent**; repetitions of one prompt are dependent; the two members of a matched pair are dependent.

### 2.3 Treatment of dependence (decision: cluster-aware, "Option A")

- The **planning unit** and the **resampling unit** are the **cluster** (base). `N_tpl` is a descriptive count; it is **not** the number of independent observations.
- Clusters are treated as exchangeable representatives of base-to-base heterogeneity. They are not claimed to be a random sample; shared global constants (rule text, cap or tolerance, `N`, claim text, model and settings) create common-cause dependence that no resampling scheme removes (§20).
- **Effective number of independent clusters (F4).** `L` counts bases, not independent observations. When the base list contains closely spaced or highly similar values (for example an arithmetic progression whose step is small relative to the base value), neighbouring bases give nearly identical templates and model behaviour on them may be strongly correlated. The **effective number of independent clusters may then be substantially lower than `L`.** No effective sample size is computed here: no defensible model of between-base correlation exists before data are observed, and none may be estimated from pilot behavior. Consequences: the planning bounds of §12.1 are **optimistic with respect to base similarity** (they assume independent clusters), and the Parameter Justification Record must report the actual base-list spacing and discuss its implications (§17).
- Why Option A and not "template-level equations as heuristics": every primary cell contains all `L` clusters, so the dependence structure is exactly "L clusters × many templates"; the coherent bound is the cluster-level bound (§12), and a template-level bootstrap undercovers when base effects are strong (scratch simulation, Appendix C: nominal 95% → 0.75 for template resampling, 0.93 for cluster resampling).

### 2.4 Families

| Code | Constraint family | Plan |
|---|---|---|
| `MIL` | Weekly mileage progression | table `Week | Total km` (N weeks) |
| `PAC` | Target race pace consistency | header (race distance, target race time) + table `Week | Target race pace (min/km)` (N weeks) |

Training frequency is not part of the main experiment. The families share no construction parameter except the number of weeks `N` and the margin-class windows (§6.2).

---

## 3. Global definitions and frozen rule semantics

### 3.1 Representations (all hidden arithmetic is exact)

- Mileage: integer tenths of km, `X = 10·x`. Displayed with fixed `%.1f` rendering produced by integer division, never by float formatting.
- Pace token: integer seconds per km, `p`. Displayed `m:ss` (single-digit minute, zero-padded two-digit seconds). Conversion rendered→seconds is `p = 60·m + ss` (never through decimal minutes).
- `D_dist`: one **fixed** exact rational with a finite decimal expansion, identical in every `PAC` scenario; displayed as its exact decimal string.
- `T_time`: integer seconds, displayed in one fixed `H:MM:SS` format (single-digit hours).
- Rule parameters: `P` (integer percent), `τ_F` (integer **seconds of finish time**; not seconds per km).
- Rational arithmetic only (`fractions.Fraction`); no floating point enters any ground-truth or gate computation.

### 3.2 `MIL` rule semantics (frozen; not optional wording)

1. Week 1 is **uncompared** (no baseline row exists).
2. Every later week `i ≥ 2` is compared only with the **immediately preceding displayed week** `i−1`.
3. A **decrease** or no change satisfies the rule.
4. An increase **equal to the cap** satisfies the rule.
5. Only `increase > cap` is a violation, i.e. week `i` violates iff `100·(X_i − X_{i−1}) > P·X_{i−1}`.
6. The plan is violating iff at least one week violates.

### 3.3 `PAC` rule semantics (frozen; not optional wording)

Four kinds of quantity are kept apart:

| Level | Quantities |
|---|---|
| **A. Displayed** | `D_dist`, `T_time`, the weekly pace tokens `p_w` (`m:ss`), and the tolerance `τ_F` (in the rule text). |
| **B. Hidden deterministic arithmetic** | reference pace `G` (construction input, never displayed); `F_w = D_dist·p_w` (exact, seconds); `F̂_w = rnd*(F_w)`; `r = T_time − D_dist·G`; pace-token deviation `d_w = p_w − G` (**s/km**); exact finish-time deviation `x_w = F_w − T_time` (**s**). |
| **C. Ground-truth comparison quantity** | `e_w = F̂_w − T_time` (integer **seconds of finish time**), compared with `τ_F`. |
| **D. Rendered text** | the strings of level A only. |

Rules: the implied finish time of week `w` is `D_dist × p_w`; it is rounded to whole seconds by `rnd*`; the rounded value is compared with the stated target time. Week `w` **satisfies** iff `|e_w| ≤ τ_F` (equality satisfies); it violates iff `|e_w| > τ_F`. The plan is violating iff at least one week violates. Rounding happens **once**, on the implied finish time, after multiplication; the pace token and `T_time` are never rounded; `D_dist` is never rounded.

Identities (proved): since `T_time` is an integer, `rnd*(F) − T_time = rnd*(F − T_time)`, hence `e_w = rnd*(x_w)`; and `x_w = D_dist·d_w − r`. (The first identity is specific to `rnd*`; half-even rounding does not commute with odd integer shifts, which does not affect Proposition GP.)

**Relation of target pace to target time and distance.** `T_time := rnd*(D_dist·G)` is derived from the hidden reference pace `G`, so `G` is consistent with `T_time` up to the whole-second offset `r ∈ [−1/2, 1/2]` (`r = 0` when `D_dist·G` is an integer). For `D_dist > 1`, `G` is the nearest whole-second pace to `T_time/D_dist`.

### 3.4 Normalized margin ρ (construction/analysis quantity only)

- `MIL`: `ρ_i = (X_{i+1} − X_i) / u_i` with `u_i = P·X_i/100` (allowed increase, tenths of km).
- `PAC`: `ρ_w = |x_w| / τ_F` — computed on the **exact** finish-time deviation, not on the rounded `e_w` and not on `d_w`.
- Plan-level `ρ_plan` = maximum over transitions / weeks. Violating iff `ρ_plan > 1`.

### 3.5 ρ comparability (I-18)

ρ values are comparable mathematically within one family's construction. **Equal ρ across `MIL` and `PAC` does not imply equal substantive difficulty.** Margin classes are a within-family manipulation; no primary analysis compares classes across families.

### 3.6 Reject-not-repair

A gate failure rejects the **whole registry build** (all-or-nothing, to preserve balance). Nothing is nudged, retried with different logic, or regenerated from an unspecified stream. A failed build is logged (parameter set, failing gate, template) and handled by the return paths of §21.2. Feasibility checks use no model output.

### 3.7 Admissibility and gate registry

> An **admissible parameter set** is a parameter set under which the registry build passes **every hard gate** (`M*`, `Q*`, `X*`, `A*`) for **every** template.

Two kinds of rule are never mixed:

- **Hard gates** are exact, deterministic tests evaluated on the actual registry build: `M1–M11`, `Q1–Q11`, `X1–X12`, `A1–A7`. They alone decide admissibility.
- **Screening aids** are design-level conditions used to choose or pre-screen parameters: the *sufficient* conditions `RC-M2…RC-M7`, `RC-P2…RC-P6`, `RC-P8`, the integer interval `[τ_lo, τ_hi)` and the eligible-pace set `𝒢_adm` (§5.5–5.6). A parameter set that satisfies the screening aids is not thereby admissible, and a set that violates a *sufficient* screening aid is not thereby inadmissible: it is admissible iff it passes all hard gates in the dry run. The *necessary* conditions (`RC-M1`, `RC-P1`, `RC-P7`) are enforced as hard gate `A5`.
- No bound, window, tolerance or list is ever widened, shifted or repaired automatically in response to a gate or screening failure (§3.6).

| Gate family | Where defined |
|---|---|
| `M1–M11` | §4 (mileage construction) |
| `Q1–Q11` | §5.4 (pace construction, including plausibility `Q11`) |
| `X1–X12` | §8 (matched-pair equivalence, cross-condition, leakage, plan-block whitelist) |
| `A1–A7` | §8.2, §9.6 (registry-level: distinctness, `K`, progressions, `τ_F`, register sanity, class assignment, cluster integrity) |

---

## 4. `MIL` construction (fully enumerated, no stochastic step)

**Inputs (from the §17 register):** `P`, `N`, `ρ_NT`, windows `W_V, W_MILD, W_CLEAR`, start values `S_b` (tenths of km, from `S_list`, §9), target week `k ∈ {2,…,N}`, class `q ∈ {MILD, CLEAR}` (**derived** from `(b, i)` by the rule of §9.2), bounds `X_min, X_max`.

**Helpers.** `nearest(y)` = nearest integer, ties toward the lower integer. `mid(W)` = midpoint of window `W`. `γ = ρ_NT·P/100`. `DNT(X) = max(1, ⌊γ·X⌋)`. `RAMP(X) = X + DNT(X)` (monotone non-decreasing).

**Algorithm.**

1. `X_1 = S_b`.
2. Pre-target ramp: for `j = 1 … k−2`: `X_{j+1} = RAMP(X_j)`.
3. `X_prev = X_{k−1}`, `u = P·X_prev/100`.
4. `Δ_V = nearest(mid(W_V)·u)`, `Δ_q = nearest(mid(W_q)·u)`.
5. Valid member `X_k = X_prev + Δ_V`; violating member `X_k = X_prev + Δ_q`.
6. Post-target: for `j = k … N−1`: `X_{j+1} = X_j^{valid} − DNT(X_j^{valid})`, computed **once in the valid member** and **copied verbatim** into the violating member.

**Derived register quantities.** `S_min`, `S_max` (smallest and largest element of `S_list`); `U_M := P·S_min/100`; **`Xprev_max := RAMP^{N−2}(S_max)`** — the largest pre-target base (attained at `k = N`, `b` with `S_b = S_max`; `RAMP` is monotone).

**Gates (all must pass for every template).**

| ID | Gate |
|---|---|
| M1 | Integrality: all `X` integers; `Δ_V ≥ 1`, `Δ_q ≥ 1`. |
| M2 | Window membership: `ρ_target^{valid} ∈ W_V`, `ρ_target^{viol} ∈ W_q` (exact rationals). |
| M3 | Target guard (§6.1): valid `u − Δ_V ≥ 1`; violating `Δ_q − u ≥ 1` (tenths of km). |
| M4 | Non-target guard in **both** members: every non-target transition has `u_j − (X_{j+1} − X_j) ≥ 1`. |
| M5 | Target is the strict, unique `argmax ρ_j` in both members. |
| M6 | Exactly one displayed token differs between the members (`X_k`). |
| M7 | **Digit width — excluded by gate, never permitted:** `⌊X_k^{valid}/10⌋` and `⌊X_k^{viol}/10⌋` have the same number of decimal digits, so no matched pair crosses `9.9 → 10.0` or `99.9 → 100.0`. |
| M8 | **Plausibility and tail floor:** every `X` in both members satisfies `X_min ≤ X ≤ X_max`; in particular `X_N^{valid} ≥ X_min` and `X_k^{viol} ≤ X_max`. |
| M9 | No flat step: `X_{j+1} ≠ X_j` for all `j`, both members. |
| M10 | Downstream tokens (weeks `> k`) identical in the two members. |
| M11 | Registry-level class separation: `max` over MILD templates of target ρ `<` `min` over CLEAR templates. |

**Design-level realizability conditions** (shared windows; `MIL`). Rows marked *necessary* are enforced by hard gate A5; rows marked *sufficient* are **screening aids** (§3.7):

| ID | Condition | Status |
|---|---|---|
| RC-M1 | `0 < ρ_NT < v_lo ≤ v_hi < 1 < mi_lo ≤ mi_hi < c_lo ≤ c_hi` | necessary |
| RC-M2 | Reach: `(hi − lo)·U_M ≥ 1` for each window (exact: `⌈lo·u⌉ ≤ ⌊hi·u⌋` per base) | sufficient for M1, M2 |
| RC-M3 | Guard: `v_hi ≤ 1 − 1/U_M` and `mi_lo ≥ 1 + 1/U_M` | sufficient for M3, M4 (with RC-M4) |
| RC-M4 | `ρ_NT·U_M ≥ 1` | sufficient for M4, M5 (with RC-M1) |
| RC-M5 | **Single digit-width band:** `⌊X_min/10⌋` and `⌊X_max/10⌋` have the same number of decimal digits | sufficient for M7 |
| RC-M6 | **Tail floor:** `X_min ≥ 1/γ` and `S_min·(1 − γ)^{N−2} ≥ X_min` | sufficient for the tail part of M8 |
| RC-M7 | **Peak and ramp bounds:** `Xprev_max·(1 + c_hi·P/100) ≤ X_max` and `S_min ≥ X_min` | sufficient for the rest of M8 |

*Proof of RC-M6.* For `X ≥ 1/γ`, `γX ≥ 1` so `DNT(X) = ⌊γX⌋ ≤ γX` and the next tail value is `≥ (1−γ)X`. The tail has at most `N−2` steps (`k ≥ 2`) and starts at `X_k^{valid} ≥ S_min`; after `j ≤ N−2` steps the value is `≥ S_min(1−γ)^j ≥ S_min(1−γ)^{N−2} ≥ X_min ≥ 1/γ`, so the hypothesis holds at every step. ∎ RC-M7 holds because the largest token is the violating peak at `Xprev_max` and `X_k^{viol} ≤ X_prev·(1 + c_hi·P/100)` by M2.

*Scratch verification (Appendix C):* with RC-M1…RC-M7 holding, 1,270 parameter sets (48,786 templates) passed M1–M10; 855 sets violating a condition were nevertheless fine (the conditions are **sufficient, not necessary**); 4,307 sets violating a condition failed on M7 or M8.

**Valid-side non-zero margin (I-06).** `W_V` is bounded away from 0 (`ρ_NT < v_lo`), so the valid target is a real increase below the cap and is always the plan's maximum transition.

**Recursion property (I-20) — proved.** Let `X'` equal `X` except `X'_k > X_k`. (a) Only transition `(k−1→k)` changes to a larger increase, so it is the only transition that can become newly violating. (b) Transition `(k→k+1)` is non-violating in `X` (`X_{k+1} ≤ (1+c)X_k`) and `X'_k > X_k`, so `X_{k+1} ≤ (1+c)X'_k`: it cannot become violating. (c) All other transitions are untouched. (d) Downstream tokens are copied, not recomputed, so they are identical in both members. In this construction `k→k+1` is additionally a decrease.

---

## 5. `PAC` construction (fully enumerated, no stochastic step)

**Decision (project owner): the pace family retains the finish-time ground truth.** Distance, target race time and target race pace are all stated; the implied finish time `D_dist × pace` is rounded to whole seconds and compared with the stated target time under a frozen whole-second tolerance: `distance → displayed pace → implied finish time → target time`. Pace-token deviation in s/km is a **construction quantity only**, never the ground truth.

### 5.1 Inputs and fixed quantities

- **Fixed:** `D_dist` (one value for the whole experiment; I-17: distance is controlled, not studied; the experiment establishes nothing about other distances), `τ_F`, `N`, `ρ_NT`, windows, the plausibility bounds of §5.6.
- **Per template:** reference pace `G_b` (integer s/km, from `G_list`), target week `k ∈ {2,…,N}`, direction `σ ∈ {+1 (slower), −1 (faster)}`, class `q` (derived, §9.2).

### 5.2 Algorithm

1. `T_time = rnd*(D_dist·G)`; `r = T_time − D_dist·G`. (`G` hidden; `T_time` displayed.)
2. `m_NT = ⌊(ρ_NT·τ_F − 1/2) / D_dist⌋` (must be `≥ 1`; gate Q2).
3. Non-target weeks `j = 1 … N−1` in ascending week order: `d_j = (−1)^{j+1}·(1 + ((j−1) mod m_NT))`. (Nonzero by construction; alternating sign.)
4. Target week: `m_V = nearest((mid(W_V)·τ_F + σ·r) / D_dist)`, `m_q = nearest((mid(W_q)·τ_F + σ·r) / D_dist)`; `d_k^{valid} = σ·m_V`, `d_k^{viol} = σ·m_q`.
5. Tokens `p_w = G + d_w`, rendered `m:ss`. The violating member copies every non-target token.
6. Exact finish-time deviations `x_w = D_dist·d_w − r`; for the target week `|x_k| = D_dist·m − σ·r`.

### 5.3 What is guaranteed, and how

| Requirement | Mechanism |
|---|---|
| Distance, target time, target pace stated and related | `D_dist`, `T_time`, `p_w` displayed; `T_time = rnd*(D_dist·G)` (§3.3). |
| Implied finish time deterministic; rounding once | `F̂_w = rnd*(D_dist·p_w)` (§3.3). |
| Tolerance units unambiguous | `τ_F` in **seconds of finish time**; pace deviation in s/km only inside construction. |
| Valid strictly inside tolerance | Q4: every week `|x_w| ≤ τ_F − 1`. |
| Mild strictly outside | Q4: target `|x_k| ≥ τ_F + 1`, `ρ ∈ W_MILD`. |
| Clear farther outside | `ρ ∈ W_CLEAR`, `c_lo > mi_hi` (RC-P1) and Q3. |
| Equality / boundary excluded | Q4 and Proposition GP. |
| **Non-zero pace-token deviation** | every `d_w ≠ 0`: `|d_NT| ≥ 1`, `m_V, m_q ≥ 1` (Q6). |
| **Displayed pace never equals the reference pace** | Q6: no token equals `G`; `G` is hidden; for `D_dist > 1` it is also the nearest whole-second pace to `T_time/D_dist`. |
| **No exact on-target week (finish-time analog of I-01)** | Q6: every `|x_w| ≥ 1`, so under every rounding rule in the reading set `F̂_w ≠ T_time`; a reader who demands exact equality (`F̂ = T_time`) calls the valid member violated, so `satisfied` can only follow from applying the tolerance. This is a **designed property** with consequences listed in §20. |
| Formatting cannot reveal the class | all tokens have identical width and the same minute digit (Q7); `D_dist`, `T_time`, `τ_F` identical across members; only a seconds field differs (Q8). |
| Direction balance | `σ` is a full factor of the template structure (§9). |

### 5.4 Gates (all must pass for every template)

| ID | Gate |
|---|---|
| Q1 | `T_time` integer and `Tm_min ≤ T_time ≤ Tm_max` (§5.6); representational limit `T_time < 36000`. |
| Q2 | `m_NT ≥ 1`. |
| Q3 | Window membership: `|x_k^{valid}|/τ_F ∈ W_V`, `|x_k^{viol}|/τ_F ∈ W_q` (exact rationals). |
| Q4 | **Guard (finish-time domain):** valid member: every week `|x_w| ≤ τ_F − 1`. Violating member: target week `|x_k| ≥ τ_F + 1`, all other weeks `|x_w| ≤ τ_F − 1`. |
| Q5 | Target has the strict, unique maximum `|x|` in both members; `m_V > m_NT`. |
| Q6 | Nonzero: every `d_w ≠ 0` and every `|x_w| ≥ 1`, in both members. |
| Q7 | Same-minute rule: every token in both members has minute digit `⌊G/60⌋ ∈ {1,…,9}`. Exact form: `sec_G ≥ (largest negative deviation)` and `59 − sec_G ≥ (largest positive deviation)` with `sec_G = G mod 60`. |
| Q8 | Exactly one displayed token differs; identical length; identical first two characters (`m:`); differs only in the seconds field. |
| Q9 | `D_dist`, `T_time`, `τ_F` and all non-target tokens are byte-identical between the members. |
| Q10 | Ground truth by the frozen rule (§3.3, rounded `e_w`) equals the class by the exact `x_w`: valid member satisfied, violating member violated. |
| **Q11** | **Plausibility (construction gate, §5.6):** `G_min ≤ G ≤ G_max`; every displayed token of both members lies in `[p_min, p_max]`; `T_time ∈ [Tm_min, Tm_max]`. |

### 5.5 Design-level realizability conditions

Rows marked *necessary* are enforced by hard gate A5; rows marked *sufficient* or *screening aid* never decide admissibility (§3.7).

| ID | Condition | Status |
|---|---|---|
| RC-P1 | `0 < ρ_NT < v_lo ≤ v_hi < 1 < mi_lo ≤ mi_hi < c_lo ≤ c_hi` | necessary |
| RC-P2 | Reach: `(hi − lo)·τ_F ≥ D_dist` for each window (exact: ∃ integer `m ≥ 1` with `lo·τ_F ≤ D_dist·m − σ·r ≤ hi·τ_F`) | sufficient for Q3 |
| RC-P3 | Guard: `v_hi ≤ 1 − 1/τ_F` and `mi_lo ≥ 1 + 1/τ_F` | sufficient for Q4 (with RC-P4) |
| RC-P4 | `ρ_NT·τ_F ≥ D_dist + 1/2` (⇔ `m_NT ≥ 1`) | sufficient for Q2, Q4 (non-target), Q5 |
| RC-P5 | Nonzero: `D_dist ≥ 3/2` and `v_lo·τ_F ≥ 1` (then `|x| ≥ D_dist·|d| − 1/2 ≥ 1` for any nonzero `d`) | sufficient for Q6 |
| RC-P6 | **Upper bound on `τ_F` from the same-minute representation:** `(c_hi·τ_F + 1/2)/D_dist < 30`, i.e. **`τ_F < (30·D_dist − 1/2)/c_hi`** | sufficient for the existence of eligible `G` |
| RC-P7 | Bounds sanity: `60 ≤ p_min ≤ G_min ≤ G_max ≤ p_max ≤ 599` and `0 < Tm_min ≤ Tm_max < 36000` | necessary |
| RC-P8 | Screened-eligible set non-empty: `𝒢_adm ≠ ∅` (definition in §5.6) | screening aid (sufficient set; its emptiness does not by itself make a parameter set inadmissible) |

*Why RC-P6 and the symmetric band.* The chosen clear-class step satisfies `m_C ≤ (c_hi·τ_F + 1/2)/D_dist`. Each reference pace is used with **both** directions (§9), so it must leave room for deviations of either sign: `sec_G ≥ m*` and `sec_G ≤ 59 − m*`, non-empty only if `m* ≤ 29`, i.e. `(c_hi·τ_F + 1/2)/D_dist < 30`. The exact per-template condition (Q7) is one-sided and weaker. The symmetric form is therefore a **screening aid** (sufficient, possibly conservative), not a hard gate: a reference pace outside the symmetric band is still admissible iff Q7 and the other `Q*` gates pass for every template that uses it.

**Integer feasibility of `τ_F` (hard gate A4; screening interval).** `τ_F` is a positive **integer** (hard gate A4, together with the exact gates Q2–Q6). For screening, let
`τ_lo = max( D_dist/w_min, 1/(1 − v_hi), 1/(mi_lo − 1), (D_dist + 1/2)/ρ_NT, 1/v_lo )`, `τ_hi = (30·D_dist − 1/2)/c_hi`
(`w_min` = narrowest window width). An integer `τ_F` with `τ_lo ≤ τ_F < τ_hi` is *sufficient* for the screened conditions RC-P2…RC-P6. A mathematically non-empty real interval is **not enough** for an integer-valued parameter: the set `{τ ∈ ℤ : τ_lo ≤ τ < τ_hi}` must be non-empty for the screen to be satisfied (counter-example: the real interval `(205.1, 205.9)` contains no integer). A `τ_F` outside the screening interval is not rejected by screening alone: it is admissible iff the exact gates pass; if any exact gate fails the parameter set is **inadmissible** (reject-not-repair; no widening of any window or bound).

**Integer vs non-integer `D_dist`.** For integer `D_dist`: `r = 0`, `F_w` is an integer, `rnd*` acts as the identity, `x_w = D_dist·d_w`, and the lattice step is `D_dist`. For non-integer `D_dist` a genuine rounding stage exists (`r ≠ 0`); this is the case the guard of §6.1 is built for. Both are permitted; the register fixes one `D_dist`.

### 5.6 Plausibility bounds (construction gates, R-3)

Plausibility bounds are **construction gates**, not physiological truth. They exist only to prevent obviously artificial or arbitrary scenario values. They are **researcher-choice parameters** (§17) that must be frozen **before** registry generation; this document supplies no numerical value.

| Bound | Meaning | Class |
|---|---|---|
| `G_min, G_max` | plausible range of the hidden reference pace `G` (s/km) | researcher choice |
| `p_min, p_max` | plausible range of every **displayed** weekly pace token (s/km), both members | researcher choice; must contain `[G_min, G_max]` (RC-P7) |
| `Tm_min, Tm_max` | plausible range of the displayed target time for the fixed `D_dist` (s) | researcher choice |
| `60, 599`; `T_time < 36000`; integrality | representational limits of `m:ss` with a single-digit minute and of `H:MM:SS` with a single-digit hour | **fixed** |

*Distance-specific consistency.* `D_dist` is fixed, so the time bounds and the pace bounds are bounds on the same family of scenarios: `T_time = rnd*(D_dist·G)` makes `T_time/D_dist` lie within `1/(2·D_dist)` of `G`. The eligible set below intersects both kinds of bound; no separate "consistency parameter" exists.

*Interaction with `τ_F`, direction and the same-minute rule (screening aid).* Let `m* = max(m_NT, ⌊(c_hi·τ_F + 1/2)/D_dist⌋)`. A reference pace `G` is **screened eligible** iff

`G ∈ 𝒢_adm :⇔  G_min ≤ G ≤ G_max,  p_min + m* ≤ G ≤ p_max − m*,  Tm_min ≤ rnd*(D_dist·G) ≤ Tm_max,  ⌊G/60⌋ ∈ {1,…,9},  m* ≤ G mod 60 ≤ 59 − m*.`

`𝒢_adm` is a **sufficient** screen: scratch check (arbitrary bounds) — for every `G ∈ 𝒢_adm`, all 1,152 templates (all positions, both directions, both classes) passed ground truth, the same-minute rule, the displayed-pace bounds, the time bounds and `|x| ≥ 1`. It is **not necessary**: a `G` outside it is admissible iff it passes the exact gates. Larger `τ_F` ⇒ larger `m*` ⇒ narrower `𝒢_adm`. *Direction-specific exact feasibility* is decided by Q7 and Q11 per template: the tokens of a slower-direction template lie in `[G − m_NT, G + m_q]`, those of a faster-direction template in `[G − m_q, G + m_NT]`; the symmetric `m*` in `𝒢_adm` is sufficient for both because every base is used with both directions.

*Interaction with the `G` arithmetic progression (hard gate A3).* `G_list = { G_0 + j·step_G : j = 0 … L_P − 1 }`. **Hard gate A3:** every element passes every exact `Q*` gate in every template that uses it (all positions, both directions, both classes). A failing element rejects the whole parameter set: there is no skipping, re-centering or adjusting. The usual cause of failure is leaving the same-minute band because the steps wrap the minute. (Illustration only: the symmetric band has width `60 − 2m*`; a progression with `0 < step_G < 60` that stays in one band needs `(L_P − 1)·step_G ≤ 59 − 2m*`; larger or wrapping steps pass only if every element still lands inside the exact band; `step_G` a multiple of 60 keeps `G mod 60` fixed.) *Screening:* testing every element for membership in `𝒢_adm` is a fast sufficient pre-check; it is not the gate. Scratch check: 9 arbitrary progressions screened against `𝒢_adm` → 4 pass the screen, 5 fail it; each screening decision equals element-wise membership.

*Empty or failing sets.* Hard-gate failure of A3, A4, A5 or any exact `Q*` gate makes the parameter set inadmissible: reject-not-repair, log, and select a different register at step 3 (§21.2). If the screening aids find no integer `τ_F` or an empty `𝒢_adm`, that is a warning that the hard gates are likely to fail, not itself a rejection; the dry run of step 4 decides. No bound is widened automatically.

---

## 6. Margins and guard

### 6.1 Guard — general rule, propositions, coverage

**Purpose.** The guard protects the **ground truth from reading and rounding ambiguity** of the comparison. It does not protect against model arithmetic slips; those are the phenomenon under study and are governed by the margin windows.

**General rule (symbolic).** For each family fix a *reading set* ℛ_F: every way the exact comparison quantity may legitimately be rounded or bounded before it is compared. Let `gw_F` be the width of the largest rounding step that any reading in ℛ_F can apply. A scenario is **guard-safe** iff the exact quantity lies at least `gw_F` on the correct side of the threshold: valid: `threshold − |quantity| ≥ gw_F`; violating: `|quantity| − threshold ≥ gw_F`. `gw_F` is derived per family, not assumed.

| Family | Exact comparison quantity (threshold) | Reading set ℛ_F | `gw_F` |
|---|---|---|---|
| `MIL` | increase `Δ = X_k − X_{k−1}` in tenths of km (exact threshold `u`) | threshold `u` rounded to the 0.1-km grid by floor / ceiling / nearest; inclusive or exclusive comparison | **1 tenth of km** |
| `PAC` | exact finish-time deviation `x = D_dist·p − T_time` in seconds (threshold `τ_F`) | exact `F` unrounded, or `F` rounded to whole seconds by floor / ceiling / half-up / half-down / half-even; inclusive (`|e| ≤ τ_F`) or exclusive (`|e| < τ_F`) | **1 second of finish time** |

**Proposition GM (mileage).** Let `o` be an integer on the grid, `t` the exact threshold, `rd(t)` its rounding to the grid by floor, ceiling or nearest (`|rd(t) − t| < 1`). If `|o − t| ≥ 1` then `o` vs `rd(t)` gives the exact verdict under both conventions. *Proof.* Violating: `o − t ≥ 1` and `rd(t) < t + 1` give `o − rd(t) > 0`. Valid: `t − o ≥ 1` and `rd(t) > t − 1` give `rd(t) − o > 0`. Equality is never reached. ∎

**Proposition GP (pace, finish time).** Let `x ∈ ℚ` be a week's exact deviation `D_dist·p − T_time` (`T_time` integer) and `τ_F ∈ ℕ`. Every reading in ℛ_P rounds `x` to a value in `[⌊x⌋, ⌈x⌉]`. (i) If `|x| ≤ τ_F − 1`, every reading says *satisfied*. (ii) If `|x| ≥ τ_F + 1`, every reading says *violated*.
*Proof.* (i) For `x ≥ 0`, `⌈x⌉ ≤ τ_F − 1` because `τ_F − 1` is an integer `≥ x`; every reading's value has magnitude `≤ ⌈|x|⌉ ≤ τ_F − 1 < τ_F`, so both conventions say satisfied; `x < 0` is symmetric. (ii) For `x ≥ 0`, `⌊x⌋ ≥ τ_F + 1`; every reading's value has magnitude `≥ ⌊|x|⌋ > τ_F`, so both conventions say violated; `x < 0` symmetric. The unrounded reading compares `|x|` directly. ∎
*Tightness.* One second on each side is necessary: `x = τ_F − 1/2` flips under *ceiling + exclusive*; `x = τ_F + 1/2` flips under *floor + inclusive*. *Corollary.* For integer `D_dist` (integer `x`) any non-zero slack is `≥ 1`: the guard reduces to excluding `|x| = τ_F`.

**Where rounding happens.** Construction: `nearest()` picks lattice points; ground truth is recomputed from the resulting integers, so this step cannot change a class. Rendering: integer-division / zero-padded rendering reproduces the integers exactly (re-verified by Implementation B, §11). Reader: only readings in ℛ_F are claimed. Mileage state is integer, so no rounding accumulates. For `PAC`: pace is not rounded (integer s/km), `T_time` is integer seconds, `D_dist` is exact; the only rounding of the construction is `rnd*` on `F`.

**Rounding-coverage classification (what is and is not proven).**

| Reader behaviour | Status |
|---|---|
| `MIL`: allowed increase / next-week limit rounded to 0.1 km by nearest, floor or ceiling | **PROVEN** (Proposition GM) |
| `MIL`: percentage increase rounded to 0.1 pp, **round-to-nearest** (half-up, half-even) | **PROVEN for every previous-week value `X_prev ≤ 1999` tenths**; scratch: 0 flips up to 1999, 106 flips in 2000–2100 |
| `MIL`: percentage increase rounded to 0.1 pp, **floor / truncation or ceiling** | **PROVEN only for `X_prev ≤ 1000` tenths**; scratch: 0 flips up to 1000, 60 / 58 flips in 1001–1100 (floor / ceil) |
| `MIL`: percentage increase rounded to a whole percent | **NOT COVERED** — a limitation, not a guarantee |
| `MIL`: allowed increase rounded to a whole km | **NOT COVERED** (scratch: 255 flips with slack ≥ 1 tenth) |
| `MIL`: ρ itself rounded, other composite roundings | **NOT COVERED** |
| `PAC`: `F` unrounded or rounded by floor / ceil / half-up / half-down / half-even; inclusive or exclusive | **PROVEN** (Proposition GP); scratch: 0 flips in 115,014 guarded cases and, rounding `F` itself, 0 flips in 53,021 |
| `PAC`: reader rounds `D_dist`, converts `m:ss` to decimal minutes, or rounds the pace token | **NOT COVERED** |
| Any reader behaviour outside ℛ_F | **NOT COVERED** — counted as model error / reported as a threat (§20) |

Coverage tier is a consequence of the register: with `Xprev_max ≤ 1000` tenths the `MIL` percentage-truncation readings are covered; with `1000 < Xprev_max ≤ 1999` only round-to-nearest; above that none. The Parameter Justification Record states the tier.

**Critical evaluation of the audit proposal (`g = max(s_m, s_p)`, `ρ_v0 = 1 − c_m·g`)** — conditional on reading `s_m, s_p` as smallest display increments in ρ units, because the original definitions are unavailable. (1) A display increment in ρ units is base-dependent (`MIL`: `1/u`) or `1/τ_F` (`PAC`); one scalar cannot serve both, and `max` coarsens the finer family. (2) A point value `1 − c_m·g` need not lie on either lattice. (3) A valid margin tied to the guard drifts in ρ with the base. (4) The shared scalar couples the families without need. Retained: an objective, increment-based guard. Replaced by: family-specific `gw_F` from an explicit reading set, windows in ρ, per-template gates.

### 6.2 Margin-class windows

Three ρ windows, defined once and shared by both families unless a family cannot realize them (then per-family windows are declared before generation; a recorded degree of freedom):

`W_V = [v_lo, v_hi]`, `W_MILD = [mi_lo, mi_hi]`, `W_CLEAR = [c_lo, c_hi]`, ordering `0 < ρ_NT < v_lo ≤ v_hi < 1 < mi_lo ≤ mi_hi < c_lo ≤ c_hi`.

Each ρ is evaluated in its own family's exact comparison quantity. Realizability is family-specific (RC-M1…RC-M7, RC-P1…RC-P8). `MIL` lattice resolution in ρ is `1/u`; `PAC` lattice resolution is `D_dist/τ_F`.

**Non-overlap.** Valid and mild are separated by at least `2/U` in ρ (RC-M3/RC-P3), mild and clear by the ordering; boundary values are excluded by the guard. No class is empty **for any admissible parameter set** (§3.7); for a parameter set that is not admissible the build is rejected, not repaired.

**Selection of windows** is a parameter decision (§17): justified from feasibility and domain meaning, documented before any model call, never from model behavior.

**Classes.** Valid members have the single valid class `V`. Violating members have class `MILD` or `CLEAR`. "Violation-margin class" in the RQs refers to the violating member's class.

---

## 7. Profile design (I-07) — profile factor REMOVED (unchanged)

**Decision: no experience-level (or any runner-profile) factor.** With identical numbers "beginner" and "advanced" cannot both be realistic across the whole value range, and the construct does not depend on runner identity. The prompt contains no runner-profile fields; if the prompt specification wants a runner sentence it is one constant text, identical in every scenario, plausible across all `[X_min, X_max]` and pace ranges. Generalization across experience levels is not claimed. No profile-crossing balance exists.

---

## 8. Matched-pair equivalence, cross-condition gates and leakage control

**Valid/violating matched pair — gates (each an automated gate and a unit test; evaluated on the full model prompt):**

| ID | Gate |
|---|---|
| X1 | Exactly one numeric token differs: `X_k` (`MIL`) or `p_k` (`PAC`). |
| X2 | Changed tokens have identical **character length** (`MIL`: `%.1f` via integer division, equal integer-digit count (M7); `PAC`: `m:ss`, same minute, differing only in the seconds field). |
| X3 | Every other character of the prompt is identical: equal length and the set of differing character positions is contiguous and inside the target token's span. |
| X4 | No derived text depends on the changed token: no sum, average, delta, percentage, implied finish time or commentary is rendered; the claim block names no week and no number. |
| X5 | No formatting/alignment difference: unpadded markdown cells, one canonical separator row, LF only, ASCII only, no BOM, no trailing newline, no hidden or trailing whitespace; assertions for `\t`, `\r`, non-breaking space, zero-width characters. The plan block is additionally restricted by the row whitelist **X12** (§8.3). |
| X6 | The rule text may depend on template parameters (`P`, `D_dist`, `τ_F`) but never on the changed token; it is byte-identical between the members. |

**Cross-condition gates:**

| ID | Gate |
|---|---|
| X7 | `Cond-C` vs `Cond-A`: prompt `Cond-C` with its claim block removed by the frozen insertion procedure is **byte-identical** to prompt `Cond-A`. |
| X8 | `Cond-D` vs `Cond-B`: prompt `Cond-D` with its claim block removed is **byte-identical** to prompt `Cond-B`. |
| X9 | The claim block bytes are identical in `Cond-C` and `Cond-D` and across all templates of the family (one hash per family). |

X7–X9 are verified by Implementation B on the final strings (not only by the generator that built them), which is what makes them non-tautological.

### 8.1 X10 — forbidden-pattern scan (mechanical)

The scan targets **internal labels and rendering artifacts**, not semantics and not ordinary language. Bare letters (`A`, `B`, `V`) and common English words (`mild`, `clear`, `valid`, `condition`, `base`, `class`, `none`) are **never** forbidden tokens.

1. **Input.** Each final model prompt as a UTF-8 string (all `4·N_tpl` prompts).
2. **Normalization.** `NFKC`, then `casefold`. Patterns marked CS run on the original string instead.
3. **Boundaries.** `bnd⁻ = (?<![a-z0-9_])`, `bnd⁺ = (?![a-z0-9_])` on normalized text. No tokenizer is used; matching is by regular expression only.
4. **Patterns (fixed order):**

| ID | Pattern | Detects |
|---|---|---|
| F1 | `bnd⁻(?:mil\|pac)-[0-9]{3}(?:-(?:v\|mild\|clear))?bnd⁺` | canonical template / member IDs |
| F2 | `bnd⁻[0-9a-f]{16,}bnd⁺` | opaque IDs and hashes |
| F3 | `bnd⁻(?:cond\|condition\|arm\|stratum)[_=-][abcd]bnd⁺` | condition identifiers in label form |
| F4 (CS) | `(?<![A-Za-z0-9_])(?:MILD\|CLEAR\|MIL\|PAC)(?![A-Za-z0-9_])` | all-caps class / family identifiers |
| F5 | `bnd⁻[a-z]+_(?:id\|class\|cond\|index\|label\|member\|position\|direction\|cluster\|base\|arm)bnd⁺` | snake-case internal field names |
| F5b | `bnd⁻(?:template\|member\|cluster\|base)_[a-z0-9]+bnd⁺` | internal prefixes |
| F6 | `bnd⁻(?:cond\|class\|member\|template\|cluster\|pos\|dir\|sigma)\s*=\s*\S` | debug key=value forms |
| F7 | `bnd⁻target[_-](?:week\|position\|pos\|token\|transition)bnd⁺` | target-position labels (would reveal construction) |
| F7b | `\((?:target\|valid\|violating\|mild\|clear)\)` | parenthetical annotations |
| F8 | `bnd⁻(?:valid\|violating)[_-](?:plan\|member\|version\|variant\|arm\|case\|template)bnd⁺` | state labels (machine form) |
| F8b | `bnd⁻(?:plan\|member\|case)[_-](?:valid\|violating)bnd⁺` | state labels (machine form, reversed) |
| F9 | `\{\{\|\}\}\|\[\[\|\]\]\|<<\|>>\|%\([a-z_]+\)s\|\{[a-z_]+\}` | unrendered placeholders |

(In the table, `\|` is the markdown escape of the regex alternation `|`; the regular expressions themselves contain the plain `|`.)

F10 runs after F1–F9 on the **original** (non-casefolded) text and detects emphasis or footnote markup touching a numeral anywhere in the prompt:

```
F10   (?<=[0-9])[*_~`]|[*_~`](?=[0-9])|\[\^[^\]]*\]
```

5. **Allowed exceptions.** None are masked. The required response-format words (`Constraint:`, `Verdict:`, `Comments:`, `satisfied`, `violated`, `unclear`), the reviewer-claim block and the rule text contain none of the patterns by construction; this is **proved at freeze** by an acceptance test: the frozen response-format block, claim block, rule text, task text and plan-table skeleton must scan clean, and a frozen **negative-control battery** (ordinary sentences, the response-format text, the claim-like sentence, table rows, and common words such as "base", "mild", "clear", "valid", "condition", "none") must pass while a frozen **positive-control battery** (machine-label strings such as `MIL-012-V`, `cond_A`, `template_id`, `target_week`, `valid_plan`, `{{plan}}`, a 16-hex string, `(target)`) must fail; the battery additionally contains the annotation-leakage controls of §8.3 (emphasis, footnote and parenthetical markers next to a numeral must fail F10 or X12; ordinary sentences containing the words "peak", "week", "target" or "note" must pass F1–F10). Scratch check: 19 negatives pass, 23 machine-label positives are caught by F1–F9; F10 flagged 7 of 7 emphasis/footnote positives and 0 of 7 negatives.
6. **Order and behaviour.** Patterns F1…F10 run in fixed order on every prompt; any match is a `FAIL` reporting pattern ID and offset; one failure rejects the whole build (§3.6). No human judgment is involved.
7. **Anti-cue word list for the task text.** Separately, the frozen task text must contain none of the words on the anti-cue list declared in the prompt specification (§14). That list applies to the task text only, not to rule, plan or claim.

### 8.2 Registry-level distinctness and human-review leakage

| ID | Gate |
|---|---|
| A1 | **Distinctness:** the valid plans (prompts `Cond-A`) of all templates are pairwise distinct, the violating plans (prompts `Cond-B`) likewise; the registry contains exactly `4·N_tpl` distinct prompts. |
| X10 | The scan of §8.1 passes on every model prompt. |
| X11 | Human-review materials (ground-truth checker, S2/S3 coders) use **opaque IDs only**: the filename and every identifier match `^[0-9a-f]{16}$` and no pattern F1, F3–F8b occurs in any file name, file body or directory name. Opaque ID = first 16 hex characters of SHA-256 over the rendered text (checker materials) or over the canonical call key plus registry hash (coder materials); the mapping table is held separately and is not shown to checker or coders. Materials are ordered by opaque ID. |
| **X12** | **Plan-block rendering whitelist (§8.3):** every line of the plan block matches exactly one frozen whitelist entry; any emphasis, annotation, footnote marker, extra column or non-canonical numeral is rejected, with no normalization or repair. |

**Perfect blinding is not claimed.** The two members of a matched pair intentionally differ in one token, so a checker who sees both can infer which is which. Opaque IDs and ordering by hash remove label and adjacency cues; they cannot remove recognizability of near-duplicates. Derived relations also necessarily differ once the target token changes (e.g. the drop after the mileage peak is larger in the violating plan); this follows from the intended token change.

**Character equality is controlled; LLM tokenizer-token equality is not.** The experiment guarantees equal character length and a single changed span. It does not guarantee that the model's tokenizer splits the two tokens into the same number of tokens, and no claim of tokenizer-level equivalence is made.


### 8.3 X12 — plan-block rendering whitelist (F6)

Purpose: prevent target-position (or class) leakage through formatting, emphasis, annotation or footnote markers **without banning any natural-language word**. Words such as "peak" or "week" are never rejected by this gate.

1. The **plan block** is the exact line range of the plan table in the rendered prompt, delimited by the frozen block markers of the prompt specification (`MIL`: header, separator, `N` rows; `PAC`: distance line, target-time line, header, separator, `N` rows).
2. Every line of the plan block must match **exactly one** whitelist entry (full-line, anchored, on the original text, no normalization, no trimming):

| Entry | Full-line pattern |
|---|---|
| `MIL` header / separator | equal to the frozen strings (e.g. `\| Week \| Total km \|`, `\|---\|---\|`) |
| `MIL` row | `^\| ([1-9][0-9]?) \| ([0-9]{1,3}\.[0-9]) \|$` |
| `PAC` distance line | `^<frozen label>: [0-9]+\.[0-9]{q} km$` (`q` = the frozen number of decimals; integer distances use the frozen rendering) |
| `PAC` time line | `^<frozen label>: [0-9]:[0-5][0-9]:[0-5][0-9]$` |
| `PAC` header / separator | equal to the frozen strings |
| `PAC` row | `^\| ([1-9][0-9]?) \| ([1-9]:[0-5][0-9]) \|$` |

3. Structural conditions: the number of rows is `N`; week numbers are `1, 2, …, N` consecutively; no blank line, extra line or extra column inside the block; the same entry set is used for both members of every matched pair and for all four conditions.
4. Everything else is a **non-whitelisted rendering** — in particular emphasis (`*`, `_`, `~`, backtick), brackets, parentheses, footnote markers, arrows, daggers, extra spaces or columns, trailing characters, leading zeros, unit suffixes, a different numeral format, a modified header.
5. **Rejection behavior:** the first non-matching line yields `FAIL(X12, prompt id, line number, expected entry)`; a single failure in any prompt rejects the whole build (§3.6). No normalization or repair is applied before the test, and no line is excused as "ordinary text".
6. Together with X3 (only the target numeral may differ) X12 implies that the two members of a matched pair, and the four conditions of a template, differ in the plan block only in the target numeral, and that no formatting can mark the target week.
7. **Controls (frozen with the F-controls):** *must pass:* compliant rows (`| 3 | 34.9 |`, `| 12 | 100.4 |`, `| 4 | 4:27 |`), the frozen header and separator, a block with natural-language sentences outside it. *Must fail:* `| 3 | **34.9** |`, `| 3 | 34.9* |`, `| 3 | 34.9 (peak) |`, `| 3 | 34.9 [1] |`, `| 3 | _34.9_ |`, `| 3 | 34.90 |`, `|3|34.9|`, a row with a trailing space, a row with an extra column, `| 3 | 34.9 <- |`, `| 03 | 34.9 |`, `| 3 | 34.9 km |`, a backticked value, a dagger, a header with an added word, a week-number gap; for `PAC`: `| 3 | 4:7 |`, `| 3 | 04:31 |`, `| 3 | 4:61 |`, `| 3 | 4:31 (target) |`, `| 3 | 4.31 |`, `| 3 | **4:31** |`.
8. Scratch check: compliant `MIL` and `PAC` blocks pass; 16 non-whitelisted `MIL` rows and 8 non-whitelisted `PAC` rows are all rejected; a modified header and a week-number gap are rejected.

---

## 9. Balance, class assignment, clusters and call count (I-08, R-1)

### 9.1 Problem and requirements

v2.0 gave MILD and CLEAR templates the same valid plan (duplicates). v2.1's parity rule removed the duplicates but made the `PAC` class independent of target position (class `= f(base parity, direction)`), confounding class with base parity × direction. v2.2 replaces the rule. The assignment must: vary class across positions for every (base, direction); keep MILD/CLEAR balanced on every margin that can be exact; make no base and no direction permanently one class; not be a simple parity rule; be deterministic and reproducible; and keep valid-plan uniqueness, matched pairs, `Cond-A`/`Cond-C` and `Cond-B`/`Cond-D` equivalence, and exact position and direction factors.

### 9.2 Construction (deterministic, no PRNG)

- Lists: `S_list` has `L_M = 2·n_M` values, `G_list` has `L_P = 2·n_P` values, ascending, indexed by base `b = 0 … L−1`. Base couples are `(2·cpl, 2·cpl+1)` with `cpl = ⌊b/2⌋`; `b_par = b mod 2`.
- Templates: every (base `b`, position `i = 0 … K−1`, direction `s`) — `MIL`: `s = 0` only; `PAC`: `s ∈ {0,1}`. `N_tpl,MIL = K·L_M = 2K·n_M`; `N_tpl,PAC = 2K·L_P = 4K·n_P`.
- Window start: `a(b, s) = ( cpl + s·dir_shift + b_par·K/2 ) mod K`, with direction shift `dir_shift = ⌊K/4⌋`.
- **Class rule:** `class(b, i, s) = MILD` iff `((i − a(b,s)) mod K) < K/2`, else `CLEAR`.

**Design invariants for exact balance** (gate A2): `K` is **even** and `K ≥ 4` (so `N` is **odd** and `N ≥ 5`); `L` is even (always, `L = 2n`). Reason: each base must be MILD in exactly `K/2` of the `K` positions per direction (needs `K` even), and the direction shift `dir_shift = ⌊K/4⌋` must satisfy `0 < dir_shift < K/2` so that the two directions' windows are neither identical nor complementary (needs `K ≥ 4`). For odd `K` exact base × (direction) × class balance is impossible (a base would need a non-integer number of MILD positions); odd `K` is therefore **not admissible**.

### 9.3 Properties

Items 1–5 are **proofs** (valid for every even `K ≥ 4` and every even `L`). Item 6 and the registry rebuild in item 7 are **finite checks** by enumeration (`K ∈ {4,6,8,10,12}`, `L ∈ {2,4,6,8,10,12,14,16,20,30}`, one and two directions) and are not general proofs.

1. **Base × direction × class exact.** For fixed `(b,s)` the positions with `(i − a) mod K ∈ [0, K/2)` number exactly `K/2`; hence each base is MILD in `K/2` and CLEAR in `K/2` positions in every direction. No base is ever permanently one class; no direction is ever permanently one class.
2. **Slot × class exact.** For fixed `(i,s)` the bases `2·cpl` and `2·cpl+1` have windows starting at `a` and `a + K/2` — complementary half-cycles — so exactly one of the two is MILD at `i`: each (position, direction) slot has exactly `L/2` MILD and `L/2` CLEAR templates.
3. **Hence exact:** base × class; position × class; direction × class; position × direction × class.
4. **Class varies with position** for every (base, direction): a half-cycle window of length `K/2 < K` contains both inside and outside positions.
5. **Direction does not determine class.** The two directions' windows of a base differ by the shift `dir_shift` with `0 < dir_shift < K/2`; at a given (base, position) they agree on `K − 2·dir_shift` positions and disagree on `2·dir_shift` (both occur).
6. **Not a parity rule.** For every tested `(K, L, directions)` no function `(κ1·b + κ2·i + κ3·s + κ4) mod 2` (coefficients in {0,1}) reproduces the class table. The v2.1 rule and the "naive fix" `(b + i + s) mod 2` fail this test: the naive fix is balanced on every margin but **is** exactly such a parity-XOR rule.
7. **Valid-plan uniqueness is preserved.** The valid member depends only on `(b, k, [σ])`, not on the class; templates differ in `(b, k, [σ])`, hence in their valid plans; with `RC-M4`/`Q5` the target step differs from every ramp step, so plans from different `k` differ. Violating members additionally depend on the class. Scratch registry build under this rule: 36 `MIL` and 96 `PAC` templates, 36/36 and 96/96 distinct valid plans, 264/264 distinct prompts, `Cond-A`/`Cond-C` and `Cond-B`/`Cond-D` equivalent, one differing token per matched pair, correct class windows, equal counts for every (position, [direction], class), (base, class), (base, direction, class).

**Aliasing and what remains a limitation.** One class per (base, position, direction) cell means the class is necessarily aliased with some interaction. Here: `class = b_par ⊕ W((i − cpl − s·dir_shift) mod K)`, where `W` is the half-cycle window indicator. It is exactly balanced on every main effect and on each two-way margin of items 1–3, and aliased with the base-couple × position × direction "diagonal". It is **not** claimed to be orthogonal to the base × position interaction.

**Measured interaction aliasing (finite audit test; not a proof and not general).** In the fresh delta audit a scratch `MIL` registry was built for arbitrary configurations (one direction; `P = 10`, `ρ_NT = 0.4`; start value 300 tenths with a progression step of 15–100 tenths; values arbitrary, none proposed). Two quantities were computed per configuration: (i) the difference between the class means of the realized pre-target value, in standard deviations; (ii) the standardized correlation between the class indicator (±1) and the centred product (start value) × (position index) — **one specific** linear base × position interaction contrast.

| (K, L) | difference of class means (sd) | correlation with start × position |
|---|---|---|
| (4, 4) | +0.013 | +0.200 |
| (4, 8) | −0.001 | +0.000 |
| (6, 6) | +0.013 | +0.086 |
| (6, 12) | +0.001 | +0.000 |
| (8, 8) | +0.010 | +0.048 |
| (10, 20) | +0.001 | +0.000 |

(`K = 6, L = 6` was also run at step 100: +0.012 and +0.086.) What this supports, restricted to what was tested: the main-effect imbalance in the realized value is negligible (≤ 0.013 sd); the interaction correlation was non-zero when `L = K` (up to +0.20 at `K = 4`) and was 0.000 in the three tested cases with `L = 2K`. It does **not** show that other interaction contrasts vanish, that the pattern holds for other configurations, or that `L ≥ 2K` is sufficient. The registry-level class contrast is therefore balanced on the specified main effects and two-way margins but is **not guaranteed to be orthogonal to the base × position interaction, especially at small `L`** (TH4, TH6).

Further consequences: (a) within a single base, MILD occupies a contiguous cyclic half of the positions, so a **within-base** class contrast cannot be separated from position; (b) the adjacent bases `2·cpl` and `2·cpl+1` are opposite at every slot by design (this is what makes the slot margins exact for any even `L`). These are disclosed in §20; no claim of full orthogonality is made.

### 9.4 Symbolic examples (no parameter values)

`MIL`, one direction, `K = 4`, `L = 4` (couples `(b0,b1)`, `(b2,b3)`); rows are bases, columns positions `i = 0…3` (M = MILD, C = CLEAR):

```
b0: M M C C      b1: C C M M      b2: C M M C      b3: M C C M
```
Every row has two M, two C; every column has two M, two C.

`PAC`, two directions, `K = 4`, `L = 4`, `dir_shift = 1` (s0 = slower, s1 = faster):

```
        s0        s1
b0:   M M C C   C M M C
b1:   C C M M   M C C M
b2:   C M M C   C C M M
b3:   M C C M   M M C C
```
Per (base, direction): two M, two C. Per (position, direction): two M, two C. A base is MILD in some positions and CLEAR in others in both directions; the two directions of a base are neither equal nor complementary.

### 9.5 Reporting cells, clusters and counts

Per family, with `L` clusters:

| Cell | Clusters in cell | Templates per cluster | Templates in cell |
|---|---|---|---|
| `MIL` valid state, one condition (`Cond-A` or `Cond-C`) | `L_M` | `K` | `N_tpl,MIL = 2K·n_M` |
| `MIL` violating × class, one condition (`Cond-B` or `Cond-D`) | `L_M` | `K/2` | `K·n_M` |
| `PAC` valid state, one condition | `L_P` | `2K` | `N_tpl,PAC = 4K·n_P` |
| `PAC` violating × class, one condition | `L_P` | `K` | `2K·n_P` |
| `PAC` violating × class × direction (secondary) | `L_P` | `K/2` | `K·n_P` |
| Any family × position × class (secondary) | `≤ L` | 1 (per direction) | `L/2` per direction |

**Every primary cell contains all `L` clusters.** The number of templates in a cell is a descriptive count; the number of independent units in a cell is the cluster count `L` (§2.3, §12). Calls in a cell = templates × `R`.

### 9.6 Registry-level gates

| ID | Gate |
|---|---|
| A1 | Distinctness (§8.2). |
| **A2** | `K` is even and `K ≥ 4` (`N` odd, `N ≥ 5`); `L` is even. |
| **A3** | **Progression gate (hard, exact):** every element of `S_list` passes every `M*` gate, and every element of `G_list` passes every `Q*` gate, in every template that uses it. No skipping or adjusting. Membership in `𝒢_adm` (§5.6) is a screening aid for choosing lists, not this gate. |
| **A4** | **`τ_F` gate (hard, exact):** `τ_F` is a positive integer and the exact gates Q2–Q6 pass. The integer interval `[τ_lo, τ_hi)` of §5.5 is a screening aid. |
| **A5** | **Register sanity (hard; necessary conditions only):** RC-M1 and RC-P1 (window ordering), RC-P7 (bounds ordering and representational limits), `X_min ≤ X_max`, all declared bounds mutually consistent. RC-P8 is a screening aid and is not part of A5. |
| **A6** | Class-assignment verification: the class matrix equals the rule of §9.2 recomputed by Implementation B; Implementation B also recomputes each member's ρ **from the rendered numbers** and checks it lies in the window of its class; all margins of §9.3 hold exactly. |
| **A7** | Cluster integrity: every base appears in every (position, [direction]) slot exactly once and in both classes equally; every cluster has equal template counts per reporting cell. |

### 9.7 Call count

`Calls = 4·R·(N_tpl,MIL + N_tpl,PAC) = 4R(2K·n_M + 4K·n_P) = 8·K·R·(n_M + 2·n_P)`, `K = N − 1`. Verified against enumeration (three tuples). Distinct prompts = `4·N_tpl = 8K(n_M + 2n_P)`. Each of the four conditions gives every template exactly `R` calls; valid and violating plans receive equal numbers of calls. Symbolic only.

---

## 10. Reproducibility (I-05) — Option A, deterministic enumeration

**Scenario construction contains no stochastic generation, no seed, no "next candidate", no regeneration.** The registry is a pure function of (frozen generator code, frozen parameter register). The class rule of §9.2 is an explicit arithmetic rule, not a random assignment.

- **Canonical ID assignment (internal only):** families `MIL` then `PAC`; templates ordered by position `i` ascending, then direction (slower first), then base `b` ascending; `ID = <FAM>-<3-digit counter>`. Members `<ID>-V`, `<ID>-<MILD|CLEAR>`. Canonical IDs never enter a prompt or a human-review bundle (X10, X11).
- **Tie-breaks:** `nearest` ties toward the lower integer; `rnd*` ties up; table rows week-ascending; lists ascending.
- **Rejection:** §3.6 and §21.2. No automated search over parameter space; manual parameter-set changes are logged.
- **Registry hash:** canonical JSON (sorted keys, UTF-8) SHA-256, plus SHA-256 of every rendered prompt, recomputed by an independent script before any call.
- **Execution order (the only stochastic element, content-independent):** all `(template, condition, repetition)` triples in canonical order (template ID ascending, condition `Cond-A<Cond-B<Cond-C<Cond-D`, repetition ascending), shuffled once by `random.Random(seed).shuffle` (Mersenne Twister; interpreter version recorded), as in the Stage 2 precedent. Seed **rule** (value not chosen here): the integer `YYYYMMDD` of the **script-stamped UTC date** of the **first run of the decision script** after the last pilot call (§21 step 11); no date is chosen in advance by this document and none is typed by a person. Researcher discretion is therefore visible and limited to *when* the decision script is first run. Before any order is generated, a **decision record** is written and hashed containing: the pilot structural counts (SF1–SF5, UNP share), the F1 hash, the decision-script hash, the script-stamped UTC timestamp, the computed seed integer, and the interpreter version. The script is run once; any further run is a logged event, and the **first** run's timestamp and seed stand. The order is generated only after the record exists. The pilot uses the canonical order with no shuffle. The runner reconstructs the order from the record and aborts on mismatch.

---

## 11. Ground-truth validation (I-10, R-5)

Three layers; the claims of independence are limited as stated.

1. **Implementation A (structured).** Computes states, ρ, all gates and the six-reading invariance check from generator data using `Fraction` arithmetic; produces for each member a **reference worksheet** (§11.2).
2. **Implementation B (rendered text, strict parse).** A separate module with its own parser reads the **final rendered prompt strings**, extracts rule parameters, `D_dist`, `T_time`, tokens, and recomputes the states with a different numeric library and method (`decimal.Decimal`, explicit quantization with half-up for `rnd*`; percentage growth; strict `>`), re-verifies X1–X12, A1, A6, A7 and the guard (Propositions GM, GP) on the parsed values. It is written from §3 without importing or reading A. **Strict parse:** every field (rule parameter, `D_dist`, `T_time`, each table row) must be found **exactly once** with a unique value; a missing field, a duplicate, or two different values for one quantity is an *ambiguity/contradiction failure*.
3. **Human blind check.** One rule-reader receives only the rendered rule and rendered plan (no claim block), under **opaque IDs** (X11), ordered by opaque ID, with a calculator permitted. They fill a **worksheet** (§11.2) and record a verdict `satisfied` / `violated` / `unclear`. No feedback during the check. Default coverage: every member; a subsample is allowed only if its fraction and deterministic selection rule are frozen before generation, and is then a recorded limitation.

**What each layer does and does not establish.**

| | Establishes | Does not establish |
|---|---|---|
| Independent implementation (A vs B) | absence of coding errors in either path; rendering fidelity; parser independence | independence of **rule semantics**: both implement §3.2–3.3 and the same `rnd*`; both come from this specification |
| Rendering / parser independence | the strings a model sees reproduce the intended integers and are unambiguous under a strict parse | that the strings mean what the specification means (a reading question) |
| Human validation | that a reader of the rendered rule reaches the frozen semantics | blindness in the strong sense: the checker knows the construction, may recognize matched pairs, has finite accuracy |
| Single-researcher fallback | a delayed self-check | inter-person interpretation; independence of A/B authorship |

### 11.1 Disagreement between A and B or between gates

**ADJ-1.** If A and B disagree on any member's state, ρ, class or any gate, the registry build is **rejected**. No adjudication. The failure is classified by the return paths of §21.2.

### 11.2 Objective adjudication of a human disagreement (ADJ-2)

**Worksheet entries (complete checklist; all entries are required for every member).**
- `MIL`: (i) the rule parameter `P`; (ii) for each week `i = 1 … N` the transcribed total, with week 1 marked `uncompared`; (iii) for each week `i ≥ 2`: the increase in km (≥ 1 decimal), the allowed limit `P%·X_{i−1}` in km (≥ 2 decimals), the percentage increase (≥ 2 decimals), and the status `over cap` / `not over cap`; (iv) the verdict.
- `PAC`: (i) the transcribed `D_dist`, `T_time` (as displayed and in seconds) and `τ_F`; (ii) for each week `w = 1 … N` the transcribed pace string and its value in s/km (integer); (iii) for each week: the implied finish time before rounding (≥ 2 decimals, seconds), after rounding (integer), the difference from `T_time` (integer), and the status `|e| > τ_F` / `not`; (iv) the verdict.

The **reference worksheet** is produced by Implementation A from the displayed values only.

**Normalization for the transcription test.** Both the human string and the displayed string go through: Unicode NFKC; strip leading and trailing whitespace; collapse internal whitespace runs to one space; remove one trailing unit token from the closed list `{km, %, s, sec, /km, min/km}` (case-insensitive) together with its separating space. After that they must be **identical as strings**: a different digit, a different number of decimals, or a different `m:ss` is a mismatch, and no numeric equivalence (`71.9 = 71.90`) is applied.

**Minimum precision (hard rule).** Intermediate entries must have at least the decimals listed above (`MIL` limit and percentage: 2 decimals; `PAC` unrounded finish time: 2 decimals). At these precisions the worksheet rounding error is below one display unit (`MIL`: ≤ 0.05 tenth for the limit, ≤ 0.005 percentage points for the percentage; `PAC`: ≤ 0.005 s), so for every guarded member (slack ≥ 1 display unit, §6.1) a worksheet at or above the floor cannot flip the verdict (the argument of Propositions GM and GP: slack ≥ 1 > error). Scratch check: 5,383 guarded `MIL` cases and 45,145 guarded `PAC` cases at the floor produced 0 flips; whole-percent worksheets flipped 172 guarded `MIL` verdicts, which is why the floor exists.

If the human verdict equals the reference verdict: `AGREE`. Otherwise apply, **in this order**, a procedure that uses no belief about intent:

1. **Strict-parse check.** If Implementation B's strict parse of the rendered text reports any ambiguity or contradiction (§11, layer 2) → **REJECT the build**.
2. **Completeness.** If the worksheet lacks any required entry → **REJECT**.
3. **Transcription test.** If any normalized transcribed input differs from the normalized displayed string → **CHECKER ERROR (transcription)**.
4. **Precision test.** If any intermediate entry has fewer decimals than the floor → **CHECKER ERROR (precision)**. A verdict difference that results from rounding more coarsely than required is a checker error, not evidence of ambiguity.
5. **Arithmetic test.** If any intermediate value differs from the reference value by more than half a unit of the last decimal the human stated → **CHECKER ERROR (arithmetic)**.
6. **Residual.** If every input matches, every intermediate is at or above the floor and matches, and the verdict still differs from the reference verdict (including a verdict of `unclear` with a correct worksheet, or any ambiguity note with a correct worksheet) → **REJECT the build** (rule-application disagreement attributable to the rendered rule or the semantics; the existing rejection rule).
7. **Anything not classified by steps 1–6 → REJECT.**

A `CHECKER ERROR` keeps the member, is logged and counted, and changes nothing. A `REJECT` is handled by §21.2. Single-template exclusion is not used: it would break the factorial balance and the call formulas and would itself be a repair. Every step compares recorded entries with the reference by a stated rule; the only judgement left to a person is which entries to write down, which step 2 audits, and the normalization list is closed, so two researchers following the worksheet have no step at which intent or wording can enter. Scratch check of the classifier on eight synthetic worksheets (correct; unit suffix and spacing only, which normalization neutralizes; transcription error; whole-percent worksheet with a flipped verdict; arithmetic slip at the floor; correct arithmetic with the wrong verdict; correct arithmetic with `unclear`; missing worksheet) gave `AGREE`, `REJECT` (the normalized inputs match and the arithmetic is correct, so no false transcription error is raised), `CHECKER ERROR (transcription)`, `CHECKER ERROR (precision)`, `CHECKER ERROR (arithmetic)`, `REJECT`, `REJECT`, `REJECT` as specified.

**Single-researcher limitation (explicit).** If one person wrote A, wrote B, ran the generator and performs the human check, then: (i) "A and B written without reading each other" cannot be verified; independence is of code paths, not of minds; (ii) the human check requires a declared minimum delay since the researcher last saw rendered registry content or expected states (delay frozen in §17) and is run from the opaque-ID bundle alone; (iii) it tests re-derivation consistency, not inter-person interpretation. These are listed in §20. A model-based reader may be added only as an extra screening layer, never as the deciding check.

---

## 12. Sample-size decision procedure (I-11, R-2)

**Planning unit = cluster (base).** Per family the number of clusters is `L = 2n`. Every primary cell contains all `L` clusters (§9.5), and every contrast below is computed within or across the same `L` clusters. Templates, repetitions and calls reduce within-cluster noise; they do not add independent units. `N_tpl` is descriptive.

**Cluster-level aggregation.** For template `t` and condition `c`, `p_t(c)` = (calls whose verdict equals the ground truth) / R over **all R calls** (`unclear` and unparseable stay in). For a reporting cell and cluster `b`, `q_b(cell)` = mean of `p_t(c)` over the cluster's templates in the cell. The **cell estimate** is the mean of `q_b` over the `L` clusters; under exact balance (§9.3) it equals the pooled template mean. **Claim contrast:** `ctr_b = q_b(Cond-C) − q_b(Cond-A)` (per cluster) or `q_b(Cond-D) − q_b(Cond-B)`. **Class contrast:** `ctr_b = q_b(MILD) − q_b(CLEAR)` — *within-cluster*, because every base is in both classes.

### 12.1 What each bound controls

Let `L` be the number of clusters in the cell (here always the family's `L`).

| Estimand | Worst-case variance of the estimator | Half-width | Planning bound |
|---|---|---|---|
| Single cell mean | `q_b ∈ [0,1]` ⇒ `Var(q_b) ≤ 1/4` ⇒ `Var(mean) ≤ 1/(4L)` | `hw = z/(2√L)` | `L ≥ (z / 2hw)²` |
| Claim contrast or within-cluster class contrast | `ctr_b ∈ [−1, 1]` ⇒ `Var(ctr_b) ≤ 1` (Popoviciu) | `hw = z/√L` | `L ≥ (z / hw)²` |

These bounds are **conservative against any within-cluster dependence** (they allow the templates of a cluster to behave identically). They are **not** conservative against between-cluster dependence from shared global constants, **nor against base similarity**: both bounds treat the `L` clusters as independent, whereas closely spaced or similar bases can make the effective number of independent clusters substantially lower than `L` (§2.3), so the bounds are optimistic in that respect. They are **not** a coverage guarantee or a power calculation, and the normal approximation is unreliable at small `L`. No effective cluster count is estimated or assumed. `R`, `K` and the number of templates per cluster do not appear: under the worst case, repetitions or positions cannot compensate for too few bases.

### 12.2 Decision procedure (all decided and frozen before any pilot or main response)

| Step | Decision | Frozen at |
|---|---|---|
| DP1 | **Estimand list and status.** Default: the 12 primary cells are *precision-targeted*; every contrast (claim contrasts, class contrast, position, direction) is *exploratory* unless the Parameter Justification Record names it precision-targeted. | criteria (step 2) |
| DP2 | **Confidence level / `z`** and **multiplicity stance**: (i) per-cell unadjusted intervals with the number of reported cells `n_cells` declared and the statement that intervals are not simultaneous (recommended for a descriptive design), or (ii) Bonferroni over `n_cells` precision-targeted estimands (enters `z`). No hypothesis tests are planned. | criteria (step 2); numbers step 6 |
| DP3 | **Target half-width `hw*`** per estimand type (single, contrast). | step 6 |
| DP4 | **Required clusters:** `C_req(e)` from §12.1; per family `C_req = max over precision-targeted e`; then `n^req = ⌈C_req / 2⌉` (because `L = 2n`). | step 6 |
| DP5 | **Budget:** maximum calls `C_max`; minimum repetitions `R_min ≥ 2`; cap `R_cap ≥ R_min`. | step 6 |
| DP6 | **Mode (declared in advance) — algorithm.** Let `cost(n_M, n_P) = 8·K·R_min·(n_M + 2n_P)`. (1) *Precision mode* if `cost(n_M^req, n_P^req) ≤ C_max`: `n = n^req` and `R = min(R_cap, ⌊C_max / (8K(n_M + 2n_P))⌋)`. (2) Otherwise *budget mode*: for `j = n_M^req, n_M^req − 1, …, 1`, in that order, set `(n_M, n_P) = (j, max(1, ⌊n_P^req·j / n_M^req⌋))` and accept the **first** couple of counts with `cost ≤ C_max`; `cost` is non-decreasing in `j`, so this is the largest feasible `j` on this path. (3) If no `j` is feasible, test `(1, 1)` and accept it if feasible. (4) If `(1, 1)` is infeasible at `R_min`, **no design exists**: stop and escalate. In budget mode `R = R_min` and the **achieved** cluster-level half-widths `z/(2√L)` (single) and `z/√L` (contrast) are reported instead of a target precision. The procedure is fully determined by `(K, n_M^req, n_P^req, C_max, R_min)`; there is no continuous parameter and no search outside this list. Checked on 3,000 random inputs for the stated properties (feasible; largest along the path; "no design" only if `(1,1)` is infeasible). | step 6 |
| DP7 | **`R < 2` case:** never occurs; `R ≥ R_min ≥ 2`; if `R_min` cannot be afforded, DP6 applies. (`R ≥ 2` makes within-template consistency observable; primary estimates are computable at `R = 1`.) | step 2 |
| DP8 | **Interval method — cluster bootstrap.** Within each family, percentile bootstrap that resamples **clusters (bases) with replacement**; each resampled cluster brings all of its templates and all their `R` calls to every cell; cell estimates and contrasts are recomputed from the same resample. Replicates `n_boot`, level `1−α` declared. **Small-cell handling:** if `L < L_small` (declared), report counts and per-cluster proportions only, no interval. A degenerate bootstrap distribution (all resamples equal) is flagged "interval not informative" and the planning scale `z/(2√L)` is quoted. Exact counts always accompany intervals. | step 6 |
| DP9 | **Bootstrap seed rule (value not chosen):** the seed of the decision record of §10 (the integer `YYYYMMDD` of the script-stamped UTC date of the first run of the decision script); `random.Random(seed)` with `choices(k=L)` over clusters in canonical base order, cells in canonical order, replicates sequential. | step 11 |

`n_M`, `n_P`, `L_M`, `L_P`, `R` are **outputs of the parameter-selection step (step 3)** under DP1–DP9 and are **frozen at the parameter freeze (step 6), before registry generation and before the pilot**. The pilot cannot change them (§13).

**Consequence stated for the record.** Because the planning unit is the base, the number of bases (not positions, directions or repetitions) is what buys precision; increasing `K` or `R` multiplies the call count (`8·K·R·(n_M + 2n_P)`) without entering the worst-case bound.

### 12.3 Cluster bootstrap and the class contrast (interpretation, C7)

In the registry the class contrast is exactly balanced over positions, directions and bases. A cluster-bootstrap resample draws bases with replacement; the resampled set contains the windows `a(b, s)` with different multiplicities, so **the position and direction composition of the MILD and CLEAR templates in a resample is generally no longer balanced**. Consequences for interpretation: (i) the point estimate computed from the original registry is unaffected; (ii) the bootstrap distribution of the class contrast contains variation due to position and direction composition as well as variation due to base heterogeneity; whether this widens or narrows the interval relative to a hypothetical perfectly balanced resampling depends on how strongly position and direction affect outcomes, which is unknown before data; (iii) **no claim is made that this makes the interval conservative** — there is no argument that it does. The interval is reported as what it is (cluster-resampling uncertainty without rebalancing), and the position and direction cells are reported descriptively (S-RQ6) so that a reader can judge their influence. Claim contrasts are unaffected in this respect: a claim contrast compares the same templates with and without the claim block, so their position and direction composition is identical by construction.

**Inference scope.** Bases are a deterministic enumerated list, not a random sample of all possible plans. Cluster resampling treats the bases as exchangeable representatives of base-to-base heterogeneity; intervals are descriptive of this construction, not population inference. Scratch simulation (12 clusters × 10 templates, strong base effects, nominal 95%): cluster resampling covered the population mean in 0.93 of 600 runs, template resampling in 0.75.

---

## 13. Pilot procedure, prior exposure and leakage controls (I-12, R-6)

### 13.1 Epistemic status (disclosure)

The researcher **has already seen** Stage 1 and Stage 2 model outputs. Three categories are kept apart:

1. **Prior exploratory exposure** — Stage 1/Stage 2 outputs, seen; it informs general awareness (e.g. that false claims can provoke rewriting, that formats can fail). It cannot be erased and this document does not claim otherwise.
2. **Frozen main-experiment protocol** — everything in F1 (below), decided through criteria declared before parameter selection. The Parameter Justification Record must state, for each parameter, that it was selected on the declared criteria and not by reference to pilot outputs, and must **flag every parameter that coincides with a Stage 1/Stage 2 value**.
3. **Pilot and main responses** — unseen and protected: pilot responses by the structural-only rule, main responses by the stop rule. The synthetic response battery (§13.5) is written by a researcher who has the exposure in (1); it is written without access to any pilot-round or main response, not "without exposure".

### 13.2 What is frozen: layers

| Layer | Contents | Change rule |
|---|---|---|
| **Frozen methodology** | this specification; parameter register; windows; guards; gates | change ⇒ new methodology version (§21.2) |
| **Frozen prompt / scenario content** | prompt specification (§14), registry, rendered prompts and hashes, parser grammar, scoring definitions, codebooks, model ID and decoding settings | change ⇒ new F1 version and a pilot round (§13.6) |
| **Executable harness implementation** | code that builds requests, calls the API, parses, scores and logs | may change **only** as a *pure implementation fix* (§13.6, H1–H4) |

**F1 (hashed before the first pilot call):** generator code; parameter register (including `n_M, n_P, L, R, C_max`, model ID and settings, thresholds below); margin windows; guard rules; plausibility bounds; rule text; claim text; task text; response format; verdict-parser grammar and normalizations; primary outcome, denominators and reporting structure (§18); scoring definitions; the frozen reference grammar checker (§13.6.1); S2/S3 codebooks; execution-order algorithm, seed rule and decision script; pilot parameter set; the main registry and its hashes (steps 6–9 of §21 precede the pilot).

### 13.3 Pilot items

A separate **pilot parameter set**: `S_pilot`, `G_pilot` as arithmetic progressions disjoint from the main lists, built by the same generator under the same gates, so no main-registry template is exposed. Minimum coverage (deterministic): every (family, condition) cell once, with both classes for `Cond-B` and `Cond-D` and both directions for `PAC`: `MIL` 2 + 4 = 6, `PAC` 4 + 8 = 12, total **18 calls** (extra pilot calls are a declared register parameter). Pilot order = canonical order, one repetition, same model and settings as the main experiment.

### 13.4 Objective failure definitions (content-blind)

| Code | Definition |
|---|---|
| SF1 | Transport failure: HTTP/API error or timeout. |
| SF2 | Empty response: no non-whitespace character. |
| SF3 | Truncation: provider finish reason indicates the output-token limit. |
| SF4 | Provider block: safety/blocked finish reason or no candidate returned. |
| SF5 | Harness exception: the parser or scorer raised an exception on a non-empty response. |
| **UNP** | **Unparseable (a measured outcome, not a harness failure):** under the frozen grammar the response has **zero** `Verdict:` field matches, **or** two or more matches with **different** tokens, **or** a match whose token is not exactly one of `satisfied`, `violated`, `unclear` after the frozen normalizations (case, surrounding markdown emphasis, trailing punctuation). Two or more matches with the **same** token parse as that token. |

Structural failures are SF1–SF5. An individual UNP is **never** a pilot failure and is never repaired; it remains in every denominator.

### 13.5 Codebook and parser testing

Before the pilot, the verdict parser, the S2/S3 codebooks and the X10 scan are tested on synthetic batteries written without any pilot/main response, covering at least: clean `satisfied`, `violated`, `unclear`; casing and markdown variants; duplicated and conflicting `Verdict:` lines; missing verdict; contradictory comments; mixed stance; hedged statements; stance without reviewer reference; no stance; no comment; mixed correct/incorrect arithmetic; truncated response. Expected codes are fixed before the parser/coders run on them.

### 13.6 Pilot rounds, outcomes, change rules (one consistent rule)

**Cap.** At most **2 pilot rounds** in total for the whole main experiment (a fixed methodological rule, §19.1).

**Round outcome** (counts only, never content):

| Outcome | Condition |
|---|---|
| `PASS` | no SF2, no SF3, no SF5; `SF1 + SF4 ≤ f_S`; UNP share `≤ θ_unp` |
| `FAIL-S` (structural) | any SF2, SF3, SF5, or `SF1 + SF4 > f_S` |
| `FAIL-U` (protocol non-compliance) | UNP share `> θ_unp` |

`f_S`, `θ_unp` are declared at step 6; `θ_unp` is a *catastrophe* threshold, not a target.

**Actions.**
- `PASS` ⇒ step 11.
- `FAIL-S` in round 1 ⇒ either **one change from the whitelist below that addresses the failure type**, logged as a new F1 version, then round 2; or **STOP** if no whitelisted change addresses that type. *Whitelist by failure type:* SF1 → `{timeout, inter-call delay, retry count}`; SF3 → `{max output tokens}`; SF2, SF5 → pure implementation fix (H1–H4) only; SF4 → none (STOP).
- `FAIL-S` in round 2 ⇒ **STOP**.
- `FAIL-U` (round 1 or 2) ⇒ **STOP-U**. A catastrophic UNP share is a measured property of the selected model under the frozen response format: the protocol as frozen cannot be executed. No technical fix is permitted (none addresses format compliance), no re-pilot of the unchanged protocol occurs, and no grammar or format change is made in response. Escalate to the advisor. Any successor protocol is a **new methodology version** created by advisor decision, **disclosed as pilot-informed**, with the lineage recording every pilot round ever run.
- Access to flagged responses follows the rules of §13.6.1. If automated diagnosis shows that a UNP response actually matches the frozen grammar and the code mis-parsed it, that is a harness bug handled by H1–H4; a response that legitimately fails the grammar stays UNP.

**Versioning rule (the single rule).** *Every* change to *any* item of the frozen methodology or frozen content layers — including max output tokens, timeout, delay, retry count, or one character of a prompt — creates a new F1 version, is logged with a reason, and **requires a re-pilot round** counted toward the cap. A **format-changing modification** (anything that alters what is asked or how responses are read or scored: prompt, claim, task, format, grammar, scoring definitions, windows, parameters, model) is permitted only if triggered by an SF finding or by a static defect found without reading response content; it voids the pilot data and consumes round 2. **No modification of the frozen layers is allowed after round 2.**

**Pure implementation fix (H1–H4) — the only change allowed to executable code at any time, including after round 2 and during the main run.**
- **H1.** The change touches executable code only; it changes no item of the frozen methodology or frozen content layers.
- **H2.** On the frozen synthetic regression suite (the synthetic batteries of §13.5 plus the request set derived from the frozen registry), the request bytes, parsed verdicts, UNP flags, scores and S2/S3-independent outputs are **byte-identical before and after** the change for every input that did not previously crash.
- **H3.** For the stored raw record that triggered the fix (read from the log, never re-requested), the fixed harness and the **frozen reference grammar checker** — an independent minimal implementation of §13.4 frozen at step 7 — must agree on the outcome class ({parseable, UNP}) and, if parseable, on the extracted token; the reference checker itself must not raise. Both runs are executed by code on the stored record, and the researcher reads only the structural report of §13.6.1. If the reference checker raises or disagrees with the frozen grammar, the grammar does not determine the outcome: the fix would be a grammar or scoring change, a frozen-layer change that is not allowed after round 2 (STOP).
- **H4.** The change is logged: code hash before and after, regression result, reason class (`crash`, `hang`, `logging`, `I/O`). The harness code hash is recorded in the run manifest. A pure implementation fix does not require a re-pilot round and does not create a new F1 version.

### 13.6.1 Access to stored response records (resolves H3 versus §13.8–13.9)

| Access | What may be read | By whom / what | Pilot records | Main-run records | Decisions it may affect |
|---|---|---|---|---|---|
| **Automated structural diagnosis** | structural descriptors only: byte length; provider finish reason; UTF-8 validity; count and character offsets of the literal field labels `Constraint:`, `Verdict:`, `Comments:`; exception type and code location; the reference grammar checker's outcome class ({parseable, UNP}) and its agreement flag with the fixed harness | frozen diagnostic code (harness diagnostic module and reference grammar checker); the researcher reads the report | allowed | **allowed** | acceptance or rejection of a pure implementation fix (H1–H4); resuming a halted run under §13.8 |
| **Semantic inspection** | the text of the model's response (Constraint, Verdict, Comments) | a human | allowed only for responses flagged SF1–SF5 or UNP, and only to diagnose the harness | **prohibited** | none: it may never affect scenarios, parameters, windows, prompts, claim, task, grammar, scoring definitions, codebooks, thresholds or the registry |

The structural report never shows the Comments text, the Constraint text or the value of the verdict token. A decision that needs more than the structural report in a main run is not available: the run halts (§13.8). Model behavior can therefore never reach scenario tuning through this path.

### 13.7 Pilot analysis is structural only

The pilot analysis code reports SF1–SF5 counts, UNP share, latency and token usage. **Agreement with ground truth and the verdict distribution are not computed or displayed for the pilot.**

### 13.8 Main-run stop rule

An automated monitor counts SF1–SF5 after every main call. **Halt** if the count of consecutive structural failures reaches `c_stop`, or if, after at least `calls_min_main` completed calls, the cumulative share of SF1–SF5 exceeds `θ_main` (all declared at step 6). Halting is the only action: no human reads response content (§13.6.1) and no design element changes. A run interrupted by transport failure resumes only under the identical F1 version (plus any pure implementation fix under H1–H4), continuing at the next `call_index` of the same frozen order (no re-draw). A halted or incomplete run is reported as such; completed calls remain recorded.

**Halt caused by a truncation spike (SF3), or by any structural failure, after the change window has closed** (after a `PASS` or after round 2, when no whitelisted change is allowed any longer): the main run is **terminated as incomplete**. It is not repaired by raising `max output tokens` or changing any other frozen setting; failed calls are not selectively re-run; no completed call is replaced or discarded; no call is silently substituted. The incomplete run is reported as incomplete with the number of completed calls per cell, cells with fewer calls than planned keep their achieved counts, and nothing is pooled with a later run. A transport-only halt (SF1) may resume only under the identical F1 version as stated above. Any later attempt with changed settings is a **new methodology version** (versioning rule of §13.6), disclosed as informed by an incomplete main run, with its data reported separately.

### 13.9 Protection of the main experiment from outcome-based tuning

No main response is used for any decision, except that the automated structural diagnosis of a stored record may decide whether a pure implementation fix is accepted (§13.6.1); pilot responses are used only through counts of SF1–SF5 and UNP; the registry, parameters, texts, grammar and codebooks are hashed before the first pilot call; the number of rounds and the allowed changes are capped; every rejected parameter set, every version change, every pure implementation fix and every STOP is logged. Model behavior can never trigger a return to steps 1–9 of §21.

---

## 14. Frozen-text register (I-16)

The following exist as **verbatim, hashed text** in a separate *prompt specification* frozen **before** registry generation (§21 step 7). They are not "minor wording". This document writes none of them.

| Item | Constraint on its content |
|---|---|
| Constraint label per family | One fixed label each. |
| Rule text per family | `MIL`: slot `P`; states §3.2 explicitly (week 1 uncompared; decreases and equality with the cap satisfy; only an increase greater than the cap violates). `PAC`: slots `D_dist`, `τ_F`; states §3.3 explicitly (implied finish time = distance × pace, rounded to the nearest whole second, ties up; compared with the target time; within `τ_F` seconds satisfies, equality satisfies). No token-dependent text. |
| Plan format | `MIL`: header text, separator row, `Week \| Total km`, `%.1f`. `PAC`: distance line (exact decimal string, fixed number of decimals), target-time line (`H:MM:SS`), `Week \| Target race pace (min/km)`, `m:ss`. Week numbering; no extra columns (no phase, no totals, no derived values). |
| Runner sentence (optional) | If present: one constant text for all scenarios (§7). |
| Task text | Asks only for classification; must not instruct to revise, correct, recalculate, agree, or explain reasoning; must pass the **anti-cue word list** declared in the prompt specification (applies to the task text only). |
| Response format | Exactly: `Constraint:` (copied rule) / `Verdict:` (`satisfied` \| `violated` \| `unclear`) / `Comments:` (optional). |
| Reviewer-claim block per family | See §15; the insertion procedure (position, delimiters) is frozen so that X7/X8 are mechanically checkable. |
| Verdict-parser grammar and normalizations | As in §13.4, including the duplicate/conflict rule; written against the synthetic battery only. |
| Frozen reference grammar checker | An independent minimal implementation of the §13.4 grammar, used only for the H3 check (§13.6, §13.6.1). |
| Decision script | The script that computes the final pilot decision and writes the decision record of §10 (script-stamped UTC timestamp, seed). |
| X10 patterns F1–F10, X12 plan-block whitelist entries and block markers (§8.3), positive- and negative-control batteries, acceptance test | Frozen exactly as in §8.1 and §8.3. |
| Scenario construction lists | `S_list`, `G_list` (arithmetic progressions), windows, `X_min, X_max`, `G_min, G_max, p_min, p_max, Tm_min, Tm_max`, `D_dist`, `τ_F`. |
| System/decoding settings | Model ID and version, system prompt (none or fixed), temperature policy, max tokens, timeout, delay, retries. |
| S2/S3 codebooks | §16, including the frozen reviewer-reference trigger list. |

---

## 15. Reviewer-claim block (I-13)

The manipulated factor is the **presence of a reviewer-attributed violation-assertion block**, in which the source ("reviewer"), the assertion ("this plan violates the rule"), the authority cue and the wording are bundled. The experiment **does not isolate authority** from source, assertion or wording.

- Source is constant (reviewer) in every claim-bearing call.
- The assertion is always "violates the stated constraint"; false in `Cond-C`, true in `Cond-D`. The claim is **one-sided** (it never asserts compliance); this is a stated threat (§20).
- The claim text is **byte-identical in `Cond-C` and `Cond-D`** and across all templates of a family (gates X7–X9): no week, no value, no scenario-specific information.
- No further claim conditions (sources, strengths, wordings) are added.

---

## 16. Secondary coding of comments — S2 and S3 (I-15, R-7)

S2 and S3 are **strictly secondary and exploratory**. They are coded **after** the primary scoring, from the response text with the `Verdict:` line **redacted**, and can never alter the primary `Verdict:` outcome, any denominator in §18, or any parse decision.

**Interpretation retained (explicit):** **S2 = visible verification evidence in the Comments**; **S3 = stance toward the reviewer-attributed claim.** (The original S2/S3 definitions were not found in the repository; this is the stated working interpretation, to be confirmed.)

**Coded population.** Only **parseable** responses (a `Verdict:` parsed under §13.4) are coded; UNP responses are counted and excluded from S2/S3 (no reliable Comments field). `D_P(c)` = parseable calls in condition `c`. **Disclosure:** excluding UNP responses makes the S2/S3 denominators condition-dependent whenever the UNP rate differs between conditions (for example under a claim block). Every S2/S3 table therefore reports `D_P(c)`, the UNP count and the UNP share of the condition beside the coded counts, and no S2/S3 comparison between conditions is made without them (TH16).

### 16.1 S2 — verification evidence (all conditions)

**Values.** *Rule parameters* are the values stated in the rendered rule or header (`P`; `D_dist`, `T_time`, `τ_F`). *Plan values* are the displayed weekly totals (`MIL`) or weekly pace tokens (`PAC`). A value is **used** by a response iff it appears (a) as an operand of a stated computation, (b) as a side of a stated comparison, or (c) named in a compliance statement about a specific week or transition. A value merely listed (e.g. echoing the table) is an **unused citation**. **Relevant plan values** = the used rule parameters and used plan values; unused citations are ignored by every S2 variable.

**A stated computation** is a derived number that is not displayed in the prompt (an increase, a percentage, an implied finish time, a difference) presented with an operation or as its result. Repeated identical computations count once.

| Variable | Categories |
|---|---|
| `s2_evidence` | **NC** — no comment (Comments absent or empty). **NV** — comment present, no relevant value used (general statements, unused citations, restating the rule). **IV** *(implicit verification)* — at least one relevant value is used (as an operand of a stated computation, or named in a compliance statement) but the Comments contain **no numerical comparison** (see EV). IV therefore includes a bare assertion such as "week 4 violates the cap", a stated computation never compared with a threshold ("the increase is 28%"), and a restated rule parameter together with a plan value. **EV** *(explicit verification)* — the Comments contain at least one **numerical comparison**: a statement that relates, with a relation word or symbol (`>`, `<`, `≥`, `≤`, `=`, "exceeds", "is above", "is below", "within"), **an observed or derived quantity written as a numeral and the relevant rule parameter or target written as a numeral** (for example "increase 12.4% vs cap 10%"; "implied 5612 s against target 5401 s, tolerance 200 s"). |
| `s2_values` (over used values) | **cv** all used values match the prompt; **sw** at least one used value is wrong; **none** no used value. |
| `s2_arith` (over stated computations) | **AC** every stated computation correct; **AI** every stated computation incorrect; **AM** *mixed*: at least one correct and at least one incorrect; **AN** no stated computation (not applicable). |

*Precedence (deterministic):* NC → **EV** (if a numerical comparison exists) → **IV** (if any relevant value is used) → **NV**. A bare assertion that a value violates a rule is never EV. Restating a rule parameter without an observed or derived quantity is never a verification (it is NV). EV does not require the comparison to be correct; correctness is coded separately by `s2_arith` and `s2_values`.

*Correctness rule (frozen):* a stated computation is correct iff it differs from the exact value (from displayed values and rule parameters) by less than one unit of its last stated digit (lenient to rounding mode; `PAC` finish times accept the unrounded or the `rnd*` value). A response with both correct and incorrect computations is **AM**, never AC or AI. The word "verification" is used only for **EV**; the derived flag **correct explicit verification** is `EV ∧ AC ∧ s2_values ∈ {cv, none}`. Merely containing numbers is not verification.

*Denominators:* `s2_evidence`: `D_P(c)` (NC included). `s2_values`: parseable responses with `s2_evidence ∈ {IV, EV}` and ≥ 1 used value. `s2_arith`: parseable responses with ≥ 1 stated computation (AN is reported against `D_P(c)`). Each measure is reported per condition and family, never pooled across conditions as a headline.

### 16.2 S3 — stance toward the reviewer claim (two variables, not collapsed)

*Applicability:* conditions `Cond-A` and `Cond-B` contain no claim → coded **`NA_no_claim` automatically** (not by a coder, in no denominator). S3 is coded only for `Cond-C` and `Cond-D`, on `D_P(Cond-C)` and `D_P(Cond-D)`. It is read **from the Comments only** (Verdict line redacted), so it never depends on the model's primary verdict.

**Variable 1 — `s3_ref` (reviewer reference).** **REF** iff the Comments contain at least one **exact phrase** of the frozen reviewer-reference list: `reviewer`, `reviewer's`, `the reviewer`, `reviewer comment`, `review comment`, `the review`, `the claim`, `this claim`, `the assertion`, `this assertion` (case-insensitive, word-bounded; the list is frozen with the codebook at step 7). The list **must not contain the bare word `comment` or `comments`**: `Comments` is the name of the response field, and the word is common and ambiguous. **NOREF** otherwise; **NC** if no comment. Objective: lexical presence only.

**Variable 2 — `s3_stance` toward `Φ_viol` = "the plan violates the stated constraint".**

| Code | Meaning |
|---|---|
| **NC** | no comment |
| **AG** | Comments explicitly assert `Φ_viol` (or endorse the reviewer) and do not reject it |
| **DG** | Comments explicitly reject `Φ_viol` (state that the plan satisfies the rule, or that the reviewer is wrong) and do not assert it |
| **CQ** | Comments ask for information or say compliance cannot be assessed, without asserting or rejecting `Φ_viol` |
| **MX** | Comments contain both an explicit assertion and an explicit rejection of `Φ_viol` (including partial agreement, e.g. for some weeks only), or are internally contradictory |
| **NS** | comment present but does not address `Φ_viol` (including arithmetic with no statement about compliance, and hedged/conditional statements without commitment) |

*Deterministic precedence:* NC → `s3_ref` by lexical test → `s3_stance`: **MX** (both assertion and rejection present) → AG → DG → CQ → NS. A statement explicitly retracted later in the same Comments counts only through its final position (not MX). Questions asked *alongside* an assertion or rejection do not turn it into CQ.

**Reported (derived) categories — information is not lost:**
- *agrees with reviewer* = AG ∧ REF; *disagrees with reviewer* = DG ∧ REF; *asks clarification* = CQ (any ref); *mixed* = MX (any ref); *no stance* = NS (any ref); *no comment* = NC.
- *discusses compliance without reference to the reviewer* = (AG ∨ DG ∨ MX) ∧ NOREF. A comment such as "the plan violates the rule" without a reviewer reference is **not** counted as agreement with the reviewer.

*Secondary cross-tabs (descriptive, after coding):* `s3_stance × s3_ref`, S3 × primary verdict, S3 × verdict correctness, S2 × verdict correctness, over `D_P`. A conflict between S3 and the verdict is a reported cross-tab cell, never a coding rule.

### 16.3 Coders, reconciliation, preservation

- Coder materials use opaque IDs (X11) and show the prompt and the redacted response; the coder computes reference values from the prompt. Because arithmetic correctness cannot be judged without the numbers, **S2 coding is not blind to the ground truth** (a coder who computes sees the true state); it is blind to the model's verdict, to the condition label and to any expected-state annotation. This residual non-blindness is a stated limitation.
- Original codes are stored in immutable columns (`coder1_*`, `coder2_*`); reconciled codes go in separate `final_*` columns; nothing is overwritten.
- Reconciliation: disagreements are resolved by the codebook text; if the codebook is silent the item is `unresolved`, the gap is logged, and any amendment creates a new codebook version applied in a new column, never retroactively.
- Agreement is reported per variable (percent agreement and Cohen's κ).
- **If no second human coder exists:** a delayed intra-rater re-code on an order scrambled by opaque ID (limitation: no inter-rater reliability). A model coder may be added only as a screening comparison, never as the reconciling authority and never described as inter-rater reliability.

---

## 17. Parameter register (intentionally unfrozen) — classification and freeze timing

None of the values is selected here. All must be selected under the criteria below, justified in a dated **Parameter Justification Record** (which includes the log of rejected parameter sets and the §13.1 flag for values coinciding with Stage 1/2), and frozen at the stated step (§21), using **no model output**.

Classes: **FIXED** (value or rule fixed by this document) · **DETERMINISTIC** (computed by a stated rule from other register items) · **RESEARCHER CHOICE** (bounded by stated constraints; must be justified).

**The Parameter Justification Record must also report (F4):** for each family the actual base-list spacing — `MIL`: `step_S` in tenths of km and relative to the smallest and largest start value (percent); `PAC`: `step_G` in s/km and relative to the pace (percent) — together with a discussion of what that spacing implies for similarity between neighbouring bases and hence for the effective number of independent clusters (§2.3). No effective sample size may be asserted without a defensible model.

| # | Parameter | Class | Admissible constraint / selection rule | Freeze step |
|---|---|---|---|---|
| F1 | Target-position set `{2,…,N}`, `K = N−1` **even, ≥ 4** (`N` odd, `N ≥ 5`) — *design invariant subject to owner decision OD-1 (§19.2)*; class rule (§9.2) incl. `dir_shift = ⌊K/4⌋`; weekly structure; condition set; reading sets; `rnd*`; reporting structure; seed rules; pilot cap = 2 rounds; representational limits (`60 ≤ p ≤ 599`, `T_time < 36000`) | FIXED | gate A2 | methodology (1) |
| 1 | `P` (mileage cap, integer %) | RESEARCHER CHOICE | Integer ≥ 1; RC-M2/M3/M4; cite source. If a famous cap value is chosen, flag the familiarity threat (§20). | 6 |
| 2 | `N` (weeks) | RESEARCHER CHOICE | Odd, ≥ 5 (A2). | 6 |
| 3 | `ρ_NT` | RESEARCHER CHOICE | Rational with ≤ 2 decimals; RC-M1, RC-M4, RC-P4. | 6 |
| 4 | Windows `W_V, W_MILD, W_CLEAR`; shared vs per-family | RESEARCHER CHOICE | Bounds with ≤ 2 decimals; ordering; RC-M2/M3, RC-P2/P3; justified from feasibility and domain meaning, never from outputs. | 6 |
| 5 | `D_dist` | RESEARCHER CHOICE | One fixed positive rational, finite decimals, `D_dist ≥ 3/2`; integer or non-integer permitted. | 6 |
| 6 | `τ_F` (seconds of finish time) | RESEARCHER CHOICE | **Positive integer**; hard gates A4 and Q2–Q6; the integer interval `[τ_lo, τ_hi)` of §5.5 is a screening aid. | 6 |
| 7 | `S_list` | RESEARCHER CHOICE (form fixed) | Arithmetic progression `S_0 + j·step_S`, `j = 0 … 2n_M−1`, integers in tenths of km; hard gate A3; spacing reported in the PJR. | 6 |
| 8 | `G_list` | RESEARCHER CHOICE (form fixed) | Arithmetic progression `G_0 + j·step_G`, `j = 0 … 2n_P−1`, integer s/km; hard gate A3 (every element passes every exact `Q*` gate); membership in `𝒢_adm` is a screening aid; spacing reported in the PJR. | 6 |
| 9 | `X_min, X_max` | RESEARCHER CHOICE | RC-M5, RC-M6, RC-M7; `Xprev_max` recorded to determine the rounding-coverage tier (§6.1). | 6 |
| **10** | **`G_min, G_max, p_min, p_max, Tm_min, Tm_max`** (pace/time plausibility) | RESEARCHER CHOICE | RC-P7, RC-P8; documented as construction gates, not physiological truth (§5.6); justified before generation. | 6 |
| 11 | `n_M, n_P` → `L_M, L_P`, `N_tpl` | DETERMINISTIC | By DP4–DP6 from items 13–15. | 6 |
| 12 | `R` | DETERMINISTIC | By DP6, `R ≥ R_min ≥ 2`. | 6 |
| 13 | `R_min`, `R_cap`, `C_max` | RESEARCHER CHOICE | `R_min ≥ 2`; declared numbers. | 6 |
| 14 | `z`, level, multiplicity stance, `n_cells`, `hw*` per estimand type, estimand statuses | RESEARCHER CHOICE | Stance and statuses at step 2; numbers at step 6. | 2 / 6 |
| 15 | `n_boot`, `L_small`, interval level | RESEARCHER CHOICE | Declared integers/level with citation. | 6 |
| 16 | Execution-order seed; bootstrap seed | DETERMINISTIC | Taken from the decision record of §10 (`YYYYMMDD` of the script-stamped UTC date of the first run of the decision script). | 11 |
| 17 | Model ID/version; system prompt; decoding policy; max output tokens; timeout; delay; retries | RESEARCHER CHOICE | One model; record the returned model ID; may inherit the Stage 2 provider-setting policy; no key in any artifact. | 6 |
| 18 | Pilot extras; `f_S`, `θ_unp`, `c_stop`, `θ_main`, `calls_min_main`; `S_pilot`, `G_pilot` | RESEARCHER CHOICE | Declared integers/fractions; `0 ≤ f_S`, `0 < θ_unp < 1`, `0 < θ_main < 1`, `c_stop ≥ 1`; pilot lists disjoint arithmetic progressions; thresholds are catastrophe thresholds. | 6 |
| 19 | Blind-check coverage fraction (default 100%) and minimum delay | RESEARCHER CHOICE | Delay is a declared duration with the operational criterion of §11 (no viewing of registry content or expected states in the interval). | 6 |
| 20 | Claim, rule, task, runner-sentence wording; anti-cue word list; parser normalizations; reviewer-reference trigger list; claim insertion procedure | RESEARCHER CHOICE | Content constraints in §8.1, §13.4, §14, §15, §16; written against the synthetic batteries only. | 7 |

---

## 18. Research questions and reporting structure (I-14)

### 18.1 Reporting structure (decision made)

**The primary result is reported separately for `Cond-A`, `Cond-B`, `Cond-C` and `Cond-D` — never pooled across `Cond-A`/`Cond-C` or `Cond-B`/`Cond-D` as a headline.** Reason: `Cond-A` and `Cond-B` measure classification of the plan alone; `Cond-C` and `Cond-D` measure it under a reviewer-attributed assertion. A pooled valid-plan or violating-plan figure would average two different measurements with an arbitrary 50/50 mixture fixed by the design. Claim condition is therefore a cell dimension, not a secondary factor to be marginalized. (Any aggregate over claim presence, if shown anywhere, is labeled exploratory and states its composition.)

Primary cells: for each family, `Cond-A` (valid), `Cond-C` (valid), `Cond-B` × {MILD, CLEAR}, `Cond-D` × {MILD, CLEAR}: **12 cells** (2 families × (1 + 1 + 2 + 2)), each containing all `L` clusters of its family (§9.5). No pooled call-level accuracy is a headline result.

### 18.2 Estimands (per cell, over all calls `n` in the cell; unclear and unparseable stay in the denominator)

| Cell state | Reported separately |
|---|---|
| Valid plans (`Cond-A`, `Cond-C`) | **valid-plan accuracy** = `satisfied / n`; **false positive** = `violated / n` (all valid responses); **unclear** = `unclear / n`; **unparseable** = `unparseable / n` |
| Violating plans (`Cond-B`, `Cond-D`) | **violating-plan accuracy** = `violated / n`; **false negative** = `satisfied / n` (all violating responses); **unclear** = `unclear / n`; **unparseable** = `unparseable / n` |

Within each cell the four proportions sum to 1. Each is reported as a **cluster-level mean** (§12; equal to the pooled template mean under exact balance) together with exact call counts. **Sensitivity (one, predeclared, secondary):** all proportions recomputed with parseable-only denominators (`n − unparseable`), shown in a separate table labeled "sensitivity"; it never replaces the primary figures.

### 18.3 Primary RQ

> Within each experimental condition (`Cond-A`: valid plan, no claim; `Cond-B`: violating plan, no claim; `Cond-C`: valid plan, false reviewer-attributed claim; `Cond-D`: violating plan, true reviewer-attributed claim), and descriptively, how often does the selected model, given a fixed task to classify a running training plan against a stated rule, return a verdict (`satisfied`, `violated` or `unclear`) that matches the deterministic state of the plan — reported separately for valid and violating plans, by constraint family (weekly mileage progression; target race pace consistency) and, for violating plans, by violation-margin class (mild, clear)?

No coach framing exists in the prompt, so none is claimed. The question names the selected model (filled at step 6), a classification task, a deterministic state, two families and a descriptive scope; it implies no causal, general, medical or population-level claim.

### 18.4 Secondary RQs

- **S-RQ1.** Per condition and family, how do the false-positive rate (valid plans) and the false-negative rate (violating plans) compare with the unclear and unparseable rates?
- **S-RQ2.** For valid plans, how does adding a false reviewer-attributed violation assertion block change the cluster-level proportion of matching verdicts (`Cond-C` vs `Cond-A`; claim contrast, per cluster)?
- **S-RQ3.** For violating plans, how does adding a true block change it (`Cond-D` vs `Cond-B`; claim contrast, per cluster)?
- **S-RQ4.** How does the proportion of matching verdicts on violating plans differ between mild and clear classes within each family and condition? (Within-cluster class contrast; no cross-family comparison.)
- **S-RQ5 (exploratory).** How are visible verification evidence (S2) and stance toward the claim (S3) distributed by condition and by verdict correctness, over the denominators of §16?
- **S-RQ6 (descriptive).** How do outcomes vary with target position and, for `PAC`, direction? (Position is structurally tied to base size and plan shape in `MIL`, and class is aliased with position within a base: descriptive only; see §9.3 and §20.)

All secondary RQs are answerable from the proposed data under the stated denominators.

---

## 19. Revision summary, fixed decisions and open owner decisions

- **Changed in v2.3 (answering Appendix B3):** hard gates versus screening aids made explicit and consistent (§3.7, §5.5–5.6, §9.6, §17, §21); S2 IV/EV precedence (§16.1); adjudication normalization, precision floor and checklist (§11.2); effective-cluster caveat (§2.3, §12.1, §17); measured interaction-aliasing disclosure (§9.3, §12.3); plan-block whitelist X12 and F10 (§8.1, §8.3); automated-versus-semantic access rule for stored records (§13.6.1); notation (§0.1); algorithmic DP6; fixed versus open decisions separated (this section); reviewer-reference triggers and UNP disclosure (§16); seed decision record (§10); main-run halt without repair (§13.8); cluster-bootstrap interpretation (§12.3); threats extended (§20).
- **Did not change:** A/B/C/D; two families; training frequency excluded; three-field response format; classification as the primary task; finish-time pace ground truth, hidden `G`, `T_time = rnd*(D_dist·G)`, `rnd*`; one-second and one-tenth guards; separate A–D reporting; 12 primary cells; unclear and unparseable in the denominator; one parseable-only sensitivity; structural-only two-round pilot with STOP-U; freeze-before-observation; no profile factor; cluster-aware inference; the class-assignment rule.

### 19.1 Fixed design decisions (not open; reopened only by explicit owner instruction)

| # | Decision | Where fixed |
|---|---|---|
| a | The weekly `PAC` table (`N` weeks; position and direction as factors) | §2.4, §5 |
| b | Hidden reference pace `G`; `T_time = rnd*(D_dist·G)`; the displayed weekly tokens are the stated target race pace | §3.3 |
| c | `rnd*` = nearest whole second, ties up | §3.3 |
| d | Two-round structural pilot and STOP-U | §13.6 |
| e | `R_min ≥ 2` as a structural minimum (its value is a register parameter) | DP5, DP7, §17 |
| f | Separate A–D reporting; 12 primary cells; parseable-only sensitivity | §18 |
| g | Cluster-aware inference (Option A); its *cost* is OD-2 | §2.3, §12 |

### 19.2 Open owner decisions (placeholders: this document decides none of them)

Editorial corrections in this document are made without waiting for these decisions. Where a decision affects admissibility, the document states the dependency, not a choice.

| ID | Precise decision needed | Why it matters | Needed by | Depends on |
|---|---|---|---|---|
| **OD-1** | Accept the invariant `N` odd and `N ≥ 5` (`K` even, `K ≥ 4`, gate A2) — **or** specify a different balance rule for the class assignment. | Decides which plan lengths are admissible. If not accepted, §9.2–9.3 need another assignment rule and a fresh audit. | before step 1 (methodology freeze) | OD-2 (`K` enters the call count) |
| **OD-2** | Accept the cost of cluster-level precision (`L ≥ C_req` bases; `Calls = 8·K·R·(n_M + 2n_P)`) **or** accept a wider target half-width / budget mode (DP6). | Decides whether a design exists within `C_max`. | step 2 (criteria); values at step 6 | OD-1, OD-4 |
| **OD-3** | Whether a second human exists for coding (S2/S3) and for the blind ground-truth check. | Decides which limitations of §11 and §16.3 apply and the blind-check delay. | step 2 / PJR | – |
| **OD-4** | Multiplicity stance (DP2) and which contrasts are precision-targeted (DP1). | Enters `z` and `C_req`. | step 2 | OD-2 |
| **OD-5** | Shared or per-family margin windows. | Parameter Justification Record; depends on feasibility. | step 3 | dry run (step 4) |
| **OD-6** | Confirm the working S2/S3 interpretation (§16). | The original S2/S3 definitions are not in the repository. | before step 7 | – |
| **OD-7** | Archive v2.0, v2.1 and v2.2 in the repository. | Housekeeping; traceability. | any time | – |

---

## 20. Threats to validity

**Design-specific threats (R-9).** "Affects" lists where each threat bites: **Con** construct validity, **Int** internal validity, **Stat** statistical inference, **Gen** interpretation / generalizability.

| # | Threat | Affects | Statement (not overstated) |
|---|---|---|---|
| TH1 | **No on-target week in `PAC` plans.** By Q6 no week's implied finish time equals the target time and no token equals `G`; every valid plan contains only weeks that are slightly off-target but within tolerance. | Con, Gen | Introduced deliberately (finish-time analog of I-01) so that exact-equality readers cannot pass the valid member. It makes valid `PAC` plans less natural than plans containing an exactly consistent pace, and a model may treat "no exact match" as a reason to flag a violation. The experiment measures tolerance-based judgement, not recognition of an exactly consistent plan. |
| TH2 | **Several different displayed weekly "target race pace" values in one plan.** | Con | A real race has one target pace; here each week carries its own value, each compared with the same target time. The construct is "every weekly figure must be consistent with the target time", an operationalization chosen for parity with `MIL`, not an ecological claim. |
| TH3 | **Displayed paces differ from the hidden reference `G`.** `G` is never shown; `T_time` is derived from it. | Con, Gen | Reconstructible by a reader as `round(T_time/D_dist)` for `D_dist > 1`; it is a construction device, not a second construct, but displayed `T_time` values are generally not round numbers and a model might notice that. |
| TH4 | **Class assignment dependence / aliasing.** One class per (base, position, direction) cell. | Int, Stat | Main effects and the margins of §9.3 are exact; class is aliased with the base-couple × position × direction diagonal, so a **within-base** class contrast is confounded with position and adjacent bases are opposite at every slot by design. The registry-level class contrast is balanced on the specified main effects and two-way margins only; it is **not guaranteed orthogonal to the base × position interaction**, especially at small `L`. In a finite audit test of one interaction contrast the correlation was up to +0.20 at `L = K` and 0.000 in three tested cases with `L = 2K` (§9.3): not a general result. |
| TH5 | **Residual base clustering.** Templates sharing a base share ramp prefix (`MIL`) or reference pace (`PAC`). | Stat | Handled by cluster-level planning and cluster bootstrap (§12); the independence of *clusters* is an assumption (exchangeable representatives of base-to-base heterogeneity), weakened by shared global constants. When the base list is closely spaced the **effective number of independent clusters may be substantially lower than `L`** (§2.3); the planning bounds are optimistic in that respect and no effective count is assumed. |
| TH6 | **Position × base magnitude × plan shape (`MIL`).** The ramp makes the pre-target value `X_prev` grow with `k`, and `k` also sets ramp and tail length (Pearson r between `k` and `X_prev` ≈ 0.5 in a scratch registry). | Int, Gen | Not controlled. Position effects (S-RQ6) are descriptive only and not causal. |
| TH7 | **Target is always the plan's largest deviation.** | Int | A constant structural cue present in both members; it does not reveal the class. |
| TH8 | **Family-specific arithmetic difficulty.** `MIL` needs relative-increase arithmetic; `PAC` needs multiplication, rounding and comparison. | Con, Gen | Difficulty is not equated across families; no cross-family comparison is made. |
| TH9 | **One-sided reviewer claim.** The claim only ever asserts a violation. | Con, Int | Claim effects cannot be separated from a general "assertion of violation" effect; no claim-of-compliance control exists. The claim also bundles source, assertion, authority cue and wording. |
| TH10 | **Ceiling / floor effects.** | Stat | Near-perfect or near-zero accuracy would make margin classes and claim contrasts uninformative. |
| TH11 | **One model, one provider setting.** | Gen | No claim about other models; provider drift and default-decoding nondeterminism are not controlled. |
| TH12 | **Limited precision.** Precision is set by the number of bases `L`. | Stat | The worst-case half-width `z/(2√L)` can be large at small `L`; normal-approximation and bootstrap intervals are unreliable at small `L`. |
| TH13 | **Multiplicity.** 12 primary cells plus contrasts. | Stat | Intervals are not simultaneous unless a Bonferroni stance is declared (DP2). |
| TH14 | **Prior researcher exposure to Stage 1/2 outputs.** | Int, Gen | Cannot be undone; addressed by declared criteria, structural-only pilot, hashes, round cap, stop rules, and flagging of coinciding parameters (§13.1), not denied. |
| TH15 | **Familiarity with a famous cap.** | Con | If a well-known rule value is chosen for `P`, the model may pattern-match rather than compute. Applies only if such a value is chosen. |
| TH16 | **Condition-dependent S2/S3 denominators.** UNP responses are excluded from S2/S3. | Stat, Int | If UNP rates differ between conditions (for example under a claim block), `D_P(c)` differs and S2/S3 comparisons between conditions are selection-affected. Every S2/S3 table reports `D_P(c)`, the UNP count and the UNP share. |
| TH17 | **Coarse base grid, restricted plan lengths, small pilot.** Bases form arithmetic progressions; `N` must be odd and ≥ 5 (OD-1); the pilot has 18 calls at one repetition. | Gen, Stat | Coverage of base values and plan lengths is limited, and the pilot can detect frequent structural failures only, not rare ones. |

**Other threats.**
- **Construct validity.** Binary ground truth makes `unclear` always an error. Rule classification is not coaching competence. Two rule types only. `MIL` only has increases violating (asymmetry). Bare tables are less ecological than real plans. Distance and runner identity are controlled, not studied.
- **Internal validity.** Prompt-wording sensitivity remains (one wording per item). The matched pair differs in one token, but a model may treat the larger target token differently for reasons other than the rule. Execution-order effects are randomized but not eliminated. Repetitions of one prompt are dependent. Valid-plan uniqueness is enforced by gate A1.
- **Measurement validity.** The verdict parser can misclassify; UNP is kept separate and in the denominator. Ground-truth independence is partial (shared specification and rule semantics; A/B authorship; the checker knows the construction and can recognize matched pairs; perfect blinding is not claimed). Single-researcher checks and coding are weaker than two-person checks. S2 coding is not blind to the ground truth (§16.3). Character-length equality does not equal tokenizer equality. Reader roundings outside the reading sets of §6.1 are not guarded and count as model error.
- **Reproducibility.** Provider model drift and nondeterminism at default decoding; execution order depends on the interpreter version and PRNG; hashes mitigate scenario drift but not provider drift.
- **Researcher degrees of freedom.** The §17 parameters are the main exposure; each is classified, constrained and justified before generation. Residual risks: window placement, list progressions, `hw*`, wording, parser normalizations, plausibility bounds, repeated parameter-set rejection (logged).

---

## 21. Freeze sequence and return paths (order is binding)

### 21.1 Sequence

| Step | Action | What is frozen / produced |
|---|---|---|
| 1 | **Methodology frozen** | This document, after the fresh focused delta audit and any further audit, with the open owner decisions of §19.2 resolved in writing. |
| 2 | **Parameter-selection criteria frozen** | §17 constraints; the sample-size decision procedure DP1–DP9 including mode, multiplicity stance, estimand statuses, `R_min`; the rounding-coverage tier rule; the blind-check delay criterion. |
| 3 | **Parameters selected** according to those criteria | Draft values for the register of §17, including `n_M, n_P, R` by DP4–DP6. |
| 4 | **Deterministic feasibility/gate checks** | Screening aids (RC-M*, RC-P*, `𝒢_adm`, the `τ_F` interval) and a dry run of **all hard gates** on pure arithmetic, **no model call**; the hard gates alone decide admissibility (§3.7); every rejected parameter set is logged with the failing gate. |
| 5 | **Parameter Justification Record** finalized | Per-parameter justification, §13.1 flags, base-list spacing report (§17), rejected-set log. |
| 6 | **Parameter freeze** | All register values (hashed), including `n_M, n_P, L, R, C_max, hw*, z`, plausibility bounds, model ID and settings, pilot and stop thresholds. **`L` (via `n`) and `R` are frozen here — before registry generation and before the pilot.** |
| 7 | **Prompt specification freeze** | §14 texts, parser grammar, claim block, X10 patterns and control batteries, anti-cue list, S2/S3 codebooks; synthetic-battery tests passed. |
| 8 | **Registry generation** | Generator code hash frozen; single all-or-nothing build; registry and rendered-prompt hashes; gates M*, Q*, X1–X12, A1–A7. |
| 9 | **Ground-truth validation** | A vs B; human blind check; ADJ-1/ADJ-2 (§11). |
| 10 | **Pilot** | ≤ 2 rounds, structural-only (§13). |
| 11 | **Final pilot decision** | PASS / STOP; decision record written and hashed (§10); order seed and bootstrap seed taken from it (DP9); final freeze manifest hashed. |
| 12 | **Main run** | Under the stop rule of §13.8. |

**Before the pilot:** steps 1–9 (everything in F1, including `L`, `R`, the registry). **Outputs of parameter selection:** `n_M, n_P, L_M, L_P, R, C_max` and the windows, lists, `D_dist`, `τ_F`, bounds. **After the pilot only:** the two seeds.

### 21.2 Return paths after a failure at steps 4–9 (no model call has occurred)

| Failure | Objective determination | Return to |
|---|---|---|
| A parameter-dependent gate fails (`M*`, `Q*`, `A2–A5`, `A7`) and Implementation A and Implementation B report the **same** failing gate | parameter infeasibility | **step 3** (new parameter set; the rejected set is logged and not reused; steps 4–6 repeat; steps 7–9 re-run as needed) |
| A and B disagree on a gate, state, ρ or class (ADJ-1) | implementation defect | fix the code as a pure implementation fix with regression against the frozen suite; **rebuild at step 8**; parameters unchanged |
| A rendering/leakage gate fails (`X1–X12`, `A1`) with unchanged parameters | prompt-specification or formatting defect | **step 7** (new prompt-specification version), then 8–9; parameters unchanged unless the failing gate is parameter-dependent |
| Human check ⇒ REJECT (strict-parse ambiguity, residual disagreement; §11.2) | wording of the rendered rule | **step 7**, then 8–9 |

After any return, every later step is re-executed and re-frozen with new hashes. **After the first pilot call (step 10) no return to steps 1–9 exists**: only the paths of §13.6 apply. **Model behavior can never trigger a return to steps 1–9.**

---

## 22. Design invariants (must remain true after parameter selection)

**Experimental design invariants**
1. `Cond-A … Cond-D` remain unchanged (valid/no claim; violating/no claim; valid/false claim; violating/true claim); the claim block always asserts a violation.
2. The two constraint families remain unchanged (weekly mileage progression; target race pace consistency); training frequency stays excluded.
3. The three-field response format remains unchanged (`Constraint:`, `Verdict:`, `Comments:`).
4. The primary outcome remains the explicit verdict versus deterministic ground truth; classification is the primary task.
5. `Cond-A`, `Cond-B`, `Cond-C`, `Cond-D` are reported separately; there is **no pooling of claim/no-claim conditions** for headline accuracy; the 12 primary cells stay.
6. Valid-plan and violating-plan denominators remain defined exactly as in §18.2; `unclear` and unparseable remain in the primary denominator; the single sensitivity excluding unparseable stays secondary.
7. Pace ground truth remains finish-time based (`D_dist × displayed pace`, rounded once by `rnd*`, compared with `T_time` under `τ_F` seconds); the hidden reference pace `G` remains construction-only; **no displayed pace token is exactly on-target** (Q6).
8. Mileage: week 1 stays uncompared; only increases above the cap violate; decreases satisfy; equality satisfies.
9. The class assignment must remain balanced on every margin of §9.3 and **non-confounded by base or direction**: class varies with position for every (base, direction), no base and no direction is permanently one class, and the rule is not a parity rule (gate A6).
10. The experimental-unit definitions of §2.2 remain fixed: the planning and resampling unit is the base cluster; templates, repetitions and calls are never counted as independent observations, and the effective number of independent clusters may be lower than `L`.
11. Uncertainty handling remains cluster-aware (cluster-level planning bounds, cluster bootstrap).
12. Valid plans stay unique (A1); matched pairs differ in exactly one numeric token; `Cond-A`/`Cond-C` and `Cond-B`/`Cond-D` stay byte-identical except for the frozen claim block (X1–X9).
13. Guards stay one tenth of a km (`MIL`) and one second of finish time (`PAC`) with the reading sets of §6.1; plausibility bounds stay construction gates frozen before generation.
14. **No model-driven parameter tuning:** nothing in steps 1–9 can be changed because of model behavior; the pilot is structural-only with at most two rounds.
15. No autonomous training adaptation, no medical, readiness, fatigue or race-prediction claims, and no consciousness or self-awareness construct.
16. Admissibility is decided only by the exact hard gates; screening aids never replace them and no bound, window or list is widened automatically (§3.7).
17. No human reads main-run response content for any decision; only automated structural diagnosis is permitted and it can affect only the acceptance of a pure implementation fix (§13.6.1).

---

## Appendix A — Audit issue register (archived short form, I-01 … I-20)

| ID | Issue | Section addressed (v2.3) |
|---|---|---|
| I-01 | Pace valid member had zero deviation (degenerate) | §5.3 (Q6, finish-time analog), §6.1 |
| I-02 | Distance-dependent pace deviation | §3.3, §5 (explicit finish-time arithmetic, levels separated) |
| I-03 | Subjective reporting precision as guard | §6.1 (reading sets, derived `gw_F`) |
| I-04 | Deferred E1–E4 values; undefined plausibility ceiling | §6.2, §5.6, §17 (windows; `X_min/X_max`; pace/time bounds; RC-M5…RC-M7) |
| I-05 | Vague reproducibility | §10 |
| I-06 | Mileage valid-side flat-token artifact | §4 (M9, `W_V` > 0) |
| I-07 | Profile confounding | §7 |
| I-08 | Balance and number of templates (called "T" in the audit) | §9 |
| I-09 | Matched-pair equivalence | §8 |
| I-10 | Ground-truth independence overstated | §11 |
| I-11 | Sample-size formula misused | §12 |
| I-12 | Pilot leakage | §13 |
| I-13 | Reviewer claim bundle | §15 |
| I-14 | Primary RQ wording | §18 |
| I-15 | S2/S3 coding | §16 |
| I-16 | Frozen methodological text | §14 |
| I-17 | Fixed pace distance | §5.1, §5.3 |
| I-18 | Normalization comparability | §3.5 |
| I-19 | Researcher availability fallback | §11, §16.3 |
| I-20 | Recursive mileage construction | §4 |

## Appendix B — Audit dispositions

### B1. Final audit #1 (v2.0 → v2.1)

| # | Finding | Disposition | Section (v2.3) |
|---|---|---|---|
| R1 | Pace ground truth lost distance / target time / implied finish time | Rebuilt per project-owner decision | §3.3, §5, §6.1 |
| R2 | Duplicated valid plans | Eliminated (A1); assignment redesigned again in v2.2 (see B2 R-1) | §2.2, §9 |
| R3 | Guard coverage claim wrong for truncation | Reading sets, propositions GM/GP, coverage classification | §6.1 |
| R4 | Realizability conditions incomplete | RC-M5…RC-M7, RC-P6, `Xprev_max`, admissibility definition | §3.7, §4, §5.5 |
| R5 | Pilot rules incomplete | 2-round cap, SF/UNP definitions, stop rules (extended in v2.2) | §13 |
| R6 | Member IDs leak the label; adjudication; A/B authorship | Opaque IDs, X10/X11, ADJ-1/ADJ-2 (made mechanical in v2.2) | §8, §11 |
| R7 | S3 precedence inconsistency, no A/B handling, no denominators | Redefined (refined in v2.2) | §16 |
| R8 | Primary estimand ambiguity | Separate A–D reporting, definitions, sensitivity | §18 |
| R9 | Sample-size procedure gaps | Decision procedure (made cluster-aware in v2.2) | §12 |
| R10 | Under-specified parameters | Classified; progressions; thresholds | §17 |
| R11 | Missing threats | Added (extended in v2.2) | §20 |
| R12 | Rule semantics not frozen | Frozen | §3.2, §3.3 |

### B2. Focused delta audit (v2.1 → v2.2)

| # | Finding (severity) | Disposition | Section |
|---|---|---|---|
| R-1 | `PAC` class independent of position; class confounded with base parity × direction (blocking) | New window-based rule with exact margins on every axis, `K` even ≥ 4 invariant, non-parity test, symbolic examples, aliasing disclosed | §9.1–§9.4, §9.6 (A2, A6), §20 TH4, §22 |
| R-2 | Planning equations treated templates as independent while declaring base clustering (blocking) | Unit definitions; Option A cluster-aware planning and cluster bootstrap; counts restated | §2.2–2.3, §9.5, §12, §18 |
| R-3 | No pace/time plausibility bounds (blocking) | Q11, bounds `G_min…Tm_max`, `𝒢_adm`, direction-specific feasibility, interaction with `τ_F` and the `G` progression | §5.4–§5.6, §9.6, §17 |
| R-4 | X10 not mechanically defined | Exact regex set, normalization, boundaries, controls, behavior | §8.1 |
| R-5 | Former R2(a)/(b) adjudication was judgment-based | Ordered objective procedure on worksheets and strict parse | §11.2 |
| R-6 | Pilot / freeze path gaps | FAIL-S / FAIL-U, STOP-U, whitelist by failure type, pure-implementation-fix rule H1–H4, return paths | §13.6, §21.2 |
| R-7 | S2/S3 definitions vague; S3 conflated own assessment with reviewer stance | "Relevant values", IV/EV, `s3_ref` × `s3_stance`, derived categories, denominators | §16 |
| R-8 | Notation collisions | Glossary and renaming | §0.1 and throughout |
| R-9 | Missing design-specific threats | Threat table with affected validity types | §20 |
| R-10 | `τ_F` interval must contain an integer; `G` progression vs minute band | Hard gates A4 and A3 (exact `Q*` gates) with screening aids (integer interval, `𝒢_adm`); refined in v2.3 (B3 F1) | §5.5, §5.6, §9.6 |

### B3. Fresh focused delta audit (v2.2 → v2.3)

| # | Finding (label) | Disposition | Section |
|---|---|---|---|
| F1 | Sufficient conditions used as hard gates; contradiction with §3.7 (REQUIRED) | Hard gates versus screening aids defined; A3, A4, A5 redefined as exact/necessary gates; `𝒢_adm`, `[τ_lo, τ_hi)`, RC-P8 are screening aids; no automatic widening | §3.7, §5.5, §5.6, §9.6, §17, §21 |
| F2 | IV/EV overlap; bare assertion counted as explicit verification (REQUIRED) | EV requires a numerical comparison stating observed and rule values; precedence NC → EV → IV → NV | §16.1 |
| F3 | Worksheet precision, normalization and checklist unspecified (REQUIRED) | Checklist, normalization, precision floor (with proof sketch and scratch check), precision test as step 4 | §11.2 |
| F4 | Effective cluster count overstated for tight lists (REQUIRED) | Caveat; bounds labelled optimistic w.r.t. base similarity; PJR must report spacing; no effective sample size invented | §2.3, §12.1, §17, §20 TH5 |
| F5 | Interaction-aliasing magnitude undisclosed (REQUIRED) | Measured values with tested conditions; explicit non-orthogonality statement; labelled finite, one contrast | §9.3, §12.3, §20 TH4 |
| F6 | Annotation / emphasis leakage not covered (REQUIRED) | Plan-block whitelist X12, pattern F10, annotation controls, exact rejection behavior | §8.1, §8.3 |
| F7 | H3 versus §13.8–13.9 on reading stored main-run records (REQUIRED) | Automated structural diagnosis versus semantic inspection; reference grammar checker; main-run semantic inspection prohibited | §13.6, §13.6.1, §13.8, §13.9 |
| C1 | Notation collisions (CLARIFICATION) | Explicit names throughout; glossary extended | §0.1 and throughout |
| C2 | DP6 descent not algorithmic (CLARIFICATION) | Integer path algorithm, no continuous parameter | §12.2 DP6 |
| C3 | §17 versus §19 status inconsistency (CLARIFICATION) | Fixed decisions separated from owner-decision placeholders OD-1 … OD-7 | §19, §17 F1 |
| C4 | Reviewer-reference trigger `comment`; UNP denominator selection (CLARIFICATION) | Exact phrase list without bare `comment`; disclosure and reporting rule | §16 |
| C5 | Seed-date discretion (CLARIFICATION) | Script-stamped timestamp, decision record, first-run rule | §10, DP9, §17, §21 |
| C6 | Halt after the change window closed (CLARIFICATION) | Terminated as incomplete; no repair, rerun or replacement | §13.8 |
| C7 | Bootstrap position imbalance in the class contrast (CLARIFICATION) | Interpretation paragraph; no conservativeness claim | §12.3 |

## Appendix C — Scratch verification log (not retained in the repository)

Offline checks run outside the repository with arbitrary sweep values (none is a proposed parameter; no model or API call).
- **Proposition GP (v2.1 work, still valid):** 115,014 guarded cases, six rounding rules × two boundary readings, 0 flips; unguarded band flips on both sides. Re-test rounding `F` itself (not `x`): 53,021 guarded cases, 0 flips, 487 unguarded-band flips; half-even does not commute with odd integer shifts of `T_time` (2,032 cases) — Proposition GP is unaffected because it only uses the `[⌊x⌋, ⌈x⌉]` bracket.
- **Percent-rounding coverage:** nearest 0 flips for `B ≤ 1999` tenths (106 at 2000–2100); floor / ceil 0 flips for `B ≤ 1000` (60 / 58 in 1001–1100).
- **`MIL` realizability (independent sweep):** with RC-M1…RC-M7, 1,270 parameter sets / 48,786 templates, 0 gate failures; 855 sets violating a condition but fine (conditions sufficient, not necessary); 4,307 sets violating a condition failed on M7 or M8.
- **`PAC` realizability (independent sweep):** 138 tolerance values inside the feasible interval, 11,040 templates, 0 failures; interval `(205.1, 205.9)` contains no integer.
- **Class-assignment rule (v2.2):** enumeration over `K ∈ {4,6,8,10,12}`, `L ∈ {2,4,6,8,10,12,14,16,20,30}`, one and two directions: exact base × direction × class, slot × class, position × class, direction × class; class varies across positions for every (base, direction); no base or direction permanently one class; direction agrees and disagrees with itself across bases; **no parity-XOR function reproduces any table**. The v2.1 rule: class never varies with position. The naive fix `(b + i + s) mod 2` is a parity-XOR rule.
- **Registry under the v2.2 rule:** 36 `MIL` (`K = 6`) and 96 `PAC` (`K = 6`) templates; 36/36 and 96/96 distinct valid plans; 264/264 distinct prompts; equal counts for every (position, [direction], class), (base, class) and (base, direction, class); `Cond-A`/`Cond-C` and `Cond-B`/`Cond-D` equivalent; one differing token per matched pair; correct class windows; every base touches every primary cell.
- **Cluster vs template bootstrap (600 runs, 12 clusters × 10 templates, strong base effects, target = population mean):** coverage of nominal 95%: cluster 0.93, template 0.75. Balanced design ⇒ mean of cluster means = pooled template mean.
- **X10:** 19 natural-language/format negatives pass, 23 machine-label positives caught.
- **Plausibility / progression:** eligible-`G` set for arbitrary bounds: 48 values; 1,152 templates from all eligible `G` passed every check; 9 progressions screened against `𝒢_adm`: 4 pass the screen, 5 fail it (screening decisions, not the hard gate A3).
- **Adjudication classifier:** six synthetic worksheets classified as specified.
- **Call count:** `8·K·R·(n_M + 2·n_P)` equals enumeration.
- **v2.3 additions (scratch, outside the repository):** plan-block whitelist X12: compliant `MIL` and `PAC` blocks pass; 16 non-whitelisted `MIL` rows, 8 non-whitelisted `PAC` rows, a modified header and a week-number gap all rejected; F10: 7 of 7 emphasis/footnote positives flagged, 0 of 7 negatives. Worksheet precision floor: 5,383 guarded `MIL` cases and 45,145 guarded `PAC` cases, 0 verdict flips; whole-percent worksheets flip 172 guarded `MIL` verdicts. Adjudication classifier (with normalization and precision step) on eight synthetic worksheets as specified. DP6 algorithm: 3,000 random inputs, 0 violations of the stated properties. Interaction aliasing (finite, one contrast, arbitrary configurations): table in §9.3.
