# MD-04: FZ hash contract and file list (with A-1 and A-2)

**Status: PENDING OWNER DECISION: READY FOR OWNER.** Prepared 2026-10-15T03:30:47Z. The owner makes this decision; nothing here is adopted. Dependencies: none beyond those named below.

## 1. Why a decision is needed
Spec 13.2 requires the FZ set to be hashed before the first pilot call; the specification does not define the FZ hash object (C-03).

## 2-3. Authoritative sources and verbatim quotations
Quotations are exact text from the files and lines named (excerpts are marked). Interpretation is confined to sections 5-8.

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 57-57**

> | 11 | MD-04 + A-1 list + A-2 | PENDING | procedure, list L-A/B/C or own, include/exclude Step 10 scoring files | `fz_index.py` (new), `fz_freeze/*` (new) | items 2-10 settled for the official hash | P5 (activation) | P5 7 tests; official computation once; `verify` | - | - | x | - |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 100-100**

> | MD-04 | P5, the FZ hash | no FZ hash exists, so the first pilot call is not allowed (spec 797) |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 135-139**

> ## MD-04 FZ hash contract (C-03, C-18, C-19) — needs your file list (details in Appendix A)
> - **Decision/recommendation:** the FZ hash = SHA-256 of a canonical index {path -> SHA-256} of the listed FZ files, computed ONCE before the first pilot call, stored as a new file, recorded in the decision record and every run manifest, recomputed by the tool (`verify`); enforcement by the gates needs the separate box **E-1**. **L-B (19 files, Appendix A) is a recommendation, not an adopted choice.** L-C (21 files) is possible only if you adopt, in the same entry, an explicit supplementary rule for H1-H4 fixes to the scoring and analysis files (draft wording in Appendix A, A-2). Owner + advisor.
> - **Consequences:** any later change of a listed file changes the hash (new FZ version, re-pilot); the decision record, run folders and the final freeze manifest stay outside the index. **Alternatives rejected:** chain of existing manifest hashes; "researcher-supplied, unverified" (today).
> - **Affects:** spec 797, 662, 1190; new `fz_index.py` (inactive P5, 7 tests); gate change in `s10_runner.py` (a separate approval). **Prerequisite:** the list, the A-2 answer and approval of the procedure; for the OFFICIAL hash additionally MD-01, MD-03, MD-05, MD-06, MD-07 and MD-10 settled and your instruction at that point.
> - `[ ] APPROVE procedure  [ ] REJECT  [ ] AMEND: ______  | File list chosen: [ ] L-A  [ ] L-B  [ ] L-C  [ ] own: ______  | A-2: [ ] include [ ] exclude the Step 10 scoring files  | Owner: ______  | Date: ______`

**`results_package_2026-10-13/MASTER_PROPOSED_DECISION_RECORD.md` lines 138-145**

> ### MD-04 FZ hash contract (C-03, C-18, C-19)
> - **Class:** record entry (clarification of an undefined object) + code after adoption.
> - **Rule quoted:** spec §10 line 662 (the record contains "the FZ hash"), §13.2 line 797 (FZ "hashed before the first pilot call"), §21.1 row 11 ("final freeze manifest hashed"); record 12.21 row 7.
> - **Proposed text:** "The FZ hash is the SHA-256 of the canonical JSON (sorted keys, compact separators, UTF-8, final LF) of the index {path → SHA-256} of ______ [list], computed once before the first pilot call, stored as the file ______, and recorded in the decision record and every run manifest. It excludes the decision record, run folders, the Step 10 harness and the final freeze manifest. The final freeze manifest of step 11 is a later object that contains the hash of the decision record. The runner and the decision script recompute the index and refuse on a mismatch."
> - **Alternatives:** chain of existing manifest hashes (CRB design B); accept 'researcher-supplied, unverified' (status quo).
> - **Acceptance:** hand recomputation equals the stored value; a one-byte change of an FZ file changes it; the gate refuses without it.
>
> - **Owner decision: PENDING | Advisor decision: PENDING | Date: PENDING | Option chosen: PENDING**

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 188-225**

> ## Appendix A. FZ index request (P5; confirmed against spec 797 and FZ-v1)
> **Contract of the inactive tool (checked against `deferred_patches/P5_fz_index.py.INACTIVE`):** input = repository root + a text file listing relative paths (one per line); output = a NEW file with canonical JSON {path: sha256} (sorted keys, compact separators, ASCII, one final LF), the FZ hash printed = SHA-256 of that file; `verify` recomputes and compares (optionally with an expected hash); it never overwrites, refuses missing, duplicate, absolute or `..` paths and a list that contains the output file; reads no network. It matches spec 797 ("FZ ... hashed before the first pilot call") and 662/1190 (the hash is recorded in the decision record; the final freeze manifest is a later object). It does not conflict with FZ-v1: FZ-v1 "carries no self-hash" and defines only `register_canonical_sha256` for the register; the stale decision-record entry in FZ-v1 `artifact_hashes` (C-19) stays historical because the decision record is outside the index. **Gate enforcement is NOT part of the tool** (a gate change needs your approval).
> **Your decisions:**
> - **A-1 The list: comparison.** Spec 797 enumerates the FZ set. The Step 8 build manifest already records the SHA-256 of the 15 generator-code files, the build inventory (2,026 files), the spec, the FZ-v1 register and the Step 7 manifest; the gate runs `s8_verify` against it.
> | | L-A (4 files) | L-B (19 files) | L-C (21 files) |
> |---|---|---|---|
> | Scope | spec; FZ-v1; Step 7 manifest; Step 8 manifest | L-A + the 15 generator-code files the Step 8 manifest hashes (`impl_a.py`; 11 Step 7 freeze-set files incl. codebook, parser, `s7_decision.py`, `s7_recode.py`; 3 `step8/` build files) | L-B + `step10/s10_scoring.py`, `step10/s10_analysis.py` |
> | Binds directly | manifests only; everything else by hash inside them | codebooks, parser grammar, decision script, generator code (spec 797 items) | also the pilot SF decision code and the §18 analysis code |
> | Left out | the 15 files are bound only through manifest hashes (a drift is caught by the gate's verifier, not by the index) | the Step 10 scoring/analysis, runner, integrity, report, glue | runner, integrity, report, glue |
> | Consequence for later fixes | none beyond Step 7/8 rules | harness fixes (H1-H4) stay outside the index, as spec 13.6 intends | any H1-H4 pure fix to `s10_scoring.py`/`s10_analysis.py` would change the index although H4 says a pure fix creates no new FZ version: a **supplement rule** is required (the fix is logged with code hashes before/after and the index is re-issued as a logged supplement) |
> | Verdict | smallest; relies on verifier | **recommended**: matches spec 797 items directly and the H1-H4 mechanism | only if you want the decision/analysis code bound and accept the supplement rule |
> - **Copy-paste lists** (paths relative to the repository root `D:\research s2`; all verified to exist on 2026-10-13; one path per line):
>   - L-A:
>     research_design/SCENARIO_CONSTRUCTION_SPECIFICATION_v2_7_DRAFT.md
>     research_design/PARAMETER_FREEZE_MANIFEST_FZ_v1.json
>     research_design/step7/STEP7_PROMPT_SPECIFICATION_FREEZE_MANIFEST_v1.json
>     research_design/step8_output/step8_build_7a6bbe465c66/manifest.json
>   - L-B = L-A plus:
>     research_design/implementation_a/impl_a.py
>     research_design/step7/CODEBOOK_S2_S3_v1_DRAFT.md
>     research_design/step7/codebook_battery_v1.py
>     research_design/step7/parser_battery_v1.py
>     research_design/step7/prompt_specification_v1.py
>     research_design/step7/s7_bundle.py
>     research_design/step7/s7_core.py
>     research_design/step7/s7_decision.py
>     research_design/step7/s7_diagnostic.py
>     research_design/step7/s7_parser.py
>     research_design/step7/s7_recode.py
>     research_design/step7/s7_refcheck.py
>     research_design/step8/s8_build.py
>     research_design/step8/s8_construct.py
>     research_design/step8/s8_gates.py
>   - L-C = L-B plus:
>     research_design/step10/s10_scoring.py
>     research_design/step10/s10_analysis.py
> - **A-2 Decision you must make:** MD-04 as drafted excludes "the Step 10 harness", while spec 797 lists "scoring definitions" and "primary outcome, denominators and reporting structure (§18)", implemented in `s10_scoring.py` and `s10_analysis.py`. Spec 13.6 protects executable code by H1-H4 (byte-identical regression, logged hashes) and says a pure implementation fix creates no new FZ version. Revised recommendation (correcting the earlier one): exclude them (L-B) and rely on H1-H4, because binding them in the index conflicts with H4 unless a supplement rule is adopted; note that a change of the pilot decision rule itself is not a pure fix and must therefore be settled BEFORE the hash. If you choose L-C, adopt the supplement rule in the same entry. **Draft wording (PROPOSED, for you to amend):** "A pure implementation fix (H1-H4) to a listed Step 10 scoring or analysis file does not create a new FZ version. It is logged with the code hashes before and after and the regression result, and the FZ index is re-issued as a numbered supplement that lists the changed file hashes; the original index is kept unchanged. Any other change to a listed file creates a new FZ version."
> - `[ ] procedure approved  | List: ______  | Timing accepted [ ]  | Owner: ______ Date: ______`

**`results_package_2026-10-13/deferred_patches/DEFERRED_PATCHES.md` lines 47-50**

> ## P5 FZ index tool and enforcement (MD-04; C-03, C-18, C-19)
> - **Source.** spec 662, 797, 1190; record 603; `s7_decision.py` 163-176 (accepts any 64-hex string); `s11_final_freeze_manifest.py`; MPR section 6.
> - **Why held.** The draft's file list is blank and the contract (object, timing, exclusions, storage) is undecided; enforcement touches `s10_runner.check_gates` (a gate change is itself a decision item, plan section 2) and `s7_decision.py` is frozen. Tool written without the list would invent the object.
> - **Design after adoption.** New `fz_index.py`: canonical JSON {path -> SHA-256} for the adopted list, UTF-8, sorted keys, compact separators, final LF; writes a NEW file only; the FZ hash is the SHA-256 of that file; excludes the decision record, run folders, step10 harness and the final freeze manifest (no circularity: the final manifest hashes the record later). Gate: pilot and main refuse without a recorded hash or on mismatch; check placed in the runner and in `s11_pilot decide` (not in the frozen `s7_decision.py`). **Acceptance:** hand recomputation equals the stored value; one byte changed in a listed file changes it; missing or mismatching hash refused; no cycle (the index excludes its own output).


## 4. Original options (labels and order as in the sources)
Options: procedure approve/amend; list L-A (4 files), L-B (19), L-C (21) or the owner's own paths; A-2 include / exclude Step 10 scoring files (labels in the quoted Appendix A).

## 5. Consequences
- Source-defined: 'MD-04 ... no FZ hash exists, so the first pilot call is not allowed (spec 797)' (OAP consequence table).
- Reasoned: this FZ-index list is a DIFFERENT object from the 31-file P13 list approved in entry 12.44 (final freeze manifest); the sources examined do not state how the two relate.

## 6. Recommendation: NOT ADOPTED
Source recommendation (NOT ADOPTED): the 'Recommendation' lines of the quoted OAP section.

## 7. Record cross-check
Decision record cross-check (read-only search of `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` for `FZ hash`, `MD-04`, `P-2`): lines [251, 507, 547, 585, 599, 603, 605, 608] .... Hits are mentions only. Entries 12.40-12.45 were read for this check: they either do not mention this item or state it as not decided (12.43, 12.44).

## 8. Dependencies
See the dependencies named in the header of this brief; no further source-backed content.

## 9. Information still missing
- The relation between the FZ-index list and the P13 list (not stated in the sources examined).

## 10. Owner response (unfilled)
- [ ] approve the procedure
- [ ] FZ file list = L-__ (or own paths: ______)
- [ ] A-2 = include / exclude
- [ ] REJECT / AMEND: ______
- Owner: ______    Date: ______    Conditions: ______

## 11. Recording instruction
Do not record any outcome until the owner explicitly adopts it. The recording is a new entry in the owner decision record written under the owner's authority; this brief and its recommendation are not an entry and not a decision.
