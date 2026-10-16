# Permintaan keputusan owner: urutan MD-09 dan `s11_pilot decide` (2026-10-16)

Status: **DRAF PERMINTAAN, BELUM DISETUJUI, BELUM dicatat sebagai keputusan.** Tidak ada `decide` yang dijalankan, tidak ada commit/push, tidak ada anchor yang dibuat.

## 1. Perbaikan yang sudah dilakukan (otorisasi: instruksi owner setelah 12.67)
| Perubahan | Berkas | Bukti |
|---|---|---|
| `s11_pilot.py` kini memakai manifest FZ yang disebut eksplisit (`--fz-manifest`), wajib saat penegakan FZ-index aktif; tidak ada fallback diam-diam ke FZ-v1. `decide` juga mensyaratkan manifest itu tercantum di FZ index dan run membawa FZ hash yang sama. Manifest dengan register hash tidak cocok atau berkas tidak ada ditolak. | `step10/s11_pilot.py` (sha256 `96d43e54366ac1a1c53d24b46f3dfa5d63954cf898d61d20f1a4a4ddd71d0fc2`) | `test_s11_pilot_fz.py`: 9 tes (positif FZ-v2 mencatat register hash FZ-v2, 7 negatif) |
| Gerbang anchor MD-09 pada scope `main` (penegakan aktif): runner menolak sebelum urutan acak dibuat jika tidak ada bukti anchor yang menyebut SHA-256 tepat dari berkas record, `anchor_kind` ∈ {git_commit, external_timestamped}, referensi tidak kosong, waktu anchor tidak lebih awal dari record. Kode **tidak** dapat memeriksa keaslian toko eksternalnya; bukti itu berasal dari owner. | `step10/s10_runner.py` (`29c444538ae643a82b41ff60ad5d07ba1d5434b1c4d21af879043468e3146d5a`), `s10_resume.py` (`620eb33328e00fa292d06f242c0606ebf626ea27bc20ac5c89d57afce0cf186c`); opsi `--decision-anchor` | `test_md09_anchor.py`: 8 tes (termasuk: `plan_calls`, pembuat urutan, tidak dipanggil bila anchor tidak ada) |
| Laporan pilot round 2 dijalankan ulang dengan manifest FZ-v2 eksplisit: **identik byte-per-byte** dengan laporan sebelumnya | `runs/pilot_round_2_report_fzv2.json` (sha256 `39598766de5bc18998c4730385e1807b7b50018173e34942ebdc0548c4fa6bbc`) | `cmp` identik |

Cadangan sebelum perubahan: `results_package_2026-10-13/_backup/s11_fix_20261016/`.

## 2. Temuan tentang konflik §10 vs 12.47 (fakta kode)
- `s7_decision.py` (yang dipanggil `decide`) **hanya** menulis record JSON kanonik (menghitung seed dari tanggal UTC, hash daftar panggilan kanonik). Ia **tidak** menghasilkan urutan acak. Urutan acak dibuat hanya di `plan_calls` pada scope `main`, sesudah semua gerbang.
- Spesifikasi §10 (baris 662): record "ditulis dan di-hash" sebelum urutan dibuat, lalu di-anchor, lalu urutan dibuat. Jadi urutan §10 yang benar: **`decide` -> anchor -> urutan (main run)**. Itu kini dijaga oleh gerbang di atas.
- 12.47 baris 8 berbunyi "decision script must not be run until the record is anchored". Dibaca harfiah ini mustahil: record adalah keluaran skrip. Instruksi Anda (menyiapkan berkas untuk di-anchor lalu menjalankan `decide`) juga berurutan sama: record harus ada dulu.

## 3. Keputusan yang saya perlukan (hanya satu)
**Apakah Anda menyetujui pembacaan: "kalimat 12.47 baris 8 berlaku untuk pembuatan urutan acak (main run), bukan untuk eksekusi `decide` yang menghasilkan record"?** Jika ya, saya akan: (a) mencatat keputusan itu sebagai entri baru, (b) menjalankan `s11_pilot decide --round 2` sekali (run pertama berlaku; seed = tanggal UTC saat itu), (c) menyiapkan berkas record + SHA-256 untuk Anda anchor, (d) berhenti sampai bukti anchor Anda diterima.
Konsekuensi jika tidak: `decide` tidak bisa dijalankan; keputusan pilot resmi tetap tertunda; main run tetap tertutup.

## 4. Instruksi anchor (untuk dilakukan Anda, setelah `decide` menghasilkan record)
Saya akan memberi path `record.json` dan SHA-256-nya. Anda lalu:
1. Hitung hash untuk memastikan sama: `Get-FileHash -Algorithm SHA256 <record.json>`.
2. Anchor eksternal bertimestamp (contoh yang dapat diverifikasi publik, OpenTimestamps): `ots stamp record.json` menghasilkan `record.json.ots`; tunggu konfirmasi, lalu `ots upgrade record.json.ots` dan `ots verify record.json.ots`. Simpan berkas `.ots` secara permanen (jangan edit `record.json`).
3. Setelah verifikasi berhasil, tulis berkas bukti (nama bebas, mis. `human_evidence/decision_record_anchor.json`) dengan **tepat** empat kunci:
```json
{"anchor_kind": "external_timestamped", "anchored_at_utc": "YYYY-MM-DDTHH:MM:SSZ", "decision_record_sha256": "<sha256 record.json>", "reference": "<mis. nama dan sha256 berkas .ots, atau ID toko>"}
```
4. Beri tahu saya path-nya. Saya hanya memeriksa kesesuaian hash/bentuk/waktu; saya tidak dapat memverifikasi toko eksternalnya dan tidak akan mengklaim anchor sebelum bukti Anda ada. (Alternatif yang diizinkan §10 sebagai bentuk utama: commit sendiri atas record di version control; itu memerlukan otorisasi commit terpisah dari Anda.)

## 5. Disiapkan, belum berlaku
- `proposals/h5_authorization_main_DRAFT_NOT_AUTHORIZED.json.txt`: usulan H5 main (2.496 panggilan, 1016 karakter input maksimum = panjang prompt terpanjang main di build FZ-v2, plafon biaya 100). **Bukan otorisasi.** Dibuat sebagai berkas aktif hanya setelah keputusan pilot resmi PASS dan persetujuan Anda atas nilainya.
- `proposals/s11_final_freeze_manifest_FZ_v2.diff` (+ berkas usulan): 12 baris berubah (FZ-v2, manifest Step 7 v2, folder build `step8_output_fz_v2`, tambah `fz_index.py` dan `s8_build.py` ke daftar). Berkas ini di luar D8: **tidak diterapkan** sampai Anda mengizinkan; hanya relevan bila pilot resmi PASS.
