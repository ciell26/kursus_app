"""Orang (abstrak) -> Peserta, Instruktur."""
from abc import ABC, abstractmethod

from utils.validator import valid_email, valid_telepon, wajib_teks


class Orang(ABC):
    def __init__(self, id, nama, email, telepon):
        self._id = id
        self.nama = nama
        self.email = email
        self.telepon = telepon

    @property
    def id(self):
        return self._id

    @property
    def nama(self):
        return self._nama

    @nama.setter
    def nama(self, nilai):
        self._nama = wajib_teks(nilai, "Nama")

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, nilai):
        self._email = valid_email(nilai)

    @property
    def telepon(self):
        return self._telepon

    @telepon.setter
    def telepon(self, nilai):
        self._telepon = valid_telepon(nilai)

    @property
    @abstractmethod
    def peran(self):
        """Peran orang di lembaga (diisi subclass)."""

    def __str__(self):
        return f"{self.id} | {self.nama} | {self.email} | {self.telepon}"
