# MD-10 final wording (PROPOSAL) and H1/H3 blocker audit, 2026-10-15

Status: PREPARATION ONLY. Nothing here is a decision. MD-10 is NOT approved; it stays PENDING until the owner's decision is recorded as a new entry. R-7 stays NOT AUTHORIZED. No registry, manifest, bundle, code (beyond the MD-06 safe-stop of this day), codebook, specification or evidence was changed for this document. No registry/prompt/expected-state content was opened. No provider call. Gate CLOSED.

Sources read: `OWNER_APPROVAL_PACKAGE.md` (rows 1-20, H3 chain and invalidation table, MD-10 section), `MASTER_PROPOSED_DECISION_RECORD.md` MD-10, decision record 12.5, 12.23 (F-3, I-6, PRD-8, PC-2 rows), 12.28 (Step 8 choices and results), 12.38, 12.44-12.50, `RESEARCHER_CHECKLIST_H4_H1_H3_2026-10-15.md`, and the Step 8/9 code named below.

## 1. MD-10 proposed final wording (for the owner to approve, amend or reject)

Replaces the source text "(PC-2) ... (I-6) informational diagnostic, gate counts stay 30 and 14; (P-3 item 1) ...; (F-3) closed; (PRD-8) unchanged; the Step 8 choices ... confirmed / amended". The owner's direction in 12.50 row 8 is applied: no "14", no "F-3 closed" without evidence, no widened PASS claim.

> **MD-10 (owner, sole decision-maker under 12.50 row 0).** The owner CONFIRMS, without amending any Step 8 choice:
> 1. **PC-2**: the pilot registry is built and gated informationally at Step 4 and as a hard gate at Step 8 by the same code (reading recorded in 12.28).
> 2. **I-6**: the six-reading check stays an informational count only; it is not a gate and is not part of any gate count.
> 3. **P-3 item 1**: `s2_values` "none" is reported as a count outside its denominator (as worded in `MASTER_PROPOSED_DECISION_RECORD.md` MD-10; the P-3 list itself remains a proposal).
> 4. **F-3**: NOT "closed". Recorded status: the register-versus-member consistency of `D_dist` and `tau_F` is enforced indirectly by equivalence check E-PAR of the Step 8 build (any difference rejects the build); there is no dedicated gate, and E-PAR compares the valid member only (the violating member's `D_dist`/`tau_F` are covered through E-PROMPT, the rendered-prompt equality). F-3 stays "open, enforced indirectly" in 12.23 terms.
> 5. **PRD-8**: unchanged (formally pending in spec 19.3; not applicable under OD-4/DP1, all 12 primary cells precision-targeted).
> 6. **Step 8 choices of 12.28 confirmed as recorded**: F-4 architecture 1, PG4 test, PG11a projection bundle of 624 files, A6b computed from rendered numerals. The PG3 reading is governed by 12.38 row 5 and is not re-decided here.
> 7. **Results are confirmed only as recorded in 12.28**: 30 numeric gates PASS on the generator's templates and on A's builders; PG1-PG10, PG11a, PG11b builder test, PG12, A1b, A6b PASS on all 1,248 main and 96 pilot prompts. No other PASS claim is made, and the same-author limit stated in 12.28 stands.
> 8. This confirmation binds nothing and changes no file, so it does not alter the Step 8 build manifest, the 624-file projection or any H1/H3 input.

Effect if approved as worded: no rebuild, no H1 invalidation, MD-10 ceases to be a prerequisite blocker of H3 and of the FZ hash. If the owner AMENDS a Step 8 choice or makes I-6 a gate: `step8/s8_*.py` and/or the projection change, the build manifest changes, H1 (if done) is void.

## 2. F-3 verification performed today (read-only, in memory)

- Chain by code reading: FZ register rows 5/6 -> `s8_build.a_register` (`D_dist=row5`, `tau_F=row6`) -> `impl_a.build_pac_template` (`N, tau, D = reg.N, reg.tau_F, reg.D_dist`, line 419) -> `s8_build.equivalence` E-PAR (line 184: `a.valid.tau_F == t["valid"]["tau_F_s"]` and `a.valid.D_dist == t["valid"]["D_dist"]`); the generator reads its own values from the register (`s8_construct.py` line 41).
- Mutation check (script `F3_register_member_mutation_check_2026-10-15.py`, pilot registry, in memory only, nothing written): baseline E-PAR/E-GATE/E-PROMPT problems 0/0/0; one generator member with `tau_F_s` + 1 -> E-PAR problems 1; one with `D_dist` numerator + 1 -> E-PAR problems 1. So a register-versus-member inconsistency of the valid member IS detected and would reject the build.
- Not shown: the violating member is not compared in E-PAR (only through E-PROMPT, not mutation-tested here); the main registry was not mutated (pilot only, same code path). Hence the wording above says "enforced indirectly", not "closed".

## 3. Blockers: what voids H1, what does not (from source tables, with today's status)

"Voids H1" = changes the registry, prompts or checker bundle (the 624 texts). "Voids H3" = changes any item bound into the Step 8 build manifest (spec hash, FZ register hash, Step 7 manifest hash, 15 generator-code files, 2,026-file inventory).

| Item | Today's status (record) | Voids H1? | Voids H3 (if H3 already created)? | Evidence / note |
|---|---|---|---|---|
| PG3 | owner ratified the "contiguous" reading (12.38 row 5); advisor review replaced by 12.50 | Only if the owner later reverts to the strict reading (rebuild of steps 3-9; strict reading would reject 90 of 104 MIL templates) | Yes in that case | OAP H3 table. Ratified = no change. |
| MD-10 | PENDING; wording above | Only if a Step 8 choice is amended or I-6 becomes a gate | Same | "confirm" changes nothing (OAP line 79). |
| F-3 | open, enforced indirectly | No (no code change proposed) | No | Section 2. A new dedicated gate would touch `step8/s8_*.py` = bound file -> would void H3 and change the manifest; it is NOT proposed. |
| K2 (decided, not applied) | chosen 12.47/12.49; blocked by R-7 | Not by itself: needs a Step 7 re-freeze; H1 stays valid ONLY if the new Step 8 manifest has an identical 2,026-file inventory. Identity has NOT been compared (no re-freeze was authorized or run) -> cannot be concluded | Yes always (`s7_recode.py`, codebook, Step 7 manifest hash change -> new manifest hash; H3 must be made against the NEW manifest) | OAP line 84 sequence step 7. |
| R-7 | NOT AUTHORIZED | n/a | n/a | gate for K2. |
| PG11b (a), D3 C, D5, MD-01, MD-02 | decided 12.47/12.48; none touches the registry | No | PG11b narrowing would (not chosen: "keep literal") | verify "keep literal" was the recorded choice before H3. |
| H4 stop rule and the two SW cells (B10, B36) | waiting: researcher's note + owner's choice among (i)/(ii)/(iii) | No | Yes only if the owner decides a codebook revision (codebook is bound) | `RESEARCHER_CHECKLIST` section 2. |
| MD-04 / P5 `fz_index.py` / E-1 | MD-04 procedure approved with list L-B (12.47/12.48); P5 NOT authorized; E-1 direction approved, not implemented (12.50) | No | No (touches `step10/*`, not the manifest) | OAP "Not able to change H3". Needed before the FZ index/pilot, not before R1/H1. |
| MD-06 safe-stop | implemented today, mock-only (suite 238 OK, quick check OK) | No | No | `step10/*` not bound. |
| H5 (authorization file) | not created; owner writes `input_tokens_per_call_assumed` (>= 1,016) and `max_input_characters` | No | No | needed for the pilot, not for R1/H1. |
| Anything done as an edit of the spec or the FZ register | none | Yes if it happened | Yes | decisions are recorded in the record, not in the spec. |

Conclusion on H1: with PG3 ratified, MD-10 confirmed as worded in section 1 (no amendment) and no change to Step 8 code, the 624-file projection is stable. The only open item that can void H1 is K2 via R-7, and only if the post-re-freeze inventory differs (unverified).

## 4. R-7 versus K1 (specific owner options; none applied)

Facts: K2 = Cohen's kappa computed and reported with the label "intra-rater consistency; no inter-rater reliability claim", never claimed (12.47, 12.49). Applying it needs a Step 7 re-freeze (R-7), a new Step 7 manifest, a rebuild of Step 8 into a new folder, and a comparison of the 2,026 file hashes; H3 is then made against the new manifest. K1 = kappa neither computed nor shown (current code/codebook): no change, no re-freeze.

| Option | Effect | Risk | Cost |
|---|---|---|---|
| **A. Authorize R-7 now, before R1/H1** | K2 applied; inventory compared; if identical, H1 is performed once on the final bundle; if not identical, nothing is lost because H1 has not started | none for H1 (done first); the re-freeze must pass the Step 7 tests | the re-freeze work (assistant can do it mock/offline; no provider call) |
| **B. Revert K2 to K1 (new owner entry)** | No re-freeze; nothing bound changes; kappa not computed; supersedes the K2 choice of 12.47/12.49 | loses the kappa output; later K2 would again need R-7 and could void a finished H1 | none |
| **C. Keep K2 chosen, R-7 not authorized, start R1/H1 now** | H1 proceeds on the current bundle | if R-7 is authorized later and the inventory differs, H1 (624 rows) must be redone; if identical, only H3 is made against the new manifest | possible loss of the 624-row effort |

Recommendation (assistant's, not a decision): A, because it is the only option that cannot waste the 624-row effort and keeps K2. B if the owner prefers not to touch Step 7. C is not recommended.

## 5. Consolidated owner decisions actually required (one list)

1. **MD-10**: APPROVE the wording of section 1 / AMEND / REJECT. (Prerequisite of H3 and of the FZ hash; not of R1.)
2. **R-7 vs K1** (section 4): A / B / C. This is the only decision that can still void H1.
3. **H4 stop rule**: choose (i), (ii) or (iii) (`RESEARCHER_CHECKLIST` section 2) after the researcher's dated note on B10/B36 (the researcher's own act). Needed before H3.
4. **Authorize P5 `fz_index.py` / E-1 implementation**: needed before the FZ index and the pilot gate enforcement; not before R1/H1. (Source order: after MD-01, MD-03, MD-05, MD-06, MD-07, MD-10 are settled.)
5. **B-1 follow-up-round rule** (12.50 row 2): documented before MD-06 is used in a pilot.
6. **H5** (owner's own act, later): the authorization file with `input_tokens_per_call_assumed` and `max_input_characters` written by the owner.
7. P11 / P12: whether the new tool/script join the freeze hash list (open question; only when they are written).

## 6. Acts only the researcher/owner can do (not done, not simulated)

- **R1**: only after items 1-2 above are decided and stable. Command (run by the researcher at the true moment of last viewing): `powershell -NoProfile -Command "[DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ssZ')"`; save the value plus the sentence "last time I viewed rendered registry content or expected states" as a NEW file `results_package_2026-10-13/human_evidence/clock/last_registry_view_utc.txt` (create the folder yourself). Never back-dated, never written by anyone else.
- **H1**: 624 rows, per `RESEARCHER_CHECKLIST` section 4, precheck BEFORE evaluation: `python -B -I results_package_2026-10-13/reproduce/precheck_human_sheets.py --kind blindcheck --sheet <csv>`; evaluation writes new files only: `python -B -I research_design/step9/s9_blindcheck.py --sheet <csv> --bundle research_design/step8_output/step8_build_7a6bbe465c66/main/checker_bundle --evaluation-out <new evaluation.json>`. No rows edited after seeing a verdict. No model is used to fill rows.
- **Wait**: gate rule `(completed_utc - last_registry_view_utc).days >= 7` (whole days, floored). The earliest H3 date is R1 + 7 full days.
- **H3**: command in `RESEARCHER_CHECKLIST` section 5, after the preconditions listed there.

## 7. Work the assistant can still do while waiting (safe; none changes H1 evidence)

Prepare the P5/E-1 implementation plan and tests (do not implement before authorization); prepare the B-1 follow-up-round text for the owner; prepare the H5 authorization TEMPLATE (blank values); write the K2/R-7 re-freeze runbook so that option A can start on one word from the owner. None of these opens R1-protected content.
