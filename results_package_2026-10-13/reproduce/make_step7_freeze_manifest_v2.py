"""Builds STEP7_PROMPT_SPECIFICATION_FREEZE_MANIFEST_v2.json from the v1 manifest for FZ-v2 (decision record 12.64, D2: the limited R-7).
Nothing of Step 7 changes: the eleven freeze-set files must still have exactly the hashes of the v1 manifest (checked); only the cited FZ register changes from FZ-v1 to FZ-v2.
Writes only the path given as argv[1] (refuses to overwrite). Usage: python -B -I make_step7_freeze_manifest_v2.py <out.json>"""
import copy, hashlib, json, os, sys
RD = r"D:\research s2\research_design"
sys.path.insert(0, os.path.join(RD, "step7")); sys.dont_write_bytecode = True
import s7_decision as D


def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


V1M = os.path.join(RD, "step7", "STEP7_PROMPT_SPECIFICATION_FREEZE_MANIFEST_v1.json")
FZ2 = os.path.join(RD, "PARAMETER_FREEZE_MANIFEST_FZ_v2.json")
m1 = json.load(open(V1M, encoding="utf-8"))
fz2 = json.load(open(FZ2, encoding="utf-8"))
assert D.register_hash(fz2) == fz2["register_canonical_sha256"]
for name, h in m1["freeze_set_files"].items():                       # no Step 7 file may have changed
    assert sha(os.path.join(RD, "step7", name)) == h, name
for rel, h in m1["file_hashes"].items():
    assert sha(os.path.join(os.path.dirname(RD), rel.replace("/", os.sep))) == h, rel
m2 = copy.deepcopy(m1)
m2["manifest_purpose"] = ("Step 7 prompt-specification freeze manifest v2 (section 21.1 step 7), written for FZ-v2 under the limited R-7 of decision record 12.64 (D2). It repeats the v1 manifest "
                          "with the SAME freeze-set files and hashes and cites the FZ-v2 register instead of FZ-v1. The v1 manifest is unchanged. Carries no self-hash.")
m2["status"] = "PREPARED 2026-10-16 for FZ-v2 (not frozen until the owner's official-hash instruction). Not advisor approved (no advisor, 12.50). A change to a freeze-set file returns to Step 7."
m2["date"] = "2026-10-16"
m2["supersedes"] = {"path": "research_design/step7/STEP7_PROMPT_SPECIFICATION_FREEZE_MANIFEST_v1.json", "sha256": sha(V1M)}
m2["fz_v1_register_superseded"] = m1["fz_v1_register"]
del m2["fz_v1_register"]
m2["fz_register"] = {"label": "FZ-v2", "path": "research_design/PARAMETER_FREEZE_MANIFEST_FZ_v2.json", "file_sha256_at_this_time": sha(FZ2),
                     "register_canonical_sha256": fz2["register_canonical_sha256"], "changed_by_step7": False}
m2["decision_record"] = "research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md, entries 12.26, 12.27, 12.63 and 12.64"
m2["changes_from_step7_manifest_v1"] = {"freeze_set_files_changed": [], "cited_fz": "FZ-v1 -> FZ-v2", "reason": "register item 17 (model and settings) changed by the new FZ version"}
out = sys.argv[1]
with open(out, "xb") as f:
    f.write(json.dumps(m2, indent=1, ensure_ascii=False, sort_keys=True).encode("utf-8") + b"\n")
print("written", out, sha(out))
