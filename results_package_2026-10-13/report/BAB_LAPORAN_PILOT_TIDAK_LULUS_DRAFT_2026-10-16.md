# DRAFT BAB — Pilot Tidak Lulus dan Hasil Utama Tidak Tersedia

**Status dokumen:** DRAFT UNTUK DITINJAU OWNER. Bukan versi final. Ditulis 2026-10-16 dari bukti yang ada di repositori (decision record `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md`, entri 12.38–12.62; artefak pilot; spesifikasi v2.7). Penanda **[PERIKSA]** menandai bagian yang belum saya verifikasi ulang terhadap sumbernya atau yang butuh keputusan/data darimu. Penanda **[ISI]** menandai bagian yang hanya kamu yang bisa menulis.

> **Status penelitian: BLOCKED / INCONCLUSIVE untuk eksperimen utama.** Eksperimen utama (2.496 panggilan) tidak dijalankan. Pilot ronde 1 berstatus resmi FAIL-S. Karena itu bab ini **tidak melaporkan hasil tentang perilaku model**, tidak menguji hipotesis, dan tidak menyatakan hipotesis terbukti atau tidak terbukti.

---

## Ringkasan

Penelitian ini merancang protokol untuk mengukur apakah sebuah model bahasa dapat mengklasifikasikan suatu rencana latihan lari sebagai memenuhi atau melanggar aturan yang dinyatakan, dibandingkan dengan kebenaran deterministik, di bawah empat kondisi (rencana valid atau melanggar, dengan atau tanpa klaim reviewer). Bab ini melaporkan apa yang berhasil dibangun (generator skenario, gerbang validasi, verifikasi dua implementasi, prosedur pembekuan, dan runner yang diaudit), satu pilot 18 panggilan pada model Gemini yang berstatus FAIL-S karena dua panggilan ditolak penyedia dengan HTTP 429, keputusan menghentikan eksperimen pilot, dan satu evaluasi kelayakan eksploratori pada model lokal dengan data sintetis. Hasil utama tidak tersedia. Kontribusi yang dapat dipertanggungjawabkan terbatas pada rancangan metodologi, instrumen yang dapat diaudit, dan pelajaran tentang kendala kapasitas infrastruktur. **[ISI: sesuaikan dengan format tesis/institusi]**

## 1. Pendahuluan, konstruk, dan batas klaim

**Konstruk.** Klasifikasi kendala: diberikan aturan yang dinyatakan dan rencana latihan lengkap, apakah model terpilih mengembalikan verdict (`satisfied`, `violated`, atau `unclear`) yang cocok dengan keadaan deterministik rencana (spesifikasi v2.7, §1). Klasifikasi adalah satu-satunya tugas primer; model tidak diminta merevisi, menghitung ulang, menyetujui, atau menjelaskan.

**Kebenaran dasar bersifat biner.** Setiap skenario berisi informasi lengkap, sehingga verdict `unclear` selalu dihitung sebagai kesalahan dan dilaporkan sebagai laju tersendiri (spec baris 104).

**Desain.** Dua keluarga aturan (`MIL`: batas kenaikan jarak mingguan; `PAC`: konsistensi pace balapan), empat kondisi (A: valid tanpa klaim; B: melanggar tanpa klaim; C: valid dengan klaim reviewer palsu; D: melanggar dengan klaim benar), 12 sel primer, dan dua pengulangan per template pada main run yang direncanakan.

**Yang tidak diklaim.** Bab ini tidak mengklaim kompetensi model, tidak mengklaim pengaruh klaim reviewer, posisi, atau margin terhadap verdict, dan tidak mengklaim generalisasi ke model lain. Kontras antar kondisi tidak pernah dihitung (analisis pilot hanya struktural, spec §13.7).

## 2. Desain dan instrumen yang dibangun

| Komponen | Status | Sumber |
|---|---|---|
| Registry utama | 312 template (104 `MIL`, 208 `PAC`), 1.248 prompt, 2.496 slot panggilan | record 12.28 **[PERIKSA angka terhadap 12.28]** |
| Registry pilot | 24 template, 96 prompt; pilot 18 panggilan satu repetisi | 12.28, spec §13.3 |
| Gerbang validasi | 30 gerbang numerik lulus pada template generator dan builder A; gerbang tahap render (PG1–PG10, PG11a, uji builder PG11b, PG12, A1b, A6b) lulus pada 1.248 dan 96 prompt | 12.28 |
| Verifikasi dua implementasi | Implementation A dan B (B mengevaluasi ulang dari teks yang dirender) setuju; keterbatasan: satu penulis, independensi hanya pada jalur kode | 12.29, spec §11 dan baris 728 |
| Pembekuan | register FZ-v1, manifest Step 7 dan Step 8, indeks FZ (daftar L-B, 19 file) dengan hash resmi `a86da74ee5fb29180a85fe265af8fc201f3cc154d1356c53410cbc311b56f870` | 12.47–12.60 |
| Runner dan gate | ledger berantai hash, bukti mentah sebelum parsing, tanpa retry, aturan henti 13.8, penegakan indeks FZ (E-1), safe-stop respons penyedia (MD-06), resume yang gagal-tertutup | `research_design/step10/`, 12.50–12.55 |
| Pengujian | suite Step 10 lengkap terakhir: 275 tes lulus; modul pembaca O4 (19), suplemen deskriptif (11), dan kelayakan lokal (19) lulus sendiri-sendiri **[PERIKSA: jalankan ulang suite lengkap bila ingin satu angka gabungan]** | sesi kerja 2026-10-15/16 |

**Catatan tentang kerangka tata kelola.** Penelitian berjalan tanpa advisor; semua keputusan tata kelola diambil owner sendiri dan dicatat append-only (12.50). Penyimpangan dari spesifikasi dicatat sebagai keputusan, bukan dengan mengubah spesifikasi.

## 3. Penyimpangan dan keputusan yang memengaruhi interpretasi

| Hal | Keputusan | Dampak pada klaim | Rujukan |
|---|---|---|---|
| Cek buta manusia (H1, 624 baris) | tidak dilakukan; diganti penyimpangan tercatat dengan waiver | lapisan pembacaan manusia atas teks yang dirender tidak ada; ambiguitas penyajian tidak dapat dikecualikan | 12.56, 12.57 |
| Pelaporan kappa | K1: kappa tidak dihitung | tidak ada klaim reliabilitas antar-penilai atau kappa; hanya satu pengode | 12.51 (OD-3) |
| Rehearsal codebook (H4) | opsi (i): dicatat sebagai keterbatasan; B10 dan B36 tidak terklasifikasi | angka kesepakatan 77,5 % (`s2_values`) dan 60 % (`s2_arith`) bukan bukti validitas atau reliabilitas | 12.53, 12.58 |
| Pembacaan "used" untuk `s2_values` | pembacaan luas owner sebagai aturan operasional | berbeda dari redaksi codebook; dilaporkan sebagai keterbatasan | 12.39, 12.53 |
| Pilot | dihentikan setelah ronde 1 (N3) | tidak ada main run | 12.61 |

## 4. Pilot ronde 1 (Gemini): hasil struktural

Pilot dijalankan sekali pada 2026-10-15 (`run_id` 913c30983b1087a1), model `gemini-3.5-flash-lite`, pengaturan beku (delay 1 detik, retries 0, concurrency 1). Analisis pilot hanya struktural (spec §13.7); verdict dan kesepakatan dengan kebenaran dasar tidak dihitung atau ditampilkan.

| Butir | Nilai |
|---|---|
| Panggilan tercatat | 18 dari 18 (`RUN_COMPLETE`, tanpa halt) |
| HTTP 200 | panggilan 1–16 |
| HTTP 429 | panggilan 17 dan 18 (tanpa model, finish reason, atau usage) |
| SF1 / SF2 / SF3 / SF4 / SF5 | 2 / 0 / 0 / 0 / 0 |
| UNP | 3 dari 18 (1/6; ambang `theta_unp` = 1/2) |
| `f_S` | 1; `SF1 + SF4` = 2 melebihi `f_S` |
| **Hasil resmi ronde** | **FAIL-S** (`s11_pilot report`; sha256 laporan `b84f82602d387f4f007b3ec659c5be8a0f4787894a7eca3414da6ffacffc080d`) |
| Hash ledger akhir | `2af68583f5b4256e49eac566c3fbe2f914ebe3a852c63cc8e658483532e75aa9` |
| Biaya teramati | batas bawah US$0,0141; konservatif US$0,0556 (batas US$100) |
| Keputusan akhir pilot (`decide`) | tidak dijalankan: FAIL-S ronde 1 tidak menghasilkan record keputusan |

**O4 (pengukuran token dari pilot).** Status resmi **INCONCLUSIVE**: 16 dari 18 record punya `promptTokenCount` valid, panggilan 17 dan 18 tidak (HTTP 429). Nilai B resmi tidak dihitung; perhitungan atas 16 record saja tidak memenuhi kriteria penerimaan yang disetujui. Asumsi 1.016 token per panggilan tetap berstatus asumsi.

**Suplemen deskriptif tidak resmi atas 16 panggilan HTTP 200** (bukan hasil pilot, bukan pilot yang lulus, mengubah populasi analisis): UNP 3 dari 16; seluruh `finish_reason` STOP; latensi 938–5.094 ms (rata-rata 2.418,9); `promptTokenCount` 216–274. Hanya untuk perencanaan pacing dan biaya. **[PERIKSA: putuskan apakah suplemen ini dimasukkan]**

## 5. Insiden HTTP 429 dan analisis kapasitas

**Fakta.** Dua panggilan terakhir ditolak penyedia dengan HTTP 429. Runner tidak menyimpan isi body error, sehingga alasan tertulis penolakan tidak tersedia. Semua 18 permintaan dimulai dalam dua menit UTC (1 pada 09:23, 17 pada 09:24); panggilan 2–16 (15 panggilan) berhasil di menit 09:24, lalu panggilan 17 dan 18 gagal. Kuota konsol yang dilaporkan owner: tier Free, 15 RPM, 250.000 TPM, 500 RPD.

**Penyebab: tidak terkonfirmasi.** Hipotesis yang konsisten dengan data (bukan fakta): batas 15 permintaan per menit jam tetap (cocok persis), batas 16 per menit bergulir (cocok), kuota harian atau penyebab lain (tidak dapat dikecualikan). Batas bergulir 15 kurang cocok karena panggilan ke-16 dalam 53 detik berhasil. Dokumentasi resmi tidak memuat angka batas untuk model ini; angka kuota hanya bersumber dari laporan owner. **[PERIKSA: lampirkan tangkapan atau salinan angka konsol bila akan dikutip sebagai bukti]**

**Implikasi kapasitas.** Pada tier Free, 500 permintaan per hari kurang dari seperlima dari 2.496 panggilan main run, dan resume setelah halt ditutup oleh keputusan yang berlaku (12.43–12.45). Anggaran API tidak tersedia, sehingga jalur Gemini ditutup secara praktis.

## 6. Keputusan menghentikan eksperimen pilot (N3)

Spesifikasi §13.6 untuk FAIL-S di ronde 1 hanya memberi dua cabang: satu perubahan dari whitelist (untuk SF1: `timeout`, `inter-call delay`, atau `retry count`) yang dicatat sebagai versi FZ baru lalu ronde 2, atau STOP. Pengulangan dengan FZ yang sama bukan cabang resmi. Owner memilih STOP (entri 12.61) karena kendala di atas dan karena penyebab 429 serta kapasitas proyek tidak terverifikasi. Keputusan itu menghentikan **eksperimen pilot saat ini**; ia bukan pernyataan bahwa penelitian gagal, selesai, atau bahwa hipotesis terbukti atau tidak terbukti. Ronde 2 tidak dijalankan, jalur versi FZ baru tidak ditempuh, dan tidak ada record keputusan pilot. Opsi yang dipertimbangkan dan tidak ditempuh (ronde 2 dengan FZ-v1 sebagai penyimpangan; perubahan delay dengan R-7 dan pembekuan ulang) beserta biayanya didokumentasikan di `DRAFT_ROUND1_DISPOSITION_AND_429_REVIEW_2026-10-15.md`.

## 7. Evaluasi kelayakan model lokal (eksploratori, bukan pilot)

**Tujuan dan batas.** Memeriksa apakah model lokal `llama3.2:3b` (Ollama) dapat menjalankan format respons beku tiga bidang dengan andal dan cukup cepat. Bukan pilot, bukan data eksperimen, tidak memakai prompt registry atau pilot, dan tidak menguji hipotesis. Kriteria ditetapkan di kode sebelum run (UNP ≤ 10 % lanjut; ≤ 25 % keputusan owner; di atasnya berhenti; kegagalan struktural ≤ 1 dari 80 dan tanpa pemotongan; proyeksi 2.496 panggilan ≤ 24 jam).

**Metode.** 64 panggilan sintetis (16 template × kondisi A–D, dari generator dan perender beku pada basis yang tidak beririsan dengan registry) ditambah 16 pengulangan, plus dua probe di luar hitungan; satu run pada 2026-10-16, di mesin owner, Ollama 0.6.7, `num_ctx` 16384, `num_predict` 8192, decoding bawaan.

| Butir | Hasil |
|---|---|
| Status terhadap kriteria | FEASIBILITY_PROCEED (UNP, struktural, waktu) |
| SF1–SF5 / UNP | 0 / 0 / 0 / 0 / 0 / UNP 2 dari 80 (2,5 %) |
| Latensi | rata-rata 1.506,8 ms; median 1.328; maksimum 4.328; sekitar 70 token/detik; proyeksi 2.496 panggilan ≈ 1,04 jam (hanya untuk mesin ini) |
| Stabilitas pengulangan | teks identik 0 dari 16 pasangan; hasil identik 13 dari 16 (decoding bawaan acak) |
| Probe | `done_reason` "length" saat dipotong (nilai ini tidak terdokumentasi, teramati untuk versi ini); "stop" normal |
| **Informasional, bukan kriteria** | 36 dari 78 respons yang dapat di-parse sesuai ekspektasi sintetis (≈ 46 %, mendekati tingkat kebetulan untuk dua kelas); satu run, n = 80, tanpa selang |

**Interpretasi yang diperbolehkan.** Format beku dipatuhi dengan andal oleh model ini pada data sintetis, dan kecepatan memadai. **Tidak** dapat disimpulkan bahwa model ini mampu atau tidak mampu pada tugas penelitian, bahwa ia setara dengan Gemini, atau bahwa hasil pada prompt sintetis berlaku untuk prompt registry. Angka sekitar 46 % menandakan risiko efek lantai (TH10) bila model ini dipakai; itu bukan temuan. Bila hasil ini kelak dipakai memilih model, pilihan tersebut terinformasi pilot dan harus diungkapkan dengan lineage (pilot Gemini FAIL-S; evaluasi ini). Entri 12.62 mencatat bahwa STOP 12.61 tetap berlaku dan tidak ada kelanjutan yang diotorisasi.

## 8. Keterbatasan dan ancaman validitas

1. **Hasil utama tidak ada.** Tidak ada estimasi kinerja, tidak ada kontras antar kondisi, tidak ada inferensi.
2. **Pilot tidak lulus.** FAIL-S oleh dua panggilan 429; penyebab tidak terkonfirmasi; pilot berakhir tanpa PASS.
3. **Satu model, satu pengaturan penyedia** (TH11); nondeterminisme decoding bawaan dan drift penyedia tidak dikendalikan.
4. **Tidak ada cek buta manusia** (H1 di-waive); independensi A, B, generator, dan skrip hanya pada jalur kode; satu penulis.
5. **Satu pengode, tanpa kappa, tanpa reliabilitas antar-penilai** (OD-3, K1); codebook ditulis oleh pengode; rehearsal terpapar label AI dan tanpa prompt, sehingga `s2_values` dan `s2_arith` tidak dapat dinilai penuh dari teks komentar.
6. **Paparan peneliti terhadap keluaran Stage 1/2** (TH14) dan **pilot kecil, basis kasar** (TH17).
7. **Klaim reviewer satu sisi** (TH9): efek klaim tidak dapat dipisahkan dari efek "pernyataan pelanggaran" umum.
8. **Efek lantai/langit-langit** (TH10) tidak dapat dinilai; bukti informasional pada model lokal menunjukkan risiko lantai.
9. **Asumsi token tidak diukur** (O4 INCONCLUSIVE).
10. **Tanpa advisor**: seluruh keputusan tata kelola oleh satu orang; tidak ada tinjauan eksternal.
11. **Pembekuan terjadi setelah paparan peneliti terhadap desain dan tidak ada pra-registrasi eksternal**; hash dan decision record append-only adalah mitigasi, bukan pengganti pra-registrasi. **[PERIKSA: sesuaikan dengan kebijakan institusi]**

**[PERIKSA]** Teks lengkap TH1–TH18 dan bagian "Other threats" di spec §20 belum saya baca penuh; sesuaikan butir di atas dengan redaksi aslinya sebelum finalisasi.

## 9. Kontribusi yang dapat dipertanggungjawabkan dan pekerjaan lanjutan

**Kontribusi (klaim rekayasa dan metodologi, bukan klaim empiris tentang model):**
- Protokol dan generator skenario dengan kebenaran dasar deterministik, gerbang validasi, dan verifikasi dua implementasi.
- Prosedur pembekuan dan audit yang dapat direproduksi (hash register, indeks FZ, ledger, decision record).
- Pelajaran praktis: kapasitas laju dan kuota harian penyedia harus diperiksa sebelum pilot; pacing beku 1 detik tidak aman terhadap batas 15 permintaan per menit; body error penyedia sebaiknya disimpan.
- Bukti bahwa format respons beku dapat dipatuhi model lokal kecil pada data sintetis (eksploratori).

**Pekerjaan lanjutan yang mungkin (semuanya memerlukan keputusan owner baru, tidak diotorisasi di sini):** tier berbayar dan ronde 2 dengan perubahan whitelist `inter-call delay` (FZ baru, R-7); versi metodologi pengganti dengan model lokal (FZ baru, adapter, pilot baru); evaluasi model lokal yang lebih besar dengan harness dan kriteria yang sama.

## 10. Kesimpulan

Rancangan dan instrumen telah dibangun dan diverifikasi sintetis; pilot ronde 1 pada Gemini berstatus FAIL-S karena dua penolakan batas laju yang penyebabnya tidak terkonfirmasi; eksperimen pilot dihentikan; hasil utama tidak tersedia, sehingga penelitian ini tidak membuktikan atau menolak hipotesis apa pun. Status akhir: **BLOCKED / INCONCLUSIVE untuk eksperimen utama.** **[ISI: kalimat penutup sesuai konvensi institusi]**

---

## Lampiran A. Rujukan keputusan (decision record)

12.38 (PG3), 12.39 (rehearsal, pembacaan "used"), 12.43–12.45 (resume, kelas error), 12.46–12.49 (PRD-5, D4, D6, MD-07, MD-03, K2 verb), 12.50 (owner sebagai pengambil keputusan tunggal; MD-06; B-1; E-1; P11/P12), 12.51 (K1, R-7 tidak diotorisasi), 12.52 (MD-10), 12.53 (H4 opsi (i)), 12.54 (aturan ronde lanjutan), 12.55 (P5/E-1), 12.56–12.57 (waiver H1 dan gate), 12.58 (konfirmasi manifest, catatan SW), 12.59 (H5 ronde 1), 12.60 (hash FZ resmi), 12.61 (N3), 12.62 (kelayakan lokal).

## Lampiran B. Hash artefak kunci

| Artefak | sha256 |
|---|---|
| Hash FZ resmi (indeks L-B) | `a86da74ee5fb29180a85fe265af8fc201f3cc154d1356c53410cbc311b56f870` |
| Laporan resmi ronde 1 | `b84f82602d387f4f007b3ec659c5be8a0f4787894a7eca3414da6ffacffc080d` |
| Ledger akhir pilot | `2af68583f5b4256e49eac566c3fbe2f914ebe3a852c63cc8e658483532e75aa9` |
| Manifest Step 8 build | `09eed00eeb79e04ccaf607a66642417cdbbdfe802b19e580a67f4b9e08c7aaa5` |
| Evaluasi lokal: `summary.json` / `calls.jsonl` / `provenance.json` | lihat entri 12.62 |

## Lampiran C. Daftar periksa sebelum finalisasi

- [ ] Verifikasi angka 12.28 (template, prompt, gerbang) dan hasil suite lambat Step 8.
- [ ] Baca penuh spec §20 (TH1–TH18) dan sesuaikan §8.
- [ ] Putuskan apakah suplemen 16 panggilan dimasukkan dan di bagian mana.
- [ ] Putuskan apakah angka kuota konsol perlu bukti terlampir.
- [ ] Sesuaikan bentuk dengan format tesis dan kebijakan institusi.
- [ ] Jalankan ulang suite lengkap bila satu angka gabungan diinginkan.
- [ ] Tinjau seluruh klaim terhadap daftar "tidak boleh" pada outline.
