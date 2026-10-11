"""
Tugas 4 - Jalur A: RPC Client (simulasi modul Pesanan)
Jalankan server.py di terminal lain terlebih dahulu.
"""

import xmlrpc.client
import time


def main():
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000")

    print("Memanggil cek_saldo('user1') ... menunggu respons sinkron")
    start = time.time()
    saldo = proxy.cek_saldo("user1")
    print(f"Saldo user1: {saldo} (waktu tunggu: {time.time() - start:.2f} detik)")
    #         (buktikan client BENAR-BENAR menunggu sampai server membalas)

    print("Memanggil proses_pembayaran('user1', 20000) ...")
    start = time.time()
    hasil = proxy.proses_pembayaran("user1", 20000)
    print(f"Hasil: {hasil} (waktu tunggu: {time.time() - start:.2f} detik)")


if __name__ == "__main__":
    main()
