# Jurnal Proses — Tugas 6


**Kesalahan pertama yang ditemui:**
Pada versi awal, pencarian successor hanya mengambil node pertama yang ID-nya `>=` hash key. Cara ini gagal ketika hash key lebih besar daripada ID node terbesar di ring (tidak ada node dengan ID `>=` key), sehingga hasilnya kosong/`None`. Kasus ini muncul nyata saat `node-jakarta-1` (id=177) keluar: `kurir-005` punya hash 175, dan setelah node 177 dihapus tidak ada lagi node aktif dengan ID `>= 175`. Artinya **lupa wrap-around**: ring Chord itu melingkar, bukan garis lurus.

**Cara memperbaikinya:**
Daftar ID node disimpan dalam keadaan terurut. Pencarian successor dilakukan dengan mencari ID node terkecil yang `>=` hash key. Jika tidak ditemukan, pencarian **melingkar kembali ke awal ring** dan mengambil node dengan ID terkecil (`ring[0]`). Dengan begitu, hash 175 setelah node 177 hilang dipetakan ke `node-bandung-1` (id=40), sesuai aturan Chord.

**Efek ke `join()` dan `leave()`:**
Keduanya bergantung pada `find_successor`, sehingga perbaikan wrap-around otomatis membuat perpindahan mapping benar.

- `join()` memindahkan key yang kini menjadi tanggung jawab node baru dari successor lamanya.
- `leave()` memindahkan seluruh key milik node yang keluar ke successor barunya.

---

## Skenario join/leave
- Hasil sebelum & sesudah node baru bergabung: ...
- Hasil sebelum & sesudah node keluar: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
