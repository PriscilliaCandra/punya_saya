# Step 11 file list: proposal (2026-10-14). NOT APPLIED.

The official tool `research_design/step10/s11_final_freeze_manifest.py` (record 12.31) hashes a fixed list of files and refuses unless the pilot decision record says `PASS`. This proposal changes nothing in it. The tool is unchanged (SHA-256 prefix `bbcbf153076a7232`); the change exists only as an inactive diff and an inactive test in `deferred_patches/` (`P13_step11_file_list.diff.INACTIVE`, `P13_test_step11_file_list.py.INACTIVE`) and needs the owner's approval before anyone applies it. No manifest exists; none can be written before a PASS record exists.

## 1. Method (reproducible)
A static import analysis (`ast`) starting from the run lifecycle -- `s10_runner`, `s10_resume`, `s10_integrity`, `s11_pilot`, `s10_report`, `s12_cli`, `s11_final_freeze_manifest`, `s9_blindcheck` (H3 evidence evaluator), `s8_verify` (build verifier used by the gate) -- collected every project module (steps 7-10 and Implementation A) they import. Each reachable module was then compared with (a) the tool's current list, (b) the Step 7 freeze set (11 files, already in the list), (c) the Step 8 generator hashes (15 files, bound by the Step 8 manifest that the list hashes). Result: **24 files are hashed today; 7 reachable files are not.** The proposed list (31 files) leaves nothing reachable un-hashed; this was checked on a synthetic PASS record in memory, without applying the change.

## 2. Matrix
| File | Role in the experiment | Hashed today | Proposed | Reason |
|---|---|---|---|---|
| spec v2.7, FZ-v1, parameter justification record, methodology freeze manifest v2.7, Step 7 freeze manifest | controlling documents | yes | keep | official procedure |
| Step 7 freeze set (11 files: codebook, battery, parser battery, prompt specification, bundle, core, decision, diagnostic, parser, recode, refcheck) | prompts, parser, decision script, coding material | yes | keep | official procedure; `s7_decision.py` also supplies the halt rule used by the runner |
| `implementation_a/impl_a.py`, `step9/impl_b.py` | independent builders of the registry | yes | keep | gate checks agreement |
| `step8_output/step8_build_*/manifest.json` | binds spec, FZ, Step 7 manifest, 15 generator files, 2,026 published files | yes | keep | official procedure |
| `step10/s10_scoring.py`, `s10_analysis.py`, `s10_runner.py`, `s10_report.py`, `s12_coding.py` | scoring, analysis, run, report, coding | yes | keep | official procedure |
| `step10/s10_integrity.py` | post-run verification, observed-cost accounting; **also imported by the runner** (`RunState.add` uses its token accounting for the cost stop) | **no** | **add** | determines run behaviour and decides whether a run is valid |
| `step10/s10_resume.py` | resume of an interrupted or halted run (not adopted; MD-08) | **no** | **add** | part of the run lifecycle; its absence from the hash list would let it change unnoticed |
| `step10/s11_pilot.py` | produces the pilot report and the decision record that the freeze depends on | **no** | **add** | the decision record is built by this code |
| `step10/s12_cli.py` | command line over `s12_coding.py` | **no** | **add** | low cost, completes the coding path |
| `step10/s11_final_freeze_manifest.py` | the tool that writes the manifest | **no** | **add** | binds the version of the procedure itself |
| `step8/s8_verify.py` | the build verifier that the runner's gate calls; not among the 15 Step 8 generator files (a verifier independent of the builder) | **no** | **add** | decides whether a run may start |
| `step9/s9_blindcheck.py` | evaluator that produces the Step 9 evidence (H3) | **no** | **add** | decides whether the gate opens |
| `step10/sf2_variants_analysis.py`, `step7/s7_outcomes.py`, `step7/s7_manifest_items.py` | analysis-only, proposed-not-adopted policy, and a Step 7 manifest helper | no | **do not add** | not part of the harness or not adopted (`s7_outcomes.py` is the proposed 18.2 policy); `s7_manifest_items.py` is already hashed inside the Step 7 manifest |
| `test_*.py` (Step 7, 8, 9, 10) | verification | no (Step 7 tests are in the Step 7 manifest) | **do not add** | tests are evidence, not the experiment; record the test run (names, counts, date) next to the manifest instead |
| owner authorization, evidence file, resume authorization | per-run inputs | no | **do not add** | each run's first ledger entry records their SHA-256 (provenance), which is stronger than a global list |
| `templates/`, `reproduce/`, `human_evidence/`, the owner decision record 12.x, `backend/`, `paper/` | operations, documents, other study track | no | **do not add** | not executable parts of the v2.7 experiment; the owner decision record is append-only and changes after the freeze |

## 3. Related rules that the list cannot enforce (decisions, not changes)
- **Code freeze point.** Spec 13.6 allows changes to executable code later only as a "pure implementation fix" (H1-H4: code hash before and after, byte-identical regression, logged reason). Finish every Step 10 change BEFORE the pilot, so that the pilot, the final freeze manifest and the main run use one code version.
- **Pilot-to-main consistency.** Each run's first ledger entry records the hashes of the code that drove it. A check that the main run's recorded code hashes equal the final freeze manifest (and that the pilot's did) is NOT implemented. It is a possible small addition after the owner decides.
- **Decision record anchoring (PRD-6) and the store (H7)** are unresolved; the freeze manifest can hash the decision record but cannot anchor it.

## 4. To apply (only after the owner approves; the assistant has not done this)
1. Back up `s11_final_freeze_manifest.py`.
2. `patch` the diff `P13_step11_file_list.diff.INACTIVE` onto it; copy `P13_test_step11_file_list.py.INACTIVE` to `research_design/step10/test_step11_file_list.py`.
3. Run the test (it must pass), the whole Step 10 suite, and `run_all_checks --quick`.
4. Record the change and the new hash in the decision record.
