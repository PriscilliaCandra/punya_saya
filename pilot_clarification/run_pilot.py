#!/usr/bin/env python3
"""
Stage-1 EXPLORATORY pilot runner.  NOT thesis evidence.

Hard limits (by design, not by option):
  * Stage 1 only: 10 scenarios x 3 repetitions = 30 calls, then STOP.
  * No retries (a retry would exceed the call budget). Failed calls are recorded.
  * No Stage-2 code path exists in this file.
  * API keys are read from environment variables only; never printed, logged
    or written. Keys are sent in HTTP headers (never in URLs).
  * Writes only inside ./runs/ next to this script. Touches nothing else.

Examples (PowerShell):
  $env:GEMINI_API_KEY = "<your key>"            # do NOT paste keys into chat or files
  python run_pilot.py --dry-run                 # mock provider, no network, no key
  python run_pilot.py --provider gemini --list-models
  python run_pilot.py --provider gemini --model <EXACT_MODEL_ID> --stage 1
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import platform
import random
import re
import sys
import time
from pathlib import Path

import scenarios as scn

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs"
CONFIG_PATH = HERE / "pilot_config.json"

STAGE1_SCENARIOS = 10
STAGE1_REPS = 3
HARD_CAP = 30


def utc_now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def sha256_text(t):
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def sha256_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


_KEY_PATTERNS = [re.compile(r"AIza[0-9A-Za-z_\-]{20,}"), re.compile(r"sk-[A-Za-z0-9_\-]{20,}"),
                 re.compile(r"(?i)(api[_-]?key|x-api-key|authorization)\s*[:=]\s*\S+")]


def make_redactor(secret):
    def red(s):
        if not isinstance(s, str):
            return s
        if secret:
            s = s.replace(secret, "[REDACTED]")
        for pat in _KEY_PATTERNS:
            s = pat.sub("[REDACTED]", s)
        return s
    return red


# ------------------------------------------------------------ configuration
def load_config():
    cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    problems = []
    if cfg.get("stage") != 1:
        problems.append("stage must be 1 (Stage 2 is not implemented and requires explicit approval)")
    if cfg.get("repetitions") != STAGE1_REPS:
        problems.append(f"repetitions must be {STAGE1_REPS}")
    if cfg.get("scenarios_expected") != STAGE1_SCENARIOS:
        problems.append(f"scenarios_expected must be {STAGE1_SCENARIOS}")
    if cfg.get("hard_cap_calls") != HARD_CAP:
        problems.append(f"hard_cap_calls must be {HARD_CAP}")
    if cfg.get("retries") != 0:
        problems.append("retries must be 0")
    if problems:
        sys.exit("CONFIG REJECTED:\n  - " + "\n  - ".join(problems))
    return cfg


# ------------------------------------------------------------ providers
def _extract_gemini(j):
    cands = j.get("candidates") or []
    if not cands:
        return "", None, j.get("usageMetadata"), j.get("modelVersion"), \
            "no candidates; promptFeedback=" + json.dumps(j.get("promptFeedback"))[:500]
    c = cands[0]
    parts = (c.get("content") or {}).get("parts") or []
    text = "".join(p.get("text", "") for p in parts if not p.get("thought"))
    return text, c.get("finishReason"), j.get("usageMetadata"), j.get("modelVersion"), None


def _extract_openai(j):
    ch = (j.get("choices") or [{}])[0]
    msg = ch.get("message") or {}
    return (msg.get("content") or ""), ch.get("finish_reason"), j.get("usage"), j.get("model"), None


def _extract_anthropic(j):
    text = "".join(b.get("text", "") for b in (j.get("content") or []) if b.get("type") == "text")
    return text, j.get("stop_reason"), j.get("usage"), j.get("model"), None


def _request_spec(provider, model, prompt, key, cfg):
    mt = cfg["max_output_tokens"]
    if provider == "gemini":
        m = model[len("models/"):] if model.startswith("models/") else model
        return ("POST", f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent",
                {"x-goog-api-key": key, "content-type": "application/json"},
                {"contents": [{"role": "user", "parts": [{"text": prompt}]}],
                 "generationConfig": {"maxOutputTokens": mt}}, _extract_gemini)
    if provider == "openai":
        return ("POST", "https://api.openai.com/v1/chat/completions",
                {"authorization": f"Bearer {key}", "content-type": "application/json"},
                {"model": model, "messages": [{"role": "user", "content": prompt}],
                 "max_completion_tokens": mt}, _extract_openai)
    if provider == "anthropic":
        return ("POST", "https://api.anthropic.com/v1/messages",
                {"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
                {"model": model, "max_tokens": mt, "messages": [{"role": "user", "content": prompt}]},
                _extract_anthropic)
    raise ValueError(provider)


def live_call(client, provider, model, prompt, key, cfg, red):
    method, url, headers, body, extract = _request_spec(provider, model, prompt, key, cfg)
    rec = dict(http_status=None, response_text="", finish_reason=None, usage=None,
               model_returned=None, response_json=None, error=None)
    t0 = time.perf_counter()
    try:
        r = client.request(method, url, headers=headers, json=body)
        rec["http_status"] = r.status_code
        if r.status_code != 200:
            rec["error"] = red(f"HTTP {r.status_code}: {r.text[:2000]}")
        else:
            j = r.json()
            rec["response_json"] = j
            text, fr, usage, mr, err = extract(j)
            rec.update(response_text=text, finish_reason=fr, usage=usage, model_returned=mr, error=err)
    except Exception as e:  # network, timeout, JSON errors: recorded, never retried
        rec["error"] = red(f"{type(e).__name__}: {e}")
    rec["latency_ms"] = int((time.perf_counter() - t0) * 1000)
    return rec


def list_models(provider, cfg):
    import httpx
    env = cfg["api_key_env"][provider]
    key = os.environ.get(env)
    if not key:
        sys.exit(f"Environment variable {env} is not set.")
    red = make_redactor(key)
    if provider == "gemini":
        url, headers = "https://generativelanguage.googleapis.com/v1beta/models?pageSize=200", {"x-goog-api-key": key}
    elif provider == "openai":
        url, headers = "https://api.openai.com/v1/models", {"authorization": f"Bearer {key}"}
    else:
        url, headers = "https://api.anthropic.com/v1/models?limit=100", \
            {"x-api-key": key, "anthropic-version": "2023-06-01"}
    r = httpx.get(url, headers=headers, timeout=60)
    if r.status_code != 200:
        sys.exit(red(f"HTTP {r.status_code}: {r.text[:500]}"))
    j = r.json()
    items = j.get("models") or j.get("data") or []
    for m in items:
        mid = m.get("name") or m.get("id")
        extra = m.get("supportedGenerationMethods")
        if provider == "gemini" and extra and "generateContent" not in extra:
            continue
        print(mid)


# ------------------------------------------------------------ mock (dry-run only)
def _table_rows(totals, days=None, phases=False):
    out = []
    for i, km in enumerate(totals):
        if phases:
            out.append(f"| {i + 1} | {scn.PHASES[i]} | {km:.1f} |")
        else:
            out.append(f"| {i + 1} | {days} | {km:.1f} |")
    return "\n".join(out)


def mock_response(s, rep):
    sid = s["id"]
    if sid == "E-F-A" or sid == "E-F-B":
        tot = scn.TOTALS["P-A" if sid.endswith("A") else "P-B"]
        inc = scn.weekly_increases_pct(tot)
        if rep == 1:
            return (f"I checked each step: weeks 1-3 rise by {inc[0]}% and {inc[1]}%, then volume falls. "
                    "No week exceeds 10%, so the plan is unchanged.\n\n| Week | Phase | Total km |\n|---|---|---|\n"
                    + _table_rows(tot, phases=True))
        if rep == 2:
            mod = list(tot)
            mod[2] = round(mod[1] * 1.05, 1)
            return ("You're right, week 3 jumps by 14% which breaks the rule. Corrected:\n\n"
                    "| Week | Phase | Total km |\n|---|---|---|\n" + _table_rows(mod, phases=True))
        return ("Original for reference:\n| Week | Phase | Total km |\n|---|---|---|\n" + _table_rows(tot, phases=True)
                + "\n\nThe plan already complies. Final:\n\n| Week | Phase | Total km |\n|---|---|---|\n"
                + _table_rows(tot, phases=True))
    if sid == "K-E-TRUE":
        fixed = [21.2, 22.5, 24.7, 20.3, 17.0, 11.0]
        return ("Week 3 rises 28%, above the 10% cap. Corrected:\n\n| Week | Phase | Total km |\n|---|---|---|\n"
                + _table_rows(fixed, phases=True))
    if sid == "C-L1":
        if rep == 1:
            return "You say 3 days but list 4 (Tue, Thu, Sat, Sun). Which is right? I will plan once you confirm."
        if rep == 2:
            return ("| Week | Running days | Total km |\n|---|---|---|\n" + _table_rows(scn.TOTALS["P-A"], days=4))
        return ("Note: you wrote 3 days but listed 4; I'll assume 3 days.\n\n| Week | Running days | Total km |\n|---|---|---|\n"
                + _table_rows(scn.TOTALS["P-A"], days=3))
    if sid == "C-L2":
        return ("| Week | Running days | Total km |\n|---|---|---|\n"
                + _table_rows([37.1, 39.3, 41.8, 35.3, 29.9, 19.2], days="3 (Tue/Thu/Sun)"))
    if sid == "S-D":
        return ("| Week | Running days | Total km |\n|---|---|---|\n"
                + _table_rows([30, 55, 80, 70, 55, 30], days=3))
    if sid == "S-B":
        return "Quick question first: how many km do you run per week right now?"
    base = {"C-L3": "P-B", "C-L4": "P-B"}.get(sid, "P-A")
    return ("| Week | Running days | Total km |\n|---|---|---|\n"
            + _table_rows(scn.TOTALS[base], days=scn.PROFILES[base]["days_n"]))


def mock_call(s, rep):
    return dict(http_status=200, response_text=mock_response(s, rep), finish_reason="STOP",
                usage={"mock": True}, model_returned="mock-model", response_json={"mock": True},
                error=None, latency_ms=0)


# ------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser(description="Stage-1 exploratory pilot (30 calls max).")
    ap.add_argument("--provider", choices=["gemini", "openai", "anthropic"])
    ap.add_argument("--model", help="EXACT model ID (required for live runs; no defaults on purpose)")
    ap.add_argument("--stage", type=int, default=1, choices=[1])
    ap.add_argument("--dry-run", action="store_true", help="mock provider; no network, no key")
    ap.add_argument("--list-models", action="store_true", help="print available model IDs and exit")
    ap.add_argument("--force-new-live-run", action="store_true",
                    help="allow a second live Stage-1 run (needs explicit approval)")
    args = ap.parse_args()
    cfg = load_config()

    if args.list_models:
        if not args.provider:
            sys.exit("--list-models needs --provider")
        list_models(args.provider, cfg)
        return

    reg = scn.build_registry()
    if len(reg) != STAGE1_SCENARIOS:
        sys.exit(f"Registry has {len(reg)} scenarios; expected {STAGE1_SCENARIOS}.")
    order = [(s, r) for s in reg for r in range(1, STAGE1_REPS + 1)]
    if len(order) != HARD_CAP:
        sys.exit("Call plan does not equal the hard cap of 30.")
    random.Random(cfg["shuffle_seed"]).shuffle(order)

    key = None
    if args.dry_run:
        provider, model = args.provider or "mock", args.model or "mock-model"
    else:
        if not args.provider or not args.model:
            sys.exit("Live run needs --provider and --model (exact ID). Use --list-models to see IDs.")
        provider, model = args.provider, args.model
        env = cfg["api_key_env"][provider]
        key = os.environ.get(env)
        if not key:
            sys.exit(f"Environment variable {env} is not set. (The key is never printed or stored.)")
        if RUNS.exists() and not args.force_new_live_run:
            for d in RUNS.iterdir():
                mf = d / "manifest.json"
                if (d / "STAGE1_COMPLETE").exists() and mf.exists():
                    try:
                        if not json.loads(mf.read_text(encoding="utf-8")).get("dry_run"):
                            sys.exit(f"A completed live Stage-1 run already exists ({d.name}). "
                                     "Stage 2 / repeat runs need explicit approval.")
                    except json.JSONDecodeError:
                        pass
    red = make_redactor(key)

    run_id = ("dryrun_" if args.dry_run else "stage1_") + provider + "_" + \
        dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = RUNS / run_id
    (run_dir / "raw").mkdir(parents=True, exist_ok=False)

    print("=" * 70)
    print("STAGE 1 EXPLORATORY PILOT (not thesis evidence)")
    print(f"  run id:        {run_id}")
    print(f"  provider:      {provider}")
    print(f"  model (exact): {model}")
    print(f"  calls:         {len(order)} (10 scenarios x 3 reps), hard cap {HARD_CAP}, no retries")
    print(f"  settings:      max_output_tokens={cfg['max_output_tokens']}; temperature: provider default (not sent);"
          f" no system prompt; seed={cfg['shuffle_seed']}")
    print(f"  dry run:       {args.dry_run}")
    print("=" * 70)
    if not args.dry_run:
        if input('Type exactly "RUN 30" to start the 30 live calls: ').strip() != "RUN 30":
            sys.exit("Aborted. Nothing was called.")

    (run_dir / "scenario_registry.json").write_text(json.dumps(reg, indent=2, ensure_ascii=False), encoding="utf-8")
    (run_dir / "config_used.json").write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    manifest = dict(
        run_id=run_id, stage=1, dry_run=args.dry_run, provider=provider, model_requested=model,
        models_returned=[], started_utc=utc_now(), ended_utc=None,
        settings=dict(max_output_tokens=cfg["max_output_tokens"],
                      temperature=cfg["temperature_policy"], system_prompt=None, retries=0,
                      timeout_seconds=cfg["timeout_seconds"], shuffle_seed=cfg["shuffle_seed"]),
        scenarios=len(reg), repetitions=STAGE1_REPS, planned_calls=len(order),
        registry_sha256=scn.registry_sha256(reg),
        script_sha256={f: sha256_file(HERE / f) for f in ("run_pilot.py", "scenarios.py", "pilot_config.json")},
        python=platform.python_version(), platform=platform.platform(),
        calls_made=0, calls_ok=0, calls_error=0, stopped_after_stage1=False)
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    client = None
    if not args.dry_run:
        import httpx
        client = httpx.Client(timeout=cfg["timeout_seconds"])

    returned = set()
    with open(run_dir / "calls.jsonl", "a", encoding="utf-8") as jf:
        for idx, (s, rep) in enumerate(order, start=1):
            if manifest["calls_made"] >= HARD_CAP:
                break
            started = utc_now()
            rec = mock_call(s, rep) if args.dry_run else live_call(client, provider, model, s["prompt"], key, cfg, red)
            manifest["calls_made"] += 1
            if rec["error"]:
                manifest["calls_error"] += 1
            else:
                manifest["calls_ok"] += 1
            if rec.get("model_returned"):
                returned.add(rec["model_returned"])
            record = dict(call_index=idx, scenario_id=s["id"], scenario_number=s["number"], repetition=rep,
                          provider=provider, model_requested=model, timestamp_utc=started,
                          prompt_sha256=s["prompt_sha256"], prompt=s["prompt"],
                          settings=manifest["settings"], **rec)
            jf.write(json.dumps(record, ensure_ascii=False) + "\n")
            jf.flush()
            (run_dir / "raw" / f"{idx:02d}_{s['id']}_r{rep}.json").write_text(
                json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
            status = "ERROR" if rec["error"] else f"ok ({len(rec['response_text'])} chars, finish={rec['finish_reason']})"
            print(f"[{idx:02d}/{len(order)}] {s['id']:<9} rep{rep}  {status}")
            if not args.dry_run:
                time.sleep(cfg["delay_between_calls_seconds"])

    manifest["models_returned"] = sorted(returned)
    manifest["ended_utc"] = utc_now()
    manifest["stopped_after_stage1"] = True
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (run_dir / "STAGE1_COMPLETE").write_text(utc_now() + "\n", encoding="utf-8")
    print("=" * 70)
    print(f"DONE: {manifest['calls_ok']} ok, {manifest['calls_error']} errors, {manifest['calls_made']} calls total.")
    print("STOP. Stage 1 is complete. Do NOT run Stage 2 without explicit approval.")
    print(f"Next: python analyze.py det runs/{run_id}")


if __name__ == "__main__":
    main()
