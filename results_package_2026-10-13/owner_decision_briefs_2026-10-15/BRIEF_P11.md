# P11: Box P11: one provider connection test

**Status: PENDING OWNER DECISION: BLOCKED — SOURCE TEXT REQUIRED (partial: see section 9).** Prepared 2026-10-15T03:30:47Z. The owner makes this decision; nothing here is adopted. Dependencies: none beyond those named below.

## 1. Why a decision is needed
Without a connection test L1-L5 stay UNKNOWN; the first live contact is the pilot itself.

## 2-3. Authoritative sources and verbatim quotations
Quotations are exact text from the files and lines named (excerpts are marked). Interpretation is confined to sections 5-8.

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 23-23**

> | P11 connection-test tool and one provider test | box **P11** + a separate written authorization file (ceiling, prompt hash, handling) | spending, token counts, a pilot |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 65-65**

> | 19 | Box P11 | PENDING | one provider connection test (separate written authorization file) | new tool | none | P11 | mock tests first | - | - | - | optional |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 107-107**

> | P11 | the connection test | L1-L5 stay UNKNOWN; the first live contact is the pilot, protected only by MD-06 if adopted |

**`results_package_2026-10-13/deferred_patches/DEFERRED_PATCHES.md` lines 90-91**

> ## P11 (proposed, not in the original plan): connection-test tool for L1-L5
> Not written. A single-call tool is needed because `s10_runner` accepts only `pilot_round_1`, `pilot_round_2` and `main`. Requirements and acceptance tests are in `PROVIDER_VERIFICATION_MATRIX.md` section 0. Status: DEFERRED / BLOCKED BY PROVIDER VERIFICATION authorization; condition to continue: owner approves the connection test in writing and the tool's mock-only acceptance tests are written first. Owner: owner (authorization), assistant (tool, after approval).

**`results_package_2026-10-13/PROVIDER_VERIFICATION_MATRIX.md` lines 5-11**

> ## 0. Common rules for any live connection test (all of L1-L5; L6 has its own rules)
> - **Authorization (written, by the owner, before any call).** A file with `authorized_by` = `owner`, a scope that names the test (`connection_test`), `max_calls` (1 recommended), `cost_ceiling_usd`, the prompt it may send (by SHA-256) and how the response is handled. NOTE: `s10_runner` accepts only `pilot_round_1`, `pilot_round_2` and `main`; **no tool exists for a connection test**. A new small tool would be needed (proposed patch P11, not part of P1-P10, NOT written): one call, neutral prompt that is not a registry prompt and not experiment content, key from the environment variable only, no pilot ledger and no pilot-round consumption, output limited to the metadata fields below. Before first use it needs mock-only acceptance tests (key never printed or stored; refuses without authorization; exactly one call; response text discarded; no file overwritten).
> - **Cost bound.** One call at the register settings is bounded by the hard-cap formula: about US$0.021 per call (US$0.3741 / 18 at 1,016 assumed input tokens and the 8,192-token output cap). The owner sets the ceiling; the true cost is expected to be far lower but is not known.
> - **What may be stored.** HTTP status; the set of top-level and `usageMetadata` key names; `modelVersion` string; `finishReason` string; `promptFeedback` key names and `blockReason` string if present; numbers in `usageMetadata`; latency; the SHA-256 and character length of the response text. **Not stored:** the response text, the key, request headers, the prompt other than its hash.
> - **Protection.** The key is read from `GEMINI_API_KEY` only and never printed; the prompt is neutral (no registry content, no personal data); the output folder is new and not overwritten; the response text is not read by a human or used for any protocol decision (13.6.1 activity B, by analogy).
> - **Result states.** PASS (the question is answered with the stated evidence), FAIL (the evidence contradicts the adapter's assumption), INCONCLUSIVE (the test cannot answer it; the safe-stop policy MD-06 is the mitigation).
>


## 4. Original options (labels and order as in the sources)
APPROVE / REJECT plus a separate written authorization file.

## 5. Consequences
- Source-defined: if rejected 'L1-L5 stay UNKNOWN ... protected only by MD-06 if adopted'.
- Reasoned: spending and token counts are explicitly not authorized by P11 alone.

## 6. Recommendation: NOT ADOPTED
None.

## 7. Record cross-check
Decision record cross-check (read-only search of `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` for `P11`, `connection test`): lines [879]. Hits are mentions only. Entries 12.40-12.45 were read for this check: they either do not mention this item or state it as not decided (12.43, 12.44).

## 8. Dependencies
See the dependencies named in the header of this brief; no further source-backed content.

## 9. Information still missing
- The tool is not written; the separate authorization file has no template in the sources examined (BLOCKED — SOURCE TEXT REQUIRED for its content: 'ceiling, prompt hash, handling').

## 10. Owner response (unfilled)
- [ ] APPROVE
- [ ] REJECT
- Owner: ______    Date: ______    Conditions: ______

## 11. Recording instruction
Do not record any outcome until the owner explicitly adopts it. The recording is a new entry in the owner decision record written under the owner's authority; this brief and its recommendation are not an entry and not a decision.
