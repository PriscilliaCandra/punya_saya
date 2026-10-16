# REFERENCES_VERIFICATION

Updated 2026-10-01 after the reference audit and manuscript revision. Numbering follows `PAPER_DRAFT.md` (references renumbered by order of first citation). **33 references.**

## Changes to the reference list
- **Removed:** former [2] Jannach et al. (editorial-type; partial relevance; [1] suffices), former [13] Lai et al. scoping review (overlaps former [12], now [13]; the evidence-base size is now supported by the systematic review [14]), former [15] Ji et al. (general NLG hallucination; the LLM-specific survey [16] remains). None was removed because of Google Scholar access problems.
- **Replaced:** former [30] Sullivan & Artino → Norman 2010 ([32]): full peer-reviewed article, PubMed-indexed, abstract directly about the analysis of Likert data, versus a short commentary of uncertain peer-review status.
- **Added:** [11] Düking 2024, [12] Havers 2025, [14] He T. 2026, [26] Feely 2020, [29] Issurin 2010.
- **Corrected:** author list of [8] (Hou et al., 7 authors).

## Old-to-new numbering
| Former | Current |
|---|---|
| [1] | [1] |
| [3] | [2] |
| [4] | [3] |
| [5] | [4] |
| [6] | [5] |
| [7] | [6] |
| [8] | [7] |
| [9] | [8] |
| [10] | [9] |
| [11] | [10] |
| [12] | [13] |
| [14] | [15] |
| [16] | [16] |
| [17] | [19] |
| [18] | [20] |
| [19] | [21] |
| [20] | [17] |
| [21] | [18] |
| [22] | [22] |
| [23] | [24] |
| [24] | [25] |
| [25] | [27] |
| [26] | [23] |
| [27] | [28] |
| [28] | [30] |
| [29] | [31] |
| [31] | [33] |
| [2], [13], [15], [30] | removed / replaced as described above |

## How each field was checked

| Check | Source actually used | Result |
|---|---|---|
| Authors, exact title, year, venue, volume, issue, pages, publisher, record type | Crossref REST API by DOI | Match the manuscript except where a note says otherwise |
| Independent index (type, year, venue, retraction flag) | OpenAlex API by DOI | Found for all 33; no retractions flagged |
| DOI resolves to a publisher | HTTP HEAD to doi.org | All 33 redirect to a publisher/society site (one, [31], to a third-party proceedings site) |
| PubMed record (biomedical items) | Europe PMC | Found for the medical/sports-science items |
| Google Scholar title search | WebFetch of scholar.google.com | **Directly confirmed for 9 of the 31 pre-existing references that remain in the list.** After those, Scholar returned CAPTCHA/error pages, so the others are *not verified due to access limitation*; they are **not** reported as absent. The 6 new references were not queried in Scholar. |
| Publisher page content | Not opened (PMC/MDPI/Nature returned CAPTCHA/403/redirect to automated fetches) | "Publisher or DOI: VERIFIED" means DOI registered with the publisher and resolving to the publisher domain |

Only abstracts were consulted; no full text was read. No reference predates 2001 (earliest: 2003). No reference was found to be fabricated.

## Summary
| Item | Count |
|---|---|
| Total | 33 |
| Journal-type articles (incl. surveys, reviews, meta-analysis) | 26 |
| Conference papers | 6 |
| Books | 1 |
| Status KEEP | 27 |
| Status VERIFY MANUALLY | 6 |
| Status REPLACE | 0 |
| Google Scholar directly confirmed | 9 |
| Before 2001 | 0 |
| Potentially fabricated | 0 |

---
### Reference [1] (former [1])
- **Authors:** G. Adomavicius; A. Tuzhilin
- **Exact title:** Toward the next generation of recommender systems: a survey of the state-of-the-art and possible extensions
- **Publication year:** 2005 (Crossref print [[2005, 6]]; online None; OpenAlex 2005)
- **Journal/conference:** IEEE Transactions on Knowledge and Data Engineering
- **Publication type:** Journal Article (survey)
- **Publisher:** Institute of Electrical and Electronics Engineers (IEEE)
- **Volume:** 17  **Issue:** 6  **Pages/article number:** 734-749
- **DOI:** 10.1109/TKDE.2005.99  (doi.org redirects to: http://ieeexplore.ieee.org/document/1423975/)
- **Google Scholar:** VERIFIED (title match in Google Scholar)
- **Publisher or DOI:** VERIFIED (Crossref record + doi.org redirect to publisher domain; article page not read)
- **Year:** VERIFIED
- **Academic publication:** YES
- **Peer reviewed:** YES
- **Relevant to this research:** YES
- **Claim supported:** Recommender systems are grouped into content-based/collaborative/hybrid; survey proposes extensions (richer user/item models, context, multicriteria ratings). Used in I, II-A.
- **Status:** **KEEP**

### Reference [2] (former [3])
- **Authors:** Bart P. Knijnenburg; Martijn C. Willemsen; Zeno Gantner; Hakan Soncu; Chris Newell
- **Exact title:** Explaining the user experience of recommender systems
- **Publication year:** 2012 (Crossref print [[2012, 10]]; online [[2012, 3, 10]]; OpenAlex 2012)
- **Journal/conference:** User Modeling and User-Adapted Interaction
- **Publication type:** Journal Article
- **Publisher:** Springer Science and Business Media LLC
- **Volume:** 22  **Issue:** 4-5  **Pages/article number:** 441-504
- **DOI:** 10.1007/s11257-011-9118-4  (doi.org redirects to: http://link.springer.com/10.1007/s11257-011-9118-4)
- **Google Scholar:** NOT VERIFIED due to access limitation (Scholar returned a CAPTCHA/error page; this does NOT mean the item is absent from Scholar)
- **Publisher or DOI:** VERIFIED (Crossref record + doi.org redirect to publisher domain; article page not read)
- **Year:** VERIFIED
- **Academic publication:** YES
- **Peer reviewed:** YES
- **Relevant to this research:** YES
- **Claim supported:** Framework linking system aspects to user experience through subjective constructs. Used in I, II-A, III-J.
- **Status:** **KEEP**

### Reference [3] (former [4])
- **Authors:** Pearl Pu; Li Chen; Rong Hu
- **Exact title:** A user-centric evaluation framework for recommender systems
- **Publication year:** 2011 (Crossref print [[2011, 10, 23]]; online [[2011, 10, 23]]; OpenAlex 2011)
- **Journal/conference:** Proceedings of the fifth ACM conference on Recommender systems
- **Publication type:** Conference Paper
- **Publisher:** ACM
- **Volume:** n/a  **Issue:** n/a  **Pages/article number:** 157-164
- **DOI:** 10.1145/2043932.2043962  (doi.org redirects to: https://dl.acm.org/doi/10.1145/2043932.2043962)
- **Google Scholar:** VERIFIED (title match in Google Scholar)
- **Publisher or DOI:** VERIFIED (Crossref record + doi.org redirect to publisher domain; article page not read)
- **Year:** VERIFIED
- **Academic publication:** YES
- **Peer reviewed:** YES
- **Relevant to this research:** YES
- **Claim supported:** ResQue: questionnaire-based user-centric evaluation framework for recommender systems. Used in I, II-A, III-J.
- **Status:** **KEEP**
- **Notes:** Authors: Pu, Chen, Hu (3). Conference, not a journal.

### Reference [4] (former [5])
- **Authors:** Jianghao Lin; Xinyi Dai; Yunjia Xi; Weiwen Liu; Bo Chen; Hao Zhang; Yong Liu; Chuhan Wu; Xiangyang Li; Chenxu Zhu; Huifeng Guo; Yong Yu; et al. (14 authors in Crossref)
- **Exact title:** How Can Recommender Systems Benefit from Large Language Models: A Survey
- **Publication year:** 2025 (Crossref print [[2025, 3, 31]]; online [[2025, 1, 18]]; OpenAlex 2024)
- **Journal/conference:** ACM Transactions on Information Systems
- **Publication type:** Journal Article (survey)
- **Publisher:** Association for Computing Machinery (ACM)
- **Volume:** 43  **Issue:** 2  **Pages/article number:** 1-47
- **DOI:** 10.1145/3678004  (doi.org redirects to: https://dl.acm.org/doi/10.1145/3678004)
- **Google Scholar:** VERIFIED (title match in Google Scholar)
- **Publisher or DOI:** VERIFIED (Crossref record + doi.org redirect to publisher domain; article page not read)
- **Year:** VERIFIED
- **Academic publication:** YES
- **Peer reviewed:** YES
- **Relevant to this research:** YES
- **Claim supported:** LLMs entering recommender systems; RS limitations (open-domain knowledge) that LLMs may address. Used in I, II-B.
- **Status:** **KEEP**

### Reference [5] (former [6])
- **Authors:** Likang Wu; Zhi Zheng; Zhaopeng Qiu; Hao Wang; Hongchao Gu; Tingjia Shen; Chuan Qin; Chen Zhu; Hengshu Zhu; Qi Liu; Hui Xiong; Enhong Chen
- **Exact title:** A survey on large language models for recommendation
- **Publication year:** 2024 (Crossref print [[2024, 9]]; online [[2024, 8, 22]]; OpenAlex 2024)
- **Journal/conference:** World Wide Web
- **Publication type:** Journal Article (survey)
- **Publisher:** Springer Science and Business Media LLC
- **Volume:** 27  **Issue:** 5  **Pages/article number:** 60
- **DOI:** 10.1007/s11280-024-01291-2  (doi.org redirects to: https://link.springer.com/10.1007/s11280-024-01291-2)
- **Google Scholar:** VERIFIED (title match in Google Scholar)
- **Publisher or DOI:** VERIFIED (Crossref record + doi.org redirect to publisher domain; article page not read)
- **Year:** VERIFIED
- **Academic publication:** YES
- **Peer reviewed:** YES
- **Relevant to this research:** YES
- **Claim supported:** Survey on LLMs for recommendation. Used in I, II-B.
- **Status:** **KEEP**
- **Notes:** Abstract not available via OpenAlex; supported by title/venue only.

### Reference [6] (former [7])
- **Authors:** Keqin Bao; Jizhi Zhang; Yang Zhang; Wenjie Wang; Fuli Feng; Xiangnan He
- **Exact title:** TALLRec: An Effective and Efficient Tuning Framework to Align Large Language Model with Recommendation
- **Publication year:** 2023 (Crossref print [[2023, 9, 14]]; online [[2023, 9, 14]]; OpenAlex 2023)
- **Journal/conference:** Proceedings of the 17th ACM Conference on Recommender Systems
- **Publication type:** Conference Paper
- **Publisher:** ACM
- **Volume:** n/a  **Issue:** n/a  **Pages/article number:** 1007-1014
- **DOI:** 10.1145/3604915.3608857  (doi.org redirects to: https://dl.acm.org/doi/10.1145/3604915.3608857)
- **Google Scholar:** VERIFIED (title match in Google Scholar)
- **Publisher or DOI:** VERIFIED (Crossref record + doi.org redirect to publisher domain; article page not read)
- **Year:** VERIFIED
- **Academic publication:** YES
- **Peer reviewed:** YES
- **Relevant to this research:** YES
- **Claim supported:** Tuning an LLM with recommendation instructions (TALLRec). Used in I, II-B.
- **Status:** **KEEP**
- **Notes:** Conference, not a journal.

### Reference [7] (former [8])
- **Authors:** Shijie Geng; Shuchang Liu; Zuohui Fu; Yingqiang Ge; Yongfeng Zhang
- **Exact title:** Recommendation as Language Processing (RLP): A Unified Pretrain, Personalized Prompt & Predict Paradigm (P5)
- **Publication year:** 2022 (Crossref print [[2022, 9, 18]]; online [[2022, 9, 13]]; OpenAlex 2022)
- **Journal/conference:** Proceedings of the 16th ACM Conference on Recommender Systems
- **Publication type:** Conference Paper
- **Publisher:** ACM
- **Volume:** n/a  **Issue:** n/a  **Pages/article number:** 299-315
- **DOI:** 10.1145/3523227.3546767  (doi.org redirects to: https://dl.acm.org/doi/10.1145/3523227.3546767)
- **Google Scholar:** VERIFIED (title match in Google Scholar)
- **Publisher or DOI:** VERIFIED (Crossref record + doi.org redirect to publisher domain; article page not read)
- **Year:** VERIFIED
- **Academic publication:** YES
- **Peer reviewed:** YES
- **Relevant to this research:** YES
- **Claim supported:** P5: recommendation tasks as unified text-to-text with personalized prompts. Used in I, II-B.
- **Status:** **KEEP**
- **Notes:** Conference, not a journal.

### Reference [8] (former [9])
- **Authors:** Yupeng Hou; Junjie Zhang; Zihan Lin; Hongyu Lu; Ruobing Xie; Julian McAuley; Wayne Xin Zhao
- **Exact title:** Large Language Models are Zero-Shot Rankers for Recommender Systems
- **Publication year:** 2024 (Crossref print [[2024]]; online [[2024, 3, 16]]; OpenAlex 2024)
- **Journal/conference:** Lecture Notes in Computer Science
- **Publication type:** Conference Paper (ECIR 2024; published as a Springer LNCS book chapter)
- **Publisher:** Springer Nature Switzerland
- **Volume:** n/a  **Issue:** n/a  **Pages/article number:** 364-381
- **DOI:** 10.1007/978-3-031-56060-6_24  (doi.org redirects to: https://link.springer.com/10.1007/978-3-031-56060-6_24)
- **Google Scholar:** VERIFIED (title match in Google Scholar)
- **Publisher or DOI:** VERIFIED (Crossref record + doi.org redirect to publisher domain; article page not read)
- **Year:** VERIFIED
- **Academic publication:** YES
- **Peer reviewed:** YES
- **Relevant to this research:** YES
- **Claim supported:** LLMs as zero-shot rankers for recommender systems. Used in I, II-B.
- **Status:** **VERIFY MANUALLY**
- **Notes:** Author list corrected in the manuscript to 'Y. Hou et al.' (7 authors in Crossref/Scholar). The clause about 'sensitivities' was removed from the manuscript; the remaining statement (LLMs as zero-shot rankers) is supported by the title. Abstract still not retrieved.

### Reference [9] (former [10])
- **Authors:** Jad Washif; Jeffrey Pagaduan; Carl James; Ismail Dergaa; Christopher Beaven
- **Exact title:** Artificial intelligence in sport: Exploring the potential of using ChatGPT in resistance training prescription
- **Publication year:** 2024 (Crossref print [[2024]]; online None; OpenAlex 2023)
- **Journal/conference:** Biology of Sport
- **Publication type:** Journal Article (research article; narrative comparison of ChatGPT output with guidelines)
- **Publisher:** Termedia Sp. z.o.o.
- **Volume:** 41  **Issue:** 2  **Pages/article number:** 209-220
- **DOI:** 10.5114/biolsport.2024.132987  (doi.org redirects to: https://www.termedia.pl/doi/10.5114/biolsport.2024.132987)
- **Google Scholar:** NOT VERIFIED due to access limitation (Scholar returned a CAPTCHA/error page; this does NOT mean the item is absent from Scholar)
- **Publisher or DOI:** VERIFIED (Crossref record + doi.org redirect to publisher domain; article page not read)
- **Year:** VERIFIED
- **Academic publication:** YES
- **Peer reviewed:** YES
- **Relevant to this research:** PARTIALLY
- **Claim supported:** ChatGPT-designed 12-week resistance programs compared with guidelines/literature. Used in I, II-C.
- **Status:** **KEEP**
- **Notes:** Resistance training, not running; fictional profiles.

### Reference [10] (former [11])
- **Authors:** Amanda L Zaleski; Rachel Berkowsky; Kelly Jean Thomas Craig; Linda S Pescatello
- **Exact title:** Comprehensiveness, Accuracy, and Readability of Exercise Recommendations Provided by an AI-Based Chatbot: Mixed Methods Study
- **Publication year:** 2024 (Crossref print None; online [[2024, 1, 11]]; OpenAlex 2024)
- **Journal/conference:** JMIR Medical Education
- **Publication type:** Journal Article
- **Publisher:** JMIR Publications Inc.
- **Volume:** 10  **Issue:** n/a  **Pages/article number:** e51308
- **DOI:** 10.2196/51308  (doi.org redirects to: https://mededu.jmir.org/2024/1/e51308)
- **Google Scholar:** VERIFIED (title match in Google Scholar)
- **Publisher or DOI:** VERIFIED (Crossref record + doi.org redirect to publisher domain; article page not read)
- **Year:** VERIFIED
- **Academic publication:** YES
- **Peer reviewed:** YES
- **Relevant to this research:** PARTIALLY
- **Claim supported:** Chatbot exercise recommendations for 26 clinical populations scored for comprehensiveness, accuracy, readability. Used in I, II-C.
- **Status:** **KEEP**
- **Notes:** Clinical-population focus.

### Reference [11] (NEW (added in this revision))
- **Authors:** Peter Düking; Billy Sperlich; Laura Voigt; Bas Van Hooren; Michele Zanini; Christoph Zinner
- **Exact title:** ChatGPT Generated Training Plans for Runners are not Rated Optimal by Coaching Experts, but Increase in Quality with Additional Input Information
- **Publication year:** 2024 (Crossref print None; online [[2024, 3, 1]]; OpenAlex 2024)
- **Journal/conference:** Journal of Sports Science and Medicine
- **Publication type:** Journal Article (research article)
- **Publisher:** Journal of Sports Science and Medicine
- **Volume:** 23  **Issue:** 1  **Pages/article number:** 56-72
- **DOI:** 10.52082/jssm.2024.56  (doi.org redirects to: https://www.jssm.org/jssm-23-56.xml%3EFulltext)
- **Google Scholar:** NOT VERIFIED due to access limitation (Scholar not queried before the block; this does NOT mean the item is absent)
- **Publisher or DOI:** VERIFIED (Crossref record + doi.org redirect to publisher domain; article page not read)
- **Year:** VERIFIED
- **Academic publication:** YES
- **Peer reviewed:** YES
- **Relevant to this research:** YES
- **Claim supported:** Three ChatGPT-generated six-week running plans with increasing input detail; coaching experts rated 22 literature-derived criteria on a 5-point scale (Friedman test); plans rated sub-optimal, higher with more input information; authors advise against use without an expert coach. Used in I, II-C, II-F.
- **Status:** **KEEP**
- **Notes:** Volume 23, issue 1 from the publisher page URL (jssm-23-56) and OpenAlex; Crossref lacks volume/issue. Details beyond the abstract (ten experts, ChatGPT version, kappa) were NOT used in the manuscript; verify in full text. Peer-reviewed: journal indexed in PubMed (PMID 38455449).

### Reference [12] (NEW (added in this revision))
- **Authors:** Tim Havers; Lukas Masur; Eduard Isenmann; Stephan Geisler; Christoph Zinner; Billy Sperlich; Peter Düking
- **Exact title:** Reproducibility and quality of hypertrophy-related training plans generated by GPT-4 and Google Gemini as evaluated by coaching experts
- **Publication year:** 2025 (Crossref print None; online [[2025]]; OpenAlex 2024)
- **Journal/conference:** Biology of Sport
- **Publication type:** Journal Article (research article)
- **Publisher:** Termedia Sp. z.o.o.
- **Volume:** 42  **Issue:** 2  **Pages/article number:** [VERIFY MANUALLY]
- **DOI:** 10.5114/biolsport.2025.145911  (doi.org redirects to: https://www.termedia.pl/doi/10.5114/biolsport.2025.145911)
- **Google Scholar:** NOT VERIFIED due to access limitation (Scholar not queried before the block; this does NOT mean the item is absent)
- **Publisher or DOI:** VERIFIED (Crossref record + doi.org redirect to publisher domain; article page not read)
- **Year:** VERIFIED
- **Academic publication:** YES
- **Peer reviewed:** YES
- **Relevant to this research:** YES
- **Claim supported:** GPT-4 vs Google Gemini hypertrophy training plans; two prompts of different detail; 12 coaching experts; high reproducibility for repeated identical prompts; GPT-4 rated higher on several criteria. Used in I, II-C, II-F.
- **Status:** **VERIFY MANUALLY**
- **Notes:** Volume 42(2) and pages 289–329 come from OpenAlex/Europe PMC (Crossref has none; page range looks long) [VERIFY]. PMID 40182716. Resistance training, not running.

### Reference [13] (former [12])
- **Authors:** Xiangxun Lai; Yue Lai; JiaCheng Chen; Shengqi Huang; Qi Gao; Caihua Huang
- **Exact title:** Evaluation Strategies for Large Language Model-Based Models in Exercise and Health Coaching: Scoping Review
- **Publication year:** 2025 (Crossref print None; online [[2025, 10, 14]]; OpenAlex 2025)
- **Journal/conference:** Journal of Medical Internet Research
- **Publication type:** Review (scoping review, journal)
- **Publisher:** JMIR Publications Inc.
- **Volume:** 27  **Issue:** n/a  **Pages/article number:** e79217-e79217
- **DOI:** 10.2196/79217  (doi.org redirects to: https://www.jmir.org/2025/1/e79217)
- **Google Scholar:** NOT VERIFIED due to access limitation (Scholar returned a CAPTCHA/error page; this does NOT mean the item is absent from Scholar)
- **Publisher or DOI:** VERIFIED (Crossref record + doi.org redirect to publisher domain; article page not read)
- **Year:** VERIFIED
- **Academic publication:** YES
- **Peer reviewed:** YES
- **Relevant to this research:** YES
- **Claim supported:** 20 studies; heterogeneous evaluation; median rigor score 2.5/5. Used in I, II-C, II-F.
- **Status:** **KEEP**
- **Notes:** Now cited only for 'heterogeneous, low-rigor evaluation' (former [13] removed).

### Reference [14] (NEW (added in this revision))
- **Authors:** Tianyuan He; Di Lu; Yongye Ma; Jiaxin He; Duanying Li; Guoxing Li; Jian Sun
- **Exact title:** The AI recommendation paradox: a systematic review evaluating the promise, peril, and path forward for large language models in exercise recommendation
- **Publication year:** 2026 (Crossref print None; online [[2026]]; OpenAlex 2026)
- **Journal/conference:** Biology of Sport
- **Publication type:** Review (systematic review, journal)
- **Publisher:** Termedia Sp. z.o.o.
- **Volume:** 43  **Issue:** n/a  **Pages/article number:** [VERIFY MANUALLY]
- **DOI:** 10.5114/biolsport.2026.158676  (doi.org redirects to: https://www.termedia.pl/doi/10.5114/biolsport.2026.158676)
- **Google Scholar:** NOT VERIFIED due to access limitation (Scholar not queried before the block; this does NOT mean the item is absent)
- **Publisher or DOI:** VERIFIED (Crossref record + doi.org redirect to publisher domain; article page not read)
- **Year:** VERIFIED
- **Academic publication:** YES
- **Peer reviewed:** YES
- **Relevant to this research:** YES
- **Claim supported:** 24 empirical studies (N=2,512); LLM plans inferior to human experts in 5 of 6 head-to-head trials of physiological adaptation; safety flaws in 14 of 24. Used in I, II-C, V-E.
- **Status:** **VERIFY MANUALLY**
- **Notes:** Volume 43 and pages 949–961 from OpenAlex/Europe PMC; Crossref has none; issue unknown [VERIFY]. PMID 42422387.

### Reference [15] (former [14])
- **Authors:** Samir Akrimi; Leon Schwensfeier; Peter Düking; Thorsten Kreutz; Christian Brinkmann
- **Exact title:** ChatGPT-4o-Generated Exercise Plans for Patients with Type 2 Diabetes Mellitus—Assessment of Their Safety and Other Quality Criteria by Coaching Experts
- **Publication year:** 2025 (Crossref print None; online [[2025, 3, 24]]; OpenAlex 2025)
- **Journal/conference:** Sports
- **Publication type:** Journal Article (self-described discussion paper based on preliminary data)
- **Publisher:** MDPI AG
- **Volume:** 13  **Issue:** 4  **Pages/article number:** 92
- **DOI:** 10.3390/sports13040092  (doi.org redirects to: https://www.mdpi.com/2075-4663/13/4/92)
- **Google Scholar:** VERIFIED (title match in Google Scholar)
- **Publisher or DOI:** VERIFIED (Crossref record + doi.org redirect to publisher domain; article page not read)
- **Year:** VERIFIED
- **Academic publication:** YES
- **Peer reviewed:** YES (MDPI; weak design: 3 fictional patients)
- **Relevant to this research:** YES
- **Claim supported:** Experts rated plans for fictional T2DM patients; serious safety issues in some plans; detailed prompts tended to be rated better. Used in I, II-C, V-E.
- **Status:** **KEEP**
- **Notes:** Now described in the manuscript as one exploratory expert review (self-described discussion paper on preliminary data). Scholar lists the 4th author as 'Döking' (Scholar typo); Crossref: Düking.

### Reference [16] (former [16])
- **Authors:** Lei Huang; Weijiang Yu; Weitao Ma; Weihong Zhong; Zhangyin Feng; Haotian Wang; Qianglong Chen; Weihua Peng; Xiaocheng Feng; Bing Qin; Ting Liu
- **Exact title:** A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions
- **Publication year:** 2025 (Crossref print [[2025, 3, 31]]; online [[2025, 1, 24]]; OpenAlex 2024)
- **Journal/conference:** ACM Transactions on Information Systems
- **Publication type:** Journal Article (survey)
- **Publisher:** Association for Computing Machinery (ACM)
- **Volume:** 43  **Issue:** 2  **Pages/article number:** 1-55
- **DOI:** 10.1145/3703155  (doi.org redirects to: https://dl.acm.org/doi/10.1145/3703155)
- **Google Scholar:** NOT VERIFIED due to access limitation (Scholar returned a CAPTCHA/error page; this does NOT mean the item is absent from Scholar)
- **Publisher or DOI:** VERIFIED (Crossref record + doi.org redirect to publisher domain; article page not read)
- **Year:** VERIFIED
- **Academic publication:** YES
- **Peer reviewed:** YES
- **Relevant to this research:** YES
- **Claim supported:** LLMs generate plausible yet nonfactual content (hallucination). Used in I, II-B.
- **Status:** **KEEP**

### Reference [17] (former [20])
- **Authors:** Rasmus Østergaard Nielsen; Erik Thorlund Parner; Ellen Aagaard Nohr; Henrik Sørensen; Martin Lind; Sten Rasmussen
- **Exact title:** Excessive Progression in Weekly Running Distance and Risk of Running-Related Injuries: An Association Which Varies According to Type of Injury
- **Publication year:** 2014 (Crossref print [[2014, 10]]; online None; OpenAlex 2014)
- **Journal/conference:** Journal of Orthopaedic & Sports Physical Therapy
- **Publication type:** Journal Article (prospective cohort, n=874 novice runners)
- **Publisher:** Journal of Orthopaedic & Sports Physical Therapy (JOSPT)
- **Volume:** 44  **Issue:** 10  **Pages/article number:** 739-747
- **DOI:** 10.2519/jospt.2014.5164  (doi.org redirects to: https://www.jospt.org/doi/10.2519/jospt.2014.5164)
- **Google Scholar:** NOT VERIFIED due to access limitation (Scholar returned a CAPTCHA/error page; this does NOT mean the item is absent from Scholar)
- **Publisher or DOI:** VERIFIED (Crossref record + doi.org redirect to publisher domain; article page not read)
- **Year:** VERIFIED
- **Academic publication:** YES
- **Peer reviewed:** YES
- **Relevant to this research:** YES
- **Claim supported:** No significant overall injury-rate difference across weekly-distance progression groups (<10%, 10-30%, >30%); differences by injury type. Used in II-D, III-E, V-E.
- **Status:** **KEEP**

### Reference [18] (former [21])
- **Authors:** Ida Buist; Steef W. Bredeweg; Willem van Mechelen; Koen A. P. M. Lemmink; Gert-Jan Pepping; Ron L. Diercks
- **Exact title:** No Effect of a Graded Training Program on the Number of Running-Related Injuries in Novice Runners
- **Publication year:** 2008 (Crossref print [[2008, 1]]; online [[2007, 10, 16]]; OpenAlex 2007)
- **Journal/conference:** The American Journal of Sports Medicine
- **Publication type:** Journal Article (randomized controlled trial)
- **Publisher:** SAGE Publications
- **Volume:** 36  **Issue:** 1  **Pages/article number:** 33-39
- **DOI:** 10.1177/0363546507307505  (doi.org redirects to: https://journals.sagepub.com/doi/10.1177/0363546507307505)
- **Google Scholar:** NOT VERIFIED due to access limitation (Scholar returned a CAPTCHA/error page; this does NOT mean the item is absent from Scholar)
- **Publisher or DOI:** VERIFIED (Crossref record + doi.org redirect to publisher domain; article page not read)
- **Year:** VERIFIED
- **Academic publication:** YES
- **Peer reviewed:** YES
- **Relevant to this research:** YES
- **Claim supported:** A graded program based on the 10% rule did not reduce running-related injuries in novice runners. Used in II-D, III-E, V-E.
- **Status:** **KEEP**
- **Notes:** Year: 2008 (print Jan 2008; online Oct 2007).

### Reference [19] (former [17])
- **Authors:** Stephen Seiler
- **Exact title:** What is Best Practice for Training Intensity and Duration Distribution in Endurance Athletes?
- **Publication year:** 2010 (Crossref print [[2010, 9]]; online None; OpenAlex 2010)
- **Journal/conference:** International Journal of Sports Physiology and Performance
- **Publication type:** Review (journal)
- **Publisher:** Human Kinetics
- **Volume:** 5  **Issue:** 3  **Pages/article number:** 276-291
- **DOI:** 10.1123/ijspp.5.3.276  (doi.org redirects to: https://journals.humankinetics.com/view/journals/ijspp/5/3/article-p276.xml)
- **Google Scholar:** NOT VERIFIED due to access limitation (Scholar returned a CAPTCHA/error page; this does NOT mean the item is absent from Scholar)
- **Publisher or DOI:** VERIFIED (Crossref record + doi.org redirect to publisher domain; article page not read)
- **Year:** VERIFIED
- **Academic publication:** YES
- **Peer reviewed:** YES
- **Relevant to this research:** YES
- **Claim supported:** Descriptive studies converge on about 80% low-intensity / 20% high-intensity sessions in endurance athletes. Used in I, II-D, III-E.
- **Status:** **KEEP**

### Reference [20] (former [18])
- **Authors:** K. Stephen Seiler; Glenn Øvrevik Kjerland
- **Exact title:** Quantifying training intensity distribution in elite endurance athletes: is there evidence for an “optimal” distribution?
- **Publication year:** 2006 (Crossref print [[2006, 2]]; online [[2004, 10, 27]]; OpenAlex 2004)
- **Journal/conference:** Scandinavian Journal of Medicine & Science in Sports
- **Publication type:** Journal Article
- **Publisher:** Wiley
- **Volume:** 16  **Issue:** 1  **Pages/article number:** 49-56
- **DOI:** 10.1111/j.1600-0838.2004.00418.x  (doi.org redirects to: https://onlinelibrary.wiley.com/doi/10.1111/j.1600-0838.2004.00418.x)
- **Google Scholar:** NOT VERIFIED due to access limitation (Scholar returned a CAPTCHA/error page; this does NOT mean the item is absent from Scholar)
- **Publisher or DOI:** VERIFIED (Crossref record + doi.org redirect to publisher domain; article page not read)
- **Year:** VERIFIED
- **Academic publication:** YES
- **Peer reviewed:** YES
- **Relevant to this research:** PARTIALLY
- **Claim supported:** Intensity distribution 75/8/17% (HR zones) in 11 well-trained junior cross-country skiers. Used in II-D, III-E.
- **Status:** **KEEP**
- **Notes:** Title says 'elite' but the abstract describes 11 well-trained junior skiers; the manuscript text now only cites the observed distribution. Year 2006 (print; online 2004).

### Reference [21] (former [19])
- **Authors:** Thomas Stöggl; Billy Sperlich
- **Exact title:** Polarized training has greater impact on key endurance variables than threshold, high intensity, or high volume training
- **Publication year:** 2014 (Crossref print None; online [[2014]]; OpenAlex 2014)
- **Journal/conference:** Frontiers in Physiology
- **Publication type:** Journal Article (randomized trial, n=48, 9 weeks)
- **Publisher:** Frontiers Media SA
- **Volume:** 5  **Issue:** n/a  **Pages/article number:** [VERIFY MANUALLY]
- **DOI:** 10.3389/fphys.2014.00033  (doi.org redirects to: http://journal.frontiersin.org/article/10.3389/fphys.2014.00033/abstract)
- **Google Scholar:** NOT VERIFIED due to access limitation (Scholar returned a CAPTCHA/error page; this does NOT mean the item is absent from Scholar)
- **Publisher or DOI:** VERIFIED (Crossref record + doi.org redirect to publisher domain; article page not read)
- **Year:** VERIFIED
- **Academic publication:** YES
- **Peer reviewed:** YES
- **Relevant to this research:** PARTIALLY
- **Claim supported:** Polarized training gave the largest VO2peak gain among four training concepts in well-trained athletes. Used in II-D.
- **Status:** **KEEP**
- **Notes:** Not recreational runners; single short trial.

### Reference [22] (former [22])
- **Authors:** I??IGO MUJIKA; SABINO PADILLA
- **Exact title:** Scientific Bases for Precompetition Tapering Strategies
- **Publication year:** 2003 (Crossref print [[2003, 7]]; online None; OpenAlex 2003)
- **Journal/conference:** Medicine & Science in Sports & Exercise
- **Publication type:** Review (journal)
- **Publisher:** Ovid Technologies (Wolters Kluwer Health)
- **Volume:** 35  **Issue:** 7  **Pages/article number:** 1182-1187
- **DOI:** 10.1249/01.MSS.0000074448.73931.11  (doi.org redirects to: https://www.ovid.com/00005768-200307000-00017)
- **Google Scholar:** NOT VERIFIED due to access limitation (Scholar returned a CAPTCHA/error page; this does NOT mean the item is absent from Scholar)
- **Publisher or DOI:** VERIFIED (Crossref record + doi.org redirect to publisher domain; article page not read)
- **Year:** VERIFIED
- **Academic publication:** YES
- **Peer reviewed:** YES
- **Relevant to this research:** YES
- **Claim supported:** Taper: keep intensity, reduce volume (up to 60-90%), progressive nonlinear taper. Used in I, II-D, III-E.
- **Status:** **KEEP**

### Reference [23] (former [26])
- **Authors:** LAURENT BOSQUET; JONATHAN MONTPETIT; DENIS ARVISAIS; IÑIGO MUJIKA
- **Exact title:** Effects of Tapering on Performance
- **Publication year:** 2007 (Crossref print [[2007, 8]]; online None; OpenAlex 2007)
- **Journal/conference:** Medicine & Science in Sports & Exercise
- **Publication type:** Review (meta-analysis, journal)
- **Publisher:** Ovid Technologies (Wolters Kluwer Health)
- **Volume:** 39  **Issue:** 8  **Pages/article number:** 1358-1365
- **DOI:** 10.1249/mss.0b013e31806010e0  (doi.org redirects to: https://www.ovid.com/00005768-200708000-00019)
- **Google Scholar:** NOT VERIFIED due to access limitation (Scholar returned a CAPTCHA/error page; this does NOT mean the item is absent from Scholar)
- **Publisher or DOI:** VERIFIED (Crossref record + doi.org redirect to publisher domain; article page not read)
- **Year:** VERIFIED
- **Academic publication:** YES
- **Peer reviewed:** YES
- **Relevant to this research:** YES
- **Claim supported:** 27 studies; 2-week taper with exponentially decreased volume gave the best performance effect. Used in II-D, III-E.
- **Status:** **KEEP**

### Reference [24] (former [23])
- **Authors:** Zhongliang He; Jiacheng Wang; Binggang Zhang; Yang Li
- **Exact title:** Knowledge-grounded large language model for personalized sports training plan generation
- **Publication year:** 2026 (Crossref print None; online [[2026, 1, 31]]; OpenAlex 2026)
- **Journal/conference:** Scientific Reports
- **Publication type:** Journal Article
- **Publisher:** Springer Science and Business Media LLC
- **Volume:** 16  **Issue:** 1  **Pages/article number:** 6793
- **DOI:** 10.1038/s41598-026-37075-z  (doi.org redirects to: https://www.nature.com/articles/s41598-026-37075-z)
- **Google Scholar:** NOT VERIFIED due to access limitation (Scholar returned a CAPTCHA/error page; this does NOT mean the item is absent from Scholar)
- **Publisher or DOI:** VERIFIED (Crossref record + doi.org redirect to publisher domain; article page not read)
- **Year:** VERIFIED
- **Academic publication:** YES
- **Peer reviewed:** YES
- **Relevant to this research:** YES
- **Claim supported:** LLM grounded in a sports-science knowledge graph for training-plan generation; outperforms baselines on coherence/goal relevance. Used in I, II-C, II-F.
- **Status:** **VERIFY MANUALLY**
- **Notes:** 'Closed-loop rule-based safety validator' wording REMOVED from the manuscript (abstract does not support it). Manuscript now says only: LLM-SPTRec is grounded in a sports-science knowledge graph and outperforms collaborative-filtering, sequential and general-purpose LLM baselines on plan coherence, goal relevance and predicted user satisfaction. Read the full text to check whether outputs are validated after generation.

### Reference [25] (former [24])
- **Authors:** Justin Khasentino; Anastasiya Belyaeva; Xin Liu; Zhun Yang; Nicholas A. Furlotte; Chace Lee; Erik Schenck; Yojan Patel; Jian Cui; Logan Douglas Schneider; Robby Bryant; Ryan G. Gomes; et al. (34 authors in Crossref)
- **Exact title:** A personal health large language model for sleep and fitness coaching
- **Publication year:** 2025 (Crossref print [[2025, 10]]; online [[2025, 8, 14]]; OpenAlex 2025)
- **Journal/conference:** Nature Medicine
- **Publication type:** Journal Article
- **Publisher:** Springer Science and Business Media LLC
- **Volume:** 31  **Issue:** 10  **Pages/article number:** 3394-3403
- **DOI:** 10.1038/s41591-025-03888-0  (doi.org redirects to: https://www.nature.com/articles/s41591-025-03888-0)
- **Google Scholar:** NOT VERIFIED due to access limitation (Scholar returned a CAPTCHA/error page; this does NOT mean the item is absent from Scholar)
- **Publisher or DOI:** VERIFIED (Crossref record + doi.org redirect to publisher domain; article page not read)
- **Year:** VERIFIED
- **Academic publication:** YES
- **Peer reviewed:** YES
- **Relevant to this research:** PARTIALLY
- **Claim supported:** Fine-tuned personal-health LLM for sleep and fitness coaching; fitness case studies similar to experts. Used in I, II-C.
- **Status:** **KEEP**
- **Notes:** Wearable-data setting; not a plan generator.

### Reference [26] (NEW (added in this revision))
- **Authors:** Ciara Feely; Brian Caulfield; Aonghus Lawlor; Barry Smyth
- **Exact title:** Providing Explainable Race-Time Predictions and Training Plan Recommendations to Marathon Runners
- **Publication year:** 2020 (Crossref print [[2020, 9, 22]]; online [[2020, 9, 22]]; OpenAlex 2020)
- **Journal/conference:** Fourteenth ACM Conference on Recommender Systems
- **Publication type:** Conference Paper
- **Publisher:** ACM
- **Volume:** n/a  **Issue:** n/a  **Pages/article number:** 539-544
- **DOI:** 10.1145/3383313.3412220  (doi.org redirects to: https://dl.acm.org/doi/10.1145/3383313.3412220)
- **Google Scholar:** NOT VERIFIED due to access limitation (Scholar not queried before the block; this does NOT mean the item is absent)
- **Publisher or DOI:** VERIFIED (Crossref record + doi.org redirect to publisher domain; article page not read)
- **Year:** VERIFIED
- **Academic publication:** YES
- **Peer reviewed:** YES
- **Relevant to this research:** YES
- **Claim supported:** Case-based recommender for marathon runners reusing training data of similar runners, with explanations; offline evaluation on a real-world dataset. Used in I, II-C, II-F.
- **Status:** **KEEP**
- **Notes:** Conference, not a journal. Not LLM-based.

### Reference [27] (former [25])
- **Authors:** Jack Daniels
- **Exact title:** Daniels’ Running Formula
- **Publication year:** 2022 (Crossref print [[2022]]; online None; OpenAlex 2022)
- **Journal/conference:** (book)
- **Publication type:** Book (professional/academic)
- **Publisher:** Human Kinetics
- **Volume:** n/a  **Issue:** n/a  **Pages/article number:** [VERIFY MANUALLY]
- **DOI:** 10.5040/9781718219113  (doi.org redirects to: https://www.humankineticslibrary.com/encyclopedia?docid=b-9781718219113)
- **Google Scholar:** NOT VERIFIED due to access limitation (Scholar returned a CAPTCHA/error page; this does NOT mean the item is absent from Scholar)
- **Publisher or DOI:** VERIFIED (Crossref record + doi.org redirect to publisher domain; article page not read)
- **Year:** VERIFIED
- **Academic publication:** YES (book)
- **Peer reviewed:** N/A (book, not journal peer review)
- **Relevant to this research:** YES
- **Claim supported:** Daniels' Running Formula: VDOT-based training paces. Used in II-D, III-D.
- **Status:** **VERIFY MANUALLY**
- **Notes:** Crossref: 4th ed., 2022 (print year may be 2021). The implemented zone fractions (0.65/0.74/0.80/0.88/0.98/1.05) must be compared with the book.

### Reference [28] (former [27])
- **Authors:** Tim J Gabbett
- **Exact title:** The training—injury prevention paradox: should athletes be training smarter <i>and</i> harder?
- **Publication year:** 2016 (Crossref print [[2016, 3]]; online [[2016, 1, 12]]; OpenAlex 2016)
- **Journal/conference:** British Journal of Sports Medicine
- **Publication type:** Review (journal)
- **Publisher:** BMJ
- **Volume:** 50  **Issue:** 5  **Pages/article number:** 273-280
- **DOI:** 10.1136/bjsports-2015-095788  (doi.org redirects to: https://bjsm.bmj.com/lookup/doi/10.1136/bjsports-2015-095788)
- **Google Scholar:** NOT VERIFIED due to access limitation (Scholar returned a CAPTCHA/error page; this does NOT mean the item is absent from Scholar)
- **Publisher or DOI:** VERIFIED (Crossref record + doi.org redirect to publisher domain; article page not read)
- **Year:** VERIFIED
- **Academic publication:** YES
- **Peer reviewed:** YES
- **Relevant to this research:** PARTIALLY
- **Claim supported:** Training load, injury risk and protective effects of training (load management framing). Used in II-D, III-E (cutback row), V-E.
- **Status:** **KEEP**
- **Notes:** The two weak uses (Table II cutback row; V-E negative claim) were REMOVED. Now used only in II-D for load-management framing.

### Reference [29] (NEW (added in this revision))
- **Authors:** Vladimir B. Issurin
- **Exact title:** New Horizons for the Methodology and Physiology of Training Periodization
- **Publication year:** 2010 (Crossref print [[2010, 3]]; online None; OpenAlex 2010)
- **Journal/conference:** Sports Medicine
- **Publication type:** Review (journal)
- **Publisher:** Springer Science and Business Media LLC
- **Volume:** 40  **Issue:** 3  **Pages/article number:** 189-206
- **DOI:** 10.2165/11319770-000000000-00000  (doi.org redirects to: http://link.springer.com/10.2165/11319770-000000000-00000)
- **Google Scholar:** NOT VERIFIED due to access limitation (Scholar not queried before the block; this does NOT mean the item is absent)
- **Publisher or DOI:** VERIFIED (Crossref record + doi.org redirect to publisher domain; article page not read)
- **Year:** VERIFIED
- **Academic publication:** YES
- **Peer reviewed:** YES
- **Relevant to this research:** PARTIALLY
- **Claim supported:** Periodization divides a program into smaller periods and units; limitations of the traditional model. Used in II-D and Table II (periodization concept only).
- **Status:** **KEEP**
- **Notes:** Does not support a specific cutback rule. PMID 20199119.

### Reference [30] (former [28])
- **Authors:** Yupeng Chang; Xu Wang; Jindong Wang; Yuan Wu; Linyi Yang; Kaijie Zhu; Hao Chen; Xiaoyuan Yi; Cunxiang Wang; Yidong Wang; Wei Ye; Yue Zhang; et al. (16 authors in Crossref)
- **Exact title:** A Survey on Evaluation of Large Language Models
- **Publication year:** 2024 (Crossref print [[2024, 6, 30]]; online [[2024, 3, 29]]; OpenAlex 2024)
- **Journal/conference:** ACM Transactions on Intelligent Systems and Technology
- **Publication type:** Journal Article (survey)
- **Publisher:** Association for Computing Machinery (ACM)
- **Volume:** 15  **Issue:** 3  **Pages/article number:** 1-45
- **DOI:** 10.1145/3641289  (doi.org redirects to: https://dl.acm.org/doi/10.1145/3641289)
- **Google Scholar:** NOT VERIFIED due to access limitation (Scholar returned a CAPTCHA/error page; this does NOT mean the item is absent from Scholar)
- **Publisher or DOI:** VERIFIED (Crossref record + doi.org redirect to publisher domain; article page not read)
- **Year:** VERIFIED
- **Academic publication:** YES
- **Peer reviewed:** YES
- **Relevant to this research:** YES
- **Claim supported:** LLM evaluation organized by what, where and how to evaluate. Used in II-E.
- **Status:** **KEEP**

### Reference [31] (former [29])
- **Authors:** Lianmin Zheng; Wei-Lin Chiang; Ying Sheng; Siyuan Zhuang; Zhanghao Wu; Yonghao Zhuang; Zi Lin; Zhuohan Li; Dacheng Li; Eric Xing; Hao Zhang; Joseph Gonzalez; et al. (13 authors in Crossref)
- **Exact title:** Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena
- **Publication year:** 2023 (Crossref print [[2023]]; online None; OpenAlex 2023)
- **Journal/conference:** Advances in Neural Information Processing Systems 36
- **Publication type:** Conference Paper (NeurIPS 2023, Datasets and Benchmarks track)
- **Publisher:** Neural Information Processing Systems Foundation, Inc. (NeurIPS)
- **Volume:** n/a  **Issue:** n/a  **Pages/article number:** 46595-46623
- **DOI:** 10.52202/075280-2020  (doi.org redirects to: http://www.proceedings.com/075280-2020.html)
- **Google Scholar:** NOT VERIFIED due to access limitation (Scholar returned a CAPTCHA/error page; this does NOT mean the item is absent from Scholar)
- **Publisher or DOI:** VERIFIED (Crossref record + doi.org redirect to publisher domain; article page not read)
- **Year:** VERIFIED
- **Academic publication:** YES
- **Peer reviewed:** YES (conference; track to confirm)
- **Relevant to this research:** PARTIALLY
- **Claim supported:** LLM-as-a-judge approximates human preferences; position, verbosity, self-enhancement biases and limited reasoning ability. Used in II-E.
- **Status:** **KEEP**
- **Notes:** The claim was checked on the abstract of the arXiv version (arXiv:2306.05685), which states the biases and the NeurIPS 2023 Datasets and Benchmarks acceptance; the NeurIPS record itself was not opened. DOI resolves to a third-party page (proceedings.com); the DOI is registered in Crossref by the proceedings publisher. Consider citing the NeurIPS proceedings URL as well.

### Reference [32] (NEW (added in this revision))
- **Authors:** Geoff Norman
- **Exact title:** Likert scales, levels of measurement and the “laws” of statistics
- **Publication year:** 2010 (Crossref print [[2010, 12]]; online [[2010, 2, 10]]; OpenAlex 2010)
- **Journal/conference:** Advances in Health Sciences Education
- **Publication type:** Journal Article
- **Publisher:** Springer Science and Business Media LLC
- **Volume:** 15  **Issue:** 5  **Pages/article number:** 625-632
- **DOI:** 10.1007/s10459-010-9222-y  (doi.org redirects to: http://link.springer.com/10.1007/s10459-010-9222-y)
- **Google Scholar:** NOT VERIFIED due to access limitation (Scholar not queried before the block; this does NOT mean the item is absent)
- **Publisher or DOI:** VERIFIED (Crossref record + doi.org redirect to publisher domain; article page not read)
- **Year:** VERIFIED
- **Academic publication:** YES
- **Peer reviewed:** YES
- **Relevant to this research:** YES
- **Claim supported:** Likert data are ordinal; parametric methods argued to be robust. Used in II-E, III-K.
- **Status:** **KEEP**
- **Notes:** Replaces former [30] (Sullivan & Artino, short commentary of uncertain peer-review status). Reason for replacement: full peer-reviewed article indexed in PubMed (PMID 20146096) whose abstract directly addresses analysis of Likert data.

### Reference [33] (former [31])
- **Authors:** Mohsen Tavakol; Reg Dennick
- **Exact title:** Making sense of Cronbach's alpha
- **Publication year:** 2011 (Crossref print None; online [[2011, 6, 27]]; OpenAlex 2011)
- **Journal/conference:** International Journal of Medical Education
- **Publication type:** Journal Article (short editorial-type article, Int. J. Med. Educ.)
- **Publisher:** International Journal of Medical Education
- **Volume:** 2  **Issue:** n/a  **Pages/article number:** 53-55
- **DOI:** 10.5116/ijme.4dfb.8dfd  (doi.org redirects to: http://www.ijme.net/archive/2/cronbachs-alpha/)
- **Google Scholar:** NOT VERIFIED due to access limitation (Scholar returned a CAPTCHA/error page; this does NOT mean the item is absent from Scholar)
- **Publisher or DOI:** VERIFIED (Crossref record + doi.org redirect to publisher domain; article page not read)
- **Year:** VERIFIED
- **Academic publication:** YES
- **Peer reviewed:** UNCERTAIN
- **Relevant to this research:** YES
- **Claim supported:** Cronbach's alpha as internal-consistency measure. Used in III-K.
- **Status:** **VERIFY MANUALLY**
- **Notes:** Short editorial-type article; confirm peer-review status on the journal site (candidate alternative: Taber 2018, Res. Sci. Educ., doi 10.1007/s11165-016-9602-2, Crossref-verified, not adopted).

