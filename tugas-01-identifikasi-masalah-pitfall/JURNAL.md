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


## Diskusi Untuk Latency is Zero [19 Sep 2026]
- Peserta: [Zain Ahmad Suraiban, Wirajalu, Mujammad Rohman Azizi]
- Poin-Poin:
1. Awalnya kami bingung membedakan gejala "tidak ada timeout" ini masuk ke Network is Reliable atau Latency is Zero. Setelah debat singkat, kami sepakat bahwa ketiadaan timeout adalah manifestasi teknis dari asumsi bahwa "waktu tunggu = 0". Kalau mereka sadar latensi itu ada, pasti mereka pasang timeout.
2. Zain menekankan bahwa dampak terbesarnya bukan sekadar "lambat", tapi thread exhaustion. Ini poin krusial yang harus ditulis di bagian dampak konkret.
3. Anam mengingatkan jangan lupa bahas false positive di trade-off, karena timeout terlalu agresif bisa bikin user kena charge ganda kalau tidak idempoten.
- Perbedaan pendapat: Sempat ada perbedaan pandangan mengenai angka timeout. Azizi menyarankan 10 detik agar aman, Zain berpendapat 3-5 detik lebih realistis untuk UX food delivery. Akhirnya kompromi di "2-5 detik" sebagai range yang bergantung pada SLA masing-masing service.
## [20 Sept 2026]
- Poin diskusi:
1. Finalisasi teks analisis. Memastikan bahasa tidak terlalu textbook, tapi tetap elegan dan menunjukkan pemahaman mendalam tentang mekanisme kegagalan.
2. Cross-check dengan jurnal Muhammad (The Network is Reliable) agar tidak tumpang tindih. Poin retry/backoff sudah diambil Azizi, jadi di bagian solusi Latency is Zero ini fokus murni pada Strict Timeout dan Circuit Breaker sebagai pelengkap.


| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 19 Sep 2026 | Qwen | Based on the FoodGo scenario where the order module calls the payment module without a timeout, explain the failure mechanism of thread exhaustion caused by the 'latency is zero' assumption. Also, discuss the trade-offs of implementing strict timeouts. | The AI explained the concept of blocking I/O, thread starvation, and the risk of false positives when using timeouts. It also highlighted the necessity of idempotency keys to mitigate these trade-offs. | Extracted the core concepts (thread starvation & false positives) and rewrote them in my own narrative, directly linking them to the "server crash" and "slow application" symptoms in the FoodGo scenario. Did not copy the AI's explanation verbatim. The specific timeout values (2-5s) and the pairing with Circuit Breakers were derived from group discussion, not AI suggestions. |
| 20 Sep 2026 | ChatGPT | Based on the FoodGo scenario where the order module calls the payment module without a timeout, explain the failure mechanism of thread exhaustion caused by the 'latency is zero' assumption. Also, discuss the trade-offs of implementing strict timeouts. | The AI explained that without a timeout, requests waiting for an unresponsive payment service can occupy threads for an extended period and eventually cause thread exhaustion. It suggested using strict timeouts together with Circuit Breaker to prevent cascading failures and improve system responsiveness. | I used the explanation as a conceptual reference, then reorganized it into my own analysis of the FoodGo case. The discussion was connected to the symptoms of slow application performance and possible server crashes. The final explanation, structure, and examples were written independently based on our group discussion and understanding of the system. |
| 20 Sep 2026 | Gemini | Based on the FoodGo scenario where the order module calls the payment module without a timeout, explain the failure mechanism of thread exhaustion caused by the 'latency is zero' assumption. Also, discuss the trade-offs of implementing strict timeouts. | The AI provided a structured breakdown of the "latency is zero" fallacy, detailing how synchronous blocking I/O depletes the server's connection pool. For trade-offs, it contrasted system resilience (failing fast) against business impact (dropped orders due to premature timeouts) and suggested asynchronous event-driven queues as a long-term fix. | I used the architectural breakdown of connection pool depletion to structure the technical analysis section of our report. The business trade-offs (resilience vs. revenue impact) were integrated into our group's evaluation. The text was entirely rewritten in my own words to focus specifically on the FoodGo architecture, substituting the AI's generic examples with our own sequence diagrams. |


## Diskusi Untuk Topology Doesn't Change & Single Point of Failure (SPOF) [19 Sep 2026]
- Peserta: [Zain Ahmad Suraiban, Wirajalu, Mujammad Rohman Azizi, Rochmatul Choirul Anam]
- Poin Diskusi:
1. Anam dan Wirajalu fokus pada gejala "crash total" dan "restart manual". Kami mengaitkannya dengan fallacy Topology Doesn't Change karena tim FoodGo seolah-olah percaya server mereka abadi dan tidak butuh pasangan (redundancy).
2. Wirajalu menekankan bahwa masalah utamanya bukan hanya jumlah server, tapi sifatnya yang monolitik. Semua telur dalam satu keranjang.
3. Zain memberikan masukan agar solusi tidak hanya "tambah server", tapi harus ada mekanisme health check dan auto-recovery agar tidak tergantung pada manusia.
- Perbedaan pendapat: Sempat debat apakah solusinya langsung ke Microservices atau cukup Horizontal Scaling pada monolit. Akhirnya kami sepakat mengusulkan Redundansi Instans dulu sebagai langkah awal yang lebih realistis sebelum memecah kode menjadi microservices penuh, karena perubahan kode monolit butuh waktu lama.
- Review Silang: [Zain Ahmad Suraiban] mengomentari analisis [Rochmatul Choirul Anam & Wirajalu]: Poin tentang self-healing sangat penting. Saran: pastikan di bagian trade-off disebutkan tentang tantangan konsistensi data antar instans, karena ini sering jadi jebakan saat pertama kali menerapkan sistem terdistribusi.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 21 Sep 2026 | Qwen | Jelaskan risiko single-point-of-failure pada arsitektur monolitik seperti FoodGo. Apa saja solusi desain untuk redundansi dan apa trade-off utamanya terkait konsistensi data? | AI menguraikan manfaat redundansi aktif-aktif, load balancing, dan orkestrasi otomatis. AI juga menyoroti bahwa trade-off utamanya adalah meningkatnya kompleksitas dalam menjaga konsistensi data di banyak node serta biaya infrastruktur yang lebih tinggi. | Kami menggunakan kerangka dari AI untuk menyusun argumen tentang "Total Service Outage". Kami memperhalus penjelasan dampak "restart manual" agar terdengar lebih kritis bagi bisnis. Penyebutan spesifik tentang "distributed locking" sebagai tantangan konsistensi ditambahkan berdasarkan diskusi kelompok, sementara konsep inti redundansi berasal dari brainstorming AI.
 |
