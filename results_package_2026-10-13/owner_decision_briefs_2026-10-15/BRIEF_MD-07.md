# MD-07: Timeout meaning (C-16)

**Status: PENDING OWNER DECISION: READY FOR OWNER.** Prepared 2026-10-15T03:30:47Z. The owner makes this decision; nothing here is adopted. Dependencies: none beyond those named below.

## 1. Why a decision is needed
The frozen text says '180 s' without saying which; the meaning (per operation or total deadline) must be fixed before the FZ hash.

## 2-3. Authoritative sources and verbatim quotations
Quotations are exact text from the files and lines named (excerpts are marked). Interpretation is confined to sections 5-8.

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 39-39**

> | 8 | **MD-07:** is any register value changed (for example `timeout_s`)? | NO: meaning only | a changed value changes the register hash | value change only | | | | |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 54-54**

> | 8 | MD-07 | PENDING | per-operation meaning (no code) or a total deadline | register value only if changed | none | P6 only for a total deadline | P6 tests | - | (x) | x | - |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 153-155**

> ## MD-07 Timeout meaning (C-16)
> - **Recommendation:** 180 s is a per-socket-operation timeout as built (stated in every run summary; calls above 180 s are flagged after the fact); no total deadline now. Record entry only; no code. **Consequence if rejected/amended:** a total deadline changes which calls are SF1, is a protocol-level change if outcomes change, needs P6 and must be decided before the FZ hash. **Alternative rejected:** total wall-clock deadline. **Affects:** FZ-v1 row 17; `GeminiProvider`. **Prerequisite:** before the FZ hash.
> - `[ ] APPROVE  [ ] REJECT  [ ] AMEND: ______  | Owner: ______  | Date: ______`

**`results_package_2026-10-13/MASTER_PROPOSED_DECISION_RECORD.md` lines 166-170**

> ### MD-07 Timeout meaning (C-16)
> - **Class:** record entry (per-operation) / PROTOCOL if a total deadline changes which calls fail.
> - **Proposed text:** "The frozen 180 s is ______ (a per-socket-operation timeout; calls whose recorded latency exceeds 180 s are flagged / a total wall-clock deadline of 180 s per request, a hit being SF1 and never retried)." Decide before the FZ hash.
>
> - **Owner decision: PENDING | Advisor decision: PENDING | Date: PENDING | Option chosen: PENDING**

**`results_package_2026-10-13/deferred_patches/DEFERRED_PATCHES.md` lines 52-54**

> ## P6 Timeout (MD-07; C-16)
> - **Source.** FZ-v1 row 17 (`timeout_s` 180, meaning undefined); `GeminiProvider` (`urlopen(timeout=...)`, per socket operation); `TIMEOUT_SEMANTICS` in every run summary; tests `test_timeout_is_not_presented_as_a_total_deadline`, `test_slow_call_is_flagged_after_the_fact` (existing).
> - **Status.** The per-operation behaviour is documented, summarized and tested; calls above 180 s are flagged after the fact. A total wall-clock deadline would change which calls are SF1 (a behaviour change of a frozen setting) and is held. If adopted: worker-thread or `socket`-level deadline, hit = SF1, never retried, summary text changed, mock test with a provider that blocks past the deadline, frozen value 180 unchanged, FZ decision first.


## 4. Original options (labels and order as in the sources)
Options as quoted (per-operation meaning with no code / a total deadline).

## 5. Consequences
- Source-defined: 'register value only if changed'; P6 only for a total deadline (OAP closure matrix).
- Reasoned: a total deadline changes which calls are SF1 (conflict index C-16 -> C-17 link).

## 6. Recommendation: NOT ADOPTED
Source recommendation (NOT ADOPTED): see the Direction line in the quoted OAP/MPDR text.

## 7. Record cross-check
Decision record cross-check (read-only search of `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` for `timeout`): lines [224, 783, 839, 842]. Hits are mentions only. Entries 12.40-12.45 were read for this check: they either do not mention this item or state it as not decided (12.43, 12.44).

## 8. Dependencies
See the dependencies named in the header of this brief; no further source-backed content.

## 9. Information still missing
- Whether the owner wants any register value changed; none specified.

## 10. Owner response (unfilled)
- [ ] meaning only (per-operation), no value change
- [ ] total deadline (value ______)
- [ ] other: ______
- Owner: ______    Date: ______    Conditions: ______

## 11. Recording instruction
Do not record any outcome until the owner explicitly adopts it. The recording is a new entry in the owner decision record written under the owner's authority; this brief and its recommendation are not an entry and not a decision.
