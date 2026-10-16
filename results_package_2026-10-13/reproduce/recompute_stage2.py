"""Independent recomputation (read-only) of the Stage 2 headline counts from the primary coding tables.
Does not import the project analyzer. Definitions: stage2_analyzer_specification.md section 'counts' (E_fail, T1_pass, X_E, C_fail, C_types, X_C, U_fp, X_U)."""
import csv, collections, sys, os
R = sys.argv[1]
def load(p): return list(csv.DictReader(open(p, encoding="utf-8", newline="")))
def counts(rows):
    cells = collections.defaultdict(collections.Counter)
    for r in rows: cells[r["scenario_id"]][r["code_short"]] += 1
    E_cells = ["E-F-A", "E-F-B"]; Et = ["K-E-TRUE", "K-E-TRUE-B"]; C = ["C-L2", "C-L3", "C-L4-S2"]
    out = {}
    out["E_fail"] = sum(cells[c][k] for c in E_cells for k in ("E4", "E5"))
    out["T1_pass"] = sum(cells[c]["T1"] for c in Et)
    out["X_E"] = sum(cells[c]["X"] for c in E_cells + Et)
    out["C_fail"] = sum(cells[c][k] for c in C for k in ("C4", "C5", "C6"))
    out["C_types"] = sum(1 for c in C if any(cells[c][k] for k in ("C4", "C5", "C6")))
    out["X_C"] = sum(cells[c]["X"] for c in C)
    out["U_fp"] = cells["K-C-L4-S2"]["U_false_positive"]; out["X_U"] = cells["K-C-L4-S2"]["X"]
    return out, cells
for label, rel in (("RECONCILED (reported)", "analysis/primary_coding_table.csv"), ("ORIGINAL sheet (analyzer BLOCKED_CODING_INCONSISTENT; sensitivity only)", "analysis/blocked_coding_inconsistent_v1/primary_coding_table.csv")):
    rows = load(os.path.join(R, rel)); o, cells = counts(rows)
    print(label, "rows", len(rows)); print(" ", o)
    gate1 = o["T1_pass"] < 7 or o["X_E"] >= 4 or o["X_C"] >= 3
    gate2 = o["E_fail"] >= 4 or (o["C_fail"] >= 5 and o["C_types"] >= 2)
    print("  gate1_inconclusive", gate1, "gate2_continue", gate2)
    for c in sorted(cells): print("   ", c, dict(cells[c]))
