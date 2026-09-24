# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** [nama kelompok]

| Nama | NIM | Kontribusi |
|---|---|---|
| [Zain Ahmad Suraiban] | [103072430001] | [Latency is Zero] |
| [Muhammad Rohman Azizi] | [103072400011] | [The Network Reliable] |
| [Rochmatul Choirul Anam] | [103072400024] | [Topology Doesn't Change & Single Point of Failure (SPOF)] |
| [Wirajalu Setyonegoro Wibowo] | [103072400094] | [Topology Doesn't Change & Single Point of Failure (SPOF)] |

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

## Pitfall 3: [Topology Doesn't Change & Single Point of Failure (SPOF)] — ditulis oleh [Rochmatul Choirul Anam]

**Bukti di skenario:** "Server backend kadang crash total dan perlu di-restart manual."
"Saat trafik naik, satu server yang menangani semua modul (pesanan, pembayaran, notifikasi kurir) kewalahan karena semuanya berjalan di satu proses monolitik yang sama."

**Kenapa ini keliru:** Asumsi bahwa topologi sistem bersifat statis dan satu node server mampu menampung seluruh beban kerja tanpa perubahan adalah kesalahan fatal. Dalam realitas sistem terdistribusi, infrastruktur selalu dinamis: server bisa mengalami kegagalan perangkat keras (hardware failure), kebocoran memori, atau kelebihan beban (overload) yang tidak terduga. Mengandalkan satu entitas fisik untuk menjalankan seluruh logika bisnis menciptakan kerentanan total; jika entitas itu gagal, tidak ada cadangan (backup) yang siap mengambil alih secara otomatis.

**Dampak ke FoodGo:** Terjadinya Total Service Outage yang bergantung pada intervensi manusia. Ketika server monolitik tersebut crash akibat kehabisan sumber daya (CPU/RAM) saat lonjakan pesanan, seluruh layanan FoodGo—mulai dari pemesanan hingga pelacakan kurir—berhenti berfungsi. Tim engineering harus melakukan restart manual, yang berarti adanya downtime signifikan. Selama periode ini, FoodGo kehilangan potensi pendapatan, merusak reputasi merek, dan mengecewakan pelanggan yang sedang lapar. Tidak adanya isolasi juga berarti bug kecil di modul notifikasi bisa meruntuhkan modul pembayaran.

**Solusi desain awal:** Implementasi **Redundansi Aktif-Aktif dengan Load Balancer dan Orkestrasi Otomatis.**
- Ubah arsitektur dari satu server tunggal menjadi beberapa instans layanan yang berjalan secara paralel.
- Gunakan Load Balancer di depan instans-instans tersebut untuk mendistribusikan trafik secara merata.
- Terapkan Health Checks otomatis: jika satu instans tidak merespons, Load Balancer akan segera menghentikan pengiriman trafik ke instans tersebut.
- Gunakan alat orkestrasi (seperti Kubernetes) untuk mendeteksi kegagalan dan secara otomatis meluncurkan instans pengganti (self-healing) tanpa perlu campur tangan manual tim engineering.

**Trade-off:** Solusi ini meningkatkan **kompleksitas manajemen data dan biaya operasional.**
- **Konsistensi Data:** Dengan banyak instans yang berjalan bersamaan, memastikan konsistensi data (misalnya: mencegah pesanan ganda atau stok makanan yang tidak akurat) menjadi jauh lebih sulit dan memerlukan mekanisme distributed locking atau database yang mendukung konsistensi tinggi.
- **Biaya:** Menjalankan beberapa server sekaligus jelas lebih mahal daripada satu server, meskipun hal ini sebanding dengan nilai keandalan (reliability) yang didapat. Selain itu, tim DevOps perlu memiliki keahlian lebih tinggi untuk mengelola lingkungan yang terdistribusi.

---

## Kesimpulan Kelompok

Jika ketiga pitfall ini diperbaiki, arsitektur yang disarankan secara garis besar adalah arsitektur *microservices* yang terdistribusi secara aktif-aktif, dengan mekanisme *resiliency* di setiap titik komunikasi, yang mencakup:

* **Isolasi layanan:** Memecah proses monolitik menjadi **service-service** independen (pesanan, pembayaran, notifikasi kurir) yang masing-masing punya siklus *deploy* dan skalanya sendiri, sehingga kegagalan satu modul tidak menjalar ke modul lain.
* **Kontrol waktu dan kegagalan antar-service:** Penerapan timeout yang realistis, retry dengan exponential backoff + jitter, dan circuit breaker untuk mencegah efek domino ketika satu service bermasalah.
* **Redundansi dan self-healing:** Menempatkan banyak instans per service di belakang load balancer dengan health check otomatis, serta memanfaatkan orkestrasi (mis. Kubernetes) agar sistem bisa pulih sendiri tanpa intervensi manual saat ada instans yang crash.
* **Jaminan konsistensi & idempotency:** Karena mekanisme retry dan multi-instans membuka risiko duplikasi transaksi, diperlukan idempotency key pada operasi pembayaran/pesanan serta strategi konsistensi data yang jelas (misalnya lewat distributed lock atau event driven consistency).