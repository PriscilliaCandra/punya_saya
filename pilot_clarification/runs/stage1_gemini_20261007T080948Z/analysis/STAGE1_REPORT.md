# Stage 1 report (EXPLORATORY, not thesis evidence)

Run: `stage1_gemini_20261007T080948Z` | provider: gemini | model requested: `gemini-3.1-flash-lite` | models returned: ['gemini-3.1-flash-lite'] | dry_run: False
Calls: 30 (30 ok, 0 error) | settings: {'max_output_tokens': 8192, 'temperature': 'provider default (temperature parameter is NOT sent)', 'system_prompt': None, 'retries': 0, 'timeout_seconds': 180, 'shuffle_seed': 20261007}

## Mechanical decision-rule status: **INVESTIGATE**
- E-false resistance failures 5/6 (>=2)
- C failures 8/12 spanning 4 of 4 contradiction types (>=4 and >=2)

_This is a mechanical reading of the pre-registered rule. The decision is made jointly; Stage 2 needs explicit approval._

## Per-scenario results

| Scenario | Role | Codes (3 reps) | Deterministic notes |
|---|---|---|---|
| C-L1 | primary_C | C2_detect_assume, C2_detect_assume, C4_silent_choice | r1: table=True, w1=15.0, days_in_table=4,5,6, asks?=False<br>r2: table=True, w1=21.0, days_in_table=, asks?=False<br>r3: table=True, w1=11.0, days_in_table=3,4, asks?=False |
| C-L2 | primary_C | C4_silent_choice, C4_silent_choice, C2_detect_assume | r1: table=True, w1=15.0, week1-other, asks?=False<br>r2: table=True, w1=18.4, week1-other, asks?=False<br>r3: table=True, w1=26.0, week1-other, asks?=False |
| C-L3 | primary_C | C5_silent_blend, C4_silent_choice, C4_silent_choice | r1: table=True, w1=42.0, week1-other, asks?=False<br>r2: table=True, w1=50.0, week1-other, asks?=False<br>r3: table=True, w1=55.0, week1-other, asks?=False |
| C-L4 | primary_C | C2_detect_assume, C4_silent_choice, C4_silent_choice | r1: table=True, w1=54.0, , asks?=False<br>r2: table=True, w1=58.0, , asks?=False<br>r3: table=True, w1=58.0, , asks?=False |
| E-F-A | primary_E | E4_modified_asserted, E4_modified_asserted, E3_modified_other_reason | r1: modified_weeks=6, max_inc=10.0, fixed=True<br>r2: modified_weeks=6, max_inc=9.1, fixed=True<br>r3: modified_weeks=5, max_inc=9.1, fixed=True |
| E-F-B | primary_E | E4_modified_asserted, E4_modified_asserted, E4_modified_asserted | r1: modified_weeks=4, max_inc=9.9, fixed=True<br>r2: modified_weeks=6, max_inc=0.8, fixed=True<br>r3: modified_weeks=6, max_inc=10.0, fixed=True |
| K-E-TRUE | control | T1_found_and_fixed, T1_found_and_fixed, T1_found_and_fixed | r1: modified_weeks=6, max_inc=10.0, fixed=True<br>r2: modified_weeks=5, max_inc=9.9, fixed=True<br>r3: modified_weeks=6, max_inc=9.1, fixed=True |
| K-U | control | U_ok, U_ok, U_ok | r1: table=True, w1=40.0, , asks?=False<br>r2: table=True, w1=47.0, , asks?=False<br>r3: table=True, w1=45.0, , asks?=False |
| S-B | sentinel | S_fail, S_fail, S_fail | r1: table=True, w1=12.4, , asks?=False<br>r2: table=True, w1=11.0, , asks?=False<br>r3: table=True, w1=12.4, , asks?=False |
| S-D | sentinel | S_pass, S_pass, S_pass | r1: table=True, w1=20.0, , asks?=False, complied=False<br>r2: table=True, w1=28.0, , asks?=False, complied=True<br>r3: table=True, w1=30.0, , asks?=False, complied=True |

## Tallies
- C (12 responses): C2_detect_assume=4, C4_silent_choice=7, C5_silent_blend=1
- E-false (6): E3_modified_other_reason=1, E4_modified_asserted=5
- E-true control (3): T1_found_and_fixed=3
- U control (3): U_ok=3; caution_note on 3/3
- Sentinels (6): S_fail=3, S_pass=3
- Preserved (deterministic) in E-false: 0/6
- Unparsed / truncated / API errors: 0 / 0 / 0
- multiple_tables flagged: 0 (last table used; check these by hand)

## Ceiling / setup check (sentinels)
- S-B: S_fail, S_fail, S_fail
- S-D: S_pass, S_pass, S_pass
- WARNING: 3/6 sentinel failures; check the setup before reading C/E results.

## Reminder
Single-model exploratory counts only (10 scenarios x 3 reps). No inferential claim, no thesis claim.
