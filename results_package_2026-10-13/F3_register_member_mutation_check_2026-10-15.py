import sys, os, copy
RD = r"D:\research s2\research_design"
sys.dont_write_bytecode = True
for d in ("step8", "step7", "step4", "implementation_a"):
    sys.path.insert(0, os.path.join(RD, d))
sys.path.insert(0, RD)
import s8_build as B
r = B.load_inputs()
print(type(r), len(r) if hasattr(r, "__len__") else "")
fz, fm, h = r
K, GT = B.K, B.GT
rg = fz["register"]
p = K.params_from_fz(rg)
S, G = p["S_pilot"], p["G_pilot"]          # pilot registry: small and fast
templates = K.construct(p, S, G)
reg = B.a_register(fz, S, G)
prompts = GT.render_all(templates, p)
eq, _, _ = B.equivalence(reg, templates, prompts, p)
print("baseline E-PAR problems:", len(eq["E-PAR"]), "E-GATE:", len(eq.get("E-GATE", [])), "E-PROMPT:", len(eq.get("E-PROMPT", [])))
# mutation 1: one generator member carries a tau_F different from the register
t2 = copy.deepcopy(templates)
i = next(n for n, t in enumerate(t2) if t["family"] == "PAC")
t2[i]["valid"]["tau_F_s"] += 1
eq2, _, _ = B.equivalence(reg, t2, prompts, p)
print("tau_F mutated -> E-PAR problems:", len(eq2["E-PAR"]))
# mutation 2: D_dist different
t3 = copy.deepcopy(templates)
t3[i]["valid"]["D_dist"]["num"] += 1
eq3, _, _ = B.equivalence(reg, t3, prompts, p)
print("D_dist mutated -> E-PAR problems:", len(eq3["E-PAR"]))
