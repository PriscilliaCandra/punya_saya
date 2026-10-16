# Owner decision sheet (prepared 2026-10-15T06:58:42Z)

**This sheet records no decision.** Claude Code did not choose, approve, reject or record anything for the owner. "Owner answer" fields are blank for the owner. Recommendations are labelled `RECOMMENDATION — NOT AN OWNER DECISION`. Quotations are exact text of the files and lines named (excerpts marked); line numbers refer to the files as of this preparation. Decisions already recorded are not re-asked: PRD-5, D4, D6, MD-07 (12.46); MD-03 K2, PG11b, D3, D5, MD-01, MD-02 main box and Q7/Q8, MD-04 procedure, L-B and A-2 (12.47, 12.48); K2 verbs and the OD-3 interpretation (12.49); P13 (12.44); X-4b (12.45); class ratification: none now (12.44). **How an answer becomes a decision:** the owner states it explicitly and authorizes its recording as a new append-only entry (the next entry number is 12.50); until then the item stays pending. Approving a box is a decision about a procedure or patch; it does not run any tool, patch, provider call, freeze or pilot, and any implementation needs a separate explicit instruction.

## Overview
| # | ID | Status | Owner part decidable now? | What else is needed for finality |
|---|---|---|---|---|
| 1 | MD-06 + B-1 | OWNER CAN DECIDE NOW | yes | advisor concurrence ("Owner + advisor"); option B-1(b) also needs the advisor's acceptance by its own template |
| 2 | Q5 | OWNER CAN DECIDE NOW | yes | none named; the decision window closes at the code freeze (section 2) |
| 3 | E-1 (added: unrecorded box whose prerequisite MD-04 is now owner-approved) | OWNER CAN DECIDE NOW | yes | advisor concurrence on MD-04 |
| 4 | P11 | OWNER CAN DECIDE NOW (procedure/patch only) | yes | a separate written authorization file before any live call |
| 5 | P12 | OWNER CAN DECIDE NOW (procedure/patch only) | yes | a completed pilot before the script can be used |
| 6 | MD-10 | OWNER CAN DECIDE NOW (owner part), WAITING FOR ADVISOR for finality | yes | advisor review before the FZ hash; F-3 and PRD-8 caveats |
| 7 | Q9 / P3b | OWNER CAN DECIDE NOW only as REJECT; APPROVE is BLOCKED — SOURCE TEXT REQUIRED | partly | the form of a "measured basis" |
| 8 | MD-09 | WAITING FOR EVIDENCE (owner deferred, 12.47) | no | verification of an anchoring mechanism |
| 9 | H4-STOP | WAITING FOR RESEARCHER/EVIDENCE and ADVISOR | no | researcher's note on B10/B36, advisor answer |
| 10 | R-7 | RECORDED: NOT AUTHORIZED (12.48); the owner may reopen | yes, if the owner wishes | advisor concurrence on MD-03; see consequences |
| 11 | H5 | OWNER ACT, not a decision of this sheet | n/a | see section 11 |

## 1. MD-06 (provider response safe-stop policy) and B-1
- **Status:** OWNER CAN DECIDE NOW (owner part). Source authority: "Owner + advisor."
- **Decision question:** Do you adopt the MD-06 safe-stop policy, and if so which of B-1 (a), (b), (c) applies to a run that stops on an anomaly?
- **Legitimate options (source):** MD-06: `[ ] APPROVE  [ ] REJECT  [ ] AMEND: ______`; B-1: `[ ] (a)  [ ] (b)  [ ] (c)  [ ] other: ______`.
- **Source quotations:**
- `results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 141-145:

  > ## MD-06 Provider response safe-stop policy (C-12..C-15) — formal approval needed (details in Appendix B)
  > - **Decision/recommendation:** after the record is stored, stop for owner review on: (1) returned model ID missing or not exactly the requested ID; (2) finish reason not STOP, not token limit, not a documented block name; (4) record without HTTP status and without error marker; (5) error marker or non-2xx remains SF1. SF4 only for structural signals (no candidate; a block-reason field); block NAMES only after an authorized observation. Owner + advisor.
  > - **Consequence you must accept:** a stop ends the run as RUN_INCOMPLETE with no PASS/FAIL-S outcome, and `s11_pilot` refuses it; what that means for round accounting and the lineage depends on your answer to **B-1** ((a) it counts as a round, (b) it is void and re-run under the identical FZ, (c) MD-06 is not adopted); the options and their consequences are in Appendix B and the assistant does not choose. **Alternatives rejected:** record only (today); automatic SF classification of new names (protocol change).
  > - **Affects:** `s10_runner.py`, `s10_integrity.py`, 5 legacy tests; inactive P2 diff + 7 tests. **Prerequisite:** your answer to B-1.
  > - `[ ] APPROVE  [ ] REJECT  [ ] AMEND: ______  | B-1 answered: [ ] (a)  [ ] (b)  [ ] (c)  [ ] other: ______  | Owner: ______  | Advisor: ______  | Date: ______`

- `results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` lines 232-234:

  >   - *Option (a), the stopped run counts as a pilot round.* Consequence: it has no outcome, so the spec defines no next action; a follow-up round needs your (and the advisor's) rule, because round 2 is defined only after FAIL-S. Record: a disposition entry "pilot attempt of scope S, folder F, ledger final hash H, recorded calls N, halt reason R: counted as round __; next step: ______".
  >   - *Option (b), the stopped run is declared void (not a round).* Consequence: after the cause is understood the same scope is run again under the identical FZ (a new authorization and a new output folder; no code change is needed to do so); this effectively raises the number of attempts above the cap of 2 unless the advisor accepts that a void run is not a round; if fixing the cause changes executable code it must satisfy H1-H4, otherwise it is a new FZ version that counts toward the cap. Record: the same disposition entry with "void" and the advisor's acceptance; the folder is kept and listed in the lineage.
  >   - *Option (c), MD-06 is not adopted (record and report only, as today).* Consequence: no stop, no round question; anomalies are counted and reported (`provider_checks`) and the pilot decision proceeds on counts; a returned-model or finish-reason problem would be seen only after the round.

- `results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` line 236:

  > - **Acceptance criteria before activation:** MD-06 and B-1 recorded; the 5 tests rewritten to the adopted policy (not weakened); the 7 new tests pass; single-flag outcomes unchanged; block-name lists unchanged until L3; `run_all_checks.py --quick` OK; gate still CLOSED; mock-only.

- **Consequences (source):** MD-06 approved: "a stop ends the run as RUN_INCOMPLETE with no PASS/FAIL-S outcome, and `s11_pilot` refuses it"; B-1 (a) the stopped run counts as a pilot round (no next action defined by the specification); (b) the stopped run is void and re-run under the identical FZ (may raise the attempts above the cap of 2 unless the advisor accepts that a void run is not a round; a code fix must satisfy H1-H4 or it is a new FZ version); (c) MD-06 is not adopted, anomalies are only counted and reported. In every option the stopped folder is never deleted or edited.
- **When it can be decided (source):** the OAP section says "Prerequisite: your answer to B-1". No observation is needed to decide: the finish-reason block NAMES are deliberately deferred ("block NAMES only after an authorized observation"). The earlier brief label BLOCKED for MD-06 was stricter than the source requires.
- **Dependencies not finished:** advisor concurrence; the five legacy tests are rewritten only after adoption; no code is changed by the decision.
- **RECOMMENDATION — NOT AN OWNER DECISION:** no source recommends a B-1 option ("the assistant does not choose"). Analytic observation only: (a) and (c) can be recorded on the owner's authority, while (b) needs the advisor's acceptance by its own sentence template. The Q-P1..Q-P4 recommendations in `ADVISOR_DECISION_BRIEF.md` D8 are the project's earlier suggestions, not adopted.
- **Owner answer:** ______

## 2. Q5 (adapter indicator for "candidate without text")
- **Status:** OWNER CAN DECIDE NOW. Depends on MD-01 (owner-decided 12.47; advisor concurrence pending).
- **Decision question:** Should the adapter store `candidates_returned`, with the SF4/SF2 rule for the rare shape "a candidate with empty text and no finishReason"?
- **Options (source):** `[ ] APPROVE  [ ] REJECT` (OAP box Q5).
- **Quotations:**
- `results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` line 60:

  > | 14 | Box Q5 | PENDING | adapter field `candidates_returned` and the SF4/SF2 rule for the rare shape | `s10_runner.py`, `s10_scoring.py`, `test_sf2_detection.py` d6 | MD-01 | Q5 | adapter/scoring tests, `--quick` | - | - | (x) (L-C) | x |

- `results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` line 103:

  > | Q5 | the adapter field | the present inference stays; the rare shape stays SF4 (soft), documented as a limitation |

- `results_package_2026-10-13/C31_C32_OWNER_DECISION_BRIEF.md` lines 168-173:

  > ## 16. Q5 contract: "no candidate" versus "a candidate with empty text and no finishReason" (execution batch 2026-10-13; NOT implemented, needs approval)
  > - **The distinction needed.** Spec 812 defines SF4 as "safety/blocked finish reason or no candidate returned". A response that DID return a candidate whose text is empty is not "no candidate"; under option B it is an empty response (SF2, hard) unless a block signal applies. Today the record cannot tell them apart: the adapter does not store the number of candidates, and `sf_flags` infers "no candidate" from HTTP 200 + no error + `finish_reason` absent + empty text. Result today: a candidate with empty text and no `finishReason` is SF4 (soft), the same candidate with `finishReason` STOP is SF2 (hard) (tested: `test_sf2_detection.py` d6).
  > - **Minimum adapter contract (proposal).** `GeminiProvider.generate` returns an additional key `candidates_returned`: the integer `len(data.get("candidates") or [])` when a JSON object was decoded, `None` when no payload was decoded (HTTP error, timeout, transport exception, non-JSON body). `run()` copies it into the stored record. No other field changes. Legacy records without the key (Stage 1/2 data, existing mocks) keep the current inference.
  > - **Scoring rule (proposal).** SF4 "no candidate" iff 2xx, no error marker, `candidates_returned == 0` (or, for legacy records, the current inference). A record with `candidates_returned >= 1`, empty text and no block signal is SF2. Block signals (finish-reason block names, `promptFeedback.blockReason`) are unchanged. **Behaviour change:** only the rare shape "candidate present, no text, no finishReason" moves from SF4 (soft) to SF2 (hard). It changes which calls fail a pilot, so it needs your approval (class C); it is not a pure implementation fix.
  > - **Tests required (written from the approved rule before the code):** adapter payload shapes with a patched `urlopen`: (1) no `candidates` key; (2) `candidates: []`; (3) one candidate without `content`; (4) `content` without `parts`; (5) `parts` with an empty text; each with and without `finishReason` and with and without `promptFeedback.blockReason` -> expected `candidates_returned` and flags; legacy record without the key -> old inference; the stored raw record round-trips through `s10_integrity` (raw equals calls.jsonl); `pilot_counts` and the decision vector unchanged for single-flag rows; no new outcome label.
  > - **UNKNOWN (do not guess):** which of shapes (1)-(5) the live API actually produces, whether a block yields an absent or an empty `candidates`, whether a candidate can lack `finishReason`. These are provider facts for L3 (`PROVIDER_VERIFICATION_MATRIX.md`); they are read from the provider documentation by the researcher, not provoked by test calls. Until approved and implemented, Q5 stays open and the pilot accepts the present inference.

- **Consequences (source):** APPROVE: new adapter key, and the rare shape moves from SF4 (soft) to SF2 (hard); "It changes which calls fail a pilot, so it needs your approval (class C); it is not a pure implementation fix." REJECT: "the present inference stays; the rare shape stays SF4 (soft), documented as a limitation". **UNKNOWN (source):** which payload shapes the live API actually produces.
- **Dependencies:** MD-01; tests to be written from the approved rule.
- **RECOMMENDATION — NOT AN OWNER DECISION:** both options are source-consistent. Reason to decide before the code freeze: because it is "not a pure implementation fix", it could not be introduced after the freeze without a new FZ version; reason for caution: approving changes pilot failure rules while the live shapes are UNKNOWN. I make no choice.
- **Owner answer:** ______

## 3. E-1 (enforce the FZ hash in the gates)
- **Status:** OWNER CAN DECIDE NOW (owner part). It is a source box that is still unanswered; its prerequisite MD-04 is owner-approved (12.48) with advisor concurrence pending; the official hash does not exist.
- **Decision question:** Should `s10_runner.py` and `s11_pilot.py` enforce the FZ hash?
- **Options (source):** `[ ] APPROVE  [ ] REJECT`.
- **Quotations:**
- `results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` line 16:

  > | FZ-hash enforcement in the gates (`s10_runner.py`, `s11_pilot.py`) | box **E-1** | P5 activation alone |

- `results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` line 58:

  > | 12 | Box E-1 | PENDING | enforce the FZ hash in the gates | `s10_runner.py`, `s11_pilot.py` | MD-04, P5 | E-1 | new gate tests, `--quick`, gate check | - | - | - | x (before the pilot) |

- `results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` line 101:

  > | E-1 | FZ-hash enforcement in the gates | the hash exists but is not machine-enforced; a documented weaker control |

- **Consequences (source):** REJECT: "the hash exists but is not machine-enforced; a documented weaker control". APPROVE: a gate change in two listed files (`s10_runner.py`, `s11_pilot.py`, both in the approved 31-file list, so their hashes move); P5 activation alone does not enforce it. MD-04 (source): without an FZ hash "the first pilot call is not allowed (spec 797)".
- **Dependencies:** MD-04 advisor concurrence; the official hash is computed only after MD-01, MD-03, MD-05, MD-06, MD-07 and MD-10 are settled.
- **RECOMMENDATION — NOT AN OWNER DECISION:** analytic only: E-1, Q5 and MD-06 all change `s10_runner.py`; deciding them together limits the number of times a listed file changes before the freeze.
- **Owner answer:** ______

## 4. P11 (connection-test tool)
- **Status:** OWNER CAN DECIDE NOW (the procedure/patch box only).
- **Decision question:** Do you approve the procedure of a single-call connection test (patch P11, tool not written)?
- **Options (source):** `[ ] APPROVE  [ ] REJECT`, plus "a separate written authorization file" before any call.
- **Quotations:**
- `results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` line 23:

  > | P11 connection-test tool and one provider test | box **P11** + a separate written authorization file (ceiling, prompt hash, handling) | spending, token counts, a pilot |

- `results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` line 107:

  > | P11 | the connection test | L1-L5 stay UNKNOWN; the first live contact is the pilot, protected only by MD-06 if adopted |

- `results_package_2026-10-13/deferred_patches/DEFERRED_PATCHES.md` lines 90-91:

  > ## P11 (proposed, not in the original plan): connection-test tool for L1-L5
  > Not written. A single-call tool is needed because `s10_runner` accepts only `pilot_round_1`, `pilot_round_2` and `main`. Requirements and acceptance tests are in `PROVIDER_VERIFICATION_MATRIX.md` section 0. Status: DEFERRED / BLOCKED BY PROVIDER VERIFICATION authorization; condition to continue: owner approves the connection test in writing and the tool's mock-only acceptance tests are written first. Owner: owner (authorization), assistant (tool, after approval).

- `results_package_2026-10-13/PROVIDER_VERIFICATION_MATRIX.md` lines 6-8:

  > - **Authorization (written, by the owner, before any call).** A file with `authorized_by` = `owner`, a scope that names the test (`connection_test`), `max_calls` (1 recommended), `cost_ceiling_usd`, the prompt it may send (by SHA-256) and how the response is handled. NOTE: `s10_runner` accepts only `pilot_round_1`, `pilot_round_2` and `main`; **no tool exists for a connection test**. A new small tool would be needed (proposed patch P11, not part of P1-P10, NOT written): one call, neutral prompt that is not a registry prompt and not experiment content, key from the environment variable only, no pilot ledger and no pilot-round consumption, output limited to the metadata fields below. Before first use it needs mock-only acceptance tests (key never printed or stored; refuses without authorization; exactly one call; response text discarded; no file overwritten).
  > - **Cost bound.** One call at the register settings is bounded by the hard-cap formula: about US$0.021 per call (US$0.3741 / 18 at 1,016 assumed input tokens and the 8,192-token output cap). The owner sets the ceiling; the true cost is expected to be far lower but is not known.
  > - **What may be stored.** HTTP status; the set of top-level and `usageMetadata` key names; `modelVersion` string; `finishReason` string; `promptFeedback` key names and `blockReason` string if present; numbers in `usageMetadata`; latency; the SHA-256 and character length of the response text. **Not stored:** the response text, the key, request headers, the prompt other than its hash.

- **Consequences (source):** APPROVE: the tool is written with mock-only acceptance tests first ("condition to continue: owner approves the connection test in writing and the tool's mock-only acceptance tests are written first"); the box "does not authorize" "spending, token counts, a pilot". A live call needs the separate authorization file (scope `connection_test`, `max_calls` (1 recommended), ceiling, prompt hash, handling), which does not exist and is not created. REJECT: "L1-L5 stay UNKNOWN; the first live contact is the pilot, protected only by MD-06 if adopted".
- **Cost bound (source):** about US$0.021 per call at the register settings (an upper bound, not a forecast).
- **Dependencies:** none for the procedure; interacts with MD-06.
- **RECOMMENDATION — NOT AN OWNER DECISION:** analytic: MD-06 and P11 are partial substitutes (the source names MD-06 as the mitigation if the test is INCONCLUSIVE, and P11's rejection leaves the pilot protected "only by MD-06 if adopted"); deciding MD-06 first clarifies how much P11 adds.
- **Owner answer:** ______

## 5. P12 (O4 usage reader)
- **Status:** OWNER CAN DECIDE NOW (the procedure/patch box); use WAITS for a completed pilot.
- **Decision question:** Do you approve the read-only script that applies method O4 to the pilot's `usageMetadata`?
- **Options (source):** `[ ] APPROVE  [ ] REJECT`.
- **Quotations:**
- `results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` line 24:

  > | P12 O4 usage reader (read-only; prints numbers only) | box **P12** + MD-02 Q8 | any provider token count (O2) |

- `results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` line 108:

  > | P12 | the O4 script | the main-run token basis must be O2 or an owner entry accepting the assumption |

- `results_package_2026-10-13/C31_C32_OWNER_DECISION_BRIEF.md` lines 177-180:

  > - **Method O4.** For each pilot call i: ratio r_i = `usageMetadata.promptTokenCount_i` / characters_i (characters from the build's prompt table); bound B = ceil(max_i r_i x 1,016). Compare B with the assumption written in the authorization. The pilot has 18 calls, 6 of them at the maximum length of 1,016 characters, so the longest prompts are observed directly and the ratio bound covers templates of other density.
  > - **Prerequisites.** (a) the pilot round has run and every call has a usable `promptTokenCount` (L4 confirms the field exists; calls without it make the result INCONCLUSIVE); (b) a small read-only script that prints only numbers (ids, characters, tokens, B) and never response text, approved by the owner (13.6.1: no human opens pilot responses; usage metadata is counts only) — not written; (c) the result recorded as a dated note and an official entry; (d) provider overhead tokens included in `promptTokenCount` are UNKNOWN until L4.
  > - **Decision rule.** B <= assumption: the assumption is confirmed as an upper bound for the pilot's templates; the main-run authorization may keep 1,016. B > assumption: recompute the hard-cap cost with B (the US$100 limit is reached only near 63,381 tokens per call) and ask the owner. Limits of O4: it measures pilot prompts only; main prompts not represented by the pilot's template types would rest on the ratio bound; if that is not acceptable, O2 (a provider token count of the 1,248 prompts) needs its own written authorization and spending basis.
  > - **Not allowed meanwhile:** any provider token count; presenting characters as tokens.

- **Consequences (source):** APPROVE: a small read-only script that prints only numbers (ids, characters, tokens, B) and never response text; not written; requires the pilot to have run with usable `promptTokenCount`. It authorizes "any provider token count" never ("Not authorized by it"). REJECT: "the main-run token basis must be O2 or an owner entry accepting the assumption". O2 (a provider token count) needs its own written authorization and cost basis.
- **Dependencies:** completed pilot; MD-02 Q8 (recorded: O4, 12.47).
- **RECOMMENDATION — NOT AN OWNER DECISION:** consistent with the recorded Q8 = O4 (without P12 the O4 method has no tool).
- **Owner answer:** ______

## 6. MD-10 (confirmations of earlier choices)
- **Status:** OWNER CAN DECIDE NOW (owner part); WAITING FOR ADVISOR for finality (source: "ask for an advisor review of them before the FZ hash").
- **Decision question:** Do you confirm MD-10 with the replacement wording below (no number 14), or amend it?
- **Options (source):** "confirmed / amended: ______" (confirm, or amend with your wording).
- **Quotations:**
- `results_package_2026-10-13/MASTER_PROPOSED_DECISION_RECORD.md` line 187:

  > Text: "(PC-2) the pilot registry is built and gated at step 8; (I-6) informational diagnostic, gate counts stay 30 and 14; (P-3 item 1) `s2_values` 'none' is reported as a count outside its denominator; (F-3) closed; (PRD-8) unchanged; the Step 8 choices of record 12.28 (F-4 architecture, PG4 test, PG11a projection bundle of 624 files, A6b actor) are confirmed / amended: ______."

- `results_package_2026-10-13/ADVISOR_WRITTEN_REQUEST_v3_DRAFT_2026-10-15.md` line 108:

  > That sentence names a count "14" that no project source defines; the verified results in record 12.28 are "30 numeric gates" (main and pilot registers) and the rendering-stage gate list. **Owner-requested wording proposal (NOT adopted, NOT recorded, awaiting the owner's confirmation):** "(PC-2) the pilot registry is built and gated at step 8; (I-6) informational diagnostic, an informational count only (record 12.28), the gate results standing as reported in record 12.28 (30 numeric gates PASS on the generator's templates and on Implementation A's builders; PG1-PG10, PG11a, the PG11b builder test, PG12, A1b and A6b PASS on all 1,248 main and 96 pilot prompts); (P-3 item 1) `s2_values` 'none' is reported as a count outside its denominator; (F-3) closed; (PRD-8) unchanged; the Step 8 choices of record 12.28 (F-4 architecture, PG4 test, PG11a projection bundle of 624 files, A6b actor) are confirmed / amended: ______." Note: confirming would close F-3 (the record lists it as open) and leave PRD-8 unchanged; both are decisions, not findings. Answer requested: review of the Step 8 choices and of the wording; confirm / amend per item (amendment wording must come with the answer).

- `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` line 650:

  > | F-3 | 12.5: the gates use the `D_dist` and `tau_F` carried by the members; Q2 uses the register values; no gate relates the two | `build_pac_template` reads both from the register (`impl_a.py` around lines 412 to 419); Q9 compares them between members; the specification requires no relating gate | open, not a specification requirement | possible software defect only for hand-made data | at Step 8 the generator must take the values from the register; a register-versus-member consistency check belongs to Step 8 (not to the protected Step 4 code) |

- `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` line 656:

  > | PRD-8 | whether `E-EMPTY-TARGET` stays a hard rejection while OD-4 is open | OD-4 (2026-10-09) declares all 12 primary cells precision-targeted (DP1); FZ-v1 row 14 agrees | not applicable under the current declarations; formally pending in 19.3 | dependency note | none |

- **Verified basis for the replacement wording:** record 12.28 states "**I-6**: informational count only." and "All 30 numeric gates PASS on the generator's templates and on A's builders" and "PG1-PG10, PG11a, PG11b builder test, PG12, A1b, A6b PASS on all 1,248 and 96 prompts"; the Step 4 re-run (record lines 360-361) shows 30 of 30 for both registers. The number 14 is defined nowhere.
- **Consequences (source):** confirm: no artifact changes; an amendment of a Step 8 choice or I-6 as a gate changes `step8/s8_*.py` and/or the 624-file projection (rebuild).
- **Caveats checked (do not assume closure):** F-3: the record row (quoted) lists it as "open, not a specification requirement" with the next action "at Step 8 the generator must take the values from the register; a register-versus-member consistency check belongs to Step 8". Code fact: `step8/s8_construct.py` line 41 reads `D` and `tau_F` from the register and carries them into the members (lines 115-116); no separate register-versus-member consistency check was found in `step8/s8_gates.py`; record 12.28 does not mention F-3. So "F-3 closed" is the owner's decision, partly supported by the generator reading the register; whether a consistency check is still wanted is UNKNOWN. PRD-8: the row (quoted) is "not applicable under the current declarations; formally pending in 19.3"; "PRD-8 unchanged" leaves it pending and resolves nothing.
- **Dependencies:** advisor review (B6 in the v3 request, not sent); owner confirmation of the final wording.
- **RECOMMENDATION — NOT AN OWNER DECISION:** if you confirm, say explicitly whether "(F-3) closed" is intended given the caveat above, or amend that clause.
- **Owner answer:** ______

## 7. Q9 / P3b (enforce assumed tokens against prompt length)
- **Status:** OWNER CAN DECIDE NOW only as REJECT. APPROVE is `BLOCKED — SOURCE TEXT REQUIRED`.
- **Decision question:** Do you want the assumed-token gate (P3b)?
- **Options (source):** `[ ] APPROVE  [ ] REJECT`; C32-1 / C32-2 / C32-3.
- **Quotations:**
- `results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` line 104:

  > | Q9 | P3b | the assumed-token value stays unenforced |

- `results_package_2026-10-13/C31_C32_OWNER_DECISION_BRIEF.md` line 112:

  > Options: **C32-1** keep as is (the owner writes a value >= 1,016 by hand; not enforced); **C32-2** enforce `input_tokens_per_call_assumed` >= longest planned prompt in characters, with an explicit `input_token_basis` object accepted for a measured basis (patch P3b; the form of the basis must be decided first); **C32-3** require a token measurement before any paid call (an external call needing separate written authorization; not allowed in this batch). Recommendation [READING]: C32-1 is acceptable for the 18-call pilot if the authorization states the 1,016 assumption and the character limit in writing; before the main run a measurement method must be chosen (O2: provider count of the 1,248 prompts; or O4: maximum `promptTokenCount` of the pilot calls checked against all prompt lengths). The character limit stays an operational control: not a token measurement, not a cost guarantee, separate from the US$100 cap.

- `results_package_2026-10-13/C31_C32_OWNER_DECISION_BRIEF.md` line 116:

  > - **Q9.** If P3b is wanted, what exact fields define a "measured basis"?

- **Consequences (source):** REJECT: "the assumed-token value stays unenforced" (consistent with the recorded Q7 = C32-1). APPROVE (C32-2) requires "the form of the basis must be decided first"; "what exact fields define a 'measured basis'?" is unanswered anywhere: BLOCKED — SOURCE TEXT REQUIRED, so approval is not offered.
- **Dependencies:** MD-02 (approved 12.48).
- **RECOMMENDATION — NOT AN OWNER DECISION:** source text (C31 section 10): C32-1 "is acceptable for the 18-call pilot if the authorization states the 1,016 assumption and the character limit in writing".
- **Owner answer:** ______ (or supply the fields of a measured basis)

## 8. MD-09 (anchoring of the decision record; box P7)
- **Status:** WAITING FOR EVIDENCE. The owner deferred it (12.47). No new decision is available.
- **Quotations:**
- `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` line 942:

  > | 8 | MD-09 | OAP lines 63 and 165-168; H7: "own commit whose ID is recorded, or an external timestamped copy of the record's SHA-256" | **NO store chosen. The owner deferred the anchoring decision until the mechanism of an external timestamped copy of the SHA-256 of the decision record can be verified.** | Status stays **PENDING**. No commit, external copy, timestamp or anchoring evidence was made; box P7 is NOT approved. The source consequence stands: the decision script must not be run until the record is anchored, so the main run cannot start; the pilot is not affected. |

- `results_package_2026-10-13/HUMAN_TASKS_H1_H7_OPERATIONAL_CHECKLIST.md` lines 112-115:

  > - **Evidence.** The record entry (approver, date, store type and location).
  > - **Acceptance.** Entry exists before the decision script is run; later the recomputed record hash matches the anchored value.
  > - **Status.** NOT DONE.
  >

- `results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` line 106:

  > | P7 | the runner's anchor check | the anchor is a manual procedure |

- **Options (source):** "own commit whose ID is recorded, or an external timestamped copy of the record's SHA-256"; P7 APPROVE/REJECT.
- **Verification still missing (no source defines it; nothing here is verified):** for an external timestamped copy: which service or mechanism, how the SHA-256 is submitted, what shows the time and that it cannot be changed, who holds the proof, and how the later recomputed hash is compared (H7 acceptance: "later the recomputed record hash matches the anchored value"). For a commit: the repository state (`research_design/` is untracked), the branch and where the commit is kept; a local commit alone is not shown by any source to be write-once. These are `BLOCKED — SOURCE TEXT REQUIRED`.
- **Timing (source):** needed after the pilot and before the decision script; the pilot is not affected. P7 (runner anchor check) cannot be built before the store type is declared.
- **Owner answer:** none now.

## 9. H4-STOP (stop rule before H3)
- **Status:** WAITING FOR RESEARCHER/EVIDENCE and ADVISOR.
- **Question and options (source, exact):**
- `results_package_2026-10-13/HUMAN_TASKS_H1_H7_OPERATIONAL_CHECKLIST.md` line 91:

  > 8. **Stop rule before H3.** If any finding is class B or C, or you are unsure, do NOT create H3. Send the findings file to the owner and the advisor with this question: "(i) no change, the point is recorded as a limitation; (ii) a codebook revision (new Step 7 version, box R-7, rebuild sequence in `OWNER_APPROVAL_PACKAGE.md`); (iii) a question on the battery for the advisor." Nobody, including the assistant, edits the codebook or any manifest-bound file on the basis of the findings without that written decision. If there are no class B or C findings, H4 does not block H3. H1 does not depend on H4.

- **Why not now:** the researcher's note on the two `SW` cells (B10, B36) does not exist, and the advisor's answer (B4 in the v3 request, not sent) is outstanding. Consequence of (ii): a codebook revision (new Step 7 version, R-7, rebuild); H3 would be created against the new manifest.
- **Owner answer:** none now.

## 10. R-7 (authorize a Step 7 re-freeze)
- **Status:** RECORDED: NOT AUTHORIZED (12.48 row 4). Reopening is the owner's choice at any time; not a new question unless you wish it.
- **Options (source):** `[ ] APPROVE  [ ] REJECT`.
- **Quotations:**
- `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` line 957:

  > | 4 | R-7 (Step 7 re-freeze) | **NOT AUTHORIZED** | The owner does not authorize the Step 7 re-freeze. No re-freeze step, no inventory comparison and no 2,026-file hash comparison was performed. This is not a rejection of the K2 choice recorded in 12.47, which stands as the owner's decision; per the source, while R-7 is not authorized "MD-03 K2 cannot be applied", so the codebook, `s7_recode.py` and the manifests stay unchanged. |

- `results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` line 105:

  > | R-7 | Step 7 re-freeze | MD-03 K2 cannot be applied |

- `results_package_2026-10-13/OWNER_APPROVAL_PACKAGE.md` line 84:

  > **If K2, a narrowed PG11b or a codebook revision is adopted, the authorized sequence is:** (1) the formal decision and box R-7 (Step 7 re-freeze); (2) back up the affected Step 7 files and both manifests; (3) edit the files and run the Step 7 tests; (4) write a NEW Step 7 freeze manifest (the old one stays; `reproduce/make_step7_freeze_manifest.py` writes a new path only); (5) rebuild Step 8 with `step8/s8_build.py --out <NEW parent folder>` (the build folder is named by the registry hash, so an unchanged registry reuses the name and the tool refuses an existing target, exit 3); (6) `s8_verify.py`, `impl_b.py`, `test_impl_b.py` and the slow Step 8 suite on the new build; (7) compare the new manifest `inventory` with the old: every one of the 2,026 file hashes must be identical (then the registry, prompts and checker bundle are unchanged and a blind check already performed on the bundle stays valid); only the changed generator-code hashes and `step7_freeze_manifest_sha256` may differ; (8) record, in the closeout report, the old and new values of: Step 7 manifest sha (old `202979de2a88`), Step 8 manifest sha (old `09eed00eeb79`), each changed file (old `s7_recode.py` `ec8f948e6209`, codebook `25a74353be54`, `s7_bundle.py` `10567178b209`), spec `d5fcffadd104` and register `c7d50e115b08` (expected unchanged), and the inventory comparison result; (9) update every reference to the build path or manifest hash (gate `--build`, checklist T1, runbook); (10) only then create H3 against the NEW manifest. Any inventory difference means the registry changed: H1 must be redone. None of this is authorized yet; nothing frozen was modified.

- **What authorizing would permit (source):** the sequence (back up, edit the affected Step 7 files, new Step 7 manifest, rebuild Step 8, verify, compare the inventory of 2,026 file hashes, record, then create H3 against the new manifest). It does not by itself edit anything or run anything; each step needs a separate instruction. **Consequences:** if the inventory is identical a blind check already done stays valid; any difference means H1 must be redone; four lines of the approved 31-file list move (`s7_recode.py`, the codebook, the Step 7 manifest, the Step 8 manifest). If R-7 stays unauthorized: "MD-03 K2 cannot be applied" (K2 stays chosen, unapplied).
- **Dependencies not finished:** advisor concurrence for MD-03 ("Owner + advisor"); the codebook wording of K2 and tests to be written; MD-10 and B1 outcomes.
- **RECOMMENDATION — NOT AN OWNER DECISION:** analytic: keep NOT AUTHORIZED until MD-10, B1 and the advisor's concurrence on MD-03 are known, so that a rebuild is done once; the sources do not require that order.
- **Owner answer:** ______ (leave as recorded unless you decide otherwise)

## 11. H5 (pilot authorization file): an owner act, not a decision on this sheet
- **Status:** NOT A DECISION; NOT CREATED. The procedure allows the owner to write it once MD-02 / C-32 are answered; the pre-pilot checklist places it at its Phase 3, after the decision, freeze and evidence chains. This sheet does not create or fill it.
- `results_package_2026-10-13/HUMAN_TASKS_H1_H7_OPERATIONAL_CHECKLIST.md` lines 93-100:

  > ## H5 Owner authorization (pilot round 1)
  > - **Purpose.** The owner's written authorization read by the gate (`check_gates`).
  > - **Procedure.** The owner (not the assistant) copies `templates/owner_authorization_TEMPLATE.json` to a new file and writes: `authorized_by` = `owner`; `scope` = `pilot_round_1`; `max_calls` = 18; `cost_ceiling_usd` = 100; `input_tokens_per_call_assumed` = a positive integer chosen by the owner (the accepted Step 7 assumption is 1016, i.e. at least one token per character; it is an assumption, not a measurement; C-32); `max_input_characters` = a positive integer chosen by the owner (the longest planned prompt is 1,016 characters; a smaller value is refused by the preflight; a larger one is allowed). The note field is not read.
  > - **Inputs.** The owner's decisions on MD-02 / C-32 (Q7-Q9) and, if the owner so decides, on the cost basis.
  > - **Evidence.** The saved authorization file with its SHA-256 and the date the owner wrote it; the hard-cap figure printed by the gate preflight (about US$0.37 for 18 calls at 1,016 assumed tokens, `hard_cap_cost_usd`; a cost bound, not a forecast).
  > - **Acceptance.** Gate check without `--live` no longer lists the authorization reasons; the limit is a control on prompt length only, not a token measurement and not a cost guarantee.
  > - **Expected location.** `human_evidence/authorization/authorization_pilot_round_1.json`.
  > - **Status.** NOT DONE (only the invalid template exists).

- `results_package_2026-10-13/PRE_PILOT_ACTION_CHECKLIST_2026-10-14.md` line 33:

  > | 18 | Write the pilot authorization (H5) as a NEW file from the template: `authorized_by = owner`, `scope = pilot_round_1`, `max_calls = 18`, cost ceiling 100 | **[OWNER]** | `authorization.json` | does not exist |

- **The value the owner must write:** `input_tokens_per_call_assumed` = "a positive integer chosen by the owner", and "the gate reads only these fields"; the source says it is "an assumption, not a measurement" and that the owner "must state a value >= 1,016 by hand". No value is proposed, entered or assumed here.
- **Owner answer / date the file was written:** ______
