"""
Tugas 4 - Jalur A: RPC Server (simulasi modul Pembayaran)
Memakai xmlrpc.server dari Python standard library - tidak perlu install apa pun.
"""
import time
from xmlrpc.server import SimpleXMLRPCServer

# Simulasi "database" saldo user
saldo_user = {
    "user1": 50000,
    "user2": 120000,
}


def cek_saldo(user_id: str) -> float:
    """Kembalikan saldo user_id saat ini."""
    print(f"[SERVER] cek_saldo dipanggil untuk {user_id}")
    time.sleep(DELAY_DETIK)
    return saldo_user.get(user_id, 0)
    # Jika user_id tidak ada, putuskan sendiri perilakunya (mis. return 0 atau raise error)
    # dan jelaskan keputusan ini di README.md.


def proses_pembayaran(user_id: str, jumlah: float) -> dict:
    """Kurangi saldo user sejumlah `jumlah`. Kembalikan status hasil."""
    print(f"[SERVER] proses_pembayaran: {user_id} sebesar {jumlah}")
    time.sleep(DELAY_DETIK)
    if user_id not in saldo_user:
        return {"status": "gagal", "alasan": "user tidak ditemukan", "saldo_akhir": 0}
    if jumlah <= 0:
        return {"status": "gagal", "alasan": "jumlah tidak valid",
                "saldo_akhir": saldo_user[user_id]}
    if saldo_user[user_id] < jumlah:
        return {"status": "gagal", "alasan": "saldo tidak cukup",
                "saldo_akhir": saldo_user[user_id]}
    saldo_user[user_id] -= jumlah
    return {"status": "sukses", "saldo_akhir": saldo_user[user_id]}
    # dict berisi minimal {"status": "sukses"/"gagal", "saldo_akhir": ...}


def main():
    server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
    server.register_function(cek_saldo, "cek_saldo")
    server.register_function(proses_pembayaran, "proses_pembayaran")
    print("RPC server modul Pembayaran berjalan di port 8000...")
    server.serve_forever()


if __name__ == "__main__":
    main()
