# Step 9 human blind check: kit (the check itself is NOT done)

What the specification requires (section 11 layer 3, 11.2, FZ-v1 row 19): one rule-reader receives only the rendered rule and rendered plan (no claim block) under opaque IDs, ordered by opaque ID, with a calculator, no feedback, coverage 100 % of members, and fills the worksheet of 11.2. The delay is **at least 7 days** from the last time the researcher saw rendered registry content or expected states (OD-3: one human, delayed self-check). A model reader may only be a screening layer.

Ready for you:
- Files to read: `research_design/step8_output/step8_build_7a6bbe465c66/main/checker_bundle/` (624 files; names are opaque IDs; each file is rule + plan block). The mapping to templates is in `main/checker_mapping_HELD_SEPARATELY.json`: **do not open it** until all rows are done.
- Blank worksheet: `blind_check_worksheet_MAIN_blank.csv` (624 rows).
- Start the 7-day clock only after you stop viewing registry content: do not open `registry.json`, `prompt_table.json`, `prompts/` or `gate_report.json` meanwhile.
- After the check: Implementation B (not written) and the reference worksheets by Implementation A are compared (ADJ-1/ADJ-2). Then the pilot (18 calls) may start.
