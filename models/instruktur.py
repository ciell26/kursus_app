"""Instruktur (turunan Orang)."""
from models.orang import Orang
from utils.mixins import SerializableMixin
from utils.validator import wajib_teks


class Instruktur(Orang, SerializableMixin):
    FIELDS = ("id", "nama", "email", "telepon", "keahlian")

    def __init__(self, id, nama, email, telepon, keahlian):
        super().__init__(id, nama, email, telepon)
        self.keahlian = keahlian

    @property
    def keahlian(self):
        return self._keahlian

    @keahlian.setter
    def keahlian(self, nilai):
        self._keahlian = wajib_teks(nilai, "Keahlian")

    @property
    def peran(self):
        return "instruktur"

    def __str__(self):
        return f"{super().__str__()} | {self.keahlian}"
