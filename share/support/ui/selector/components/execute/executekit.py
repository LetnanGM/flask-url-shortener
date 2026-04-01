from typing import Any
from ..childprocess.manager import process
from ..model import vmodel
from ..find.find import uitil


class executeKit:
    def __init__(self) -> None:
        pass

    def execute_redirect(self, command: str, **kwargs) -> Any:
        """
        Eksekusi redirect berdasarkan command string.

        Params:
            command : string command yang cocok dengan entry.
            **kwargs: argumen tambahan yang diteruskan ke redirect.

        Return:
            Hasil dari redirect, atau None jika command tidak ditemukan.
        """
        if not isinstance(command, str) or not command:
            raise ValueError("command harus string tidak kosong!")

        label = uitil.getLabelWithCommand(command=command)
        if label is None or label not in vmodel.InMemorydb:
            print(f"[!] Command '{command}' tidak ditemukan.")
            return None

        obj = vmodel.InMemorydb[label]["redirect"]
        return obj(**kwargs)

    def execute_by_index(self, index: int, *args, **kwargs) -> Any:
        """
        Eksekusi redirect berdasarkan index tampilan menu.

        Params:
            index  : nomor index dari show_menu.
            **kwargs: argumen tambahan yang diteruskan ke redirect.
        """

        obj = uitil.get_redirect_with_index(index)
        print(f"[>] Menjalankan: {obj.__name__}")
        return obj(*args, **kwargs)

    def execute_by_label(self, label: str, *args, **kwargs) -> Any:
        """
        Eksekusi redirect berdasarkan label tampilan menu.

        Params:
            label: nama index dari show_menu.
            *args: argument tunggal tambahan yang diteruskan ke redirect.
            **kwargs: argument tambahan yang diteruskan ke redirect.
        """

        for label_value, value in vmodel.InMemorydb.items():
            if label_value == label:
                obj = vmodel.InMemorydb[label]["redirect"]
                print(f"[>] Menjalankan: {obj.__name__}")
                return obj(*args, **kwargs)

        print("Label tidak tersedia.")

    def execute_by_background(
        self, label: str | None = ..., index: int | None = ..., *args, **kwargs
    ):
        """
        input value in label or index for executing pattern.
        """
        import multiprocessing

        def execute(obj: callable, *args, **kwargs) -> multiprocessing.Process:
            p = multiprocessing.Process(
                target=obj, args=args, kwargs=kwargs, daemon=True
            )
            p.start()

            process().add_new_process(pid=p.pid, process_name=obj.__name__)

        if not label and not index:
            raise TypeError("label or index must be fieled!")

        if label and isinstance(label, str):
            obj = uitil.get_redirect_with_label(label=label)
            execute(obj, *args, **kwargs)

        if index and isinstance(index, int):
            obj = uitil.get_redirect_with_index(index=index)
            execute(obj, *args, **kwargs)
