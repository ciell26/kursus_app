"""F3: pembayaran (AB5-AB7)."""
from exceptions.errors import PembayaranGagalError, StatusTidakValidError
from models import Pembayaran, Pendaftaran
from services.base_proses import ProsesBase


class ProsesPembayaran(ProsesBase):
    def __init__(self, repo_pendaftaran, repo_kelas, repo_pembayaran, daftar_metode):
        super().__init__(repo_pendaftaran, repo_kelas)
        self._repo_pembayaran = repo_pembayaran
        self._daftar_metode = daftar_metode

    def validasi(self, pendaftaran_id, metode):
        pendaftaran = self._repo_pendaftaran.ambil(pendaftaran_id)
        if pendaftaran.status != Pendaftaran.MENUNGGU:  # AB7
            raise StatusTidakValidError(
                f"Pembayaran hanya untuk status {Pendaftaran.MENUNGGU}, "
                f"status sekarang {pendaftaran.status}.")
        metode_obj = self._daftar_metode.get(str(metode).strip().lower())
        if metode_obj is None:
            raise PembayaranGagalError(
                f"Metode '{metode}' tidak dikenal. Pilihan: "
                f"{', '.join(self._daftar_metode)}.")
        kelas = self._repo_kelas.ambil(pendaftaran.kelas_id)
        return {"pendaftaran": pendaftaran, "kelas": kelas, "metode": metode_obj}

    def proses(self, konteks):
        kelas, metode = konteks["kelas"], konteks["metode"]
        biaya_kelas = kelas.hitung_biaya()
        biaya_admin = metode.hitung_biaya_admin(biaya_kelas)
        pembayaran = Pembayaran(self._repo_pembayaran.id_berikutnya(),
                                konteks["pendaftaran"].id, metode.NAMA,
                                biaya_kelas, biaya_admin,
                                biaya_kelas + biaya_admin)  # AB7
        konteks["pendaftaran"].tandai_lunas()
        return {"pendaftaran": konteks["pendaftaran"], "pembayaran": pembayaran}

    def simpan(self, hasil):
        self._repo_pembayaran.tambah(hasil["pembayaran"])
        self._repo_pendaftaran.perbarui(hasil["pendaftaran"])

    def _pesan(self, hasil):
        p = hasil["pembayaran"]
        return (f"Pembayaran {p.id} berhasil via {p.metode}: total "
                f"Rp{p.total:,}. Pendaftaran {hasil['pendaftaran'].id} LUNAS."
                ).replace(",", ".")
