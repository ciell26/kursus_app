"""Kelas (abstrak) -> KelasReguler, KelasIntensif, KelasOnline."""
from abc import ABC, abstractmethod

from exceptions.errors import InputTidakValidError, KuotaPenuhError
from utils.mixins import SerializableMixin
from utils.validator import angka_positif, wajib_teks


class Kelas(ABC, SerializableMixin):
    FIELDS = ("id", "jenis", "nama", "tarif_dasar", "kuota_maks",
              "kuota_tersisa", "instruktur_id")
    JENIS = ""
    _registry = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.JENIS:
            Kelas._registry[cls.JENIS] = cls

    def __init__(self, id, nama, tarif_dasar, kuota_maks,
                 kuota_tersisa=None, instruktur_id=None):
        self._id = id
        self._nama = wajib_teks(nama, "Nama kelas")
        self._tarif_dasar = angka_positif(tarif_dasar, "Tarif dasar")
        self._kuota_maks = angka_positif(kuota_maks, "Kuota")
        if kuota_tersisa is None:
            kuota_tersisa = self._kuota_maks
        if not 0 <= int(kuota_tersisa) <= self._kuota_maks:
            raise InputTidakValidError("Kuota tersisa di luar rentang.")
        self._kuota_tersisa = int(kuota_tersisa)
        self._instruktur_id = instruktur_id

    @property
    def id(self):
        return self._id

    @property
    def jenis(self):
        return self.JENIS

    @property
    def nama(self):
        return self._nama

    @property
    def tarif_dasar(self):
        return self._tarif_dasar

    @property
    def kuota_maks(self):
        return self._kuota_maks

    @property
    def kuota_tersisa(self):
        return self._kuota_tersisa

    @property
    def instruktur_id(self):
        return self._instruktur_id

    def ada_kuota(self):
        return self._kuota_tersisa > 0

    def kurangi_kuota(self):
        if not self.ada_kuota():
            raise KuotaPenuhError(f"Kuota kelas {self.nama} sudah penuh.")
        self._kuota_tersisa -= 1

    def kembalikan_kuota(self):
        if self._kuota_tersisa < self._kuota_maks:
            self._kuota_tersisa += 1

    @abstractmethod
    def hitung_biaya(self):
        """Biaya kelas sesuai jenis (AB5); wajib diisi subclass."""

    @classmethod
    def from_dict(cls, data):
        sub = Kelas._registry.get(data.get("jenis"))
        if sub is None:
            raise InputTidakValidError(
                f"Jenis kelas tidak dikenal: {data.get('jenis')}")
        isi = {n: data[n] for n in cls.FIELDS if n != "jenis" and n in data}
        return sub(**isi)

    @classmethod
    def jenis_tersedia(cls):
        return sorted(cls._registry)

    @classmethod
    def buat(cls, jenis, **kwargs):
        sub = cls._registry.get(str(jenis).lower())
        if sub is None:
            raise InputTidakValidError(
                f"Jenis kelas harus salah satu dari: {', '.join(cls.jenis_tersedia())}.")
        return sub(**kwargs)

    def __str__(self):
        return (f"{self.id} | {self.nama} ({self.jenis}) | "
                f"Rp{self.hitung_biaya():,} | kuota {self.kuota_tersisa}/{self.kuota_maks}"
                ).replace(",", ".")


class KelasReguler(Kelas):
    JENIS = "reguler"

    def hitung_biaya(self):
        return self.tarif_dasar


class KelasIntensif(Kelas):
    JENIS = "intensif"

    def hitung_biaya(self):
        return self.tarif_dasar * 125 // 100  # tarif dasar + 25%


class KelasOnline(Kelas):
    JENIS = "online"

    def hitung_biaya(self):
        return self.tarif_dasar * 90 // 100  # tarif dasar - 10%
