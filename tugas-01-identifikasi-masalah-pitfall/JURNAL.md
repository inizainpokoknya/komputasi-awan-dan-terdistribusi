# Jurnal Proses — Tugas 1

> Isi jurnal ini selama proses diskusi berlangsung, bukan ditulis ulang rapi di akhir. Tulis dengan gaya bebas — poin diskusi, kebuntuan, perubahan pikiran.

## [Tanggal 19 September 2026]
- Peserta: [Muhammad Rohman Azizi, Zain Ahmad Suraiban, Rochmatul Choirul Anam]
- Poin diskusi: Pitfall yang ditambahkan adalah "The Netrwork is Reliable", Karena berdasarkan gejalanya mengarah ke pitfall "The Network is Reliable"
- Perbedaan pendapat (jika ada): Belum ada

## [Tanggal diskusi 2]
- ...

## Review Silang
- [Rochmatul Choirul Anam] mengomentari analisis [Muhammad rohman Azizi]: Gunakan retry dan timeout dibanding timeout saja, karena tanpa retry tingkat kegagalan user lebih tinggi.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 19 Sep 2026 | Calude AI | Dari Gejala Tim menemukan bahwa kode mereka menulis asumsi seperti # network is always reliable, no need for retry dan tidak ada timeout sama sekali pada pemanggilan antar service (modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu). Saya mengidentifikasi kalau gejala ini termasuk pitfall "The Network is Reliable" karena dari yang saya asumsikan tidak ada 100% jaringan yang andal. Apa dampak dari pitfall, Solusi konsep, dan trade off apa yang memungkinkan untuk pitfall dan gejala tersebut? | Terapkan retry otomatis (maksimal 3x) dengan jeda meningkat (exponential backoff) dan variasi acak (jitter), khusus untuk operasi idempoten seperti cek status bukan untuk operasi seperti charge kartu tanpa idempotency key. | Mengidentifikasi lagi bagian kekeliruan serta poin poin yang sudah diberikan oleh AI, lalu diolah dengan bahasa sendiri. |
