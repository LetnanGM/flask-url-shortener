from flask import Flask
from plugin.internal.protection.data.configuration.security.authfactor import (
    DATABASED_FIF,
)
from shared.utilities.submodule.FileHandling import FileHandler


class FA3_config:
    file = FileHandler()


class FA3:
    def __init__(self) -> None:
        """Something you are"""
        self.app = None
        self.database = {}

    def init_database(self) -> None:
        self.database = FA3_config.file.Read(DATABASED_FIF)

    def init_app(self, app: Flask) -> None:
        self.app = app

    def factor(self) -> None:
        return NotImplementedError("function are not implementation, wait update")
