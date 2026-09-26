# Jurnal Proses — Tugas 2

## [21 September 2026]
- Opsi arsitektur yang dipertimbangkan: Service-Oriented Architecture (SOA) murni untuk seluruh modul, Publish-Subscribe murni (Event-driven) untuk seluruh modul, Kombinasi SOA dan Publish-Subscribe.
- Kenapa akhirnya pilih [SOA/Pub-Sub]: Kami memilih kombinasi SOA dan Publish-Subscribe, karena komunikasi sinkron (SOA/RPC) dipertahankan antara Service Pesanan dan Service Pembayaran dan juga karena transaksi finansial wajib divalidasi secara real-time sebelum prosesnya dilanjutkan. Sebaliknya, Publish-Subscribe dipilih untuk menghubungkan Service Pesanan dengan Service Katalog Resto dan Service Notifikasi Kurir melalui Message Broker. Hal tersebut bisa mengurai tight coupling dari sistem monolitik sebelumnya, sehingga saat tim Kurir melakukan deploy ulang, modul Pesanan tidak akan terblokir atau ikut down.
- Revisi diagram (versi 1 → versi 2, apa yang berubah dan kenapa): Kami mengubah dari diagram yang hanya blok menjadi alur kerja sekuensial. Tujuan pembaruan sendiri untuk memperjelas kapan sistem menggunakan pola Request-Respone secara sinkron dan kapan sistem beralih ke pola Event-Driven asinkron melalui Publish-Subscribe. Kami juga menambahkan "Kurir" dan "Resto" sebagai tujuan tujuan akhir dari sistem notifikasi, serta respon balik ke pelanggan.
- Alur End-to-End: Pelanggan Buat Pesanan → Bayar → Notifikasi Resto & Kurir

Skenario: Pelanggan memesan makanan di FoodGo, sistem memvalidasi pembayaran, lalu resto dan kurir mendapat notifikasi secara paralel tanpa membuat pelanggan menunggu proses tersebut selesai.

Tahap 1 — Permintaan Pesanan (Sinkron)

Pelanggan → Service Pesanan
Pelanggan mengirim HTTP request untuk membuat pesanan. Ini bersifat sinkron, request-response — pelanggan menunggu balasan langsung dari server sebelum melanjutkan interaksi di aplikasi.

Tahap 2 — Validasi & Charge Pembayaran (Sinkron)

Service Pesanan → Service Pembayaran
Service Pesanan memanggil Service Pembayaran melalui RPC untuk memvalidasi dan mengeksekusi charge kartu/e-wallet pelanggan. Komunikasi ini sinkron, request-response — Service Pesanan bersifat blocking, artinya dia berhenti dan menunggu hasil dari Service Pembayaran sebelum bisa melangkah ke proses berikutnya. Sifat blocking inilah yang menjadi akar masalah "Latency is Zero" di Tugas 1 apabila tidak dipasangi timeout.

Tahap 3 — Konfirmasi Pembayaran (Sinkron)

Service Pembayaran → Service Pesanan
Service Pembayaran mengirim balik response bahwa transaksi sukses. Ini bukan panggilan baru, melainkan bagian kembalian (response) dari RPC call di Tahap 2 — tetap tergolong sinkron, request-response.

Tahap 4 — Publish Event Pesanan Dibayar (Asinkron)

Service Pesanan → Message Broker
Setelah pembayaran dikonfirmasi sukses, Service Pesanan mem-publish event OrderPaid ke Message Broker. Ini asinkron, event-based (publish) — Service Pesanan tidak menunggu ada yang memproses event ini, dia langsung lanjut ke tahap berikutnya (Tahap 7) tanpa perlu tahu siapa saja yang akan menerima event tersebut.

Tahap 5 — Distribusi Event ke Subscriber (Asinkron, Paralel)

Message Broker → Service Notifikasi Kurir & Service Katalog Resto
Kedua service ini masing-masing subscribe terhadap event OrderPaid dan menerimanya secara independen dari broker. Ini asinkron, event-based (subscribe), mengikuti pola publish-subscribe (pub-sub) — kedua service ini tidak saling tahu keberadaan satu sama lain, mereka hanya sama-sama "mendengarkan" broker. Karena sifatnya paralel, proses di kedua service ini berjalan bersamaan, tidak berurutan satu-satu.

Tahap 6 — Notifikasi ke Pihak Eksternal (Hasil dari Tahap 5)
Service Notifikasi Kurir → Kurir: kurir ditugaskan untuk mengambil pesanan.
Service Katalog Resto → Resto: resto menerima notifikasi bahwa pesanan sudah masuk dan perlu disiapkan.

Kedua notifikasi ini adalah efek samping dari pemrosesan event di Tahap 5, dan berjalan tanpa ketergantungan satu sama lain.

Tahap 7 — Konfirmasi ke Pelanggan (Sinkron)

Service Pesanan → Pelanggan
Service Pesanan mengirim HTTP response konfirmasi bahwa pesanan berhasil dibuat. Ini adalah balasan dari HTTP request di Tahap 1, sehingga tetap sinkron, request-response. Poin pentingnya: pelanggan sudah menerima konfirmasi tanpa perlu menunggu kurir benar-benar ditugaskan atau resto benar-benar menerima notifikasi — kedua proses itu berjalan di belakang layar secara asinkron.


## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

