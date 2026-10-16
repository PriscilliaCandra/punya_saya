# Step 3 Owner Provisional Preferences

**Date recorded:** 2026-10-11
**Methodology baseline:** `research_design/SCENARIO_CONSTRUCTION_SPECIFICATION_v2_7_DRAFT.md` (version tag `S2-SCENARIO-METHODOLOGY-v2.7-FROZEN`; sha256 `d5fcffadd1045fc0c86a7c84eb8d51592d807576b6a51b712cef025164082ca8`).

## 0. Nature of this file (read first)

- This is an **administrative record**, created on the explicit authorization of the project owner. The frozen v2.7 protocol does not specify its location or format.
- It records **provisional owner preferences**. It is **not** an amendment of the specification, **not** the Parameter Justification Record (PJR), and **not** final approval of any parameter.
- Every entry below has the status **`PROVISIONAL — NOT APPROVED`**. A value becomes a parameter of the study only after explicit written owner approval and the later freeze steps of the protocol.
- No v2.8 or other methodology version exists or is implied. The specification, the freeze manifest, `STEP2_OWNER_DECISIONS_RECORD.md` and `STEP3_PARAMETER_DRAFT.md` are unchanged by this file.
- No model or API call, Step 4 gate, dry run, pilot or experiment was run in preparing it. No currency amount, price or token estimate appears here.
- Labels: **[P]** protocol provision · **[H]** arithmetic result · **[J]** researcher judgment · **[O]** owner decision still pending.

## 1. Register of provisional preferences

| # | Provisional choice | Status | Dependencies / implications | Follow-up decision needed |
|---|---|---|---|---|
| 1 | Provider: **Gemini**. Model ID and version **not decided**. | PROVISIONAL — NOT APPROVED | [P] One model; the returned model ID is recorded; model ID, system prompt, decoding, max output tokens, timeout, delay and retries are frozen at Step 6 (§17 row 17). Any later change creates a new FZ version and needs a re-pilot (§13). Determines cost per call. | Exact model ID/version; settings (section 3). |
| 2 | **`hw* = 0.20`** as the provisional main candidate; **`0.25`** remains the alternative. | PROVISIONAL — NOT APPROVED | [H] At 95%, `hw* = 0.20`: `C_req = 25`, `n^req = 13`, `L = 26` clusters per family, nominal half-width at realized `L` 0.1922. `hw* = 0.25`: `C_req = 16`, `n^req = 8`, `L = 16`, nominal 0.2450. Nominal planning figures only: worst-case variance, independent clusters, normal approximation; not coverage, power or achieved precision, and optimistic under base similarity [P, §12.1, TH5, TH12]. | Final choice of `hw*` (0.20 or 0.25). |
| 3 | Level **95%**, **`z = 1.96`** | PROVISIONAL — NOT APPROVED (awaiting final confirmation) | Enters `C_req`, `n^req` and the calls. [J] A convention, not a derived value; DP2(i), no multiplicity correction (OD-4). | Final confirmation of level and `z`. |
| 4 | **`R_cap = 2`** | PROVISIONAL — NOT APPROVED | [P] `R_cap ≥ R_min ≥ 2` (A5(b)). `R_min` itself is not decided. [H] With `R_cap = R_min = 2`, `R = 2` whenever precision mode is feasible; unused budget is not spent on repeats. `R` does not enter the precision bound. | Final `R_min` and `R_cap`; comparison with `R_cap = 3` (+50% calls) remains open. |
| 5 | **`D_dist = 10`** (km) | PROVISIONAL — NOT APPROVED | [P] Integer `D_dist`: `r = 0`, the half-second rounding stage is not exercised in the data (guard proofs still cover it). `D_dist` sets the PAC lattice step. `τ_F`, the windows and the plausibility bounds are conditional on it. | Final `D_dist`; recomputation of `τ_F` if it changes. |
| 6 | **`P = 10`** (% mileage cap) | PROVISIONAL — NOT APPROVED | [P] A citable source is required for the chosen cap, and the familiarity threat TH15 must be disclosed (a well-known 10% rule can be pattern-matched rather than computed). The value coincides with the Stage 1/2 cap, which §13.1 requires the PJR to flag. No source has been supplied; none is invented here. [H] The MIL screening arithmetic does not force `P = 10`. | A source for `P`; the owner's stance on TH15 and its disclosure. |
| 7 | **`G_max = 349`** retained | PROVISIONAL — NOT APPROVED | [H] With `G_max = 349`: 41 admissible elements, operational limit `L_P ≤ 40` (`L_P` even). The theoretical limit 42 would need `G_max ≥ 350` and passing all bounds and gates; it is a sensitivity analysis, not a decision, and not a global limit. [H] For `L_P = 26` the candidate list `G = 310…335` lies inside the exact band (screening arithmetic only; Q11 and A3 are Step 4). | Reopen only if `hw* < 0.155` is considered. |
| 8 | **`τ_F = 50`** | PROVISIONAL — NOT APPROVED (conditional candidate) | Conditional on `D_dist = 10`, the candidate windows, `ρ_NT = 0.40` and OD-5; not an independent decision. [H] `τ_F = 50` sits at the lower end of the screening interval `[50, 149]`; MILD has one lattice value (thin margin). The exact gates M3, Q3, Q4 decide at Step 4. | Final `D_dist` first; then `τ_F` after the step-4 result. |
| 9 | **API budget limit not decided.** | PROVISIONAL — NOT APPROVED (no value) | See section 2. No budget is assumed. | Owner budget and the definition of `C_max`. |
| 10 | **All other parameters remain unapproved** (including `N`, `K`, `R_min`, `ρ_NT`, the windows and OD-5, `S_list`, `G_list`, `X_min/X_max`, plausibility bounds, `n_cells`, `n_boot`, `L_small`, pilot thresholds, blind-check delay). | NOT APPROVED | Draft candidates in `STEP3_PARAMETER_DRAFT.md` keep their draft status (PROPOSED / OWNER DECISION REQUIRED / DEFERRED). | Case-by-case owner decisions. |

## 2. Definition of `C_max` and separation of budgets

- [P] `C_max` is the **maximum number of calls** (DP5; §12.2), a positive integer (A5(b)). It is a count, not an amount of money. The call formula `8·K·R·(n_M + 2n_P)` counts the planned main-run calls (`R` per template-condition).
- [P] The specification does **not** say whether pilot calls, retries and failed calls count toward `C_max`. This is a gap in the frozen text; it is not resolved here and the specification is not amended.
- [O] The owner must define the coverage of `C_max`:
  1. main-run planned calls only; or
  2. main plus pilot; and
  3. whether retries and failed calls are inside or outside it.
- [O] The owner must also decide whether the **calls budget** (`C_max`, a count) and the **monetary budget** (a currency ceiling, possibly covering main, pilot, retries and a possible re-selection of the model after a pilot STOP) are kept **separate** or combined into one budget. [J] Keeping them as two distinct quantities avoids confusing a call count with a cost cap.
- [H] **Conditional computation, not a decision and not a cost estimate:** for `N = 5`, `K = 4`, `R = 2`, `n_M = n_P = 13`, `Calls = 8·4·2·(13 + 26) = 2,496`. This is the minimum `C_max` at which precision mode would be feasible for that configuration (DP6, with `R_min = 2`). It is the call count only, in no currency. It holds only if `N = 5`, `R = 2` and 95%/`hw* = 0.20` are finally approved and the later gates admit `n_M = n_P = 13`. Below that `C_max`, DP6 budget mode or its fallbacks apply [P].

## 3. Model, pricing and limits to be confirmed (no values assumed)

The following must be confirmed by the owner from official sources before any cost figure is produced. None is estimated here.

1. Exact model ID and version.
2. Official input and output price per token (source, date, currency).
3. Whether the model bills hidden reasoning tokens as output.
4. Maximum output tokens and the decoding policy.
5. Prompt token count, from the final prompt and the model's own tokenizer (final prompts do not exist before Step 7).
6. Quota and rate limits, inter-call delay, timeout, and any batch pricing.
7. Currency and exchange rate for the monetary ceiling.
8. Whether main and pilot share one monetary budget.

## 4. Citations still required

- **`P = 10`:** a citable source for the chosen cap, plus the TH15 familiarity disclosure and the Stage 1/2 coincidence flag (§13.1). Missing.
- **`n_boot = 10,000`:** a citation for the replicate count (§17 row 15). Missing. No citation has been verified or invented.
- Also noted in the draft as judgment without source: plausibility bounds, `L_small`, pilot thresholds.

## 5. Decisions that must wait for the feasibility gate (Step 4)

- Admissibility of the candidate register under the exact gates (M*, Q*, A1–A7), including the thin MILD lattice at `D_dist = 10`, `τ_F = 50`.
- OD-5: shared versus per-family windows (a Step-4 failure returns to Step 3 under §21.2; no automatic switch).
- Final `S_list`, `G_list`, `Xprev_max` and the coverage tier.
- Whether `n_M = n_P = 13` (and `L_M = L_P = 26`) is admitted; the DP6 mode outcome and `R`.
- Final `τ_F` and plausibility bounds.

## 6. Not done

Step 4, feasibility gate, dry run, pilot, main experiment, scenario or prompt construction, PJR finalization, and model/API calls have not been started.
