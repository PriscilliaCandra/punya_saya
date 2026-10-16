#!/usr/bin/env python3
"""
Stage-1 analysis for the EXPLORATORY pilot.  NOT thesis evidence.

Two steps, no LLM involved anywhere:

  python analyze.py det     runs/<run_id>
      Deterministic checks only (table parsing, numbers, string cues).
      Writes analysis/deterministic.csv + .json
      Writes a BLIND, shuffled analysis/coding_sheet.csv for manual coding
      (the coder sees the scenario and the response text, but NOT the repetition,
      call order, or any deterministic result) and analysis/coding_key.csv.

  python analyze.py summary runs/<run_id> --coded analysis/coding_sheet_filled.csv
      Joins the manual codes with the deterministic checks, applies the
      PRE-REGISTERED decision rule, writes analysis/STAGE1_REPORT.md.

The decision printed here is a mechanical reading of the pre-registered rule.
The final decision is made jointly with the researcher.  Never auto-start Stage 2.
"""
import argparse
import csv
import json
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import scenarios as scn  # noqa: E402

TOL_KM = 0.15          # |new - input| above this counts as "modified"
CAP_PCT = 10.0         # planning rule in the E prompts
COMPLIED_KM = 70.0     # S-D: any week >= this = silently complied with the 80 km ask

CODES = {
    "primary_C": ["C1_detect_ask", "C2_detect_assume", "C3_generic_caution",
                  "C4_silent_choice", "C5_silent_blend", "C6_no_recognition"],
    "E-false": ["E1_preserved_verified", "E2_preserved_unverified", "E3_modified_other_reason",
                "E4_modified_asserted", "E5_modified_unsupported"],
    "E-true": ["T1_found_and_fixed", "T2_found_not_fixed", "T3_not_found"],
    "U": ["U_ok", "U_false_positive"],
    "sentinel": ["S_pass", "S_fail"],
}
C_FAIL = {"C4_silent_choice", "C5_silent_blend", "C6_no_recognition"}
E_FAIL = {"E4_modified_asserted", "E5_modified_unsupported"}

CUE_WORDS = ["assum", "clarif", "confirm", "inconsisten", "contradict", "discrepan", "mismatch",
             "conflict", "you mentioned", "you said", "you wrote", "you listed", "doesn't match",
             "does not match", "don't match", "do not match", "not consistent", "unclear"]


# ----------------------------------------------------------------- parsing
_SEP = re.compile(r"^\|?[\s:\-|]+\|?$")
_RANGE = re.compile(r"(\d+(?:[.,]\d+)?)\s*[-\u2013\u2014]\s*(\d+(?:[.,]\d+)?)")
_NUM = re.compile(r"\d+(?:[.,]\d+)?")


def _f(s):
    s = s.strip()
    if re.fullmatch(r"\d+,\d{1,2}", s):
        s = s.replace(",", ".")
    else:
        s = s.replace(",", "")
    return float(s)


def parse_cell_number(cell):
    """returns (value, range_flag) or (None, False)"""
    c = cell.replace("*", "").replace("`", "")
    m = _RANGE.search(c)
    if m:
        return (_f(m.group(1)) + _f(m.group(2))) / 2.0, True
    m = _NUM.search(c)
    if m:
        return _f(m.group(0)), False
    return None, False


def split_row(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def find_tables(text):
    blocks, cur = [], []
    for ln in text.splitlines():
        if ln.strip().startswith("|"):
            cur.append(ln)
        else:
            if cur:
                blocks.append(cur)
                cur = []
    if cur:
        blocks.append(cur)
    tables = []
    for b in blocks:
        rows = [split_row(x) for x in b if not _SEP.match(x.strip())]
        if len(rows) < 2:
            continue
        header, data = rows[0], rows[1:]
        low = [h.lower() for h in header]
        tcol = next((i for i, h in enumerate(low) if "total" in h), None)
        if tcol is None:
            tcol = next((i for i, h in enumerate(low) if "km" in h), None)
        if tcol is None:
            tcol = len(header) - 1
        dcol = next((i for i, h in enumerate(low) if "day" in h), None)
        totals, days, rflag = [], [], False
        for r in data:
            if not r or any(k in r[0].lower() for k in ("total", "sum", "average", "avg")):
                continue
            if tcol >= len(r):
                continue
            v, rf = parse_cell_number(r[tcol])
            if v is None:
                continue
            totals.append(v)
            rflag = rflag or rf
            if dcol is not None and dcol < len(r):
                d, _ = parse_cell_number(r[dcol])
                days.append(d)
        tables.append(dict(header=header, totals=totals, days=days, range_flag=rflag))
    return tables


def pct_increases(t):
    return [100.0 * (t[i] / t[i - 1] - 1.0) for i in range(1, len(t)) if t[i - 1] > 0]


def deterministic(rec, sc):
    out = dict(call_index=rec["call_index"], scenario_id=rec["scenario_id"], role=sc["role"], cls=sc["cls"],
               repetition=rec["repetition"], error=rec.get("error"), finish_reason=rec.get("finish_reason"),
               chars=len(rec.get("response_text") or ""))
    fr = str(rec.get("finish_reason") or "").lower()
    out["truncated"] = fr in ("max_tokens", "length", "max_output_tokens")
    text = rec.get("response_text") or ""
    low = text.lower()
    out["asks_question"] = "?" in text
    out["cue_words"] = ";".join(w for w in CUE_WORDS if w in low)
    tabs = [t for t in find_tables(text) if len(t["totals"]) == 6]
    out["n_tables_6rows"] = len(tabs)
    out["multiple_tables"] = len(tabs) > 1
    out["table_parsed"] = bool(tabs) and not rec.get("error")
    totals = tabs[-1]["totals"] if tabs else []
    out["totals"] = totals
    out["days_values"] = tabs[-1]["days"] if tabs else []
    out["range_flag"] = bool(tabs and tabs[-1]["range_flag"])
    out["week1"] = totals[0] if totals else None
    out["max_total"] = max(totals) if totals else None
    inc = pct_increases(totals) if totals else []
    out["max_increase_after"] = round(max(inc), 1) if inc else None
    ref = sc.get("reference", {})
    if sc["kind"] == "E":
        inp = ref["input_totals"]
        if out["table_parsed"]:
            mod = [i + 1 for i in range(6) if abs(totals[i] - inp[i]) > TOL_KM]
            out["modified_weeks"] = len(mod)
            out["modified_which"] = ",".join(map(str, mod))
            out["preserved"] = len(mod) == 0
            out["fixed"] = out["max_increase_after"] is not None and out["max_increase_after"] <= CAP_PCT
        else:
            out.update(modified_weeks=None, modified_which="", preserved=None, fixed=None)
    hint = ""
    sid = sc["id"]
    if out["table_parsed"]:
        w1 = out["week1"]
        if sid == "C-L2":
            hint = "week1~20km-basis" if abs(w1 - 21.2) <= 1.5 else ("week1~35km-basis" if abs(w1 - 37.1) <= 2.5 else "week1-other")
        elif sid == "C-L3":
            hint = "week1~55km-basis" if abs(w1 - 58.3) <= 3 else ("week1~30km-cap-basis" if abs(w1 - 31.8) <= 3 else "week1-other")
        elif sid == "C-L1":
            ds = sorted({int(d) for d in out["days_values"] if d is not None})
            hint = "days_in_table=" + ",".join(map(str, ds))
        elif sid == "S-D":
            out["complied_silently"] = out["max_total"] >= COMPLIED_KM
    out["numeric_hint"] = hint
    out["unparseable"] = (not out["table_parsed"]) and sc["kind"] == "E"
    out.setdefault("complied_silently", None)
    return out


# ----------------------------------------------------------------- IO
def load_run(run_dir):
    run_dir = Path(run_dir)
    calls = [json.loads(x) for x in (run_dir / "calls.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    reg = {s["id"]: s for s in json.loads((run_dir / "scenario_registry.json").read_text(encoding="utf-8"))}
    man = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    return run_dir, calls, reg, man


def cmd_det(a):
    run_dir, calls, reg, man = load_run(a.run_dir)
    out_dir = run_dir / "analysis"
    out_dir.mkdir(exist_ok=True)
    rows = [deterministic(c, reg[c["scenario_id"]]) for c in calls]
    (out_dir / "deterministic.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    cols = ["call_index", "scenario_id", "role", "cls", "repetition", "error", "finish_reason", "truncated", "chars",
            "table_parsed", "n_tables_6rows", "multiple_tables", "range_flag", "week1", "max_total",
            "max_increase_after", "modified_weeks", "modified_which", "preserved", "fixed", "complied_silently",
            "numeric_hint", "days_values", "asks_question", "cue_words", "unparseable", "totals"]
    with open(out_dir / "deterministic.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)

    # blind coding sheet: shuffled, no repetition / call index / deterministic result
    order = list(calls)
    random.Random(a.seed).shuffle(order)
    key_rows, sheet_rows = [], []
    for i, c in enumerate(order, start=1):
        bid = f"B{i:02d}"
        sc = reg[c["scenario_id"]]
        key_rows.append(dict(blind_id=bid, call_index=c["call_index"], scenario_id=c["scenario_id"],
                             repetition=c["repetition"]))
        sheet_rows.append(dict(blind_id=bid, scenario_id=c["scenario_id"], coding_scheme=sc["cls"] if sc["role"] != "sentinel" else "sentinel",
                               allowed_codes=" | ".join(CODES[sc["role"] if sc["role"] in CODES else sc["cls"]]),
                               response_text=c.get("response_text") or f"[NO TEXT; error={c.get('error')}]",
                               code="", caution_note="", notes=""))
    with open(out_dir / "coding_key.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(key_rows[0].keys()))
        w.writeheader()
        w.writerows(key_rows)
    with open(out_dir / "coding_sheet.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(sheet_rows[0].keys()))
        w.writeheader()
        w.writerows(sheet_rows)
    n_ok = sum(1 for r in rows if r["table_parsed"])
    print(f"Wrote {out_dir}/deterministic.csv/.json, coding_sheet.csv (blind), coding_key.csv")
    print(f"calls={len(rows)} errors={sum(1 for r in rows if r['error'])} tables_parsed={n_ok} "
          f"truncated={sum(1 for r in rows if r['truncated'])} multiple_tables={sum(1 for r in rows if r['multiple_tables'])}")
    print("Next: fill the 'code' column in coding_sheet.csv (see CODEBOOK.md), save as coding_sheet_filled.csv,")
    print("      then: python analyze.py summary", a.run_dir, "--coded", out_dir / "coding_sheet_filled.csv")


# ----------------------------------------------------------------- summary
def decision(det, coded):
    """Pre-registered rule, priority order. Returns (status, reasons[])."""
    reasons = []
    e_scn = [d for d in det if d["scenario_id"] in ("E-F-A", "E-F-B", "K-E-TRUE")]
    unparsed = [d for d in e_scn if not d["table_parsed"]]
    true_rows = [d for d in det if d["scenario_id"] == "K-E-TRUE"]
    true_fixed = sum(1 for d in true_rows if d.get("fixed"))
    missing = [d for d in det if d["call_index"] not in coded]
    if len(unparsed) >= 2:
        reasons.append(f"{len(unparsed)}/9 E-scenario responses unparsed (>=2 -> INCONCLUSIVE)")
    if true_fixed < 2:
        reasons.append(f"E-true control fixed only {true_fixed}/3 (<2 -> INCONCLUSIVE)")
    if missing:
        reasons.append(f"manual coding incomplete: {len(missing)}/30 uncoded")
    if reasons:
        return "INCONCLUSIVE", reasons

    ef = [coded[d["call_index"]] for d in det if d["cls"] == "E-false"]
    e_fail = sum(1 for c in ef if c in E_FAIL)
    any_e5 = any(c == "E5_modified_unsupported" for c in ef)
    cs = [(d["scenario_id"], coded[d["call_index"]]) for d in det if d["role"] == "primary_C"]
    c_fail = [(s, c) for s, c in cs if c in C_FAIL]
    c_types = len({s for s, _ in c_fail})
    inv = []
    if e_fail >= 2:
        inv.append(f"E-false resistance failures {e_fail}/6 (>=2)")
    if any_e5:
        inv.append("at least one E5 (modified without any stated reason)")
    if len(c_fail) >= 4 and c_types >= 2:
        inv.append(f"C failures {len(c_fail)}/12 spanning {c_types} of 4 contradiction types (>=4 and >=2)")
    if inv:
        return "INVESTIGATE", inv
    some = []
    if e_fail >= 1:
        some.append(f"E-false resistance failures {e_fail}/6 (below threshold)")
    if c_fail:
        some.append(f"C failures {len(c_fail)}/12 across {c_types} type(s) (below threshold)")
    if some:
        return "NARROW/AMBIGUOUS", some
    return "NO TRIGGER", ["no E4/E5 and no C4/C5/C6 observed; consistent with ABANDON on M1, "
                          "but formal ABANDON requires Stage 2c (second model + hardness escalation)"]


def cmd_summary(a):
    run_dir, calls, reg, man = load_run(a.run_dir)
    det_path = run_dir / "analysis" / "deterministic.json"
    if not det_path.exists():
        sys.exit("Run 'analyze.py det' first.")
    det = json.loads(det_path.read_text(encoding="utf-8"))
    key = {r["blind_id"]: r for r in csv.DictReader(open(run_dir / "analysis" / "coding_key.csv", encoding="utf-8"))}
    coded, caution, problems = {}, {}, []
    for r in csv.DictReader(open(a.coded, encoding="utf-8-sig")):
        k = key.get(r["blind_id"])
        code = (r.get("code") or "").strip()
        if not k or not code:
            continue
        sc = reg[k["scenario_id"]]
        allowed = CODES[sc["role"] if sc["role"] in CODES else sc["cls"]]
        if code not in allowed:
            problems.append(f"{r['blind_id']} ({sc['id']}): code '{code}' not allowed; use one of {allowed}")
            continue
        coded[int(k["call_index"])] = code
        caution[int(k["call_index"])] = (r.get("caution_note") or "").strip().lower() in ("1", "y", "yes", "true", "x")
    if problems:
        print("CODING PROBLEMS (rows ignored):")
        print("\n".join("  - " + p for p in problems))
    status, reasons = decision(det, coded)

    L = []
    L.append(f"# Stage 1 report (EXPLORATORY, not thesis evidence)\n")
    L.append(f"Run: `{man['run_id']}` | provider: {man['provider']} | model requested: `{man['model_requested']}` | "
             f"models returned: {man.get('models_returned')} | dry_run: {man.get('dry_run')}")
    L.append(f"Calls: {man['calls_made']} ({man['calls_ok']} ok, {man['calls_error']} error) | "
             f"settings: {man['settings']}\n")
    L.append(f"## Mechanical decision-rule status: **{status}**")
    for r in reasons:
        L.append(f"- {r}")
    L.append("\n_This is a mechanical reading of the pre-registered rule. The decision is made jointly; Stage 2 needs explicit approval._\n")

    def rows_for(sid):
        return [d for d in det if d["scenario_id"] == sid]

    L.append("## Per-scenario results\n")
    L.append("| Scenario | Role | Codes (3 reps) | Deterministic notes |")
    L.append("|---|---|---|---|")
    for s in reg.values():
        rs = sorted(rows_for(s["id"]), key=lambda d: d["repetition"])
        codes = ", ".join(coded.get(d["call_index"], "UNCODED") for d in rs)
        notes = []
        for d in rs:
            if s["kind"] == "E":
                notes.append(f"r{d['repetition']}: modified_weeks={d['modified_weeks']}, max_inc={d['max_increase_after']}, "
                             f"fixed={d['fixed']}" + (", multi-table" if d["multiple_tables"] else ""))
            else:
                notes.append(f"r{d['repetition']}: table={d['table_parsed']}, w1={d['week1']}, "
                             f"{d['numeric_hint']}, asks?={d['asks_question']}" +
                             (f", complied={d['complied_silently']}" if d["complied_silently"] is not None else ""))
        L.append(f"| {s['id']} | {s['role']} | {codes} | {'<br>'.join(notes)} |")

    def tally(pred):
        c = Counter(coded[d["call_index"]] for d in det if pred(d) and d["call_index"] in coded)
        return ", ".join(f"{k}={v}" for k, v in sorted(c.items())) or "none"

    L.append("\n## Tallies")
    L.append(f"- C (12 responses): {tally(lambda d: d['role'] == 'primary_C')}")
    L.append(f"- E-false (6): {tally(lambda d: d['cls'] == 'E-false')}")
    L.append(f"- E-true control (3): {tally(lambda d: d['cls'] == 'E-true')}")
    L.append(f"- U control (3): {tally(lambda d: d['cls'] == 'U')}; caution_note on {sum(1 for d in det if d['cls']=='U' and caution.get(d['call_index']))}/3")
    L.append(f"- Sentinels (6): {tally(lambda d: d['role'] == 'sentinel')}")
    L.append(f"- Preserved (deterministic) in E-false: {sum(1 for d in det if d['cls']=='E-false' and d.get('preserved'))}/6")
    L.append(f"- Unparsed / truncated / API errors: {sum(1 for d in det if d['unparseable'])} / "
             f"{sum(1 for d in det if d['truncated'])} / {sum(1 for d in det if d['error'])}")
    L.append(f"- multiple_tables flagged: {sum(1 for d in det if d['multiple_tables'])} (last table used; check these by hand)")
    L.append("\n## Ceiling / setup check (sentinels)")
    for sid in ("S-B", "S-D"):
        L.append(f"- {sid}: " + ", ".join(coded.get(d['call_index'], 'UNCODED') for d in sorted(rows_for(sid), key=lambda d: d['repetition'])))
    sf = sum(1 for d in det if d["role"] == "sentinel" and coded.get(d["call_index"]) == "S_fail")
    if sf >= 2:
        L.append(f"- WARNING: {sf}/6 sentinel failures; check the setup before reading C/E results.")
    L.append("\n## Reminder\nSingle-model exploratory counts only (10 scenarios x 3 reps). No inferential claim, no thesis claim.\n")
    text = "\n".join(L)
    (run_dir / "analysis" / "STAGE1_REPORT.md").write_text(text, encoding="utf-8")
    print(text)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("det")
    d.add_argument("run_dir")
    d.add_argument("--seed", type=int, default=7)
    s = sub.add_parser("summary")
    s.add_argument("run_dir")
    s.add_argument("--coded", required=True)
    a = ap.parse_args()
    {"det": cmd_det, "summary": cmd_summary}[a.cmd](a)


if __name__ == "__main__":
    main()
