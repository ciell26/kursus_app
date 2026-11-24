"""Peserta (turunan Orang) dengan mixin serialisasi dan jejak waktu."""
from models.orang import Orang
from utils.mixins import AuditMixin, SerializableMixin


class Peserta(Orang, SerializableMixin, AuditMixin):
    FIELDS = ("id", "nama", "email", "telepon", "dibuat_pada")

    def __init__(self, id, nama, email, telepon, dibuat_pada=None):
        super().__init__(id, nama, email, telepon)
        self._init_audit(dibuat_pada)

    @property
    def peran(self):
        return "peserta"
