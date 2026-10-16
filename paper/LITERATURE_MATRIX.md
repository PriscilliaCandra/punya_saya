# LITERATURE_MATRIX

Updated 2026-10-01 after the reference audit and manuscript revision. Reference numbers follow the current `PAPER_DRAFT.md` (33 references). Type key: J = journal article, R = review/survey/meta-analysis (journal), C = conference paper, B = book. Google Scholar status for every item is in `REFERENCES_VERIFICATION.md` ("not verified due to access limitation" is not "absent from Scholar").

## A. Personalized recommender systems

| Ref | Type | Year | Contribution to this paper | Limitation |
|---|---|---|---|---|
| [1] Adomavicius & Tuzhilin | R | 2005 | Taxonomy of recommenders; proposed extensions | Item recommendation, pre-LLM |
| [26] Feely et al. | C | 2020 | Case-based, explainable marathon training-plan recommender (running-specific) | Marathon; non-LLM; offline evaluation |

Not adopted (optional): Tran et al. 2020 (J. Intell. Inf. Syst., doi 10.1007/s10844-020-00633-6), Ni et al. WWW 2019 (doi 10.1145/3308558.3313643) — Crossref-verified, moderate relevance.
Former [2] (Jannach et al.) was removed: editorial-type, only partial relevance.

## B. LLM-based recommender systems

| Ref | Type | Year | Contribution | Limitation |
|---|---|---|---|---|
| [4] Lin et al. | R | 2025 | Survey of LLMs in recommender systems | Item recommendation |
| [5] Wu et al. | R | 2024 | Survey of LLMs for recommendation | Abstract not retrieved |
| [6] Bao et al. (TALLRec) | C | 2023 | Instruction tuning for recommendation | Requires training |
| [7] Geng et al. (P5) | C | 2022 | Text-to-text recommendation | Not exercise |
| [8] Hou et al. | C | 2024 | Zero-shot ranking | Author list fixed; abstract not retrieved |

Coverage: adequate. No source on *constraining* LLM output in recommendation was adopted.

## C. LLM-based exercise / physical-activity recommendation (incl. running-specific)

| Ref | Type | Year | Design | Key finding (abstract level) | Relevance |
|---|---|---|---|---|---|
| [9] Washif et al. | J | 2024 | ChatGPT 12-week resistance programs vs guidelines | Compared with established guidelines | Partial (not running) |
| [10] Zaleski et al. | J | 2024 | 26 clinical populations, coding scheme | Comprehensiveness, accuracy, readability | Partial |
| **[11] Düking et al.** | J | 2024 | **Three ChatGPT six-week running plans, increasing input detail; coaching experts; 22 criteria; Friedman test** | Sub-optimal ratings; higher with more input information; advise expert feedback | **Highest (running-specific)** |
| **[12] Havers et al.** | J | 2025 | GPT-4 vs Gemini hypertrophy plans; reproducibility; 12 experts | High reproducibility with repeated identical prompts; GPT-4 rated higher on several criteria | **High for RQ2** (volume/pages to verify) |
| [13] Lai et al. | R | 2025 | Scoping review, 20 studies | Heterogeneous, low-rigor evaluation (median 2.5/5) | High |
| **[14] He T. et al.** | R | 2026 | Systematic review, 24 studies | Safety flaws in 14/24; LLM plans inferior in 5/6 head-to-head trials | **High for safety** (volume/pages to verify) |
| [15] Akrimi et al. | J | 2025 | 3 fictional T2DM profiles, 3 prompts, 3 experts (discussion paper, preliminary data) | Serious safety issues in some plans | Safety evidence — one small study |
| [24] He Z. et al. | J | 2026 | LLM + sports-science knowledge graph | Better than baselines on coherence, goal relevance, predicted satisfaction | High; check full text for output validation |
| [25] Khasentino et al. | J | 2025 | Fine-tuned PH-LLM, 857 case studies | Similar to experts on fitness tasks | Partial |

Removed: former [13] (Lai, scoping review of 11 studies; overlaps [13] now and [14]).

## D. Running / exercise prescription / training science

| Ref | Type | Year | Supports | Strength / caveat |
|---|---|---|---|---|
| [27] Daniels | B | 2022 | VDOT-based paces | Authoritative text; edition and zone fractions to verify |
| [19] Seiler | R | 2010 | ~80/20 session distribution | Strong |
| [20] Seiler & Kjerland | J | 2006 | Observed 75/8/17 distribution | 11 junior skiers |
| [21] Stöggl & Sperlich | J | 2014 | Polarized-training RCT | n=48, 9 weeks, mixed sports |
| [17] Nielsen et al. | J | 2014 | Progression vs injury (cohort) | Novices; no overall difference |
| [18] Buist et al. | J | 2008 | 10%-rule program RCT | Novices; no reduction in injuries |
| [22] Mujika & Padilla | R | 2003 | Taper principles | Strong |
| [23] Bosquet et al. | R | 2007 | Taper meta-analysis | Strong |
| [28] Gabbett | R | 2016 | Load–injury framing | Team-sport emphasis; context only |
| **[29] Issurin** | R | 2010 | Periodization concept and limitations | Does not support a specific cutback rule |

Optional, not adopted: Garber et al. 2011 (doi 10.1249/MSS.0b013e318213fefb), Bull et al. 2020 (doi 10.1136/bjsports-2020-102955).

### Running-specific coverage check
| Topic requested | Covered by | Gap |
|---|---|---|
| LLM-generated running plans | [11] | One study; no multi-LLM running comparison found |
| Running training prescription | [27], [11] | — |
| Marathon/running recommenders | [26] | No LLM-based one found |
| Training-plan personalization | [26], [24], [25] | — |
| Running training intensity | [19], [20], [21] | Not recreational-runner specific |
| Progression and periodization | [17], [18], [29], [28] | No source for a cutback magnitude/frequency |
| Taper | [22], [23] | No source for 0.85×/0.55× values |
| Long-run share; quality share | — | **No source found** (engineering design constraints) |

## E. Personalization / user-centered evaluation

| Ref | Type | Year | Supports |
|---|---|---|---|
| [2] Knijnenburg et al. | J | 2012 | User-experience framework |
| [3] Pu et al. (ResQue) | C | 2011 | Questionnaire-based evaluation framework |
| [32] Norman | J | 2010 | Analysis of Likert data (replaces former [30]) |
| [33] Tavakol & Dennick | J (short) | 2011 | Cronbach's alpha (optional alternative: Taber 2018, doi 10.1007/s11165-016-9602-2) |

Gap: no source from which the 16 questionnaire items could be adapted was verified; see `QUESTIONNAIRE_TRACEABILITY.md`.

## F. LLM evaluation and reliability

| Ref | Type | Year | Supports |
|---|---|---|---|
| [30] Chang et al. | R | 2024 | What/where/how of LLM evaluation |
| [31] Zheng et al. | C | 2023 | LLM-as-a-judge; biases (checked on the arXiv-version abstract) |
| [16] Huang et al. | R | 2025 | Hallucination in LLMs |
| [13], [12] | R, J | 2025 | Evaluation of LLM coaches; reproducibility across repeated prompts |

Removed: former [15] (Ji et al., general NLG hallucination).

## G. Safety / validation of AI-generated exercise recommendations

| Ref | Contribution |
|---|---|
| [15] | One small expert-rated safety study |
| [14] | Systematic safety evidence |
| [11] | Expert-rated quality of running plans; advises expert feedback |
| [24] | Knowledge grounding |
| [13], [16] | Evaluation rigor; hallucination |

Still missing: peer-reviewed work on *programmatic* validation or guardrails for LLM health advice (searches returned only preprints/software, none adopted).

## Remaining missing literature areas
1. A documented search protocol supporting any gap or novelty statement.
2. Sources for the long-run share, quality share, cutback and taper magnitudes, and feasibility thresholds.
3. Sources from which questionnaire items can be adapted.
4. Programmatic validation/guardrail literature for LLM health recommendations.
5. Confirmation of volume/pages for [12] and [14].
