"""Builds STEP7_PROMPT_SPECIFICATION_FREEZE_MANIFEST_v1.json from manifest v4 and the current files (decision record 12.26).
Reads research_design/step7; writes only the path given as argv[1] (refuses to overwrite). Usage: python -B -I make_step7_freeze_manifest.py <out.json>"""
import hashlib, json, os, sys
STEP7 = r"D:\research s2\research_design\step7"
sys.path.insert(0, STEP7); sys.dont_write_bytecode = True
import s7_manifest_items as MI

def sha(p):
    with open(p, "rb") as f: return hashlib.sha256(f.read()).hexdigest()

v4 = json.load(open(os.path.join(STEP7, "STEP7_PROMPT_SPECIFICATION_MANIFEST_DRAFT_v4.json"), encoding="utf-8"))
items = {k: v for k, v in v4["items_section_14_and_21_1"].items()}
computed = MI.compute_item_hashes()
for k, info in computed.items():
    if k in items: items[k] = dict(items[k], sha256=info["sha256"]) if k != "I04_runner_sentence" else items[k]
    else: items[k] = {"sha256": info["sha256"]}
items["I17_codebook_S2_S3"] = dict(items["I17_codebook_S2_S3"], where="CODEBOOK_S2_S3_v1_DRAFT.md (revision 5)")
OUT_KEYS = ["I27_proposed_clarifications_and_amendments", "I29_outcomes_proposed_policy", "I30_proposed_amendment_18_2"]
out_items = {k: items.pop(k) for k in OUT_KEYS}
FREEZE = ["prompt_specification_v1.py", "s7_core.py", "s7_parser.py", "s7_refcheck.py", "s7_decision.py", "s7_diagnostic.py",
          "s7_bundle.py", "CODEBOOK_S2_S3_v1_DRAFT.md", "codebook_battery_v1.py", "parser_battery_v1.py", "s7_recode.py"]
file_hashes = {"research_design/step7/" + n: h for n, h in MI.compute_file_hashes().items()}
m = {
 "manifest_purpose": "Step 7 prompt-specification freeze manifest v1 (section 21.1 step 7; section 14), decision record 12.26. Supersedes STEP7_PROMPT_SPECIFICATION_MANIFEST_DRAFT_v4.json (unchanged, sha256 5db81eac...544d9). Carries no self-hash.",
 "status": "FROZEN_ON_OWNER_INSTRUCTION (2026-10-13). Not advisor approved: see open_advisor_items. A change to a freeze-set file before the FZ hash returns to Step 7 (new version). Nothing here authorizes Step 8 execution beyond the owner's instruction of 2026-10-13, the pilot, or any API call.",
 "date": "2026-10-13",
 "supersedes": {"path": "research_design/step7/STEP7_PROMPT_SPECIFICATION_MANIFEST_DRAFT_v4.json", "sha256": v4_sha if (v4_sha := sha(os.path.join(STEP7, "STEP7_PROMPT_SPECIFICATION_MANIFEST_DRAFT_v4.json"))) else None,
                "revision4_snapshot": "research_design/step7_history/revision4_2026-10-13/ (hash list revision4_2026-10-13.SHA256SUMS.txt)"},
 "specification": v4["specification"], "fz_v1_register": v4["fz_v1_register"],
 "decision_record": "research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md, entries 12.26 and 12.27",
 "owner_decisions_2026_10_13": {"sf_policy": "keep v2.7 section 18.2 as written", "pg11b_scan": "keep the literal text", "recode": "keep delegated values, no kappa", "write_scope": "research_design step7_history, step7, step8, step8_output, decision record append"},
 "hash_method": v4["hash_method"],
 "freeze_set_files": {n: sha(os.path.join(STEP7, n)) for n in FREEZE},
 "items_section_14_and_21_1": items,
 "not_in_freeze_set_items": out_items,
 "evidence_not_frozen": ["test_step7.py", "s7_manifest_items.py"],
 "file_hashes": file_hashes,
 "open_advisor_items": ["SF/UNP main-run policy (Policy 1 / Policy 2 / interim = v2.7 as written)", "PG11b scan scope (literal text may reject ordinary response words; post-run only)",
   "delegated re-code values and the section 16.3 departures (codebook 5.3)", "human rehearsal of the codebook battery (section 13.5, before the pilot; not done)"],
 "not_done": ["advisor review", "human rehearsal", "Step 8 execution at the time of this manifest", "pilot", "API or model call", "commit or push"],
}
out = sys.argv[1]
with open(out, "xb") as f: f.write(json.dumps(m, indent=1, ensure_ascii=False, sort_keys=True).encode("utf-8") + b"\n")
print("written", out, sha(out))
