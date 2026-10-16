# H5: Pilot authorization file (H5)

**Status: PENDING OWNER DECISION: READY FOR OWNER.** Prepared 2026-10-15T03:30:47Z. The owner makes this decision; nothing here is adopted. Dependencies: MD-02; code freeze.

## 1. Why a decision is needed
The runner gate requires an owner-written authorization file; none exists.

## 2-3. Authoritative sources and verbatim quotations
Quotations are exact text from the files and lines named (excerpts are marked). Interpretation is confined to sections 5-8.

**`results_package_2026-10-13/HUMAN_TASKS_H1_H7_OPERATIONAL_CHECKLIST.md` lines 93-100**

> ## H5 Owner authorization (pilot round 1)
> - **Purpose.** The owner's written authorization read by the gate (`check_gates`).
> - **Procedure.** The owner (not the assistant) copies `templates/owner_authorization_TEMPLATE.json` to a new file and writes: `authorized_by` = `owner`; `scope` = `pilot_round_1`; `max_calls` = 18; `cost_ceiling_usd` = 100; `input_tokens_per_call_assumed` = a positive integer chosen by the owner (the accepted Step 7 assumption is 1016, i.e. at least one token per character; it is an assumption, not a measurement; C-32); `max_input_characters` = a positive integer chosen by the owner (the longest planned prompt is 1,016 characters; a smaller value is refused by the preflight; a larger one is allowed). The note field is not read.
> - **Inputs.** The owner's decisions on MD-02 / C-32 (Q7-Q9) and, if the owner so decides, on the cost basis.
> - **Evidence.** The saved authorization file with its SHA-256 and the date the owner wrote it; the hard-cap figure printed by the gate preflight (about US$0.37 for 18 calls at 1,016 assumed tokens, `hard_cap_cost_usd`; a cost bound, not a forecast).
> - **Acceptance.** Gate check without `--live` no longer lists the authorization reasons; the limit is a control on prompt length only, not a token measurement and not a cost guarantee.
> - **Expected location.** `human_evidence/authorization/authorization_pilot_round_1.json`.
> - **Status.** NOT DONE (only the invalid template exists).

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 92-92**

> 5. The pilot authorization file (H5), a NEW file written by you: `authorized_by` = `owner`, `scope` = `pilot_round_1`, `max_calls` = 18, `cost_ceiling_usd` = 100, `input_tokens_per_call_assumed` (positive integer, your assumption), `max_input_characters` (positive integer, at least the longest planned prompt, 1,016). The gate reads only these fields, plus the Step 9 evidence file, a verified build and the expected register settings. Provider-related permissions are NOT read by the gate: a connection test (P11) needs its own written authorization file; a provider token count (O2) needs its own written authorization with a spending basis; the pilot itself needs your separate explicit instruction after the gate prints "gates open". The API key must be present in the environment variable (the preflight checks presence and never prints it).


## 4. Original options (labels and order as in the sources)
Not an option choice: a NEW file written by the owner with the fields named in the quotation.

## 5. Consequences
- Source-defined: the fields and values in the quoted procedure.
- Reasoned: the file is invalid while empty; the assistant must not write it; it follows MD-02 and the code-freeze declaration.

## 6. Recommendation: NOT ADOPTED
None.

## 7. Record cross-check
Decision record cross-check (read-only search of `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` for `authorization`): lines [9, 279, 280, 346, 396, 443, 458, 473] .... Hits are mentions only. Entries 12.40-12.45 were read for this check: they either do not mention this item or state it as not decided (12.43, 12.44).

## 8. Dependencies
See the dependencies named in the header of this brief; no further source-backed content.

## 9. Information still missing
- None for the procedure. The values depend on MD-02.

## 10. Owner response (unfilled)
- [ ] I have written the authorization file at: ______
- [ ] not yet
- Owner: ______    Date: ______    Conditions: ______

## 11. Recording instruction
Do not record any outcome until the owner explicitly adopts it. The recording is a new entry in the owner decision record written under the owner's authority; this brief and its recommendation are not an entry and not a decision.
