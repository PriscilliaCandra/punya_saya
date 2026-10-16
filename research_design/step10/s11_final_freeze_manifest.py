"""Step 11 'final freeze manifest' writer (specification 21.1 row 11) -- decision record 12.31. NOT RUN.
Lists the SHA-256 of the actual files that define the experiment at the time of the final pilot decision (specification, FZ-v1, Step 7 freeze
manifest and its files, Step 8 manifest, Implementation A and B, Step 10 code, the decision record of the script). It does NOT define an
'FZ hash' (proposal P-2 is not adopted): the decision script's supplied fz_hash stays 'researcher-supplied, unverified'. Refuses to
overwrite; refuses unless the decision record says final_decision PASS (a STOP / STOP-U record gets no freeze manifest).
Usage: python -B -I s11_final_freeze_manifest.py --decision-record <json> --out <new file>"""
import argparse, hashlib, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RD = os.path.normpath(os.path.join(HERE, ".."))
sys.dont_write_bytecode = True

def fsha(p):
    with open(p, "rb") as f: return hashlib.sha256(f.read()).hexdigest()

def build(record_path):
    with open(record_path, "rb") as f: rec = json.loads(f.read().decode("utf-8"))
    if rec.get("final_decision") != "PASS":
        raise ValueError("final pilot decision is not PASS: no final freeze manifest")
    rel = ["SCENARIO_CONSTRUCTION_SPECIFICATION_v2_7_DRAFT.md", "PARAMETER_FREEZE_MANIFEST_FZ_v1.json", "PARAMETER_JUSTIFICATION_RECORD_DRAFT.md",
           "METHODOLOGY_FREEZE_MANIFEST_v2_7.json", "step7/STEP7_PROMPT_SPECIFICATION_FREEZE_MANIFEST_v1.json", "implementation_a/impl_a.py", "step9/impl_b.py",
           "step10/s10_scoring.py", "step10/s10_analysis.py", "step10/s10_runner.py", "step10/s10_report.py", "step10/s12_coding.py",
           # proposed P13 additions (owner decision pending): code that decides whether a run may start, how it is verified, resumed, decided and coded
           "step8/s8_verify.py", "step9/s9_blindcheck.py", "step10/s10_integrity.py", "step10/s10_resume.py", "step10/s11_pilot.py",
           "step10/s12_cli.py", "step10/s11_final_freeze_manifest.py"]
    with open(os.path.join(RD, "step7", "STEP7_PROMPT_SPECIFICATION_FREEZE_MANIFEST_v1.json"), "rb") as f:
        fm = json.loads(f.read())
    rel += ["step7/" + n for n in sorted(fm["freeze_set_files"])]
    rel += ["step8_output/" + d + "/manifest.json" for d in sorted(os.listdir(os.path.join(RD, "step8_output"))) if d.startswith("step8_build_")]
    return {"manifest_kind": "final freeze manifest (21.1 step 11)", "carries_no_self_hash": True, "fz_hash_contract": "none adopted (P-2 open)",
            "decision_record_sha256": fsha(record_path), "decision_record_fields": {k: rec[k] for k in ("seed", "call_list_sha256", "utc_timestamp", "final_decision") if k in rec},
            "files": {r: fsha(os.path.join(RD, *r.split("/"))) for r in sorted(set(rel))}}

def main(argv=None):
    a = argparse.ArgumentParser(); a.add_argument("--decision-record", required=True); a.add_argument("--out", required=True); a = a.parse_args(argv)
    try: m = build(a.decision_record)
    except ValueError as e: print("refused:", e); return 2
    with open(a.out, "xb") as f: f.write((json.dumps(m, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8"))
    print("written", a.out); return 0

if __name__ == "__main__": sys.exit(main())
