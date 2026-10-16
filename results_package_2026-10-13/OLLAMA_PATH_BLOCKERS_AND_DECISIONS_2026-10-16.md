# Ollama `llama3.2:3b` path: blocker audit and decisions required (2026-10-16)

Status: audit and PROPOSALS only. Nothing here is a decision, an authorization or a change. It supports decision record entry 12.63, which records the owner's mandate. The official statuses are unchanged: Gemini pilot round 1 FAIL-S; O4 INCONCLUSIVE; main experiment BLOCKED / INCONCLUSIVE; local evaluation 12.62 = synthetic feasibility check only. The history (12.61 and earlier) is not changed.

## 1. What the specification says about changing the model (read-only)

- The specification text does not name a model: the model, provider and decoding settings are register item 17 ("RESEARCHER CHOICE", spec line 1036; frozen content layer, lines 794 and 797). The question names "the selected model" (lines 98, 1064).
- Spec 13.6 (versioning rule): any change of a frozen item "creates a new FZ version, is logged with a reason, and requires a re-pilot round counted toward the cap". A "format-changing modification" that lists the **model** "is permitted only if triggered by an SF finding or by a static defect found without reading response content; it voids the pilot data and consumes round 2. No modification of the frozen layers is allowed after round 2."
- Spec 13.6, FAIL-S in round 1: "one change from the whitelist (SF1: timeout, inter-call delay, retry count), logged as a new FZ version, then round 2; or STOP". The model is not on the whitelist.
- Spec 21.2: after the first pilot call there is no return to steps 1-9; only the paths of 13.6 apply.
- Two readings exist, and the specification does not settle between them (this is a stated ambiguity, not a finding): **(a)** the round-1 SF1 failure is the "SF finding" that triggers the format-changing modification: new FZ version, Gemini pilot data voided, the local pilot is round 2 (final), cap 2 holds; **(b)** the change is a successor protocol (a new methodology version, pilot-informed, lineage recording every round), which would restart the round count. (a) follows the text of 13.6 literally and keeps the cap; (b) is more permissive and needs a new specification document.

## 2. Gemini and cloud dependencies in the code (read-only audit)

| File | Dependency | Needed for Ollama |
|---|---|---|
| `step10/s10_runner.py` (18 hits) | `EXPECTED_SETTINGS` (model id, `thinking_level`, `max_output_tokens`); `REQUIRED_SETTING_TYPES`; `GeminiProvider` (REST `generateContent`, API key from the environment, `thinkingConfig`, `candidates`, `finishReason`, `modelVersion`, `usageMetadata`, `promptFeedback`); cost constants (Gemini prices), `hard_cap_cost_usd`, `RunState` cost from `promptTokenCount`/thoughts; `main()` builds `GeminiProvider` | new provider class or module (adapter verified against Ollama 0.6.7 and the installed digest); settings schema for the local provider; cost accounting for a zero-price provider; provider choice in `main()`; gate comparison of the settings |
| `step10/s10_resume.py` (4) | constructs `GeminiProvider` in its CLI and messages | same provider selection |
| `step10/s10_integrity.py` (5) | `output_tokens` (thinking tokens), requested-model checks, cost at recorded prices | accept the adapter's usage shape; cost reporting for the local provider |
| `step10/s10_scoring.py` (6) | `BLOCK_REASONS`, `TOKEN_LIMIT_REASONS` (`MAX_TOKENS`), `KNOWN_FINISH` | none if the adapter maps `done_reason` `stop` to `STOP` and `length` to `MAX_TOKENS` (observed for Ollama 0.6.7); unlisted values already count as anomalies |
| `step8/s8_build.py` (2) | settings tuple check at line 85 (model id, thinking level, tokens, retries, timeout, delay, concurrency) and the register hash constant | new expected tuple and register hash for FZ-v2 |
| `step7/*`, `step9/*`, `implementation_a/*`, `s8_construct.py`, `s8_gates.py`, parser, codebooks | no Gemini dependency found (grep) | none |

Not Gemini-specific and kept: generator, construct, conditions A-D, families MIL/PAC, registry content, prompts, SF1-SF5 definitions, scoring, ledger, E-1 mechanism, waiver mechanism, O4 reader (it needs `promptTokenCount`-shaped usage, which the adapter provides), analysis code.

## 3. Decisions and authorizations still required (proposals, none recorded)

| # | Decision | Proposal (assistant's, not a decision) |
|---|---|---|
| D1 | Methodology status and round counting (section 1) | Reading (a): new FZ version under the format-changing clause; Gemini pilot data voided (it was never analysed beyond counts); the local pilot is **round 2 and final**; a FAIL-S in round 2 is STOP. No new specification document |
| D2 | R-7 (Step 7 re-freeze), limited scope | Authorize only what FZ-v2 forces: a new Step 7 freeze manifest citing the FZ-v2 register hash, a Step 8 rebuild into a NEW folder, comparison of the rendered prompt hashes with the current build (expected identical; registry/provenance files differ), a new waiver and a new FZ index and hash. No change to the specification, codebook, K1, H4, PG decisions or the waiver decision 12.56 |
| D3 | Content of FZ-v2 (register item 17; all other rows unchanged) | provider Ollama (loopback `127.0.0.1:11434`); model `llama3.2:3b` with the digest and Ollama version of the installed instance, re-checked in preflight (abort on mismatch); `num_ctx` 16384; `num_predict` 8192; `keep_alive` 30m; `stream` false; no system prompt; `temperature`, `seed`, `top_k`, `top_p` not sent (Ollama defaults); timeout 180 s; delay 1 s; concurrency 1; retries 0; returned model id recorded for every call |
| D4 | Decoding policy and repetitions | Keep the Ollama defaults as in 12.62 (observed stochastic: 0 of 16 repeat pairs identical text), so R = 2 stays meaningful; record version and digest |
| D5 | Pilot criteria | Unchanged from the register declared before any result: `f_S` 1, `theta_unp` 0.50, `c_stop` 5, `theta_main` 0.10, `calls_min_main` 100; the pilot size stays 18 calls. Not changed after seeing any result |
| D6 | Stop rules | Unchanged 13.8 monitor; resume stays closed (12.43-12.45): if the local server stops, the run ends incomplete and nothing is replaced; MD-06 safe-stop triggers (model id, unlisted finish reason, record without HTTP status) apply to the adapter |
| D7 | Cost gate for a local provider | Zero-price accounting for the Ollama provider; the H5 file keeps `cost_ceiling_usd` 100, `input_tokens_per_call_assumed` 1016 and `max_input_characters` 1016 (nominal; no money is spent) |
| D8 | Code authorization | Implement the adapter and the edits listed in section 2 with backups and tests (mock server and negative tests); new tests for the settings schema, the cost accounting and the preflight; the 31-file list membership stays (a new provider file would need a decision whether it joins the list) |
| D9 | MD-09 anchoring | Needed before the first successful `s11_pilot decide` (the local pilot) and before the main run. The owner must declare the store (for example a commit of the decision record, which needs a separate commit authorization, or another write-once store) |
| D10 | Authorization files | The owner writes (or asks for) a new H5 for the local pilot (scope `pilot_round_2`, 18 calls) and later one for the main run (2,496 calls) |
| D11 | Who runs the live steps | The owner starts them, or authorizes the assistant to run the local pilot and main run on the loopback server as was done for 12.62 |
| D12 | Acknowledgement of a known risk | The only evidence on this model is a synthetic check with about 46 % verdict agreement (informational); a floor effect (TH10) is possible. The owner accepts proceeding, with this disclosed |

## 4. Sequence after the decisions (each step has a gate)

1. Record D1-D12 as a new entry. 2. Backups; FZ-v2 file (new; FZ-v1 untouched). 3. Code and tests (negative, stop, integrity, adapter against a mock server; then a read-only check against the installed Ollama for the mapping). 4. R-7 sequence: new Step 7 manifest, Step 8 rebuild into a new folder, verifier, Implementation B, slow Step 8 suite, prompt-hash comparison. 5. New waiver, FZ index and official FZ hash (owner's instruction). 6. H5, MD-09. 7. Preflight (settings match runtime, version and digest, criteria, call count, E-1, gate). 8. Pilot round 2 (18 calls). 9. `report`, then `decide` only after MD-09. 10. If PASS: final freeze manifest, H5 for the main run, main run (2,496 calls), integrity check, report. If FAIL-S or FAIL-U: STOP; no main run.

## 5. Stop conditions

Any mandatory check fails; the installed Ollama version or model digest differs from the frozen values; the prompt hashes of the rebuilt registry differ unexpectedly; MD-09 undecided before `decide`; the pilot is not PASS; any anomaly that MD-06 treats as a stop. No threshold, setting or criterion is changed after a result is seen.

## 6. What the mandate covers now

The owner's message of 2026-10-16 is recorded in entry 12.63 as the decision to pursue this path and to supersede the "next step: STOP" of 12.61 for it. It authorizes read-only audit and the preparation of proposals. It does not decide D1-D12, authorize R-7, a code change, FZ-v2, a rebuild, an official hash, a pilot, a main run, a commit or a push. These stay blockers until the owner records the decisions above.
