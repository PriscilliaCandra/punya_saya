"""P8 resume, provenance, cost stop and fail-closed behaviour -- MOCK provider only (temporary folders, no network, no API key, no model call).
These tests check the local implementation in s10_resume.py / s10_runner.py / s10_integrity.py. They do not show that resume is ALLOWED: MD-08 is still pending
owner/advisor; the tests pin what the code does and refuses.
Run: python -B -I -W error::ResourceWarning -m unittest discover -s research_design/step10 -p test_resume.py"""
import io
import json
import os
import shutil
import sys
import unittest
from contextlib import redirect_stdout
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
import s10_integrity as IG  # noqa: E402
import s10_resume as RS  # noqa: E402
import s10_runner as RN  # noqa: E402
import test_ledger_resilience as LR  # noqa: E402
import test_pilot_flow as PF  # noqa: E402
import test_step10 as T10  # noqa: E402

BUILD = T10.BUILD
SECRET = "SECRET-KEY-VALUE-0123456789"


def ledger_of(run):
    return [json.loads(l) for l in PF.rb(os.path.join(run, "ledger.jsonl")).decode().split("\n") if l]


def calls_of(run):
    return [json.loads(l) for l in PF.rb(os.path.join(run, "calls.jsonl")).decode().split("\n") if l]


class OtherProvider(RN.MockProvider):
    pass


class Base(PF.Base):
    def setUp(self):
        super().setUp()
        self.k = 0

    # ---- building interrupted runs -------------------------------------------------------------------------------------------------
    def pilot_files(self):
        self.k += 1
        return T10.TestRunner.files(self, "pilot_round_1", days=30 + self.k, calls=18)

    def interrupted_pilot(self, kill_at=None, patch=None, extra_env=None):
        ev, au = self.pilot_files()
        out = os.path.join(self.tmp, f"int{self.k}")
        seen = []

        def script(key, prompt):
            seen.append(key)
            if kill_at is not None and patch is None and len(seen) == kill_at:
                raise KeyboardInterrupt()
            return T10.good(key, prompt)
        prov = RN.MockProvider(script)
        ctx = patch if patch is not None else mock.patch.dict(os.environ, extra_env or {})
        with ctx, redirect_stdout(io.StringIO()):
            with self.assertRaises(KeyboardInterrupt):
                RN.run("pilot_round_1", BUILD, out, prov, evidence_path=ev, auth_path=au, sleeper=lambda x: None, verify_build=False)
        return out, ev, au, prov

    @staticmethod
    def kill_on_event(event, index):
        orig = RN.RunWriter.ledger

        def ledger(self_, entry):
            if entry.get("event") == event and entry.get("call_index") == index:
                raise KeyboardInterrupt()
            return orig(self_, entry)
        return mock.patch.object(RN.RunWriter, "ledger", ledger)

    @staticmethod
    def kill_on_calls_write(n):
        orig_init = RN.RunWriter.__init__

        class Boom:
            def __init__(self, f):
                self.f, self.count = f, 0

            def write(self, b):
                self.count += 1
                if self.count == n:
                    raise KeyboardInterrupt()
                return self.f.write(b)

            def flush(self):
                self.f.flush()

            def fileno(self):
                return self.f.fileno()

        def init(self_, out_dir, led, calls, prev):
            orig_init(self_, out_dir, led, Boom(calls), prev)
        return mock.patch.object(RN.RunWriter, "__init__", init)

    # ---- resume helpers -------------------------------------------------------------------------------------------------------------
    @staticmethod
    def head_of(run):
        lines = [l for l in PF.rb(os.path.join(run, "ledger.jsonl")).split(b"\n") if l]
        return RN.sha(lines[-1] + b"\n")

    def write_ra(self, run, name="ra.json", scope="pilot_round_1", total=18, basis="process_interruption", **over):
        led = ledger_of(run)
        ra = {"authorized_by": "owner", "scope": scope, "run_id": led[0]["run_id"], "ledger_head_sha256": self.head_of(run), "resume_basis": basis,
              "acknowledges_unspecified_basis": basis == "process_interruption", "remaining_calls": total - len(os.listdir(os.path.join(run, "raw"))),
              "cost_ceiling_usd": 100}
        ra.update(over)
        p = os.path.join(self.tmp, f"{name}.{self.k}.json")
        PF.wb(p, (json.dumps(ra, sort_keys=True) + "\n").encode())
        return p

    def resume(self, run, ev, au, ra, prov, **kw):
        with redirect_stdout(io.StringIO()):
            return RS.resume(run, BUILD, prov, evidence_path=ev, auth_path=au, resume_auth_path=ra, sleeper=lambda x: None, verify_build=False, **kw)

    def assert_refused(self, run, ev, au, ra, text, prov=None, **kw):
        prov = prov or RN.MockProvider(T10.good)
        before = LR.tree_hashes(run)
        with self.assertRaises(RS.ResumeRefused) as cm:
            self.resume(run, ev, au, ra, prov, **kw)
        self.assertIn(text, " | ".join(cm.exception.reasons))
        self.assertEqual(prov.calls, 0)                                    # no provider call
        self.assertEqual(LR.tree_hashes(run), before)                      # nothing changed
        return cm.exception


class TestProvenance(Base):
    def test_provenance_is_on_the_ledger_before_the_first_call_finishes_and_holds_no_secret(self):
        out, ev, au, prov = self.interrupted_pilot(kill_at=1, extra_env={"GEMINI_API_KEY": SECRET})
        led = ledger_of(out)
        self.assertEqual([(e["event"], e["call_index"]) for e in led], [("start", 0), ("intent", 1)])        # stopped inside the first call
        s = led[0]
        self.assertEqual((s["scope"], s["planned_calls"], s["provider"], s["ledger_format"]), ("pilot_round_1", 18, "MockProvider", 2))
        self.assertEqual(s["build_manifest_sha256"], RN.file_sha(os.path.join(BUILD, "manifest.json")))
        self.assertEqual(s["authorization"]["sha256"], RN.file_sha(au))
        self.assertEqual(s["evidence_sha256"], RN.file_sha(ev))
        self.assertEqual(s["fz_file_sha256"], RN.file_sha(RN.FZ_PATH))
        self.assertEqual(s["settings"]["model_id"], "gemini-3.5-flash-lite")
        self.assertEqual(len(s["run_id"]), 16)
        for d, _, fs in os.walk(out):
            for f in fs:
                self.assertNotIn(SECRET.encode(), PF.rb(os.path.join(d, f)))                                    # no key anywhere in the run folder

    def test_a_clean_run_has_provenance_and_passes_integrity(self):
        ev, au = self.pilot_files()
        out = os.path.join(self.tmp, "clean")
        with redirect_stdout(io.StringIO()):
            s = RN.run("pilot_round_1", BUILD, out, RN.MockProvider(T10.good), evidence_path=ev, auth_path=au, sleeper=lambda x: None, verify_build=False)
        self.assertEqual((s["ledger_format"], s["resumes"]), (2, []))
        P, st = IG.verify_run(out, BUILD)
        self.assertEqual(P, [])
        self.assertEqual((st["provenance_present"], st["resumes"]), (True, 0))

    def test_integrity_flags_a_format_2_run_without_its_provenance_entry(self):
        ev, au = self.pilot_files()
        out = os.path.join(self.tmp, "clean2")
        with redirect_stdout(io.StringIO()):
            RN.run("pilot_round_1", BUILD, out, RN.MockProvider(T10.good), evidence_path=ev, auth_path=au, sleeper=lambda x: None, verify_build=False)
        p = os.path.join(out, "ledger.jsonl")
        lines = [l for l in PF.rb(p).split(b"\n") if l]
        PF.wb(p, b"\n".join(lines[1:]) + b"\n")
        P, _ = IG.verify_run(out, BUILD)
        self.assertTrue(any("provenance" in x for x in P) and any("chain" in x for x in P))


class TestResumeAfterProcessInterruption(Base):
    def test_intent_without_a_persisted_record_is_never_repeated_and_the_resume_is_refused(self):
        out, ev, au, _ = self.interrupted_pilot(kill_at=4)
        ra = self.write_ra(out)
        e = self.assert_refused(out, ev, au, ra, "attempted, no record")
        self.assertIn("MD-08", " ".join(e.reasons))

    def test_raw_saved_but_ledger_raw_entry_missing_is_reconciled_without_calling_again(self):
        out, ev, au, prov1 = self.interrupted_pilot(patch=self.kill_on_event("raw", 5))
        self.assertTrue(os.path.exists(os.path.join(out, "raw", "00005.json")))
        self.assertNotIn(("raw", 5), [(e["event"], e["call_index"]) for e in ledger_of(out)])
        raw5 = LR.tree_hashes(out)["raw\\00005.json" if os.sep == "\\" else "raw/00005.json"]
        prov2 = RN.MockProvider(T10.good)
        s = self.resume(out, ev, au, self.write_ra(out), prov2)
        self.assertEqual((s["status"], s["recorded_calls"]), ("RUN_COMPLETE", 18))
        self.assertEqual((prov1.calls, prov2.calls), (5, 13))                      # call 5 reached the provider once and is not called again
        self.assertEqual(LR.tree_hashes(out)["raw\\00005.json" if os.sep == "\\" else "raw/00005.json"], raw5)   # the persisted record is untouched
        ev5 = [(e["event"], e["call_index"]) for e in ledger_of(out) if e.get("call_index") in (5,) or e["event"] in ("resume", "reconcile")]
        self.assertEqual(ev5, [("intent", 5), ("resume", 6), ("reconcile", 5), ("raw", 5), ("classified", 5)])
        self.assertEqual(len({c["call_key"] for c in calls_of(out)}), 18)
        P, st = IG.verify_run(out, BUILD)
        self.assertEqual(P, [])
        self.assertEqual((st["resumes"], st["reconciled_calls"]), (1, [5]))

    def test_calls_line_missing_is_reconciled(self):
        out, ev, au, prov1 = self.interrupted_pilot(patch=self.kill_on_calls_write(5))
        self.assertEqual(len(calls_of(out)), 4)
        self.assertIn(("raw", 5), [(e["event"], e["call_index"]) for e in ledger_of(out)])
        prov2 = RN.MockProvider(T10.good)
        s = self.resume(out, ev, au, self.write_ra(out), prov2)
        self.assertEqual((s["status"], prov1.calls + prov2.calls), ("RUN_COMPLETE", 18))
        self.assertEqual(IG.verify_run(out, BUILD)[0], [])

    def test_classified_entry_missing_is_reconciled(self):
        out, ev, au, prov1 = self.interrupted_pilot(patch=self.kill_on_event("classified", 5))
        prov2 = RN.MockProvider(T10.good)
        s = self.resume(out, ev, au, self.write_ra(out), prov2)
        self.assertEqual((s["status"], prov1.calls + prov2.calls), ("RUN_COMPLETE", 18))
        self.assertEqual(IG.verify_run(out, BUILD)[0], [])

    def test_two_interruptions_two_resumes_form_one_chain(self):
        out, ev, au, p1 = self.interrupted_pilot(patch=self.kill_on_event("raw", 5))
        ra = self.write_ra(out, "raA")
        p2 = RN.MockProvider(T10.good)
        with self.kill_on_event("classified", 9), self.assertRaises(KeyboardInterrupt):
            self.resume(out, ev, au, ra, p2)
        p3 = RN.MockProvider(T10.good)
        s = self.resume(out, ev, au, self.write_ra(out, "raB"), p3)
        self.assertEqual(s["status"], "RUN_COMPLETE")
        self.assertEqual(p1.calls + p2.calls + p3.calls, 18)
        P, st = IG.verify_run(out, BUILD)
        self.assertEqual((P, st["resumes"]), ([], 2))
        self.assertEqual([r["resume_number"] for r in s["resumes"]], [1, 2])
        self.assertEqual([(r["persisted_calls"], r["reconciles_call"]) for r in s["resumes"]], [(5, 5), (9, 9)])
        self.assertEqual(len({r["previous_ledger_head"] for r in s["resumes"]}), 2)                        # each resume continues from a different chain head
        self.assertEqual(len({c["call_key"] for c in calls_of(out)}), 18)

    def test_a_finished_run_that_only_lost_its_marker_is_finalised_without_any_call(self):
        ev, au = self.pilot_files()
        out = os.path.join(self.tmp, "nomarker")
        with redirect_stdout(io.StringIO()):
            RN.run("pilot_round_1", BUILD, out, RN.MockProvider(T10.good), evidence_path=ev, auth_path=au, sleeper=lambda x: None, verify_build=False)
        os.remove(os.path.join(out, "RUN_COMPLETE"))                       # as if the process died after the last classified entry
        prov = RN.MockProvider(T10.good)
        s = self.resume(out, ev, au, self.write_ra(out), prov)
        self.assertEqual((s["status"], s["recorded_calls"], prov.calls), ("RUN_COMPLETE", 18, 0))
        self.assertEqual(IG.verify_run(out, BUILD)[0], [])


class TestResumeRefusals(Base):
    def prepared(self):
        out, ev, au, _ = self.interrupted_pilot(patch=self.kill_on_event("raw", 5))
        return out, ev, au

    def test_authorization_conditions(self):
        out, ev, au = self.prepared()
        cases = {
            "not owner": ({"authorized_by": "assistant"}, "not written by the owner"),
            "wrong scope": ({"scope": "main"}, "another scope"),
            "wrong run": ({"run_id": "0" * 16}, "another run"),
            "stale head": ({"ledger_head_sha256": "f" * 64}, "current ledger head"),
            "bad count": ({"remaining_calls": 14}, "remaining_calls"),
            "bool count": ({"remaining_calls": True}, "remaining_calls"),
            "wrong ceiling": ({"cost_ceiling_usd": 1000}, "cost ceiling"),
            "no acknowledgement": ({"acknowledges_unspecified_basis": False}, "acknowledges_unspecified_basis"),
            "wrong basis": ({"resume_basis": "transport_halt"}, "requires resume_basis"),
            "unknown basis": ({"resume_basis": "whatever"}, "resume_basis must be"),
        }
        for name, (over, text) in cases.items():
            with self.subTest(name):
                self.assert_refused(out, ev, au, self.write_ra(out, "ra_" + name.replace(" ", "_"), **over), text)
        with self.subTest("missing file"):
            self.assert_refused(out, ev, au, os.path.join(self.tmp, "nowhere.json"), "resume authorization file missing")

    def test_mismatch_of_authorization_evidence_fz_settings_or_provider_refuses(self):
        out, ev, au = self.prepared()
        ra = self.write_ra(out)
        au2 = os.path.join(self.tmp, "au_other.json")
        d = json.loads(PF.rb(au))
        d["input_tokens_per_call_assumed"] = 1017
        PF.wb(au2, (json.dumps(d) + "\n").encode())
        self.assert_refused(out, ev, au2, ra, "authorization file differs")
        ev2 = os.path.join(self.tmp, "ev_other.json")
        e = json.loads(PF.rb(ev))
        e["human_blind_check"]["worksheet_sha256"] = "b" * 64
        PF.wb(ev2, (json.dumps(e) + "\n").encode())
        self.assert_refused(out, ev2, au, ra, "evidence file differs")
        fz2 = os.path.join(self.tmp, "fz_copy.json")
        PF.wb(fz2, PF.rb(RN.FZ_PATH) + b"\n")
        with mock.patch.object(RN, "FZ_PATH", fz2):
            self.assert_refused(out, ev, au, ra, "FZ-v1 file differs")
        self.assert_refused(out, ev, au, ra, "provider class differs", prov=OtherProvider(T10.good))

    def test_settings_differing_from_the_run_refuse(self):
        real = RN.check_gates

        def altered(*a, **k):
            return dict(real(*a, **k), timeout_s=181)
        with mock.patch.object(RN, "check_gates", altered):
            out, ev, au, _ = self.interrupted_pilot(patch=self.kill_on_event("raw", 5))
        self.assert_refused(out, ev, au, self.write_ra(out), "settings differ")

    def test_complete_run_and_runs_without_provenance_cannot_be_resumed(self):
        ev, au = self.pilot_files()
        out = os.path.join(self.tmp, "done")
        with redirect_stdout(io.StringIO()):
            RN.run("pilot_round_1", BUILD, out, RN.MockProvider(T10.good), evidence_path=ev, auth_path=au, sleeper=lambda x: None, verify_build=False)
        self.assert_refused(out, ev, au, self.write_ra(out, remaining_calls=0), "COMPLETE")
        legacy = os.path.join(self.tmp, "legacy")
        shutil.copytree(out, legacy)
        p = os.path.join(legacy, "ledger.jsonl")
        PF.wb(p, b"\n".join([l for l in PF.rb(p).split(b"\n") if l][1:]) + b"\n")
        os.remove(os.path.join(legacy, "RUN_COMPLETE"))
        with self.assertRaises(RS.ResumeRefused) as cm:
            self.resume(legacy, ev, au, os.path.join(self.tmp, "x.json"), RN.MockProvider(T10.good))
        self.assertIn("provenance", " ".join(cm.exception.reasons))

    def test_damaged_files_refuse_with_a_diagnosis_and_change_nothing(self):
        def tail(name):
            def m(d):
                p = os.path.join(d, name)
                PF.wb(p, PF.rb(p)[:-40])
            return m
        damage = {
            "ledger last line truncated": (tail("ledger.jsonl"), "truncated"),
            "calls last line truncated": (tail("calls.jsonl"), "truncated"),
            "complete raw file deleted": (lambda d: os.remove(os.path.join(d, "raw", "00002.json")), "raw file of call 2 is missing"),
            "pending raw file garbage": (lambda d: PF.wb(os.path.join(d, "raw", "00005.json"), b"{not json"), "not a valid record"),
            "extra raw file": (lambda d: PF.wb(os.path.join(d, "raw", "00099.json"), b"{}"), "raw folder"),
        }
        for name, (mut, text) in damage.items():
            with self.subTest(name):
                out, ev, au = self.prepared()
                ra = self.write_ra(out, "ra_" + name.replace(" ", "_"))
                mut(out)
                self.assert_refused(out, ev, au, ra, text)


class TestCostStop(Base):
    def test_observed_cost_at_the_limit_halts_and_the_run_cannot_be_resumed(self):
        ev, au = self.pilot_files()
        out = os.path.join(self.tmp, "cost")
        seen = []

        def script(key, prompt):
            seen.append(key)
            r = T10.good(key, prompt)
            if len(seen) == 3:
                r["usage"] = {"promptTokenCount": 100, "totalTokenCount": 100 + 40_000_001}        # 40,000,001 output tokens ~ US$100.0000025
            return r
        with redirect_stdout(io.StringIO()):
            s = RN.run("pilot_round_1", BUILD, out, RN.MockProvider(script), evidence_path=ev, auth_path=au, sleeper=lambda x: None, verify_build=False)
        self.assertEqual((s["status"], s["recorded_calls"], len(seen)), ("RUN_INCOMPLETE", 3, 3))
        self.assertEqual(s["halt"], RN.COST_STOP_HALT)
        self.assertIn("observed cost reaches the OD-10 limit", IG.verify_run(out, BUILD)[0])
        self.assert_refused(out, ev, au, self.write_ra(out, basis="transport_halt", remaining_calls=15), "cost stop")

    def test_ordinary_usage_never_triggers_the_cost_stop(self):
        ev, au = self.pilot_files()
        out = os.path.join(self.tmp, "nocost")
        with redirect_stdout(io.StringIO()):
            s = RN.run("pilot_round_1", BUILD, out, RN.MockProvider(T10.good), evidence_path=ev, auth_path=au, sleeper=lambda x: None, verify_build=False)
        self.assertEqual((s["status"], s["halt"]), ("RUN_COMPLETE", None))


class TestMainRunTransportHalt(Base):
    def main_setup(self, days):
        ev, au = T10.TestRunner.files(self, "main", days=days)
        reg = json.loads(PF.rb(os.path.join(BUILD, "main", "registry.json")))["templates"]
        text = RN.D.call_list([t["id"] for t in reg], 2)
        rec = os.path.join(self.tmp, f"rec_{days}.json")
        PF.wb(rec, (json.dumps({"final_decision": "PASS", "seed": 20261030, "call_list_sha256": RN.sha(text.encode("ascii"))}) + "\n").encode())
        return ev, au, rec

    def run_main(self, days, script):
        ev, au, rec = self.main_setup(days)
        out = os.path.join(self.tmp, f"main{days}")
        prov = RN.MockProvider(script)
        with redirect_stdout(io.StringIO()):
            s = RN.run("main", BUILD, out, prov, evidence_path=ev, auth_path=au, pilot_record_path=rec, sleeper=lambda x: None, verify_build=False)
        return out, ev, au, rec, s, prov

    def ra(self, out, total=2496, **kw):
        return self.write_ra(out, scope="main", total=total, basis="transport_halt", **kw)

    def test_transport_only_halt_resumes_to_completion_without_repeating_any_call(self):
        seen = []

        def script(key, prompt):
            seen.append(key)
            if 3 <= len(seen) <= 7:
                return {"http_status": None, "text": "", "error": "TimeoutError"}
            return T10.good(key, prompt)
        out, ev, au, rec, s, p1 = self.run_main(60, script)
        self.assertEqual((s["status"], s["recorded_calls"]), ("RUN_INCOMPLETE", 7))
        self.assertIn("13.8", s["halt"])
        p2 = RN.MockProvider(T10.good)
        with redirect_stdout(io.StringIO()):
            s2 = RS.resume(out, BUILD, p2, evidence_path=ev, auth_path=au, resume_auth_path=self.ra(out), pilot_record_path=rec,
                           sleeper=lambda x: None, verify_build=False)
        self.assertEqual((s2["status"], s2["recorded_calls"], p1.calls + p2.calls), ("RUN_COMPLETE", 2496, 2496))      # each call exactly once in total
        self.assertEqual(len({c["call_key"] for c in calls_of(out)}), 2496)
        self.assertEqual(s2["resumes"][0]["counters_carried"], {"consecutive_sf": 5, "sf_total": 5, "completed": 7})
        self.assertEqual(os.listdir(os.path.join(out, "segments")), ["RUN_INCOMPLETE.segment1"])                      # earlier marker kept, not deleted
        P, st = IG.verify_run(out, BUILD)
        self.assertEqual((P, st["resumes"], st["status"]), ([], 1, "RUN_COMPLETE"))

    def test_counters_are_not_reset_by_a_resume(self):
        def fail(key, prompt):
            return {"http_status": None, "text": "", "error": "TimeoutError"}
        out, ev, au, rec, s, p1 = self.run_main(61, fail)
        self.assertEqual((s["recorded_calls"], s["status"]), (5, "RUN_INCOMPLETE"))
        p2 = RN.MockProvider(fail)
        with redirect_stdout(io.StringIO()):
            s2 = RS.resume(out, BUILD, p2, evidence_path=ev, auth_path=au, resume_auth_path=self.ra(out), pilot_record_path=rec, sleeper=lambda x: None, verify_build=False)
        self.assertEqual((s2["status"], s2["recorded_calls"], p2.calls), ("RUN_INCOMPLETE", 6, 1))        # the carried count of 5 makes the first new failure halt again
        self.assertEqual(IG.verify_run(out, BUILD)[0], [])

    def test_halt_caused_by_an_http_status_error_is_not_resumable(self):
        out, ev, au, rec, s, _ = self.run_main(62, lambda k, p: {"http_status": 503, "text": "", "error": "HTTP 503"})
        self.assertEqual(s["recorded_calls"], 5)
        self.assert_refused(out, ev, au, self.ra(out), "not transport-only", pilot_record_path=rec)

    def test_halt_caused_by_an_unlisted_exception_class_is_not_resumable(self):
        def script(key, prompt):
            raise RuntimeError("provider bug")                  # recorded as SF1 by the unchanged scoring, but not on the transport allow-list
        out, ev, au, rec, s, _ = self.run_main(63, script)
        self.assert_refused(out, ev, au, self.ra(out), "not transport-only", pilot_record_path=rec)


class TestCommandLine(Base):
    def test_cli_refuses_without_gate_evidence_and_never_calls_a_provider(self):
        out, ev, au, _ = self.interrupted_pilot(patch=self.kill_on_event("raw", 5))
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = RS.main(["--run", out, "--build", BUILD, "--evidence", os.path.join(self.tmp, "none.json"), "--authorization", au,
                          "--resume-authorization", os.path.join(self.tmp, "none2.json")])
        self.assertEqual(rc, 2)
        self.assertIn("GATE CLOSED", buf.getvalue())

    def test_cli_refuses_a_folder_with_no_provenance(self):
        ev, au = self.pilot_files()
        empty = os.path.join(self.tmp, "empty")
        os.makedirs(empty)
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = RS.main(["--run", empty, "--build", BUILD, "--evidence", ev, "--authorization", au, "--resume-authorization", os.path.join(self.tmp, "none.json")])
        self.assertEqual(rc, 2)
        self.assertIn("RESUME REFUSED", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
