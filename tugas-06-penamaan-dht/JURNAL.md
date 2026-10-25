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

* **Hasil sebelum & sesudah node baru bergabung:**
  Sebelum `node-medan-1` (id=123) bergabung, ring berisi node dengan ID 40, 102, 136, dan 177. Pada kondisi ini `kurir-012` (hash=116) dipegang oleh node id=136, karena 136 adalah node pertama yang ID-nya lebih besar atau sama dengan 116.
  Setelah `node-medan-1` bergabung, program mencetak:

  Node 'node-medan-1' (id=123) bergabung, alamat 10.0.0.5, successor lama = 136
    PINDAH: kurir-012 (hash=116) dari node id=136 -> node id=123
  
  Sekarang `kurir-012` dipegang node id=123, karena 123 menjadi successor baru untuk hash 116. Hanya satu key yang berpindah, sedangkan key lain tidak berubah. Lookup `kurir-001` juga masih benar (`192.168.1.10`), jadi penambahan node tidak merusak mapping yang sudah ada.

* **Hasil sebelum & sesudah node keluar:**
  Sebelum `node-jakarta-1` (id=177) keluar, node tersebut memegang `kurir-005` (hash=175). Setelah node keluar, program mencetak:
  ```text
  Node 'node-jakarta-1' (id=177) keluar dari ring
    PINDAH: kurir-005 (hash=175) dari node id=177 -> node id=40
  ```
  Sisa node di ring adalah 40, 102, 123, dan 136. Tidak ada lagi node dengan ID >= 175, sehingga pencarian successor berputar balik (wrap-around) ke node dengan ID terkecil, yaitu `node-bandung-1` (id=40). Maka `kurir-005` pindah ke node id=40. Lookup `kurir-001` dan `kurir-002` tetap berhasil (`192.168.1.10` dan `192.168.1.11`), jadi data tidak hilang saat node keluar.
## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
