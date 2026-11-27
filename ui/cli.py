"""Antarmuka CLI. Semua KursusError ditangkap di sini (program tidak berhenti)."""
from pathlib import Path

from exceptions.errors import InputTidakValidError, KursusError
from models import Instruktur, Kelas, Pembayaran, Pendaftaran, Peserta, metode_default
from repositories.json_repository import JsonRepository
from services.laporan import Laporan
from services.proses_pembatalan import ProsesPembatalan
from services.proses_pembayaran import ProsesPembayaran
from services.proses_pendaftaran import ProsesPendaftaran


def rupiah(n):
    return f"Rp{n:,}".replace(",", ".")


class AplikasiCLI:
    def __init__(self, folder_data=None):
        folder = Path(folder_data or Path(__file__).resolve().parent.parent / "data")
        self.peserta = JsonRepository(folder / "peserta.json", Peserta, "P", "Peserta")
        self.instruktur = JsonRepository(folder / "instruktur.json", Instruktur, "I", "Instruktur")
        self.kelas = JsonRepository(folder / "kelas.json", Kelas, "K", "Kelas")
        self.pendaftaran = JsonRepository(folder / "pendaftaran.json", Pendaftaran, "D", "Pendaftaran")
        self.pembayaran = JsonRepository(folder / "pembayaran.json", Pembayaran, "B", "Pembayaran")

        self.proses_daftar = ProsesPendaftaran(self.pendaftaran, self.kelas, self.peserta)
        self.proses_bayar = ProsesPembayaran(self.pendaftaran, self.kelas,
                                             self.pembayaran, metode_default())
        self.proses_batal = ProsesPembatalan(self.pendaftaran, self.kelas, self.pembayaran)
        self.laporan = Laporan(self.peserta, self.kelas, self.pendaftaran, self.pembayaran)

    @staticmethod
    def _tanya(label):
        return input(f"{label}: ").strip()

    @staticmethod
    def _cetak_daftar(judul, daftar):
        print(f"\n--- {judul} ---")
        if not daftar:
            print("(kosong)")
        for item in daftar:
            print(item)

    @staticmethod
    def tampilkan_menu():
        print("\n=== SISTEM MANAJEMEN KURSUS ===")
        print("1. Kelola data")
        print("2. Pendaftaran")
        print("3. Pembayaran")
        print("4. Pembatalan/Refund")
        print("5. Laporan")
        print("0. Keluar")

    def menu_data(self):
        print("\n[Kelola data]")
        print("1. Tambah peserta")
        print("2. Lihat peserta")
        print("3. Tambah instruktur")
        print("4. Lihat instruktur")
        print("5. Tambah kelas")
        print("6. Lihat kelas")
        print("0. Kembali")
        pilih = self._tanya("Pilih")
        if pilih == "1":
            p = Peserta(self.peserta.id_berikutnya(), self._tanya("Nama"),
                        self._tanya("Email"), self._tanya("Telepon"))
            self.peserta.tambah(p)
            print(f"Peserta tersimpan: {p}")
        elif pilih == "2":
            self._cetak_daftar("Peserta", self.peserta.semua())
        elif pilih == "3":
            i = Instruktur(self.instruktur.id_berikutnya(), self._tanya("Nama"),
                           self._tanya("Email"), self._tanya("Telepon"),
                           self._tanya("Keahlian"))
            self.instruktur.tambah(i)
            print(f"Instruktur tersimpan: {i}")
        elif pilih == "4":
            self._cetak_daftar("Instruktur", self.instruktur.semua())
        elif pilih == "5":
            print("Jenis tersedia:", ", ".join(Kelas.jenis_tersedia()))
            jenis = self._tanya("Jenis kelas")
            nama = self._tanya("Nama kelas")
            tarif = self._tanya("Tarif dasar (Rp)")
            kuota = self._tanya("Kuota maksimal")
            instr_id = self.instruktur.ambil(self._tanya("ID instruktur")).id
            k = Kelas.buat(jenis, id=self.kelas.id_berikutnya(), nama=nama,
                           tarif_dasar=tarif, kuota_maks=kuota, instruktur_id=instr_id)
            self.kelas.tambah(k)
            print(f"Kelas tersimpan: {k}")
        elif pilih == "6":
            self._cetak_daftar("Kelas", self.kelas.semua())
        elif pilih != "0":
            raise InputTidakValidError("Pilihan menu tidak dikenal.")

    def menu_pendaftaran(self):
        self._cetak_daftar("Peserta", self.peserta.semua())
        self._cetak_daftar("Kelas", self.kelas.semua())
        self.proses_daftar.jalankan(peserta_id=self._tanya("ID peserta"),
                                    kelas_id=self._tanya("ID kelas"))
        print(self.proses_daftar.pesan_terakhir)

    def menu_pembayaran(self):
        menunggu = self.pendaftaran.filter(lambda d: d.status == "MENUNGGU_PEMBAYARAN")
        self._cetak_daftar("Menunggu pembayaran", menunggu)
        print("Metode: tunai, transfer, ewallet")
        self.proses_bayar.jalankan(pendaftaran_id=self._tanya("ID pendaftaran"),
                                   metode=self._tanya("Metode"))
        print(self.proses_bayar.pesan_terakhir)

    def menu_pembatalan(self):
        self._cetak_daftar("Pendaftaran", self.pendaftaran.semua())
        self.proses_batal.jalankan(pendaftaran_id=self._tanya("ID pendaftaran"))
        print(self.proses_batal.pesan_terakhir)

    def menu_laporan(self):
        print("\n[Laporan]")
        print("1. Peserta per kelas")
        print("2. Sisa kuota")
        print("3. Ringkasan pendapatan")
        print("0. Kembali")
        pilih = self._tanya("Pilih")
        if pilih == "1":
            kelas, daftar = self.laporan.peserta_per_kelas(self._tanya("ID kelas"))
            print(f"\nPeserta kelas {kelas.nama}:")
            if not daftar:
                print("(belum ada peserta aktif)")
            for d, p in daftar:
                print(f"- {p.nama} ({p.id}) | {d.id} | {d.status}")
        elif pilih == "2":
            for k in self.laporan.sisa_kuota():
                print(f"{k.id} | {k.nama} | sisa {k.kuota_tersisa}/{k.kuota_maks}")
        elif pilih == "3":
            r = self.laporan.ringkasan_pendapatan()
            print(f"Transaksi        : {r['jumlah_transaksi']}")
            print(f"Pendapatan kotor : {rupiah(r['pendapatan_kotor'])}")
            print(f"Total refund     : {rupiah(r['total_refund'])}")
            print(f"Pendapatan bersih: {rupiah(r['pendapatan_bersih'])}")
        elif pilih != "0":
            raise InputTidakValidError("Pilihan menu tidak dikenal.")

    def jalankan(self):
        aksi = {"1": self.menu_data, "2": self.menu_pendaftaran,
                "3": self.menu_pembayaran, "4": self.menu_pembatalan,
                "5": self.menu_laporan}
        while True:
            self.tampilkan_menu()
            try:
                pilih = self._tanya("Pilih menu")
                if pilih == "0":
                    print("Data sudah tersimpan. Sampai jumpa.")
                    break
                if pilih not in aksi:
                    raise InputTidakValidError("Pilihan menu tidak dikenal.")
                aksi[pilih]()
            except KursusError as e:
                print(f"[GAGAL] {e}")
            except (EOFError, KeyboardInterrupt):
                print("\nProgram ditutup.")
                break