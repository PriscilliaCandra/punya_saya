# Human task guide: blind check and codebook rehearsal

Both tasks must be done by you. Nothing in this guide has been done, and no date has been entered anywhere. All commands below were checked against the `--help` output of the tools on 2026-10-13. Run them from `D:\research s2`.

## Part 1. The blind check (specification section 11 layer 3, 11.2; FZ-v1 row 19: coverage 100 %, minimum delay 7 days)

**What it is.** You re-derive, with a calculator, the verdict for each of the 624 rendered rule + plan texts, from the opaque-ID files only, and fill a worksheet. It tests re-derivation consistency, not inter-person interpretation (11, single-researcher limitation). A model may be used only as an extra screening layer, never as the check.

**The 7-day delay.** It is measured from the last time you saw rendered registry content or expected states until the day you complete the check, and you must not view such content in between. The clock is not running now. You decide and record the date when you stop viewing; the tools never fill it in.

**Do not open before and during the check** (opening any of them restarts your clock): `research_design/step8_output/step8_build_7a6bbe465c66/` files `main/registry.json`, `main/prompt_table.json`, `main/prompts/`, `main/gate_report.json`, `main/checker_mapping_HELD_SEPARATELY.json`, the whole `pilot/` folder, and any run or analysis output. Also avoid re-reading chat or report passages that show rendered prompts or expected states. Open only the files of `main/checker_bundle/` one at a time, as the worksheet rows come.

**Files**
- Texts to read: `research_design/step8_output/step8_build_7a6bbe465c66/main/checker_bundle/<opaque id>` (624 files).
- Blank worksheet: `results_package_2026-10-13/step9_blind_check_kit/blind_check_worksheet_MAIN_blank.csv`. Never edit the blank. Copy it to a new name (for example `blind_check_filled_<your initials>.csv`) in a folder of your choice and fill the copy in a spreadsheet program, then save as CSV (UTF-8).

**Filling one row** (all entries are required; the file name is the `opaque_id`).
- MIL file (starts "Constraint (weekly mileage cap)"): `P_or_D_dist` = the cap in percent as displayed (for example `10%`). For each week 1 to 5: `wN_transcribed` = the displayed total (for example `21.5`, a trailing `km` is allowed), `wN_value` = the same total in km. Week 1: status `uncompared` and leave the three computed columns empty. Weeks 2 to 5: `increase` (km, at least 1 decimal), `limit` = P % of the previous week (km, at least 2 decimals), `percent` increase (at least 2 decimals), `status` = `over cap` or `not over cap` (over cap only if the percent is strictly above P). Verdict: `violated` if any week is over cap, else `satisfied`.
- PAC file (starts "Constraint (race pace consistency)"): `P_or_D_dist` = the distance (for example `10 km`), `T_time_displayed` = the target time as displayed, `T_time_seconds`, `tau_F` = the displayed tolerance in seconds (`50` or `50 sec`). For each week: `wN_transcribed` = pace as displayed (`5:11`, `min/km` allowed), `wN_value` = seconds per km, the first computed column = distance x pace in seconds (at least 2 decimals), the second = that value rounded to the nearest whole second (half rounds up), the third = rounded value minus target time (integer), `status` = `|e|>tau` if its absolute value is more than tau, else `not`. Verdict: `violated` if any week is `|e|>tau`, else `satisfied`.
- Hypothetical MIL illustration (not from the registry): P = 10, totals 30.0, 32.0, 34.0, 31.0, 29.0 give week 2: increase 2.0, limit 3.00, percent 6.67, `not over cap`; week 3: 2.0, 3.20, 6.25, `not over cap`; week 4: -3.0, 3.40, -8.82; week 5: -2.0, 3.10, -6.45; verdict `satisfied`.
- Rounding too coarsely (fewer decimals than the floors above) is a logged checker error, not a finding about the design.
- Use only `satisfied`, `violated` or `unclear`. If you write anything else or leave a required cell empty, the row is judged by the ordered procedure of 11.2 and can lead to a build rejection.
- Fill in the date columns of your own copy as you work if you want to; the evidence file takes the two dates from the command line, not from these columns.

**Evaluate** (writes new files only; does not open the mapping):
```
python -B -I research_design/step9/s9_blindcheck.py --sheet <your filled csv> --bundle research_design/step8_output/step8_build_7a6bbe465c66/main/checker_bundle --evaluation-out <new evaluation.json>
```
Read `build_verdict`: `NO REJECT` means no REJECT row; `counts` shows AGREE / CHECKER ERROR / REJECT. A REJECT rejects the build (21.2): stop and consult the advisor; do not edit rows to change the outcome.

**Create the evidence file** only after you have finished, with dates that you determine and that are true (UTC, format `2026-10-28T09:00:00Z`; completion date must be at least 7 days after the last viewing date):
```
python -B -I research_design/step9/s9_blindcheck.py --sheet <your filled csv> --bundle research_design/step8_output/step8_build_7a6bbe465c66/main/checker_bundle --evaluation-out <another new evaluation.json> --evidence-out <new step9_evidence.json> --completed-utc <date> --last-registry-view-utc <date>
```
It refuses to write the file for any REJECT or coverage below 100 %. Keep the filled worksheet unchanged: its hash is in the evidence file.

**Mistakes to avoid:** editing the blank; opening the files listed above; changing a row after seeing the evaluation; starting the clock by writing a date in advance; using a model to fill rows; asking the assistant to "fix" rows.

**Still needed for the gate** (not part of this task): Implementation B must agree on the same build (done on 2026-10-13, re-checked automatically by the runner), and the owner authorization file (see `templates/owner_authorization_TEMPLATE.json`).

## Part 2. Codebook rehearsal (specification 13.5; codebook revision 5, section 6)

**What it is.** You code the 40 synthetic comments from the comment text only, with the codebook, to find ambiguities before the pilot. It is not a reliability or validity claim. No model response is involved.

**Files.** Codebook: `research_design/step7/CODEBOOK_S2_S3_v1_DRAFT.md`. Sheet: `results_package_2026-10-13/codebook_rehearsal_kit/rehearsal_sheet_BLANK.csv` (copy it to a new name; never edit the blank). Do not open `research_design/step7/codebook_battery_v1.py` (it holds the expected codes) until you have coded all 40 rows. Optionally wait some days between reading the codebook and coding, as the codebook notes the coder will remember the items.

**Fill** `s2_evidence` (NC/NV/IV/EV), `s2_prov` (Y/N, empty if the comment has no derived quantity), `s2_values` (cv/sw/none), `s2_arith` (AC/AI/AM/AN), `s2_rel` (RT/RF/RM, empty unless EV), `s3_stance` (NC/AG/DG/CQ/MPG/NS). Rows are in scrambled order.

**Compare** (this opens the expected codes; run once, after you finish):
```
python -B -I results_package_2026-10-13/reproduce/compare_rehearsal.py --sheet <your filled csv> --out <new comparison.json>
```
It prints raw agreement per variable and lists each disagreement. Any disagreement is a place where the codebook text may need a new version; do not change the codebook or the expected codes yourself: record the points for the advisor. Note that the comparator was added on 2026-10-13 and is not part of the frozen set.

## Schema notes (checked 2026-10-13)
- The H1 worksheet has a column `family_read_from_text`; the specification's list for the worksheet (11.2) does not require it and neither the evaluator nor the pre-check reads it. You may enter MIL or PAC there if it helps you; it is optional.
- H4: for a mixed stance write `MPG` (the codebook code); the specification text also writes `MX`, but the comparator expects `MPG`, and the pre-check rejects `MX`. `s2_prov` and `s2_rel` may stay empty when not applicable; all other columns need a code.

## Optional format pre-check (added 2026-10-13)
Before you evaluate (part 1) or compare (part 2), you can check that no cell is empty or malformed: `python -B -I results_package_2026-10-13/reproduce/precheck_human_sheets.py --kind blindcheck --sheet <your filled csv>` or `--kind rehearsal`. It reads only your sheet and the blank kit sheet, opens no checker bundle, mapping, registry or expected-code file, prints only row ids and column names, writes nothing, and cannot tell you whether a verdict is right. A blank sheet reports `NOT FILLED` and exit 1, which is the expected state today.

## What to record when done
Dates (last viewing, completion), the three output files, and the hash of each filled sheet (`certutil -hashfile <file> SHA256`). Give the evidence file and the owner authorization to the runner only via the gate check in `OPERATIONS_RUNBOOK.md`.
