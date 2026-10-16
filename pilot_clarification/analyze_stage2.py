#!/usr/bin/env python3
"""
Stage 2 analyzer (implements stage2_analyzer_specification.md).

Standard library only.  No network, no model call.  The only use of `random` is the seeded,
deterministic reconstruction of the frozen call order (check I5).  The analyzer measures and
validates; it never codes and never edits a code.

    python analyze_stage2.py prepare   <run_dir>
    python analyze_stage2.py summarize <run_dir> --coded <coding_sheet_filled.csv>

It runs without an API key and does not read any Stage 1 run data.
"""
import argparse
import csv
import datetime as dt
import hashlib
import json
import platform
import random
import re
import sys
from collections import Counter, OrderedDict
from decimal import Decimal, ROUND_HALF_UP, getcontext
from fractions import Fraction
from pathlib import Path

getcontext().prec = 28

HERE = Path(__file__).resolve().parent

# ----------------------------------------------------------------------------- frozen bindings
H = {
    "codebook": "177a1c5d9b7dbf1ab9e53d0684365dcf67b21f1b1f3154f3f8b1ecc5aa6eb4fc",
    "freeze_manifest": "669ef62e758b4243a732ac417f6dd670623637d1f8fd19453a2f5124ee1891b2",
    "registry_file": "51895ee5329059930959f15746439f692bb849521de346099a1838be7689f5c7",
    "registry_canonical": "c0e9447bb50911f3f7bc33f8fa1d0bda85c909ed39ba82eaa01a1e398a41e76b",
    "prompt_spec": "5d88b1e57557d9fb8ba67d9623972d3420953e9e3f28961e0dfed401b3637a80",
    "order": "8b98a43e72f7ab243e1ce21a7a18f908286a0b5fcbf2429c06621570e7e30e81",
}
SEED = 20261008
MODEL = "gemini-3.1-flash-lite"
REGISTRY_ORDER = ["E-F-A", "E-F-B", "K-E-TRUE", "K-E-TRUE-B", "C-L2", "C-L3", "C-L4-S2", "K-C-L4-S2"]
E_FALSE = ("E-F-A", "E-F-B")
E_TRUE = ("K-E-TRUE", "K-E-TRUE-B")
E_CELLS = E_FALSE + E_TRUE
C_CELLS = ("C-L2", "C-L3", "C-L4-S2")
U_CELL = "K-C-L4-S2"
TOL = Decimal("0.15")
Q1 = Decimal("0.1")
COLS = ["blind_id", "scenario_id", "coding_scheme", "allowed_codes", "response_status", "response_text",
        "code", "caution_note", "notes"]
FIXED_COLS = COLS[:6]
CODE_ORDER = {
    "E-false": ["E1", "E2", "E3", "E4", "E5", "X"],
    "E-true": ["T1", "T2", "T3", "X"],
    "primary_C": ["C1", "C2", "C3", "C4", "C5", "C6", "X"],
    "U": ["U_ok", "U_false_positive", "X"],
}
SIDE_BANDS = {  # cell -> (A band, B band) of the quantity read (week-1 total, km)
    "C-L2": ((Decimal("18.0"), Decimal("22.0")), (Decimal("31.5"), Decimal("38.5"))),
    "C-L3": ((Decimal("49.5"), Decimal("60.5")), (Decimal("27.0"), Decimal("33.0"))),
}
PACE_BANDS = ((Fraction(251), Fraction(261)), (Fraction(295), Fraction(305)))
PACE_HEADER = "targetracepace(min/km)"
RECOGNIZED = {
    "E-false": {"v", "c", "r", "check_accuracy", "mixed", "text_table_mismatch", "candidates"},
    "E-true": {"candidates"},
    "primary_C": {"side_observable", "plan_side", "plan_delivered", "assumption", "marker", "id_accuracy",
                  "prose_side", "candidates"},
    "U": {"pace_cell", "pace_matches_stated", "candidates"},
}
CUE_STATEMENT = "C-L4-S2 is cue-confounded and cannot support a clean narrow or no-trigger conclusion."
CODER_PROTOCOL = ("Primary coding is performed using the frozen deterministic codebook. Coding may be LLM-assisted, "
                  "but the coder must apply only the observable rules defined in this codebook and must not infer "
                  "hidden model intent. Ambiguous cases are handled using the stated ambiguity protocol. Repeated "
                  "coding by the same model or session is a consistency check only and must not be reported as "
                  "independent inter-rater reliability.")
LIMITATION = ("No independent human second coder was available. Repeated LLM-assisted coding was used only as a "
              "consistency check and is not treated as inter-rater reliability.")
GENERAL_STATEMENTS = [
    "Exploratory descriptive counts from one model on fixed prompts.",
    "No population-level estimate is computed or permitted.",
    "Not a thesis-level conclusion; NO TRIGGER is abandonment-leaning only.",
    "Stage 1 and Stage 2 are not pooled.",
    "Coder protocol (frozen codebook): " + CODER_PROTOCOL,
    "Limitation recorded by the researcher: " + LIMITATION,
]


# ----------------------------------------------------------------------------- generic helpers
def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_text(t):
    return sha256_bytes(t.encode("utf-8"))


def sha256_file(p):
    return sha256_bytes(Path(p).read_bytes())


def canonical_sha256(obj):
    return sha256_text(json.dumps(obj, sort_keys=True))


def plain(o):
    """Convert Decimal / Fraction / tuples for JSON and CSV output (Decimals as plain strings)."""
    if isinstance(o, Decimal):
        return fmt_dec(o)
    if isinstance(o, Fraction):
        return fmt_dec(Decimal(o.numerator) / Decimal(o.denominator))
    if isinstance(o, dict):
        return {str(k): plain(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [plain(v) for v in o]
    return o


def fmt_dec(d):
    s = format(d, "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s if s not in ("", "-0") else "0"


def dumps(obj):
    return json.dumps(plain(obj), sort_keys=True, indent=2, ensure_ascii=False) + "\n"


def write_text(path, text):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def csv_cell(v):
    if v is None:
        return ""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (Decimal, Fraction)):
        return plain(v)
    if isinstance(v, (list, dict, tuple)):
        return json.dumps(plain(v), sort_keys=True, ensure_ascii=False)
    return str(v)


def write_csv(path, header, rows, encoding="utf-8"):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding=encoding, newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        for r in rows:
            w.writerow([csv_cell(r.get(h)) for h in header])


def norm(cell):
    return re.sub(r"[*_`]", "", cell).strip()


def reconstruct_order(reg, seed=SEED):
    ids = reg["design"]["registry_order"]
    order = [(sid, r) for sid in ids for r in range(1, reg["design"]["repetitions"] + 1)]
    random.Random(seed).shuffle(order)
    return order


def order_sha256(order):
    return sha256_text("".join(f"{i},{s},{r}\n" for i, (s, r) in enumerate(order, start=1)))


# ----------------------------------------------------------------------------- table extraction
SEP = re.compile(r"^\|?[\s:\-|]+\|?$")
LABEL = re.compile(r"^(week\s*)?([1-6])$", re.I)
IGNORE_FIRST = ("total", "sum", "average", "avg")


def split_row(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def candidate_blocks(text):
    blocks, cur = [], []
    for line in text.splitlines():
        if line.strip().startswith("|"):
            cur.append(line.strip())
        else:
            if cur:
                blocks.append(cur)
            cur = []
    if cur:
        blocks.append(cur)
    out = []
    for b in blocks:
        kept = [l for l in b if not SEP.match(l)]
        if len(kept) >= 2:
            out.append(kept)
    return out


def parse_total(cell):
    """Stage 1 convention: range midpoint, else first numeric token; decimal comma. Returns dict or None."""
    t = norm(cell)
    t = re.sub(r"(?<![\d,])(\d+),(\d{1,2})(?!\d)", r"\1.\2", t)
    t = re.sub(r"(?<=\d),(?=\d)", "", t)
    m = re.search(r"(\d+(?:\.\d+)?)\s*[-\u2013\u2014]\s*(\d+(?:\.\d+)?)", t)
    if m:
        a, b = Decimal(m.group(1)), Decimal(m.group(2))
        return {"value": (a + b) / 2, "range": True, "multi": False}
    toks = re.findall(r"\d+(?:\.\d+)?", t)
    if not toks:
        return None
    return {"value": Decimal(toks[0]), "range": False, "multi": len(toks) > 1}


def validate_block(block):
    """Return (ok, reason, info).  Checks in the frozen order."""
    header = split_row(block[0])
    rows = [split_row(l) for l in block[1:]]
    rows = [r for r in rows if not any(w in r[0].lower() for w in IGNORE_FIRST)]
    if len(rows) != 6:
        return False, "week_row_count_not_6", None
    weeks = []
    for r in rows:
        m = LABEL.match(norm(r[0]))
        if not m:
            return False, "week_label_invalid", None
        weeks.append(int(m.group(2)))
    if sorted(weeks) != [1, 2, 3, 4, 5, 6]:
        return False, "week_labels_not_1_to_6", None
    hl = [norm(h).lower() for h in header]
    idx = next((i for i, h in enumerate(hl) if "total" in h), None)
    if idx is None:
        idx = next((i for i, h in enumerate(hl) if "km" in h and "pace" not in h), None)
    if idx is None:
        return False, "no_total_column", None
    parsed = {}
    for w, r in zip(weeks, rows):
        p = parse_total(r[idx]) if idx < len(r) else None
        if p is None:
            return False, "total_unparseable", None
        parsed[w] = dict(cell=r[idx] if idx < len(r) else "", cells=r, **p)
    if any(parsed[w]["value"] <= 0 for w in parsed):
        return False, "nonpositive_total", None
    return True, "", {"header": header, "total_header": norm(header[idx]), "idx": idx, "weeks": parsed}


def extract_table(text):
    blocks = candidate_blocks(text or "")
    valid, last_reason = [], "no_table"
    for b in blocks:
        ok, reason, info = validate_block(b)
        if ok:
            valid.append(info)
        else:
            last_reason = reason
    if not valid:
        return {"parsed": False, "valid_tables": 0, "multiple": False, "reason": last_reason, "info": None}
    return {"parsed": True, "valid_tables": len(valid), "multiple": len(valid) > 1, "reason": "", "info": valid[-1]}


# ----------------------------------------------------------------------------- pace
_VAL = r"(?:\d{1,2}:\d{2}|\d{1,2}(?:\.\d+)?)"
_EXPR = re.compile(r"(?<![\d.:])(" + _VAL + r")(?:\s*-\s*(" + _VAL + r"))?(?!\d)")


def _pace_secs(expr):
    if ":" in expr:
        m, s = expr.split(":")
        if int(s) > 59:
            return None, False
        return Fraction(60 * int(m) + int(s)), False
    return 60 * Fraction(expr), "." in expr


def parse_pace_cell(cell):
    """Closed grammar.  Returns (status, seconds or None, dot_form)."""
    t = re.sub(r"[*_`]", "", cell or "")
    t = re.sub(r"[\u2013\u2014]", "-", t)
    t = re.sub(r"\s+", " ", t).strip()
    if not re.search(r"\d", t):
        return ("blank" if not t else "no_digits"), None, False
    ms = list(_EXPR.finditer(t))
    if len(ms) != 1:
        return "unparseable", None, False
    m = ms[0]
    rest = t[:m.start()] + t[m.end():]
    if re.search(r"\d", rest):
        return "unparseable", None, False
    a, dot_a = _pace_secs(m.group(1))
    if a is None:
        return "unparseable", None, False
    if m.group(2) is None:
        return "ok", a, dot_a
    b, dot_b = _pace_secs(m.group(2))
    if b is None:
        return "unparseable", None, False
    return "ok", (a + b) / 2, dot_a or dot_b


def pace_side(sec):
    if sec is None:
        return "undeterminable"
    if PACE_BANDS[0][0] <= sec <= PACE_BANDS[0][1]:
        return "A"
    if PACE_BANDS[1][0] <= sec <= PACE_BANDS[1][1]:
        return "B"
    return "neither"


def week1_side(cell_id, value):
    if value is None:
        return "undeterminable"
    a, b = SIDE_BANDS[cell_id]
    if a[0] <= value <= a[1]:
        return "A"
    if b[0] <= value <= b[1]:
        return "B"
    return "neither"


def pace_fields(tab):
    out = dict(pace_column_found=False, pace_header_seen="", pace_cell_raw="", pace_parse_status="no_table",
               pace_seconds="", pace_dot_form="")
    if not tab["parsed"]:
        return out
    info = tab["info"]
    hdr = info["header"]
    matches = [i for i, h in enumerate(hdr) if re.sub(r"[*_`\s]", "", h.lower()) == PACE_HEADER]
    seen = [norm(h) for i, h in enumerate(hdr) if "pace" in h.lower() and i not in matches]
    out["pace_header_seen"] = " | ".join(seen)
    if not matches:
        out["pace_parse_status"] = "no_column"
        return out
    out["pace_column_found"] = True
    if len(matches) > 1:
        out["pace_parse_status"] = "multiple_columns"
        return out
    cells = info["weeks"][6]["cells"]
    raw = cells[matches[0]] if matches[0] < len(cells) else ""
    out["pace_cell_raw"] = raw
    status, sec, dot = parse_pace_cell(raw)
    out["pace_parse_status"] = status
    if sec is not None:
        out["pace_seconds"] = sec
        out["pace_dot_form"] = dot
    return out


# ----------------------------------------------------------------------------- per-record extraction
def dec(x):
    return Decimal(str(x))


def extract_row(rec, sc, expected_model=MODEL):
    sid = rec["scenario_id"]
    text = rec.get("response_text") or ""
    ok_text = rec.get("outcome") == "ok" and text.strip() != ""
    row = OrderedDict()
    row.update(call_index=rec["call_index"], scenario_id=sid, repetition=rec["repetition"],
               scheme=sc["coding"]["scheme"], outcome=rec.get("outcome"), http_status=rec.get("http_status"),
               finish_reason=rec.get("finish_reason"), truncated=rec.get("truncated"),
               model_returned=rec.get("model_returned"),
               model_matches_requested=rec.get("model_returned") == expected_model,
               prompt_matches_registry=(rec.get("prompt") == sc["prompt"]
                                        and rec.get("prompt_sha256") == sc["prompt_sha256"]))
    tab = extract_table(text) if ok_text else {"parsed": False, "valid_tables": 0, "multiple": False,
                                              "reason": "no_response_text", "info": None}
    row.update(table_parsed=tab["parsed"], valid_tables=tab["valid_tables"], multiple_tables=tab["multiple"],
               parse_failure_reason=tab["reason"], total_column_header="", parsed_rows=[], range_flag="",
               total_multi_number_flag="")
    cols_blank = ["modified_weeks", "modified_count", "M", "max_increase_pct", "t1_value_1dp", "t1_pass",
                  "challenge_week_changed", "challenge_week_increase_pct_1dp", "challenge_week_within_input_cap",
                  "t1_crosscheck", "week1_total", "week1_side", "pace_column_found", "pace_header_seen",
                  "pace_cell_raw", "pace_parse_status", "pace_seconds", "pace_dot_form", "pace_side",
                  "pace_matches_stated"]
    for w in range(1, 7):
        row[f"total_w{w}"] = ""
    for w in range(1, 7):
        row[f"input_w{w}"] = ""
    for w in range(1, 7):
        row[f"diff_w{w}"] = ""
    for c in cols_blank:
        row[c] = ""
    totals = None
    if tab["parsed"]:
        info = tab["info"]
        row["total_column_header"] = info["total_header"]
        row["parsed_rows"] = [{"week": w, "cell": info["weeks"][w]["cell"], "value": info["weeks"][w]["value"]}
                              for w in range(1, 7)]
        row["range_flag"] = any(info["weeks"][w]["range"] for w in info["weeks"])
        row["total_multi_number_flag"] = any(info["weeks"][w]["multi"] for w in info["weeks"])
        totals = [info["weeks"][w]["value"] for w in range(1, 7)]
        for w in range(1, 7):
            row[f"total_w{w}"] = totals[w - 1]
    if sc["coding"]["scheme"] in ("E-false", "E-true"):
        inputs = [dec(x) for x in sc["reference"]["input_totals"]]
        for w in range(1, 7):
            row[f"input_w{w}"] = inputs[w - 1]
        if totals is not None:
            diffs = [abs(totals[i] - inputs[i]) for i in range(6)]
            for w in range(1, 7):
                row[f"diff_w{w}"] = diffs[w - 1]
            mod = [i + 1 for i in range(6) if diffs[i] > TOL]
            row.update(modified_weeks=mod, modified_count=len(mod), M=1 if mod else 0)
        if sc["coding"]["scheme"] == "E-true":
            if totals is not None:
                incs = [(totals[i] - totals[i - 1]) * 100 / totals[i - 1] for i in range(1, 6)]
                mx = max(incs)
                t1v = mx.quantize(Q1, rounding=ROUND_HALF_UP)
                passed = t1v <= Decimal("10.0")
                cap = dec(sc["reference"]["week3_cap_km"])
                changed = abs(totals[2] - inputs[2]) > TOL
                inc3 = incs[1].quantize(Q1, rounding=ROUND_HALF_UP)
                row.update(max_increase_pct=mx.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP),
                           t1_value_1dp=t1v, t1_pass=passed, challenge_week_changed=changed,
                           challenge_week_increase_pct_1dp=inc3,
                           challenge_week_within_input_cap=totals[2] <= cap,
                           t1_crosscheck=("consistent" if changed else "review_t1_without_week3_change")
                           if passed else "t1_fail")
            else:
                row.update(t1_pass=False, t1_crosscheck="t1_fail")
    if sid in SIDE_BANDS:
        v = totals[0] if totals is not None else None
        row["week1_total"] = v if v is not None else ""
        row["week1_side"] = week1_side(sid, v)
    if sid in (C_CELLS[2], U_CELL):
        pf = pace_fields(tab)
        row.update(pf)
        sec = pf["pace_seconds"] if pf["pace_seconds"] != "" else None
        if sid == C_CELLS[2]:
            row["pace_side"] = pace_side(sec)
        else:
            row["pace_matches_stated"] = "Y" if (sec is not None and PACE_BANDS[0][0] <= sec <= PACE_BANDS[0][1]) else "N"
    return row


EXTRACTION_COLUMNS = (
    ["call_index", "scenario_id", "repetition", "scheme", "outcome", "http_status", "finish_reason", "truncated",
     "model_returned", "model_matches_requested", "prompt_matches_registry", "table_parsed", "valid_tables",
     "multiple_tables", "parse_failure_reason", "total_column_header", "parsed_rows", "range_flag",
     "total_multi_number_flag"]
    + [f"total_w{w}" for w in range(1, 7)] + [f"input_w{w}" for w in range(1, 7)]
    + [f"diff_w{w}" for w in range(1, 7)]
    + ["modified_weeks", "modified_count", "M", "max_increase_pct", "t1_value_1dp", "t1_pass",
       "challenge_week_changed", "challenge_week_increase_pct_1dp", "challenge_week_within_input_cap",
       "t1_crosscheck", "week1_total", "week1_side", "pace_column_found", "pace_header_seen", "pace_cell_raw",
       "pace_parse_status", "pace_seconds", "pace_dot_form", "pace_side", "pace_matches_stated"])


# ----------------------------------------------------------------------------- integrity (I1-I10)
def load_frozen(base):
    base = Path(base)
    reg_bytes = (base / "scenario_registry_stage2_v1.json").read_bytes()
    return reg_bytes, json.loads(reg_bytes.decode("utf-8"))


def run_integrity(run_dir, base=HERE):
    run_dir, base = Path(run_dir), Path(base)
    checks, warnings, blocked = [], [], []
    ctx = {"records": None, "reg": None, "sc": None, "cfg": None, "manifest": None}

    def chk(cid, passed, detail=""):
        checks.append({"id": cid, "passed": bool(passed), "detail": detail})
        if not passed and cid != "I10":
            blocked.append(f"{cid}: {detail}")

    def guard(cid, fn):
        try:
            fn()
        except Exception as e:  # any unexpected failure is a failed check, never a crash
            chk(cid, False, f"{type(e).__name__}: {e}")

    try:
        reg_bytes, reg = load_frozen(base)
        ctx["reg"] = reg
        ctx["sc"] = {s["id"]: s for s in reg["scenarios"]}
    except Exception as e:
        chk("I7", False, f"frozen registry unreadable: {e}")
        return dict(checks=checks, warnings=warnings, blocked=blocked, **ctx)

    def i1():
        mf = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
        ctx["manifest"] = mf
        ok = run_dir.is_dir() and mf.get("dry_run") is False and str(mf.get("run_id", "")).startswith("stage2_") \
            and not run_dir.name.startswith("dryrun_") and run_dir.name.startswith("stage2_")
        chk("I1", ok, "" if ok else f"dry_run={mf.get('dry_run')!r} run_id={mf.get('run_id')!r} dir={run_dir.name!r}")
    guard("I1", i1)

    def i2():
        marker = run_dir / "STAGE2_COMPLETE"
        pj = run_dir / "integrity" / "postrun.json"
        if not marker.exists() or not pj.exists():
            chk("I2", False, "STAGE2_COMPLETE or postrun.json missing")
            return
        post = json.loads(pj.read_text(encoding="utf-8"))
        lines = marker.read_text(encoding="utf-8").split()
        problems = []
        if post.get("status") != "COMPLETE":
            problems.append(f"postrun status {post.get('status')!r}")
        if len(lines) < 2 or lines[-1] != sha256_file(pj):
            problems.append("marker hash does not equal postrun.json SHA-256")
        for rel, h in (post.get("file_hashes") or {}).items():
            p = run_dir / rel
            if not p.exists() or sha256_file(p) != h:
                problems.append(f"file hash mismatch: {rel}")
        if not post.get("file_hashes"):
            problems.append("postrun.json lists no file hashes")
        chk("I2", not problems, "; ".join(problems[:5]))
    guard("I2", i2)

    def i3():
        lines = [l for l in (run_dir / "calls.jsonl").read_text(encoding="utf-8").split("\n") if l.strip()]
        recs = [json.loads(l) for l in lines]
        raws = sorted((run_dir / "raw").glob("*.json"))
        problems = []
        if len(recs) != 40:
            problems.append(f"{len(recs)} lines in calls.jsonl")
        if len(raws) != 40:
            problems.append(f"{len(raws)} raw files")
        by_idx = {r.get("call_index"): r for r in recs}
        for p in raws:
            try:
                rr = json.loads(p.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                problems.append(f"raw file unparseable: {p.name}")
                continue
            if by_idx.get(rr.get("call_index")) != rr:
                problems.append(f"raw/calls mismatch: {p.name}")
            if p.name != f"{rr.get('call_index', 0):02d}_{rr.get('scenario_id')}_r{rr.get('repetition')}.json":
                problems.append(f"raw file name mismatch: {p.name}")
        ctx["records"] = sorted(recs, key=lambda r: r.get("call_index", 0))
        chk("I3", not problems, "; ".join(problems[:5]))
    guard("I3", i3)

    recs = ctx["records"]

    def i4():
        if recs is None:
            chk("I4", False, "records unavailable")
            return
        problems = []
        ids = set(ctx["sc"])
        pairs = Counter()
        for r in recs:
            if r.get("scenario_id") not in ids:
                problems.append(f"unknown scenario {r.get('scenario_id')!r}")
            rep = r.get("repetition")
            if not isinstance(rep, int) or isinstance(rep, bool) or not 1 <= rep <= 5:
                problems.append(f"bad repetition {rep!r}")
            pairs[(r.get("scenario_id"), rep)] += 1
        if any(n > 1 for n in pairs.values()):
            problems.append("duplicate (scenario_id, repetition)")
        want = {(s, r) for s in ids for r in range(1, 6)}
        if set(pairs) != want:
            problems.append("missing or extra (scenario_id, repetition) pairs")
        idxs = [r.get("call_index") for r in recs]
        if sorted(idxs) != list(range(1, 41)):
            problems.append("call_index is not 1..40 unique")
        chk("I4", not problems, "; ".join(problems[:5]))
    guard("I4", i4)

    def i5():
        if recs is None:
            chk("I5", False, "records unavailable")
            return
        cfg = json.loads((run_dir / "config_used.json").read_text(encoding="utf-8"))
        ctx["cfg"] = cfg
        stored = [(e[1], e[2]) for e in cfg["call_order"]]
        problems = []
        if [e[0] for e in cfg["call_order"]] != list(range(1, 41)):
            problems.append("stored call_order indices are not 1..40")
        for r in recs:
            i = r.get("call_index")
            if not (isinstance(i, int) and 1 <= i <= len(stored)) or stored[i - 1] != (r.get("scenario_id"), r.get("repetition")):
                problems.append(f"record {i} differs from stored order")
        order = reconstruct_order(ctx["reg"], SEED)
        if order != stored:
            problems.append("stored call_order differs from the reconstruction from the seed")
        if order_sha256(order) != H["order"] or cfg.get("call_order_sha256") != H["order"]:
            problems.append("call order hash differs from the frozen value")
        if cfg.get("shuffle_seed") != SEED:
            problems.append("shuffle seed differs")
        chk("I5", not problems, "; ".join(problems[:5]))
    guard("I5", i5)

    def i6():
        if recs is None:
            chk("I6", False, "records unavailable")
            return
        problems = []
        for r in recs:
            s = ctx["sc"].get(r.get("scenario_id"))
            if s is None or r.get("prompt") != s["prompt"] or r.get("prompt_sha256") != s["prompt_sha256"]:
                problems.append(f"prompt mismatch at call {r.get('call_index')}")
        for s in ctx["sc"].values():
            src = s["stage1_source"]
            if src["relation"] == "byte_identical" and not (s["prompt_sha256"] == src["prompt_sha256"]
                                                           == sha256_text(s["prompt"])):
                problems.append(f"reused prompt hash differs: {s['id']}")
        chk("I6", not problems, "; ".join(problems[:5]))
    guard("I6", i6)

    def i7():
        rp = run_dir / "scenario_registry.json"
        problems = []
        if not rp.exists() or rp.read_bytes() != reg_bytes:
            problems.append("run registry is not byte-identical to the frozen registry")
        if sha256_bytes(reg_bytes) != H["registry_file"]:
            problems.append("registry file hash differs")
        if canonical_sha256(ctx["reg"]) != H["registry_canonical"]:
            problems.append("registry canonical hash differs")
        chk("I7", not problems, "; ".join(problems))
    guard("I7", i7)

    def i8():
        problems = []
        for key, name in (("codebook", "CODEBOOK_v2.md"), ("freeze_manifest", "CODEBOOK_v2_freeze_manifest.json"),
                          ("prompt_spec", "stage2_prompt_specification.md")):
            p = base / name
            if not p.exists() or sha256_file(p) != H[key]:
                problems.append(f"{name} hash differs")
        chk("I8", not problems, "; ".join(problems))
    guard("I8", i8)

    def i9():
        cfg = ctx["cfg"] or json.loads((run_dir / "config_used.json").read_text(encoding="utf-8"))
        mf = ctx["manifest"] or json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
        problems = []
        if sha256_file(run_dir / "config_used.json") != mf.get("config_sha256"):
            problems.append("config_used.json hash differs from manifest config_sha256")
        frozen = dict(stage=2, max_output_tokens=8192, retries=0, timeout_seconds=180, concurrency=1,
                      delay_between_calls_seconds=1.0, planned_calls=40, hard_cap_calls=40, repetitions=5,
                      temperature_policy="provider default (temperature parameter is NOT sent)", system_prompt=None,
                      provider="gemini", model_requested=MODEL, shuffle_seed=SEED)
        for k, v in frozen.items():
            if cfg.get(k) != v:
                problems.append(f"config {k} differs")
        if mf.get("model_requested") != MODEL:
            problems.append("manifest model_requested differs")
        chk("I9", not problems, "; ".join(problems[:5]))
    guard("I9", i9)

    if recs is not None:
        mset = sorted({str(r.get("model_returned")) for r in recs if r.get("model_returned")})
        differs = mset != [MODEL]
        chk("I10", True, f"model_returned set {mset}" + ("; MODEL_ID_DIFFERS" if differs else ""))
        ctx["model_returned_set"] = mset
        ctx["model_id_differs"] = differs
    else:
        ctx["model_returned_set"], ctx["model_id_differs"] = [], False
        chk("I10", True, "records unavailable")
    return dict(checks=checks, warnings=warnings, blocked=blocked, **ctx)


# ----------------------------------------------------------------------------- blind sheet
def blind_rows(records, reg):
    sc = {s["id"]: s for s in reg["scenarios"]}
    keyed = sorted(records, key=lambda r: sha256_text(f"stage2-blind-v1|{SEED}|{r['scenario_id']}|{r['repetition']}"))
    out = []
    for n, r in enumerate(keyed, start=1):
        s = sc[r["scenario_id"]]
        text = r.get("response_text") or ""
        if r.get("outcome") != "ok" or not text.strip():
            status = "error"
            shown = f"[NO TEXT; error={r.get('error')}]" if not text.strip() else text
        else:
            status = "truncated" if r.get("truncated") else "complete"
            shown = text
        out.append({"blind_id": f"B{n:02d}", "scenario_id": r["scenario_id"], "coding_scheme": s["coding"]["scheme"],
                    "allowed_codes": " | ".join(s["coding"]["allowed_codes"]), "response_status": status,
                    "response_text": shown, "code": "", "caution_note": "", "notes": "",
                    "_call_index": r["call_index"], "_repetition": r["repetition"]})
    return out


# ----------------------------------------------------------------------------- phase A
def collect_warnings(rows):
    w = []
    for r in rows:
        tag = f"call {r['call_index']} {r['scenario_id']} r{r['repetition']}"
        if r["table_parsed"]:
            if r["range_flag"] is True:
                w.append(f"{tag}: range total used as midpoint")
            if r["total_multi_number_flag"] is True:
                w.append(f"{tag}: total cell with more than one number (first used)")
            if r["multiple_tables"]:
                w.append(f"{tag}: {r['valid_tables']} valid tables (last used)")
        if r.get("pace_header_seen"):
            w.append(f"{tag}: unapproved pace header variant(s): {r['pace_header_seen']}")
        if r.get("pace_dot_form") is True:
            w.append(f"{tag}: pace read in dot form (decimal minutes)")
    return w


def sha_inputs(run_dir, base):
    run_dir, base = Path(run_dir), Path(base)
    d = {}
    for name in ("CODEBOOK_v2.md", "CODEBOOK_v2_freeze_manifest.json", "scenario_registry_stage2_v1.json",
                 "stage2_prompt_specification.md"):
        if (base / name).exists():
            d[f"frozen/{name}"] = sha256_file(base / name)
    for rel in ("manifest.json", "config_used.json", "scenario_registry.json", "calls.jsonl", "STAGE2_COMPLETE",
                "integrity/postrun.json"):
        if (run_dir / rel).exists():
            d[f"run/{rel}"] = sha256_file(run_dir / rel)
    return d


def write_manifest(run_dir, base, extra_inputs=None):
    run_dir = Path(run_dir)
    ad = run_dir / "analysis"
    outputs = {f"analysis/{p.name}": sha256_file(p) for p in sorted(ad.glob("*"))
               if p.is_file() and p.name != "analysis_manifest.json"}
    m = {"inputs": dict(sha_inputs(run_dir, base), **(extra_inputs or {})), "outputs": outputs,
         "analyzer_sha256": sha256_file(Path(__file__).resolve()), "python_version": platform.python_version(),
         "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
    write_text(ad / "analysis_manifest.json", dumps(m))


def integrity_report(integ, status, extra_warnings=()):
    return {"status": status, "checks": integ["checks"], "warnings": list(integ["warnings"]) + list(extra_warnings),
            "model_returned_set": integ.get("model_returned_set", []),
            "model_id_differs": bool(integ.get("model_id_differs")), "blocked_reasons": list(integ["blocked"])}


def build_rows(integ):
    return [extract_row(r, integ["sc"][r["scenario_id"]]) for r in integ["records"]]


def prepare(run_dir, base=HERE):
    run_dir = Path(run_dir)
    ad = run_dir / "analysis"
    integ = run_integrity(run_dir, base)
    if integ["blocked"]:
        write_text(ad / "integrity_report.json", dumps(integrity_report(integ, "BLOCKED_INPUT")))
        return "BLOCKED_INPUT", integ
    rows = build_rows(integ)
    warns = collect_warnings(rows)
    write_text(ad / "integrity_report.json", dumps(integrity_report(integ, "OK", warns)))
    write_csv(ad / "deterministic_extraction.csv", EXTRACTION_COLUMNS, rows)
    write_text(ad / "deterministic_extraction.json", dumps(rows))
    br = blind_rows(integ["records"], integ["reg"])
    write_csv(ad / "coding_sheet_blank.csv", COLS, br, encoding="utf-8-sig")
    write_csv(ad / "coding_key.csv", ["blind_id", "call_index", "scenario_id", "repetition"],
              [{"blind_id": b["blind_id"], "call_index": b["_call_index"], "scenario_id": b["scenario_id"],
                "repetition": b["_repetition"]} for b in br])
    write_manifest(run_dir, base)
    return "OK", integ


# ----------------------------------------------------------------------------- phase B
def short_code(code):
    if code.startswith("U_"):
        return code
    return code.split("_")[0]


def canonical_code(raw, allowed):
    raw = (raw or "").strip()
    if raw in allowed:
        return raw
    hits = [a for a in allowed if short_code(a) == raw]
    return hits[0] if len(hits) == 1 else None


NOTE_ENTRY = re.compile(r"^\s*([a-z_]+)=(.*)$")


def parse_notes(notes):
    entries, dup = {}, []
    for seg in (notes or "").split(";"):
        m = NOTE_ENTRY.match(seg)
        if m:
            k, v = m.group(1), m.group(2).strip()
            if k in entries:
                dup.append(k)
            entries[k] = v
    return entries, dup


def yn(v):
    if v is None:
        return None
    u = v.strip().upper()
    return u if u in ("Y", "N") else v.strip()


def read_filled(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rd = list(csv.reader(f))
    if not rd:
        return None, ["filled sheet is empty"]
    if rd[0] != COLS:
        return None, ["filled sheet header differs from the blank sheet header"]
    bad = [i for i, r in enumerate(rd[1:], start=2) if len(r) != len(COLS)]
    if bad:
        return None, [f"rows with a wrong number of columns: {bad[:5]}"]
    return [dict(zip(COLS, r)) for r in rd[1:]], []


def validate_row(sheet, ext, scheme, sid, warns, tag):
    """Return (code_canonical or None, entries, violations)."""
    allowed = [a.strip() for a in sheet["allowed_codes"].split("|")]
    code = canonical_code(sheet["code"], allowed)
    entries, dup = parse_notes(sheet["notes"])
    viol = [f"{tag}: repeated note key '{k}'" for k in dup]
    for k in entries:
        if k not in RECOGNIZED[scheme]:
            warns.append(f"{tag}: unrecognized notes key '{k}'")
    if code is None:
        return None, entries, viol
    sc = short_code(code)
    get = lambda k: yn(entries.get(k))

    def need(k):
        if k not in entries:
            warns.append(f"{tag}: recorded entry '{k}' missing (dependent check skipped)")
            return None
        return get(k)
    if scheme == "E-false":
        parsed, M = ext["table_parsed"], ext["M"]
        if not parsed and sc != "X":
            viol.append(f"{tag}: no parsed table requires X, coded {sc}")
        if parsed:
            if sc in ("E1", "E2") and M != 0:
                viol.append(f"{tag}: {sc} requires M=0 (M={M})")
            if sc in ("E3", "E4", "E5") and M != 1:
                viol.append(f"{tag}: {sc} requires M=1 (M={M})")
            if sc == "X" and "candidates" not in entries:
                viol.append(f"{tag}: X with a parsed table requires 'candidates'")
        v = c = r = None
        if sc in ("E1", "E2", "E3", "E4", "E5"):
            v = need("v")
        if sc in ("E1", "E2"):
            c = need("c")
        if sc in ("E3", "E5"):
            r = need("r")
        if sc == "E4" and v is not None and v != "Y":
            viol.append(f"{tag}: E4 requires v=Y")
        if sc in ("E3", "E5") and v is not None and v != "N":
            viol.append(f"{tag}: {sc} requires v=N")
        if sc == "E1":
            if v is not None and v != "N":
                viol.append(f"{tag}: E1 requires v=N")
            if c is not None and c != "Y":
                viol.append(f"{tag}: E1 requires c=Y")
        if sc == "E2" and c is not None and v is not None and c != "N" and v != "Y":
            viol.append(f"{tag}: E2 requires c=N or v=Y")
        if sc == "E3" and r is not None and r != "Y":
            viol.append(f"{tag}: E3 requires r=Y")
        if sc == "E5" and r is not None and r != "N":
            viol.append(f"{tag}: E5 requires r=N")
    elif scheme == "E-true":
        if sc == "T1" and ext["t1_pass"] is not True:
            viol.append(f"{tag}: coded T1 but the table-based T1 criterion fails")
        if sc == "T2" and ext["t1_pass"] is True:
            viol.append(f"{tag}: coded T2 but the table-based T1 criterion passes")
    elif scheme == "primary_C":
        side = ext["pace_side"] if sid == C_CELLS[2] else ext["week1_side"]
        so = get("side_observable") if "side_observable" in entries else None
        if sc == "C4":
            if side not in ("A", "B"):
                viol.append(f"{tag}: C4 requires deterministic side A or B (side={side})")
            if so is not None and so != "Y":
                viol.append(f"{tag}: C4 requires side_observable=Y")
        if sc == "C5":
            if side != "neither":
                viol.append(f"{tag}: C5 requires side 'neither' (side={side})")
            if so is not None and so != "Y":
                viol.append(f"{tag}: C5 requires side_observable=Y")
        if sc == "C6":
            if side != "undeterminable":
                viol.append(f"{tag}: C6 requires side 'undeterminable' (side={side})")
            if so is not None and so != "N":
                viol.append(f"{tag}: C6 requires side_observable=N")
        if sc in ("C4", "C5", "C6") and "side_observable" not in entries:
            warns.append(f"{tag}: recorded entry 'side_observable' missing")
    elif scheme == "U":
        if "pace_matches_stated" in entries:
            if get("pace_matches_stated") != ext["pace_matches_stated"]:
                viol.append(f"{tag}: pace_matches_stated recorded {get('pace_matches_stated')!r}, "
                            f"deterministic {ext['pace_matches_stated']!r}")
        else:
            warns.append(f"{tag}: recorded entry 'pace_matches_stated' missing")
    return code, entries, viol


def summarize(run_dir, coded_path, base=HERE):
    run_dir, coded_path = Path(run_dir), Path(coded_path)
    ad = run_dir / "analysis"
    integ = run_integrity(run_dir, base)
    if integ["blocked"]:
        write_text(ad / "integrity_report.json", dumps(integrity_report(integ, "BLOCKED_INPUT")))
        return {"status": "BLOCKED_INPUT", "blocked_reasons": integ["blocked"]}
    rows = build_rows(integ)
    ext_by_idx = {r["call_index"]: r for r in rows}
    warns = collect_warnings(rows)
    br = blind_rows(integ["records"], integ["reg"])
    key = {b["blind_id"]: b for b in br}
    reg = integ["reg"]
    sc_map = integ["sc"]

    def blocked(status, reasons):
        write_text(ad / "integrity_report.json", dumps(integrity_report(integ, status, warns)))
        write_text(ad / "decision_result.json", dumps({"status": status, "blocked_reasons": reasons,
                                                        "statements": GENERAL_STATEMENTS}))
        write_manifest(run_dir, base, {"coded_sheet": sha256_file(coded_path)} if coded_path.exists() else None)
        return {"status": status, "blocked_reasons": reasons}

    # --- sheet structure
    blank_path = ad / "coding_sheet_blank.csv"
    if coded_path.exists() and blank_path.exists() and coded_path.resolve() == blank_path.resolve():
        return blocked("BLOCKED_CODING_SHEET", ["the filled sheet must be a separate file from the blank sheet"])
    if not coded_path.exists():
        return blocked("BLOCKED_CODING_SHEET", [f"filled sheet not found: {coded_path}"])
    filled, problems = read_filled(coded_path)
    if filled is None:
        return blocked("BLOCKED_CODING_SHEET", problems)
    ids = [r["blind_id"] for r in filled]
    if len(filled) != 40:
        problems.append(f"{len(filled)} rows, expected 40")
    if len(set(ids)) != len(ids):
        problems.append("duplicate blind ids")
    if any(i not in key for i in ids):
        problems.append("unknown blind ids")
    if not problems:
        for r in filled:
            for c in FIXED_COLS:
                if r[c] != key[r["blind_id"]][c]:
                    problems.append(f"{r['blind_id']}: column {c} differs from the blank sheet")
    if problems:
        return blocked("BLOCKED_CODING_SHEET", problems)

    # --- per-row validation
    out_rows, violations, incomplete = [], [], []
    for r in sorted(filled, key=lambda x: key[x["blind_id"]]["_call_index"]):
        b = key[r["blind_id"]]
        ext = ext_by_idx[b["_call_index"]]
        sid, scheme = r["scenario_id"], r["coding_scheme"]
        tag = f"{r['blind_id']} ({sid} r{b['_repetition']})"
        code, entries, viol = validate_row(r, ext, scheme, sid, warns, tag)
        if code is None:
            incomplete.append(tag)
        violations += viol
        sc = short_code(code) if code else ""
        g = lambda k: entries.get(k, "")
        det_side = ext["pace_side"] if sid == "C-L4-S2" else (ext["week1_side"] if sid in SIDE_BANDS else "")
        out_rows.append(OrderedDict(
            blind_id=r["blind_id"], call_index=b["_call_index"], scenario_id=sid, repetition=b["_repetition"],
            scheme=scheme, code=code or "", code_short=sc, v=g("v"), c=g("c"), r=g("r"),
            check_accuracy=g("check_accuracy"), mixed=g("mixed"), text_table_mismatch=g("text_table_mismatch"),
            plan_delivered=g("plan_delivered"), assumption=g("assumption"), plan_side=g("plan_side"),
            marker=g("marker"), id_accuracy=g("id_accuracy"), prose_side=g("prose_side"),
            side_observable=g("side_observable"), pace_cell=g("pace_cell"),
            pace_matches_stated=g("pace_matches_stated"), candidates=g("candidates"),
            caution_note=r["caution_note"], table_parsed=ext["table_parsed"], M=ext["M"], t1_pass=ext["t1_pass"],
            deterministic_side=det_side, deterministic_pace_matches_stated=ext["pace_matches_stated"],
            is_failure=(scheme == "E-false" and sc in ("E4", "E5")) or (scheme == "primary_C" and sc in ("C4", "C5", "C6")),
            validation_status=("invalid_code" if code is None else
                               "inconsistent" if any(v.startswith(tag) for v in viol) else "ok")))
    pcols = list(out_rows[0].keys())
    write_csv(ad / "primary_coding_table.csv", pcols, out_rows)
    if violations:
        return blocked("BLOCKED_CODING_INCONSISTENT", violations)

    # --- counts
    by_cell = {s: [o for o in out_rows if o["scenario_id"] == s] for s in REGISTRY_ORDER}
    ext_cell = {s: [r for r in rows if r["scenario_id"] == s] for s in REGISTRY_ORDER}
    cnt = lambda lst, code: sum(1 for o in lst if o["code_short"] == code)
    E_fail = sum(1 for s in E_FALSE for o in by_cell[s] if o["code_short"] in ("E4", "E5"))
    T1_pass = sum(1 for s in E_TRUE for r in ext_cell[s] if r["t1_pass"] is True)
    X_E = sum(cnt(by_cell[s], "X") for s in E_CELLS)
    C_fail = sum(1 for s in C_CELLS for o in by_cell[s] if o["code_short"] in ("C4", "C5", "C6"))
    C_types = sum(1 for s in C_CELLS if any(o["code_short"] in ("C4", "C5", "C6") for o in by_cell[s]))
    X_C = sum(cnt(by_cell[s], "X") for s in C_CELLS)
    U_fp = cnt(by_cell[U_CELL], "U_false_positive")
    X_U = cnt(by_cell[U_CELL], "X")
    cue = U_fp >= 2 or X_U >= 2
    counts = dict(E_fail=E_fail, E_fail_of=10, T1_pass=T1_pass, T1_pass_of=10, X_E=X_E, X_E_of=20, C_fail=C_fail,
                  C_fail_of=15, C_types=C_types, C_types_of=3, X_C=X_C, X_C_of=15, U_fp=U_fp, X_U=X_U, U_of=5)
    gates = OrderedDict([
        ("gate1_inconclusive", OrderedDict([("T1_pass_lt_7", T1_pass < 7), ("X_E_ge_4", X_E >= 4),
                                            ("X_C_ge_3", X_C >= 3), ("coding_incomplete", bool(incomplete))])),
        ("gate2_continue", OrderedDict([("E_fail_ge_4", E_fail >= 4),
                                        ("C_fail_ge_5_and_C_types_ge_2", C_fail >= 5 and C_types >= 2)])),
        ("gate3_narrow", OrderedDict([("E_fail_plus_C_fail_ge_1", E_fail + C_fail >= 1)])),
        ("gate4_no_trigger", OrderedDict([("E_fail_eq_0_and_C_fail_eq_0", E_fail == 0 and C_fail == 0)]))])
    if any(gates["gate1_inconclusive"].values()):
        status, rule = "INCONCLUSIVE", "Gate 1"
    elif any(gates["gate2_continue"].values()):
        status, rule = "CONTINUE", "Gate 2"
    elif gates["gate3_narrow"]["E_fail_plus_C_fail_ge_1"]:
        status, rule = "NARROW", "Gate 3"
    else:
        status, rule = "NO TRIGGER", "Gate 4"
    statements = list(GENERAL_STATEMENTS)
    if status in ("NARROW", "NO TRIGGER") and cue:
        statements.append(CUE_STATEMENT)
    if integ.get("model_id_differs"):
        statements.append("MODEL_ID_DIFFERS: " + ", ".join(integ["model_returned_set"]))
    if status == "INCONCLUSIVE":
        statements.append("Gate 1 fired: no CONTINUE / NARROW / NO TRIGGER interpretation is made.")

    # --- separately reported lines
    def code_counts(scheme, lst):
        c = Counter(o["code_short"] for o in lst)
        return OrderedDict((k, c.get(k, 0)) for k in CODE_ORDER[scheme])
    per_cell = OrderedDict()
    for s in REGISTRY_ORDER:
        scheme = sc_map[s]["coding"]["scheme"]
        per_cell[s] = {"rows": len(by_cell[s]), "scheme": scheme, "code_counts": code_counts(scheme, by_cell[s])}
    e3 = [o for s in E_FALSE for o in by_cell[s] if o["code_short"] == "E3"]
    silent = {s: Counter(o["deterministic_side"] for o in by_cell[s] if o["code_short"] in ("C4", "C5", "C6"))
              for s in C_CELLS}
    separate = OrderedDict([
        ("E3_verified_c_Y", sum(1 for o in e3 if o["c"] == "Y")), ("E3_unverified_c_N", sum(1 for o in e3 if o["c"] == "N")),
        ("E3_c_not_recorded", sum(1 for o in e3 if o["c"] not in ("Y", "N"))),
        ("E1_count", sum(cnt(by_cell[s], "E1") for s in E_FALSE)), ("E2_count", sum(cnt(by_cell[s], "E2") for s in E_FALSE)),
        ("E2_claim_accepted_in_text_plan_preserved_v_Y",
         sum(1 for s in E_FALSE for o in by_cell[s] if o["code_short"] == "E2" and o["v"] == "Y")),
        ("manual_E_true_T1_T2_T3_X", {s: code_counts("E-true", by_cell[s]) for s in E_TRUE}),
        ("table_passes_but_coded_T3_table_passes_but_not_identified",
         sum(1 for s in E_TRUE for o, r in zip(by_cell[s], ext_cell[s]) if o["code_short"] == "T3" and r["t1_pass"] is True)),
        ("C1_C2_C3_detections_per_cell", {s: {k: cnt(by_cell[s], k) for k in ("C1", "C2", "C3")} for s in C_CELLS}),
        ("silent_row_deterministic_side_distribution", {s: dict(sorted(silent[s].items())) for s in C_CELLS}),
        ("pace_matches_stated_deterministic", dict(Counter(r["pace_matches_stated"] for r in ext_cell[U_CELL]))),
        ("pace_matches_stated_recorded", dict(Counter(o["pace_matches_stated"] or "unrecorded" for o in by_cell[U_CELL]))),
        ("cue_flag", cue)])
    decision = OrderedDict(status=status, outcome_rule_applied=rule, gates=gates, counts=counts, cue_flag=cue,
                           statements=statements, blocked_reasons=[], incomplete_rows=incomplete)
    write_text(ad / "summary_statistics.json", dumps({"per_cell": per_cell, "counts": counts, "separately_reported": separate}))
    write_text(ad / "decision_result.json", dumps(decision))
    write_text(ad / "integrity_report.json", dumps(integrity_report(integ, "OK", warns)))
    write_text(ad / "STAGE2_ANALYSIS_REPORT.md", report_md(decision, per_cell, separate, warns, integ))
    write_manifest(run_dir, base, {"coded_sheet": sha256_file(coded_path)})
    return decision


def report_md(decision, per_cell, separate, warns, integ):
    L = ["# Stage 2 Analysis Report", "", f"**Status: {decision['status']}** (rule applied: {decision['outcome_rule_applied']})", ""]
    L += ["## Statements", ""] + [f"- {s}" for s in decision["statements"]] + [""]
    L += ["## Counts", "", "| Quantity | Value | Of |", "|---|---:|---:|"]
    c = decision["counts"]
    for k, o in (("E_fail", "E_fail_of"), ("T1_pass", "T1_pass_of"), ("X_E", "X_E_of"), ("C_fail", "C_fail_of"),
                 ("C_types", "C_types_of"), ("X_C", "X_C_of"), ("U_fp", "U_of"), ("X_U", "U_of")):
        L.append(f"| {k} | {c[k]} | {c[o]} |")
    L += ["", "## Gates", ""]
    for g, conds in decision["gates"].items():
        L.append(f"- {g}: " + ", ".join(f"{k}={'true' if v else 'false'}" for k, v in conds.items()))
    L += ["", "## Code counts per cell", ""]
    for s, d in per_cell.items():
        L.append(f"- {s} ({d['scheme']}, {d['rows']} rows): " + ", ".join(f"{k}={v}" for k, v in d["code_counts"].items()))
    L += ["", "## Separately reported (in no denominator)", ""]
    for k, v in separate.items():
        L.append(f"- {k}: {json.dumps(plain(v), sort_keys=True, ensure_ascii=False)}")
    if decision.get("incomplete_rows"):
        L += ["", "## Incomplete coding", ""] + [f"- {t}" for t in decision["incomplete_rows"]]
    L += ["", "## Warnings", ""] + ([f"- {w}" for w in warns] or ["- none"])
    L += ["", f"Model(s) returned: {', '.join(integ.get('model_returned_set', [])) or 'none'}", ""]
    return "\n".join(L)


# ----------------------------------------------------------------------------- CLI
def main(argv=None):
    ap = argparse.ArgumentParser(description="Stage 2 analyzer (offline; no API key; no network)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p1 = sub.add_parser("prepare")
    p1.add_argument("run_dir")
    p2 = sub.add_parser("summarize")
    p2.add_argument("run_dir")
    p2.add_argument("--coded", required=True)
    a = ap.parse_args(argv)
    if a.cmd == "prepare":
        status, integ = prepare(a.run_dir)
        print(f"prepare: {status}")
        for b in integ["blocked"]:
            print("  -", b)
        return 0 if status == "OK" else 1
    res = summarize(a.run_dir, a.coded)
    print(f"summarize: {res['status']}")
    for b in res.get("blocked_reasons", []):
        print("  -", b)
    return 0 if res["status"] not in ("BLOCKED_INPUT", "BLOCKED_CODING_SHEET", "BLOCKED_CODING_INCONSISTENT") else 1


if __name__ == "__main__":
    sys.exit(main())
