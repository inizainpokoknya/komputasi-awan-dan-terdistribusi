# Jurnal Proses — Tugas 2

## [21 September 2026]
- Opsi arsitektur yang dipertimbangkan: Service-Oriented Architecture (SOA) murni untuk seluruh modul, Publish-Subscribe murni (Event-driven) untuk seluruh modul, Kombinasi SOA dan Publish-Subscribe.
- Kenapa akhirnya pilih [SOA/Pub-Sub]: Kami memilih kombinasi SOA dan Publish-Subscribe, karena komunikasi sinkron (SOA/RPC) dipertahankan antara Service Pesanan dan Service Pembayaran dan juga karena transaksi finansial wajib divalidasi secara real-time sebelum prosesnya dilanjutkan. Sebaliknya, Publish-Subscribe dipilih untuk menghubungkan Service Pesanan dengan Service Katalog Resto dan Service Notifikasi Kurir melalui Message Broker. Hal tersebut bisa mengurai tight coupling dari sistem monolitik sebelumnya, sehingga saat tim Kurir melakukan deploy ulang, modul Pesanan tidak akan terblokir atau ikut down.
- Revisi diagram (versi 1 → versi 2, apa yang berubah dan kenapa): Kami mengubah dari diagram yang hanya blok menjadi alur kerja sekuensial. Tujuan pembaruan sendiri untuk memperjelas kapan sistem menggunakan pola Request-Respone secara sinkron dan kapan sistem beralih ke pola Event-Driven asinkron melalui Publish-Subscribe. Kami juga menambahkan "Kurir" dan "Resto" sebagai tujuan tujuan akhir dari sistem notifikasi, serta respon balik ke pelanggan.

Jadi kita akhirnya sepakat pakai kombinasi: SOA/RPC buat bagian Pesanan-Pembayaran (karena emang harus sinkron, harus dipastiin real-time), sisanya (notifikasi ke kurir & resto) pake Pub-Sub lewat message broker.

## Kenapa kombinasi ini

Alasan utamanya karena Pembayaran itu sifatnya kritikal, gaboleh "keliru" atau "belum ke-konfirm" tapi pesanan udah lanjut. Makanya komunikasi Pesanan ↔ Pembayaran tetep pakai request-response biasa (RPC), biar Service Pesanan bener-bener nunggu hasilnya dulu sebelum ngasih tau pelanggan pesanannya berhasil atau nggak.

Sedangkan buat Kurir sama Resto, mereka gapunya urusan langsung sama proses bayar-membayar. Mereka cuma perlu "tau" kalau ada pesanan baru yang udah dibayar, terus mereka proses sendiri-sendiri. Makanya ini cocok pake Pub-Sub — Service Pesanan tinggal publish event terus lanjut, gaperlu nunggu Kurir atau Resto selesai proses punya mereka.

Ini juga yang jadi solusi buat masalah tim Kurir yang katanya suka bikin down modul lain pas deploy ulang (masalah dari Tugas 1). Karena sekarang Kurir cuma "denger" broker doang, jadi kalau mereka mau redeploy servicenya, Pesanan gaikut down.

## Revisi Diagram V1 -> V2

Diagram versi 1 kemarin cuma kotak-kotak doang, panahnya belum jelas mana yang sync mana yang async — istilahnya masih "asal ada panah" aja, gaada penanda jenis komunikasinya.

Di v2 ini kita perbaiki jadi alur per komponen yang lebih jelas: Pelanggan kirim request ke Service Pesanan (ditandain sync), Pesanan manggil Pembayaran lewat RPC (sync juga), abis itu Pesanan publish event OrderCreated ke Message Broker (async), terus broker nerusin (subscribe) ke Service Notifikasi Kurir sama Service Katalog Resto. Setiap panah sekarang dikasih label jenis komunikasinya biar keliatan mana yang request-response biasa sama mana yang event-based.

<img src="diagram/Diagram%20Versi%202.png" alt="Diagram Versi 2" width="600">

## Alur end-to-end (skenario: pelanggan pesan → bayar → resto & kurir dapet notif)

Skenarionya: pelanggan pesen makanan di FoodGo, sistem validasi pembayarannya, terus resto sama kurir dapet notif tanpa bikin pelanggan nunggu itu semua kelar. Di diagram v2, yang digambar baru sampe ke titik broker nerusin event ke dua servis subscriber-nya — belom nyampe ke Kurir/Resto langsung atau balesan akhir ke pelanggan. Tapi biar jawab soal secara lengkap, kita jabarin juga alur sampe abis (termasuk bagian yang belom ada di gambar), komponen mana komunikasi ke siapa dan jenis komunikasinya:

Pelanggan → Service Pesanan Jenis: sinkron, request-response. Pelanggan kirim HTTP request buat bikin pesanan, terus nunggu balesan langsung sebelum ngelanjutin apa-apa di aplikasinya.

Service Pesanan → Service Pembayaran Jenis: sinkron, request-response (RPC). Pesanan manggil Pembayaran buat validasi & charge kartu/e-wallet. Ini yang sifatnya blocking — Pesanan bener-bener berhenti nunggu hasil dari Pembayaran, gabisa lanjut kemana-mana dulu. (Ini juga yang jadi akar masalah "latency" di Tugas 1 kalo gapake timeout — servis nunggu tanpa batas.) Pembayaran balik jawab sukses/gagal ke Pesanan, masih bagian dari RPC yang sama, jadi masih sinkron juga.

Service Pesanan → Message Broker Jenis: asinkron, event-based (publish). Abis pembayaran dikonfirmasi sukses, Pesanan publish event OrderCreated (di jurnal lama sempet ditulis OrderPaid, tapi maksudnya sama) ke broker. Di titik ini Pesanan gak nunggu ada yang proses eventnya atau nggak, dia bisa langsung lanjut balesin pelanggan.

Message Broker → Service Notifikasi Kurir & Service Katalog Resto Jenis: asinkron, event-based (subscribe), paralel. Ini bagian terakhir yang ada di diagram v2. Dua servis ini masing-masing subscribe ke event tadi dan nerima dari broker secara independen — mereka gak saling tau keberadaan satu sama lain, cuma sama-sama "dengerin" broker aja. Karena paralel, proses di keduanya jalan bersamaan, bukan gantian satu-satu.

(Belum ada di gambar v2) Service Notifikasi Kurir → Kurir, dan Service Katalog Resto → Resto Jenis: masih async, efek samping dari proses subscribe di atas. Notifikasi Kurir ngasih tau kurir buat ambil pesanan, Katalog Resto ngasih tau resto kalo ada pesanan masuk yang perlu disiapin.

(Belum ada di gambar v2) Service Pesanan → Pelanggan Jenis: sinkron, request-response — ini balesan dari request pertama tadi. Poin pentingnya, Pesanan bisa balikin konfirmasi ke pelanggan tanpa nunggu notifikasi ke Kurir/Resto beres duluan, soalnya publish event di broker sifatnya udah "lempar terus lupa" (gapake nunggu balesan).

Jadi kalo diringkes sesuai jenis komunikasinya: bagian Pelanggan-Pesanan-Pembayaran itu sync (request-response), sedangkan bagian Pesanan-Broker-Kurir/Resto itu async (event-based publish/subscribe) yang jalan di "belakang layar" tanpa bikin pelanggan nunggu.

## Kenapa pola ini nyelesain masalah coupling di Tugas 1

Tugas 1 itu masalahnya bukan cuma soal timeout doang, tapi emang dari arsitekturnya sendiri yang monolitik — semua modul nempel jadi satu, jadi kalo satu lemot/error semua ikut kena. Ini kalo dipecah bisa dibagi jadi dua masalah:

Yang pertama, kopling temporal — Pesanan kepaksa nunggu Kurir & Resto beres dulu baru bisa jawab pelanggan. Padahal buat pelanggan, dia cuma peduli pesanannya berhasil dibuat atau nggak, gapeduli soal kurir udah ditugasin apa belom.

Yang kedua, kopling struktural — karena satu proses, Pesanan otomatis "kenal" dan gantung ke keberadaan Kurir & Resto secara langsung. Jadi kalo tim Kurir ganti logic dikit aja, semua servis lain ikut harus di-rebuild bareng. Ini penyebab utama kenapa deploy bisa bikin downtime total kemarin.

Nah, pake broker (tahap 4-5) ini masalah kopling temporal keselesain karena Pesanan gaperlu nunggu apa-apa lagi setelah publish, langsung jawab pelanggan. Kopling struktural juga keselesain karena Pesanan gaperlu tau siapa aja yang denger event itu — misal suatu saat mau nambah "Service Analytics" buat nyatet statistik pesanan, itu bisa nambah subscriber baru tanpa ubah kode Pesanan sama sekali. Kurir sama Resto juga bebas redeploy kapan aja karena mereka cuma dengerin broker, bukan dipanggil langsung sama Pesanan.

## Trade-off (kekurangan yang muncul)

Ini bagian yang kadang keskip kalo cuma bahas kelebihan doang, jadi kita coba jujur juga soal kekurangannya:

- **Debug jadi lebih ribet.** Kalo dulu tinggal baca stack trace dari atas ke bawah, sekarang kalo misal Resto gapernah dapet notifnya, kita harus cek satu-satu: eventnya kekirim beneran gak ke broker, brokernya nerima gak, terus Katalog Resto beneran berhasil consume gak. Tiga titik yang bisa gagal, tersebar di tempat beda-beda. Makanya butuh semacam correlation ID yang nempel di tiap event biar bisa ditrack alurnya lintas servis.
- **Eventual consistency**, bukan strong consistency lagi. Karena prosesnya async, ada jeda (walopun keciiil, biasanya ms sampe detik) antara pelanggan dapet konfirmasi sama Resto beneran liat pesanannya di sistem mereka. Kalo pas lagi sial ada bug di consumer, bisa aja Resto gapernah dapet notif itu sama sekali — padahal di sisi pelanggan udah dianggep "sukses".
- **Butuh retry & dead-letter queue**. Kalo Katalog Resto lagi down pas event dikirim, dan brokernya gak dikonfig bener, event itu bisa ilang gitu aja. Jadi mesti nambah mekanisme kayak DLQ (nyimpen event yang gagal diproses, buat di-retry nanti) — ini nambah biaya infrastruktur & kompleksitas yang sebelumnya gaperlu dipikirin di monolitik.
- **Testing lebih susah**. Di monolitik kan gampang, tinggal unit test/integration test biasa dalam satu proses. Di event-driven gini, buat mastiin Pesanan publish bener dan Resto respon bener, butuh testing lintas servis (contract testing atau nyalain broker beneran di staging) — makan waktu lebih di tahap QA.
Kesimpulan

Intinya kita nuker kesederhanaan alur yang linear (gampang ditrace tapi kaku & saling gantung) sama fleksibilitas deploy yang independen (kopling putus, tapi kompleksitasnya nyebar ke seluruh sistem). Kayak prinsip di sistem terdistribusi pada umumnya — gaada yang gratis, masalah kopling yang dipindahin ya cuma mindahin lokasi ribetnya doang, bukan ngilangin sepenuhnya.

## Log Penggunaan AI (Level 2)

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 26 Sep 2026 | Claude | The FoodGo case where the order module needs to call both a payment service and a notification service, compare pure SOA, pure Pub-Sub, and a hybrid approach, and justify which one avoids the tight-coupling problem from Task 1 while still keeping payment validation reliable. | Claude memberikan perbandingan 3 opsi, menekankan jika pembayaran itu membutuhkan sinkron karena kritikal (real-time validation), sedangkan notifikasi cocok pake pub-sub karena gapunya dependensi langsung ke proses bayar | Kami tidak langsung pakai alasan dari Claude mentah-mentah, tapi didiskusiin dulu di kelompok — akhirnya alasan yang dipake diringkas ulang pake bahasa sendiri di bagian "Kenapa Kombinasi Ini", fokus ke poin kritikalnya transaksi duit yang emang jadi concern utama kita |
| 26 Sep 2026 | Claude | Review this architecture diagram (v2) against the assignment rubric criteria — communication type labeling, component completeness, and consistency with the accompanying journal narrative — and list what still doesn't meet the requirements | Claude menemukan beberapa hal: penomoran tahap di diagram tidak konsisten sama narasi jurnal, ada typo "Request-Respone", dan istilah "Latency is Zero" butuh konteks lebih jelas buat pembaca yang gak tau Tugas 1 kita | Typo langsung kami benerin. Soal penomoran, kami diskusiin ulang mana yang bener-bener perlu diubah di jurnal vs yang emang keterbatasan diagram doang (jadi ada beberapa masukan yang kita skip karena kerasa kepanjangan buat konteks tugas kita) |
| 27 Sep 2026 | Claude | Based on the FoodGo scenario where the order module calls the payment module without a timeout, explain the failure mechanism of thread exhaustion caused by the 'latency is zero' assumption. Also, discuss the trade-offs of implementing strict timeouts. | AI explained how a blocking RPC call with no timeout ties up a request-handling thread for as long as the downstream service takes to respond, so under load this exhausts the available thread pool and causes cascading failure; it also laid out the trade-off that a strict timeout avoids exhaustion but introduces its own risk of prematurely failing slow-but-valid payment transactions | We used this to sharpen the explanation of why Task 2's blocking RPC call between Order and Payment services is the same root cause as Task 1's "Latency is Zero" issue, and folded the timeout trade-off point into our own trade-off discussion instead of copying the AI's phrasing directly |
| 27 Sep 2026 | Claude | Rewrite the trade-off analysis section (debugging complexity, eventual consistency, dead-letter queue, testing difficulty) so it reads less like AI-generated text and more like a student's own casual writing style." | AI provided a draft broken down by point (debugging, eventual consistency, DLQ, testing), with the tone adjusted to sound more casual/personal | We re-read every point and rephrased several sentences to better match our own writing style, and added a concrete example (e.g. the Resto service "overloaded from a promo") to tie it more closely to our own scenario |
