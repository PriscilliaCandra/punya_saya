# MD-02: Input-size basis, token measurement and cost (with Q7 and Q8)

**Status: PENDING OWNER DECISION: READY FOR OWNER.** Prepared 2026-10-15T03:30:47Z. The owner makes this decision; nothing here is adopted. Dependencies: none beyond those named below.

## 1. Why a decision is needed
The 1,016-character preflight and the token assumption are working decisions; the owner confirms them in the record and in the pilot authorization.

## 2-3. Authoritative sources and verbatim quotations
Quotations are exact text from the files and lines named (excerpts are marked). Interpretation is confined to sections 5-8.

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 56-56**

> | 10 | MD-02 (+ Q7, Q8) | WORKING DECISION | the 1,016-character preflight, C32-1 for the pilot, O4 first for the main run | template, `test_input_limit.py` | none | none | already run | - | - | - | x |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 98-98**

> | MD-02 | the preflight limit and the authorization values | the template value and tests change to your limit; P3b only if Q9 |

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 129-133**

> ## MD-02 Input-size basis, token measurement and cost (C-01, C-23, C-32) — WORKING DECISION, formal entry needed
> - **Decision/recommendation:** preflight maximum **1,016 characters** per prompt (verified maximum of the build: 96 pilot / 1,248 main prompts; pre-filled in the authorization template, you confirm it when you sign the authorization); refuse an empty or longer prompt before any provider call; never truncate; characters are not tokens; `input_tokens_per_call_assumed` = 1,016 is the Step 7 ASSUMPTION, not a measurement; pilot: accept as is (C32-1); main run: measure by O4 after the pilot (brief section 17), O2 only with separate written authorization; US$100 ceiling unchanged, stop if it cannot be assured. Owner.
> - **Consequences:** the hard-cap bound is about US$0.37 for 18 calls and US$51.88 for 2,496 slots at the 1,016 assumption; the input term is about 1.5 % of it. **Alternatives rejected:** inheriting the Step 7 bound silently; a gate on assumed tokens vs characters now (P3b: the form of a "measured basis" is undefined); a provider token count now (spending).
> - **Affects:** `s10_runner.py`, `templates/owner_authorization_TEMPLATE.json`, `test_input_limit.py` (10); record 12.11 OD-10, 12.18 row 6. **Prerequisite:** none for the pilot. **Unresolved:** the main-run measurement itself (needs pilot data). Separate boxes: **Q9** (only if you want the assumed-token gate P3b) and **P12** (the read-only O4 script).
> - `[ ] APPROVE  [ ] REJECT  [ ] AMEND: ______  | Owner: ______  | Date: ______`   Q7 accept C32-1 for the pilot `[ ]`  Q8 O4 first for the main run `[ ]`

**`results_package_2026-10-13/MASTER_PROPOSED_DECISION_RECORD.md` lines 116-127**

> ### MD-02 OD-10 scope of the input-size basis (C-01, C-23, C-29)
> - **Class:** record entry; measurement option = external call (separate authorization).
> - **Rule quoted:** record 12.11 OD-10 (line 402) "At Step 7 `I_max` is measured on the actual prompt ... If ... the limit cannot be adequately assured, stop before any paid API call"; 12.18 row 6 "accepts the character bound as the Step 7 input-size bound ... replaces, for Step 7 ... not a measurement".
> - **STATUS OF THIS TEXT (read first):** WORKING TECHNICAL DECISION directed by the project owner on 2026-10-13 for P1/P3 preparation; NOT an institutional approval by the advisor or owner; approval block stays PENDING. It does not amend 12.11 OD-10 or 12.18 row 6.
> - **Proposed text (working decision, items 1-8 as directed):** (1) "For a pilot round the input-size control is an explicit character limit per prompt, written by the owner in the authorization as `max_input_characters` (a positive integer; no default and no inherited value). (2) The Step 7 bound of 12.18 row 6 is not assumed to apply to paid calls; it applies only if the owner writes it into the authorization. (3) Preflight, before any provider call is made, refuses a missing/invalid limit, an empty prompt, and any prompt longer than the limit; nothing is truncated, and a refused run consumes no round and writes no call artefact. (4) Preflight records, without printing prompt text, the limit, the number of prompts checked and the maximum observed length (`input_size_check` in the run summary). (5) The character limit is an operational control, NOT a token measurement (stated in the summary). (6) Before the main run a documented token measurement or check method that fits the protocol and the provider must be set (open: MD-02 main-run basis, separate authorization if it needs an external call). (7) The cost ceiling (US$100) is separate from the input limit; a character limit alone does not guarantee a maximum cost; `input_tokens_per_call_assumed` and the hard-cap cost gate are unchanged."
> - **Source check:** record 12.11 OD-10 (line 402): `I_max` to be measured on the actual prompt, stop before any paid call if the limit cannot be adequately assured; 12.18 row 6 (line 511): the owner accepted a character bound of 1016 as the Step 7 bound, "an assumption, not a measurement; the tokenizer was not queried"; 12.18 follow-up row 8 (line 604): no measured `I_max` exists, P-4 describes the method, requires an external call. Value check (read-only, 2026-10-13): `step8_output/step8_build_7a6bbe465c66/pilot/prompt_table.json` has 96 entries and `.../main/prompt_table.json` 1,248 entries, both with maximum `chars` = 1,016, which agrees with 12.18 row 6. 1,016 is therefore a VERIFIABLE candidate value, but the code does not use it as a default: the owner must write a value >= the longest planned prompt (for the pilot, the longest prompt among the 18 planned calls; for the main run 1,016 as of this build) in the authorization file.
> - **Where it lives:** authorization field `max_input_characters` (`templates/owner_authorization_TEMPLATE.json`, value 0 = unset, rejected); gate `s10_runner.check_gates`; preflight `s10_runner.check_input_sizes` (inside the live-run path, before the provider is built); the prompt text is read from the published build and sent unchanged.
> - **Impact:** none on the protocol; cost stays at the hard cap (US$0.37 for 18 calls, US$51.88 for 2,496 slots at 1,016 assumed tokens) and is governed only by the cost gate.
> - **Still unresolved / not implemented (not covered by this working decision):** (a) the main-run token measurement method (item 6); (b) a gate refusal of `input_tokens_per_call_assumed` below the longest prompt in characters (the earlier draft acceptance and plan P3 text): the Step 7 assumption "a token covers at least one character" is not enforced by the gate, because it would add a gate rule beyond the directed scope; the owner must state a value >= 1,016 by hand. Both stay open for ratification.
> - **Acceptance (met by `test_input_limit.py`, 10 tests, mock provider, no live call):** missing/zero/negative/boolean/non-integer limit closes the gate; a prompt exactly at the limit is accepted and one character above is refused; empty prompt refused; an over-limit run is refused before any provider call (mock provider call count 0), no call artefact and no consumed round; prompts are sent unchanged (no truncation); limit independent of the cost assumption; the template (value 0) is rejected.
>
> - **Owner decision: PENDING | Advisor decision: PENDING | Date: PENDING | Option chosen: PENDING**

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
Options: APPROVE / REJECT / AMEND; Q7 'accept C32-1 for the pilot'; Q8 'O4 first for the main run'; C32-1 / C32-2 in C31 section 10 (quoted).

## 5. Consequences
- Source-defined: hard-cap bound about US$0.37 for 18 calls and US$51.88 for 2,496 slots at 1,016 (OAP, MPDR).
- Reasoned: the gate does not enforce `input_tokens_per_call_assumed` >= 1,016 (MPDR 'Still unresolved'); the owner must state a value by hand.

## 6. Recommendation: NOT ADOPTED
Source recommendation (NOT ADOPTED): OAP: 1,016-character preflight, C32-1 for the pilot, O4 first for the main run.

## 7. Record cross-check
Decision record cross-check (read-only search of `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` for `MD-02`, `OD-10`, `1016`): lines [398, 402, 500, 511, 759, 771, 877, 897] .... Hits are mentions only. Entries 12.40-12.45 were read for this check: they either do not mention this item or state it as not decided (12.43, 12.44).

## 8. Dependencies
See the dependencies named in the header of this brief; no further source-backed content.

## 9. Information still missing
- The main-run measurement itself (needs pilot data).

## 10. Owner response (unfilled)
- [ ] APPROVE
- [ ] REJECT
- [ ] AMEND: ______
- [ ] Q7 accept C32-1 for the pilot
- [ ] Q8 O4 first for the main run
- Owner: ______    Date: ______    Conditions: ______

## 11. Recording instruction
Do not record any outcome until the owner explicitly adopts it. The recording is a new entry in the owner decision record written under the owner's authority; this brief and its recommendation are not an entry and not a decision.
