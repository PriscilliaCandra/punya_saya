# Proposed amendment of section 18.2 - DRAFT v1 (outcome denominators and structural failures)

Status: **PROPOSED AMENDMENT. NOT APPLIED. NOT ADOPTED.** Specification v2.7 (sha256 `d5fcffad...082ca8`) is unchanged and remains the
text in force. This file records the owner's delegated decision of 2026-10-12 (decision record 12.24, decision 1) as a proposal for a
future methodology version (13.2, 21.2). It supersedes proposal P-1 (alternative A1) of `PROPOSED_CLARIFICATIONS_AND_AMENDMENTS_DRAFT_v1.md`.
The draft code that expresses it (`s7_outcomes.py`) is conditional on adoption. The author of this proposal, the code and the tests is the same.

## 1. The proposed policy

1. The four primary outcome proportions (satisfied, violated, unclear, unparseable) use the number of **evaluable responses** of the cell as denominator.
2. Evaluable responses = the actual calls of the cell excluding the calls classified as structural failures (SF1 to SF5).
3. The four proportions sum to 1 (exact rational arithmetic, 3.1).
4. The **structural-failure rate** is reported separately over the protocol-defined total number of calls of the cell.
5. Pilot UNP share = UNP calls / all actual calls of the round (as implemented in `s7_decision.py`; unchanged).
6. SF and UNP are separate classifications. UNP is never inferred from SF.
7. If the observed number of calls differs from the frozen registry, or a denominator is invalid, no PASS and no figure is produced.

## 2. What the frozen text says (read before implementing)

| Definition | Frozen text | Consequence for the policy |
|---|---|---|
| SF1 to SF5 | 13.4: transport error or timeout; empty response (no non-whitespace character); truncation (finish reason at the output-token limit); provider block or no candidate; harness exception on a non-empty response | SF1 and SF4 have no response; SF2, SF3, SF5 may |
| UNP | 13.4: a **measured outcome**, defined on a response: zero Verdict matches, or two or more with different tokens, or a token not allowed | defined by the parse of a response |
| Four outcomes | 18.2: satisfied / violated / unclear / unparseable, each over `n_calls`; "the four proportions sum to 1" | the sum is true only if every call is in exactly one of the four |
| `n_calls` | 0.1: the number of calls in a reporting cell | planned and actual calls coincide in a complete run |
| Pilot | 13.6, 13.7: counts of SF1 to SF5 and the UNP share; no 18.2 figures | no conflict for the pilot |

### Can SF and UNP overlap under the frozen definitions? **Yes, read literally.**
- SF2 (no non-whitespace character) has zero `Verdict:` matches, which 13.4 also defines as UNP.
- SF3 (truncation) can have zero matches (UNP), or can contain a complete and parseable verdict (neither UNP nor an unclassified call).
- SF5 (the parser raised) leaves the outcome class of that call undefined.
- 13.4 says "Structural failures are SF1-SF5. An individual UNP is never a pilot failure", and 18.2 gives no precedence between a structural classification and an outcome class.

So the frozen text does **not** establish that SF and the four outcome classes are exclusive. Exclusivity holds only under a **precedence
rule**: *a call that meets any SF definition is classified SF and in no outcome class.* That rule is recorded as an owner clarification
for the pilot counts (12.18 row 1), and the proposed policy needs it for 18.2 as well. It is not stated in v2.7. **The amendment
therefore has to state the precedence rule explicitly (item A5 below).**

## 3. Proposed text (to replace the corresponding passages in a future methodology version)

- **A1 (18.2 heading).** "Estimands (per cell, over the evaluable responses of the cell; unclear and unparseable stay in the denominator)".
- **A2 (18.2 table).** In both rows replace `n_calls` by `n_eval`, where `n_eval` = `n_calls` minus the number of calls classified SF1 to SF5. The four proportions of each row sum to 1.
- **A3 (new sentence after the table).** "The structural-failure rate `(SF1 + ... + SF5) / n_calls` is reported beside the four proportions of every cell, with the SF counts by type. It is not one of the four proportions."
- **A4 (sensitivity sentence).** The parseable-only sensitivity keeps its meaning; its denominator becomes `n_eval - unparseable`. *This is a consequence of the policy that the owner's decision did not state; it needs confirmation.*
- **A5 (precedence, new sentence in 13.4).** "A call that meets any definition SF1 to SF5 is classified under that code only, even if it also has a parse outcome; the code is never counted as UNP and UNP is never inferred from it. A call that meets more than one SF definition is reported under [order to be fixed by the amendment]."
- **A6 (consequential passages to review).** 0.1 (`n_calls`), 1 (primary outcome sentence), 12.3 (`p_t(c)`), 13.4 (last sentence: UNP "remains in every denominator" stays true), 19 (the lists "did not change"), 22 item 6 (denominators "defined exactly as in 18.2").

## 4. Unresolved points (no rule is invented; the corresponding implementation is not written)

1. **Cluster-level figures (12.3, 18.2).** The reported figures are cluster-level means of `p_t(c)` = matches / `R`, and "equal to the pooled template mean under exact balance". With SF calls removed, a template-condition has between 0 and `R` evaluable calls; `p_t(c)` is undefined when there is none, the templates of a cluster no longer carry equal weight, and the equality with the pooled mean fails. A rule is needed for the per-template denominator, for templates without an evaluable call, and for the cluster bootstrap and the planning bounds of 12.1 (which assume `h_b` in [0,1] from `R` calls per template). `s7_outcomes.py` therefore computes **pooled cell counts only**.
2. **Several SF codes on one call.** No order is defined (item A5). `classify_call` refuses such a call.
3. **Incomplete cells.** 13.8 reports cells of an incomplete run "with their achieved counts". Under the proposal the SF-rate denominator is the protocol-defined number of calls; for an incomplete cell that number and the achieved number differ. `cell_outcomes` produces no figure when the observed number of calls differs from the frozen cell size. How an incomplete run is reported is not decided.
4. **Rounding of reported figures.** 18.2 has no reporting-rounding convention (the two-decimal convention of PRD-3 concerns parameters). The code returns exact fractions. "Subject to the specification's existing rounding convention" cannot be applied because none exists for these proportions.
5. **Selection effect.** Removing SF calls conditions the outcome proportions on calls that did not fail structurally. If SF (for example truncation or a provider block) is related to the scenario or to the answer, the four proportions describe the evaluable calls only. The separate SF rate discloses the size of the exclusion; it does not remove the effect. This is a threat to be stated (20), not resolved here.
6. **Pilot versus main run.** The pilot rule (UNP over all calls; SF and UNP counted apart) and the main-run policy (SF removed from the outcome denominators) use different denominators on purpose; the amendment should say so.

## 5. Interim behaviour (no specification change)
Until a decision exists, the specification text stands: the figures of 18.2 are not rescaled by this draft. `s7_outcomes.py` is not used by any decision script, and its output carries the status "PROPOSED POLICY, NOT ADOPTED".
