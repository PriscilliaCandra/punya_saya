# Staged changes for CODEBOOK_S2_S3_v1_DRAFT.md revision 5 (NOT APPLIED)

Target file: `research_design/step7/CODEBOOK_S2_S3_v1_DRAFT.md` (sha256 `54116a75283d20411514756eab4792c382c455213be09b5590f52c8f7ec00eca`, revision 4). Apply only after a snapshot of the revision-4 state exists in `research_design/step7_history/` and write access is granted. No rule of the codebook changes; two defects of presentation are corrected.

## Change 1 (defect: stale sentence, section 1, last bullet, lines 48 to 50)

Replace the final sentence

> The columns, the delay, the scrambling and the statistics reported for the re-code are **not yet specified** (open item C9).

with

> The columns, the delay, the scrambling and the statistics reported for the re-code are specified in section 5 (delegated values, advisor review pending). Their departures from the literal text of section 16.3 are listed in section 5.3.

Reason: section 5 (lines 159 to 203) specifies all four; the sentence contradicts it.

## Change 2 (new section 5.3, after section 5.2)

> ### 5.3 Departures from the literal text of section 16.3 (status table; none is advisor-approved)
>
> | Point | Literal text | This codebook | Source and status |
> |---|---|---|---|
> | Original-code columns | `coder1_*`, `coder2_*` (line 1000) | `coder1_*` and `recode1_*` | naming, delegated (decision record 12.24, decision 2) |
> | Re-code sample | "a delayed intra-rater re-code on an order scrambled by opaque ID", no sample stated | all parseable responses of a cell if there are at most 20, otherwise max(20, ceil(0.20 x D_P)) | delegated; can be read as a reduction from "all coded responses" |
> | Minimum delay | none stated | 14 days | delegated, no empirical basis |
> | Concealment of first-pass codes | none stated | closed first-pass sheet | delegated design addition |
> | Agreement statistics | "percent agreement and Cohen's kappa" (line 1002) | raw agreement and cross-tables, no kappa | OD-3 (Step 2 record, 2026-10-09) forbids claiming inter-rater reliability or kappa, which does not say kappa must not be computed; omission delegated (12.24); open decision: not computed, or computed with the label "intra-rater consistency, no reliability claim" |
>
> Until the owner and the advisor decide, section 16 governs where it is explicit, and every table that uses the re-code carries the statement "single coder, intra-rater only; delegated values pending advisor review".

## Change 3 (revision history, header)

Append to the revision history paragraph: "Revision 5 (decision record 12.26) corrects the stale sentence of section 1 and adds section 5.3; no coding rule changes."

## Hash consequence

Item I17 (`file(CODEBOOK_S2_S3_v1_DRAFT.md)`) of the Step 7 manifest changes; `TestManifestConsistency` must then point to the new manifest.
