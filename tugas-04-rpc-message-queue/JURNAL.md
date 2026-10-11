# Jurnal Proses — Tugas 4

## Jalur yang dipilih
- **Keduanya (RPC dan MQ)**, alasan: studi kasus FoodGo memuat dua kebutuhan berbeda.
  Cek saldo/proses pembayaran butuh jawaban seketika (sinkron → RPC), sedangkan notifikasi
  "pembayaran berhasil" ke kurir tidak boleh membuat modul Pembayaran menunggu (asinkron → MQ).
  Jalur RPC dan MQ dikerjakan penuh supaya perbedaannya bisa dibandingkan langsung.

## Kendala teknis
- **Jalur A (RPC):** saat `client.py` dijalankan sebelum `server.py`, muncul
  `ConnectionRefusedError: [Errno 111] Connection refused`. Solusi: urutan menjalankan harus
  server dulu, baru client.
- **Jalur B (MQ):** *(isi dengan kendala nyata kalian, mis. `docker compose` belum jalan →
  `pika.exceptions.AMQPConnectionError`, port 5672/15672 bentrok, Docker Desktop belum aktif, dll.
  Jika tidak ada kendala, tulis itu.)*
- Fungsi server diberi `time.sleep(2)` sengaja agar waktu tunggu client terlihat jelas
  (±2,00 detik per panggilan), karena tanpa jeda pemanggilan lokal terlalu cepat untuk diamati.

## Hasil uji Jalur A (RPC)
- `cek_saldo('user1')` → `50000`, client menunggu **4,05 detik**.
- `proses_pembayaran('user1', 20000)` → `{'status': 'sukses', 'saldo_akhir': 30000}`, menunggu **4,04 detik**.
- Terminal client **diam/blocking** sampai server membalas → bukti komunikasi sinkron.

### Apa yang terjadi pada request RPC jika server mati di tengah proses?
- **Client dijalankan sebelum server:** client langsung gagal dengan
  `ConnectionRefusedError` karena tidak ada proses yang mendengarkan di port 8000
- **Server dihentikan (Ctrl+C) saat client sedang menunggu:** client tidak mendapat hasil, melainkan `xmlrpc.client.Fault: KeyboardInterrupt` Dispatcher xmlrpc menangkap interupsi di dalam fungsi `cek_saldo` dan mengirimnya sebagai Fault, sehingga log server tetap mencatat status 200. Request tidak diselesaikan dan tidak ada antrean yang menyimpannya, sehingga client harus melakukan ulang sendiri.
- **Kesimpulan:** RPC bersifat sinkron dan terikat erat. Jika server tiba tiba mati atau berhenti maka request akan hilang karena tidak memiliki antrian. ketika client mencoba saat server sedang mati maka request akan langsung gagal.

## Uji "pesan tidak hilang" (khusus Jalur B)
- Langkah uji:
  1. `docker compose up -d`, pastikan consumer **belum** dijalankan (atau dimatikan dengan Ctrl+C).
  2. Jalankan `python publisher.py` 2–3 kali → tiap run mengirim 3 event.
     Publisher tetap selesai tanpa error dan tanpa menunggu kurir (tidak ada blocking).
  3. Buka `http://localhost:15672` → tab *Queues* → `pembayaran_berhasil`:
     kolom **Ready** naik menjadi 2 × jumlah run (mis. 6) ini yang jadi screenshot bukti.
  4. Nyalakan `python consumer.py`.
- Hasil yang diamati: *(isi sesuai hasil nyata kalian. Hasil yang seharusnya muncul: consumer langsung
  mencetak semua event yang tertunda, "Kurir menerima notifikasi pembayaran untuk user1 sejumlah 20000", dst.,
  lalu **Ready** di dashboard turun ke 0.)*

### Ke mana pesan "hilang sementara" tersimpan saat consumer mati?
Pesan tidak hilang, tapi disimpan di dalam queue `pembayaran_berhasil` pada RabbitMQ
(container Docker), bukan di publisher maupun consumer. Karena queue dideklarasikan `durable=True` dan pesan dikirim `delivery_mode=Persistent`, pesan juga ditulis ke disk broker, jadi tetap aman jika RabbitMQ restart. Pesan baru dihapus setelah consumer mengirim `basic_ack`. Karena ack dikirim setelah pemrosesan selesai, jika consumer mati di tengah pemrosesan, pesan dikembalikan ke antrean dan dikirim ulang. Inilah yang membuat publisher dan consumer tidak perlu hidup bersamaan.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md)[cite: 1]. Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai[cite: 1]. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir[cite: 1]. Isi dengan jujur sesuai yang benar-benar kalian lakukan[cite: 2].

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 09 Oktober 2026 | ChatGPT |"Berikan ide langkah pengujian konseptual untuk membuktikan antrean pesan tidak hilang saat consumer RabbitMQ dimatikan." | Menyarankan alur pengujian: matikan consumer terlebih dahulu, jalankan publisher beberapa kali, periksa queue di management dashboard, lalu nyalakan consumer lagi. | Menyusun langkah kerja riil di terminal dengan Docker, memantau metrik antrean Ready di RabbitMQ Management (port 15672), dan memverifikasi data berhasil diproses kembali oleh worker secara mandiri. |
| 10 Oktober 2026 | Claude | "Apa saja poin evaluasi yang perlu diamati saat server RPC dihentikan paksa (Ctrl+C) di tengah proses client?" | Menyarankan untuk meninjau penanganan exception pada dispatcher XML-RPC, status respon HTTP yang tercatat, dan perilaku client ketika request tidak terselesaikan. | Melakukan pengujian langsung dengan menghentikan server.py, mencatat pesan error riil xmlrpc.client.Fault: KeyboardInterrupt, dan menarik kesimpulan terkait sifat stateless/tanpa buffer pada RPC. |
| 11 Oktober 2026 | Gemini | "Bantu buatkan outline struktur jurnal pengujian sistem untuk membandingkan sifat sinkron RPC vs asinkron Message Broker pada FoodGo." | Menyarankan kerangka perbandingan: alasan pemilihan metode, pencatatan kendala urutan start server/client, pengujian kondisi server/consumer down, dan perilaku blocking. | Menggunakan kerangka tersebut sebagai acuan penulisan, lalu mengisi seluruh data teknis, pesan error riil (ConnectionRefusedError), durasi blocking (4,05 detik), dan konfigurasi parameter RabbitMQ berdasarkan hasil praktikum sendiri. |