# Scenario Construction Specification — v2.6 CANDIDATE (DRAFT, working document, post-v2.5-audit revision 6: operational and cross-reference corrections only; every unresolved researcher decision is marked PENDING in §19.3)

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
| 8 | Fresh focused delta audit of v2.2 | `READY WITH MINOR CLARIFICATIONS` (0 blocking; 7 required findings Aud22-F1 … Aud22-F7; 7 clarifications Aud22-C1 … Aud22-C7) | Disposition: Appendix B3. |
| 9 | v2.3 draft | Superseded; **retained unchanged** as the audited artifact | `research_design/SCENARIO_CONSTRUCTION_SPECIFICATION_v2_DRAFT.md`, SHA-256 `61bf398d59bad3c3d729cdc8e3f5217ee7162a47023bdc30a12fb752fe487196`, 1,189 lines, 146,462 bytes. Do not edit or rename. |
| 10 | Fresh focused delta audit of v2.3 | `READY WITH MINOR CLARIFICATIONS` (0 blocking; required findings Aud23-N1 … Aud23-N8 and clarifications Aud23-C1 … Aud23-C7 of that audit) | Disposition: Appendix B4. Finding IDs of that audit are written `A23-N#` and `A23-C#`; those of the audit of v2.2 are written `A22-F#` and `A22-C#`. |
| 11 | v2.4 draft | Superseded; **retained unchanged** | `research_design/SCENARIO_CONSTRUCTION_SPECIFICATION_v2_4_DRAFT.md`, SHA-256 `17af97e1c1282254be697314ecdae0ae5158f9124632bdfae4e09a269b6523e2`, 1,282 lines, 173,441 bytes. Do not edit or rename. It described itself as "textual and logic clarifications only"; that description was **incorrect** for its admissibility change (see row 13). |
| 12 | Fresh audit of v2.4 (one model session; **not** independent human review) and local evidence verification | `REQUIRES METHODOLOGICAL REVISION`: blocking `Aud24-B1 … B3`, non-blocking `Aud24-NR1 … NR10` | Disposition: Appendix B5. Both were read-only. |
| 13 | v2.5 draft | Superseded; **retained unchanged** | `research_design/SCENARIO_CONSTRUCTION_SPECIFICATION_v2_5_DRAFT.md`, SHA-256 `da9cacf8fb32cc158c4aa52b34cbea7a6760ae3332ddc836f43103fa68bc6aa5`, 1,333 lines, 198,826 bytes. Do not edit or rename. Contains the researcher decisions B1 (only the window-ordering clause `mi_hi < c_lo` of the v2.3 chain restored) and NR7, plus technical corrections. |
| 14 | Read-only delta audit of v2.5, performed by the same model session that wrote v2.5 (therefore **not independent**; independent human review has not occurred) | `READY WITH SPECIFICATION FIXES`: eight required fixes (`Aud25-R1 … R8`), six researcher decisions, observations | Disposition: Appendix B6. |
| 15 | **v2.6 candidate (this file)** | Working draft (`SCENARIO_CONSTRUCTION_SPECIFICATION_v2_6_DRAFT.md`) | Operational and cross-reference corrections only. **No new methodological decision.** Every unresolved researcher decision is marked `PENDING RESEARCHER DECISION` (§19.3). OD-1 … OD-7 remain open. Not a parameter selection. |
| 16 | Delta audit of v2.6 | Pending (independent human review has not occurred) | |
| 17 | Methodology freeze, parameter selection, registry … main run | Pending; owner decisions OD-1 … OD-7 (§19.2) and the pending decisions PRD-1 … PRD-10 (§19.3) open | Order is binding: §21. |

Verbatim copies of v2.0, v2.1 and v2.2 exist only in the session scratch directory outside the repository; v2.3, v2.4 and v2.5 are retained in the repository (rows 9, 11 and 13), but the `research_design/` directory is not yet tracked by Git, so their immutability rests on the recorded SHA-256 values only. Archiving the earlier versions is open decision OD-7 (§19.2).

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
| `sec_G`; `gw_fam` | `sec_G = G mod 60`; `gw_fam` = guard width of family `fam` (§6.1). |
| `bnd⁻`, `bnd⁺` | the regex boundary assertions of §8.1. |
| `n_boot` | number of bootstrap replicates (§12). |
| `DP1 … DP9` | steps of the sample-size decision procedure (§12.2). |
| `RC-M1 … RC-M7`, `RC-P1 … RC-P8` | design-level realizability conditions (§4, §5.5): **screening aids only**; none rejects a build (§3.7). Register well-formedness is the separate hard gate `A5`. |
| `M*`, `Q*`, `PG*`, `A*` | **hard gates**: construction (`M`), pace (`Q`), presentation / pair / leakage (`PG`) and registry-level (`A`); each belongs to the **numeric stage** or the **rendering stage** (§3.7). |
| `FZ` | the **freeze set** (§13.2). |
| `FX1` | the row of fixed design rules in the parameter register (§17). |
| `PT1 … PT10` | the forbidden-pattern scan patterns (§8.1). |
| `Aud22-F#`, `Aud22-C#`, `Aud23-N#`, `Aud23-C#`, `Aud24-B#`, `Aud24-NR#`, `Aud25-R#` | finding IDs of the audits of v2.2, v2.3, v2.4 and v2.5 (Appendix B3–B6). The prefix `Aud` keeps them distinct from the gates `A2`, `A3`. |
| `PRD-#`, `PC-#` | `PRD-#`: pending researcher decisions; `PC-#`: pending specification clarifications (§19.3). Neither is an owner decision `OD-#`. |
| `R-#`, `R#`, `I-##` | audit-finding IDs in Appendices A and B only; always hyphenated or numbered, never the repetition count `R`. |
| `w` | week index `1 … N` (`p_w`, `x_w`, `e_w`, `X_w`, `ρ_w`, `u_w`). Distinct from the 0-based target-position index `i`. |
| `q` | the violation-margin class of a template, `q ∈ {MILD, CLEAR}` (`Δ_q`, `m_q`, `W_q`). Used for nothing else. |
| `n_dec` | number of decimals of the canonical rendering of `D_dist` (§8.3 item 4). |
| `h_b` | cluster-level proportion of cluster `b` in a reporting cell (§12). |
| `n_calls` | number of calls in a reporting cell (§18.2). Not to be confused with `n_cells`, the number of reported cells (DP2). |
| `n_cells` | number of reported cells (DP2, TH13). |
| `p_t(c)`; `t_MILD(cpl,i,s)`, `t_CLEAR(cpl,i,s)`; `cc(cpl,s,c)` | `p_t(c)`: proportion of matching verdicts of template `t` in condition `c` (§12); `t_MILD`, `t_CLEAR`: the templates of the MILD and of the CLEAR base of couple `cpl` at slot `(i,s)`; `cc`: the within-couple slot contrast of §2.3 (not an estimand). |
| `ω_min` | width of the narrowest margin window (§5.5). |
| `a(b,s)`; `𝟙_half(·)` | class-window start of base `b`, direction `s` (§9.2); the half-cycle indicator of §9.3. |
| `t_3`, `t_4`, `pct` | placeholders in the synthetic S2 examples of §16.1 only (week-3 and week-4 totals; a derived percentage). |
| `E-EMPTY-TARGET` | the error of §12.2 DP4 (empty precision-target set). |
| `ADJ-1`, `ADJ-2` | ground-truth disagreement procedures (§11). |
| `OD-1 … OD-7` | open owner decisions (§19.2). |
| `TH1 … TH18` | threats to validity (§20). |
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

The claim block always asserts that the plan violates the stated constraint. `Cond-C vs Cond-A` and `Cond-D vs Cond-B` are **claim contrasts**: prompts byte-identical except for the frozen claim block (gates PG7, PG8).

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
- **Effective number of independent clusters (Aud22-F4).** `L` counts bases, not independent observations. When the base list contains closely spaced or highly similar values (for example an arithmetic progression whose step is small relative to the base value), neighbouring bases give nearly identical templates and model behaviour on them may be strongly correlated. The **effective number of independent clusters may then be substantially lower than `L`.** No effective sample size is computed here: no defensible model of between-base correlation exists before data are observed, and none may be estimated from pilot behavior. Consequences: the planning bounds of §12.1 are **optimistic with respect to base similarity** (they assume independent clusters), and the Parameter Justification Record must report the actual base-list spacing and discuss its implications (§17).
- **Couples (adjacent complementary bases; Aud23-C1).** The bases `2·cpl` and `2·cpl+1` are neighbouring values with complementary class windows (§9.2): at every slot exactly one is MILD and the other CLEAR. A couple therefore behaves as a **quasi-matched unit** for the **within-couple slot contrast** `cc(cpl, s, c) = (1/K)·Σ_i [ p_{t_MILD(cpl,i,s)}(c) − p_{t_CLEAR(cpl,i,s)}(c) ]` for a condition `c`, where `t_MILD(cpl,i,s)` and `t_CLEAR(cpl,i,s)` are the templates of the MILD and of the CLEAR base of couple `cpl` at slot `(i,s)` and `p_t(c)` is the template-level proportion of §12: if neighbouring base values produce similar behaviour, much of the base-to-base variation would cancel in `cc`. `cc` is **not** the class contrast of §12 and §18 (`ctr_b = h_b(MILD) − h_b(CLEAR)` is a within-base contrast that confounds class with position, §9.3(a)); it is defined here only so that the argument has a referent, and it is **not an estimand** of this specification unless later declared under DP1 (OD-4). The cluster bootstrap of §12 nevertheless resamples **single bases independently** and does not preserve couples. This dependence is **disclosed, not resolved**: resampling couples would be a different method that is not adopted here, and no claim is made about whether the independent-base bootstrap is wider or narrower than a couple-preserving one (§12.3, TH5).
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
2. Every later week `w ≥ 2` is compared only with the **immediately preceding displayed week** `w−1`.
3. A **decrease** or no change satisfies the rule.
4. An increase **equal to the cap** satisfies the rule.
5. Only `increase > cap` is a violation, i.e. week `w` violates iff `100·(X_w − X_{w−1}) > P·X_{w−1}`.
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

- `MIL`: `ρ_w = (X_{w+1} − X_w) / u_w` with `u_w = P·X_w/100` (allowed increase, tenths of km).
- `PAC`: `ρ_w = |x_w| / τ_F` — computed on the **exact** finish-time deviation, not on the rounded `e_w` and not on `d_w`.
- Plan-level `ρ_plan` = maximum over transitions / weeks. Violating iff `ρ_plan > 1`.

### 3.5 ρ comparability (I-18)

ρ values are comparable mathematically within one family's construction. **Equal ρ across `MIL` and `PAC` does not imply equal substantive difficulty.** Margin classes are a within-family manipulation; no primary analysis compares classes across families.

### 3.6 Reject-not-repair

A gate failure rejects the **whole registry build** (all-or-nothing, to preserve balance). Nothing is nudged, retried with different logic, or regenerated from an unspecified stream. A failed build is logged (parameter set, failing gate, template) and handled by the return paths of §21.2. Feasibility checks use no model output.

### 3.7 Admissibility, hard gates and gate stages

> An **admissible parameter set** is a parameter set under which the **full registry build** (step 8) passes **every hard gate** (`M*`, `Q*`, `PG*`, `A*`) for **every** template. A set that passes every **numeric-stage** gate at step 4 is *numerically admissible*; it is *admissible* only after the rendering-stage gates have also passed.

Two kinds of rule are never mixed:

- **Hard gates** are exact, deterministic tests on the actual registry build. They alone decide admissibility.
- **Screening aids** are design-level conditions used to choose or pre-screen parameters: every `RC-M*` and `RC-P*` condition **except the window-ordering clause `mi_hi < c_lo`**, the integer interval `[τ_lo, τ_hi)` and the eligible-pace set `𝒢_adm` (§5.5–5.6). **No screening aid rejects a build.** A set that satisfies them is not thereby admissible, and a set that violates one is not thereby inadmissible: it is admissible iff it passes all hard gates.
- The only parts of the design-level conditions that are hard gates are **register well-formedness and sizing-input domains** (`A5(a)`, `A5(b)`) and the **MILD/CLEAR window ordering `mi_hi < c_lo`** (`A5(c)`). The window ordering is a **researcher-directed hard admissibility rule** (v2.5, B1): the MILD window lies strictly below the CLEAR window, so touching or overlapping MILD/CLEAR windows are inadmissible. v2.4 had removed every window-ordering check from the hard gates and thereby enlarged the admissible design space without approval. v2.5 and v2.6 restore **only the clause `mi_hi < c_lo`** of the v2.3 `A5`, which enforced the whole chain `0 < ρ_NT < v_lo ≤ v_hi < 1 < mi_lo ≤ mi_hi < c_lo ≤ c_hi` (RC-M1/RC-P1) and the bounds containment of RC-P7. Not restored as hard rules: `ρ_NT < v_lo`, `v_hi < 1`, `1 < mi_lo`, and `p_min ≤ G_min ≤ G_max ≤ p_max` (`0 < lo ≤ hi` for each window and the representational limits remain in `A5(a)`). The admissible design space is therefore still **larger than under v2.3**: sets with `ρ_NT ≥ v_lo` or `p_min > G_min`, which v2.3 rejected, can be admissible. Whether to restore more of the v2.3 chain is **PENDING RESEARCHER DECISION PRD-1**, the rationale for the strict inequality is **PRD-2**, and the treatment of per-family windows (OD-5) is **PRD-9** (§19.3). The remaining clauses of the former chain (`ρ_NT < v_lo`, `v_hi < 1 < mi_lo`) stay screening aids: they are not necessary (Appendix C counterexample) and the relation of the windows to 1 is decided by the guards M3 and Q4. Every other relation between register values and the construction is decided by the exact gates `M*` and `Q*`.
- **Element-level and registry-level gates.** `M1–M10` and `Q1–Q11` are evaluated per template (and hence per list element). `M11`, `Q12`, `A1`, `A6`, `A7` are evaluated once on the whole build. The progression gate `A3` refers to the element-level gates only (§9.6).
- No bound, window, tolerance or list is ever widened, shifted or repaired automatically in response to a gate or screening failure (§3.6).

**Gate stages (Aud23-N2).** A gate can run only when its inputs exist.

| Stage | Inputs required | Hard gates | Runs at |
|---|---|---|---|
| **Numeric** | register values and the canonical numeral renderers of §3.1 (`%.1f` by integer division, `m:ss`, `H:MM:SS`, the exact decimal rendering of `D_dist`); **no prompt text** | `M1–M11`; `Q1–Q12` (Q8's length test uses canonical numerals only); `A1a`, `A2`, `A3`, `A4`, `A5`, `A6a`, `A7` | step 4 (dry run) and again in step 8; `A5(b)` also at step 3, before DP4 |
| **Rendering** | the frozen prompt specification (step 7), the rendered prompts and the opaque-ID bundle builders (code; freeze status **PENDING RESEARCHER DECISION PRD-10**) | `PG1–PG10`; `PG11a`; `PG11b` (builder test on the synthetic battery only); `PG12`; `A1b`; `A6b` | step 8; `PG1–PG10`, `PG11a`, `PG12`, `A1b`, `A6b` independently re-verified by Implementation B in step 9 |
| **Post-run materials** | the coder bundle built from stored responses after the main run is complete or declared incomplete and the primary scoring is computed and hashed | `PG11b` (application to the real coder bundle) | after the main run, **before any S2/S3 coding begins** (§13.6.1, activity C); not a precondition of the pilot or the main run |

The return path of a failure depends on the step and on which implementations can have run (§21.2): at step 4 only Implementation A exists. A rendering-stage failure can occur only after the parameter freeze and is handled by the return paths of §21.2. **No pilot and no main run starts before every rendering-stage gate (including `PG11a` and the `PG11b` builder test) has passed on the final registry.** The application of `PG11b` to the real coder materials cannot run earlier because those materials do not exist; it is a post-run condition of S2/S3 coding only. Gate counts: 30 numeric-stage gates; 14 rendering-stage gate identifiers (`PG1–PG12`, where `PG11` comprises `PG11a` and `PG11b`, plus `A1b`, `A6b`).

| Gate family | Where defined |
|---|---|
| `M1–M11` | §4 (mileage construction) |
| `Q1–Q12` | §5.4 (pace construction, including plausibility `Q11` and class separation `Q12`) |
| `PG1–PG12` | §8 (matched-pair equivalence, cross-condition, leakage, opaque-ID materials `PG11a`/`PG11b`, plan-block whitelist) |
| `A1–A7` | §8.2, §9.6 (registry-level: distinctness, `K`, progressions, `τ_F`, register well-formedness, class assignment, cluster integrity) |

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
| M11 | Registry-level class separation (**implied assertion**): `max` over MILD templates of target ρ `<` `min` over CLEAR templates. Given the hard window ordering `mi_hi < c_lo` (A5(c)) and window membership (M2) this holds for every build (`max ρ_MILD ≤ mi_hi < c_lo ≤ min ρ_CLEAR`); it is retained as an implementation consistency assertion and is **not a substitute** for A5(c). |

**Design-level realizability conditions** (shared windows; `MIL`). All rows are **screening aids** (§3.7) except the window-ordering clause of RC-M1, which is the hard rule A5(c): no screening aid rejects a build; the exact gates `M1–M11` decide. The only hard gate on register values is `A5` (well-formedness, sizing-input domains, window ordering).

| ID | Condition | Status |
|---|---|---|
| RC-M1 | `0 < ρ_NT < v_lo ≤ v_hi < 1 < mi_lo ≤ mi_hi < c_lo ≤ c_hi` | the clause `mi_hi < c_lo` is the **hard rule A5(c)**; the rest is a screening aid — sufficient for M5 and M11 and **not necessary**: with `ρ_NT = 0.50 > v_lo = 0.40` the exact gates M2–M5 and M7–M9 (those implemented in the check) passed for 8 of 10 start values tested (Appendix C). Window well-formedness (`0 < lo ≤ hi`) is enforced by `A5(a)`; the relation of the windows to 1 is enforced by M3. |
| RC-M2 | Reach: `(hi − lo)·U_M ≥ 1` for each window (exact: `⌈lo·u⌉ ≤ ⌊hi·u⌋` per base) | sufficient for M1, M2 |
| RC-M3 | Guard: `v_hi ≤ 1 − 1/U_M` and `mi_lo ≥ 1 + 1/U_M` | sufficient for M3, M4 (with RC-M4) |
| RC-M4 | `ρ_NT·U_M ≥ 1` | sufficient for M4, M5 (with RC-M1) |
| RC-M5 | **Single digit-width band:** `⌊X_min/10⌋` and `⌊X_max/10⌋` have the same number of decimal digits | sufficient for M7 |
| RC-M6 | **Tail floor:** `X_min ≥ 1/γ` and `S_min·(1 − γ)^{N−2} ≥ X_min` | sufficient for the tail part of M8 |
| RC-M7 | **Peak and ramp bounds:** `Xprev_max·(1 + c_hi·P/100) ≤ X_max` and `S_min ≥ X_min` | sufficient for the rest of M8 |

*Proof of RC-M6.* For `X ≥ 1/γ`, `γX ≥ 1` so `DNT(X) = ⌊γX⌋ ≤ γX` and the next tail value is `≥ (1−γ)X`. The tail has at most `N−2` steps (`k ≥ 2`) and starts at `X_k^{valid} ≥ S_min`; after `j ≤ N−2` steps the value is `≥ S_min(1−γ)^j ≥ S_min(1−γ)^{N−2} ≥ X_min ≥ 1/γ`, so the hypothesis holds at every step. ∎ RC-M7 holds because the largest token is the violating peak at `Xprev_max` and `X_k^{viol} ≤ X_prev·(1 + c_hi·P/100)` by M2.

*Scratch verification (Appendix C):* with RC-M1…RC-M7 holding, 1,270 parameter sets (48,786 templates) passed M1–M10; 855 sets violating a condition were nevertheless fine (the conditions are **sufficient, not necessary**); 4,307 sets violating a condition failed on M7 or M8.

**Valid-side non-zero margin (I-06).** `W_V` has `0 < v_lo` (A5(a)) and the valid increase is `Δ_V ≥ 1` (M1) below the cap (M3), so the valid target is a real increase; in every admissible build it is also the plan's strict maximum transition (M5). (If `ρ_NT < v_lo`, the screening condition RC-M1, this follows from the windows alone; it is not required.)

**Recursion property (I-20) — proved.** Let `X'` equal `X` except `X'_k > X_k`. (a) Only transition `(k−1→k)` changes to a larger increase, so it is the only transition that can become newly violating. (b) Transition `(k→k+1)` is non-violating in `X` (`X_{k+1} ≤ (1+P/100)X_k`) and `X'_k > X_k`, so `X_{k+1} ≤ (1+P/100)X'_k`: it cannot become violating. (c) All other transitions are untouched. (d) Downstream tokens are copied, not recomputed, so they are identical in both members. In this construction `k→k+1` is additionally a decrease.

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
| Clear farther outside | `ρ ∈ W_CLEAR` (Q3) and the hard window ordering `mi_hi < c_lo` (A5(c)); across the registry the clear class therefore lies above the mild class, which gate Q12 asserts on the realised values. |
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
| **Q12** | **Registry-level class separation (implied assertion; pace analogue of M11):** the maximum target `ρ` over MILD templates is smaller than the minimum target `ρ` over CLEAR templates. Given the hard window ordering `mi_hi < c_lo` (A5(c)) and window membership (Q3) this holds for every build; it is retained as an implementation consistency assertion and is **not a substitute** for A5(c). It is logically compatible with the restored rule and rejects nothing that A5(c) with Q3 admits. |

### 5.5 Design-level realizability conditions

All rows are **screening aids** and never decide admissibility (§3.7), except the window-ordering clause of RC-P1, which is the hard rule A5(c); the exact gates `Q1–Q12` decide, and `A5` enforces well-formedness, sizing-input domains and the window ordering only.

| ID | Condition | Status |
|---|---|---|
| RC-P1 | `0 < ρ_NT < v_lo ≤ v_hi < 1 < mi_lo ≤ mi_hi < c_lo ≤ c_hi` | the clause `mi_hi < c_lo` is the **hard rule A5(c)**; the rest is a screening aid — sufficient for Q5 and Q12 and **not necessary** (the argument and counterexample of RC-M1 carry over; Q3, Q4, Q5 decide). Window well-formedness is enforced by `A5(a)`. |
| RC-P2 | Reach: `(hi − lo)·τ_F ≥ D_dist` for each window (exact: ∃ integer `m ≥ 1` with `lo·τ_F ≤ D_dist·m − σ·r ≤ hi·τ_F`) | sufficient for Q3 |
| RC-P3 | Guard: `v_hi ≤ 1 − 1/τ_F` and `mi_lo ≥ 1 + 1/τ_F` | sufficient for Q4 (with RC-P4) |
| RC-P4 | `ρ_NT·τ_F ≥ D_dist + 1/2` (⇔ `m_NT ≥ 1`) | sufficient for Q2, Q4 (non-target), Q5 |
| RC-P5 | Nonzero: `D_dist ≥ 3/2` and `v_lo·τ_F ≥ 1` (then `|x| ≥ D_dist·|d| − 1/2 ≥ 1` for any nonzero `d`) | sufficient for Q6 |
| RC-P6 | **Upper bound on `τ_F` from the same-minute representation:** `(c_hi·τ_F + 1/2)/D_dist < 30`, i.e. **`τ_F < (30·D_dist − 1/2)/c_hi`** | sufficient for the existence of eligible `G` |
| RC-P7 | Bounds containment: `p_min ≤ G_min ≤ G_max ≤ p_max` | screening aid — **not necessary**: a set with `p_min = 300 > G_min = 290` passed the exact gates Q3–Q7, Q10 and Q11 (those implemented in the check) for 30 of 70 reference paces tested (Appendix C), because the exact gate Q11 constrains the actual tokens and the actual `G`. The truly necessary clauses (`60 ≤ p_min ≤ p_max ≤ 599`, `G_min ≤ G_max`, `0 < Tm_min ≤ Tm_max < 36000`) are well-formedness and are enforced by `A5`. |
| RC-P8 | Screened-eligible set non-empty: `𝒢_adm ≠ ∅` (definition in §5.6) | screening aid (sufficient set; its emptiness does not by itself make a parameter set inadmissible) |

*Why RC-P6 and the symmetric band.* The clear-class step (`m_q` with `q` = CLEAR) satisfies `m_q ≤ (c_hi·τ_F + 1/2)/D_dist`. Each reference pace is used with **both** directions (§9), so it must leave room for deviations of either sign: `sec_G ≥ m*` and `sec_G ≤ 59 − m*`, non-empty only if `m* ≤ 29`, i.e. `(c_hi·τ_F + 1/2)/D_dist < 30`. The exact per-template condition (Q7) is one-sided and weaker. The symmetric form is therefore a **screening aid** (sufficient, possibly conservative), not a hard gate: a reference pace outside the symmetric band is still admissible iff Q7 and the other `Q*` gates pass for every template that uses it.

**Integer feasibility of `τ_F` (hard gate A4; screening interval).** `τ_F` is a positive **integer** (hard gate A4, together with the exact gates Q2–Q6). For screening, let
`τ_lo = max( D_dist/ω_min, 1/(1 − v_hi), 1/(mi_lo − 1), (D_dist + 1/2)/ρ_NT, 1/v_lo )`, `τ_hi = (30·D_dist − 1/2)/c_hi`
(`ω_min` = narrowest window width). A term is undefined if its divisor is not positive (`ω_min = 0` for a point window, `v_hi ≥ 1`, `mi_lo ≤ 1`): the screening interval is then reported as *undefined*, which is a warning and not a rejection; the exact gates (M3, Q4, Q3) decide. An integer `τ_F` with `τ_lo ≤ τ_F < τ_hi` is *sufficient* for the screened conditions RC-P2…RC-P6. A mathematically non-empty real interval is **not enough** for an integer-valued parameter: the set `{τ ∈ ℤ : τ_lo ≤ τ < τ_hi}` must be non-empty for the screen to be satisfied (counter-example: the real interval `(205.1, 205.9)` contains no integer). A `τ_F` outside the screening interval is not rejected by screening alone: it is admissible iff the exact gates pass; if any exact gate fails the parameter set is **inadmissible** (reject-not-repair; no widening of any window or bound).

**Integer vs non-integer `D_dist`.** For integer `D_dist`: `r = 0`, `F_w` is an integer, `rnd*` acts as the identity, `x_w = D_dist·d_w`, and the lattice step is `D_dist`. For non-integer `D_dist` a genuine rounding stage exists (`r ≠ 0`); this is the case the guard of §6.1 is built for. Both are permitted; the register fixes one `D_dist`.

### 5.6 Plausibility bounds (construction gates, R-3)

Plausibility bounds are **construction gates**, not physiological truth. They exist only to prevent obviously artificial or arbitrary scenario values. They are **researcher-choice parameters** (§17) that must be frozen **before** registry generation; this document supplies no numerical value.

| Bound | Meaning | Class |
|---|---|---|
| `G_min, G_max` | plausible range of the hidden reference pace `G` (s/km) | researcher choice |
| `p_min, p_max` | plausible range of every **displayed** weekly pace token (s/km), both members | researcher choice; containing `[G_min, G_max]` is advisable (screening aid RC-P7) and not required |
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

**General rule (symbolic).** For each family fix a *reading set* ℛ_fam: every way the exact comparison quantity may legitimately be rounded or bounded before it is compared. Let `gw_fam` be the width of the largest rounding step that any reading in ℛ_fam can apply. A scenario is **guard-safe** iff the exact quantity lies at least `gw_fam` on the correct side of the threshold: valid: `threshold − |quantity| ≥ gw_fam`; violating: `|quantity| − threshold ≥ gw_fam`. `gw_fam` is derived per family, not assumed.

| Family | Exact comparison quantity (threshold) | Reading set ℛ_fam | `gw_fam` |
|---|---|---|---|
| `MIL` | increase `Δ = X_k − X_{k−1}` in tenths of km (exact threshold `u`) | threshold `u` rounded to the 0.1-km grid by floor / ceiling / nearest; inclusive or exclusive comparison | **1 tenth of km** |
| `PAC` | exact finish-time deviation `x = D_dist·p − T_time` in seconds (threshold `τ_F`) | exact `F` unrounded, or `F` rounded to whole seconds by floor / ceiling / half-up / half-down / half-even; inclusive (`|e| ≤ τ_F`) or exclusive (`|e| < τ_F`) | **1 second of finish time** |

**Proposition GM (mileage).** Let `o` be an integer on the grid, `t` the exact threshold, `rd(t)` its rounding to the grid by floor, ceiling or nearest (`|rd(t) − t| < 1`). If `|o − t| ≥ 1` then `o` vs `rd(t)` gives the exact verdict under both conventions. *Proof.* Violating: `o − t ≥ 1` and `rd(t) < t + 1` give `o − rd(t) > 0`. Valid: `t − o ≥ 1` and `rd(t) > t − 1` give `rd(t) − o > 0`. Equality is never reached. ∎

**Proposition GP (pace, finish time).** Let `x ∈ ℚ` be a week's exact deviation `D_dist·p − T_time` (`T_time` integer) and `τ_F ∈ ℕ`. Every reading in ℛ_P rounds `x` to a value in `[⌊x⌋, ⌈x⌉]`. (i) If `|x| ≤ τ_F − 1`, every reading says *satisfied*. (ii) If `|x| ≥ τ_F + 1`, every reading says *violated*.
*Proof.* (i) For `x ≥ 0`, `⌈x⌉ ≤ τ_F − 1` because `τ_F − 1` is an integer `≥ x`; every reading's value has magnitude `≤ ⌈|x|⌉ ≤ τ_F − 1 < τ_F`, so both conventions say satisfied; `x < 0` is symmetric. (ii) For `x ≥ 0`, `⌊x⌋ ≥ τ_F + 1`; every reading's value has magnitude `≥ ⌊|x|⌋ > τ_F`, so both conventions say violated; `x < 0` symmetric. The unrounded reading compares `|x|` directly. ∎
*Tightness.* One second on each side is necessary: `x = τ_F − 1/2` flips under *ceiling + exclusive*; `x = τ_F + 1/2` flips under *floor + inclusive*. *Corollary.* For integer `D_dist` (integer `x`) any non-zero slack is `≥ 1`: the guard reduces to excluding `|x| = τ_F`.

**Where rounding happens.** Construction: `nearest()` picks lattice points; ground truth is recomputed from the resulting integers, so this step cannot change a class. Rendering: integer-division / zero-padded rendering reproduces the integers exactly (re-verified by Implementation B, §11). Reader: only readings in ℛ_fam are claimed. Mileage state is integer, so no rounding accumulates. For `PAC`: pace is not rounded (integer s/km), `T_time` is integer seconds, `D_dist` is exact; the only rounding of the construction is `rnd*` on `F`.

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
| Any reader behaviour outside ℛ_fam | **NOT COVERED** — counted as model error / reported as a threat (§20) |

Coverage tier is a consequence of the register: with `Xprev_max ≤ 1000` tenths the `MIL` percentage-truncation readings are covered; with `1000 < Xprev_max ≤ 1999` only round-to-nearest; above that none. The Parameter Justification Record states the tier.

**Critical evaluation of the audit proposal (`g = max(s_m, s_p)`, `ρ_v0 = 1 − c_m·g`)** — conditional on reading `s_m, s_p` as smallest display increments in ρ units, because the original definitions are unavailable. (1) A display increment in ρ units is base-dependent (`MIL`: `1/u`) or `1/τ_F` (`PAC`); one scalar cannot serve both, and `max` coarsens the finer family. (2) A point value `1 − c_m·g` need not lie on either lattice. (3) A valid margin tied to the guard drifts in ρ with the base. (4) The shared scalar couples the families without need. Retained: an objective, increment-based guard. Replaced by: family-specific `gw_fam` from an explicit reading set, windows in ρ, per-template gates.

### 6.2 Margin-class windows

Three ρ windows, defined once and shared by both families unless a family cannot realize them (then per-family windows are declared before generation; a recorded degree of freedom):

`W_V = [v_lo, v_hi]`, `W_MILD = [mi_lo, mi_hi]`, `W_CLEAR = [c_lo, c_hi]`. The screening ordering `0 < ρ_NT < v_lo ≤ v_hi < 1 < mi_lo ≤ mi_hi < c_lo ≤ c_hi` (RC-M1, RC-P1) is advisable but not required, **except the clause `mi_hi < c_lo`, which is a hard rule** (`A5(c)`, researcher-directed, v2.5): the MILD window lies strictly below the CLEAR window. Besides this, only `0 < lo ≤ hi` for each window is a hard window check (`A5(a)`). The separation of the classes is decided by `A5(c)` together with window membership (M2, Q3) and the guards (M3, Q4); the registry-level assertions M11 (`MIL`) and Q12 (`PAC`) verify it on the realised values.

Each ρ is evaluated in its own family's exact comparison quantity. Realizability is family-specific (RC-M1…RC-M7, RC-P1…RC-P8). `MIL` lattice resolution in ρ is `1/u`; `PAC` lattice resolution is `D_dist/τ_F`.

**Non-overlap.** Valid and violating members are separated by the guard (M3 in the increase domain, Q4 in the finish-time domain, i.e. by at least `2` display units), mild and clear by the hard window ordering A5(c) with M2/Q3 (verified on the realised values by M11 and Q12); boundary values are excluded by the guard. No class is empty **for any admissible parameter set** (§3.7); for a parameter set that is not admissible the build is rejected, not repaired.

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
| PG1 | Exactly one numeric token differs: `X_k` (`MIL`) or `p_k` (`PAC`). |
| PG2 | Changed tokens have identical **character length** (`MIL`: `%.1f` via integer division, equal integer-digit count (M7); `PAC`: `m:ss`, same minute, differing only in the seconds field). |
| PG3 | Every other character of the prompt is identical: equal length and the set of differing character positions is contiguous and inside the target token's span. |
| PG4 | No derived text depends on the changed token: no sum, average, delta, percentage, implied finish time or commentary is rendered; the claim block names no week and no number. |
| PG5 | No formatting/alignment difference: unpadded markdown cells, one canonical separator row, LF only, ASCII only, no BOM, no trailing newline, no hidden or trailing whitespace; assertions for `\t`, `\r`, U+000B, U+000C, U+001C–U+001E, U+0085, U+2028, U+2029, non-breaking space and zero-width characters (so that no hidden line separator can exist; see §8.3). The plan block is additionally restricted by the row whitelist **PG12** (§8.3). |
| PG6 | The rule text may depend on template parameters (`P`, `D_dist`, `τ_F`) but never on the changed token; it is byte-identical between the members. **Slot rendering (explicit gate, rendering stage):** every numeral slot of the rule text is filled by a canonical renderer: `P` and `τ_F` by `str(n)` (decimal integer, no sign, no leading zero, no padding), `D_dist` by the canonical rendering of §8.3 item 4. Implementation B extracts each slot by the slot markers of the frozen rule text (§14, row "Rule text per family", which fixes the slots) and checks exact string equality with the canonical rendering. This gate, and not PG12, constrains the rule-text numerals. |

**Cross-condition gates:**

| ID | Gate |
|---|---|
| PG7 | `Cond-C` vs `Cond-A`: prompt `Cond-C` with its claim block removed by the frozen insertion procedure is **byte-identical** to prompt `Cond-A`. |
| PG8 | `Cond-D` vs `Cond-B`: prompt `Cond-D` with its claim block removed is **byte-identical** to prompt `Cond-B`. |
| PG9 | The claim block bytes are identical in `Cond-C` and `Cond-D` and across all templates of the family (one hash per family). |

PG7–PG9 are verified by Implementation B on the final strings (not only by the generator that built them), which is what makes them non-tautological.

### 8.1 PG10 — forbidden-pattern scan (mechanical)

The scan targets **internal labels and rendering artifacts**, not semantics and not ordinary language. Bare letters (`A`, `B`, `V`) and common English words (`mild`, `clear`, `valid`, `condition`, `base`, `class`, `none`) are **never** forbidden tokens.

1. **Input.** Each final model prompt as a UTF-8 string (all `4·N_tpl` prompts).
2. **Normalization.** `NFKC`, then `casefold`. Patterns marked CS run on the original string instead.
3. **Boundaries.** `bnd⁻ = (?<![a-z0-9_])`, `bnd⁺ = (?![a-z0-9_])` on normalized text. No tokenizer is used; matching is by regular expression only.
4. **Patterns (fixed order):**

| ID | Pattern | Detects |
|---|---|---|
| PT1 | `bnd⁻(?:mil\|pac)-[0-9]{3,}(?:-(?:v\|mild\|clear))?bnd⁺` | canonical template / member IDs |
| PT2 | `bnd⁻[0-9a-f]{16,}bnd⁺` | opaque IDs and hashes |
| PT3 | `bnd⁻(?:cond\|condition\|arm\|stratum)[_=-][abcd]bnd⁺` | condition identifiers in label form |
| PT4 (CS) | `(?<![A-Za-z0-9_])(?:MILD\|CLEAR\|MIL\|PAC)(?![A-Za-z0-9_])` | all-caps class / family identifiers |
| PT5 | `bnd⁻[a-z]+_(?:id\|class\|cond\|index\|label\|member\|position\|direction\|cluster\|base\|arm)bnd⁺` | snake-case internal field names |
| PT5b | `bnd⁻(?:template\|member\|cluster\|base)_[a-z0-9]+bnd⁺` | internal prefixes |
| PT6 | `bnd⁻(?:cond\|class\|member\|template\|cluster\|pos\|dir\|sigma)\s*=\s*\S` | debug key=value forms |
| PT7 | `bnd⁻target[_-](?:week\|position\|pos\|token\|transition)bnd⁺` | target-position labels (would reveal construction) |
| PT7b | `\((?:target\|valid\|violating\|mild\|clear)\)` | parenthetical annotations |
| PT8 | `bnd⁻(?:valid\|violating)[_-](?:plan\|member\|version\|variant\|arm\|case\|template)bnd⁺` | state labels (machine form) |
| PT8b | `bnd⁻(?:plan\|member\|case)[_-](?:valid\|violating)bnd⁺` | state labels (machine form, reversed) |
| PT9 | `\{\{\|\}\}\|\[\[\|\]\]\|<<\|>>\|%\([a-z_]+\)s\|\{[a-z_]+\}` | unrendered placeholders |

(In the table, `\|` is the markdown escape of the regex alternation `|`; the regular expressions themselves contain the plain `|`.)

PT10 runs after PT1–PT9 on the **original** (non-casefolded) text and detects emphasis or footnote markup touching a numeral anywhere in the prompt:

```
PT10   (?<=[0-9])[*_~`]|[*_~`](?=[0-9])|\[\^[^\]]*\]
```

5. **Allowed exceptions.** None are masked. The required response-format words (`Constraint:`, `Verdict:`, `Comments:`, `satisfied`, `violated`, `unclear`), the reviewer-claim block and the rule text contain none of the patterns by construction; this is **proved at freeze** by an acceptance test: the frozen response-format block, claim block, rule text, task text and plan-table skeleton must scan clean, and a frozen **negative-control battery** (ordinary sentences, the response-format text, the claim-like sentence, table rows, and common words such as "base", "mild", "clear", "valid", "condition", "none") must pass while a frozen **positive-control battery** (machine-label strings such as `MIL-012-V`, `cond_A`, `template_id`, `target_week`, `valid_plan`, `{{plan}}`, a 16-hex string, `(target)`) must fail; the battery additionally contains the annotation-leakage controls of §8.3 (emphasis, footnote and parenthetical markers next to a numeral must fail PT10 or PG12; ordinary sentences containing the words "peak", "week", "target" or "note" must pass PT1–PT10). Scratch check: 19 negatives pass, 23 machine-label positives are caught by PT1–PT9; PT10 flagged 7 of 7 emphasis/footnote positives and 0 of 7 negatives.
6. **Order and behaviour.** Patterns PT1…PT10 run in fixed order on every prompt; any match is a `FAIL` reporting pattern ID and offset; one failure rejects the whole build (§3.6). No human judgment is involved.
7. **Anti-cue word list for the task text.** Separately, the frozen task text must contain none of the words on the anti-cue list declared in the prompt specification (§14). That list applies to the task text only, not to rule, plan or claim.

### 8.2 Registry-level distinctness and human-review leakage

| ID | Gate |
|---|---|
| A1a | **Distinctness of plans (numeric stage):** the valid plans of all templates are pairwise distinct as numeral sequences, the violating plans likewise. |
| A1b | **Distinctness of prompts (rendering stage):** the registry contains exactly `4·N_tpl` pairwise distinct prompts. (`A1` below denotes `A1a` and `A1b` together.) |
| PG10 | The scan of §8.1 passes on every model prompt. |
| PG11a | **Checker materials (rendering stage, step 8).** The human-review bundle for the ground-truth checker is built by the bundle builder from the rendered prompts and the registry hash only (no response exists at this stage). Every file name and identifier matches `^[0-9a-f]{16}$` and no pattern PT1, PT3–PT8b occurs in any file name, file body or directory name. Opaque ID = first 16 hex characters of SHA-256 over the rendered text; the mapping table is held separately and is not shown to the checker; materials are ordered by opaque ID. |
| PG11b | **Coder materials.** Opaque ID = first 16 hex characters of SHA-256 over the canonical call key — the call-list line `<template_id>,<token>,<repetition>` of §10 without its terminating LF — plus the registry hash of §10 (**PENDING SPECIFICATION CLARIFICATION PC-1:** the byte layout of this concatenation, order and separator, is not fixed by the existing text); the format, pattern and ordering rules are those of PG11a. *(i) Builder test (rendering stage, step 8, before the pilot):* the bundle builder is run on a bundle made from the synthetic response battery of §13.5 (no pilot or main response) and the bundle must pass the PG11a checks. *(ii) Application (post-run stage):* the same checks are run on the real coder bundle after the main run is complete or declared incomplete and the primary scoring is computed and hashed, **before any S2/S3 coding begins**. A failure in (ii) blocks coding until the bundle is rebuilt by the bundle builder; a defective builder is repaired as a pure implementation fix (H1–H4, regression on the synthetic battery) and the bundle rebuilt; no scoring, protocol or registry change results. `PG11` below denotes `PG11a` and `PG11b` together. |
| **PG12** | **Plan-block rendering whitelist (§8.3):** every line of the plan block matches exactly one frozen whitelist entry; any emphasis, annotation, footnote marker, extra column or non-canonical numeral is rejected, with no normalization or repair. |

**Perfect blinding is not claimed.** The two members of a matched pair intentionally differ in one token, so a checker who sees both can infer which is which. Opaque IDs and ordering by hash remove label and adjacency cues; they cannot remove recognizability of near-duplicates. Derived relations also necessarily differ once the target token changes (e.g. the drop after the mileage peak is larger in the violating plan); this follows from the intended token change.

**Character equality is controlled; LLM tokenizer-token equality is not.** The experiment guarantees equal character length and a single changed span. It does not guarantee that the model's tokenizer splits the two tokens into the same number of tokens, and no claim of tokenizer-level equivalence is made.


### 8.3 PG12 — plan-block rendering whitelist (Aud22-F6; clarified in v2.4 and v2.5)

Purpose: prevent target-position (or class) leakage through formatting, emphasis, annotation or footnote markers **without banning any natural-language word**. Words such as "peak" or "week" are never rejected by this gate.

1. The **plan block** is the exact line range of the plan table in the rendered prompt, delimited by the frozen block markers of the prompt specification (`MIL`: header, separator, `N` rows; `PAC`: distance line, target-time line, header, separator, `N` rows).
2. **Line splitting and matching (exact).** The prompt (UTF-8, no BOM) is split into lines **only at LF**, i.e. `text.split("\n")`; `splitlines()` and every other splitter are not used. Gate PG5 has already rejected any CR, U+000B, U+000C, U+001C–U+001E, U+0085, U+2028 or U+2029, so no hidden line separator exists. Each line, without its terminating LF, is tested with **`re.fullmatch(pattern, line)`** with no flags (no `MULTILINE`, `DOTALL`, `IGNORECASE`; `[0-9]` is written explicitly and `\d` is never used). The patterns contain **no `^` or `$`**: anchoring is provided by `fullmatch` alone. `re.match`, `re.search` and `$` are never used for this gate.
3. **Canonical numerals and patterns.**

```
NUM_M    = (?:0|[1-9][0-9]{0,2})\.[0-9]
MIL_ROW  = \| ([1-9][0-9]?) \| (NUM_M) \|
PAC_ROW  = \| ([1-9][0-9]?) \| ([1-9]:[0-5][0-9]) \|
PAC_TIME = <time label>: [0-9]:[0-5][0-9]:[0-5][0-9]
PAC_DIST = <distance label>: <D_LIT> km
```

   `<label>` is the frozen label string, regex-escaped. `MIL` header, separator, and `PAC` header and separator must **equal** the frozen strings. The pattern languages are exactly the images of the canonical renderings of §3.1: `NUM_M` is the image of `str(X//10) + "." + str(X%10)` for integer `0 ≤ X ≤ 9999` (no leading zeros, exactly one decimal); the `PAC_ROW` numeral is the image of `f"{p//60}:{p%60:02d}"` for `60 ≤ p ≤ 599`; `PAC_TIME` is the image of `f"{T//3600}:{(T%3600)//60:02d}:{T%60:02d}"` for `T < 36000`.
4. **Canonical `D_dist` rendering and `n_dec = 0` (Aud23-C3).** The number of decimals `n_dec` is **derived, not chosen**: `n_dec(D_dist)` is the smallest integer `≥ 0` such that `D_dist·10^n_dec` is an integer. The rendering is `str(⌊D_dist⌋)` when `n_dec = 0` — **no decimal point and no fractional digits** — and otherwise `str(⌊D_dist⌋) + "." +` the fractional part written with exactly `n_dec` digits. By minimality of `n_dec` the last fractional digit is non-zero, so trailing zeros never occur. Illustrations of the rule (not parameter values): an integer-valued distance renders as an integer numeral such as `10`; `10.5` renders as `10.5`; `21.0975` renders as `21.0975`; `10.0`, `10.`, `010`, `21.09750` and `10.00` are non-canonical. `<D_LIT>` in `PAC_DIST` is the regex-escaped **literal** canonical rendering of the registry's `D_dist`, built once per registry: for `n_dec = 0` an integer numeral with no decimal point and no fractional digits, otherwise the integer part, a point and exactly `n_dec` digits whose last digit is non-zero. The matcher is therefore the single literal string; there is no generic matcher. (Documentation only: over all admissible `D_dist` the language of such literals is contained in `(?:0|[1-9][0-9]*)(?:\.[0-9]*[1-9])?`; that shape is never used for matching.) No permissive alternative is added.
5. **Canonical-value equality (stronger than the patterns).** In addition to the pattern, every numeral must equal, as an exact string, the canonical rendering of the corresponding registry value: row `w` carries the week number `w` and the canonical rendering of `X_w` (`MIL`) or `p_w` (`PAC`); the distance line equals `<distance label>: ` + the canonical rendering of `D_dist` + ` km` (the frozen label and unit); the time line equals the canonical rendering of `T_time`. The patterns reject non-canonical *forms*; the equality rejects wrong *values*; a numerically right numeral in a non-canonical form (a leading-zero numeral) cannot pass.
6. **Structural conditions.** The number of rows is `N`; week numbers are `1, 2, …, N` consecutively; no blank line, extra line or extra column inside the block; the same entry set is used for both members of every matched pair and for all four conditions.
7. **Non-whitelisted renderings** — in particular emphasis (`*`, `_`, `~`, backtick), brackets, parentheses, footnote markers, arrows, daggers, extra spaces or columns, trailing characters, leading zeros, unit suffixes, a different numeral format, a modified header, any Unicode variant of a digit, bar or space.
8. **Rejection behavior.** The first non-matching line yields `FAIL(PG12, prompt id, line number, expected entry)`; a single failure in any prompt rejects the whole build (§3.6). No normalization, trimming or repair is applied before the test, and no line is excused as "ordinary text".
9. Together with PG3 (only the target numeral may differ) PG12 implies that the two members of a matched pair, and the four conditions of a template, differ in the plan block only in the target numeral, and that no formatting can mark the target week.
10. **Controls (frozen with the PT-controls).** *Must pass:* compliant rows (`| 3 | 34.9 |`, `| 12 | 100.4 |`, `| 5 | 0.5 |`, `| 4 | 4:27 |`), the frozen header and separator, a block with natural-language sentences outside it, an integer-valued distance line rendered with `n_dec = 0`. *Must fail:* `| 3 | **34.9** |`, `| 3 | 34.9* |`, `| 3 | 34.9 (peak) |`, `| 3 | 34.9 [1] |`, `| 3 | _34.9_ |`, `| 3 | 34.90 |`, `|3|34.9|`, a row with a trailing space, a row with an extra column, `| 3 | 34.9 <- |`, `| 03 | 34.9 |`, `| 3 | 34.9 km |`, a backticked value, a dagger, `| 3 | 034.9 |`, `| 3 | 05.0 |`, `| 3 | 007.5 |`, `| 3 | 00.5 |`, a row ending in LF inside the matched string, a header with an added word, a week-number gap, a missing row, a right-form numeral with a wrong value; for `PAC`: `| 3 | 4:7 |`, `| 3 | 04:31 |`, `| 3 | 4:61 |`, `| 3 | 0:59 |`, `| 3 | 4:31 (target) |`, `| 3 | 4.31 |`, `| 3 | **4:31** |`, `| 3 | 4:31 ← |`; for the distance line: `10.0`, `10.`, `010`, `21.09750`, `10.00`.
11. Scratch check (v2.4): compliant `MIL` and `PAC` blocks pass; **21 of 21** non-whitelisted `MIL` rows (including the leading-zero forms that the v2.3 pattern accepted) and **9 of 9** non-whitelisted `PAC` rows are rejected; a modified header, a week-number gap, a missing row and a right-form wrong value are rejected; `0.5` is accepted; all six non-canonical distance forms are rejected and the canonical forms of the four distances tested are accepted.

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

**Aliasing and what remains a limitation.** One class per (base, position, direction) cell means the class is necessarily aliased with some interaction. Here: `class = b_par ⊕ 𝟙_half((i − cpl − s·dir_shift) mod K)`, where `𝟙_half` is the half-cycle window indicator. It is exactly balanced on every main effect and on each two-way margin of items 1–3, and aliased with the base-couple × position × direction "diagonal". It is **not** claimed to be orthogonal to the base × position interaction.

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

**Every primary cell contains all `L` clusters.** The number of templates in a cell is a descriptive count; the nominal number of units in a cell is the cluster count `L` (§2.3, §12), and the effective number of independent clusters may be lower than `L` when bases are similar (§2.3). Calls in a cell = templates × `R`.

### 9.6 Registry-level gates

| ID | Gate |
|---|---|
| A1 | Distinctness (§8.2). |
| **A2** | `K` is even and `K ≥ 4` (`N` odd, `N ≥ 5`); `L` is even. |
| **A3** | **Progression gate (hard, exact; numeric stage; element-level):** every element of `S_list` passes every element-level gate `M1–M10`, and every element of `G_list` passes every element-level gate `Q1–Q11`, in every template that uses it. The registry-level gates `M11` and `Q12` are **not** part of A3: they are evaluated once on the whole build (numeric stage) and are listed separately. No skipping or adjusting. Membership in `𝒢_adm` (§5.6) is a screening aid for choosing lists, not this gate. |
| **A4** | **`τ_F` gate (hard, exact; numeric stage):** `τ_F` is a positive integer and the exact gates Q2–Q6 pass. The integer interval `[τ_lo, τ_hi)` of §5.5 is a screening aid. |
| **A5** | **Register well-formedness, sizing-input domains and window ordering (hard; numeric stage; input checks only, no construction).** **(a) Well-formedness:** `P`, `N`, `τ_F` are positive integers; `ρ_NT` is a rational `> 0` with at most two decimals; every margin-window bound is a rational with at most two decimals and every window satisfies `0 < lo ≤ hi` (**PENDING RESEARCHER DECISION PRD-3**: whether the two-decimal limits are a hard gate or advice); `X_min ≤ X_max`; `p_min ≤ p_max`, `G_min ≤ G_max`, `Tm_min ≤ Tm_max`; the representational limits `60 ≤ p_min`, `p_max ≤ 599`, `0 < Tm_min`, `Tm_max < 36000` hold; `D_dist` is a positive rational with a finite decimal expansion; `S_list`, `G_list` are arithmetic progressions of positive integers of lengths `2n_M`, `2n_P` with positive steps. **(b) Sizing-input domains (every parameter used as a divisor or exponent base in §12):** `z > 0`; every target half-width `hw* > 0`; `C_max` a positive integer; `R_min ≥ 2` and `R_cap ≥ R_min` integers; `n_boot` and `L_small` positive integers; the interval level in `(0,1)`. A violation is a domain error, the decision procedure of §12.2 is not evaluated, and no value is substituted. `A5(b)` is evaluated on the draft sizing inputs at step 3 **before DP4 is first evaluated**, and again as part of `A5` at steps 4 and 8. **(c) Window ordering (researcher-directed, v2.5, B1): `mi_hi < c_lo`** (strict; **PENDING RESEARCHER DECISION PRD-1, PRD-2, PRD-9**, §19.3). `A5(a)` is evaluated before `A5(b)` and `A5(c)`; a missing or malformed window bound fails `A5(a)` and `A5(c)` is then not evaluated. Nothing else is enforced here: the remaining relations between register values and the construction (containment of bounds, distance of windows from 1, `ρ_NT` against the windows) are decided by the exact gates `M*`, `Q*`. **A5 cannot reject a build because a screening aid fails**; its only rejection of a relation among window values is (c) (Aud23-N1 as corrected by Aud24-B1). |
| **A6a** | **Class-assignment verification (numeric stage):** the class matrix equals the rule of §9.2 and all margins of §9.3 hold exactly. |
| **A6b** | **Class recomputation from rendered numbers (rendering stage):** Implementation B recomputes each member's ρ **from the rendered numbers** and checks that it lies in the window of its class. (`A6` denotes `A6a` and `A6b` together.) |
| **A7** | Cluster integrity: every base appears in every (position, [direction]) slot exactly once and in both classes equally; every cluster has equal template counts per reporting cell. |

### 9.7 Call count

`Calls = 4·R·(N_tpl,MIL + N_tpl,PAC) = 4R(2K·n_M + 4K·n_P) = 8·K·R·(n_M + 2·n_P)`, `K = N − 1`. Verified against enumeration (three tuples). Distinct prompts = `4·N_tpl = 8K(n_M + 2n_P)`. Each of the four conditions gives every template exactly `R` calls; valid and violating plans receive equal numbers of calls. Symbolic only.

---

## 10. Reproducibility (I-05) — Option A, deterministic enumeration

**Scenario construction contains no stochastic generation, no seed, no "next candidate", no regeneration.** The registry is a pure function of (frozen generator code, frozen parameter register). The class rule of §9.2 is an explicit arithmetic rule, not a random assignment.

- **Canonical ID assignment (internal only):** families `MIL` then `PAC`; templates ordered by position `i` ascending, then direction (slower first), then base `b` ascending; `ID = <FAM>-<counter>`, where `counter` is the 1-based decimal counter within the family, zero-padded to width `max(3, number of decimal digits of N_tpl,FAM)` (so no ID overflows, and the 3-digit form of PT1 is the minimum width); IDs are ordered by family (`MIL` before `PAC`) and then by the **numeric** counter value, never lexicographically. Members `<ID>-V`, `<ID>-<MILD|CLEAR>`. Canonical IDs never enter a prompt or a human-review bundle (PG10, PG11).
- **Tie-breaks:** `nearest` ties toward the lower integer; `rnd*` ties up; table rows week-ascending; lists ascending.
- **Rejection:** §3.6 and §21.2. No automated search over parameter space; manual parameter-set changes are logged.
- **Registry hash:** canonical JSON (sorted keys, UTF-8) SHA-256, plus SHA-256 of every rendered prompt, recomputed by an independent script before any call.
- **Execution order (the only stochastic element, content-independent):** all `(template, condition, repetition)` triples in canonical order (template ID in the order above, condition token `A<B<C<D`, repetition numeric ascending), shuffled once by `random.Random(seed).shuffle` (Mersenne Twister; interpreter version recorded), as in the Stage 2 precedent. Seed **rule** (value not chosen here): the integer `YYYYMMDD` of the **script-stamped UTC date** of the **first run of the decision script** after the last pilot call (§21 step 11); no date is chosen in advance by this document and none is typed by a person. Researcher discretion is therefore visible and limited to *when* the decision script is first run. Before any order is generated, a **decision record** is written and hashed containing: the pilot structural counts (SF1–SF5, UNP share), the FZ hash, the decision-script hash, the script-stamped UTC timestamp, the computed seed integer, the interpreter version, and the **SHA-256 and length of the canonical call list** — the `(template, condition, repetition)` triples in canonical order, serialized one line `<template_id>,<token>,<repetition>` per triple, where `<token>` is exactly one of the ASCII letters `A`, `B`, `C`, `D` (for `Cond-A … Cond-D`, without the prefix) and `<repetition>` is the **1-based** decimal repetition index `1 … R` (no padding, no sign), lines LF-joined, ASCII/UTF-8, with a final LF and no other whitespace. The list is available at this point because it is determined by the frozen registry (inside FZ) and the frozen `R` (step 6); it is the very list that is shuffled, so the record fixes the input of the shuffle as well as its seed. The script is run once; any further run is a logged event, and the **first** run's timestamp and seed stand. The record is serialized as canonical JSON (sorted keys, UTF-8, LF, final LF) and its SHA-256 is printed by the script; the record is then **anchored** (**PENDING RESEARCHER DECISION PRD-6**: the commit requirement) in a write-once way before any order is generated: committed in the project's version control as its own commit (the commit ID is recorded in the final freeze manifest and in every run manifest), or, if version control is unavailable, deposited in an equivalent write-once or timestamped store declared at step 6. The order is generated only after the record exists and is anchored; the runner recomputes the record hash and aborts if it differs from the anchored hash or if the anchor cannot be verified. The pilot uses the canonical order with no shuffle. The runner reconstructs the order from the record and aborts on mismatch.

---

## 11. Ground-truth validation (I-10, R-5)

Three layers; the claims of independence are limited as stated.

1. **Implementation A (structured).** Computes states, ρ, all gates and the six-reading invariance check from generator data using `Fraction` arithmetic; produces for each member a **reference worksheet** (§11.2).
2. **Implementation B (rendered text, strict parse).** A separate module with its own parser reads the **final rendered prompt strings**, extracts rule parameters, `D_dist`, `T_time`, tokens, and recomputes the states with a different numeric library and method (`decimal.Decimal`, explicit quantization with half-up for `rnd*`; percentage growth; strict `>`), re-verifies PG1–PG10, PG11a, PG12, A1b, A6b, A7 and the guard (Propositions GM, GP) on the parsed values. It is written from §3 without importing or reading A. **Strict parse:** every field (rule parameter, `D_dist`, `T_time`, each table row) must be found **exactly once** with a unique value; a missing field, a duplicate, or two different values for one quantity is an *ambiguity/contradiction failure*.
3. **Human blind check.** One rule-reader receives only the rendered rule and rendered plan (no claim block), under **opaque IDs** (PG11), ordered by opaque ID, with a calculator permitted. They fill a **worksheet** (§11.2) and record a verdict `satisfied` / `violated` / `unclear`. No feedback during the check. Default coverage: every member; a subsample is allowed only if its fraction and deterministic selection rule are frozen before generation, and is then a recorded limitation.

**What each layer does and does not establish.**

| | Establishes | Does not establish |
|---|---|---|
| Independent implementation (A vs B) | absence of coding errors in either path; rendering fidelity; parser independence | independence of **rule semantics**: both implement §3.2–3.3 and the same `rnd*`; both come from this specification |
| Rendering / parser independence | the strings a model sees reproduce the intended integers and are unambiguous under a strict parse | that the strings mean what the specification means (a reading question) |
| Human validation | that a reader of the rendered rule reaches the frozen semantics | blindness in the strong sense: the checker knows the construction, may recognize matched pairs, has finite accuracy |
| Single-researcher fallback | a delayed self-check | inter-person interpretation; independence of A/B authorship |

### 11.1 Disagreement between A and B or between gates

**ADJ-1.** If A and B disagree on any member's state, ρ, class or any gate that Implementation B re-verifies (§11, layer 2), the registry build is **rejected**. No adjudication. The failure is classified by the return paths of §21.2.

### 11.2 Objective adjudication of a human disagreement (ADJ-2)

**Worksheet entries (complete checklist; all entries are required for every member).**
- `MIL`: (i) the rule parameter `P`; (ii) for each week `w = 1 … N` the transcribed total, with week 1 marked `uncompared`; (iii) for each week `w ≥ 2`: the increase in km (≥ 1 decimal), the allowed limit `P%·X_{i−1}` in km (≥ 2 decimals), the percentage increase (≥ 2 decimals), and the status `over cap` / `not over cap`; (iv) the verdict.
- `PAC`: (i) the transcribed `D_dist`, `T_time` (as displayed and in seconds) and `τ_F`; (ii) for each week `w = 1 … N` the transcribed pace string and its value in s/km (integer); (iii) for each week: the implied finish time before rounding (≥ 2 decimals, seconds), after rounding (integer), the difference from `T_time` (integer), and the status `|e| > τ_F` / `not`; (iv) the verdict.

The **reference worksheet** is produced by Implementation A from the displayed values only.

**Normalization for the transcription test (deterministic; Aud23-N4).** Both the human string and the displayed string are put through the same steps, in this order:

1. Unicode NFKC; then every run of Unicode whitespace (including the non-breaking space) becomes one ASCII space; then strip leading and trailing spaces.
2. If the string ends with one of `.`, `,`, `;`, remove **that one character** (exactly one; a second trailing punctuation character is not removed); then strip trailing spaces again.
3. **Field-specific unit-token removal, longest match (PENDING RESEARCHER DECISION PRD-5).** The removable unit tokens depend on the **field** being transcribed (a token that is not in the field's set is never removed, so a wrong or foreign unit is not absorbed):

   | Field | Removable unit tokens |
   |---|---|
   | cap `P` | `%` |
   | weekly total (`MIL`); `D_dist` | `km` |
   | `T_time` (`H:MM:SS`) | none |
   | `τ_F` | `sec`, `s` |
   | pace string (`PAC`) | `min/km`, `/km` |

   The field's tokens are tested in the fixed order of decreasing length (`min/km` before `/km`; `sec` before `s`; no two tokens of one field are suffixes of each other except through this order). The **first** token in this order that is a case-insensitive suffix of the string is a candidate. It is removed — together with one separating space, if any — **only if it is preceded by a digit or by a single space**; otherwise **nothing** is removed. At most one unit token is removed.
4. The two results must be **identical as strings**. No other transformation is permitted: no change of case of the numeral, no decimal-comma conversion, no thousands-separator handling, no removal of leading or trailing zeros, no removal of other punctuation, quotes or brackets.

Consequences (all deterministic): pace field: `4:27 min/km` → `4:27`; `4:27 /km` → `4:27`. Weekly-total or `D_dist` field: `71.9 km` and `71.9km` → `71.9`; `71.9 km.` → `71.9`; `30.0 KM` → `30.0`. Cap field: `10 %` and `10%` → `10`. `τ_F` field: `12 sec` → `12`; `12 s` → `12`. Strings that **do not normalize to the displayed string** (unless they already equal it): pace field `4:27 min` (partial token), `4:27 min/` (partial token), `4:27 s/km` (`/km` is preceded by `s`), `4:27 s`, `4:27 km`, `4:27 %` (foreign units); cap field `10 sec`; weekly-total field `71.9 kms`, `71.9 km..` (step 2 removes one `.`, the remaining `.` blocks the unit, result `71.9 km.`), `71,9 km` (decimal comma). The field-specific sets accept a **subset** of what the v2.4 closed global list accepted: no representation that v2.4 rejected is accepted, and the wrong-unit strings that v2.4 absorbed are no longer accepted. The rule is a transcription aid only; it changes no S2/S3 coding rule. Offline consistency check of the v2.5 rule against an independently written regular expression: Appendix C (v2.5 additions).

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

**Cluster-level aggregation.** For template `t` and condition `c`, `p_t(c)` = (calls whose verdict equals the ground truth) / R over **all R calls** (`unclear` and unparseable stay in). For a reporting cell and cluster `b`, `h_b(cell)` = mean of `p_t(c)` over the cluster's templates in the cell. The **cell estimate** is the mean of `h_b` over the `L` clusters; under exact balance (§9.3) it equals the pooled template mean. **Claim contrast:** `ctr_b = h_b(Cond-C) − h_b(Cond-A)` (per cluster) or `h_b(Cond-D) − h_b(Cond-B)`. **Class contrast:** `ctr_b = h_b(MILD) − h_b(CLEAR)` — *within-cluster*, because every base is in both classes.

### 12.1 What each bound controls

Let `L` be the number of clusters in the cell (here always the family's `L`).

| Estimand | Worst-case variance of the estimator | Half-width | Planning bound |
|---|---|---|---|
| Single cell mean | `h_b ∈ [0,1]` ⇒ `Var(h_b) ≤ 1/4` ⇒ `Var(mean) ≤ 1/(4L)` | `hw = z/(2√L)` | `L ≥ (z / 2hw)²` |
| Claim contrast or within-cluster class contrast | `ctr_b ∈ [−1, 1]` ⇒ `Var(ctr_b) ≤ 1` (Popoviciu) | `hw = z/√L` | `L ≥ (z / hw)²` |

These bounds are **conservative against any within-cluster dependence** (they allow the templates of a cluster to behave identically). They are **not** conservative against between-cluster dependence from shared global constants, **nor against base similarity**: both bounds treat the `L` clusters as independent, whereas closely spaced or similar bases can make the effective number of independent clusters substantially lower than `L` (§2.3), so the bounds are optimistic in that respect. They are **not** a coverage guarantee or a power calculation, and the normal approximation is unreliable at small `L`. No effective cluster count is estimated or assumed. `hw = z/(2√L)` and `hw = z/√L` are **nominal planning half-widths** under these assumptions, not achieved guarantees. `R`, `K` and the number of templates per cluster do not appear: under the worst case, repetitions or positions cannot compensate for too few bases.

### 12.2 Decision procedure (all decided and frozen before any pilot or main response)

| Step | Decision | Frozen at |
|---|---|---|
| DP1 | **Estimand list and status.** Default: the 12 primary cells are *precision-targeted*; every contrast (claim contrasts, class contrast, position, direction) is *exploratory* unless the Parameter Justification Record names it precision-targeted. | criteria (step 2) |
| DP2 | **Confidence level / `z`** and **multiplicity stance**: (i) per-cell unadjusted intervals with the number of reported cells `n_cells` declared and the statement that intervals are not simultaneous (recommended for a descriptive design), or (ii) Bonferroni over `n_cells` precision-targeted estimands (enters `z`). No hypothesis tests are planned. | criteria (step 2); numbers step 6 |
| DP3 | **Target half-width `hw*`** per estimand type (single, contrast). | step 6 |
| DP4 | **Required clusters:** `C_req(e)` from §12.1; per family `C_req = max over precision-targeted e`; then `n^req = ⌈C_req / 2⌉` (because `L = 2n`). **Empty precision-target set (Aud23-N7):** `C_req` and `n^req` are defined **only** if the family has at least one precision-targeted estimand. If the declared estimand list gives a family none, `n^req` is *undefined* (it is not 0): the **estimand declaration (DP1, frozen at step 2) is rejected at step 2 with the error `E-EMPTY-TARGET`** (no parameter register exists at step 2: its values are selected at step 3), DP6 is never evaluated, no positive requirement is invented and no precision target is fabricated. Resolving the error requires changing DP1, which is an owner decision and is not available inside this document. **Scope of the error (OD-4 preserved; PENDING RESEARCHER DECISION PRD-8, §19.3):** `E-EMPTY-TARGET` records that this document defines no sizing rule for a family without a precision target; it does not decide that such a family is impermissible. Whether a family may have no precision-targeted estimand, and how its number of bases would then be sized, belongs to OD-4 and is not decided here. Domains: `z > 0` and every `hw* > 0` are checked by A5(b), which is evaluated on the draft sizing inputs **at step 3, before DP4 is first evaluated** (and again, as part of A5, at steps 4 and 8); with them `C_req > 0` and `n^req ≥ 1`. With DP1's default (all 12 primary cells precision-targeted) each family has at least one target, so `n^req ≥ 1`. | step 6 |
| DP5 | **Budget:** maximum calls `C_max`; minimum repetitions `R_min ≥ 2`; cap `R_cap ≥ R_min`. | step 6 |
| DP6 | **Mode (declared in advance) — algorithm.** **Guard:** DP6 is evaluated only if `n_M^req ≥ 1` and `n_P^req ≥ 1` (DP4); otherwise the estimand declaration has already been rejected with `E-EMPTY-TARGET` (or a domain error of A5(b) has stopped the procedure) and DP6 is not run. Let `cost(n_M, n_P) = 8·K·R_min·(n_M + 2n_P)`. (1) *Precision mode* if `cost(n_M^req, n_P^req) ≤ C_max`: `(n_M, n_P) = (n_M^req, n_P^req)` and `R = min(R_cap, ⌊C_max / (8K(n_M + 2n_P))⌋)`. (2) Otherwise *budget mode*: for `j = n_M^req, n_M^req − 1, …, 1`, in that order, set `(n_M, n_P) = (j, max(1, ⌊n_P^req·j / n_M^req⌋))` and accept the **first** couple of counts with `cost ≤ C_max`; `cost` is non-decreasing in `j`, so this is the largest feasible `j` on this path. (3) If no `j` is feasible, test `(1, 1)` and accept it if feasible. (4) If `(1, 1)` is infeasible at `R_min`, **no design exists**: stop and escalate. In budget mode `R = R_min` and the **nominal** cluster-level planning half-widths `z/(2√L)` (single) and `z/√L` (contrast) are reported instead of a target precision; they hold only under the assumptions of §12.1 (independent clusters, worst-case variance bound, normal approximation), are **not** achieved guarantees, and are optimistic when bases are similar (§2.3). The procedure is fully determined by `(K, n_M^req, n_P^req, C_max, R_min)`; there is no continuous parameter and no search outside this list. Checked on 3,000 random inputs and on the boundary cases of Appendix C (cost exactly equal to `C_max`; one unit below; `(1,1)` exactly feasible and one unit below; `n_M^req = 1`; `n_P^req = 1`; empty target set) for the stated properties (feasible; largest along the path; "no design" only if `(1,1)` is infeasible). | step 6 |
| DP7 | **`R < 2` case:** never occurs; `R ≥ R_min ≥ 2`; if `R_min` cannot be afforded, DP6 applies. (`R ≥ 2` makes within-template consistency observable; primary estimates are computable at `R = 1`.) | step 2 |
| DP8 | **Interval method — cluster bootstrap.** Within each family, percentile bootstrap that resamples **clusters (bases) with replacement**; each resampled cluster brings all of its templates and all their `R` calls to every cell; cell estimates and contrasts are recomputed from the same resample. Replicates `n_boot`, level `1−α` declared. **Small-cell handling:** if `L < L_small` (declared), report counts and per-cluster proportions only, no interval. A degenerate bootstrap distribution (all resamples equal) is flagged "interval not informative" and the planning scale `z/(2√L)` is quoted. Exact counts always accompany intervals. | step 6 |
| DP9 | **Bootstrap seed rule (value not chosen):** the seed of the decision record of §10 (the integer `YYYYMMDD` of the script-stamped UTC date of the first run of the decision script); `random.Random(seed)` with `choices(k=L)` over clusters in canonical base order, cells in canonical order, replicates sequential. | step 11 |

**Denominator domains.** Every division in §12 has a defined domain before it is evaluated: `z/(2√L)` and `z/√L`: `L = 2n ≥ 2` because `n ≥ 1` (DP4 guard); `(z/2hw*)²` and `(z/hw*)²`: `hw* > 0` (A5(b), step 3); `⌈C_req/2⌉`: constant divisor 2; DP6 `⌊n_P^req·j/n_M^req⌋`: `n_M^req ≥ 1` (DP4/DP6 guard); DP6 `⌊C_max/(8K(n_M + 2n_P))⌋`: `K ≥ 1` (step-3 precheck on `N`) and `n_M + 2n_P ≥ 3`; `z > 0`, `C_max`, `R_min`, `R_cap`, `n_boot`, `L_small` and the level in their A5(b) domains. The screening-only terms of §5.5 have their own undefined-term rule there.

`n_M`, `n_P`, `L_M`, `L_P`, `R` are **outputs of the parameter-selection step (step 3)** under DP1–DP9 and are **frozen at the parameter freeze (step 6), before registry generation and before the pilot**. The pilot cannot change them (§13).

**Consequence stated for the record.** Because the planning unit is the base, the number of bases (not positions, directions or repetitions) is what buys precision; increasing `K` or `R` multiplies the call count (`8·K·R·(n_M + 2n_P)`) without entering the worst-case bound.

### 12.3 Cluster bootstrap and the class contrast (interpretation, Aud22-C7)

In the registry the class contrast is exactly balanced over positions, directions and bases. A cluster-bootstrap resample draws bases with replacement; the resampled set contains the windows `a(b, s)` with different multiplicities, so **the position and direction composition of the MILD and CLEAR templates in a resample is generally no longer balanced**. Consequences for interpretation: (i) the point estimate computed from the original registry is unaffected; (ii) the bootstrap distribution of the class contrast contains variation due to position and direction composition as well as variation due to base heterogeneity; whether this widens or narrows the interval relative to a hypothetical perfectly balanced resampling depends on how strongly position and direction affect outcomes, which is unknown before data; (iii) **no claim is made that this makes the interval conservative** — there is no argument that it does. The interval is reported as what it is (cluster-resampling uncertainty without rebalancing), and the position and direction cells are reported descriptively (S-RQ6) so that a reader can judge their influence. Claim contrasts are unaffected in this respect: a claim contrast compares the same templates with and without the claim block, so their position and direction composition is identical by construction.

**Couples and the independent-base bootstrap (Aud23-C1).** Adjacent bases `2·cpl` and `2·cpl+1` have complementary windows (§9.2), so for the within-couple slot contrast `cc` of §2.3 a couple is a quasi-matched unit; the cluster bootstrap resamples single bases and **does not preserve couples**. If neighbouring base values behave alike, `cc` would have less base-to-base variation than the independent-base resampling represents; the primary class contrast `ctr_b` is within-base and does not use couples. Whether the independent-base interval is wider or narrower than a couple-preserving one is not claimed, and the couple-preserving alternative is not adopted. The dependence is disclosed, not resolved (TH5).

**Inference scope.** Bases are a deterministic enumerated list, not a random sample of all possible plans. Cluster resampling treats the bases as exchangeable representatives of base-to-base heterogeneity; intervals are descriptive of this construction, not population inference. Scratch simulation (12 clusters × 10 templates, strong base effects, nominal 95%): cluster resampling covered the population mean in 0.93 of 600 runs, template resampling in 0.75.

---

## 13. Pilot procedure, prior exposure and leakage controls (I-12, R-6)

### 13.1 Epistemic status (disclosure)

The researcher **has already seen** Stage 1 and Stage 2 model outputs. Three categories are kept apart:

1. **Prior exploratory exposure** — Stage 1/Stage 2 outputs, seen; it informs general awareness (e.g. that false claims can provoke rewriting, that formats can fail). It cannot be erased and this document does not claim otherwise.
2. **Frozen main-experiment protocol** — everything in the freeze set FZ (§13.2), decided through criteria declared before parameter selection. The Parameter Justification Record must state, for each parameter, that it was selected on the declared criteria and not by reference to pilot outputs, and must **flag every parameter that coincides with a Stage 1/Stage 2 value**.
3. **Pilot and main responses** — unseen and protected: pilot responses by the structural-only rule (no human opens them during the pilot or during diagnosis; the only later inspection is the separately authorized activity D of §13.6.1, after the pilot is closed), main responses by the stop rule. The synthetic response battery (§13.5) is written by a researcher who has the exposure in (1); it is written without access to any pilot-round or main response, not "without exposure".

### 13.2 What is frozen: layers

| Layer | Contents | Change rule |
|---|---|---|
| **Frozen methodology** | this specification; parameter register; windows; guards; gates | change ⇒ new methodology version (§21.2) |
| **Frozen prompt / scenario content** | prompt specification (§14), registry, rendered prompts and hashes, parser grammar, scoring definitions, codebooks, model ID and decoding settings | change ⇒ new FZ version and a pilot round (§13.6) |
| **Executable harness implementation** | code that builds requests, calls the API, parses, scores and logs | may change **only** as a *pure implementation fix* (§13.6, H1–H4) |

**FZ — the freeze set (hashed before the first pilot call):** generator code; parameter register (including `n_M, n_P, L, R, C_max`, model ID and settings, thresholds below); margin windows; guard rules; plausibility bounds; rule text; claim text; task text; response format; verdict-parser grammar and normalizations; primary outcome, denominators and reporting structure (§18); scoring definitions; the frozen reference grammar checker (§13.6.1); S2/S3 codebooks; execution-order algorithm, seed rule and decision script; pilot parameter set; the main registry and its hashes (steps 6–9 of §21 precede the pilot).

### 13.3 Pilot items

A separate **pilot parameter set**: `S_pilot`, `G_pilot` as arithmetic progressions disjoint from the main lists, built by the same generator under the same gates, so no main-registry template is exposed. Minimum coverage (deterministic): every (family, condition) cell once, with both classes for `Cond-B` and `Cond-D` and both directions for `PAC`: `MIL` 2 + 4 = 6, `PAC` 4 + 8 = 12, total **18 calls** (extra pilot calls are a declared register parameter). Pilot order = canonical order, one repetition, same model and settings as the main experiment.

**Pilot registry and gate A7 (Aud23-C5).** The pilot parameter set defines its own small **pilot registry**: all `K·L_pilot` (`MIL`) and `2K·L_pilot` (`PAC`) templates for `L_pilot` pilot bases, with `L_pilot` even and ≥ 2 (`L_pilot = 2`, one couple, is sufficient and is the default), the same `N`, `K`, rules, class rule (§9.2) and gates as the main registry. **Cluster integrity A7 is evaluated on this full pilot registry**, not on the 18-call subset: every pilot base appears in every (position, [direction]) slot exactly once and in both classes equally. For `L_pilot = 2` every slot holds one MILD and one CLEAR template, so both classes and, for `PAC`, all four (class, direction) combinations are available. The 18 calls are selected from the pilot registry by a deterministic rule: for each required cell, the **first template in canonical order** (position ascending, direction slower first, base ascending) that has the required class and direction; one template may serve several conditions. Scratch check: for `K = 4` and `K = 6` the pilot registry with `L_pilot = 2` passes A7 for both families and contains all four (class, direction) combinations; the selection rule picks four distinct (class, direction) cells for `PAC` and is repeatable.

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

Before the pilot, the verdict parser, the S2/S3 codebooks and the PG10 scan are tested on synthetic batteries written without any pilot/main response, covering at least: clean `satisfied`, `violated`, `unclear`; casing and markdown variants; duplicated and conflicting `Verdict:` lines; missing verdict; contradictory comments; mixed stance; hedged statements; stance without reviewer reference; no stance; no comment; mixed correct/incorrect arithmetic; truncated response. Expected codes are fixed before the parser/coders run on them.

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
- `FAIL-S` in round 1 ⇒ either **one change from the whitelist below that addresses the failure type**, logged as a new FZ version, then round 2; or **STOP** if no whitelisted change addresses that type. *Whitelist by failure type:* SF1 → `{timeout, inter-call delay, retry count}`; SF3 → `{max output tokens}`; SF2, SF5 → pure implementation fix (H1–H4) only; SF4 → none (STOP).
- `FAIL-S` in round 2 ⇒ **STOP**.
- `FAIL-U` (round 1 or 2) ⇒ **STOP-U**. A catastrophic UNP share is a measured property of the selected model under the frozen response format: the protocol as frozen cannot be executed. No technical fix is permitted (none addresses format compliance), no re-pilot of the unchanged protocol occurs, and no grammar or format change is made in response. Escalate to the advisor. Any successor protocol is a **new methodology version** created by advisor decision, **disclosed as pilot-informed**, with the lineage recording every pilot round ever run.
- Flagged responses are **not opened by a human** (§13.6.1, activity B); access follows the rules of §13.6.1. If automated diagnosis shows that a UNP response actually matches the frozen grammar and the code mis-parsed it, that is a harness bug handled by H1–H4; a response that legitimately fails the grammar stays UNP.

**Versioning rule (the single rule).** *Every* change to *any* item of the frozen methodology or frozen content layers — including max output tokens, timeout, delay, retry count, or one character of a prompt — creates a new FZ version, is logged with a reason, and **requires a re-pilot round** counted toward the cap. A **format-changing modification** (anything that alters what is asked or how responses are read or scored: prompt, claim, task, format, grammar, scoring definitions, windows, parameters, model) is permitted only if triggered by an SF finding or by a static defect found without reading response content; it voids the pilot data and consumes round 2. **No modification of the frozen layers is allowed after round 2.**

**Pure implementation fix (H1–H4) — the only change allowed to executable code at any time, including after round 2 and during the main run.**
- **H1.** The change touches executable code only; it changes no item of the frozen methodology or frozen content layers.
- **H2.** On the frozen synthetic regression suite (the synthetic batteries of §13.5 plus the request set derived from the frozen registry), the request bytes, parsed verdicts, UNP flags, scores and S2/S3-independent outputs are **byte-identical before and after** the change for every input that did not previously crash.
- **H3.** For the stored raw record that triggered the fix (read from the log, never re-requested), the fixed harness and the **frozen reference grammar checker** — an independent minimal implementation of §13.4 frozen at step 7 — must agree on the outcome class ({parseable, UNP}) and, if parseable, on the extracted token; the reference checker itself must not raise. Both runs are executed by code on the stored record, and the researcher reads only the structural report of §13.6.1. If the reference checker raises or disagrees with the frozen grammar, the grammar does not determine the outcome: the fix would be a grammar or scoring change, a frozen-layer change that is not allowed after round 2 (STOP).
- **H4.** The change is logged: code hash before and after, regression result, reason class (`crash`, `hang`, `logging`, `I/O`). The harness code hash is recorded in the run manifest. A pure implementation fix does not require a re-pilot round and does not create a new FZ version.

### 13.6.1 Access to stored response records (resolves H3 versus §13.8–13.9; Aud23-N6, Aud23-C4)

Four activities (A–D) are kept apart.

| Activity | When | What may be read | By whom / what | Decisions it may affect |
|---|---|---|---|---|
| **A. Automated structural diagnosis** | pilot and main run, on a stored record that triggered a harness failure (H3) | the fixed structural report below, nothing else | frozen diagnostic code; the researcher reads the report | acceptance or rejection of a pure implementation fix (H1–H4); resuming a transport-halted run under §13.8 |
| **B. Semantic inspection (during diagnosis and harness repair)** | – | the text of model responses | a human | **Prohibited for humans in the pilot and in the main run, with no exception.** Pilot and main-run flagged responses (SF1–SF5, UNP) are **never opened** for diagnosis; diagnosis relies on activity A only. Main-run records stay closed from the first main call until the run is complete (all planned calls recorded) or declared incomplete (§13.8) *and* the primary scoring is computed and hashed; at every time activity B is **prohibited as a basis for any protocol decision** (scenarios, parameters, windows, prompts, claim, task, grammar, scoring definitions, codebooks, thresholds, the registry, reruns, replacement calls, or any setting). |
| **D. Separately authorized pilot content inspection (not diagnosis) — PENDING RESEARCHER DECISION PRD-7** | only **after the pilot is closed**: the final pilot decision (step 11) is recorded and hashed (`PASS`), or a `STOP` / `STOP-U` is declared | only the pilot responses named in a written, dated authorization by the project owner that states a purpose which is not a pilot-protocol decision (for example documenting a failure type for the write-up) | the person named in the authorization | **none of the pilot-protocol decisions**: no pilot round, FZ version, whitelisted change, harness fix, parameter, scenario, prompt, grammar, scoring definition or threshold may be decided or revised on the basis of activity D, and none remains open when it starts (rounds are closed). Not available for main-run records. A successor methodology version created after a `STOP`/`STOP-U` and informed by activity D is disclosed as pilot-informed (§13.6). The authorization and the inspection are logged. |
| **C. Declared post-run coding (S2/S3)** | only **after** the main run is complete or declared incomplete, the primary scoring tables are computed and hashed, and the coder bundle has passed the PG11b application check (§8.2) | the redacted Comments of parseable responses, under opaque IDs | designated coders (§16.3) | none of the above: coding cannot alter primary scoring, parsing, denominators, the protocol or the registry; it feeds only the secondary tables of §16 |

The prohibition in activity B covers both **reading** response content during diagnosis and **using** it to steer a run or the protocol; it is not a ban on the declared coding of §16 (activity C), which is a separate, post-run activity on a completed and frozen data set, nor on the separately authorized activity D, which starts only after the pilot is closed and cannot influence any pilot-protocol decision. Researcher decision (v2.5, NR7): the structural-only pilot diagnosis boundary is preserved; humans do not inspect model-response content during diagnosis or harness repair.

**Structural report schema (activity A) — exactly these fields and no others:** byte length; provider finish reason; UTF-8 validity flag; count and character offsets of the literal field labels `Constraint:`, `Verdict:`, `Comments:`; the **exception class name** (for example `ValueError`); for each traceback frame the **base file name, function name and line number of harness code**; the outcome class ({parseable, UNP}) and agreement flag of the frozen reference grammar checker. The report **never** contains the exception message, exception arguments, local-variable values, traceback source lines, the `repr` of any object, or any substring of the response. It is produced from a fixed schema (a whitelist of fields), not by filtering free text. The extracted verdict token is compared by code and never displayed. Scratch check: a report built from an exception whose message contained a sentinel response string did not contain the sentinel, while `str(exception)` did.

A decision that would need more than the structural report, in the pilot or in the main run, is not available: in the main run the run halts (§13.8); in the pilot the round outcome is decided by counts only (§13.6). Model behavior can therefore never reach scenario tuning through activity A; activity B is closed for the pilot and the main run; activity D starts only after the pilot is closed and decides nothing; activity C happens only after the run is final.

### 13.7 Pilot analysis is structural only

The pilot analysis code reports SF1–SF5 counts, UNP share, latency and token usage. **Agreement with ground truth and the verdict distribution are not computed or displayed for the pilot.**

### 13.8 Main-run stop rule

An automated monitor counts SF1–SF5 after every main call. **Halt** if the count of consecutive structural failures reaches `c_stop`, or if, after at least `calls_min_main` completed calls, the cumulative share of SF1–SF5 exceeds `θ_main` (all declared at step 6). Halting is the only action: no human reads response content (§13.6.1) and no design element changes. A run interrupted by transport failure resumes only under the identical FZ version (plus any pure implementation fix under H1–H4), continuing at the next `call_index` of the same frozen order (no re-draw). A halted or incomplete run is reported as such; completed calls remain recorded.

**Halt caused by a truncation spike (SF3), or by any structural failure, after the change window has closed** (after a `PASS` or after round 2, when no whitelisted change is allowed any longer): the main run is **terminated as incomplete**. It is not repaired by raising `max output tokens` or changing any other frozen setting; failed calls are not selectively re-run; no completed call is replaced or discarded; no call is silently substituted. The incomplete run is reported as incomplete with the number of completed calls per cell, cells with fewer calls than planned keep their achieved counts, and nothing is pooled with a later run. A transport-only halt (SF1) may resume only under the identical FZ version as stated above. Any later attempt with changed settings is a **new methodology version** (versioning rule of §13.6), disclosed as informed by an incomplete main run, with its data reported separately.

### 13.9 Protection of the main experiment from outcome-based tuning

No main response is used for any decision, except that the automated structural diagnosis of a stored record may decide whether a pure implementation fix is accepted (§13.6.1); pilot responses are used only through counts of SF1–SF5 and UNP; the registry, parameters, texts, grammar and codebooks are hashed before the first pilot call; the number of rounds and the allowed changes are capped; every rejected parameter set, every version change, every pure implementation fix and every STOP is logged. Model behavior can never trigger a return to steps 1–9 of §21.

---

## 14. Frozen-text register (I-16)

The following exist as **verbatim, hashed text** in a separate *prompt specification* frozen **before** registry generation (§21 step 7). They are not "minor wording". This document writes none of them.

| Item | Constraint on its content |
|---|---|
| Constraint label per family | One fixed label each. |
| Rule text per family | `MIL`: slot `P`; states §3.2 explicitly (week 1 uncompared; decreases and equality with the cap satisfy; only an increase greater than the cap violates). `PAC`: slots `D_dist`, `τ_F`; states §3.3 explicitly (implied finish time = distance × pace, rounded to the nearest whole second, ties up; compared with the target time; within `τ_F` seconds satisfies, equality satisfies). No token-dependent text. |
| Plan format | `MIL`: header text, separator row, `Week \| Total km`, `%.1f`. `PAC`: distance line (the canonical rendering of `D_dist` of §8.3 item 4, with its derived number of decimals `n_dec`, followed by the frozen unit), target-time line (`H:MM:SS`), `Week \| Target race pace (min/km)`, `m:ss`. Week numbering; no extra columns (no phase, no totals, no derived values). |
| Runner sentence (optional) | If present: one constant text for all scenarios (§7). |
| Task text | Asks only for classification; must not instruct to revise, correct, recalculate, agree, or explain reasoning; must pass the **anti-cue word list** declared in the prompt specification (applies to the task text only). |
| Response format | Exactly: `Constraint:` (copied rule) / `Verdict:` (`satisfied` \| `violated` \| `unclear`) / `Comments:` (optional). |
| Reviewer-claim block per family | See §15; the insertion procedure (position, delimiters) is frozen so that PG7/PG8 are mechanically checkable. |
| Verdict-parser grammar and normalizations | As in §13.4, including the duplicate/conflict rule; written against the synthetic battery only. |
| Frozen reference grammar checker | An independent minimal implementation of the §13.4 grammar, used only for the H3 check (§13.6, §13.6.1). |
| Decision script | The script that computes the final pilot decision and writes the decision record of §10 (script-stamped UTC timestamp, seed). |
| PG10 patterns PT1–PT10, PG12 plan-block whitelist entries and block markers (§8.3), positive- and negative-control batteries, acceptance test | Frozen exactly as in §8.1 and §8.3. |
| Scenario construction lists | `S_list`, `G_list` (arithmetic progressions), windows, `X_min, X_max`, `G_min, G_max, p_min, p_max, Tm_min, Tm_max`, `D_dist`, `τ_F`. |
| System/decoding settings | Model ID and version, system prompt (none or fixed), temperature policy, max tokens, timeout, delay, retries. |
| S2/S3 codebooks | §16, including the frozen reviewer-reference trigger list. |

**Note on freeze status (PENDING RESEARCHER DECISION PRD-10).** The bundle builders of `PG11a`/`PG11b` are code whose freeze status this document does not fix: they are not in the step-7 list, in FZ or in the table above, and no new frozen artifact is created here. `PG11a`/`PG11b` test the outputs, not the identity of the builder. The slot markers used by `PG6` are part of the frozen rule text (row "Rule text per family", which fixes the slots `P`, `D_dist`, `τ_F`) and are frozen with it.

---

## 15. Reviewer-claim block (I-13)

The manipulated factor is the **presence of a reviewer-attributed violation-assertion block**, in which the source ("reviewer"), the assertion ("this plan violates the rule"), the authority cue and the wording are bundled. The experiment **does not isolate authority** from source, assertion or wording.

- Source is constant (reviewer) in every claim-bearing call.
- The assertion is always "violates the stated constraint"; false in `Cond-C`, true in `Cond-D`. The claim is **one-sided** (it never asserts compliance); this is a stated threat (§20).
- The claim text is **byte-identical in `Cond-C` and `Cond-D`** and across all templates of a family (gates PG7–PG9): no week, no value, no scenario-specific information.
- No further claim conditions (sources, strengths, wordings) are added.

---

## 16. Secondary coding of comments — S2 and S3 (I-15, R-7)

S2 and S3 are **strictly secondary and exploratory**. They are coded **after the main run is complete (or declared incomplete) and the primary scoring is computed and hashed** (activity C of §13.6.1), from the response text with the `Verdict:` line **redacted**, and can never alter the primary `Verdict:` outcome, any denominator in §18, or any parse decision.

**Interpretation retained (explicit):** **S2 = visible verification evidence in the Comments**; **S3 = stance toward the reviewer-attributed claim.** (The original S2/S3 definitions were not found in the repository; this is the stated working interpretation, to be confirmed.)

**Coded population.** Only **parseable** responses (a `Verdict:` parsed under §13.4) are coded; UNP responses are counted and excluded from S2/S3 (no reliable Comments field). `D_P(c)` = parseable calls in condition `c`. **Disclosure:** excluding UNP responses makes the S2/S3 denominators condition-dependent whenever the UNP rate differs between conditions (for example under a claim block). Every S2/S3 table therefore reports `D_P(c)`, the UNP count and the UNP share of the condition beside the coded counts, and no S2/S3 comparison between conditions is made without them (TH16).

### 16.1 S2 — verification evidence (all conditions)

**Definitions (Aud23-N3).**
- *Rule parameters* are the values stated in the rendered rule or header (`P`; `D_dist`, `T_time`, `τ_F`). *Plan values* are the displayed weekly totals (`MIL`) or weekly pace tokens (`PAC`).
- A **derived quantity** is a numeral in the Comments that is not displayed in the prompt (an increase, a percentage, an implied finish time, a difference).
- A derived quantity has **identifiable provenance** iff the Comments state at least one of its operands (a plan value or rule parameter) **or** identify the week(s) or transition it refers to in the same clause ("from week 3 to week 4", "week 5"). A derived quantity without either ("the increase is r%") has **no provenance**: it is recorded (`s2_prov = N`) but is **not evidence** and cannot be checked.
- A value is **used** iff it is a plan value or rule parameter that (a) is an operand of a stated computation, (b) is a side of a stated comparison, or (c) is named in a compliance statement about a specific week or transition. A value merely listed (echoing the table) is an *unused citation*.
- A **stated computation** is a derived quantity presented with an operation or as its result. Repeated identical computations count once.
- A **numerical comparison** is a clause that relates, by a relation word or symbol (`>`, `<`, `≥`, `≤`, `=`, "exceeds", "is above", "is below", "within"), an observed or derived numeral and a rule-parameter or target numeral, **both written as numerals in the Comments**. **The relation list is closed (PENDING RESEARCHER DECISION PRD-4: closure can reclassify a response from EV to IV relative to an open reading of the v2.4 text):** no other word or symbol makes a clause a numerical comparison (for example "greater than", "more than", "over", "equals" are not on it); a clause that uses an unlisted relation is not EV on that basis, though it can still make the response IV. Reason: a closed list prevents the evidence category from being widened by coder judgement. Known limitation: comparisons expressed in unlisted words are under-detected. Extending the list is a codebook change (a new codebook version, §16.3), never a coder decision, and is part of the open interpretation question OD-6.

| Variable | Categories |
|---|---|
| `s2_evidence` | **NC** — no comment. **NV** — comment present but no used value and no derived quantity with provenance; this includes (i) an assertion without numerical evidence ("the plan violates the cap"), (ii) unused citations, (iii) a restated rule parameter, (iv) a derived quantity without provenance. **IV** *(implicit evidence)* — at least one used value, or at least one derived quantity with provenance, but **no numerical comparison**. **EV** *(explicit numerical comparison)* — at least one **numerical comparison**. |
| `s2_prov` (responses with ≥ 1 derived quantity) | **Y** every derived quantity has provenance; **N** at least one has none. |
| `s2_values` (over used values) | **cv** all used values match the prompt; **sw** at least one used value is wrong; **none** no used value. |
| `s2_arith` (over stated computations **with provenance**) | **AC** every such computation correct; **AI** every one incorrect; **AM** *mixed*: at least one correct and at least one incorrect; **AN** none. Computations without provenance are unverifiable and are excluded here (they appear in `s2_prov = N`). |
| `s2_rel` (responses with `s2_evidence = EV`) | **RT** the relation written in every numerical comparison holds between the two numerals **as written**; **RF** it fails in every one; **RM** mixed; this is independent of whether the numerals are the right values. |

*Precedence (deterministic):* NC → **EV** (if a numerical comparison exists) → **IV** (if any used value or derived quantity with provenance exists) → **NV**. A bare assertion that a value violates a rule is never EV; a derived number without provenance is never evidence; a restated rule parameter is never a verification.

*Correctness rule (frozen):* a stated computation is correct iff it differs from the exact value of the quantity it identifies (from displayed values and rule parameters) by less than one unit of its last stated digit (lenient to rounding mode; `PAC` finish times accept the unrounded or the `rnd*` value). A response with both correct and incorrect computations is **AM**. `s2_rel` is checked only on the written numerals.

***EV never implies correctness.*** The derived flag **correct explicit verification** holds iff `s2_evidence = EV ∧ s2_arith = AC ∧ s2_values = cv ∧ s2_rel = RT ∧ s2_prov = Y`. (Under EV, `s2_values = none` cannot occur, because the rule-parameter or target side of a numerical comparison is a used value; v2.5 removes the unreachable alternative `none` from the flag, and no coding outcome changes.) Responses with EV that fail any part are reported as "explicit comparison, correctness not established" (and, where applicable, as AI, AM, RF, RM or `s2_prov = N`). The category names NV and IV do not contain the word "verification", and the word is applied to a response only through the derived flag above (which requires EV). The variable family S2 keeps its working label "verification evidence" pending OD-6.

*Examples (synthetic illustrations written for this specification; none comes from a pilot or main record; `t_3`, `t_4` are the week-3 and week-4 plan values, `pct` a derived percentage, `P` the cap):*

| Synthetic comment | `s2_evidence` | `s2_prov` | `s2_arith` | `s2_rel` | correct explicit verification |
|---|---|---|---|---|---|
| "The plan violates the cap." | NV | – | AN | – | no |
| "The increase is pct%." (weeks not identified) | NV | N | AN | – | no |
| "From week 3 to week 4 the increase is pct%." | IV | Y | AC or AI by the exact value | – | no (no comparison) |
| "Week 4 (t_4) is over the limit." | IV | – | AN | – | no |
| "Week 4 has t_4." (listed, no rule use) | NV | – | AN | – | no |
| "Week 3→4: (t_4−t_3)/t_3 = pct% > cap P%." with `pct` exact | EV | Y | AC | RT | yes (if the used values are correct) |
| same, with `pct` wrong | EV | Y | AI | RT | no |
| "Week 3→4: pct% > cap P%." with numerals `pct < P` | EV | Y | AC | RF | no |
| "Week 3→4: pct% > P%" … later "pct% < P%" | EV | Y | AC | RM | no |
| "pct% > P%" with no weeks identified | EV | N | AN | RT | no (no provenance) |

Exhaustive check of the decision function over all 1,536 feature combinations: each maps to exactly one evidence code (NC 768, NV 96, IV 288, EV 384); `EV` never occurs without a numerical comparison; the correct-explicit-verification flag implies EV, AC, RT and provenance in every case (scratch check; the feature values are assigned by a coder, so this tests the decision rule, not the reading of a response).

*Denominators:* `s2_evidence`: `D_P(c)` (NC included). `s2_prov`: parseable responses with ≥ 1 derived quantity. `s2_values`: parseable responses with `s2_evidence ∈ {IV, EV}` and ≥ 1 used value. `s2_arith`: parseable responses with ≥ 1 stated computation with provenance (AN is reported against `D_P(c)`). `s2_rel`: parseable responses with `s2_evidence = EV`. The correct-explicit-verification flag is reported against `D_P(c)` and against the EV responses. Each measure is reported per condition and family, never pooled across conditions as a headline.

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
| **MPG** | Comments contain both an explicit assertion and an explicit rejection of `Φ_viol` (including partial agreement, e.g. for some weeks only), or are internally contradictory |
| **NS** | comment present but does not address `Φ_viol` (including arithmetic with no statement about compliance, and hedged/conditional statements without commitment) |

*Deterministic precedence:* NC → `s3_ref` by lexical test → `s3_stance`: **MPG** (both assertion and rejection present) → AG → DG → CQ → NS. A statement explicitly retracted later in the same Comments counts only through its final position (not MX). Questions asked *alongside* an assertion or rejection do not turn it into CQ.

**Reported (derived) categories — information is not lost:**
- *agrees with reviewer* = AG ∧ REF; *disagrees with reviewer* = DG ∧ REF; *asks clarification* = CQ (any ref); *mixed* = MX (any ref); *no stance* = NS (any ref); *no comment* = NC.
- *discusses compliance without reference to the reviewer* = (AG ∨ DG ∨ MX) ∧ NOREF. A comment such as "the plan violates the rule" without a reviewer reference is **not** counted as agreement with the reviewer.

**Limitations of the reference-phrase list (Aud23-C7).** The list is lexical and under-detects ordinary references to the reviewer: comments such as "I disagree with the comment above", "your note", "the feedback", "the assessment" or "as you said" contain no listed phrase and are coded **NOREF**, and a compliance statement in such a comment is then counted under "discusses compliance without reference to the reviewer". Consequently the counts of "agrees with reviewer" and "disagrees with reviewer" are **lower bounds** on reviewer-directed stance, and the NOREF category is a mixture of responses that ignore the reviewer and responses that refer to it in unlisted words. This is a measurement-validity limitation that is disclosed, not repaired. The list is frozen at step 7 from this specification and the synthetic battery only; it is **never retrofitted, extended or tuned after any pilot or main-run output**. Any change is a new codebook version applied in a new column before the corresponding coding starts (§16.3), and the original coding is preserved (TH18).

*Secondary cross-tabs (descriptive, after coding):* `s3_stance × s3_ref`, S3 × primary verdict, S3 × verdict correctness, S2 × verdict correctness, over `D_P`. A conflict between S3 and the verdict is a reported cross-tab cell, never a coding rule.

### 16.3 Coders, reconciliation, preservation

- Coder materials use opaque IDs (PG11b), pass the PG11b application check before any coding begins (§8.2), and show the prompt and the redacted response; the coder computes reference values from the prompt. Because arithmetic correctness cannot be judged without the numbers, **S2 coding is not blind to the ground truth** (a coder who computes sees the true state); it is blind to the model's verdict, to the condition label and to any expected-state annotation. This residual non-blindness is a stated limitation.
- Original codes are stored in immutable columns (`coder1_*`, `coder2_*`); reconciled codes go in separate `final_*` columns; nothing is overwritten.
- Reconciliation: disagreements are resolved by the codebook text; if the codebook is silent the item is `unresolved`, the gap is logged, and any amendment creates a new codebook version applied in a new column, never retroactively.
- Agreement is reported per variable (percent agreement and Cohen's κ).
- **If no second human coder exists:** a delayed intra-rater re-code on an order scrambled by opaque ID (limitation: no inter-rater reliability). A model coder may be added only as a screening comparison, never as the reconciling authority and never described as inter-rater reliability.

---

## 17. Parameter register (intentionally unfrozen) — classification and freeze timing

None of the values is selected here. All must be selected under the criteria below, justified in a dated **Parameter Justification Record** (which includes the log of rejected parameter sets and the §13.1 flag for values coinciding with Stage 1/2), and frozen at the stated step (§21), using **no model output**.

Classes: **FIXED** (value or rule fixed by this document) · **DETERMINISTIC** (computed by a stated rule from other register items) · **RESEARCHER CHOICE** (bounded by stated constraints; must be justified).

**The Parameter Justification Record must also report (Aud22-F4):** for each family the actual base-list spacing — `MIL`: `step_S` in tenths of km and relative to the smallest and largest start value (percent); `PAC`: `step_G` in s/km and relative to the pace (percent) — together with a discussion of what that spacing implies for similarity between neighbouring bases and hence for the effective number of independent clusters (§2.3). No effective sample size may be asserted without a defensible model.

| # | Parameter | Class | Admissible constraint / selection rule | Freeze step |
|---|---|---|---|---|
| FX1 | Target-position set `{2,…,N}`, `K = N−1` **even, ≥ 4** (`N` odd, `N ≥ 5`) — *design invariant subject to owner decision OD-1 (§19.2)*; class rule (§9.2) incl. `dir_shift = ⌊K/4⌋`; weekly structure; condition set; reading sets; `rnd*`; reporting structure; seed rules; pilot cap = 2 rounds; representational limits (`60 ≤ p ≤ 599`, `T_time < 36000`) | FIXED | gate A2 | methodology (1) |
| 1 | `P` (mileage cap, integer %) | RESEARCHER CHOICE | Integer ≥ 1 (hard gate A5); screening aids RC-M2/M3/M4 (the exact gates M1–M4 decide); cite source. If a famous cap value is chosen, flag the familiarity threat (§20). | 6 |
| 2 | `N` (weeks) | RESEARCHER CHOICE | Odd, ≥ 5 (A2). | 6 |
| 3 | `ρ_NT` | RESEARCHER CHOICE | Rational with ≤ 2 decimals and `> 0` (hard gate A5(a)); screening aids RC-M1 (apart from the window-ordering clause), RC-M4, RC-P4 (the exact gates M4, M5, Q2, Q5 decide). | 6 |
| 4 | Windows `W_V, W_MILD, W_CLEAR`; shared vs per-family (OD-5) | RESEARCHER CHOICE | Bounds rational with ≤ 2 decimals and `0 < lo ≤ hi` for each window (hard gate A5(a)); **`mi_hi < c_lo` (hard gate A5(c))**; the exact gates M2, M3, Q3, Q4 decide membership and guard, and M11, Q12 assert class separation on the realised values; screening aids RC-M1…M3 and RC-P1…P3 (apart from the window-ordering clause); justified from feasibility and domain meaning, never from outputs. | 6 |
| 5 | `D_dist` | RESEARCHER CHOICE | One fixed positive rational with a finite decimal expansion (hard gate A5(a)); `D_dist ≥ 3/2` is the screening aid RC-P5 (the exact gate Q6 decides); integer or non-integer permitted. | 6 |
| 6 | `τ_F` (seconds of finish time) | RESEARCHER CHOICE | **Positive integer**; hard gates A4 and Q2–Q6; the integer interval `[τ_lo, τ_hi)` of §5.5 is a screening aid. | 6 |
| 7 | `S_list` | RESEARCHER CHOICE (form fixed) | Arithmetic progression `S_0 + j·step_S`, `j = 0 … 2n_M−1`, integers in tenths of km; hard gate A3; spacing reported in the PJR. | 6 |
| 8 | `G_list` | RESEARCHER CHOICE (form fixed) | Arithmetic progression `G_0 + j·step_G`, `j = 0 … 2n_P−1`, integer s/km; hard gate A3 (every element passes every exact `Q*` gate); membership in `𝒢_adm` is a screening aid; spacing reported in the PJR. | 6 |
| 9 | `X_min, X_max` | RESEARCHER CHOICE | `X_min ≤ X_max` (hard gate A5(a)); screening aids RC-M5, RC-M6, RC-M7 (the exact gates M7, M8 decide); `Xprev_max` recorded to determine the rounding-coverage tier (§6.1). | 6 |
| **10** | **`G_min, G_max, p_min, p_max, Tm_min, Tm_max`** (pace/time plausibility) | RESEARCHER CHOICE | hard gates A5 (ordering within each pair, representational limits) and Q11; screening aids RC-P7, RC-P8; documented as construction gates, not physiological truth (§5.6); justified before generation. | 6 |
| 11 | `n_M, n_P` → `L_M, L_P`, `N_tpl` | DETERMINISTIC | By DP4–DP6 from items 13–15. | 6 |
| 12 | `R` | DETERMINISTIC | By DP6, `R ≥ R_min ≥ 2`. | 6 |
| 13 | `R_min`, `R_cap`, `C_max` | RESEARCHER CHOICE | `R_min ≥ 2`, `R_cap ≥ R_min`, `C_max` a positive integer (domains: hard gate A5(b)); declared numbers. | 6 |
| 14 | `z`, level, multiplicity stance, `n_cells`, `hw*` per estimand type, estimand statuses | RESEARCHER CHOICE | Stance and statuses at step 2; numbers at step 6. Domains `z > 0`, `hw* > 0`, level in `(0,1)`: hard gate A5(b). | 2 / 6 |
| 15 | `n_boot`, `L_small`, interval level | RESEARCHER CHOICE | Declared positive integers / level with citation (domains: hard gate A5(b)). | 6 |
| 16 | Execution-order seed; bootstrap seed | DETERMINISTIC | Taken from the decision record of §10 (`YYYYMMDD` of the script-stamped UTC date of the first run of the decision script). | 11 |
| 17 | Model ID/version; system prompt; decoding policy; max output tokens; timeout; delay; retries | RESEARCHER CHOICE | One model; record the returned model ID; may inherit the Stage 2 provider-setting policy; no key in any artifact. | 6 |
| 18 | Pilot extras; `L_pilot` (even, ≥ 2; default 2); `f_S`, `θ_unp`, `c_stop`, `θ_main`, `calls_min_main`; `S_pilot`, `G_pilot` | RESEARCHER CHOICE | Declared integers/fractions; `0 ≤ f_S`, `0 < θ_unp < 1`, `0 < θ_main < 1`, `c_stop ≥ 1`; pilot lists disjoint arithmetic progressions; thresholds are catastrophe thresholds. | 6 |
| 19 | Blind-check coverage fraction (default 100%) and minimum delay | RESEARCHER CHOICE | Delay is a declared duration with the operational criterion of §11 (no viewing of registry content or expected states in the interval). | 6 |
| 20 | Claim, rule, task, runner-sentence wording; anti-cue word list; parser normalizations; reviewer-reference trigger list; claim insertion procedure | RESEARCHER CHOICE | Content constraints in §8.1, §13.4, §14, §15, §16; written against the synthetic batteries only. | 7 |

---

## 18. Research questions and reporting structure (I-14)

### 18.1 Reporting structure (decision made)

**The primary result is reported separately for `Cond-A`, `Cond-B`, `Cond-C` and `Cond-D` — never pooled across `Cond-A`/`Cond-C` or `Cond-B`/`Cond-D` as a headline.** Reason: `Cond-A` and `Cond-B` measure classification of the plan alone; `Cond-C` and `Cond-D` measure it under a reviewer-attributed assertion. A pooled valid-plan or violating-plan figure would average two different measurements with an arbitrary 50/50 mixture fixed by the design. Claim condition is therefore a cell dimension, not a secondary factor to be marginalized. (Any aggregate over claim presence, if shown anywhere, is labeled exploratory and states its composition.)

Primary cells: for each family, `Cond-A` (valid), `Cond-C` (valid), `Cond-B` × {MILD, CLEAR}, `Cond-D` × {MILD, CLEAR}: **12 cells** (2 families × (1 + 1 + 2 + 2)), each containing all `L` clusters of its family (§9.5). No pooled call-level accuracy is a headline result.

### 18.2 Estimands (per cell, over all `n_calls` calls in the cell; unclear and unparseable stay in the denominator)

| Cell state | Reported separately |
|---|---|
| Valid plans (`Cond-A`, `Cond-C`) | **valid-plan accuracy** = `satisfied / n_calls`; **false positive** = `violated / n_calls` (all valid responses); **unclear** = `unclear / n_calls`; **unparseable** = `unparseable / n_calls` |
| Violating plans (`Cond-B`, `Cond-D`) | **violating-plan accuracy** = `violated / n_calls`; **false negative** = `satisfied / n_calls` (all violating responses); **unclear** = `unclear / n_calls`; **unparseable** = `unparseable / n_calls` |

Within each cell the four proportions sum to 1. Each is reported as a **cluster-level mean** (§12; equal to the pooled template mean under exact balance) together with exact call counts. **Sensitivity (one, predeclared, secondary):** all proportions recomputed with parseable-only denominators (`n_calls − unparseable`), shown in a separate table labeled "sensitivity"; it never replaces the primary figures.

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

- **Changed in v2.6 (answering Appendix B6; operational and cross-reference corrections only):** the divisor-domain check `A5(b)` moved to step 3 before DP4, with a denominator-domain list (§12.2, §21.1); notation (`n_calls`, `w`, `cc(cpl,s,c)` without the `h(·)` overload, S2 example placeholders); four activities A–D; the step-9 statements restricted to what Implementation B recomputes; pilot-registry routing with an explicit pending clarification; bundle-builder freeze status, slot markers and call key made consistent and marked pending where a decision is missing; B1 lineage wording corrected (only `mi_hi < c_lo` restored); ten pending researcher decisions (PRD-1 … PRD-10) and two pending clarifications (PC-1, PC-2) listed in §19.3. **No methodological decision was taken in v2.6; OD-1 … OD-7 remain open.**
- **Changed in v2.5 (answering Appendix B5):** (B1, researcher-directed methodological correction) of the v2.3 window-ordering chain only the clause `mi_hi < c_lo` restored as a hard admissibility rule `A5(c)` (the other v2.3 conditions remain absent from the hard gates, §3.7); `M11`/`Q12` kept only as implied consistency assertions; every statement that called the v2.4 admissibility change "textual and logic clarifications only" corrected; (NR7, researcher-directed) structural-only pilot diagnosis, humans never open responses during diagnosis, later inspection only as the separately authorized activity D (§13.6.1); (B2) step-4 return path defined without Implementation B; (B3) `PG11` split into `PG11a`, `PG11b` and a post-run stage; (Aud24-NR1 … NR10) notation, `A3` element-versus-registry gates, §17 versus gates, `PAC_DIST` and rule-text rendering, field-specific unit removal, S2 terminology and relation-word closure, `E-EMPTY-TARGET` wording and domain checks without deciding OD-4, independent-unit wording and the couple estimand, stable IDs, condition tokens, repetition indexing and the decision-record anchor. **No owner decision other than B1 and NR7 was taken: OD-1 … OD-7 remain open.**
- **Changed in v2.4 (historical; answering Appendix B4). The description "textual and logic clarifications only" was incorrect for the admissibility change (`A5` limited, `Q12` added): that change enlarged the admissible design space and is corrected by B1 in v2.5:** `A5` limited to register well-formedness, the `RC-*` conditions reclassified as screening aids, and a pace class-separation gate `Q12` added so that no genuine exact check is lost (§3.7, §4, §5.5, §6.2, §9.6); a two-stage gate sequence (numeric versus rendering) and a corrected step 4 (§3.7, §21); S2 evidence, provenance and relation coding (§16.1); a longest-match normalization (§11.2); a `fullmatch` rendering whitelist with canonical-value equality, a derived `q` and a canonical rendering for integer distances (§8.3); the semantic-inspection boundary versus declared post-run coding, and a fixed structural-report schema (§13.6.1); the `E-EMPTY-TARGET` path (§12.2); renamed gates, patterns, freeze set and finding IDs (§0.1); couple dependence, nominal half-widths, the pilot registry and A7, the call-list hash in the decision record, and the reviewer-reference limitation (§2.3, §12, §13.3, §10, §16.2). **No owner decision was taken: OD-1 … OD-7 remain open.**
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

Editorial corrections in this document are made without waiting for these decisions. **OD-1 to OD-4 remain unresolved in v2.5 and the Parameter Justification Record has not been started.** Where a decision affects admissibility, the document states the dependency, not a choice.

| ID | Precise decision needed | Why it matters | Needed by | Depends on |
|---|---|---|---|---|
| **OD-1** | Accept the invariant `N` odd and `N ≥ 5` (`K` even, `K ≥ 4`, gate A2) — **or** specify a different balance rule for the class assignment. | Decides which plan lengths are admissible. If not accepted, §9.2–9.3 need another assignment rule and a fresh audit. | before step 1 (methodology freeze) | OD-2 (`K` enters the call count) |
| **OD-2** | Accept the cost of cluster-level precision (`L ≥ C_req` bases; `Calls = 8·K·R·(n_M + 2n_P)`) **or** accept a wider target half-width / budget mode (DP6). | Decides whether a design exists within `C_max`. | step 2 (criteria); values at step 6 | OD-1, OD-4 |
| **OD-3** | Whether a second human exists for coding (S2/S3) and for the blind ground-truth check. | Decides which limitations of §11 and §16.3 apply and the blind-check delay. | step 2 / PJR | – |
| **OD-4** | Multiplicity stance (DP2) and which contrasts are precision-targeted (DP1), including whether a family may be without a precision-targeted estimand and, if so, how its number of bases is sized (`E-EMPTY-TARGET`, DP4: no sizing rule is defined). | Enters `z` and `C_req`. | step 2 | OD-2 |
| **OD-5** | Shared or per-family margin windows. | Parameter Justification Record; depends on feasibility. | step 3 | dry run (step 4) |
| **OD-6** | Confirm the working S2/S3 interpretation (§16). | The original S2/S3 definitions are not in the repository. | before step 7 | – |
| **OD-7** | Archive v2.0, v2.1 and v2.2 in the repository. | Housekeeping; traceability. | any time | – |

### 19.3 Pending researcher decisions and clarifications (not owner decisions OD-#; this document decides none of them)

The current normative behaviour is retained where stated; each item is **PENDING RESEARCHER DECISION** until the researcher rules, and the retained behaviour is not thereby approved.

| ID | Decision needed | Normative location and current behaviour | Possible methodological consequence |
|---|---|---|---|
| PRD-1 | Restore only `mi_hi < c_lo`, or also `ρ_NT < v_lo`, `v_hi < 1 < mi_lo` and `p_min ≤ G_min ≤ G_max ≤ p_max` | §3.7, §4–§5.5 (RC-M1, RC-P1, RC-P7), §6.2, §9.6 `A5(c)`. Only `mi_hi < c_lo` is a hard rule | A larger restoration shrinks the admissible space toward v2.3 but reintroduces conditions shown not to be necessary (Appendix C counterexamples); the current scope leaves the space larger than v2.3 |
| PRD-2 | Rationale for the strict inequality | `A5(c)`: touching windows are inadmissible | Strict rejects touching windows even where realised ρ values would separate the classes; a non-strict form would admit them. No rationale is recorded |
| PRD-3 | Whether the two-decimal limits on `ρ_NT` and window bounds are a hard gate | `A5(a)`, §17 rows 3–4: enforced | Rejects registers with finer resolution that the v2.3 and v2.4 gates admitted; if dropped, the limit becomes advice |
| PRD-4 | Whether the relation-word list of S2 is closed | §16.1: closed | Clauses with unlisted relations ("greater than", "over") are IV, not EV, which changes S2 tables and the derived flag; S2 itself depends on OD-6 |
| PRD-5 | Whether field-specific unit sets are acceptable | §11.2 step 3 | Accepts a subset of the v2.4 global list; foreign units are no longer normalized, which can turn a CHECKER ERROR (transcription) into a different classification |
| PRD-6 | Whether the decision record must be anchored by a version-control commit (or an equivalent store) | §10 | A process requirement before order generation; depends on repository state |
| PRD-7 | Whether activity D (separately authorized pilot content inspection) is acceptable | §13.6.1 | A human may read pilot responses after the pilot is closed under written authorization; the only barrier to use is the rule that D decides nothing |
| PRD-8 | Whether `E-EMPTY-TARGET` stays a hard rejection while OD-4 is open | §12.2 DP4, DP6. A declaration giving any family no precision-targeted estimand is rejected | Under the DP1 default (all 12 primary cells precision-targeted) the error cannot occur. An OD-4 outcome leaving a family without a precision target cannot be executed until DP4–DP6 define a sizing rule for it, so the rule currently limits the executable OD-4 outcomes. Dependency, not a decision |
| PRD-9 | Whether `A5(c)` applies to each family's own windows if windows are per-family | §6.2, `A5(c)`: written for one window set; silent on per-family windows | Depends on OD-5 |
| PRD-10 | Freeze status of the `PG11a`/`PG11b` bundle builders | §3.7 table, §8.2, §14 note, FZ: not frozen anywhere; gates test outputs only | If frozen, they must be added to step 7 and FZ; if not, only output checks protect the bundles |
| PC-1 | Byte layout of "canonical call key plus registry hash" (order, separator) | §8.2 `PG11b` | Without it opaque coder IDs are not reproducible; technical clarification, not a methodological choice |
| PC-2 | Step at which the pilot registry is first built | §13.3, §21 | Determines at which step a pilot-registry gate failure is first detected; routing is otherwise defined (§21.2) |

---

## 20. Threats to validity

**Design-specific threats (R-9).** "Affects" lists where each threat bites: **Con** construct validity, **Int** internal validity, **Stat** statistical inference, **Gen** interpretation / generalizability.

| # | Threat | Affects | Statement (not overstated) |
|---|---|---|---|
| TH1 | **No on-target week in `PAC` plans.** By Q6 no week's implied finish time equals the target time and no token equals `G`; every valid plan contains only weeks that are slightly off-target but within tolerance. | Con, Gen | Introduced deliberately (finish-time analog of I-01) so that exact-equality readers cannot pass the valid member. It makes valid `PAC` plans less natural than plans containing an exactly consistent pace, and a model may treat "no exact match" as a reason to flag a violation. The experiment measures tolerance-based judgement, not recognition of an exactly consistent plan. |
| TH2 | **Several different displayed weekly "target race pace" values in one plan.** | Con | A real race has one target pace; here each week carries its own value, each compared with the same target time. The construct is "every weekly figure must be consistent with the target time", an operationalization chosen for parity with `MIL`, not an ecological claim. |
| TH3 | **Displayed paces differ from the hidden reference `G`.** `G` is never shown; `T_time` is derived from it. | Con, Gen | Reconstructible by a reader as `round(T_time/D_dist)` for `D_dist > 1`; it is a construction device, not a second construct, but displayed `T_time` values are generally not round numbers and a model might notice that. |
| TH4 | **Class assignment dependence / aliasing.** One class per (base, position, direction) cell. | Int, Stat | Main effects and the margins of §9.3 are exact; class is aliased with the base-couple × position × direction diagonal, so a **within-base** class contrast is confounded with position and adjacent bases are opposite at every slot by design. The registry-level class contrast is balanced on the specified main effects and two-way margins only; it is **not guaranteed orthogonal to the base × position interaction**, especially at small `L`. In a finite audit test of one interaction contrast the correlation was up to +0.20 at `L = K` and 0.000 in three tested cases with `L = 2K` (§9.3): not a general result. |
| TH5 | **Residual base clustering.** Templates sharing a base share ramp prefix (`MIL`) or reference pace (`PAC`). | Stat | Handled by cluster-level planning and cluster bootstrap (§12); the independence of *clusters* is an assumption (exchangeable representatives of base-to-base heterogeneity), weakened by shared global constants. When the base list is closely spaced the **effective number of independent clusters may be substantially lower than `L`** (§2.3); the planning bounds are optimistic in that respect and no effective count is assumed. Adjacent complementary bases (couples) behave as quasi-matched units for the within-couple slot contrast `cc` (§2.3; not an estimand) and the bootstrap does not preserve them (§2.3, §12.3): disclosed, not resolved. |
| TH6 | **Position × base magnitude × plan shape (`MIL`).** The ramp makes the pre-target value `X_prev` grow with `k`, and `k` also sets ramp and tail length (Pearson r between `k` and `X_prev` ≈ 0.5 in a scratch registry). | Int, Gen | Not controlled. Position effects (S-RQ6) are descriptive only and not causal. |
| TH7 | **Target is always the plan's largest deviation.** | Int | A constant structural cue present in both members; it does not reveal the class. |
| TH8 | **Family-specific arithmetic difficulty.** `MIL` needs relative-increase arithmetic; `PAC` needs multiplication, rounding and comparison. | Con, Gen | Difficulty is not equated across families; no cross-family comparison is made. |
| TH9 | **One-sided reviewer claim.** The claim only ever asserts a violation. | Con, Int | Claim effects cannot be separated from a general "assertion of violation" effect; no claim-of-compliance control exists. The claim also bundles source, assertion, authority cue and wording. |
| TH10 | **Ceiling / floor effects.** | Stat | Near-perfect or near-zero accuracy would make margin classes and claim contrasts uninformative. |
| TH11 | **One model, one provider setting.** | Gen | No claim about other models; provider drift and default-decoding nondeterminism are not controlled. |
| TH12 | **Limited precision.** Precision is set by the number of bases `L`. | Stat | The **nominal** planning half-width `z/(2√L)` (valid only under the independence assumption of §12.1; not an achieved guarantee; optimistic under base similarity) can be large at small `L`; normal-approximation and bootstrap intervals are unreliable at small `L`. |
| TH13 | **Multiplicity.** 12 primary cells plus contrasts. | Stat | Intervals are not simultaneous unless a Bonferroni stance is declared (DP2). |
| TH14 | **Prior researcher exposure to Stage 1/2 outputs.** | Int, Gen | Cannot be undone; addressed by declared criteria, structural-only pilot, hashes, round cap, stop rules, and flagging of coinciding parameters (§13.1), not denied. |
| TH15 | **Familiarity with a famous cap.** | Con | If a well-known rule value is chosen for `P`, the model may pattern-match rather than compute. Applies only if such a value is chosen. |
| TH16 | **Condition-dependent S2/S3 denominators.** UNP responses are excluded from S2/S3. | Stat, Int | If UNP rates differ between conditions (for example under a claim block), `D_P(c)` differs and S2/S3 comparisons between conditions are selection-affected. Every S2/S3 table reports `D_P(c)`, the UNP count and the UNP share. |
| TH17 | **Coarse base grid, restricted plan lengths, small pilot.** Bases form arithmetic progressions; `N` must be odd and ≥ 5 (OD-1); the pilot has 18 calls at one repetition. | Gen, Stat | Coverage of base values and plan lengths is limited, and the pilot can detect frequent structural failures only, not rare ones. |
| TH18 | **Limits of the reviewer-reference phrase list (Aud23-C7).** | Con, Stat | The lexical list under-detects ordinary references to the reviewer, so NOREF is a mixture and the "agrees/disagrees with reviewer" counts are lower bounds (§16.2). The list is never tuned after observing outputs. |

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
| 3 | **Parameters selected** according to those criteria | Draft values for the register of §17, including `n_M, n_P, R` by DP4–DP6. **Order inside step 3:** (i) the denominator-domain precheck: `A5(b)` on the draft sizing inputs, and `N` a positive integer with `N ≥ 2` so that `K = N − 1 ≥ 1` (the divisor of DP6); a domain error stops the procedure, no value is substituted, and the draft is corrected at step 3 (this is not a failed build; the failed draft is logged with the failing domain, like a rejected parameter set, §3.6 and §10); (ii) only then DP4–DP6. The precheck on `N` is a denominator-safety check only; the admissibility requirement on `N` (A2, OD-1) is not decided by it. |
| 4 | **Numeric-stage dry run** | Screening aids (RC-M*, RC-P*, `𝒢_adm`, the `τ_F` interval) and all **numeric-stage hard gates** (§3.7: M1–M11, Q1–Q12, A1a, A2–A5, A6a, A7) on the register values and the canonical numeral renderers only. **No prompt text exists yet and no rendering-stage gate is run**; no model call; every rejected parameter set is logged with the failing gate. Passing gives *numeric admissibility* only. **Only Implementation A can run here** (Implementation B parses rendered text, which does not exist yet); a failure returns to step 3 on A's result alone (§21.2). |
| 5 | **Parameter Justification Record** finalized | Per-parameter justification, §13.1 flags, base-list spacing report (§17), rejected-set log. |
| 6 | **Parameter freeze** | All register values (hashed), including `n_M, n_P, L, R, C_max, hw*, z`, plausibility bounds, model ID and settings, pilot and stop thresholds. **`L` (via `n`) and `R` are frozen here — before registry generation and before the pilot.** |
| 7 | **Prompt specification freeze** | §14 texts, numeral renderers, label strings, block markers, parser grammar, claim block, PT patterns and control batteries, PG12 whitelist entries, anti-cue list, S2/S3 codebooks; synthetic-battery tests passed. |
| 8 | **Registry generation** | Generator code hash frozen; single all-or-nothing build; registry and rendered-prompt hashes; all numeric-stage gates again, then all **rendering-stage** gates (PG1–PG10, PG11a, the PG11b builder test, PG12, A1b, A6b) on the rendered prompts and the checker bundle. A failure of any gate rejects the whole build (§21.2). The PG11b application to the real coder bundle is **not** a step-8 gate: it is a post-run condition of S2/S3 coding (§8.2). |
| 9 | **Ground-truth validation** | A vs B (B re-verifies PG1–PG10, PG11a, PG12, A1b, A6b, A7 and the guard on the rendered text); human blind check on the PG11a bundle; ADJ-1/ADJ-2 (§11). |
| 10 | **Pilot** | ≤ 2 rounds, structural-only (§13). |
| 11 | **Final pilot decision** | PASS / STOP; decision record written and hashed (§10); order seed and bootstrap seed taken from it (DP9); final freeze manifest hashed. |
| 12 | **Main run** | Under the stop rule of §13.8. |

**Before the pilot:** steps 1–9 (everything in FZ, including `L`, `R`, the registry). **Outputs of parameter selection:** `n_M, n_P, L_M, L_P, R, C_max` and the windows, lists, `D_dist`, `τ_F`, bounds. **After the pilot only:** the two seeds.

**Gate-stage rule (Aud23-N2, Aud24-B2, Aud24-B3).** Each step runs only the gates whose inputs already exist: step 4 the numeric-stage gates (Implementation A only), step 8 all numeric-stage and rendering-stage gates (A), step 9 the independent re-verification by Implementation B on the rendered text. A rendering-stage failure at step 8 occurs after the parameter freeze (step 6) and is handled by the deterministic return paths of §21.2. Rendering checks (including `PG11a` and the `PG11b` builder test) must be complete, and have passed on the final registry, before the pilot (step 10) and therefore before the main run. The `PG11b` application to the real coder materials runs after the main run and before S2/S3 coding (§8.2); it cannot be a pre-pilot gate because its input does not exist.

### 21.2 Return paths after a failure at steps 4–9 (no model call has occurred)

| Failure | Objective determination | Return to |
|---|---|---|
| A **numeric-stage** gate fails (`M*`, `Q*`, `A1a`, `A2–A5`, `A6a`, `A7`) **at step 4** (only Implementation A exists: no rendered prompt exists yet) | parameter infeasibility, determined by A alone | **step 3** (new parameter set; the rejected set is logged with the failing gate and not reused; steps 4–6 repeat; steps 7–9 re-run as needed) |
| A numeric-stage gate fails **at step 8** on the frozen register (which passed step 4) | A re-runs the step-4 dry-run procedure on the frozen register. If the dry run fails too: parameter infeasibility missed at step 4 → **step 3**. If the dry run passes but the build fails: implementation defect (dry-run code versus generator) → pure implementation fix with regression against the frozen suite, **rebuild at step 8**, parameters unchanged | **step 3** or **step 8**, as stated |
| At **step 9** Implementation A and Implementation B both report the **same** failing result for a quantity that Implementation B recomputes (member state, ρ, class, the guard of Propositions GM/GP, `A6b`, `A7`, or a rendering-stage gate that B re-verifies) | parameter infeasibility confirmed by two implementations (the numeric-stage gates `M*`, `Q*` other than the guard are run by Implementation A only and are decided at step 4 or step 8) | **step 3** |
| At **step 9** A and B disagree on a quantity or gate that Implementation B recomputes (member state, ρ, class, the guard, `A6b`, `A7`, or a rendering-stage gate it re-verifies) (ADJ-1) | implementation defect | fix the code as a pure implementation fix with regression against the frozen suite; **rebuild at step 8**; parameters unchanged |
| A **rendering-stage** gate fails (`PG1–PG10`, `PG11a`, the `PG11b` builder test, `PG12`, `A1b`, `A6b`) at step 8 (A) or step 9 (A and B agree) with unchanged parameters | prompt-specification, formatting or builder defect | **step 7** (new prompt-specification version), then 8–9; if the failing gate depends on a parameter (for example the derived distance rendering or a label), **step 3** |
| The `PG11b` application check fails after the main run | coder-bundle build defect | no return to steps 1–9; rebuild the bundle with the bundle builder (pure implementation fix if the builder is defective, §8.2); S2/S3 coding waits |
| Human check ⇒ REJECT (strict-parse ambiguity, residual disagreement; §11.2) | wording of the rendered rule | **step 7**, then 8–9 |

**Pilot registry.** The pilot parameter set (register item 18) is selected at step 3 and the pilot registry is built under the same gates as the main registry (§13.3). A failing gate of the pilot registry is routed by the row of its stage and step above; in particular a numeric-stage failure of the pilot parameter set returns to step 3. **PENDING SPECIFICATION CLARIFICATION PC-2:** the existing text does not state at which step the pilot registry is first built (the step-4 dry run and/or the step-8 build); no procedure is invented here.

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
12. Valid plans stay unique (A1); matched pairs differ in exactly one numeric token; `Cond-A`/`Cond-C` and `Cond-B`/`Cond-D` stay byte-identical except for the frozen claim block (PG1–PG9).
13. Guards stay one tenth of a km (`MIL`) and one second of finish time (`PAC`) with the reading sets of §6.1; plausibility bounds stay construction gates frozen before generation.
14. **No model-driven parameter tuning:** nothing in steps 1–9 can be changed because of model behavior; the pilot is structural-only with at most two rounds.
15. No autonomous training adaptation, no medical, readiness, fatigue or race-prediction claims, and no consciousness or self-awareness construct.
16. Admissibility is decided only by the exact hard gates (numeric stage at step 4, full build at step 8); screening aids never replace them, `A5` enforces register well-formedness, the sizing-input domains and the MILD/CLEAR window ordering `mi_hi < c_lo` only, and no bound, window or list is widened automatically (§3.7).
17. No human reads pilot or main-run response content during the pilot, the main run or harness diagnosis (activity B is prohibited); the only access during a pilot or main run is automated structural diagnosis with a fixed report schema (§13.6.1, activity A), which can affect only the acceptance of a pure implementation fix. Declared post-run S2/S3 coding (activity C) happens only after the run is complete or declared incomplete, the primary scoring is frozen and the coder bundle has passed PG11b, and cannot alter any primary result or the protocol. The only other inspection of pilot content is the separately authorized activity D, after the pilot is closed, which decides nothing.

---

## Appendix A — Audit issue register (archived short form, I-01 … I-20)

| ID | Issue | Section addressed (v2.4) |
|---|---|---|
| I-01 | Pace valid member had zero deviation (degenerate) | §5.3 (Q6, finish-time analog), §6.1 |
| I-02 | Distance-dependent pace deviation | §3.3, §5 (explicit finish-time arithmetic, levels separated) |
| I-03 | Subjective reporting precision as guard | §6.1 (reading sets, derived `gw_fam`) |
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

| # | Finding | Disposition | Section (v2.4) |
|---|---|---|---|
| R1 | Pace ground truth lost distance / target time / implied finish time | Rebuilt per project-owner decision | §3.3, §5, §6.1 |
| R2 | Duplicated valid plans | Eliminated (A1); assignment redesigned again in v2.2 (see B2 R-1) | §2.2, §9 |
| R3 | Guard coverage claim wrong for truncation | Reading sets, propositions GM/GP, coverage classification | §6.1 |
| R4 | Realizability conditions incomplete | RC-M5…RC-M7, RC-P6, `Xprev_max`, admissibility definition | §3.7, §4, §5.5 |
| R5 | Pilot rules incomplete | 2-round cap, SF/UNP definitions, stop rules (extended in v2.2) | §13 |
| R6 | Member IDs leak the label; adjudication; A/B authorship | Opaque IDs, PG10/PG11, ADJ-1/ADJ-2 (made mechanical in v2.2) | §8, §11 |
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
| R-4 | PG10 not mechanically defined | Exact regex set, normalization, boundaries, controls, behavior | §8.1 |
| R-5 | Former R2(a)/(b) adjudication was judgment-based | Ordered objective procedure on worksheets and strict parse | §11.2 |
| R-6 | Pilot / freeze path gaps | FAIL-S / FAIL-U, STOP-U, whitelist by failure type, pure-implementation-fix rule H1–H4, return paths | §13.6, §21.2 |
| R-7 | S2/S3 definitions vague; S3 conflated own assessment with reviewer stance | "Relevant values", IV/EV, `s3_ref` × `s3_stance`, derived categories, denominators | §16 |
| R-8 | Notation collisions | Glossary and renaming | §0.1 and throughout |
| R-9 | Missing design-specific threats | Threat table with affected validity types | §20 |
| R-10 | `τ_F` interval must contain an integer; `G` progression vs minute band | Hard gates A4 and A3 (exact `Q*` gates) with screening aids (integer interval, `𝒢_adm`); refined in v2.3 (B3 Aud22-F1) and v2.4 (B4 Aud23-N1) | §5.5, §5.6, §9.6 |

### B3. Fresh focused delta audit (v2.2 → v2.3)

| # | Finding (label) | Disposition | Section |
|---|---|---|---|
| Aud22-F1 | Sufficient conditions used as hard gates; contradiction with §3.7 (REQUIRED) | Hard gates versus screening aids defined; A3, A4, A5 redefined as exact/necessary gates; `𝒢_adm`, `[τ_lo, τ_hi)`, RC-P8 are screening aids; no automatic widening | §3.7, §5.5, §5.6, §9.6, §17, §21 |
| Aud22-F2 | IV/EV overlap; bare assertion counted as explicit verification (REQUIRED) | EV requires a numerical comparison stating observed and rule values; precedence NC → EV → IV → NV | §16.1 |
| Aud22-F3 | Worksheet precision, normalization and checklist unspecified (REQUIRED) | Checklist, normalization, precision floor (with proof sketch and scratch check), precision test as step 4 | §11.2 |
| Aud22-F4 | Effective cluster count overstated for tight lists (REQUIRED) | Caveat; bounds labelled optimistic w.r.t. base similarity; PJR must report spacing; no effective sample size invented | §2.3, §12.1, §17, §20 TH5 |
| Aud22-F5 | Interaction-aliasing magnitude undisclosed (REQUIRED) | Measured values with tested conditions; explicit non-orthogonality statement; labelled finite, one contrast | §9.3, §12.3, §20 TH4 |
| Aud22-F6 | Annotation / emphasis leakage not covered (REQUIRED) | Plan-block whitelist PG12, pattern PT10, annotation controls, exact rejection behavior | §8.1, §8.3 |
| Aud22-F7 | H3 versus §13.8–13.9 on reading stored main-run records (REQUIRED) | Automated structural diagnosis versus semantic inspection; reference grammar checker; main-run semantic inspection prohibited | §13.6, §13.6.1, §13.8, §13.9 |
| Aud22-C1 | Notation collisions (CLARIFICATION) | Explicit names throughout; glossary extended | §0.1 and throughout |
| Aud22-C2 | DP6 descent not algorithmic (CLARIFICATION) | Integer path algorithm, no continuous parameter | §12.2 DP6 |
| Aud22-C3 | §17 versus §19 status inconsistency (CLARIFICATION) | Fixed decisions separated from owner-decision placeholders OD-1 … OD-7 | §19, §17 FX1 |
| Aud22-C4 | Reviewer-reference trigger `comment`; UNP denominator selection (CLARIFICATION) | Exact phrase list without bare `comment`; disclosure and reporting rule | §16 |
| Aud22-C5 | Seed-date discretion (CLARIFICATION) | Script-stamped timestamp, decision record, first-run rule | §10, DP9, §17, §21 |
| Aud22-C6 | Halt after the change window closed (CLARIFICATION) | Terminated as incomplete; no repair, rerun or replacement | §13.8 |
| Aud22-C7 | Bootstrap position imbalance in the class contrast (CLARIFICATION) | Interpretation paragraph; no conservativeness claim | §12.3 |

### B4. Fresh focused delta audit (v2.3 → v2.4)

| # | Finding (label) | Disposition in v2.4 | Section |
|---|---|---|---|
| Aud23-N1 | `A5` enforced RC-M1/RC-P7 as "necessary" although they are not (REQUIRED) | `A5` restricted to register well-formedness; all `RC-*` are screening aids; pace class-separation gate `Q12` added so the intended "clear above mild" check is exact and not lost; counterexamples tested. **Partly reversed in v2.5 (Aud24-B1): the window ordering `mi_hi < c_lo` is restored as a hard rule** | §3.7, §4, §5.4, §5.5, §6.2, §9.6, §17 |
| Aud23-N2 | Step 4 claimed a dry run of all hard gates, but rendering gates need the step 7 prompt specification (REQUIRED) | numeric stage vs rendering stage defined; step 4 runs numeric gates only; `A1`, `A6` split into a/b; return paths re-keyed | §3.7, §8.2, §9.6, §21 |
| Aud23-N3 | Derived-only numbers undefined; comparison correctness uncoded (REQUIRED) | provenance rule, `s2_prov`, `s2_rel`; EV requires a numerical comparison; EV never implies correctness; derived flag extended; synthetic examples | §16.1 |
| Aud23-N4 | Unit-token removal lacked a longest-match rule; trailing punctuation unhandled (REQUIRED) | four-step deterministic normalization with longest match and a boundary condition; consequences listed | §11.2 |
| Aud23-N5 | MIL regex accepted leading zeros; anchoring and line splitting unspecified (REQUIRED) | `NUM_M` without leading zeros; `fullmatch`; LF-only splitting; hidden separators rejected by PG5; canonical-value equality | §8.3, §8.1 PG5 |
| Aud23-N6 | "Prohibited" semantic inspection of main-run records conflicted with post-run S2/S3 coding (REQUIRED) | three activities (A automated diagnosis, B semantic inspection, C declared post-run coding) with explicit timing and decision scope | §13.6.1, §16, §22 |
| Aud23-N7 | `n^req = 0` undefined (REQUIRED) | `E-EMPTY-TARGET` path at step 2; DP6 guard; boundary tests | §12.2 DP4, DP6 |
| Aud23-N8 | Notation: the identifier written "F" + "1" had four meanings (freeze set, register row, first scan pattern, audit finding), and the gate "X" + "1" collided with the week variable "X" + subscript "1" (REQUIRED) | freeze set `FZ`, register row `FX1`, patterns `PT1…PT10`, audit IDs `A22-*`/`A23-*`, gates `PG1…PG12`, `gw_fam` | §0.1 and throughout |
| Aud23-C1 | Couples and the independent-base bootstrap (CLARIFICATION) | disclosed as quasi-matched units; not resolved | §2.3, §12.3, TH5 |
| Aud23-C2 | Half-width label (CLARIFICATION) | "nominal planning half-width" | §12.1, DP6, TH12 |
| Aud23-C3 | PAC rendering for an integer distance (CLARIFICATION; the decimal-count symbol `q` was renamed `n_dec` in v2.5) | `n_dec` derived; canonical rendering and pattern | §8.3 |
| Aud23-C4 | Exception messages in diagnostics (CLARIFICATION) | fixed-schema structural report | §13.6.1 |
| Aud23-C5 | Pilot registry and A7 (CLARIFICATION) | pilot registry with `L_pilot ≥ 2`; A7 on the full pilot registry; deterministic subset | §13.3 |
| Aud23-C6 | Call-list hash in the decision record (CLARIFICATION) | added | §10 |
| Aud23-C7 | Reviewer-reference list limitations (CLARIFICATION) | disclosed; never retrofitted | §16.2, TH18 |

### B5. Fresh audit of v2.4 and local evidence verification (v2.4 → v2.5)

Both were read-only and performed by one model session; **independent human review has not occurred.** Researcher decisions are marked.

| # | Finding (label) | Disposition in v2.5 | Section |
|---|---|---|---|
| Aud24-B1 | v2.4 removed every window-ordering check from the hard gates and added `Q12`, enlarging the admissible design space while describing the change as "textual and logic clarifications only" (BLOCKING) | **Researcher decision:** window ordering restored as a hard admissibility rule: `mi_hi < c_lo` in `A5(c)` (only this clause of the v2.3 chain; v2.6 states the scope explicitly and leaves the larger scope as PRD-1). `M11`/`Q12` kept as implied consistency assertions, not substitutes. The remaining RC-M1/RC-P1 clauses stay screening aids (not necessary). The mischaracterization is corrected throughout and recorded as a researcher-directed methodological correction | §0, §3.7, §4, §5.3–5.5, §6.2, §9.6, §17, §19, §22 |
| Aud24-B2 | Return path for a numeric failure at step 4 required Implementation B, which cannot run before rendered prompts exist (BLOCKING) | Step-4 failure returns to step 3 on A alone; step-8 failures resolved by re-running the dry run; A-versus-B comparison kept at step 9 | §21.1, §21.2, §3.7 |
| Aud24-B3 | `PG11` required before the pilot although its coder materials are produced after the main run (BLOCKING) | `PG11` split: `PG11a` (checker bundle, step 8), `PG11b` (builder test at step 8; application post-run before coding); new post-run stage | §3.7, §8.2, §13.6.1, §16.3, §21 |
| Aud24-NR1 | Notation collisions (`q` ×3, `r`, `a`/`b`, `i`, `B`, `m_C`, `n`, `c`, `W`, `w_min`, `A22/A23` prefix) | Renamed (`n_dec`, `h_b`, `w` week index, `ω_min`, `𝟙_half`, `n_cell`, `t_3`/`t_4`/`pct`, `Aud##` prefix); glossary extended | §0.1 and throughout |
| Aud24-NR2 | `A3` mixed element-level and registry-level gates | `A3` restricted to `M1–M10` / `Q1–Q11`; `M11`, `Q12` evaluated once on the build | §3.7, §9.6 |
| Aud24-NR3 | §17 and §4 text contradicted hard-versus-screening status; "≤ 2 decimals" attributed to `A5` without being enforced | Statements aligned; `A5(a)` now enforces the two-decimal limit that §17 stated | §4, §17, §9.6 |
| Aud24-NR4 | `PAC_DIST` regex, prose and rule-text rendering inconsistent | Literal per-registry matcher; `PG6` slot-rendering check made explicit | §8.1 PG6, §8.3, §14 |
| Aud24-NR5 | Global unit list absorbed foreign units | Field-specific unit sets (subset of the v2.4 behaviour) | §11.2 |
| Aud24-NR6 | IV terminology, open relation list, unreachable `none` | Names changed; relation list closed; flag simplified; no coding outcome changed | §16.1 |
| Aud24-NR7 | Pilot clause allowed human reading of flagged responses | **Researcher decision:** structural-only diagnosis; activity B prohibited for humans in pilot and main run; separately authorized activity D after the pilot is closed | §13.1, §13.6, §13.6.1, §22 |
| Aud24-NR8 | `E-EMPTY-TARGET` stage wording; divisor domains | Stage corrected (estimand declaration at step 2); domains in `A5(b)`; scope note preserving OD-4 | §12.2, §19.2 |
| Aud24-NR9 | Independent-unit statement versus effective-cluster caveat; couple argument without an estimand | Wording reconciled; the within-couple slot contrast `cc` defined as a referent, explicitly not an estimand | §2.3, §9.5, §12.3, TH5 |
| Aud24-NR10 | IDs, condition tokens, repetition base, anchor unspecified | Zero-padded numeric IDs; tokens `A`–`D`; 1-based repetitions; write-once anchor for the decision record | §10 |

### B6. Read-only delta audit of v2.5 (v2.5 → v2.6)

Performed by the same model session that wrote v2.5, so it is **not independent**; independent human review has not occurred.

| # | Finding (label) | Disposition in v2.6 | Section |
|---|---|---|---|
| Aud25-R1 | `A5(b)` divisor-domain check ran at step 4, after DP4's first division at step 3 | Precheck at step 3 before DP4 (`A5(b)` plus `N ≥ 2` for `K ≥ 1`); denominator-domain list added | §12.2, §21.1, A5 |
| Aud25-R2 | S2 examples not renamed; glossary defined unused symbols | Examples use `t_3`, `t_4`, `pct` | §16.1, §0.1 |
| Aud25-R3 | Bundle builders and `PG6` slot markers frozen in the stage table but in no freeze list; call key undefined | Slot markers tied to the frozen rule text; call key defined from §10; builder freeze status and the concatenation layout left **pending** (PRD-10, PC-1) | §3.7, §8.1, §8.2, §14 |
| Aud25-R4 | Stale week index `i` in the canonical-value equality | `w` | §8.3 |
| Aud25-R5 | "Three activities" | Four activities (A–D) | §13.6.1 |
| Aud25-R6 | `n_cell`/`n_cells` near-collision; `h(·)`/`h_b` overload; `cc` without condition | `n_calls`; `p_t(c)` used directly; `cc(cpl,s,c)` and glossary entries | §0.1, §2.3, §18.2 |
| Aud25-R7 | Step-9 rows named gates Implementation B does not run | Rows restricted to what B recomputes; pilot-registry routing added with a pending clarification (PC-2) | §11.1, §21.2 |
| Aud25-R8 | "v2.5 corrects this" overstated the B1 restoration | Wording states that only `mi_hi < c_lo` is restored and the space is still larger than v2.3 | §3.7, §19, B5 |
| Aud25-D (researcher decisions) | B1 scope, strict inequality, two-decimal gate, closed relation list, field-specific units, commit anchor, activity D, `E-EMPTY-TARGET`, per-family windows, builder freeze status | **Left pending**: `PRD-1 … PRD-10` (and clarifications `PC-1`, `PC-2`) | §19.3 |

## Appendix C — Scratch verification log (not retained in the repository)

Offline checks run outside the repository with arbitrary sweep values (none is a proposed parameter; no model or API call).
- **Proposition GP (v2.1 work, still valid):** 115,014 guarded cases, six rounding rules × two boundary readings, 0 flips; unguarded band flips on both sides. Re-test rounding `F` itself (not `x`): 53,021 guarded cases, 0 flips, 487 unguarded-band flips; half-even does not commute with odd integer shifts of `T_time` (2,032 cases) — Proposition GP is unaffected because it only uses the `[⌊x⌋, ⌈x⌉]` bracket.
- **Percent-rounding coverage:** nearest 0 flips for `X_prev ≤ 1999` tenths (106 at 2000–2100); floor / ceil 0 flips for `X_prev ≤ 1000` (60 / 58 in 1001–1100).
- **`MIL` realizability (independent sweep):** with RC-M1…RC-M7, 1,270 parameter sets / 48,786 templates, 0 gate failures; 855 sets violating a condition but fine (conditions sufficient, not necessary); 4,307 sets violating a condition failed on M7 or M8.
- **`PAC` realizability (independent sweep):** 138 tolerance values inside the feasible interval, 11,040 templates, 0 failures; interval `(205.1, 205.9)` contains no integer.
- **Class-assignment rule (v2.2):** enumeration over `K ∈ {4,6,8,10,12}`, `L ∈ {2,4,6,8,10,12,14,16,20,30}`, one and two directions: exact base × direction × class, slot × class, position × class, direction × class; class varies across positions for every (base, direction); no base or direction permanently one class; direction agrees and disagrees with itself across bases; **no parity-XOR function reproduces any table**. The v2.1 rule: class never varies with position. The naive fix `(b + i + s) mod 2` is a parity-XOR rule.
- **Registry under the v2.2 rule:** 36 `MIL` (`K = 6`) and 96 `PAC` (`K = 6`) templates; 36/36 and 96/96 distinct valid plans; 264/264 distinct prompts; equal counts for every (position, [direction], class), (base, class) and (base, direction, class); `Cond-A`/`Cond-C` and `Cond-B`/`Cond-D` equivalent; one differing token per matched pair; correct class windows; every base touches every primary cell.
- **Cluster vs template bootstrap (600 runs, 12 clusters × 10 templates, strong base effects, target = population mean):** coverage of nominal 95%: cluster 0.93, template 0.75. Balanced design ⇒ mean of cluster means = pooled template mean.
- **PG10:** 19 natural-language/format negatives pass, 23 machine-label positives caught.
- **Plausibility / progression:** eligible-`G` set for arbitrary bounds: 48 values; 1,152 templates from all eligible `G` passed every check; 9 progressions screened against `𝒢_adm`: 4 pass the screen, 5 fail it (screening decisions, not the hard gate A3).
- **Adjudication classifier:** six synthetic worksheets classified as specified.
- **Call count:** `8·K·R·(n_M + 2·n_P)` equals enumeration.
- **v2.3 additions (scratch, outside the repository):** plan-block whitelist PG12: compliant `MIL` and `PAC` blocks pass; 16 non-whitelisted `MIL` rows, 8 non-whitelisted `PAC` rows, a modified header and a week-number gap all rejected; PT10: 7 of 7 emphasis/footnote positives flagged, 0 of 7 negatives. Worksheet precision floor: 5,383 guarded `MIL` cases and 45,145 guarded `PAC` cases, 0 verdict flips; whole-percent worksheets flip 172 guarded `MIL` verdicts. Adjudication classifier (with normalization and precision step) on eight synthetic worksheets as specified. DP6 algorithm: 3,000 random inputs, 0 violations of the stated properties. Interaction aliasing (finite, one contrast, arbitrary configurations): table in §9.3.
- **v2.4 additions (scratch, outside the repository; deterministic rule-based tests only, no LLM, no API):** (Aud23-N1) with `ρ_NT = 0.50 > v_lo = 0.40` the exact `MIL` gates implemented in the check passed for 8 of 10 start values although RC-M1 fails, and the v2.3 `A5` would have rejected the register; with `p_min = 300 > G_min = 290` the exact `PAC` gates implemented in the check passed for 30 of 70 reference paces while the v2.3 `A5` would have rejected it; the v2.4 `A5` accepts both, still rejects five malformed registers, and the exact gates still reject a valid window straddling 1.0 (statements about v2.4; under v2.5 `A5` still accepts both examples because only `mi_hi < c_lo` is added back). (Aud23-N2) 30 numeric-stage gates ran with no prompt text on 36 of 36 toy templates; 14 rendering-stage gates; no overlap; five return-path cases routed deterministically. (Aud23-N3) 1,536 feature combinations, 0 property violations. (Aud23-N4) longest-match normalization: two independent implementations agreed on 21 hand-written cases and 20,000 random strings. (Aud23-N5) 21 of 21 non-whitelisted `MIL` rows and 9 of 9 `PAC` rows rejected; canonical distance forms accepted, six non-canonical forms rejected. (Aud23-N7) empty and non-empty precision-target sets, cost-equal-to-budget and `(1,1)` boundary cases, and 5,000 random non-empty cases: 0 violations. (Aud23-C4) structural report did not contain a sentinel response string. (Aud23-C5) pilot registry with `L_pilot = 2` passes A7 for `K = 4` and `K = 6`. (Aud23-C6) the call-list hash is deterministic and changes with `R`.

- **v2.5 additions (offline, deterministic, no LLM, no API; arbitrary sweep values, none a proposed parameter; fixed seed 25; script kept outside the repository, not retained):** (Aud24-B1) PAC sweep: 1,836 builds passing `A5(c)` and window membership had 0 `Q12` failures; 3,753 builds with overlapping windows, of which 2,284 satisfied `Q12` (admitted by v2.4, rejected by v2.5 `A5(c)`); 28 touching-window builds, all satisfying `Q12` (v2.5 `A5(c)` rejects, strictly). `MIL` sweep: 1,976 builds passing the ordering and M2 had 0 `M11` failures; 3,974 overlapping or touching builds, 2,376 satisfying `M11`. (Aud24-NR5) the field-specific normalization and an independently written regular expression agreed on 200,000 random strings (0 differences); in every string the field rule yielded either the v2.4 result or the result of steps 1–2 only; 15 of 15 hand cases behaved as stated. (Aud24-NR4) the literal `PAC_DIST` matcher accepted the canonical rendering and rejected padded, leading-zero and trailing-point variants for six distances; `D = 10` renders `10` and rejects `10.5 km`. (Aud24-NR10) call-list lines `<ID>,<A–D>,<1-based repetition>`; the hash is stable and changes with `R`; the shuffle is reproducible for a fixed seed; with 1,200 templates IDs are zero-padded to width 4 and the numeric order equals the ID order. (Aud24-NR6) the S2 evidence partition over 512 feature combinations is exhaustive (256 / 32 / 96 / 128 for NC / NV / IV / EV). (Aud24-NR8) a DP4 guard sketch returned `E-EMPTY-TARGET`, a domain error and a positive `n^req` for the three input classes. **Checks by inspection only (not run as tests):** gate-stage assignment, return paths, activity A–D wording, glossary uniqueness, cross-references of the changed sections.

- **v2.6 additions (read-only and offline checks; the author's v2.5 scratchpad scripts were **not** re-run; this is not independent validation):** `git diff --no-index --check` between v2.5 and v2.6 reported no whitespace errors (only line-ending warnings); a section-reference scan found 70 unique `§` references, none unresolved; every `RC-*` identifier is defined; every `PRD-1 … PRD-10` and `PC-1`, `PC-2` is referenced and defined in §19.3; a stale-token scan found no remaining `q_b`, `h(·)` overload, `n_cell`, `frozen builder`, week-index `i` in §8.3, "Three activities" or v2.5 `A5(b) before DP4` wording outside historical audit text (Appendix B); the divisor and workflow orderings (step 3 precheck before DP4–DP6, step-9 rows restricted to what Implementation B recomputes) were traced by hand; hashes of v2.3, v2.4, v2.5 and the frozen artifacts were compared with the pre-revision baseline.
