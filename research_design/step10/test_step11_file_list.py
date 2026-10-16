"""INACTIVE proposal P13 (owner decision pending): guard test for the file list of s11_final_freeze_manifest.py.
Copy to research_design/step10/test_step11_file_list.py ONLY together with the diff P13_step11_file_list.diff.INACTIVE.
It builds the manifest from a SYNTHETIC PASS record (written to a temporary folder; it is not a decision record) and requires that every project module
reachable by import from the run lifecycle (runner, resume, integrity, pilot glue, report, coding, evidence evaluator, build verifier) is hashed.
Run: python -B -I -m unittest discover -s research_design/step10 -p test_step11_file_list.py"""
import ast
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
RD = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
import s11_final_freeze_manifest as FM  # noqa: E402

ENTRY = ["step10/s10_runner.py", "step10/s10_resume.py", "step10/s10_integrity.py", "step10/s11_pilot.py", "step10/s10_report.py", "step10/s12_cli.py",
         "step10/s11_final_freeze_manifest.py", "step9/s9_blindcheck.py", "step8/s8_verify.py"]
DIRS = ["step7", "step8", "step9", "step10", "implementation_a"]


def project_modules():
    mods = {}
    for d in DIRS:
        for f in os.listdir(os.path.join(RD, d)):
            if f.endswith(".py") and not f.startswith("test_"):
                mods.setdefault(f[:-3], []).append(f"{d}/{f}")
    return mods


def reachable():
    mods, seen, todo = project_modules(), set(), list(ENTRY)
    while todo:
        p = todo.pop()
        if p in seen:
            continue
        seen.add(p)
        tree = ast.parse(open(os.path.join(RD, p), encoding="utf-8").read())
        names = set()
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                names |= {a.name.split(".")[0] for a in n.names}
            elif isinstance(n, ast.ImportFrom) and n.module:
                names.add(n.module.split(".")[0])
        for m in names & set(mods):
            todo += mods[m]
    return seen


def hashed_files(build=FM.build):
    tmp = tempfile.mkdtemp()
    rec = os.path.join(tmp, "synthetic_record.json")
    with open(rec, "w") as f:
        json.dump({"final_decision": "PASS", "seed": 1, "call_list_sha256": "0" * 64}, f)
    return set(build(rec)["files"])


class TestFileListCoversTheRunLifecycle(unittest.TestCase):
    def test_every_reachable_module_is_hashed(self):
        missing = sorted(reachable() - hashed_files())
        self.assertEqual(missing, [], "modules reachable from the run lifecycle but not in the final freeze manifest")

    def test_proposals_that_are_not_adopted_are_not_hashed(self):
        files = hashed_files()
        self.assertNotIn("step7/s7_outcomes.py", files)                     # PROPOSED 18.2 policy, not adopted
        self.assertFalse([f for f in files if "/test_" in f])               # tests are verification evidence, not part of the freeze set


if __name__ == "__main__":
    unittest.main()
