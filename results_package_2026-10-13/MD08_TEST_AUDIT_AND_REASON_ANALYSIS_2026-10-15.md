# MD-08: audit of the process-death contract tests, analysis of `URLError.reason`, 14-class re-audit, blocker map (2026-10-15, audit round)

Changes no policy and no record entry. Entries 12.40, 12.41 and 12.42 are untouched. `HTTP_STATUS_ALLOWLIST` and `RATIFIED_TRANSPORT_ERROR_CLASSES` are empty (read from the module on 2026-10-15); `PROCESS_DEATH_CONTRACT_ENFORCED = True`; the gate is CLOSED. No class is ratified (0 of 14). No resume is allowed.

## 1. Baseline (verified, not taken from the earlier summaries)
HEAD `224d910`; 0 staged files; `.env` absent; entries 12.40, 12.41, 12.42 present. Hashes at the start equal the ones reported in the previous round for `s10_resume.py` (`eaa0d092...1b5`), `test_resume.py` before this round (`f74bdfce...873e51`), the decision record (`8e79b603...ddb9`), the gap report, audit file, answer table, package, checklist and template. `s10_runner.py`, `s10_integrity.py`, `s10_scoring.py` unchanged.

## 2. Contract test matrix
Legend. **Mode**: *PROD* = shipped constants, nothing ratified; *TEST-ONLY set* = contract enforced, ratified set `{"TimeoutError"}` (a stand-in, NOT a ratification, so the test proves the mechanism and not production eligibility); *MECH* = `Base` class, contract switched off and TEST-ONLY set (reconcile/chain/lock machinery only). "Enforced" = `PROCESS_DEATH_CONTRACT_ENFORCED` during the test. All results below were observed in the run of this round (54 tests in `test_resume.py`, OK).

| Contract condition / requested scenario | Test(s) (file `test_resume.py` unless noted) | Mode | Enforced | Observed | Gap | Action |
|---|---|---|---|---|---|---|
| 1 ledger chain, hash chain invalid | `TestProcessDeathContract.test_negative_damaged_files` [corrupt ledger chain] | TEST-ONLY set | yes | ResumeRefused | asserts only the exception type, not the reason text | optional: assert the text (not done) |
| 2a raw file missing / corrupt | same test [missing raw file], [corrupt raw file] | TEST-ONLY set | yes | ResumeRefused | same as above | same |
| 2b raw disagrees with `calls.jsonl` | **NEW** `TestProcessDeathContractGaps.test_calls_jsonl_that_disagrees_with_the_raw_record_is_refused` | TEST-ONLY set | yes | refused, reason mentions `calls.jsonl` | none | done |
| 3 intent without raw result | `test_negative_intent_without_a_raw_record`; also `TestResumeAfterProcessInterruption.test_intent_without_a_persisted_record...` | TEST-ONLY set / MECH | yes / no | refused "attempted, no record" | none | done |
| 4 last result is a success | `test_negative_trailing_successful_record`, `..._success_after_an_earlier_failure` | TEST-ONLY set | yes | refused "not an SF1-only transport failure" | none | done |
| 5 HTTP status present | `test_negative_trailing_sf1_with_an_http_status`; unit `TestHttpAndClassPolicy.test_every_http_status_is_rejected_even_for_a_ratified_class` (20 statuses) | TEST-ONLY set | yes | refused | none | done |
| 6 class not ratified | `test_negative_unratified_class` (ConnectionResetError), `test_default_without_any_ratified_class...` | TEST-ONLY set / **PROD** | yes | refused | none | done |
| 7 mixed or contradictory SF flags | `test_negative_mixed_sf_flags` (SF1+SF3); unit tests (SF1+SF4, text present, no error) | TEST-ONLY set | yes | refused | none | done |
| 8a `RUN_COMPLETE`, two markers | `test_negative_markers` | TEST-ONLY set | yes | refused "COMPLETE" / "two status markers" | none | done |
| 8b marker contradicting the ledger | **NEW** `test_a_marker_that_contradicts_the_ledger_is_refused` | TEST-ONLY set | yes | refused "does not match the ledger" | none | done |
| 8c cost stop | **NEW** `test_a_cost_stopped_run_is_refused_under_the_production_configuration`; older `TestCostStop` (MECH) | TEST-ONLY set / MECH | yes / no | refused "cost stop" for both bases; records carry no SF1 flag | none | done |
| 9 lock active | **NEW** `test_an_active_run_lock_blocks_the_resume_...` (with a control: the same authorization succeeds once the lock is free); older adversarial test (run alive) | TEST-ONLY set / MECH | yes / no | refused "in progress" | none | done |
| 10 stale ledger head | `test_negative_stale_head_wrong_run_...` [stale head] | TEST-ONLY set | yes | refused "current ledger head" | none | done |
| 11 authorization reused | `test_negative_duplicate_authorization` | TEST-ONLY set | yes | refused | the refusal observed is "COMPLETE" (the run is finished); the property "an authorization is consumed" is carried by the head binding: every resume appends ledger entries, so the old head can never match again (covered by the stale-head case). No test reuses an authorization on a run that is still incomplete | accepted; a direct test needs a run that stays incomplete after a resume |
| 12 `trailing_transport_failures` inconsistent | `..._wrong_count`, bool count, **NEW** `test_trailing_count_must_equal_the_stored_evidence_exactly` (0, 1, 3, -2, 2.0, "2", None against 2) | TEST-ONLY set | yes | all refused | none | done |
| 12b `failure_cause` wrong / missing, run id wrong, advisor, malformed JSON | `test_negative_stale_head_wrong_run_wrong_cause_...` | TEST-ONLY set | yes | all refused | none | done |
| 13 crash while a call is running | `test_negative_intent_without_a_raw_record` (crash at call 4) and **NEW** `test_a_crash_during_a_call_gives_no_credit_from_an_earlier_transport_failure` (call 4 transport failure, crash during call 5) | TEST-ONLY set | yes | refused "attempted, no record" | none | done |
| positive path | `test_positive_after_a_persisted_transport_failure_with_a_test_only_class`, `..._two_trailing_failures...` | TEST-ONLY set | yes | RUN_COMPLETE, `verify_run` clean | proves the mechanism only | cannot become a production test until the owner ratifies a class |
| production state | `TestHttpAndClassPolicy.test_the_shipped_policy_is_empty`, `test_nothing_is_transport_only_while_no_class_is_ratified` (all 14), `test_a_main_run_halt_is_refused_while_no_class_is_ratified`, `test_default_without_any_ratified_class_the_death_after_a_transport_failure_is_refused` | **PROD** | yes | refused / empty | none | these are the only tests of the shipped policy |

Statement of what is VERIFIED: the contract's checks refuse each listed scenario in the production configuration (enforced), using the TEST-ONLY set whenever a state with a transport failure was needed so that the refusal can be attributed to the condition tested. NOT VERIFIED: any positive resume under real policy (none exists), real provider behaviour, concurrency beyond the OS lock test, Windows-specific power-loss behaviour.

## 3. `URLError.reason`: findings (offline; constructed objects and a local-only socket probe; no DNS, no provider)
- **Where it is lost.** `urllib` wraps connect and send errors (`OSError`) into `URLError(err)`; `GeminiProvider.generate` and `execute_call` then store only `type(e).__name__` (`s10_runner.py`, `except Exception as e` in `generate`, and in `execute_call`). So for every connect-phase failure the record says `URLError` and nothing else; `reason` (an exception object) is dropped.
- **What `reason` carries.** Constructed examples: `gaierror` with errno 11001; `ConnectionRefusedError` errno 10061; `TimeoutError` (no errno); `SSLCertVerificationError` errno 1; `FileNotFoundError` errno 2. Observed once on the real stack (local probe, closed port on this Windows host): `URLError` with `reason` `TimeoutError`, i.e. even a refusal can present as a timeout, so the reason class alone does not prove a transient network loss.
- **What it can tell apart.** Its class and errno separate DNS (`gaierror`), refusal (`ConnectionRefusedError`), timeout, TLS verification (`SSLCertVerificationError`) and local file/config errors (`FileNotFoundError`, an unreadable CA path). Without it, TLS interception or a bad CA path looks identical to a network blip.
- **Sensitivity.** `str(reason)` is free text: it can hold host names (`Hostname mismatch ... 'internal.example'`), IP addresses, and file system paths (a local user name in a CA path). It must not be stored raw. (Constructed examples above contain such strings.)
- **Minimum safe representation (design, NOT implemented).** Two new record fields, both from closed vocabularies: `error_reason_class` = the class name of `reason` if it is in a fixed list (the 14 audited names plus `SSLCertVerificationError`, `FileNotFoundError`, `PermissionError`, `OSError`), else the literal `"other"`; `error_reason_errno` = `reason.errno` if it is an int, else null. Never `str(e)`, never `args`, never `filename`.
- **What would change if the owner approves.** (a) Code: `generate` and `execute_call` in `s10_runner.py` (write the two fields); `is_transport_only`/the contract would then be allowed to key on the reason class for `URLError`. (b) Record schema: the raw record gains two keys; `s10_integrity.py` has no fixed key list (checked by grep), `calls.jsonl` is the same bytes as raw, so no format migration, but all raw-record hashes in any new run include the fields; no existing run is affected (none exists). (c) Hashes: `s10_runner.py` hash changes, hence the P13 list and the final freeze manifest; the Step 8 build and the Step 7 freeze are not touched. (d) Tests: runner test that a `URLError(gaierror)` produces the fields and no free text; scoring unchanged (still `error` set -> SF1); a resume test with `URLError` + reason class. (e) Is it a pure implementation fix (spec 13.6)? It changes executable code only (H1 plausible), but it changes the stored record, so H2 ("request bytes, parsed verdicts, UNP flags, scores byte-identical") must be shown for the fields that matter, and the raw record bytes are NOT byte-identical, so the owner must state whether raw-record content is inside H2's scope. If it is, this is not a pure fix and needs an FZ decision. Before the code freeze the question can be settled as an ordinary change; after the freeze it needs H1-H4 evidence or a new FZ version. Whether it also needs a re-pilot: not decided here.
- **Tests designed (offline, not written because no code change is made this round).** (1) generate-path unit test with a stub raising `URLError(socket.gaierror(...))` expecting `error_reason_class == "gaierror"`, errno set, no host name in the record; (2) free-text test: reason with a path in `filename` leaves no path in the record; (3) closed-vocabulary test: unknown class -> `"other"`; (4) HTTP errors unchanged.
- **Limit.** All of this is about the stdlib path on this machine (Python 3.11.9). It says nothing about how the real provider behaves.

## 4. 14 classes: re-audit against the constants and the exception path
Verified by script: `TRANSPORT_ERROR_CLASSES` has exactly 14 names and equals the 14 rows of `MD08_EXCEPTION_AUDIT_2026-10-15.md`. Ratified: 0 of 14 (`RATIFIED_TRANSPORT_ERROR_CLASSES` empty; `is_transport_only` is False for every name, tested). Origin for all: the `except Exception` of `generate`/`execute_call` stores `type(e).__name__`; urllib wraps connect/send errors into `URLError`, so only getresponse/read-phase names appear raw. Statuses are unchanged from the audit file; this round adds the extra evidence needed:

| Class | Raw name reachable on the real path? | Evidence available | Status | Extra evidence needed | Recommendation to the owner (not a decision) |
|---|---|---|---|---|---|
| TimeoutError | yes (read phase; connect phase via URLError) | local probe: silent server | CANDIDATE | none for the name; ambiguity connect/read remains | may ratify if the owner accepts that a timeout may follow provider-side processing |
| timeout | no on Python 3.11 (alias of TimeoutError) | stdlib | REJECT | n/a | do not ratify |
| URLError | yes (all connect/send failures) | `reason` discarded | NEEDS_EVIDENCE | stored reason class/errno (section 3) | do not ratify as is |
| ConnectionError | no (only subclasses are raised) | stdlib MRO | REJECT | n/a | do not ratify |
| ConnectionResetError | yes (read phase) | local probe: RST after request | CANDIDATE | none for the name | may ratify |
| ConnectionAbortedError | possible (Windows local aborts) | none | NEEDS_EVIDENCE | host-side evidence that it is not local software | hold |
| ConnectionRefusedError | not expected raw (wrapped) | probe showed URLError | REJECT | n/a | do not ratify |
| BrokenPipeError | not expected raw (send is wrapped) | none | NEEDS_EVIDENCE | a raw occurrence or the reason field | hold |
| RemoteDisconnected | yes (getresponse) | local probe: close without reply | CANDIDATE | none for the name | may ratify |
| IncompleteRead | yes (read) | local probe: truncated body | CANDIDATE | none for the name; usage unknown (cost bound applies) | may ratify with the cost note |
| gaierror | not expected raw (DNS inside connect) | not probed (needs network) | REJECT | n/a | do not ratify |
| SSLError | broad base | stdlib MRO | REJECT | n/a | do not ratify |
| SSLEOFError | on read only | none | NEEDS_EVIDENCE | a raw occurrence or reason field | hold |
| SSLZeroReturnError | on read only | none | NEEDS_EVIDENCE | same | hold |
Local probes do not prove provider behaviour; the real-provider path is NOT RUN.

## 5. Independent blocker map
Classes: OWNER_ACTION, ADVISOR_ACTION, RESEARCHER_EVIDENCE, SAFE_OFFLINE_WORK, DEPENDENCY_BLOCKED. Status checked in the repository on 2026-10-15 (`human_evidence/` holds only `rehearsal/`; no `clock/`; no `step9_evidence.json`; no authorization file).
| Blocker | Class | Status | What exists | What is needed |
|---|---|---|---|---|
| Per-class ratification | OWNER_ACTION | 0/14 | audit + draft entry | entry per class |
| `URLError.reason` change | OWNER_ACTION | not decided | design in section 3 | approve/refuse; scope of H2 |
| P13 owner-record entry | OWNER_ACTION | not written | patch applied, test passes, draft entry (gap report U3) | write |
| MD-03/K2, PG11b, D3, D5, MD-10 | OWNER_ACTION (MD-10, D3 also ADVISOR_ACTION) | undecided | package rows, conflicts C-08/C-09 | answers; rebuild if K2/narrowing |
| Advisor notice + Q1-Q5, H4 stop-rule, PG3 review | OWNER_ACTION (send) then ADVISOR_ACTION | notice unsent; no answer | draft updated in gap report U4 | send; answers in writing |
| R1 | RESEARCHER_EVIDENCE | not recorded | template (not evidence) | true UTC time note |
| H1 blind check | RESEARCHER_EVIDENCE | not done | blank worksheet, evaluator tests | filled worksheet + `evaluation.json` |
| Seven-day wait | DEPENDENCY_BLOCKED | not started | FZ-v1 row 19 rule | R1 |
| H3 `step9_evidence.json` | DEPENDENCY_BLOCKED | not created | evaluator | H1, wait, H4 stop-rule clearance, owner confirmation |
| H4 rehearsal classification | RESEARCHER_EVIDENCE (+ ADVISOR_ACTION) | open | comparison + findings files | researcher classification, advisor answers |
| PRD-6 / H7 / MD-09 | OWNER_ACTION | not declared | none | declaration |
| MD-02 | OWNER_ACTION | working decision | template values | confirmation |
| H5 pilot authorization | OWNER_ACTION (DEPENDENCY_BLOCKED on MD-02) | none | empty template | owner-written new file |
| Price/model re-read | OWNER_ACTION / RESEARCHER_EVIDENCE | due on pilot day | FZ-v1 prices | dated note on the day |
| API key / terminal | OWNER_ACTION | not done | none | owner sets it in the terminal, never in a file |
| 31-file hashes + code freeze | DEPENDENCY_BLOCKED | not declared | P13 list applied | after all code-affecting decisions; then full `run_all_checks` and hash record |
| SAFE_OFFLINE_WORK | done this round | the test additions (6 tests) and this analysis; nothing else is safe to do without a decision | | |

## 6. Test results of this round (all offline, no provider)
| Command | Exit | Count | Result |
|---|---|---|---|
| `python -B -I -W ignore -m unittest discover -s research_design/step10 -p "test_*.py"` | 0 | 216 | OK |
| same with `-p test_resume.py` | 0 | 54 | OK (was 48; +6 gap tests) |
| same with `-p test_step11_file_list.py` | 0 | 2 | OK |
| `python -B -I results_package_2026-10-13/reproduce/run_all_checks.py --quick` | 0 | 23 checks OK | ALL CHECKS AS EXPECTED; gate check exit 2 = CLOSED (expected) |
| `python -B -I research_design/step10/s10_runner.py --scope pilot_round_1 ...` with absent evidence/authorization | 2 | - | `GATE CLOSED` (missing Step 9 evidence; missing owner authorization); no output folder created |
| full `run_all_checks.py` with the slow Step 8 suite | - | - | NOT RUN this round (ran in the previous round, 24 OK, before this round's test-only change) |

## 7. State summary
- ADOPTED (12.42): empty HTTP list, process-death contract text, manual H1-H3, audit of 14. IMPLEMENTED: all of these in `s10_resume.py` (unchanged this round). VERIFIED: refusals listed in section 2 and the mechanism under TEST-ONLY set. NOT VERIFIED: positive resume under production policy (impossible, 0 ratified), provider behaviour, H1-H3 truth, `URLError.reason` design (not implemented).
- Gate CLOSED; code freeze not declared; no final freeze manifest.

---
# ADDENDUM (post-audit round, 2026-10-15). Adds to sections 2, 5 and 6; changes no policy, no record entry and no production constant.

## A1. Adversarial review of `_process_death_contract`
- **F1 (finding, behaviour NOT changed).** The contract inspects only the TRAILING persisted records. A run with an earlier non-transport failure (for example an HTTP 500 on call 2) and a trailing ratified timeout passes the evidence rule, whereas the halt path (`prepare_resume`, `bad` list) requires EVERY structural failure in the run to be transport-only. The two paths are therefore not equally strict. Confirmed by a characterization test (`test_finding_F1_current_behaviour_...`; it documents the code as it is and is expected to change if the owner decides). Owner decision needed: (a) keep (trailing-only, as 12.42 A2 condition 2 literally says), or (b) also require that no earlier call in the run is a non-transport structural failure. Option (b) is stricter and matches the halt path; it is a one-condition change in `_process_death_contract` plus tests.
- **F2 (observation).** `execute_call` also stores `type(e).__name__` for an exception raised by the provider adapter itself, so an adapter bug that raises `TimeoutError` would be indistinguishable from a real timeout. This is a reason to keep ratification narrow; no code change proposed.
- **F3 (observation).** The contract proves a past transport failure was persisted; it cannot prove the cause is gone. The owner's authorization is the only check on that.
- Not found: a path by which an authorization file, a ratified-set name that is not an audited candidate, an advisor name, an HTTP status, or a marker could open a resume.

## A2. Tests added or strengthened in this round (all offline; production constants never edited)
| Test | Mode | Enforced | Type | What it proves |
|---|---|---|---|---|
| `test_negative_damaged_files` (strengthened) | TEST-ONLY set | yes | negative | each damage is refused by the integrity layer (text mentions raw/ledger/chain, and is NOT the contract's own message); before: only the exception type |
| `test_an_authorization_cannot_be_reused_on_a_run_that_is_still_incomplete` | TEST-ONLY set | yes | negative + control | after a resume that dies again, the first authorization is refused (`current ledger head`), a fresh head with the old count is refused (`trailing_transport_failures`), the correct new one works |
| `test_the_basis_must_match_the_state` | TEST-ONLY set | yes | negative | `transport_halt` basis on a no-marker state, and `process_interruption` basis on a halted main run, are refused |
| `test_a_non_owner_authorization_is_refused_even_with_valid_evidence` | TEST-ONLY set | yes | negative | advisor, assistant, empty, None, "Owner" (case) are refused |
| `test_finding_F1_current_behaviour_...` | TEST-ONLY set | yes | characterization | finding F1 |
They use the TEST-ONLY set `{"TimeoutError"}` as a stand-in: they prove the mechanism, not production eligibility (production eligibility is nil, 0 of 14 ratified). Together with the previous round: lock active, cost stop, stale head, reuse, ledger/raw inconsistency, mid-call crash are all covered (section 2 table).

## A3. Pre-freeze snapshot of the 31 files the final-freeze tool would hash (read-only; NOT a manifest)
Computed 2026-10-15 by calling `build()` of `s11_final_freeze_manifest.py` on a SYNTHETIC in-memory PASS record kept in the scratchpad (nothing written in the repository, no manifest created, no PASS record exists). These hashes will change if any listed file changes (`s10_resume.py`, `s10_runner.py` etc.); a snapshot is not a freeze.
| File (relative to `research_design/`) | SHA-256 (first 16) |
|---|---|
| METHODOLOGY_FREEZE_MANIFEST_v2_7.json | `b93ff372d44854e1` |
| PARAMETER_FREEZE_MANIFEST_FZ_v1.json | `149445715a8280f4` |
| PARAMETER_JUSTIFICATION_RECORD_DRAFT.md | `a1b2148766965d0b` |
| SCENARIO_CONSTRUCTION_SPECIFICATION_v2_7_DRAFT.md | `d5fcffadd1045fc0` |
| implementation_a/impl_a.py | `daa2cd49b86ed1a5` |
| step10/s10_analysis.py | `7993a7347e07f391` |
| step10/s10_integrity.py | `f2a109cfdcc27d32` |
| step10/s10_report.py | `f9857e5603941a6c` |
| step10/s10_resume.py | `eaa0d09248be0b54` |
| step10/s10_runner.py | `9f235dec8b6d6525` |
| step10/s10_scoring.py | `8c0e6b9fecb559fb` |
| step10/s11_final_freeze_manifest.py | `7395140ce37bcb83` |
| step10/s11_pilot.py | `68fc807f85a7eaa6` |
| step10/s12_cli.py | `e6de02879a580eeb` |
| step10/s12_coding.py | `a571c6ba64fdf651` |
| step7/CODEBOOK_S2_S3_v1_DRAFT.md | `25a74353be546cf9` |
| step7/STEP7_PROMPT_SPECIFICATION_FREEZE_MANIFEST_v1.json | `202979de2a88c1b6` |
| step7/codebook_battery_v1.py | `8200cfea41e23255` |
| step7/parser_battery_v1.py | `82af5d5361561d98` |
| step7/prompt_specification_v1.py | `8b9a73e945f0251c` |
| step7/s7_bundle.py | `10567178b20976ea` |
| step7/s7_core.py | `64789acb84047f3d` |
| step7/s7_decision.py | `cf0823f7abdf4b6b` |
| step7/s7_diagnostic.py | `5e0f6e707231d66f` |
| step7/s7_parser.py | `b9d60196c50f8099` |
| step7/s7_recode.py | `ec8f948e6209147d` |
| step7/s7_refcheck.py | `39e10a85068262c9` |
| step8/s8_verify.py | `b9a46f599320e542` |
| step8_output/step8_build_7a6bbe465c66/manifest.json | `09eed00eeb79e04c` |
| step9/impl_b.py | `ada22199bb472d93` |
| step9/s9_blindcheck.py | `e870b8d03b317900` |

## A4. Path to the code freeze (dependency order)
1. Owner: ratify (or not) exception classes (12.42 draft entry); decide F1 (a/b); decide whether to store `URLError.reason` (and whether raw-record content is inside H2's scope). These can change `s10_resume.py` and `s10_runner.py`.
2. Owner: write the P13 entry; decide MD-03/K2, PG11b, D3, D5, MD-10 (K2 or a narrowed PG11b forces a Step 7 re-freeze and Step 8 rebuild, which changes listed files).
3. Advisor: notice (unsent) and written answers to Q1-Q5 and the H4 stop-rule. The request file named in the checklist (`H4_ADVISOR_DECISION_REQUEST_READY_2026-10-14.md`) is in a scratch folder and was NOT found in the repository, so the draft in the gap report U4 is the only text under version control.
4. Assistant (after 1-3): implement any approved code change with backups; full `run_all_checks` including the slow Step 8 suite; record the new 31 hashes.
5. Owner: dated code-freeze declaration (checklist row 10).
6. In parallel, independent of 1-5: researcher writes R1, then H1; seven days after R1; H3 (needs the owner's written confirmation that nothing bound into the build is still open, so after 2); owner PRD-6/H7, MD-02, H5 file, price re-read on the day, key in the terminal, explicit pilot start.
Verified absent on 2026-10-15: `human_evidence/clock/`, `step9_evidence.json`, any authorization file, any final freeze manifest.

