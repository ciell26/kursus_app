"""Fungsi validasi input (AB10)."""
import re

from exceptions.errors import InputTidakValidError

_POLA_EMAIL = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")
_POLA_TELEPON = re.compile(r"\d{10,13}")


def wajib_teks(nilai, label):
    nilai = str(nilai).strip()
    if not nilai:
        raise InputTidakValidError(f"{label} tidak boleh kosong.")
    return nilai


def valid_email(nilai):
    nilai = str(nilai).strip()
    if not _POLA_EMAIL.fullmatch(nilai):
        raise InputTidakValidError("Format email tidak valid.")
    return nilai


def valid_telepon(nilai):
    nilai = str(nilai).strip()
    if not _POLA_TELEPON.fullmatch(nilai):
        raise InputTidakValidError("Telepon harus 10-13 digit angka.")
    return nilai


def angka_positif(nilai, label):
    try:
        angka = int(nilai)
    except (TypeError, ValueError):
        raise InputTidakValidError(f"{label} harus berupa angka bulat.")
    if angka <= 0:
        raise InputTidakValidError(f"{label} harus lebih dari 0.")
    return angka
