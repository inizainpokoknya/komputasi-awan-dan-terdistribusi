# Jurnal Proses — Tugas 3

## Percobaan tanpa Lock
- Hasil `processed_count` yang didapat: 10 dari 100 (tanpa Docker) dan 39 dari 100 (dalam container Docker)
- Kenapa bisa meleset (jelaskan mekanisme race condition dengan kata sendiri): processed_count dibaca, ditambah 1, lalu ditulis kembali lewat 3 langkah yang terpisah. Karena 10 thread berjalan bersamaan beberapa thread membaca nilai lama yang sama sebelum ada yang menuliskan hasilnya. Pada akhirnya semua menulis nilai yang sama, sehingga sebagian penambahan hilang dan total jauh di bawah 100.

## Percobaan dengan Lock
- Hasil `processed_count` setelah perbaikan: Setelah perbaikan hasilnya menjadi 100 dari 100, tanpa Docker maupun dengan container Docker. Lock membuat langkah baca, tambah, dan tulis hanya bisa dijalankan satu thread pada satu waktu.

## Kendala Docker
- Error yang ditemui saat `docker build`/`docker run` dan cara memperbaikinya: 
1. `WSL not installed` pada Docker Desktop: dijalankan `wsl --install` di PowerShell administrator, lalau tinggal restart laptop.
3. `meta.json ... being used by another process`: Docker Desktop belum selesai startup, tunggu sampai berstatus running lalu `docker build` diulang.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 03 Oktober 2026 | Claude | Bagaimana cara install Docker untuk Windows, karena saya sudah coba install tapi tidak bisa masuk ke Docker. Lalu bagaimana cara menghubungkan Docker ke file Python| Untuk install Docker di Windows, aktifkan virtualisasi di BIOS, jalankan wsl --install, lalu pasang Docker Desktop dengan opsi WSL 2 dan buka aplikasinya sampai statusnya "Engine running". Jika tidak bisa masuk, penyebab tersering adalah Docker Desktop belum berjalan, virtualisasi belum aktif, WSL perlu diperbarui (wsl --update). Untuk menghubungkan Python, buat Dockerfile di folder yang sama dengan app.py yang berisi FROM python:3.12-slim, WORKDIR /app, COPY, dan CMD ["python", "app.py"]. Terakhir, jalankan docker build -t python-app . lalu docker run python-app di terminal. | Mengikuti petunjuk cara install yang sudah diberikan, lalu menyambungkan dengan Pyhton yang sudah kita edit |
| 03 Oktober 2026 | Claude | Kenapa disini terjadi error Docker build pada bagian pythonnya dan  error `meta.json` terkunci | Hal ini terjadi karena placeholder di Dockerfile belum diganti. Untuk meta.json, disarankan menunggu Docker Desktop selesai start-up lalu mengulang build | Kami mengganti placeholder menjadi `python:3.12-slim` dan `CMD ["python3", "src/order_simulator.py"]`, menunggu Docker siap, lalu build berhasil |
|  03 Oktober 2026 | Claude | Mengunggah `order_simulator.py` apakah ada contoh yang cocok untuk TODO dalam `order_simulator.py`| Konsep race condition pada `processed_count += 1`, lalu memberi contoh isi TODO 1 (`threading.Lock()`), TODO 2 (increment tanpa lock dan dengan `with lock:`), TODO 3 (pembagian pesanan ke 10 thread dengan slicing `order_ids[i::NUM_WORKERS]`) | Contoh kode dari AI dipakai sebagai acuan untuk TODO 1-3, lalu kita modifikasi:mengganti nama variabel, mengubah pembagian pesanan dari slicing step ke blok berurutan, menambahkan opsi `--no-lock` agar kedua mode bisa diuji dari command line, memakai `sleep(0.001)` di antara baca dan tulis untuk memunculkan race condition, serta menambahkan pengukuran waktu. |