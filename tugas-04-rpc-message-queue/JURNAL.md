# Jurnal Proses — Tugas 4

## Jalur yang dipilih
- **Keduanya (RPC dan MQ)**, alasan: studi kasus FoodGo memuat dua kebutuhan berbeda.
  Cek saldo/proses pembayaran butuh jawaban seketika (sinkron → RPC), sedangkan notifikasi
  "pembayaran berhasil" ke kurir tidak boleh membuat modul Pembayaran menunggu (asinkron → MQ).
  Jalur RPC dan MQ dikerjakan penuh supaya perbedaannya bisa dibandingkan langsung.
  
## Kendala teknis
-  **Jalur A (RPC):** saat `client.py` dijalankan sebelum `server.py`, muncul
  `ConnectionRefusedError: [Errno 111] Connection refused`. Solusi: urutan menjalankan harus
  server dulu, baru client.
- **Jalur B (MQ):** *(isi dengan kendala nyata kalian, mis. `docker compose` belum jalan →
  `pika.exceptions.AMQPConnectionError`, port 5672/15672 bentrok, Docker Desktop belum aktif, dll.
  Jika tidak ada kendala, tulis itu.)*
- Fungsi server diberi `time.sleep(2)` sengaja agar waktu tunggu client terlihat jelas
  (±2,00 detik per panggilan), karena tanpa jeda pemanggilan lokal terlalu cepat untuk diamati.

## Uji "pesan tidak hilang" (khusus Jalur B)
- Langkah uji: matikan consumer → jalankan publisher → nyalakan consumer
- Hasil yang diamati: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
