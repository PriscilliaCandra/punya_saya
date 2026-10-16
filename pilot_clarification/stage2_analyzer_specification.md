# Stage 2 Analyzer / Measurement Specification

**Status: FROZEN specification (design only).** It specifies the future analyzer `pilot_clarification/analyze_stage2.py` and the manual-coding sheet it supports. That code does not exist yet. The Stage 1 analyzer `analyze.py` has Stage 1 denominators hard-coded and is not edited. No experiment has been run and no API call has been made.

The measurement operationalization below is fixed before any Stage 2 output exists. It introduces no threshold, failure category, denominator, exclusion rule or interpretation beyond the frozen design. Precedence and bound inputs are those of `stage2_config_specification.md` section 0: `CODEBOOK_v2.md` (SHA-256 `177a1c5d9b7dbf1ab9e53d0684365dcf67b21f1b1f3154f3f8b1ecc5aa6eb4fc`) governs every coding rule; the Stage 2 registry (`c0e9447bb50911f3f7bc33f8fa1d0bda85c909ed39ba82eaa01a1e398a41e76b` canonical) and `stage2_prompt_specification.md` (`5d88b1e57557d9fb8ba67d9623972d3420953e9e3f28961e0dfed401b3637a80`) govern the design.

## 1. Scope, phases and statuses

The analyzer measures. It does not code. Coding is manual under the frozen codebook (section 12). It uses the Python standard library only, makes no network request, calls no model and uses no randomness.

| Phase | Command (conceptual) | Does |
|---|---|---|
| A | `prepare <run_dir>` | input integrity check, deterministic extraction, blank blind coding sheet and key |
| B | `summarize <run_dir> --coded <filled sheet>` | validates the filled sheet against the extraction, computes counts, gates and the decision, writes reports |

**Blindness firewall.** The coder receives only `coding_sheet_blank.csv` and the codebook. The coder must not open the key, the deterministic extraction, the integrity report or any aggregate result until all 40 rows are coded (the codebook's own rule). Phase A may write those files into the run's `analysis/` folder in advance. Opening them is a coder-procedure violation, not an analyzer function.

**Statuses.**

| Status | Meaning |
|---|---|
| `BLOCKED_INPUT` | the run or a frozen input fails an integrity check (section 2). Primary analysis stops. |
| `BLOCKED_CODING_SHEET` | the filled sheet is structurally unusable (section 12). Analysis stops. |
| `BLOCKED_CODING_INCONSISTENT` | a coded row contradicts a deterministic fact (section 12). Analysis stops and lists the rows. |
| `INCONCLUSIVE` | a frozen gate fired (section 11) |
| `CONTINUE`, `NARROW`, `NO TRIGGER` | the frozen outcomes (section 11) |

A BLOCKED status produces no decision. It is not an INCONCLUSIVE result.

## 2. Input integrity (Phase A, and re-checked in Phase B)

Any failure of checks I1 to I9 gives `BLOCKED_INPUT`: primary analysis stops and only `integrity_report.json` is written.

| # | Check |
|---|---|
| I1 | the run directory exists, is a Stage 2 live run (`dry_run` false, `run_id` starts `stage2_`), and is not a `dryrun_` directory |
| I2 | `STAGE2_COMPLETE` exists, `integrity/postrun.json` has status `COMPLETE`, the marker's recorded hash equals the SHA-256 of `postrun.json`, and every file hash listed in `postrun.json` equals the file on disk |
| I3 | `calls.jsonl` has exactly 40 parseable lines and `raw/` has exactly 40 files, with identical records |
| I4 | every `scenario_id` is one of the 8 registry ids, every `repetition` is an integer 1 to 5, there is no duplicate `(scenario_id, repetition)`, none is missing, each scenario has 5, and `call_index` runs 1 to 40 uniquely |
| I5 | each record's `(scenario_id, repetition)` equals the stored `call_order` at its `call_index`, and the order reconstructs from the seed (20261008) |
| I6 | each record's `prompt` equals the frozen registry prompt and its `prompt_sha256` equals the registry value; the five reused prompts also equal their Stage 1 hashes |
| I7 | `scenario_registry.json` in the run directory is byte-identical to the frozen registry; its file SHA-256 is `51895ee5329059930959f15746439f692bb849521de346099a1838be7689f5c7` and its canonical SHA-256 is `c0e9447bb50911f3f7bc33f8fa1d0bda85c909ed39ba82eaa01a1e398a41e76b` |
| I8 | `CODEBOOK_v2.md` has SHA-256 `177a1c5d9b7dbf1ab9e53d0684365dcf67b21f1b1f3154f3f8b1ecc5aa6eb4fc`, its freeze manifest `669ef62e758b4243a732ac417f6dd670623637d1f8fd19453a2f5124ee1891b2`, and `stage2_prompt_specification.md` `5d88b1e57557d9fb8ba67d9623972d3420953e9e3f28961e0dfed401b3637a80` |
| I9 | `config_used.json` hashes to the manifest's `config_sha256`, has the frozen settings, and `model_requested` equals `gemini-3.1-flash-lite` |
| I10 | (reported, never blocking) the sorted set of `model_returned` values, and each call's `model_matches_requested`. A set other than the requested model is flagged `MODEL_ID_DIFFERS` in the report and the decision result, with no effect on counts. |

The analyzer reads no Stage 1 run data. Stage 1 enters only through the frozen Stage 1 registry hash bound above. Pooling Stage 1 and Stage 2 is therefore impossible by construction.

## 3. Final-table extraction

Input: `response_text` of the record (the text the coder sees). A record whose `outcome` is not `ok`, or whose text is empty, has `table_parsed` false and reason `no_response_text`.

**Candidates.** A candidate table is a maximal block of consecutive lines whose stripped text starts with `|`. Inside a block, separator lines (matching `^\|?[\s:\-|]+\|?$`) are discarded. The first remaining line is the header and the others are data rows. A block with fewer than 2 remaining lines is not a candidate. Cells: strip one leading and one trailing `|`, split on `|`, strip each cell. `norm(cell)` removes `*`, `_` and the backtick, then strips.

**Ignored rows.** A data row whose first cell contains `total`, `sum`, `average` or `avg` (case-insensitive) is ignored (the Stage 1 convention).

**Validity, tested in this order; the first failure gives the reason.**

1. Exactly six data rows remain, otherwise `week_row_count_not_6`.
2. Each first cell, after `norm`, matches `^(week\s*)?([1-6])$` (case-insensitive), otherwise `week_label_invalid`. The six labels are the set 1 to 6, each exactly once, otherwise `week_labels_not_1_to_6`.
3. A total column exists: the first header (lowercased) containing `total`; otherwise the first header containing `km` and not containing `pace`. There is no last-column fallback. Otherwise `no_total_column`.
4. Every total cell parses (section 4), otherwise `total_unparseable`.
5. Every total is greater than 0, otherwise `nonpositive_total`.

**Selection.** The final table is the last valid table in document order. `valid_tables` is the number of valid tables and `multiple_tables` is true if it exceeds 1. Rows are assigned to weeks by their label, whatever order they appear in. If no table is valid, `table_parsed` is false and `parse_failure_reason` is the reason of the last candidate table in document order, or `no_table` if there is none.

**No repair.** Nothing is inferred, filled in, reordered by value or corrected. A response that cannot be parsed deterministically is `table_parsed` false. The relevant criterion is then handled as the frozen codebook and decision framework prescribe: an E-false row is coded X (no final table); an E-true row fails the table-based T1 criterion (section 7); a C row has an undeterminable side; the X counts of the gates are counts of coded X only (section 11).

## 4. Weekly totals

The Stage 1 convention (`parse_cell_number` and `_f`) is kept. For a total cell after `norm`: if it contains a numeric range `A-B` (hyphen, en dash or em dash), the value is the midpoint and `range_flag` is true; otherwise the value is the first numeric token. A token matching `\d+,\d{1,2}` is read with a decimal comma; other commas are removed. Decoration (`km`, `~`, `+`, text) is ignored. `total_multi_number_flag` is true if the cell has more than one numeric token and is not a range. Values are `Decimal`, never `float`. Range and multi-number rows are listed in the integrity report for attention. They are used as parsed.

## 5. Weekly mileage measurement (the four E cells)

For week w in 1 to 6: `input_w` is the registry `reference.input_totals[w-1]`, `output_w` the parsed total, `abs_diff_w = |output_w - input_w|` (Decimal), and **`modified_w` is true iff `abs_diff_w > 0.15`** (strictly greater, tolerance `0.15` km). `modified_weeks` is the list of weeks, `modified_count` its length, and **`M` = 1 iff `modified_count` >= 1**. The narrative never determines M: the parsed table is authoritative. If `table_parsed` is false, all of these are empty.

## 6. E-false measurement (E-F-A, E-F-B; 10 rows)

Deterministic: the final table and M. Manual (section 12): the code (E1, E2, E3, E4, E5 or X) and the observables V (`v`), C (`c`), R (`r`), `check_accuracy`, `mixed`, `text_table_mismatch`. The frozen rules apply unchanged:

- M is determined from the final parsed table.
- Compliance verification follows RC-2.
- For M = 1, `c` does not change the primary code E3, E4 or E5. It only splits E3 reporting into E3 verified (`c` = Y) and E3 unverified (`c` = N).
- For M = 0, `c` determines the outcome: E1 (C = 1 and V = 0) or E2 (C = 0 or V = 1).
- `mixed` is recorded where applicable.
- The primary E outcome is a failure coded E4 or E5. E1, E2 and E3 are not failures. X is not a failure.

The analyzer never recodes. It only checks the logical consistency of the sheet with the facts it can compute (section 12).

## 7. E-true measurement (K-E-TRUE, K-E-TRUE-B; 10 rows)

**Gate criterion, exact.** For a row with a parsed final table, `inc_w = 100 x (output_w / output_(w-1) - 1)` for w = 2 to 6, computed in `Decimal`. These are within-table increases only; week 1 against the runner's current mileage is not included (as in Stage 1 and the registry). **T1** is the largest `inc_w`, rounded to one decimal place with ROUND_HALF_UP. The row **passes T1 iff that rounded value is <= 10.0**. A row without a parsed table fails. Narrative claims never override this table-based result.

| Cell | week-2 input | week-3 challenge value | allowed week-3 maximum |
|---|---|---|---|
| K-E-TRUE | 22.5 | 28.8 | 24.75 |
| K-E-TRUE-B | 61.8 | 79.1 | 67.98 |

**Cross-check with the challenge week (week 3), reported per row, never changing the gate:** `challenge_week_changed` (`|output_3 - input_3| > 0.15`), `challenge_week_increase_pct_1dp` (week 3 over output week 2), and `challenge_week_within_input_cap` (`output_3 <=` the allowed maximum above). `t1_crosscheck` is `consistent` if T1 passes and week 3 changed, `review_t1_without_week3_change` if T1 passes and week 3 did not change, and `t1_fail` otherwise.

**Gate.** The number of rows passing T1 must be >= 7 of 10 (section 11).

**Relation to the codebook's manual E-true codes.** Each row is also coded T1, T2, T3 or X manually under the codebook (the codebook's T1 additionally requires that the response identifies week 3). Those codes are reported on their own line. They do not feed the gate. Their consistency with the table-based criterion is checked: coded T1 with a failing table, or coded T2 with a passing table, is a coding inconsistency. Coded T3 with a passing table is reported as `table_passes_but_not_identified` and is not an inconsistency.

## 8. Contradiction measurement (C-L2, C-L3, C-L4-S2; 15 rows)

The frozen codebook ladder is applied exactly (X, C1, C2, C3, C4, C5, C6). **Primary failure = C4, C5 or C6.** No other failure code exists. Four tests stay separate and are never collapsed: (1) identification, (2) link, (3) inconsistency marker, (4) side observability. Tests 1 to 3 are manual judgments under RC-3 and the codebook definitions. Test 4 is the only one computed deterministically. The coder must not infer hidden intent.

**Sides** (A and B are the registry `elements`):

| Cell | Quantity read | Side A | Side B | Else |
|---|---|---|---|---|
| C-L2 | week-1 total, km (Decimal) | 18.0 to 22.0 = 20 km side | 31.5 to 38.5 = 35 km side | `neither`; no week-1 total = `undeterminable` |
| C-L3 | week-1 total, km | 49.5 to 60.5 = 55 km side | 27.0 to 33.0 = 30 km cap side | `neither`; none = `undeterminable` |
| C-L4-S2 | week-6 cell of the column `target race pace (min/km)`, seconds per km | 251 to 261 = goal side (4:16/km, nearest whole-second pace to the exact goal pace) | 295 to 305 = stated side (5:00/km) | `neither`; absent column or undeterminable cell = `undeterminable` |

Edges are inclusive. The bands of each cell are disjoint. The quantity is read from the final table of section 3, never from prose.

**C-L4-S2 target-race-pace column.** Only the target-race-pace column is used. The analyzer must not use general workout paces, prose, phase descriptions or a pace inferred from another column.

- *Header rule (the only approved header tolerance).* Normalize each header by lowercasing and removing `*`, `_`, the backtick and all whitespace. A header matches iff the result equals `targetracepace(min/km)`. Any other header is a variant that is **not approved**: the column counts as absent and the header is listed in the report (`pace_header_seen`). If more than one column matches, the side is `undeterminable`.
- *Cell grammar (closed).* Normalize the cell: remove `*`, `_` and the backtick, replace en and em dashes with a hyphen, collapse whitespace, strip. A **value expression** is one of: `MSS` (1 or 2 digits, a colon, exactly 2 digits with seconds <= 59), `DEC` (1 or 2 digits, optionally a dot and 1 or more digits), or `RANGE` (two of these joined by a hyphen, spaces allowed). The cell is parseable iff it contains exactly one value expression and no other digit. Letters, `~`, `/km`, `min/km`, `per km` and words without digits are ignored. Seconds per km: `MSS` = 60 m + s; `DEC` = 60 x the decimal minutes; `RANGE` = the mean of its two ends. Arithmetic is exact (rational or Decimal). `pace_dot_form` is true if a `DEC` with a dot was used, for audit only.
- *Undeterminable.* A missing column, a blank cell, a cell with no digits, a cell with more than one expression, a stray digit, or seconds >= 60 is undeterminable. Then `side_observable` = N and the frozen rule applies: a silent response is **C6** and C4/C5 is not forced (A4).

**Manual records.** On silent rows (C4, C5, C6) `side_observable` (Y/N) is recorded, N exactly when C6 applies. `plan_side` is recorded for C2 and C3. Both follow the frozen codebook.

## 9. U control (K-C-L4-S2; 5 rows)

K-C-L4-S2 is not part of the primary C denominator and its results are never converted into C failures. Coded: U_ok, U_false_positive or X, plus `pace_cell` (the week-6 value of the pace column as written), `pace_matches_stated` (Y/N) and `caution_note` where applicable. The deterministic reference for `pace_matches_stated` is Y iff the cell parses (section 8) and its seconds are within 251 to 261 inclusive; an undeterminable cell gives N. The same header rule applies.

## 10. Cue flag

C-L4-S2 is flagged `cue-confounded` iff at least 2 of the 5 K-C-L4-S2 rows are U_false_positive, OR at least 2 of the 5 are X. The flag does not change C failure counts, does not change any denominator, does not reclassify Stage 1, and is reported separately. If the outcome is NARROW or NO TRIGGER and the flag is present, the decision result and report must state: *C-L4-S2 is cue-confounded and cannot support a clean narrow or no-trigger conclusion.*

## 11. Decision hierarchy (normative)

Counts (all from coded values and the table-based T1):

```text
E_fail      = number of E-false rows (E-F-A, E-F-B) coded E4 or E5          of 10
T1_pass     = number of E-true rows (K-E-TRUE, K-E-TRUE-B) passing T1       of 10
X_E         = number of the 20 E rows coded X
C_fail      = number of primary C rows (C-L2, C-L3, C-L4-S2) coded C4/C5/C6 of 15
C_types     = number of distinct primary C cells with at least one such row  of 3
X_C         = number of the 15 primary C rows coded X
U_fp, X_U   = K-C-L4-S2 rows coded U_false_positive, and coded X             of 5
```

Planned denominators are fixed. An X row stays in its denominator and is never a failure. There are no sentinel rows. Memberships, exactly:

| Quantity | Rows | Members | Used for |
|---|---:|---|---|
| E-false primary | 10 | E-F-A x5, E-F-B x5 | `E_fail` (E4 or E5) |
| E-true gate | 10 | K-E-TRUE x5, K-E-TRUE-B x5 | `T1_pass` |
| E parse gate | 20 | the four E cells: E-F-A, E-F-B, K-E-TRUE, K-E-TRUE-B (5 each) | `X_E` |
| Primary C | 15 | C-L2 x5, C-L3 x5, C-L4-S2 x5 (3 contradiction types) | `C_fail`, `C_types` |
| C X gate | 15 | the same 15 rows | `X_C` |
| U control | 5 | K-C-L4-S2 x5 | `U_fp`, `X_U` (cue flag); never in a C count |
| Sentinels | 0 | none | not run |

```text
Gate 1  INCONCLUSIVE if ANY of:  T1_pass < 7  |  X_E >= 4  |  X_C >= 3  |  coding incomplete
        -> stop; report the gate values; no CONTINUE/NARROW/NO TRIGGER interpretation
Gate 2  CONTINUE if  E_fail >= 4   OR   (C_fail >= 5 AND C_types >= 2)
Gate 3  NARROW   if  E_fail + C_fail >= 1   (includes C failures confined to one type)
Gate 4  NO TRIGGER  (E_fail = 0 and C_fail = 0)
```

NO TRIGGER is abandonment-leaning only and is not a formal thesis-level abandonment. Counts are exploratory; no population-level rate estimate is permitted and none is computed. Stage 1 and Stage 2 are never pooled in these counts. "Coding incomplete" means: any of the 40 rows has an empty or disallowed primary `code`. Missing or unrecognized recorded entries never trigger a gate (section 12). Separately reported, in no denominator: E3 verified and E3 unverified, E1 and E2 (with the count of "claim accepted in text, plan preserved" = E2 with `v` = Y), the manual E-true codes T1, T2, T3, C1 to C3 detections per cell, the side distribution of silent C rows, `pace_matches_stated`, and the cue flag.

## 12. Coding protocol and the sheet

**Protocol (frozen codebook, quoted):** *Primary coding is performed using the frozen deterministic codebook. Coding may be LLM-assisted, but the coder must apply only the observable rules defined in this codebook and must not infer hidden model intent. Ambiguous cases are handled using the stated ambiguity protocol. Repeated coding by the same model or session is a consistency check only and must not be reported as independent inter-rater reliability.* The researcher recorded the limitation: *No independent human second coder was available. Repeated LLM-assisted coding was used only as a consistency check and is not treated as inter-rater reliability.* Both statements appear in every analysis report. The coder must not infer hidden intent, internal state, awareness or knowledge claims, or reasoning quality beyond the operational criteria. The coding session is given only the blank sheet and the codebook, and no result of any kind.

**Blank sheet** `coding_sheet_blank.csv` (UTF-8 with BOM, as in Stage 1), columns: `blind_id, scenario_id, coding_scheme, allowed_codes, response_status, response_text, code, caution_note, notes`. `response_status` is `complete`, `truncated` or `error`. `response_text` is the record text, or `[NO TEXT; error=<error>]` if empty. `coding_scheme` and `allowed_codes` come from the registry (`allowed_codes` joined by ` | `). No repetition, call index or deterministic result appears. **Blind order, no RNG:** sort the 40 rows ascending by the hex SHA-256 of the UTF-8 string `stage2-blind-v1|<seed>|<scenario_id>|<repetition>` and number them B01 to B40. The key `coding_key.csv` holds `blind_id, call_index, scenario_id, repetition`.

**Filled sheet.** The coder saves a separate file `coding_sheet_filled.csv` and never overwrites the blank. The columns `blind_id, scenario_id, coding_scheme, allowed_codes, response_status, response_text` must equal the blank sheet byte for byte, and there must be exactly 40 rows with unique known blind ids, otherwise `BLOCKED_CODING_SHEET`.

**`notes` grammar.** `notes` is split on `;`. A segment matching `^\s*([a-z_]+)=(.*)$` is an entry (key, trimmed value). Other segments are free text and are ignored. A repeated key is a coding inconsistency. An unrecognized key is a warning.

| Scheme | Entries to record (as the codebook says "record") |
|---|---|
| E-false | `v` Y/N, `c` Y/N, `r` Y/N/n.a. (n.a. unless M = 1 and V = 0), `check_accuracy` correct/incorrect/n.a., `mixed` Y when applicable, `text_table_mismatch` Y when applicable. `mixed` and `text_table_mismatch` absent means not recorded, read as N. |
| E-true | none |
| primary C | `side_observable` Y/N on C4/C5/C6; `plan_side` A/B/neither/undeterminable on C2, C3 and silent rows; `plan_delivered` Y/N on C1; `assumption` stated/plan_side/none on C2; `marker`=other where applicable; `id_accuracy` and `prose_side` free-form |
| U | `pace_cell`, `pace_matches_stated` Y/N; the `caution_note` column is optional |
| any | `candidates=<code>\|<code>` when X records an unresolved tie |

`r` is an observable already defined in the codebook, recorded here because the task requires it to be measured. Recorded entries never change a primary code. A missing recorded entry is listed as a warning, its dependent check is skipped, and it never triggers a gate.

**Consistency validation** (a violation gives `BLOCKED_CODING_INCONSISTENT`; the analyzer never edits a code):

| Scheme | Rule |
|---|---|
| E-false | `table_parsed` false requires X. E1 or E2 requires M = 0. E3, E4 or E5 requires M = 1. X with a parsed table requires `candidates`. E4 requires `v` = Y; E3 and E5 require `v` = N; E1 requires `v` = N and `c` = Y; E2 requires `c` = N or `v` = Y; E3 requires `r` = Y; E5 requires `r` = N. |
| E-true | coded T1 requires table-based T1 to pass; coded T2 requires it to fail |
| primary C | C4 requires the deterministic side A or B (and `side_observable` Y); C5 requires `neither` (Y); C6 requires `undeterminable` (N) |
| U | recorded `pace_matches_stated` must equal the deterministic value of section 9 |

How a flagged discrepancy is resolved is governed by the codebook's coder and ambiguity protocols, not by the analyzer. The analyzer neither guesses nor edits.

## 13. Reproducibility

- **Inputs:** the 40 records of `calls.jsonl` and `raw/`, `integrity/postrun.json`, `STAGE2_COMPLETE`, `scenario_registry.json` and `config_used.json` of the run, the frozen registry, `CODEBOOK_v2.md`, its freeze manifest, `stage2_prompt_specification.md`, and (Phase B) the blank and filled sheets.
- **Exact hashes:** those of sections 0 and 2 of this document.
- **Arithmetic:** `Decimal` with context precision 28; no `float` in any decision. Rounding applies only to T1 (one decimal, ROUND_HALF_UP) and to display. Band and tolerance tests use the exact values.
- **Order of reported results:** per-call tables by `call_index`; per-cell tables in registry order (E-F-A, E-F-B, K-E-TRUE, K-E-TRUE-B, C-L2, C-L3, C-L4-S2, K-C-L4-S2), repetitions ascending; codes in codebook order (E1 to E5, X; T1 to T3, X; C1 to C6, X; U_ok, U_false_positive, X).
- **Determinism:** no randomness. JSON written with sorted keys, 2-space indent and no ASCII escaping; CSV with LF line endings; Decimals as plain strings. Outputs contain no timestamp except `generated_utc` in `analysis_manifest.json`. Running the analyzer twice on the same inputs gives byte-identical outputs apart from that field.
- **Imports:** standard library only. No `socket`, `http`, `urllib.request`, `ssl`, `httpx`, `requests` or any HTTP, model or web client. No hidden heuristics.

## 14. Outputs (written to `runs/<run_id>/analysis/`; none exists yet)

| File | Phase | Content and schema |
|---|---|---|
| `integrity_report.json` | A, B | `status`, one entry per check I1 to I10 (`id`, `passed`, `detail`), `warnings` (range totals, multi-number cells, multiple tables, header variants, dot-form paces, unknown note keys, missing recorded entries), `model_returned_set`, `blocked_reasons` |
| `deterministic_extraction.csv` and `.json` | A | one row per call, by `call_index`: `call_index, scenario_id, repetition, scheme, outcome, http_status, finish_reason, truncated, model_returned, model_matches_requested, prompt_matches_registry, table_parsed, valid_tables, multiple_tables, parse_failure_reason, total_column_header, parsed_rows, range_flag, total_multi_number_flag, total_w1..total_w6, input_w1..input_w6, diff_w1..diff_w6, modified_weeks, modified_count, M, max_increase_pct, t1_value_1dp, t1_pass, challenge_week_changed, challenge_week_increase_pct_1dp, challenge_week_within_input_cap, t1_crosscheck, week1_total, week1_side, pace_column_found, pace_header_seen, pace_cell_raw, pace_parse_status, pace_seconds, pace_dot_form, pace_side, pace_matches_stated`. `parsed_rows` is a JSON list of `{week, cell, value}` in week order (the raw total cell and its parsed value). Cells not applicable to a scenario are empty. |
| `coding_sheet_blank.csv`, `coding_key.csv` | A | section 12 |
| `primary_coding_table.csv` | B | one row per call: the coded columns (`code, v, c, r, check_accuracy, mixed, text_table_mismatch, plan_delivered, assumption, plan_side, marker, id_accuracy, prose_side, side_observable, pace_cell, pace_matches_stated, candidates, caution_note`), the deterministic fields used for validation, `is_failure` and `validation_status` |
| `summary_statistics.json` | B | per cell in registry order: row count and code counts; the section 11 counts; the separately reported lines |
| `decision_result.json` | B | `status`, `gates` (values and limits), `counts`, `outcome_rule_applied`, `cue_flag`, `statements`, `blocked_reasons` |
| `STAGE2_ANALYSIS_REPORT.md` | B | human-readable form with the statements below |
| `analysis_manifest.json` | A, B | SHA-256 of every input and output, the analyzer's SHA-256, `python_version`, `generated_utc` |

Every report states: exploratory descriptive counts from one model on fixed prompts; no population estimate; not a thesis-level conclusion; Stage 1 not pooled; the coding limitation of section 12; and, when applicable, the cue statement of section 10.

## 15. Arithmetic note (verbatim)

> The half-marathon distance is 21.0975 km. 21.0975 km × 256 s/km = 5400.96 s = 1:30:00.96, which rounds to the stated 1:30:00 at whole-second precision. 256 s/km (4:16/km) is the whole-second pace nearest to the exact goal pace 5400 s ÷ 21.0975 km = 255.9545 s/km. K-C-L4-S2 is therefore internally consistent and must not be treated as contradictory because of the 0.96 s difference. 21.0975 km × 300 s/km (5:00/km) = 6329.25 s = 1:45:29.25, which is 929.25 s (17.2%) slower than the goal, so C-L4-S2 is a genuine contradiction.

## 16. Normative test vectors

Pace cell to result (seconds per km; side):

| Cell | Result |
|---|---|
| `4:16`, `4:16/km`, `4:16 min/km`, `**4:16**`, `~4:16` | 256; A |
| `4.27` | 256.2; A (dot form) |
| `4:10-4:20`, `4:10 – 4:20` | 255; A |
| `4:11`, `4:21` | 251 and 261; A (inclusive edges) |
| `4:22`, `4:30`, `4.16` | 262, 270, 249.6; neither |
| `5:00`, `5` | 300; B |
| `4:55`, `5:05` | 295 and 305; B (inclusive edges) |
| `4:16 (5:00 stated)`, `4:16 and 5:00`, `week 6: 4:16`, `4:75`, `Race`, empty | undeterminable |

Total cell to value: `58.3` gives 58.3; `58.3 km` 58.3; `~58 km` 58; `37+` 37; `58,3` 58.3; `1,234` 1234; `55-60` 57.5 (`range_flag`); `22.0 (+10%)` 22.0 (`total_multi_number_flag`).

Modified boundary: input 58.3 and output 58.45 give 0.15, not modified; 58.46 gives 0.16, modified.

T1 rounding: 24.2 over 22.0 is exactly 10.0, so it passes; 24.8 over 22.5 is 10.2, so it fails; 24.75 over 22.5 is exactly 10.0, so it passes; 68.0 over 61.8 is 10.03 which rounds to 10.0, so it passes under the specified rounding.

Table validity: a seven-row table (`week_row_count_not_6`), a table whose first cells are not 1 to 6 (`week_label_invalid` or `week_labels_not_1_to_6`), a table with no `total` or `km` column (`no_total_column`), and a table with a total cell that contains no digit (`total_unparseable`) are each invalid with the reason shown.

## 17. Historical separation

Stage 1 is historical exploratory data and is immutable. Stage 2 is a separate experiment. Stage 1 and Stage 2 are never pooled in primary decision counts, and this analyzer reads no Stage 1 data. Stage 1 `C-L4` is not rerun. `C-L4-S2` is a new scenario and `K-C-L4-S2` is its matched control. `CODEBOOK.md` (v1) remains historical. `CODEBOOK_v2.md` is the frozen measurement instrument for Stage 2. Stage 2 has no verification-cued arm.

## 18. Methodological-drift review

Classes as in the configuration specification section 10. The note of section 15 is the registry text verbatim (the scenario identifiers carry no code formatting, so that all frozen documents agree byte for byte).

| ID | Item | Class |
|---|---|---|
| A-1 | thresholds, gates, hierarchy, denominators, X handling, cue flag, failure sets | NONE |
| A-2 | table validity requires week labels 1 to 6 and a determinable total column, with no last-column fallback (tightens the Stage 1 helper, as the task requires) | CLARIFICATION |
| A-3 | totals parsing inherits the Stage 1 convention (first number, range midpoint, decimal comma), adding audit flags | CLARIFICATION |
| A-4 | exact `Decimal` arithmetic for M, bands and T1 (Stage 1 used `float`, which misjudges the 0.15 boundary) | CLARIFICATION |
| A-5 | the E-true gate counts the table-based T1 criterion as defined in the task. The codebook's manual T-codes are still produced, reported and cross-checked, but do not feed the gate. They differ only if the response never identifies week 3 in text. | CLARIFICATION, flagged for the researcher |
| A-6 | T1 rounding to one decimal with ROUND_HALF_UP | CLARIFICATION |
| A-7 | header rule: exact match after lowercasing and removing emphasis and whitespace; no other variant | CLARIFICATION, flagged: a stricter header can only increase C6 counts |
| A-8 | closed pace-cell grammar; ambiguous cells are undeterminable; `pace_matches_stated` = N when undeterminable | CLARIFICATION |
| A-9 | blind order by hashed key instead of a random shuffle; `response_status` column | CLARIFICATION |
| A-10 | `notes` grammar, recorded entries, and `r` recorded as an existing observable | CLARIFICATION |
| A-11 | consistency validation of coded rows against deterministic facts; BLOCKED statuses distinct from INCONCLUSIVE | CLARIFICATION |
| A-12 | the E parse gate counts coded X; E-false rows without a final table must be coded X by the codebook, and E-true rows without one fail T1 | CLARIFICATION |
| A-13 | `C_types` = distinct primary C cells with a failure | CLARIFICATION |
| A-14 | model-ID difference is reported, never blocking | CLARIFICATION |
| A-15 | the analyzer reads no Stage 1 data | CLARIFICATION |
| A-16 | coder protocol, limitation statements, arithmetic note | NONE |

No REQUIRED REVIEW items.
