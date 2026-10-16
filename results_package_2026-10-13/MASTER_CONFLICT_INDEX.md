# Master conflict index (status of every row: PROPOSED — NOT ADOPTED unless stated; all decisions PENDING)

Prepared 2026-10-13 from the sources named in each row. "Doc" points to the section of `MASTER_PREPILOT_RESOLUTION.md` (MPR) or `CONFLICT_RESOLUTION_BRIEF.md` (CRB) that analyses the row. Line numbers are those of 2026-10-13. State words: OPEN (no decision), DELEGATED (assistant under delegation, not owner-approved), DECIDED (owner entry), UNRESOLVED (cannot be settled from current evidence).

| ID | Conflict or open item | Sources | Depends on | Phase | State | Doc |
|---|---|---|---|---|---|---|
| C-01 | OD-10: the Step 7 character bound (12.18 row 6) versus the input size of paid calls (12.11 OD-10 "measured on the actual prompt") | record 402, 511, 604; FZ-v1 lines 21, 173; spec has no OD-10 | C-23 | before pilot | OPEN (code: owner-stated `max_input_characters`, working decision; no token measurement) | CRB 1, MPR 4 |
| C-02 | Kappa: spec 16.3 line 1002 "reported" versus OD-3 "may not be claimed" versus 12.21 row 6 / P-3 "not reported" (scope and verb, delegated reading) | spec 1002-1003; STEP2 record 45; record 602, 689-691; PROPOSED_CLARIFICATIONS 72-73; codebook 49, 196, 202, 213 | C-09 | before FZ hash | OPEN / DELEGATED | CRB 2, MPR 3 D5 |
| C-03 | FZ hash: object undefined; time order (13.2 before pilot; record and final manifest after); runner does not mention an FZ hash | spec 662, 797, 1190; record 603; `s7_decision.py` 163-176; `s11_final_freeze_manifest.py` 15-27 | C-18 | before FZ hash | OPEN | CRB 3, MPR 6 |
| C-04 | Pilot counts built from a provisional primary SF type hide hard flags (false pass for SF1/SF4 together with SF3/SF5) | spec 807-816, 828-834; record 506, 793; `s10_scoring.py` 20, 46-63, 92; `s7_decision.py` 75-80 | C-05 | before pilot | PARTLY ADDRESSED: hard-flag false passes closed in code under working decision MD-01 (not ratified); SF2 part see C-31 | MPR 2 |
| C-05 | `SF1 + SF4 <= f_S`: per call or per flag | spec 830; PJR J-10 (line 140); Policy 2 package 4.4 | C-04 | before pilot | OPEN (code implements per call as a working decision; ratification pending) | MPR 2 |
| C-06 | PG3 "contiguous": strict positions versus single span | spec 461, 525; record 743 (12.28) | none | before pilot | DELEGATED (assistant under owner instruction) | MPR 3 D1 |
| C-07 | PG11b literal scan rejects ordinary response words | spec 519-520, 1206; `s7_bundle.py` 30, 64-98; record 724 | none | before FZ hash | OPEN (owner kept literal) | MPR 3 D2 |
| C-08 | §18.2 "four proportions sum to 1" versus SF calls; Policy 1/2 | spec 1051-1058, 1223; record 506, 724; amendment drafts | C-04 | before FZ hash | OPEN (interim rule) | MPR 3 D3 |
| C-09 | Re-code sample, delay, columns versus 16.3 | spec 1000-1003; record 602, 689; codebook 5.3 | C-02 | before FZ hash | DELEGATED | MPR 3 D5 |
| C-10 | "Parseable" for coding: SF3 with a verdict, partial text | spec 925, 859; codebook 32; `s12_coding.py` | C-04 | before coding | OPEN | MPR 3 D6 |
| C-11 | PRD-5 unit sets pending; premise correction: it is the blind-check worksheet normalization (11.2), not the codebook | spec 699, 1131; `s9_blindcheck.py` | none | before the blind check is evaluated | OPEN | MPR 3 D7 |
| C-12 | Returned model ID differs: record only in the text | FZ-v1 row 17; spec 1036; record 68; pilot-study analyzer spec line 45 (precedent only) | live fact | before pilot (policy) | OPEN / UNRESOLVED (alias forms) | MPR 3 Q-P1 |
| C-13 | Unlisted finish reason | spec 805-816 (silent); `s10_scoring.py` 27-39 | live fact | before pilot (policy) | OPEN | MPR 3 Q-P2 |
| C-14 | Which names mean blocked; names undocumented in the repository | spec 812; `s10_scoring.py` 18 | live fact | before pilot (policy) | OPEN / UNRESOLVED (names) | MPR 3 Q-P3 |
| C-15 | Record without HTTP status; error marker with text | spec 809; record 793 | none | before pilot | OPEN | MPR 3 Q-P4 |
| C-16 | Timeout 180 s: per socket operation versus total deadline | FZ-v1 row 17; `s10_runner.py` `TIMEOUT_SEMANTICS` | live fact | before FZ hash | OPEN | MPR 5 |
| C-17 | Resume after transport halt: five open points; unresolved intent shown by simulation | spec 871-875; PRE_PILOT_FIX_REPORT 4 | C-03, C-16 | before main run | OPEN | MPR 5 |
| C-18 | PRD-6: write-once store not declared at step 6 | spec 662, 1132; record 655 (12.23) | none | before step 11 | OPEN | MPR 7 |
| C-19 | FZ-v1 manifest stores decision-record hash `94fa64f9...`; the file differs (append-only record) | FZ-v1 `artifact_hashes`; record 12.12-12.18 notes | none | historical | RECORDED (documented mismatch) | MPR 7 |
| C-20 | PC-2: step at which the pilot registry is first built | spec 1136; record 657 (12.23), 743 | none | confirm | DELEGATED reading | MPR 7 |
| C-21 | I-6 six-reading check undefined; made informational | spec 670, 226 (gate counts); record 653, 743 | none | confirm | DELEGATED | MPR 7 |
| C-22 | P-3 item 1: `s2_values` "none" outside its denominator | PROPOSED_CLARIFICATIONS 65-70; spec 941, 968 | none | before coding | OPEN | MPR 7 |
| C-23 | P-4: token measurement method and authorization | PROPOSED_CLARIFICATIONS 77 ff.; record 604 | C-01 | before main run | OPEN | MPR 4 |
| C-24 | F-3: generator uses register values | record 650 (12.23) | none | confirm | technically satisfied | MPR 7 |
| C-25 | PRD-8 `E-EMPTY-TARGET` | spec 756, 1133 | none | none | not applicable under DP1/OD-4 | MPR 7 |
| C-26 | P-5 human readiness (codebook rehearsal) | spec 818-820 (13.5); codebook 6 | human | before pilot | OPEN (human) | checklist |
| C-27 | Round-1 FAIL-S action and multi-type case | spec 836-840; record 510, 599 | none | when it occurs | OPEN | MPR 7 |
| C-28 | Step 8 design choices (F-4 architecture, PG4 test, PG11a projections, A6b actor) taken under the owner's instruction without advisor review | record 743-750 (12.28) | none | before FZ hash | DELEGATED | MPR 7 |
| C-29 | Price and model re-verification at the freeze | PJR J-9; FZ-v1 `model_verification` | live/web fact | before first paid call | OPEN (human) | MPR 4 |
| C-30 | Status word `RUN_COMPLETE` means "all planned calls have a record", not success | `s10_runner.py` summary; PROVIDER_STATIC_AUDIT item 7 | none | wording | LOW | checklist |

## Dependency relations between decisions
C-05 → C-04 → C-08 → C-10 (counting convention → denominator policy → coding population). C-02 ↔ C-09 (same codebook decision). C-03 needs C-18 (anchor) only for the later record, not for the FZ hash. C-16 → C-17 (a total timeout changes which calls are transport failures). C-01 ↔ C-23 ↔ C-29 (basis of input size, method, prices). C-12..C-15 depend on one live observation for their names and shapes but need a safe-stop policy before it.

## Not decidable from current evidence (UNRESOLVED)
Whether live payloads can contain the multi-flag combinations of C-04; the real finish-reason vocabulary and whether RECITATION/OTHER/LANGUAGE mean a block (C-14); the exact form of the returned model ID (C-12); whether `thoughtsTokenCount` exists and how totals are composed (cost accounting, PRE_PILOT_FIX_REPORT 1); who may authorize a resume (C-17); whether "transport-only" needs an HTTP-level distinction (C-17); whether the owner's message behind 12.24 meant "kappa not computed" or "not claimed" (C-02); whether "Step 7" in OD-10 meant the freeze step or the first paid call (C-01); the independence limit of the Step 8/9 checks (one author, `MASTER_PILOT_READINESS_CHECKLIST.md`).
| C-31 | SF2 detection with SF1/SF4: spec 810 has no exception, `sf_flags` suppresses SF2 when SF1/SF4 is met; literal independent detection makes the `f_S` allowance of 13.6 unreachable for adapter-made records (measured: 10 tests flip) | spec 810, 816, 830-831; `s10_scoring.py` 59; PJR J-10; `deferred_patches/` | C-04, C-05 | before pilot | WORKING DECISION option B (researcher, 2026-10-13); formal ratification PENDING OWNER (Q1-Q6; Q5 open) | MD-01 |
| C-32 | Assumed input tokens versus prompt length in characters is not enforced by the gate; form of a "measured basis" undefined | MPR 4 line 74; record 12.18 row 6; `deferred_patches/` P3b | C-01, C-23 | before pilot (owner writes >= 1,016 by hand) / before main run | OPEN, options C32-1..3 in `C31_C32_OWNER_DECISION_BRIEF.md` (decision owner: owner; an external token count needs separate written authorization) | MD-02 |
| C-33 | Status statements about the SF counting in the official record (12.30, 12.37) no longer match the code (the two code comments were corrected in the closeout batch, docstring-only); the official record is not edited by the assistant | `PROPOSED_RECORD_CORRECTION_12_37.md` | none | any time before the pilot | OPEN (owner decides whether and how to append/amend) | audit file |
