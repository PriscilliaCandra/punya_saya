# Advisor / owner decision brief (2026-10-13)

Every "recommendation" is a technical or methodological suggestion by the assistant; it is not a decision and nothing here changes the frozen specification (v2.7, sha256 `d5fcffad...`). The last column of each item is for the advisor and the owner and is intentionally empty. Section numbers refer to `research_design/SCENARIO_CONSTRUCTION_SPECIFICATION_v2_7_DRAFT.md`; "12.n" refers to `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md`. All items verified as still open on 2026-10-13 by reading the record entries named.

Timing key: **Before pilot** = needed before the first pilot call. **Before FZ hash** = before the freeze set is hashed (a later change means a new FZ version and a re-pilot, 13.6). **Before main run / coding** = can wait, but must be fixed before any data exist for it.

## D1. PG3: "contiguous" changed span  (before pilot: yes, it decides whether the built registry stands)
- **Reference:** §8.1 row PG3 ("the set of differing character positions is contiguous and inside the target token's span"); §8.2 "a single changed span"; 12.28 (clarification taken, advisor review pending); `step8/s8_gates.py` (`pair_problems`); `main/gate_report.json` field `PG3_strict_nonconsecutive_pairs_informational` = 180 pairs.
- **Problem:** read as consecutive character positions, 90 of the 104 MIL templates fail because the decimal point is shared (21.5 vs 22.4 differ in two non-adjacent characters). PAC never fails.
- **Options:** (a) ratify the single-span reading as a clarification (record entry); (b) keep the strict reading: the build is rejected, which returns to step 3 or 7 (§21.2) with new MIL parameters or wording, and Steps 3 to 9 repeat; (c) amend the text of PG3 in a new methodology version.
- **Consequences:** (a) none for the built artefacts; (b) invalidates the registry, the Step 8 output and Implementation B's agreement, and costs days; (c) as (a) but formal and slower.
- **Recommendation:** (a), because §8.2 states the intent ("single changed span"), and (b) would reject the frozen design for a property of the decimal point rather than of leakage.
- **Decision (advisor/owner):** ________________  **Date:** ________

## D2. PG11b scan scope  (before FZ hash: the bundle builder is an FZ item, 12.14)
- **Reference:** §8.2 rows PG11a/PG11b ("no pattern PT1, PT3-PT8b occurs in any file name, file body or directory name"); §21.2 row 6; 12.26 item 2 (owner kept the literal text); `step7/s7_bundle.py` lines 30, 64-98; `test_step7.py` `test_D1_pt4_is_in_the_pg11_scan`.
- **Problem:** the post-run application check scans model-written text. In an in-memory test with synthetic strings, ordinary words such as "CLEAR", "PAC", "(valid)", "class = A" were rejected, and rebuilding cannot help. The effect would be to block the secondary S2/S3 coding; primary results are unaffected.
- **Options:** (a) keep literal (current); (b) amend to scan names, directory names, skeleton and prompt part only; (c) amend to scan response text only for machine-form patterns; (d) mask matches in the builder (changes what coders see).
- **Consequences:** (a) risk of blocked coding, no cost now; (b), (c), (d) need a new methodology version and a Step 7 re-freeze before the FZ hash; (d) alters coder material and is the hardest to defend.
- **Recommendation:** (a) for the first run if the timeline matters, accepting the risk in writing; (c) if the advisor wants S2/S3 coding protected. The choice should be made before the FZ hash because a later change is an FZ change.
- **Decision:** ________________  **Date:** ________

## D3. Structural failures and UNP in the main run  (before main run; before FZ hash because §18 is in FZ)
- **Reference:** §13.4 (SF1-SF5, UNP), §13.6, §13.8, §18.2 (four proportions over all `n_calls`, "sum to 1"), §22 item 6; 12.18 row 1 (pilot rule); 12.24 decision 1 (Policy 1 proposed); 12.26 item 1 (owner kept v2.7 as written); `PROPOSED_AMENDMENT_18_2_DRAFT_v1.md`; `POLICY_2_METHODOLOGY_DECISION_PACKAGE_DRAFT_v1.md`.
- **Problem:** under the literal text SF2 and SF3 without a verdict also meet the UNP definition; 12.18 row 1 fixes SF-first precedence for the pilot only. With an SF call in a main cell the four proportions cannot sum to 1.
- **Options:** (L) literal text, overlap unresolved; (C) v2.7 plus the SF-first sentence, SF reported beside the four proportions (current interim rule); (P1) evaluable-call denominators plus a separate SF rate; (P2) SF as a fifth class over planned calls; (PF) parse-first.
- **Consequences:** L and PF contradict 12.18 row 1. C needs no amendment but leaves "sum to 1" false when an SF occurs. P1 contradicts §12 ("over all R calls") and leaves cluster means undefined. P2 keeps §12 intact, sums to 1, matches the halting monitor, and needs an amendment, a call ledger and a counting sentence.
- **Recommendation:** C for the pilot and the first main run (it needs nothing); P2 if the advisor wants a clean "sums to 1" statement, adopted before the FZ hash.
- **Decision:** ________________  **Date:** ________

## D4. Priority when several SF flags occur on one call  (before pilot: it fixes the count vector)
- **Reference:** §13.4 states none; `step10/s10_scoring.py` `PRIMARY_ORDER` (SF1 > SF4 > SF3 > SF2 > SF5, provisional); Policy 2 package §4.5 and D-4; 12.30.
- **Problem:** the decision script needs disjoint counts. By reading `sf_flags`, the only realistic co-occurrence is SF3 with SF2 (empty text at the token limit); both are "hard" in 13.6, so the pilot outcome does not depend on the order. The order only decides the per-type table.
- **Options:** (a) flags-only reporting, the order used only to build the pilot count vector; (b) freeze an exclusive order (the provisional one); (c) another order.
- **Consequences:** pilot outcome is unaffected under (a) and (b) for the realistic case; (b) adds a rule that the text lacks.
- **Recommendation:** (a), with the provisional order recorded as a counting convention.
- **Decision:** ________________  **Date:** ________

## D5. Re-code values and the departures from §16.3  (before FZ hash: the codebook is an FZ item; before S2/S3 coding at the latest)
- **Reference:** §16.3 lines 997-1003; OD-3 (`STEP2_OWNER_DECISIONS_RECORD.md`: one coder, no inter-rater reliability or kappa claim); 12.21 row 6; 12.24 decision 2; 12.26 item 3; codebook revision 5 section 5.3; `step7/s7_recode.py`.
- **Problem:** the delegated procedure uses a 20 % sample (floor 20), 14 days, `recode1_*` columns and no kappa; §16.3 states no sample, no delay, names `coder1_*`/`coder2_*` and says kappa is reported.
- **Options:** (a) approve the delegated values and record the departures; (b) re-code every coded response and report kappa labelled "intra-rater consistency, no reliability claim"; (c) other values.
- **Consequences:** (a) fastest, weakest evidence; (b) closest to the literal text and OD-3's wording (OD-3 forbids claims, not computation), larger workload and a change to `s7_recode.py`; the owner chose (a) on 2026-10-13 pending the advisor.
- **Recommendation:** (a), with the advisor's explicit approval of the 14-day delay and the sample.
- **Decision:** ________________  **Date:** ________

## D6. Which responses are eligible for coding  (before coding)
- **Reference:** §16 "only parseable responses"; TH16; 12.31; Policy 2 package §7 and D-10; `step10/s12_coding.py` (provisional).
- **Problem:** "parseable" is undefined for an SF3 call whose truncated text still contains a valid verdict.
- **Options:** (a) non-SF calls with a parseable verdict (current provisional rule); (b) include SF3-partial calls as a separate stratum; (c) all calls with a parseable verdict.
- **Consequences:** (a) consistent with SF-first precedence; (b) adds a stratum and tables; (c) contradicts SF-first.
- **Recommendation:** (a).
- **Decision:** ________________  **Date:** ________

## D7. PRD-5: unit-token normalization of the human check  (before the human blind check is evaluated)
- **Reference:** §11.2 step 3 (field-specific sets, marked "PENDING RESEARCHER DECISION PRD-5"), §19.3; `step9/s9_blindcheck.py` (`UNITS`).
- **Problem:** the field sets are printed in the text but the decision is still marked pending.
- **Options:** (a) adopt the printed field-specific sets; (b) return to the older global list (accepts more representations, absorbs wrong units).
- **Consequences:** (a) stricter; a human who writes a foreign unit gets a transcription CHECKER ERROR (logged, member kept); (b) is not the text of v2.7.
- **Recommendation:** (a).
- **Decision:** ________________  **Date:** ________

## Other open items found while reading the record (not in the list you gave)
| Item | Reference | Needed |
|---|---|---|
| PRD-6: anchoring of the decision record in a write-once store | §10, §19.3; 12.23 table; `research_design/` is untracked, FZ-v1 declares none | before the final pilot decision is written (Step 11): owner declares the store |
| P-2: FZ hash contract | 12.21 row 7; decision script records the hash as "researcher-supplied, unverified" | before Step 11 (or accept "unverified" in writing) |
| P-4 / OD-10: input size is a character bound, not measured | 12.18 row 6 ("for Step 7"); PJR J-9 (re-verify model, prices, cost at the freeze) | before the first paid call: re-accept the bound or authorize a measurement |
| Round-1 FAIL-S action and the multi-type case | §13.6 actions; 12.18 row 5, 12.21 row 3 | when it occurs; researcher decision, logged |
| PC-2: step at which the pilot registry is first built | §19.3; 12.23 table; 12.28 (reading taken) | confirm the reading |
| I-6 six-reading check; F-3; PRD-8 | 12.23 table; 12.28 | confirm "informational" / current handling |
| P-3: text inconsistencies (`s2_values`, MX, kappa, 13.4 versus SF2/SF3) | 12.21 row 5 | before coding |
| Codebook rehearsal by the human coder | §13.5; codebook section 6 | before the pilot |
