# Methodology and freeze record (2026-10-13)

**Status labels used.** FROZEN = in a frozen artefact whose hash is verified below. DECIDED = recorded owner decision (decision record `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md`), not specification text. DELEGATED = made by the assistant under the owner's delegation; subject to owner and advisor review. PREPARED = my resolution under the owner's instruction of 2026-10-13, **not applied to any repository file** (write access to `research_design/` was denied, see `01_EXECUTION_STATUS_REPORT.md` section 5). PROPOSAL = not adopted. Nothing in this file is advisor-approved.

## 1. Frozen and verified today

| Artefact | SHA-256 (prefix) | Result today |
|---|---|---|
| `SCENARIO_CONSTRUCTION_SPECIFICATION_v2_7_DRAFT.md` | `d5fcffad...ca8` | match |
| FZ-v1 register (recomputed, sorted compact JSON, `ensure_ascii=False`) | `c7d50e11...987a2` | match |
| `PARAMETER_FREEZE_MANIFEST_FZ_v1.json` | `14944571...` | match |
| `PARAMETER_JUSTIFICATION_RECORD_DRAFT.md` | `a1b21487...` | match |
| `METHODOLOGY_FREEZE_MANIFEST_v2_7.json` | `b93ff372...` | match |
| `implementation_a/` (5 files) | `impl_a.py` `daa2cd49...` | all equal to the FZ-v1 hashes |
| Step 7 manifest v4 (16 file hashes) | `5db81eac...` | 16/16 match; says NOT DECLARED FROZEN |
| Decision record | `61dd7a41...` | matches the baseline you gave; differs from the hash stored in the FZ-v1 manifest (`94fa64f9...`), a documented historical mismatch (the record is append-only and was amended after the freeze); not repaired |

Frozen design values (FZ-v1): K = 4, L_M = L_P = 26, 104 MIL + 208 PAC = 312 templates, 1,248 prompts, R = 2, 2,496 main call slots; pilot L_pilot = 2 (24 templates, 96 prompts, 18 calls); thresholds f_S = 1, theta_unp = 0.50, c_stop = 5, theta_main = 0.10, calls_min_main = 100; blind check coverage 100 %, minimum delay 7 days; model `gemini-3.5-flash-lite`, `thinking_level` minimal, `max_output_tokens` 8192, retries 0, timeout 180 s, delay 1 s, concurrency 1; cost limit US$100 (OD-10).

## 2. What is decided versus open

- DECIDED (owner): OD-1 to OD-10, PRD-4 (closed S2 relation list), PRD-10 Option A (bundle builders are in Step 7 and FZ), PC-1 Option E (coder opaque-ID layout), GAP-1 (pilot UNP share = UNP / all calls; SF and UNP counts disjoint), GAP-2 (FAIL-U takes precedence), GAP-3 (diagnostic code built in Step 7), ASCII whitespace in the verdict grammar, wording of `prompt_specification_v1.py` approved as written (approval is not a freeze), character bound accepted for OD-10 at Step 7.
- DELEGATED, advisor review pending: the delayed intra-rater re-code (20 % of each cell with a floor of 20, 14-day delay, hash-based selection, `recode1_*` columns, no kappa), the symbol-run tokenization rule.
- PROPOSAL, not adopted: P-1 (main-run handling of structural failures: Policy 1 evaluable denominators, Policy 2 five classes), P-2 (FZ hash contract), P-3 (specification text inconsistencies), P-4 (token measurement, needs an external call), I-6, F-3, F-4, PRD-5, PRD-6, PRD-8, PC-2.

**UPDATE (after the owner authorized writes and answered the three questions):** the resolutions A to D below were APPLIED as decision entries 12.26 and 12.27, codebook revision 5 and `STEP7_PROMPT_SPECIFICATION_FREEZE_MANIFEST_v1.json` (owner choices: keep v2.7 section 18.2; keep the PG11b scan literal; keep the delegated re-code values, no kappa). Section 4 was APPLIED as Step 8 (entry 12.28), plus one further clarification: PG3 "contiguous" is read as one changed span inside the target token (the strict reading would reject 90 of 104 MIL templates). The words PREPARED below are historical. Nothing is advisor approved.

## 3. The four Step 7 blockers: resolutions (smallest defensible, no new methodology)

The principle used: v2.7 is not amended, no proposal is promoted to a rule, and the freeze set contains only what the specification or a recorded owner decision requires.

**A. Structural failures (SF) and UNP.**
- Resolution: the specification text stands (section 18.2 unchanged). For the pilot, the recorded precedence applies (SF-only; UNP share over all calls; FAIL-U over FAIL-S; implemented in `s7_decision.py`). For the main run, the documented interim behaviour applies: an SF call stays in `n_calls`, is in none of the four numerators, the SF count and rate are reported beside the four proportions, and the proportions are not rescaled. Policy 1, Policy 2 and parse-first remain proposals.
- Rationale and evidence: `PROPOSED_AMENDMENT_18_2_DRAFT_v1.md` section 5 ("until a decision exists, the specification text stands") and P-1 "interim behaviour"; the literal section 12 aggregator (over all R calls) already treats an SF call as a non-match, so no estimator has to be invented.
- Deviation: none from v2.7. Known limitation: "the four proportions sum to 1" holds only when no SF call occurs.
- Outstanding approval: advisor and owner choice among Policy 1 / Policy 2 / interim, before the main run (not needed for Step 8 or the pilot).
- Effect on the freeze set: `s7_outcomes.py`, `PROPOSED_AMENDMENT_18_2_DRAFT_v1.md`, `PROPOSED_CLARIFICATIONS_AND_AMENDMENTS_DRAFT_v1.md` and the Policy 2 package are **not** in the freeze set.

**B. PG11b scan scope.**
- Resolution: keep the literal text (names, directory names and bodies, patterns PT1 and PT3 to PT8b, including model-authored response text). No code change.
- Evidence: specification section 8.2; `s7_bundle.py` (scan range at line 30, check at lines 80 to 98). A read-only experiment with synthetic strings showed that ordinary English such as "CLEAR", "(valid)", "class = A" is rejected, and that rebuilding cannot help (section 21.2 row 6).
- Deviation: none. Known risk: the post-run PG11b application check can stop S2/S3 coding (a secondary analysis; primary results are unaffected).
- Outstanding approval: advisor and owner decision on a narrowing (needs a methodology amendment), before the post-run coding, ideally before the FZ hash.

**C. Section 16.3 codebook conformance.**
- Resolution: codebook revision 5 (prepared text in `staged_step7_freeze/`) removes the stale sentence of section 1 that says the re-code columns, delay and statistics are "not yet specified", and adds a table listing every departure from the literal text of section 16.3 with its source: sample (20 % with a floor of 20 versus a possible "all"), delay (14 days; section 16.3 is silent), concealment, column name `recode1_*` versus `coder2_*`, and no Cohen's kappa versus "percent agreement and Cohen's kappa". OD-3 (owner, 2026-10-09) forbids claiming inter-rater reliability or kappa; it does not say that kappa must not be computed.
- Deviation from the literal text: yes, as listed; all are DELEGATED, none is advisor-approved.
- Outstanding approval: advisor review of the re-code values and a decision on kappa (not computed / computed with a "no reliability claim" label), before S2/S3 coding; ideally before the FZ hash because the codebook is an FZ item.

**D. Freeze-set composition.**
- Resolution: a new manifest that separates the **freeze set** (`prompt_specification_v1.py`, `s7_core.py`, `s7_parser.py`, `s7_refcheck.py`, `s7_decision.py`, `s7_diagnostic.py`, `s7_bundle.py`, codebook revision 5, both batteries, `s7_recode.py` with its flagged values) from **evidence** (`test_step7.py`, `s7_manifest_items.py`) and from **not in the freeze set** (`s7_outcomes.py`, the proposal documents, the Policy 2 package). The freeze act is the owner's instruction of 2026-10-13, recorded with the manifest hash; the manifest states the open advisor items and that a change to an item before the FZ hash means a new Step 7 version.
- Required evidence for the freeze: 145 existing tests plus new membership tests, hash reconciliation, and the pending human rehearsal of the codebook battery recorded as an open item (it is a pre-pilot requirement of section 13.5, and under OD-3 a model coder could only be a screening layer).
- Status: **not written**.

## 4. Step 8 choices PREPARED (not implemented; all are proposals until adopted)

F-4: independent construction code with Implementation A's gates imported unmodified (the specification gives the step 8 gates to A), tested for equal IDs, template parameters, gate verdicts and prompt bytes against A's builders; any difference rejects the build and is adjudicated by a person against the specification. Registry JSON: provenance and templates only, canonical JSON (sorted keys, compact separators, `ensure_ascii=False`, UTF-8) plus one final LF, hash = SHA-256 of the file bytes. Prompt hash: SHA-256 of the ASCII bytes. Pilot registry built and gated at step 8 with the same code; pilot selection by the rule of section 13.3. IDs distinguished by `registry_kind` and the registry hash. Output: registry, prompts, hashes, gate report, PG11a bundle, manifest; the call list is only cross-checked. I-6 informational. A6b computed at step 8 from rendered numerals with exact fractions and repeated by Implementation B at step 9. PG4 derived from PG3, PG7 to PG9 and PG12. All-or-nothing build in a temporary folder with one rename to publish; failures logged in a separate file; interpreter version recorded, not enforced. No model or token-counting call. None of this has been written or run.

## 5. Deviations register

| # | Deviation or limitation | Source | Status |
|---|---|---|---|
| 1 | Re-code is a sample, 14-day delay, `recode1_*`, no kappa | 12.24 decision 2 | DELEGATED, advisor pending |
| 2 | "Four proportions sum to 1" fails when an SF call occurs | section 18.2 under the interim rule | open advisor choice |
| 3 | PG11b can reject ordinary response text | section 8.2 as written | open advisor choice |
| 4 | Single LLM-assisted coder for Stage 2; no human second coder | Stage 2 limitation | recorded |
| 5 | Stage 1 used 60 call attempts (30 failed on another model ID) | Stage 1 run history | recorded |
| 6 | Pilot study model (`gemini-3.1-flash-lite`) differs from the v2.7 model (`gemini-3.5-flash-lite`) | manifests | recorded |
