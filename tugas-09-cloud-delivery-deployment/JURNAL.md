# Jurnal Proses — Tugas 9

## Diskusi deployment model
- Opsi yang dipertimbangkan dan kenapa akhirnya memilih salah satu:
  - Awalnya kelompok mempertimbangkan **Private Cloud murni** karena data kependudukan (NIK dan biometrik) bersifat sangat rahasia dan diatur UU PDP sehingga wajib berada di bawah kendali penuh negara. Namun, setelah mengevaluasi karakteristik NIST *rapid elasticity*, Private Cloud murni dinilai tidak efisien karena memaksa negara membeli perangkat keras berlebih (*over-provisioning*) hanya untuk menghadapi lonjakan trafik musiman seperti Pemilu dan PPDB.
  - Kami juga sempat melihat **Community Cloud** (khusus antar-instansi pemerintah), tetapi model ini tetap kurang fleksibel untuk akses ribuan pihak non-pemerintah seperti perbankan dan *fintech* (verifikasi KYC) yang membutuhkan skalabilitas instan.
  - Akhirnya kami sepakat memilih **Hybrid Cloud**: menyimpan dan memproses data inti (NIK & biometrik) di *Private Cloud* milik negara, sementara lapisan akses (API Gateway KYC dan portal cek status) diletakkan di *Public Cloud* agar elastis menghadapi lonjakan trafik tanpa mengorbankan kedaulatan data.

## Diskusi service model per komponen
- Kami memisahkan komponen sistem berdasarkan tingkat sensitivitas data dan kebutuhan kontrol:
  - **Database Inti & Biometric Vault -> IaaS (di Private Cloud):** Dipilih IaaS agar pemerintah memiliki kendali penuh dari level OS, jaringan terisolasi, hingga pengelolaan kunci enkripsi mandiri (HSM) sesuai UU PDP.
  - **API Gateway KYC & Portal Cek Status -> PaaS (di Public Cloud):** Dipilih PaaS agar tim pengembang cukup fokus pada logika aplikasi, autentikasi, dan *auto-scaling* saat beban puncak tanpa direpotkan perawatan server fisik maupun *patching* OS.
  - **Monitoring Operasional & Helpdesk Ticketing -> SaaS (di Public Cloud):** Dipilih SaaS untuk mempercepat dukungan teknis bagi ribuan instansi daerah/bank, dengan syarat ketat hanya memproses metadata sistem dan tiket gangguan (bukan data pribadi/NIK).

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 2026-11-22 | Gemini | Meminta kerangka analisis pemetaan 5 karakteristik NIST SP 800-145 untuk studi kasus Sistem Data Kependudukan, ide pemetaan IaaS/PaaS/SaaS, risiko spesifik, dan ide skenario tandingan. | Menyarankan Hybrid Cloud dengan pemisahan Private Cloud (IaaS untuk DB inti/biometrik) dan Public Cloud (PaaS untuk API Gateway/portal, SaaS untuk helpdesk); memberikan ide mitigasi *data minimization* (respons Boolean KYC), risiko *insider threat/scraping*, serta skenario daerah 3T dan DDoS saat Pemilu. | Kerangka dan poin ide dari AI dijadikan bahan diskusi kelompok, lalu disusun ulang narasinya dengan penekanan konteks regulasi UU PDP No. 27 Tahun 2022, perbandingan tabel terhadap Public Cloud murni, serta ditambahkan diagram arsitektur pendukung di folder `bukti/`. |