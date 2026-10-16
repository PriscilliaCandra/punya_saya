# Stage 2 Runner Specification

**Status: FROZEN specification (design only).** It specifies the future runner `pilot_clarification/run_stage2.py`. That file does not exist yet. The Stage 1 runner `run_pilot.py` is Stage-1-locked, its hash is recorded in the Stage 1 manifest, and it is not edited. No experiment has been run and no API call has been made.

Precedence and bound inputs are those of `stage2_config_specification.md` section 0. The runner is bound to `CODEBOOK_v2.md` (SHA-256 `177a1c5d9b7dbf1ab9e53d0684365dcf67b21f1b1f3154f3f8b1ecc5aa6eb4fc`), the Stage 2 registry (file `51895ee5329059930959f15746439f692bb849521de346099a1838be7689f5c7`, canonical `c0e9447bb50911f3f7bc33f8fa1d0bda85c909ed39ba82eaa01a1e398a41e76b`) and `stage2_prompt_specification.md` (`5d88b1e57557d9fb8ba67d9623972d3420953e9e3f28961e0dfed401b3637a80`).

## 1. Scope

The runner performs exactly one thing: it sends the 40 frozen prompts, in the frozen order, to one model, one at a time, and preserves every response. It never analyzes, codes, scores or classifies a response. It has these modes:

| Mode | Purpose | Network | Counts as a run |
|---|---|---|---|
| live | the Stage 2 experiment | yes (generation only) | yes |
| dry run (`--dry-run`) | pipeline test with a mock provider | none | no |
| `--list-models` | audit-only read of the provider's model list (one metadata request, no generation) | one GET | no |

`--list-models` exists only for the pre-run audit, needs its own explicit approval, is never part of a run, and is never counted toward the 40 calls.

Live invocation requires `--provider gemini`, `--model gemini-3.1-flash-lite` (it must equal the configuration), and the operator typing exactly `RUN 40` at the confirmation prompt. Any other input aborts with nothing called.

## 2. Preflight

All checks are offline. They run before any run directory is created and before any API call. **If any check fails, the runner prints the failures and exits non-zero without creating a run directory and without calling the API.** No check prints a secret.

| # | Check |
|---|---|
| 1 | `CODEBOOK_v2.md` exists and its SHA-256 equals the bound value |
| 2 | the Stage 2 registry exists and its file SHA-256 and canonical SHA-256 equal the bound values |
| 3 | `stage2_prompt_specification.md` exists and its SHA-256 equals the bound value |
| 4 | the registry contains exactly 8 scenarios, in the registry order |
| 5 | each scenario has exactly 5 repetitions |
| 6 | total planned calls = 40, equal to the hard cap |
| 7 | each scenario's `prompt_sha256` equals the SHA-256 of its `prompt` |
| 8 | each reused Stage 1 prompt (E-F-A, E-F-B, K-E-TRUE, C-L2, C-L3) equals the string in the Stage 1 registry file byte for byte, and its hash equals the Stage 1 value recorded in the registry |
| 9 | the registry has exactly the eight approved top-level keys; no key anywhere has a name matching `seed`, `timestamp`, `_utc`, `date`, `created`, `started`, `ended`, `mtime`, `run_id`, `call_index`, `calls_made` or `status`; and no string value matches a date or time pattern (`\d{4}-\d{2}-\d{2}`, `\d{8}T\d{6}`, or a standalone 8-digit number). The descriptive `design.shuffle_policy` text is permitted: it holds no seed value. |
| 10 | the model ID given on the command line equals the configuration's `model_requested` |
| 11 | the environment variable `GEMINI_API_KEY` exists and is non-empty (live mode only). Its value is never printed. |
| 12 | the realized order reconstructed from the registry, the seed and the algorithm equals the stored `call_order`, and its serialization hash equals `call_order_sha256` |
| 13 | no existing Stage 2 live run would be overwritten or duplicated (section 9) |
| 14 | the configuration passes the loader validation of the configuration specification section 7, including the exact Python version |
| 15 | the codebook freeze manifest hash, the Stage 1 registry canonical hash and the post-implementation bindings (the runner's own SHA-256 and the analyzer's SHA-256) equal the configuration's values (live mode) |
| 16 | the target run directory does not exist |

Checks 14 to 16 are additions that follow from the configuration bindings.

## 3. Run initialization

After preflight and a correct confirmation phrase, the runner creates the run directory exclusively, then writes the static files, then starts the call loop.

```text
runs/<run_id>/
  manifest.json            static header, written once before the first call, never rewritten
  config_used.json         byte-identical copy of the frozen configuration
  scenario_registry.json   byte-identical copy of the frozen Stage 2 registry
  integrity/
    preflight.json         result of every preflight check (no secrets)
    call_order.csv         the 40-line serialization of the realized order
    postrun.json           written after the last call (section 8)
  calls.jsonl              append-only; one terminal record per attempted call
  raw/
    <NN>_<scenario_id>_r<rep>.json   one file per call, created exclusively
  STAGE2_COMPLETE          written last, only for a complete run
```

`run_id` = `stage2_gemini_<UTC %Y%m%dT%H%M%SZ>`; a dry run uses `dryrun_stage2_<provider>_<UTC>`. This follows the Stage 1 naming convention. Runs live under `pilot_clarification/runs/`.

Raw response data and metadata are separate. `raw/` and `calls.jsonl` hold response data and call metadata. `manifest.json`, `config_used.json`, `scenario_registry.json` and `integrity/` hold run-level metadata and never contain response text.

**`manifest.json` (static)** contains: `run_id`, `stage` = 2, `dry_run`, `provider`, `model_requested`, `registry_version`, `planned_calls`, `repetitions`, `scenarios`, `shuffle_seed`, `call_order_sha256`, `settings` (max output tokens, temperature policy, system prompt = null, retries = 0, timeout, delay), the bound hashes, the runner's own SHA-256, the `config_sha256`, `python_version`, `platform` and the HTTP client version, and `started_utc`. It has no counters and no end time.

## 4. Execution loop

For `call_index` in 1..40, in the stored order:

1. Check the loop invariants. If any fails, abort (section 7): the index equals the expected one; the `(scenario_id, repetition)` equals the stored order entry; the scenario's registry prompt hash recomputes; no record or raw file for this index exists yet; fewer than 40 attempts have been made.
2. Record `timestamp_utc` (call start). Send exactly the request of the configuration specification section 2, with the registry prompt.
3. Classify the outcome (section 6). Record `completed_utc` and latency.
4. Build the call record (section 5). Write the raw file exclusively, append the same record to `calls.jsonl`, and flush and fsync both. If either write fails, abort.
5. Sleep the configured delay (1.0 s), also after the last call.

There is no concurrency, no reordering, no skipping, no retry and no re-sending.

## 5. Per-call record

The same object is written to `raw/<NN>_<id>_r<rep>.json` (pretty-printed) and to `calls.jsonl` (one compact line). `ensure_ascii` is off.

| Field | Content |
|---|---|
| `call_index`, `scenario_id`, `scenario_number`, `repetition` | position and identity |
| `run_id`, `provider`, `model_requested` | |
| `model_returned` | provider-reported model (`modelVersion`) or null |
| `timestamp_utc`, `completed_utc` | call start and end, UTC, seconds precision |
| `prompt_sha256`, `prompt` | the registry hash and the exact text sent |
| `http_status` | integer or null |
| `response_text` | concatenation of the non-`thought` text parts of the first candidate (as in Stage 1); empty string if none |
| `response_text_sha256` | SHA-256 of `response_text` (UTF-8) |
| `response_json` | the full provider JSON on HTTP 200, otherwise null |
| `finish_reason` | provider finish reason or null |
| `truncated` | true iff the lowercased `finish_reason` is one of `max_tokens`, `length`, `max_output_tokens` |
| `usage` | provider token-usage object or null |
| `latency_ms` | integer |
| `outcome` | `ok`, `http_error`, `no_candidates` or `exception` |
| `error` | redacted error text or null |
| `settings` | the settings of the manifest (never a key) |
| `registry_version`, `config_sha256`, `registry_file_sha256`, `codebook_sha256` | reference hashes |

The API key, request headers and any credential never appear in any record.

## 6. Failure behavior

| Outcome | Definition |
|---|---|
| `ok` | HTTP 200 and at least one candidate |
| `http_error` | HTTP status other than 200; error text redacted and cut to 2000 characters |
| `no_candidates` | HTTP 200 with no candidates; error text states it |
| `exception` | network, timeout or JSON error; error text is the redacted `Type: message` |

All four are terminal and are recorded. There are **zero retries**, no automatic substitution to another model, no automatic prompt modification and no change of the call order.

**Frozen execution policy.** After an individual call failure the runner records it and **continues with the next scheduled call**. This is the Stage 1 behavior and is what the frozen design presupposes, because API-error rows stay in their denominators and are never counted as failures. The runner stops only on an integrity-state violation, an unwritable log, the hard cap, or an operator interrupt. It does not halt after a number of consecutive errors; adding such a rule would be a new decision. Its consequence is noted in section 10.

**Integrity-state violation** (abort before the next call): a loop invariant fails, a file that must not exist exists, a record or raw write fails, the realized order no longer matches the stored one, or a prompt hash fails to recompute.

## 7. Incomplete runs

An incomplete run is never resumed or completed by the runner. It is represented as follows.

| State | Evidence |
|---|---|
| in progress | `manifest.json` exists; `calls.jsonl` has fewer than 40 lines; no `postrun.json`; no marker |
| `ABORTED_INTEGRITY` | `integrity/postrun.json` with that status and the reason, if it could be written; no marker |
| `ABORTED_OPERATOR` | `integrity/postrun.json` with that status, if it could be written; no marker |
| `COMPLETE` | `postrun.json` with status `COMPLETE` and the marker (section 8) |

The absence of `STAGE2_COMPLETE` means the run is incomplete, whatever else exists. A call that was in flight at an abort has no terminal record. The analyzer never analyzes an incomplete run for primary results. Replacing or continuing an incomplete run needs a separately approved run identity, which this document does not design.

## 8. Completion

After the 40th terminal record the runner writes `integrity/postrun.json`, then the marker last. A run is complete only if all hold:

- `calls.jsonl` has exactly 40 lines, `raw/` has exactly 40 files, and their records are identical;
- every `call_index` 1..40 appears exactly once, and each record's `(scenario_id, repetition)` equals the stored order at that index;
- each of the 40 `(scenario_id, repetition)` pairs appears exactly once (no duplicate, none missing), and each scenario has 5;
- every record's prompt hash equals the registry value;
- every record has a terminal `outcome`;
- the realized order still reconstructs to the stored order.

**`integrity/postrun.json`** contains: `status` (`COMPLETE`, `ABORTED_INTEGRITY` or `ABORTED_OPERATOR`), `reason`, `calls_attempted`, `calls_terminal`, outcome counts, finish-reason counts, `truncated_count`, the sorted set of `model_returned` values, the reconciliation results above, the SHA-256 of every file in the run directory except itself and the marker, `readonly_applied`, and `ended_utc`.

**`STAGE2_COMPLETE`** contains the UTC time and the SHA-256 of `integrity/postrun.json`. It is written only after `postrun.json`, and only if the status is `COMPLETE`. Afterwards the runner sets the raw files, `calls.jsonl`, `manifest.json` and `integrity/` read-only and records whether it succeeded in `postrun.json` (`readonly_applied`).

## 9. One live run

Preflight check 13 aborts if any previous Stage 2 live run directory (`dry_run` false) exists whose `manifest.json` has the same `config_sha256` and whose `calls.jsonl` holds at least one record, whether the run is complete or not. There is no override option. A dry run never counts, and it never counts as data. No second-live-run mechanism is designed here.

## 10. Observations (no methodological change)

- **Systemic errors.** Because the runner continues after failures, a systemic provider problem (wrong model ID, rejected key) would turn all 40 scheduled calls into error rows. The frozen gates would then give INCONCLUSIVE, and section 9 would block another live run under the same configuration. The mitigation is operational, not methodological: the pre-run audit confirms the model ID with `--list-models` and runs the mock dry run before any live call.
- **Operator interrupt.** Stopping a live run midway leaves an incomplete run (section 7).

## 11. Dry-run mode

A dry run uses a mock provider (`model_returned` = `mock-model`, `dry_run` = true), makes no network request, needs no key, writes only to a `dryrun_` directory, never writes `STAGE2_COMPLETE` as a completed live run, and its output is never data. The analyzer refuses to take a dry-run directory as primary input. The mock responses exist only to exercise the pipeline.

## 12. The runner must never

contact any host other than the provider endpoint, send any field beyond the frozen request, alter a prompt, reorder or skip a call, retry, resume, choose or change the seed, read or write Stage 1 artifacts (it only reads the Stage 1 registry file for check 8), write outside `pilot_clarification/runs/<run_id>/`, analyze or classify a response, or store or print a secret.

## 13. Historical separation

Stage 1 is historical exploratory data and is immutable; Stage 2 is a separate experiment; the two are never pooled in primary decision counts; Stage 1 `C-L4` is not rerun; `C-L4-S2` is new and `K-C-L4-S2` is its matched control; `CODEBOOK.md` (v1) remains historical; `CODEBOOK_v2.md` is the frozen measurement instrument; Stage 2 has no verification-cued arm.

## 14. Methodological-drift review

| ID | Item | Class |
|---|---|---|
| R-1 | the 13 required preflight checks | NONE |
| R-2 | preflight checks 14 to 16 (configuration validity, bound hashes, directory not existing) | CLARIFICATION |
| R-3 | frozen execution policy: record the failure, continue, no retry (the Stage 1 convention and the frozen fixed-denominator rule) | CLARIFICATION |
| R-4 | no halt after consecutive errors; consequence noted in section 10 | CLARIFICATION |
| R-5 | run directory layout, `integrity/` folder, static manifest, completion marker written last | CLARIFICATION |
| R-6 | one live run per configuration, including an incomplete one; no override | CLARIFICATION |
| R-7 | dry-run mode with a mock provider, as the decision record's pre-run audit prescribes | NONE |
| R-8 | `--list-models` as an audit-only mode; confirmation phrase `RUN 40` (Stage 1 used `RUN 30`) | CLARIFICATION |
| R-9 | no resume; incomplete runs are never analyzed for primary results | CLARIFICATION |

No REQUIRED REVIEW items.
