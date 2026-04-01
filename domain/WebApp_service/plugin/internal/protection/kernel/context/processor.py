from flask import Flask
from typing import Dict, Any
from ...data.configuration.sys.config import DYNAMIC_CONTEXT


class ContextProcessor:
    def __init__(self, app: Flask) -> None:
        self.database = {}
        self.app = app

        self.load_database_from_config()
        self.context_register()

    def load_database_from_config(self) -> None:
        self.database = DYNAMIC_CONTEXT

    def context_register(self):
        @self.app.context_processor
        def inject_dynamic_context():
            return self.all()

    # function register akan mendatang dan akan di update sehingga berfungsi
    def register(self, key: str, value: Any) -> bool:
        self.database[key] = value

        return True

    def all(self) -> Dict[str, Any]:
        return self.database
