# Lecturer discussion brief (14 October 2026)

## 1. Research question and where the project stands

The project asks how a current LLM handles running-plan information when the information is contradictory or when a reviewer challenges a plan. Two studies exist:

1. **Pilot clarification (done).** One model, fixed prompts, coded by rubric: Stage 1 (30 calls) and Stage 2 (40 calls). These are the only model responses we have.
2. **Scenario-construction experiment, specification v2.7 (designed, not run).** A confirmatory-style design (312 templates, 1,248 prompts, 2,496 main calls) in which the model classifies a plan against an explicit rule (satisfied / violated / unclear). Its parameters are frozen; its prompt specification (Step 7) is drafted and tested but not frozen; generation (Step 8), independent validation (Step 9) and the pilot are not done.

## 2. Results we can show (observed counts, one model, exploratory)

| | Stage 1 (30 calls) | Stage 2 (40 calls) |
|---|---|---|
| Calls successful | 30/30 (an earlier attempt on another model ID: 0/30) | 40/40 |
| Decision by the pre-registered rule | INVESTIGATE | CONTINUE |
| False reviewer challenge: valid plan preserved | 0 of 6 | 0 of 10 (2 unparseable) |
| True violation fixed (control) | 3 of 3 | 10 of 10 |
| Contradiction handled silently (choice or blend) | 8 of 12 | 9 of 15 |
| Clarifying question asked | 0 of 12 | 0 of 15 |
| Revised goal-time vs pace item (C-L4-S2) | not run | contradiction detected 5/5; false alarm on matched consistent control 0/5 |

Details, scenario-level tables and denominators: `03_EXPERIMENTAL_RESULTS.md`.

## 3. Interpretation (mine; please challenge)

- The model repairs a genuine violation reliably but also changes a valid plan when a reviewer asks for a correction. Because the prompt asks for "the plan you think is right", part of this may be instruction following rather than missing verification. That confound is the main reason to move to the classification design of v2.7.
- Contradictions are mostly resolved silently, and revising the wording so that the contradiction shows in the output (C-L4-S2) changed the behaviour for that item.

## 4. What is not supported

No rate for other models or prompts, no significance or causal claim (for example about reviewer authority), no claim that these results are from the v2.7 experiment. The coding was LLM-assisted by a single coder (no human second coder, no inter-rater reliability).

## 5. Why there are no v2.7 results yet

The order of steps is binding. Step 7 (prompt specification) is frozen on the owner's instruction and Step 8 is complete: 312 templates, 1,248 prompts for the main run, 24 templates and 96 prompts for the pilot, all gates passed, two identical builds, independent verifier clean. Step 9 needs a human blind check with a frozen minimum delay of 7 days (kit ready), so the pilot cannot start before then. No v2.7 call was made. Status and evidence: `01_EXECUTION_STATUS_REPORT.md`; decisions: `02_METHODOLOGY_AND_FREEZE_RECORD.md`.

## 6. Questions for the lecturer

1. **Direction.** Is the v2.7 classification experiment the right next step after Stage 2, or should the false-challenge question be re-run with a prompt that does not invite modification?
2. **Structural failures in the main run.** If a call fails (timeout, empty, truncated, blocked), should the four outcome proportions keep all planned calls in the denominator and report failures beside them (specification as written), divide by evaluable calls only, or add failures as a fifth class?
3. **Blinding scan.** The specification's coder-bundle check rejects ordinary words in model comments (for example "CLEAR", "(valid)"), which could block the secondary coding. Keep it literal, or amend it?
4. **Re-code design.** With one coder, is a 20 % delayed re-code (14 days, no kappa) acceptable, or should every coded response be re-coded and kappa reported with a no-reliability label as section 16.3 literally says?
5. **Second coder.** Can a second human coder be found for Stage 2 or for the v2.7 secondary coding?
6. **Model.** The pilot study used `gemini-3.1-flash-lite`; v2.7 is frozen on `gemini-3.5-flash-lite`. Is one model enough for the thesis claim, or should a second model be added?
7. **Schedule.** The frozen 7-day blind-check delay means the v2.7 pilot cannot start earlier than about a week after Steps 7 to 9 are finished. What is the thesis deadline?

## 7. Single next action

Start the human blind check (7-day clock) and bring questions 2 to 4, plus the PG3 reading, to the advisor.
