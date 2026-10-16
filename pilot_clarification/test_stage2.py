"""
Offline tests for the Stage 2 runner, configuration and analyzer.

No test needs GEMINI_API_KEY, opens a socket, or calls the runner's provider code.  All synthetic runs are built
in temporary directories (never in the repository).  Run from this folder:

    python -B -m unittest test_stage2 -v
"""
import ast
import copy
import csv
import hashlib
import json
import os
import random
import shutil
import sys
import tempfile
import unittest
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import analyze_stage2 as az
import run_stage2 as rn

HERE = Path(__file__).resolve().parent
REG = json.loads((HERE / "scenario_registry_stage2_v1.json").read_text(encoding="utf-8"))
SC = {s["id"]: s for s in REG["scenarios"]}
CFG, _CFG_PROBLEMS = rn.load_config()
EXPECTED_ORDER_SHA = "8b98a43e72f7ab243e1ce21a7a18f908286a0b5fcbf2429c06621570e7e30e81"
D = Decimal


# ------------------------------------------------------------------ synthetic run builder (temp dirs only)
def table(totals, pace=None, header=None):
    if pace is None:
        h = header or "| Week | Total km |"
        lines = [h, "|---|---|"] + [f"| {w} | {t} |" for w, t in enumerate(totals, 1)]
    else:
        h = header or "| Week | Total km | Target race pace (min/km) |"
        lines = [h, "|---|---|---|"] + [f"| {w} | {t} | {pace[w - 1]} |" for w, t in enumerate(totals, 1)]
    return "Here is the plan.\n\n" + "\n".join(lines) + "\n"


def default_text(sid):
    inputs = list(SC[sid]["reference"].get("input_totals", []))
    if sid in ("E-F-A", "E-F-B"):
        return table(inputs)
    if sid == "K-E-TRUE":
        return table([21.2, 22.5, 23.4, 20.3, 17.0, 11.0])
    if sid == "K-E-TRUE-B":
        return table([58.3, 61.8, 65.4, 55.7, 46.8, 30.2])
    if sid == "C-L2":
        return table([20.0, 22.0, 24.0, 20.0, 17.0, 12.0])
    if sid == "C-L3":
        return table([55.0, 58.0, 60.0, 50.0, 45.0, 30.0])
    paces = ["5:30", "5:25", "5:20", "5:10", "5:00", "4:16"]
    return table([55.0, 58.0, 60.0, 50.0, 45.0, 30.0], pace=paces)


def build_run(tmp, texts=None, mutate=None):
    """Create a complete synthetic Stage 2 run directory under tmp; returns its path."""
    texts = texts or {}
    run = Path(tmp) / "runs" / "stage2_gemini_20260101T000000Z"
    (run / "raw").mkdir(parents=True)
    (run / "integrity").mkdir()
    cfg_bytes = (HERE / "pilot_config_stage2.json").read_bytes()
    (run / "config_used.json").write_bytes(cfg_bytes)
    (run / "scenario_registry.json").write_bytes((HERE / "scenario_registry_stage2_v1.json").read_bytes())
    manifest = {"run_id": run.name, "dry_run": False, "model_requested": az.MODEL,
                "config_sha256": hashlib.sha256(cfg_bytes).hexdigest()}
    (run / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    (run / "integrity" / "call_order.csv").write_text(rn.order_serialization(
        [(e[1], e[2]) for e in CFG["call_order"]]), encoding="utf-8")
    recs = []
    for idx, sid, rep in CFG["call_order"]:
        s = SC[sid]
        text = texts.get((sid, rep), default_text(sid))
        recs.append({"call_index": idx, "scenario_id": sid, "repetition": rep, "outcome": "ok", "http_status": 200,
                     "finish_reason": "STOP", "truncated": False, "model_returned": az.MODEL, "response_text": text,
                     "prompt": s["prompt"], "prompt_sha256": s["prompt_sha256"], "error": None})
    if mutate:
        mutate(recs)
    with open(run / "calls.jsonl", "w", encoding="utf-8", newline="\n") as f:
        for r in recs:
            f.write(json.dumps(r) + "\n")
            (run / "raw" / f"{r['call_index']:02d}_{r['scenario_id']}_r{r['repetition']}.json").write_text(
                json.dumps(r, indent=2), encoding="utf-8")
    finalize(run)
    return run


def finalize(run):
    hashes = {str(p.relative_to(run).as_posix()): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(run.rglob("*")) if p.is_file() and p.name not in ("postrun.json", "STAGE2_COMPLETE")}
    pj = run / "integrity" / "postrun.json"
    pj.write_text(json.dumps({"status": "COMPLETE", "file_hashes": hashes}), encoding="utf-8")
    (run / "STAGE2_COMPLETE").write_text("2026-01-01T00:00:00+00:00\n" + hashlib.sha256(pj.read_bytes()).hexdigest() + "\n")


def fill_sheet(run, spec, out_name="coding_sheet_filled.csv", edit=None):
    """spec: (scenario, repetition) -> (code, notes).  Missing entries get the clean default."""
    key = {}
    with open(run / "analysis" / "coding_key.csv", encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            key[r["blind_id"]] = (r["scenario_id"], int(r["repetition"]))
    with open(run / "analysis" / "coding_sheet_blank.csv", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    defaults = {"E-F-A": ("E1", "v=N;c=Y"), "E-F-B": ("E1", "v=N;c=Y"), "K-E-TRUE": ("T1", ""),
                "K-E-TRUE-B": ("T1", ""), "C-L2": ("C1", ""), "C-L3": ("C1", ""), "C-L4-S2": ("C1", ""),
                "K-C-L4-S2": ("U_ok", "pace_matches_stated=Y")}
    for r in rows:
        sid, rep = key[r["blind_id"]]
        code, notes = spec.get((sid, rep), defaults[sid])
        r["code"], r["notes"] = code, notes
    if edit:
        edit(rows)
    out = run / out_name
    with open(out, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=az.COLS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    return out


class Tmp(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="stage2_test_")
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def prepared(self, texts=None, mutate=None):
        run = build_run(tempfile.mkdtemp(dir=self.tmp), texts, mutate)
        status, integ = az.prepare(run)
        self.assertEqual(status, "OK", integ["blocked"])
        return run

    def summarize(self, run, spec=None, **kw):
        coded = fill_sheet(run, spec or {}, **kw)
        return az.summarize(run, coded)


# ------------------------------------------------------------------ configuration and runner
class TestConfig(unittest.TestCase):
    def test_loads_without_problems(self):
        self.assertEqual(_CFG_PROBLEMS, [])

    def test_frozen_values(self):
        c = CFG
        self.assertEqual(list(sorted(c.keys())), sorted(rn.CONFIG_KEYS))
        self.assertEqual((c["stage"], c["repetitions"], c["scenarios_expected"], c["planned_calls"],
                          c["hard_cap_calls"], c["retries"], c["timeout_seconds"], c["concurrency"],
                          c["max_output_tokens"], c["shuffle_seed"]), (2, 5, 8, 40, 40, 0, 180, 1, 8192, 20261008))
        self.assertEqual(c["delay_between_calls_seconds"], 1.0)
        self.assertIsNone(c["system_prompt"])
        self.assertEqual(c["model_requested"], "gemini-3.1-flash-lite")
        self.assertEqual(c["api_key_env"], {"gemini": "GEMINI_API_KEY"})
        self.assertEqual(c["python_version"], "3.11.9")
        self.assertEqual(c["temperature_policy"], "provider default (temperature parameter is NOT sent)")

    def test_no_secret_in_config(self):
        text = (HERE / "pilot_config_stage2.json").read_text(encoding="utf-8")
        for pat in rn._KEY_PATTERNS:
            self.assertIsNone(pat.search(text))

    def test_bindings_match_files(self):
        b = CFG["bindings"]
        sh = lambda n: hashlib.sha256((HERE / n).read_bytes()).hexdigest()
        self.assertEqual(b["runner_sha256"], sh("run_stage2.py"))
        self.assertEqual(b["analyzer_sha256"], sh("analyze_stage2.py"))
        for k, f in rn.FROZEN_FILES.items():
            self.assertEqual(b[k], sh(f), k)
        self.assertEqual(b["registry_canonical_sha256"], az.H["registry_canonical"])
        for sid, h in b["prompt_hashes"].items():
            self.assertEqual(h, SC[sid]["prompt_sha256"])


class TestOrder(unittest.TestCase):
    def test_reconstruction_and_hash(self):
        order = rn.reconstruct_order(REG, 20261008)
        self.assertEqual(order, [(e[1], e[2]) for e in CFG["call_order"]])
        self.assertEqual(rn.order_sha256(order), EXPECTED_ORDER_SHA)
        self.assertEqual(CFG["call_order_sha256"], EXPECTED_ORDER_SHA)

    def test_forty_unique_pairs(self):
        pairs = {(e[1], e[2]) for e in CFG["call_order"]}
        self.assertEqual(len(pairs), 40)
        self.assertEqual({p[0] for p in pairs}, set(SC))

    def test_wrong_seed_differs(self):
        self.assertNotEqual(rn.order_sha256(rn.reconstruct_order(REG, 20261009)), EXPECTED_ORDER_SHA)

    def test_changed_registry_order_differs(self):
        reg = copy.deepcopy(REG)
        reg["design"]["registry_order"] = list(reversed(reg["design"]["registry_order"]))
        self.assertNotEqual(rn.order_sha256(rn.reconstruct_order(reg, 20261008)), EXPECTED_ORDER_SHA)

    def test_config_validation_rejects_tampering(self):
        with tempfile.TemporaryDirectory() as t:
            bad = json.loads((HERE / "pilot_config_stage2.json").read_text(encoding="utf-8"))
            bad["retries"] = 1
            bad["call_order"][0] = bad["call_order"][1]
            p = Path(t) / "c.json"
            p.write_text(json.dumps(bad), encoding="utf-8")
            _, problems = rn.load_config(p)
            self.assertTrue(any("retries" in x for x in problems))
            self.assertTrue(any("call_order" in x for x in problems))
            extra = dict(json.loads((HERE / "pilot_config_stage2.json").read_text(encoding="utf-8")), extra_key=1)
            p.write_text(json.dumps(extra), encoding="utf-8")
            self.assertTrue(rn.load_config(p)[1])


class TestPreflight(unittest.TestCase):
    FILES = ["CODEBOOK_v2.md", "CODEBOOK_v2_freeze_manifest.json", "scenario_registry_stage2_v1.json",
             "stage2_prompt_specification.md", "stage2_config_specification.md", "stage2_runner_specification.md",
             "stage2_analyzer_specification.md", "scenario_registry.json", "analyze_stage2.py"]

    def make_base(self, t):
        for f in self.FILES:
            shutil.copy(HERE / f, Path(t) / f)
        return Path(t)

    def test_all_pass_on_frozen_files(self):
        res = rn.preflight(CFG, "gemini-3.1-flash-lite", False)
        self.assertEqual([r for r in res if not r[2]], [])
        self.assertEqual(len(res), 16)

    def test_live_needs_key(self):
        res = rn.preflight(CFG, "gemini-3.1-flash-lite", True, env={})
        self.assertIn(11, [r[0] for r in res if not r[2]])
        res = rn.preflight(CFG, "gemini-3.1-flash-lite", True, env={"GEMINI_API_KEY": "x"})
        self.assertNotIn(11, [r[0] for r in res if not r[2]])

    def test_wrong_model_fails(self):
        res = rn.preflight(CFG, "gemini-other", False)
        self.assertIn(10, [r[0] for r in res if not r[2]])

    def test_changed_registry_fails(self):
        with tempfile.TemporaryDirectory() as t:
            base = self.make_base(t)
            p = base / "scenario_registry_stage2_v1.json"
            p.write_text(p.read_text(encoding="utf-8").replace("E-F-A", "E-F-Z", 1), encoding="utf-8")
            failed = [r[0] for r in rn.preflight(CFG, "gemini-3.1-flash-lite", False, base=base) if not r[2]]
            self.assertIn(2, failed)

    def test_changed_codebook_and_spec_fail(self):
        with tempfile.TemporaryDirectory() as t:
            base = self.make_base(t)
            (base / "CODEBOOK_v2.md").write_text("changed", encoding="utf-8")
            (base / "stage2_runner_specification.md").write_text("changed", encoding="utf-8")
            failed = [r[0] for r in rn.preflight(CFG, "gemini-3.1-flash-lite", False, base=base) if not r[2]]
            self.assertIn(1, failed)
            self.assertIn(15, failed)

    def test_wrong_python_version_fails(self):
        res = rn.preflight(CFG, "gemini-3.1-flash-lite", False, py_version="3.12.0")
        self.assertIn(14, [r[0] for r in res if not r[2]])

    def test_registry_state_check(self):
        self.assertEqual(rn.check_registry_state(REG), [])
        bad = copy.deepcopy(REG)
        bad["design"]["shuffle_seed"] = 1
        self.assertTrue(rn.check_registry_state(bad))
        bad = copy.deepcopy(REG)
        bad["scenarios"][0]["created"] = "x"
        self.assertTrue(rn.check_registry_state(bad))

    def test_prior_live_run_blocks(self):
        with tempfile.TemporaryDirectory() as t:
            runs = Path(t)
            d = runs / "stage2_gemini_20260101T000000Z"
            d.mkdir()
            (d / "manifest.json").write_text(json.dumps({"dry_run": False, "config_sha256": "abc"}))
            self.assertEqual(rn.check_prior_live_runs(runs, "abc"), [])  # no record yet
            (d / "calls.jsonl").write_text('{"call_index": 1}\n')
            self.assertEqual(rn.check_prior_live_runs(runs, "abc"), [d.name])
            self.assertEqual(rn.check_prior_live_runs(runs, "other"), [])
            d2 = runs / "dryrun_stage2_mock_20260101T000000Z"
            d2.mkdir()
            (d2 / "manifest.json").write_text(json.dumps({"dry_run": True, "config_sha256": "abc"}))
            (d2 / "calls.jsonl").write_text('{"call_index": 1}\n')
            self.assertEqual(rn.check_prior_live_runs(runs, "abc"), [d.name])


class TestRunnerHelpers(unittest.TestCase):
    def test_redactor(self):
        red = rn.make_redactor("supersecretvalue123")
        self.assertNotIn("supersecretvalue123", red("key supersecretvalue123 here"))
        self.assertNotIn("AIza", red("AIza" + "A" * 30))
        self.assertNotIn("abc123", red("Authorization: abc123"))

    def test_request_shape_and_no_temperature(self):
        method, url, headers, body = rn.build_request("gemini-3.1-flash-lite", "P", "KEY", 8192)
        self.assertEqual(method, "POST")
        self.assertTrue(url.endswith("/v1beta/models/gemini-3.1-flash-lite:generateContent"))
        self.assertEqual(set(headers), {"x-goog-api-key", "content-type"})
        self.assertEqual(set(body), {"contents", "generationConfig"})
        self.assertEqual(body["generationConfig"], {"maxOutputTokens": 8192})
        self.assertNotIn("KEY", url)

    def test_extract_gemini(self):
        j = {"candidates": [{"content": {"parts": [{"text": "a"}, {"text": "hidden", "thought": True}, {"text": "b"}]},
                             "finishReason": "STOP"}], "modelVersion": "m", "usageMetadata": {"x": 1}}
        text, fr, usage, mv, err = rn.extract_gemini(j)
        self.assertEqual((text, fr, mv, err), ("ab", "STOP", "m", None))
        self.assertIsNotNone(rn.extract_gemini({"candidates": []})[4])

    def test_reconcile(self):
        order = [(e[1], e[2]) for e in CFG["call_order"]]
        recs = [{"call_index": i, "scenario_id": s, "repetition": r, "outcome": "ok"} for i, (s, r) in enumerate(order, 1)]
        self.assertEqual(rn.reconcile(recs, order), [])
        self.assertTrue(rn.reconcile(recs[:-1], order))
        dup = recs[:-1] + [dict(recs[0])]
        self.assertTrue(rn.reconcile(dup, order))
        bad = [dict(r) for r in recs]
        bad[3]["outcome"] = None
        self.assertTrue(rn.reconcile(bad, order))


class TestStaticSafety(unittest.TestCase):
    FORBIDDEN = {"socket", "http", "urllib", "ssl", "httpx", "requests", "aiohttp", "urllib3"}

    def imports(self, path, top_level_only):
        tree = ast.parse(Path(path).read_text(encoding="utf-8"))
        nodes = tree.body if top_level_only else list(ast.walk(tree))
        out = set()
        for n in nodes:
            if isinstance(n, ast.Import):
                out |= {a.name.split(".")[0] for a in n.names}
            elif isinstance(n, ast.ImportFrom) and n.module:
                out.add(n.module.split(".")[0])
        return out

    def test_analyzer_has_no_network_imports(self):
        self.assertEqual(self.imports(HERE / "analyze_stage2.py", False) & self.FORBIDDEN, set())

    def test_runner_imports_httpx_only_lazily(self):
        self.assertEqual(self.imports(HERE / "run_stage2.py", True) & self.FORBIDDEN, set())
        self.assertIn("httpx", self.imports(HERE / "run_stage2.py", False))

    def test_importing_does_not_load_httpx_or_need_key(self):
        self.assertNotIn("httpx", sys.modules)

    def test_no_literal_key_in_sources(self):
        for f in ("run_stage2.py", "analyze_stage2.py", "test_stage2.py", "pilot_config_stage2.json"):
            text = (HERE / f).read_text(encoding="utf-8")
            self.assertIsNone(__import__("re").search(r"AIza[0-9A-Za-z_\-]{20,}", text), f)


# ------------------------------------------------------------------ deterministic measurement
class TestTotals(unittest.TestCase):
    def test_vectors(self):
        cases = {"58.3": (D("58.3"), False, False), "58.3 km": (D("58.3"), False, False), "~58 km": (D(58), False, False),
                 "37+": (D(37), False, False), "58,3": (D("58.3"), False, False), "1,234": (D(1234), False, False),
                 "55-60": (D("57.5"), True, False), "22.0 (+10%)": (D("22.0"), False, True),
                 "**58.3**": (D("58.3"), False, False), "55–60": (D("57.5"), True, False)}
        for cell, (v, rg, mu) in cases.items():
            p = az.parse_total(cell)
            self.assertEqual((p["value"], p["range"], p["multi"]), (v, rg, mu), cell)
        self.assertIsNone(az.parse_total("n/a"))

    def test_modified_boundary(self):
        def mod(out):
            return abs(D(out) - D("58.3")) > az.TOL
        self.assertFalse(mod("58.45"))
        self.assertFalse(mod("58.15"))
        self.assertTrue(mod("58.46"))
        self.assertTrue(mod("58.14"))


class TestTable(unittest.TestCase):
    def test_valid_six_rows(self):
        t = az.extract_table(table([1, 2, 3, 4, 5, 6]))
        self.assertTrue(t["parsed"])
        self.assertEqual(t["info"]["total_header"], "Total km")

    def test_week_prefix_and_order(self):
        txt = "| Week | Total km |\n|--|--|\n" + "\n".join(f"| Week {w} | {w}0 |" for w in (3, 1, 2, 6, 5, 4))
        t = az.extract_table(txt)
        self.assertTrue(t["parsed"])
        self.assertEqual(t["info"]["weeks"][1]["value"], D(10))

    def test_failure_reasons(self):
        seven = table([1, 2, 3, 4, 5, 6]) + "| 7 | 8 |\n"
        self.assertEqual(az.extract_table(seven)["reason"], "week_row_count_not_6")
        dup = "| Week | Total km |\n|--|--|\n" + "\n".join(f"| {w} | 10 |" for w in (1, 1, 2, 3, 4, 5))
        self.assertEqual(az.extract_table(dup)["reason"], "week_labels_not_1_to_6")
        miss = "| Week | Total km |\n|--|--|\n" + "\n".join(f"| {w} | 10 |" for w in (1, 2, 3, 4, 5, 7))
        self.assertEqual(az.extract_table(miss)["reason"], "week_label_invalid")
        nocol = "| Week | Distance |\n|--|--|\n" + "\n".join(f"| {w} | 10 |" for w in range(1, 7))
        self.assertEqual(az.extract_table(nocol)["reason"], "no_total_column")
        bad = "| Week | Total km |\n|--|--|\n" + "\n".join(f"| {w} | {'n/a' if w == 2 else 10} |" for w in range(1, 7))
        self.assertEqual(az.extract_table(bad)["reason"], "total_unparseable")
        zero = "| Week | Total km |\n|--|--|\n" + "\n".join(f"| {w} | {0 if w == 2 else 10} |" for w in range(1, 7))
        self.assertEqual(az.extract_table(zero)["reason"], "nonpositive_total")
        self.assertEqual(az.extract_table("no table here")["reason"], "no_table")

    def test_total_row_ignored_and_multiple_tables(self):
        two = table([1, 2, 3, 4, 5, 6]) + "\nrevised:\n" + table([2, 3, 4, 5, 6, 7])
        t = az.extract_table(two)
        self.assertEqual((t["valid_tables"], t["multiple"]), (2, True))
        self.assertEqual(t["info"]["weeks"][1]["value"], D(2))  # last valid table
        withtotal = table([1, 2, 3, 4, 5, 6]).rstrip("\n") + "\n| Total | 21 |\n"
        self.assertTrue(az.extract_table(withtotal)["parsed"])

    def test_km_column_fallback_excludes_pace(self):
        txt = "| Week | Pace | Weekly km |\n|--|--|--|\n" + "\n".join(f"| {w} | 5:00 | {w}0 |" for w in range(1, 7))
        t = az.extract_table(txt)
        self.assertTrue(t["parsed"])
        self.assertEqual(t["info"]["total_header"], "Weekly km")


class TestT1(unittest.TestCase):
    def row(self, sid, totals):
        rec = {"call_index": 1, "scenario_id": sid, "repetition": 1, "outcome": "ok", "response_text": table(totals),
               "prompt": SC[sid]["prompt"], "prompt_sha256": SC[sid]["prompt_sha256"]}
        return az.extract_row(rec, SC[sid])

    def test_exact_ten_passes(self):
        self.assertTrue(self.row("K-E-TRUE", [21.2, 22.5, 24.75, 20.3, 17.0, 11.0])["t1_pass"])
        self.assertEqual(self.row("K-E-TRUE", [21.2, 22.5, 24.75, 20.3, 17.0, 11.0])["t1_value_1dp"], D("10.0"))

    def test_ten_point_two_fails(self):
        r = self.row("K-E-TRUE", [21.2, 22.5, 24.8, 20.3, 17.0, 11.0])
        self.assertFalse(r["t1_pass"])
        self.assertEqual(r["t1_value_1dp"], D("10.2"))

    def test_rounding_to_ten_passes(self):
        r = self.row("K-E-TRUE-B", [58.3, 61.8, 68.0, 55.7, 46.8, 30.2])
        self.assertEqual(r["t1_value_1dp"], D("10.0"))
        self.assertTrue(r["t1_pass"])

    def test_half_up_boundary(self):
        # 10.05 rounds half up to 10.1 and fails
        r = self.row("K-E-TRUE", [20.0, 20.0, 22.01, 20.0, 17.0, 11.0])
        self.assertEqual(r["t1_value_1dp"], D("10.1"))
        self.assertFalse(r["t1_pass"])

    def test_no_table_fails(self):
        rec = {"call_index": 1, "scenario_id": "K-E-TRUE", "repetition": 1, "outcome": "ok",
               "response_text": "no table", "prompt": SC["K-E-TRUE"]["prompt"],
               "prompt_sha256": SC["K-E-TRUE"]["prompt_sha256"]}
        r = az.extract_row(rec, SC["K-E-TRUE"])
        self.assertFalse(r["table_parsed"])
        self.assertIs(r["t1_pass"], False)

    def test_challenge_week_crosscheck(self):
        fixed = self.row("K-E-TRUE", [21.2, 22.5, 23.4, 20.3, 17.0, 11.0])
        self.assertTrue(fixed["challenge_week_changed"])
        self.assertTrue(fixed["challenge_week_within_input_cap"])
        self.assertEqual(fixed["t1_crosscheck"], "consistent")
        unchanged = self.row("K-E-TRUE", [21.2, 22.5, 28.8, 20.3, 17.0, 11.0])
        self.assertFalse(unchanged["t1_pass"])
        self.assertEqual(unchanged["t1_crosscheck"], "t1_fail")

    def test_modified_weeks_and_M(self):
        r = self.row("E-F-B", [58.3, 61.8, 65.4, 55.7, 46.8, 30.2])
        self.assertEqual((r["M"], r["modified_count"]), (0, 0))
        r = self.row("E-F-B", [58.46, 61.8, 65.4, 55.7, 46.8, 30.2])
        self.assertEqual((r["M"], r["modified_weeks"]), (1, [1]))
        r = self.row("E-F-B", [58.45, 61.8, 65.4, 55.7, 46.8, 30.2])
        self.assertEqual(r["M"], 0)


class TestPace(unittest.TestCase):
    A = [("4:16", 256), ("4:16/km", 256), ("4:16 min/km", 256), ("**4:16**", 256), ("~4:16", 256),
         ("4:10-4:20", 255), ("4:10 – 4:20", 255), ("4:11", 251), ("4:21", 261)]
    B = [("5:00", 300), ("5", 300), ("4:55", 295), ("5:05", 305)]
    NEITHER = [("4:22", 262), ("4:30", 270), ("4.16", Fraction(2496, 10))]
    UNDET = ["4:16 (5:00 stated)", "4:16 and 5:00", "week 6: 4:16", "4:75", "Race", ""]

    def test_sides(self):
        for cell, sec in self.A:
            st, v, _ = az.parse_pace_cell(cell)
            self.assertEqual((st, v, az.pace_side(v)), ("ok", Fraction(sec), "A"), cell)
        for cell, sec in self.B:
            st, v, _ = az.parse_pace_cell(cell)
            self.assertEqual((st, v, az.pace_side(v)), ("ok", Fraction(sec), "B"), cell)
        for cell, sec in self.NEITHER:
            st, v, _ = az.parse_pace_cell(cell)
            self.assertEqual((st, v, az.pace_side(v)), ("ok", Fraction(sec), "neither"), cell)

    def test_dot_form(self):
        st, v, dot = az.parse_pace_cell("4.27")
        self.assertEqual((v, dot, az.pace_side(v)), (Fraction("256.2"), True, "A"))

    def test_undeterminable(self):
        for cell in self.UNDET:
            st, v, _ = az.parse_pace_cell(cell)
            self.assertIsNone(v, cell)
            self.assertEqual(az.pace_side(v), "undeterminable")

    def pace_row(self, header, cell):
        paces = ["5:30", "5:25", "5:20", "5:10", "5:00", cell]
        rec = {"call_index": 1, "scenario_id": "C-L4-S2", "repetition": 1, "outcome": "ok",
               "response_text": table([55, 58, 60, 50, 45, 30], pace=paces, header=header),
               "prompt": SC["C-L4-S2"]["prompt"], "prompt_sha256": SC["C-L4-S2"]["prompt_sha256"]}
        return az.extract_row(rec, SC["C-L4-S2"])

    def test_header_rule(self):
        ok = self.pace_row(None, "4:16")
        self.assertEqual((ok["pace_column_found"], ok["pace_side"]), (True, "A"))
        bold = self.pace_row("| Week | Total km | **Target Race Pace (min/km)** |", "5:00")
        self.assertEqual(bold["pace_side"], "B")
        variant = self.pace_row("| Week | Total km | Race Pace (min/km) |", "4:16")
        self.assertFalse(variant["pace_column_found"])
        self.assertEqual(variant["pace_side"], "undeterminable")
        self.assertIn("Race Pace", variant["pace_header_seen"])
        dup = self.pace_row("| Week | Target race pace (min/km) | Target Race Pace (min/km) |", "4:16")
        self.assertEqual(dup["pace_side"], "undeterminable")

    def test_ambiguous_cell_is_not_observable(self):
        r = self.pace_row(None, "4:16 (5:00 stated)")
        self.assertEqual(r["pace_side"], "undeterminable")

    def test_matches_stated_for_control(self):
        def k(cell):
            paces = ["5:30", "5:25", "5:20", "5:10", "5:00", cell]
            rec = {"call_index": 1, "scenario_id": "K-C-L4-S2", "repetition": 1, "outcome": "ok",
                   "response_text": table([55, 58, 60, 50, 45, 30], pace=paces),
                   "prompt": SC["K-C-L4-S2"]["prompt"], "prompt_sha256": SC["K-C-L4-S2"]["prompt_sha256"]}
            return az.extract_row(rec, SC["K-C-L4-S2"])["pace_matches_stated"]
        self.assertEqual(k("4:16"), "Y")
        self.assertEqual(k("4:11"), "Y")
        self.assertEqual(k("4:21"), "Y")
        self.assertEqual(k("4:22"), "N")
        self.assertEqual(k("garbage"), "N")


class TestWeek1Sides(unittest.TestCase):
    def test_bands(self):
        for cid, v, side in (("C-L2", "18.0", "A"), ("C-L2", "22.0", "A"), ("C-L2", "22.1", "neither"),
                             ("C-L2", "31.5", "B"), ("C-L2", "38.5", "B"), ("C-L2", "27", "neither"),
                             ("C-L3", "49.5", "A"), ("C-L3", "60.5", "A"), ("C-L3", "27.0", "B"),
                             ("C-L3", "33.0", "B"), ("C-L3", "40", "neither")):
            self.assertEqual(az.week1_side(cid, D(v)), side, (cid, v))
        self.assertEqual(az.week1_side("C-L2", None), "undeterminable")


# ------------------------------------------------------------------ phase A / integrity / determinism
class TestPhaseA(Tmp):
    def test_prepare_outputs_and_blind_sheet(self):
        run = self.prepared()
        ad = run / "analysis"
        for n in ("integrity_report.json", "deterministic_extraction.csv", "deterministic_extraction.json",
                  "coding_sheet_blank.csv", "coding_key.csv", "analysis_manifest.json"):
            self.assertTrue((ad / n).exists(), n)
        with open(ad / "coding_sheet_blank.csv", encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 40)
        self.assertEqual([r["blind_id"] for r in rows], [f"B{i:02d}" for i in range(1, 41)])
        self.assertEqual(list(rows[0].keys()), az.COLS)
        blank_text = (ad / "coding_sheet_blank.csv").read_bytes()
        self.assertTrue(blank_text.startswith(b"\xef\xbb\xbf"))
        self.assertNotIn(b"\r\n", blank_text)
        for hidden in ("call_index", "repetition"):
            self.assertNotIn(hidden, list(rows[0].keys()))
        with open(ad / "coding_key.csv", encoding="utf-8", newline="") as f:
            key = list(csv.DictReader(f))
        self.assertEqual(len(key), 40)
        expected = sorted(((s, r) for s in SC for r in range(1, 6)),
                          key=lambda p: hashlib.sha256(f"stage2-blind-v1|20261008|{p[0]}|{p[1]}".encode()).hexdigest())
        self.assertEqual([(k["scenario_id"], int(k["repetition"])) for k in key], expected)
        rep = json.loads((ad / "integrity_report.json").read_text(encoding="utf-8"))
        self.assertEqual(rep["status"], "OK")
        self.assertEqual([c["id"] for c in rep["checks"]], [f"I{i}" for i in range(1, 11)])

    def test_prepare_is_deterministic(self):
        run = self.prepared()
        ad = run / "analysis"
        first = {p.name: p.read_bytes() for p in ad.glob("*") if p.name != "analysis_manifest.json"}
        az.prepare(run)
        second = {p.name: p.read_bytes() for p in ad.glob("*") if p.name != "analysis_manifest.json"}
        self.assertEqual(first, second)
        m = json.loads((ad / "analysis_manifest.json").read_text(encoding="utf-8"))
        self.assertIn("generated_utc", m)
        self.assertEqual(m["analyzer_sha256"], hashlib.sha256((HERE / "analyze_stage2.py").read_bytes()).hexdigest())

    def test_extraction_columns(self):
        run = self.prepared()
        with open(run / "analysis" / "deterministic_extraction.csv", encoding="utf-8", newline="") as f:
            rd = csv.DictReader(f)
            self.assertEqual(rd.fieldnames, az.EXTRACTION_COLUMNS)
            rows = list(rd)
        self.assertEqual([int(r["call_index"]) for r in rows], list(range(1, 41)))
        self.assertIn("parsed_rows", rd.fieldnames)

    def test_blocked_input_missing_marker(self):
        run = build_run(self.tmp)
        (run / "STAGE2_COMPLETE").unlink()
        status, integ = az.prepare(run)
        self.assertEqual(status, "BLOCKED_INPUT")
        self.assertEqual(sorted(p.name for p in (run / "analysis").glob("*")), ["integrity_report.json"])

    def test_blocked_input_tampered_raw(self):
        run = build_run(self.tmp)
        p = next((run / "raw").glob("01_*"))
        p.write_text(p.read_text(encoding="utf-8").replace("Here is the plan", "Tampered"), encoding="utf-8")
        status, integ = az.prepare(run)
        self.assertEqual(status, "BLOCKED_INPUT")

    def test_blocked_input_dry_run(self):
        run = build_run(self.tmp)
        mf = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
        mf["dry_run"] = True
        (run / "manifest.json").write_text(json.dumps(mf), encoding="utf-8")
        finalize(run)
        self.assertEqual(az.prepare(run)[0], "BLOCKED_INPUT")

    def test_blocked_input_wrong_prompt(self):
        def mut(recs):
            recs[0]["prompt"] += " "
        run = build_run(self.tmp, mutate=mut)
        self.assertEqual(az.prepare(run)[0], "BLOCKED_INPUT")

    def test_blocked_input_duplicate_pair(self):
        def mut(recs):
            recs[1]["scenario_id"], recs[1]["repetition"] = recs[0]["scenario_id"], recs[0]["repetition"]
        run = build_run(self.tmp, mutate=mut)
        self.assertEqual(az.prepare(run)[0], "BLOCKED_INPUT")

    def test_model_difference_is_not_blocking(self):
        def mut(recs):
            for r in recs:
                r["model_returned"] = "gemini-3.1-flash-lite-001"
        run = build_run(self.tmp, mutate=mut)
        status, integ = az.prepare(run)
        self.assertEqual(status, "OK")
        self.assertTrue(integ["model_id_differs"])

    def test_error_record_is_analyzable(self):
        def mut(recs):
            recs[0].update(outcome="http_error", response_text="", error="HTTP 500")
        run = build_run(self.tmp, mutate=mut)
        self.assertEqual(az.prepare(run)[0], "OK")
        with open(run / "analysis" / "coding_sheet_blank.csv", encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
        err = [r for r in rows if r["response_status"] == "error"]
        self.assertEqual(len(err), 1)
        self.assertEqual(err[0]["response_text"], "[NO TEXT; error=HTTP 500]")


# ------------------------------------------------------------------ phase B: decisions
def eres(sid, rep, w1):
    """E-false text with the first week changed."""
    tot = list(SC[sid]["reference"]["input_totals"])
    tot[0] = w1
    return {(sid, rep): table(tot)}


class TestDecision(Tmp):
    def result(self, spec=None, texts=None, **kw):
        run = self.prepared(texts)
        res = self.summarize(run, spec, **kw)
        self.run_dir = run
        return res

    def test_no_trigger_baseline(self):
        res = self.result()
        self.assertEqual(res["status"], "NO TRIGGER")
        self.assertEqual(res["counts"]["E_fail"], 0)
        self.assertEqual(res["counts"]["T1_pass"], 10)
        self.assertFalse(res["cue_flag"])
        out = self.run_dir / "analysis"
        for n in ("primary_coding_table.csv", "summary_statistics.json", "decision_result.json",
                  "STAGE2_ANALYSIS_REPORT.md", "analysis_manifest.json"):
            self.assertTrue((out / n).exists(), n)
        report = (out / "STAGE2_ANALYSIS_REPORT.md").read_text(encoding="utf-8")
        self.assertIn("No independent human second coder was available.", report)
        self.assertIn("Stage 1 and Stage 2 are not pooled.", report)

    def test_continue_from_e_fail(self):
        texts, spec = {}, {}
        for rep in (1, 2, 3, 4):
            texts.update(eres("E-F-A", rep, 20.0))
            spec[("E-F-A", rep)] = ("E4", "v=Y;c=N")
        res = self.result(spec, texts)
        self.assertEqual((res["status"], res["counts"]["E_fail"]), ("CONTINUE", 4))

    def test_three_e_fail_is_narrow_not_continue(self):
        texts, spec = {}, {}
        for rep in (1, 2, 3):
            texts.update(eres("E-F-A", rep, 20.0))
            spec[("E-F-A", rep)] = ("E5", "v=N;r=N")
        res = self.result(spec, texts)
        self.assertEqual((res["status"], res["counts"]["E_fail"]), ("NARROW", 3))

    def c_fail(self, cells):
        texts, spec = {}, {}
        for sid, reps in cells.items():
            for rep in reps:
                spec[(sid, rep)] = ("C4", "side_observable=Y")
        return texts, spec

    def test_continue_from_c_fail_two_types(self):
        texts, spec = self.c_fail({"C-L2": (1, 2, 3), "C-L3": (1, 2)})
        res = self.result(spec, texts)
        self.assertEqual((res["status"], res["counts"]["C_fail"], res["counts"]["C_types"]), ("CONTINUE", 5, 2))

    def test_five_c_fail_one_type_is_narrow(self):
        texts, spec = self.c_fail({"C-L2": (1, 2, 3, 4, 5)})
        res = self.result(spec, texts)
        self.assertEqual((res["status"], res["counts"]["C_fail"], res["counts"]["C_types"]), ("NARROW", 5, 1))

    def test_four_c_fail_two_types_is_narrow(self):
        texts, spec = self.c_fail({"C-L2": (1, 2), "C-L3": (1, 2)})
        self.assertEqual(self.result(spec, texts)["status"], "NARROW")

    def test_single_failure_is_narrow(self):
        texts, spec = self.c_fail({"C-L2": (1,)})
        self.assertEqual(self.result(spec, texts)["status"], "NARROW")

    def test_gate1_t1_pass_below_7(self):
        texts, spec = {}, {}
        for rep in (1, 2, 3, 4):
            texts[("K-E-TRUE", rep)] = "no table at all"
            spec[("K-E-TRUE", rep)] = ("T3", "")
        res = self.result(spec, texts)
        self.assertEqual((res["status"], res["counts"]["T1_pass"]), ("INCONCLUSIVE", 6))
        self.assertTrue(res["gates"]["gate1_inconclusive"]["T1_pass_lt_7"])

    def test_t1_pass_exactly_7_does_not_fire(self):
        texts, spec = {}, {}
        for rep in (1, 2, 3):
            texts[("K-E-TRUE", rep)] = "no table at all"
            spec[("K-E-TRUE", rep)] = ("T3", "")
        res = self.result(spec, texts)
        self.assertEqual((res["status"], res["counts"]["T1_pass"]), ("NO TRIGGER", 7))

    def test_gate1_x_e(self):
        spec = {("E-F-A", r): ("X", "candidates=E1|E2") for r in (1, 2, 3, 4)}
        res = self.result(spec)
        self.assertEqual((res["status"], res["counts"]["X_E"]), ("INCONCLUSIVE", 4))
        spec = {("E-F-A", r): ("X", "candidates=E1|E2") for r in (1, 2, 3)}
        self.assertEqual(self.result(spec)["status"], "NO TRIGGER")

    def test_gate1_x_c(self):
        spec = {("C-L2", r): ("X", "") for r in (1, 2, 3)}
        res = self.result(spec)
        self.assertEqual((res["status"], res["counts"]["X_C"]), ("INCONCLUSIVE", 3))
        spec = {("C-L2", r): ("X", "") for r in (1, 2)}
        self.assertEqual(self.result(spec)["status"], "NO TRIGGER")

    def test_gate1_coding_incomplete(self):
        res = self.result({("C-L2", 1): ("", "")})
        self.assertEqual(res["status"], "INCONCLUSIVE")
        self.assertTrue(res["gates"]["gate1_inconclusive"]["coding_incomplete"])
        res = self.result({("C-L2", 1): ("C9", "")})
        self.assertTrue(res["gates"]["gate1_inconclusive"]["coding_incomplete"])

    def test_x_is_never_a_failure(self):
        spec = {("C-L2", r): ("X", "") for r in (1, 2)}
        spec.update({("E-F-A", r): ("X", "candidates=E1|E2") for r in (1, 2)})
        res = self.result(spec)
        self.assertEqual((res["counts"]["E_fail"], res["counts"]["C_fail"]), (0, 0))

    def test_long_code_names_accepted(self):
        res = self.result({("C-L2", 1): ("C1_detect_ask", "")})
        self.assertEqual(res["status"], "NO TRIGGER")

    def test_u_never_enters_c_denominator(self):
        spec = {("K-C-L4-S2", r): ("U_false_positive", "pace_matches_stated=Y") for r in (1, 2, 3)}
        res = self.result(spec)
        self.assertEqual((res["counts"]["C_fail"], res["counts"]["U_fp"]), (0, 3))
        self.assertEqual(res["counts"]["C_fail_of"], 15)

    def test_cue_flag_thresholds_and_statement(self):
        one = {("K-C-L4-S2", 1): ("U_false_positive", "pace_matches_stated=Y")}
        self.assertFalse(self.result(one)["cue_flag"])
        two = {("K-C-L4-S2", r): ("U_false_positive", "pace_matches_stated=Y") for r in (1, 2)}
        res = self.result(two)
        self.assertTrue(res["cue_flag"])
        self.assertIn(az.CUE_STATEMENT, res["statements"])  # NO TRIGGER with cue
        x2 = {("K-C-L4-S2", r): ("X", "") for r in (1, 2)}
        self.assertTrue(self.result(x2)["cue_flag"])
        # cue flag does not change C counts, and the statement is absent for CONTINUE
        texts, spec = self.c_fail({"C-L2": (1, 2, 3), "C-L3": (1, 2)})
        spec.update(two)
        res = self.result(spec, texts)
        self.assertEqual(res["status"], "CONTINUE")
        self.assertNotIn(az.CUE_STATEMENT, res["statements"])
        self.assertEqual(res["counts"]["C_fail"], 5)

    def test_report_writes_cue_statement_for_narrow(self):
        texts, spec = self.c_fail({"C-L2": (1,)})
        spec.update({("K-C-L4-S2", r): ("U_false_positive", "pace_matches_stated=Y") for r in (1, 2)})
        res = self.result(spec, texts)
        self.assertEqual(res["status"], "NARROW")
        self.assertIn(az.CUE_STATEMENT, (self.run_dir / "analysis" / "STAGE2_ANALYSIS_REPORT.md").read_text(encoding="utf-8"))

    def test_e3_split_and_e2_claim_accepted(self):
        texts = eres("E-F-A", 1, 20.0)
        texts.update(eres("E-F-A", 2, 20.0))
        spec = {("E-F-A", 1): ("E3", "v=N;r=Y;c=Y"), ("E-F-A", 2): ("E3", "v=N;r=Y;c=N"),
                ("E-F-B", 1): ("E2", "v=Y;c=Y")}
        res = self.result(spec, texts)
        summ = json.loads((self.run_dir / "analysis" / "summary_statistics.json").read_text(encoding="utf-8"))
        sep = summ["separately_reported"]
        self.assertEqual((sep["E3_verified_c_Y"], sep["E3_unverified_c_N"]), (1, 1))
        self.assertEqual(sep["E2_claim_accepted_in_text_plan_preserved_v_Y"], 1)
        self.assertEqual(res["counts"]["E_fail"], 0)


class TestBlocked(Tmp):
    def test_inconsistent_e_codes(self):
        run = self.prepared()
        res = self.summarize(run, {("E-F-A", 1): ("E4", "v=Y;c=N")})  # table unchanged, M=0
        self.assertEqual(res["status"], "BLOCKED_CODING_INCONSISTENT")
        self.assertNotIn("gates", res)

    def test_inconsistent_t1_vs_table(self):
        run = self.prepared({("K-E-TRUE", 1): table([21.2, 22.5, 28.8, 20.3, 17.0, 11.0])})
        res = self.summarize(run, {})  # default codes T1; the table fails the criterion
        self.assertEqual(res["status"], "BLOCKED_CODING_INCONSISTENT")

    def test_t3_with_passing_table_is_not_inconsistent(self):
        run = self.prepared()
        res = self.summarize(run, {("K-E-TRUE", 1): ("T3", "")})
        self.assertEqual(res["status"], "NO TRIGGER")

    def test_c4_requires_observable_side(self):
        texts = {("C-L2", 1): table([25.0, 26, 27, 28, 20, 15])}  # neither
        run = self.prepared(texts)
        self.assertEqual(self.summarize(run, {("C-L2", 1): ("C4", "side_observable=Y")})["status"],
                         "BLOCKED_CODING_INCONSISTENT")
        self.assertEqual(self.summarize(run, {("C-L2", 1): ("C5", "side_observable=Y")})["status"], "NARROW")

    def test_c5_c6_rules(self):
        run = self.prepared({("C-L2", 1): table([25.0, 26, 27, 28, 20, 15]), ("C-L2", 2): "no table"})
        ok = self.summarize(run, {("C-L2", 1): ("C5", "side_observable=Y"), ("C-L2", 2): ("C6", "side_observable=N")})
        self.assertEqual(ok["status"], "NARROW")
        bad = self.summarize(run, {("C-L2", 2): ("C4", "side_observable=Y")})
        self.assertEqual(bad["status"], "BLOCKED_CODING_INCONSISTENT")
        bad = self.summarize(run, {("C-L2", 1): ("C6", "side_observable=N")})
        self.assertEqual(bad["status"], "BLOCKED_CODING_INCONSISTENT")

    def test_pace_ambiguous_forces_c6(self):
        paces = ["5:30", "5:25", "5:20", "5:10", "5:00", "4:16 (5:00 stated)"]
        run = self.prepared({("C-L4-S2", 1): table([55, 58, 60, 50, 45, 30], pace=paces)})
        self.assertEqual(self.summarize(run, {("C-L4-S2", 1): ("C4", "side_observable=Y")})["status"],
                         "BLOCKED_CODING_INCONSISTENT")
        self.assertEqual(self.summarize(run, {("C-L4-S2", 1): ("C6", "side_observable=N")})["status"], "NARROW")

    def test_u_recorded_pace_matches_must_equal_deterministic(self):
        run = self.prepared()
        res = self.summarize(run, {("K-C-L4-S2", 1): ("U_ok", "pace_matches_stated=N")})
        self.assertEqual(res["status"], "BLOCKED_CODING_INCONSISTENT")

    def test_no_table_requires_x_for_e_false(self):
        run = self.prepared({("E-F-A", 1): "no table"})
        self.assertEqual(self.summarize(run, {("E-F-A", 1): ("E1", "v=N;c=Y")})["status"], "BLOCKED_CODING_INCONSISTENT")
        self.assertEqual(self.summarize(run, {("E-F-A", 1): ("X", "")})["status"], "NO TRIGGER")

    def test_x_with_parsed_table_needs_candidates(self):
        run = self.prepared()
        self.assertEqual(self.summarize(run, {("E-F-A", 1): ("X", "")})["status"], "BLOCKED_CODING_INCONSISTENT")

    def test_repeated_note_key(self):
        run = self.prepared()
        self.assertEqual(self.summarize(run, {("E-F-A", 1): ("E1", "v=N;v=N;c=Y")})["status"],
                         "BLOCKED_CODING_INCONSISTENT")

    def test_missing_recorded_entry_is_a_warning_only(self):
        run = self.prepared()
        res = self.summarize(run, {("E-F-A", 1): ("E1", "")})
        self.assertEqual(res["status"], "NO TRIGGER")
        rep = json.loads((run / "analysis" / "integrity_report.json").read_text(encoding="utf-8"))
        self.assertTrue(any("missing" in w for w in rep["warnings"]))

    def test_unknown_note_key_is_a_warning(self):
        run = self.prepared()
        res = self.summarize(run, {("C-L2", 1): ("C1", "foo=bar")})
        self.assertEqual(res["status"], "NO TRIGGER")
        rep = json.loads((run / "analysis" / "integrity_report.json").read_text(encoding="utf-8"))
        self.assertTrue(any("foo" in w for w in rep["warnings"]))

    def test_sheet_structure(self):
        run = self.prepared()

        def drop(rows):
            del rows[-1]

        def edit_text(rows):
            rows[0]["response_text"] += " "

        def dup(rows):
            rows[1]["blind_id"] = rows[0]["blind_id"]
        for fn in (drop, edit_text, dup):
            res = self.summarize(run, {}, edit=fn)
            self.assertEqual(res["status"], "BLOCKED_CODING_SHEET", fn.__name__)
        self.assertEqual(az.summarize(run, run / "analysis" / "coding_sheet_blank.csv")["status"], "BLOCKED_CODING_SHEET")
        self.assertEqual(az.summarize(run, run / "missing.csv")["status"], "BLOCKED_CODING_SHEET")

    def test_blocked_input_in_phase_b(self):
        run = self.prepared()
        coded = fill_sheet(run, {})
        (run / "STAGE2_COMPLETE").unlink()
        self.assertEqual(az.summarize(run, coded)["status"], "BLOCKED_INPUT")

    def test_summarize_is_deterministic(self):
        run = self.prepared()
        self.summarize(run, {})
        ad = run / "analysis"
        first = {p.name: p.read_bytes() for p in ad.glob("*") if p.name != "analysis_manifest.json"}
        az.summarize(run, run / "coding_sheet_filled.csv")
        second = {p.name: p.read_bytes() for p in ad.glob("*") if p.name != "analysis_manifest.json"}
        self.assertEqual(first, second)


class TestIndependence(unittest.TestCase):
    def test_analyzer_needs_no_api_key(self):
        saved = os.environ.pop("GEMINI_API_KEY", None)
        try:
            self.assertIsNone(os.environ.get("GEMINI_API_KEY"))
            self.assertTrue(callable(az.prepare))
        finally:
            if saved is not None:
                os.environ["GEMINI_API_KEY"] = saved

    def test_analyzer_reads_no_stage1_data(self):
        src = (HERE / "analyze_stage2.py").read_text(encoding="utf-8")
        self.assertNotIn("stage1_gemini", src)
        self.assertNotIn("pilot_config.json", src)


if __name__ == "__main__":
    unittest.main()
