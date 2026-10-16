# P12: Box P12: read-only O4 usage reader

**Status: PENDING OWNER DECISION: BLOCKED — SOURCE TEXT REQUIRED (partial: see section 9).** Prepared 2026-10-15T03:30:47Z. The owner makes this decision; nothing here is adopted. Dependencies: MD-02 Q8; completed pilot.

## 1. Why a decision is needed
The main-run token basis needs either a provider count (O2) or the O4 estimate from pilot `usageMetadata`; P12 is the read-only script for O4.

## 2-3. Authoritative sources and verbatim quotations
Quotations are exact text from the files and lines named (excerpts are marked). Interpretation is confined to sections 5-8.

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 24-24**

> | P12 O4 usage reader (read-only; prints numbers only) | box **P12** + MD-02 Q8 | any provider token count (O2) |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 66-66**

> | 20 | Box P12 | PENDING | the O4 read-only script | new script | completed pilot, MD-02 Q8 | P12 | mock tests | - | - | - | before the main-run authorization |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 108-108**

> | P12 | the O4 script | the main-run token basis must be O2 or an owner entry accepting the assumption |

**`results_package_2026-10-13/C31_C32_OWNER_DECISION_BRIEF.md` lines 175-181**

> ## 17. Main-run token measurement: the O4-after-pilot path (execution batch 2026-10-13)
> - **Status of the numbers.** `input_tokens_per_call_assumed` = 1,016 is an ASSUMPTION (one token per character, Step 7). No input token has been measured. This stays labelled an assumption in the authorization, the cost figures and every report until a measurement exists.
> - **Method O4.** For each pilot call i: ratio r_i = `usageMetadata.promptTokenCount_i` / characters_i (characters from the build's prompt table); bound B = ceil(max_i r_i x 1,016). Compare B with the assumption written in the authorization. The pilot has 18 calls, 6 of them at the maximum length of 1,016 characters, so the longest prompts are observed directly and the ratio bound covers templates of other density.
> - **Prerequisites.** (a) the pilot round has run and every call has a usable `promptTokenCount` (L4 confirms the field exists; calls without it make the result INCONCLUSIVE); (b) a small read-only script that prints only numbers (ids, characters, tokens, B) and never response text, approved by the owner (13.6.1: no human opens pilot responses; usage metadata is counts only) — not written; (c) the result recorded as a dated note and an official entry; (d) provider overhead tokens included in `promptTokenCount` are UNKNOWN until L4.
> - **Decision rule.** B <= assumption: the assumption is confirmed as an upper bound for the pilot's templates; the main-run authorization may keep 1,016. B > assumption: recompute the hard-cap cost with B (the US$100 limit is reached only near 63,381 tokens per call) and ask the owner. Limits of O4: it measures pilot prompts only; main prompts not represented by the pilot's template types would rest on the ratio bound; if that is not acceptable, O2 (a provider token count of the 1,248 prompts) needs its own written authorization and spending basis.
> - **Not allowed meanwhile:** any provider token count; presenting characters as tokens.
>


## 4. Original options (labels and order as in the sources)
APPROVE / REJECT; depends on MD-02 Q8.

## 5. Consequences
- Source-defined: if rejected 'the main-run token basis must be O2 or an owner entry accepting the assumption'.
- Reasoned: needs a completed pilot.

## 6. Recommendation: NOT ADOPTED
None.

## 7. Record cross-check
Decision record cross-check: no mention of `P12`, `O4` in the record.

## 8. Dependencies
See the dependencies named in the header of this brief; no further source-backed content.

## 9. Information still missing
- The script is not written ('new script').

## 10. Owner response (unfilled)
- [ ] APPROVE
- [ ] REJECT
- Owner: ______    Date: ______    Conditions: ______

## 11. Recording instruction
Do not record any outcome until the owner explicitly adopts it. The recording is a new entry in the owner decision record written under the owner's authority; this brief and its recommendation are not an entry and not a decision.
