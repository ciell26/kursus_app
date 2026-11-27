"""F4: pembatalan dan refund (AB8-AB9)."""
from exceptions.errors import DataTidakDitemukanError, StatusTidakValidError
from models import Pendaftaran
from services.base_proses import ProsesBase


class ProsesPembatalan(ProsesBase):
    PERSEN_REFUND = 80

    def __init__(self, repo_pendaftaran, repo_kelas, repo_pembayaran):
        super().__init__(repo_pendaftaran, repo_kelas)
        self._repo_pembayaran = repo_pembayaran

    def validasi(self, pendaftaran_id):
        pendaftaran = self._repo_pendaftaran.ambil(pendaftaran_id)
        if pendaftaran.status not in (Pendaftaran.MENUNGGU, Pendaftaran.LUNAS):  # AB8
            raise StatusTidakValidError(
                f"Pembatalan hanya untuk status {Pendaftaran.MENUNGGU} atau "
                f"{Pendaftaran.LUNAS}, status sekarang {pendaftaran.status}.")
        kelas = self._repo_kelas.ambil(pendaftaran.kelas_id)
        pembayaran = None
        if pendaftaran.status == Pendaftaran.LUNAS:
            ditemukan = self._repo_pembayaran.filter(
                lambda b: b.pendaftaran_id == pendaftaran.id)
            if not ditemukan:
                raise DataTidakDitemukanError(
                    f"Data pembayaran untuk {pendaftaran.id} tidak ditemukan.")
            pembayaran = ditemukan[0]
        return {"pendaftaran": pendaftaran, "kelas": kelas, "pembayaran": pembayaran}

    def proses(self, konteks):
        pembayaran = konteks["pembayaran"]
        refund = 0
        if pembayaran is not None:  # AB9
            refund = pembayaran.biaya_kelas * self.PERSEN_REFUND // 100
            pembayaran.tandai_refund(refund)
        konteks["pendaftaran"].batalkan()
        konteks["kelas"].kembalikan_kuota()  # AB8
        konteks["refund"] = refund
        return konteks

    def simpan(self, hasil):
        self._repo_pendaftaran.perbarui(hasil["pendaftaran"])
        self._repo_kelas.perbarui(hasil["kelas"])
        if hasil["pembayaran"] is not None:
            self._repo_pembayaran.perbarui(hasil["pembayaran"])

    def _pesan(self, hasil):
        return (f"Pendaftaran {hasil['pendaftaran'].id} dibatalkan. Kuota kembali. "
                f"Refund: Rp{hasil['refund']:,}.").replace(",", ".")
