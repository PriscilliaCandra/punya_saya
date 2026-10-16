# Scenario Construction Specification — v2.5 → v2.6 Candidate Revision Report

**Status.** v2.6 is a **candidate** working draft. It is **not independently validated**: the same model session that wrote v2.5 audited it and wrote v2.6, and all checks below are self-authored. Independent human review has not occurred.

**Artifacts.**
- v2.6: `research_design/SCENARIO_CONSTRUCTION_SPECIFICATION_v2_6_DRAFT.md`, 1,382 lines, 212,125 bytes, SHA-256 `19f989337a8b8c9fab6a8497f36049ad8267b248c8d99bd77c56e9c92ceea425`.
- v2.5, v2.4 and v2.3: retained unchanged (hashes in the specification's lineage table, rows 9, 11 and 13).

**Scope.** Operational and cross-reference corrections only. No methodological decision was taken. Every unresolved researcher decision is marked `PENDING RESEARCHER DECISION` in the specification itself (§19.3) at the normative location, so this report does not describe anything the specification does not.

## Corrections made

| Audit item | Change | Where in v2.6 |
|---|---|---|
| Aud25-R1 (DP4/A5(b) order) | The divisor-domain check `A5(b)` is now evaluated on the draft sizing inputs **at step 3, before DP4 is first evaluated**, together with `N` a positive integer ≥ 2 so that `K = N − 1 ≥ 1`. It is repeated inside `A5` at steps 4 and 8. A step-3 domain error stops the procedure, substitutes nothing, and is logged like a rejected draft. A "denominator domains" paragraph lists every division in §12 and its domain. The `N ≥ 2` precheck is weaker than A2, so it does not touch OD-1. | §12.2 (DP4 row, new paragraph), §21.1 step 3, §3.7 stage table, §9.6 `A5(b)` |
| Aud25-R2 | S2 examples now use `t_3`, `t_4`, `pct`. | §16.1 |
| Aud25-R3 | The slot markers of `PG6` are tied to the frozen rule text (§14, "Rule text per family", which fixes the slots). "Canonical call key" is defined as the call-list line `<template_id>,<token>,<repetition>` of §10. Claims that the bundle builders are "frozen" were removed from the stage table and gate text, and their freeze status is left pending. | §3.7, §8.1, §8.2, §14 note |
| Aud25-R4 | Week index `i` → `w` in the canonical-value equality. | §8.3 item 5 |
| Aud25-R5 | "Three activities" → "Four activities (A–D)"; all references to A–D checked. | §13.6.1 |
| Aud25-R6 | `n_cell` → `n_calls` (distinct from `n_cells`); `cc(cpl, s, c)` has a condition index and uses `p_t(c)` directly, so the `h(·)`/`h_b` overload is gone; glossary extended. | §0.1, §2.3, §18.2 |
| Aud25-R7 | Step-9 rows now name only what Implementation B recomputes (state, ρ, class, the guard, `A6b`, `A7`, rendering gates it re-verifies); ADJ-1 aligned. Pilot-registry gate failures are routed by stage and step. | §11.1, §21.2 |
| Aud25-R8 (B1 lineage) | The text now says that only `mi_hi < c_lo` of the v2.3 chain is restored; `ρ_NT < v_lo`, `v_hi < 1`, `1 < mi_lo` and `p_min ≤ G_min ≤ G_max ≤ p_max` remain absent; the admissible space is still **larger than under v2.3**. | §3.7, §19, lineage row 13, Appendix B5 |

## Methodological changes

**NONE.**

Edits that might look like decisions, and why they are not:
- **`A5(b)` timing:** it was already a hard gate with the same domains, so it moves earlier without changing which sets are admissible. The `N ≥ 2` precheck is strictly weaker than A2.
- **Builder wording:** removing "frozen" from the builders drops a claim no freeze list supported. No step list, FZ definition or gate result changes. Decision left as PRD-10.
- **Slot markers:** treated as part of the frozen rule text. This is a reading of §14, not a new frozen artifact; stated in the specification so the researcher can reject it.
- **Step-9 rows:** narrowed to what Implementation B actually recomputes, so no behavior is claimed that does not exist.

## Pending researcher decisions (not resolved here)

All ten are in §19.3 with the normative location, current behavior and possible consequence. The current behavior is retained where stated and **is not thereby approved**.

- **PRD-1** B1 scope: only `mi_hi < c_lo`, or also `ρ_NT < v_lo`, `v_hi < 1 < mi_lo`, and the bounds containment.
- **PRD-2** Rationale for the strict inequality.
- **PRD-3** Two-decimal limits as a hard gate (`A5(a)`, §17 rows 3–4). The specification is coherent either way, so I did not stop for this one.
- **PRD-4** Closed S2 relation-word list (§16.1).
- **PRD-5** Field-specific unit sets (§11.2).
- **PRD-6** Commit-based decision-record anchor (§10).
- **PRD-7** Activity D (§13.6.1).
- **PRD-8** `E-EMPTY-TARGET` as a hard rejection while OD-4 is open.
- **PRD-9** `A5(c)` with per-family windows (OD-5).
- **PRD-10** Freeze status of the `PG11a`/`PG11b` bundle builders.

**Pending clarifications (technical, not methodological):**
- **PC-1** Byte layout of "canonical call key plus registry hash".
- **PC-2** The step at which the pilot registry is first built.

## OD-1 to OD-7
All seven remain open. I checked the normative rules, not only the table.
- **`E-EMPTY-TARGET`** (§12.2, DP4 and DP6) does limit which OD-4 outcomes are executable: a declaration leaving a family without a precision-targeted estimand is rejected because no sizing rule exists. Under DP1's default (all 12 primary cells targeted) it cannot fire. This is recorded as PRD-8, a dependency of OD-4, not a decision. I did not stop, because the specification is executable under its stated default.
- OD-1 is untouched; the `N ≥ 2` denominator precheck is weaker than A2.
- OD-5 interacts with `A5(c)` (PRD-9).
- OD-6 interacts with the relation list (PRD-4).

## Validation
**Run (read-only, offline; not independent):**
- `git diff --no-index --check` between v2.5 and v2.6: no whitespace errors, only line-ending warnings.
- Cross-references: 70 unique `§` references, none unresolved. Every `RC-*`, `PRD-1…10` and `PC-1…2` is defined and referenced.
- Stale-token scan: nothing remains outside historical audit text (Appendix B).
- v2.5-to-v2.6 diff: 43 lines removed, 90 added, read in full against the scope above.
- Hash comparison with the pre-revision baseline (below).

**By inspection only:** the step-3 ordering of the domain precheck before DP4–DP6, the step-9 rows, formulas and inequalities untouched except where listed.

**Not run:** the author's v2.5 scratchpad scripts, which were not re-run. That evidence therefore stays report-only.

## Remaining blockers
- Ten pending researcher decisions and two clarifications, plus OD-1 to OD-7, block the methodology freeze and the Parameter Justification Record, which has not started.
- v2.3 to v2.6 and the reports are untracked in Git; immutability rests on hashes only.
- An independent human delta audit of v2.6 is still needed.

## Recommendation
**Blocked pending researcher decisions.** All eight required fixes of the v2.5 audit are addressed, but this is a self-check, and the candidate cannot be frozen. Methodology freeze, the PJR and main-experiment execution are not justified.

No existing file was overwritten, no frozen artifact was modified, and no commit or push occurred.
