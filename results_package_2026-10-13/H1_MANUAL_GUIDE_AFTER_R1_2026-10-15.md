# H1 manual guide (after R1), prepared 2026-10-15

Preparation only. Written from `HUMAN_TASK_GUIDE.md` Part 1, `step9_blind_check_kit/README.md`, the blank worksheet header, and `s10_runner.py check_gates`. The assistant opened NO registry, prompt table, prompts, gate report, checker mapping, pilot folder, checker_bundle file or run output for this guide. The assistant fills no row and judges no row.

## 0. Clock facts (verified from the R1 file, read-only)

- R1 file: `results_package_2026-10-13/human_evidence/clock/last_registry_view_utc.txt`, line 1 `2026-10-15T07:50:10Z`, line 2 the required sentence (sha256 `3671da75e31e35fe349faef5715984859884d90a06e23c0b3d002997b91d1a0c`). It has a UTF-8 BOM and CRLF line ends (Windows PowerShell 5.1 `Set-Content -Encoding utf8`); no tool reads this file, the date is passed on the command line, so this is harmless. Do not edit or re-create the file.
- Gate rule (`s10_runner.py` line 133): `(completed_utc - last_registry_view_utc).days >= 7` (floor of whole days; `minimum_delay_days` = 7 from FZ-v1 row 19).
- **Earliest valid `--completed-utc`: `2026-10-22T07:50:10Z`.** Anything earlier gives "blind-check delay N days < 7" and the gate stays CLOSED. The completion date must be true: the day you actually finish the last row, not a date chosen to pass.
- Working on the rows BEFORE that date is allowed (the clock only needs no registry/expected-state viewing); only the `--completed-utc` you declare must be at least the date above and true.

## 1. Allowed and forbidden files

Allowed: the 624 files in `research_design/step8_output/step8_build_7a6bbe465c66/main/checker_bundle/` (one at a time), the blank worksheet, your own filled copy, the guide.
Forbidden until all rows are done (opening restarts the clock and, for the first two, breaks blinding): `main/checker_mapping_HELD_SEPARATELY.json`, `main/registry.json`, `main/prompt_table.json`, `main/prompts/`, `main/gate_report.json`, the `pilot/` folder, any run/analysis output, and chat/report passages that show rendered prompts or expected states.

## 2. Setup (commands run by you; they only copy and validate)

Work from `D:\research s2`. Copy the blank (never edit it):

```powershell
Copy-Item "results_package_2026-10-13\step9_blind_check_kit\blind_check_worksheet_MAIN_blank.csv" "results_package_2026-10-13\human_evidence\blind_check_filled_<initials>.csv"
```

The copy is NEW work product (one human, OD-3). Fill it in a spreadsheet program; save as CSV (UTF-8). Keep a dated backup copy before big edits if you want, but never edit rows after seeing the evaluator's verdict.

## 3. The 40 columns (header of the blank, in order)

`opaque_id`, `date_first_seen_registry_content_or_expected_states_UTC`, `date_of_this_check_UTC`, `family_read_from_text` (optional, MIL or PAC), `P_or_D_dist`, `T_time_displayed`, `T_time_seconds`, `tau_F`, then for each week w1..w5: `wN_transcribed`, `wN_value`, `wN_increase_km_or_implied_finish_s_2dp`, `wN_limit_km_2dp_or_rounded_finish_s`, `wN_percent_2dp_or_diff_s`, `wN_status`; then `verdict_satisfied_violated_unclear`, `notes`. (The date columns are optional for the evidence file, which takes the two dates from the command line.)

## 4. Rules per row (from `HUMAN_TASK_GUIDE.md` Part 1; all entries required)

**MIL file** (text starts "Constraint (weekly mileage cap)"): `P_or_D_dist` = cap percent as displayed (e.g. `10%`). Leave `T_time_*` and `tau_F` empty only as the guide allows (check with the precheck). Weeks 1-5: `wN_transcribed` = displayed total (trailing `km` allowed), `wN_value` = same total in km. Week 1: status `uncompared`, three computed columns empty. Weeks 2-5: increase (km, >= 1 decimal) = this week minus previous; limit = P % of the previous week (km, >= 2 decimals); percent increase = increase / previous x 100 (>= 2 decimals); status `over cap` only if the percent is strictly above P, else `not over cap`. Verdict `violated` if any week is over cap, else `satisfied`.

**PAC file** (text starts "Constraint (race pace consistency)"): `P_or_D_dist` = distance as displayed (e.g. `10 km`), `T_time_displayed`, `T_time_seconds`, `tau_F` (`50` or `50 sec`). Weeks: `wN_transcribed` = pace as displayed (`5:11`, `min/km` allowed), `wN_value` = seconds per km; first computed column = distance x pace in seconds (>= 2 decimals); second = that value rounded to the nearest whole second, half rounds UP; third = rounded value minus target time (integer); status `|e|>tau` if the absolute value is strictly more than tau, else `not`. Verdict `violated` if any week is `|e|>tau`, else `satisfied`.

Verdict words only: `satisfied`, `violated`, `unclear`. Rounding coarser than the floors is a logged checker error. An empty required cell or another verdict word can lead to a build rejection. Use a calculator or a spreadsheet formula YOU write; do not use a model to fill or judge rows.

## 5. Order of operations

1. Fill all 624 rows from the checker_bundle files only (the row `opaque_id` = the file name). Do not open the mapping.
2. Precheck BEFORE evaluating (reads only your sheet and the blank; prints row ids and column names only; exit 0 when nothing is empty or malformed):

```bash
python -B -I results_package_2026-10-13/reproduce/precheck_human_sheets.py --kind blindcheck --sheet results_package_2026-10-13/human_evidence/blind_check_filled_<initials>.csv
```

3. Fix empty or malformed cells now, never after an evaluation.
4. Evaluate (writes a NEW file; read `build_verdict`; `NO REJECT` required, coverage 100 %):

```bash
python -B -I research_design/step9/s9_blindcheck.py --sheet results_package_2026-10-13/human_evidence/blind_check_filled_<initials>.csv --bundle research_design/step8_output/step8_build_7a6bbe465c66/main/checker_bundle --evaluation-out results_package_2026-10-13/human_evidence/blind_check_evaluation_1.json
```

5. If the verdict is REJECT: stop; do not edit rows to change the outcome. Under 12.50 there is no advisor; the owner decides the next step as a new owner decision (a REJECT rejects the build, 21.2).
6. Keep the filled sheet unchanged; record its hash: `certutil -hashfile results_package_2026-10-13\human_evidence\blind_check_filled_<initials>.csv SHA256`.
7. The evidence file (H3) is created only on or after `2026-10-22T07:50:10Z`, when the other H3 preconditions hold (H4 stop rule decided; the owner's written confirmation that nothing bound into the Step 8 manifest is still open; K1 per 12.51 means no new manifest). Command (dates are yours, true, UTC):

```bash
python -B -I research_design/step9/s9_blindcheck.py --sheet results_package_2026-10-13/human_evidence/blind_check_filled_<initials>.csv --bundle research_design/step8_output/step8_build_7a6bbe465c66/main/checker_bundle --evaluation-out results_package_2026-10-13/human_evidence/blind_check_evaluation_2.json --evidence-out results_package_2026-10-13/human_evidence/step9_evidence.json --completed-utc <YYYY-MM-DDTHH:MM:SSZ, >= 2026-10-22T07:50:10Z> --last-registry-view-utc 2026-10-15T07:50:10Z
```

The writer refuses REJECT or coverage below 100 %. The file records the worksheet hash; the gate then compares `build_manifest_sha256` with the build's manifest (any manifest change voids it).

## 6. Mistakes that cost the clock or the evidence

Opening a forbidden file; editing the blank; editing a row after an evaluation; writing a date that is not true; using a model to fill rows; asking the assistant to "fix" rows; asking the assistant to open the checker_bundle (the assistant will not).
