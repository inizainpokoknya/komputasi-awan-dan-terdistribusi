# Jurnal Proses — Tugas 2

## [21 September 2026]
- Opsi arsitektur yang dipertimbangkan: Service-Oriented Architecture (SOA) murni untuk seluruh modul, Publish-Subscribe murni (Event-driven) untuk seluruh modul, Kombinasi SOA dan Publish-Subscribe.
- Kenapa akhirnya pilih [SOA/Pub-Sub]: Kami memilih kombinasi SOA dan Publish-Subscribe, karena komunikasi sinkron (SOA/RPC) dipertahankan antara Service Pesanan dan Service Pembayaran dan juga karena transaksi finansial wajib divalidasi secara real-time sebelum prosesnya dilanjutkan. Sebaliknya, Publish-Subscribe dipilih untuk menghubungkan Service Pesanan dengan Service Katalog Resto dan Service Notifikasi Kurir melalui Message Broker. Hal tersebut bisa mengurai tight coupling dari sistem monolitik sebelumnya, sehingga saat tim Kurir melakukan deploy ulang, modul Pesanan tidak akan terblokir atau ikut down.
- Revisi diagram (versi 1 → versi 2, apa yang berubah dan kenapa): Kami mengubah dari diagram yang hanya blok menjadi alur kerja sekuensial. Tujuan pembaruan sendiri untuk memperjelas kapan sistem menggunakan pola Request-Respone secara sinkron dan kapan sistem beralih ke pola Event-Driven asinkron melalui Publish-Subscribe. Kami juga menambahkan "Kurir" dan "Resto" sebagai tujuan tujuan akhir dari sistem notifikasi, serta respon balik ke pelanggan.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
