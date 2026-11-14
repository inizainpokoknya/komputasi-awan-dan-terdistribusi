# Tugas 7 (Pekan 7) — Konsistensi Data

**Materi terkait:** Data-Centric Consistency (Sequential, Eventual), Client-Centric Consistency.

## Studi Kasus

Data saldo *e-wallet* pelanggan FoodGo berbeda antara server wilayah **Jakarta** dan **Bandung** karena replikasi antar server berjalan lambat. Contoh kasus nyata: pelanggan top-up saldo lewat server Jakarta, lalu dalam hitungan detik memesan makanan lewat aplikasi yang tersambung ke server Bandung — saldo belum ter-update, transaksi ditolak padahal saldo sebenarnya cukup.

## Tugas Kelompok

### Bagian 1 — Analisis (wajib)

1. Tentukan: apakah kasus ini **membutuhkan Sequential Consistency** (semua replika melihat urutan operasi yang sama) atau **cukup Eventual Consistency** (replika akan konsisten "pada akhirnya", boleh sementara berbeda)? Berikan argumen berbasis dampak bisnis (mis. kasus saldo *e-wallet* jauh lebih sensitif dibanding kasus "jumlah like" di media sosial).

Eventual Consistency saja tidak cukup, karena saldo e-wallet membutuhkan Sequential Consistency untuk operasi yang mengubah saldo (top-up, bayar, refund), sedangkan Eventual Consistency hanya layak untuk data non-kritis.
 
Argumen berbasis dampak bisnis:
 
- **Terkait uang:** Saldo stale membuat transaksi ditolak padahal saldo cukup (pesanan hilang, pelanggan kesal, beban CS naik). Sebaliknya, replika yang masih melihat saldo lama bisa membiarkan saldo dipakai dua kali (*double spending*, kerugian uang).
- **Urutan operasi menentukan hasil:** Top-up 50rb lalu bayar 40rb berbeda hasilnya dengan bayar dulu lalu top-up. Semua replika harus menerapkan urutan yang sama.
- **Biaya sepadan:** Tambahan latensi puluhan sampai ratusan milidetik jauh lebih murah daripada kehilangan pesanan dan kepercayaan pelanggan.
**Mengapa saldo e-wallet jauh lebih sensitif daripada "jumlah like" di media sosial:**
 
| Aspek | Saldo e-wallet | Jumlah like |
|---|---|---|
| Sifat data | Nilai uang nyata milik pelanggan | Angka popularitas, tidak punya nilai uang |
| Kebenaran data | Harus tepat (selisih Rp1 pun salah) | Boleh perkiraan (1.203 atau 1.205 sama saja bagi pembaca) |
| Keputusan yang bergantung pada data | Sistem mengambil keputusan dari angka ini: pembayaran diterima atau ditolak | Hanya ditampilkan, tidak memicu keputusan penting |
| Akibat jika stale | Pesanan batal, saldo terpakai dua kali, perlu refund dan penelusuran manual | Tidak ada akibat, angka menyusul sendiri beberapa detik kemudian |
| Bisa diperbaiki diam-diam? | Tidak. Pelanggan sudah terlanjur mengalami penolakan atau kehilangan uang | Ya, tidak ada yang menyadari |
| Dampak ke kepercayaan | Satu kejadian cukup membuat pelanggan meninggalkan aplikasi, dan ada risiko komplain serta regulasi uang elektronik | Hampir tidak ada |
| Urutan operasi | Penting (top-up lalu bayar tidak sama dengan bayar lalu top-up) | Tidak penting, like hanya dijumlahkan |
 
Pada saldo kesalahan kecil dan sementara pun berubah menjadi kerugian nyata yang tidak bisa ditarik kembali, sedangkan pada jumlah like kesalahan sementara akan hilang dengan sendirinya tanpa kerugian. Karena itu like cukup memakai Eventual Consistency, tetapi saldo tidak.
 
| Data FoodGo | Model |
|---|---|
| Saldo e-wallet, status pembayaran | Sequential (write terurut) |
| Rating, jumlah ulasan, menu, lokasi driver | Eventual |

2. Jika kalian menyimpulkan Eventual Consistency saja **tidak cukup** untuk skenario ini, usulkan pendekatan **Client-Centric Consistency** yang relevan (mis. *Read-Your-Writes*: pelanggan yang baru top-up harus selalu melihat saldo terbarunya sendiri, walau replika lain belum sinkron).
3. Gambarkan **diagram alir urutan (sequence diagram)** yang menunjukkan operasi read/write antara pelanggan, server Jakarta, server Bandung, dan proses replikasi — untuk skenario **tanpa** jaminan konsistensi (bug terjadi) DAN skenario **dengan** solusi yang kalian usulkan (bug teratasi). Pakai Mermaid (`sequenceDiagram`) di `README.md` — lihat contoh cara pakai di Tugas 2.

### Bagian 2 — Simulasi (opsional, nilai tambah)

Skeleton `src/replica_simulation.py` mensimulasikan dua replika (Jakarta & Bandung) dengan delay replikasi buatan. Lengkapi TODO untuk:
1. Menunjukkan kondisi **inconsistent read** (replika Bandung masih menunjukkan saldo lama walau Jakarta sudah update).
2. Mengimplementasikan mekanisme **Read-Your-Writes** sederhana (mis. dengan version/timestamp per client) yang memperbaiki masalah tersebut.

```bash
python3 src/replica_simulation.py
```

## Struktur Submission

```
tugas-07-konsistensi-data/
├── README.md      # Analisis konsistensi + sequence diagram Mermaid
├── JURNAL.md
├── src/            # (opsional) simulasi replikasi
└── bukti/          # (jika mengerjakan simulasi) output program
```

## Rubrik Penilaian (Tugas 7)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Ketepatan pemilihan model konsistensi | 30% | Argumen berbasis dampak bisnis nyata, bukan hafalan definisi |
| Kualitas sequence diagram | 30% | Menunjukkan jelas titik kegagalan & titik perbaikan |
| Usulan solusi client-centric | 25% | Solusi konkret dan dapat diimplementasikan (bukan wacana abstrak) |
| Proses & kontribusi kelompok | 15% | `JURNAL.md`, commit history (+ bonus jika simulasi dikerjakan) |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya konsep umum consistency model ke AI untuk brainstorming; **tidak boleh** meminta AI menuliskan analisis akhir/sequence diagram atau isi `# TODO` di `src/replica_simulation.py` yang tinggal ditempel. Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- Sebagai bukti pemahaman konsep (bukan hafalan jawaban skenario FoodGo saja), `README.md` wajib menyertakan **satu skenario tambahan** yang kalian buat sendiri (mis. kasus lain di aplikasi ojek online) dan menentukan model konsistensi yang tepat untuk skenario tambahan tersebut.
