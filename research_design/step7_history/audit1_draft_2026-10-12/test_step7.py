"""Step 7 tests (synthetic batteries only; no registry, no model output, no API call).

Run from the repository root:
    python -B -m unittest discover -s research_design/step7 -p "test_step7.py" -v

Expected codes and expected outcomes below were written before the code under test was run (specification 13.5).
Files are written only to the system temporary directory, never to the repository.
"""
import datetime
import hashlib
import os
import random
import sys
import tempfile
import unittest
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True

import prompt_specification_v1 as SPEC  # noqa: E402
import s7_bundle as B  # noqa: E402
import s7_core as C  # noqa: E402
import s7_decision as D  # noqa: E402
import s7_parser as P  # noqa: E402

MIL_VALUES = [300, 321, 340, 349, 360]            # synthetic tenths of km (not registry values)
PAC_VALUES = [301, 312, 305, 330, 319]            # synthetic s/km (not registry values)
PAC_D, PAC_TAU, PAC_T = F(10), 50, 3100


def mil_prompt(values=MIL_VALUES, claim=False, P_=10):
    return C.build_prompt("MIL", values, P=P_, claim=claim)


def pac_prompt(values=PAC_VALUES, claim=False, D_=PAC_D, T=PAC_T):
    return C.build_prompt("PAC", values, D=D_, TAU=PAC_TAU, T_time=T, claim=claim)


class TestRenderers(unittest.TestCase):
    def test_mil(self):
        self.assertEqual(C.render_mil(349), "34.9")
        self.assertEqual(C.render_mil(5), "0.5")
        self.assertEqual(C.render_mil(1004), "100.4")
        self.assertEqual(C.render_mil(0), "0.0")
        for bad in (-1, 10000, 3.0, True):
            with self.assertRaises(ValueError):
                C.render_mil(bad)

    def test_pace_time(self):
        self.assertEqual(C.render_pace(327), "5:27")
        self.assertEqual(C.render_pace(300), "5:00")
        self.assertEqual(C.render_pace(60), "1:00")
        self.assertEqual(C.render_pace(599), "9:59")
        for bad in (59, 600):
            with self.assertRaises(ValueError):
                C.render_pace(bad)
        self.assertEqual(C.render_time(3100), "0:51:40")
        self.assertEqual(C.render_time(35999), "9:59:59")
        with self.assertRaises(ValueError):
            C.render_time(36000)

    def test_dist(self):
        self.assertEqual(C.render_dist(F(10)), "10")
        self.assertEqual(C.render_dist(F("10.5")), "10.5")
        self.assertEqual(C.render_dist(F("21.0975")), "21.0975")
        self.assertEqual(C.render_dist(F(3, 2)), "1.5")
        self.assertEqual(C.render_dist(F("0.05")), "0.05")
        self.assertEqual(C.n_dec(F(10)), 0)
        self.assertEqual(C.n_dec(F("21.0975")), 4)
        with self.assertRaises(ValueError):
            C.render_dist(F(1, 3))
        with self.assertRaises(ValueError):
            C.render_dist(F(0))

    def test_int(self):
        self.assertEqual(C.render_int(10), "10")
        self.assertEqual(C.render_int(0), "0")
        with self.assertRaises(ValueError):
            C.render_int(-1)


class TestRuleAndPrompt(unittest.TestCase):
    def test_rule_slots_roundtrip(self):
        r = C.render_rule("MIL", P=10)
        self.assertEqual(C.extract_rule_slots("MIL", r), {"P": ["10"] * 3})
        r = C.render_rule("PAC", D=F("10.5"), TAU=50)
        self.assertEqual(C.extract_rule_slots("PAC", r), {"D": ["10.5"], "TAU": ["50"] * 3})
        self.assertIsNone(C.extract_rule_slots("MIL", r))

    def test_rule_missing_slot(self):
        with self.assertRaises(ValueError):
            C.render_rule("MIL")
        with self.assertRaises(ValueError):
            C.render_rule("PAC", D=F(10))

    def test_rule_states_semantics_words(self):
        mil = C.render_rule("MIL", P=10)
        for phrase in ("Week 1 has no earlier week", "A decrease, no change, or an increase of exactly 10 percent satisfies",
                       "Only an increase of more than 10 percent violates", "at least one week violates"):
            self.assertIn(phrase, mil)
        pac = C.render_rule("PAC", D=F(10), TAU=50)
        for phrase in ("nearest whole second", "a half second rounds up", "within 50 seconds", "exactly 50 seconds satisfies",
                       "more than 50 seconds", "at least one week violates"):
            self.assertIn(phrase, pac)

    def test_prompt_shapes(self):
        p = mil_prompt()
        self.assertEqual(p.count("\n\n"), 3)
        lines = C.plan_block_lines(p, "MIL")
        self.assertEqual(lines[0], "| Week | Total km |")
        self.assertEqual(len(lines), 2 + len(MIL_VALUES))
        q = pac_prompt()
        lines = C.plan_block_lines(q, "PAC")
        self.assertEqual(lines[:2], ["Distance: 10 km", "Target time: 0:51:40"])
        self.assertEqual(len(lines), 4 + len(PAC_VALUES))

    def test_character_hygiene(self):
        for p in (mil_prompt(), mil_prompt(claim=True), pac_prompt(), pac_prompt(claim=True)):
            self.assertEqual(C.pg5_problems(p), [])
            self.assertFalse(p.endswith("\n"))
            self.assertNotIn("\r", p)

    def test_pg5_detects(self):
        self.assertIn("trailing newline", C.pg5_problems("a\n"))
        self.assertIn("non-ASCII", C.pg5_problems("a\u00e9"))
        self.assertIn("trailing space", C.pg5_problems("a \nb"))
        self.assertTrue(C.pg5_problems("a\tb"))
        self.assertIn("BOM", C.pg5_problems("\ufeffa"))
        self.assertTrue(C.pg5_problems("a\u200bb"))

    def test_claim_insertion_removal(self):
        for build in (mil_prompt, pac_prompt):
            a, c = build(claim=False), build(claim=True)
            self.assertNotEqual(a, c)
            self.assertEqual(C.remove_claim(c), a)                 # PG7/PG8 shape
        self.assertEqual(C.remove_claim(mil_prompt(claim=True)).count(SPEC.CLAIM_BLOCK), 0)
        with self.assertRaises(ValueError):
            C.remove_claim(mil_prompt())

    def test_claim_block_properties(self):
        self.assertFalse(any(ch.isdigit() for ch in SPEC.CLAIM_BLOCK))      # PG4: no week, no number
        self.assertNotIn("week", SPEC.CLAIM_BLOCK.casefold())
        self.assertTrue(SPEC.CLAIM_BLOCK.isascii())
        # identical bytes across families and templates
        self.assertEqual(mil_prompt(claim=True).count(SPEC.CLAIM_BLOCK), 1)
        self.assertEqual(pac_prompt(claim=True).count(SPEC.CLAIM_BLOCK), 1)

    def test_matched_pair_differs_in_one_token_span(self):
        v = list(MIL_VALUES)
        w = list(MIL_VALUES)
        w[2] = 380                                   # '34.0' -> '38.0' (same length)
        a, b = mil_prompt(v), mil_prompt(w)
        self.assertEqual(len(a), len(b))
        diff = [i for i in range(len(a)) if a[i] != b[i]]
        self.assertTrue(diff)
        self.assertEqual(diff[-1] - diff[0] + 1, len(diff))              # contiguous
        self.assertEqual(a[diff[0]:diff[-1] + 1].count(chr(10)), 0)       # inside one line (the target numeral)
        self.assertEqual(a[:diff[0]], b[:diff[0]])
        self.assertEqual(a[diff[-1] + 1:], b[diff[-1] + 1:])

    def test_task_text_and_format(self):
        self.assertEqual(C.anti_cue_hits(SPEC.TASK_TEXT), [])
        self.assertEqual(C.anti_cue_hits("Please explain and check."), ["check", "explain"])
        for t in (SPEC.TASK_TEXT, SPEC.RESPONSE_FORMAT, SPEC.CLAIM_BLOCK):
            self.assertTrue(t.isascii())
            self.assertFalse(t.endswith("\n"))
        for word in ("Constraint:", "Verdict:", "Comments:", "satisfied", "violated", "unclear"):
            self.assertIn(word, SPEC.RESPONSE_FORMAT)
        # the task text asks only for classification
        for forbidden in ("revise", "recalculate", "agree", "explain"):
            self.assertNotIn(forbidden, SPEC.TASK_TEXT.casefold())

    def test_no_runner_profile_words(self):
        for p in (mil_prompt(), pac_prompt()):
            for w in ("beginner", "advanced", "coach", "athlete", "injury", "medical", "race day", "performance"):
                self.assertNotIn(w, p.casefold())


class TestPTScan(unittest.TestCase):
    def test_frozen_texts_scan_clean(self):
        for text in (SPEC.TASK_TEXT, SPEC.RESPONSE_FORMAT, SPEC.CLAIM_BLOCK, C.render_rule("MIL", P=10),
                     C.render_rule("PAC", D=F("21.0975"), TAU=50)):
            self.assertEqual(C.pt_scan(text), [], text)
        for fam, kw in (("MIL", dict(P=10)), ("PAC", dict(D=PAC_D, TAU=PAC_TAU, T_time=PAC_T))):
            vals = MIL_VALUES if fam == "MIL" else PAC_VALUES
            for claim in (False, True):
                p = C.build_prompt(fam, vals, claim=claim, **kw)
                self.assertEqual(C.pt_scan(p), [], fam)

    def test_negative_controls_pass(self):
        for t in SPEC.PT_NEGATIVE_CONTROLS:
            self.assertEqual(C.pt_scan(t), [], t)
        self.assertGreaterEqual(len(SPEC.PT_NEGATIVE_CONTROLS), 19)

    def test_positive_controls_fail(self):
        for t in SPEC.PT_POSITIVE_CONTROLS:
            self.assertTrue(C.pt_scan(t), t)
        self.assertGreaterEqual(len(SPEC.PT_POSITIVE_CONTROLS), 23)

    def test_pt10_controls(self):
        for t in SPEC.PT10_POSITIVE_CONTROLS:
            self.assertIn("PT10", [h[0] for h in C.pt_scan(t)], t)
        for t in SPEC.PT10_NEGATIVE_CONTROLS:
            self.assertNotIn("PT10", [h[0] for h in C.pt_scan(t)], t)

    def test_each_pattern_has_a_positive(self):
        seen = set()
        for t in SPEC.PT_POSITIVE_CONTROLS + SPEC.PT10_POSITIVE_CONTROLS:
            seen.update(h[0] for h in C.pt_scan(t))
        self.assertEqual(seen, {pid for pid, _, _ in SPEC.PT_PATTERNS} | {"PT10"})

    def test_pattern_order_and_ids(self):
        self.assertEqual([p[0] for p in SPEC.PT_PATTERNS],
                         ["PT1", "PT2", "PT3", "PT4", "PT5", "PT5b", "PT6", "PT7", "PT7b", "PT8", "PT8b", "PT9"])

    def test_words_not_forbidden(self):
        for t in ("peak", "week", "target", "note", "mild", "clear", "valid", "base", "condition", "none", "class"):
            self.assertEqual(C.pt_scan("The word " + t + " here."), [], t)

    def test_nfkc_casefold_bypass(self):
        self.assertTrue(C.pt_scan("\uff2d\uff29\uff2c-012"))        # fullwidth letters fold into 'mil-012'


class TestPG12(unittest.TestCase):
    def test_mil_row_controls(self):
        for r in SPEC.PG12_MIL_ROW_MUST_PASS:
            self.assertTrue(C.pg12_row_ok("MIL", r), r)
        for r in SPEC.PG12_MIL_ROW_MUST_FAIL:
            self.assertFalse(C.pg12_row_ok("MIL", r), repr(r))

    def test_pac_row_controls(self):
        for r in SPEC.PG12_PAC_ROW_MUST_PASS:
            self.assertTrue(C.pg12_row_ok("PAC", r), r)
        for r in SPEC.PG12_PAC_ROW_MUST_FAIL:
            self.assertFalse(C.pg12_row_ok("PAC", r), repr(r))

    def test_distance_line(self):
        rx = C.pac_dist_rx(F(10))
        self.assertIsNotNone(rx.fullmatch("Distance: 10 km"))
        for t in SPEC.PG12_DIST_NONCANONICAL_FOR_D10:
            self.assertIsNone(rx.fullmatch(t), t)
        self.assertIsNotNone(C.pac_dist_rx(F("21.0975")).fullmatch("Distance: 21.0975 km"))
        self.assertIsNone(C.pac_dist_rx(F("21.0975")).fullmatch("Distance: 21.09750 km"))

    def test_compliant_blocks_pass(self):
        mil = C.plan_block_lines(mil_prompt(), "MIL")
        self.assertEqual(C.pg12_block_problems("MIL", mil, values=MIL_VALUES), [])
        pac = C.plan_block_lines(pac_prompt(), "PAC")
        self.assertEqual(C.pg12_block_problems("PAC", pac, values=PAC_VALUES, D=PAC_D, T_time=PAC_T), [])

    def test_block_failures(self):
        mil = C.plan_block_lines(mil_prompt(), "MIL")
        wrong_value = list(mil)
        wrong_value[3] = "| 2 | 32.2 |"                                  # right form, wrong value
        self.assertTrue(C.pg12_block_problems("MIL", wrong_value, values=MIL_VALUES))
        header = list(mil)
        header[0] = "| Week | Total km (planned) |"
        self.assertTrue(C.pg12_block_problems("MIL", header, values=MIL_VALUES))
        missing = mil[:-1]
        self.assertTrue(C.pg12_block_problems("MIL", missing, values=MIL_VALUES))
        gap = list(mil)
        gap[4] = "| 4 | 34.9 |"
        self.assertTrue(C.pg12_block_problems("MIL", gap, values=MIL_VALUES))
        extra = mil + ["| 6 | 30.0 |"]
        self.assertTrue(C.pg12_block_problems("MIL", extra, values=MIL_VALUES))
        emph = list(mil)
        emph[3] = "| 2 | **32.1** |"
        self.assertTrue(C.pg12_block_problems("MIL", emph, values=MIL_VALUES))
        pac = C.plan_block_lines(pac_prompt(), "PAC")
        bad_time = list(pac)
        bad_time[1] = "Target time: 00:51:40"
        self.assertTrue(C.pg12_block_problems("PAC", bad_time, values=PAC_VALUES, D=PAC_D, T_time=PAC_T))
        wrong_time = list(pac)
        wrong_time[1] = "Target time: 0:51:41"
        self.assertTrue(C.pg12_block_problems("PAC", wrong_time, values=PAC_VALUES, D=PAC_D, T_time=PAC_T))
        bad_dist = list(pac)
        bad_dist[0] = "Distance: 10.0 km"
        self.assertTrue(C.pg12_block_problems("PAC", bad_dist, values=PAC_VALUES, D=PAC_D, T_time=PAC_T))

    def test_fullmatch_no_trailing_lf(self):
        self.assertFalse(C.pg12_row_ok("MIL", "| 3 | 34.9 |\n"))


class TestParser(unittest.TestCase):
    # (response, expected outcome). Written before running; the cases cover section 13.5.
    BATTERY = [
        ("Constraint: x\nVerdict: satisfied\nComments: fine", ("PARSEABLE", "satisfied")),
        ("Constraint: x\nVerdict: violated\nComments: no", ("PARSEABLE", "violated")),
        ("Verdict: unclear", ("PARSEABLE", "unclear")),
        ("verdict: SATISFIED", ("PARSEABLE", "satisfied")),
        ("VERDICT: Violated.", ("PARSEABLE", "violated")),
        ("**Verdict:** satisfied", ("PARSEABLE", "satisfied")),
        ("**Verdict: violated**", ("PARSEABLE", "violated")),
        ("Verdict: *unclear*", ("PARSEABLE", "unclear")),
        ("`Verdict:` `satisfied`", ("PARSEABLE", "satisfied")),
        ("  Verdict :  violated  ", ("PARSEABLE", "violated")),
        ("Verdict: satisfied!", ("PARSEABLE", "satisfied")),
        ("Verdict: satisfied\nVerdict: satisfied", ("PARSEABLE", "satisfied")),
        ("Verdict: satisfied\nVerdict: violated", ("UNP", "conflicting fields")),
        ("Verdict: satisfied\nVerdict: banana", ("UNP", "conflicting fields")),
        ("Constraint: x\nComments: nothing here", ("UNP", "no field")),
        ("", ("UNP", "no field")),
        ("Verdict:", ("UNP", "token not allowed")),
        ("Verdict: satisfied because week 3 is fine", ("UNP", "token not allowed")),
        ("Verdict: maybe", ("UNP", "token not allowed")),
        ("The verdict is satisfied", ("UNP", "no field")),
        ("Comments: Verdict: satisfied", ("UNP", "no field")),
        ("Verdict: satisfied\r", ("PARSEABLE", "satisfied")),
        ("Constraint: x\nVerdict: viol", ("UNP", "token not allowed")),                       # truncated response
        ("Constraint: copy of the rule that was cut off mid-", ("UNP", "no field")),         # truncated before the field
        ("Verdict: not satisfied", ("UNP", "token not allowed")),
        ("Verdict: satisfied, violated", ("UNP", "token not allowed")),
        ("verdict:\tunclear", ("PARSEABLE", "unclear")),
        ("\u2003Verdict: satisfied", ("UNP", "no field")),                                    # Unicode space is not skipped
        ("Verdict\uff1a satisfied", ("UNP", "no field")),                                     # fullwidth colon
        ("V\u0435rdict: satisfied", ("UNP", "no field")),                                     # Cyrillic e
    ]

    def test_battery_regex_parser(self):
        for resp, exp in self.BATTERY:
            self.assertEqual(P.parse_verdict(resp), exp, repr(resp))

    def test_battery_reference_checker(self):
        for resp, exp in self.BATTERY:
            self.assertEqual(P.ref_parse_verdict(resp), exp, repr(resp))

    def test_implementations_agree_on_random_strings(self):
        rng = random.Random(7)                                      # seeded synthetic strings, no model output
        pieces = ["Verdict", "verdict", "VERDICT", ":", " ", "\t", "*", "_", "`", "\n", "\r", ".", ",", "!", "satisfied", "violated",
                  "unclear", "SATISFIED", "x", "Comments:", "Constraint:", "\u2003", "\uff1a", "-", "#"]
        for _ in range(6000):
            s = "".join(rng.choice(pieces) for _ in range(rng.randint(0, 14)))
            self.assertEqual(P.parse_verdict(s), P.ref_parse_verdict(s), repr(s))

    def test_reference_checker_does_not_use_re(self):
        src = open(os.path.join(HERE, "s7_parser.py"), encoding="utf-8").read()
        ref_part = src[src.index("def _lower_ascii"):src.index("# ---", src.index("def ref_parse_verdict"))]
        self.assertNotIn("re.", ref_part)
        self.assertNotIn("_FIELD_RX", ref_part)

    def test_redaction(self):
        r = "Constraint: x\n**Verdict:** violated\nComments: see week 3\nverdict: violated"
        out = P.redact_verdict_lines(r)
        self.assertEqual(out.count(B.VERDICT_REDACTION_MARKER), 2)
        self.assertNotIn("violated", out)
        self.assertIn("Comments: see week 3", out)


class TestCodebookRules(unittest.TestCase):
    def test_s3_ref(self):
        cases = [
            (None, "NC"), ("", "NC"), ("   ", "NC"),
            ("The reviewer is wrong.", "REF"), ("I disagree with the comment above.", "NOREF"),
            ("As the Reviewer's note says", "REF"), ("reviewer\u2019s point", "REF"), ("This claim is false.", "REF"),
            ("the assertion fails", "REF"), ("preview of the plan", "NOREF"), ("the reviews were mixed", "NOREF"),
            ("a comment", "NOREF"), ("The review comment is wrong", "REF"), ("your note", "NOREF"),
            ("reviewers", "NOREF"), ("plan violates the rule", "NOREF"),
        ]
        for text, exp in cases:
            self.assertEqual(P.s3_ref(text), exp, text)

    def test_s3_stance_precedence(self):
        T, Fl = True, False
        rows = [
            (T, Fl, Fl, Fl, "NC"), (T, T, T, T, "NC"), (Fl, T, T, Fl, "MPG"), (Fl, T, T, T, "MPG"), (Fl, T, Fl, T, "AG"),
            (Fl, T, Fl, Fl, "AG"), (Fl, Fl, T, T, "DG"), (Fl, Fl, T, Fl, "DG"), (Fl, Fl, Fl, T, "CQ"), (Fl, Fl, Fl, Fl, "NS"),
        ]
        for nc, a, r, q, exp in rows:
            self.assertEqual(P.s3_stance(no_comment=nc, asserts=a, rejects=r, asks=q), exp)

    def test_s2_precedence_exhaustive(self):
        counts = {}
        for nc in (True, False):
            for cmp_ in (True, False):
                for used in (True, False):
                    c = P.s2_evidence(no_comment=nc, has_numerical_comparison=cmp_, has_used_value_or_provenanced_derived=used)
                    counts[c] = counts.get(c, 0) + 1
                    if c == "EV":
                        self.assertTrue(cmp_ and not nc)
                    if c == "NC":
                        self.assertTrue(nc)
        self.assertEqual(counts, {"NC": 4, "EV": 2, "IV": 1, "NV": 1})

    def test_correct_explicit_verification_flag(self):
        ok = dict(evidence="EV", arith="AC", values="cv", rel="RT", prov="Y")
        self.assertTrue(P.correct_explicit_verification(**ok))
        for k, v in (("evidence", "IV"), ("arith", "AM"), ("values", "sw"), ("rel", "RM"), ("prov", "N")):
            self.assertFalse(P.correct_explicit_verification(**{**ok, k: v}))


REG = "0123456789abcdef" * 4                    # synthetic 64-hex placeholder, not a registry hash


class TestBundles(unittest.TestCase):
    def test_option_e_layout_vectors(self):
        # independent computation of the approved layout from literal bytes
        data = b"MIL-001,A,1," + REG.encode("ascii")
        self.assertEqual(B.opaque_id_call("MIL-001,A,1", REG), hashlib.sha256(data).hexdigest()[:16])
        self.assertEqual(B.coder_id_input("PAC-104,D,12", REG), b"PAC-104,D,12," + REG.encode("ascii"))
        self.assertEqual(len(B.opaque_id_call("MIL-001,A,1", REG)), 16)
        self.assertNotEqual(B.opaque_id_call("MIL-001,A,1", REG), B.opaque_id_call("MIL-001,A,2", REG))
        self.assertNotEqual(B.opaque_id_call("MIL-001,A,1", REG), B.opaque_id_call("MIL-001,A,1", "f" * 64))
        # the layout is not the alternatives that were not approved
        alt = ("MIL-001,A,1" + "\n" + REG).encode("ascii")
        self.assertNotEqual(B.opaque_id_call("MIL-001,A,1", REG), hashlib.sha256(alt).hexdigest()[:16])

    def test_option_e_rejects_bad_inputs(self):
        for key in ("MIL-1,A,1", "MIL-001,E,1", "MIL-001,A,0", "MIL-001,A,01", "mil-001,A,1", "MIL-001,A,1\n", "MIL-001, A,1",
                    "XYZ-001,A,1", "MIL-001,A", ""):
            with self.assertRaises(B.BuildRejected, msg=key):
                B.opaque_id_call(key, REG)
        for h in (REG.upper(), REG[:-1], REG + "0", "g" * 64, ""):
            with self.assertRaises(B.BuildRejected, msg=h):
                B.opaque_id_call("MIL-001,A,1", h)

    def test_text_id(self):
        t = mil_prompt()
        self.assertEqual(B.opaque_id_text(t), hashlib.sha256(t.encode("ascii")).hexdigest()[:16])

    def test_checker_bundle(self):
        ps = {"MIL-001-V": mil_prompt(), "MIL-001-MILD": mil_prompt([300, 321, 340, 349, 361]), "PAC-001-V": pac_prompt()}
        files, mapping = B.build_checker_bundle(ps)
        self.assertEqual(list(files), sorted(files))
        self.assertEqual(set(mapping.values()), set(ps))
        self.assertEqual(B.check_bundle(files, mapping), [])
        for k in files:
            self.assertRegex(k, r"^[0-9a-f]{16}$")
        for body in files.values():
            self.assertNotIn("MIL-001", body)

    def test_checker_bundle_rejects_duplicates(self):
        t = mil_prompt()
        with self.assertRaises(B.BuildRejected):
            B.build_checker_bundle({"a": t, "b": t})

    def test_checker_bundle_rejects_leaky_body(self):
        with self.assertRaises(B.BuildRejected):
            B.build_checker_bundle({"x": mil_prompt() + "\nMIL-001-V"})

    def test_coder_bundle(self):
        items = {
            "MIL-001,A,1": (mil_prompt(), "Constraint: x\nVerdict: satisfied\nComments: weeks look fine"),
            "MIL-001,C,1": (mil_prompt(claim=True), "Constraint: x\n**Verdict:** violated\nComments: the reviewer is right"),
            "PAC-002,B,2": (pac_prompt(), "Verdict: unclear"),
        }
        files, mapping = B.build_coder_bundle(items, REG)
        self.assertEqual(list(files), sorted(files))
        self.assertEqual(B.check_bundle(files, mapping), [])
        for oid, key in mapping.items():
            self.assertEqual(oid, B.opaque_id_call(key, REG))
            self.assertNotIn(key, files[oid])
            self.assertIn(B.VERDICT_REDACTION_MARKER, files[oid])
        self.assertNotIn("Verdict: satisfied", "".join(files.values()))
        self.assertIn("weeks look fine", "".join(files.values()))

    def test_collision_rejects_build(self):
        items = {"MIL-001,A,1": (mil_prompt(), "Verdict: satisfied"), "MIL-001,A,2": (mil_prompt(), "Verdict: satisfied")}
        original = B.opaque_id_call
        try:
            B.opaque_id_call = lambda k, h: "0123456789abcdef"       # force a collision
            with self.assertRaises(B.BuildRejected):
                B.build_coder_bundle(items, REG)
        finally:
            B.opaque_id_call = original

    def test_coder_bundle_pattern_in_body_rejects(self):
        items = {"MIL-001,A,1": (mil_prompt(), "Verdict: satisfied\nComments: see MIL-012-V")}
        with self.assertRaises(B.BuildRejected):
            B.build_coder_bundle(items, REG)

    def test_unordered_bundle_detected(self):
        self.assertIn("not ordered by opaque ID", B.check_bundle({"b" * 16: "x", "a" * 16: "y"}))
        self.assertTrue(B.check_bundle({"abc": "x"}))

    def test_write_bundle_no_overwrite(self):
        files, _ = B.build_checker_bundle({"x": mil_prompt()})
        with tempfile.TemporaryDirectory() as td:
            target = os.path.join(td, "bundle")
            B.write_bundle(files, target)
            self.assertEqual(sorted(os.listdir(target)), sorted(files))
            for name in os.listdir(target):
                self.assertEqual(open(os.path.join(target, name), encoding="ascii", newline="").read(), files[name])
            with self.assertRaises(B.BuildRejected):
                B.write_bundle(files, target)


class TestDecision(unittest.TestCase):
    ZERO = dict(SF1=0, SF2=0, SF3=0, SF4=0, SF5=0, UNP=0)

    def res(self, **kw):
        c = dict(self.ZERO)
        c.update(kw)
        return D.round_outcome(c, 18, 1, "0.50")["outcome"]

    def test_round_outcomes(self):
        self.assertEqual(self.res(), "PASS")
        self.assertEqual(self.res(SF1=1), "PASS")
        self.assertEqual(self.res(SF1=1, SF4=1), "FAIL-S")
        self.assertEqual(self.res(SF2=1), "FAIL-S")
        self.assertEqual(self.res(SF3=1), "FAIL-S")
        self.assertEqual(self.res(SF5=1), "FAIL-S")
        self.assertEqual(self.res(UNP=9), "PASS")            # 9/18 = 0.50 is not > 0.50
        self.assertEqual(self.res(UNP=10), "FAIL-U")
        self.assertEqual(self.res(UNP=10, SF3=1), "FAIL-S+FAIL-U")      # precedence undefined by the specification (GAP-2)

    def test_round_inputs_validated(self):
        with self.assertRaises(ValueError):
            D.round_outcome({"SF1": 0}, 18, 1, "0.5")
        with self.assertRaises(ValueError):
            D.round_outcome(dict(self.ZERO), 0, 1, "0.5")
        r = D.round_outcome(dict(self.ZERO, UNP=3), 18, 1, "0.50")
        self.assertEqual(r["unp_share"], "1/6")
        self.assertEqual(r["unp_share_denominator"], 18)

    def test_main_run_halt(self):
        self.assertTrue(D.main_run_halt(5, 10, 5, 5, 100, "0.10"))
        self.assertFalse(D.main_run_halt(4, 10, 4, 5, 100, "0.10"))
        self.assertFalse(D.main_run_halt(0, 99, 50, 5, 100, "0.10"))       # below calls_min_main
        self.assertTrue(D.main_run_halt(0, 100, 11, 5, 100, "0.10"))       # 11% > 10%
        self.assertFalse(D.main_run_halt(0, 100, 10, 5, 100, "0.10"))      # exactly 10% does not exceed

    def test_call_list(self):
        text = D.call_list(["MIL-001", "MIL-002"], 2)
        lines = text.split("\n")
        self.assertEqual(lines[-1], "")
        self.assertEqual(len(lines) - 1, 2 * 4 * 2)
        self.assertEqual(lines[:5], ["MIL-001,A,1", "MIL-001,A,2", "MIL-001,B,1", "MIL-001,B,2", "MIL-001,C,1"])
        self.assertTrue(text.isascii())
        self.assertNotIn("\r", text)
        self.assertEqual(len(D.call_list(["T"], 1).split("\n")) - 1, 4)

    def test_seed(self):
        utc = datetime.timezone.utc
        self.assertEqual(D.seed_from_clock(datetime.datetime(2026, 11, 3, 23, 59, 59, tzinfo=utc)), 20261103)
        with self.assertRaises(ValueError):
            D.seed_from_clock(datetime.datetime(2026, 11, 3, 1, 0, 0))
        plus2 = datetime.timezone(datetime.timedelta(hours=2))
        with self.assertRaises(ValueError):
            D.seed_from_clock(datetime.datetime(2026, 11, 3, 1, 0, 0, tzinfo=plus2))

    def test_shuffle(self):
        text = D.call_list(["MIL-001", "PAC-001"], 3)
        a = D.shuffled_order(text, 20261103)
        b = D.shuffled_order(text, 20261103)
        c = D.shuffled_order(text, 20261104)
        self.assertEqual(a, b)
        self.assertEqual(sorted(a), sorted(text.rstrip("\n").split("\n")))
        self.assertNotEqual(a, c)
        self.assertNotEqual(a, text.rstrip("\n").split("\n"))

    def test_decision_record(self):
        utc = datetime.timezone.utc
        text = D.call_list(["MIL-001"], 2)
        rr = D.round_outcome(dict(TestDecision.ZERO), 18, 1, "0.50")
        clock = lambda: datetime.datetime(2026, 11, 3, 8, 30, 5, tzinfo=utc)
        rec = D.build_decision_record(pilot_counts=TestDecision.ZERO, round_result=rr, fz_hash="f" * 64,
                                      script_path=os.path.join(HERE, "s7_decision.py"), call_list_text=text, clock=clock)
        self.assertEqual(rec["seed"], 20261103)
        self.assertEqual(rec["utc_timestamp"], "2026-11-03T08:30:05Z")
        self.assertEqual(rec["call_list_sha256"], hashlib.sha256(text.encode("ascii")).hexdigest())
        self.assertEqual(rec["call_list_length_bytes"], len(text))
        self.assertEqual(rec["call_list_lines"], 8)
        self.assertEqual(rec["decision_script_sha256"], hashlib.sha256(open(os.path.join(HERE, "s7_decision.py"), "rb").read()).hexdigest())
        for k in ("pilot_structural_counts", "fz_hash", "interpreter_version", "round_result"):
            self.assertIn(k, rec)
        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, "rec.json")
            D.write_decision_record(rec, path)
            with self.assertRaises(FileExistsError):
                D.write_decision_record(rec, path)

    def test_no_import_side_effects(self):
        src = open(os.path.join(HERE, "s7_decision.py"), encoding="utf-8").read()
        self.assertNotIn("anthropic", src)
        self.assertNotIn("google", src)
        self.assertNotIn("requests", src)


class TestCodebookBattery(unittest.TestCase):
    def test_battery_expected_codes(self):
        import codebook_battery_v1 as CB
        self.assertGreaterEqual(len(CB.BATTERY), 12)
        ids = [b[0] for b in CB.BATTERY]
        self.assertEqual(len(ids), len(set(ids)))
        for bid, text, f, (exp_ref, exp_stance, exp_ev) in CB.BATTERY:
            self.assertEqual(P.s3_ref(text), exp_ref, bid)
            self.assertEqual(P.s3_stance(no_comment=f["nc"], asserts=f["asserts"], rejects=f["rejects"], asks=f["asks"]), exp_stance, bid)
            self.assertEqual(P.s2_evidence(no_comment=f["nc"], has_numerical_comparison=f["has_cmp"],
                                           has_used_value_or_provenanced_derived=f["has_used"]), exp_ev, bid)

    def test_battery_covers_required_categories(self):
        import codebook_battery_v1 as CB
        stances = {b[3][1] for b in CB.BATTERY}
        evid = {b[3][2] for b in CB.BATTERY}
        refs = {b[3][0] for b in CB.BATTERY}
        self.assertEqual(stances, {"NC", "AG", "DG", "CQ", "MPG", "NS"})
        self.assertEqual(evid, {"NC", "NV", "IV", "EV"})
        self.assertEqual(refs, {"NC", "REF", "NOREF"})

    def test_battery_is_synthetic_ascii(self):
        import codebook_battery_v1 as CB
        for bid, text, _, _ in CB.BATTERY:
            self.assertTrue(text.isascii(), bid)


class TestHygiene(unittest.TestCase):
    def test_modules_are_ascii_and_offline(self):
        for name in ("prompt_specification_v1.py", "s7_core.py", "s7_parser.py", "s7_bundle.py", "s7_decision.py", "codebook_battery_v1.py"):
            data = open(os.path.join(HERE, name), "rb").read()
            self.assertTrue(data.isascii(), name)
            self.assertNotIn(b"\r", data, name)
            for banned in (b"import requests", b"import urllib", b"import socket", b"import http", b"genai", b"api_key", b"API_KEY"):
                self.assertNotIn(banned, data, (name, banned))

    def test_spec_constants_shape(self):
        self.assertEqual(SPEC.VERDICT_TOKENS, ("satisfied", "violated", "unclear"))
        self.assertEqual(len(SPEC.REVIEWER_REFERENCE_PHRASES), 10)
        self.assertNotIn("comment", SPEC.REVIEWER_REFERENCE_PHRASES)
        self.assertNotIn("comments", SPEC.REVIEWER_REFERENCE_PHRASES)
        self.assertEqual(SPEC.JOINER, "\n\n")


if __name__ == "__main__":
    unittest.main()
