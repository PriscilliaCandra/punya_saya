# Policy 2 methodology decision package - DRAFT v1

**DRAFT FOR OWNER AND ADVISOR REVIEW — NOT ADOPTED — NOT FROZEN**

Nothing in this document is a decision, an amendment of specification v2.7, an entry of the decision record, or an instruction to change
code. Every statement marked CANDIDATE is a proposal. Every statement marked FROZEN quotes `SCENARIO_CONSTRUCTION_SPECIFICATION_v2_7_DRAFT.md`
(sha256 `d5fcffad...082ca8`). Statements about the decision record (12.18, 12.24, 12.25) are statements about owner clarifications and
delegated proposals, which are not specification text. The author of this package also wrote the draft code, tests and earlier proposals,
so no independence is claimed.

Scope note: the request that defined this package was cut off in the middle of its list of worked examples (after "5. One satisfied call plus
one planned but..."). The remaining cases of section 10 were taken from the preceding Policy 2 consistency audit.

---

## 0. Baseline at the time of writing

Branch `master`, HEAD `224d9101f3737bf5d5057b2cb8835ddea037a860`, 31 status lines. Specification `d5fcffadd1045fc0c86a7c84eb8d51592d807576b6a51b712cef025164082ca8`;
FZ-v1 register (recomputed) `c7d50e115b08b6d70b9c35f1d09183118c3d2aaffa89b1c838987f7ab73987a2`; FZ-v1 manifest `14944571...`; PJR `a1b21487...`;
decision record `61dd7a41...`; Step 7 manifest v4 `5db81eac...`; the three snapshots and `implementation_a/` unchanged. This file is not listed in
manifest v4 and has no hash recipe; it is outside the Step 7 hash set until the owner decides otherwise.

Sources read for this package: FROZEN sections 0.1, 2.2, 9.5, 9.7, 10, 12 (aggregation, 12.1, 12.2 DP1-DP9, 12.3), 13.4, 13.6, 13.7, 13.8, 16
(coded population, 16.1-16.3), 18.2-18.4, 20 (TH16), 22 item 6; decision record 12.18, 12.24, 12.25; `PROPOSED_AMENDMENT_18_2_DRAFT_v1.md`;
`s7_outcomes.py`; `s7_decision.py`; the PJR rows on the pilot thresholds; the Policy 2 consistency audit.

---

## 1. Vocabulary: units that must not be interchanged

A call can be in exactly one of the following **ledger states**. The frozen text defines only the first and the "recorded" notion in part.

| State | Meaning | Frozen basis |
|---|---|---|
| **Planned** | a (template, condition, repetition) triple of the canonical call list | 10; 9.7 (`Calls = 4*R*N_tpl`) |
| **Never attempted** | planned, no request was ever issued | not defined (13.8 speaks of "completed calls") |
| **Attempted, no record** | a request may have been issued; no result was stored | not defined; FROZEN 2.2: "Call: One model invocation: one request, one stored response." |
| **Recorded** | a result (a response or a failure event) is stored | 13.8: "completed calls remain recorded" |
| **Classified** | recorded, and the frozen code has assigned its flags and primary class | 13.4 (flags), this package (class) |

Derived sets over **recorded** calls:

| Set | Definition |
|---|---|
| **SF call** | meets at least one of SF1-SF5 (FROZEN 13.4) |
| **Non-SF call** | recorded and meets none of SF1-SF5 |
| **Call with a parseable verdict** | the stored response text parses, under the frozen grammar of 13.4, to `satisfied`, `violated` or `unclear` (computed by code on the stored text; an SF3 call can have one) |
| **Unparseable call (UNP)** | a non-SF call whose response has zero Verdict matches, conflicting tokens or a token not allowed |
| **Unclear call** | a non-SF call that parses to `unclear` |

Mapping to the units named in the request: *planned*; *executed* = attempted (an "attempt" is the only executed notion a ledger can observe, see
section 6.4); *calls with a successfully stored response* = recorded and not SF1/SF4; *structurally failed* = SF call; *parseable verdict*,
*unparseable*, *unclear* as above; *never executed* = never attempted; *executed but not recorded* = attempted, no record.

---

## 2. Primary estimand (CANDIDATE)

### 2.1 Target
The preferred target is overall system performance over the **planned** calls, operational failures included. FROZEN 18.2 already keeps
`unclear` and unparseable in the denominator; the candidate extends the same idea to structural failures.

**CANDIDATE E1.** For a reporting cell and a class `k` of the five primary classes (section 3), `theta_k(cell)` = the cluster-level mean of the
within-cluster proportion of **planned** calls whose primary class is `k`. In symbols, with `n_{t,k}` the number of the `R` planned calls of
template `t` (in the cell's condition) in class `k`: `p_{t,k} = n_{t,k} / R`; `h_{b,k}` = mean of `p_{t,k}` over the templates of cluster `b` in the
cell; `theta_k` = mean of `h_{b,k}` over the `L` clusters. This is the frozen estimator of `p_t(c)`, `h_b` and the cell estimate (FROZEN 12,
"Cluster-level aggregation") applied to five classes instead of one "match" class.

### 2.2 What is identifiable
| Execution | Identification of `theta_k` |
|---|---|
| **Complete cell** (every planned call recorded and classified) | **Point identified.** By cluster integrity (A7, 9.5) every cluster has the same number of templates in the cell, so `theta_k` equals the pooled planned-call proportion `N_k / N_plan`; the five proportions sum to exactly 1. Uncertainty about the population of bases is handled by the frozen cluster bootstrap (DP8). |
| **Incomplete cell** (`U` planned calls without a recorded class) | **Only partially identified.** With no assumption, `N_k / N_plan <= theta_k <= (N_k + U) / N_plan` (exact bounds). A point value needs an assumption about the `U` calls. |

The assumption that the unrecorded calls resemble the recorded ones is **not supported by the frozen design** in general: the execution order is
a random shuffle (10), which makes the never-attempted calls of a run that stopped for a content-independent reason an exchangeable subset, but
the frozen halt rules (13.8) stop the run **because of structural failures**, so the recorded prefix is selected by outcomes. Executed-but-lost
records are exchangeable only if raw persistence precedes any content-dependent processing (section 6.4). The direction and size of any bias are
not known before data and are not claimed here.

### 2.3 CANDIDATE reporting behaviour for an incomplete cell
Report, for the cell and for each class: planned, never-attempted, attempted-no-record, recorded and classified counts; the recorded-call
distribution **labelled as conditional on recording**; and the exact bounds above. Do **not** report a point estimate of `theta_k`, a bootstrap
interval or a contrast that uses the cell as if it were complete. This follows FROZEN 13.8 ("reported as incomplete with the number of completed
calls per cell, cells with fewer calls than planned keep their achieved counts, and nothing is pooled with a later run") and invents no estimator.
Decision required before the experiment: section 12, D-6.

---

## 3. Primary outcome classification (CANDIDATE)

### 3.1 Terminology
The frozen text uses the verdict tokens `satisfied`, `violated`, `unclear` (13.4), the word "unparseable" with code UNP (13.4, 18.2) and the code
SF with SF1-SF5. The conceptual labels of the request (`SATISFIED`, `VIOLATED`, `UNCLEAR`, `UNPARSABLE`, `STRUCTURAL_FAILURE`) are not used in the
specification; this package keeps the frozen spelling to avoid a second vocabulary: **`satisfied`, `violated`, `unclear`, `unparseable`,
`structural failure`**. (The all-caps labels are internal analysis terms and never enter a prompt; note that PT4 forbids all-caps `MIL`, `PAC`,
`MILD`, `CLEAR` in prompts, not these words.) Role names in 18.2 stay: in a valid-plan cell `satisfied` is the match and `violated` the false
positive; in a violating-plan cell `violated` is the match and `satisfied` the false negative.

### 3.2 A total, deterministic classification function
For each recorded call let `F` be its set of SF flags (computed from provider metadata and the stored text by frozen code) and `V` its parse
outcome under the frozen grammar of 13.4 when a response exists.

**CANDIDATE class function.** `class(call) = structural failure` if `F` is not empty; otherwise `class(call) = V`, one of `satisfied`,
`violated`, `unclear`, `unparseable`.

Totality: a recorded call with `F` empty has a response (the absence of a response is covered by SF1 or SF4, on the assumption that the provider interface reports every response-less outcome as a transport error, a block or "no candidate"), so `V` is defined. A stored
record that has neither a response nor SF1/SF4 is malformed and is treated as *attempted, no record* (section 6). Exclusivity: the function returns
one value. Hence the five classes **partition the recorded calls and sum to exactly 1** at call, template, cluster and cell level; because every
template vector sums to 1, any weighted mean of template vectors does as well.

### 3.3 Non-exclusive diagnostic flags
The flags SF1-SF5 stay available as **diagnostic indicators**, one per call and code, not exclusive. They are reported with the number of calls
carrying each flag, the number of calls with two or more flags, and the exclusive total; **per-type counts may therefore sum to more than the
exclusive total** and must be labelled non-exclusive. They are never used as a second partition.

---

## 4. Structural-failure precedence (CANDIDATE, to be evaluated, not adopted)

### 4.1 Candidate
Any call with a flag SF1-SF5 is `structural failure` in the primary classification: SF2, SF3 (also with a parseable partial verdict), SF5, SF1
and SF4 alike. This is **SF-only precedence**.

### 4.2 Comparison with the alternatives
| | SF-only (candidate) | Parse-first | Flags + explicit class table |
|---|---|---|---|
| SF2 (empty) | structural failure | unparseable (zero matches) | per table |
| SF3, no verdict | structural failure | unparseable | per table |
| SF3 with a parseable verdict | structural failure | the parsed class | per table |
| SF5 | structural failure | structural failure when parsing did not run, else parsed class | per table |
| Class "structural failure" equals the calls counted by the 13.8 monitor | **yes** | no (SF2/SF3 become flags only) | depends |
| Same rule can serve pilot and main run | **yes** | no | depends |

### 4.3 Compatibility with the frozen pilot rules
FROZEN 13.6: PASS needs "no SF2, no SF3, no SF5; SF1 + SF4 <= f_S; UNP share <= theta_unp"; FAIL-S is any SF2, SF3, SF5 or `SF1 + SF4 > f_S`;
FAIL-U is "UNP share > theta_unp" and means STOP-U, with "no re-pilot of the unchanged protocol". The frozen text does not say whether an empty or
truncated response counts toward the UNP share; the owner clarification 12.18 row 1 (not specification text) says it does not.

**The choice changes a frozen outcome.** Example: a pilot round of 18 calls with 10 empty responses (SF2). If empty responses were also UNP
(literal reading of "zero Verdict matches"), the UNP share is 10/18 = 5/9 > 1/2 and the round is FAIL-U, hence STOP-U. Under SF-only precedence the
UNP share is 0 and the round is FAIL-S, the recoverable branch (SF2: a pure implementation fix, H1-H4). SF-only precedence is therefore
**consequential for the pilot**, and it must be written into the specification (section 11, A-1) for the pilot and the main run alike. The
candidate matches the clarification already applied by `s7_decision.py` (disjoint counts) and the halting monitor of 13.8, which counts SF1-SF5
per call. Parse-first would make the main run and the pilot differ, and would turn some pilot FAIL-S cases into FAIL-U.

### 4.4 Counting convention (clarification needed)
`SF1 + SF4 <= f_S` (13.6) adds two counts. The PJR (J-10) describes `f_S = 1` as tolerating "one transport or block failure in 18 calls", i.e. a
per-call meaning. CANDIDATE: count **calls** (a call carrying both SF1 and SF4 counts once), and count a call as "hard" if it carries any of SF2,
SF3, SF5. This needs one sentence in 13.6.

### 4.5 Multiple SF flags on one call
For the **primary** class no ordering is needed: the class is `structural failure` however many flags are set. If the advisor wants an
**exclusive per-type table**, a deterministic "primary SF type" must be frozen before any data. CANDIDATE order, by the sequence of the pipeline
and cause before symptom: SF1 (request failed) > SF4 (blocked or no candidate) > SF3 (token limit) > SF2 (empty) > SF5 (exception after a
response exists). The cause-before-symptom placement of SF3 before SF2 matters because an empty response whose finish reason is the token limit
(reasoning tokens consume the limit) would otherwise be reported as "empty". The order is a convention without empirical basis; flags-only
reporting needs no convention and is the recommendation.

### 4.6 SF3 with a parseable verdict
Primary: `structural failure` (never also `satisfied`/`violated`/`unclear`). The partial verdict is stored as a **diagnostic field**
(`satisfied`, `violated`, `unclear` or none) and counted in the diagnostics. It is not a second primary distribution and not an added sensitivity
(section 9). Risk to be stated: the verdict precedes the comments, so a cut-off inside the comments discards a valid verdict; the frozen pilot
(any SF3 fails the round) and the output limit (OD-9) are the safeguards, and SF3 is expected to be rare after a PASS. This expectation is not
evidence.

---

## 5. Execution cases A-D (CANDIDATE reporting rules)

| | A. all planned calls executed and recorded | B. a planned call never attempted | C. attempted, response/result not recorded | D. recorded response, parser/scorer fails |
|---|---|---|---|---|
| Observed | complete record | no request, no record | a ledger intent, no outcome (or no ledger entry at all) | stored response; exception in parser or scorer |
| Primary class | the class function | **none** | **none** | `structural failure` (SF5) |
| SF-rate numerator / denominator | numerator if SF; denominator = planned (= recorded) | in neither | in neither | numerator and denominator |
| Primary outcome denominator | yes | **not in the recorded denominator; counted as unknown (U)** | same as B | yes |
| `p_t` defined | yes | defined only if all R calls of the template-condition are classified; otherwise `UNDEFINED UNDER CURRENT TEXT` | same as B | yes |
| `h_b` | yes | `UNDEFINED UNDER CURRENT TEXT` if any template is undefined | same | yes |
| Cell estimate and bootstrap interval | yes (DP8 unchanged) | **not defined** for the cell | **not defined** for the cell | yes |
| Must be reported | counts | planned, never attempted, recorded; exact bounds; cell marked incomplete (13.8) | the same, with the attempted-no-record count shown separately | SF5 count and the structural report of 13.6.1 (activity A only) |

Nothing in B or C is classified as SF, UNP or a non-match. A never-attempted call is not an observed event of a call, and SF is defined for
completed calls and feeds the halting thresholds (13.8); mixing the two would change the halting behaviour. A lost record cannot be an SF flag
because the flags need an observable event.

### 5.1 Distinguishing B from C: the smallest ledger requirement (implementation-independent, CANDIDATE, not implemented)
1. **Intent before request.** Before each request an append-only entry (call index, triple) is written.
2. **Raw before processing.** After the request returns or fails, the raw provider result (or the failure event) is stored **before** any parsing,
   scoring or other content-dependent step, so that a processing failure is a recorded SF5 and not a lost record.
3. **Classification last.** The flags, the parse outcome and the class are computed by frozen code and appended.
4. **Tamper evidence.** Entries are chained by hash; the final ledger hash is stored in the run manifest.
5. **Completeness check.** Counts of planned, intent, raw and classified entries are compared at the end; a mismatch marks the cell incomplete.

Limit: an intent entry without an outcome cannot tell "crash before the request was sent" from "sent, response lost". They are one category
(attempted, no record) unless external provider logs say otherwise. Without any ledger B and C are indistinguishable and C is
`UNDEFINED UNDER CURRENT TEXT`.

---

## 6. Template, cluster and cell estimators

### 6.1 Complete templates and cells: no change
For a complete template `p_{t,k}` is as in section 2.1. The planning bounds of 12.1 use only that `h_b` is in [0,1] and `ctr_b` in [-1,1]
and hold for every class. DP8 (resample clusters, each bringing all its templates and all their `R` calls) is defined because every `h_b` is
defined. The frozen statement "equal to the pooled template mean under exact balance" remains true.

### 6.2 Incomplete templates and clusters: what the frozen text does not define
FROZEN: `p_t(c)` is "(calls whose verdict equals the ground truth) / R over **all R calls**". With fewer than `R` classified calls the
quantity cannot be formed: `UNDEFINED UNDER CURRENT TEXT`. A template with no classified call is 0/0. `h_b` over a cluster with an undefined
template is undefined; DP8's "all their R calls" cannot be satisfied. The equal-weight mean of template scores no longer equals the pooled
mean once denominators differ: in the example of section 10.7 four candidate cluster values are 1/2, 3/4, 2/3 and 1/2, all arguably "the cluster
mean". A resample of `L = 26` clusters contains at least one undefined cluster with probability about 0.639 if one cluster is undefined and 0.875
if two are.

### 6.3 Options
| | Option 1: counts and bounds only | Option 2: predefined complete-case estimator | Option 3: another estimator (available-case, equal template weights) |
|---|---|---|---|
| Estimand | the planned-call estimand is **not claimed**; bounds are reported | average over the **complete clusters** only | the recorded-call distribution, cluster-structured |
| Research question | answered descriptively for that cell | answered for a subpopulation that may differ from the planned bases | answered for recorded calls; equals the planned estimand only under an ignorability assumption that halts violate |
| Cluster weighting | none | equal over complete clusters | equal template weights with unequal call counts: templates with one call weigh as much as templates with `R` |
| Effective cluster count | not applicable | `L'` = number of complete clusters (random) | `L'` = clusters with a defined `h_b` |
| Confidence interval | none | bootstrap over complete clusters, conditional on completeness | cluster bootstrap with a rule for undefined clusters; variance depends on call counts |
| Contrasts | undefined for incomplete cells | clusters complete in both cells only | clusters defined in both cells only |
| Assumptions | none beyond the ledger | completeness unrelated to outcomes | non-recording ignorable; call-count heterogeneity ignorable |

Practical size of Option 2 (illustration, assuming each planned call is recorded independently with probability `f`; independence is an
assumption): a MIL valid-plan cell has 8 calls per cluster (K*R), so the chance that a cluster is complete is `f^8` = 0.923, 0.663, 0.431 for
`f` = 0.99, 0.95, 0.90; a claim contrast needs two cells (16 calls: 0.851, 0.440, 0.185); a PAC claim contrast needs 32 calls (0.725, 0.194,
0.034). With `f = 0.95` about 17 of 26 clusters would remain in one MIL valid cell. A complete-case estimator therefore discards most of the
information as soon as the run is not complete, and the retained clusters are selected by completeness.

### 6.4 CANDIDATE recommendation for advisor review: **Option 1**
Reasons: (i) without assumptions the planned-call estimand is not identified, and the most likely cause of an incomplete cell, a halt triggered
by structural failures, is outcome-dependent; (ii) Option 2 degenerates quickly and changes the target population; (iii) Option 3 changes the
weighting principle (the frozen "equal to the pooled mean" property is lost) and needs an unverifiable ignorability assumption; (iv) the design is
built for a complete run (retries 0, no replacement, a pre-declared call list) and 13.8 already says an incomplete run is reported as
incomplete; (v) the rule is fixed **before** any data, so no estimator is chosen after seeing which calls are missing. The cost is that an incomplete
cell yields no inference; the advisor may add Option 3 as a pre-declared, labelled **descriptive** table, which this package does not recommend as
a primary output.

If an unrecorded executed call (case C) is judged an engineering fault that should not invalidate a cell, the alternative is a **void-and-resume
rule**: a call with an intent entry and no outcome is declared void and re-executed once under the identical FZ version, with the reason logged.
Its justification is exchangeability of an unobserved stateless call; it is valid only if raw persistence precedes any content-dependent
processing (section 5.1, item 2), otherwise a content-dependent crash would be hidden by the re-run. It needs an amendment of 13.8 ("no
completed call is replaced"); it is not proposed here as a default.

---

## 7. Secondary S2/S3 coding population (CANDIDATE)

FROZEN: "Only **parseable** responses (a `Verdict:` parsed under 13.4) are coded; UNP responses are counted and excluded"; `D_P(c)` = parseable
calls in condition `c`; every S2/S3 table reports `D_P(c)`, the UNP count and the UNP share (16, TH16). Activity C of 13.6.1 builds the coder bundle
from "the redacted Comments of parseable responses". S-RQ5 asks about S2 and S3 "by condition and by verdict correctness".

Under five primary classes "parseable" is ambiguous for an SF3 call that parses. CANDIDATE eligibility, stated as separate sets:

| Set | Definition | S2/S3 coding |
|---|---|---|
| Primary performance distribution | all planned calls with a class (complete cell) | not coded |
| Calls with a parseable verdict | verdict parses, structural failure or not | superset, used for diagnostics only |
| **Coding-eligible calls** | recorded, **non-SF**, primary class `satisfied`, `violated` or `unclear` | **coded** (`D_P(c)` is redefined as this count) |
| Enough recorded text | the Comments field is absent or empty: coded `NC` (an existing code, included in `D_P(c)`); no further exclusion by text length | no separate exclusion |
| SF calls with a parseable partial verdict | recorded, SF, verdict parses | **not coded**; counted and reported beside the tables, with SF counts and UNP counts |

Reasons: S-RQ5's "verdict correctness" needs a primary verdict class, which an SF call does not have; truncated comments are incomplete material;
the disclosure of TH16 extends naturally to SF. The advisor may prefer to code the SF3-partial calls as a separate stratum, never pooled with the
non-SF calls. The parseable status is computed by code on the stored text (the frozen reference checker), never by a person reading
pilot or main responses. The delayed intra-rater re-code (16.3, OD-3; sample 20 percent with floor 20, 14 days, hash-based selection, `recode1_*`
columns, delegated and pending advisor review) is unchanged; **no inter-rater reliability and no Cohen's kappa is claimed** (OD-3).
OD-6 (the operational definitions of S2 and S3) is unaffected.

---

## 8. Sensitivity analysis

FROZEN 18.2: "**Sensitivity (one, predeclared, secondary):** all proportions recomputed with parseable-only denominators (`n_calls - unparseable`),
shown in a separate table labeled 'sensitivity'; it never replaces the primary figures."

Is `n_calls - unparseable` coherent under five classes? It is a well-formed number but its meaning changes: it removes the model's format failures
and keeps infrastructure failures in the denominator as non-matches.

| Candidate | Denominator | Estimand | Excluded |
|---|---|---|---|
| S-A (literal extension) | planned calls minus `unparseable` | match proportion among calls that are not unparseable, structural failures counted as non-matches | unparseable only |
| **S-B (CANDIDATE)** | `satisfied + violated + unclear` | accuracy among structurally valid calls with a parseable verdict: the intent of "parseable-only" | structural failures and unparseable |
| S-C | calls with a parseable verdict, SF3-partial included | accuracy among parseable verdicts, crediting partial verdicts of truncated calls | SF1, SF2, SF4, SF5-without-token, unparseable |

CANDIDATE: S-B replaces the wording of the single sensitivity (it does not add a second one); the SF3-partial count is a diagnostic, not a
second sensitivity table. S-A is not recommended because its estimand mixes two kinds of exclusion. S-C is defensible if the advisor wants
partial verdicts credited. The denominator is defined only for complete cells; for an incomplete cell the sensitivity is not reported. The
frozen wording is not edited here; proposed wording concept: "parseable-only denominators: the calls whose primary class is satisfied, violated
or unclear".

---

## 9. Compatibility with the other frozen mechanisms

- **Halting rule (13.8):** the share of SF1-SF5 over completed calls equals the share of the class `structural failure` under SF-only
  precedence. No change to `c_stop`, `theta_main`, `calls_min_main`.
- **Cluster integrity A7, call counts 9.5, 9.7:** unchanged; a cell contains `templates x R` planned calls.
- **Pilot decision script:** `s7_decision.py` already treats SF counts and UNP as disjoint, counts calls and refuses a wrong call count. It
  needs the counting sentence of section 4.4 written into the specification, not new logic.
- **`s7_outcomes.py`:** implements Policy 1 (pooled counts over non-SF calls) and refuses incomplete cells; it would have to be replaced by
  the five-class calculation. This package does not modify it.

---

## 10. Worked examples (exact arithmetic; `R = 2`; SF-only precedence; no rounding)

"Sum" is the sum of the five class proportions of the template.

| # | Calls (planned `R = 2`) | satisfied | violated | unclear | unparseable | structural failure | Sum |
|---|---|---|---|---|---|---|---|
| 1 | complete: `[satisfied, violated]` | 1/2 | 1/2 | 0 | 0 | 0 | **1** |
| 2 | empty response (SF2) + `satisfied` | 1/2 | 0 | 0 | 0 | 1/2 | **1** |
| 3 | SF3 with a parseable `satisfied` + `violated` | 0 | 1/2 | 0 | 0 | 1/2 | **1** |
| 4 | one call with SF2 and SF3 + `unclear` | 0 | 0 | 1/2 | 0 | 1/2 | **1** |
| 5 | `satisfied` + one planned call never attempted | see below | | | | | |
| 6 | `satisfied` + one attempted call with no record | see below | | | | | |

- **2:** without a precedence rule the empty response would also be unparseable by the literal 13.4 definition, giving 1/2 + 1/2 + 1/2 = **3/2**.
  With SF-only it is one class.
- **3:** the same call counted both as `satisfied` and as structural failure would give **3/2**. The diagnostic field records "partial verdict:
  satisfied" for 1/2 of the template's calls; under S-C that 1/2 would be credited.
- **4:** non-exclusive flags: SF2 1/2 and SF3 1/2 (flags sum to **1**, above the exclusive class 1/2); calls with two or more flags 1/2. An
  *exclusive* per-type split is `UNDEFINED UNDER CURRENT TEXT` (no order is defined; section 4.5 gives a candidate order).
- **5 and 6:** one call has a class (`satisfied`), the other has none. The frozen `p_t(c)` over all `R = 2` calls is `UNDEFINED UNDER CURRENT TEXT`.
  Dividing by `R` would make satisfied 1/2 and the sum **1/2** (the missing call silently a non-match); dividing by the one recorded call makes
  satisfied 1 and the sum 1 but describes a conditional quantity. Exact bounds for the planned-call proportion: satisfied [1/2, 1]; each other
  class [0, 1/2]. Case 5 and case 6 are identical in the bounds and differ only in the ledger (never attempted vs attempted, no record).

### 10.7 A cluster containing an undefined template
Cluster `b` = `{t1 = [satisfied, violated], t2 = [satisfied, not recorded]}`, match class `satisfied`.
- FROZEN text: `p_{t1} = 1/2`, `p_{t2}` = `UNDEFINED UNDER CURRENT TEXT`, so `h_b` = `UNDEFINED UNDER CURRENT TEXT`.
- Candidates that are **not in any text**: missing counted as non-match: `h_b = (1/2 + 1/2)/2 = 1/2` (the vector of `t2` sums to 1/2); recorded
  denominators, equal template weights: `(1/2 + 1)/2 = 3/4`; recorded denominators, weights by recorded calls: `2/3`; undefined template dropped: `1/2`.
  Four plausible values, three distinct numbers. This is why Option 1 refuses to choose.
- Bootstrap: with one undefined cluster of `L = 26`, a resample contains it with probability `1 - (25/26)^26` = 0.6393; with two, 0.8752.

### 10.8 A cell with unknown calls (counts and bounds)
Planned 8; recorded 6 (satisfied 3, violated 1, unclear 1, unparseable 0, structural failure 1); never attempted 1; attempted, no record 1; so
`U = 2`. Recorded-call distribution (conditional): 1/2, 1/6, 1/6, 0, 1/6, sum **1**. Exact bounds for the planned-call proportions: satisfied
[3/8, 5/8], violated [1/8, 3/8], unclear [1/8, 3/8], unparseable [0, 1/4], structural failure [1/8, 3/8]. The lower bounds sum to 3/4 = 6/8 and
every upper bound adds 2/8, so the planned-call distribution is not reported as a point.

---

## 11. Amendments that Policy 2 would need (none is made here)

All items need the **owner and the advisor**, and a new methodology version (13.2, 21.2). "Frozen" means v2.7 today.

### Necessary
| # | Clause | Current frozen rule | Unresolved ambiguity | Wording concept | Methodological consequence |
|---|---|---|---|---|---|
| A-1 | 13.4 | SF1-SF5 and UNP defined separately; "UNP ... remains in every denominator" | no precedence; SF2/SF3 also meet the UNP definition; SF3 with a verdict; several flags | a total classification function: any SF flag gives the class `structural failure`, otherwise the parse outcome; flags kept as non-exclusive diagnostics; calls with no record are outside the classification | five exclusive classes; pilot and main run use one rule |
| A-2 | 13.6, 13.7, 13.8 | counts `SF1 + SF4`, UNP share, monitor over "completed calls" | per call or per flag; what "completed" includes | count calls; UNP share excludes SF calls; "completed" = recorded and classified; the monitor share equals the class share | removes the STOP-U vs FAIL-S ambiguity (section 4.3) |
| A-3 | 18.2, 22.6, 0.1 | four proportions over `n_calls`, "sum to 1", sensitivity `n_calls - unparseable` | no class for structural failure | five proportions over the planned calls of a complete cell; SF rate is one of them; sensitivity restated (section 8) | all-call estimand with failures visible |
| A-4 | 2.2, 13.8, 10 | a Call is one request and one stored response; incomplete runs reported with achieved counts | planned vs attempted vs recorded; completeness; lost records | define the five ledger states, the completeness criterion, the reporting of incomplete cells (counts and bounds), and the ledger requirement of section 5.1 | Cases B and C become distinguishable and reportable |
| A-5 | 12 aggregation, DP8 | `p_t` over "all R calls"; bootstrap brings "all their R calls" | fewer than `R` classified calls | state that the cluster estimator and the bootstrap are defined for complete cells only; incomplete cells follow A-4 | no silent imputation; no interval for incomplete cells |
| A-6 | 16, TH16, 13.6.1 activity C, S-RQ5 | coded population = parseable responses | SF3 with a parseable verdict; "verdict correctness" for SF calls | eligibility table of section 7 | S2/S3 denominators stay interpretable |

### Optional clarifications
- 18.4 S-RQ1 to include the structural-failure rate; 18.2 role names for the fifth class.
- A new threat in 20: structural failures may depend on scenario, condition or answer length (for example a claim block changing output length); conditioning on non-SF calls is not done in the primary analysis, but contrasts include any such differential effect.
- 19 and 22 "did not change" lists.
- The exclusive per-type order of section 4.5, only if an exclusive table is wanted.
- A void-and-resume rule for lost records (section 6.4).
- Spelling: keep "unparseable".

---

## 12. Decisions still needed (the assistant makes none of them)

| # | Decision | Options | Assistant's candidate (for review only) |
|---|---|---|---|
| D-1 | Primary target | all planned calls / non-SF calls / another | all planned calls |
| D-2 | Primary classification | SF-only / parse-first / flags + class table | SF-only |
| D-3 | SF3 with a parseable verdict | structural failure (diagnostic partial verdict) / parsed class | structural failure, diagnostic field |
| D-4 | Several flags | flags-only reporting / flags + a frozen exclusive order | flags-only reporting |
| D-5 | Counting convention for `SF1 + SF4` and "hard" failures | per call / per flag | per call |
| D-6 | Incomplete cells | Option 1 / Option 2 / Option 3 / other | Option 1 |
| D-7 | Lost records (case C) | cell becomes incomplete / void-and-resume | cell incomplete, unless the advisor adopts void-and-resume with raw-first persistence |
| D-8 | Ledger | adopt the requirement of section 5.1 / another / none | adopt (smallest version) |
| D-9 | Sensitivity | S-A / S-B / S-C | S-B, replacing the frozen wording, one table only |
| D-10 | S2/S3 eligibility | table of section 7 / code SF3-partial as a stratum | table of section 7 |
| D-11 | Pilot consistency | write A-1/A-2 into 13.4 and 13.6 for both pilot and main run | yes |

Consequences if left undecided: the pilot outcome of an empty-response round remains ambiguous between STOP-U and FAIL-S; incomplete cells
cannot be reported under a rule fixed in advance; and the decision script and the scoring definitions (items of the freeze set, 13.2) cannot be
frozen consistently.

---

## 13. Limits and claims not made

- No data exist. The probabilities in section 6.3 and 10.7 are illustrations under an independence assumption that is unlikely to hold.
- No claim is made about the size or direction of any bias caused by structural failures or by missing calls.
- No claim is made that the candidate is authorized by 12.18; that entry is an owner clarification for pilot counts and is not part of
  specification v2.7.
- The ledger requirement is a design requirement, not an implementation.
- Nothing here has been tested by a human coder; no pilot, experiment, API call, token measurement or Step 8 work was involved.
- This package leaves unresolved: P-2 (FZ hash contract), P-3 (other text inconsistencies), P-4 (token measurement), the round-1 FAIL-S action
  for several failure types, the round-2 record without a round-1 outcome, the PG11 scan of response text, and the carried-over items F-3, F-4,
  T-1, I-6, PRD-5, PRD-6, PRD-8, PC-2.
