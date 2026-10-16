# Step 11 code readiness and decision check (2026-10-14, later run)

Status: **HELD. Nothing was applied, no manifest exists, no gate was opened, no provider was called.**

## 1. Written decisions found (read from the files, not from earlier reports)
| Item | What the files show |
|---|---|
| Owner decision record `STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` | Last entry is 12.39 (2026-10-14, the four H4 issues). SHA-256 prefix `4bba65210c734181`, unchanged since it was written. **No entry about MD-08, MD-02, D3, D5, the Step 11 file list, the cost stop or the code freeze exists.** |
| `MD08_DECISION_PACKAGE_2026-10-14.md` decision block | All six rows are `PENDING` (owner, advisor, option, date). |
| Advisor answer | None exists in the project (no file, no record entry). The request itself has not been recorded as sent. |
| R1 / `human_evidence/clock/`, `step9_evidence.json`, pilot authorization, resume authorization, pilot decision record | None exists. `human_evidence/` holds only `rehearsal/`; `templates/` holds the two empty templates. |
**Conclusion:** there is no enacted decision to apply. Consequently nothing that needs a decision was applied: not the P13 patch, not any MD-08 code change, not the cost-stop choice.

## 2. P13 (Step 11 file list)
- The diff `P13_step11_file_list.diff.INACTIVE` still applies cleanly to the unchanged tool (`patch --dry-run -p1 -N` from the repository root: "checking file ...", no rejection; the tool hash stayed `bbcbf153076a7232`).
- Guard test, run in memory on a synthetic PASS record: against the CURRENT tool it reports exactly seven reachable modules missing (`step10/s10_integrity.py`, `s10_resume.py`, `s11_final_freeze_manifest.py`, `s11_pilot.py`, `s12_cli.py`, `step8/s8_verify.py`, `step9/s9_blindcheck.py`); against the PROPOSED list it reports none. Tests and the unadopted `s7_outcomes.py` are not hashed in either.
- Not applied: the list is part of the official procedure (record 12.31) and needs the owner's approval.

## 3. SF1 in the code against spec 13.4 and 13.8
Spec 13.4 (line 809): **SF1 = "Transport failure: HTTP/API error or timeout."** Spec 13.8: "A transport-only halt (SF1) may resume only under the identical FZ version." Results of `s10_scoring.classify` and `s10_resume.is_transport_only` on synthetic records (no scoring code was changed):

| Case | Scoring outcome | Flags | SF1 only, no response text (literal reading of 13.8 '(SF1)') | Resumable now (strict allow-list) |
|---|---|---|---|---|
| TimeoutError (no status) | SF | SF1 | yes | yes |
| URLError (no status) | SF | SF1 | yes | yes |
| ConnectionResetError (no status) | SF | SF1 | yes | yes |
| SSLError (no status) | SF | SF1 | yes | yes |
| RuntimeError raised by the provider (software fault) | SF | SF1 | yes | no |
| KeyError raised by the provider (software fault) | SF | SF1 | yes | no |
| HTTP 400 | SF | SF1 | yes | no |
| HTTP 401 | SF | SF1 | yes | no |
| HTTP 403 | SF | SF1 | yes | no |
| HTTP 408 | SF | SF1 | yes | no |
| HTTP 429 | SF | SF1 | yes | no |
| HTTP 500 | SF | SF1 | yes | no |
| HTTP 502 | SF | SF1 | yes | no |
| HTTP 503 | SF | SF1 | yes | no |
| HTTP 504 | SF | SF1 | yes | no |
| HTTP 200 with an error marker and text (fail-closed, record 12.36) | SF | SF1 | no | no |
| HTTP 200, MAX_TOKENS | SF | SF3 | no | no |
| HTTP 200, no candidate and no text | SF | SF4 | no | no |
| HTTP 200, ordinary verdict | satisfied | - | no | no |

Findings (no category was widened or narrowed here):
1. **Scoring conforms to row 809:** every HTTP/API error status and every timeout/connection failure is SF1 (not SF1 + anything else).
2. **Scoring also gives SF1 to any exception raised inside the provider** (for example `RuntimeError`, `KeyError`), because the runner records the exception class name in `error` and scoring treats any `error` as SF1. A software fault is therefore indistinguishable from a transport failure in the scoring output. This is existing, unchanged behaviour; whether it is acceptable is not decided.
3. **The resume rule is stricter than the literal "(SF1)" in 13.8:** only the first four rows are resumable. HTTP 408/429/500/502/503/504 and exceptions outside the allow-list are refused. This narrower reading was chosen as the fail-closed default and has no decision behind it; MD-08 row 2 asks the owner to choose (strict, literal, or a transient-status list). Until then the code stays as it is.

## 4. Step 10 code versions and the freeze point
Not at the version that would be frozen: the pending decisions would change these files, so declaring a code freeze now would be premature.
| Pending decision | Files that would change |
|---|---|
| MD-08 row 1 (disposition of an intent without result) | `s10_resume.py`, `test_resume.py` |
| MD-08 row 2 (transport-only definition) | `s10_resume.py`, tests |
| MD-08 row 3 (killed process) | `s10_resume.py`, tests |
| MD-08 row 4 (who authorises) | `s10_resume.py` (only if the advisor must co-sign) |
| MD-08 row 5 (code differences on resume) | `s10_resume.py` |
| MD-08 row 6 (cost stop) | `s10_runner.py` |
| P13 (file list) | `s11_final_freeze_manifest.py`, new `test_step11_file_list.py` |
| D3/D5 or a codebook revision | possibly Step 7 files and a rebuild (then Step 8 hashes change) |
Candidate hashes of the files that the proposed list would hash (a snapshot of today; NOT a freeze manifest, written nowhere else, to detect drift):
| path (relative to `research_design/`) | SHA-256 |
|---|---|
| `METHODOLOGY_FREEZE_MANIFEST_v2_7.json` | `b93ff372d44854e19266159f389f29e8051a4f678ffbbf4a35b9a85a602bb1d3` |
| `PARAMETER_FREEZE_MANIFEST_FZ_v1.json` | `149445715a8280f4079bcd34d3594e25fe1b6b30118e382e96e94360c0faf338` |
| `PARAMETER_JUSTIFICATION_RECORD_DRAFT.md` | `a1b2148766965d0b7a35f5996e83e77cf9c303eece09e275589f5939f7df7de1` |
| `SCENARIO_CONSTRUCTION_SPECIFICATION_v2_7_DRAFT.md` | `d5fcffadd1045fc0c86a7c84eb8d51592d807576b6a51b712cef025164082ca8` |
| `implementation_a/impl_a.py` | `daa2cd49b86ed1a546e95478bc3f40c1fc131ea52d4622b981e4e3b117f018ee` |
| `step10/s10_analysis.py` | `7993a7347e07f3916ebf6f758d9e0cf3478a6c0b98ba78b4ae6ad304d2be4dc7` |
| `step10/s10_integrity.py` | `f2a109cfdcc27d326126afef1fdf1590ca7cedb261bb0ca747f033a1578af07d` |
| `step10/s10_report.py` | `f9857e5603941a6c67a53a63efadc2de87291334ab454d0df111b84aaf89c68a` |
| `step10/s10_resume.py` | `c9a6550fe5e95842f8969c620e36d73a167c1964c56cbaedc3784a134e888390` |
| `step10/s10_runner.py` | `9f235dec8b6d65259eb283633a4924ce0f1faef669b3570c72d7bc428bf0d1a9` |
| `step10/s10_scoring.py` | `8c0e6b9fecb559fb44519bcf7f1d8048ae755e9c63b03ba9264d57f53efc45b2` |
| `step10/s11_final_freeze_manifest.py` | `bbcbf153076a7232a52622670790f65a33fcd818d898fdb7e217e076abe6f762` |
| `step10/s11_pilot.py` | `68fc807f85a7eaa6ed212bb4a234842ef4578b3e4beebb88a65410fd297f5a3a` |
| `step10/s12_cli.py` | `e6de02879a580eebbee1ee8533df4c2b67674507ef9d4442a4c19ec3deec7f0e` |
| `step10/s12_coding.py` | `a571c6ba64fdf651dfd3b6f95b240e789bd95d3fa2809068f4aa94f4f7db84fa` |
| `step7/CODEBOOK_S2_S3_v1_DRAFT.md` | `25a74353be546cf9db27e58acbd8ed7c02bc896cbf5a0c594b1f4de8ed63d53c` |
| `step7/STEP7_PROMPT_SPECIFICATION_FREEZE_MANIFEST_v1.json` | `202979de2a88c1b667c3510fc632b25f7108a11d7fdb103cc3473f2fb7c220f7` |
| `step7/codebook_battery_v1.py` | `8200cfea41e23255242576ace494fa039ce28880d1a443a2326d6900e0107d49` |
| `step7/parser_battery_v1.py` | `82af5d5361561d9812dd0827a061fa609e42a76dc6f03c6dc90ba2ab38296b27` |
| `step7/prompt_specification_v1.py` | `8b9a73e945f0251c648ca2045ce9c0ee2de25581127f905764139229bcae3167` |
| `step7/s7_bundle.py` | `10567178b20976eab4958c98db0fca8bd54eabcfa0cb96727936b4985dfa1636` |
| `step7/s7_core.py` | `64789acb84047f3dabbdd9855baa997317cab637dbb0d7f152cabac98cadea21` |
| `step7/s7_decision.py` | `cf0823f7abdf4b6b44d4efd44006567ac42290350714415e8e11496444f57618` |
| `step7/s7_diagnostic.py` | `5e0f6e707231d66f2ca89b4a0765d6edcde78cdc5bc1e1137e7c9fa6fe9806b6` |
| `step7/s7_parser.py` | `b9d60196c50f8099c0a8319c1308abd40937f7fc3e87e58a30983225c3bd56d8` |
| `step7/s7_recode.py` | `ec8f948e6209147d0ada8fb0018a97068f352cf5dbed3894c9821bacd164bc37` |
| `step7/s7_refcheck.py` | `39e10a85068262c960a475fc30cacc7e43ca5ebc8a8ce395bd41fad8d3bf80d4` |
| `step8/s8_verify.py` | `b9a46f599320e5420510f911a25d3e2d904cb818ee1d4a21b3d81d8c73a833f2` |
| `step8_output/step8_build_7a6bbe465c66/manifest.json` | `09eed00eeb79e04ccaf607a66642417cdbbdfe802b19e580a67f4b9e08c7aaa5` |
| `step9/impl_b.py` | `ada22199bb472d934b4004a3fa6b8ee89551b5cb2f69ac69ca998ac8cc12f600` |
| `step9/s9_blindcheck.py` | `e870b8d03b3179005517ad6431d840cfc260ceca2f01adc7d30d17e84c84752e` |

## 5. Tests run on 2026-10-14 (this run)
- `research_design/step10`: 182 tests, **OK** (no failed, no xfail, no xpass).
- `run_all_checks --quick`: **ALL CHECKS AS EXPECTED**; 22 checks OK, the slow Step 8 suite skipped by design, the gate check returned exit 2 (CLOSED, as expected).
- P13 guard test: see section 2 (not a file in the suite until approved).
- No provider call, no key, no credit used.

## 6. Blockers for Step 11 (unchanged)
1. No pilot `final_decision = PASS` record (the official tool refuses; no pilot can run).
2. Gate closed: no Step 9 evidence (R1, H1, 7 days, H3 not done), no owner authorization (H5).
3. Pending owner/advisor decisions listed in section 1 and section 4.
4. PRD-6 / H7 store not declared.
