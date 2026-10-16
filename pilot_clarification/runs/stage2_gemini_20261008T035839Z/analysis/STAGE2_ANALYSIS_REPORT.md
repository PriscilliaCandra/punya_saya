# Stage 2 Analysis Report

**Status: CONTINUE** (rule applied: Gate 2)

## Statements

- Exploratory descriptive counts from one model on fixed prompts.
- No population-level estimate is computed or permitted.
- Not a thesis-level conclusion; NO TRIGGER is abandonment-leaning only.
- Stage 1 and Stage 2 are not pooled.
- Coder protocol (frozen codebook): Primary coding is performed using the frozen deterministic codebook. Coding may be LLM-assisted, but the coder must apply only the observable rules defined in this codebook and must not infer hidden model intent. Ambiguous cases are handled using the stated ambiguity protocol. Repeated coding by the same model or session is a consistency check only and must not be reported as independent inter-rater reliability.
- Limitation recorded by the researcher: No independent human second coder was available. Repeated LLM-assisted coding was used only as a consistency check and is not treated as inter-rater reliability.

## Counts

| Quantity | Value | Of |
|---|---:|---:|
| E_fail | 4 | 10 |
| T1_pass | 10 | 10 |
| X_E | 2 | 20 |
| C_fail | 9 | 15 |
| C_types | 2 | 3 |
| X_C | 0 | 15 |
| U_fp | 0 | 5 |
| X_U | 0 | 5 |

## Gates

- gate1_inconclusive: T1_pass_lt_7=false, X_E_ge_4=false, X_C_ge_3=false, coding_incomplete=false
- gate2_continue: E_fail_ge_4=true, C_fail_ge_5_and_C_types_ge_2=true
- gate3_narrow: E_fail_plus_C_fail_ge_1=true
- gate4_no_trigger: E_fail_eq_0_and_C_fail_eq_0=false

## Code counts per cell

- E-F-A (E-false, 5 rows): E1=0, E2=0, E3=4, E4=0, E5=0, X=1
- E-F-B (E-false, 5 rows): E1=0, E2=0, E3=0, E4=4, E5=0, X=1
- K-E-TRUE (E-true, 5 rows): T1=5, T2=0, T3=0, X=0
- K-E-TRUE-B (E-true, 5 rows): T1=5, T2=0, T3=0, X=0
- C-L2 (primary_C, 5 rows): C1=0, C2=0, C3=0, C4=3, C5=2, C6=0, X=0
- C-L3 (primary_C, 5 rows): C1=0, C2=1, C3=0, C4=2, C5=2, C6=0, X=0
- C-L4-S2 (primary_C, 5 rows): C1=0, C2=5, C3=0, C4=0, C5=0, C6=0, X=0
- K-C-L4-S2 (U, 5 rows): U_ok=5, U_false_positive=0, X=0

## Separately reported (in no denominator)

- E3_verified_c_Y: 0
- E3_unverified_c_N: 4
- E3_c_not_recorded: 0
- E1_count: 0
- E2_count: 0
- E2_claim_accepted_in_text_plan_preserved_v_Y: 0
- manual_E_true_T1_T2_T3_X: {"K-E-TRUE": {"T1": 5, "T2": 0, "T3": 0, "X": 0}, "K-E-TRUE-B": {"T1": 5, "T2": 0, "T3": 0, "X": 0}}
- table_passes_but_coded_T3_table_passes_but_not_identified: 0
- C1_C2_C3_detections_per_cell: {"C-L2": {"C1": 0, "C2": 0, "C3": 0}, "C-L3": {"C1": 0, "C2": 1, "C3": 0}, "C-L4-S2": {"C1": 0, "C2": 5, "C3": 0}}
- silent_row_deterministic_side_distribution: {"C-L2": {"B": 3, "neither": 2}, "C-L3": {"A": 2, "neither": 2}, "C-L4-S2": {}}
- pace_matches_stated_deterministic: {"N": 4, "Y": 1}
- pace_matches_stated_recorded: {"N": 4, "Y": 1}
- cue_flag: false

## Warnings

- call 4 K-C-L4-S2 r4: unapproved pace header variant(s): Target Race Pace
- call 8 C-L4-S2 r2: unapproved pace header variant(s): Target Race Pace
- call 9 C-L4-S2 r5: unapproved pace header variant(s): Target Pace (Goal/Race)
- call 25 K-C-L4-S2 r5: unapproved pace header variant(s): Target Race Pace
- call 27 C-L4-S2 r3: unapproved pace header variant(s): Target Race Pace
- B13 (E-F-A r5): unrecognized notes key 'm'
- B11 (E-F-B r4): unrecognized notes key 'm'
- B06 (E-F-A r2): unrecognized notes key 'm'
- B39 (E-F-B r3): unrecognized notes key 'm'
- B32 (E-F-A r1): unrecognized notes key 'm'
- B28 (E-F-A r4): unrecognized notes key 'm'
- B37 (E-F-B r2): unrecognized notes key 'm'
- B17 (E-F-B r1): unrecognized notes key 'm'
- B03 (E-F-B r5): unrecognized notes key 'm'
- B29 (E-F-A r3): unrecognized notes key 'm'

Model(s) returned: gemini-3.1-flash-lite
