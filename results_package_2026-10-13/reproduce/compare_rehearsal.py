"""Compares a FILLED codebook rehearsal sheet with the pre-registered expected codes of codebook_battery_v1.py (hash recorded in decision record 12.22).
Run it only AFTER you finished coding all 40 rows (running it opens the expected codes). Reports raw agreement per variable and each disagreement.
It is NOT a reliability or validity claim (the coder wrote the codebook; codebook section 6). Writes a new JSON file; refuses to overwrite.
Usage: python -B -I compare_rehearsal.py --sheet <filled csv> --out <new json>
Sheet columns: opaque_id, comment_text, s2_evidence, s2_prov, s2_values, s2_arith, s2_rel, s3_stance. Leave s2_prov and s2_rel EMPTY when not applicable
(expected None); s2_values and s2_arith always carry a code (cv/sw/none, AC/AI/AM/AN). Comparison is case-insensitive."""
import argparse
import csv
import hashlib
import io
import json
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "research_design", "step7"))
sys.dont_write_bytecode = True
import codebook_battery_v1 as CB  # noqa: E402

VARS = (("s2_evidence", "evidence"), ("s2_prov", "prov"), ("s2_values", "values"), ("s2_arith", "arith"), ("s2_rel", "rel"), ("s3_stance", "stance"))


def opaque(item_id):
    return hashlib.sha256(item_id.encode()).hexdigest()[:16]


def compare(rows):
    exp = {opaque(it[0]): (it[0], it[3]) for it in CB.BATTERY}
    got = {r["opaque_id"]: r for r in rows}
    out = {"items_expected": len(exp), "items_in_sheet": len(got), "missing": sorted(exp[i][0] for i in exp if i not in got), "variables": {}, "disagreements": []}
    for col, key in VARS:
        agree = n = 0
        for oid, (iid, e) in exp.items():
            if oid not in got:
                continue
            h = (got[oid].get(col) or "").strip().casefold()
            x = "" if e[key] is None else str(e[key]).casefold()
            n += 1
            if h == x:
                agree += 1
            else:
                out["disagreements"].append({"item": iid, "variable": col, "coder": got[oid].get(col, ""), "expected": "" if e[key] is None else e[key]})
        out["variables"][col] = {"n": n, "agree": agree, "raw_agreement_percent": None if not n else f"{100 * agree / n:.1f}"}
    out["statement"] = "rehearsal on synthetic comments; not a reliability or validity claim; no kappa"
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--sheet", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    with open(a.sheet, "rb") as f:
        rows = list(csv.DictReader(io.StringIO(f.read().decode("utf-8"))))
    res = compare(rows)
    with open(a.out, "xb") as f:
        f.write((json.dumps(res, indent=1, sort_keys=True) + "\n").encode("utf-8"))
    print(json.dumps(res["variables"], sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
