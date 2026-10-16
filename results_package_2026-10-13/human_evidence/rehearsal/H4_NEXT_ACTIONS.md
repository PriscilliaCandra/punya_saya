# H4 next actions: procedural dependencies after the H4 documents (state of 2026-10-14)

Read-only analysis. No label, CSV, codebook, spec, registry, manifest, frozen artifact or official record was changed; `compare_rehearsal.py` and the format pre-check were not run; no R1 file, no evidence file, no provider call. Paths are relative to `D:\research s2`. H4 is NOT complete: the current labels are AI-assisted candidates, not an independent human rehearsal (OD-3: `research_design/STEP2_OWNER_DECISIONS_RECORD.md` line 45, row "Operational implications": "A model coder, if used at all, is a screening comparison only, never the reconciling authority"; codebook lines 49-50; spec line 1003). Abbreviations: spec = `research_design/SCENARIO_CONSTRUCTION_SPECIFICATION_v2_7_DRAFT.md`; codebook = `research_design/step7/CODEBOOK_S2_S3_v1_DRAFT.md`; checklist = `results_package_2026-10-13/HUMAN_TASKS_H1_H7_OPERATIONAL_CHECKLIST.md`; package = `results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md`.

## 1. Actual status of every gate (checked on 2026-10-14)
| Item | Status | Evidence |
|---|---|---|
| R1 (true time the researcher stops viewing registry content) | NOT RECORDED; the 7-day clock has NOT started | `results_package_2026-10-13/human_evidence/clock/` does not exist; checklist line 8 (only the researcher creates the file) |
| H2 seven-day delay | not started (depends on R1) | FZ-v1 `row19_blind_check.minimum_delay_days` = 7; `research_design/step10/s10_runner.py` lines 128-130 compute `completed_utc - last_registry_view_utc` in days |
| H1 blind check | not started; blank worksheet only | `human_evidence/blind_check/` does not exist; checklist line 11 (ask first whether PG3 is ratified) |
| H3 evidence file | NOT CREATED | `human_evidence/blind_check/step9_evidence.json` does not exist; it needs both dates from the person (`research_design/step9/s9_blindcheck.py` lines 181-190) |
| H4 codebook rehearsal | NOT DONE (AI-assisted candidates only); NOT read by the gate | `grep -i rehears research_design/step10/s10_runner.py` finds nothing; see 5.3 on whether it is mandatory |
| H5 pilot authorization | absent; the template is not an authorization | gate output below; `templates/owner_authorization_TEMPLATE.json` |
| Step 8 verifier and Implementation B | pass (they are not among the gate reasons) | gate output below |
| Pilot gate | CLOSED | `python -B -I research_design/step10/s10_runner.py --scope pilot_round_1 --build research_design/step8_output/step8_build_7a6bbe465c66 --out unused --evidence results_package_2026-10-13/human_evidence/blind_check/step9_evidence.json --authorization results_package_2026-10-13/templates/owner_authorization_TEMPLATE.json` printed "GATE CLOSED: - Step 9 evidence file missing (human blind check not documented) - authorization does not match the scope and the planned number of calls", exit 2 |
| Main-run gate | CLOSED (needs a PASS pilot record, anchor, final freeze manifest, authorization for 2,496 calls) | `MASTER_PILOT_READINESS_CHECKLIST.md` section 6 |

## 2. Is correcting `s2_arith` to AN a local change or a change of the specification? (item 5)
**Finding: a local change to a screening candidate only. No specification change, and R-7 is NOT required for it.** Evidence:
- The specification already says AN: spec line 942, `s2_arith` "(over stated computations **with provenance**) ... **AN** none. Computations without provenance are unverifiable and are excluded here (they appear in `s2_prov = N`)"; spec line 956 gives the analogous example ("The increase is pct%." -> N, AN). Nothing in the specification needs to change to apply it.
- The codebook says section 16 governs when they differ (codebook lines 4-5); codebook line 93 omits the exclusion sentence, which the codebook itself treats as a defect of the codebook, not as the rule.
- The working CSV is outside everything that is hashed or frozen: it is not one of the 11 files in the Step 7 manifest `freeze_set_files`, not one of the 15 generator-code files of the Step 8 manifest `generator_code_sha256`, and not in the manifest `inventory` (main/pilot prompts, checker bundles, mapping, gate report, prompt table, registry; `research_design/step8_output/step8_build_7a6bbe465c66/manifest.json`). Changing a candidate label there changes no hash in the H3 chain.
- Procedure: a candidate label is not a coding decision of record; OD-3 and spec line 1003 make a model coder a screening comparison only. The change itself must still be made in a NEW file version (never overwriting) after the user's approval; it was not made in this step.
**When R-7 (a Step 7 return) WOULD be required.** "R-7" is the name of a box in the package for authorizing a Step 7 re-freeze; it is not a term of the sources. The underlying requirement is documented and applies only if the CODEBOOK FILE is edited (for example to add the omitted sentence): the Step 7 manifest `status` reads "A change to a freeze-set file before the FZ hash returns to Step 7 (new version)"; `research_design/step7/test_step7.py` lines 1549-1551 assert that the hashes of the 11 freeze-set files equal the manifest, and line 1559 pins the codebook header "revision 5"; the codebook is in the FZ (spec line 797) and in the prompt-specification freeze (spec line 1186); spec line 1211: after a return "every later step is re-executed and re-frozen with new hashes", and after the first pilot call there is no return. Leaving the codebook unchanged and relying on "section 16 governs" avoids all of this. Which option to take is the owner's question A-2 in `H4_ADJUDICATION_REQUEST.md`.
Spec line 1001 (amendment = new codebook version "applied in a new column, never retroactively") concerns coding of responses after coding has started; no coding has started, so it does not apply to the rehearsal.

## 3. Corrections of earlier statements found in this step (earlier files were NOT edited)
1. `H4_PROCEDURAL_FINDINGS.md` section 4 cites OD-3 at "line 44" of `STEP2_OWNER_DECISIONS_RECORD.md`; the row "Operational implications" with the quoted text is line 45 (line 44 is "Approved choice"). `H4_ADJUDICATION_REQUEST.md` cites "lines 39-48", which is correct.
2. The package (`OWNER_APPROVAL_PACKAGE.md`, Appendix A-1: "the gate runs `s8_verify` against it", and the L-A row "a drift is caught by the gate's verifier") and `MASTER_CLOSEOUT_REPORT.md` Addendum F ("no drift; `s8_verify.py` exit 0") imply that the verifier compares the generator-code hashes. It does not: `research_design/step8/s8_verify.py` checks the published inventory (lines 45-64), the manifest header (66-67), registry hashes (77-78), prompts (105) and the call list (188); no code outside the builder reads `generator_code_sha256`, `specification_sha256` or `step7_freeze_manifest_sha256` (grep over `research_design`, excluding history and outputs). Drift of the 11 Step 7 files against the Step 7 manifest is caught only by `test_step7.py` (lines 1549-1551); drift of `implementation_a/impl_a.py` and `step8/s8_build.py`, `s8_construct.py`, `s8_gates.py` against the hashes recorded in the registry provenance is caught only by `research_design/step8/test_step8.py` `test_generator_code_hashes_in_the_registry_are_current` (lines 123-128), which belongs to the slow Step 8 suite that `run_all_checks.py --quick` skips; the gate does not run it. The ad hoc hash comparison I ran earlier (15 files against the manifest, no drift) was correct but was not the verifier. Consequences: L-A is weaker than described (its protection against drift of the generator files depends on running those tests, not on the gate); and the H3 dependency chain is a procedure (a file edit without regenerating the manifests would not change the Step 8 manifest hash and would not mechanically invalidate H3), not something the gate enforces. The chain remains the right order to follow. An in-place correction of these two passages is proposed for your approval.
3. Documents I wrote list H4 as required "before the pilot (spec 13.5)". The sources are weaker: spec line 820 requires codebooks to be tested "on synthetic batteries"; codebook lines 219-223 say the human coder "**may** code the items"; the human rehearsal is the proposal P-5 ("Proposed rehearsal, **pending**", `research_design/step7/PROPOSED_CLARIFICATIONS_AND_AMENDMENTS_DRAFT_v1.md` lines 102-112); the gate does not read it. Whether it is mandatory is an owner decision (question 5.3).

## 4. Dependencies and unmet prerequisites
| Next step | Needs | Unmet |
|---|---|---|
| Start the 7-day wait | the researcher's genuine R1 file | R1 absent |
| H1 | R1; PG3 ratified or its consequence accepted | R1, PG3 |
| H3 | R1 + 7 full days; H1 done with coverage 100 % and no REJECT; nothing bound into the Step 8 manifest still open (MD-03 K2, PG11b narrowing, SF/UNP policy, MD-10 amendment, a codebook revision, a changed register value); the owner's written confirmation | all |
| Codebook revision (only if chosen) | owner/advisor decision A-2 or a stance clarification; Step 7 return (section 2); rebuild sequence in the package; BEFORE H3 and before the first pilot call | decision |
| Update of candidate labels | the user's approval; a new file version | approval |
| Independent human rehearsal (if kept) | the researcher codes the 40 rows from the blank kit; the existing pre-check; then the one-time comparison with the owner's agreement | decision on 5.3; coding |
| Pilot authorization | MD-02 confirmed; H5 file written by the owner | owner |

## 5. Decisions and questions
### 5.1 Decisions that follow from explicit written rules (no new rule needed; applying them to files still needs your approval)
- Row 20 `d614cbb672fe000e`: `s2_arith` = AN (spec 942). The candidate AC conflicts with the spec.
- Row 05 `00ceeab4df7002aa`: `s2_prov` = N, `s2_evidence` NV, `s2_arith` AN (spec 931, 932, 940, 956). Already applied in the working file.
- Row 01 `b7721cb9eafab528`: `s2_evidence` = IV and `s2_rel` empty ("less than" is outside the closed list: spec line 935, codebook line 73). Already applied.
- `N/A` -> empty in `s2_prov`/`s2_rel` (codebook line 99). Already applied.
### 5.2 Questions that really need the owner/advisor (all in `H4_ADJUDICATION_REQUEST.md`)
- B-1: row 25 (`fe7db0c0524f62b4`) referent and limit direction missing: rules insufficient.
- C-1, D-1, E-1 with the scope principle: do statements that a quantity does or does not exceed the cap count as explicit assertion or rejection of Φ_viol (rows 28, 29, 35)? Spec lines 981-985, 991 and 933 (c) lean toward yes but do not say it; adopting it affects 16 more rows.
- A-2: leave the codebook as it is (spec governs) or revise (Step 7 return).
- G-1: how to treat `s2_values` and `s2_arith` that depend on a prompt the rehearsal does not provide (spec 941, 947).
- PG3 (for H1) and the other bound-artifact decisions in the package's "Blocking decisions" log.
### 5.3 Added question
Is a human rehearsal mandatory before the pilot, or optional (codebook "may", P-5 pending, not read by the gate)? If optional, H4 stops being a prerequisite of H3 unless the owner keeps it; if mandatory, the researcher's independent coding is needed and the AI-assisted labels remain only a screening input. The researcher has already seen the AI labels and the assistant's readings, which limits the independence of any later coding; that limitation must be stated with the evidence.

## 6. Safe order of next actions
1. Nothing is blocked for the researcher except what depends on R1: the researcher decides when they genuinely stop viewing registry content and creates the R1 file themselves (checklist line 8).
2. Owner/advisor, in parallel: answer 5.3, A-2, PG3, then B-1/C-1/D-1/E-1/G-1 and the rest of the decision log. Decisions that can change a bound file (A-2 revise, MD-03, PG11b, SF/UNP, MD-10) come before H3.
3. After the user approves: write a new version of the working candidate file with `s2_arith` of row 20 = AN (never overwrite); no other label until the owner answers.
4. If H4 is kept: the researcher codes the 40 rows independently on a fresh copy of the blank kit; pre-check; one comparison with the owner's agreement; findings with the A/B/C template; stop before H3 on B/C.
5. If a codebook revision is chosen: Step 7 return, rebuild with a new output folder, inventory comparison (all 2,026 hashes must match, otherwise H1 is void), then H3.
6. H1 after PG3 is answered; H3 only after R1 + 7 days and the owner's written confirmation; then H5; then the non-live gate check must print "gates open" before any pilot instruction.
