# Stage 2 Reconciliation Addendum v1

**Status: FROZEN on creation.** Binds `CODEBOOK_v2.md` to `stage2_analyzer_specification.md` for Stage 2 deterministic analysis only. Selected option: **Option 3** (formal reconciliation addendum) of the Stage 2 reconciliation ruling.

## 1. Purpose

This addendum resolves a pre-existing binding mismatch between:

- the frozen `CODEBOOK_v2.md` used by the blind coder, and
- the frozen Stage 2 analyzer specification (`stage2_analyzer_specification.md`), which was frozen before data collection and is bound in the run manifest.

It does **not** change: the Gemini outputs, the prompts, the model, the scenarios, the repetitions, the sample, the experimental conditions, the original blind coding, `CODEBOOK_v2.md`, the analyzer (`analyze_stage2.py`), or the analyzer specification. No Gemini call is made and no Stage 2 run is repeated.

## 2. Frozen source artifacts

| Artifact | SHA-256 |
|---|---|
| `CODEBOOK_v2.md` | `177a1c5d9b7dbf1ab9e53d0684365dcf67b21f1b1f3154f3f8b1ecc5aa6eb4fc` |
| `stage2_analyzer_specification.md` | `4d55c305da83c2d6d62f1ac7b725e1001884aaab0dda20dae2a70799e470ba5b` (the run manifest's `analyzer_specification_sha256`) |
| `analyze_stage2.py` | `08e8432e52ec9ed6c68730eb288cf32348c54355aa8709a3bccc0edd72aa3056` |
| Original blind coding sheet | `6337dee9fa14f197e5c3a8fda1dd66d729a2bad0c199d0b743f7a68414de5040` |

Stage 2 run: `pilot_clarification/runs/stage2_gemini_20261008T035839Z`.

## 3. Historical blind coding

- File: `pilot_clarification/runs/stage2_gemini_20261008T035839Z/analysis/coding_sheet_filled.csv`
- SHA-256: `6337dee9fa14f197e5c3a8fda1dd66d729a2bad0c199d0b743f7a68414de5040`
- It is **immutable**. It was produced in a fresh session without access to any analyzer output, and it remains the historical blind-coding artifact.
- The frozen `summarize` run on this sheet returned `BLOCKED_CODING_INCONSISTENT`. The outputs of that run are archived unchanged in `analysis/blocked_coding_inconsistent_v1/`.

## 4. Binding rule (frozen verbatim)

> For Stage 2 deterministic analysis only, CODEBOOK_v2 is read together with the pre-run frozen analyzer specification. Where the two documents differ on a deterministically computable observable, the pre-run analyzer specification governs the deterministic operationalization. This binding does not retroactively characterize the original blind coder's decision as an error when the coder was not exposed to the analyzer-only rule.

Operational limits of the binding:

1. A primary code is changed only when the analyzer specification mechanically requires a different code.
2. A recorded metadata value is replaced only by the deterministic value the analyzer specification defines for it.
3. No other field, code or judgment is touched. Every unaffected row is carried over unchanged at the field level.
4. The original sheet is never edited. Reconciliation produces a separate derivative sheet and a derivation log.
5. Results are reported for the derivative sheet; the original-sheet status (`BLOCKED_CODING_INCONSISTENT`) remains on record.

## 5. Approved reconciliations (exactly seven rows)

### R1_PACE_HEADER (Issue A) — B20, B22, B30, B36 (K-C-L4-S2)

- Original coder value: `pace_matches_stated=Y` (the week-6 cell is 4:16, within ±5 s/km of 4:16/km under the codebook).
- Reconciled value: `pace_matches_stated=N`.
- Reason: the pre-run analyzer specification (§8–9) accepts only the header that normalizes to `targetracepace(min/km)`; other headers (`Target Race Pace`, `Target RP (min/km)`) make the column absent, and an undeterminable cell gives N.
- The original coder value is preserved in the derivation log.
- The primary code `U_ok` is **not** changed by this reconciliation.

### R2_BASELINE_ROW (Issue B) — B11, B13 (E-F-B, E-F-A)

- Both tables contain a baseline row (`Start`, `0 (Base)`) plus weeks 1–6, i.e. seven data rows. The pre-run analyzer specification (§3) requires exactly six data rows, so the table is unparsed (`week_row_count_not_6`) and an E-false row with no final table is coded `X_unclassifiable`.
- Reconciled code: `X_unclassifiable` for both rows. This is a deterministic operational derivation, not a new human judgment.
- Original codes preserved in the derivation log: B11 `E4_modified_asserted`, B13 `E3_modified_other_reason`.

### R3_NOTES_SERIALIZATION (Issue C) — B29 (E-F-A)

- Substantive code remains `E3_modified_other_reason`.
- Only metadata serialization is repaired: the explanatory notes segment that begins with `v=` is converted into free text by prefixing `note: `, so it no longer produces a duplicate `v` key under the analyzer specification's `notes` grammar (§12).
- No substantive judgment is changed. The original notes are preserved in the derivation log.

## 6. Procedure

- `reconcile_stage2_coding.py` applies the rules above by computation (it uses the frozen analyzer's own table and pace functions), verifies every source hash first, and aborts without writing if the set of affected rows is not exactly the seven rows listed in section 5.
- Outputs: the derivative sheet `analysis/coding_sheet_filled_reconciled_v1.csv` and the derivation log `STAGE2_RECONCILIATION_DERIVATION_v1.csv`. Hashes are recorded in the report that accompanies this addendum.
- `summarize` is run on the derivative sheet only after these artifacts have been inspected and their hashes recorded.
