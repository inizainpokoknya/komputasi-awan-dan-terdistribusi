# Jurnal Proses — Tugas 2

## [21 September 2026]
- Opsi arsitektur yang dipertimbangkan: Service-Oriented Architecture (SOA) murni untuk seluruh modul, Publish-Subscribe murni (Event-driven) untuk seluruh modul, Kombinasi SOA dan Publish-Subscribe.
- Kenapa akhirnya pilih [SOA/Pub-Sub]: Kami memilih kombinasi SOA dan Publish-Subscribe, karena komunikasi sinkron (SOA/RPC) dipertahankan antara Service Pesanan dan Service Pembayaran dan juga karena transaksi finansial wajib divalidasi secara real-time sebelum prosesnya dilanjutkan. Sebaliknya, Publish-Subscribe dipilih untuk menghubungkan Service Pesanan dengan Service Katalog Resto dan Service Notifikasi Kurir melalui Message Broker. Hal tersebut bisa mengurai tight coupling dari sistem monolitik sebelumnya, sehingga saat tim Kurir melakukan deploy ulang, modul Pesanan tidak akan terblokir atau ikut down.
- Revisi diagram (versi 1 → versi 2, apa yang berubah dan kenapa): Kami mengubah dari diagram yang hanya blok menjadi alur kerja sekuensial. Tujuan pembaruan sendiri untuk memperjelas kapan sistem menggunakan pola Request-Respone secara sinkron dan kapan sistem beralih ke pola Event-Driven asinkron melalui Publish-Subscribe. Kami juga menambahkan "Kurir" dan "Resto" sebagai tujuan tujuan akhir dari sistem notifikasi, serta respon balik ke pelanggan.

**Alur End-to-End: Pelanggan Buat Pesanan → Bayar → Notifikasi Resto & Kurir**

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

**Analisis: Mengapa Event-Driven / Pub-Sub Mengatasi Masalah Kopling**
Kaitan dengan Masalah di Tugas 1

Di Tugas 1, akar masalah FoodGo bukan cuma soal timeout dan retry yang hilang, tapi juga soal arsitektur monolitik yang membuat semua modul (pesanan, pembayaran, notifikasi kurir, katalog resto) berjalan dalam satu proses yang sama. Ini menciptakan dua bentuk kopling yang saling terkait:

Kopling temporal — Service Pesanan "terpaksa" menunggu Service Pembayaran, Service Notifikasi Kurir, dan Service Katalog Resto selesai memproses sebelum bisa memberi respons ke pelanggan. Kalau salah satu dari mereka lambat (misalnya Service Katalog Resto sedang overload karena promo), seluruh alur pemesanan ikut lambat — padahal fungsi resto menerima notifikasi sama sekali tidak relevan untuk memberi tahu pelanggan bahwa pesanannya berhasil dibuat.
Kopling struktural — karena semua modul berjalan dalam satu proses monolitik, Service Pesanan "tahu" dan bergantung langsung pada keberadaan Service Notifikasi Kurir dan Service Katalog Resto. Kalau tim kurir mau menambah logic baru di modul mereka, seluruh aplikasi harus di-build ulang dan restart bersamaan — inilah yang memicu risiko downtime total yang dilaporkan di gejala Tugas 1.

Pola event-driven pub-sub yang diterapkan lewat Message Broker (Tahap 4-5 di alur diagram) memutus kedua bentuk kopling ini sekaligus:

Memutus kopling temporal: Service Pesanan cukup mem-publish event OrderPaid dan langsung lanjut memberi respons ke pelanggan (Tahap 7), tanpa menunggu Service Notifikasi Kurir atau Service Katalog Resto selesai memproses. Waktu respons ke pelanggan jadi tidak lagi bergantung pada kecepatan pemrosesan dua service tersebut.
Memutus kopling struktural: Service Pesanan tidak perlu tahu siapa saja yang subscribe ke event OrderPaid. Kalau suatu hari tim ingin menambah subscriber baru (misalnya "Service Analytics" untuk mencatat statistik pesanan), itu bisa ditambahkan tanpa mengubah satu baris kode pun di Service Pesanan. Ini juga berarti tim kurir dan tim resto bisa deploy ulang service mereka masing-masing kapan saja, karena mereka hanya "mendengarkan" broker — bukan dipanggil langsung oleh Service Pesanan.

Dengan kata lain, gaya ini mengubah relasi antar modul dari "tahu dan bergantung langsung satu sama lain" menjadi "tahu keberadaan event, tapi tidak saling tahu siapa produsen/konsumennya" — inilah esensi loose coupling yang dibutuhkan agar tim kurir dan tim resto tidak saling mengganggu saat deploy.

Trade-off yang Muncul

Meski pola ini menyelesaikan masalah kopling, ia memunculkan kompleksitas baru yang perlu diakui secara jujur di analisis:

Kompleksitas debugging meningkat — alur eksekusi tidak lagi linier dan mudah ditelusuri seperti pemanggilan fungsi biasa. Kalau resto tidak kunjung menerima notifikasi pesanan, engineer tidak bisa lagi sekadar membaca satu stack trace dari atas ke bawah; ia harus menelusuri apakah event benar-benar ter-publish, apakah broker menerima dan menyimpannya, dan apakah Service Katalog Resto benar-benar berhasil consume event tersebut — tiga titik potensi kegagalan yang tersebar di sistem berbeda. Ini butuh distributed tracing (misalnya dengan correlation ID yang diteruskan lewat event) agar satu alur pesanan tetap bisa ditelusuri lintas service.
Eventual consistency, bukan lagi strong consistency — karena notifikasi ke kurir dan resto berjalan asinkron, ada jeda waktu (meski biasanya dalam hitungan milidetik hingga detik) antara pelanggan menerima konfirmasi pesanan dan resto benar-benar melihat pesanan itu di sistem mereka. Kalau ada bug yang membuat consumer gagal memproses event, resto bisa saja tidak pernah menerima notifikasi sama sekali — padahal dari sisi pelanggan, pesanan sudah dianggap "berhasil".
Kebutuhan mekanisme retry & dead-letter queue di level konsumen — kalau Service Katalog Resto gagal memproses event (misalnya karena sedang down saat event dikirim), event tersebut bisa hilang begitu saja kalau broker tidak dikonfigurasi dengan benar. Ini berarti tim harus menambahkan mekanisme seperti dead-letter queue (menyimpan event yang gagal diproses untuk di-retry nanti) — yang berarti ada biaya infrastruktur dan kompleksitas operasional tambahan dibanding sekadar memanggil fungsi secara langsung seperti di arsitektur monolitik.
Testing jadi lebih sulit — pada monolitik, satu service bisa diuji secara end-to-end dengan mudah dalam satu proses (unit test/integration test biasa). Pada pola event-driven, menguji bahwa Service Pesanan mem-publish event dengan benar dan Service Katalog Resto meresponsnya dengan benar butuh pengujian lintas service (misalnya dengan contract testing atau environment staging yang menyalakan broker sungguhan) — ini menambah waktu dan effort di tahap QA.

Kesimpulan singkat: Trade-off intinya adalah menukar kesederhanaan alur eksekusi linier (mudah di-trace, tapi kaku dan saling bergantung) dengan fleksibilitas deployment independen (memutus kopling, tapi menyebarkan kompleksitas ke seluruh sistem). Ini konsisten dengan prinsip umum di sistem terdistribusi: tidak ada solusi gratis — memindahkan masalah kopling berarti memindahkan lokasi kompleksitasnya, bukan menghilangkannya sepenuhnya.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

