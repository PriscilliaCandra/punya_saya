"""Writes the BLANK worksheet for the human blind check (specification 11, 11.2) from the published checker bundle.
Reads only checker_bundle file names and the rendered text (no mapping, no expected state). Usage: python -B -I make_blank_worksheet.py <build>/main/checker_bundle <out.csv>"""
import csv, os, sys
src, out = sys.argv[1], sys.argv[2]
cols = ["opaque_id", "date_first_seen_registry_content_or_expected_states_UTC", "date_of_this_check_UTC", "family_read_from_text", "P_or_D_dist", "T_time_displayed", "T_time_seconds", "tau_F"]
for w in range(1, 6):
    cols += [f"w{w}_transcribed", f"w{w}_value", f"w{w}_increase_km_or_implied_finish_s_2dp", f"w{w}_limit_km_2dp_or_rounded_finish_s", f"w{w}_percent_2dp_or_diff_s", f"w{w}_status"]
cols += ["verdict_satisfied_violated_unclear", "notes"]
ids = sorted(os.listdir(src))
with open(out, "x", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(cols)
    for i in ids: w.writerow([i] + [""] * (len(cols) - 1))
print(len(ids), "rows written to", out)
