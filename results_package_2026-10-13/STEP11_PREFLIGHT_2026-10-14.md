# Step 11 (final freeze manifest): preflight report, 2026-10-14

**Status: HELD. No manifest was created and none can be created yet.** This file is a preflight report, not a freeze. Nothing in it opens a gate, authorises a call, or records any approval.

## 1. Why Step 11 cannot be done now
| # | Blocker | Evidence | Who can clear it |
|---|---|---|---|
| 1 | **There is no final pilot decision record with `final_decision = PASS`.** Spec 21.1 row 11 defines Step 11 as "final pilot decision: PASS / STOP; decision record written and hashed; order seed and bootstrap seed taken from it; final freeze manifest hashed". `s11_final_freeze_manifest.py` refuses any other record (checked on a non-PASS record in scratch: "refused: final pilot decision is not PASS", exit 2, nothing written). | no pilot has been run; `human_evidence/` holds only `rehearsal/` | pilot round 1 (or 2) PASS, which needs everything below |
| 2 | Pilot gate is CLOSED: no Step 9 evidence file (H3 not made), no valid owner authorization (H5). | `run_all_checks --quick` gate line, exit 2 | owner and researcher |
| 3 | H3's own prerequisites are open: R1 not recorded, H1 blind check not done, 7-day wait not started, stop rule from the H4 findings holds (22 class B cells, 2 unclassified `SW` cells), advisor answers not received. | `H4_STATUS_AND_BLOCKERS_2026-10-14.md` | researcher, owner, advisor |
| 4 | Decisions that must be final before the freeze are pending: MD-08 (resume), D3 SF/UNP policy, D5 re-code values, MD-03 K2, PG11b scope, MD-10 amendments, advisor review of PG3 (ratified by the owner only, 12.38 row 5). MD-02 (input limit) is a working decision, not ratified. | `OWNER_APPROVAL_PACKAGE.md`, `ADVISOR_DECISION_BRIEF.md`, record 12.38 / 12.39 | owner and advisor |
| 5 | PRD-6 (anchoring of the decision record by a commit or an equivalent store) is undecided and the store is not declared (H7). `research_design/` is untracked in Git. | spec 19.3 PRD-6; `DEFERRED_PATCHES.md` P7 | owner |
| 6 | The tool `s11_final_freeze_manifest.py` lists the files it hashes in a fixed list. That list does not include `s10_integrity.py`, `s10_resume.py`, `s11_pilot.py`, `s12_cli.py` or `s11_final_freeze_manifest.py` itself, although `s10_integrity.py` and `s10_resume.py` now carry experiment-relevant logic (provenance checks, resume rules). The list is part of the official procedure (record 12.31); it was NOT changed. Proposed for the owner: add those files before the manifest is ever written. | `s11_final_freeze_manifest.py`, `build()` | owner decision, then a tested edit |

## 2. State of the Step 10 code that a future freeze would hash (all local, mock-provider tests only)
Adversarial review of the P8 implementation found and fixed these defects (each has a regression test in `test_adversarial_p8.py` that FAILED before the fix, 13 of 19 failing or erroring):
1. A crash between the "resume" ledger entry and moving the status marker left the run permanently refused ("marker does not match the ledger"). Fixed: a marker that precedes only trailing resume entries is accepted.
2. A halted run whose marker was lost (process died before writing it) could be resumed as a generic "process_interruption", bypassing the transport-only rule (for example after an HTTP 503 halt). Fixed: the halt rule is re-evaluated on the persisted records; if it holds, the transport-only evidence and `resume_basis = transport_halt` are required.
3. `os.replace` into `segments/` could overwrite an existing file. Fixed: never overwrites.
4. A missing or altered earlier marker in `segments/` did not block a further resume. Fixed: refused.
5. No exclusion between a live run and a resume (a resume started between two calls of a live run would have appended to the same ledger). Fixed: an operating-system lock (`run.lock`) held by both; released by the system if the process dies.
6. A resume could mix two versions of the scoring code in one run. Fixed: refused when `s10_scoring.py` differs from the provenance entry.
7. Prompt hashes of completed records were not checked on resume. Fixed.
8. `verify_run` accepted a forged but chain-consistent `resume` entry (false previous head or false carried counters). Fixed: both are re-derived from the ledger.
9. The cost stop only ran after a call (one call could cross the limit) and ignored calls without usage. Fixed: checked BEFORE each call with the worst case of the next call, and calls without usable usage are charged at worst case. This is a new halt cause (see section 4).
10. Writes were flushed but not forced to disk. Fixed with `fsync` (about 8-10 ms per call in the suite; negligible for a multi-hour run).

Not found (within the scenarios tested; this is not a proof of safety): stops at each boundary between intent, provider call, raw file, ledger entry, calls line and classified entry; two resumes in a row; reuse of a resume authorization after the head moved; HTTP 429/500/503, timeout, unlisted exception and cost-stop halts; counters across two resumes; duplicate result lines; swapped ledger entries.

Test status on 2026-10-14: `research_design/step10`: 182 tests, OK (no failures, no xfail, no xpass); `run_all_checks --quick`: ALL CHECKS AS EXPECTED (the slow Step 8 suite is skipped by design; gate check exit 2 = CLOSED as expected). No provider was called; no key was used.

## 3. Hashes recorded now (not a freeze)
Files changed in the review: `s10_runner.py` `9f235dec8b6d6525` (before `ab2686e0f89fd78e`), `s10_integrity.py` `f2a109cfdcc27d32` (before `93750c67b373449d`), `s10_resume.py` `c9a6550fe5e95842` (before `9a934233c502d947`), `test_resume.py` `4e7e010f85f348a9` (before `7327e9c4bb07e7e9`), new `test_adversarial_p8.py` `53f229b29b3dbd30`, `run_all_checks.py` `74159df5d168bba9`. Backups: `_backup/p8_resume_20261014/adversarial_round/`. Unchanged: spec `d5fcffad…`, FZ-v1 `14944571…`, Step 7 manifest `202979de…`, Step 8 manifest `09eed00e…`, `s10_scoring.py` `8c0e6b9f…`, `s10_report.py`, `s11_pilot.py`, `s10_analysis.py`.

## 4. Decisions still open (none was made by the assistant)
- **MD-08:** disposition of a call with an intent and no persisted record (the code refuses); definition of "transport-only" (the allow-list is provisional); whether a stop without status marker may be resumed at all (`process_interruption`, owner acknowledgement required); who authorises a resume; whether a resume may follow an implementation fix.
- **Cost stop as an extra halt cause** (spec 13.8 names the SF monitor as the halting rule): it only enforces the existing US$100 limit; accept, or remove the check in `s10_runner.drive`.
- **Step 11 file list** (blocker 6), PRD-6 anchoring, and every item in blocker 4.
- Whether the Step 10 code may still change after the pilot (spec allows "pure implementation fixes"; the provenance entry records the code hashes of every segment, and scoring code must not change between segments).

## 5. Next steps toward pilot authorisation (in dependency order)
1. Send the advisor request; record the answers as a new record entry.
2. Decide the MD-08 items and the cost-stop question; decide the Step 11 file list.
3. R1 (researcher, when true), H1, 7-day wait, H3 (stop rule must be cleared first).
4. Owner writes the pilot authorization (H5), confirms MD-02, re-reads prices (B7), declares the store (H7/PRD-6).
5. Gate check without `--live` prints "gates open"; only then a pilot instruction.
6. After a PASS decision record: write the final freeze manifest with the (extended) file list, backup first, then recompute every hash independently.
