"""Read-only integrity verification of the completed pilot_clarification runs (Stage 1 and Stage 2).
Recomputes SHA-256 of files and compares them with the hashes recorded by the runs themselves. Writes nothing."""
import hashlib, json, os, sys
ROOT = sys.argv[1] if len(sys.argv) > 1 else r"D:\research s2\pilot_clarification"
def h(p):
    with open(p, "rb") as f: return hashlib.sha256(f.read()).hexdigest()
bad = 0; n = 0
def chk(label, path, exp):
    global bad, n
    n += 1
    if not os.path.exists(path): print("MISSING", label, path); bad += 1; return
    a = h(path)
    if a != exp: print("MISMATCH", label, a[:12], exp[:12]); bad += 1
# Stage 2 postrun file hashes
r2 = os.path.join(ROOT, "runs", "stage2_gemini_20261008T035839Z")
post = json.load(open(os.path.join(r2, "integrity", "postrun.json"), encoding="utf-8"))
for rel, exp in post["file_hashes"].items(): chk("s2 postrun " + rel, os.path.join(r2, rel), exp)
print("stage2 postrun:", post["status"], post["calls_attempted"], post["outcome_counts"], post["finish_reason_counts"], post["models_returned"])
am = json.load(open(os.path.join(r2, "analysis", "analysis_manifest.json"), encoding="utf-8"))
for rel, exp in am["outputs"].items(): chk("s2 analysis output " + rel, os.path.join(r2, rel.replace("analysis/", "analysis/", 1)), exp)
# the three frozen artefacts referenced by the addendum
exp = {"CODEBOOK_v2.md": "177a1c5d9b7dbf1ab9e53d0684365dcf67b21f1b1f3154f3f8b1ecc5aa6eb4fc",
       "stage2_analyzer_specification.md": "4d55c305da83c2d6d62f1ac7b725e1001884aaab0dda20dae2a70799e470ba5b",
       "analyze_stage2.py": "08e8432e52ec9ed6c68730eb288cf32348c54355aa8709a3bccc0edd72aa3056"}
for f, e in exp.items(): chk("frozen " + f, os.path.join(ROOT, f), e)
# Stage 1 (successful run): calls and raw records
r1 = os.path.join(ROOT, "runs", "stage1_gemini_20261007T080948Z")
calls = [json.loads(l) for l in open(os.path.join(r1, "calls.jsonl"), encoding="utf-8")]
print("stage1 successful run calls:", len(calls), "with response_text:", sum(1 for c in calls if c.get("response_text")), "errors:", sum(1 for c in calls if c.get("error")))
r1b = os.path.join(ROOT, "runs", "stage1_gemini_20261007T070917Z")
cb = [json.loads(l) for l in open(os.path.join(r1b, "calls.jsonl"), encoding="utf-8")]
print("stage1 first (failed) run calls:", len(cb), "errors:", sum(1 for c in cb if c.get("error")))
print("hash checks:", n, "problems:", bad)
