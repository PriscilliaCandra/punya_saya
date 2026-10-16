> **Status note (2026-10-13, added later):** the SF items of this file describe the SF counting BEFORE patch P1. Since then the code applies the working technical decision MD-01 (hard flags -> FAIL-S, one decision count per call; not ratified) and the SF2-with-SF1/SF4 question is analysed in `C31_C32_OWNER_DECISION_BRIEF.md`. Read the case tables below as the earlier state.

# Proposed final decisions (PROPOSED — NOT ADOPTED)

Prepared 2026-10-13 from the files named in each item. Nothing here is a decision, an amendment, a protocol change or an instruction to change code. Every item ends with `Owner/advisor decision: PENDING`. Draft record entries are in `PROPOSED_DECISION_RECORD_ENTRIES.md`; the official record `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` was not touched.

Abbreviations as defined in the sources: **OD-10** cost limit US$100 and measure `I_max` (record 12.11, line ~402; spec §19.2); **PRD-n** pending researcher decisions (spec §19.3, lines 1126-1136); **PC-2** step at which the pilot registry is first built (spec line 1136); **I-6** the undefined "six-reading invariance check" (spec §11 layer 1, line 670; record 12.23 table, line ~653); **P-2** FZ hash contract, **P-3** specification text inconsistencies, **P-4** token adequacy (proposals in `research_design/step7/PROPOSED_CLARIFICATIONS_AND_AMENDMENTS_DRAFT_v1.md`, adopted nowhere, record 12.21 rows 5, 7, 8); **F-3** generator must take values from the register (12.23 table); **D1-D8** the items of `ADVISOR_DECISION_BRIEF.md`. Line numbers are those of the files on 2026-10-13.

## 0. Impact matrix
Categories: NPC = NO PROTOCOL CHANGE; CN = CLARIFICATION NEEDED; PCA = PROTOCOL CHANGE — APPROVAL REQUIRED; LV = LIVE VERIFICATION REQUIRED; HT = HUMAN TASK REQUIRED.

| # | Item | Categories | Why |
|---|---|---|---|
| 1 | D1 PG3 single changed span | CN | The text says "contiguous" and, in §8.2, "a single changed span"; the strict reading rejects 90 of 104 MIL templates. Ratifying the §8.2 reading adds no rule. The strict reading would be a build rejection and a return to step 3/7. |
| 2 | D2 PG11b scan | NPC (keep) / PCA (narrow) | Keeping is the frozen text; any narrowing contradicts "any file body". |
| 3 | D3 SF / UNP policy | CN (interim) / PCA (Policy 1, 2, parse-first) | Interim rule is v2.7 text plus the SF-first sentence of 12.18 row 1; any change of §18.2 is a new methodology version. |
| 4 | D4 primary SF order | CN | §13.4 states no order. The order is a counting convention; a code point (section 4) must follow the literal flag reading of §13.6. |
| 5 | D5 re-code and §16.3 | CN / PCA | Sample, delay, columns and kappa depart from the literal §16.3 text. |
| 6 | D6 coding eligibility | CN | "parseable" is undefined for SF3 with a verdict. |
| 7 | D7 PRD-5 | CN | Field-specific unit sets are printed; the decision is marked pending. |
| 8 | Q-P1 returned model | CN / LV | Protocol: record only. Whether a difference matters is a rule the text lacks; the real form of the returned ID is a live fact. |
| 9 | Q-P2 unlisted finish reason | CN / LV | Protocol silent; the real vocabulary is a live fact. |
| 10 | Q-P3 "blocked" names | CN / LV | §13.4 says "safety/blocked"; names beyond it are an implementation list. |
| 11 | Q-P4 record without HTTP status | CN | A coding rule for an incoherent record. |
| 12 | Timeout 180 s | CN or PCA, LV | Text says "timeout 180 s"; a total deadline is a behaviour change of a frozen setting if it changes outcomes. |
| 13 | Resume after transport halt | CN / PCA | §13.8 allows it but leaves five points open; counters reset would be a new rule. |
| 14 | PRD-6 anchor of the decision record | CN, HT | §10 requires it and says the store is declared at step 6; FZ-v1 declares none. |
| 15 | P-2 FZ hash contract | CN / PCA | The text names "the FZ hash" without an object. |
| 16 | OD-10 / P-4 input size and cost | CN, LV, HT | Frozen text requires measurement of `I_max`; the owner accepted a character bound "for Step 7". |
| 17 | PC-2 | CN | Reading already applied in 12.28. |
| 18 | I-6 | CN | Undefined check; made informational in 12.28. |
| 19 | P-3 (four text inconsistencies) | CN | Three already applied by owner entries; one open (`s2_values`). |
| 20 | F-3, PRD-8, round-1 FAIL-S multi-type, P-5 | CN / HT | Technical closure or researcher decisions at the time they arise. |

What can be settled by reading documents: items 1, 4, 7, 17, 18, 19 (partly 20). What needs an owner/advisor decision: 2, 3, 5, 6, 8-13, 15, 16. What needs the blind check or the codebook rehearsal: the evidence of items 1 (nothing), 7 (unit sets are exercised by the human worksheet), 5 and 6 (rehearsal exposes codebook ambiguity), P-5. What needs one authorized live connection test: 8, 9, 10, 12 (behaviour), 16 (a token count) and the facts listed in `PROVIDER_RESPONSE_VALIDATION_REPORT.md` section 5.

## 0.1 Conflicts between sources or between a recommendation and the protocol (not resolved here)
1. **OD-10 versus the accepted character bound.** Record 12.11 (OD-10, line ~402) says `I_max` is measured on the actual prompt; 12.18 row 6 accepts a character bound "for Step 7" and says it replaces the measurement for Step 7 only. No entry says what holds at the first paid call.
2. **Kappa.** §16.3 line 1002 says kappa is reported; OD-3 (`STEP2_OWNER_DECISIONS_RECORD.md`) says none "may be claimed"; 12.21 row 6 and P-3 item 3 say "kappa is not reported". These are three different statements.
3. **Step 11 order versus the final freeze manifest tool.** §10 puts "the FZ hash" inside the decision record; §21.1 row 11 hashes the final freeze manifest after the record. `step10/s11_final_freeze_manifest.py` includes the decision-record hash, so its output cannot be the FZ hash of the record (circular). See item 15.
4. **Blocked list.** The earlier brief (`ADVISOR_DECISION_BRIEF.md` D8) recommended keeping RECITATION, OTHER, LANGUAGE as SF4; the conservative principle (do not widen "blocked" by name) argues against. This document supersedes that recommendation (item 10).
5. **Primary SF order.** The earlier brief (D4) said the pilot outcome does not depend on the order. After the fail-closed rule of 12.36 an incoherent record can carry SF1 together with SF3, and the provisional order would count it as SF1 (soft). This document corrects that statement (item 4).
6. **`pilot_counts` versus §13.6.** §13.6 states the outcome in terms of the SF definitions met ("any SF2, SF3, SF5"), while the implementation counts one primary type per call.

---
## 1. D1 — PG3: "contiguous" changed span   `PROPOSED — NOT ADOPTED`
- **Sources:** spec §8.1 row PG3 (line 461), §8.2 final paragraph (line 525: "a single changed span"); record 12.28; `step8/s8_gates.py` `pair_problems`; `main/gate_report.json` field `PG3_strict_nonconsecutive_pairs_informational` (180); `step9/impl_b.py` PG3 check.
- **Current rule:** differing positions lie inside the target token's span; strict consecutiveness is counted, not enforced.
- **Recommendation:** ratify the single-span reading as a clarification. **Consistency:** clarifies an ambiguity; the strict reading cannot hold for the frozen registry. **Alternatives:** (b) strict reading: the build is rejected (§21.2) and steps 3-9 repeat with new MIL parameters or wording; (c) amend PG3 in a new methodology version.
- **Impact:** validity: none lost (the intent is that nothing outside the token differs); cost: (b) days of work and a new registry; reproducibility: (a) none; ledger and analysis: none; gate: (a) the PG3 reading stays as built.
- **Reason:** §8.2 states the intent; the strict reading would reject the design for the decimal point.
- Owner/advisor decision: PENDING

## 2. D2 — PG11b scan scope   `PROPOSED — NOT ADOPTED`
- **Sources:** spec §8.2 (lines 519-520), §21.2 row 6 (line 1206), §22 item 17; record 12.14 (builders are FZ items), 12.26 item 2; `step7/s7_bundle.py` lines 30, 64-98.
- **Current rule:** literal: names, directories and bodies, PT1 and PT3-PT8b, applied to the post-run coder bundle including model text.
- **Recommendation:** keep the literal rule for the pilot and the first run, state the risk in writing (secondary coding may be blocked; primary results unaffected). **Consistency:** consistent. **Alternatives:** scan only non-response parts; scan response text only for machine-form patterns; mask matches (alters coder material). All three are protocol changes (new methodology version, Step 7 re-freeze, builder is an FZ item).
- **Impact:** validity: keep = blinding protection of the secondary analysis intact; cost: narrowing costs a re-freeze before the FZ hash; reproducibility: unchanged if kept; ledger/analysis: none for the primary analysis; gate: not a pilot gate (post-run).
- **Reason:** least change; the failure is recoverable only by an amendment, which can be made after seeing which words occur only if the amendment is made before data (it cannot use responses), so the decision belongs before the FZ hash.
- Owner/advisor decision: PENDING

## 3. D3 — Structural failures, SF and UNP   `PROPOSED — NOT ADOPTED`
- **Sources:** spec §13.4 (805-816), §13.6 (822-841), §13.8 (871-875), §18.2 (1051-1058), §22 item 6 (1223); record 12.18 row 1 (506), 12.24 decision 1, 12.26 item 1; `PROPOSED_AMENDMENT_18_2_DRAFT_v1.md`; `POLICY_2_METHODOLOGY_DECISION_PACKAGE_DRAFT_v1.md`; `step10/s10_analysis.py`.
- **Current rule:** pilot: SF-first, UNP over all calls, FAIL-U over FAIL-S (12.18). Main run: §18.2 as written, SF kept in `n_calls`, SF count and rate reported beside four proportions, no rescaling (12.26).
- **Recommendation:** keep the interim rule for the pilot and the main run; do not adopt Policy 1 (it contradicts §12 "over all R calls" and leaves cluster means undefined); consider Policy 2 only if the advisor wants "sums to 1", adopted before the FZ hash. **Consistency:** keep = consistent; Policy 2 / Policy 1 / parse-first = protocol change (§18.2, §22 item 6, §12, §13.4).
- **Alternatives:** literal text (overlap undefined), Policy 1, Policy 2, parse-first (contradicts 12.18 row 1).
- **Impact:** validity: no denominator is changed under the interim rule, nothing is hidden; cost: Policy 2 needs a call ledger and an amendment; reproducibility: the analysis code is fixed; ledger: unaffected; analysis: `s10_analysis` already implements the interim rule; gate: not a pilot gate, but it is in the FZ hash (§13.2), so it must be settled before it.
- Owner/advisor decision: PENDING

## 4. D4 — Primary SF when several flags occur   `PROPOSED — NOT ADOPTED`
- **Sources:** spec §13.4 (no order), §13.6 (outcome by "any SF2, SF3 or SF5", `SF1 + SF4 <= f_S`); Policy 2 package §4.4-4.5, D-4, D-5; `step10/s10_scoring.py` `PRIMARY_ORDER`, `sf_flags`, `pilot_counts`; record 12.30; `s7_decision.round_outcome`.
- **Current rule:** all flags are computed; one provisional primary type (SF1 > SF4 > SF3 > SF2 > SF5) builds the disjoint count vector.
- **Finding:** because §13.6 speaks of the definitions met, a call that meets SF3 or SF2 must make the round FAIL-S whatever its primary type. With the provisional order an incoherent record carrying SF1 and SF3 is counted as SF1 and could pass.
- **Recommendation:** (a) decide the pilot outcome from the flag sets (any hard flag SF2/SF3/SF5 → FAIL-S; soft count per call), use the primary order only for the per-type table, and report the number of multi-flag calls. This is a clarification of how counts are formed from §13.6, not a new threshold. **Alternatives:** (b) freeze an exclusive order with hard flags first; (c) keep the current order. **Impact:** validity: (a) cannot hide a hard failure; cost: a small code change and tests after adoption; reproducibility: deterministic; ledger: unchanged (flags are already in the `classified` entry); analysis: per-type table unchanged; gate: none.
- **Also open (Policy 2 D-5):** whether `SF1 + SF4 <= f_S` counts calls or flags (PJR J-10 reads it as calls).
- Owner/advisor decision: PENDING

## 5. D5 — Re-code values and the departures from §16.3   `PROPOSED — NOT ADOPTED`
- **Sources:** spec §16.3 (997-1003); OD-3 (`research_design/STEP2_OWNER_DECISIONS_RECORD.md`, lines 39-48); record 12.21 row 6, 12.24 decision 2, 12.26 item 3; codebook revision 5 section 5.3; `step7/s7_recode.py` lines 30-32; P-3 item 3.
- **Current rule:** 20 % sample (floor 20), 14 days, `recode1_*`, raw agreement, no kappa; every table states "single coder, intra-rater only".
- **Recommendation:** approve the values with the advisor's explicit sign-off and record each departure as a clarification of silence (sample, delay, concealment, column name). Treat kappa separately: either "not computed" (current) or "computed and labelled intra-rater consistency, no reliability claim"; the second reading satisfies §16.3 line 1002 and OD-3 (which forbids claims) at once but contradicts 12.24/12.21 as written. **Consistency:** sample, delay, columns = clarification; kappa omission = departs from the literal text. **Alternatives:** re-code every coded response; other values.
- **Impact:** validity: weaker evidence of intra-rater consistency with a sample; cost: re-coding everything is workload; reproducibility: selection is hash-based and deterministic; ledger: none; analysis: tables use raw agreement; gate: not a pilot gate; the codebook is an FZ item so decide before the FZ hash.
- Owner/advisor decision: PENDING

## 6. D6 — Which responses are coded   `PROPOSED — NOT ADOPTED`
- **Sources:** spec §16 ("only parseable responses"), TH16 (line 1161), §13.6.1 activity C; Policy 2 package §7, D-10; record 12.31; `step10/s12_coding.py`.
- **Current rule (provisional):** non-SF calls with a parseable verdict.
- **Recommendation:** keep it; report beside the tables the counts of UNP, SF and, as a diagnostic, SF3 calls that carried a verdict. **Consistency:** clarifies "parseable" consistently with SF-first. **Alternatives:** SF3-partial as a separate stratum; all calls with a parseable verdict (contradicts SF-first).
- **Impact:** validity: avoids coding truncated comments; analysis: D_P per condition reported (TH16); gate: none; reproducibility: deterministic.
- Owner/advisor decision: PENDING

## 7. D7 — PRD-5: unit-token normalization   `PROPOSED — NOT ADOPTED`
- **Sources:** spec §11.2 step 3 (line 699), §19.3 (line 1131); `step9/s9_blindcheck.py` `UNITS`.
- **Current rule:** the field-specific sets printed in §11.2 step 3.
- **Recommendation:** adopt the printed sets (a subset of the older global list; foreign units are not absorbed). **Consistency:** consistent with the text, closes a pending flag. **Alternative:** the older global list (not v2.7 text). **Impact:** a foreign unit yields CHECKER ERROR (transcription), logged, member kept; no effect on the registry or the primary analysis; gate: affects the evaluation of the blind check, which should therefore not start before the decision.
- Owner/advisor decision: PENDING

## 8-11. Q-P1 to Q-P4 — provider response handling   `PROPOSED — NOT ADOPTED`
Sources: spec FZ-v1 row 17 / §17 row 17 ("record the returned model ID"), §13.4 SF1-SF5, §13.6, §13.8; `PROVIDER_RESPONSE_VALIDATION_REPORT.md`; record 12.36; `step10/s10_scoring.py`, `s10_runner.py`, `s10_integrity.py`.
- **Q-P1 returned model differs.** Rule: record only. Recommendation: record, flag in the pilot report, and treat a difference observed in the first live observation as a **safe stop for owner review** before the next call/round, not an automatic rule, because model identity affects what the data mean and the registry says deprecated IDs may be routed. What "differs" means (suffix, alias) cannot be decided without seeing a real value (LV). Alternatives: record only; automatic stop. Impact: validity: protects against silent model substitution; cost: at most one interrupted round; ledger: a stop leaves a run without a status marker unless a stop path is built; analysis: reported. Classification: CN, LV; an automatic stop would be a PCA.
- **Q-P2 unlisted finish reason.** Rule: silent. Recommendation: do not classify by name; treat an unlisted non-STOP reason as a **safe stop for owner review** (the response is kept as recorded, not replaced), and add a stop path before any live run if the owner agrees. Alternatives: parse decides (current, reported), structural failure. Impact: avoids scoring a possibly unusable response as valid; cost: needs a small stop mechanism and tests after adoption.
- **Q-P3 which names mean blocked.** Rule: "safety/blocked finish reason or no candidate" (§13.4). Recommendation: restrict the list to the names whose meaning is a block (SAFETY, BLOCKLIST, PROHIBITED_CONTENT, SPII, IMAGE_SAFETY) and move RECITATION, OTHER, LANGUAGE to "unlisted" (Q-P2), without widening by name. This changes the current code list (a failure-classified call becomes a stop-for-review) and contradicts D8 of the earlier brief. Alternative: keep. Impact: gate/pilot counts: a call with those reasons would no longer be an automatic SF4.
- **Q-P4 no HTTP status and no error.** Rule: silent. Recommendation: fail closed (SF1) once the live adapter is known to always set the status; until then keep reporting. Alternative: keep current. Impact: removes a path to a silent success.
- Owner/advisor decision (Q-P1..Q-P4): PENDING

## 12. Timeout 180 s   `PROPOSED — NOT ADOPTED`
- **Sources:** FZ-v1 row 17 (`timeout_s` 180), §17 row 17; `step10/s10_runner.py` `TIMEOUT_SEMANTICS`, `GeminiProvider.generate`; `PRE_PILOT_FIX_REPORT.md` section 1.
- **Current rule:** per-socket-operation timeout; no total deadline; latency recorded; calls above 180 s flagged afterwards.
- **Recommendation:** keep behaviour for the pilot and record the meaning in the decision record; decide a total deadline only if the first live observation shows a stalled response. **Consistency:** consistent with the text, which does not define "timeout". **Alternative:** total wall-clock deadline of 180 s (implementable with a worker thread; a deadline hit is SF1, never retried). **Impact:** a total deadline would change which calls fail; changing a frozen setting's behaviour after the FZ hash is a new FZ version (§13.6). Decide before the FZ hash.
- Owner/advisor decision: PENDING

## 13. Resume after a transport halt   `PROPOSED — NOT ADOPTED`
- **Sources:** spec §13.8 (871-875); `PRE_PILOT_FIX_REPORT.md` section 4 (five questions); `step10/s10_runner.py` (existing folder refused).
- **Rule:** may resume under the identical FZ version at the next `call_index`; no completed call replaced, no failed call re-run.
- **Recommendation:** no resume tool until written answers exist. Proposed answers for review: (1) counters carry over (a reset is a new rule); (2) an intent without a raw record stays "attempted, no record", is never repeated and is reported; (3) "transport-only" means every call in the current consecutive-failure run is SF1; (4) the owner records a resume event and a new authorization for the remaining call count; (5) no delay beyond the frozen 1 s. With carry-over the run may halt again at once, which is the safe outcome. **Consistency:** (1)-(3) clarify; a reset would be a PCA. Impact: ledger: a resume entry appended to the same hash chain; cost: remaining calls only; gate: needs authorization; reproducibility: deterministic order.
- Owner/advisor decision: PENDING

## 14. PRD-6 — anchoring of the decision record   `PROPOSED — NOT ADOPTED`
- **Sources:** spec §10 (line 662: committed as its own commit, with the commit ID recorded in the final freeze manifest and run manifests, "or, if version control is unavailable, deposited in an equivalent write-once or timestamped store declared at step 6"), §19.3 (line 1132); record 12.23 table; FZ-v1 declares no store; `research_design/` is untracked.
- **Recommendation:** the owner declares in writing which store is used before the decision script is run: preferred is a version-control commit of the decision record alone (the repository exists; only the owner can authorize a commit), alternative an external timestamped copy of its SHA-256. The runner must abort if the anchor cannot be verified (§10); that check is not yet implemented. **Consistency:** the missing step-6 declaration is a gap to be recorded, not a change. Impact: validity of the seed rule (nobody can re-run the script to choose a date); reproducibility high; gate: needed before step 11, not before the pilot rounds.
- Owner/advisor decision: PENDING

## 15. P-2 — FZ hash contract   `PROPOSED — NOT ADOPTED`
- **Sources:** spec §10 (record contains "the FZ hash"), §13.2 line 797 (FZ hashed before the first pilot call), §21.1 row 11; record 12.21 row 7; `PROPOSED_CLARIFICATIONS...` P-2; `step7/s7_decision.py` (records the value as researcher-supplied, unverified); `step10/s11_final_freeze_manifest.py`.
- **Recommendation:** adopt a versioned contract: an index object of file hashes of the FZ items **excluding** the decision record, canonical JSON, SHA-256 of its bytes, verified by recomputation, taken before the pilot; the final freeze manifest of row 11 stays a later object that includes the record. This needs a small new tool (NOT_STARTED) and a decision-script input check. **Consistency:** clarification of an undefined object; it does not redefine the FZ-v1 register hash. **Alternative:** accept "researcher-supplied, unverified" in writing. Impact: verification of the freeze; reproducibility; no effect on the pilot outcome.
- Owner/advisor decision: PENDING

## 16. OD-10 / P-4 — input size and cost   `PROPOSED — NOT ADOPTED`
- **Sources:** record 12.11 OD-9/OD-10 (lines 401-402), 12.18 row 6 (line 511), 12.21 row 8; P-4; FZ-v1 `cost_estimate_conditional`; PJR J-9; `step10/s10_runner.py` `hard_cap_cost_usd`, `s10_integrity.py`.
- **Facts (recomputed):** hard cap US$51.88 (2,496 slots) or US$52.63 (2,532) with 1,016 tokens assumed; break-even input about 63,381 tokens per call; recorded Stage 1/2 prompts ran 2.91-3.10 characters per token (a different model).
- **Recommendation:** before the first paid call the owner either re-accepts the character bound in writing for the pilot (the cap is far below the limit) or authorizes one token-count request on the final prompts; re-read prices on the day (J-9); keep the authorization's `input_tokens_per_call_assumed` honest. **Conflict:** see 0.1 item 1. **Alternative:** measure with the provider's count method (an external call). Impact: cost assurance only; no protocol change if the owner states the basis; LV for the measurement.
- Owner/advisor decision: PENDING

## 17-20. Remaining open items   `PROPOSED — NOT ADOPTED`
- **PC-2** (spec line 1136; 12.23 table; 12.28): recommendation: confirm the reading "informational at step 4, hard at step 8" already applied. CN.
- **I-6** (spec line 670; 12.23; 12.28): the check is undefined and §3.7 fixes the gate counts at 30 and 14; recommendation: confirm it as an informational diagnostic (0 failures in the build report) and not a gate. A gate would change gate counts (PCA).
- **P-3** (four items): (1) `s2_values` "none" outside its denominator: report as a count outside the denominator (open); (2) MX = MPG (applied, 12.18 row 13); (3) kappa (see item 5 and conflict 2); (4) SF versus UNP (item 3). Recommendation: record items 1 and 3 explicitly.
- **F-3** (12.23): the Step 8 build reads values from the frozen register and gates A5/Q9 relate members to it; recommendation: close as technically satisfied. **PRD-8** (spec 1133): not applicable under DP1/OD-4; recommendation: leave as recorded. **Round-1 FAIL-S action and the multi-type case** (12.18 row 5; spec §13.6): researcher decision when it occurs, logged. **P-5** (codebook rehearsal): human task, pre-pilot (§13.5).
- Owner/advisor decision: PENDING
