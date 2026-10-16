"""Acceptance tests for the pilot decision derived from the TEXT of spec 13.6 (lines 828-834): "PASS: no SF2, no SF3, no SF5; SF1 + SF4 <= f_S; UNP share <= theta_unp"
and "FAIL-S: any SF2, SF3, SF5, or SF1 + SF4 > f_S". They do not depend on the unadopted primary order or on the per-call/per-flag unit of f_S
(MASTER_PREPILOT_RESOLUTION.md section 2): they only say that a call which meets SF2, SF3 or SF5 must make the round FAIL-S.
The rows that the current code gets wrong are marked expectedFailure: the suite stays green, the defect is documented, and when the counting rule
is adopted and patched (MASTER_IMPLEMENTATION_PLAN.md patch P1) these tests start to PASS ("unexpected success"), at which point the markers must be removed.
No code was changed. Mock records only. Run: python -B -I -W error::ResourceWarning -m unittest discover -s research_design/step10 -p test_sf_matrix_literal.py"""
import os
import sys
import unittest
from fractions import Fraction as F
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
import s10_runner as RN  # noqa: E402
import s10_scoring as SC  # noqa: E402

D = RN.D


def rec(**kw):
    r = {"response_text": "Verdict: satisfied", "error": None, "http_status": 200, "finish_reason": "STOP"}
    r.update(kw)
    return r


def pilot_outcome(bad, raise_in_parser=False):
    """Outcome of an 18-call pilot round: one record `bad`, 17 clean ones. f_S = 1, theta_unp = 0.50 (FZ-v1 row 18)."""
    recs = [rec() for _ in range(17)]
    if raise_in_parser:
        with mock.patch.object(SC.s7_parser, "parse_verdict", side_effect=lambda t: (_ for _ in ()).throw(ValueError("x")) if t == "BOOM" else ("PARSEABLE", "satisfied")):
            recs.append(dict(bad, response_text="BOOM"))
            pc = SC.pilot_counts(recs)
    else:
        recs.append(bad)
        pc = SC.pilot_counts(recs)
    return D.round_outcome(pc["counts"], pc["n_calls"], 1, F(1, 2), planned_calls=18)["outcome"]


class TestSingleFlagRows(unittest.TestCase):
    def test_single_flags_follow_the_text(self):
        self.assertEqual(pilot_outcome(rec(response_text="", error="HTTP 503", http_status=503)), "PASS")      # SF1 alone: soft 1 <= f_S
        self.assertEqual(pilot_outcome(rec(response_text="")), "FAIL-S")                                        # SF2
        self.assertEqual(pilot_outcome(rec(finish_reason="MAX_TOKENS")), "FAIL-S")                              # SF3
        self.assertEqual(pilot_outcome(rec(finish_reason="SAFETY")), "PASS")                                    # SF4 alone: soft
        self.assertEqual(pilot_outcome(rec(), raise_in_parser=True), "FAIL-S")                                  # SF5
        self.assertEqual(pilot_outcome(rec(finish_reason="MAX_TOKENS", response_text="")), "FAIL-S")            # SF3 + SF2 (both hard)

    def test_two_soft_failures_exceed_f_S(self):
        recs = [rec(response_text="", error="HTTP 503", http_status=503), rec(finish_reason="SAFETY")] + [rec() for _ in range(16)]
        pc = SC.pilot_counts(recs)
        self.assertEqual(D.round_outcome(pc["counts"], 18, 1, F(1, 2), planned_calls=18)["outcome"], "FAIL-S")


class TestHardFlagHiddenBySoftFlag(unittest.TestCase):
    """A call that meets a hard definition must make the round FAIL-S whatever other flag it also meets (spec 13.6 text)."""

    @unittest.expectedFailure
    def test_sf1_plus_sf3(self):
        self.assertEqual(pilot_outcome(rec(error="HTTP 500", http_status=500, finish_reason="MAX_TOKENS")), "FAIL-S")

    @unittest.expectedFailure
    def test_sf4_plus_sf3(self):
        self.assertEqual(pilot_outcome(rec(block_reason="SAFETY", finish_reason="MAX_TOKENS")), "FAIL-S")

    @unittest.expectedFailure
    def test_sf1_plus_sf5(self):
        self.assertEqual(pilot_outcome(rec(error="HTTP 500", http_status=500), raise_in_parser=True), "FAIL-S")

    @unittest.expectedFailure
    def test_sf4_plus_sf5(self):
        self.assertEqual(pilot_outcome(rec(block_reason="SAFETY"), raise_in_parser=True), "FAIL-S")

    @unittest.expectedFailure
    def test_sf1_plus_sf3_plus_sf5(self):
        self.assertEqual(pilot_outcome(rec(error="HTTP 500", http_status=500, finish_reason="MAX_TOKENS"), raise_in_parser=True), "FAIL-S")

    @unittest.expectedFailure
    def test_sf4_plus_sf3_plus_sf5(self):
        self.assertEqual(pilot_outcome(rec(block_reason="SAFETY", finish_reason="MAX_TOKENS"), raise_in_parser=True), "FAIL-S")


class TestFlagsAreAlwaysRecorded(unittest.TestCase):
    def test_all_flags_are_detected_even_when_the_count_hides_them(self):
        self.assertEqual(SC.classify(rec(error="HTTP 500", http_status=500, finish_reason="MAX_TOKENS"))["flags"], ["SF1", "SF3"])
        self.assertEqual(SC.classify(rec(block_reason="SAFETY", finish_reason="MAX_TOKENS"))["flags"], ["SF4", "SF3"])
        pc = SC.pilot_counts([rec(error="HTTP 500", http_status=500, finish_reason="MAX_TOKENS")])
        self.assertEqual(pc["multi_flag_calls"], 1)                                   # the multi-flag call is at least reported


class TestUnknownUnit(unittest.TestCase):
    def test_sf1_plus_sf4_outcome_depends_on_the_unadopted_unit(self):
        bad = rec(error="HTTP 500", http_status=500, block_reason="SAFETY")
        self.assertEqual(SC.classify(bad)["flags"], ["SF1", "SF4"])
        self.assertEqual(pilot_outcome(bad), "PASS")          # counted per call (current); per flag it would be 2 > f_S = 1: UNRESOLVED until adopted


if __name__ == "__main__":
    unittest.main()
