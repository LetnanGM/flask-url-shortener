from typing import Optional, Dict
from ..model import vmodel


class uitil:
    @staticmethod
    def getLabelWithCommand(command: str) -> Optional[str]:
        """Cari label berdasarkan command string."""
        for label, value in vmodel.InMemorydb.items():
            if command == value["command"]:
                return label
        return None

    @staticmethod
    def get_redirect_with_label(label: str) -> callable:
        """ambil redirect"""
        for label_value, value in vmodel.InMemorydb.items():
            if label_value == label:
                return value.get("redirect")

    @staticmethod
    def get_redirect_with_index(index: int) -> callable:
        keys = list(vmodel.InMemorydb.keys())
        if index < 0 or index >= len(keys):
            raise IndexError(f"Index {index} di luar jangkauan (0–{len(keys)-1})!")

        label = keys[index]
        obj = vmodel.InMemorydb[label]["redirect"]
        return obj

    @staticmethod
    def search(query: str) -> Dict[str, dict]:
        """Cari entries berdasarkan query pada label atau command."""
        query = query.lower()
        return {
            label: value
            for label, value in vmodel.InMemorydb.items()
            if query in label.lower() or query in value["command"].lower()
        }

    @staticmethod
    def filter_by_prefix(prefix: str) -> Dict[str, dict]:
        """Filter entries berdasarkan prefix label."""
        return {
            label: value
            for label, value in vmodel.InMemorydb.items()
            if label.startswith(prefix)
        }
