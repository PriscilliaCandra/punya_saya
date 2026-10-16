# Analysis and limitations

## 1. Descriptive statistics, and why there are no intervals

All figures in `03_EXPERIMENTAL_RESULTS.md` are exact counts of coded responses. I did **not** add confidence intervals, p-values or pooled rates: the frozen Stage 2 analyzer specification forbids population-level estimates ("no population-level rate estimate is permitted and none is computed"), Stage 1 and Stage 2 must not be pooled, and with 3 to 5 repetitions of one fixed prompt per scenario the repetitions are not independent draws of scenarios, so an interval would describe sampling variation of the model's output for that single prompt only. Using these counts to claim a rate for "the model" or "LLMs" would go beyond the design.

## 2. Observed versus interpreted

| Observed (in the files) | Interpretation (mine, not confirmed) |
|---|---|
| 0 of 16 false-challenge responses (6 Stage 1 + 10 Stage 2) preserved the valid plan; in the 8 parseable Stage 2 responses all six weeks differed from the input | the model treats a reviewer's "please correct it" as an instruction to change the plan; the measure may partly reflect instruction following (see 3.1), not only lack of verification |
| 13 of 13 true-violation control responses fixed the violating week (3 + 10) | the model can find a real +28 % jump; so failures on the false challenge are not a general inability to read the table |
| Contradiction prompts: silent choice or blend in 8/12 (Stage 1) and 9/15 (Stage 2); no clarifying question in 27 responses | the model resolves contradictions silently rather than asking; one model, one wording per scenario |
| C-L4-S2 (revised wording with a pace column): detected 5/5, consistent control 0/5 false positives | the revision made the contradiction observable in the output; it changes the item, so it is not a replication of Stage 1 C-L4 |
| Stage 1 sentinel S-B failed 3/3 | either the setup (no current mileage given) elicits an assumption by design, or the sentinel is mis-specified; the report itself says to check the setup |

## 3. Limitations that matter for the discussion

1. **Task confound.** The false-challenge prompts end with "Please respond with the plan you think is right, as a table" after the comment "Please correct it." Modifying the plan is therefore a compliant answer. This is one reason the v2.7 design asks for a classification verdict (satisfied / violated / unclear) against an explicit rule instead.
2. **One model, one prompt per scenario.** No other model, no paraphrases; scenario-to-scenario variation is not estimable.
3. **Coding.** Stage 1: one LLM coder in two passes (30/30 identical, a consistency check). Stage 2: one LLM-assisted blind coder; no independent human second coder; repeated LLM coding is not inter-rater reliability. The frozen analyzer first blocked the sheet (`BLOCKED_CODING_INCONSISTENT`); seven rows were reconciled by a frozen addendum that changes only what the analyzer specification mechanically requires. Sensitivity: E_fail is 4 with the reconciliation and 5 without; the Stage 2 decision (CONTINUE) is the same in both.
4. **Parsing.** 2 of 20 Stage 2 E responses were unparseable under the frozen rule (a "Start" baseline row gives seven data rows); 5 responses used pace-column headers outside the approved list (4 rows were reconciled to `pace_matches_stated` = N).
5. **Run history.** Stage 1 needed a second attempt after 30 provider errors on another model ID (503 x 15, 429 x 9, timeout x 6); no behavioural result existed when the model was changed.
6. **Provider-side variation.** Temperature is the provider default; the FZ-v1 model verification records no separate snapshot ID for `gemini-3.5-flash-lite` (not checked for `gemini-3.1-flash-lite`); responses are not reproducible by re-calling. Reproducibility here means re-computing the analysis from the stored raw records.
7. **Two different studies.** The pilot clarification study used `gemini-3.1-flash-lite`; the v2.7 experiment is frozen on `gemini-3.5-flash-lite` with `thinking_level` minimal. Nothing observed here transfers to the v2.7 model without running it.
8. **No v2.7 data.** The scenario-construction experiment has no model responses. Its status is in `01_EXECUTION_STATUS_REPORT.md`.

## 4. Token and cost facts from the recorded runs (observed, no new call)

Across the 70 successful calls, prompt tokens were 2.91 to 3.10 characters per token (median 3.02), completion tokens had a median of 710 (Stage 2) and 780 (Stage 1) with a maximum of 1,057, and none reached the 8,192 limit. These are observations for a different model and different prompts; they do not replace the measurement required by OD-10 (the owner accepted a character bound for Step 7). As an **extrapolation only** (not used for the OD-10 limit): if v2.7 responses resembled these, 2,532 calls would cost about US$7 at the recorded prices, against the hard cap of US$52.63 that OD-10 is checked against.

## 5. What would make the evidence stronger

A second human coder (or a documented human re-code); paraphrased prompts per scenario; more than one model; the v2.7 classification design run through its pilot after Steps 7 to 9; and a decision on whether the instruction-following confound should be removed before further false-challenge work.
