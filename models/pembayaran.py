"""Pembayaran untuk satu pendaftaran (0..1)."""
from exceptions.errors import PembayaranGagalError, StatusTidakValidError
from utils.mixins import AuditMixin, SerializableMixin


class Pembayaran(SerializableMixin, AuditMixin):
    LUNAS = "LUNAS"
    REFUND = "REFUND"

    FIELDS = ("id", "pendaftaran_id", "metode", "biaya_kelas", "biaya_admin",
              "total", "status", "jumlah_refund")

    def __init__(self, id, pendaftaran_id, metode, biaya_kelas, biaya_admin,
                 total, status=LUNAS, jumlah_refund=0):
        if biaya_kelas <= 0 or biaya_admin < 0 or total != biaya_kelas + biaya_admin:
            raise PembayaranGagalError("Nominal pembayaran tidak konsisten.")
        self._id = id
        self._pendaftaran_id = pendaftaran_id
        self._metode = metode
        self._biaya_kelas = biaya_kelas
        self._biaya_admin = biaya_admin
        self._total = total
        self._status = status
        self._jumlah_refund = jumlah_refund
        self._init_audit()

    @property
    def id(self):
        return self._id

    @property
    def pendaftaran_id(self):
        return self._pendaftaran_id

    @property
    def metode(self):
        return self._metode

    @property
    def biaya_kelas(self):
        return self._biaya_kelas

    @property
    def biaya_admin(self):
        return self._biaya_admin

    @property
    def total(self):
        return self._total

    @property
    def status(self):
        return self._status

    @property
    def jumlah_refund(self):
        return self._jumlah_refund

    def tandai_refund(self, jumlah):
        if self._status != self.LUNAS:
            raise StatusTidakValidError("Hanya pembayaran LUNAS yang dapat di-refund.")
        self._status = self.REFUND
        self._jumlah_refund = jumlah
        self.sentuh()
