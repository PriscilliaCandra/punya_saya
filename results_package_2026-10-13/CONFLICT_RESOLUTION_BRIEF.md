# Conflict resolution brief (PROPOSED — NOT ADOPTED)

Prepared 2026-10-13 for the owner and the advisor. Analysis only: no protocol, record, manifest, registry, code or historical result was changed. Every recommendation is `PROPOSED — NOT ADOPTED`. Paths are relative to `D:\research s2\research_design\` unless stated; "spec" = `SCENARIO_CONSTRUCTION_SPECIFICATION_v2_7_DRAFT.md`; "record" = `STEP3_OWNER_DECISIONS_RECORD_DRAFT.md`. Where a source cannot be pinned down the text says UNRESOLVED.

Change classes used for options: **RECORD ONLY** (an owner clarification entry in the record, like PC-1/12.16), **PROTOCOL** (needs a new methodology version, spec §13.2/§21.2), **CODE** (source change and tests after adoption), **EXTERNAL CALL** (needs separate written authorization).

---
## 1. OD-10 — input size

### CURRENT RULE
- Record 12.11, line 402: "US$100 is the operational cost limit for this FZ version. Cost estimates before the final prompt are conditional, not a guarantee. At Step 7 `I_max` is measured on the actual prompt and the estimate recomputed with official prices and all planned calls. If the estimate exceeds US$100, or the limit cannot be adequately assured, stop before any paid API call and ask the owner; do not reduce calls, change the model or change parameters silently." The same decision is carried in `PARAMETER_FREEZE_MANIFEST_FZ_v1.json` line 21 (`owner_decisions.OD-10`) and `cost_estimate_conditional` (line 173: "I_max assumed 1,000-2,000 tokens (prompt does not exist until Step 7) ... recompute at Step 7").
- Record 12.18 row 6, line 511: "The owner accepts the **character bound** as the Step 7 input-size bound: 1016 characters (worst case ...), assuming a token covers at least one character. Hard cap US$52.63 including the 36 pilot slots. ... This replaces, for Step 7, the clause of 12.11 'I_max is measured on the actual prompt'. It is an assumption, not a measurement; the tokenizer was not queried. The US$100 limit of OD-10 is unchanged. If any prompt text changes, the bound is recomputed (a test checks it)."
- Record 12.21 row 8, line 604: "No measured `I_max` exists ... Pending authorization. Requires an external call." Proposal P-4: `step7/PROPOSED_CLARIFICATIONS_AND_AMENDMENTS_DRAFT_v1.md` line 77 ff. ("Character count is not evidence of token adequacy").
- The specification itself contains no OD-10 and no `I_max` (searched: no match). OD-8 to OD-10 exist only in the record (12.11) and the FZ-v1 manifest. The spec's relevant Step 7 text is §21.1 row 7 (line 1186), which has no cost clause, and §13.2 (change of a frozen setting is a new FZ version).
- Code: `step10/s10_runner.py` `hard_cap_cost_usd` and `check_gates` (authorization must state `input_tokens_per_call_assumed`; hard-cap cost must be below 100); `step7/test_step7.py` `test_od10_character_bound_still_holds_for_the_current_texts` (878 and 1,016 characters, US$51.88 / 52.63).

### CONFLICT
Two different things are called "the input size": (a) the Step 7 bound, accepted by the owner "for Step 7" as a substitute for measurement; (b) the input size on the paid calls, for which 12.11 requires "adequate assurance" before "any paid API call". No entry says whether (a) also serves as (b). Step 7 is now frozen on the owner's instruction, so the "Step 7" in 12.11 and 12.18 has passed without a measurement and without a statement about paid calls. Whether "Step 7" in 12.11 means the freeze step or "before the first paid call" is UNRESOLVED (the wording "At Step 7 ... the actual prompt" can only be met after prompts exist, i.e. after Step 8).

### FACTS (recomputed, no new data)
Hard cap, all calls at 8,192 output tokens, retries 0, prices USD 0.30 / 2.50 per 1M (read 2026-10-12, FZ-v1 `model_verification`, not re-verified): US$51.12 for output alone (2,496 slots); US$51.88 with 1,016 input tokens; US$52.63 for 2,532 slots. The limit is reached only at about 63,381 input tokens per call (2,532 slots) or 65,280 (2,496 slots), roughly 60 times the bound; the cost ceiling is far more sensitive to the output price (a factor of about 1.9) than to the input size. Observed on other prompts and another model: 2.91-3.10 characters per token over 70 calls (`results_package.../03_EXPERIMENTAL_RESULTS.md` section 1). This is not a measurement on the v2.7 prompts or model.

### OPTIONS
| Option | What it says | Class | Cost and method |
|---|---|---|---|
| O1 | The owner states in a new record entry that the 12.18 character bound is also accepted as the basis for the paid calls of the pilot (and the main run) | RECORD ONLY | no cost; cost assurance rests on the headroom above; the assumption "a token covers at least one character" stays unverified |
| O2 | Count tokens of every final prompt with the provider's count method before the first paid call (1,248 + 96 prompts, one user turn, no system prompt, model `gemini-3.5-flash-lite`) | EXTERNAL CALL (needs authorization; this document does not claim the method's cost or exact name) | meets 12.11 literally; first live contact with the provider; the count response is metadata, not model output |
| O3 | Keep the bound but require the basis to be written in each run authorization (`input_tokens_per_call_assumed`, as the runner already requires) and re-accepted per round | RECORD ONLY | a per-round decision; consistent with the runner |
| O4 | After pilot round 1 take the recorded `promptTokenCount` of the 18 pilot calls as a first measurement and re-check before the main run | RECORD ONLY (use of recorded metadata) | covers only the 24 pilot templates, not all 1,248 main prompts; a supplement, not a substitute |
| O5 | Change the limit or the model | PROTOCOL (new FZ version; changes a frozen setting) | not recommended; not needed given the headroom |

### RECOMMENDATION (PROPOSED — NOT ADOPTED)
For the pilot: O1 limited in time to the pilot rounds, applied through O3, with the owner writing the basis in the authorization; for the main run: require O2 or the O4 check against all 1,248 prompts before the call that exceeds the pilot, because the main run is 138 times larger than a pilot round. None needs a protocol change. Reason: the arithmetic shows the US$100 limit is not threatened by the input size, so the open point is the correctness of the stated basis, not the budget.
### OWNER/ADVISOR DECISION: PENDING

---
## 2. Cohen's kappa

### CURRENT RULE (verbatim, in source order)
1. Spec §16.3, line 1002 (bullet in the list "Coders, reconciliation, preservation"): "Agreement is reported per variable (percent agreement and Cohen's κ)."
2. Spec §16.3, line 1003, next bullet: "**If no second human coder exists:** a delayed intra-rater re-code on an order scrambled by opaque ID (limitation: no inter-rater reliability). A model coder may be added only as a screening comparison, never as the reconciling authority and never described as inter-rater reliability."
3. OD-3, `STEP2_OWNER_DECISIONS_RECORD.md` line 45 (2026-10-09, "Owner decision recorded. Not a specification amendment"): "S2/S3 coding follows the delayed intra-rater re-code ... **No inter-rater reliability and no Cohen's κ may be claimed.**"
4. Record §5 (blind check), line 134: "No inter-rater reliability and no Cohen's κ may be claimed" (about the blind check).
5. Record 12.21 row 6, line 602 (DELEGATED): "16.3 also says that agreement is reported with Cohen's kappa; that sentence is read as applying to two coders, and OD-3 (no kappa for one coder) governs the single-coder case." Record 12.24 decision 2 (line ~689-691): "per-variable raw agreement and full cross-tables ... no Cohen's kappa ..."; "16.3 says agreement is reported with Cohen's kappa; OD-3 governs." `PROPOSED_CLARIFICATIONS...` P-3 item 3 (lines 72-73): "Applied: raw agreement only; kappa is not reported or claimed (12.21 row 6)." Codebook revision 5 lines 49, 196, 202, 213.
6. Code: `step7/s7_recode.py` `agreement_table` (line 104 ff.) returns raw counts, percentage and cross-table; no kappa anywhere.

### CONFLICT — classification
Not a direct contradiction between OD-3 and §16.3: they differ in **verb and scope**. §16.3 line 1002 says kappa is *reported* (general, two-coder wording); OD-3 says kappa may not be *claimed* (for the single-coder case). A kappa can be computed and shown with an explicit "not a reliability claim" label without violating OD-3, or omitted without violating line 1003. The real problem is a **sequence/authority gap**: the reading "line 1002 applies to two coders only" was made by the delegated assistant (12.21 row 6, labelled DELEGATED and "subject to the owner's and the advisor's review"), and the stronger statement "no kappa is reported" (P-3, 12.24) goes beyond OD-3's words ("claimed"). No owner entry decides between "computed with a label" and "not computed". UNRESOLVED: whether the owner's message that fixed 12.24 meant "not computed" or "not claimed" (the record says only "no kappa").
Also relevant: whether kappa is meaningful for an intra-rater re-code of 20 % samples with several categories (many cells small); that is a statistical question for the advisor.

### OPTIONS
| Option | What is reported | Class | Consequence for reliability reporting |
|---|---|---|---|
| K1 | Raw agreement and cross-tables only; kappa neither computed nor shown (current implementation) | RECORD ONLY (decides the reading of line 1002) | no chance-corrected figure; a reader cannot judge agreement beyond raw counts; departs from the literal line 1002 |
| K2 | Also compute kappa per variable (with the cross-table) and print it with the label "intra-rater consistency; no inter-rater reliability claim" | RECORD ONLY + CODE (add kappa to `agreement_table`, tests, codebook 5.1/5.3 wording) | satisfies line 1002 and OD-3 together; kappa is unstable for small or skewed tables and can be undefined (all one category) — rules for that case would be needed |
| K3 | Report kappa only for variables where each category has at least a stated number of items; otherwise raw only | RECORD ONLY + CODE | a threshold that is not in the protocol must be chosen and justified |
| K4 | Amend §16.3 to remove the kappa phrase | PROTOCOL | only needed if the advisor wants the text to match K1 |

### RECOMMENDATION (PROPOSED — NOT ADOPTED)
K2 with an explicit rule for undefined or unstable cases (report "undefined" with the counts), because it needs no protocol change, satisfies both texts, and gives the reader more information; K1 if the advisor judges kappa unsuitable for this design. Since the codebook is an FZ item and the FZ hash precedes the first pilot call (spec §13.2 line 797), the decision is needed before the FZ hash; it does not change any pilot call.
### OWNER/ADVISOR DECISION: PENDING

---
## 3. FZ hash

### CURRENT RULE
- Spec §10, line 662: before any order is generated "a **decision record** is written and hashed containing: the pilot structural counts ..., the FZ hash, the decision-script hash, the script-stamped UTC timestamp, the computed seed integer, the interpreter version, and the SHA-256 and length of the canonical call list"; the record is serialized as canonical JSON, then "**anchored** (PENDING RESEARCHER DECISION PRD-6) in a write-once way ... the commit ID is recorded in the final freeze manifest and in every run manifest"; "the runner recomputes the record hash and aborts if it differs from the anchored hash".
- Spec §13.2, line 797: "FZ — the freeze set (hashed before the first pilot call)": generator code, parameter register, texts, parser grammar, reference checker, codebooks, "execution-order algorithm, seed rule and decision script; pilot parameter set; the main registry and its hashes".
- Spec §21.1 row 11, line 1190: "decision record written and hashed (§10); order seed and bootstrap seed taken from it (DP9); **final freeze manifest hashed**." Row 6 (parameter freeze) hashes the register.
- No spec text defines the object called "the FZ hash". Record 12.21 row 7, line 603 (DELEGATED, proposal only): the specification does not define it; proposal P-2 (`PROPOSED_CLARIFICATIONS...` line 42 ff.): a versioned `FZ_INDEX` object of item hashes, canonical JSON, final LF, self-reference excluded, verification by recomputation; not adopted. Meanwhile `step7/s7_decision.py` lines 163-176 requires 64 hex characters and stores `"fz_hash_provenance": "researcher-supplied, unverified: no FZ hash contract is adopted (proposal P-2)"`.
- `step10/s11_final_freeze_manifest.py` (lines 15-27) builds a "final freeze manifest" that contains `decision_record_sha256` and file hashes (spec, FZ-v1, Step 7 freeze manifest and files, Step 8 manifest, Implementation A and B, Step 10 code).

### DEPENDENCY MAP (what hashes what)
```
FZ items (spec, FZ-v1 register, Step 7 freeze set, Step 8 registry/prompts/manifest, pilot parameter set, decision script)
      │ hashed BEFORE the first pilot call (13.2)  ──►  H_FZ  (object undefined)
pilot rounds ──► counts
decision script( counts, H_FZ, timestamp, seed, call list hash, script hash ) ──► decision record R  (contains H_FZ)
R ──► anchor (PRD-6: commit ID, or external timestamp)
M_final (21.1 row 11)  = hashes of FZ items + hash of R  (+ anchor ID, recorded in every run manifest)
runner (main run): recomputes hash(R), compares with the anchor, aborts on a mismatch
```
### WHY A CYCLE APPEARS
It appears only if H_FZ is taken to be the hash of M_final (the "final freeze manifest"): M_final contains hash(R), R contains H_FZ, so H_FZ = hash(M_final) = hash(… hash(R(H_FZ)) …). The tool in `s11_final_freeze_manifest.py` makes that reading tempting because its output contains the record hash. Time order confirms it cannot be the FZ hash of §10: FZ is hashed before the first pilot call (13.2), while R and M_final exist only after the last pilot round (21.1 rows 10-11). So H_FZ must be computed from objects that exist earlier and must not include R. The spec's phrase "final freeze manifest hashed" at row 11 is a later, different object.

### DESIGNS
| Design | What is hashed | Excluded | Integrity check |
|---|---|---|---|
| **A. FZ index (P-2)** | canonical JSON of {file path → SHA-256} for every FZ item file (spec, FZ-v1 file, Step 7 freeze manifest and its 11 files, Step 8 `manifest.json` and the registry/prompt tables it lists, `s7_decision.py`, Implementation A, pilot parameter set inside FZ-v1); H_FZ = SHA-256 of the index bytes | decision record R, run folders, Step 10 harness (harness changes only by H1-H4, 13.2), results | recompute the index from the files and compare with the H_FZ in R; M_final later adds R and the anchor |
| **B. Chain of existing manifest hashes** | canonical JSON of {spec_sha256, fz_v1_register_sha256, step7_freeze_manifest_sha256, step8_manifest_sha256}; H_FZ = SHA-256 of it. Each of those manifests already lists the hashes of its files | the files not covered by those manifests (decision script is covered by the Step 7 freeze set; Implementation A/B are not) | recompute the four hashes and the object; deeper checks via the manifests; smaller object, coarser, relies on the manifests being complete (the 11-file Step 7 set, the 624-file Step 8 inventory) |
| **C. Two explicit objects** | H_FZ as in A or B, and M_final as a separate object that references H_FZ and hash(R) (the `s11` tool) | M_final is never an input to R | R carries H_FZ; M_final carries both; the runner checks hash(R) against the anchor and H_FZ against a recomputation |
| **D. Status quo** | nothing verified: R records a researcher-supplied 64-hex value | everything | none by tool; the supplied value is a declaration |
Acyclicity: A, B and C are acyclic because H_FZ never depends on R. D is acyclic but unverifiable. UNRESOLVED: spec says the FZ is "hashed" (13.2) but not whether a single hash or a list is meant, and the FZ-v1 manifest hashes only the register (its `register_canonical_sha256`).

Observation about the current runner: no gate checks that an FZ hash exists or equals a recomputation; the pilot gate checks Step 9 evidence, authorization, verifier and Implementation B. So §13.2's "hashed before the first pilot call" is not enforced by code. (Adding such a check would be CODE after adoption.)

### CLASS AND RECOMMENDATION (PROPOSED — NOT ADOPTED)
A or B or C: RECORD ONLY (clarifying an undefined object, no change of FZ-v1) plus CODE (a small tool that writes the index and a check in the decision script or gate). D: RECORD ONLY (an explicit acceptance). Recommended: C built on A, with the index computed and recorded before pilot round 1, so that the object exists when the record is written; reason: it matches the time order of §13.2, §10 and §21.1, needs no format change of any frozen artefact, and keeps verification by recomputation. Do not change `s11_final_freeze_manifest.py` until the design is chosen.
### OWNER/ADVISOR DECISION: PENDING

---
## 4. SF flags and `pilot_counts`
> **Status note (2026-10-13, added later):** this section describes the SF counting BEFORE patch P1. Since then the code applies the working technical decision MD-01 (hard flags -> FAIL-S, one decision count per call; not ratified) and the SF2-with-SF1/SF4 question is analysed in `C31_C32_OWNER_DECISION_BRIEF.md`. Read the case tables below as the earlier state.


### CURRENT RULE (sources)
- Spec §13.4, lines 807-814: SF1 transport failure (HTTP/API error or timeout); SF2 empty response; SF3 truncation (finish reason at the output-token limit); SF4 provider block (safety/blocked finish reason or no candidate); SF5 harness exception on a non-empty response. Line 816: "Structural failures are SF1-SF5. An individual UNP is never a pilot failure."
- Spec §13.6, lines 828-834: `PASS`: "no SF2, no SF3, no SF5; `SF1 + SF4 ≤ f_S`; UNP share ≤ θ_unp"; `FAIL-S`: "any SF2, SF3, SF5, or `SF1 + SF4 > f_S`"; `FAIL-U`: UNP share > θ_unp. §13.7, line 869: the pilot analysis reports "SF1-SF5 counts, UNP share, latency and token usage".
- Record 12.18 row 1 (line 506): the UNP share is UNP / all calls; "A call classified under SF1 to SF5 is not counted as UNP (the counts of SF1..SF5 and UNP are disjoint)". Row 2: FAIL-U takes precedence. PJR J-10 (line 140): "`f_S` = 1 tolerates one transport or block failure in 18 calls".
- Record 12.36 (line 793): a record with an error marker or an HTTP status outside 2xx is SF1, a prompt block reason is SF4; unlisted finish reasons and missing usage are counted and reported.
- `step10/s10_scoring.py`: `sf_flags` computes all flags (lines 46-63) and returns them in `PRIMARY_ORDER = (SF1, SF4, SF3, SF2, SF5)` (line 20); `classify` sets `primary_sf` to the first flag (line 66 ff.); `pilot_counts` increments exactly one counter per SF call (`c[cl["primary_sf"]] += 1`, line 92) and counts calls with several flags in `multi_flag_calls` (line 93). `step10/s11_pilot.py` `report` (lines 34-40) passes `pc["counts"]` to `round_outcome`. `step7/s7_decision.py` `round_outcome` (lines 75-80): `hard = SF2 + SF3 + SF5`, `soft = SF1 + SF4`, `fail_s = hard > 0 or soft > f_S`.

### THREE THINGS KEPT APART
(1) **All detected flags** — `sf_flags`, stored per call in the ledger `classified` event (`flags`). (2) **Primary classification for the record** — first flag in `PRIMARY_ORDER`; the order is provisional and appears in no source text (12.30; Policy 2 package §4.5). (3) **Counts used for the pilot decision** — currently the primary-type vector, so decision = f(primary types), not f(flag sets). §13.6 is written on (1) ("any SF2, SF3, SF5"), and 12.18 row 1 asks the counts to be disjoint, which a flag-set reading cannot satisfy for a multi-flag call without choosing which count it enters.

### CASE TABLE (flags from `sf_flags` as written; "current" = primary order SF1>SF4>SF3>SF2>SF5)
| # | Record | Flags | Primary (current) | Counts (current) | §13.6 literal (flag sets) | Differs? |
|---|---|---|---|---|---|---|
| 1 | HTTP 200, STOP, empty text | SF2 | SF2 | hard +1 | hard | no |
| 2 | HTTP 503, error, no text | SF1 | SF1 | soft +1 | soft | no |
| 3 | 200, MAX_TOKENS, text with a verdict | SF3 | SF3 | hard +1 | hard | no |
| 4 | 200, MAX_TOKENS, empty text | SF3, SF2 | SF3 | hard +1 | hard (two definitions) | no outcome change |
| 5 | 200, SAFETY, partial text | SF4 | SF4 | soft +1 | soft | no |
| 6 | 200, no candidate, no text | SF4 | SF4 | soft +1 | soft | no |
| 7 | error marker plus text (contradictory) | SF1 | SF1 | soft +1 | soft | no |
| 8 | error marker plus text, finish MAX_TOKENS | SF1, SF3 | SF1 | soft +1 (hard SF3 not counted) | hard (SF3 met) | **yes: can PASS with f_S = 1** |
| 9 | prompt block reason, finish MAX_TOKENS | SF4, SF3 | SF4 | soft +1 | hard | **yes** |
| 10 | error marker plus text, parser exception | SF1, SF5 | SF1 | soft +1 | hard (SF5 met) | **yes** |
| 11 | prompt block reason plus text, parser exception | SF4, SF5 | SF4 | soft +1 | hard | **yes** |
| 12 | error marker plus prompt block | SF1, SF4 | SF1 | soft +1 | soft: 1 per call, 2 per flag | **yes if flags are counted** (`1 + 1 = 2 > f_S`) |
Reachability: with the adapter as written, an HTTP error or exception yields text "" and no finish reason (SF1 only); a normal response has no error marker. Rows 8-11 need a payload the adapter does not produce today (for example a prompt block together with candidates, or a hand-made record). So today's real risk is low, but the 12.36 fail-closed rule does **not** prevent the bypass: it adds a flag SF1 or SF4 that, being first in the order, can mask a hard flag. Tests: `test_provider_response.py` checks the single-flag rows only; no test covers rows 8-12 (UNRESOLVED whether anyone intended those combinations to be reachable; they are reachable by construction of `sf_flags`).

### OPTIONS
| Option | Pilot decision input | Class | Consequence |
|---|---|---|---|
| S1 | Keep the primary-type vector (current) | none | rows 8-11 can hide a hard failure; the pilot could PASS where the literal text says FAIL-S |
| S2 | Hard-first primary order (SF3, SF2, SF5, then SF1, SF4) so that a hard flag always decides the type; soft counted per call | CODE (constant `PRIMARY_ORDER`, tests) + RECORD ONLY | keeps disjoint counts and `round_outcome` unchanged; rows 8-11 become FAIL-S; row 12 stays soft once (per call) |
| S3 | Compute the decision from the flag sets: `hard_calls` = calls with any of SF2/SF3/SF5; `soft_calls` = other SF calls; pass these as the SF counts; keep the per-type table by order | CODE (`pilot_counts`, tests; `round_outcome` unchanged if the vector stays disjoint) | decision follows §13.6 wording exactly; per-type table can sum to more than the failure total (must be labelled) |
| S4 | Count `SF1 + SF4` per flag | CODE; changes the counting convention of `f_S` | row 12 fails the round; conflicts with PJR J-10 ("one transport or block failure in 18 calls" reads per call) — PROTOCOL if it changes the meaning of `f_S` |
| S5 | Refuse to classify a multi-flag call: stop for owner review | CODE; adds a stop path that does not exist | safest for contradictory records; costs a round in the rare case |
The pilot outcome of real runs can change between options only when rows 8-12 occur; for single-flag responses all options agree. Do not assume the outcome is unchanged: it changes in exactly those rows.

### RECOMMENDATION (PROPOSED — NOT ADOPTED)
S3 (equivalently S2 plus a note), with per-call counting of `SF1 + SF4` as in PJR J-10, and S5 as the handling of any call with a hard flag together with SF1/SF4 until the owner has seen a live example. Reason: §13.6 is stated on the definitions met, 12.18 asks for disjoint counts, and S3 satisfies both; nothing needs a protocol change. Record the number of multi-flag calls in every pilot report (already done).
### OWNER/ADVISOR DECISION: PENDING

---
## 5. Minimum decisions

### Before the pilot (before the first pilot call)
1. **SF counting convention (section 4, S1-S5) and per-call versus per-flag `f_S`**: the pilot outcome depends on it in rows 8-12.
2. **OD-10 basis for the paid pilot calls (section 1, O1/O3 or O2)**: written in the authorization, no run without it.
3. **The decisions already listed as pre-pilot in `ADVISOR_DECISION_BRIEF.md`**: D1 (PG3), D7 (PRD-5, before the blind check is evaluated), Q-P1 to Q-P4 (provider responses), and the owner's written authorization and the Step 9 evidence (human tasks).
4. **Because FZ is hashed before the first pilot call (spec 13.2 line 797):** the decisions listed in the next block are pre-pilot in practice, even though no runner gate checks them.

### Before the FZ hash (which precedes the first pilot call, spec 13.2)
1. **FZ hash contract (section 3)**: which object H_FZ is, and the tool that computes it.
2. **Kappa and the re-code values (section 2 and D5)**: the codebook is an FZ item.
3. D2 (PG11b scan scope), D3 (SF/UNP policy for §18.2), the timeout meaning (a total deadline would change a frozen setting), and the freeze status of the new harness code (the harness is outside FZ by 13.2, but H1-H4 govern later changes).

### Later (not blocking either hash)
Resume rules (§13.8), PRD-6 anchoring before the decision record is written, token measurement before the main run, coding eligibility before coding.
