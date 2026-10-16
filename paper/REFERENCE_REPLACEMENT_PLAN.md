# REFERENCE_REPLACEMENT_PLAN

## Execution status (2026-10-01)

The plan below was written with the OLD numbering (31 references). It has now been executed in `PAPER_DRAFT.md` / `PAPER_IEEE.docx` (33 references, current numbering).

| Plan item | Decision | Result |
|---|---|---|
| Fix [9] Hou author list | Done | "Y. Hou et al."; "sensitivities" clause removed |
| [29] Zheng | Claim verified on arXiv-version abstract; reference kept; NeurIPS record not opened; DOI left as registered in Crossref | Now [31]; VERIFY MANUALLY (publisher page) |
| [23] He Z. | Validator wording removed | Now [24]; full-text check pending |
| [25] Daniels | Not changed | Now [27]; edition and zone fractions pending |
| [27] Gabbett weak uses | Removed from Table II and V-E | Now [28], used only in II-D |
| [14] Akrimi | Reworded | Now [15] |
| [18] Seiler & Kjerland wording | Manuscript cites only the observed distribution | Now [20] |
| [30] Sullivan & Artino → Norman 2010 | **Replaced**: Norman verified in Crossref, doi.org and PubMed (PMID 20146096); full peer-reviewed article whose abstract addresses analysis of Likert data; Sullivan & Artino was a short commentary of uncertain peer-review status | Now [32] |
| [31] Tavakol & Dennick → Taber 2018 | Not replaced (Tavakol retained; Taber remains an option) | Now [33]; VERIFY MANUALLY |
| Add Düking 2024 | Done | [11] |
| Add Havers 2025 | Done | [12]; volume/pages [VERIFY] |
| Add He T. 2026 | Done | [14]; volume/pages [VERIFY] |
| Add Feely 2020 | Done | [26] |
| Add Issurin 2010 (periodization) | Done (not in the original plan) | [29] |
| Remove [13], [15], [2] | Done, for relevance/redundancy (not because of Scholar access) | Former [2], [13], [15] removed |
| Remove [29] (Zheng) | Not removed: claim verified | Kept as [31] |
| Optional additions (Garber, Bull, Tran, Ni) | Not adopted | — |

Google Scholar: 9 of the retained original references were directly confirmed; the rest are "not verified due to access limitation", not "not found".

---

# Original plan (OLD numbering)

Audit date: 2026-10-01. **No change has been applied to `PAPER_DRAFT.md` or `PAPER_IEEE.docx`.** Result of the audit: 0 references need mandatory replacement (none fabricated, none pre-2001, all DOIs resolve); 7 need manual verification; several wording/citation fixes and four recommended additions follow.

## 1. Mandatory fixes (no replacement of the reference itself)

| Ref | Problem | Fix |
|---|---|---|
| [9] Hou et al. | Author list in the manuscript has 6 names; Crossref and Scholar list 7 (adds W. X. Zhao). The "sensitivities" claim is unverified | Cite as "Y. Hou *et al.*"; read the abstract and keep or delete the clause |
| [29] Zheng et al. | DOI resolves to proceedings.com (third party), not the NeurIPS site | Replace DOI with the NeurIPS proceedings URL (obtain from neurips.cc); confirm Datasets and Benchmarks track; or drop the reference (not used by the method) |
| [23] He Z. et al. | "Closed-loop rule-based safety validator" not confirmed by the abstract | Read full text (Sci. Rep. 16:6793); keep or delete the phrase |
| [25] Daniels | Edition/year ambiguity (Crossref: 4th ed., 2022) | Check the physical book; compare zone fractions 0.65/0.74/0.80/0.88/0.98/1.05 |
| [2], [30], [31] | Short/editorial-type items; peer-review status uncertain | Verify on publisher pages; consider replacing [30], [31] (below) |
| [27] | Used in two weak places (Table II cutback row; V-E negative claim) | Remove those two citations; keep it in II-D |
| [14] | One small study generalized as "studies" | Reword; add He T. 2026 for generalization |
| [18] | Title says "elite"; sample is junior skiers | Reword to "well-trained junior skiers" |

## 2. Recommended replacements

| Current | Proposed | Why | Verification state |
|---|---|---|---|
| [30] Sullivan & Artino (short commentary) | G. Norman, "Likert scales, levels of measurement and the 'laws' of statistics," *Adv. Health Sci. Educ.*, vol. 15, no. 5, pp. 625–632, 2010, doi 10.1007/s10459-010-9222-y | Full peer-reviewed article on Likert analysis | Crossref VERIFIED; Scholar NOT CHECKED |
| [31] Tavakol & Dennick (editorial-type) — optional | K. S. Taber, "The use of Cronbach's alpha when developing and reporting research instruments in science education," *Res. Sci. Educ.*, vol. 48, no. 6, pp. 1273–1296, 2018, doi 10.1007/s11165-016-9602-2 | Full article on alpha in instrument development (relevant to the 16-item instrument) | Crossref VERIFIED; Scholar NOT CHECKED |

## 3. Recommended additions (fill the gaps)

| Priority | Reference | Gap filled | Verification state |
|---|---|---|---|
| **1 — must add** | P. Düking, B. Sperlich, L. Voigt, B. Van Hooren, M. Zanini, and C. Zinner, "ChatGPT generated training plans for runners are not rated optimal by coaching experts, but increase in quality with additional input information," *J. Sports Sci. Med.*, vol. [VERIFY MANUALLY], pp. 56–72, 2024, doi 10.52082/jssm.2024.56 | Directly running-specific; six-week plans, 22 expert criteria; invalidates the draft's current gap statement | Crossref VERIFIED (no volume in record); Europe PMC VERIFIED (PMID 38455449); Scholar NOT CHECKED |
| 2 | T. Havers, L. Masur, E. Isenmann, S. Geisler, C. Zinner, B. Sperlich, and P. Düking, "Reproducibility and quality of hypertrophy-related training plans generated by GPT-4 and Google Gemini as evaluated by coaching experts," *Biol. Sport*, 2025, doi 10.5114/biolsport.2025.145911 | Closest precedent for RQ2 (two LLMs, repeated generation, expert rating) | Crossref + Europe PMC (PMID 40182716) VERIFIED; volume/pages [VERIFY MANUALLY] (Crossref none; Europe PMC shows pp. 289–329, suspicious) |
| 3 | T. He, D. Lu, Y. Ma, J. He, D. Li, and G. Li, "The AI recommendation paradox: a systematic review evaluating the promise, peril, and path forward for large language models in exercise recommendation," *Biol. Sport*, 2026, doi 10.5114/biolsport.2026.158676 | Systematic evidence on safety/efficacy (24 studies; safety flaws in 14/24) | Crossref + Europe PMC (PMID 42422387) VERIFIED; volume [VERIFY MANUALLY] |
| 4 | C. Feely, B. Caulfield, A. Lawlor, and B. Smyth, "Providing explainable race-time predictions and training plan recommendations to marathon runners," in *Proc. 14th ACM Conf. Recommender Syst.*, 2020, pp. 539–544, doi 10.1145/3383313.3412220 | Running-specific recommender with explanation (conference) | Crossref VERIFIED; Scholar NOT CHECKED |
| Optional | Garber et al., *Med. Sci. Sports Exerc.*, 43(7):1334–1359, 2011, doi 10.1249/MSS.0b013e318213fefb; Bull et al., *Br. J. Sports Med.*, 54(24):1451–1462, 2020, doi 10.1136/bjsports-2020-102955; Tran et al., *J. Intell. Inf. Syst.*, 57(1):171–201, 2020, doi 10.1007/s10844-020-00633-6; Ni et al., WWW 2019, doi 10.1145/3308558.3313643 | General exercise-prescription guidance; health recommenders; fitness recommendation | Crossref VERIFIED; relevance moderate — add only if a sentence needs them |

Rejected candidates: preprints (arXiv: "Exploring LLM as an Interactive Sports Coach… half marathon", PlanFitting, consistency of AI exercise prescriptions) — not peer reviewed; a marathon-handbook web page (non-scholarly); SSRN/CRAN guardrail items (not peer reviewed); Galitsky 2025 book chapter (low relevance, not read).

## 4. Candidates for removal if the list must shrink to ≈30

| Ref | Reason |
|---|---|
| [13] | Overlaps [12]; only supports "early stage" |
| [15] | General NLG hallucination; [16] covers LLMs |
| [2] | Editorial-type, peer review uncertain, partial relevance |
| [29] | Not used in the method; DOI problem |

Net effect of "replace [30] with Norman, add Düking, Havers, He T., Feely, remove [2], [13], [15], [29]" → **31 references** (31 − 4 + 4).

## 5. Required follow-up in the manuscript (when you allow rewriting)

1. Rewrite the research-gap statement (Sections I and II-F) around Düking 2024 and Havers 2025.
2. Fix citation of [9]; qualify [14]; remove [27] from the cutback row and V-E.
3. Replace the range citation "[17]–[22]" with individual citations.
4. Renumber references in order of first appearance after changes.

## 6. Manual checks only you can do
1. Google Scholar title search for the 21 references not verified here (all except [1], [2], [4]–[9], [11], [14]) and for every candidate above.
2. Open each publisher page for [23], [25], [29], [2], [30], [31].
3. Confirm volumes for Düking 2024 (JSSM), Havers 2025, He T. 2026.
4. Decide on the pre-2001 Daniels–Gilbert (1979) source — still not cited.
