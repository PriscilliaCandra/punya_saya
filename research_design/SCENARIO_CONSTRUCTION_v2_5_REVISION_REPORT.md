# Scenario Construction Specification — v2.4 → v2.5 Revision Report

**Status.** v2.5 is a working draft. It is **not independently validated**: the same model session that made the changes also ran the offline checks. A fresh audit and local evidence verification of v2.4 preceded this revision; independent human review has not occurred.

**Artifacts.**
- v2.5: `research_design/SCENARIO_CONSTRUCTION_SPECIFICATION_v2_5_DRAFT.md`, 1,333 lines, 198,826 bytes, SHA-256 `da9cacf8fb32cc158c4aa52b34cbea7a6760ae3332ddc836f43103fa68bc6aa5`.
- v2.4: retained unchanged, SHA-256 `17af97e1c1282254be697314ecdae0ae5158f9124632bdfae4e09a269b6523e2`.
- v2.3: retained unchanged, SHA-256 `61bf398d59bad3c3d729cdc8e3f5217ee7162a47023bdc30a12fb752fe487196`.
- The v2.4 revision report is untouched.

**Correction of a prior description.** v2.4 (title line, §19 and its revision report) described itself as "textual and logic clarifications only". That was incorrect for its admissibility change (`A5` limited to well-formedness, `Q12` added): the change enlarged the admissible design space. v2.5 records the restoration below as a **researcher-directed methodological correction**, not a clarification.

## Researcher decisions implemented

| ID | Decision | Implementation |
|---|---|---|
| B1 | Restore explicit MILD/CLEAR window ordering as a hard admissibility rule | New clause `A5(c)`: `mi_hi < c_lo` (strict). Stated in §3.7, §5.5, §6.2, RC-M1/RC-P1 rows, §17 item 4, §22.16, §19 summary, the lineage table and Appendix B5/C. |
| NR7 | Preserve the structural-only pilot diagnosis boundary | §13.6.1: activity B (human semantic inspection) is prohibited in the pilot and in the main run with no exception. Flagged responses are never opened for diagnosis. New activity D, a separately authorized inspection, is allowed only after the pilot is closed and decides nothing. §13.1, §13.6, §22.17 aligned. |

**What B1 does and does not restore.**
- Restored: `mi_hi < c_lo` only, as instructed.
- Not restored: the other clauses of the v2.3 chain (`ρ_NT < v_lo`, `v_hi < 1 < mi_lo`) remain screening aids. They are not necessary (the Appendix C counterexample stands), and the guards M3/Q4 decide the relation of the windows to 1.
- **Open question for the researcher:** if "consistent with the v2.3 design" was meant to include the full v2.3 chain as hard rules, that would reintroduce the `ρ_NT < v_lo` restriction the audit showed to be non-necessary. I did not do this because the instruction named only the MILD/CLEAR ordering.

**Q12 and M11 under the restored rule.**
- With `A5(c)` and window membership (M2 / Q3), the realised targets satisfy `max ρ_MILD ≤ mi_hi < c_lo ≤ min ρ_CLEAR`. Q12 and M11 are therefore implied and can never reject a build that passes `A5(c)` and Q3 / M2.
- They are kept only as implementation consistency assertions, labelled "not a substitute for `A5(c)`". This is a redundancy, not a conflict. M11 was already redundant with the v2.3 ordering. Removing Q12 would also be consistent; I kept it so the gate counts (30 numeric, 14 rendering) and the references stay stable.

## Technical and textual corrections

| ID | Disposition |
|---|---|
| B2 | §21.2 return paths rewritten. A step-4 numeric failure returns to step 3 on Implementation A alone. A step-8 numeric failure is resolved by re-running the step-4 dry run: parameter infeasibility goes to step 3, an implementation defect to a rebuild at step 8. The A-versus-B conditions move to step 9, where B can run. |
| B3 | `PG11` split. `PG11a` (checker bundle, built from rendered text) is a step-8 gate. `PG11b` has a builder test at step 8 on the synthetic battery, which is part of the pre-pilot precondition, and an application to the real coder bundle after the main run and before coding (a new post-run stage in §3.7, §8.2, §13.6.1, §16.3). Nothing that must pass before the pilot was weakened. |
| NR1 | `q` now means the class only (decimals are `n_dec`, the cluster proportion is `h_b`). Also renamed: week index `w` in §3, `ω_min`, `𝟙_half`, `n_cell`, synthetic placeholders `t_3`, `t_4`, `pct`, `(1+P/100)`. Stale `B` and `m_C` fixed. Audit-ID prefix changed to `Aud22-`/`Aud23-`/`Aud24-`. Glossary extended. |
| NR2 | `A3` covers the element-level gates `M1–M10` / `Q1–Q11`. `M11` and `Q12` are evaluated once on the build. |
| NR3 | §17 rows 1, 3, 4, 5, 9 and §4 now match the gates. `A5(a)` enforces the "≤ 2 decimals" limit that §17 had stated without a gate. |
| NR4 | `PAC_DIST` is a literal per-registry matcher (no generic regex as matcher). `PG6` explicitly requires canonical slot rendering of `P`, `τ_F`, `D_dist` in the rule text, checked by Implementation B. §14 wording fixed. |
| NR5 | Unit removal is field-specific, so foreign units are not absorbed. The accepted set is a subset of v2.4's behaviour. |
| NR6 | IV renamed "implicit evidence", EV "explicit numerical comparison". The relation-word list is declared closed. The unreachable `s2_values = none` is removed from the flag. No coding outcome changes. |
| NR8 | DP4 stage wording corrected (the estimand declaration, not a register, is rejected at step 2). `A5(b)` adds positivity or integer domains for `z`, `hw*`, `C_max`, `R_min`, `R_cap`, `n_boot`, `L_small` and the level. The τ_lo undefined-term case is handled. **OD-4 is not decided**: the E-EMPTY-TARGET scope note says the error records "no sizing rule defined", not "target-free family forbidden", and the OD-4 row now names this question. |
| NR9 | §9.5 now says "nominal number of units"; the effective-cluster caveat is cross-referenced. The couple argument is tied to a defined within-couple slot contrast `cc`, explicitly not an estimand. |
| NR10 | Zero-padded numeric IDs with no overflow limit. Condition tokens `A`–`D`. 1-based repetition index. Call-list line format fixed. The decision record is anchored write-once (own commit, or an equivalent store declared at step 6) before the order is generated. |

## OD-1 to OD-7
All remain **open and undecided**. No wording was changed that resolves any of them. E-EMPTY-TARGET was kept (see NR8). The only decisions taken are B1 and NR7, which the researcher made.

## Validation
**Tests actually run** (offline, no API; script and output kept outside the repository, fixed seed 25):
- Window ordering: 1,836 PAC builds passing `A5(c)` plus Q3 had 0 Q12 failures; 3,753 overlapping-window builds, of which 2,284 satisfied Q12 (v2.4 admitted them, v2.5 rejects them); 28 touching-window builds, all satisfying Q12 (rejected by the strict inequality). MIL: 1,976 builds with 0 M11 failures; 3,974 overlapping or touching builds, 2,376 satisfying M11.
- Normalization: two independent implementations agreed on 200,000 strings (0 differences); the field rule always yielded the v2.4 result or the steps-1–2-only result; 15 of 15 hand cases.
- PAC_DIST literal matcher for six distances.
- Call-list serialization, hash and seeded shuffle reproducibility.
- S2 evidence partition over 512 combinations.
- A DP4 guard sketch.
- Section-reference, RC-id and stale-token scan on v2.5: 68 section references, 0 unresolved.

**Checked by inspection only** (not tests): gate-stage assignment, return paths, activity A–D wording, glossary uniqueness for changed symbols, and the full v2.4 → v2.5 diff (132 lines removed, 183 added), which I read against the approved scope.

## Remaining uncertainties
- The B1 scope question above (chain beyond `mi_hi < c_lo`).
- v2.3, v2.4, v2.5 and this report are untracked in Git, so immutability rests on hashes alone.
- The author's earlier scratch counts in Appendix C remain unverifiable.
- OD-1 to OD-7 block the methodology freeze and the Parameter Justification Record, which has not started.
- A focused delta audit by an independent human is still required.

No commit or push occurred. No frozen artifact, v2.3, v2.4, backend or frontend file was modified.
