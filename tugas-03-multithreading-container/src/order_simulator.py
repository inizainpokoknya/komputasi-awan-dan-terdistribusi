"""
Tugas 3 - Simulasi Pesanan Masuk dengan Multithreading

Skeleton ini sengaja belum lengkap. Isi bagian bertanda TODO.
Jangan mengubah nama fungsi (dipakai untuk pengecekan otomatis oleh asisten).
"""
import sys
import threading
import random
import time

NUM_ORDERS = 100        # jumlah pesanan simulasi yang masuk
NUM_WORKERS = 10        # jumlah thread pekerja

# Counter bersama untuk menghitung total pesanan yang berhasil diproses.
# Sengaja rawan race condition jika diakses tanpa proteksi.
processed_count = 0

lock = threading.Lock()
USE_LOCK = "--no-lock" not in sys.argv


def process_order(order_id: int) -> None:
    """Proses satu pesanan. Dipanggil oleh tiap thread pekerja."""
    global processed_count

    # Simulasikan kerja nyata (mis. validasi, hitung total harga)
    time.sleep(random.uniform(0.001, 0.01))

    if USE_LOCK:
        with lock:
            nilai_sekarang = processed_count
            time.sleep(0.001)
            processed_count = nilai_sekarang + 1
    else:
        nilai_sekarang = processed_count
        time.sleep(0.001)
        processed_count = nilai_sekarang + 1


def worker(order_ids: list) -> None:
    """Satu thread pekerja memproses sekumpulan order_id."""
    for order_id in order_ids:
        process_order(order_id)


def main() -> None:
    order_ids = list(range(1, NUM_ORDERS + 1))

    ukuran = NUM_ORDERS // NUM_WORKERS
    threads = []
    for i in range(NUM_WORKERS):
        bagian = order_ids[i * ukuran:(i + 1) * ukuran]
        t = threading.Thread(target=worker, args=(bagian,), name=f"worker-{i + 1}")
        threads.append(t)

    mulai = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    durasi = time.perf_counter() - mulai


    print(f"Mode: {'DENGAN lock' if USE_LOCK else 'TANPA lock'}")
    print(f"Total pesanan diproses: {processed_count} (seharusnya {NUM_ORDERS})")
    print(f"Waktu: {durasi:.3f} detik dengan {NUM_WORKERS} thread")
    if processed_count != NUM_ORDERS:
        print("RACE CONDITION TERDETEKSI - lengkapi TODO 1 & TODO 2 dengan Lock!")


if __name__ == "__main__":
    main()
