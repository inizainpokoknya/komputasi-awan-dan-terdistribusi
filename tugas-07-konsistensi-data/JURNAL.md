# Jurnal Proses — Tugas 7

## Diskusi pemilihan model konsistensi
- Argumen yang dipertimbangkan:
* Penggunaan *Eventual Consistency* penuh memiliki keunggulan berupa performa baca/tulis yang cepat tanpa penalti latensi lintas wilayah, namun sangat berisiko untuk data finansial karena dapat memicu pembacaan saldo basi (*stale read*), penolakan pesanan yang sah, hingga potensi pemakaian saldo ganda (*double spending*).
  * Penggunaan *Sequential Consistency* penuh memastikan semua replika melihat urutan operasi transaksi (top-up, bayar, refund) secara ketat dan seragam, namun penerapan sinkronisasi global secara sinkron untuk setiap operasi dapat menambah latensi jaringan.
  * Pendekatan *Client-Centric Consistency* (khususnya *Read-Your-Writes*) dipertimbangkan sebagai jalan tengah yang praktis, di mana pengguna dijamin selalu bisa membaca hasil pembaruan datanya sendiri meski replikasi latar belakang antar server regional belum selesai[cite: 1].
- Kesimpulan akhir & alasan: ...

## Simulasi (jika dikerjakan)
- Hasil skenario naif vs Read-Your-Writes: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
