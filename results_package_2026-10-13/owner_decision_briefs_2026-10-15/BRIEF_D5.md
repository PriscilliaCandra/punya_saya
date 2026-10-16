# D5: Re-code values and the departures from 16.3 (sample, delay, columns)

**Status: PENDING OWNER DECISION: BLOCKED — SOURCE TEXT REQUIRED (partial: see section 9).** Prepared 2026-10-15T03:30:47Z. The owner makes this decision; nothing here is adopted. Dependencies: MD-03.

## 1. Why a decision is needed
The sample rule, the 14-day delay and the column names of the re-code are 'delegated' choices without empirical basis; they live in the codebook, an FZ item (C-09).

## 2-3. Authoritative sources and verbatim quotations
Quotations are exact text from the files and lines named (excerpts are marked). Interpretation is confined to sections 5-8.

**`results_package_2026-10-13/ADVISOR_DECISION_BRIEF.md` lines 39-45**

> ## D5. Re-code values and the departures from §16.3  (before FZ hash: the codebook is an FZ item; before S2/S3 coding at the latest)
> - **Reference:** §16.3 lines 997-1003; OD-3 (`STEP2_OWNER_DECISIONS_RECORD.md`: one coder, no inter-rater reliability or kappa claim); 12.21 row 6; 12.24 decision 2; 12.26 item 3; codebook revision 5 section 5.3; `step7/s7_recode.py`.
> - **Problem:** the delegated procedure uses a 20 % sample (floor 20), 14 days, `recode1_*` columns and no kappa; §16.3 states no sample, no delay, names `coder1_*`/`coder2_*` and says kappa is reported.
> - **Options:** (a) approve the delegated values and record the departures; (b) re-code every coded response and report kappa labelled "intra-rater consistency, no reliability claim"; (c) other values.
> - **Consequences:** (a) fastest, weakest evidence; (b) closest to the literal text and OD-3's wording (OD-3 forbids claims, not computation), larger workload and a change to `s7_recode.py`; the owner chose (a) on 2026-10-13 pending the advisor.
> - **Recommendation:** (a), with the advisor's explicit approval of the 14-day delay and the sample.
> - **Decision:** ________________  **Date:** ________

**`research_design/step7/CODEBOOK_S2_S3_v1_DRAFT.md` lines 159-185**

> ## 5. Delayed intra-rater re-code (OD-3; section 16.3; 12.21 row 6)
>
> One human coder exists. All values below were fixed in this draft before any response exists; they are delegated choices without an
> empirical basis. `s7_recode.py` implements the selection, the order and the agreement table.
>
> - **Eligible material.** Parseable responses (`D_P`). S2 is re-coded for all conditions, S3 for Cond-C and Cond-D. One sample per
>   (family, condition) cell serves both.
> - **Sample size.** All parseable responses of the cell if there are at most 20; otherwise max(20, ceil(0.20 x `D_P`)). The counts
>   `D_P` come from the primary scoring, not from any code, so the size cannot depend on agreement.
> - **Selection.** Responses are ranked by SHA-256 of `recode-select,<bundle hash>,<opaque id>`; the smallest keys are taken. The bundle
>   hash is the SHA-256 of the sorted opaque IDs, LF separated, final LF. It is recorded when the coder bundle has passed PG11b and
>   before any coding starts. No random state.
> - **Order.** The re-code order is by SHA-256 of `recode-order,<bundle hash>,<opaque id>`; the first pass is in opaque-ID order, so the
>   orders differ. The selected list and the order are written to files and hashed before the re-code starts.
> - **Concealment.** The re-code sheet is built from the coder bundle and contains no first-pass code. The first-pass sheet is not
>   opened between the end of the first pass and the end of the re-code.
> - **Delay.** At least 14 full days between the last first-pass code and the first re-code; both UTC dates are recorded.
> - **Storage.** First pass in the immutable `coder1_*` columns, re-code in immutable `recode1_*` columns. The name `coder2_*` is not
>   used, so that nothing reads as two coders. Nothing is overwritten.
> - **Reporting.** Per variable (`s2_evidence`, `s2_prov`, `s2_values`, `s2_arith`, `s2_rel`, `s3_stance`, the derived flag), overall and
>   per cell: number of pairs, number of agreements, raw agreement percentage, the full first-by-second cross-table and the disagreement
>   counts. `s3_ref` is computed by rule, not coded, and is not re-coded. **No Cohen's kappa, no interval, no inter-rater reliability
>   claim**; the statement "single coder, intra-rater only" accompanies every table.
> - **Disagreements.** Resolved by the codebook text into the `final_*` columns; if the codebook is silent the item is `unresolved`
>   and the gap is logged (section 16.3). A new reading is a new codebook version in a new column.
>
> ### 5.1 Canonical inputs and reproducibility (12.24 decision 2; `s7_recode.py`)

**`results_package_2026-10-13/MASTER_PREPILOT_RESOLUTION.md` lines 58-58**

> **D5 Re-code and kappa (C-02, C-09).** Rule: spec §16.3 lines 1000-1003 (columns `coder1_*`/`coder2_*`; "Agreement is reported per variable (percent agreement and Cohen's κ)"; the single-coder fallback "delayed intra-rater re-code ... (limitation: no inter-rater reliability)"); OD-3 (`STEP2_OWNER_DECISIONS_RECORD.md` line 45: "No inter-rater reliability and no Cohen's κ may be claimed"); 12.21 row 6 (line 602), 12.24 decision 2 (DELEGATED), P-3 item 3, codebook revision 5 sections 5 and 5.3. State: `s7_recode.py` computes raw agreement only. Conflict (scope and verb, not a direct contradiction): see `CONFLICT_RESOLUTION_BRIEF.md` section 2. The sample (20 %, floor 20), the 14-day delay and `recode1_*` are silence-filling choices that the sources label delegated. I do not conclude that kappa will or will not be reported. Options: K1 raw only; K2 kappa with label; K3 kappa with threshold; K4 amend. Recommendation: K2 with a rule for undefined cases, values approved by the advisor. Impact: code only for K2/K3 (`agreement_table`, tests, codebook 5.1/5.3); codebook is an FZ item. Protocol change: K1/K2/K3 no (clarification of how the text is read; K1 departs from the literal line 1002), K4 yes. Acceptance: record entry stating the verb ("computed" / "reported" / "claimed") separately.

**`results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 33-33**

> | 2 | **MD-03:** K1 (raw agreement only, recorded departure from spec line 1002) or K2 (kappa labelled intra-rater, literal text)? | K1: no code, no re-freeze | K2: Step 7 re-freeze (R-7), Step 8 rebuild, new manifest | K2 only | | | | |


## 4. Original options (labels and order as in the sources)
The sources offer one concrete value set (confirm as written) and say alternatives would be 'other values'; the options of the departures are those of MD-03 (K1-K4), quoted in the MD-03 brief. Original option labels of ADVISOR_DECISION_BRIEF D5 are in the quoted section.

## 5. Consequences
- Source-defined: values are 'delegated choices without an empirical basis' (codebook 5); the codebook is an FZ item (ADV D5 heading).
- Reasoned: confirming as written changes nothing; any other value changes the codebook and `s7_recode.py` (Step 7 re-freeze, Step 8 rebuild).

## 6. Recommendation: NOT ADOPTED
Source recommendation (NOT ADOPTED): `MASTER_PREPILOT_RESOLUTION.md` D5: 'K2 with a rule for undefined cases, values approved by the advisor' (quoted above).

## 7. Record cross-check
Decision record cross-check (read-only search of `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` for `D5`, `C-09`, `recode`): lines [547, 602, 627, 642, 689, 691, 703, 716] .... Hits are mentions only. Entries 12.40-12.45 were read for this check: they either do not mention this item or state it as not decided (12.43, 12.44).

## 8. Dependencies
See the dependencies named in the header of this brief; no further source-backed content.

## 9. Information still missing
- Alternative values: none supplied by any source (BLOCKED — SOURCE TEXT REQUIRED for any value other than 20 %/floor 20, 14 days, `recode1_*`).
- Advisor approval of the values: not obtained.

## 10. Owner response (unfilled)
- [ ] confirm the values as written (sample max(20, ceil(0.20 x D_P)), 14 full days, columns `recode1_*`)
- [ ] other values: ______ (must be supplied)
- Owner: ______    Date: ______    Conditions: ______

## 11. Recording instruction
Do not record any outcome until the owner explicitly adopts it. The recording is a new entry in the owner decision record written under the owner's authority; this brief and its recommendation are not an entry and not a decision.
