from flask import Flask
from typing import Tuple


class FA1:
    def __init__(self) -> None:
        """Something You Know"""
        self.app: Flask = None

    def init_app(self, app: Flask) -> None:
        self.app = app

    def factor(self, password: str, salt: bytes | str) -> Tuple[str, bool]:
        if not password and not salt:
            return "You don't have anything awokaokw", False

        if not len(password) < 64 and salt:
            return "You have anytihing. :S", True

        return "F*ck you self", False
