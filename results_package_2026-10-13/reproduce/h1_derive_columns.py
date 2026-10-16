"""CALCULATOR for the H1 blind-check worksheet (written 2026-10-15). It does NOT read the checker bundle, the registry, the prompts or any other file: it reads ONLY the
worksheet CSV that the researcher filled and computes, with exact Decimal arithmetic, the arithmetic columns from the researcher's OWN transcriptions:
  MIL : wN_value (the number inside the transcription), and for weeks 2-5 increase, limit (P % of the previous week), percent increase and status;
  PAC : T_time_seconds (from T_time_displayed), wN_value (seconds per km), the unrounded finish time, the rounded finish time (half rounds up), the difference to the
        target and the status, for weeks 1-5.
It never writes: opaque_id, the dates, family, P_or_D_dist, T_time_displayed, tau_F, any wN_transcribed, week-1 status, the VERDICT or the notes. Those are the
researcher's reading and judgement (specification 11.2: the only judgement left to a person is which entries to write down).
Cells the researcher already filled are KEPT; if one differs from the computed value the row id and column name are listed (never the cell contents).
Writes a NEW csv (never overwrites). Prints only row ids and column names.
Usage: python -B -I h1_derive_columns.py --sheet <your filled csv> --out <new csv>"""
import argparse
import csv
import io
import os
import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

sys.dont_write_bytecode = True
WEEKS = range(1, 6)
DEC = 4


def cols(w):
    p = f"w{w}_"
    return (p + "transcribed", p + "value", p + "increase_km_or_implied_finish_s_2dp", p + "limit_km_2dp_or_rounded_finish_s", p + "percent_2dp_or_diff_s", p + "status")


def num(s, tokens=()):
    """Decimal from a transcription after removing one trailing unit token (case-insensitive) and spaces; None if not a plain number."""
    t = (s or "").strip()
    low = t.lower()
    for tok in sorted(tokens, key=len, reverse=True):
        if low.endswith(tok):
            t = t[: len(t) - len(tok)].strip()
            break
    try:
        v = Decimal(t)
    except InvalidOperation:
        return None
    return v if v.is_finite() else None


def mmss(s):
    t = (s or "").strip().lower()
    for tok in ("min/km", "/km"):
        if t.endswith(tok):
            t = t[: len(t) - len(tok)].strip()
            break
    parts = t.split(":")
    if len(parts) != 2 or not all(p.isdigit() for p in parts) or len(parts[1]) != 2:
        return None
    return int(parts[0]) * 60 + int(parts[1])


def hmmss(s):
    parts = (s or "").strip().split(":")
    if len(parts) != 3 or not all(p.isdigit() for p in parts) or len(parts[1]) != 2 or len(parts[2]) != 2:
        return None
    return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])


def fmt(d, places=DEC, floor=1):
    q = d.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)
    return f"{q:.{places}f}"


def plain(d):
    s = format(d, "f")
    return s


def derive_row(r):
    """Returns (computed {col: text}, problems [col names])."""
    out, bad = {}, []
    if not any((r.get(cols(w)[0]) or "").strip() for w in WEEKS):          # nothing transcribed yet: the row is left alone
        return out, bad
    pac = any((r.get(c) or "").strip() for c in ("T_time_displayed", "T_time_seconds", "tau_F"))
    if not pac:
        P = num(r.get("P_or_D_dist"), ("%",))
        if P is None:
            bad.append("P_or_D_dist")
        prev = None
        for w in WEEKS:
            tr, va, inc, lim, pct, st = cols(w)
            v = num(r.get(tr), ("km",))
            if v is None:
                if (r.get(tr) or "").strip():
                    bad.append(tr)
                prev = None
                continue
            out[va] = plain(v)
            if w >= 2 and prev is not None and P is not None and prev != 0:
                d = v - prev
                out[inc] = fmt(d, max(1, -d.as_tuple().exponent) if d.as_tuple().exponent < 0 else 1)
                out[lim] = fmt(P * prev / 100)
                out[pct] = fmt(d / prev * 100)
                out[st] = "over cap" if d * 100 > P * prev else "not over cap"
            prev = v
    else:
        D = num(r.get("P_or_D_dist"), ("km",))
        T = hmmss(r.get("T_time_displayed"))
        tau = num(r.get("tau_F"), ("sec", "s"))
        if D is None:
            bad.append("P_or_D_dist")
        if T is None:
            bad.append("T_time_displayed")
        else:
            out["T_time_seconds"] = str(T)
        if tau is None:
            bad.append("tau_F")
        for w in WEEKS:
            tr, va, inc, lim, pct, st = cols(w)
            sec = mmss(r.get(tr))
            if sec is None:
                if (r.get(tr) or "").strip():
                    bad.append(tr)
                continue
            out[va] = str(sec)
            if D is not None and T is not None and tau is not None:
                fin = D * sec
                rnd = int(fin.quantize(Decimal(1), rounding=ROUND_HALF_UP))
                diff = rnd - T
                out[inc] = fmt(fin)
                out[lim] = str(rnd)
                out[pct] = str(diff)
                out[st] = "|e|>tau" if abs(diff) > tau else "not"
    return out, bad


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--sheet", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    with open(a.sheet, "rb") as f:
        text = f.read().decode("utf-8-sig")
    rdr = csv.DictReader(io.StringIO(text, newline=""))
    header, rows = rdr.fieldnames, list(rdr)
    filled = conflicts = unreadable = 0
    report = []
    for r in rows:
        calc, bad = derive_row(r)
        for c in bad:
            report.append((r["opaque_id"], f"cannot read as a number / time: {c}"))
        if bad:
            unreadable += 1
        for c, v in calc.items():
            cur = (r.get(c) or "").strip()
            if not cur:
                r[c] = v
                filled += 1
            elif cur != v:
                try:
                    same = Decimal(cur) == Decimal(v)
                except InvalidOperation:
                    same = False
                if not same:
                    conflicts += 1
                    report.append((r["opaque_id"], f"your value differs from the computed value: {c}"))
    with open(a.out, "xb") as f:                                         # FileExistsError if it exists: never overwrites
        buf = io.StringIO(newline="")
        w = csv.DictWriter(buf, fieldnames=header, lineterminator="\r\n")
        w.writeheader()
        w.writerows(rows)
        f.write(buf.getvalue().encode("utf-8"))
    for oid, msg in report[:200]:
        print(oid, msg)
    print(f"rows: {len(rows)}; cells filled: {filled}; your cells that differ from the calculation: {conflicts}; rows with unreadable transcriptions: {unreadable}")
    return 0 if not (conflicts or unreadable) else 1


if __name__ == "__main__":
    sys.exit(main())
