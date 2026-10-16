# Pre-pilot runner fixes: report (2026-10-13)

No live API call, pilot or main run was made. No frozen artefact changed (checked at the end: specification `d5fcffad...`, Step 7 freeze manifest `202979de...`, Step 8 build manifest `09eed00e...`, FZ-v1 file `14944571...`). Git status differs from the earlier baseline only by the untracked `results_package_2026-10-13/` folder. Backups of every edited tested file are in `results_package_2026-10-13/_backup/prepilot_fix/`.

## 1. Findings and what was done
| Task | Finding | Result |
|---|---|---|
| 1 Preflight | The runner created the output folder, the ledger and one failed record per call before noticing a missing key (all calls SF1, a pilot round consumed). | **FIXED.** `run()` validates the register settings (all seven fields present, typed, retries 0, concurrency 1) and asks the provider to preflight (key variable present and non-blank, model ID equals the register's, https endpoint host) before any folder exists. Failure raises `PreflightFailed`; on the command line `--live` prints the reasons and exits 2; without `--live` a "local preflight (no network)" line is printed. Reasons name the variable, never the value. The ledger order (intent, raw, classified) and the gate are untouched. |
| 2 Tokens and cost | `s10_integrity` used `candidatesTokenCount` only. Thinking tokens are billed as output and count against the 8192 limit (FZ-v1 model verification, 12.11 OD-9). The provider's exact reporting convention is unknown. | **FIXED in the accounting tool, no schema change** (usage is stored verbatim). Output tokens = total - prompt when both exist (correct whether or not candidates already include thinking tokens, so nothing is counted twice); else candidates + thoughts; else candidates; otherwise "unavailable". Calls with incomplete usage are counted and the cost is flagged as a lower bound. **UNVERIFIED:** whether the live API reports `thoughtsTokenCount` or how `totalTokenCount` is composed; no price or usage was invented. |
| 3 Latency, timeout | `GeminiProvider` returned no latency. The 180 s `urllib` timeout is per socket operation. | **Latency FIXED**: wall-clock around the provider call, the provider's own figure wins; the schema field `latency_ms` already existed. **Timeout NOT changed** (frozen value unchanged, behaviour unchanged): the run summary now states "per socket operation, NO total deadline", and the integrity tool flags calls with recorded latency above 180 s. **Owner decision needed:** whether 180 s must be a total deadline (changing behaviour needs its own test and a FZ read). |
| 4 Resume | Not implemented, see section 4. | **WAITING_FOR_ADVISOR** |
| 5 Step 12 CLI | Not a pilot blocker (coding happens after the main run). | Added anyway as a thin wrapper `s12_cli.py` (`prepare`, `tabulate`, `recode`); it calls the tested functions unchanged and writes new files only. |

## 2. Files
Changed: `research_design/step10/s10_runner.py`, `research_design/step10/s10_integrity.py`, `research_design/step10/test_s12.py` (two CLI tests appended), `results_package_2026-10-13/` documents `PROVIDER_STATIC_AUDIT.md`, `NEXT_ACTIONS.md`, `OPERATIONS_RUNBOOK.md`, `reproduce/run_all_checks.py`, decision record entries 12.34 and 12.35 (appended).
New: `research_design/step10/test_prepilot_fixes.py`, `research_design/step10/s12_cli.py`, this report.

## 3. Tests (mock providers, synthetic data, no network)
| Suite | Result |
|---|---|
| `test_prepilot_fixes.py` (new): missing/blank key, model mismatch without printing the key, incomplete or invalid settings, provider preflight failure leaves the folder free and the same folder then runs, CLI `--live` without key creates nothing and calls nothing, CLI without `--live` never prints the key, token variants (with/without thoughts, incomplete, inconsistent), integrity lower-bound, latency measured vs provider-given, timeout statement, slow call flagged | 11 tests OK, exit 0 |
| `test_s12.py` (CLI tests added) | 11 tests OK, exit 0 |
| `test_step10.py`, `test_pilot_flow.py` (relevance: runner and integrity changed) | 18 and 8 tests OK |
| `run_all_checks.py --quick` (includes the Step 7, 4, 8 verifier, B, blind-check suites) | all as expected; gate status still CLOSED (exit 2) |
The slow Step 8 suite was not re-run: nothing it covers changed.

## 4. Resume after a transport halt (13.8): why it is not implemented
Text: "A run interrupted by transport failure resumes only under the identical FZ version (plus any pure implementation fix under H1-H4), continuing at the next `call_index` of the same frozen order (no re-draw)"; "failed calls are not selectively re-run; no completed call is replaced or discarded; no call is silently substituted"; a transport-only halt (SF1) "may resume".
Unclear points that a tool would have to decide: (1) whether the halt rule counters (consecutive failures, cumulative share, `calls_min_main`) restart on resume or carry over (carrying over can halt again at once; restarting is a new rule); (2) what "next `call_index`" means when the last ledger entry is an intent without a raw record (the call may or may not have reached the provider; repeating it risks a duplicate, skipping it leaves a gap: the "attempted, no record" case of the Policy 2 package, section 5.1); (3) what counts as "transport-only" (all halting failures SF1, or SF1 at the moment of halt); (4) who authorizes a resume and how it is logged (a human decision event, the scope of the authorization, the cost ceiling for the remaining calls); (5) the delay between the last call of the halted process and the first of the resumed one.
Options for the advisor: (a) no tool; a resume is a new documented human decision and a new run folder is not allowed to reuse indices (current behaviour: the folder is refused); (b) a resume tool that continues at the next index after the last classified entry, with counters carried over, and refuses when the last entry is an unresolved intent; (c) as (b) with counters restarted. Any of these needs a written decision before code; none was written.

## 5. Remaining risks and open decisions
- Live-API facts not verified: request field names, finish-reason vocabulary, thought parts, usage fields, returned model ID.
- Unknown finish reasons other than `MAX_TOKENS` and the listed block reasons are scored as ordinary responses.
- No stop rule if the returned model ID differs from the requested one (it is recorded and listed by the integrity tool).
- Timeout total-deadline decision (owner).
- All earlier gate reasons remain: no Step 9 evidence file, no valid owner authorization; advisor items in `ADVISOR_DECISION_BRIEF.md` unchanged.

Passing local tests do not make the research ready for the pilot. Gate status: CLOSED (evidence file missing; authorization missing or invalid).
