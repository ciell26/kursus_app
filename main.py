from exceptions.errors import KursusError
from ui.cli import AplikasiCLI

if __name__ == "__main__":
    try:
        AplikasiCLI().jalankan()
    except KursusError as e:
        print(f"[GAGAL] {e}")
