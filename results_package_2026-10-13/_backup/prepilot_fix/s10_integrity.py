"""Post-run integrity of a pilot or main run folder (specification 10, 13.8, 13.9) -- decision record 12.32. Read-only; prints no response text.
Checks: one status marker; hash-chained ledger valid and equal to the summary; per call intent -> raw -> classified in order; raw file hash equals the
ledger and the calls.jsonl line; every record's prompt hash equals the published prompt hash; call keys unique (no retry, no replacement) and,
for a pilot, equal to pilot_calls.txt in order; a COMPLETE run has every planned call; model ID returned; observed token cost against OD-10.
Usage: python -B -I s10_integrity.py --run <dir> --build <build>   exit 0 = no problem."""
import argparse
import hashlib
import json
import os
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
import s10_runner as RN  # noqa: E402


def rb(p):
    with open(p, "rb") as f:
        return f.read()


def verify_run(run, build):
    P, st = [], {}
    marks = [m for m in ("RUN_COMPLETE", "RUN_INCOMPLETE") if os.path.exists(os.path.join(run, m))]
    if len(marks) != 1:
        return ["not exactly one status marker"], st
    summ = json.loads(rb(os.path.join(run, marks[0])))
    scope = summ["scope"]
    kind = "main" if scope == "main" else "pilot"
    led = [json.loads(l) for l in rb(os.path.join(run, "ledger.jsonl")).decode().split("\n") if l]
    prev = "0" * 64
    for e in led:
        if e["prev"] != prev:
            P.append("ledger chain broken")
            break
        prev = hashlib.sha256(RN.cj(e)).hexdigest()
    if prev != summ["ledger_final_hash"]:
        P.append("ledger final hash differs from the summary")
    recs = [json.loads(l) for l in rb(os.path.join(run, "calls.jsonl")).decode().split("\n") if l]
    if len(recs) != summ["recorded_calls"]:
        P.append("calls.jsonl length differs from the summary")
    ev = [(e["event"], e["call_index"]) for e in led]
    if ev != [(k, i) for i in range(1, len(recs) + 1) for k in ("intent", "raw", "classified")]:
        P.append("ledger events are not intent/raw/classified per call in order")
    table = {(r["template_id"], r["condition"]): r["sha256"] for r in json.loads(rb(os.path.join(build, kind, "prompt_table.json")))}
    keys = [r["call_key"] for r in recs]
    if len(set(keys)) != len(keys):
        P.append("duplicate call keys (retry or replacement)")
    raws = {e["call_index"]: e["raw_sha256"] for e in led if e["event"] == "raw"}
    for r in recs:
        raw = rb(os.path.join(run, "raw", f"{r['call_index']:05d}.json"))
        if hashlib.sha256(raw).hexdigest() != raws.get(r["call_index"]):
            P.append(f"raw hash differs from the ledger at call {r['call_index']}")
        if json.loads(raw) != r:
            P.append(f"raw record differs from calls.jsonl at call {r['call_index']}")
        if table.get((r["template_id"], r["condition"])) != r["prompt_sha256"]:
            P.append(f"prompt hash differs from the build at call {r['call_index']}")
    if len(os.listdir(os.path.join(run, "raw"))) != len(recs):
        P.append("raw folder size")
    if kind == "pilot":
        planned = rb(os.path.join(build, "pilot", "pilot_calls.txt")).decode().split("\n")[:-1]
        if keys != planned[:len(keys)]:
            P.append("pilot calls differ from pilot_calls.txt (order or content)")
    if marks[0] == "RUN_COMPLETE" and len(recs) != summ["planned_calls"]:
        P.append("COMPLETE run with missing calls")
    toks_in = sum(((r.get("usage") or {}).get("promptTokenCount") or 0) for r in recs)
    toks_out = sum(((r.get("usage") or {}).get("candidatesTokenCount") or 0) for r in recs)
    st = {"scope": scope, "status": marks[0], "recorded": len(recs), "models_returned": sorted({r.get("model_returned") for r in recs if r.get("model_returned")}),
          "observed_tokens": {"prompt": toks_in, "completion": toks_out},
          "observed_cost_usd_at_recorded_prices": float((F(toks_in) * F(30, 100) + F(toks_out) * F(250, 100)) / 10 ** 6)}
    if st["observed_cost_usd_at_recorded_prices"] >= 100:
        P.append("observed cost reaches the OD-10 limit")
    return P, st


def main(argv=None):
    a = argparse.ArgumentParser()
    a.add_argument("--run", required=True)
    a.add_argument("--build", required=True)
    a = a.parse_args(argv)
    P, st = verify_run(a.run, a.build)
    for p in P[:30]:
        print("PROBLEM:", p)
    print(json.dumps(st, sort_keys=True))
    print("RUN INTEGRITY OK" if not P else f"{len(P)} problem(s)")
    return 1 if P else 0


if __name__ == "__main__":
    sys.exit(main())
