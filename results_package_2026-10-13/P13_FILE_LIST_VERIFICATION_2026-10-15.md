# P13: verification of the 31-file list (2026-10-15)

Read-only check. It is NOT a freeze manifest and NOT evidence of a code freeze: no PASS decision record exists, no final freeze manifest was written, no code freeze is declared. The tool `s11_final_freeze_manifest.py` was called only through its `build()` function on a SYNTHETIC PASS record kept in the scratchpad (nothing was written in the repository) so that the listed paths could be hashed from the actual files; the hashes below are hashes of the real files on disk at the time of the check and will change when a listed file changes.

Authoritative source of the list: `research_design/step10/s11_final_freeze_manifest.py` (P13 applied 2026-10-15, tool hash `7395140c...10eb`), the Step 7 freeze manifest (11 files) and the Step 8 build manifest.

Results of the check:
- 19 literal entries (12 original + 7 added by P13) + 11 Step 7 freeze-set files + 1 Step 8 manifest = 31 listed; 31 unique; **0 duplicates; 0 missing on disk**; the tool's `build()` returns exactly these 31 paths.
- The 11 Step 7 files match the hashes recorded in the Step 7 freeze manifest (0 mismatches): they are unchanged since the Step 7 freeze.
- Changed since the previous snapshot (audit report A3, taken before this round's code changes): `step10/s10_resume.py` (owner decision 12.43, option A1) and `step10/s10_runner.py` (owner decision 12.43, option O3). Nothing else changed.
- `s10_runner.py` is not referenced by the Step 7 manifest, the Step 8 manifest, the methodology manifest or FZ-v1 (0 matches), so its change needs no Step 7/Step 8 rebuild; only its line in the final freeze list changes.

| Path (relative to `research_design/`) | SHA-256 |
|---|---|
| METHODOLOGY_FREEZE_MANIFEST_v2_7.json | `b93ff372d44854e19266159f389f29e8051a4f678ffbbf4a35b9a85a602bb1d3` |
| PARAMETER_FREEZE_MANIFEST_FZ_v1.json | `149445715a8280f4079bcd34d3594e25fe1b6b30118e382e96e94360c0faf338` |
| PARAMETER_JUSTIFICATION_RECORD_DRAFT.md | `a1b2148766965d0b7a35f5996e83e77cf9c303eece09e275589f5939f7df7de1` |
| SCENARIO_CONSTRUCTION_SPECIFICATION_v2_7_DRAFT.md | `d5fcffadd1045fc0c86a7c84eb8d51592d807576b6a51b712cef025164082ca8` |
| implementation_a/impl_a.py | `daa2cd49b86ed1a546e95478bc3f40c1fc131ea52d4622b981e4e3b117f018ee` |
| step10/s10_analysis.py | `7993a7347e07f3916ebf6f758d9e0cf3478a6c0b98ba78b4ae6ad304d2be4dc7` |
| step10/s10_integrity.py | `f2a109cfdcc27d326126afef1fdf1590ca7cedb261bb0ca747f033a1578af07d` |
| step10/s10_report.py | `f9857e5603941a6c67a53a63efadc2de87291334ab454d0df111b84aaf89c68a` |
| step10/s10_resume.py | `5e9ea70f1fdf4f407054eac3e9ef3d04762c44a7063867b4dd35ab4f28eb1ac9` |
| step10/s10_runner.py | `7c10dbff3cd9dc8cde2f0c9d4a2134193d7d343d69a76241ea31a8a33335ed04` |
| step10/s10_scoring.py | `8c0e6b9fecb559fb44519bcf7f1d8048ae755e9c63b03ba9264d57f53efc45b2` |
| step10/s11_final_freeze_manifest.py | `7395140ce37bcb8315aa2eff6b5672b31f985734f6c08da9fec3582c85be10eb` |
| step10/s11_pilot.py | `68fc807f85a7eaa6ed212bb4a234842ef4578b3e4beebb88a65410fd297f5a3a` |
| step10/s12_cli.py | `e6de02879a580eebbee1ee8533df4c2b67674507ef9d4442a4c19ec3deec7f0e` |
| step10/s12_coding.py | `a571c6ba64fdf651dfd3b6f95b240e789bd95d3fa2809068f4aa94f4f7db84fa` |
| step7/CODEBOOK_S2_S3_v1_DRAFT.md | `25a74353be546cf9db27e58acbd8ed7c02bc896cbf5a0c594b1f4de8ed63d53c` |
| step7/STEP7_PROMPT_SPECIFICATION_FREEZE_MANIFEST_v1.json | `202979de2a88c1b667c3510fc632b25f7108a11d7fdb103cc3473f2fb7c220f7` |
| step7/codebook_battery_v1.py | `8200cfea41e23255242576ace494fa039ce28880d1a443a2326d6900e0107d49` |
| step7/parser_battery_v1.py | `82af5d5361561d9812dd0827a061fa609e42a76dc6f03c6dc90ba2ab38296b27` |
| step7/prompt_specification_v1.py | `8b9a73e945f0251c648ca2045ce9c0ee2de25581127f905764139229bcae3167` |
| step7/s7_bundle.py | `10567178b20976eab4958c98db0fca8bd54eabcfa0cb96727936b4985dfa1636` |
| step7/s7_core.py | `64789acb84047f3dabbdd9855baa997317cab637dbb0d7f152cabac98cadea21` |
| step7/s7_decision.py | `cf0823f7abdf4b6b44d4efd44006567ac42290350714415e8e11496444f57618` |
| step7/s7_diagnostic.py | `5e0f6e707231d66f2ca89b4a0765d6edcde78cdc5bc1e1137e7c9fa6fe9806b6` |
| step7/s7_parser.py | `b9d60196c50f8099c0a8319c1308abd40937f7fc3e87e58a30983225c3bd56d8` |
| step7/s7_recode.py | `ec8f948e6209147d0ada8fb0018a97068f352cf5dbed3894c9821bacd164bc37` |
| step7/s7_refcheck.py | `39e10a85068262c960a475fc30cacc7e43ca5ebc8a8ce395bd41fad8d3bf80d4` |
| step8/s8_verify.py | `b9a46f599320e5420510f911a25d3e2d904cb818ee1d4a21b3d81d8c73a833f2` |
| step8_output/step8_build_7a6bbe465c66/manifest.json | `09eed00eeb79e04ccaf607a66642417cdbbdfe802b19e580a67f4b9e08c7aaa5` |
| step9/impl_b.py | `ada22199bb472d934b4004a3fa6b8ee89551b5cb2f69ac69ca998ac8cc12f600` |
| step9/s9_blindcheck.py | `e870b8d03b3179005517ad6431d840cfc260ceca2f01adc7d30d17e84c84752e` |
