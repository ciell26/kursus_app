"""F5: laporan sederhana (hanya membaca data)."""


class Laporan:
    def __init__(self, repo_peserta, repo_kelas, repo_pendaftaran, repo_pembayaran):
        self._peserta = repo_peserta
        self._kelas = repo_kelas
        self._pendaftaran = repo_pendaftaran
        self._pembayaran = repo_pembayaran

    def peserta_per_kelas(self, kelas_id):
        kelas = self._kelas.ambil(kelas_id)
        daftar = self._pendaftaran.filter(
            lambda d: d.kelas_id == kelas_id and d.aktif)
        return kelas, [(d, self._peserta.ambil(d.peserta_id)) for d in daftar]

    def sisa_kuota(self):
        return self._kelas.semua()

    def ringkasan_pendapatan(self):
        semua = self._pembayaran.semua()
        kotor = sum(b.total for b in semua)
        refund = sum(b.jumlah_refund for b in semua)
        return {"jumlah_transaksi": len(semua), "pendapatan_kotor": kotor,
                "total_refund": refund, "pendapatan_bersih": kotor - refund}
