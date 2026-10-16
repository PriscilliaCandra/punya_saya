# Stage 2 Configuration Specification

**Status: FROZEN specification (design only).** This document specifies the future file `pilot_clarification/pilot_config_stage2.json`. That file does not exist yet, and this document is not it. No experiment has been run and no API call has been made.

## 0. Authority and bound inputs

Precedence, highest first: (1) `CODEBOOK_v2.md`, the sole coding authority; (2) the Stage 2 registry and `stage2_prompt_specification.md`; (3) the three specifications written together with this one (configuration, runner, analyzer). If a statement here conflicts with a higher artifact, the higher artifact governs. The conflict must then be reported and resolved by a new approval. An implementer must not resolve it.

| Input | Path | SHA-256 |
|---|---|---|
| Frozen codebook | `pilot_clarification/CODEBOOK_v2.md` | `177a1c5d9b7dbf1ab9e53d0684365dcf67b21f1b1f3154f3f8b1ecc5aa6eb4fc` |
| Codebook freeze manifest | `pilot_clarification/CODEBOOK_v2_freeze_manifest.json` | `669ef62e758b4243a732ac417f6dd670623637d1f8fd19453a2f5124ee1891b2` |
| Stage 2 registry (file bytes) | `pilot_clarification/scenario_registry_stage2_v1.json` | `51895ee5329059930959f15746439f692bb849521de346099a1838be7689f5c7` |
| Stage 2 registry (canonical) | same file, `sha256(json.dumps(obj, sort_keys=True).encode('utf-8'))` | `c0e9447bb50911f3f7bc33f8fa1d0bda85c909ed39ba82eaa01a1e398a41e76b` |
| Stage 2 prompt specification | `pilot_clarification/stage2_prompt_specification.md` | `5d88b1e57557d9fb8ba67d9623972d3420953e9e3f28961e0dfed401b3637a80` |
| Stage 1 registry (canonical) | `pilot_clarification/scenario_registry.json` | `d5213f039073acc72140956b46c792c4f76d980e2c800982cbca247bafb86e81` |

Stage 1 run `stage1_gemini_20261007T080948Z` is historical and immutable. It is referenced only through the Stage 1 registry binding above.

## 1. Experiment identity

| Item | Value |
|---|---|
| `stage` | 2 |
| `registry_version` | `stage2-v1` |
| provider | `gemini` (one provider) |
| `model_requested` | `gemini-3.1-flash-lite` (one model only; no substitution) |
| cells (scenarios) | 8, in registry order: E-F-A, E-F-B, K-E-TRUE, K-E-TRUE-B, C-L2, C-L3, C-L4-S2, K-C-L4-S2 |
| repetitions per cell | 5 |
| planned calls and hard cap | 40 (8 x 5); the runner may never attempt a 41st call |
| pooling with Stage 1 | forbidden in primary decision counts. The analyzer reads no Stage 1 data. |
| instruction style | natural instruction only; no verification-cued arm |

## 2. Provider settings

| Setting | Frozen value |
|---|---|
| system prompt | none (`null`; no `systemInstruction` field is sent) |
| temperature | **not sent**; the provider default applies. The policy string is `provider default (temperature parameter is NOT sent)`. |
| max output tokens | 8192 (`generationConfig.maxOutputTokens`) |
| retries | 0 |
| timeout | 180 seconds per call |
| concurrency | 1 (strictly sequential) |
| delay | 1.0 second after every call |
| API key | environment variable `GEMINI_API_KEY` only |

**Request, exact.** Method POST to `https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent` (a leading `models/` in the model ID is stripped). Headers: `x-goog-api-key` and `content-type: application/json`, and no others. Body: `{"contents":[{"role":"user","parts":[{"text":<prompt>}]}],"generationConfig":{"maxOutputTokens":8192}}`. No `temperature`, `topP`, `topK`, `systemInstruction`, `safetySettings`, `thinkingConfig`, `tools` or any other field is sent. The prompt is the registry `prompt` string, unmodified.

**Secrets.** The API key is read from the environment and used only in the request header. It must never be logged, printed, serialized, written to any file (including manifests, raw records, error text and the config), placed in a URL, or echoed by the preflight. Error text is passed through a redactor that replaces the key value and common key patterns before it is stored.

**`model_returned`.** The model identifier reported by the provider in each response (the `modelVersion` field) must be captured into every call record. If a response carries none, the record stores `null`. The analyzer reports the set of returned values.

## 3. Shuffle seed and execution order

**Seed.** The configuration contains exactly one shuffle seed: **20261008**. It is the integer `YYYYMMDD` of the UTC date on which this configuration specification was frozen (2026-10-08), as required by the approved policy. It was not chosen using any expected output, scenario difficulty or observed model behavior, and none existed.

- The seed is frozen before any Stage 2 call.
- The seed cannot be changed after any output is seen. A different seed would be a new configuration version needing a new approval, and it would not be a re-draw of this run.
- One shuffle covers all 40 `(scenario_id, repetition)` pairs. There is no per-cell or blocked shuffle.

**Algorithm, exact.**

```text
order = [
  (scenario_id, repetition)
  for scenario_id in registry order            # registry design.registry_order, positions 1..8
  for repetition in 1..5
]
random.Random(seed).shuffle(order)
call_index = 1-based position in the shuffled order
```

**Persistence and hash.** The future configuration stores the realized order as 40 `[call_index, scenario_id, repetition]` entries and its SHA-256. Serialization for hashing: one line per call, `call_index,scenario_id,repetition`, joined with LF, a final LF, UTF-8, no header, no BOM. The runner copies this serialization into the run directory.

**Reconstruction.** The runner must independently reconstruct the order from the frozen registry, the frozen seed, the algorithm above and the bound Python version, and compare it to the stored order. If the reconstructed order, or its hash, differs from the stored order in any position, execution aborts before the first API call.

**Realized order at this freeze** (reconstruction verified; Python 3.11.9):

```text
1,K-E-TRUE-B,2
2,C-L2,1
3,K-E-TRUE,1
4,K-C-L4-S2,4
5,C-L4-S2,4
6,K-C-L4-S2,2
7,C-L3,2
8,C-L4-S2,2
9,C-L4-S2,5
10,C-L3,3
11,E-F-A,5
12,E-F-B,4
13,E-F-A,2
14,C-L4-S2,1
15,C-L3,5
16,K-C-L4-S2,3
17,K-C-L4-S2,1
18,C-L2,5
19,E-F-B,3
20,K-E-TRUE,2
21,K-E-TRUE,3
22,E-F-A,1
23,K-E-TRUE,5
24,C-L2,4
25,K-C-L4-S2,5
26,E-F-A,4
27,C-L4-S2,3
28,E-F-B,2
29,C-L2,3
30,C-L2,2
31,C-L3,1
32,K-E-TRUE-B,5
33,K-E-TRUE,4
34,E-F-B,1
35,K-E-TRUE-B,3
36,E-F-B,5
37,K-E-TRUE-B,1
38,C-L3,4
39,E-F-A,3
40,K-E-TRUE-B,4
```

SHA-256 of the order serialization: `8b98a43e72f7ab243e1ce21a7a18f908286a0b5fcbf2429c06621570e7e30e81`

## 4. Python version

The bound Python version is **3.11.9** (the version recorded in the Stage 1 run manifest and used to verify the order above). The runner aborts if `platform.python_version()` differs from the bound value. Changing the bound version requires a new configuration version and approval. The order comparison in section 3 remains the decisive reproducibility test.

## 5. Conceptual schema of `pilot_config_stage2.json`

The implementation step creates this file with exactly these keys and no others.

| Key | Frozen value / rule |
|---|---|
| `stage` | 2 |
| `registry_version` | `"stage2-v1"` |
| `provider` | `"gemini"` |
| `model_requested` | `"gemini-3.1-flash-lite"` |
| `scenarios_expected` | 8 |
| `repetitions` | 5 |
| `planned_calls`, `hard_cap_calls` | 40, 40 |
| `shuffle_seed` | 20261008 |
| `call_order` | the 40 entries of section 3 |
| `call_order_sha256` | `8b98a43e72f7ab243e1ce21a7a18f908286a0b5fcbf2429c06621570e7e30e81` |
| `max_output_tokens` | 8192 |
| `temperature_policy` | `"provider default (temperature parameter is NOT sent)"` |
| `system_prompt` | `null` |
| `retries` | 0 |
| `timeout_seconds` | 180 |
| `concurrency` | 1 |
| `delay_between_calls_seconds` | 1.0 |
| `api_key_env` | `{"gemini": "GEMINI_API_KEY"}` (the variable name only, never a value) |
| `python_version` | `"3.11.9"` |
| `bindings` | the hashes of section 6 |

## 6. Integrity bindings and hash categories

**A. Pre-run frozen hashes** (known now and bound by the configuration):

| Binding key | Value |
|---|---|
| `codebook_sha256` | `177a1c5d9b7dbf1ab9e53d0684365dcf67b21f1b1f3154f3f8b1ecc5aa6eb4fc` |
| `codebook_freeze_manifest_sha256` | `669ef62e758b4243a732ac417f6dd670623637d1f8fd19453a2f5124ee1891b2` |
| `registry_file_sha256` | `51895ee5329059930959f15746439f692bb849521de346099a1838be7689f5c7` |
| `registry_canonical_sha256` | `c0e9447bb50911f3f7bc33f8fa1d0bda85c909ed39ba82eaa01a1e398a41e76b` |
| `prompt_specification_sha256` | `5d88b1e57557d9fb8ba67d9623972d3420953e9e3f28961e0dfed401b3637a80` |
| `stage1_registry_canonical_sha256` | `d5213f039073acc72140956b46c792c4f76d980e2c800982cbca247bafb86e81` |
| `call_order_sha256` | `8b98a43e72f7ab243e1ce21a7a18f908286a0b5fcbf2429c06621570e7e30e81` |
| the 8 prompt hashes | the registry `prompt_sha256` values, listed below |

| Scenario | prompt `prompt_sha256` |
|---|---|
| E-F-A | `1770f1572342116c12e75b0b42efa70789d1a54f2f4b670cba6b56a15024cb49` |
| E-F-B | `5406c93c376febd64b2df037580f1d1f4ed5995eece059cba390a4e92e8a2a46` |
| K-E-TRUE | `808c1545b65a1ce4f2052bdd06458967a500de06cd151cffbdaf992702f29967` |
| K-E-TRUE-B | `4b33b6067d75783dd3b77c0417ef21cfe768a8e5be82d1f5c80e347408776085` |
| C-L2 | `9479e2e9ba1d0540bddec16b29ba9be044e76004a87402eb9ed44d22b61c0a04` |
| C-L3 | `a672ab88f0101ea5c5ca67c36f65205630c85091ab66d6d76070ec190375893c` |
| C-L4-S2 | `ba5ef99887b0dccc05caec191dbe08469f876eb3d0d2ee5e0b8e8afc552bdee8` |
| K-C-L4-S2 | `61eeac0b0c4043b0ae463756483241f33641cf64548867a453545e91fc601393` |

The SHA-256 values of the three specification files written with this one (configuration, runner, analyzer) are also pre-run frozen. They are recorded in the freeze report and are bound when the configuration is created. A file cannot contain its own hash, so they are not stored inside these documents.

**B. Post-implementation hashes** (do not exist yet; none is invented here). They are computed when the code exists and recorded before any run in the configuration or the Stage 2 freeze manifest: `runner_sha256`, `analyzer_sha256`, the analyzer tests' hash, the configuration file's own SHA-256 (recorded in the freeze manifest, not inside the config), and the Stage 2 freeze manifest.

**C. Post-run hashes** (produced by a run and recorded in the run directory): the SHA-256 of every raw record, `calls.jsonl`, `manifest.json`, the configuration copy, the registry copy, the order copy and `integrity/postrun.json`, and later the analysis outputs listed in the analyzer specification.

Until the post-implementation bindings are filled, a live run must refuse to start. A dry run may proceed.

## 7. Loader validation (the configuration is rejected if any check fails)

- exactly the keys of section 5, with exactly the frozen values, in particular `stage` = 2, `repetitions` = 5, `scenarios_expected` = 8, `planned_calls` = `hard_cap_calls` = 40, `retries` = 0, `timeout_seconds` = 180, `concurrency` = 1, `delay_between_calls_seconds` = 1.0, `max_output_tokens` = 8192, `system_prompt` = null;
- `shuffle_seed` equals 20261008 and appears exactly once;
- every binding equals the SHA-256 of the file it names, and every post-implementation binding is non-null for a live run;
- `python_version` equals the running interpreter;
- `call_order` has 40 entries, each registry scenario appears 5 times, every `(scenario_id, repetition)` pair appears once, and its serialization hash equals `call_order_sha256`.

## 8. Lifecycle

The configuration file is created in a later approved implementation step. After creation its SHA-256 is recorded in the Stage 2 freeze manifest, and it is never edited afterwards. Any change creates a new configuration version and needs a new approval. This document designs no second-run mechanism, no resume mechanism and no alternative model.

## 9. Historical separation

- Stage 1 is historical exploratory data and is immutable.
- Stage 2 is a separate experiment. Stage 1 and Stage 2 are never pooled in primary decision counts.
- Stage 1 `C-L4` is not rerun. Stage 2 `C-L4-S2` is a new scenario and `K-C-L4-S2` is its matched control.
- `CODEBOOK.md` (v1) remains historical. `CODEBOOK_v2.md` is the frozen measurement instrument for Stage 2.
- Stage 2 has no verification-cued arm.

## 10. Methodological-drift review

Compared with `stage2_prompt_specification.md` and `CODEBOOK_v2.md`. NONE = identical to a frozen statement. CLARIFICATION = makes a frozen statement operational without changing any threshold, failure category, denominator, exclusion or interpretation. REQUIRED REVIEW = would need an unapproved methodological decision.

| ID | Item | Class |
|---|---|---|
| C-1 | model, repetitions, calls, timeout, retries, concurrency, delay, output limit, temperature, system prompt | NONE |
| C-2 | seed value 20261008 as the instance of the approved `YYYYMMDD` UTC policy | NONE |
| C-3 | realized order and its hash computed now from the frozen registry, seed and algorithm | CLARIFICATION |
| C-4 | exact order serialization for hashing | CLARIFICATION |
| C-5 | exact binding of Python 3.11.9 (the task asks that it be bound) | CLARIFICATION |
| C-6 | only the `gemini` key variable is configured (Stage 1 listed three providers; Stage 2 is one model) | CLARIFICATION |
| C-7 | the exact request body and headers, copied from the Stage 1 runner's Gemini request | CLARIFICATION |
| C-8 | hash categories (pre-run, post-implementation, post-run) and the refusal to run live with unbound post-implementation hashes | CLARIFICATION |

No REQUIRED REVIEW items.
