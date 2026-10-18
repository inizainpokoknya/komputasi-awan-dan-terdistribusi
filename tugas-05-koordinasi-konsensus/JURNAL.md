# Jurnal Proses — Tugas 5

## Implementasi Bully
- Kendala saat mengisi TODO 1-4: 
- **TODO 1 :** handler berjalan di thread perkoneksi, sedangkan `start_election()` memblokir kurang lebih 2 detik karena menunggu OK. node juga hars mengirimkan OK ke setiap pengirim ELECTION.
- **TODO 2 :** Awalnya ingin menggunakan `time.sleep(2)` tetapi ketika digunakan selalu menunggu penuh walaupun OK sudah terkirim. Pada akhinya `time.sleep(2)` tidak jadi digunakan dan diganti `threading.Event`. Pada node 5 ELECTION diterima dari banyak node yang menjadikan ELECTION ganda. Flag `election_running` dengan lock digunakan untuk mengatasi ELECTION ganda yang terjadi. 

## Skenario 1: Start normal
- Leader terpilih: Node 5 (ID tertinggi).Node 1 hingga 4 berhasil memperbarui status dan mencatat log Leader sekarang adalah node 5.   
- Log dan Observasi:
    - Node dinyalakan satu per satu secara manual. Karena Node 5 baru aktif sekitar pukul `09:32:20`, Node 4 sempat mendeklarasikan diri sebagai leader sementara pada `09:32:22.129`. Hal ini terjadi karena pesan `ELECTION` dari Node 4 ke Node 5 gagal terkirim saat Node 5 masih dalam keadaan mati. 
    - Setelah Node 5 menyala, ia langsung memulai election. Karena tidak mendapat balasan `OK` dari node mana pun, Node 5 menyatakan dirinya sebagai leader pada `09:32:23.404` lalu mem-broadcast pesan `COORDINATOR`. Merespons pesan tersebut, Node 1 hingga 4 memindahkan status leader mereka dari Node 4 ke Node 5 (proses takeover oleh ID tertinggi).   
    - Pada pukul `09:32:34.277` , seluruh jaringan telah mencapai konsensus bahwa leader adalah Node 5.   
    - Waktu pengiriman pesan antar-node terukur sekitar ±1 detik per pesan (kemungkinan dipengaruhi oleh perilaku delay `localhost` pada sistem Windows). Akibatnya, proses broadcast `COORDINATOR` ke seluruh node memakan waktu total sekitar ±4 detik.   
    - Bukti: Tangkapan layar terminal Node 1 hingga 5 terlampir di dalam folder bukti/ (Skenario 1).   

## Skenario 2: Leader dimatikan
- Leader baru yang terpilih: ...
- Berapa lama waktu sampai leader baru terdeteksi: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 18 Oktober 2026 | Claude | Dari TODO1-4 apa yang harus dilakukan secara garis besar sesuai TODOnya? | TODO 1 menangani pesan ELECTION/OK/COORDINATOR, TODO 2 memulai election dan menunggu OK, TODO 3 mengumumkan diri sebagai leader, TODO 4 memantau leader. Ditambah hubungan antar-TODO dan pertanyaan pemantik untuk diskusi | Kami jadikan bahan brainstorming untuk memahami alur keempat TODO sebelum mengisi kode dan menulis bagian Kendala |
| 18 Oktober 2026 | Claude | Pada TODO 2 terjadi ELECTION ganda karena node 5 bisa menerima banyak ELECTION dari banyak node, apa yang bisa dilakukan agar mencegah ini terjadi? | Pakai flag `election_running` yang dijaga lock: jika sudah ada election berjalan, panggilan `start_election()` berikutnya langsung berhenti. Node tetap harus membalas OK ke setiap pengirim ELECTION, dan flag dikembalikan ke False di blok finally supaya tidak macet bila terjadi error | Dari beberapa ide, kami memilih flag karena paling sederhana, lalu menuliskannya sendiri di awal `start_election()` dan mencobanya langsung pada saat 5 node dijalankan |
| ... | ... | ... | ... | ... |
