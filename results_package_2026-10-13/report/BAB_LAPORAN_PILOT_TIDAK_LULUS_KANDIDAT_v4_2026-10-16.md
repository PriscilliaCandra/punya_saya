# Pilot yang Tidak Lulus dan Ketiadaan Hasil Utama: Laporan Teknis atas Protokol Klasifikasi Kendala Rencana Latihan Lari oleh Model Bahasa

**Status dokumen:** kandidat v4 untuk ditinjau owner (2026-10-16). **Belum final, dan bukan pernyataan bahwa laporan atau tesis selesai.** Versi sebelumnya dipertahankan tanpa perubahan: v1 (`ce382532…`), v2 (`da0afa2e…`), v3 (`a398db7d…`); hash lengkap ada di Lampiran E. Semua penanda kerja pada v3 telah diganti dengan pernyataan keterbatasan atau catatan konfirmasi; hal yang masih menunggu konfirmasi manusia atau institusi dikumpulkan di Lampiran C.

> **Status penelitian: BLOCKED / INCONCLUSIVE untuk eksperimen utama.** Eksperimen utama (2.496 panggilan atas 1.248 prompt) tidak dijalankan, dan **hasil utama tidak tersedia**. Pilot ronde 1 berstatus resmi **FAIL-S**; pengukuran token O4 berstatus **INCONCLUSIVE**; eksperimen pilot dihentikan oleh keputusan 12.61. Bab ini tidak melaporkan hasil tentang perilaku model dan tidak menyatakan hipotesis terbukti atau tidak terbukti.

---

## Ringkasan

Penelitian ini merancang protokol deskriptif untuk mengukur seberapa sering sebuah model bahasa, diberi aturan tertulis dan rencana latihan lari yang lengkap, mengembalikan verdict (`satisfied`, `violated`, atau `unclear`) yang cocok dengan keadaan rencana yang dapat dihitung secara deterministik. Desainnya memakai dua keluarga aturan (batas kenaikan jarak mingguan dan konsistensi pace balapan), empat kondisi (rencana valid atau melanggar, dengan atau tanpa klaim reviewer), 12 sel primer, dan 2.496 panggilan terencana atas 1.248 prompt berbeda. Bab ini melaporkan apa yang berhasil dibangun: generator skenario berbasis enumerasi deterministik, gerbang validasi numerik dan tahap render, verifikasi oleh dua implementasi terpisah, prosedur pembekuan berbasis hash, dan runner berledger yang diaudit. Ia juga melaporkan satu pilot 18 panggilan pada model Gemini yang berstatus FAIL-S karena dua panggilan ditolak penyedia dengan HTTP 429 yang penyebabnya tidak terkonfirmasi, keputusan menghentikan eksperimen pilot, dan satu evaluasi kelayakan eksploratori pada model lokal dengan data sintetis. **Hasil utama pada 1.248 prompt tidak tersedia.** Karena itu tidak ada kesimpulan tentang akurasi model pada tugas utama, pengaruh kondisi atau klaim reviewer, atau pertanyaan penelitian primer, dan tidak ada klaim bahwa Gemini dan model lokal setara. Kontribusi yang dapat dipertanggungjawabkan terbatas pada rancangan metodologi, instrumen yang dapat diaudit, dan pelajaran tentang kendala kapasitas infrastruktur. Format ringkasan dan panjangnya mengikuti ketentuan institusi yang belum dikonfirmasi (Lampiran C).

## 1. Pendahuluan

### 1.1 Latar dan tujuan

Model bahasa semakin sering dipakai untuk memeriksa apakah suatu rencana memenuhi aturan yang dinyatakan. Pada rencana latihan lari, aturan seperti batas kenaikan jarak mingguan atau konsistensi pace terhadap waktu target mengandung aritmetika yang dapat diperiksa dengan pasti. Penelitian ini memanfaatkan sifat itu: setiap skenario dibangun secara deterministik sehingga keadaan sebenarnya (memenuhi atau melanggar) diketahui, dan perilaku model dibandingkan dengan keadaan tersebut. Tujuan awalnya adalah memperoleh gambaran deskriptif bagi satu model terpilih; tujuan bab ini adalah melaporkan secara jujur apa yang telah dicapai, mengapa eksperimen utama tidak terlaksana, dan apa yang tidak boleh disimpulkan.

### 1.2 Sifat deskriptif dan pertanyaan penelitian

Pertanyaan primer dalam spesifikasi v2.7 (§18.3) bersifat deskriptif: dalam setiap kondisi dan secara deskriptif, seberapa sering model terpilih mengembalikan verdict yang cocok dengan keadaan deterministik rencana, dilaporkan terpisah untuk rencana valid dan melanggar, per keluarga aturan, dan per kelas margin. Spesifikasi menyatakan bahwa pertanyaan itu tidak mengimplikasikan klaim kausal, umum, medis, atau tingkat populasi, dan bahwa tidak ada uji hipotesis yang direncanakan (keputusan DP2). Karena itu bab ini tidak memakai bahasa "hipotesis terbukti" atau "hipotesis ditolak": desainnya tidak memuat hipotesis yang diuji, dan hasil utamanya memang tidak tersedia.

### 1.3 Batas klaim

Bab ini tidak mengklaim kompetensi model apa pun, pengaruh klaim reviewer, posisi, atau margin terhadap verdict, ataupun generalisasi ke model lain. Analisis pilot, menurut spesifikasi (§13.7), hanya struktural: hitungan kegagalan, porsi respons tak terparse, latensi, dan penggunaan token; kesepakatan dengan kebenaran dasar dan distribusi verdict tidak dihitung atau ditampilkan. Perbandingan Gemini dengan model lokal tidak dilakukan dan tidak boleh disimpulkan dari bab ini.

### 1.4 Peta bab

Bab 2 menguraikan rancangan. Bab 3 memaparkan instrumen, verifikasi, pembekuan, dan hasil pengujian perangkat lunak. Bab 4 mencatat tata kelola dan penyimpangan dari spesifikasi. Bab 5 sampai 7 melaporkan pilot ronde 1, insiden HTTP 429, dan keputusan menghentikan pilot. Bab 8 melaporkan evaluasi kelayakan model lokal. Bab 9 membahas keterbatasan, bab 10 kontribusi, dan bab 11 kesimpulan.

## 2. Rancangan penelitian

### 2.1 Konstruk dan kebenaran dasar

Konstruknya adalah klasifikasi kendala: diberi aturan yang dinyatakan dan rencana latihan lengkap, apakah model mengembalikan verdict yang cocok dengan keadaan rencana. Klasifikasi adalah satu-satunya tugas primer; model tidak diminta merevisi, menghitung ulang, menyetujui, atau menjelaskan. Setiap skenario berisi informasi lengkap, sehingga keadaan sebenarnya selalu `satisfied` atau `violated`; verdict `unclear` tidak pernah cocok dengan kebenaran dasar, dihitung sebagai ketidakcocokan, dan dilaporkan sebagai laju tersendiri. Respons yang tidak dapat diparse tetap berada di setiap penyebut.

### 2.2 Dua keluarga aturan

Keluarga `MIL` (progresi jarak mingguan) menyajikan tabel `Pekan | Total km` untuk N = 5 pekan dengan batas kenaikan P = 10 %. Semantiknya dibekukan: pekan 1 tidak dibandingkan; setiap pekan berikutnya dibandingkan hanya dengan pekan sebelumnya yang tertampil; penurunan atau tidak berubah memenuhi aturan; kenaikan yang tepat sama dengan batas memenuhi aturan; hanya kenaikan yang melebihi batas yang melanggar, yaitu 100·(X_w − X_{w−1}) > P·X_{w−1}; dan rencana melanggar bila setidaknya satu pekan melanggar.

Keluarga `PAC` (konsistensi pace) menyajikan jarak balapan D = 10 km, waktu target dalam format `H:MM:SS`, toleransi τ_F = 50 detik, dan tabel `Pekan | Target race pace (min/km)`. Waktu selesai tersirat suatu pekan adalah jarak dikali pace yang tertampil, dibulatkan ke detik terdekat dengan ketentuan setengah naik; selisihnya terhadap waktu target dibandingkan dengan toleransi. Pekan memenuhi bila selisih mutlak tidak melebihi τ_F (kesamaan memenuhi), dan rencana melanggar bila setidaknya satu pekan melanggar. Pembulatan dilakukan sekali, setelah perkalian. Pace referensi tersembunyi G tidak pernah ditampilkan; waktu target diturunkan dari G, sehingga pace yang tertampil tidak persis cocok dengan waktu target (ancaman TH1 sampai TH3, bab 9).

### 2.3 Kondisi dan klaim reviewer

Empat kondisi mengatur anggota rencana dan keberadaan blok klaim: A (valid, tanpa klaim), B (melanggar, tanpa klaim), C (valid, dengan klaim palsu), dan D (melanggar, dengan klaim benar). Blok klaim selalu menyatakan bahwa rencana melanggar aturan, bersumber dari "reviewer", dan teksnya identik byte pada kondisi C dan D serta pada semua template satu keluarga. Konsekuensinya, klaim bersifat satu sisi (tidak pernah menyatakan kepatuhan) dan menggabungkan sumber, pernyataan, isyarat otoritas, dan redaksi; eksperimen tidak mengisolasi otoritas dari unsur lain. Pasangan C dengan A serta D dengan B adalah kontras klaim yang prompt-nya identik byte kecuali blok klaim.

### 2.4 Margin, penjaga, dan kelas

Setiap template adalah satu konstruksi skenario deterministik (keluarga, basis, posisi pekan target, dan untuk `PAC` arah), yang menghasilkan sepasang rencana valid dan melanggar yang berbeda dalam tepat satu token numerik yang tertampil. Margin ternormalisasi ρ dihitung untuk keperluan konstruksi dan analisis: untuk `MIL`, kenaikan dibagi kenaikan yang diizinkan; untuk `PAC`, nilai mutlak deviasi waktu selesai yang tepat dibagi τ_F. Rencana melanggar bila ρ plan melebihi 1. Rencana valid memiliki kelas tunggal V dengan ρ pada jendela [0,60; 0,90]; rencana melanggar memiliki kelas MILD (ρ dalam [1,10; 1,30]) atau CLEAR ([1,50; 2,00]). Pekan bukan target dibangun dengan margin ρ_NT = 0,40. Sebuah penjaga sebesar sepersepuluh kilometer (`MIL`) atau satu detik waktu selesai (`PAC`) memisahkan anggota valid dan melanggar dari batas. Nilai ρ sebanding hanya dalam satu keluarga; kelas margin adalah manipulasi dalam keluarga dan tidak dibandingkan lintas keluarga.

### 2.5 Registry dan jumlah panggilan

Template dibangun tanpa langkah stokastik. Basis `MIL` adalah nilai awal 20,0 sampai 45,0 km dengan langkah 1,0 km; basis `PAC` adalah pace referensi 310 sampai 335 detik per km (5:10 sampai 5:35) dengan langkah 1 detik; masing-masing 26 basis. Posisi pekan target ada empat (K = 4, pekan 2 sampai 5), dan `PAC` memiliki dua arah. Hasilnya 104 template `MIL` dan 208 template `PAC`, yaitu 312 template dan 1.248 prompt berbeda (empat kondisi per template). Dengan dua pengulangan per prompt (R = 2) jumlah panggilan terencana adalah 4·R·312 = 2.496. Pilot memakai daftar basis terpisah (nilai awal 45,5 dan 46,5 km; pace referensi 340 dan 341 detik per km) yang tidak beririsan dengan daftar utama, dengan 24 template dan 96 prompt; pilot minimal 18 panggilan, satu repetisi, untuk menutup setiap sel keluarga dan kondisi dengan kelas dan arah yang relevan.

### 2.6 Format respons, parser, dan kegagalan struktural

Format respons beku terdiri atas tiga bidang: `Constraint:` (aturan yang disalin), `Verdict:` (`satisfied`, `violated`, atau `unclear`), dan `Comments:` (opsional). Parser verdict dan tata bahasanya dibekukan sebelum pilot dan diuji pada baterai sintetis yang ditulis tanpa akses ke respons pilot atau utama. Kegagalan struktural didefinisikan tanpa membaca isi: SF1 (kegagalan transport atau galat HTTP/API), SF2 (respons kosong), SF3 (pemotongan oleh batas token keluaran), SF4 (blokir penyedia atau tidak ada kandidat), dan SF5 (pengecualian pada parser atau skorer). Respons tak terparse (UNP: tanpa bidang `Verdict:`, dua bidang dengan token berbeda, atau token di luar tiga nilai) adalah hasil terukur, bukan kegagalan harness, dan tidak pernah diperbaiki.

### 2.7 Estimand dan rencana analisis

Hasil primer dilaporkan terpisah untuk kondisi A, B, C, dan D, tidak pernah digabung sebagai angka utama. Dua belas sel primer adalah, untuk setiap keluarga, A, C, B dengan kelas MILD dan CLEAR, serta D dengan kelas MILD dan CLEAR. Dalam tiap sel, empat proporsi dilaporkan terpisah: akurasi, kesalahan berlawanan (positif palsu atau negatif palsu), `unclear`, dan tak terparse; semuanya adalah rata-rata tingkat klaster dengan hitungan panggilan eksak. Unit perencanaan dan pengambilan ulang sampel adalah klaster (basis), bukan panggilan, karena template dengan basis yang sama bergantung satu sama lain. Interval dihitung dengan bootstrap klaster (10.000 ulangan) pada tingkat kepercayaan 0,95 per sel tanpa penyesuaian simultan; setengah-lebar perencanaan nominal bernilai 0,20, dengan catatan bahwa nilai itu optimistis bila basis berdekatan. Satu analisis sensitivitas yang dideklarasikan sebelumnya memakai penyebut hanya respons yang dapat diparse dan tidak menggantikan angka primer.

### 2.8 Pengodean sekunder

Komentar model dikodekan secara sekunder dan eksploratori (S2: bukti verifikasi; S3: sikap terhadap klaim reviewer) hanya setelah main run selesai atau dinyatakan tidak lengkap dan skor primer dihitung dan di-hash. Pengodean dilakukan oleh satu orang (keputusan OD-3), tidak buta terhadap kebenaran dasar, dan tidak dapat mengubah skor primer, parser, penyebut, atau registry.

## 3. Instrumen, verifikasi, dan pembekuan

### 3.1 Generator dan gerbang

Generator (`step8/s8_construct.py`) membangun template secara deterministik dari register parameter. Gerbang validasi dijalankan bertahap. Pada tahap numerik, 30 gerbang menguji kelayakan parameter, margin, penjaga, dan kebenaran konstruksi pada template generator maupun pada pembangun Implementation A. Pada tahap render, gerbang PG1 sampai PG10, PG11a, uji pembangun PG11b, PG12, A1b, dan A6b diterapkan pada 1.248 prompt utama dan 96 prompt pilot. Pemeriksaan kesetaraan E-ID, E-PAR, E-GATE, dan E-PROMPT membandingkan keluaran generator dengan pembangun A. Seluruhnya lulus pada build yang dipublikasikan, dua build identik byte, dan verifier mandiri Step 8 tidak menemukan masalah (record 12.28). Setiap kegagalan gerbang menolak seluruh build.

### 3.2 Verifikasi oleh dua implementasi

Implementation B hanya memakai pustaka standar dan tidak mengimpor modul proyek apa pun. Ia membaca teks prompt yang dirender, mengurai ketat, dan menghitung ulang keadaan anggota, ρ, kelas, dan sejumlah gerbang. Hasilnya AGREE tanpa kegagalan pada registry utama maupun pilot (12.29). Spesifikasi menegaskan keterbatasannya: bila satu orang menulis A, B, generator, dan melakukan pemeriksaan manusia, independensi hanya pada jalur kode dan bukan pada pikiran, dan pernyataan "A dan B ditulis tanpa membaca satu sama lain" tidak dapat diverifikasi.

### 3.3 Cek buta manusia: dirancang, tidak dilakukan

Spesifikasi menetapkan lapisan ketiga validasi berupa pemeriksaan buta oleh satu pembaca manusia dengan tunda minimal tujuh hari setelah peneliti terakhir melihat isi registry, dengan cakupan 100 % dari 624 anggota. Lapisan itu **tidak dilaksanakan**. Owner memutuskan (12.56) mengganti pemeriksaan tersebut dengan penyimpangan tercatat berupa pernyataan waiver, dan gate diubah untuk menerima waiver itu (12.57). Waiver adalah bukti sebuah keputusan, bukan bukti pemeriksaan yang berhasil: ia menyatakan eksplisit bahwa cek buta manusia tidak dilakukan. Akibatnya tidak ada bukti dari pembaca manusia bahwa teks yang dirender tidak ambigu.

### 3.4 Pembekuan

Urutan pembekuan yang mengikat (spesifikasi §21) menahan semua unsur yang memengaruhi pilot sebelum panggilan pertama: parameter, prompt, parser, kode generator, dan model beserta pengaturannya. Indeks FZ memuat peta path ke SHA-256 dari 19 berkas (spesifikasi, register FZ-v1, manifest Step 7, manifest Step 8, Implementation A, dan 14 berkas Step 7 dan Step 8) tanpa berkas harness Step 10; hash resminya `a86da74ee5fb29180a85fe265af8fc201f3cc154d1356c53410cbc311b56f870` dicatat di 12.60 setelah diverifikasi dengan alat penulis dan dengan verifier independen di gate. Setiap perubahan berkas terdaftar mengubah hash dan menuntut versi FZ baru serta pilot ulang.

### 3.5 Runner dan gate

Runner mencatat ledger berantai hash dengan entri niat sebelum panggilan, menyimpan rekaman mentah sebelum parsing, tidak pernah mengulang panggilan, dan menjalankan aturan henti. Gate menolak eksekusi kecuali pengaturan model sesuai register, verifier Step 8 bersih, Implementation B setuju, ada bukti Step 9 atau waiver, ada otorisasi owner yang cocok dengan lingkup dan jumlah panggilan dengan batas biaya terburuk di bawah batas US$100, dan indeks FZ valid beserta hash yang dicatat (E-1, 12.55). Safe-stop (MD-06) menghentikan run setelah rekaman tersimpan bila model yang dikembalikan tidak cocok, finish reason tidak terdaftar, atau rekaman tidak berstatus HTTP tanpa penanda error. Resume setelah halt ditutup (gagal-tertutup) karena kelas error belum diratifikasi (12.43 sampai 12.45).

### 3.6 Pengujian perangkat lunak

Semua suite dijalankan ulang pada 2026-10-16 di mesin owner. Lingkungan yang dapat diverifikasi: Windows (modul `platform` Python melaporkan `Windows-10-10.0.26300-SP0`; keterangan lingkungan sesi menyebut Windows 11 Pro build 10.0.26300), Python 3.11.9 (MSC v.1938, 64-bit AMD64), prosesor Intel64 Family 6 Model 191, kerangka `unittest`, dengan opsi `-B -I -W ignore`. Nama dagang prosesor, memori, dan akselerator tidak tercatat dan karena itu tidak dilaporkan. Pada evaluasi model lokal, Ollama versi 0.6.7 tercatat di berkas provenansi.

| Suite (berkas uji) | Cakupan | Tes | Gagal / error |
|---|---|---|---|
| `step10/test_*.py` | runner, skoring, integritas, resume, E-1, safe-stop, waiver gate, pembaca O4, suplemen deskriptif, harness kelayakan lokal, dan tes lain di folder | 324 | 0 / 0 |
| `step7/test_step7.py` | modul Step 7 (parser, decision script, dan lainnya) | 150 | 0 / 0 |
| `implementation_a/test_impl_a.py` | Implementation A ("Step 4" di record; sama dengan 123 tes di record baris 558) | 123 | 0 / 0 |
| `step8/test_step8.py` | konstruksi dan build Step 8 (satu tes negatif mencetak "BUILD REJECTED" sebagai hasil yang diharapkan) | 30 | 0 / 0 |
| `step9/test_impl_b.py` | Implementation B | 10 | 0 / 0 |
| `step9/test_blindcheck.py` | alat evaluator cek buta, bukan hasil pemeriksaan manusia | 6 | 0 / 0 |

Hasil ini hanya menunjukkan bahwa kode berperilaku sesuai pengujiannya sendiri. **Ia bukan bukti validitas ilmiah** konstruk, desain, atau instrumen, dan bukan bukti apa pun tentang model. Angka 324 mencakup tes untuk komponen yang ditulis selama pekerjaan pilot dan karenanya lebih besar daripada 275 yang diperoleh pada 2026-10-15.

## 4. Tata kelola dan penyimpangan dari spesifikasi

Penelitian berjalan tanpa advisor. Karena itu keputusan tata kelola yang oleh sumber ditugaskan kepada "owner dan advisor" diambil owner sendiri (12.50), dicatat append-only di decision record, dan penyimpangan dari spesifikasi dicatat sebagai keputusan dan bukan dengan mengubah teks spesifikasi. Konsekuensinya jelas: tidak ada tinjauan eksternal atas keputusan tata kelola mana pun, dan pembaca perlu menimbangnya.

| Hal | Keputusan | Dampak pada klaim | Rujukan |
|---|---|---|---|
| Cek buta manusia (H1, 624 baris) | tidak dilakukan; diganti penyimpangan tercatat dengan waiver | lapisan pembacaan manusia atas teks yang dirender tidak ada; ambiguitas penyajian tidak dapat dikecualikan | 12.56, 12.57 |
| Pelaporan kappa | K1: kappa tidak dihitung (penyimpangan tercatat dari kalimat spesifikasi tentang kappa) | tidak ada klaim kappa atau reliabilitas antar-penilai; hanya satu pengode | 12.51, OD-3 |
| Rehearsal codebook (H4) | opsi (i): dicatat sebagai keterbatasan; B10 dan B36 tidak terklasifikasi | kesepakatan mentah 77,5 % (`s2_values`) dan 60 % (`s2_arith`) bukan bukti validitas atau reliabilitas | 12.53, 12.58 |
| Pembacaan "used" untuk `s2_values` | pembacaan luas owner sebagai aturan operasional | berbeda dari redaksi codebook; dilaporkan sebagai keterbatasan | 12.39, 12.53 |
| Kebijakan resume dan kelas error | tidak ada kelas error yang diratifikasi untuk resume | run yang berhenti karena transport tidak dapat dilanjutkan | 12.43 sampai 12.45 |
| Pilot | dihentikan setelah ronde 1 (N3) | tidak ada main run | 12.61 |

Catatan penting: H1 tidak dilakukan dan K1 bukan pemeriksaan yang berhasil; keduanya adalah pilihan atau penyimpangan yang dicatat. Spesifikasi juga mengungkapkan bahwa peneliti telah melihat keluaran Stage 1 dan Stage 2 sebelum protokol ini dibekukan (§13.1); paparan itu tidak dapat dibatalkan, dan mitigasinya (kriteria yang dideklarasikan, pilot struktural, hash, batas ronde, aturan henti) tidak menggantikan pra-registrasi eksternal. Apakah mitigasi ini memenuhi kebijakan pra-registrasi institusi belum dikonfirmasi dan memerlukan konfirmasi institusi (Lampiran C).

## 5. Pilot ronde 1 pada Gemini

Pilot dijalankan sekali pada 2026-10-15 (`run_id` 913c30983b1087a1) pada model `gemini-3.5-flash-lite` dengan pengaturan beku: delay 1 detik antarpanggilan, tanpa percobaan ulang, satu panggilan pada satu waktu, batas waktu 180 detik. Sesuai spesifikasi, analisis pilot hanya struktural. Kegagalan struktural menentukan hasil ronde menurut tiga kategori: PASS (tanpa SF2, SF3, SF5, dengan SF1+SF4 ≤ `f_S`, dan porsi UNP ≤ θ_unp), FAIL-S (ada SF2, SF3, SF5, atau SF1+SF4 > `f_S`), dan FAIL-U (porsi UNP > θ_unp). Nilai terdeklarasi pada register adalah `f_S` = 1 dan θ_unp = 0,50.

| Butir | Nilai |
|---|---|
| Panggilan tercatat | 18 dari 18 (`RUN_COMPLETE`, tanpa halt) |
| HTTP 200 | panggilan 1 sampai 16 |
| HTTP 429 | panggilan 17 dan 18 (tanpa model, finish reason, atau usage) |
| SF1 / SF2 / SF3 / SF4 / SF5 | 2 / 0 / 0 / 0 / 0 |
| UNP | 3 dari 18 (1/6; di bawah θ_unp = 1/2) |
| **Hasil resmi ronde** | **FAIL-S** (SF1 + SF4 = 2 melebihi `f_S` = 1) |
| Laporan resmi | `pilot_round_1_report.json`, sha256 `b84f82602d387f4f007b3ec659c5be8a0f4787894a7eca3414da6ffacffc080d` |
| Hash ledger akhir | `2af68583f5b4256e49eac566c3fbe2f914ebe3a852c63cc8e658483532e75aa9` |
| Biaya teramati | batas bawah US$0,0141; konservatif US$0,0556 (batas US$100) |
| Keputusan akhir pilot (`decide`) | tidak dijalankan: FAIL-S pada ronde 1 tidak menghasilkan record keputusan |

Dari tiga kategori hasil, hanya komponen SF yang menentukan FAIL-S; porsi UNP sebesar 3 dari 18 berada di bawah ambang. Kedua kegagalan SF1 adalah panggilan terakhir dari 18, dan keduanya adalah penolakan penyedia, bukan kegagalan jaringan umum.

**O4 (pengukuran token dari pilot).** Prosedur O4 membandingkan `promptTokenCount` yang dilaporkan penyedia dengan panjang karakter prompt untuk memeriksa asumsi 1.016 token per panggilan yang dipakai dalam batas biaya terburuk. Status resmi O4 adalah **INCONCLUSIVE**: 16 dari 18 record memiliki `promptTokenCount` yang valid, sedangkan panggilan 17 dan 18 tidak memilikinya (keduanya HTTP 429). Karena data wajib hilang, batas B resmi tidak dihitung; perhitungan atas 16 record saja tidak memenuhi kriteria penerimaan yang disetujui. Asumsi 1.016 token tetap berstatus asumsi, bukan pengukuran.

**Catatan nonresmi.** Sebuah analisis deskriptif atas 16 panggilan HTTP 200 dijalankan di luar prosedur pilot. Ia bukan hasil pilot dan tidak menggantikan laporan resmi; provenansi dan keterbatasannya dijelaskan di Lampiran D.

## 6. Insiden HTTP 429 dan analisis kapasitas

**Fakta yang tercatat.** Dua panggilan terakhir ditolak penyedia dengan status HTTP 429. Runner hanya menyimpan status dan penanda error, tidak isi body, sehingga alasan tertulis penolakan tidak tersedia. Waktu mulai panggilan terekam: seluruh 18 permintaan dimulai dalam dua menit UTC (satu pada 09:23 dan 17 pada 09:24). Dalam menit 09:24, panggilan 2 sampai 16 (15 panggilan) berhasil, kemudian panggilan 17 dan 18 gagal. Rata-rata jarak antarpanggilan sekitar 3,3 sampai 3,5 detik (latensi rata-rata sekitar 2,4 detik ditambah delay 1 detik).

**Kuota.** Kuota yang diketahui berasal dari pengamatan owner pada konsol: tier Free, 15 permintaan per menit, 250.000 token per menit, dan 500 permintaan per hari. **Tidak ada artefak independen di repositori yang memuat angka ini** (tidak ada tangkapan layar atau ekspor konsol), sehingga angka tersebut diperlakukan sebagai pengamatan owner yang belum diverifikasi secara independen. Dokumentasi resmi yang dibaca (halaman umum batas laju; tanpa kredensial) menyatakan bahwa batas diterapkan per proyek, dapat mencakup permintaan per menit, token per menit, dan permintaan per hari, dan tidak memuat angka batas untuk model ini.

**Penyebab: tidak terkonfirmasi.** Tiga hipotesis konsisten dengan data, tanpa satu pun yang terbukti: (1) batas 15 permintaan per menit jam tetap, yang cocok persis dengan pola 15 keberhasilan diikuti kegagalan; (2) batas 16 per menit bergulir, yang juga cocok; (3) kuota harian atau sebab lain, yang tidak dapat dikecualikan. Batas bergulir sebesar 15 kurang cocok karena panggilan ke-16 dalam 53 detik berhasil. Token tidak mungkin menjadi pembatas: sekitar 9 ribu token digunakan dalam menit itu, jauh di bawah 250.000.

**Implikasi kapasitas.** Pada tier Free, kuota harian 500 permintaan kurang dari seperlima dari 2.496 panggilan main run. Selain itu, run yang terhenti oleh kegagalan transport tidak dapat dilanjutkan (bab 3.5, bab 4). Dengan tidak tersedianya anggaran API, jalur Gemini ditutup secara praktis, terlepas dari penyebab pasti 429.

## 7. Keputusan menghentikan eksperimen pilot

Menurut spesifikasi §13.6, hasil FAIL-S pada ronde 1 membuka tepat dua cabang: satu perubahan dari daftar putih (untuk SF1: `timeout`, jeda antarpanggilan, atau jumlah percobaan ulang) yang dicatat sebagai versi FZ baru dan dilanjutkan dengan ronde 2, atau STOP. Mengulang dengan FZ yang sama bukan cabang resmi. Spesifikasi juga menyatakan bahwa setelah panggilan pilot pertama tidak ada pengembalian ke langkah pembekuan awal, dan bahwa perilaku model tidak boleh menjadi pemicu pengembalian.

Owner memilih STOP (entri 12.61). Alasannya: kendala kapasitas di atas membuat main run tidak dapat dilayani pada tier gratis, anggaran API tidak tersedia, dan baik penyebab 429 maupun kapasitas proyek tidak terverifikasi. Perubahan delay, meskipun termasuk daftar putih, akan membuat versi FZ baru dan menuntut pembekuan ulang Step 7, rebuild Step 8, dan penggantian waiver serta indeks FZ; pilihan itu dinilai tidak sebanding sebelum kapasitas terbukti memadai untuk main run. Keputusan tersebut menghentikan **eksperimen pilot saat ini**. Ia bukan pernyataan bahwa penelitian gagal atau selesai. Ronde 2 tidak dijalankan, tidak ada versi FZ baru, dan tidak ada record keputusan pilot. Opsi lain yang ditinjau, seperti menjalankan ronde 2 dengan FZ-v1 sebagai penyimpangan tercatat, diuraikan dalam dokumen kerja `DRAFT_ROUND1_DISPOSITION_AND_429_REVIEW_2026-10-15.md` beserta biayanya.

Satu catatan prosedural: skrip keputusan pilot tidak dapat menulis record untuk STOP setelah ronde 1 (FAIL-S pada ronde 1 memunculkan penolakan "tidak final" dan tidak menulis apa pun). Entri owner 12.61 karenanya merupakan satu-satunya catatan aksi ronde 1.

## 8. Evaluasi kelayakan model lokal (eksploratori)

### 8.1 Tujuan dan batas

Setelah pilot Gemini dihentikan, owner meninjau kemungkinan memakai model lokal tanpa biaya API. Sebagai langkah pertama, dilakukan evaluasi kelayakan sintetis eksploratori atas `llama3.2:3b` melalui Ollama untuk menjawab pertanyaan sempit: dapatkah model itu menjalankan format respons beku tiga bidang dengan andal dan dengan kecepatan yang wajar? **Ini bukan pilot resmi**, bukan data eksperimen, tidak memakai prompt registry atau pilot, dan tidak menguji hipotesis. Hasilnya tidak mengubah keputusan STOP 12.61 (entri 12.62).

### 8.2 Metode dan kriteria yang ditetapkan sebelum run

Kriteria dikunci di kode sebelum run: lanjut bila porsi UNP ≤ 10 %; keputusan owner bila ≤ 25 %; berhenti bila di atasnya; kegagalan struktural SF1 sampai SF5 paling banyak 1 dari 80 dan tanpa pemotongan; dan proyeksi 2.496 panggilan tidak melebihi 24 jam. Populasi adalah 80 panggilan sintetis: 64 panggilan (16 template × kondisi A sampai D) dari generator dan perender beku pada basis yang tidak beririsan dengan registry utama maupun pilot, ditambah 16 pengulangan; dua panggilan probe di luar hitungan memeriksa nilai `done_reason` saat keluaran dipotong dan saat normal. Format respons beku dipakai apa adanya (bukan JSON). Opsi yang dikirim: `num_ctx` 16.384, `num_predict` 8.192, `keep_alive` 30 menit, tanpa streaming; `temperature`, `seed`, `top_k`, dan `top_p` tidak dikirim sehingga memakai bawaan Ollama. Run tunggal dilakukan pada 2026-10-16 di mesin owner terhadap server Ollama lokal pada 127.0.0.1 (versi 0.6.7; digest model `a80c4f17acd55265feec403c7aef86be0c25983ab279d83f3bcd3abbcb5b8b72`; 3,2 miliar parameter; kuantisasi Q4_K_M). Harness diuji lebih dulu dengan server tiruan (19 tes), tanpa soket.

### 8.3 Hasil

| Butir | Hasil |
|---|---|
| Status terhadap kriteria | FEASIBILITY_PROCEED (komponen UNP, struktural, dan waktu semuanya lanjut) |
| SF1 sampai SF5 / UNP | semua SF 0; UNP 2 dari 80 (2,5 %) |
| Latensi | rata-rata 1.506,8 ms; median 1.328; maksimum 4.328 (panggilan pertama 1.609); sekitar 70 token keluaran per detik |
| Proyeksi 2.496 panggilan | sekitar 1,04 jam (hanya berlaku untuk mesin ini) |
| Penggunaan token | prompt 225 sampai 277 token; keluaran 46 sampai 295 token; `prompt_eval_count` dan `eval_count` ada pada 80 dari 80 panggilan |
| Stabilitas pengulangan | teks identik pada 0 dari 16 pasangan; hasil klasifikasi identik pada 13 dari 16 |
| Probe | `done_reason` "length" saat dipotong; "stop" pada keluaran normal |
| **Informasional, bukan kriteria** | 36 dari 78 respons yang dapat diparse bersesuaian dengan ekspektasi sintetis (sekitar 46 %) |

### 8.4 Interpretasi dan batasnya

Yang dapat dinyatakan: pada data sintetis, model patuh pada format beku (UNP 2,5 %), tidak ada kegagalan struktural, kecepatan memadai untuk menjalankan 2.496 panggilan dalam kisaran satu jam di mesin yang sama, dan decoding bawaan Ollama bersifat acak (tidak satu pun pasangan pengulangan menghasilkan teks identik), sehingga pengulangan benar-benar merupakan tarikan yang berbeda. Pemetaan field Ollama kini didukung pengamatan untuk versi 0.6.7: nilai `done_reason` "length" teramati saat pemotongan, padahal dokumentasi yang dibaca hanya menyebut "stop" dan "unload".

Yang tidak dapat dinyatakan: bahwa model ini mampu atau tidak mampu pada tugas penelitian; bahwa ia setara dengan Gemini; atau bahwa hasil pada prompt sintetis berlaku untuk prompt registry. Angka sekitar 46 % hanyalah indikasi informasional dari satu run dengan n = 80 tanpa selang kepercayaan. Ia mendekati tingkat kebetulan untuk tugas dua kelas dan menandai risiko efek lantai (TH10) bila model ini dipakai kelak, tetapi bukan temuan. Bila hasil evaluasi ini kelak dipakai untuk memilih model, pilihan itu terinformasi pilot dan harus diungkapkan dengan lineage lengkap (pilot Gemini FAIL-S dan evaluasi ini). Satu mesin, satu run, dan satu versi Ollama membatasi generalisasi.

## 9. Keterbatasan dan ancaman validitas

### 9.1 Ancaman dari spesifikasi §20 yang tetap berlaku

| ID | Ancaman (ringkas, mengikuti teks spesifikasi) | Relevansi untuk laporan ini |
|---|---|---|
| TH1 sampai TH3 | Tidak ada pekan tepat sasaran pada rencana `PAC`; beberapa nilai "target pace" per rencana; pace yang tertampil berbeda dari referensi tersembunyi G | Konstruk operasional; berlaku bila desain dipakai lagi |
| TH4 sampai TH6 | Aliasing kelas dengan basis × posisi × arah; klasterisasi basis dan jumlah klaster efektif yang mungkin jauh lebih kecil daripada L; posisi × besaran basis × bentuk rencana | Berlaku untuk analisis yang tidak dilakukan; dicatat sebagai keterbatasan desain |
| TH7 sampai TH8 | Target selalu menjadi deviasi terbesar rencana (isyarat struktural konstan); kesulitan aritmetika berbeda antar keluarga tanpa perbandingan lintas keluarga | Desain |
| TH9 | Klaim reviewer satu sisi: efek klaim tidak dapat dipisahkan dari "pernyataan pelanggaran" umum | Membatasi tafsir bila main run dijalankan kelak |
| TH10 | Efek lantai atau langit-langit membuat margin dan kontras klaim tidak informatif | Terkait indikasi informasional model lokal yang mendekati kebetulan (bukan temuan) |
| TH11 | Satu model dan satu pengaturan penyedia; drift penyedia dan nondeterminisme decoding bawaan tidak dikendalikan | Relevan: Gemini dan model lokal adalah subjek berbeda; decoding bawaan lokal teramati acak |
| TH12 dan TH13 | Presisi terbatas oleh jumlah basis; multiplisitas atas 12 sel primer dan kontras | Tidak berlaku sebagai hasil: tidak ada analisis |
| TH14 | Paparan peneliti terhadap keluaran Stage 1 dan 2 tidak dapat dibatalkan | Berlaku |
| TH15 | Familiaritas dengan nilai aturan terkenal | Hanya jika nilai terkenal dipilih |
| TH16 | Penyebut S2 dan S3 bergantung kondisi karena UNP dikecualikan | Tidak berlaku: tidak ada pengodean S2 atau S3 |
| TH17 | Grid basis kasar, panjang rencana terbatas, pilot kecil (18 panggilan, satu repetisi) yang hanya mendeteksi kegagalan struktural yang sering | Berlaku langsung pada pilot ini |
| TH18 | Daftar frasa rujukan reviewer meremehkan rujukan biasa; hitungan adalah batas bawah | Tidak berlaku: tidak ada pengodean |

Ancaman lain dari spesifikasi yang relevan mencakup validitas pengukuran (parser dapat salah klasifikasi; independensi kebenaran dasar parsial karena spesifikasi dan semantik aturan dipakai bersama dan A dan B ditulis oleh orang yang sama; pemeriksaan dan pengodean satu peneliti lebih lemah daripada dua orang; pengodean S2 tidak buta terhadap kebenaran dasar), reproduksibilitas (drift model penyedia dan nondeterminisme decoding bawaan; hash memitigasi drift skenario tetapi tidak drift penyedia; urutan eksekusi bergantung versi interpreter), dan derajat kebebasan peneliti (parameter pada §17 adalah eksposur utama).

### 9.2 Keterbatasan khusus laporan ini

1. **Hasil utama pada 1.248 prompt tidak ada.** Tidak ada estimasi kinerja, kontras antar kondisi, atau inferensi.
2. **Pilot tidak lulus.** FAIL-S oleh dua panggilan 429 yang penyebabnya tidak terkonfirmasi; pilot berakhir tanpa PASS dan tanpa ronde 2.
3. **Tidak ada cek buta manusia** (H1 tidak dilakukan, 12.56). Independensi A, B, generator, dan skrip hanya pada jalur kode.
4. **Satu pengode, tanpa kappa** (OD-3, K1). Rehearsal terpapar label AI dan tanpa prompt, sehingga `s2_values` dan `s2_arith` tidak dapat dinilai penuh dari teks komentar; B10 dan B36 tidak terklasifikasi karena dasar pelabelan tidak dapat dipulihkan.
5. **Asumsi token tidak diukur** (O4 INCONCLUSIVE).
6. **Tanpa advisor.** Seluruh keputusan tata kelola dibuat oleh satu orang.
7. **Pembekuan tanpa pra-registrasi eksternal.** Hash dan decision record append-only adalah mitigasi, bukan pengganti; kesesuaiannya dengan kebijakan institusi belum dikonfirmasi.
8. **Kendala infrastruktur.** Kuota penyedia pada tier gratis menutup main run, dan angka kuota berasal dari pengamatan owner tanpa artefak independen.
9. **Provenansi hasil tertentu.** Keluaran analisis nonresmi 16 panggilan tidak tersimpan sebagai berkas (Lampiran D).
10. **Lingkungan pengujian terbatas.** Tes perangkat lunak dijalankan pada satu mesin; spesifikasi mesin lain (memori, akselerator) tidak tercatat.

## 10. Kontribusi dan pekerjaan lanjutan

**Kontribusi** yang dapat dipertanggungjawabkan bersifat rekayasa dan metodologis, bukan klaim empiris tentang model. Pertama, sebuah protokol dan generator skenario dengan kebenaran dasar deterministik, gerbang validasi bertingkat, dan verifikasi oleh dua implementasi. Kedua, prosedur pembekuan dan audit yang dapat direproduksi: hash register, indeks FZ yang diverifikasi independen di gate, ledger berantai, dan decision record append-only. Ketiga, pelajaran praktis: kuota laju dan kuota harian penyedia perlu diperiksa sebelum pilot; pacing satu detik tidak aman terhadap batas 15 permintaan per menit; isi body error penyedia sebaiknya disimpan; dan resume yang gagal-tertutup membuat run panjang rentan terhadap gangguan. Keempat, bukti eksploratori bahwa format respons beku dapat dipatuhi oleh model lokal kecil pada data sintetis.

**Pekerjaan lanjutan yang mungkin** semuanya memerlukan keputusan owner baru dan tidak diotorisasi di sini: tier berbayar dengan ronde 2 setelah perubahan daftar putih pada jeda antarpanggilan (versi FZ baru, otorisasi R-7 untuk pembekuan ulang Step 7); versi metodologi pengganti dengan model lokal (versi FZ baru, adapter, pilot baru, pengungkapan lineage); atau evaluasi model lokal yang lebih besar dengan harness dan kriteria yang sama. Pilihan mana pun harus memperlakukan bab ini sebagai bagian dari lineage terinformasi pilot.

## 11. Kesimpulan

Rancangan dan instrumen penelitian telah dibangun dan diuji secara perangkat lunak. Pilot ronde 1 pada Gemini berstatus FAIL-S karena dua penolakan batas laju yang penyebabnya tidak terkonfirmasi; O4 tidak dapat disimpulkan; eksperimen pilot dihentikan oleh keputusan owner; dan evaluasi kelayakan sintetis pada model lokal hanya menunjukkan bahwa format dapat dipatuhi dan kecepatan memadai, tanpa menunjukkan kemampuan pada tugas penelitian. **Hasil utama pada 1.248 prompt tidak tersedia**, sehingga penelitian ini belum menjawab pertanyaan primernya dan tidak memberikan kesimpulan tentang akurasi model, pengaruh kondisi atau klaim reviewer, atau kesetaraan antar model. Status akhir: **BLOCKED / INCONCLUSIVE untuk eksperimen utama.** Apakah laporan seperti ini memenuhi syarat akademik program, dan dalam format apa ia diterima, memerlukan konfirmasi institusi dan tidak dapat saya tentukan.

---

## Lampiran A. Rujukan keputusan (decision record)

12.38 (PG3), 12.39 (rehearsal, pembacaan "used"), 12.43 sampai 12.45 (resume, kelas error), 12.46 sampai 12.49 (PRD-5, D4, D6, MD-07, MD-03, K2), 12.50 (owner sebagai pengambil keputusan tunggal; MD-06; B-1; E-1; P11 dan P12), 12.51 (K1, R-7 tidak diotorisasi), 12.52 (MD-10), 12.53 (H4 opsi (i)), 12.54 (aturan ronde lanjutan), 12.55 (P5 dan E-1), 12.56 dan 12.57 (waiver H1 dan gate), 12.58 (konfirmasi manifest, catatan SW), 12.59 (H5 ronde 1), 12.60 (hash FZ resmi), 12.61 (N3), 12.62 (kelayakan lokal).

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
| Decision record saat v4 ditulis (setelah entri 12.62) | `e4be4cb3abe66e4f74eb87c53c5d1f3e0c9b884fae5ea3637d634fa9844c3b4c` |

## Lampiran C. Hal yang memerlukan konfirmasi manusia atau institusi

Hal-hal berikut tidak dapat diverifikasi dari repositori dan tidak diisi dengan asumsi:

1. **Format dan panjang** bab, ringkasan, dan kalimat penutup sesuai ketentuan tesis atau institusi: perlu konfirmasi institusi.
2. **Kebijakan pra-registrasi institusi**: belum diverifikasi; perlu konfirmasi institusi apakah mitigasi hash dan decision record append-only memadai.
3. **Kelayakan akademik** laporan tanpa hasil utama bagi syarat program S2: perlu konfirmasi institusi. Tidak ada advisor yang dapat menilainya, dan ini bukan penilaian teknis.
4. **Bukti kuota konsol**: hanya pengamatan owner yang ada; tidak ada artefak independen di repositori. Bila institusi atau penelaah menghendaki bukti, owner perlu menyediakannya (misalnya tangkapan atau ekspor konsol bertanggal).
5. **Pencantuman catatan nonresmi** (Lampiran D) dalam versi final: keputusan owner.
6. **Spesifikasi mesin** selain yang tercantum di bab 3.6 (nama dagang prosesor, memori, akselerator) tidak tercatat; bila diwajibkan, owner perlu menyediakannya.

## Lampiran D. Catatan nonresmi: analisis deskriptif atas 16 panggilan (provenansi dan keterbatasan)

- **Apa ini:** analisis deskriptif struktural atas 16 panggilan pilot berstatus HTTP 200 dengan usage lengkap, dijalankan owner dengan `research_design/step10/pilot_supplement_16.py` (sha256 `3e9e3aadf370ebc5a71ebc0c187a5acb049bf6431641fc7f89d4b32f6fa6110c`; berkas uji `test_pilot_supplement_16.py`, sha256 `79355d8768067a967763186bce493d728f002bab373b557823fea9b08d6d45de`).
- **Provenansi:** keluarannya dicetak ke terminal dan ditempel owner ke percakapan kerja; **tidak tersimpan sebagai berkas**. Angka yang dipakai di sini hanya yang ada pada salinan tempel itu: UNP 3 dari 16; seluruh `finish_reason` STOP; latensi 938 sampai 5.094 ms (rata-rata 2.418,9); `promptTokenCount` 216 sampai 274. Tidak ada angka lain yang direkonstruksi. Skrip bersifat read-only dan dapat dijalankan ulang terhadap folder pilot yang sama; jalan ulang untuk verifikasi belum dilakukan.
- **Status:** bukan hasil pilot dan bukan "pilot yang lulus"; tidak menggantikan laporan resmi (FAIL-S) atau O4 (INCONCLUSIVE). Mengecualikan dua panggilan 429 mengubah populasi analisis; tanpa kedua panggilan itu SF1 tampak 0, yang menyesatkan bila dikutip tanpa konteks.
- **Penggunaan wajar:** hanya sebagai konteks untuk perencanaan pacing dan biaya.

## Lampiran E. Riwayat versi dan ringkasan audit

| Versi | Berkas | sha256 |
|---|---|---|
| v1 | `BAB_LAPORAN_PILOT_TIDAK_LULUS_DRAFT_2026-10-16.md` | `ce382532e13b728a8ac4b63b34120b5d846386381af1f6db1c96ae001a44ecac` |
| v2 | `BAB_LAPORAN_PILOT_TIDAK_LULUS_DRAFT_v2_2026-10-16.md` | `da0afa2e575ad46909876f8248799d9e2f58f5eca9a30b51d8dbf7aecf8bc85b` |
| v3 | `BAB_LAPORAN_PILOT_TIDAK_LULUS_KANDIDAT_v3_2026-10-16.md` | `a398db7daf7d8a0b8b430af32677cad379f16e34c7459a6d3408f4d6dfc60166` |

**Perubahan v3 ke v4:** (1) gaya diubah ke laporan teknis akademik dengan bab rancangan (2), instrumen (3), tata kelola (4), pilot (5), insiden 429 (6), keputusan (7), evaluasi lokal (8), keterbatasan (9), kontribusi (10), dan kesimpulan (11); (2) konten rancangan ditambahkan dari spesifikasi v2.7 dan register FZ-v1 (semantik aturan, kondisi, margin, registry, estimand) dan diverifikasi terhadap teks; (3) penanda kerja [OWNER] dan [PERIKSA] diganti pernyataan keterbatasan atau catatan konfirmasi (Lampiran C); (4) lingkungan pengujian dicantumkan hanya dari sumber yang dapat diverifikasi (versi Python, string platform, prosesor, Ollama 0.6.7); (5) angka kuota dinyatakan berasal dari pengamatan owner; (6) Lampiran D tetap sebagai catatan nonresmi; (7) kalimat tentang bahwa desain bersifat deskriptif tanpa uji hipotesis ditambahkan (DP2). Status resmi dipertahankan: Gemini FAIL-S, O4 INCONCLUSIVE, eksperimen utama BLOCKED / INCONCLUSIVE, STOP 12.61.
