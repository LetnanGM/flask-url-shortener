"""
wait update and implementation
"""

from flask import Flask
from typing import Tuple

from plugin.internal.protection.data.configuration.security.authfactor import (
    DATABASE_TOTP,
    DATABASE_HOTP,
)
from shared.utilities.submodule.FileHandling import FileHandler


class FA2_config:
    file = FileHandler()


class FA2:
    def __init__(self) -> None:
        """whatever you have"""
        self.app = None
        self.database_totp = {}

    def __init_database__(self) -> bool:
        self.database_totp = FA2_config.file.Read(DATABASE_TOTP)
        self.database_hotp = FA2_config.file.Read(DATABASE_HOTP)
        return True if self.database and self.database_hotp else False

    def init_app(self, app: Flask) -> None:
        self.app = app

    def factor(self, totp: int, hotp: int | bytes) -> Tuple[str, bool]:
        if not totp and not hotp:
            return ""
