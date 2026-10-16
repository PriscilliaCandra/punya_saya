# Q9: Box Q9: enforce assumed tokens versus prompt length (P3b)

**Status: PENDING OWNER DECISION: BLOCKED — SOURCE TEXT REQUIRED (partial: see section 9).** Prepared 2026-10-15T03:30:47Z. The owner makes this decision; nothing here is adopted. Dependencies: MD-02.

## 1. Why a decision is needed
The Step 7 assumption 'a token covers at least one character' is not enforced by the gate.

## 2-3. Authoritative sources and verbatim quotations
Quotations are exact text from the files and lines named (excerpts are marked). Interpretation is confined to sections 5-8.

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 19-19**

> | P3b assumed-token gate | box **Q9** (C32-2 and the form of a measured basis) | MD-02 as written (C32-1 needs no code) |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 61-61**

> | 15 | Box Q9 | PENDING | enforce assumed tokens vs characters, define a measured basis | `s10_runner.py`, `test_input_limit.py` | MD-02 | P3b | `test_input_limit` | - | - | - | (x) |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 104-104**

> | Q9 | P3b | the assumed-token value stays unenforced |

**`results_package_2026-10-13/deferred_patches/DEFERRED_PATCHES.md` lines 35-40**

> ## P3b Assumed-tokens versus prompt-length gate (MD-02; C-01, C-23)
> - **Source.** MPR section 4 ("proposed gate check: refuse if the maximum prompt length in characters exceeds the assumed tokens, unless the owner states a measured basis"); record 12.18 row 6.
> - **Why held.** The exception ("a measured basis") has no defined field or form; a measured basis below the characters (typical 3 chars/token) is legitimate, so a hard refusal without the exception would block a correct future authorization, and the exception is the undecided token-measurement method (P-4/O2). Today the owner must write `input_tokens_per_call_assumed` >= 1,016 by hand; nothing enforces it.
> - **Design after adoption.** Gate reason when `input_tokens_per_call_assumed` < longest planned prompt in characters and the authorization has no `input_token_basis` object `{"method": ..., "document": ..., "measured_max_tokens": int}` accepted by the record; cost gate unchanged; limit and cost remain separate (MD-02 item 8).
> - **Acceptance:** assumed 1,015 with no basis refused; 1,016 accepted; basis present and valid accepted; hard-cap cost unchanged; `test_input_limit.py` still passes.
> - **Main-run token method (MD-02 item 7):** NOT chosen. Options O2 (provider token count of all 1,248 prompts, an external call needing separate authorization, D) and O4 (maximum `promptTokenCount` of pilot calls checked against the 1,248 prompt lengths). No token count by a live call is allowed in this batch.

**`results_package_2026-10-13/C31_C32_OWNER_DECISION_BRIEF.md` lines 107-119**

> ## 10. C-32: assumed input tokens versus prompt length (OD-10 basis)
> [TEXT] record 12.11 OD-10: `I_max` is to be measured on the actual prompt; 12.18 row 6: the owner accepted the 1016-character bound as the Step 7 bound ("a token covers at least one character"), "an assumption, not a measurement"; `MASTER_PREPILOT_RESOLUTION.md` section 4 proposed a gate refusing an assumption below the longest prompt in characters unless a measured basis is stated. [CODE] the gate (`check_gates`) uses `input_tokens_per_call_assumed` only in the cost formula and (working decision MD-02) checks `max_input_characters` against the prompt lengths; it does not compare the two numbers. Prompt lengths: pilot 96 entries and main 1,248 entries, maximum 1,016 characters (`prompt_table.json`).
>
> Cost sensitivity (the real `hard_cap_cost_usd`, output cap 8,192 tokens): 18 calls: US$0.3686 at 1 assumed token, US$0.3741 at 1,016, US$0.3851 at 3,048; 2,496 slots: US$51.12 at 1, US$51.88 at 1,016, US$53.40 at 3,048; the US$100 limit is reached at about 63,381 tokens per call. An understated input assumption changes the cost bound by about 1.5 % at most (1 versus 1,016 tokens); the output term dominates. [READING] The risk of C-32 is the integrity of the stated basis (OD-10 asks for a measurement), not the budget.
>
> Options: **C32-1** keep as is (the owner writes a value >= 1,016 by hand; not enforced); **C32-2** enforce `input_tokens_per_call_assumed` >= longest planned prompt in characters, with an explicit `input_token_basis` object accepted for a measured basis (patch P3b; the form of the basis must be decided first); **C32-3** require a token measurement before any paid call (an external call needing separate written authorization; not allowed in this batch). Recommendation [READING]: C32-1 is acceptable for the 18-call pilot if the authorization states the 1,016 assumption and the character limit in writing; before the main run a measurement method must be chosen (O2: provider count of the 1,248 prompts; or O4: maximum `promptTokenCount` of the pilot calls checked against all prompt lengths). The character limit stays an operational control: not a token measurement, not a cost guarantee, separate from the US$100 cap.
>
> - **Q7.** Accept C32-1 for the pilot?
> - **Q8.** Which measurement method (O2/O4) before the main run, and who authorizes an external count?
> - **Q9.** If P3b is wanted, what exact fields define a "measured basis"?
>
> Decision fields: **PENDING**.
>


## 4. Original options (labels and order as in the sources)
APPROVE / REJECT; C32-1 / C32-2 in C31 section 10.

## 5. Consequences
- Source-defined: if rejected 'the assumed-token value stays unenforced'.
- Reasoned: a gate rule beyond the directed scope (MPDR MD-02).

## 6. Recommendation: NOT ADOPTED
None offered.

## 7. Record cross-check
Decision record cross-check (read-only search of `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` for `Q9`, `C32`): lines [650]. Hits are mentions only. Entries 12.40-12.45 were read for this check: they either do not mention this item or state it as not decided (12.43, 12.44).

## 8. Dependencies
See the dependencies named in the header of this brief; no further source-backed content.

## 9. Information still missing
- 'The form of a measured basis is undefined' (MPDR MD-02): BLOCKED — SOURCE TEXT REQUIRED for the gate's measured-basis form.

## 10. Owner response (unfilled)
- [ ] APPROVE (C32-2) with measured-basis form ______
- [ ] REJECT
- Owner: ______    Date: ______    Conditions: ______

## 11. Recording instruction
Do not record any outcome until the owner explicitly adopts it. The recording is a new entry in the owner decision record written under the owner's authority; this brief and its recommendation are not an entry and not a decision.
