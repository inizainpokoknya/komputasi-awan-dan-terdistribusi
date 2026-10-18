# Jurnal Proses — Tugas 5

## Implementasi Bully
- Kendala saat mengisi TODO 1-4: 
- **TODO 1 : handler berjalan di thread perkoneksi, sedangkan `start_election()` memblokir kurang lebih 2 detik karena menunggu OK. node juga hars mengirimkan OK ke setiap pengirim ELECTION.
- **TODO 2 : Awalnya ingin menggunakan `time.sleep(2)` tetapi ketika digunakan selalu menunggu penuh walaupun OK sudah terkirim. Pada akhinya `time.sleep(2)` tidak jadi digunakan dan diganti `threading.Event`. Pada node 5 ELECTION diterima dari banyak node yang menjadikan ELECTION ganda. Flag `election_running` dengan lock digunakan untuk mengatasi ELECTION ganda yang terjadi. 

## Skenario 1: Start normal
- Leader yang terpilih: ...
- Log/observasi: ...

## Skenario 2: Leader dimatikan
- Leader baru yang terpilih: ...
- Berapa lama waktu sampai leader baru terdeteksi: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
