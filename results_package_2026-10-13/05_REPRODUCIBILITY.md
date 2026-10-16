# Reproducibility package

Everything below is read-only: no step makes a model call, needs an API key, or writes into `pilot_clarification/` or `research_design/`.

## 1. Re-verify the stored evidence (60 hash checks)

```powershell
cd "D:\research s2"
python -B -I results_package_2026-10-13\reproduce\verify_stage_evidence.py
```
Expected: `stage2 postrun: COMPLETE 40 {'ok': 40} {'STOP': 40} ['gemini-3.1-flash-lite']`, `stage1 successful run calls: 30 with response_text: 30 errors: 0`, `stage1 first (failed) run calls: 30 errors: 30`, `hash checks: 60 problems: 0`. Result on 2026-10-13: exactly this.

## 2. Recompute the Stage 2 headline counts without the project analyzer

```powershell
cd "D:\research s2\pilot_clarification\runs\stage2_gemini_20261008T035839Z"
python -B -I "D:\research s2\results_package_2026-10-13\reproduce\recompute_stage2.py" .
```
Expected (reconciled sheet): E_fail 4, T1_pass 10, X_E 2, C_fail 9, C_types 2, X_C 0, U_fp 0, X_U 0, gate 2 true. Original sheet (sensitivity): E_fail 5, X_E 0.

## 3. Re-run the project's own tests (no network, bytecode disabled)

```powershell
cd "D:\research s2"
python -B -I -W error::ResourceWarning -m unittest discover -s research_design/step7 -p test_step7.py   # Ran 145 tests, OK
python -B -I -m unittest discover -s research_design/implementation_a -p test_impl_a.py                 # Ran 123 tests, OK
```
Both were run on 2026-10-13 with these results. `-B` keeps the run from writing `.pyc` files.

## 4. Where the raw data and provenance are

| Item | Path |
|---|---|
| Stage 1 raw responses, calls, manifest | `pilot_clarification/runs/stage1_gemini_20261007T080948Z/` |
| Failed first Stage 1 attempt | `pilot_clarification/runs/stage1_gemini_20261007T070917Z/` |
| Stage 2 raw responses, calls, manifest, integrity | `pilot_clarification/runs/stage2_gemini_20261008T035839Z/` |
| Stage 2 coding, extraction, decision | `.../analysis/` (hashes in `analysis_manifest.json`) |
| Frozen Stage 2 specifications and codebook | `pilot_clarification/*.md`, `CODEBOOK_v2.md`, `analyze_stage2.py` |
| v2.7 specification, FZ-v1, decision record, Step 7 drafts | `research_design/` |

Re-calling the model will not reproduce the responses (provider default decoding, no model snapshot). The reproducible part is the computation from the stored raw records to the counts.
