# Gate predicates, blockers and owner decisions after R1, 2026-10-15

Preparation and audit only. Gate CLOSED. R1 recorded by the researcher at 2026-10-15T07:50:10Z (file verified read-only; not touched). No forbidden artifact was opened; no provider call; no frozen file, gate, manifest or timestamp changed. Status words: HOLDS = checked today against actual files/code; MISSING = the required file does not exist; NOT YET = depends on a later step.

## 1. Gate predicates (`s10_runner.check_gates`; verified by running the gate CLI for `pilot_round_1` and `main` with absent evidence files: exit 2, no provider contact)

| # | Predicate (scope) | Evidence required | Status today |
|---|---|---|---|
| G1 | Register model settings equal the expected frozen values (all) | FZ-v1 row 17: gemini-3.5-flash-lite, minimal, 8192, retries 0, timeout 180, delay 1, concurrency 1 | HOLDS (no reason raised) |
| G2 | Step 8 verifier clean (all, `verify_build`) | `s8_verify.verify(build)` | HOLDS (no reason raised) |
| G3 | Implementation B agrees (all) | `impl_b.verify(build)["failures"]` empty | HOLDS (no reason raised) |
| G4 | Step 9 evidence file exists (all) | `step9_evidence.json` | **MISSING** (H3 not created) |
| G5 | Blind-check delay >= 7 days (all) | `(completed_utc - last_registry_view_utc).days >= 7`; R1 = 2026-10-15T07:50:10Z -> earliest completed_utc **2026-10-22T07:50:10Z** | NOT YET (needs H1, true completion date) |
| G6 | Coverage 100 % (all) | `coverage_percent == 100` from H1 | NOT YET |
| G7 | Worksheet hash present, 64 hex (all) | filled worksheet hash | NOT YET |
| G8 | Adjudication AGREE or ADJUDICATED_NO_REJECT (all) | from `s9_blindcheck.py` | NOT YET |
| G9 | Evidence names this build (all) | `build_manifest_sha256` = SHA-256 of `step8_build_7a6bbe465c66/manifest.json`; unchanged by 12.51 (K1) and 12.52 (MD-10 confirmation) | NOT YET (holds if no bound item changes) |
| G10 | Owner authorization file exists (all) | H5 file | **MISSING** |
| G11 | Authorization matches scope and calls (all) | `authorized_by=owner`, `scope`, `max_calls` = 18 / 18 / 2496 | NOT YET |
| G12 | Hard-cap cost below the OD-10 limit and `cost_ceiling_usd` = 100 (all) | with `input_tokens_per_call_assumed` = 1016: pilot US$0.3741, main US$51.8789 (computed today, below 100) | NOT YET (value is the owner's to write) |
| G13 | `max_input_characters` positive integer, longest planned prompt not above it (all) | owner's value (template proposes 1016, the verified maximum) | NOT YET |
| G14 | Final pilot decision record exists (main only) | `s11_pilot decide` output | NOT YET |
| G15 | Final pilot decision is PASS (main only) | `final_decision == "PASS"` | NOT YET |
| G16 | Call-list hash equals the pilot record's (main plan) | `call_list_sha256` | NOT YET |
| — | Not a gate predicate in code: FZ hash enforcement (E-1, needs P5), freeze of the 31-file list, `--live` flag, API key in the environment, MD-09 anchor | see sections 3-4 | the code does NOT check them; they are procedural prerequisites |

Gate reasons printed today: G4, G10 (pilot); G4, G10, G14 (main). The gate stops adding reasons only because the other files are absent; nothing else was weakened.

## 2. Work completed today (record and code)

- 12.50: owner as sole decision-maker; MD-06, B-1(a), Q5, E-1 direction, P11/P12 procedure, Q9/P3b recorded. 12.51: K1 replaces K2; R-7 NOT AUTHORIZED. 12.52: MD-10 approved as worded (confirmation only).
- MD-06/P2 safe-stop implemented mock-only (`provider_anomaly`, `drive`, `s10_integrity` halt check, `test_safe_stop.py` 7 tests, 5+ legacy fixtures/tests rewritten without weakening); suite 238 OK; `run_all_checks.py --quick` OK.
- F-3 verified: E-PAR catches a register-versus-member difference in the valid member (in-memory mutation, `F3_register_member_mutation_check_2026-10-15.py`).
- `MD10_AND_H1_BLOCKER_AUDIT_2026-10-15.md` and `H1_MANUAL_GUIDE_AFTER_R1_2026-10-15.md` written.

## 3. Audit of the remaining items

- **R-7 / K1 / K2.** Decided B (12.51): K1, R-7 NOT AUTHORIZED. Effect on Step 8 / manifest / freeze / H1: none (no bound item changes). A codebook revision (H4 answer (ii)) would again require R-7 and a rebuild; that is the only remaining route to a bound-item change.
- **H4.** Findings DONE (class B cells exist, B10 and B36 `SW` unclassified). Stop rule holds until the owner answers (i) limitation, (ii) codebook revision, (iii) battery question (`H4_STATUS_AND_BLOCKERS_2026-10-14.md`). With no advisor (12.50), the advisor inputs listed there become owner decisions. Choosing (ii) conflicts with R-7 NOT AUTHORIZED and can void H3 (and H1 if the inventory changes); choosing (i) or (iii) changes no bound item. Owner choice required BEFORE H3; best before spending the H1 effort.
- **SW note for B10/B36 (researcher's own act).** Write a dated NEW note in `human_evidence/rehearsal/` either (a) stating, from your own recollection, why you entered SW and naming one class (A, B or C), or (b) stating that the basis cannot be recovered (cells stay "not classified"). Do not change a label, the sheet or the comparison. The assistant does not write this note.
- **P5 / E-1.** Inactive artifacts exist and are unchanged (`P5_fz_index.py.INACTIVE` 108 lines, `P5_test_fz_index.py.INACTIVE` 91 lines, 7 tests verified in scratch). P5 is NOT authorized (12.50 row 4); MD-04 procedure approved with list L-B, A-2 = exclude (12.47/12.48). E-1 direction approved, not implemented. Implementation changes `s10_runner.py` and `s11_pilot.py` (two of the 31-file list; hashes move; list membership unchanged). Needs, before the official hash: MD-01, MD-03, MD-05, MD-06, MD-07, MD-10 settled (now all recorded; the owner must instruct the computation) and the P5 authorization. Does not touch H1/H3.
- **H5.** Not created. The owner writes a NEW file from `templates/owner_authorization_TEMPLATE.json`: `authorized_by` = `owner`, `scope`, `max_calls`, `cost_ceiling_usd` 100, `input_tokens_per_call_assumed` (positive integer, your own value; 1016 is the Step 7 assumption), `max_input_characters` (template proposes 1016). Q9/P3b rejected (12.50): values stay unenforced beyond the existing checks; no measured basis exists. B7 (price re-verification) and B8 (write-once store declaration, MD-09 deferred) are human tasks, not started.
- **B-1 follow-up-round rule (draft for the owner; none chosen).** Spec 13.6: at most 2 pilot rounds in total; a stopped (safe-stop) run counts as a round (12.50 row 2). Options to document BEFORE MD-06 is used in a pilot: (1) after a safe-stop in round 1, the owner reviews the stop reason, records the disposition, and runs round 2 under the same FZ, same build, new output folder; a safe-stop in round 2 ends the pilot without PASS, and the research status is BLOCKED/INCONCLUSIVE until a new owner decision on a new methodology version; (2) after a safe-stop the owner stops without a second round (research BLOCKED). Recommendation (not a decision): (1). Stopped folders are never deleted or edited, and no resume is automatic.
- **MD-06 activation / 31-file list.** Code for MD-06 is in place (mock-only). The 31-file membership is unchanged; hashes of `s10_runner.py` and `s10_integrity.py` changed and are fixed at the code freeze.

## 4. Chain to the main experiment and what blocks each step

1. **H1** 624 rows (researcher) -> precheck -> evaluation NO REJECT. Blocker: your work.
2. **Wait**: completion >= 2026-10-22T07:50:10Z (168 h; no viewing of forbidden content). Blocker: time.
3. **H4 stop rule answer** (owner) and the SW note (researcher). Blocker: decisions/acts.
4. **H3** `step9_evidence.json` (researcher, after the owner's written confirmation that nothing bound is open). Blocker: 1-3.
5. **P5/E-1 authorization** and implementation (assistant, mock tests), B-1 rule recorded, MD-09 decision before the decision script.
6. **Code freeze**: 31-file list exact (P13), final freeze manifest, FZ hash in the source order (L-B index), final checks, freeze recorded. Blocker: 3-5 and the owner's instruction for the official hash.
7. **H5** authorization, API key set in your own terminal, explicit `--live`. Pilot round 1 (max 2 rounds), decision record; main only after PASS.
8. Main experiment, analysis against the predefined criteria, final report (discloses: no advisor; K1 departure; limitations).

## 5. Owner decisions still required (one list)

1. **H4 stop rule**: (i), (ii) or (iii) (recommend deciding before H1 is finished; (ii) implies R-7).
2. **B-1 follow-up-round rule**: option 1 or 2 above (before MD-06 is used in a pilot).
3. **P5 `fz_index.py` and E-1 implementation**: authorize or not (needed before the official FZ hash and the pilot gate enforcement).
4. **Instruction to compute the official FZ hash** (when step 4 of section 4 is done).
5. **MD-09 anchoring** (deferred) before the decision script.
6. **H5 values** (your own act) and whether P11 (connection test) is wanted, with its own live authorization.

## 6. Researcher/owner acts only you can do (not done)

H1 rows and commands (`H1_MANUAL_GUIDE_AFTER_R1_2026-10-15.md`); the SW note; H3 on or after 2026-10-22T07:50:10Z; H5; API key; `--live`. None may be backdated, delegated to a model, or hidden in tracked files.

## 7. Status

Experiment: NOT RUN. Final status if stopped now: BLOCKED (waiting on H1/H3, the 168-hour wait, H4 answer, P5/E-1 authorization, freeze, H5, live authorization). The wait is not complete and is not assumed complete.
