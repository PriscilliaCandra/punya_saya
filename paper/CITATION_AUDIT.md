# CITATION_AUDIT

## Round 2 — corrections applied to PAPER_DRAFT.md (current numbering)

Numbers in this section are the **current** reference numbers (33 references). The Round-1 table further below keeps the **old** numbering of the pre-correction manuscript (31 references) and is retained as the audit record; see the old-to-new table in `REFERENCES_VERIFICATION.md`.

| Round-1 row | Problem | Correction applied | Where now |
|---|---|---|---|
| 12, 25 | Gap statement said no peer-reviewed LLM running-plan study exists; contradicted by Düking et al. 2024 | Gap rewritten: running-plan generation by LLMs is acknowledged [11]; gap restated as limited evidence on a hybrid design with deterministic baseline, post-generation validation, same-profile/same-baseline multi-LLM comparison, and user perception; explicit statement that novelty beyond the literature is not claimed; [VERIFY] search protocol | I (paragraph 3), II-F |
| — | Düking 2024 missing | Added with verified bibliographic data (J. Sports Sci. Med. 23(1):56–72, 2024, doi 10.52082/jssm.2024.56); described at abstract level; methodological comparison paragraph added (direct generation vs baseline + personalization; post-generation validation; model comparison; expert vs runner evaluation); no superiority claim | II-C |
| 37 | Gabbett cited for the cutback row | Citation removed; cutback classified as an engineering design constraint; Issurin 2010 [29] cited only for the periodization concept | Table II |
| 45 | Gabbett cited for the "no performance claim" sentence | Replaced by the systematic review [14] (LLM plans inferior to expert plans in most head-to-head trials of physiological adaptation) | V-E item (6) |
| 7 | Akrimi (one small study) described as "individual studies" | Reworded: "one exploratory expert review of plans for fictional patients with type 2 diabetes"; [15] described as a discussion paper based on preliminary data | I, II-C, V-E |
| 10 | "Closed-loop rule-based safety validator" attributed to He et al. | Removed; text now limited to what the abstract supports (knowledge-graph grounding; gains over baselines on coherence, goal relevance, predicted satisfaction); full-text check listed as [VERIFY] | I, II-C |
| 33 | LLM-as-a-judge claim not verified | Claim verified on the arXiv-version abstract (position, verbosity, self-enhancement biases; limited reasoning; approximates human preferences); wording matched to it; NeurIPS record itself not opened | II-E |
| 18 | Hou et al. "sensitivities" claim unverified; author list incomplete | Clause removed; author list changed to "Y. Hou et al." | II-B, References |
| 6 | "[12], [13]" cited for heterogeneous/low-rigor evaluation | Only the scoping review of 20 studies [13] cited for that statement; former [13] removed | I, II-C |
| 14 | Former [2] "open challenges" claim unconfirmed | Sentence and reference removed | II-A |
| 34 | Likert claim rested on a short commentary | Replaced by Norman 2010 [32]; wording changed to "analysis of Likert data is debated; parametric methods argued robust" | II-E, III-K |
| 36, 38, 39, 40, 43 | Rule constants cited to sources that do not give those values | Table II now has a Classification column; factors, cutback, caps, shares and feasibility thresholds are labelled engineering design constraints or implementation heuristics; only direction of taper effects is attributed to [22], [23] | III-D, III-E, Table II |
| 9 | Range citation "[17]–[22]" | Split into individual citations by topic | I |
| 5 | Chatbot studies "compared with guidelines" | Now "guidelines or coaching-expert criteria" to include [11], [12] | I, II-C |

Open after Round 2: full-text checks of [24], [11], [12] for post-generation validation; volume/pages of [12], [14]; peer-review type check for [33]; search protocol for the gap statement; sources for rule constants (see `PAPER_GAPS.md` Section 5b).

---

# Round 1 — original audit (OLD numbering, 31 references; kept as the audit record)

Audit date: 2026-10-01. Each row compares a literature-based claim in `PAPER_DRAFT.md` with what the cited source's abstract/metadata supports. Only abstracts were read. "Supports?" values: YES, PARTIAL, NO, UNVERIFIED (abstract not available), NONE (no citation).

| # | Section | Paper claim | Citation | Supports? | Action |
|---|---|---|---|---|---|
| 1 | I | Personalization is the central promise of recommender systems | [1], [2] | YES for [1]; PARTIAL for [2] (abstract: personalized recommendations are ubiquitous) | Keep [1]; [2] optional |
| 2 | I | Quality is judged by perceived user experience, not only accuracy | [3], [4] | YES | Keep |
| 3 | I | LLMs proposed for recommender systems because of world knowledge and reasoning | [5], [6] | YES for [5] (abstract: open-domain knowledge, reasoning); UNVERIFIED for [6] | Keep; read [6] abstract |
| 4 | I | LLMs adapted via instruction tuning [7], text-to-text [8], zero-shot ranking [9] | [7], [8], [9] | YES (abstracts for [7], [8]); title-level for [9] | Keep |
| 5 | I, II-C | Chatbots used to generate exercise recommendations/programs and compared with guidelines | [10], [11] | YES | Keep |
| 6 | I | Reviews report heterogeneous and often low-rigor evaluation of LLM exercise recommendation | [12], [13] | YES for [12] (median rigor 2.5/5; heterogeneous); PARTIAL for [13] (says early-stage, 11 studies) | Cite [12] for rigor; [13] for "early-stage" only |
| 7 | I | Individual studies documented safety problems in LLM-generated plans for clinical populations | [14] | PARTIAL: one study, three fictional T2DM profiles, "preliminary data" | Reword to "one expert review"; add He T. 2026 systematic review (14/24 studies with safety flaws) after verifying volume |
| 8 | I | LLMs produce fluent but unfaithful content | [15], [16] | YES ([16] "plausible yet nonfactual"; [15] hallucination in NLG) | Keep |
| 9 | I | Training science treats volume progression, intensity distribution, tapering as managed quantities | [17]–[22] | YES collectively; range citation hides which source supports what | Split into individual citations in the text |
| 10 | I, II-C | A recent LLM + sports-science knowledge graph approach with a closed-loop rule-based safety validator | [23] | PARTIAL: abstract confirms knowledge-graph grounding and baseline comparison; validator/regeneration not in abstract | Read full text; if not confirmed, delete "closed-loop rule-based safety validator" |
| 11 | I, II-C | Fine-tuned personal-health LLM evaluated for sleep/fitness coaching | [24] | YES | Keep |
| 12 | I, II-F | "To our knowledge… a lightweight hybrid design for running plans… has not been reported" | none | **NONE; contradicted in part**: Düking 2024 (JSSM) evaluated ChatGPT running plans; Feely 2020 recommended marathon plans | Rewrite the gap claim around "constrained LLM personalization with programmatic validation and cross-LLM comparison" and cite Düking; add search protocol |
| 13 | II-A | Survey proposed extensions: richer user/item models, context, multicriteria | [1] | YES (abstract) | Keep |
| 14 | II-A | Retrospective reviews history and open challenges | [2] | PARTIAL (history yes; challenges unconfirmed) | Verify or soften |
| 15 | II-A | Knijnenburg: system characteristics affect perceived quality and experience | [3] | YES | Keep |
| 16 | II-A | Pu et al.: questionnaire-based user-centric framework | [4] | YES (ResQue) | Keep |
| 17 | II-B | TALLRec tunes an LLM with recommendation instructions; P5 unified text-to-text | [7], [8] | YES | Keep |
| 18 | II-B | Hou et al. report sensitivities in how LLMs use interaction history | [9] | UNVERIFIED (abstract missing) | Read abstract or delete the clause |
| 19 | II-B | Hallucination documented; mitigation needed | [15], [16] | YES | Keep |
| 20 | II-C | Washif: ChatGPT 12-week programs vs guidelines; Zaleski: 26 populations; Akrimi: expert review | [10], [11], [14] | YES | Keep |
| 21 | II-C | Scoping review found a small early-stage body of work | [13] | YES (11 of 598 studies) | Keep |
| 22 | II-C | 20 studies, median rigor 2.5/5 | [12] | YES | Keep |
| 23 | II-C | He et al.: gains over baselines on plan coherence and goal relevance | [23] | YES (abstract) | Keep |
| 24 | II-C | Khasentino: performed similarly to experts on fitness case studies | [24] | YES | Keep |
| 25 | II-C | "None of the sources isolates the personalization layer on a deterministic running baseline across several LLMs" | none | NONE (author claim); weakened by Havers 2025 (GPT-4 vs Gemini) and Düking 2024 | Qualify; cite Havers/Düking as closest precedents |
| 26 | II-D | VDOT derived from a race result sets paces | [25] | YES (book subject) but edition/content unverified | Verify against book |
| 27 | II-D | ~80/20 low/high intensity sessions in endurance training | [17], [18] | YES ([17]); PARTIAL ([18]: junior skiers, 75/8/17) | Keep; correct "elite" wording |
| 28 | II-D | Randomized study in well-trained athletes: polarized gave the largest gains | [19] | YES (n=48, 9 weeks) | Keep with caveat (already stated) |
| 29 | II-D | 10% rule evidence is mixed: RCT showed no reduction [21]; cohort no overall difference [20] | [20], [21] | YES | Keep |
| 30 | II-D | Taper: maintain intensity, reduce volume; 2-week exponential taper best | [22], [26] | YES | Keep |
| 31 | II-D | Load management balances stimulus and injury risk | [27] | YES (abstract) | Keep |
| 32 | II-E | LLM evaluation organized by what/where/how | [28] | YES | Keep |
| 33 | II-E | LLM-as-a-judge examined for scalable assessment, with biases | [29] | UNVERIFIED (abstract missing); DOI resolves to third-party site | Replace DOI with NeurIPS URL; verify abstract or remove |
| 34 | II-E, III-K | Likert data ordinal → report medians/distributions | [30] | YES, but source is a short commentary | Keep or replace with Norman 2010 |
| 35 | II-E, III-K | Cronbach's alpha for internal consistency | [31] | YES, but short editorial-type article | Keep or add Taber 2018 |
| 36 | III-E Table II | Gradual progression / 10% heuristic is contested | [20], [21] | YES for "contested"; PARTIAL as support for the specific ×1.06/1.08 factors (no source gives these) | Say the factors are design choices |
| 37 | III-E Table II | Cutback rows cite "Load management" | [27] | **WEAK**: [27] does not support a 4th-week 15% deload | Remove citation or cite a source on deload weeks (none found yet) |
| 38 | III-E Table II | Taper 0.85× and 0.55× of base volume | [22], [26] | PARTIAL: sources support reducing volume while keeping intensity, not these factors | State factors as design choices |
| 39 | III-E Table II | Quality session ≈20% / low-high split | [17], [18] | PARTIAL: sources report share of *sessions*, code uses share of *distance* | Already noted in text; keep wording |
| 40 | III-E | Long run 30%, caps 12/16/21 km, floors 4/3.5/3 km | none | NONE (design heuristic) | Label as design heuristic (done); find source or justify |
| 41 | III-D | Equations (1)–(3) attributed to Daniels and Gilbert | none (source pre-2001) | NONE | Await approval of the 1979 source; [25] cited for the approach |
| 42 | III-D | Zone fractions 0.65–1.05 | [25] | UNVERIFIED | Cross-check with the book |
| 43 | III-D | Feasibility thresholds 3.5% / 6.5% | none | NONE | Already flagged [VERIFY/JUSTIFY] |
| 44 | V-E | Validation does not verify text safety; text may contain unverified advice | [14] | PARTIAL (relevant to unsafe plans, not to this validator) | Keep as context only |
| 45 | V-E | "No claim of improved performance or injury reduction is made" | [27] | **WEAK/irrelevant** (a negative claim does not need this citation) | Remove [27] here |
| 46 | V-E | Progression rationale has mixed evidence | [20], [21] | YES | Keep |

## Summary
- Of 46 rows: 30 supported (YES, some with caveats), 6 PARTIAL, 3 UNVERIFIED (abstract unavailable), 5 with no citation (NONE), 2 WEAK. The substantive problems are rows 12, 25, 37 and 45.
- Mandatory fixes: row 7 (generalization from one study), row 10 (validator claim), row 12 (gap claim contradicted by Düking 2024), rows 37 and 45 (weak [27] citations), row 18 and 33 (unverified claims).
- Fix the author list of [9] (Crossref and Scholar list 7 authors incl. W. X. Zhao).
- No citation was added merely to look academic; candidate additions are listed in `REFERENCE_REPLACEMENT_PLAN.md`.
