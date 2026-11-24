"""Pendaftaran peserta ke kelas. Relasi lewat ID (bukan objek bersarang)."""
from exceptions.errors import InputTidakValidError, StatusTidakValidError
from utils.mixins import AuditMixin, SerializableMixin


class Pendaftaran(SerializableMixin, AuditMixin):
    MENUNGGU = "MENUNGGU_PEMBAYARAN"
    LUNAS = "LUNAS"
    DIBATALKAN = "DIBATALKAN"
    STATUS_VALID = (MENUNGGU, LUNAS, DIBATALKAN)

    FIELDS = ("id", "peserta_id", "kelas_id", "status",
              "dibuat_pada", "diubah_pada")

    def __init__(self, id, peserta_id, kelas_id, status=MENUNGGU,
                 dibuat_pada=None, diubah_pada=None):
        if status not in self.STATUS_VALID:
            raise InputTidakValidError(f"Status pendaftaran tidak dikenal: {status}")
        self._id = id
        self._peserta_id = peserta_id
        self._kelas_id = kelas_id
        self._status = status
        self._init_audit(dibuat_pada, diubah_pada)

    @property
    def id(self):
        return self._id

    @property
    def peserta_id(self):
        return self._peserta_id

    @property
    def kelas_id(self):
        return self._kelas_id

    @property
    def status(self):
        return self._status

    @property
    def aktif(self):
        """Aktif = bukan DIBATALKAN (AB2)."""
        return self._status != self.DIBATALKAN

    def tandai_lunas(self):
        if self._status != self.MENUNGGU:
            raise StatusTidakValidError(
                f"Pembayaran hanya untuk status {self.MENUNGGU}, "
                f"status sekarang {self._status}.")
        self._status = self.LUNAS
        self.sentuh()

    def batalkan(self):
        if self._status not in (self.MENUNGGU, self.LUNAS):
            raise StatusTidakValidError(
                f"Pembatalan hanya untuk status {self.MENUNGGU} atau {self.LUNAS}, "
                f"status sekarang {self._status}.")
        self._status = self.DIBATALKAN
        self.sentuh()

    def __str__(self):
        return f"{self.id} | peserta {self.peserta_id} | kelas {self.kelas_id} | {self.status}"
