# X-6 and X-7: concrete options, evidence, consequences, and pilot-prerequisite readiness (2026-10-15)

**Preparation only. The owner has not chosen any value below; general approval of a conservative approach (2026-10-15) is NOT read as approval of any of these values.** Nothing here is recorded as a decision, and no frozen artefact was changed. Sources read in the repository: `OWNER_APPROVAL_PACKAGE.md` (rows 2-6, 10, 17), `ADVISOR_DECISION_BRIEF.md` (D2, D3), `MASTER_PREPILOT_RESOLUTION.md` (D3, D5), `MASTER_CONFLICT_INDEX.md` (C-02, C-08, C-09), `CODEBOOK_S2_S3_v1_DRAFT.md` section 5, spec v2.7 16.3 and 18.2, `STEP11_PREFLIGHT_2026-10-14.md`, `templates/owner_authorization_TEMPLATE.json`. Common rule for "bound" artefacts: a change to a Step 7 file triggers the Step 7 re-freeze (box R-7), a Step 8 rebuild with verification, new manifests, a different hash for the corresponding line of the 31-file final-freeze list, and H3 must be created after the rebuild. Advisor input is shown where the sources require or recommend it.

## X-6.1 MD-03 / K2 and D5 (one decision cluster: C-02 and C-09)
Evidence: spec 16.3 (agreement "reported per variable (percent agreement and Cohen's kappa)"; single-coder fallback "delayed intra-rater re-code ... limitation: no inter-rater reliability"); owner decision OD-3 ("no Cohen's kappa may be claimed"); records 12.21 row 6 and 12.24 decision 2 (delegated); codebook section 5 (sample max(20, ceil(0.20 x D_P)) per cell, 14 full days delay, columns `recode1_*`, raw agreement only, no kappa). Today `s7_recode.py` computes raw agreement only.
| Option | Meaning | Consequence |
|---|---|---|
| K1 | raw agreement only (as built); a recorded departure from the literal "reported ... Cohen's kappa" of line 1002 | no code change, no re-freeze, no rebuild |
| K2 | kappa reported, labelled intra-rater, with a rule for undefined cases | `s7_recode.py`, codebook 5.1/5.3 change; Step 7 re-freeze (R-7), Step 8 rebuild, new manifests; the 31-list hashes of the Step 7 files and of the Step 8 manifest change |
| K3 | K2 with a threshold | as K2, plus a threshold value to be chosen (not proposed) |
| K4 | amend the spec text | new methodology version |
D5 values (20 % with floor 20, 14 days, `recode1_*` columns) are delegated choices without empirical basis: confirm as written, or give other values (a changed value is a codebook change: bound). Advisor: the resolution file recommends that the values be approved by the advisor. Not decided.

## X-6.2 PG11b scope (brief D2)
Evidence: spec 8.2 rows PG11a/PG11b; record 12.26 item 2 (owner kept the literal text); `s7_bundle.py`; `test_step7.py` test D1 pt4; in-memory test: ordinary words ("CLEAR", "PAC", "(valid)") rejected.
Options: (a) keep literal; (b) scan names, directory names, skeleton and prompt part only; (c) scan response text only for machine-form patterns; (d) mask matches in the builder. Consequence: (a) none now, risk that S2/S3 coding is blocked (primary results unaffected); (b)-(d) new methodology version, spec 8.2 and `s7_bundle.py` change, Step 7 re-freeze before the FZ hash. Advisor: the brief asks for the advisor's choice. Not decided.

## X-6.3 D3: SF/UNP policy (brief D3, C-08)
Evidence: spec 13.4, 13.6, 13.8, 18.2; record 12.18 row 1, 12.24 decision 1, 12.26 item 1 (owner kept v2.7 as written); the amendment drafts named in the brief.
Options: L literal; C interim rule (SF first, SF reported beside the four proportions; current); P1 evaluable-call denominators plus a separate SF rate; P2 SF as a fifth class over planned calls; PF parse-first. Consequence: C none; P1/P2 amend spec 18.2 (new methodology version) and touch the decision script and report before the FZ hash; L and PF contradict 12.18 row 1. Advisor: the brief addresses the advisor. Not decided.

## X-6.4 MD-10
Evidence: `OWNER_APPROVAL_PACKAGE.md` row 6: confirm PC-2, I-6 informational (gate counts 30 and 14), P-3 item 1, F-3, PRD-8 and the Step 8 choices of 12.28 (F-4, PG4, PG11a bundle of 624 files, A6b); advisor review stated as part of the question. Options: confirm all; amend one (an amended Step 8 choice or I-6 as a gate changes `step8/s8_*.py` and/or the 624-file projection: rebuild). Advisor review: required by the question; not obtained. Not decided.

## X-7 Pilot prerequisites: readiness
| Prerequisite | Authority and rule | Evidence in the repository | Status | Safe next action |
|---|---|---|---|---|
| PRD-6 / H7 / MD-09 | owner declares the write-once store and the anchoring of the pilot decision record (package row 17; checklist item 15) | none | NOT DECLARED | owner: choose the store (the package suggests the owner's own commit); decision needed after the pilot and before the decision script/main run |
| MD-02 | owner confirms `max_input_characters` (1,016 proposed: verified maximum prompt length of the Step 8 build) and `input_tokens_per_call_assumed` (1,016 = one token per character, an assumption not a measurement) | template values; `test_input_limit.py` | WORKING DECISION ONLY | owner: confirm or change in writing |
| H5 pilot authorization | owner writes a NEW file from `templates/owner_authorization_TEMPLATE.json`: `authorized_by = owner`, `scope = pilot_round_1`, `max_calls = 18`, `cost_ceiling_usd = 100`, plus the two MD-02 values | the template is invalid while empty; no authorization file exists anywhere in the repository | NOT CREATED (the assistant creates none) | owner, after MD-02 |
| Step 9 evidence (H3) | evaluator output needing H1, seven full days after R1, H4 stop-rule clearance and the owner's written confirmation | none | NOT CREATED | see the R1 line below |
| Price and model re-read (B7/H6) | on the first paid-call day: compare current prices and model terms with FZ-v1 (input 0.30, output 2.50 US$ per 1M tokens); a difference is a stop-and-ask | stored constants only | NOT DONE; must be done on the pilot day, old data is not accepted | owner/researcher on the day |
| API key and terminal | owner puts the key into the environment of the terminal that runs the pilot, never into a file; disables sleep; stable power and network | `.env` does not exist | NOT DONE (assistant never handles it) | owner, last |
| Explicit pilot start (`--live`) | owner's explicit instruction | none | NOT GIVEN | owner |
| Code freeze | owner's dated declaration after all code-affecting decisions and a full check | none | NOT DECLARED | see order below |

## Waiting period (Step 9)
Rule: FZ-v1 row 19 and `HUMAN_TASKS_H1_H7_OPERATIONAL_CHECKLIST.md`: the blind check may be completed no earlier than R1 + 7 full days, where R1 is the true UTC time the researcher stopped viewing rendered registry content or expected states, written by the researcher as a new file in `human_evidence/clock/`. Verified 2026-10-15: that folder does not exist, so R1 is NOT RECORDED and the wait is NOT STARTED; no earliest date exists and none is computed. A template that is not evidence is at `templates/R1_clock_note_TEMPLATE.md`. H1: a blank worksheet exists (`step9_blind_check_kit/`), no filled worksheet, no `evaluation.json`. H3 stays blocked until H1, the seven days, the H4 stop-rule clearance and the owner's confirmation exist. H4 rehearsal: comparison and findings exist as documents; the researcher's classification (basis of `SW` on B10 and B36) and the advisor answers are open.

## Advisor items (sources actually present in the repository)
The file `H4_ADVISOR_DECISION_REQUEST_READY_2026-10-14.md` named in the checklist does NOT exist in the repository (searched on 2026-10-15). The questions under version control are `human_evidence/rehearsal/H4_ADJUDICATION_REQUEST.md` (items A-G and decision log), `H4_STATUS_AND_BLOCKERS_2026-10-14.md` (unmet prerequisites: the reading of "used" 12.39 row 1; sufficiency without a prompt 12.39 row 3; who decides 12.39 row 2; advisor review of PG3), `H4_NEXT_ACTIONS.md` section 5.2-5.3 and `ADVISOR_DECISION_BRIEF.md` (D1-D3 and following). The checklist's "Q1-Q5" correspond by topic to the first four H4 items plus the PG3 review; their exact original wording is NOT available, and none is invented here. Draft of the cover message: `MD08_OWNER_DECISION_PACKAGE_2026-10-15.md` section 5 (not sent). No advisor answer exists.

## Order
1. Owner records X-2 (classes), X-5 (P13) and the X-6 choices; any "not default" choice triggers the rebuild sequence. 2. Advisor answers the items above in writing. 3. Assistant applies only authorized changes, runs the full check, records the 31 hashes. 4. Owner declares the code freeze. 5. Researcher: R1 -> H1 -> 7 days -> H3. 6. Owner: PRD-6/H7, MD-02, H5 file; on the pilot day: price re-read, key, explicit start. 7. After a PASS record only: final freeze manifest.
