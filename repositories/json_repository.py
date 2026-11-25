"""JsonRepository: satu-satunya kelas yang tahu soal berkas JSON."""
import json
from pathlib import Path

from exceptions.errors import DataTidakDitemukanError, KursusError


class JsonRepository:
    def __init__(self, path, model_cls, prefix, label):
        self._path = Path(path)
        self._model = model_cls
        self._prefix = prefix
        self._label = label
        self._items = self._muat()

    def _muat(self):
        if not self._path.exists():
            self._path.parent.mkdir(parents=True, exist_ok=True)
            self._path.write_text("[]", encoding="utf-8")
            return []
        try:
            with open(self._path, encoding="utf-8") as f:
                return [self._model.from_dict(d) for d in json.load(f)]
        except (json.JSONDecodeError, TypeError, KeyError, AttributeError) as e:
            raise KursusError(
                f"Berkas {self._path.name} rusak atau formatnya tidak sesuai.") from e

    def _tulis(self):
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump([o.to_dict() for o in self._items], f,
                      ensure_ascii=False, indent=2)

    def semua(self):
        return list(self._items)

    def cari(self, id):
        return next((o for o in self._items if o.id == id), None)

    def ambil(self, id):
        obj = self.cari(id)
        if obj is None:
            raise DataTidakDitemukanError(f"{self._label} dengan ID {id} tidak ditemukan.")
        return obj

    def filter(self, kondisi):
        return [o for o in self._items if kondisi(o)]

    def id_berikutnya(self):
        angka = [int(o.id[len(self._prefix):]) for o in self._items]
        return f"{self._prefix}{max(angka, default=0) + 1:03d}"

    def tambah(self, obj):
        self._items.append(obj)
        self._tulis()

    def perbarui(self, obj):
        for i, lama in enumerate(self._items):
            if lama.id == obj.id:
                self._items[i] = obj
                self._tulis()
                return
        raise DataTidakDitemukanError(f"{self._label} dengan ID {obj.id} tidak ditemukan.")
