> **Status note (2026-10-13, added later):** the SF items of this file describe the SF counting BEFORE patch P1. Since then the code applies the working technical decision MD-01 (hard flags -> FAIL-S, one decision count per call; not ratified) and the SF2-with-SF1/SF4 question is analysed in `C31_C32_OWNER_DECISION_BRIEF.md`. Read the case tables below as the earlier state.

# Draft decision-record entries (PROPOSED — NOT ADOPTED)

Drafts to be copied into `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` only after the named person has decided; the record is append-only and the next free number at adoption time is assigned then (the last entry on 2026-10-13 is 12.36). Nothing here has been added to the record. Source and reasoning for each entry: `PROPOSED_FINAL_DECISIONS.md` (same item numbers). Each entry has an empty approval block; a recommendation that the approver changes must be edited before copying. Entries that change the protocol say so and need a new methodology version (spec §13.2, §21.2) in addition to a record entry.

Approval block used below:
`Approved by (owner): ______  Advisor: ______  Date: ______  Option chosen: ______  Changes: ______`

---
### DRAFT-D1 (PG3 reading) — class: clarification — PROPOSED — NOT ADOPTED
Text: "PG3 (spec 8.1) is read as: every differing character position between the two members of a pair lies inside the span of the target numeral; shared characters inside the numeral (the decimal point) do not break the span. The strict reading (consecutive positions) is not enforced; the number of strictly non-consecutive pairs is reported in gate_report.json." Source: spec 8.1 PG3, 8.2 "a single changed span"; record 12.28. Reason: the strict reading rejects 90 of 104 MIL templates. If not approved: the build is rejected and steps 3 to 9 repeat.
Approval block.

### DRAFT-D2 (PG11b scan) — class: no change (keep) — PROPOSED — NOT ADOPTED
Text: "The literal text of 8.2 stands: PT1 and PT3-PT8b are scanned in names, bodies and directory names of the coder bundle including model text. Known risk: ordinary words in model comments can block the secondary S2/S3 coding; primary results are unaffected. Any narrowing is a protocol change decided before the FZ hash." Source: spec 8.2; record 12.14, 12.26 item 2. Reason: least change. Alternative entries (protocol change): scan scope narrowed to ___.
Approval block.

### DRAFT-D3 (SF / UNP) — class: clarification of interim handling; Policy 1/2 = protocol change — PROPOSED — NOT ADOPTED
Text: "Pilot and main run: a call that meets any of SF1-SF5 is classified SF only (12.18 row 1). Main-run reporting follows spec 18.2 as written: SF calls remain in n_calls, the SF count and rate are reported beside the four proportions, no proportion is rescaled. Policy 1, Policy 2 and parse-first are not adopted." Source: spec 13.4, 13.6, 18.2, 22 item 6; record 12.18 row 1, 12.24, 12.26. Reason: no denominator is changed. Option if the advisor prefers Policy 2: amend 13.4, 13.6-13.8, 18.2, 12 in a new methodology version before the FZ hash.
Approval block.

### DRAFT-D4 (SF flags and primary type) — class: clarification (counting convention) — PROPOSED — NOT ADOPTED
Text: "All SF flags met by a call are recorded. The pilot round outcome (13.6) is computed from the flag sets: any call meeting SF2, SF3 or SF5 makes the round FAIL-S; SF1 + SF4 is counted per call [or per flag: ______]. For the per-type table only, the primary type is chosen by the order ______ (proposed: SF1 > SF4 > SF3 > SF2 > SF5). Multi-flag calls are counted and reported." Source: spec 13.4, 13.6; Policy 2 package 4.4-4.5; record 12.30, 12.36. Reason: the definitions in 13.4 are not exclusive and 13.6 speaks of definitions met. Code consequence after adoption: `pilot_counts` and its tests.
Approval block.

### DRAFT-D5 (re-code and 16.3) — class: clarification of silence; kappa line = departure — PROPOSED — NOT ADOPTED
Text: "Delayed intra-rater re-code per (family, condition) cell: all responses if at most 20, otherwise max(20, ceil(20 % of D_P)); at least 14 full days after the last first-pass code; first-pass codes concealed; re-codes in recode1_* columns; raw agreement and full cross-tables per variable. Cohen's kappa: ______ (not computed / computed and labelled 'intra-rater consistency, no reliability claim'). Every table states 'single coder, intra-rater only'." Source: spec 16.3; OD-3 (STEP2 record); record 12.21 row 6, 12.24 decision 2, 12.26 item 3; codebook rev 5 section 5.3. Reason: values are delegated and have no empirical basis; kappa statements in the sources conflict.
Approval block.

### DRAFT-D6 (coding eligibility) — class: clarification — PROPOSED — NOT ADOPTED
Text: "Responses coded for S2/S3 are the recorded calls with no SF flag and a verdict that parses (satisfied, violated, unclear). UNP and SF calls are counted and reported beside every table with D_P(c) (TH16). SF3 calls that carried a verdict are counted as a diagnostic and not coded." Source: spec 16, TH16; Policy 2 package 7; record 12.31.
Approval block.

### DRAFT-D7 (PRD-5) — class: clarification — PROPOSED — NOT ADOPTED
Text: "The field-specific unit-token sets of spec 11.2 step 3 are adopted as printed." Source: spec 11.2, 19.3; step9/s9_blindcheck.py. Decide before the blind check is evaluated.
Approval block.

### DRAFT-Q-P1..Q-P4 (provider responses) — class: clarification; automatic stops = protocol change — PROPOSED — NOT ADOPTED
Text: "(Q-P1) The returned model ID is recorded for every call; a returned ID that is not exactly the requested ID is reported in the pilot report and stops the workflow for owner review before the next call or round [stop mechanism to be built after adoption]. (Q-P2) A finish reason that is not STOP, not the token limit and not on the blocked list is not classified by name; the workflow stops for owner review. (Q-P3) The blocked list is: SAFETY, BLOCKLIST, PROHIBITED_CONTENT, SPII, IMAGE_SAFETY; RECITATION, OTHER, LANGUAGE are treated as unlisted. (Q-P4) A record without HTTP status and without error marker is SF1 [from the first live observation]." Source: spec 13.4, FZ-v1 row 17; record 12.36; PROVIDER_RESPONSE_VALIDATION_REPORT.md. Reason: no failure or unverifiable response may be silently scored as a success; names are not widened. Code consequence after adoption: s10_scoring.py, s10_runner.py and tests; the stop mechanism does not exist yet.
Approval block.

### DRAFT-12 (timeout meaning) — class: clarification; total deadline = change of frozen setting behaviour — PROPOSED — NOT ADOPTED
Text: "The frozen timeout of 180 s is a per-socket-operation timeout; there is no total deadline. Latency is recorded and calls above 180 s are flagged. [Alternative: total wall-clock deadline of 180 s; a deadline hit is SF1 and is never retried.]" Source: FZ-v1 row 17; spec 17 row 17; record 12.34. Decide before the FZ hash.
Approval block.

### DRAFT-13 (resume after transport halt) — class: clarification; reset of counters = protocol change — PROPOSED — NOT ADOPTED
Text: "Resume of a main run halted by transport failures (13.8): (1) halt counters carry over; (2) an intent without a raw record is 'attempted, no record', is never repeated and is reported; (3) 'transport-only' means every call of the current consecutive-failure run is SF1; (4) a resume is a recorded owner event with a new authorization for the remaining calls; (5) no delay other than the frozen 1 s. The resume appends to the same hash chain." Source: spec 13.8; PRE_PILOT_FIX_REPORT.md section 4. No tool exists; build only after adoption.
Approval block.

### DRAFT-14 (PRD-6 anchor) — class: clarification (declaration missing at step 6) — PROPOSED — NOT ADOPTED
Text: "The decision record of step 11 is anchored by: ______ (own version-control commit with its ID recorded in the final freeze manifest and the run manifests / external timestamped copy of its SHA-256). The runner aborts if the anchor cannot be verified." Source: spec 10 (line 662), 19.3; FZ-v1 declares no store. A commit needs the owner's explicit permission.
Approval block.

### DRAFT-15 (P-2 FZ hash) — class: clarification of an undefined object — PROPOSED — NOT ADOPTED
Text: "The FZ hash recorded in the decision record is the SHA-256 of a versioned FZ index (canonical JSON of the file hashes of the FZ items, excluding the decision record), computed before the first pilot call and verified by recomputation. The final freeze manifest of step 11 is a later object. The FZ-v1 register hash is not redefined." Alternative: 'researcher-supplied, unverified' accepted in writing. Source: spec 10, 13.2, 21.1 row 11; record 12.21 row 7. Tool to be built after adoption.
Approval block.

### DRAFT-16 (OD-10 / P-4) — class: clarification of the basis; measurement = external call — PROPOSED — NOT ADOPTED
Text: "For the pilot rounds the input-size basis is: ______ (the character bound of 1,016 re-accepted for the paid calls / a token count of the final prompts, authorized separately). Prices are re-read on the day of the call (PJR J-9). The authorization file states the assumed tokens per call." Source: record 12.11 OD-10, 12.18 row 6, 12.21 row 8; FZ-v1 cost estimate.
Approval block.

### DRAFT-17/18/19/20 (PC-2, I-6, P-3, F-3, PRD-8) — class: clarification/closure — PROPOSED — NOT ADOPTED
Text: "(PC-2) The pilot registry is built and gated at step 8 with the same code; step 4 ran it informationally. (I-6) The six-reading check is an informational diagnostic of the build, not a gate; gate counts stay 30 and 14. (P-3) item 1: s2_values 'none' is reported as a count outside its denominator; item 2: MX means MPG; item 3: see DRAFT-D5; item 4: see DRAFT-D3. (F-3) closed: the Step 8 build takes values from the frozen register and the numeric gates relate members to it. (PRD-8) not applicable under DP1 and OD-4; unchanged." Source: spec 19.3 lines 1131-1136, 11 layer 1, 3.7; record 12.23, 12.28.
Approval block.
