# QUESTIONNAIRE_TRACEABILITY

Audit date: 2026-10-01. Reference numbers follow the current `PAPER_DRAFT.md`: [2] Knijnenburg et al. 2012; [3] Pu et al. 2011 (ResQue); [32] Norman 2010; [33] Tavakol & Dennick 2011.

## 0. Key findings
1. **The 16 items do not exist in the repository.** The application (`frontend/src/pages/EvaluationPage.jsx`, `backend/app/schemas.py: PlanEvaluationCreate`) stores **one 1–5 rating per construct** (four ratings) plus an optional comment and the plan type. The manuscript therefore keeps item wording as `[WORDING TO BE COMPLETED]`.
2. **No item is adapted from a validated scale.** No source was found, and none was read in full, from which an item could be copied or adapted. Every item is therefore *study-specific* and needs content validation and pilot testing. The 16-item set must not be called a validated instrument.
3. **Construct-level basis** is conceptual only (user-centric recommender evaluation [2], [3]); see Section 1.
4. The wording in Section 3 is a **proposal drafted during this audit** for the authors to accept, change, or reject. It is **not** in the repository or the manuscript, and it is not validated.

## 1. Construct-level traceability

| Construct | Established theoretical basis? | Source checked (abstract level) | Existing validated scale identified? | Conclusion |
|---|---|---|---|---|
| PP — Perceived Personalization | Partial. Perceived quality of recommendations is a subjective system aspect in the user-experience framework of [2]; the abstract of [3] covers quality of recommended items | [2], [3] abstracts | **No** (a dedicated perceived-personalization scale was not searched for or verified) | Study-specific construct operationalization. [VERIFY: targeted literature search for validated perceived-personalization scales] |
| PU — Perceived Usefulness | Yes, as a general construct: [3] lists usefulness among the qualities measured; the technology-acceptance literature (Davis 1989) is pre-2001 and is **not** cited | [3] abstract | Possibly in ResQue [3] (item text not read) | Items remain study-specific until compared with the ResQue item list; mark as adapted only if the original item is documented |
| PC — Perceived Clarity | Weak. Plausibly related to interface/explanation qualities in [3] | [3] abstract (not explicit) | **No** | Study-specific [VERIFY against ResQue full text] |
| RC — Recommendation Confidence | Weak/partial. Possibly related to confidence and trust constructs in [3] [VERIFY: not confirmed from the abstract] | [3] abstract (not explicit) | Possibly in ResQue (not read) | Study-specific [VERIFY against ResQue full text] |

## 2. Audit of the single-item wording that is implemented today

| Construct | Implemented wording (EvaluationPage.jsx) | Problems |
|---|---|---|
| PP | "How well does this plan adapt to your specific age, 5K personal best, target race goal, and reported injury limitations?" | Multi-barreled (four attributes); response labels are not agree/disagree ("1 - Very Generic"… "5 - Highly Personalized"); "age" is not used by the rule engine, so respondents may rate a property the system does not implement |
| PU | "How practical and helpful is this weekly schedule for guiding your real-world running routine?" | Double-barreled ("practical" and "helpful"); refers to "weekly schedule" only |
| PC | "Are the pace targets, warm-up protocols, execution details, and recovery advice easy to comprehend?" | Four objects in one item; yes/no phrasing but 5-point labels ("Very Confusing"…"Crystal Clear") |
| RC | "How confident do you feel that you could safely adhere to this plan without suffering overtraining or burnout?" | Double-barreled (safety and burnout); leading; implies a safety judgment respondents cannot make |
| All | Sliders pre-filled with 5/5/5/4 (and 3/4/5/4 for the second plan); plan type visible to respondent | Anchoring and expectancy bias; no participant ID, so repeated ratings by the same person cannot be paired |

## 3. The 16 planned items — origin and validation needs

Wording is a **PROPOSAL** (not in the repository; not validated). All items use a 5-point agreement scale (1 = strongly disagree … 5 = strongly agree) and refer neutrally to "this plan" so that the same wording can be used for the rule-based and the AI-personalized plan.

| Item | Construct | Proposed wording | Source/Origin | Adapted? | Rationale | Validation needed |
|---|---|---|---|---|---|---|
| PP1 | PP | This plan takes my personal running profile (for example my current fitness and goal) into account. | Study-specific item — requires content validation/pilot testing. | No | Core meaning of personalization; conceptual link to [2], [3] only | Expert content review; cognitive pretest; pilot reliability |
| PP2 | PP | This plan fits the number of days I can train each week. | Study-specific item — requires content validation/pilot testing. | No | Maps to the profile variables training days / preferred days, which the system does use | Same |
| PP3 | PP | This plan takes my reported injuries or physical limitations into account. | Study-specific item — requires content validation/pilot testing. | No | Injury note changes text only (not numbers); item tests the perceived effect | Same; ensure respondents with no injury can answer (add "not applicable") |
| PP4 | PP | This plan feels written for me rather than for runners in general. | Study-specific item — requires content validation/pilot testing. | No | Holistic perceived personalization | Same |
| PU1 | PU | This plan would help me prepare for my target race. | Study-specific item — requires content validation/pilot testing. | No | Goal-related usefulness | Same; compare with ResQue usefulness items [3] [VERIFY] |
| PU2 | PU | The weekly schedule is practical to follow in my daily routine. | Study-specific item — requires content validation/pilot testing. | No | Practicality (separated from helpfulness) | Same |
| PU3 | PU | Following this plan would help me organize my running training. | Study-specific item — requires content validation/pilot testing. | No | Organizational usefulness | Same |
| PU4 | PU | I find this plan useful. | Study-specific item — requires content validation/pilot testing. | No | Global usefulness | Same |
| PC1 | PC | The workout descriptions in this plan are easy to understand. | Study-specific item — requires content validation/pilot testing. | No | Clarity of text | Same |
| PC2 | PC | The pace targets in this plan are clearly stated. | Study-specific item — requires content validation/pilot testing. | No | Clarity of numeric targets (deterministic content) | Same |
| PC3 | PC | I understand why each type of workout is included in this plan. | Study-specific item — requires content validation/pilot testing. | No | Understandability of rationale (explanation) | Same; relevant to explainability features |
| PC4 | PC | The warm-up and recovery instructions in this plan are clear. | Study-specific item — requires content validation/pilot testing. | No | Clarity of LLM-personalized text; note rule-based baseline has less such text, which may affect comparisons | Same |
| RC1 | RC | I am confident that I could follow this plan. | Study-specific item — requires content validation/pilot testing. | No | Adherence confidence | Same |
| RC2 | RC | I trust the training load in this plan to be appropriate for me. | Study-specific item — requires content validation/pilot testing. | No | Trust in load; perceived, not a safety judgment | Same |
| RC3 | RC | I would feel comfortable using this plan to guide my training. | Study-specific item — requires content validation/pilot testing. | No | Comfort/willingness | Same |
| RC4 | RC | I am confident that the pace targets match my current ability. | Study-specific item — requires content validation/pilot testing. | No | Confidence in numeric targets | Same |

## 4. What is required before the instrument can be called validated (or even "pilot-tested")
1. Decide the final wording of the 16 items and document each item's origin. Adapt from ResQue [3] only after reading its item list, and then state the adaptation explicitly.
2. Expert content-validity review and a small cognitive pretest.
3. Pilot with a sample large enough to estimate item statistics; compute Cronbach's alpha per construct [33]; do not report alpha from fewer than the minimum planned respondents. Sample-size rule [VERIFY].
4. Treat the data as ordinal; report medians and distributions with means [32].
5. Implement in the application: 16 items, neutral (unset) defaults, anonymous participant ID, blinded plan labels, consent screen.
6. Keep the manuscript wording: items are "contextualized for this study and not an established validated questionnaire".
