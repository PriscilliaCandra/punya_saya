# DRAFT (NOT RECORDED, NOT APPROVED): review of the HTTP 429 on pilot round 1 and the disposition of round 1, for the owner's review, 2026-10-15

Status: a draft text only. Nothing was run for it (no provider call, no network, no credential, no change of any pilot artifact, record, FZ-v1 value or code). Evidence: `calls.jsonl`, `ledger.jsonl` and `RUN_COMPLETE` of `runs/pilot_round_1_run1` read for field names, types and numbers only (no prompt, response, call key or condition printed), `pilot_round_1_report.json`, spec 13.6, `s10_runner.py`.

## 1. What is known (facts)

- Calls 17 and 18 (the last two) returned HTTP 429, recorded as `error` = "HTTP 429", no model, no finish reason, no usage; classified SF1; retries = 0 (frozen). The runner stores nothing of an error body (`generate`, HTTPError branch), so the reason text of the 429 does not exist locally.
- Calls 1-16 returned HTTP 200 with complete usage. Round 1 counts: SF1 = 2, SF2-SF5 = 0, UNP = 3 of 18 (1/6 < 1/2). `f_S` = 1, so SF1 + SF4 = 2 > 1: **FAIL-S** (`s11_pilot report`, sha256 `b84f82602d38...080d`). `RUN_COMPLETE`, 18 calls, ledger final hash `2af68583f5b4256e49eac566c3fbe2f914ebe3a852c63cc8e658483532e75aa9`, observed cost US$0.0141 (lower bound) to US$0.0556 (conservative).
- Timing (UTC, 2026-10-15): call 1 at 09:23:55; calls 2-18 all started in the clock minute 09:24 (17 calls, the last at 09:24:52). Offsets in seconds from call 1: 0, 7, 10, 15, 18, 21, 26, 29, 33, 37, 39, 41, 43, 47, 50, 53, 55, 57. The settings were the frozen ones (delay 1 s, concurrency 1). Tokens of the 16 successful calls: 9,153 in total.

## 2. Likely cause (hypotheses; none confirmed without the provider's error body or documentation)

- **H1, a limit of 15 requests per fixed clock minute:** calls 2-16 are the 15 successes of minute 09:24; calls 17 and 18 are the 16th and 17th requests of that minute. This matches exactly.
- **H2, a limit of 16 requests per rolling minute:** also consistent (call 17 is the 17th within 55 s). A rolling limit of 15 is NOT consistent (call 16 would have failed).
- A token-per-minute limit is unlikely (about 9k tokens in the minute). A daily quota cannot be excluded.
- Under both H1 and H2 the frozen pacing (about 3.3 s per call, 18 calls in 57 s) produces more than 15 requests in one minute again. Waiting between rounds alone does not remove the cause unless it was a daily quota. The provider's documented limits are not available locally; they were not looked up (no network).

## 3. A correction of my earlier statement

I wrote that round 2 "remains possible". Spec 13.6 says: FAIL-S in round 1 => EITHER one change from the whitelist that addresses the failure type (SF1 => `{timeout, inter-call delay, retry count}`), logged as a NEW FZ version, then round 2; OR STOP if no whitelisted change fits. A plain repeat under the unchanged FZ-v1 is neither. Decision 12.54 row 1 ("same FZ and same build") concerns a SAFE-STOP, which has no round outcome; row 6 of 12.54 sends FAIL-S to spec 13.6 and its change rules. So the choices below are the real ones.

## 4. Options for the next step

| | N1. Round 2 under the unchanged FZ-v1, as a recorded departure (after the provider limit is verified) | N2. The whitelisted change: a longer inter-call delay (spec 13.6), new FZ version | N3. STOP |
|---|---|---|---|
| What changes | no frozen value. The owner records a departure from the FAIL-S action clause: the SF1 were provider rate-limit responses, an external condition | `delay_between_calls_s` in FZ-v1 row 17 (for example 1 s to about 4 s so that fewer than 15 calls fall in a minute) | nothing |
| Fixing the cause | only if the provider limit allows at least 19 requests per minute for this key and model (the owner checks the account/console; a different tier is an account action, not an FZ change), or by luck of timing under H1 | yes, if the limit is about 15 per minute | none |
| Conformity | NOT conform to the letter of 13.6; disclosed as a departure; counts as round 2 (cap 2 holds) | conform to 13.6 | conform |
| Effort | small: a record entry, a new H5 file, the live start | large: register change = new FZ version; the runner's `EXPECTED_SETTINGS`, the Step 8 builder's settings check, the Step 7 manifest and the Step 8 manifest cite the old register, so it needs R-7 (NOT AUTHORIZED), a Step 7 re-freeze, a Step 8 rebuild with the 2,026-file comparison, a new waiver, a new FZ index and FZ hash, then round 2 | none |
| Risk | if the limit is not lifted, round 2 fails the same way and, being FAIL-S in round 2, ends in STOP | round 2 can still fail for other reasons | ends the research without a main run |
| O4 | round 2 would supply usage for all calls if no 429 | same | INCONCLUSIVE stays |

Not options: changing the delay or adding a throttle in code without an FZ version (spec 13.6, "versioning rule": any change of delay, timeout or retry creates a new FZ version); retrying the two failed calls (retries = 0, frozen); editing or deleting round 1.

Recommendation (assistant's, not a decision): first verify the provider limit (owner action, no code). If it allows at least 19 requests per minute, N1; if it cannot be lifted, N2 only if the owner authorizes R-7, otherwise N3. N1 is the fastest but it is a departure; N2 is the only fully conform way to continue.

## 5. Draft disposition of round 1 (the form of 12.54)

> **12.__ Disposition of pilot round 1.** Pilot attempt of scope `pilot_round_1`, folder `results_package_2026-10-13/runs/pilot_round_1_run1`, ledger final hash `2af68583f5b4256e49eac566c3fbe2f914ebe3a852c63cc8e658483532e75aa9`, recorded calls 18, halt reason: none (`RUN_COMPLETE`); round outcome by `s11_pilot report` (sha256 `b84f82602d387f4f007b3ec659c5be8a0f4787894a7eca3414da6ffacffc080d`): **FAIL-S** (SF1 = 2 > `f_S` = 1; the two SF1 are HTTP 429 on calls 17 and 18; SF2-SF5 = 0; UNP 3/18, below the threshold): **counted as round 1**; next step: ______ (the owner states N1, N2 or N3 of the review above, and for N1 the verified provider limit and the reason for the departure).
>
> The folder is never deleted, edited or resumed. `s11_pilot decide` was not run for round 1: FAIL-S in round 1 writes no record. The O4 result stays INCONCLUSIVE (calls 17 and 18 have no usage). Observed cost US$0.0141 to US$0.0556. The two failures and the cause hypotheses (H1, H2) are disclosed in the final report.

Not authorized by this draft: any entry, any change, any run.
