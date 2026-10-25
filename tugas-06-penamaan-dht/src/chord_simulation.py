"""
Tugas 6 - Simulasi Chord DHT (single-process, tanpa jaringan sungguhan)

Fungsi hashing & struktur data ring sudah disediakan.
Lengkapi TODO untuk lookup(), join(), dan leave().
"""

import hashlib

M_BITS = 8               # ruang identifier 0..255 (disederhanakan dari Chord asli yang pakai 160-bit)
RING_SIZE = 2 ** M_BITS


def hash_id(key: str) -> int:
    """Hash string (ID node atau ID kurir) ke ruang identifier 0..RING_SIZE-1."""
    digest = hashlib.sha1(key.encode()).digest()
    return int.from_bytes(digest, "big") % RING_SIZE


class ChordRing:
    def __init__(self):
        # node_id (hasil hash) -> alamat IP node tersebut
        self.nodes: dict[int, str] = {}
        # key kurir (hasil hash) -> IP kurir yang disimpan node yang bertanggung jawab
        self.data: dict[int, tuple[str, str]] = {}  # hash -> (kurir_id, ip_kurir)

    def join(self, node_name: str, node_ip: str):
        """Tambahkan node baru ke ring. Pindahkan data yang seharusnya
        menjadi tanggung jawab node baru ini dari successor lamanya."""
        node_id = hash_id(node_name)

        # TODO 1: tambahkan node_id -> node_ip ke self.nodes.
        self.nodes[node_id] = node_ip
        # TODO 2: cari successor LAMA dari node_id ini (successor sebelum node
        # baru bergabung, gunakan find_successor() dengan node_id INI dikecualikan
        # dulu dari self.nodes saat mencari).
        lain = [n for n in self.nodes if n != node_id]
        succ_lama = None
        if lain:
            lebih_besar = [n for n in lain if n >= node_id]
            succ_lama = min(lebih_besar) if lebih_besar else min(lain)
        # TODO 3: pindahkan semua key di self.data yang seharusnya menjadi
        # tanggung jawab node baru (key dengan hash <= node_id, tapi masih
        # dipegang oleh successor lama) ke bawah tanggung jawab node baru.
        # (Untuk simulasi sederhana, cukup print log siapa mengambil alih apa -
        # tidak perlu benar-benar memindahkan struktur data kompleks.)
        print(f"Node '{node_name}' (id={node_id}) bergabung, alamat {node_ip}, successor lama = {succ_lama}")
        if succ_lama is not None:
            for key_hash, (kurir_id, _ip) in sorted(self.data.items()):
                if self.find_successor(key_hash) == node_id:
                    print(f"  PINDAH: {kurir_id} (hash={key_hash}) dari node id={succ_lama} -> node id={node_id}")

    def leave(self, node_name: str):
        """Keluarkan sebuah node dari ring. Data yang dipegangnya harus
        berpindah ke successor-nya."""
        node_id = hash_id(node_name)

        # TODO 4: hapus node_id dari self.nodes.
        if node_id not in self.nodes:
            print(f"Node '{node_name}' (id={node_id}) tidak ada di ring")
            return
        milik_node = [k for k in sorted(self.data) if self.find_successor(k) == node_id]
        del self.nodes[node_id]
        # TODO 5: cari successor BARU untuk tiap key yang tadinya dipegang
        # node ini, pindahkan ke successor tersebut.
        print(f"Node '{node_name}' (id={node_id}) keluar dari ring")
        for key_hash in milik_node:
            if not self.nodes:
                print(f"  {self.data[key_hash][0]} (hash={key_hash}) hilang, ring kosong")
                continue
            succ_baru = self.find_successor(key_hash)
            print(f"  PINDAH: {self.data[key_hash][0]} (hash={key_hash}) dari node id={node_id} -> node id={succ_baru}")

    def find_successor(self, key_hash: int) -> int:
        """Cari node_id dengan nilai hash TERKECIL yang >= key_hash
        (successor menurut aturan Chord). Jika tidak ada, wrap-around
        ke node dengan hash terkecil di ring (karena ring melingkar)."""
        # TODO 6: implementasikan logika successor di atas menggunakan
        # self.nodes.keys(). Kembalikan node_id (bukan IP).
        kandidat = [nid for nid in self.nodes.keys() if nid >= key_hash]
        if kandidat:
            return min(kandidat)
        return min(self.nodes.keys())

    def register_kurir(self, kurir_id: str, ip_kurir: str):
        """Simpan mapping ID Kurir -> IP di node yang bertanggung jawab."""
        key_hash = hash_id(kurir_id)
        # TODO 7: panggil find_successor(key_hash) untuk menentukan node
        # penanggung jawab, lalu simpan (kurir_id, ip_kurir) ke self.data[key_hash].
        node_id = self.find_successor(key_hash)
        self.data[key_hash] = (kurir_id, ip_kurir)

    def lookup(self, kurir_id: str) -> str | None:
        """Cari alamat IP terkini untuk sebuah ID Kurir."""
        key_hash = hash_id(kurir_id)
        # TODO 8: gunakan find_successor(key_hash) untuk menemukan node
        # penanggung jawab, lalu kembalikan ip_kurir dari self.data jika ada.
        node_id = self.find_successor(key_hash)
        entry = self.data.get(key_hash)
        return entry[1] if entry else None


def main():
    ring = ChordRing()

    # Skenario awal: 4 node bergabung
    ring.join("node-jakarta-1", "10.0.0.1")
    ring.join("node-jakarta-2", "10.0.0.2")
    ring.join("node-bandung-1", "10.0.0.3")
    ring.join("node-surabaya-1", "10.0.0.4")

    # Daftarkan beberapa kurir
    ring.register_kurir("kurir-001", "192.168.1.10")
    ring.register_kurir("kurir-002", "192.168.1.11")
    ring.register_kurir("kurir-003", "192.168.1.12")

    ring.register_kurir("kurir-012", "192.168.1.13")  # Pindah ke node-medan-1 saat join
    ring.register_kurir("kurir-005", "192.168.1.14")  # Pindah ke node-bandung-1 saat leave

    print("\n--- Lookup sebelum perubahan topologi ---")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))

    print("\n--- Node baru bergabung ---")
    ring.join("node-medan-1", "10.0.0.5")
    print("kurir-001 ->", ring.lookup("kurir-001"))

    print("\n--- Sebuah node keluar ---")
    ring.leave("node-jakarta-1")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))


if __name__ == "__main__":
    main()
