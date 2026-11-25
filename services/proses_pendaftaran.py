"""F2: pendaftaran peserta (AB1-AB4)."""
from exceptions.errors import KuotaPenuhError, PendaftaranGandaError
from models import Pendaftaran
from services.base_proses import ProsesBase


class ProsesPendaftaran(ProsesBase):
    def __init__(self, repo_pendaftaran, repo_kelas, repo_peserta):
        super().__init__(repo_pendaftaran, repo_kelas)
        self._repo_peserta = repo_peserta

    def validasi(self, peserta_id, kelas_id):
        peserta = self._repo_peserta.ambil(peserta_id)  # AB1
        kelas = self._repo_kelas.ambil(kelas_id)  # AB1
        ganda = self._repo_pendaftaran.filter(
            lambda d: d.peserta_id == peserta_id
            and d.kelas_id == kelas_id and d.aktif)
        if ganda:  # AB2
            raise PendaftaranGandaError(
                f"{peserta.nama} sudah terdaftar aktif di kelas {kelas.nama}.")
        if not kelas.ada_kuota():  # AB3
            raise KuotaPenuhError(f"Kuota kelas {kelas.nama} sudah penuh.")
        return {"peserta": peserta, "kelas": kelas}

    def proses(self, konteks):  # AB4
        kelas = konteks["kelas"]
        kelas.kurangi_kuota()
        pendaftaran = Pendaftaran(self._repo_pendaftaran.id_berikutnya(),
                                  konteks["peserta"].id, kelas.id)
        return {"pendaftaran": pendaftaran, "kelas": kelas}

    def simpan(self, hasil):
        self._repo_pendaftaran.tambah(hasil["pendaftaran"])
        self._repo_kelas.perbarui(hasil["kelas"])

    def _pesan(self, hasil):
        return (f"Pendaftaran {hasil['pendaftaran'].id} dibuat "
                f"({hasil['pendaftaran'].status}). Sisa kuota {hasil['kelas'].kuota_tersisa}.")
