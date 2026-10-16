"""FORMAT-ONLY pre-check of the two human worksheets (H1 blind check, H4 codebook rehearsal). It tells the researcher which cells are empty or malformed BEFORE the real
evaluation is run, so that no row is left incomplete by accident. It is advisory: it cannot predict whether a verdict agrees with anything.
It reads ONLY the sheet you filled and the matching blank kit sheet (for the ids and, for H4, the printed synthetic comment text). It never opens the checker bundle,
the checker mapping, the registry, the prompts, the expected codes of codebook_battery_v1.py or any run output, and it prints only row ids and column names (never
cell contents). It writes nothing. Exit 0 = no format problem found, 1 = problems or unfilled rows, 2 = unusable input.
Usage: python -B -I precheck_human_sheets.py --kind blindcheck --sheet <your filled csv>
       python -B -I precheck_human_sheets.py --kind rehearsal  --sheet <your filled csv>
Rules are those printed in HUMAN_TASK_GUIDE.md (rows with every judgment cell empty are reported as NOT FILLED)."""
import argparse
import csv
import os
import re
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.normpath(os.path.join(HERE, "..", "step9_blind_check_kit", "blind_check_worksheet_MAIN_blank.csv"))
KIT_H4 = os.path.normpath(os.path.join(HERE, "..", "codebook_rehearsal_kit", "rehearsal_sheet_BLANK.csv"))

VERDICTS = {"satisfied", "violated", "unclear"}
MIL_STATUS = {"over cap", "not over cap"}
PAC_STATUS = {"|e|>tau", "not"}
H4_CODES = {"s2_evidence": {"NC", "NV", "IV", "EV"}, "s2_prov": {"Y", "N"}, "s2_values": {"CV", "SW", "NONE"}, "s2_arith": {"AC", "AI", "AM", "AN"},
            "s2_rel": {"RT", "RF", "RM"}, "s3_stance": {"NC", "AG", "DG", "CQ", "MPG", "NS"}}
H4_OPTIONAL = {"s2_prov", "s2_rel"}                       # may stay empty when not applicable (guide)
WEEKS = range(1, 6)


def read(path):
    with open(path, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8-sig")
    rdr = csv.DictReader(text.splitlines(True))
    return rdr.fieldnames, list(rdr)


def val(row, col):
    return (row.get(col) or "").strip()


def decimals(s):
    m = re.fullmatch(r"[+-]?\d+(?:\.(\d+))?", s.replace(" ", ""))
    return None if not m else len(m.group(1) or "")


def check_blindcheck(header, rows, blank_header, blank_rows):
    probs, unfilled = [], []
    if header != blank_header:
        probs.append(("(header)", "columns differ from the blank worksheet"))
        return probs, unfilled
    ids_blank = [r["opaque_id"] for r in blank_rows]
    ids = [r["opaque_id"] for r in rows]
    if len(ids) != len(ids_blank) or set(ids) != set(ids_blank):
        probs.append(("(rows)", f"expected the {len(ids_blank)} ids of the blank worksheet; found {len(ids)} rows, {len(set(ids) ^ set(ids_blank))} ids differ"))
    if len(set(ids)) != len(ids):
        probs.append(("(rows)", "duplicate opaque ids"))
    judged = [c for c in header if c not in ("opaque_id", "notes") and not c.startswith("date_")]
    for r in rows:
        oid = r["opaque_id"]
        if not any(val(r, c) for c in judged):
            unfilled.append(oid)
            continue
        pac = any(val(r, c) for c in ("T_time_displayed", "T_time_seconds", "tau_F"))
        need = ["verdict_satisfied_violated_unclear", "P_or_D_dist"] + (["T_time_displayed", "T_time_seconds", "tau_F"] if pac else [])
        for w in WEEKS:
            need += [f"w{w}_transcribed", f"w{w}_value", f"w{w}_status"]
            if pac or w >= 2:
                need += [f"w{w}_increase_km_or_implied_finish_s_2dp", f"w{w}_limit_km_2dp_or_rounded_finish_s", f"w{w}_percent_2dp_or_diff_s"]
        for c in need:
            if not val(r, c):
                probs.append((oid, f"empty required cell: {c}"))
        if val(r, "verdict_satisfied_violated_unclear") and val(r, "verdict_satisfied_violated_unclear").lower() not in VERDICTS:
            probs.append((oid, "verdict must be satisfied, violated or unclear"))
        inc = lambda w: f"w{w}_increase_km_or_implied_finish_s_2dp"      # noqa: E731
        lim = lambda w: f"w{w}_limit_km_2dp_or_rounded_finish_s"         # noqa: E731
        pct = lambda w: f"w{w}_percent_2dp_or_diff_s"                    # noqa: E731
        if not pac:
            if val(r, "w1_status") and val(r, "w1_status").lower() != "uncompared":
                probs.append((oid, "week 1 status must be 'uncompared' for a mileage row"))
            for c in (inc(1), lim(1), pct(1)):
                if val(r, c):
                    probs.append((oid, f"week 1 computed cell must stay empty: {c}"))
            for w in range(2, 6):
                if val(r, f"w{w}_status") and val(r, f"w{w}_status").lower() not in MIL_STATUS:
                    probs.append((oid, f"week {w} status must be 'over cap' or 'not over cap'"))
                for c, floor in ((inc(w), 1), (lim(w), 2), (pct(w), 2)):
                    d = decimals(val(r, c)) if val(r, c) else floor
                    if d is None:
                        probs.append((oid, f"not a number: {c}"))
                    elif d < floor:
                        probs.append((oid, f"too few decimals (need {floor}): {c}"))
        else:
            for w in WEEKS:
                if val(r, f"w{w}_status") and val(r, f"w{w}_status").lower() not in PAC_STATUS:
                    probs.append((oid, f"week {w} status must be '|e|>tau' or 'not'"))
                d = decimals(val(r, inc(w))) if val(r, inc(w)) else 2
                if d is None:
                    probs.append((oid, f"not a number: {inc(w)}"))
                elif d < 2:
                    probs.append((oid, f"too few decimals (need 2): {inc(w)}"))
    return probs, unfilled


def check_rehearsal(header, rows, blank_header, blank_rows):
    probs, unfilled = [], []
    if header != blank_header:
        probs.append(("(header)", "columns differ from the blank sheet"))
        return probs, unfilled
    blank = {r["opaque_id"]: r for r in blank_rows}
    ids = [r["opaque_id"] for r in rows]
    if set(ids) != set(blank) or len(ids) != len(blank):
        probs.append(("(rows)", f"expected the {len(blank)} ids of the blank sheet; found {len(ids)} rows"))
    if len(set(ids)) != len(ids):
        probs.append(("(rows)", "duplicate opaque ids"))
    for r in rows:
        oid = r["opaque_id"]
        if oid in blank and r.get("comment_text") != blank[oid]["comment_text"]:
            probs.append((oid, "comment_text was changed"))
        cols = list(H4_CODES)
        if not any(val(r, c) for c in cols):
            unfilled.append(oid)
            continue
        for c in cols:
            v = val(r, c)
            if not v:
                if c not in H4_OPTIONAL:
                    probs.append((oid, f"empty required cell: {c}"))
            elif v.upper() not in H4_CODES[c]:
                probs.append((oid, f"not an allowed code: {c}"))
    return probs, unfilled


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", required=True, choices=["blindcheck", "rehearsal"])
    ap.add_argument("--sheet", required=True)
    a = ap.parse_args(argv)
    try:
        header, rows = read(a.sheet)
        bh, br = read(KIT if a.kind == "blindcheck" else KIT_H4)
        probs, unfilled = (check_blindcheck if a.kind == "blindcheck" else check_rehearsal)(header, rows, bh, br)
    except (OSError, KeyError, UnicodeDecodeError, csv.Error) as e:
        print("unusable input:", type(e).__name__)
        return 2
    for oid, msg in probs[:200]:
        print("PROBLEM:", oid, "-", msg)
    print(f"rows: {len(rows)}; not filled: {len(unfilled)}; problems: {len(probs)}")
    if unfilled:
        print("NOT FILLED (first 5 ids):", ", ".join(unfilled[:5]))
    print("FORMAT PRE-CHECK OK (advisory; it does not predict the evaluation)" if not probs and not unfilled else "FORMAT PRE-CHECK: NOT COMPLETE")
    return 0 if not probs and not unfilled else 1


if __name__ == "__main__":
    sys.exit(main())
