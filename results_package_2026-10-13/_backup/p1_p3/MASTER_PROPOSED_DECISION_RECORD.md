# Master proposed decision record (PROPOSED — NOT ADOPTED)

Drafts for review. Nothing here is in `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` (last entry on 2026-10-13: 12.36); numbers are assigned at adoption. Conflict IDs C-xx are defined in `MASTER_CONFLICT_INDEX.md`; analysis in `MASTER_PREPILOT_RESOLUTION.md` (MPR) and `CONFLICT_RESOLUTION_BRIEF.md` (CRB). Shorter earlier drafts exist in `PROPOSED_DECISION_RECORD_ENTRIES.md` (DRAFT-D1 to DRAFT-20); where they differ, this file is the later and more complete draft (differences: SF counting, OD-10 scope, FZ index contract, resume answers, safe-stop policy for provider anomalies, kappa wording). Each entry: `Status: PROPOSED — NOT ADOPTED`; `Class` says whether a record entry suffices or a new methodology version is needed (spec §13.2, §21.2); the last line of each entry is the approval block, left empty.

Approval block (all entries): `Approved by owner: PENDING | Advisor: PENDING | Date: PENDING | Option chosen: PENDING | Edits: PENDING`

---
- **Owner decision: PENDING | Advisor decision: PENDING | Date: PENDING | Option chosen: PENDING**

### MD-01 SF counting for the pilot decision (C-04, C-05)
- **Class:** record entry (counting convention) + code after adoption; no protocol change.
- **Rule quoted:** spec §13.6: PASS needs "no SF2, no SF3, no SF5; SF1 + SF4 <= f_S"; FAIL-S is "any SF2, SF3, SF5, or SF1 + SF4 > f_S". Record 12.18 row 1: SF and UNP counts disjoint.
- **Proposed text:** "All SF flags met by a call are recorded. The pilot round outcome is computed from the flag sets: every call that meets SF2, SF3 or SF5 counts once as a hard failure; every other call that meets SF1 or SF4 counts once as a soft failure; `f_S` is compared with the number of soft-failure calls. The primary type used for the per-type table follows the order ______ and has no role in the outcome. A call that meets a hard flag together with SF1 or SF4 stops the workflow for owner review. The number of multi-flag calls is reported."
- **Reason/impact:** closes the false-pass rows (SF1/SF4 combined with SF3/SF5); per-type table may sum to more than the failure total and is labelled. Code: `s10_scoring.pilot_counts`, tests. Data/analysis/cost: none beyond the stop path. Alternatives: S1 keep, S2 hard-first order, S4 per-flag (changes the meaning of `f_S`: PROTOCOL).
- **Acceptance:** outcomes equal hand-derived values for the full flag-combination matrix; no combination containing SF2/SF3/SF5 passes.

- **Owner decision: PENDING | Advisor decision: PENDING | Date: PENDING | Option chosen: PENDING**

### MD-02 OD-10 scope of the input-size basis (C-01, C-23, C-29)
- **Class:** record entry; measurement option = external call (separate authorization).
- **Rule quoted:** record 12.11 OD-10 (line 402) "At Step 7 `I_max` is measured on the actual prompt ... If ... the limit cannot be adequately assured, stop before any paid API call"; 12.18 row 6 "accepts the character bound as the Step 7 input-size bound ... replaces, for Step 7 ... not a measurement".
- **Proposed text:** "For pilot round(s) ______ the input-size basis is the character bound of 1,016 characters per prompt (largest actual prompt: 1,016), stated in the authorization as `input_tokens_per_call_assumed` = ______. For the main run the basis is ______ (token count of all 1,248 prompts, authorized separately / the maximum `promptTokenCount` of the pilot calls checked against the 1,248 prompt lengths). Prices are re-read on the day of the call. The US$100 limit is unchanged."
- **Impact:** none on the protocol; cost stays at the hard cap (US$0.37 for 18 calls, US$51.88 for 2,496 slots at 1,016 assumed tokens).
- **Acceptance:** authorization states the basis; the gate check (once implemented) refuses an assumption below the longest prompt in characters.

- **Owner decision: PENDING | Advisor decision: PENDING | Date: PENDING | Option chosen: PENDING**

### MD-03 Kappa and the re-code procedure (C-02, C-09)
- **Class:** record entry (K1-K3) / PROTOCOL (K4 amends §16.3).
- **Rule quoted:** spec §16.3 line 1002 "Agreement is reported per variable (percent agreement and Cohen's κ)"; line 1003 single-coder fallback; OD-3 "No inter-rater reliability and no Cohen's κ may be claimed"; 12.21 row 6; 12.24 decision 2.
- **Proposed text (choose one sentence):** (K1) "Agreement is reported as raw agreement and cross-tables; kappa is not computed; this departs from the literal text of line 1002 and is recorded as a departure." (K2) "Agreement is reported as raw agreement and cross-tables and, per variable, Cohen's kappa labelled 'intra-rater consistency; no inter-rater reliability claim'; a variable with a degenerate table reports 'undefined' with its counts." (K3) as K2 for variables meeting ______.
  Values: sample = all responses if at most 20, otherwise max(20, ceil(20 %)); delay at least 14 full days; concealed first-pass codes; columns `recode1_*`. The verbs computed / reported / claimed are stated separately.
- **Acceptance:** codebook section 5.3 and `s7_recode` match the chosen sentence; decided before the FZ hash.

- **Owner decision: PENDING | Advisor decision: PENDING | Date: PENDING | Option chosen: PENDING**

### MD-04 FZ hash contract (C-03, C-18, C-19)
- **Class:** record entry (clarification of an undefined object) + code after adoption.
- **Rule quoted:** spec §10 line 662 (the record contains "the FZ hash"), §13.2 line 797 (FZ "hashed before the first pilot call"), §21.1 row 11 ("final freeze manifest hashed"); record 12.21 row 7.
- **Proposed text:** "The FZ hash is the SHA-256 of the canonical JSON (sorted keys, compact separators, UTF-8, final LF) of the index {path → SHA-256} of ______ [list], computed once before the first pilot call, stored as the file ______, and recorded in the decision record and every run manifest. It excludes the decision record, run folders, the Step 10 harness and the final freeze manifest. The final freeze manifest of step 11 is a later object that contains the hash of the decision record. The runner and the decision script recompute the index and refuse on a mismatch."
- **Alternatives:** chain of existing manifest hashes (CRB design B); accept 'researcher-supplied, unverified' (status quo).
- **Acceptance:** hand recomputation equals the stored value; a one-byte change of an FZ file changes it; the gate refuses without it.

- **Owner decision: PENDING | Advisor decision: PENDING | Date: PENDING | Option chosen: PENDING**

### MD-05 PG3, PG11b, SF/UNP policy, coding eligibility, PRD-5 (C-06, C-07, C-08, C-10, C-11)
- **PG3 (class: clarification):** "Every differing character position between the members of a pair lies inside the span of the target numeral; shared characters inside the numeral do not break the span." Source: spec 8.1, 8.2 "a single changed span". If rejected: the build is rejected and steps 3-9 repeat.
- **PG11b (class: keep = no change; narrowing = PROTOCOL):** "The literal text of 8.2 stands. Known risk: ordinary words in model comments can block secondary coding." Alternative text if narrowed: ______.
- **SF/UNP policy (class: interim = clarification; Policy 1/2/parse-first = PROTOCOL):** "A call that meets any SF definition is classified SF only. Main-run reporting follows §18.2 as written: SF calls stay in `n_calls`, the SF count and rate are reported beside the four proportions, no proportion is rescaled."
- **Coding eligibility (clarification):** "Coded: recorded calls with no SF flag and a verdict that parses. UNP, SF and SF3-with-verdict calls are counted beside every table with D_P(c)."
- **PRD-5 (clarification; note it concerns the blind-check worksheet, §11.2 step 3):** "The field-specific unit-token sets printed in §11.2 step 3 are adopted."
- **Acceptance:** each reflected in the codebook/tests/gate report as applicable.

- **Owner decision: PENDING | Advisor decision: PENDING | Date: PENDING | Option chosen: PENDING**

### MD-06 Provider response safe-stop policy (C-12, C-13, C-14, C-15)
- **Class:** record entry (a stop is not a classification); automatic SF classification of new names would be PROTOCOL.
- **Rule quoted:** FZ-v1 row 17 (returned model ID "recorded for every call"); spec §13.4 SF1, SF3, SF4; record 12.36.
- **Proposed text:** "(1) A response whose returned model ID is missing or not exactly the requested ID is recorded and stops the workflow for owner review before the next call. (2) A finish reason that is not STOP and not the token limit and not a documented block signal stops the workflow for owner review; the response is kept as recorded and not replaced. (3) SF4 is assigned only to: no candidate returned; a prompt block reason; and finish reasons ______ [names, each with its source after the first live observation]. (4) A record without an HTTP status stops the workflow for owner review. (5) An error marker or an HTTP status outside 2xx is SF1 even if text is present. A stop leaves the run marked INCOMPLETE with the reason."
- **Impact:** needs a stop path in the runner (none today); retries stay 0.
- **Acceptance:** mock tests for every clause; no stop case is scored as a valid response.

- **Owner decision: PENDING | Advisor decision: PENDING | Date: PENDING | Option chosen: PENDING**

### MD-07 Timeout meaning (C-16)
- **Class:** record entry (per-operation) / PROTOCOL if a total deadline changes which calls fail.
- **Proposed text:** "The frozen 180 s is ______ (a per-socket-operation timeout; calls whose recorded latency exceeds 180 s are flagged / a total wall-clock deadline of 180 s per request, a hit being SF1 and never retried)." Decide before the FZ hash.

- **Owner decision: PENDING | Advisor decision: PENDING | Date: PENDING | Option chosen: PENDING**

### MD-08 Resume after a transport halt (C-17)
- **Class:** record entry; a counter reset would be PROTOCOL.
- **Rule quoted:** spec §13.8 "resumes only under the identical FZ version ... continuing at the next call_index ... (no re-draw)"; "no completed call is replaced".
- **Proposed text:** "(1) Halt counters carry over. (2) An intent entry without a raw entry is 'attempted, no record': it is never repeated, it is reported, and the owner records its disposition before any resume. (3) 'Transport-only' means every call of the current consecutive-failure run has the flag set [SF1] and no response text. (4) A resume is a recorded owner event with a new authorization for the remaining calls and the same cost ceiling, under the identical FZ hash. (5) The resume appends to the same hash-chained ledger and starts at the first index without an intent entry. (6) No delay other than the frozen 1 s."
- **Acceptance:** local simulations in `MASTER_IMPLEMENTATION_PLAN.md` patch P8.

- **Owner decision: PENDING | Advisor decision: PENDING | Date: PENDING | Option chosen: PENDING**

### MD-09 Anchoring of the decision record, authorization content, order of runs (C-18)
- **Class:** record entry.
- **Proposed text:** "The decision record is anchored by ______ (own commit with ID recorded in the final freeze manifest and run manifests / external timestamped copy of its SHA-256), declared on ______ [date], before the decision script is run. The owner authorization for a run is a file with `authorized_by` = owner, the scope, the exact number of calls, the cost ceiling 100 and the input-size basis of MD-02. Order: pilot round 1 → report and integrity check → decision → [round 2 only after a whitelisted change as a new FZ version] → decision record anchored → final freeze manifest → main run."

- **Owner decision: PENDING | Advisor decision: PENDING | Date: PENDING | Option chosen: PENDING**

### MD-10 Confirmations of earlier choices (C-20, C-21, C-22, C-24, C-25, C-28)
Text: "(PC-2) the pilot registry is built and gated at step 8; (I-6) informational diagnostic, gate counts stay 30 and 14; (P-3 item 1) `s2_values` 'none' is reported as a count outside its denominator; (F-3) closed; (PRD-8) unchanged; the Step 8 choices of record 12.28 (F-4 architecture, PG4 test, PG11a projection bundle of 624 files, A6b actor) are confirmed / amended: ______."

- **Owner decision: PENDING | Advisor decision: PENDING | Date: PENDING | Option chosen: PENDING**
