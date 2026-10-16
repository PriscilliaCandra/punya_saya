# Provider verification matrix L1-L6 (PREPARED — NOTHING BELOW HAS BEEN EXECUTED; no network call, no token count, no credit use)

Prepared 2026-10-13 from `MASTER_PILOT_READINESS_CHECKLIST.md` section 4, `PROVIDER_STATIC_AUDIT.md`, `PROVIDER_RESPONSE_VALIDATION_REPORT.md`, `MASTER_PREPILOT_RESOLUTION.md` (Q-P1..Q-P4, sections 4-5), `C31_C32_OWNER_DECISION_BRIEF.md` and the adapter `s10_runner.GeminiProvider`. Every statement about the provider's API below is **UNKNOWN** unless a source in this repository records it; the field names in the adapter were written from memory of the public REST shape and have never been checked. This matrix is usable only after the owner has given the written authorization named in each row. It does not authorize anything.

## 0. Common rules for any live connection test (all of L1-L5; L6 has its own rules)
- **Authorization (written, by the owner, before any call).** A file with `authorized_by` = `owner`, a scope that names the test (`connection_test`), `max_calls` (1 recommended), `cost_ceiling_usd`, the prompt it may send (by SHA-256) and how the response is handled. NOTE: `s10_runner` accepts only `pilot_round_1`, `pilot_round_2` and `main`; **no tool exists for a connection test**. A new small tool would be needed (proposed patch P11, not part of P1-P10, NOT written): one call, neutral prompt that is not a registry prompt and not experiment content, key from the environment variable only, no pilot ledger and no pilot-round consumption, output limited to the metadata fields below. Before first use it needs mock-only acceptance tests (key never printed or stored; refuses without authorization; exactly one call; response text discarded; no file overwritten).
- **Cost bound.** One call at the register settings is bounded by the hard-cap formula: about US$0.021 per call (US$0.3741 / 18 at 1,016 assumed input tokens and the 8,192-token output cap). The owner sets the ceiling; the true cost is expected to be far lower but is not known.
- **What may be stored.** HTTP status; the set of top-level and `usageMetadata` key names; `modelVersion` string; `finishReason` string; `promptFeedback` key names and `blockReason` string if present; numbers in `usageMetadata`; latency; the SHA-256 and character length of the response text. **Not stored:** the response text, the key, request headers, the prompt other than its hash.
- **Protection.** The key is read from `GEMINI_API_KEY` only and never printed; the prompt is neutral (no registry content, no personal data); the output folder is new and not overwritten; the response text is not read by a human or used for any protocol decision (13.6.1 activity B, by analogy).
- **Result states.** PASS (the question is answered with the stated evidence), FAIL (the evidence contradicts the adapter's assumption), INCONCLUSIVE (the test cannot answer it; the safe-stop policy MD-06 is the mitigation).

## L1 Request field names and thinking-level parameter
- **Question.** Does the endpoint accept `generationConfig.maxOutputTokens` and `generationConfig.thinkingConfig.thinkingLevel` as written by the adapter, and is the thinking level actually applied? Endpoint, header name and request body shape are UNKNOWN until checked.
- **Why needed.** A rejected field gives HTTP 400 (SF1) for every call and would consume a pilot round; an ignored field silently changes the frozen setting (thinking minimal).
- **Minimal check.** Read the provider's current documentation for the model first (human, no call); then one authorized call with the register settings.
- **Authorization.** Owner, connection-test file (section 0). **Cost.** <= about US$0.021.
- **Evidence kept.** Status code, response key names, `usageMetadata` key names.
- **PASS** HTTP 2xx and the documentation lists both fields as supported for this model. **FAIL** HTTP 4xx naming a field, or documentation says a field does not exist or has another name. **INCONCLUSIVE** HTTP 2xx but no way to tell whether the thinking level was applied (likely: usage may show thinking tokens only if reported).
- **If not verified.** Pilot risk: round consumed by systematic SF1 or a silently different setting. Mitigation available now: none beyond mock tests.

## L2 Returned model ID form
- **Question.** What exact string does the provider return for the requested ID `gemini-3.5-flash-lite` (alias, version suffix, other)?
- **Why needed.** FZ-v1 row 17 requires the returned ID to be recorded; today a difference is recorded but stops nothing (MPR Q-P1, MD-06 clause 1 proposes a safe stop).
- **Minimal check.** The same single call as L1; compare `modelVersion` with the requested ID.
- **Authorization / cost.** As L1 (no extra call).
- **Evidence kept.** The returned string.
- **PASS** exactly equal. **INCONCLUSIVE** an alias or suffix (the owner must write in an official entry which forms count as the same model). **FAIL** a different model.
- **If not verified.** An unexpected string stops the run only if MD-06 clause 1 is adopted; otherwise it is only reported.

## L3 Finish-reason vocabulary and block markers
- **Question.** Which `finishReason` names exist, which of them mean a block, and how does a prompt-level block appear (`promptFeedback.blockReason`, absent candidates)? The adapter's list of eight block names (SAFETY, BLOCKLIST, PROHIBITED_CONTENT, SPII, IMAGE_SAFETY, RECITATION, OTHER, LANGUAGE) comes from memory and is UNKNOWN as to correctness; RECITATION, OTHER and LANGUAGE are not shown to mean "blocked".
- **Why needed.** SF3/SF4 depend on these names (spec 811-812); MPR Q-P2/Q-P3.
- **Minimal check.** Primary: the researcher reads the provider's current documentation of finish reasons and block fields and records the names with the page and date (no call). A single connection test shows only the reason of that one benign call (expected `STOP`); **do not provoke blocks or truncation on purpose**.
- **Authorization / cost.** Documentation reading: none. The one-call test: as L1.
- **Evidence kept.** A dated note with the documented names; the observed `finishReason` of the test call.
- **PASS** each name used by the code has a documented meaning. **INCONCLUSIVE** (expected after one call) names unobserved but documented, or not documented. **FAIL** a name in the code is documented to mean something else.
- **If not verified.** Unlisted reasons are counted and reported (current code) or stop the run (MD-06 clause 2, if adopted). Block-name changes are decided by the owner (C-14), not by the assistant.

## L4 Usage fields and token accounting
- **Question.** Does `usageMetadata` carry `promptTokenCount`, `candidatesTokenCount`, `totalTokenCount` and `thoughtsTokenCount`, and how is the total composed (is thinking included in the candidates count)?
- **Why needed.** Observed cost (`s10_integrity.output_tokens`) assumes output = total - prompt when both exist; thinking tokens are billed as output (FZ-v1 model verification, OD-10). The 70 recorded Stage 1/2 calls have no `thoughtsTokenCount`.
- **Minimal check.** The same single call; compare key names and arithmetic; read the documentation for the billed composition.
- **Authorization / cost.** As L1.
- **Evidence kept.** The key names and the four numbers of the call.
- **PASS** the arithmetic and the documentation agree with `output_tokens`. **INCONCLUSIVE** thinking tokens not reported at the minimal level. **FAIL** the total contradicts the assumption (a code change to the accounting would be needed, with its own tests).
- **If not verified.** The observed cost may be a lower bound (the tool already flags incomplete usage); the hard-cap bound is unaffected.

## L5 Timeout behaviour
- **Question.** Is the frozen 180 s a per-socket-operation or a total deadline (MD-07 / C-16), and how does the endpoint behave near the limit?
- **Why needed.** The meaning decides which calls are SF1 and whether a slow trickling response is a failure.
- **Minimal check.** Not answerable by one call. The semantics is an owner decision; behaviour is documented in the run summary (`timeout_semantics`) and calls above 180 s are flagged after the fact (local tests exist: `test_timeout_is_not_presented_as_a_total_deadline`, `test_slow_call_is_flagged_after_the_fact`). The latency of the L1 call is recorded as an observation only.
- **Authorization / cost.** None additional.
- **PASS** the owner records the meaning in an official entry (MD-07). **INCONCLUSIVE** any live observation alone. **FAIL** n/a.
- **If not verified.** The present per-operation behaviour stays and is reported as such.

## L6 Token count of the prompts (1,248 main + 96 pilot entries)
- **Question.** What is the true number of input tokens of every planned prompt (maximum 1,016 characters), versus the Step 7 assumption "a token covers at least one character"?
- **Why needed.** OD-10 asks for `I_max` measured on the actual prompt (record 12.11); 12.18 row 6 accepted an assumption; P-4 describes a measurement (C-23, C-32). The cost bound is insensitive to the input term (about 1.5 % between 1 and 1,016 tokens), so this is about integrity of the stated basis, not budget.
- **Methods (owner chooses; none authorized).** **O2** use the provider's documented token-counting facility, if one exists for this model (UNKNOWN), on all 1,344 prompt files: an external call that needs its own written authorization, a stated cost basis (cost of a count request is UNKNOWN) and the same protection rules as above (prompt text leaves the machine, so the prompts are experiment content; the owner must accept that exposure). **O4** after a pilot, compare the maximum `promptTokenCount` of the pilot calls with the lengths of all 1,248 main prompts (no extra call; bound is valid only if the pilot prompts are representative of the longest ones, which the 18-call pilot may not be: UNKNOWN until checked against `prompt_table.json`).
- **Evidence kept.** A table of prompt id (opaque hash), characters, tokens; the method and date.
- **PASS** maximum tokens per call <= the assumption written in the authorization. **FAIL** above it: the authorization and cost bound are recomputed (the 100 US$ limit is reached only at about 63,381 tokens per call). **INCONCLUSIVE** O4 with unrepresentative pilot prompts.
- **If not verified before the main run.** The main run lacks the measurement that OD-10 asks for; MD-02 item 7 requires a documented method before it.

## Order and gating
L1-L5 can share one authorized connection test plus documentation reading; L6 is separate. Nothing here is needed to start the human tasks. The pilot gate (`check_gates`) does not read any L result; MD-06 safe-stop is the protection for what stays unverified. Today: L1-L6 are all NOT DONE and UNKNOWN.

## Cross-links added in the execution batch (2026-10-13)
- **L3 and Q5.** The candidate-count contract and the tests it needs are in `C31_C32_OWNER_DECISION_BRIEF.md` section 16. Evidence required from L3 for Q5: from the provider documentation (read by the researcher, dated, with the page), whether `candidates` can be absent or empty on a prompt block, whether a candidate can lack `finishReason`, whether a candidate can lack `content`/`parts`. Result states: PASS = each shape is documented; INCONCLUSIVE = not documented (then the contract's `candidates_returned` is recorded and the shape is treated as observed-only); no call is made to provoke a shape.
- **L2, L3, L4 evidence summary.** L2: the exact `modelVersion` string of one authorized call; L3: documented finish-reason and block names; L4: key names and the four token numbers of one authorized call. Each is UNKNOWN today.
- **L6 and O4.** The O4-after-pilot path (needs no provider call; prerequisites; decision rule) is in the brief section 17; `input_tokens_per_call_assumed` stays an assumption until it is run.
