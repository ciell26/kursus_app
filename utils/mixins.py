"""Mixin: serialisasi objek <-> dict dan jejak waktu."""
from datetime import datetime


class SerializableMixin:
    """Konversi objek <-> dict. Kelas pemakai mengisi FIELDS."""

    FIELDS = ()

    def to_dict(self):
        return {nama: getattr(self, nama) for nama in self.FIELDS}

    @classmethod
    def from_dict(cls, data):
        return cls(**{n: data[n] for n in cls.FIELDS if n in data})


class AuditMixin:
    """Menambah dibuat_pada dan diubah_pada."""

    @staticmethod
    def _sekarang():
        return datetime.now().replace(microsecond=0).isoformat()

    def _init_audit(self, dibuat_pada=None, diubah_pada=None):
        self._dibuat_pada = dibuat_pada or self._sekarang()
        self._diubah_pada = diubah_pada or self._dibuat_pada

    @property
    def dibuat_pada(self):
        return self._dibuat_pada

    @property
    def diubah_pada(self):
        return self._diubah_pada

    def sentuh(self):
        self._diubah_pada = self._sekarang()
