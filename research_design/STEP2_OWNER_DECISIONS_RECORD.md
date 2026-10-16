# Step 2 Owner Decisions Record

**Decision date:** 2026-10-09
**Methodology baseline:** `research_design/SCENARIO_CONSTRUCTION_SPECIFICATION_v2_7_DRAFT.md` (version tag `S2-SCENARIO-METHODOLOGY-v2.7-FROZEN`; sha256 `d5fcffadd1045fc0c86a7c84eb8d51592d807576b6a51b712cef025164082ca8`; 219,455 bytes), as recorded in `research_design/METHODOLOGY_FREEZE_MANIFEST_v2_7.json`.

## 0. Nature of this file

- This is an **administrative Step 2 record** created on the **explicit authorization of the project owner on 2026-10-09**.
- The frozen v2.7 protocol did **not** specify the location or format of this file. It is not claimed to be a protocol-defined artifact; the owner authorized it as a new administrative file, in the same manner in which the owner approved the format and location of the Step 1 freeze manifest.
- It **records owner decisions; it is not an amendment** of the specification. The specification, the freeze manifest, the codebook, the prompt specification, the scenario registry and all other artifacts are unchanged. No v2.8 or other methodology version exists or is implied.
- This file does **not** declare Step 2 complete. Step 2 completion is a separate check against §21.1.
- No numerical Step 6 parameter is chosen here.

## 1. Owner decisions

### OD-4 — Precision targets and interval interpretation

| Field | Content |
|---|---|
| ID / date | OD-4 / 2026-10-09 |
| Approved choice | **DP1:** all 12 primary cells are precision-targeted. **DP2:** per-cell unadjusted intervals; these are **not** simultaneous intervals across cells; **no Bonferroni correction** is applied to the targeted estimands. Contrasts (claim contrasts, class contrast, position, direction) remain **exploratory** unless explicitly designated precision-targeted in the Parameter Justification Record (PJR) under the protocol. The rule `E-EMPTY-TARGET` is preserved unchanged. |
| Operational implications | Both choices coincide with the protocol defaults of DP1 and DP2(i). Every family has at least one precision-targeted estimand, so `E-EMPTY-TARGET` cannot arise under this declaration (PRD-8 remains a dependency note, not a decision). The reported intervals must carry the statement that they are not simultaneous, and `n_cells` must be declared (number at step 6). No hypothesis tests are planned (DP2). |
| Relevant specification | §12.2 DP1, DP2, DP4 (`E-EMPTY-TARGET`); §17 row 14; §19.2 (OD-4); §19.3 (PRD-8); §20 TH13. |
| Dependency status | OD-4 was listed as depending on OD-2. OD-2 is recorded below. Enters `z` and `C_req`; their numerical values are deferred to step 6. |
| Status | Owner decision recorded. Not a specification amendment. |

### OD-2 — Design mode

| Field | Content |
|---|---|
| ID / date | OD-2 / 2026-10-09 |
| Approved choice | **Precision mode** is the desired mode. The feasibility rule and fallback written in the frozen specification apply as written. |
| Operational implications | Per DP6, precision mode applies if `cost(n_M^req, n_P^req) = 8·K·R_min·(n_M^req + 2n_P^req) ≤ C_max`. If the precision design is not feasible within the budget, the protocol's own fallback applies (budget mode, then the `(1,1)` test, then "no design exists: stop and escalate"). This record neither adds nor removes any step of that fallback. Because mode is determined by feasibility, precision mode is the preferred outcome, not a guarantee. |
| Not decided here | `C_max`, `hw*`, `z`, `R_min` (value), `R_cap`, `n_boot`, `L_small`, level, `n_cells` and any other value the protocol assigns to step 6. The criterion `R_min ≥ 2` (DP5, DP7, §19.1 e) is unchanged. |
| Relevant specification | §12.2 DP3–DP7; §17 rows 11–15; §19.2 (OD-2); §21.1 rows 2, 3, 6. |
| Dependency status | OD-2 depended on OD-1 (resolved in the freeze manifest, 2026-10-09) and OD-4 (recorded above). Values at step 6. |
| Status | Owner decision recorded. Not a specification amendment. |

### OD-3 — Human coding arrangement

| Field | Content |
|---|---|
| ID / date | OD-3 / 2026-10-09 |
| Approved choice | **One human coder only**; no second human exists for S2/S3 coding or for the blind ground-truth check. |
| Operational implications | The single-researcher limitations of §11 and §16.3 apply. S2/S3 coding follows the **delayed intra-rater re-code** on an order scrambled by opaque ID. **No inter-rater reliability and no Cohen's κ may be claimed.** A model coder, if used at all, is a screening comparison only, never the reconciling authority and never described as inter-rater reliability. The blind ground-truth check is the delayed self-check ("single-researcher fallback", §11); its minimum delay is a declared duration chosen at step 6 under the operational criterion of §11 and §17 row 19 (no viewing of registry content or expected states in the interval). Pilot response content stays unread by humans in this methodology version (PRD-7, §13.1, §13.6.1). |
| Relevant specification | §11 (layer 3 and the single-researcher row); §16.3; §17 row 19; §19.2 (OD-3); §19.3 (PRD-7); §20 (measurement validity). |
| Dependency status | None (OD-3 lists no dependency). Delay duration deferred to step 6. |
| Status | Owner decision recorded. Not a specification amendment. |

## 2. Already resolved (not re-decided here)

- **OD-1** resolved 2026-10-09 per the freeze manifest (`N` odd, `N ≥ 5`; `K` even, `K ≥ 4`).

## 3. Items deferred (not decided by this record)

| Item | Deferred to |
|---|---|
| DP3 (`hw*`), DP4 numbers (`C_req`, `n^req`), DP5 (`C_max`, `R_min` value, `R_cap`), DP8 (`n_boot`, `L_small`, level), `z`, `n_cells` number, blind-check delay duration and coverage fraction | Step 6 |
| DP9 (bootstrap seed) and the execution-order seed | Step 11 |
| OD-5 | Step 3 |
| OD-6 | Before step 7 |
| OD-7 | Any time |
| PRD-4, PRD-5, PRD-6, PRD-8, PRD-10, PC-1, PC-2 | Pending per §19.3; unchanged |

## 4. Protocol defaults retained

DP1 default and DP2(i) are retained as written; DP6 mode algorithm, DP7 (`R ≥ R_min ≥ 2`), the rounding-coverage tier rule (§6.1; tier stated in the PJR from `Xprev_max`) and the blind-check delay criterion (§11, §17 row 19) are frozen in the specification and are unchanged by this record.

## 5. Not started

Step 3 (parameter selection), PJR finalization, scenario or prompt generation, pilot and main experiment have not been started by this record.
