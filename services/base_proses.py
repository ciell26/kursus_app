"""ProsesBase: kerangka Template Method untuk tiga proses bisnis."""
from abc import ABC, abstractmethod
from datetime import datetime


class ProsesBase(ABC):
    """Urutan tetap: validasi -> proses -> simpan -> log."""

    def __init__(self, repo_pendaftaran, repo_kelas):
        self._repo_pendaftaran = repo_pendaftaran
        self._repo_kelas = repo_kelas
        self.riwayat = []
        self.pesan_terakhir = ""

    def jalankan(self, **data):
        konteks = self.validasi(**data)
        hasil = self.proses(konteks)
        self.simpan(hasil)
        self.log(hasil)
        return hasil

    @abstractmethod
    def validasi(self, **data):
        """Memeriksa aturan bisnis; mengembalikan konteks untuk proses()."""

    @abstractmethod
    def proses(self, konteks):
        """Mengubah objek di memori; mengembalikan hasil."""

    @abstractmethod
    def simpan(self, hasil):
        """Menulis perubahan lewat repository."""

    @abstractmethod
    def _pesan(self, hasil):
        """Pesan ringkas hasil proses."""

    def log(self, hasil):
        self.pesan_terakhir = self._pesan(hasil)
        self.riwayat.append(
            f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {self.pesan_terakhir}")
