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

### Implementasi pada `src/replica_simulation.py`
- **TODO 1 (Simulasi Delay Replikasi):** Menggunakan `threading.Timer(REPLICATION_DELAY, self.bandung.write, args=(user_id, saldo_baru, version))` agar penulisan ke replika Bandung tertunda selama `2.0` detik secara asinkron di latar belakang, sementara penulisan di server utama (Jakarta) langsung selesai.
- **TODO 2 (Mekanisme *Read-Your-Writes*):** Memeriksa apakah versi data pada replika tujuan lebih kecil dari `versi_minimal` yang dipegang oleh client (`replica.last_write_version.get(user_id, 0) < versi_minimal`). Jika replika tujuan (Bandung) terdeteksi masih *stale*, pembacaan langsung dialihkan (*redirect*) ke server Jakarta yang sudah memiliki versi terbaru.
- **TODO 3 (Pengujian Perbandingan):** Memanggil `baca_saldo_naif` dan `baca_saldo_read_your_writes` secara berdampingan tepat setelah top-up kedua (sebelum delay replikasi 2 detik selesai) untuk membuktikan perbedaan hasilnya.

### Hasil Skenario Naif vs Read-Your-Writes
Berdasarkan eksekusi `python3 src/replica_simulation.py` (lihat `bukti/Simulasi.png`):

1. **Skenario Naif (Tanpa *Read-Your-Writes*):**
   - `user1` melakukan top-up sebesar `50000` di server Jakarta (`[Jakarta] WRITE saldo user1 = 50000.0 (versi 1)`), sedangkan replikasi ke Bandung tertunda `2.0` detik.
   - Saat pelanggan langsung memesan makanan `0.5` detik kemudian dan membaca saldo dari server Bandung menggunakan `baca_saldo_naif`, nilai yang dikembalikan adalah **`0.0`** (*inconsistent / stale read*).
   - Replika Bandung baru memperbarui saldonya menjadi `50000.0` (versi 1) setelah jeda 2 detik berlalu. Akibatnya, pesanan pelanggan ditolak padahal top-up sudah berhasil.

2. **Skenario dengan *Read-Your-Writes*:**
   - Setelah menunggu replika sinkron di angka `50000.0`, `user1` kembali melakukan top-up sebesar `20000` di server Jakarta sehingga saldo menjadi `70000.0` dengan `versi_terakhir = 2`.
   - Saat langsung dibaca dari server Bandung tanpa menunggu replikasi selesai:
     * Pemanggilan `baca_saldo_naif("user1", "Bandung")` masih mengembalikan saldo lama yaitu **`50000.0`**.
     * Pemanggilan `baca_saldo_read_your_writes("user1", "Bandung", versi_minimal=2)` mendeteksi bahwa versi di Bandung masih `< 2` (`[RYW] Bandung masih stale (versi < 2), redirect ke Jakarta`), lalu mengambil data dari Jakarta dan mengembalikan nilai yang akurat yaitu **`70000.0`**.
   - **Kesimpulan Simulasi:** Mekanisme *Read-Your-Writes* berbasis pelacakan versi (*version tracking*) per client berhasil mencegah bug pembacaan saldo basi (*stale read*) meskipun replikasi antar-server mengalami keterlambatan.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 01 Nov 2026 | Claude | Jelaskan perbedaan dampak bisnis antara Sequential Consistency dan Eventual Consistency pada kasus saldo e-wallet dibandingkan fitur jumlah like di media sosial, serta bagaimana konsep Read-Your-Writes bekerja. | AI memberikan poin perbandingan terkait sifat nilai uang vs metrik popularitas, risiko *double spending* dan penolakan transaksi jika data *stale*, serta konsep pelacakan versi/timestamp pada sisi klien untuk *Read-Your-Writes*. | Poin-poin tersebut didiskusikan kembali oleh kelompok, lalu disusun ulang menggunakan bahasa sendiri menjadi tabel perbandingan dan pengelompokan model konsistensi data FoodGo di `README.md`. |
| 02 Nov 2026 | Gemini | Bagaimana cara mensimulasikan penundaan eksekusi fungsi secara non-blocking di Python menggunakan modul `threading` standar? | AI menjelaskan penggunaan `threading.Timer(interval, function, args=...)` yang menjalankan fungsi di thread terpisah setelah waktu tunda tertentu tanpa memblokir thread utama. | Konsep `threading.Timer` digunakan untuk mengimplementasikan TODO 1 pada `src/replica_simulation.py`, serta dipadukan dengan pengecekan `last_write_version` untuk logika redirect pada TODO 2 dan pengujian di TODO 3. |
