#!/usr/bin/env python3
"""
Stage 2 reconciliation: deterministic derivation of a reconciled coding sheet.

Implements STAGE2_RECONCILIATION_ADDENDUM_v1.md.  Offline, standard library only, no randomness,
no timestamps.  It never edits the original coding sheet; it writes a separate derivative sheet and a
derivation log, and refuses to overwrite either.

    python reconcile_stage2_coding.py

Rules (computed with the frozen analyzer's own functions, not typed in by hand):
  R1_PACE_HEADER         U rows: recorded pace_matches_stated replaced by the analyzer's deterministic value.
  R2_BASELINE_ROW        E-false rows whose final table is unparsed but not coded X are coded X_unclassifiable.
  R3_NOTES_SERIALIZATION a notes segment that repeats a key is turned into free text by prefixing "note: ".
The set of affected rows must equal the seven approved rows, otherwise nothing is written.
"""
import csv
import hashlib
import io
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
RUN = HERE / "runs" / "stage2_gemini_20261008T035839Z"
ORIG = RUN / "analysis" / "coding_sheet_filled.csv"
OUT_SHEET = RUN / "analysis" / "coding_sheet_filled_reconciled_v1.csv"
OUT_LOG = HERE / "STAGE2_RECONCILIATION_DERIVATION_v1.csv"

FROZEN = {
    HERE / "CODEBOOK_v2.md": "177a1c5d9b7dbf1ab9e53d0684365dcf67b21f1b1f3154f3f8b1ecc5aa6eb4fc",
    HERE / "analyze_stage2.py": "08e8432e52ec9ed6c68730eb288cf32348c54355aa8709a3bccc0edd72aa3056",
    HERE / "stage2_analyzer_specification.md": "4d55c305da83c2d6d62f1ac7b725e1001884aaab0dda20dae2a70799e470ba5b",
    ORIG: "6337dee9fa14f197e5c3a8fda1dd66d729a2bad0c199d0b743f7a68414de5040",
}
APPROVED = {"B11", "B13", "B20", "B22", "B29", "B30", "B36"}
COLS = ["blind_id", "scenario_id", "coding_scheme", "allowed_codes", "response_status", "response_text",
        "code", "caution_note", "notes"]
LOG_COLS = ["blind_id", "field", "original_value", "reconciled_value", "rule_id", "reason", "source_rule",
            "original_sheet_sha256"]
ENTRY = re.compile(r"^\s*([a-z_]+)=(.*)$")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def fail(msg):
    sys.exit("RECONCILIATION STOPPED: " + msg)


def main():
    for p, h in FROZEN.items():
        if sha(p) != h:
            fail(f"hash mismatch for {p.name}: {sha(p)} != {h}")
    man = json.loads((RUN / "manifest.json").read_text(encoding="utf-8"))["bindings"]
    if man["analyzer_sha256"] != FROZEN[HERE / "analyze_stage2.py"] or \
            man["analyzer_specification_sha256"] != FROZEN[HERE / "stage2_analyzer_specification.md"] or \
            man["codebook_sha256"] != FROZEN[HERE / "CODEBOOK_v2.md"]:
        fail("run manifest bindings differ from the frozen hashes")
    if OUT_SHEET.exists() or OUT_LOG.exists():
        fail("an output file already exists; refusing to overwrite")

    sys.path.insert(0, str(HERE))
    import analyze_stage2 as A

    raw = ORIG.read_bytes()
    if raw[:3] != b"\xef\xbb\xbf":
        fail("original sheet has no BOM")
    rows = list(csv.reader(io.StringIO(raw.decode("utf-8-sig"), newline="")))
    if rows[0] != COLS:
        fail("unexpected header")
    probe = io.StringIO(newline="")
    csv.writer(probe, lineterminator="\n").writerows(rows)
    if ("﻿" + probe.getvalue()).encode("utf-8") != raw:
        fail("round-trip of the original sheet is not byte-identical; cannot guarantee field-level preservation")
    body = rows[1:]
    ids = [r[0] for r in body]
    if len(body) != 40 or len(set(ids)) != 40:
        fail("original sheet is not 40 unique rows")

    sha0 = FROZEN[ORIG]
    log = []
    out = [list(rows[0])]
    changed = set()
    for r in body:
        d = dict(zip(COLS, r))
        new = dict(d)
        tab = A.extract_table(d["response_text"])
        allowed = [a.strip() for a in d["allowed_codes"].split("|")]
        scheme = d["coding_scheme"]

        # R3: repeated note keys -> free text (applies to any scheme)
        segs, seen, new_segs, r3 = d["notes"].split(";"), set(), [], False
        for s in segs:
            m = ENTRY.match(s)
            if m and m.group(1) in seen:
                lead = s[:len(s) - len(s.lstrip())]
                s = lead + "note: " + s.lstrip()
                r3 = True
            elif m:
                seen.add(m.group(1))
            new_segs.append(s)
        if r3:
            new["notes"] = ";".join(new_segs)
            log.append((d["blind_id"], "notes", d["notes"], new["notes"], "R3_NOTES_SERIALIZATION",
                        "notes segment repeated a key and is converted to free text; code unchanged",
                        "stage2_analyzer_specification.md section 12 (notes grammar)", sha0))
            changed.add(d["blind_id"])

        # R2: E-false row with an unparsed final table must be X
        if scheme == "E-false" and not tab["parsed"] and A.short_code(d["code"]) != "X":
            xs = [a for a in allowed if A.short_code(a) == "X"]
            if len(xs) != 1:
                fail(f"{d['blind_id']}: no unique X code in allowed_codes")
            new["code"] = xs[0]
            log.append((d["blind_id"], "code", d["code"], new["code"], "R2_BASELINE_ROW",
                        "final table unparsed (" + str(tab.get("reason", "")) + "); unparsed E-false row is X",
                        "stage2_analyzer_specification.md section 3 (exactly six data rows; no repair) and section 6",
                        sha0))
            changed.add(d["blind_id"])

        # R1: recorded pace_matches_stated -> deterministic value (U rows)
        if scheme == "U":
            pf = A.pace_fields(tab)
            sec = pf["pace_seconds"] if pf["pace_seconds"] != "" else None
            det = "Y" if (sec is not None and A.PACE_BANDS[0][0] <= sec <= A.PACE_BANDS[0][1]) else "N"
            parts, hit, orig_v = d["notes"].split(";"), False, None
            for i, s in enumerate(parts):
                m = ENTRY.match(s)
                if m and m.group(1) == "pace_matches_stated":
                    orig_v = m.group(2).strip()
                    if orig_v.upper() != det:
                        head, _, tail = s.partition("=")
                        parts[i] = head + "=" + tail.replace(tail.strip(), det, 1)
                        hit = True
            if hit:
                new["notes"] = ";".join(parts)
                log.append((d["blind_id"], "notes:pace_matches_stated", orig_v, det, "R1_PACE_HEADER",
                            "target-race-pace header not approved (" + pf["pace_header_seen"] + "); column absent",
                            "stage2_analyzer_specification.md sections 8-9 (header rule; undeterminable = N)", sha0))
                changed.add(d["blind_id"])
        out.append([new[c] for c in COLS])

    if changed != APPROVED:
        fail(f"affected rows {sorted(changed)} differ from the approved set {sorted(APPROVED)}; nothing written")
    final = out[1:]
    if len(final) != 40 or [r[0] for r in final] != ids:
        fail("row count or order changed")
    for r in final:
        if r[6].strip() not in [a.strip() for a in r[3].split("|")]:
            fail(f"{r[0]}: final code {r[6]!r} not in allowed_codes")
        for i in (0, 1, 2, 3, 4, 5):
            if r[i] != next(b for b in body if b[0] == r[0])[i]:
                fail(f"{r[0]}: an input column changed")
    untouched = [b for b in body if b[0] not in APPROVED]
    if [f for f in final if f[0] not in APPROVED] != untouched:
        fail("an unaffected row differs from the original")

    log.sort(key=lambda t: (t[0], t[1]))
    sl = io.StringIO(newline="")
    w = csv.writer(sl, lineterminator="\n")
    w.writerow(LOG_COLS)
    w.writerows(log)
    OUT_LOG.write_bytes(sl.getvalue().encode("utf-8"))
    ss = io.StringIO(newline="")
    csv.writer(ss, lineterminator="\n").writerows(out)
    OUT_SHEET.write_bytes(("﻿" + ss.getvalue()).encode("utf-8"))

    assert sha(ORIG) == FROZEN[ORIG]
    print("rows:", len(final), "| affected:", sorted(changed), "| log entries:", len(log))
    print("original sheet sha256 :", sha(ORIG))
    print("derivative sheet      :", OUT_SHEET, sha(OUT_SHEET))
    print("derivation log        :", OUT_LOG, sha(OUT_LOG))
    print("script                :", Path(__file__).name, sha(__file__))


if __name__ == "__main__":
    main()
