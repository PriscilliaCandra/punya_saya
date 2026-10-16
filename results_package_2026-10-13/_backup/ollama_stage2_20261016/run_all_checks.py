"""One command that re-runs every read-only check of the package and prints a table with exit codes. Writes nothing, makes no network call.
Usage (repository root): python -B -I results_package_2026-10-13/reproduce/run_all_checks.py [--quick]   (--quick skips the slow Step 8 suite, about 3 minutes)"""
import os
import subprocess
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
BUILD = "research_design/step8_output/step8_build_7a6bbe465c66"
PY = [sys.executable, "-B", "-I"]
UT = ["-W", "error::ResourceWarning", "-m", "unittest", "discover", "-s"]
CHECKS = [
    ("stage evidence hashes (Stage 1/2)", PY + ["results_package_2026-10-13/reproduce/verify_stage_evidence.py"], False),
    ("Stage 2 headline recomputation", PY + ["results_package_2026-10-13/reproduce/recompute_stage2.py", "pilot_clarification/runs/stage2_gemini_20261008T035839Z"], False),
    ("Step 4 tests (Implementation A)", PY + UT + ["research_design/implementation_a", "-p", "test_impl_a.py"], False),
    ("Step 7 tests", PY + UT + ["research_design/step7", "-p", "test_step7.py"], False),
    ("Step 8 independent verifier", PY + ["research_design/step8/s8_verify.py", BUILD], False),
    ("Implementation B on the build", PY + ["research_design/step9/impl_b.py", BUILD], False),
    ("Implementation B tests", PY + UT + ["research_design/step9", "-p", "test_impl_b.py"], False),
    ("blind-check evaluator tests", PY + UT + ["research_design/step9", "-p", "test_blindcheck.py"], False),
    ("Step 10 tests", PY + UT + ["research_design/step10", "-p", "test_step10.py"], False),
    ("post-run coding tests", PY + UT + ["research_design/step10", "-p", "test_s12.py"], False),
    ("pilot glue and integrity tests", PY + UT + ["research_design/step10", "-p", "test_pilot_flow.py"], False),
    ("pre-pilot fix tests", PY + UT + ["research_design/step10", "-p", "test_prepilot_fixes.py"], False),
    ("provider response tests", PY + UT + ["research_design/step10", "-p", "test_provider_response.py"], False),
    ("input limit acceptance tests (P3)", PY + UT + ["research_design/step10", "-p", "test_input_limit.py"], False),
    ("SF acceptance tests (P1)", PY + UT + ["research_design/step10", "-p", "test_sf_matrix_literal.py"], False),
    ("SF2 detection acceptance tests (option B working decision, C-31)", PY + UT + ["research_design/step10", "-p", "test_sf2_detection.py"], False),
    ("ledger / interrupted-run characterization tests", PY + UT + ["research_design/step10", "-p", "test_ledger_resilience.py"], False),
    ("SF2 variant analysis tests (C-31 decision table)", PY + UT + ["research_design/step10", "-p", "test_sf2_variants.py"], False),
    ("disruption scenario tests (mock provider)", PY + UT + ["research_design/step10", "-p", "test_disruption_scenarios.py"], False),
    ("resume / provenance / cost-stop tests (mock provider; MD-08 not adopted)", PY + UT + ["research_design/step10", "-p", "test_resume.py"], False),
    ("adversarial P8 regression tests (mock provider)", PY + UT + ["research_design/step10", "-p", "test_adversarial_p8.py"], False),
    ("MD-06 safe-stop tests (mock provider)", PY + UT + ["research_design/step10", "-p", "test_safe_stop.py"], False),
    ("P5 FZ index tool tests (synthetic files)", PY + UT + ["research_design/step10", "-p", "test_fz_index.py"], False),
    ("E-1 FZ index enforcement tests (mock provider)", PY + UT + ["research_design/step10", "-p", "test_fz_enforcement.py"], False),
    ("H1 waiver gate tests (mock provider)", PY + UT + ["research_design/step10", "-p", "test_h1_waiver.py"], False),
    ("P13 Step 11 file list guard", PY + UT + ["research_design/step10", "-p", "test_step11_file_list.py"], False),
    ("human worksheet format pre-check tests (synthetic)", PY + UT + ["results_package_2026-10-13/reproduce", "-p", "test_precheck_human_sheets.py"], False),
    ("Step 8 tests (slow)", PY + UT + ["research_design/step8", "-p", "test_step8.py"], True),
    ("gate status (expected: CLOSED until human evidence exists)", PY + ["research_design/step10/s10_runner.py", "--scope", "pilot_round_1", "--build", BUILD,
                                                                      "--out", "unused", "--evidence", "results_package_2026-10-13/templates/none.json",
                                                                      "--authorization", "results_package_2026-10-13/templates/owner_authorization_TEMPLATE.json"], False),
]


def main():
    quick = "--quick" in sys.argv
    bad = 0
    for name, cmd, slow in CHECKS:
        if slow and quick:
            print(f"{'SKIPPED':8} {name}")
            continue
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        gate = name.startswith("gate status")
        ok = (r.returncode == 2) if gate else (r.returncode == 0)
        bad += not ok
        print(f"{'OK' if ok else 'FAILED':8} exit={r.returncode} {name}")
    print("ALL CHECKS AS EXPECTED" if not bad else f"{bad} check(s) not as expected")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
