# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** [nama kelompok]

| Nama | NIM | Kontribusi |
|---|---|---|
| [Zain Ahmad Suraiban] | [103072430001] | [Latency is Zero] |
| [Muhammad Rohman Azizi] | [103072400011] | [The Network Reliable] |
| [Rochmatul Choirul Anam] | [103072400024] | [pitfall/bagian yang dikerjakan] |
| [Wirajalu Setyonegoro Wibowo] | [103072400094] | [pitfall/bagian yang dikerjakan] |

## Pitfall 1: [Latency is Zero] — ditulis oleh [Zain Ahmad Suraiban]

**Bukti di skenario:** [Tim menemukan bahwa kode mereka... tidak ada timeout sama sekali pada pemanggilan antar service (modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu)."
"Aplikasi jadi sangat lambat, beberapa permintaan timeout.]

**Kenapa ini keliru:** [Dalam sistem terdistribusi nyata, latensi tidak pernah nol. Komunikasi antar-proses atau antar-jaringan selalu melibatkan biaya waktu (overhead) akibat propagasi sinyal, serialisasi data, antrian pada router, dan pemrosesan di sisi penerima. Mengasumsikan latensi nol berarti mengabaikan variabilitas kinerja jaringan dan beban server, yang merupakan hal yang tidak dapat dihindari dalam lingkungan produksi yang dinamis.]

**Dampak ke FoodGo:** [Karena asumsi latensi nol, pengembang tidak menetapkan batas waktu (timeout). Ketika modul pembayaran mengalami keterlambatan respons (misalnya karena beban tinggi atau garbage collection), modul pesanan akan memblokir thread eksekusi secara indefinitif. Hal ini menyebabkan kehabisan thread pool pada server backend. Server menjadi tidak responsif terhadap permintaan baru meskipun sumber daya CPU masih tersedia, karena semua worker thread terjebak dalam status waiting. Ini memicu efek domino yang membuat seluruh aplikasi terasa sangat lambat dan akhirnya crash karena kehabisan memori atau file descriptor]

**Solusi desain awal:** [Implementasi Strict Timeout pada setiap panggilan antar-layanan (inter-service calls). Setiap permintaan harus memiliki batas waktu maksimal yang realistis (misalnya 2-5 detik). Jika respons tidak diterima dalam batas waktu tersebut, koneksi harus diputus secara paksa dan dianggap sebagai kegagalan. Solusi ini sebaiknya dipadukan dengan pola Circuit Breaker untuk mencegah pemanggilan berulang ke layanan yang sedang bermasalah.]

**Trade-off:** [Penerapan timeout yang ketat berisiko menyebabkan false positive failures. Artinya, permintaan sebenarnya berhasil diproses oleh server tujuan, tetapi responsnya datang sedikit lebih lambat dari batas timeout yang ditetapkan. Klien akan menganggap permintaan gagal dan mungkin memicu retry, yang berpotensi menyebabkan duplikasi transaksi (misalnya: pembayaran terpotong dua kali) jika tidak ditangani dengan mekanisme idempotency yang tepat.]

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
