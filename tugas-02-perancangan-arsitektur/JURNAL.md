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
## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

