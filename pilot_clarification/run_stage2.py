#!/usr/bin/env python3
"""
Stage 2 runner (implements stage2_runner_specification.md and stage2_config_specification.md).

Network access is confined to live_call() and list_models(), which import httpx lazily.
Everything else (configuration validation, order reconstruction, preflight) is offline and importable
without an API key.  Zero retries, no resume, no second live run, no circuit breaker.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import platform
import random
import re
import stat
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs"
CONFIG_PATH = HERE / "pilot_config_stage2.json"

CONFIG_KEYS = ["stage", "registry_version", "provider", "model_requested", "scenarios_expected", "repetitions",
               "planned_calls", "hard_cap_calls", "shuffle_seed", "call_order", "call_order_sha256",
               "max_output_tokens", "temperature_policy", "system_prompt", "retries", "timeout_seconds",
               "concurrency", "delay_between_calls_seconds", "api_key_env", "python_version", "bindings"]
BINDING_KEYS = ["codebook_sha256", "codebook_freeze_manifest_sha256", "registry_file_sha256",
                "registry_canonical_sha256", "prompt_specification_sha256", "stage1_registry_canonical_sha256",
                "call_order_sha256", "config_specification_sha256", "runner_specification_sha256",
                "analyzer_specification_sha256", "prompt_hashes", "runner_sha256", "analyzer_sha256"]
FROZEN_FILES = {  # binding key -> file name under HERE
    "codebook_sha256": "CODEBOOK_v2.md",
    "codebook_freeze_manifest_sha256": "CODEBOOK_v2_freeze_manifest.json",
    "registry_file_sha256": "scenario_registry_stage2_v1.json",
    "prompt_specification_sha256": "stage2_prompt_specification.md",
    "config_specification_sha256": "stage2_config_specification.md",
    "runner_specification_sha256": "stage2_runner_specification.md",
    "analyzer_specification_sha256": "stage2_analyzer_specification.md",
}
TOP_KEYS = ["registry_version", "stage", "registry_hash_method", "codebook", "stage1_registry", "design",
            "profiles", "scenarios"]
FORBID_KEY = re.compile(r"seed|timestamp|_utc|date|created|started|ended|mtime|run_id|call_index|calls_made|status", re.I)
FORBID_VAL = re.compile(r"\d{4}-\d{2}-\d{2}|\d{8}T\d{6}|(?<![\w.])\d{8}(?![\w.])")
_KEY_PATTERNS = [re.compile(r"AIza[0-9A-Za-z_\-]{20,}"), re.compile(r"sk-[A-Za-z0-9_\-]{20,}"),
                 re.compile(r"(?i)(api[_-]?key|x-api-key|authorization)\s*[:=]\s*\S+")]
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent"


# ------------------------------------------------------------------ helpers (offline)
def utc_now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_text(t):
    return sha256_bytes(t.encode("utf-8"))


def sha256_file(p):
    return sha256_bytes(Path(p).read_bytes())


def canonical_sha256(obj):
    return sha256_text(json.dumps(obj, sort_keys=True))


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


def reconstruct_order(registry, seed):
    """order = [(scenario, repetition) for scenario in registry order for repetition in 1..5]; one shuffle."""
    ids = registry["design"]["registry_order"]
    reps = registry["design"]["repetitions"]
    order = [(sid, r) for sid in ids for r in range(1, reps + 1)]
    random.Random(seed).shuffle(order)
    return order


def order_serialization(order):
    return "".join(f"{i},{sid},{rep}\n" for i, (sid, rep) in enumerate(order, start=1))


def order_sha256(order):
    return sha256_text(order_serialization(order))


# ------------------------------------------------------------------ configuration
def load_config(path=CONFIG_PATH):
    """Load and validate the frozen configuration.  Returns (cfg, problems)."""
    p = []
    cfg = json.loads(Path(path).read_text(encoding="utf-8"))
    if list(cfg.keys()) != CONFIG_KEYS and sorted(cfg.keys()) != sorted(CONFIG_KEYS):
        p.append(f"configuration keys differ from the frozen schema: {sorted(set(cfg) ^ set(CONFIG_KEYS))}")
        return cfg, p
    exact = {"stage": 2, "registry_version": "stage2-v1", "provider": "gemini", "model_requested": "gemini-3.1-flash-lite",
             "scenarios_expected": 8, "repetitions": 5, "planned_calls": 40, "hard_cap_calls": 40,
             "shuffle_seed": 20261008, "max_output_tokens": 8192,
             "temperature_policy": "provider default (temperature parameter is NOT sent)", "system_prompt": None,
             "retries": 0, "timeout_seconds": 180, "concurrency": 1, "delay_between_calls_seconds": 1.0,
             "api_key_env": {"gemini": "GEMINI_API_KEY"}, "python_version": "3.11.9"}
    for k, v in exact.items():
        if cfg.get(k) != v or type(cfg.get(k)) is not type(v):
            p.append(f"{k}: expected {v!r}, found {cfg.get(k)!r}")
    co = cfg["call_order"]
    if not (isinstance(co, list) and len(co) == 40):
        p.append("call_order must have 40 entries")
    else:
        ok_shape = all(isinstance(e, list) and len(e) == 3 for e in co)
        if not ok_shape or [e[0] for e in co] != list(range(1, 41)):
            p.append("call_order entries must be [call_index, scenario_id, repetition] with call_index 1..40")
        else:
            pairs = {(e[1], e[2]) for e in co}
            if len(pairs) != 40:
                p.append("call_order contains duplicate (scenario_id, repetition) pairs")
            ser = order_serialization([(e[1], e[2]) for e in co])
            if sha256_text(ser) != cfg["call_order_sha256"]:
                p.append("call_order_sha256 does not equal the hash of call_order")
    b = cfg["bindings"]
    if not isinstance(b, dict) or sorted(b.keys()) != sorted(BINDING_KEYS):
        p.append("bindings keys differ from the frozen schema")
    elif b["call_order_sha256"] != cfg["call_order_sha256"]:
        p.append("bindings.call_order_sha256 differs from call_order_sha256")
    return cfg, p


def post_implementation_bound(cfg):
    return bool(cfg["bindings"].get("runner_sha256")) and bool(cfg["bindings"].get("analyzer_sha256"))


# ------------------------------------------------------------------ preflight (offline)
def check_registry_state(reg):
    """Spec check 9: exactly the approved top-level keys, no mutable execution state."""
    bad = []
    if list(reg.keys()) != TOP_KEYS:
        bad.append("top-level keys differ")

    def walk(o, path=""):
        if isinstance(o, dict):
            for k, v in o.items():
                if FORBID_KEY.search(k):
                    bad.append(f"forbidden key {path}/{k}")
                walk(v, f"{path}/{k}")
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, f"{path}[{i}]")
        elif isinstance(o, str) and path != "/design/shuffle_policy" and FORBID_VAL.search(o):
            bad.append(f"date/time/seed-like value at {path}")
    walk(reg)
    return bad


def check_prior_live_runs(runs_dir, config_sha):
    """Spec check 13 / section 9: any prior live Stage 2 run with the same config and >= 1 record blocks."""
    found = []
    runs_dir = Path(runs_dir)
    if runs_dir.exists():
        for d in sorted(runs_dir.iterdir()):
            if not d.is_dir() or not d.name.startswith("stage2_"):
                continue
            mf = d / "manifest.json"
            if not mf.exists():
                continue
            try:
                m = json.loads(mf.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                found.append(f"{d.name}: unreadable manifest")
                continue
            if m.get("dry_run") is False and m.get("config_sha256") == config_sha:
                cj = d / "calls.jsonl"
                if cj.exists() and any(x.strip() for x in cj.read_text(encoding="utf-8").splitlines()):
                    found.append(d.name)
    return found


def preflight(cfg, model_arg, live, env=None, base=HERE, config_path=CONFIG_PATH, runs_dir=RUNS,
              runner_path=None, py_version=None):
    """Return list of (number, name, ok, detail).  Offline only; never prints or returns a secret."""
    base = Path(base)
    env = os.environ if env is None else env
    out = []

    def add(n, name, ok, detail=""):
        out.append((n, name, bool(ok), detail))

    b = cfg["bindings"]
    sha = lambda n: sha256_file(base / n) if (base / n).exists() else None
    add(1, "CODEBOOK_v2.md hash", sha("CODEBOOK_v2.md") == b["codebook_sha256"])
    reg_path = base / "scenario_registry_stage2_v1.json"
    reg = json.loads(reg_path.read_text(encoding="utf-8")) if reg_path.exists() else None
    add(2, "Stage 2 registry file and canonical hash",
        reg is not None and sha256_file(reg_path) == b["registry_file_sha256"]
        and canonical_sha256(reg) == b["registry_canonical_sha256"])
    add(3, "prompt specification hash", sha("stage2_prompt_specification.md") == b["prompt_specification_sha256"])
    if reg is None:
        for n in range(4, 9):
            add(n, "registry-dependent check", False, "registry missing")
        return out
    scs = reg["scenarios"]
    add(4, "exactly 8 scenarios in registry order",
        len(scs) == 8 and [s["id"] for s in scs] == reg["design"]["registry_order"])
    add(5, "each scenario has 5 repetitions", all(s["reps"] == 5 for s in scs))
    add(6, "planned calls = 40 = hard cap",
        sum(s["reps"] for s in scs) == 40 == reg["design"]["planned_calls"] == cfg["hard_cap_calls"])
    add(7, "prompt hashes recompute and equal bindings",
        all(sha256_text(s["prompt"]) == s["prompt_sha256"] == b["prompt_hashes"].get(s["id"]) for s in scs)
        and sorted(b["prompt_hashes"]) == sorted(s["id"] for s in scs))
    s1p = base / "scenario_registry.json"
    ok8 = s1p.exists() and canonical_sha256(json.loads(s1p.read_text(encoding="utf-8"))) == b["stage1_registry_canonical_sha256"]
    if ok8:
        s1 = {s["id"]: s for s in json.loads(s1p.read_text(encoding="utf-8"))}
        for s in scs:
            if s["stage1_source"]["relation"] == "byte_identical":
                src = s1.get(s["stage1_source"]["id"])
                ok8 = ok8 and src is not None and src["prompt"] == s["prompt"] \
                    and src["prompt_sha256"] == s["stage1_source"]["prompt_sha256"] == s["prompt_sha256"]
    add(8, "reused Stage 1 prompts byte-identical", ok8)
    bad = check_registry_state(reg)
    add(9, "registry has no mutable execution state", not bad, "; ".join(bad[:3]))
    add(10, "model ID equals configuration", model_arg == cfg["model_requested"])
    if live:
        key = env.get(cfg["api_key_env"]["gemini"])
        add(11, "API key environment variable present", bool(key))  # value never printed
    else:
        add(11, "API key check (skipped: not a live run)", True)
    order = reconstruct_order(reg, cfg["shuffle_seed"])
    stored = [(e[1], e[2]) for e in cfg["call_order"]]
    add(12, "reconstructed order equals stored order and hash",
        order == stored and order_sha256(order) == cfg["call_order_sha256"] == b["call_order_sha256"])
    csha = sha256_file(config_path)
    prior = check_prior_live_runs(runs_dir, csha) if live else []
    add(13, "no existing live Stage 2 run for this configuration", not prior, ", ".join(prior))
    _, problems = load_config(config_path)
    pv = py_version or platform.python_version()
    add(14, "configuration valid and Python version bound", not problems and pv == cfg["python_version"],
        "; ".join(problems[:3]))
    ok15 = sha("CODEBOOK_v2_freeze_manifest.json") == b["codebook_freeze_manifest_sha256"] \
        and ok8 or False
    for k, f in FROZEN_FILES.items():
        if k in ("codebook_sha256", "registry_file_sha256", "prompt_specification_sha256"):
            continue
        ok15 = ok15 and sha(f) == b[k]
    rp = Path(runner_path) if runner_path else Path(__file__).resolve()
    ap = base / "analyze_stage2.py"
    if live:
        ok15 = ok15 and post_implementation_bound(cfg) and sha256_file(rp) == b["runner_sha256"] \
            and ap.exists() and sha256_file(ap) == b["analyzer_sha256"]
    else:
        if b.get("runner_sha256"):
            ok15 = ok15 and sha256_file(rp) == b["runner_sha256"]
        if b.get("analyzer_sha256") and ap.exists():
            ok15 = ok15 and sha256_file(ap) == b["analyzer_sha256"]
    add(15, "bound hashes (manifest, specs, Stage 1, runner, analyzer)", ok15)
    add(16, "target run directory does not exist", True, "checked again at creation (exclusive)")
    return out


# ------------------------------------------------------------------ provider layer (the ONLY network code)
def build_request(model, prompt, key, max_tokens):
    m = model[len("models/"):] if model.startswith("models/") else model
    return ("POST", ENDPOINT.format(m=m), {"x-goog-api-key": key, "content-type": "application/json"},
            {"contents": [{"role": "user", "parts": [{"text": prompt}]}],
             "generationConfig": {"maxOutputTokens": max_tokens}})


def extract_gemini(j):
    cands = j.get("candidates") or []
    if not cands:
        return "", None, j.get("usageMetadata"), j.get("modelVersion"), \
            "no candidates; promptFeedback=" + json.dumps(j.get("promptFeedback"))[:500]
    c = cands[0]
    parts = (c.get("content") or {}).get("parts") or []
    text = "".join(p.get("text", "") for p in parts if not p.get("thought"))
    return text, c.get("finishReason"), j.get("usageMetadata"), j.get("modelVersion"), None


def live_call(client, model, prompt, key, cfg, red):
    method, url, headers, body = build_request(model, prompt, key, cfg["max_output_tokens"])
    rec = dict(http_status=None, response_text="", finish_reason=None, usage=None, model_returned=None,
               response_json=None, error=None, outcome="exception")
    t0 = time.perf_counter()
    try:
        r = client.request(method, url, headers=headers, json=body)
        rec["http_status"] = r.status_code
        if r.status_code != 200:
            rec["error"] = red(f"HTTP {r.status_code}: {r.text[:2000]}")
            rec["outcome"] = "http_error"
        else:
            j = r.json()
            rec["response_json"] = j
            text, fr, usage, mr, err = extract_gemini(j)
            rec.update(response_text=text, finish_reason=fr, usage=usage, model_returned=mr, error=err)
            rec["outcome"] = "no_candidates" if err else "ok"
    except Exception as e:  # network, timeout, JSON: recorded, never retried
        rec["error"] = red(f"{type(e).__name__}: {e}")
    rec["latency_ms"] = int((time.perf_counter() - t0) * 1000)
    return rec


def list_models(cfg):
    import httpx  # audit-only mode; one metadata request
    key = os.environ.get(cfg["api_key_env"]["gemini"])
    if not key:
        sys.exit("GEMINI_API_KEY is not set.")
    red = make_redactor(key)
    r = httpx.get("https://generativelanguage.googleapis.com/v1beta/models?pageSize=200",
                  headers={"x-goog-api-key": key}, timeout=60)
    if r.status_code != 200:
        sys.exit(red(f"HTTP {r.status_code}: {r.text[:500]}"))
    for m in r.json().get("models") or []:
        if "generateContent" in (m.get("supportedGenerationMethods") or ["generateContent"]):
            print(m.get("name"))


def mock_call(s, rep):
    return dict(http_status=200, response_text="| Week | Total km |\n|---|---|\n| 1 | 1.0 |", finish_reason="STOP",
                usage={"mock": True}, model_returned="mock-model", response_json={"mock": True}, error=None,
                outcome="ok", latency_ms=0)


# ------------------------------------------------------------------ run bookkeeping
def reconcile(records, order):
    """Return a list of problems; empty means the run reconciles."""
    pr = []
    if len(records) != 40:
        pr.append(f"{len(records)} terminal records, expected 40")
    seen_idx, seen_pair = set(), set()
    for r in records:
        i = r.get("call_index")
        if i in seen_idx:
            pr.append(f"duplicate call_index {i}")
        seen_idx.add(i)
        pair = (r.get("scenario_id"), r.get("repetition"))
        if pair in seen_pair:
            pr.append(f"duplicate pair {pair}")
        seen_pair.add(pair)
        if isinstance(i, int) and 1 <= i <= len(order) and order[i - 1] != pair:
            pr.append(f"record {i} does not match stored order")
        if r.get("outcome") not in ("ok", "http_error", "no_candidates", "exception"):
            pr.append(f"record {i} has no terminal outcome")
    missing = set(order) - seen_pair
    if missing:
        pr.append(f"missing pairs: {sorted(missing)[:5]}")
    return pr


def write_exclusive(path, data):
    mode = "xb" if isinstance(data, bytes) else "x"
    kw = {} if isinstance(data, bytes) else {"encoding": "utf-8", "newline": "\n"}
    with open(path, mode, **kw) as f:
        f.write(data)


def set_readonly(paths):
    ok = True
    for p in paths:
        try:
            os.chmod(p, stat.S_IREAD)
        except OSError:
            ok = False
    return ok


def main():
    ap = argparse.ArgumentParser(description="Stage 2 runner (40 calls, no retries, no resume)")
    ap.add_argument("--provider", choices=["gemini"])
    ap.add_argument("--model")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--list-models", action="store_true")
    args = ap.parse_args()
    cfg, problems = load_config()
    if problems:
        sys.exit("CONFIG REJECTED:\n  - " + "\n  - ".join(problems))
    if args.list_models:
        list_models(cfg)
        return
    live = not args.dry_run
    if live and (args.provider != "gemini" or not args.model):
        sys.exit("A live run needs --provider gemini and --model (exact ID).")
    model = args.model or "mock-model"
    if args.dry_run:
        model = cfg["model_requested"] if not args.model else args.model
    results = preflight(cfg, model, live)
    failed = [r for r in results if not r[2]]
    if failed:
        print("PREFLIGHT FAILED (nothing created, nothing called):")
        for n, name, _, d in failed:
            print(f"  [{n}] {name} {d}")
        sys.exit(1)

    reg_bytes = (HERE / "scenario_registry_stage2_v1.json").read_bytes()
    reg = json.loads(reg_bytes.decode("utf-8"))
    sc = {s["id"]: s for s in reg["scenarios"]}
    order = [(e[1], e[2]) for e in cfg["call_order"]]
    key = os.environ.get(cfg["api_key_env"]["gemini"]) if live else None
    red = make_redactor(key)
    print("=" * 70)
    print("STAGE 2 EXPERIMENT" + (" (DRY RUN, mock provider)" if not live else ""))
    print(f"  model: {model} | calls: {len(order)} | retries 0 | seed {cfg['shuffle_seed']}")
    print("=" * 70)
    if live and input('Type exactly "RUN 40" to start the 40 live calls: ').strip() != "RUN 40":
        sys.exit("Aborted. Nothing was called.")

    run_id = ("dryrun_" if not live else "") + "stage2_" + ("gemini" if live else "mock") + "_" + \
        dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = RUNS / run_id
    (run_dir / "raw").mkdir(parents=True, exist_ok=False)
    (run_dir / "integrity").mkdir()
    config_bytes = CONFIG_PATH.read_bytes()
    config_sha = sha256_bytes(config_bytes)
    b = cfg["bindings"]
    settings = dict(max_output_tokens=cfg["max_output_tokens"], temperature=cfg["temperature_policy"],
                    system_prompt=None, retries=0, timeout_seconds=cfg["timeout_seconds"],
                    delay_between_calls_seconds=cfg["delay_between_calls_seconds"])
    manifest = dict(run_id=run_id, stage=2, dry_run=not live, provider="gemini" if live else "mock",
                    model_requested=model, registry_version=cfg["registry_version"], planned_calls=40, repetitions=5,
                    scenarios=8, shuffle_seed=cfg["shuffle_seed"], call_order_sha256=cfg["call_order_sha256"],
                    settings=settings, bindings=b, config_sha256=config_sha,
                    runner_sha256=sha256_file(Path(__file__).resolve()), python_version=platform.python_version(),
                    platform=platform.platform(), started_utc=utc_now())
    if live:
        import httpx
        manifest["httpx_version"] = httpx.__version__
    write_exclusive(run_dir / "manifest.json", json.dumps(manifest, indent=2, ensure_ascii=False))
    write_exclusive(run_dir / "config_used.json", config_bytes)
    write_exclusive(run_dir / "scenario_registry.json", reg_bytes)
    write_exclusive(run_dir / "integrity" / "preflight.json", json.dumps(
        [dict(id=n, name=name, passed=ok, detail=d) for n, name, ok, d in results], indent=2))
    write_exclusive(run_dir / "integrity" / "call_order.csv", order_serialization(order))

    client = None
    if live:
        import httpx
        client = httpx.Client(timeout=cfg["timeout_seconds"])
    records, status, reason = [], "COMPLETE", ""
    try:
        with open(run_dir / "calls.jsonl", "x", encoding="utf-8", newline="\n") as jf:
            for idx, (sid, rep) in enumerate(order, start=1):
                s = sc[sid]
                if len(records) >= 40 or (sid, rep) != (cfg["call_order"][idx - 1][1], cfg["call_order"][idx - 1][2]) \
                        or sha256_text(s["prompt"]) != s["prompt_sha256"] \
                        or (run_dir / "raw" / f"{idx:02d}_{sid}_r{rep}.json").exists():
                    status, reason = "ABORTED_INTEGRITY", f"loop invariant failed at call {idx}"
                    break
                started = utc_now()
                rec = live_call(client, model, s["prompt"], key, cfg, red) if live else mock_call(s, rep)
                fr = str(rec.get("finish_reason") or "").lower()
                record = dict(
                    call_index=idx, scenario_id=sid, scenario_number=s["number"], repetition=rep, run_id=run_id,
                    provider=manifest["provider"], model_requested=model, model_returned=rec.get("model_returned"),
                    timestamp_utc=started, completed_utc=utc_now(), prompt_sha256=s["prompt_sha256"],
                    prompt=s["prompt"], http_status=rec.get("http_status"), response_text=rec.get("response_text", ""),
                    response_text_sha256=sha256_text(rec.get("response_text", "") or ""),
                    response_json=rec.get("response_json"), finish_reason=rec.get("finish_reason"),
                    truncated=fr in ("max_tokens", "length", "max_output_tokens"), usage=rec.get("usage"),
                    latency_ms=rec.get("latency_ms", 0), outcome=rec["outcome"], error=rec.get("error"),
                    settings=settings, registry_version=cfg["registry_version"], config_sha256=config_sha,
                    registry_file_sha256=b["registry_file_sha256"], codebook_sha256=b["codebook_sha256"])
                try:
                    write_exclusive(run_dir / "raw" / f"{idx:02d}_{sid}_r{rep}.json",
                                    json.dumps(record, indent=2, ensure_ascii=False))
                    jf.write(json.dumps(record, ensure_ascii=False) + "\n")
                    jf.flush()
                    os.fsync(jf.fileno())
                except OSError as e:
                    status, reason = "ABORTED_INTEGRITY", f"write failure at call {idx}: {type(e).__name__}"
                    break
                records.append(record)
                print(f"[{idx:02d}/40] {sid:<11} rep{rep}  {record['outcome']}")
                if live:
                    time.sleep(cfg["delay_between_calls_seconds"])
    except KeyboardInterrupt:
        status, reason = "ABORTED_OPERATOR", "operator interrupt"
    problems = reconcile(records, order)
    if status == "COMPLETE" and problems:
        status, reason = "ABORTED_INTEGRITY", "; ".join(problems[:3])

    ro_targets = [p for p in (run_dir / "raw").glob("*.json")] + \
        [run_dir / n for n in ("calls.jsonl", "manifest.json", "config_used.json", "scenario_registry.json")] + \
        list((run_dir / "integrity").glob("*"))
    readonly_applied = set_readonly([p for p in ro_targets if p.exists()])
    file_hashes = {str(p.relative_to(run_dir).as_posix()): sha256_file(p)
                   for p in sorted(run_dir.rglob("*")) if p.is_file() and p.name not in ("postrun.json", "STAGE2_COMPLETE")}
    from collections import Counter
    postrun = dict(status=status, reason=reason, calls_attempted=len(records), calls_terminal=len(records),
                   outcome_counts=dict(Counter(r["outcome"] for r in records)),
                   finish_reason_counts=dict(Counter(str(r["finish_reason"]) for r in records)),
                   truncated_count=sum(1 for r in records if r["truncated"]),
                   models_returned=sorted({r["model_returned"] for r in records if r["model_returned"]}),
                   reconciliation_problems=problems, file_hashes=file_hashes,
                   readonly_applied=readonly_applied, ended_utc=utc_now())
    pj = run_dir / "integrity" / "postrun.json"
    write_exclusive(pj, json.dumps(postrun, indent=2, ensure_ascii=False))
    if status == "COMPLETE" and live:
        write_exclusive(run_dir / "STAGE2_COMPLETE", f"{utc_now()}\n{sha256_file(pj)}\n")  # written LAST
        set_readonly([pj, run_dir / "STAGE2_COMPLETE"])
    print(f"DONE: status {status} {reason}. Calls recorded: {len(records)}")


if __name__ == "__main__":
    main()
