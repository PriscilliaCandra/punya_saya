# Q5: Box Q5: adapter field and the SF4/SF2 rule for the rare shape

**Status: PENDING OWNER DECISION: READY FOR OWNER.** Prepared 2026-10-15T03:30:47Z. The owner makes this decision; nothing here is adopted. Dependencies: MD-01.

## 1. Why a decision is needed
The rare shape 'a candidate with empty text and no finishReason' is currently inferred, not read from an explicit adapter field.

## 2-3. Authoritative sources and verbatim quotations
Quotations are exact text from the files and lines named (excerpts are marked). Interpretation is confined to sections 5-8.

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 18-18**

> | Q5 adapter field + SF4/SF2 rule for the rare shape | box **Q5** | MD-01 (it does not cover Q5) |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 60-60**

> | 14 | Box Q5 | PENDING | adapter field `candidates_returned` and the SF4/SF2 rule for the rare shape | `s10_runner.py`, `s10_scoring.py`, `test_sf2_detection.py` d6 | MD-01 | Q5 | adapter/scoring tests, `--quick` | - | - | (x) (L-C) | x |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 103-103**

> | Q5 | the adapter field | the present inference stays; the rare shape stays SF4 (soft), documented as a limitation |

**`results_package_2026-10-13/C31_C32_OWNER_DECISION_BRIEF.md` lines 168-173**

> ## 16. Q5 contract: "no candidate" versus "a candidate with empty text and no finishReason" (execution batch 2026-10-13; NOT implemented, needs approval)
> - **The distinction needed.** Spec 812 defines SF4 as "safety/blocked finish reason or no candidate returned". A response that DID return a candidate whose text is empty is not "no candidate"; under option B it is an empty response (SF2, hard) unless a block signal applies. Today the record cannot tell them apart: the adapter does not store the number of candidates, and `sf_flags` infers "no candidate" from HTTP 200 + no error + `finish_reason` absent + empty text. Result today: a candidate with empty text and no `finishReason` is SF4 (soft), the same candidate with `finishReason` STOP is SF2 (hard) (tested: `test_sf2_detection.py` d6).
> - **Minimum adapter contract (proposal).** `GeminiProvider.generate` returns an additional key `candidates_returned`: the integer `len(data.get("candidates") or [])` when a JSON object was decoded, `None` when no payload was decoded (HTTP error, timeout, transport exception, non-JSON body). `run()` copies it into the stored record. No other field changes. Legacy records without the key (Stage 1/2 data, existing mocks) keep the current inference.
> - **Scoring rule (proposal).** SF4 "no candidate" iff 2xx, no error marker, `candidates_returned == 0` (or, for legacy records, the current inference). A record with `candidates_returned >= 1`, empty text and no block signal is SF2. Block signals (finish-reason block names, `promptFeedback.blockReason`) are unchanged. **Behaviour change:** only the rare shape "candidate present, no text, no finishReason" moves from SF4 (soft) to SF2 (hard). It changes which calls fail a pilot, so it needs your approval (class C); it is not a pure implementation fix.
> - **Tests required (written from the approved rule before the code):** adapter payload shapes with a patched `urlopen`: (1) no `candidates` key; (2) `candidates: []`; (3) one candidate without `content`; (4) `content` without `parts`; (5) `parts` with an empty text; each with and without `finishReason` and with and without `promptFeedback.blockReason` -> expected `candidates_returned` and flags; legacy record without the key -> old inference; the stored raw record round-trips through `s10_integrity` (raw equals calls.jsonl); `pilot_counts` and the decision vector unchanged for single-flag rows; no new outcome label.
> - **UNKNOWN (do not guess):** which of shapes (1)-(5) the live API actually produces, whether a block yields an absent or an empty `candidates`, whether a candidate can lack `finishReason`. These are provider facts for L3 (`PROVIDER_VERIFICATION_MATRIX.md`); they are read from the provider documentation by the researcher, not provoked by test calls. Until approved and implemented, Q5 stays open and the pilot accepts the present inference.


## 4. Original options (labels and order as in the sources)
APPROVE / REJECT (OAP box).

## 5. Consequences
- Source-defined: if rejected 'the present inference stays; the rare shape stays SF4 (soft), documented as a limitation'.
- Reasoned: touches `s10_runner.py`, `s10_scoring.py` (listed).

## 6. Recommendation: NOT ADOPTED
None offered.

## 7. Record cross-check
Decision record cross-check: no mention of `Q5` in the record.

## 8. Dependencies
See the dependencies named in the header of this brief; no further source-backed content.

## 9. Information still missing
- None found.

## 10. Owner response (unfilled)
- [ ] APPROVE
- [ ] REJECT
- Owner: ______    Date: ______    Conditions: ______

## 11. Recording instruction
Do not record any outcome until the owner explicitly adopts it. The recording is a new entry in the owner decision record written under the owner's authority; this brief and its recommendation are not an entry and not a decision.
