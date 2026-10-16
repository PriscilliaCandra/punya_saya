# DRAFT BAB (versi 2) — Pilot Tidak Lulus dan Hasil Utama Tidak Tersedia

**Status dokumen:** DRAFT UNTUK DITINJAU OWNER. Bukan versi final. Versi 2 (2026-10-16) menggantikan penanda yang bisa diverifikasi dari repositori pada versi 1 (`BAB_LAPORAN_PILOT_TIDAK_LULUS_DRAFT_2026-10-16.md`, tidak diubah). Sumber: decision record `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md` (entri 12.38–12.62), artefak pilot, spesifikasi v2.7. Penanda **[PERIKSA]** tersisa hanya untuk hal yang tidak dapat diverifikasi dari repositori; **[ISI]** menandai bagian yang hanya kamu yang bisa menulis.

> **Status penelitian: BLOCKED / INCONCLUSIVE untuk eksperimen utama.** Eksperimen utama (2.496 panggilan) tidak dijalankan. Pilot ronde 1 berstatus resmi FAIL-S. Karena itu bab ini **tidak melaporkan hasil tentang perilaku model**, tidak menguji hipotesis, dan tidak menyatakan hipotesis terbukti atau tidak terbukti.

---

## Ringkasan

Penelitian ini merancang protokol untuk mengukur apakah sebuah model bahasa dapat mengklasifikasikan suatu rencana latihan lari sebagai memenuhi atau melanggar aturan yang dinyatakan, dibandingkan dengan kebenaran deterministik, di bawah empat kondisi (rencana valid atau melanggar, dengan atau tanpa klaim reviewer). Bab ini melaporkan apa yang berhasil dibangun (generator skenario, gerbang validasi, verifikasi dua implementasi, prosedur pembekuan, dan runner yang diaudit), satu pilot 18 panggilan pada model Gemini yang berstatus FAIL-S karena dua panggilan ditolak penyedia dengan HTTP 429, keputusan menghentikan eksperimen pilot, dan satu evaluasi kelayakan eksploratori pada model lokal dengan data sintetis. Hasil utama tidak tersedia. Kontribusi yang dapat dipertanggungjawabkan terbatas pada rancangan metodologi, instrumen yang dapat diaudit, dan pelajaran tentang kendala kapasitas infrastruktur. **[ISI: sesuaikan dengan format tesis/institusi]**

## 1. Pendahuluan, konstruk, dan batas klaim

**Konstruk.** Klasifikasi kendala: diberikan aturan yang dinyatakan dan rencana latihan lengkap, apakah model terpilih mengembalikan verdict (`satisfied`, `violated`, atau `unclear`) yang cocok dengan keadaan deterministik rencana (spesifikasi v2.7, §1). Klasifikasi adalah satu-satunya tugas primer; model tidak diminta merevisi, menghitung ulang, menyetujui, atau menjelaskan.

**Kebenaran dasar bersifat biner.** Setiap skenario berisi informasi lengkap, sehingga verdict `unclear` selalu dihitung sebagai kesalahan dan dilaporkan sebagai laju tersendiri (spec §1).

**Desain.** Dua keluarga aturan (`MIL`: batas kenaikan jarak mingguan; `PAC`: konsistensi pace balapan), empat kondisi (A: valid tanpa klaim; B: melanggar tanpa klaim; C: valid dengan klaim reviewer palsu; D: melanggar dengan klaim benar), 12 sel primer, dan dua pengulangan per template pada main run yang direncanakan.

**Yang tidak diklaim.** Bab ini tidak mengklaim kompetensi model, tidak mengklaim pengaruh klaim reviewer, posisi, atau margin terhadap verdict, dan tidak mengklaim generalisasi ke model lain. Kontras antar kondisi tidak pernah dihitung (analisis pilot hanya struktural, spec §13.7).

## 2. Desain dan instrumen yang dibangun

| Komponen | Status | Sumber |
|---|---|---|
| Registry utama | 312 template (104 `MIL`, 208 `PAC`), 1.248 prompt berbeda, 2.496 slot panggilan direncanakan | record 12.28 (diverifikasi dari teks record) |
| Registry pilot | 24 template, 96 prompt; pilot 18 panggilan, satu repetisi | 12.28, spec §13.3 |
| Gerbang validasi | 30 gerbang numerik lulus pada template generator dan pada builder A; E-ID, E-PAR, E-GATE, E-PROMPT lulus; PG1–PG10, PG11a, uji builder PG11b, PG12, A1b, dan A6b lulus pada 1.248 prompt utama dan 96 prompt pilot; dua build identik byte; verifier mandiri Step 8 tidak menemukan masalah | 12.28 |
| Verifikasi dua implementasi | Implementation B (hanya pustaka standar, tanpa mengimpor modul proyek) membaca prompt yang dirender dan menghitung ulang keadaan, rho, dan gerbang: hasil AGREE tanpa kegagalan pada registry utama dan pilot. Keterbatasan: satu penulis; independensi hanya pada jalur kode | 12.29, spec §11 dan baris 728 |
| Pembekuan | register FZ-v1, manifest Step 7 dan Step 8, indeks FZ (daftar L-B, 19 file) dengan hash resmi `a86da74ee5fb29180a85fe265af8fc201f3cc154d1356c53410cbc311b56f870` | 12.47–12.60 |
| Runner dan gate | ledger berantai hash, bukti mentah sebelum parsing, tanpa retry, aturan henti 13.8, penegakan indeks FZ (E-1), safe-stop respons penyedia (MD-06), resume yang gagal-tertutup | `research_design/step10/`, 12.50–12.55 |

**Hasil pengujian (dijalankan ulang 2026-10-16, semua lulus):**

| Suite | Tes | Gagal / error |
|---|---|---|
| Step 10 (runner, skoring, integritas, resume, E-1, safe-stop, waiver, O4, suplemen, kelayakan lokal) | 324 | 0 / 0 |
| Step 7 (parser, decision script, dsb.) | 150 | 0 / 0 |
| Implementasi A (Step 4) | 123 | 0 / 0 |
| Step 8 (konstruksi dan build) | 30 | 0 / 0 |
| Step 9 (Implementation B; blind check) | 10; 6 | 0 / 0 |

Angka ini menunjukkan perilaku kode sesuai spesifikasi pengujiannya; ini fakta rekayasa dan bukan bukti validitas ilmiah. Pada Step 8 satu tes negatif memang memicu pesan "BUILD REJECTED" dan itu hasil yang diharapkan.

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

**Suplemen deskriptif tidak resmi atas 16 panggilan HTTP 200** (bukan hasil pilot, bukan pilot yang lulus, mengubah populasi analisis): UNP 3 dari 16; seluruh `finish_reason` STOP; latensi 938–5.094 ms (rata-rata 2.418,9); `promptTokenCount` 216–274. Hanya untuk perencanaan pacing dan biaya. **[ISI: putuskan apakah suplemen ini dimasukkan; keluarannya hanya ada di terminal dan percakapan, tidak tersimpan sebagai file]**

## 5. Insiden HTTP 429 dan analisis kapasitas

**Fakta.** Dua panggilan terakhir ditolak penyedia dengan HTTP 429. Runner tidak menyimpan isi body error, sehingga alasan tertulis penolakan tidak tersedia. Semua 18 permintaan dimulai dalam dua menit UTC (1 pada 09:23, 17 pada 09:24); panggilan 2–16 (15 panggilan) berhasil di menit 09:24, lalu panggilan 17 dan 18 gagal. Kuota konsol yang dilaporkan owner: tier Free, 15 RPM, 250.000 TPM, 500 RPD.

**Penyebab: tidak terkonfirmasi.** Hipotesis yang konsisten dengan data (bukan fakta): batas 15 permintaan per menit jam tetap (cocok persis), batas 16 per menit bergulir (cocok), kuota harian atau penyebab lain (tidak dapat dikecualikan). Batas bergulir 15 kurang cocok karena panggilan ke-16 dalam 53 detik berhasil. Dokumentasi resmi yang dibaca tidak memuat angka batas untuk model ini; angka kuota hanya bersumber dari laporan owner. **[PERIKSA: lampirkan tangkapan atau salinan angka konsol bila akan dikutip sebagai bukti]**

**Implikasi kapasitas.** Pada tier Free, 500 permintaan per hari kurang dari seperlima dari 2.496 panggilan main run, dan resume setelah halt ditutup oleh keputusan yang berlaku (12.43–12.45). Anggaran API tidak tersedia, sehingga jalur Gemini ditutup secara praktis.

## 6. Keputusan menghentikan eksperimen pilot (N3)

Spesifikasi §13.6 untuk FAIL-S di ronde 1 hanya memberi dua cabang: satu perubahan dari whitelist (untuk SF1: `timeout`, `inter-call delay`, atau `retry count`) yang dicatat sebagai versi FZ baru lalu ronde 2, atau STOP. Pengulangan dengan FZ yang sama bukan cabang resmi. Owner memilih STOP (entri 12.61) karena kendala di atas dan karena penyebab 429 serta kapasitas proyek tidak terverifikasi. Keputusan itu menghentikan **eksperimen pilot saat ini**; ia bukan pernyataan bahwa penelitian gagal, selesai, atau bahwa hipotesis terbukti atau tidak terbukti. Ronde 2 tidak dijalankan, jalur versi FZ baru tidak ditempuh, dan tidak ada record keputusan pilot. Opsi yang dipertimbangkan dan tidak ditempuh (ronde 2 dengan FZ-v1 sebagai penyimpangan; perubahan delay dengan R-7 dan pembekuan ulang) beserta biayanya didokumentasikan di `DRAFT_ROUND1_DISPOSITION_AND_429_REVIEW_2026-10-15.md`.

## 7. Evaluasi kelayakan model lokal (eksploratori, bukan pilot)

**Tujuan dan batas.** Memeriksa apakah model lokal `llama3.2:3b` (Ollama) dapat menjalankan format respons beku tiga bidang dengan andal dan cukup cepat. Bukan pilot, bukan data eksperimen, tidak memakai prompt registry atau pilot, dan tidak menguji hipotesis. Kriteria ditetapkan di kode sebelum run (UNP ≤ 10 % lanjut; ≤ 25 % keputusan owner; di atasnya berhenti; kegagalan struktural ≤ 1 dari 80 dan tanpa pemotongan; proyeksi 2.496 panggilan ≤ 24 jam).

**Metode.** 64 panggilan sintetis (16 template × kondisi A–D, dari generator dan perender beku pada basis yang tidak beririsan dengan registry) ditambah 16 pengulangan, plus dua probe di luar hitungan; satu run pada 2026-10-16, di mesin owner, Ollama 0.6.7, `num_ctx` 16384, `num_predict` 8192, decoding bawaan.

| Butir | Hasil |
|---|---|
| Status terhadap kriteria | FEASIBILITY_PROCEED (UNP, struktural, waktu) |
| SF1–SF5 / UNP | semua SF 0; UNP 2 dari 80 (2,5 %) |
| Latensi | rata-rata 1.506,8 ms; median 1.328; maksimum 4.328; sekitar 70 token/detik; proyeksi 2.496 panggilan ≈ 1,04 jam (hanya untuk mesin ini) |
| Stabilitas pengulangan | teks identik 0 dari 16 pasangan; hasil identik 13 dari 16 (decoding bawaan acak) |
| Probe | `done_reason` "length" saat dipotong (nilai ini tidak terdokumentasi, teramati untuk versi ini); "stop" normal |
| **Informasional, bukan kriteria** | 36 dari 78 respons yang dapat di-parse sesuai ekspektasi sintetis (≈ 46 %, mendekati tingkat kebetulan untuk dua kelas); satu run, n = 80, tanpa selang |

**Interpretasi yang diperbolehkan.** Format beku dipatuhi dengan andal oleh model ini pada data sintetis, dan kecepatan memadai. **Tidak** dapat disimpulkan bahwa model ini mampu atau tidak mampu pada tugas penelitian, bahwa ia setara dengan Gemini, atau bahwa hasil pada prompt sintetis berlaku untuk prompt registry. Angka sekitar 46 % menandakan risiko efek lantai (TH10) bila model ini dipakai; itu bukan temuan. Bila hasil ini kelak dipakai memilih model, pilihan tersebut terinformasi pilot dan harus diungkapkan dengan lineage (pilot Gemini FAIL-S; evaluasi ini). Entri 12.62 mencatat bahwa STOP 12.61 tetap berlaku dan tidak ada kelanjutan yang diotorisasi.

## 8. Keterbatasan dan ancaman validitas

### 8.1 Ancaman dari spesifikasi §20 yang tetap berlaku (diverifikasi terhadap teks §20)

| ID | Ancaman (ringkas, mengikuti teks spesifikasi) | Relevansi untuk laporan ini |
|---|---|---|
| TH1–TH3 | Tidak ada pekan tepat sasaran pada rencana `PAC`; beberapa nilai "target pace" per rencana; pace yang ditampilkan berbeda dari referensi tersembunyi `G` | Konstruk operasional; berlaku bila desain dipakai lagi |
| TH4–TH6 | Aliasing kelas dengan basis × posisi × arah; klasterisasi basis; posisi × besaran basis × bentuk rencana (`MIL`) | Berlaku untuk analisis yang tidak dilakukan; dicatat sebagai keterbatasan desain |
| TH7–TH8 | Target selalu deviasi terbesar rencana (isyarat struktural konstan); kesulitan aritmetika berbeda antar keluarga, tanpa perbandingan lintas keluarga | Desain |
| TH9 | Klaim reviewer satu sisi: efek klaim tidak dapat dipisahkan dari "pernyataan pelanggaran" umum | Membatasi tafsir bila main run dijalankan kelak |
| TH10 | Efek lantai/langit-langit membuat margin dan kontras klaim tidak informatif | Terkait: bukti informasional model lokal mendekati kebetulan |
| TH11 | Satu model, satu pengaturan penyedia; drift penyedia dan nondeterminisme decoding bawaan tidak dikendalikan | Terbukti relevan: dua model yang dicoba berbeda, decoding bawaan acak teramati |
| TH12–TH13 | Presisi terbatas oleh jumlah basis `L`; multiplisitas 12 sel primer dan kontras | Tidak berlaku sebagai hasil: tidak ada analisis |
| TH14 | Paparan peneliti pada keluaran Stage 1/2 tidak dapat dibatalkan | Berlaku |
| TH15 | Familiaritas dengan nilai aturan terkenal | Hanya jika nilai terkenal dipilih |
| TH16 | Penyebut S2/S3 bergantung kondisi karena UNP dikecualikan | Tidak berlaku: tidak ada pengodean S2/S3 |
| TH17 | Grid basis kasar, panjang rencana terbatas, pilot kecil (18 panggilan, satu repetisi) yang hanya mendeteksi kegagalan struktural yang sering | Berlaku langsung pada pilot ini |
| TH18 | Daftar frasa rujukan reviewer meremehkan rujukan biasa; hitungan adalah batas bawah | Tidak berlaku: tidak ada pengodean |

**Ancaman lain dari §20 yang relevan:** (a) validitas pengukuran: parser dapat salah klasifikasi; independensi kebenaran dasar bersifat parsial (spesifikasi dan semantik aturan dipakai bersama; A/B satu penulis; pemeriksa mengetahui konstruksi dan dapat mengenali pasangan; kebutaan sempurna tidak diklaim); pemeriksaan dan pengodean satu peneliti lebih lemah daripada dua orang; pengodean S2 tidak buta terhadap kebenaran dasar; (b) reproduksibilitas: drift model penyedia dan nondeterminisme decoding bawaan; urutan eksekusi bergantung versi interpreter dan PRNG; hash memitigasi drift skenario tetapi tidak drift penyedia; (c) derajat kebebasan peneliti: parameter §17 adalah eksposur utama, tiap parameter diklasifikasikan, dibatasi, dan dijustifikasi sebelum generasi.

### 8.2 Keterbatasan khusus bab ini (tidak tercantum di §20)

1. **Hasil utama tidak ada.** Tidak ada estimasi kinerja, kontras antar kondisi, atau inferensi.
2. **Pilot tidak lulus.** FAIL-S oleh dua panggilan 429; penyebab tidak terkonfirmasi; pilot berakhir tanpa PASS.
3. **Tidak ada cek buta manusia** (H1 di-waive, 12.56); A, B, generator, dan skrip satu penulis.
4. **Satu pengode, tanpa kappa** (OD-3, K1); rehearsal terpapar label AI dan tanpa prompt, sehingga `s2_values` dan `s2_arith` tidak dapat dinilai penuh dari teks komentar; B10 dan B36 tidak terklasifikasi.
5. **Asumsi token tidak diukur** (O4 INCONCLUSIVE).
6. **Tanpa advisor**: seluruh keputusan tata kelola oleh satu orang; tidak ada tinjauan eksternal.
7. **Pembekuan tanpa pra-registrasi eksternal**: hash dan decision record append-only adalah mitigasi, bukan pengganti. **[PERIKSA: sesuaikan dengan kebijakan institusi]**
8. **Kendala infrastruktur**: kuota penyedia menutup main run pada tier gratis; tidak ada anggaran API.

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

## Lampiran B. Hash artefak kunci (sha256)

| Artefak | sha256 |
|---|---|
| Hash FZ resmi (indeks L-B) | `a86da74ee5fb29180a85fe265af8fc201f3cc154d1356c53410cbc311b56f870` |
| Laporan resmi ronde 1 | `b84f82602d387f4f007b3ec659c5be8a0f4787894a7eca3414da6ffacffc080d` |
| Ledger akhir pilot | `2af68583f5b4256e49eac566c3fbe2f914ebe3a852c63cc8e658483532e75aa9` |
| Manifest Step 8 build | `09eed00eeb79e04ccaf607a66642417cdbbdfe802b19e580a67f4b9e08c7aaa5` |
| Evaluasi lokal `summary.json` | `d63ec45ae111cdc9e40b18257f1211fcb440b7cbb9ea9f7453679823a8f6a568` |
| Evaluasi lokal `calls.jsonl` | `dfe30aa36f32b23544cfe0ce3b37703aab1106838146acd424847f3215efebe1` |
| Evaluasi lokal `provenance.json` | `32e4a100fb2134411f9ee5961e34528f29f2fa1d714228c79244ef594bd8b80d` |
| Evaluasi lokal `prompts_manifest.json` | `cdd92c9f982bcf82edb7c41e84072111418ed0d4135cf447dd6eb305a250a3f3` |

## Lampiran C. Daftar periksa yang tersisa (tidak dapat diverifikasi dari repositori)

- [ ] Putuskan apakah suplemen 16 panggilan dimasukkan dan di bagian mana (keluarannya tidak tersimpan sebagai file).
- [ ] Putuskan apakah angka kuota konsol perlu bukti terlampir (hanya laporan owner yang ada).
- [ ] Sesuaikan bentuk dengan format tesis dan kebijakan institusi, termasuk apakah laporan tanpa hasil utama memenuhi syarat S2.
- [ ] Kebijakan pra-registrasi institusi (butir 8.2 nomor 7).
- [ ] Tinjau seluruh klaim terhadap daftar "tidak boleh" pada outline.
- [ ] Tulis bagian bertanda [ISI] (ringkasan sesuai format, kalimat penutup).
