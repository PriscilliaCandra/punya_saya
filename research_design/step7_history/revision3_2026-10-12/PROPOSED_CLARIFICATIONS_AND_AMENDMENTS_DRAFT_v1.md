# Proposed clarifications and amendments - DRAFT v1 (Step 7 second review)

Status: **PROPOSALS ONLY. Nothing here is adopted, applied or frozen.** Specification v2.7 (sha256 `d5fcffad...082ca8`), the FZ-v1
manifest and the FZ-v1 register are not changed by this file. Each proposal needs the owner's explicit approval; P-1 and P-3 would
need a formal specification amendment (a new methodology version, section 13.2 and 21.2). Written under the owner's delegation to
the assistant acting as the S2 student (decision record 12.21); the author of the proposals is also the author of the draft code and
tests, so no independence is claimed.

## P-1. Section 18.2 versus structural failures (GAP-1)

**Conflict (specification text).**
- 18.2: for each cell, over all `n_calls` calls of the cell (`n_calls` = number of calls in a reporting cell, 0.1), four proportions
  `satisfied`, `violated`, `unclear`, `unparseable`, each `/ n_calls`; "within each cell the four proportions sum to 1".
- 13.4: UNP is "a measured outcome, not a harness failure" and is defined on a response (zero field matches, conflicting fields,
  a token not allowed). SF1 (transport error or timeout) and SF4 (no candidate) have no response; SF2 (empty), SF3 (truncated) and
  SF5 (harness exception) are separate codes.
- 13.8 and 13.9: the main run continues below the halting thresholds; a failed call is not re-run, replaced or discarded.
- 12.18 row 1 (pilot): the SF counts and the UNP count are disjoint.

An SF call that occurs in the main run below the halting threshold is in `n_calls` (planned) but in none of the four numerators.
The four proportions then sum to less than 1. Making them sum to 1 requires either counting the SF call as `unparseable` (against
13.4 and against the disjointness of 12.18 row 1) or removing it from `n_calls` (against "all `n_calls` calls", and it makes the
denominator depend on failures). For the pilot there is no conflict: 13.7 reports counts only.

**Alternatives.**
| | Change | Effect | Assessment |
|---|---|---|---|
| A1 | Add a fifth reported proportion `structural failure = (SF1+...+SF5) / n_calls`; the five sum to 1; the sensitivity table keeps `n_calls - unparseable` as the denominator of the four outcome proportions' parseable-only variant and reports SF separately | No change when no SF call occurs; the other definitions are untouched | **Smallest change; proposed** |
| A2 | State that for 18.2 an SF call counts as `unparseable` | Four proportions sum to 1 | Mislabels a transport or provider failure as a model outcome; conflicts with 13.4 and 12.18 row 1 |
| A3 | Define `n_calls` as the calls with a recorded response | Four proportions sum to 1 | Cell denominators vary with failures; conflicts with the fixed planned counts of 9.7 |

**Proposed text for A1 (to be added to 18.2).** "A call classified SF1 to SF5 (13.4) is counted in `n_calls`. Each cell also
reports `structural failure = (SF1 + ... + SF5) / n_calls`. The five proportions sum to 1. No SF call is counted as `unparseable`."

**Interim behaviour (no specification change).** Until a decision exists, any cell containing an SF call is reported with its SF
count beside the four proportions, and the four proportions are not rescaled to sum to 1.

## P-2. The FZ hash (decision record field "the FZ hash", section 10)

**Finding.** Section 13.2 says FZ is "hashed before the first pilot call"; section 10 lists "the FZ hash" in the decision record;
section 21.1 step 11 hashes "the final freeze manifest" after the record. No object, serialization or encoding is defined. The only
hash defined for FZ-v1 is the register hash (`register_canonical_sha256`, method recorded in the FZ-v1 manifest) and the file hashes
of that manifest. The decision script currently records a researcher-supplied value as unverified.

**Proposed contract (a versioned clarification; FZ-v1 is not redefined and its manifest is not rewritten).**
- *Object.* An `FZ_INDEX` JSON object: `{"fz_version": ..., "items": {<logical name>: {"path": <relative path>, "sha256": <64 hex>}}}`
  with one entry per FZ item of 13.2: the specification; the FZ-v1 register (with its register hash and the method); every Step 7
  item of the Step 7 manifest; the generator code; the registry and the list of rendered-prompt hashes; the pilot parameter set;
  the decision script; the diagnostic code; the codebooks.
- *Serialization.* JSON, keys sorted, separators `,` and `:`, `ensure_ascii=False`, UTF-8 without BOM, no other whitespace, one
  final LF (the register-hash convention of the FZ-v1 manifest plus the final LF of section 10).
- *Hash.* SHA-256 of the exact bytes of the index file, written as 64 lowercase hexadecimal characters.
- *Exclusions (no self-reference).* The index itself, the decision record (it contains the FZ hash) and the final freeze manifest of
  step 11 (hashed after it).
- *Verification.* A verifier recomputes each listed item hash from its file, parses the index and re-serializes it to check byte
  equality (canonical form), then recomputes the hash. The decision script takes `--fz-index PATH` and computes the value instead of
  accepting `--fz-hash`.
- *Not decided here.* Which items are in the index at which step (the registry and generator exist only after Step 8) and whether the
  harness code hash of H4 belongs in it.

## P-3. Inconsistencies of the specification text found by this review (clarifications; no change of meaning proposed)

1. **`s2_values` (16.1).** The categories include `none` (no used value), but the denominator is "parseable responses with
   `s2_evidence` in {IV, EV} and at least one used value". A response in IV through a derived quantity with provenance and no used
   value has `none` and is outside the denominator, so `none` never occurs inside it. Proposal: report `none` as a count outside the
   denominator.
2. **"MX" (16.2).** The derived categories and the retraction rule use "MX", the table uses MPG. Applied as MPG (12.18 row 13).
3. **Cohen's kappa (16.3).** "Agreement is reported per variable (percent agreement and Cohen's kappa)" versus OD-3 and the
   single-coder fallback ("no inter-rater reliability"). Applied: raw agreement only; kappa is not reported or claimed (12.21 row 6).
4. **13.4 versus SF2/SF3.** A response that is empty or truncated has "zero Verdict matches", which 13.4 also calls UNP. Applied for
   counting: SF takes precedence and the counts are disjoint (12.18 row 1).

## P-4. Token adequacy and cost (OD-10)

**Not established.** `I_max` has not been measured. The character counts (878 for MIL, 1016 for PAC with the claim block and the
widest numerals, current texts) are an upper bound on tokens only under the unproven assumption that a token covers at least one
character. Character count is not evidence of token adequacy.

**Measurement method (to be confirmed against the provider's current documentation; not verified here, no network access was used).**
The Gemini API offers a token-counting method (`models.countTokens`) for a given model; the `promptTokenCount` of a generation
response is not usable because it needs a generative call. Inputs to measure: every final rendered prompt exactly as sent
(`4 x 312 = 1248` main prompts, plus the pilot prompts), in the same request structure as the run (one user turn, no system prompt),
with the model `gemini-3.5-flash-lite`. `I_max` = the largest count. A call to this method is an external API call and is **pending
explicit authorization**; it must be made only after Step 8 has produced the final prompts (a measurement on synthetic worst-case
strings now would not be the final-prompt measurement the owner's OD-10 requires).

**Effect on the US$100 ceiling (arithmetic from FZ-v1: 8192 output tokens on every call, retries 0, USD 0.30 / 2.50 per 1M tokens read on
2026-10-12).**
| Slots | Output part (USD) | Largest `I_max` per call that keeps the total at or below USD 100 | Total at I = 1,016 | at I = 10,160 | at I = 50,000 |
|---|---|---|---|---|---|
| 2,496 (main) | 51.12 | 65,280 | 51.88 | 58.73 | 88.56 |
| 2,532 (main + 36 pilot slots) | 51.86 | 63,381 | 52.63 | 59.57 | 89.84 |

The ceiling is insensitive to the input size for any plausible prompt; the open risk is the output side (thinking tokens count in the
8192 limit and are billed; the price table must be re-read at the time of the run). If a measurement exceeded the break-even value or
could not be made, OD-10 requires stopping before any paid call.

## P-5. Human readiness of the codebook (what can and cannot be assessed before the experiment)

Can be assessed now, without any response: the deterministic functions (tested); the internal consistency of the battery (tested);
that every codebook definition maps to an implemented rule or is marked as a coder judgement (documented).

Cannot be assessed without a human: whether the free-text reading step (assertion, rejection, used value, provenance, numerical
comparison, correctness) is interpretable and consistent. Proposed rehearsal, **pending**: the human coder codes the 40 battery items
from the comment text only, in the order of their hash keys, on a sheet that does not contain the expected codes; the expected codes
are fixed and hashed (decision record 12.22) before the rehearsal; the comparison reports raw agreement per variable and the
disagreements, and is **not** a reliability claim (the coder is the author of the codebook, remembers the items, and the items are
short synthetic sentences). No pilot or main response is used, and none exists.
