"""Tests of precheck_human_sheets.py with SYNTHETIC sheets (ids and printed synthetic comments are taken from the blank kits; every judgment value below is invented
for the test and is not a registry value or an expected code). No registry content is read.
Run: python -B -I -W error::ResourceWarning -m unittest discover -s results_package_2026-10-13/reproduce -p test_precheck_human_sheets.py"""
import builtins
import csv
import io
import os
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
import precheck_human_sheets as PC  # noqa: E402


def read_blank(path):
    return PC.read(path)


def write(path, header, rows):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def mil(r):
    r.update({"P_or_D_dist": "10%", "verdict_satisfied_violated_unclear": "satisfied"})
    for w in range(1, 6):
        r[f"w{w}_transcribed"] = "30.0"
        r[f"w{w}_value"] = "30.0"
        if w == 1:
            r["w1_status"] = "uncompared"
        else:
            r[f"w{w}_increase_km_or_implied_finish_s_2dp"] = "2.0"
            r[f"w{w}_limit_km_2dp_or_rounded_finish_s"] = "3.00"
            r[f"w{w}_percent_2dp_or_diff_s"] = "6.67"
            r[f"w{w}_status"] = "not over cap"
    return r


def pac(r):
    r.update({"P_or_D_dist": "10 km", "T_time_displayed": "0:50:00", "T_time_seconds": "3000", "tau_F": "50", "verdict_satisfied_violated_unclear": "satisfied"})
    for w in range(1, 6):
        r[f"w{w}_transcribed"] = "5:00"
        r[f"w{w}_value"] = "300"
        r[f"w{w}_increase_km_or_implied_finish_s_2dp"] = "3000.00"
        r[f"w{w}_limit_km_2dp_or_rounded_finish_s"] = "3000"
        r[f"w{w}_percent_2dp_or_diff_s"] = "0"
        r[f"w{w}_status"] = "not"
    return r


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="pc_")
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def run_main(self, kind, rows, header):
        p = os.path.join(self.tmp, "sheet.csv")
        write(p, header, rows)
        out = io.StringIO()
        with redirect_stdout(out):
            code = PC.main(["--kind", kind, "--sheet", p])
        return code, out.getvalue()


class TestBlindcheck(Base):
    def setUp(self):
        super().setUp()
        self.header, self.blank = read_blank(PC.KIT)

    def filled(self):
        rows = []
        for i, r in enumerate(self.blank):
            r = dict(r)
            rows.append(mil(r) if i % 2 == 0 else pac(r))
        return rows

    def test_blank_worksheet_is_not_filled_and_has_no_problem(self):
        code, out = self.run_main("blindcheck", [dict(r) for r in self.blank], self.header)
        self.assertEqual(code, 1)
        self.assertIn("not filled: 624", out)
        self.assertIn("problems: 0", out)

    def test_complete_synthetic_sheet_passes(self):
        code, out = self.run_main("blindcheck", self.filled(), self.header)
        self.assertEqual((code, "problems: 0" in out, "not filled: 0" in out), (0, True, True), out[-300:])

    def test_empty_required_cell_is_named_without_printing_cell_values(self):
        rows = self.filled()
        rows[0]["w3_value"] = ""
        rows[1]["tau_F"] = ""
        code, out = self.run_main("blindcheck", rows, self.header)
        self.assertEqual(code, 1)
        self.assertIn("empty required cell: w3_value", out)
        self.assertNotIn("6.67", out)
        self.assertNotIn("10%", out)

    def test_invalid_words_and_decimals(self):
        rows = self.filled()
        rows[0]["verdict_satisfied_violated_unclear"] = "yes"
        rows[0]["w1_status"] = "ok"
        rows[0]["w2_increase_km_or_implied_finish_s_2dp"] = "2"
        rows[0]["w3_limit_km_2dp_or_rounded_finish_s"] = "3.0"
        rows[0]["w4_status"] = "not"
        rows[1]["w2_status"] = "over cap"
        rows[1]["w3_increase_km_or_implied_finish_s_2dp"] = "3000.0"
        rows[2]["w2_percent_2dp_or_diff_s"] = "abc"
        code, out = self.run_main("blindcheck", rows, self.header)
        for part in ("verdict must be", "week 1 status must be 'uncompared'", "too few decimals (need 1): w2_increase", "too few decimals (need 2): w3_limit",
                     "week 4 status must be 'over cap' or 'not over cap'", "week 2 status must be '|e|>tau' or 'not'", "too few decimals (need 2): w3_increase", "not a number: w2_percent"):
            self.assertIn(part, out, part)
        self.assertEqual(code, 1)

    def test_week1_computed_cells_must_stay_empty_for_mileage_rows(self):
        rows = self.filled()
        rows[0]["w1_percent_2dp_or_diff_s"] = "0.00"
        self.assertIn("week 1 computed cell must stay empty", self.run_main("blindcheck", rows, self.header)[1])

    def test_unknown_duplicate_missing_ids_and_header(self):
        rows = self.filled()
        rows[0]["opaque_id"] = "ffffffffffffffff"
        rows[1]["opaque_id"] = rows[2]["opaque_id"]
        out = self.run_main("blindcheck", rows, self.header)[1]
        self.assertIn("ids differ", out)
        self.assertIn("duplicate opaque ids", out)
        bad_header = self.header[:-1]
        code, out = self.run_main("blindcheck", [{k: r[k] for k in bad_header} for r in self.filled()], bad_header)
        self.assertEqual(code, 1)
        self.assertIn("columns differ", out)

    def test_unusable_input_exit_2(self):
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(PC.main(["--kind", "blindcheck", "--sheet", os.path.join(self.tmp, "missing.csv")]), 2)


class TestRehearsal(Base):
    def setUp(self):
        super().setUp()
        self.header, self.blank = read_blank(PC.KIT_H4)

    def filled(self):
        rows = []
        for r in self.blank:
            r = dict(r)
            r.update({"s2_evidence": "ev", "s2_values": "cv", "s2_arith": "AC", "s3_stance": "ns", "s2_prov": "", "s2_rel": ""})
            r["s2_evidence"] = "EV"
            r["s2_rel"] = "RT"
            r["s2_prov"] = "Y"
            rows.append(r)
        return rows

    def test_blank_sheet_not_filled(self):
        code, out = self.run_main("rehearsal", [dict(r) for r in self.blank], self.header)
        self.assertEqual(code, 1)
        self.assertIn("not filled: 40", out)

    def test_valid_codes_case_insensitive_and_optional_cells(self):
        rows = self.filled()
        rows[0].update({"s2_prov": "", "s2_rel": "", "s2_evidence": "nc", "s2_values": "none"})
        code, out = self.run_main("rehearsal", rows, self.header)
        self.assertEqual((code, "problems: 0" in out), (0, True), out)

    def test_invalid_and_empty_required_codes(self):
        rows = self.filled()
        rows[0]["s2_evidence"] = "XX"
        rows[1]["s3_stance"] = ""
        rows[2]["s2_arith"] = "AX"
        code, out = self.run_main("rehearsal", rows, self.header)
        self.assertEqual(code, 1)
        self.assertIn("not an allowed code: s2_evidence", out)
        self.assertIn("empty required cell: s3_stance", out)
        self.assertIn("not an allowed code: s2_arith", out)

    def test_changed_comment_text_and_ids_are_flagged(self):
        rows = self.filled()
        rows[0]["comment_text"] = rows[0]["comment_text"] + " x"
        rows.pop()
        out = self.run_main("rehearsal", rows, self.header)[1]
        self.assertIn("comment_text was changed", out)
        self.assertIn("expected the 40 ids", out)


class TestItNeverOpensForbiddenFiles(Base):
    def test_only_the_sheet_and_the_blank_kits_are_opened(self):
        header, blank = read_blank(PC.KIT)
        rows = [mil(dict(r)) for r in blank]
        p = os.path.join(self.tmp, "sheet.csv")
        write(p, header, rows)
        opened = []
        real = builtins.open

        def spy(file, *a, **k):
            opened.append(str(file))
            return real(file, *a, **k)
        with mock.patch.object(builtins, "open", spy), redirect_stdout(io.StringIO()):
            PC.main(["--kind", "blindcheck", "--sheet", p])
        low = [o.replace("\\", "/").lower() for o in opened]
        for bad in ("checker_bundle", "mapping", "registry", "prompt", "codebook_battery", "gate_report"):
            self.assertFalse(any(bad in o for o in low), (bad, low))
        self.assertTrue(any(o.endswith("sheet.csv") for o in low))


if __name__ == "__main__":
    unittest.main()
