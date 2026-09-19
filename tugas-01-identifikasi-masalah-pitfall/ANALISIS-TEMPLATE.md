# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** [nama kelompok]

| Nama | NIM | Kontribusi |
|---|---|---|
| [Zain Ahmad Suraiban] | [103072430001] | [pitfall/bagian yang dikerjakan] |
| [Muhammad Rohman Azizi] | [103072400011] | [The Network Reliable] |
| [nama 3] | [nim] | [pitfall/bagian yang dikerjakan] |
| [nama 4] | [nim] | [pitfall/bagian yang dikerjakan] |

## Pitfall 1: [nama pitfall] — ditulis oleh [nama]

**Bukti di skenario:** [kutip/paraphrase bagian skenario]

**Kenapa ini keliru:** [penjelasan]

**Dampak ke FoodGo:** [mekanisme kegagalan konkret]

**Solusi desain awal:** [usulan solusi]

**Trade-off:** [apa yang dikorbankan/risiko dari solusi ini]

---

## Pitfall 2: [The Network Reliable] — ditulis oleh [Muhammad Rohman Azizi]

**Bukti di skenario:** [Tim menemukan bahwa kode mereka menulis asumsi seperti # network is always reliable, no need for retry dan tidak ada timeout sama sekali pada pemanggilan antar service (modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu).]

**Kenapa ini keliru:** [Karena dalam sistem terdistribusi nyata, tidak ada jaringan yang 100% reliable. Panggilan antar service yang melewati jaringan bisa mengalami packet loss, koneksi terputus, DNS gagal resolve, atau service sedang restart. Saat trafik melonjak, meningkatkan kemungkinkan koneksi gagal sesaat karena resource jaringan ikut jenuh.]

**Dampak ke FoodGo:** [Saat modul pembayaran mengalami masalah sesaat, modul pesanan akan mengalami kegagalan total tanpa mencoba ulang, yang padahal jika dicoba ulang beberapa saat kemudian kemungkinan besar berhasil. Ini membuat tingkat kegagalan transaksi jauh lebih tinggi dari yang seharusnya, terutama ketika jam sibuk.]

**Solusi desain awal:** [Memastikan setiap panggilan jaringan punya batas maksimum, menambahkan mekanisme percobaan ulang otomatis saat kegagalan bersifat sementara dengan jeda yang meningkat bertahap (exponential backoff) dan variasi acak (jitter) agar tidak semua user mencoba bersamaan. Membatasi jumlah percobaan user (contoh maksimal 3 percobaan) agar tidak menunggu tanpa kejelasan.]

**Trade-off:** [User harus menunggu lebih lama untuk mendapat hasil akhir, karena sistem mencoba beberapa kali dengan jeda yang makin panjang di setiap percobaannya (exponential backoff) sebelum benar benar menyerah]

---

## Pitfall 3: [nama pitfall] — ditulis oleh [nama]

(ulangi struktur di atas)

---

## Kesimpulan Kelompok

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]
