# Operational checklist for the human tasks H1-H7 (PREPARED — NOTHING BELOW HAS BEEN DONE)

Prepared 2026-10-13. Every status in this file is **NOT DONE** because no evidence exists. This file does not fill any worksheet, date, hash or authorization, and no field may be marked COMPLETE by anyone except the person who performed the task and produced the evidence file named in the last column. Row-by-row filling instructions for the blind check and the rehearsal are in `HUMAN_TASK_GUIDE.md` (not repeated); commands are in `OPERATIONS_RUNBOOK.md`; decisions are in `MASTER_PROPOSED_DECISION_RECORD.md` (MD-xx) and `C31_C32_OWNER_DECISION_BRIEF.md`. Paths are relative to `D:\research s2`. `BUILD` = `research_design/step8_output/step8_build_7a6bbe465c66`.
Suggested (not created) storage folder for human evidence, outside the frozen trees: `results_package_2026-10-13/human_evidence/` ; files are written once and never edited. Dates are UTC, written by the person at the time, never filled in advance and never changed.

## START HERE: minimal checklist (updated 2026-10-13; nothing in it has been done by the assistant)
**Researcher: tasks you can start now** (independent unless a dependency is written)
- [ ] **R1. Record the true time you stop viewing registry content (the start of the 7-day clock).** At the moment you actually stop, run `powershell -NoProfile -Command "[DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ssZ')"`, and save the printed value plus one sentence ("last time I viewed rendered registry content or expected states") yourself as a NEW file `results_package_2026-10-13/human_evidence/clock/last_registry_view_utc.txt`. Do not run the command "to try it" and keep the value; do not back-date; do not let the assistant write the file. **Until this file exists the clock is NOT running** and no date in this package is a start date.
  - What counts as viewing (opening any of these restarts the clock): `BUILD/main/registry.json`, `main/prompt_table.json`, `main/prompts/`, `main/gate_report.json`, `main/checker_mapping_HELD_SEPARATELY.json`, the whole `BUILD/pilot/` folder, any run or analysis output, and any chat or report passage that shows rendered prompts or expected states. To the assistant's knowledge the working transcripts show only aggregate prompt lengths and counts, no rendered prompt text or expected state; judge this yourself before choosing the time.
- [ ] **R2. H4 codebook rehearsal** (independent of the clock; uses synthetic comments only): follow `HUMAN_TASK_GUIDE.md` part 2; before comparing, run the format pre-check (it never opens the expected codes): `python -B -I results_package_2026-10-13/reproduce/precheck_human_sheets.py --kind rehearsal --sheet <your filled csv>`; evidence: filled sheet, `comparison.json`, the sheet's SHA-256, a written list of disagreements, saved in `human_evidence/rehearsal/`. Do not open `codebook_battery_v1.py` before finishing all 40 rows.
- [ ] **R3. H1 blind check** (needs R1; ask the owner first whether PG3 is ratified: a strict PG3 reading would rebuild the registry and make this work void; the owner's entry on PRD-5 should exist before you rely on the evaluation): follow `HUMAN_TASK_GUIDE.md` part 1 with your own copy of the blank worksheet; open only `checker_bundle` files, one at a time. Before the first evaluation run the format pre-check (it opens only your sheet and the blank kit; it prints row ids and column names only, never cell contents, and does not predict the verdict): `python -B -I results_package_2026-10-13/reproduce/precheck_human_sheets.py --kind blindcheck --sheet <your filled csv>`; fix empty or malformed cells BEFORE evaluating, never after. Evidence in `human_evidence/blind_check/`: filled worksheet (never edited afterwards), `evaluation.json`, worksheet SHA-256.
  - Timing rule (from the guide): the evidence requires `completion >= R1 + 7 days`; you may start H1 as soon as R1 exists and the tools check only those two dates, so do not wait out of convenience. Two limits: you cannot validly COMPLETE before R1 + 7 days (the evidence tool refuses), and the purpose of the delay is that you no longer remember the expected states, so keep all registry and expected-state material closed until you finish; whether your own state of knowledge is independent enough is your and your advisor's judgment, not something a tool checks. Never write a completion date before the check is truly finished.
- [ ] **R4. H3 evidence file** [first ask the owner to confirm in writing that nothing bound into the build manifest is still open: MD-03 (K2), the PG3/PG11b/SF-UNP items of MD-05, MD-10, any codebook revision from your H4 findings, and a changed register value in MD-07; any of them changes the Step 8 manifest hash that this evidence file names, so the evidence must be created after the rebuild; if all are settled as 'no change', nothing waits] (needs R1, R3 and at least 7 full days between the R1 value and your completion time): run the second command of `HUMAN_TASK_GUIDE.md` part 1 with your true `--last-registry-view-utc` (the R1 value) and `--completed-utc`; output `human_evidence/blind_check/step9_evidence.json`. The tool refuses on a REJECT or coverage below 100 %.
**Owner: tasks you can do now**
- [ ] **O1. Decide the entries** in `OWNER_APPROVAL_PACKAGE.md` (PRD-5 first); record them yourself in the official record. No chat reply is an entry.
- [ ] **O2. Choose the FZ file list** (Appendix A of the package) and approve or amend the hash procedure.
- [ ] **O3. H7:** declare the write-once store for the decision record (an official entry; your own commit is the recommended store). Needed before the decision script, not before the pilot.
- [ ] **O4. H5 (after O1):** create the pilot-round-1 authorization as a NEW file from `templates/owner_authorization_TEMPLATE.json`: `authorized_by` = `owner`, `scope` = `pilot_round_1`, `max_calls` = 18, `cost_ceiling_usd` = 100, `input_tokens_per_call_assumed` (your assumption; 1016 is the Step 7 assumption, not a measurement), `max_input_characters` (pre-filled 1016, confirm or change; at least the longest planned prompt, 1,016 characters). Save under `human_evidence/authorization/authorization_pilot_round_1.json`; keep its SHA-256 and date.
- [ ] **O5. Decide whether to authorize one provider connection test** (`PROVIDER_VERIFICATION_MATRIX.md`); not required for the pilot; MD-06 is the protection if you do not.
**H6 (researcher or owner):** on the day of the first paid call, read current prices and model terms and save a dated note `human_evidence/price_reread_<date>.md` (compare with FZ-v1: input 0.30, output 2.50 US$ per 1M tokens as stored; a difference is a stop-and-ask).
**Independent now:** R2, O1, O2, O3, O5. **Chained:** R1 -> R3 -> R4 (7-day gap from R1); O1 -> O4 -> gate check; the FZ hash only after O1/O2 are settled. **Evidence folder** (suggested, create it yourself when you have the first evidence): `results_package_2026-10-13/human_evidence/{clock,blind_check,rehearsal,authorization}/`.

## Summary
| # | Task | Who | Status | Depends on | Blocks |
|---|---|---|---|---|---|
| H1 | Blind check of the 624 rendered texts | the researcher alone | NOT DONE | B1 (date decision), PRD-5 decided (MD-05) before the evaluation is read as final | H2, H3 |
| H2 | Seven-day delay | the researcher (a calendar fact, not an action) | NOT STARTED (clock not running) | H1 started and the true last-viewing date | H3 |
| H3 | Step 9 evidence file | the researcher runs the evaluator | NOT DONE | H1, H2, MD-05 (PRD-5) | gate reason 1 |
| H4 | Codebook rehearsal, 40 rows | the researcher | NOT DONE | none (before the pilot, spec 13.5) | pilot |
| H5 | Owner authorization for pilot round 1 | the owner | NOT DONE | MD-02 / C-32 answered; H3 not required to write it but the gate needs both | gate reason 2 |
| H6 | Re-read prices and model terms | the researcher or owner on the day of the paid call | NOT DONE | H5 content | first paid call |
| H7 | Declare the write-once store (PRD-6) | the owner | NOT DONE | MD-09 | decision script, main run |
Order (checklist H8): H1 -> H2 -> (PRD-5 decided) -> H3; H4 any time before the pilot; MD-items; H5 last, after the cost basis is chosen; H6 on the day.

## H1 Blind check
- **Purpose.** Re-derive by calculator the verdict for each of the 624 rendered texts and compare with the held mapping (spec 11 layer 3, 11.2; FZ-v1 row 19: coverage 100 %). It tests re-derivation consistency, not inter-person agreement.
- **Procedure.** Follow `HUMAN_TASK_GUIDE.md` part 1. Copy `step9_blind_check_kit/blind_check_worksheet_MAIN_blank.csv` to a new file; fill every required cell yourself; do not use a model to fill rows; do not edit the blank; do not open the listed registry, prompt, gate-report or pilot files before or during the check.
- **Inputs.** Files of `BUILD/main/checker_bundle/` one at a time; the blank worksheet.
- **Output / evidence to keep.** The filled worksheet CSV (unchanged afterwards); `evaluation.json` from `s9_blindcheck.py --evaluation-out`; the SHA-256 of the worksheet (`certutil -hashfile <file> SHA256`).
- **Acceptance.** Coverage 100 %; `build_verdict` = `NO REJECT`; a REJECT rejects the build (spec 21.2): stop, consult the advisor, do not edit rows.
- **Expected location.** `human_evidence/blind_check/` (suggested).
- **Status.** NOT DONE (no filled worksheet exists). **Next action.** The researcher performs it; the assistant fills nothing and stops here.

## H2 Seven-day delay
- **Purpose.** The check must be completed at least 7 days after the researcher last viewed rendered registry content or expected states (FZ-v1 row 19).
- **Procedure.** The researcher decides the true date and time at which they stop viewing such content (task B1 in `NEXT_ACTIONS.md`), notes it, and does not view that content until completing H1. Nothing restarts, back-dates or pre-fills the clock; the evaluator takes both dates from the command line.
- **Input.** Two true UTC timestamps supplied by the researcher: `--last-registry-view-utc` and `--completed-utc`.
- **Evidence.** The researcher's own dated note and the two values inside the evidence file; the gate recomputes the difference (must be >= 7 days).
- **Acceptance.** Difference >= 7 full days; no viewing in between (a statement by the researcher; the tools cannot verify it).
- **Status.** NOT STARTED: today no stop-viewing date has been recorded, so the clock is not running. The earliest possible completion is the stop-viewing date plus 7 days; the delay cannot be shortened or simulated.

## H3 Step 9 evidence file
- **Purpose.** The only file that lets the gate see the human blind check.
- **Procedure.** After H1 and H2: run the second command of `HUMAN_TASK_GUIDE.md` part 1 (`--evidence-out ... --completed-utc ... --last-registry-view-utc ...`). The tool refuses for any REJECT or coverage below 100 %.
- **Output.** `step9_evidence.json` (new file, never overwritten) and the second `evaluation.json`.
- **Acceptance.** File exists; gate reason "Step 9 evidence file missing" disappears; the evidence names this build manifest (`09eed00e...`) and the worksheet hash.
- **Expected location.** `human_evidence/blind_check/step9_evidence.json`.
- **Status.** NOT DONE. **Do not** create it by script on the researcher's behalf.

## H4 Codebook rehearsal (40 rows)
- **Purpose.** Spec 13.5 / codebook section 6: find ambiguities before the pilot; not a reliability or validity claim.
- **Procedure.** `HUMAN_TASK_GUIDE.md` part 2. Copy `codebook_rehearsal_kit/rehearsal_sheet_BLANK.csv`; code all 40 rows from the comment text and the codebook only; do not open `step7/codebook_battery_v1.py` until finished; then run `reproduce/compare_rehearsal.py` once.
- **Output / evidence.** Filled sheet CSV, `comparison.json`, hash of the sheet; a written list of disagreements for the advisor. Do not change the codebook or the expected codes.
- **Acceptance.** All 40 rows coded; comparison produced; disagreements recorded (their presence does not fail the task but may require a codebook version before the FZ hash).
- **Expected location.** `human_evidence/rehearsal/`.
- **Status.** NOT DONE.

## H4 step by step: commands, expected output, and what to do with findings (verified 2026-10-13 on an unedited copy of the blank sheet; nothing here is a result)
Run from `D:\research s2` in PowerShell. Creating the `human_evidence\rehearsal` folder does NOT start the 7-day clock (only your own R1 file does).
1. **Create your working copy** (never edit the blank):
   `mkdir results_package_2026-10-13\human_evidence\rehearsal`
   `copy results_package_2026-10-13\codebook_rehearsal_kit\rehearsal_sheet_BLANK.csv results_package_2026-10-13\human_evidence\rehearsal\rehearsal_filled.csv`
   Check the blank is intact: `certutil -hashfile results_package_2026-10-13\codebook_rehearsal_kit\rehearsal_sheet_BLANK.csv SHA256` must print `19db7b40ac239c97e971aa6445db9e9d7a3ae4ff70a25a8523af94dc62c65c49`.
2. **Check the blank copy before you begin** (expected state: nothing coded yet):
   `python -B -I results_package_2026-10-13\reproduce\precheck_human_sheets.py --kind rehearsal --sheet results_package_2026-10-13\human_evidence\rehearsal\rehearsal_filled.csv`
   Expected output exactly:
   `rows: 40; not filled: 40; problems: 0`
   `NOT FILLED (first 5 ids): b7721cb9eafab528, 1701d0609e59cfd2, bc413c5b52ef04c8, ec2cb38a3c7f3280, 00ceeab4df7002aa`
   `FORMAT PRE-CHECK: NOT COMPLETE`
   and exit code 1 (`$LASTEXITCODE`). Any `PROBLEM:` line at this point means the copy was altered: copy again from the blank.
3. **Code the 40 rows yourself** in a spreadsheet program, from the comment text and `research_design\step7\CODEBOOK_S2_S3_v1_DRAFT.md` only. Allowed codes: `s2_evidence` NC/NV/IV/EV; `s2_prov` Y/N (empty when there is no derived quantity); `s2_values` cv/sw/none; `s2_arith` AC/AI/AM/AN; `s2_rel` RT/RF/RM (empty unless EV); `s3_stance` NC/AG/DG/CQ/MPG/NS (`MPG`, not `MX`). Do not touch `comment_text` or `opaque_id`. Save as CSV UTF-8 under the same name. Do not open `codebook_battery_v1.py` or any file that shows expected codes. No model may fill rows.
4. **Re-run the pre-check until it is clean.** Complete state: `rows: 40; not filled: 0; problems: 0` then `FORMAT PRE-CHECK OK (advisory; it does not predict the evaluation)`, exit 0. Fix empty or malformed cells now, before step 5.
5. **Compare ONCE** (this opens the expected codes; do not edit the sheet afterwards):
   `python -B -I results_package_2026-10-13\reproduce\compare_rehearsal.py --sheet results_package_2026-10-13\human_evidence\rehearsal\rehearsal_filled.csv --out results_package_2026-10-13\human_evidence\rehearsal\comparison.json`
   Expected: one line of JSON with the six variables `s2_evidence, s2_prov, s2_values, s2_arith, s2_rel, s3_stance`, each with `n`, `agree`, `raw_agreement_percent`, exit 0; the file `comparison.json` lists every disagreement (item, variable, your code, expected code) and the statement "rehearsal on synthetic comments; not a reliability or validity claim; no kappa". The tool never overwrites.
6. **Record the evidence:** `certutil -hashfile results_package_2026-10-13\human_evidence\rehearsal\rehearsal_filled.csv SHA256` and the same for `comparison.json`; keep both hashes with the dates in your own note.
7. **Findings.** Every disagreement is a finding, not automatically a codebook defect. For each one write, in your own file `human_evidence\rehearsal\rehearsal_findings.md`, its class: **(A)** your slip or misreading (no codebook action; still recorded); **(B)** the codebook wording allows two defensible readings (a codebook discrepancy); **(C)** the pre-registered expected code looks wrong (a battery question; the battery hash is pre-registered in record 12.22, nothing is changed). Blank template (copy it into your findings file and fill it yourself):
   | item | variable | my code | expected | class A/B/C | one-sentence reason |
   |---|---|---|---|---|---|
   | | | | | | |
8. **Stop rule before H3.** If any finding is class B or C, or you are unsure, do NOT create H3. Send the findings file to the owner and the advisor with this question: "(i) no change, the point is recorded as a limitation; (ii) a codebook revision (new Step 7 version, box R-7, rebuild sequence in `OWNER_APPROVAL_PACKAGE.md`); (iii) a question on the battery for the advisor." Nobody, including the assistant, edits the codebook or any manifest-bound file on the basis of the findings without that written decision. If there are no class B or C findings, H4 does not block H3. H1 does not depend on H4.

## H5 Owner authorization (pilot round 1)
- **Purpose.** The owner's written authorization read by the gate (`check_gates`).
- **Procedure.** The owner (not the assistant) copies `templates/owner_authorization_TEMPLATE.json` to a new file and writes: `authorized_by` = `owner`; `scope` = `pilot_round_1`; `max_calls` = 18; `cost_ceiling_usd` = 100; `input_tokens_per_call_assumed` = a positive integer chosen by the owner (the accepted Step 7 assumption is 1016, i.e. at least one token per character; it is an assumption, not a measurement; C-32); `max_input_characters` = a positive integer chosen by the owner (the longest planned prompt is 1,016 characters; a smaller value is refused by the preflight; a larger one is allowed). The note field is not read.
- **Inputs.** The owner's decisions on MD-02 / C-32 (Q7-Q9) and, if the owner so decides, on the cost basis.
- **Evidence.** The saved authorization file with its SHA-256 and the date the owner wrote it; the hard-cap figure printed by the gate preflight (about US$0.37 for 18 calls at 1,016 assumed tokens, `hard_cap_cost_usd`; a cost bound, not a forecast).
- **Acceptance.** Gate check without `--live` no longer lists the authorization reasons; the limit is a control on prompt length only, not a token measurement and not a cost guarantee.
- **Expected location.** `human_evidence/authorization/authorization_pilot_round_1.json`.
- **Status.** NOT DONE (only the invalid template exists).

## H6 Re-read prices and model terms (PJR J-9)
- **Purpose.** Prices and model terms in FZ-v1 were read on 2026-10-12 (input 0.30, output 2.50 US$ per 1M tokens as stored); the paid call must rest on current terms.
- **Procedure.** On the day of the first paid call the researcher or owner reads the provider's current pricing and model-terms pages (a human reading task; no API call), writes the date, the sources, the values and any difference from the FZ-v1 prices.
- **Acceptance.** A dated note exists; if prices or terms differ from FZ-v1, stop and ask the owner (a different price changes the cost bound; a different model is a protocol change, not an adjustment).
- **Expected location.** `human_evidence/price_reread_<date>.md`.
- **Status.** NOT DONE (no note; the date is not known in advance).

## H7 Declare the write-once store (PRD-6)
- **Purpose.** Spec 10 line 662 and 19.3 line 1132: the decision record must be anchored in a write-once store before an order is generated; the runner verifies the anchor for the main run (patch P7, MD-09).
- **Procedure.** The owner chooses and declares the store (own commit whose ID is recorded, or an external timestamped copy of the record's SHA-256), as an official record entry, before the decision script runs. Committing is the owner's permission; the assistant does not commit.
- **Evidence.** The record entry (approver, date, store type and location).
- **Acceptance.** Entry exists before the decision script is run; later the recomputed record hash matches the anchored value.
- **Status.** NOT DONE.

## Stop point
The assistant has prepared the instructions only. It stops here: every row above needs a person, and none of the evidence may be produced on their behalf. The pilot gate remains CLOSED until H3 and H5 exist and the other gate conditions hold.
