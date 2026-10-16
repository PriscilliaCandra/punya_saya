# E-1: Box E-1: enforce the FZ hash in the gates

**Status: PENDING OWNER DECISION: READY FOR OWNER.** Prepared 2026-10-15T03:30:47Z. The owner makes this decision; nothing here is adopted. Dependencies: MD-04.

## 1. Why a decision is needed
Without E-1 the FZ hash exists but is not machine-enforced.

## 2-3. Authoritative sources and verbatim quotations
Quotations are exact text from the files and lines named (excerpts are marked). Interpretation is confined to sections 5-8.

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 16-16**

> | FZ-hash enforcement in the gates (`s10_runner.py`, `s11_pilot.py`) | box **E-1** | P5 activation alone |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 58-58**

> | 12 | Box E-1 | PENDING | enforce the FZ hash in the gates | `s10_runner.py`, `s11_pilot.py` | MD-04, P5 | E-1 | new gate tests, `--quick`, gate check | - | - | - | x (before the pilot) |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 101-101**

> | E-1 | FZ-hash enforcement in the gates | the hash exists but is not machine-enforced; a documented weaker control |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 26-26**

> **Additional authorization boxes (blank):** E-1 `[ ] APPROVE [ ] REJECT`  Q5 `[ ] APPROVE [ ] REJECT`  Q9 `[ ] APPROVE [ ] REJECT`  R-7 `[ ] APPROVE [ ] REJECT`  P7 `[ ] APPROVE [ ] REJECT`  P11 `[ ] APPROVE [ ] REJECT`  P12 `[ ] APPROVE [ ] REJECT`   | Owner: ______  Date: ______

**`results_package_2026-10-13/deferred_patches/DEFERRED_PATCHES.md` lines 47-50**

> ## P5 FZ index tool and enforcement (MD-04; C-03, C-18, C-19)
> - **Source.** spec 662, 797, 1190; record 603; `s7_decision.py` 163-176 (accepts any 64-hex string); `s11_final_freeze_manifest.py`; MPR section 6.
> - **Why held.** The draft's file list is blank and the contract (object, timing, exclusions, storage) is undecided; enforcement touches `s10_runner.check_gates` (a gate change is itself a decision item, plan section 2) and `s7_decision.py` is frozen. Tool written without the list would invent the object.
> - **Design after adoption.** New `fz_index.py`: canonical JSON {path -> SHA-256} for the adopted list, UTF-8, sorted keys, compact separators, final LF; writes a NEW file only; the FZ hash is the SHA-256 of that file; excludes the decision record, run folders, step10 harness and the final freeze manifest (no circularity: the final manifest hashes the record later). Gate: pilot and main refuse without a recorded hash or on mismatch; check placed in the runner and in `s11_pilot decide` (not in the frozen `s7_decision.py`). **Acceptance:** hand recomputation equals the stored value; one byte changed in a listed file changes it; missing or mismatching hash refused; no cycle (the index excludes its own output).


## 4. Original options (labels and order as in the sources)
APPROVE / REJECT (OAP box).

## 5. Consequences
- Source-defined: 'E-1 | FZ-hash enforcement in the gates | the hash exists but is not machine-enforced; a documented weaker control'.
- Reasoned: changes `s10_runner.py` and `s11_pilot.py` (both listed) after MD-04/P5.

## 6. Recommendation: NOT ADOPTED
None offered; depends on MD-04.

## 7. Record cross-check
Decision record cross-check: no mention of `E-1` in the record.

## 8. Dependencies
See the dependencies named in the header of this brief; no further source-backed content.

## 9. Information still missing
- No drafted gate-change text was found (P5 deferred patch: 'The gate enforcement is a separate change').

## 10. Owner response (unfilled)
- [ ] APPROVE
- [ ] REJECT
- Owner: ______    Date: ______    Conditions: ______

## 11. Recording instruction
Do not record any outcome until the owner explicitly adopts it. The recording is a new entry in the owner decision record written under the owner's authority; this brief and its recommendation are not an entry and not a decision.
