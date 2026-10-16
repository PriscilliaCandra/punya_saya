# Operations runbook (commands verified against the argparse of each tool on 2026-10-13)

Run from `D:\research s2`. `BUILD` = `research_design/step8_output/step8_build_7a6bbe465c66`. Paths in angle brackets are new files or folders you choose; the tools refuse to overwrite.

## 1. Local checks (read-only, no network)
```
python -B -I results_package_2026-10-13/reproduce/run_all_checks.py --quick      # about 1 minute; omit --quick to include the slow Step 8 suite (about 3 minutes)
python -B -I research_design/step8/s8_verify.py BUILD                              # independent verifier of the build
python -B -I research_design/step9/impl_b.py BUILD                                 # Implementation B
```
(the checker prints "gate status ... exit=2 OK" because the gate is supposed to be closed now).

## 2. Check the gate without opening it
```
python -B -I research_design/step10/s10_runner.py --scope pilot_round_1 --build BUILD --out <unused folder> --evidence <step9_evidence.json> --authorization <authorization.json>
```
Without `--live` the command only checks and never calls anything (since the pre-pilot fix it also prints a network-free local preflight line: whether the API key variable is present and the settings are usable, never the key): it prints `GATE CLOSED:` with every reason (exit 2) or `gates open; --live not given: nothing was run` (exit 0). Current reasons: Step 9 evidence file missing, authorization not valid. The gate also requires: a clean verifier and Implementation B agreement on the build, blind-check delay at least 7 days, 100 % coverage, worksheet hash, adjudication AGREE or ADJUDICATED_NO_REJECT, the evidence file naming this build, and an authorization with `authorized_by` = `owner`, the exact scope and call count (18, 18 or 2496), cost ceiling 100 and the input-size assumption (hard-cap cost below US$100). Main scope additionally needs `--pilot-record` (a final pilot decision with `final_decision` PASS whose call-list hash matches the build).

## 3. What a pilot round needs saved (all of it, unedited)
The run folder (`raw/`, `calls.jsonl`, `ledger.jsonl`, the `RUN_COMPLETE`/`RUN_INCOMPLETE` marker), the evidence and authorization files, the build manifest hash, the integrity output, the pilot report, the decision record and its `.runlog`. **Do not open `raw/` or `calls.jsonl` for a pilot** (13.6.1 activity B): use the tools below, which print counts only.

## 4. After a pilot run (not before the gate is open and the run exists)
```
python -B -I research_design/step10/s10_integrity.py --run <run folder> --build BUILD
python -B -I research_design/step10/s11_pilot.py report --run <run folder> --round 1 --out <new report.json>
python -B -I research_design/step10/s11_pilot.py decide --run <run folder> --round 1 --fz-hash <64 hex> --record <new decision_record.json>
```
`decide` writes a record only for a final decision. Exit codes: 0 record written, 3 not final (round-1 FAIL-S), 4 record exists, 2 invalid input. The `--fz-hash` is recorded as "researcher-supplied, unverified" (P-2 open). The decision record must be anchored in a write-once store before an order is generated (§10, PRD-6): the owner declares the store.

## 5. Protocol outcomes (§13.6, §13.8)
- **Round 1 PASS:** decision record with `PASS` (step 11); `python -B -I research_design/step10/s11_final_freeze_manifest.py --decision-record <record> --out <new manifest.json>`; the main run follows with `--scope main --pilot-record <record>`.
- **Round 1 FAIL-S:** `decide` exits 3. The researcher either makes one whitelisted change that addresses the failure type (SF1: timeout, delay or retries; SF3: max output tokens; SF2/SF5: a pure implementation fix; SF4: none, STOP) as a new FZ version and then runs round 2, or STOPs. The runner's expected settings are fixed, so a whitelisted settings change needs a code update and a new FZ version first.
- **Round 2 FAIL-S:** `decide --round 2` writes `STOP`.
- **FAIL-U (any round):** `STOP-U`; no re-pilot; escalate to the advisor.
- **Main run:** halts by itself at 5 consecutive structural failures, or when the cumulative share exceeds 0.10 after 100 completed calls (FZ-v1 row 18); the folder is marked `RUN_INCOMPLETE`. Resume after a transport-only halt is not implemented; do not re-run into the same folder (it is refused) and do not replace calls.
- **After the main run:** `python -B -I research_design/step10/s10_integrity.py ...`, then `python -B -I research_design/step10/s10_report.py --run <run> --build BUILD --decision-record <record> --out <new folder>`.
- **Coding preparation:** `python -B -I research_design/step10/s12_cli.py prepare --run <run> --build BUILD --analysis <report folder> --out <new coding folder>`; later `tabulate --prepared <coding folder> --run <run> --sheet <filled csv> --out <new json>` and `recode --prepared <coding folder> --first <csv> --second <csv> --out <new json>`. It takes minutes for 2,496 items. A `PG11B_FAILED` result means coding waits (§8.2).

## 6. Stopping safely
- If any gate reason appears, stop: nothing was created. Do not edit the gate or the evidence to pass it.
- Stop a running pilot or main run with Ctrl+C only if unavoidable: records written so far stay; there is no status marker, so the folder is not a valid run (`s10_integrity` reports "not exactly one status marker"); it cannot be resumed or reused, and a pilot round is consumed (cap 2, 13.6). Prefer to prevent a start: run section 2 first, the runner now refuses to start (exit 2, nothing created, no round consumed) when the API key or the settings are not usable.
- Never delete or overwrite run folders, decision records or the evidence file.
