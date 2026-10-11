# Jurnal Proses — Tugas 4[cite: 1, 2]

## Jalur yang dipilih[cite: 1, 2]
- **Keduanya (RPC dan MQ)**, alasan: studi kasus FoodGo memuat dua kebutuhan berbeda[cite: 1, 2]. Cek saldo/proses pembayaran butuh jawaban seketika (sinkron → RPC), sedangkan notifikasi "pembayaran berhasil" ke kurir tidak boleh membuat modul Pembayaran menunggu (asinkron → MQ)[cite: 1, 2]. Jalur RPC dan MQ dikerjakan penuh supaya perbedaannya bisa dibandingkan langsung[cite: 1, 2].
  
## Kendala teknis[cite: 1, 2]
- **Jalur A (RPC):** saat `client.py` dijalankan sebelum `server.py`, muncul `ConnectionRefusedError: [Errno 111] Connection refused`[cite: 1, 2]. Solusi: urutan menjalankan harus server dulu, baru client[cite: 1, 2]. Jika server dihentikan (Ctrl+C) saat client sedang menunggu, client menerima `xmlrpc.client.Fault: KeyboardInterrupt` karena RPC bersifat sinkron, tidak memiliki antrean penyimpanan, dan request langsung gagal jika server mati[cite: 2].
- **Jalur B (MQ):** *(isi dengan kendala nyata kalian, mis. `docker compose` belum jalan → `pika.exceptions.AMQPConnectionError`, port 5672/15672 bentrok, Docker Desktop belum aktif, dll. Jika tidak ada kendala, tulis itu.)*[cite: 1, 2]
- Fungsi server diberi `time.sleep(2)` sengaja agar waktu tunggu client terlihat jelas (±2,00 detik per panggilan), karena tanpa jeda pemanggilan lokal terlalu cepat untuk diamati[cite: 1, 2]. Pada pengujian nyata, client mengalami blocking/diam selama 4,05 detik pada `cek_saldo` dan 4,04 detik pada `proses_pembayaran` hingga server selesai membalas[cite: 2].

## Uji "pesan tidak hilang" (khusus Jalur B)[cite: 1, 2]
- Langkah uji: matikan consumer → jalankan publisher → nyalakan consumer[cite: 1].
  1. Jalankan `docker compose up -d`, pastikan consumer belum dijalankan (atau dimatikan dengan Ctrl+C)[cite: 2].
  2. Jalankan `python publisher.py` 2–3 kali (tiap run mengirim 3 event secara asinkron tanpa blocking)[cite: 2].
  3. Buka dashboard `http://localhost:15672` tab *Queues* → `pembayaran_berhasil`, amati kolom **Ready** bertambah sesuai jumlah run (mis. 6 pesan tertunda)[cite: 2].
  4. Nyalakan `python consumer.py`[cite: 2].
- Hasil yang diamati: Consumer langsung memproses dan mencetak seluruh pesan yang tertunda (misal: "Kurir menerima notifikasi pembayaran untuk user1 sejumlah 20000", dst.), lalu antrean **Ready** pada dashboard RabbitMQ turun kembali menjadi 0[cite: 2]. Pesan tersimpan aman di antrean RabbitMQ karena queue disetel `durable=True` dan pesan bersifat `delivery_mode=Persistent` (tersimpan ke disk broker), serta baru dihapus setelah consumer mengirim `basic_ack`[cite: 2].

## Log Penggunaan AI (Level 2)[cite: 1, 2]

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md)[cite: 1]. Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai[cite: 1]. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir[cite: 1]. Isi dengan jujur sesuai yang benar-benar kalian lakukan[cite: 2].

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 11 Oktober 2026 | Gemini | "Bantu buatkan outline struktur jurnal pengujian sistem untuk membandingkan sifat sinkron RPC vs asinkron Message Broker pada FoodGo." | Menyarankan kerangka perbandingan: alasan pemilihan metode, pencatatan kendala urutan start server/client, pengujian kondisi server/consumer down, dan perilaku blocking. | Menggunakan kerangka tersebut sebagai acuan penulisan, lalu mengisi seluruh data teknis, pesan error riil (ConnectionRefusedError), durasi blocking (4,05 detik), dan konfigurasi parameter RabbitMQ berdasarkan hasil praktikum sendiri. |