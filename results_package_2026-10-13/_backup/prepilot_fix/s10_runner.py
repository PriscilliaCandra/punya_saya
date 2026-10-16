"""Pilot / main-run harness (specification 10, 13.2, 13.3, 13.6, 13.8, 21.1 steps 10-12) -- decision record 12.30. NOT RUN.

Gates (all must hold, otherwise GateClosed and nothing is created): the published build verifies (s8_verify) and Implementation B
agrees; a Step 9 evidence file proves the human blind check (completion date, last viewing date, delay >= FZ row 19 = 7 days,
worksheet hash, adjudication) and is not self-contradictory; an owner authorization file names the scope (pilot_round_N or main),
the exact number of calls, the cost ceiling and the source of the input-size figure, and the recomputed hard-cap cost stays below the
OD-10 limit; for the main run a final pilot decision record with final_decision PASS exists. The runner never creates evidence or
authorization files, never reads the registry's expected states for any decision, and prints no response text.

Per call: intent entry (write-ahead, hash-chained) -> provider call (retries 0, timeout 180 s, concurrency 1, delay 1 s) -> raw
record stored BEFORE any parsing -> classification (s10_scoring). Main run: halt per 13.8 (s7_decision.main_run_halt); a halted or
incomplete run is marked INCOMPLETE and nothing is replaced. The Gemini provider below follows the public REST shape and is
UNVERIFIED against the live API (never exercised); tests use MockProvider only.
"""
import datetime
import hashlib
import json
import os
import sys
import time
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
RD = os.path.normpath(os.path.join(HERE, ".."))
for d in (HERE, os.path.join(RD, "step7"), os.path.join(RD, "step8"), os.path.join(RD, "step9")):
    sys.path.insert(0, d)
sys.dont_write_bytecode = True
import impl_b  # noqa: E402
import s10_scoring as SC  # noqa: E402
import s7_decision as D  # noqa: E402
import s8_verify  # noqa: E402

FZ_PATH = os.path.join(RD, "PARAMETER_FREEZE_MANIFEST_FZ_v1.json")
EXPECTED_SETTINGS = {"model_id": "gemini-3.5-flash-lite", "thinking_level": "minimal", "max_output_tokens": 8192, "retries": 0,
                     "timeout_s": 180, "delay_between_calls_s": 1, "concurrency": 1}


class GateClosed(Exception):
    def __init__(self, reasons):
        super().__init__("; ".join(reasons))
        self.reasons = reasons


def sha(b):
    return hashlib.sha256(b).hexdigest()


def cj(o):
    return (json.dumps(o, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def file_sha(p):
    with open(p, "rb") as f:
        return sha(f.read())


def file_bytes(p):
    with open(p, "rb") as f:
        return f.read()


def jl(p):
    with open(p, "rb") as f:
        return json.loads(f.read().decode("utf-8"))


def _utc(s):
    return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)


def hard_cap_cost_usd(slots, i_max_tokens, out_tokens=8192, p_in=F(30, 100), p_out=F(250, 100)):
    return (F(slots) * (F(i_max_tokens) * p_in + F(out_tokens) * p_out)) / 10 ** 6


def check_gates(scope, build, evidence_path, auth_path, pilot_record_path=None, verify_build=True):
    """Return the frozen register settings if every gate holds, else raise GateClosed with all reasons."""
    why = []
    fz = jl(FZ_PATH)["register"]
    m = fz["row17_model_and_settings"]
    got = {k: m[k] for k in EXPECTED_SETTINGS}
    if got != EXPECTED_SETTINGS:
        why.append("model settings of the register differ from the expected frozen values")
    if verify_build:
        if s8_verify.verify(build):
            why.append("Step 8 verifier reports problems")
        if impl_b.verify(build)["failures"]:
            why.append("Implementation B does not agree")
    if not os.path.exists(evidence_path):
        why.append("Step 9 evidence file missing (human blind check not documented)")
    else:
        ev = jl(evidence_path)
        hc = ev.get("human_blind_check") or {}
        try:
            delay = (_utc(hc["completed_utc"]) - _utc(hc["last_registry_view_utc"])).days
            if delay < fz["row19_blind_check"]["minimum_delay_days"]:
                why.append(f"blind-check delay {delay} days < {fz['row19_blind_check']['minimum_delay_days']}")
        except (KeyError, ValueError):
            why.append("blind-check dates missing or malformed")
        if hc.get("coverage_percent") != 100:
            why.append("blind-check coverage is not 100 percent")
        if len(hc.get("worksheet_sha256", "")) != 64:
            why.append("blind-check worksheet hash missing")
        if hc.get("adjudication") not in ("AGREE", "ADJUDICATED_NO_REJECT"):
            why.append("blind-check adjudication is not AGREE / ADJUDICATED_NO_REJECT")
        if ev.get("build_manifest_sha256") != file_sha(os.path.join(build, "manifest.json")):
            why.append("evidence refers to another build")
    if not os.path.exists(auth_path):
        why.append("owner authorization file missing")
    else:
        au = jl(auth_path)
        planned = {"pilot_round_1": 18, "pilot_round_2": 18, "main": fz["row13_C_max_planned_main_call_slots"]}.get(scope)
        if planned is None or au.get("scope") != scope or au.get("max_calls") != planned or au.get("authorized_by") != "owner":
            why.append("authorization does not match the scope and the planned number of calls")
        try:
            cost = hard_cap_cost_usd(planned, au["input_tokens_per_call_assumed"])
            if cost >= fz["operational_cost_limit_usd"] or au.get("cost_ceiling_usd") != fz["operational_cost_limit_usd"]:
                why.append("hard-cap cost not below the OD-10 limit or ceiling not stated")
        except (KeyError, TypeError):
            why.append("input-size assumption missing in the authorization")
    if scope == "main":
        if not pilot_record_path or not os.path.exists(pilot_record_path):
            why.append("final pilot decision record missing")
        else:
            rec = jl(pilot_record_path)
            if rec.get("final_decision") != "PASS":
                why.append("final pilot decision is not PASS")
    if why:
        raise GateClosed(why)
    return m


def plan_calls(scope, build, pilot_record_path=None):
    """List of call dicts in execution order. Pilot: canonical order, one repetition. Main: the canonical call list shuffled once
    by random.Random(seed).shuffle with the seed of the decision record (10); the list hash must equal the recorded one."""
    if scope.startswith("pilot"):
        with open(os.path.join(build, "pilot", "pilot_calls.txt"), "rb") as f:
            lines = f.read().decode("ascii").split("\n")[:-1]
    else:
        reg = jl(os.path.join(build, "main", "registry.json"))
        fz = jl(FZ_PATH)["register"]
        text = D.call_list([t["id"] for t in reg["templates"]], fz["row12_R"])
        rec = jl(pilot_record_path)
        if sha(text.encode("ascii")) != rec["call_list_sha256"]:
            raise GateClosed(["call list hash differs from the decision record"])
        lines = D.shuffled_order(text, rec["seed"])
    out = []
    for n, ln in enumerate(lines, 1):
        tid, cond, rep = ln.split(",")
        out.append({"call_index": n, "call_key": ln, "template_id": tid, "condition": cond, "repetition": int(rep)})
    return out


class MockProvider:
    """Deterministic scripted provider for tests: script is a callable (call_key, prompt) -> dict."""
    def __init__(self, script):
        self.script, self.calls = script, 0

    def generate(self, prompt, settings, call_key):
        self.calls += 1
        return self.script(call_key, prompt)


class GeminiProvider:
    """REST provider. UNVERIFIED against the live API; the key comes from the environment only and is never stored or printed."""
    def __init__(self, model_id, env="GEMINI_API_KEY"):
        self.model_id, self.env = model_id, env

    def generate(self, prompt, settings, call_key):
        import urllib.error
        import urllib.request
        key = os.environ.get(self.env)
        if not key:
            return {"http_status": None, "text": "", "error": "no API key in the environment"}
        body = {"contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"maxOutputTokens": settings["max_output_tokens"], "thinkingConfig": {"thinkingLevel": settings["thinking_level"]}}}
        req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_id}:generateContent",
                                     data=json.dumps(body).encode("utf-8"), headers={"Content-Type": "application/json", "x-goog-api-key": key})
        try:
            with urllib.request.urlopen(req, timeout=settings["timeout_s"]) as r:
                data = json.loads(r.read().decode("utf-8"))
                status = r.status
        except urllib.error.HTTPError as e:
            return {"http_status": e.code, "text": "", "error": f"HTTP {e.code}"}
        except Exception as e:                                       # timeout or transport failure (SF1); message not stored beyond the class
            return {"http_status": None, "text": "", "error": type(e).__name__}
        cands = data.get("candidates") or []
        text = "".join(p.get("text", "") for p in (cands[0].get("content", {}).get("parts", []) if cands else []))
        return {"http_status": status, "text": text, "error": None, "finish_reason": cands[0].get("finishReason") if cands else None,
                "model_returned": data.get("modelVersion"), "usage": data.get("usageMetadata")}


def run(scope, build, out_dir, provider, *, evidence_path, auth_path, pilot_record_path=None, sleeper=time.sleep, clock=None, verify_build=True):
    settings = check_gates(scope, build, evidence_path, auth_path, pilot_record_path, verify_build)
    plan = plan_calls(scope, build, pilot_record_path)
    fz = jl(FZ_PATH)["register"]
    pil = fz["row18_pilot"]
    meta = {t["id"]: t for t in jl(os.path.join(build, "main" if scope == "main" else "pilot", "registry.json"))["templates"]}
    os.makedirs(os.path.join(out_dir, "raw"))                         # FileExistsError if the output exists: nothing is overwritten
    clock = clock or (lambda: datetime.datetime.now(datetime.timezone.utc))
    prev, consec, sf_total, done = "0" * 64, 0, 0, 0
    records = []
    halted = None
    with open(os.path.join(out_dir, "ledger.jsonl"), "xb") as led, open(os.path.join(out_dir, "calls.jsonl"), "xb") as calls:
        def ledger(entry):
            nonlocal prev
            entry = dict(entry, prev=prev)
            b = cj(entry)
            prev = sha(b)
            led.write(b)
            led.flush()
        for c in plan:
            with open(os.path.join(build, "main" if scope == "main" else "pilot", "prompts", f"{c['template_id']}-{c['condition']}.txt"), "rb") as f:
                prompt = f.read().decode("ascii")
            ledger({"event": "intent", "call_index": c["call_index"], "call_key": c["call_key"]})
            t0 = clock()
            try:
                res = provider.generate(prompt, settings, c["call_key"])
            except Exception as e:
                res = {"http_status": None, "text": "", "error": type(e).__name__}
            rec = dict(c, utc_start=t0.strftime("%Y-%m-%dT%H:%M:%SZ"), http_status=res.get("http_status"), error=res.get("error"),
                       response_text=res.get("text") or "", finish_reason=res.get("finish_reason"), model_returned=res.get("model_returned"),
                       usage=res.get("usage"), latency_ms=res.get("latency_ms"), prompt_sha256=sha(prompt.encode("ascii")))
            raw = cj(rec)
            with open(os.path.join(out_dir, "raw", f"{c['call_index']:05d}.json"), "xb") as f:
                f.write(raw)                                          # raw record stored before any parsing
            ledger({"event": "raw", "call_index": c["call_index"], "raw_sha256": sha(raw)})
            calls.write(raw)
            calls.flush()
            cl = SC.classify(rec)
            ledger({"event": "classified", "call_index": c["call_index"], "outcome": cl["outcome"], "flags": cl["flags"]})
            records.append(rec)
            done += 1
            if cl["outcome"] == "SF":
                consec += 1
                sf_total += 1
            else:
                consec = 0
            if scope == "main" and D.main_run_halt(consec, done, sf_total, pil["c_stop"], pil["calls_min_main"], pil["theta_main"]):
                halted = f"halt rule 13.8 after call {done}"
                break
            if done < len(plan):
                sleeper(settings["delay_between_calls_s"])
    status = "RUN_COMPLETE" if done == len(plan) and halted is None else "RUN_INCOMPLETE"
    summary = {"scope": scope, "status": status, "halt": halted, "planned_calls": len(plan), "recorded_calls": done,
               "ledger_final_hash": prev, "build_manifest_sha256": file_sha(os.path.join(build, "manifest.json")),
               "settings": settings}
    if scope.startswith("pilot"):
        summary["pilot_counts"] = SC.pilot_counts(records)           # counts only (13.7)
    with open(os.path.join(out_dir, status), "xb") as f:
        f.write(cj(summary))
    return summary


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(prog="s10_runner.py")
    ap.add_argument("--scope", required=True, choices=["pilot_round_1", "pilot_round_2", "main"])
    ap.add_argument("--build", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--evidence", required=True)
    ap.add_argument("--authorization", required=True)
    ap.add_argument("--pilot-record")
    ap.add_argument("--live", action="store_true", help="use the real provider; without it the gates are checked and the run is refused")
    a = ap.parse_args(argv)
    try:
        check_gates(a.scope, a.build, a.evidence, a.authorization, a.pilot_record)
    except GateClosed as e:
        print("GATE CLOSED:", *e.reasons, sep="\n  - ")
        return 2
    if not a.live:
        print("gates open; --live not given: nothing was run")
        return 0
    summary = run(a.scope, a.build, a.out, GeminiProvider(EXPECTED_SETTINGS["model_id"]), evidence_path=a.evidence,
                  auth_path=a.authorization, pilot_record_path=a.pilot_record)
    print(summary["status"], summary["recorded_calls"], "of", summary["planned_calls"])
    return 0 if summary["status"] == "RUN_COMPLETE" else 1


if __name__ == "__main__":
    sys.exit(main())
