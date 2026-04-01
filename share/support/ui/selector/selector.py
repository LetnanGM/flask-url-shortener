from typing import Any, Optional
from .components.model import vmodel
from .components.find.find import uitil
from .components.execute.executekit import executeKit


class ui(executeKit):
    def __init__(self):
        super().__init__()

    @property
    def show_menu(self) -> None:
        """Tampilkan semua entries di InMemorydb."""
        if not vmodel.InMemorydb:
            print("(kosong — belum ada command terdaftar)")
            return
        print(f"{'IDX':<5} {'LABEL':<25} {'COMMAND':<20}")
        print("-" * 55)
        for idx, (label, value) in enumerate(vmodel.InMemorydb.items()):
            print(f"{idx:<5} {label:<25} {value['command']:<20}")

    def add_new_command(self, label: str, command: str, redirect: Any) -> bool:
        """
        Tambah command baru ke InMemorydb.

        Params:
            label    : nama / judul command.
            command  : pola string untuk eksekusi.
            redirect : fungsi atau class yang dijalankan.

        Return:
            True jika berhasil ditambahkan.
        """
        if not isinstance(label, str) or not isinstance(command, str):
            raise TypeError("label dan command harus bertipe string!")
        if not label or not command:
            raise ValueError("label dan command tidak boleh kosong!")
        if not callable(redirect):
            raise TypeError("redirect harus callable (fungsi atau class)!")

        vmodel.InMemorydb[label] = {"command": command, "redirect": redirect}
        return True

    def update_command(
        self,
        label: str,
        new_command: Optional[str] = None,
        new_redirect: Optional[Any] = None,
    ) -> bool:
        """
        Update command atau redirect dari entry yang ada.

        Params:
            label       : label entry yang ingin diupdate.
            new_command : command baru (opsional).
            new_redirect: redirect baru (opsional).

        Return:
            True jika berhasil diupdate.
        """
        if label not in vmodel.InMemorydb:
            raise KeyError(f"Label '{label}' tidak ditemukan!")

        if new_command is not None:
            if not isinstance(new_command, str) or not new_command:
                raise ValueError("new_command harus string tidak kosong!")
            vmodel.InMemorydb[label]["command"] = new_command

        if new_redirect is not None:
            if not callable(new_redirect):
                raise TypeError("new_redirect harus callable!")
            vmodel.InMemorydb[label]["redirect"] = new_redirect

        return True

    def remove_command(self, label: str) -> bool:
        """
        Hapus entry berdasarkan label.

        Return:
            True jika berhasil dihapus, False jika label tidak ada.
        """
        if label in vmodel.InMemorydb:
            del vmodel.InMemorydb[label]
            return True
        return False

    def search(self, query: str) -> None:
        """Cari dan tampilkan entries yang cocok dengan query."""
        results = uitil.search(query)
        if not results:
            print(f"Tidak ada hasil untuk '{query}'.")
            return
        print(f"Hasil pencarian '{query}':")
        for idx, (label, value) in enumerate(results.items()):
            print(f"  {idx} : {label:<25} [{value['command']}]")
