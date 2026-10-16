# Pre-pilot action checklist (ordered; 2026-10-14)

Tags: **[OWNER]** only the owner can do or decide it; **[RESEARCHER]** only the person who did the blind-check work (no one else, no model, may do it); **[ADVISOR]** needs the advisor's answer; **[ASSISTANT]** mechanical work the assistant can do after the stated approval. Nothing below has been done unless a status says so. Gate status on 2026-10-14: CLOSED. R1: not recorded. H3: not created.

## Phase 1 -- decisions that must exist before anything is frozen
| # | Action | Who | Output | Status |
|---|---|---|---|---|
| 1 | Send the advisor request (`H4_ADVISOR_DECISION_REQUEST_READY_2026-10-14.md`, scratch folder) with `rehearsal_findings.md` and the excerpts of records 12.38 and 12.39 | **[OWNER]** (the assistant never sends) | sent message, dated note | not sent |
| 2 | Advisor answers questions 1-5 (reading of "used", `s2_arith` without a prompt, sufficiency of the rehearsal, role in 12.39, PG3 review) | **[ADVISOR]** | written answer | waiting |
| 3 | Record the answers as a NEW entry in the owner decision record (back up first); never mark an advisor review done without the written answer | **[OWNER]** | record entry | pending |
| 4 | Answer the stop-rule question of the H4 findings: (i) limitation, (ii) codebook revision (new Step 7 version, R-7, rebuild, hash comparison), (iii) battery question | **[OWNER]** with **[ADVISOR]** | entry; rebuild if (ii) | pending |
| 5 | Researcher states the basis of `SW` on B10 and B36 or records that it cannot be recovered | **[RESEARCHER]** | note in `rehearsal_findings.md` | pending |
| 6 | Decide the six MD-08 rows (`MD08_DECISION_PACKAGE_2026-10-14.md`) | **[OWNER]** (advisor where the table says so) | filled decision block | PARTIAL: owner choices recorded 2026-10-15 as entry 12.40 (all six rows). Not complete: HTTP status list (row 2), evidence rule for a killed process (row 3) and H1-H4 check at resume (row 5) UNRESOLVED; code not yet aligned (row 3 branch); advisor not informed |
| 7 | Decide the Step 11 file list (`STEP11_FILE_LIST_PROPOSAL_2026-10-14.md`) | **[OWNER]** | approval or refusal | approved in principle by the owner in chat 2026-10-15 (P13 applied); NOT yet written as an entry in the owner decision record |
| 8 | Decide the other items that can change a manifest-bound artefact: MD-03 (K2), PG11b scope, D3 SF/UNP policy, D5 re-code values, MD-10 amendments | **[OWNER]** and **[ADVISOR]** | entries; rebuild if any artefact changes | pending |
| 9 | Apply the approved changes (P13 diff and test, MD-08 code changes, cost-stop decision), rerun the Step 10 suite and `run_all_checks` (full, with the slow Step 8 suite) | **[ASSISTANT]** after 6-8 | new hashes recorded | PARTIAL: P13 applied 2026-10-15 (tests pass, see update below). MD-08 code changes and other approvals: not applicable yet (undecided). Full run_all_checks (with slow Step 8 suite) not rerun |
| 10 | **Code freeze point:** no Step 10 code change after this point; any later change is an H1-H4 fix with logged hashes | **[OWNER]** declares it | dated note | not declared |

## Phase 2 -- human evidence
| # | Action | Who | Output | Status |
|---|---|---|---|---|
| 11 | Decide when you stop viewing registry content, and write R1 yourself, with the true time | **[RESEARCHER]** | `human_evidence/clock/` file | not recorded; never backdate |
| 12 | H1 blind check of 624 files from the blank worksheet (PG3 reading ratified by the owner in 12.38; advisor review pending) | **[RESEARCHER]** | filled worksheet; evaluator NO REJECT, coverage 100% | not started |
| 13 | Wait at least 7 full days after R1 | time | -- | not started |
| 14 | Create the Step 9 evidence file with the evaluator, only after the H4 stop rule is cleared and the owner confirms in writing | **[RESEARCHER]** with **[OWNER]** confirmation | `step9_evidence.json` | blocked by 3, 4, 11-13 |

## Phase 3 -- authorisation of the pilot
| # | Action | Who | Output | Status |
|---|---|---|---|---|
| 15 | Declare the write-once store and the anchoring of the pilot decision record (H7, PRD-6, MD-09) | **[OWNER]** | record entry | not declared |
| 16 | Re-read the provider's prices and the model identifier on the run date (B7); if prices differ from the constants in `s10_runner.py` (US$0.30 / US$2.50 per million tokens), recompute the bound before authorising | **[OWNER]** | dated note | pending |
| 17 | Confirm MD-02 (`max_input_characters`, proposed 1,016; `input_tokens_per_call_assumed`) | **[OWNER]** | confirmed values | working decision only |
| 18 | Write the pilot authorization (H5) as a NEW file from the template: `authorized_by = owner`, `scope = pilot_round_1`, `max_calls = 18`, cost ceiling 100 | **[OWNER]** | `authorization.json` | does not exist |
| 19 | Put the API key into the environment of the terminal that will run the pilot (never into a file in the repository); disable sleep, use stable power and network | **[OWNER]** | -- | not done |

## Phase 4 -- gate check and the pilot itself
| # | Action | Who | Output | Status |
|---|---|---|---|---|
| 20 | Gate check without `--live`: `python -B -I research_design/step10/s10_runner.py --scope pilot_round_1 --build research_design/step8_output/step8_build_7a6bbe465c66 --out <unused> --evidence <step9_evidence.json> --authorization <authorization.json>` must print `gates open; --live not given` and `local preflight: OK` | **[ASSISTANT]** | printed output | closed today |
| 21 | Optional single-call connection test (A5/P11) only if you authorise it separately and in writing | **[OWNER]** | -- | not authorised |
| 22 | Say explicitly that the pilot may start (`--live`) | **[OWNER]** | instruction | not given |
| 23 | After the run: `s10_integrity.py`, then `s11_pilot.py report` and `decide`; no one reads response content | **[ASSISTANT]** runs, **[OWNER]** records | integrity OK; report; decision record | not started |
| 24 | FAIL-S in round 1: a whitelisted change as a new FZ version, then round 2 (or STOP); FAIL-U: STOP-U and the advisor | **[OWNER]** with **[ADVISOR]** | record | n/a |
| 25 | After a `PASS` record: write the final freeze manifest (extended list if approved), backup first, recompute every hash independently | **[ASSISTANT]** with **[OWNER]** approval | `step11 manifest` | impossible before 23 |
| 26 | Main-run authorization (`scope = main`, 2,496 calls) and the resume decision in force | **[OWNER]** | authorization | after 25 |

The shortest dependency chain is: 1 -> 2 -> 3/4/6/7/8 -> 9 -> 10, and in parallel 11 -> 12 -> 13 -> 14; both chains must finish before 15-19. The only item that does not wait for anything else is number 1.

## Update 2026-10-15 (status only; no prerequisite below was met by this update)
- **P13 applied** to `research_design/step10/s11_final_freeze_manifest.py` (24 -> 31 hashed files); guard test installed as `research_design/step10/test_step11_file_list.py`. Backup: `_backup/p13_20261015/`. Results: P13 test 2 tests OK (exit 0); whole Step 10 suite 184 tests OK (exit 0); `run_all_checks.py --quick` exit 0, ALL CHECKS AS EXPECTED, gate status exit 2 = CLOSED (expected). New SHA-256: manifest tool `7395140c...10eb`, test `0def2e1f...ffaf44` (old tool hash `bbcbf153...f762`). Still to do: write the change and new hash as an entry in the owner decision record (owner), rerun the full check with the slow Step 8 suite before the code freeze.
- **MD-08: all six rows PENDING.** Answer sheet: `MD08_OWNER_ANSWER_TABLE_2026-10-15.md`. Runner/resume code and the current cost stop are unchanged.
- **Not available / not done:** advisor answers (rows 1-5 above), owner record entries (rows 3, 4, 8), code freeze declaration (row 10), R1 timestamp (never recorded, never backdate), H1 blind check, 7-day wait after R1, H3 evidence file, pilot authorization, API key setup.
- **Unresolved:** PRD-6 (anchoring of the pilot decision record) and the H7 write-once store declaration (row 15).
- **Final freeze:** no final freeze manifest exists. It may be written only when the pilot decision record says `final_decision = PASS`; the tool refuses otherwise.

## Update 2026-10-15 (MD-08 decisions)
- Owner decisions for MD-08 rows 1-6 recorded as entry **12.40**: 1=A, 2=C, 3=C, 4=C, 5=C, 6=A. The advisor has not answered or approved; the notices for rows 4 and 6 are not yet sent. Gate remains CLOSED; no pilot authorization, R1, H1, H3, code freeze or final freeze manifest exists.
- Item 6 is NOT marked complete. Open: permitted HTTP status list, evidence rule for resume after a killed process, H1-H4 evidence check, and the code change that follows (the row 3 `process_interruption` branch contradicts the decision). Item 9 (apply approved code changes) is blocked on these.

## Update 2026-10-15 (second): MD-08 implementation and blocker matrix
- Resume code made fail-closed per 12.40 and recorded as entry 12.41 (see `MD08_GAP_RESOLUTION_2026-10-15.md`). Implementation status: implemented and tested for the closed gates and the H1-H4 evidence check; the definitions (HTTP status list, exception allow-list ratification, killed-process evidence contract) remain unresolved, so item 6 stays PARTIAL and item 9 stays blocked.
- Advisor notice for rows 4 and 6: drafted in the gap-resolution file, NOT SENT. No advisor answer received.
- Full blocker matrix, code-freeze readiness (NOT READY) and gate assessment (CLOSED): `MD08_GAP_RESOLUTION_2026-10-15.md` sections 7-9.

## Update 2026-10-15 (third): record 12.42
- MD-08 item 6 stays PARTIAL. Done: HTTP list empty (recorded, implemented, tested); process-death contract adopted, implemented, machinery tested; 14 classes audited. Open: owner ratification of exception classes (none ratified, so no resume exists), advisor notice (unsent), H1-H3 evidence for any actual fix.
- Item 7 (Step 11 list): applied and tested; the owner-record entry is still `AWAITING_OWNER` (draft in `MD08_GAP_RESOLUTION_2026-10-15.md` U3).
- Item 11 (R1): NOT RECORDED; template `templates/R1_clock_note_TEMPLATE.md` is not evidence. Items 12-15, 18, 19: not done. Gate CLOSED. Item 9 and 10: blocked on the ratification decision.

## Update 2026-10-15 (fourth): record 12.43
- Owner decisions X-1 (A1) and X-3 (O3) recorded and implemented; X-4 classified (pre-freeze change, not an FZ change; open sub-question X-4b for post-freeze changes). MD-08 item 6 stays PARTIAL: class ratification (draft 12.44, 0 of 14 ratified), advisor notice (unsent) and answers still open.
- Item 7 (P13): list verified (`P13_FILE_LIST_VERIFICATION_2026-10-15.md`); the record entry is still `AWAITING_OWNER`.
- Item 8 (MD-03/K2, PG11b, D3, D5, MD-10): options in `MD08_X6_X7_DECISION_AND_READINESS_PACKAGE_2026-10-15.md`; NOT decided.
- Items 11-15, 18, 19: R1 not recorded (`human_evidence/clock/` absent), H1/H3 not done, seven-day wait not started, PRD-6/H7, H5 not done. Gate CLOSED; no code freeze.

## Update 2026-10-15 (fifth): record 12.44
- P13 / item 7: the owner APPROVED the 31-file list (entry 12.44). This is not a code freeze, not a final-freeze approval and not a pilot authorization. Item 10 (code freeze declaration) remains not declared.
- X-2: the owner instructed that no class be ratified now (entry 12.44); 0 of 14 ratified; MD-08 item 6 stays PARTIAL. X-4b and X-6 (item 8) still AWAITING_OWNER: `MD08_OWNER_DECISION_PACKAGE_2_2026-10-15.md`.
- Items 11-15, 18, 19 unchanged: R1 not recorded, H1/H3 not done, wait not started, PRD-6/H7 and H5 not done. Gate CLOSED.
