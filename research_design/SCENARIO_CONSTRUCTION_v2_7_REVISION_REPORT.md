# Scenario Construction Specification — v2.6 → v2.7 Revision Report

**Status.** v2.7 is a candidate working draft. It implements only the Horizon A decisions the researcher approved by instruction, plus the consistency corrections they directly require. The bounded verification below was done by the same model session that wrote v2.7, so it is **not independent validation**. The methodology is not frozen, the Parameter Justification Record has not started, and no experiment was run.

**Artifacts.**
- v2.7: `research_design/SCENARIO_CONSTRUCTION_SPECIFICATION_v2_7_DRAFT.md`, 1,407 lines, 219,455 bytes, SHA-256 `d5fcffadd1045fc0c86a7c84eb8d51592d807576b6a51b712cef025164082ca8`.
- v2.6 (unchanged): SHA-256 `19f989337a8b8c9fab6a8497f36049ad8267b248c8d99bd77c56e9c92ceea425`.
- v2.3, v2.4, v2.5 and the earlier reports: unchanged.

## Decisions implemented

| ID | Decision | Implementation |
|---|---|---|
| PRD-1 | `A5(c)` = `v_hi < 1 < mi_lo` and `mi_hi < c_lo`. Not restored as hard gates: `ρ_NT < v_lo`, `p_min ≤ G_min`, `G_max ≤ p_max` | `A5(c)` (§9.6), §3.7 bullets, RC-M1 / RC-P1 / RC-P7 rows, §6.2, §17 rows 3–4. The text states that the space is still larger than under v2.3. |
| PRD-2 | `mi_hi < c_lo` stays strict, as a deliberate operational convention consistent with v2.3, not a scientific necessity. M11 and Q12 stay strict | wording in §3.7, §6.2, `A5(c)`; the M11 and Q12 rows are byte-identical to v2.6 |
| PRD-3 | Two decimals become a PJR transparency/reporting convention, not a gate | `A5(a)` no longer mentions decimals; §17 rows 3–4 and a new precision-convention paragraph (the PJR reports and reviews precision; a register is never rejected solely for more decimals) |
| PRD-9 | `A5(c)` applies separately to every declared window set (one shared set, or each family's own); no cross-family condition; OD-5 not decided | `A5(c)`, §3.7, §6.2 |
| PRD-7 | Activity D removed; pilot response content stays unread by humans in this methodology version; a later proposal needs a documented successor methodology version | §13.1 item 3, STOP-U note, §13.6.1 (D row deleted, prose rewritten, now three activities A–C), §13.9, §22 item 17 |
| PC-3 | Alternative 2: the §19.2 "Needed by" table is authoritative; step 1 requires OD-1, the Horizon A decisions, and a text valid under deferred decisions | §19.2 intro, §21.1 step 1, §19.3 |

The stale status text "OD-1 to OD-4 remain unresolved in v2.5" was replaced with an accurate statement: OD-1 to OD-7 are open at their scheduled stages, and the decided and pending PRD/PC items are named.

## Consistency corrections (directly required)

- Lineage rows 15–18, the glossary row for `PRD-#`/`PC-#`, and the §19 summary bullet ("Changed in v2.7").
- §19.3 restructured into a "decided for v2.7" table and a "still pending" table. The pending rows are byte-identical to v2.6.
- Appendix B7 added. History rows in B5 and B6 annotated, and not rewritten, where they mention activity D or "Four activities".
- One reference corrected during verification (`§22.17` → `§22 item 17`).

## Deferred items left unresolved

PRD-4, PRD-5, PRD-6, PRD-8, PRD-10, PC-1 and PC-2 are unchanged, and each is still marked pending. OD-1 to OD-7 are unchanged in the table; OD-1 is listed as a step-1 prerequisite, as instructed. No OD deadline was moved.

## Verification (one bounded pass)

- `git diff --no-index --check` v2.6 vs v2.7: no whitespace errors (only line-ending warnings); no trailing spaces or tabs.
- The v2.6 file and all 13 baseline hashes matched their pre-edit values. Baseline limitation: `runs/**` and `paper/` have no baseline hashes, so I could not hash them.
- Diff v2.6 → v2.7: 37 lines removed, 62 added. Each was traced to an approved decision or a directly required correction.
- Unchanged by diff: all `M*`, `Q*`, `DP*` rows, `A1b`–`A7` except `A5`, §12, §16–§18, and the research-question and construct text.
- Stale-wording searches: no `PENDING` marker remains on PRD-1/2/3/7/9; no live Activity D mention outside the removal statement and history rows; no two-decimal gate; no "all owner decisions before step 1" text; the old v2.5 status text is gone.
- Cross-references: 71 unique `§` references, none unresolved after the one correction above.
- The v2.5 and v2.6 scratchpad scripts were not re-run.
- Git status and HEAD are reported in the closing confirmation.

## Remaining issues

**Non-blocking, needs the researcher's attention:**
1. Step-1 prerequisite (iii) requires the text to be valid under every deferred decision. The only known rule that restricts a deferred OD is `E-EMPTY-TARGET` (with OD-4, PRD-8). Until PRD-8 is decided or made outcome-neutral, prerequisite (iii) cannot be certified. This does not block v2.7 itself.
2. Pending items (PRD-4, 5, 6, 8, 10, PC-1, 2) have no assigned deadline stage. Your instruction did not assign one, so I did not invent it. Step 1 is silent on whether they are prerequisites.
3. Appendix B6 row "Aud25-D" still says "Left pending: PRD-1 … PRD-10". That is accurate for v2.6; B7 records the v2.7 outcome.
4. The audit-history appendices (B3–B6) still use the older wording by design.

**Documentation-only:** line-ending warnings on existing files; wording of history rows.

## Recommendation

v2.7 is ready for one final human review of the approved changes. It is not ready for methodology freeze, the PJR or the main experiment.

No commit or push occurred; no existing file was overwritten.
