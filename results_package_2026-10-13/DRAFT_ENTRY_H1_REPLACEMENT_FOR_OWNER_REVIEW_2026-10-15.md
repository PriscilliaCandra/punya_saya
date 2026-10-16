# DRAFT (NOT RECORDED, NOT APPROVED): replacement of the H1 human blind check by a recorded departure, for the owner's review, 2026-10-15

Status: a draft text only. It is not an entry of the decision record, changes no official document, frozen specification, FZ-v1 register, manifest, gate, registry, evidence or code, and authorizes nothing. It becomes effective only if the owner approves it explicitly and a separate implementation authorization is given. The owner has the authority (12.50 row 0); this draft does not claim that the departure satisfies the protocol: it IS a departure from it.

## 1. What the sources say (checked today, read-only)

- Spec v2.7 section 11, layer 3: "One rule-reader ... fills a worksheet ... Default coverage: every member; a subsample is allowed only if its fraction and deterministic selection rule are frozen before generation, and is then a recorded limitation." Layer 2 (Implementation B, strict parse and recomputation) and layer 3 are different layers; line 728 states that A, B, the generator and the human check by one person give code-path independence only, and that the human check "tests re-derivation consistency, not inter-person interpretation". A model-based reader "may be added only as an extra screening layer, never as the deciding check".
- FZ-v1 row 19 (frozen): coverage 100 %, minimum delay 7 days.
- Gate (`s10_runner.check_gates`, the ONLY code that reads the Step 9 evidence, lines 175 ff.): predicates G4-G9 = evidence file exists; `(completed_utc - last_registry_view_utc).days >= 7`; coverage 100; worksheet hash present; adjudication AGREE or ADJUDICATED_NO_REJECT; `build_manifest_sha256` equals the build's manifest. G1-G3 (settings, Step 8 verifier, Implementation B) hold today and are not affected.
- Project practice for departures: recorded in the decision record without editing the specification (for example K1, "recorded departure from spec line 1002", 12.51; "record the decision in the decision record, do not edit the spec").

## 2. The three alternatives

| | (1) Automated evaluation instead of H1 | (2) Remove H1 from the gate by a formal amendment (recorded departure) | (3) H1 stays "not done"; other work continues |
|---|---|---|---|
| What it is | A script re-derives the 624 verdicts from the checker bundle and writes the evidence file | The owner records that layer 3 (human check) is NOT performed, accepts the limitation, and the gate accepts an explicit owner waiver in place of G4-G8 | No change |
| Minimum change | Same as (2), plus a script; AND the evidence file would have to say it is not a human check | One decision-record entry; one gate edit in `s10_runner.py` (hash moves, list membership unchanged); tests; a waiver file written by the owner; NO spec, FZ-v1, Step 7 or Step 8 edit, so no R-7, no rebuild, the build manifest and G9 stay as they are | None |
| Research validity | Not independent: Implementation B is already an automated re-derivation and the same author wrote A, B, the generator and the script; the result would add nothing, and calling it "the blind check" would misstate what was done (spec: a model is never the deciding check) | The only human reading of the rendered texts is dropped; what remains is B (strict parse, recomputation), the Step 8 verifier and the 30 numeric gates. Residual risk: a presentation ambiguity that a human reader would catch is not caught. Disclosed as a limitation | Fully protocol-conform |
| Gate | Would have to be CLOSED until the script's output is accepted as evidence; a forged "human" label must not be used | Stays CLOSED until the waiver exists and the other predicates (H5, FZ index, etc.) hold; after that G4-G8 are satisfied by the waiver | CLOSED until H1 and H3 are done (earliest 2026-10-22T07:50:10Z) |
| Time | Not faster than (2) and weaker | Removes the 624 rows AND the 7-day wait; the next blockers are H5, the FZ hash, the freeze, the pilot | The 624 rows and the wait remain |

(1) collapses into (2): an automated reader cannot honestly be recorded as the human blind check, so the honest form of "automated instead of H1" is a recorded departure plus the existing Implementation B. A smaller variant of (2) exists and is NOT recommended here unless the owner wants some human check: a deterministic subsample (the spec allows it only if fraction and rule were frozen before generation; FZ-v1 froze 100 %, so it would also be a recorded departure).

## 3. Recommendation (assistant's, not a decision)

(2) in its minimal form, because it is the only alternative that removes both the 624 rows and the 168-hour wait without touching the frozen specification, the register or the Step 8 build. Its cost is real: the research loses the human reading layer and must say so. It does not weaken any other gate predicate.

## 4. Draft decision-record entry (proposed text, to be given the next free number only if approved)

> **12.__ Owner decision: the H1 human blind check is replaced by a recorded departure.** Authority: the owner's explicit approval, as sole decision-maker under 12.50 row 0. The owner decides that spec v2.7 section 11 layer 3 (human blind check, FZ-v1 row 19) is NOT performed for this research. This is a recorded departure from the specification and from the frozen register row 19; neither is edited. Reason: the owner's priority is to complete the research within the available time; the 624-row manual check and the 7-day delay are not carried out.
>
> | # | Item | Decision |
> |---|---|---|
> | 1 | Layer 3 | NOT performed. No worksheet, no evaluation, no `step9_evidence.json` of kind human blind check is created. R1 (2026-10-15T07:50:10Z) stays recorded and unused. |
> | 2 | What remains | Layer 1 (Step 8 gates, 30 numeric gates and PG checks), layer 2 (Implementation B, AGREE, re-checked by the runner at every gate check), the Step 8 verifier. |
> | 3 | Gate | Predicates G4-G8 are replaced by one predicate: an owner waiver file `step9_waiver.json` with `waived_by` = owner, `decision_entry` = this entry's number, `human_blind_check` = "NOT PERFORMED", `build_manifest_sha256` = the build's manifest hash (G9 retained). A file claiming a performed check is refused. G1-G3 and all other predicates are unchanged. Implemented only after a separate implementation authorization. |
> | 4 | Limitation (final report) | The human re-derivation check of the rendered texts was not performed; A, B and the generator share one author (code-path independence only); a presentation ambiguity that a reader would catch is not excluded. |
> | 5 | Not changed | The specification, FZ-v1, the Step 7 and Step 8 manifests, the registry, the codebook, K1, H4 (i), R-7 (NOT AUTHORIZED), the safe-stop, E-1 enforcement, the 31-file list membership. |
>
> Not authorized by this entry: the gate edit (separate authorization), the waiver file, the FZ hash, the code freeze, any live call, the pilot, a commit or a push. The gate stays CLOSED.

## 5. Implementation that would follow an approval (not authorized now)

`s10_runner.check_gates`: accept `step9_waiver.json` in place of the evidence file when it validates as above (about 15 lines); new tests for waiver accepted, waiver missing, waiver claiming a performed check, wrong manifest hash, wrong entry; `run_all_checks.py --quick`; backups. The gate must still refuse when neither a valid evidence file nor a valid waiver exists.
