# Tugas 9 (Pekan 9) — Cloud Delivery & Deployment Model

**Materi terkait:** Karakteristik esensial cloud computing (NIST SP 800-145), Deployment Model (Public/Private/Hybrid/Community), Service Model (IaaS/PaaS/SaaS).

> Bagian 2 mata kuliah ini murni **analisis & desain di atas kertas** — tidak ada biaya cloud sama sekali, karena tugas berhenti di tahap rekomendasi, bukan implementasi nyata (implementasi baru mulai Tugas 11).

## Studi Kasus

Pemerintah ingin membangun **Sistem Data Kependudukan** (nama, NIK, alamat, data biometrik) yang:
- Sangat **rahasia** (data pribadi warga negara, diatur UU Perlindungan Data Pribadi).
- Diakses oleh **ribuan instansi** (dukcapil daerah, kepolisian, bank untuk verifikasi KYC) dengan pola akses yang **tidak rata** (lonjakan saat musim pemilu/pendaftaran sekolah).
- Butuh **skalabilitas** agar tidak downtime saat lonjakan akses, tapi **tidak boleh** datanya berada di infrastruktur yang tidak terkendali penuh oleh negara.

## Tugas Kelompok

1. **Rekomendasikan Deployment Model** (Public / Private / Hybrid / Community Cloud) yang paling tepat untuk sistem ini. Jelaskan alasannya berdasarkan **karakteristik NIST** (on-demand self-service, broad network access, resource pooling, rapid elasticity, measured service) dikaitkan dengan kebutuhan kerahasiaan vs skalabilitas.
2. **Rekomendasikan Service Model** (IaaS / PaaS / SaaS) yang tepat untuk komponen-komponen berbeda dari sistem ini (boleh berbeda service model untuk komponen berbeda, mis. database inti vs portal publik untuk pengecekan status).
3. Jelaskan **minimal 2 risiko spesifik** dari pilihan kalian dan mitigasinya (mis. jika Hybrid Cloud dipilih: risiko sinkronisasi data antara private & public segment).
4. Bandingkan singkat dengan **satu alternatif yang kalian tolak** — kenapa alternatif itu kurang tepat (mis. kenapa Public Cloud murni ditolak, atau kenapa Private Cloud murni dianggap kurang skalabel).

## 1. Rekomendasi Deployment Model: Hybrid Cloud

Deployment model yang paling tepat untuk Sistem Data Kependudukan Nasional adalah **Hybrid Cloud**, yaitu kombinasi antara **Private Cloud** (dikelola penuh oleh negara melalui Pusat Data Nasional / PDN) untuk menyimpan dan memproses data inti, serta **Public Cloud** untuk menangani lapisan akses publik, gerbang API, dan lonjakan trafik musiman.

Pilihan ini menyeimbangkan dua kebutuhan yang saling bertolak belakang—**kedaulatan/kerahasiaan data** (sesuai UU No. 27 Tahun 2022 tentang Pelindungan Data Pribadi / UU PDP) dan **skalabilitas elastis**—yang dapat dijelaskan melalui 5 karakteristik esensial **NIST SP 800-145**:

1. **On-Demand Self-Service**
   Menjelang momentum lonjakan akses seperti Pemilu atau Penerimaan Peserta Didik Baru (PPDB), tim teknis pemerintah dapat langsung melakukan *provisioning* kapasitas komputasi tambahan pada segmen *Public Cloud* (lapisan portal dan API Gateway) secara mandiri dalam hitungan menit tanpa harus menunggu proses pengadaan server fisik baru yang memakan waktu berbulan-bulan.
2. **Broad Network Access**
   Sistem harus diakses oleh ribuan instansi lintas sektor (514 Dukcapil kabupaten/kota, kepolisian, KPU, sekolah, hingga perbankan untuk verifikasi KYC) dari seluruh Indonesia. Segmen *Public Cloud* menyediakan akses terstandar berbasis web dan REST API dengan latensi rendah di berbagai wilayah, sementara jalur ke *Private Cloud* tetap terkunci lewat koneksi privat terenkripsi.
3. **Resource Pooling**
   Karakteristik ini diterapkan secara terpisah sesuai tingkat sensitivitas data. Pada segmen **Private Cloud**, *resource pooling* bersifat *dedicated* khusus antar-instansi pemerintah saja, sehingga data NIK dan biometrik warga negara tidak pernah berbagi perangkat keras fisik dengan pihak eksternal (*multi-tenant* publik). Sementara di segmen **Public Cloud**, *resource pooling* dimanfaatkan hanya untuk memproses permintaan antarmuka (*stateless*) yang tidak menyimpan data pribadi.
4. **Rapid Elasticity**
   Pola akses data kependudukan sangat tidak merata: normal di hari biasa, tetapi melonjak puluhan kali lipat saat pencocokan daftar pemilih (Pemilu) atau validasi NIK serentak (PPDB). Segmen *Public Cloud* memungkinkan *auto-scaling* secara instan untuk menyerap lonjakan trafik agar layanan tidak *downtime*, lalu menyusut kembali (*scale-in*) saat beban normal sehingga anggaran negara tetap efisien.
5. **Measured Service**
   Setiap permintaan verifikasi KYC yang masuk dari perbankan, *fintech*, atau instansi lain melalui API Gateway diukur dan dicatat secara otomatis (*metering*). Data pengukuran ini penting untuk transparansi penagihan layanan (PNBP), pemantauan kuota akses (*quota management*), serta deteksi dini apabila ada instansi yang melakukan penarikan data tidak wajar.

---

## 2. Rekomendasi Service Model per Komponen

Karena setiap komponen dalam Sistem Data Kependudukan memiliki tingkat sensitivitas dan kebutuhan kendali yang berbeda, arsitektur ini menerapkan kombinasi **IaaS, PaaS, dan SaaS**:

| Komponen Sistem | Service Model | Deployment Segment | Alasan Pemilihan |
| :--- | :--- | :--- | :--- |
| **Database Inti Kependudukan (NIK, Nama, Alamat, KK)** | **IaaS** | Private Cloud (PDN) | Negara memerlukan kendali penuh hingga level sistem operasi, konfigurasi jaringan terisolasi, kebijakan enkripsi *at-rest* (AES-256), dan penempatan fisik server demi kepatuhan UU PDP. |
| **Biometric Vault & Core Verification Engine** | **IaaS** | Private Cloud (PDN) | Data biometrik (sidik jari, iris, wajah) termasuk data pribadi spesifik yang tidak bisa diubah jika bocor. IaaS memungkinkan integrasi langsung dengan *Hardware Security Module* (HSM) yang kunci enkripsinya dipegang penuh oleh negara. |
| **API Gateway (KYC) & Portal Layanan Publik** | **PaaS** | Public Cloud | Fokus utama komponen ini adalah ketersediaan tinggi dan *auto-scaling* saat lonjakan trafik Pemilu/PPDB. Dengan PaaS, tim pengembang pemerintah cukup fokus pada kode aplikasi, autentikasi API, dan *rate limiting* tanpa terbebani pengelolaan *patching* OS atau *runtime* server. |
| **Monitoring Operasional & Helpdesk Ticketing** | **SaaS** | Public Cloud | Memudahkan pengelolaan laporan kendala teknis dari ribuan operator Dukcapil daerah dan bank secara cepat. Aman menggunakan SaaS karena data yang diproses murni metadata sistem dan tiket gangguan (*Zero PII*), tanpa pernah menyentuh data NIK atau biometrik. |

---

## 3. Analisis Risiko Spesifik & Mitigasi

### Risiko 1: Kebocoran Data saat Transit atau Tersimpan di *Cache* Segmen Public Cloud
* **Konteks Masalah:** Dalam arsitektur Hybrid Cloud, permintaan verifikasi KYC dari bank masuk melalui API Gateway di *Public Cloud* sebelum diteruskan ke *Private Cloud*. Jika konfigurasi tidak ketat, data NIK atau respons profil lengkap warga berisiko disadap saat transit atau tidak sengaja tersimpan di *cache*/*log* milik vendor *Public Cloud*, yang melanggar kedaulatan data dan UU PDP.
* **Mitigasi:**
  * Membangun jalur komunikasi tertutup antara *Public Cloud* dan *Private Cloud* menggunakan **Dedicated Private Link / VPN IPSec** dengan enkripsi **mTLS (TLS 1.3)**.
  * Menerapkan prinsip **Data Minimization** pada API KYC: *Core Verification Engine* di *Private Cloud* hanya mengirimkan respons **Boolean (`Match` / `No Match`)** atau skor kecocokan ke *Public Cloud*, bukan data mentah (foto biometrik/alamat lengkap).
  * Menonaktifkan penyimpanan *payload* pada *cache* dan *log* di segmen *Public Cloud* (*stateless processing*).

### Risiko 2: Penyalahgunaan Akses & *Data Scraping* Massal oleh Kredensial Instansi Eksternal
* **Konteks Masalah:** Sistem diakses oleh ribuan instansi (bank, kepolisian, Dukcapil daerah). Risiko terbesar bukan hanya peretasan dari luar, melainkan kebocoran API Key atau penyalahgunaan akun operator (*insider threat*) di salah satu instansi yang kemudian dipakai untuk menyedot jutaan data NIK secara ilegal.
* **Mitigasi:**
  * Menerapkan arsitektur **Zero Trust**, **Role-Based Access Control (RBAC)**, dan **IP Whitelisting** per instansi sehingga kredensial yang bocor tidak bisa dipakai dari jaringan luar.
  * Menerapkan **Rate Limiting** adaptif dan kuota harian pada API Gateway sesuai profil kebutuhan masing-masing instansi.
  * Menyimpan **Immutable Audit Log** di *Private Cloud* yang mencatat secara permanen siapa mengakses NIK siapa, dari instansi mana, dan untuk keperluan apa, lengkap dengan sistem deteksi anomali (*SIEM*) yang otomatis memblokir akses jika terdeteksi pola *scraping*.

---

## 4. Perbandingan dengan Alternatif yang Ditolak: Public Cloud Murni

Alternatif utama yang kami tolak adalah **Public Cloud Murni** (menempatkan seluruh sistem termasuk database NIK dan biometrik di infrastruktur penyedia cloud komersial).

| Aspek Penilaian | Hybrid Cloud (Dipilih) | Public Cloud Murni (Ditolak) |
| :--- | :--- | :--- |
| **Kedaulatan & Kendali Data** | Data NIK & biometrik 100% berada di infrastruktur fisik milik negara (*Private Cloud*). | Data inti berada di infrastruktur pihak ketiga; bergantung pada kebijakan dan yurisdiksi vendor. |
| **Kepatuhan UU PDP** | Sangat tinggi; negara memegang kendali penuh atas enkripsi (HSM) dan isolasi data sensitif. | Berisiko tinggi terhadap pelanggaran prinsip kendali penuh negara atas data strategis kependudukan. |
| **Skalabilitas saat Lonjakan** | Sangat baik; lapisan akses di *Public Cloud* menyerap lonjakan Pemilu/PPDB secara elastis. | Sangat baik, tetapi harus mengorbankan kendali penuh atas data inti. |
| **Efisiensi Risiko (*Blast Radius*)** | Jika segmen publik diretas, database inti tetap terisolasi di *Private Cloud*. | Satu celah konfigurasi di lingkungan publik dapat langsung mengekspos seluruh data inti warga. |

**Kesimpulan Penolakan:** Meskipun *Public Cloud* murni unggul dalam kemudahan operasional dan elastisitas, menyerahkan penyimpanan data biometrik seluruh warga negara ke infrastruktur yang tidak dikendalikan penuh oleh negara melanggar syarat utama studi kasus dan terlalu berisiko bagi keamanan nasional. *(Catatan: **Private Cloud Murni** juga tidak dipilih karena memaksa negara melakukan over-provisioning server fisik secara masif hanya untuk menampung lonjakan musiman Pemilu/PPDB, sehingga sangat boros anggaran saat trafik normal).*

---

## 5. Skenario Tandingan (*Counter-Scenario*)

### Skenario 1: Bagaimana jika Dukcapil di daerah 3T tidak memiliki infrastruktur Private Cloud sendiri dan koneksi internetnya tidak stabil?
* **Analisis & Jawaban:** Dalam arsitektur Hybrid Cloud ini, Dukcapil daerah **tidak diwajibkan** membangun infrastruktur *Private Cloud* sendiri—seluruh *Private Cloud* terpusat di Pusat Data Nasional (PDN) dengan replikasi lintas wilayah (*Disaster Recovery Center*). Untuk mengatasi koneksi internet yang tidak stabil di wilayah 3T, diterapkan mekanisme **lokal *edge buffering* terenkripsi** pada terminal Dukcapil daerah. Operator tetap dapat melayani perekaman atau antrean permohonan secara *offline* sementara, lalu sistem akan melakukan sinkronisasi otomatis secara bertahap (*batch synchronization*) melalui jalur VPN terenkripsi begitu koneksi kembali tersedia, tanpa menyimpan salinan permanen database nasional di perangkat daerah.

### Skenario 2: Bagaimana jika terjadi serangan DDoS masif pada portal layanan tepat saat hari pencoblosan Pemilu atau puncak pendaftaran PPDB?
* **Analisis & Jawaban:** Justru di sinilah keunggulan utama **Hybrid Cloud**. Karena seluruh trafik publik terlebih dahulu melewati lapisan **WAF, CDN, dan DDoS Mitigation** di *Public Cloud*, lonjakan trafik serangan akan diserap dan disaring di tepi jaringan (*edge*) menggunakan kapasitas elastis *Public Cloud*. Jalur *Private Link* menuju *Private Cloud* hanya meneruskan permintaan sah yang sudah lolos autentikasi dan *rate limiting*, sehingga database inti kependudukan tetap terisolasi, stabil, dan tidak ikut lumpuh.

## Struktur Submission

```
tugas-09-cloud-delivery-deployment/
├── README.md      # Analisis lengkap (isi dengan poin 1-4 di atas)
├── JURNAL.md
└── bukti/          # (opsional) diagram pendukung
```

## Rubrik Penilaian (Tugas 9)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Ketepatan rekomendasi deployment model | 30% | Argumen berbasis karakteristik NIST, bukan sekadar "private cloud lebih aman" tanpa detail |
| Ketepatan rekomendasi service model | 25% | Pemetaan komponen sistem ke IaaS/PaaS/SaaS masuk akal |
| Analisis risiko & mitigasi | 25% | Risiko spesifik ke konteks data kependudukan (bukan risiko generik) |
| Perbandingan dengan alternatif yang ditolak | 20% | Argumen penolakan jelas dan berdasar |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya ke AI gambaran umum karakteristik NIST/deployment model untuk brainstorming; **tidak boleh** meminta AI menuliskan rekomendasi/analisis akhir yang tinggal ditempel ke `README.md`. Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- Jawaban yang terasa seperti "template" (bisa dipakai untuk sistem cloud apa saja tanpa menyebut spesifik kependudukan/data pribadi/regulasi) akan dinilai rendah pada komponen ketepatan rekomendasi.
- `README.md` wajib membahas minimal satu skenario tandingan yang kalian buat sendiri (mis. "bagaimana jika instansi daerah tidak punya infrastruktur private cloud sendiri?") beserta jawabannya.
