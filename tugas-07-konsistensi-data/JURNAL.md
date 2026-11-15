# Jurnal Proses — Tugas 7

## Diskusi pemilihan model konsistensi
- Argumen yang dipertimbangkan:
  * Penggunaan *Eventual Consistency* penuh memiliki keunggulan berupa performa baca/tulis yang cepat tanpa penalti latensi lintas wilayah, namun sangat berisiko untuk data finansial karena dapat memicu pembacaan saldo basi (*stale read*), penolakan pesanan yang sah, hingga potensi pemakaian saldo ganda (*double spending*).
  * Penggunaan *Sequential Consistency* penuh memastikan semua replika melihat urutan operasi transaksi (top-up, bayar, refund) secara ketat dan seragam, namun penerapan sinkronisasi global secara sinkron untuk setiap operasi dapat menambah latensi jaringan.
  * Pendekatan *Client-Centric Consistency* (khususnya *Read-Your-Writes*) dipertimbangkan sebagai jalan tengah yang praktis, di mana pengguna dijamin selalu bisa membaca hasil pembaruan datanya sendiri meski replikasi latar belakang antar server regional belum selesai[cite: 1].
- Kesimpulan akhir & alasan:
  * *Eventual Consistency* saja tidak cukup dan ditolak untuk data saldo *e-wallet* (hanya dipertahankan untuk data non-kritis seperti rating atau jumlah ulasan).
  * Sistem memadukan jaminan urutan transaksi (*Sequential Consistency* pada operasi saldo utama) dengan mekanisme *Read-Your-Writes*. Alasannya, dalam transaksi keuangan, selisih data sementara pun berakibat pada kerugian finansial nyata dan hilangnya kepercayaan pelanggan, sehingga akurasi saldo jauh lebih diprioritaskan dibandingkan sedikit tambahan latensi pengalihan (*redirect*) server.

## Simulasi (jika dikerjakan)
- Hasil skenario naif vs Read-Your-Writes: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
