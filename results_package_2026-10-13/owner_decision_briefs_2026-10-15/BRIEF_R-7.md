# R-7: Box R-7: authorize a Step 7 re-freeze

**Status: PENDING OWNER DECISION: READY FOR OWNER.** Prepared 2026-10-15T03:30:47Z. The owner makes this decision; nothing here is adopted. Dependencies: MD-03 / PG11b / H4-STOP.

## 1. Why a decision is needed
Needed only if MD-03 K2, a narrowed PG11b or a codebook revision (H4 option ii) is adopted.

## 2-3. Authoritative sources and verbatim quotations
Quotations are exact text from the files and lines named (excerpts are marked). Interpretation is confined to sections 5-8.

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 20-20**

> | P4 kappa / re-code | MD-03 = K2, and the Step 7 re-freeze authorization (box **R-7**) | K1 (no code) |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 62-62**

> | 16 | Box R-7 | PENDING | authorize a Step 7 re-freeze | Step 7 files, manifests | item 2 or 4 or 7 | part of P4 / rebuild | rebuild sequence | - | x (in that case) | x | - |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 105-105**

> | R-7 | Step 7 re-freeze | MD-03 K2 cannot be applied |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 84-84**

> **If K2, a narrowed PG11b or a codebook revision is adopted, the authorized sequence is:** (1) the formal decision and box R-7 (Step 7 re-freeze); (2) back up the affected Step 7 files and both manifests; (3) edit the files and run the Step 7 tests; (4) write a NEW Step 7 freeze manifest (the old one stays; `reproduce/make_step7_freeze_manifest.py` writes a new path only); (5) rebuild Step 8 with `step8/s8_build.py --out <NEW parent folder>` (the build folder is named by the registry hash, so an unchanged registry reuses the name and the tool refuses an existing target, exit 3); (6) `s8_verify.py`, `impl_b.py`, `test_impl_b.py` and the slow Step 8 suite on the new build; (7) compare the new manifest `inventory` with the old: every one of the 2,026 file hashes must be identical (then the registry, prompts and checker bundle are unchanged and a blind check already performed on the bundle stays valid); only the changed generator-code hashes and `step7_freeze_manifest_sha256` may differ; (8) record, in the closeout report, the old and new values of: Step 7 manifest sha (old `202979de2a88`), Step 8 manifest sha (old `09eed00eeb79`), each changed file (old `s7_recode.py` `ec8f948e6209`, codebook `25a74353be54`, `s7_bundle.py` `10567178b209`), spec `d5fcffadd104` and register `c7d50e115b08` (expected unchanged), and the inventory comparison result; (9) update every reference to the build path or manifest hash (gate `--build`, checklist T1, runbook); (10) only then create H3 against the NEW manifest. Any inventory difference means the registry changed: H1 must be redone. None of this is authorized yet; nothing frozen was modified.


## 4. Original options (labels and order as in the sources)
APPROVE / REJECT.

## 5. Consequences
- Source-defined: if rejected 'MD-03 K2 cannot be applied'.
- Reasoned: moot if K1 / PG11b literal / no revision are chosen.

## 6. Recommendation: NOT ADOPTED
None; depends on those choices.

## 7. Record cross-check
Decision record cross-check: no mention of `R-7` in the record.

## 8. Dependencies
See the dependencies named in the header of this brief; no further source-backed content.

## 9. Information still missing
- None found.

## 10. Owner response (unfilled)
- [ ] APPROVE
- [ ] REJECT
- [ ] not needed (K1, literal PG11b, no revision)
- Owner: ______    Date: ______    Conditions: ______

## 11. Recording instruction
Do not record any outcome until the owner explicitly adopts it. The recording is a new entry in the owner decision record written under the owner's authority; this brief and its recommendation are not an entry and not a decision.
