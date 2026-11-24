"""MetodePembayaran (abstrak) -> Tunai, Transfer, EWallet (AB6)."""
from abc import ABC, abstractmethod


class MetodePembayaran(ABC):
    NAMA = ""

    @abstractmethod
    def hitung_biaya_admin(self, biaya_kelas):
        """Biaya administrasi metode; wajib diisi subclass."""


class Tunai(MetodePembayaran):
    NAMA = "tunai"

    def hitung_biaya_admin(self, biaya_kelas):
        return 0


class Transfer(MetodePembayaran):
    NAMA = "transfer"

    def hitung_biaya_admin(self, biaya_kelas):
        return 2500


class EWallet(MetodePembayaran):
    NAMA = "ewallet"

    def hitung_biaya_admin(self, biaya_kelas):
        return biaya_kelas * 2 // 100  # 2% dari biaya kelas


def metode_default():
    """Daftar metode yang disuntikkan ke ProsesPembayaran."""
    return {m.NAMA: m for m in (Tunai(), Transfer(), EWallet())}
