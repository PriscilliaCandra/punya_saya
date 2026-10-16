# Pilot and main run: operations checklist (2026-10-14; supplements `OPERATIONS_RUNBOOK.md`, does not replace it)

**UPDATE 2026-10-14 (later the same day): the local changes in section 7 were made on the owner's instruction (provenance entry, fail-closed resume module, integrity diagnosis, cost stop). The table in section 1 describes the behaviour BEFORE those changes; section 7 states what changed. MD-08 is still not adopted.**

Status: PREPARATION ONLY. Nothing here opens a gate, authorises a call or records R1. Facts below were read from `research_design/step10/s10_runner.py`, `s10_integrity.py`, `s10_scoring.py`, the FZ-v1 register, spec 13.8 and the tests named in the last section. Items marked **[recommendation]** are operating practice proposed by the assistant, not protocol. Items marked **[owner]** need the owner's own action or written authorisation.

## 1. What the code does and does not do (verified)
| Topic | Verified behaviour |
|---|---|
| Call identity | `call_key` = `template,condition,repetition`, stable; the order is the canonical list (pilot: `pilot_calls.txt`; main: shuffled once with the seed in the pilot decision record, list hash must match). |
| Per-call persistence | Order per call: ledger `intent` -> provider call -> raw file written (`xb`) -> ledger `raw` (hash) -> `calls.jsonl` line -> ledger `classified`. Hash-chained ledger; files are flushed to the operating system, not `fsync`ed. |
| Recorded per call | call key and index, UTC start, HTTP status, error class, response text, finish reason, returned model, block reason, usage metadata, latency (the provider's figure, else wall clock), prompt SHA-256. **Not recorded per call:** end time, requested model, cost. |
| Recorded once, at the END | settings, build manifest hash, input-size check, ledger final hash (run summary / status marker). **A killed run never writes them.** The ledger has no start entry naming the build, the authorisation or the settings. |
| Failures | Exceptions and transport errors are caught per call, recorded with the error class, classified (SF1 etc.), and the run continues. Retries are 0. A failed call is never repeated, replaced or re-drawn. |
| Halt (main scope only) | `RUN_INCOMPLETE` with a valid marker when 5 consecutive structural failures occur (`c_stop`), or when, after 100 calls, structural failures exceed 10% of completed calls. The folder is then valid and can be reported as incomplete (spec 13.8). |
| Kill, crash, Ctrl+C, power loss | Not caught. No status marker is written. `s10_integrity` answers "not exactly one status marker"; the folder cannot be re-entered (FileExistsError) and cannot be reported as a run. |
| Resume | **Not implemented.** Spec 13.8 allows a resume of a transport-only (SF1) interruption under the identical FZ version at the next `call_index`; patch P8 / MD-08 is HELD. Open points: who authorises, what "transport-only" means, whether the 5-in-a-row counter carries over, and what happens to a last call with an `intent` and no `raw`. |
| Restart in a new folder | Possible but it re-issues every call already made (28 provider invocations for 18 planned in the simulation). Nothing links it to the killed folder; whether that is allowed is not decided. |
| Cost | The gate computes a worst-case bound, `slots x (assumed input tokens x 0.30 + 8192 x 2.50) / 10^6` (US$51.88 for 2,496 slots at 1,016; US$0.37 for 18). Prices are constants in the code. **Nothing stops a run on actual spend**; `s10_integrity` computes observed cost afterwards and reports a problem at US$100. |
| Slow call / sleeping computer | A call that takes 400 s is recorded with its latency and counted by `s10_integrity` (`calls_with_latency_over_nominal_timeout_180s`); it is not a problem and does not stop the run. The 180 s timeout applies to each socket operation, not to a whole request. |
| Damaged files after the run | A truncated last line of `calls.jsonl` or `ledger.jsonl`, or a deleted raw file, make `s10_integrity.verify_run` RAISE (an exception) instead of printing a PROBLEM line. It still fails closed (never "OK"). An extra raw file or a missing marker is reported as a problem. |

## 2. Preflight (before any `--live`)
Mechanical (assistant can run; none of it calls a provider):
- [ ] `python -B -I research_design/step10/s10_runner.py --scope <scope> --build <BUILD> --out <unused> --evidence <...> --authorization <...>` prints `gates open; --live not given` and `local preflight: OK` (key present, settings usable; the key is never printed).
- [ ] `run_all_checks.py` (full, including the slow Step 8 suite) is as expected on the day; the three Step 7/8 hash comparisons show no drift.
- [ ] The output folder does not exist yet; the disk has room for about 2,500 raw files plus ledger (a few tens of MB at most).
- [ ] Call plan reconciliation: planned calls equal the authorised `max_calls` (18, or 2,496); for main, the call-list hash equals the pilot decision record.

Owner actions **[owner]**:
- [ ] Authorisation file written by the owner for exactly that scope, with `max_calls`, `cost_ceiling_usd`, `input_tokens_per_call_assumed`, `max_input_characters` (MD-02).
- [ ] Prices and model identifier re-read on the run date (B7); if the provider's prices differ from the constants in the code, the worst-case bound is wrong and must be recomputed before the run.
- [ ] API key present in the environment of the terminal that will run it (never in a file in the repository).
- [ ] Decision on resume (MD-08 / A3), or a written acceptance that an interruption ends the run as incomplete or forces a restart in a new folder.
- [ ] Written decision on what is done with a restart in a new folder (allowed or not).

Machine practice **[recommendation]** (not enforced by any code): disable sleep and hibernation, plug in power, use a wired or stable network, run in a terminal that will not be closed, no automatic updates or restarts during the run, one run at a time.

## 3. During a run
- The runner prints nothing per call. Progress can be read without opening response content: the number of files in `raw/` (call count) and the size of `ledger.jsonl`. **Do not open `raw/` or `calls.jsonl` for a pilot (13.6.1) and do not read response text for the main run (13.8).**
- Expected pace from the earlier pilot-clarification runs (different model and task): about 4 to 5.5 hours for 2,496 calls (mean latency 4.9 to 6.9 s plus the 1 s delay). Treat as a rough guide only.
- Do not close the terminal, do not put the computer to sleep, do not start a second run.

## 4. When something goes wrong (decision table)
| Event | What the code does | Allowed next step |
|---|---|---|
| Single failed call | Recorded as SF; the run continues | none; never repeat or replace it |
| 5 consecutive structural failures (for example a network drop of about 5 s, if each call then fails at once; **assumption, not measured**) | Main halts: `RUN_INCOMPLETE`, valid folder | Report as incomplete (spec 13.8). Resume only after the owner/advisor decision on P8 and only under the same FZ version |
| SF share above 10% after 100 calls | Main halts | as above; a truncation spike (SF3) after the change window closes terminates the run as incomplete |
| Process killed, Ctrl+C, crash, power loss | No marker; folder is not a valid run | Do not edit or complete the folder by hand. Preserve it. Owner decision needed (see section 2) before anything is started again; a pilot round is consumed |
| Gate reason appears | nothing is created | stop; do not edit the gate or the evidence |

## 5. After a run: reconciliation and verification
1. `s10_integrity.py --run <run> --build <BUILD>`: exit 0, one marker, `recorded` equals planned for a COMPLETE run, `provider_checks` read (returned model equals the requested one, unlisted finish reasons, records without status, block reasons), observed cost below the authorised ceiling.
2. Reconcile counts: calls in `calls.jsonl` = files in `raw/` = `recorded_calls` in the marker = `classified` entries in the ledger; call keys unique; no key outside the plan.
3. Keep unedited: the run folder, evidence and authorisation files, build manifest hash, integrity output, pilot report and decision record.
4. Pilot: `s11_pilot.py report` then `decide` (counts only, no verdict agreement, 13.7). Main: `s10_report.py` produces the call table and the analysis from the stored records; the primary analysis hash is recorded before `s12_cli.py prepare` (coding).
5. Any damaged-file exception from the integrity tool counts as "not verified", not as "ok".

## 6. Simulations that exist (mock provider only, no network)
`test_ledger_resilience.py` (11 tests: interrupted run, chain breaks, duplicates), `test_pilot_flow.py`, `test_step10.py` (full mock main run of 2,496 calls, halt rule), and the new `test_disruption_scenarios.py` (10 tests: burst of transport failures, eight anomalous response types, a 400 s stall, kill and restart, damaged run files). The 139 tests of `research_design/step10` passed on 2026-10-14.

## 7. Changes made on 2026-10-14 (local, mock-provider tests only; nothing run live; gate still closed)
| Topic | Before | Now |
|---|---|---|
| Provenance | none until the end-of-run summary | first ledger entry `start` (format 2) before any provider call: run id, scope, build manifest hash, FZ-v1 file hash, evidence hash, authorization hash and content, pilot record hash, call-list hash, settings, provider class, code hashes, Python version; no secret |
| Resume | not implemented | `s10_resume.py`, fail-closed (see its docstring): same run folder, append-only, one hash chain; refuses on any mismatch of build, FZ file, evidence, authorization, settings, call list or provider class; never repeats a call with a persisted record; a late-written ledger/calls entry for a persisted record is appended as `reconcile`; counters are rebuilt, never reset; needs a separate owner-written resume authorization bound to the exact ledger head |
| Intent without a persisted record | run unusable | resume REFUSED; no disposition is implemented (MD-08 point 2 undecided) |
| Halt by HTTP status error, unlisted exception class, cost stop, or a COMPLETE run | n/a | not resumable |
| Stop without a status marker | folder unusable | resumable only with `process_interruption` + `acknowledges_unspecified_basis` written by the owner (spec 13.8 names only transport failure; interpretation is the owner's) |
| `s10_integrity` on damaged files | raised an exception | explicit PROBLEM lines for truncated or invalid lines, missing or unreadable files, missing provenance in a format 2 run, resume/segment inconsistencies |
| Cost | worst-case bound at the gate only | additionally, an observed-cost stop at the OD-10 limit (lower bound from recorded usage; halts the run as RUN_INCOMPLETE). Because the gate bound is far below the limit it can only fire if the provider bills more tokens than the bound assumes. **Whether a new halt cause is acceptable for the protocol is an owner decision; revert by removing the `limit_usd` check in `s10_runner.drive`.** |
| Tests | 139 in step10 | 163 (new: `test_resume.py` 22, `test_disruption_scenarios.py` 12; two older tests that pinned the old format or the absence of resume were updated) |
