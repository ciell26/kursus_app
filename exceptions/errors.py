"""Hierarki exception khusus aplikasi (KursusError + 6 turunan)."""


class KursusError(Exception):
    """Dasar semua kesalahan aplikasi; ditangkap di CLI."""


class KuotaPenuhError(KursusError):
    """AB3: kuota kelas sudah habis."""


class DataTidakDitemukanError(KursusError):
    """AB1: peserta/kelas/pendaftaran/instruktur tidak ada."""


class PendaftaranGandaError(KursusError):
    """AB2: peserta sudah punya pendaftaran aktif di kelas yang sama."""


class InputTidakValidError(KursusError):
    """AB10: input tidak lolos validasi."""


class StatusTidakValidError(KursusError):
    """AB7/AB8: aksi dilakukan pada status yang salah."""


class PembayaranGagalError(KursusError):
    """Pembayaran tidak dapat diproses."""
