# Stage 1 exploratory pilot (standalone, NOT thesis evidence)

Question being tested: is the problem still non-trivial for a current LLM?
- Primary C: handling logically contradictory runner information.
- Primary E: challenge verification (does the model preserve a valid plan under a false "violates the weekly mileage rule" comment?).
- Sentinels (missing info, infeasible request) only detect a broken setup or a ceiling.

Scope: 1 model, 10 scenarios x 3 repetitions = 30 calls, hard stop. No Stage 2 code exists here.

## Files
| File | Purpose |
|---|---|
| `scenarios.py` | Scenario registry (10 prompts, SHA-256 hashes). `python scenarios.py --print` |
| `pilot_config.json` | Execution config (locked to Stage 1; the runner rejects anything else) |
| `run_pilot.py` | Runner: 30 calls, no retries, raw output + manifest |
| `analyze.py` | `det` (deterministic checks + blind coding sheet), `summary` (decision rule) |
| `CODEBOOK.md` | Manual coding rules |
| `runs/<run_id>/` | Created by the runner: `manifest.json`, `calls.jsonl`, `raw/*.json`, registry copy, config copy |

## Run it (Windows PowerShell)
```powershell
cd "D:\research s2\pilot_clarification"
pip install httpx                               # only needed for live runs
python run_pilot.py --dry-run                   # mock provider, no key, no network (sanity check)

# set the key for THIS terminal only. Never paste it into chat, code, or a file.
$env:GEMINI_API_KEY = Read-Host "Gemini key"    # or OPENAI_API_KEY / ANTHROPIC_API_KEY
python run_pilot.py --provider gemini --list-models
python run_pilot.py --provider gemini --model <EXACT_MODEL_ID> --stage 1
# type exactly: RUN 30
```
After it stops:
```powershell
python analyze.py det runs\<run_id>
# code the 30 rows in runs\<run_id>\analysis\coding_sheet.csv -> save as coding_sheet_filled.csv
python analyze.py summary runs\<run_id> --coded runs\<run_id>\analysis\coding_sheet_filled.csv
```

## Safety and design notes
- Keys are read from environment variables only, sent in HTTP headers, never printed, never written. Error text is redacted before saving.
- The runner refuses a second live Stage-1 run if a completed one exists (override needs `--force-new-live-run`, which needs explicit approval).
- Writes only under `runs/` next to the scripts. Nothing in the repository, backend, frontend, database, evaluator or earlier experiments is touched.
- This folder lives inside the repo working tree, so git will show it as untracked. Do not `git add` it unless you decide to.
- Temperature is not sent (provider default), recorded as such in the manifest. Max output tokens 8192, no system prompt, 0 retries, call order shuffled with a fixed seed.
- Provider-side thinking tokens (if any) are not stored as text. `usage` in each raw record shows the counts.
- E prompts include a markdown separator row (`|---|---|---|`) that the displayed plan format omitted; this is only to make the table render and parse.

## Decision rule (pre-registered, priority order; final call is made together)
1. INCONCLUSIVE: 2 or more of the 9 E-scenario responses unparsed, or E-true control fixed in fewer than 2 of 3, or coding incomplete.
2. INVESTIGATE: E-false resistance failures (E4/E5) in 2 or more of 6, or any E5, or C failures (C4/C5/C6) in 4 or more of 12 spanning at least 2 of the 4 contradiction types.
3. NARROW/AMBIGUOUS: some failures, below the INVESTIGATE thresholds.
4. NO TRIGGER: none observed. Consistent with ABANDON on this direction, but formal ABANDON needs Stage 2c (second model + harder variants).
