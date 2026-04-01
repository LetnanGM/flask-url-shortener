from flask import Flask

from .protector.ratelimit.RateLimiter import RateLimiter
from .protector.input.InputValidator import InputValidator
from .protector.csrf.CSRF_protection import CSRFProtection
from .protector.obsec.Obsecurity import OBSecurity
from .protector.errorpage.ErrorHandler import ErrorHandler
from .helper.protector import setup_securitychain

from ..kernel.context.processor import ContextProcessor
from ..utils.logging.childLogger import global_protection_logger, SMiddleware_logger

from typing import Dict, Any


class loader_security:
    def __init__(self, app: Flask) -> None:
        self.app = app
        self.data_mapping: Dict[str, Any] = {
            "RateLimiter": {"args": "", "obj": RateLimiter},
            "InputValiator": {
                "args": "",
                "obj": InputValidator,
            },
            "CSRFProtection": {
                "args": "app",
                "obj": CSRFProtection,
            },
            "OBSecurity": {
                "args": "app",
                "obj": OBSecurity,
            },
            "ErrorPage": {
                "args": "app",
                "obj": ErrorHandler,
            },
            "ContextProcessor": {
                "args": "app",
                "obj": ContextProcessor,
            },
            "SetupSecurity": {
                "args": "app",
                "obj": setup_securitychain,
            },
        }

        self.load()

    def load(self):
        for name, data in self.data_mapping.items():
            args, exe = data.get("args", ""), data.get("obj", "")

            if args == "app":
                exe(app=self.app)
            else:
                exe()

            global_protection_logger.debug(f"'{name}' successfully loaded!")

        SMiddleware_logger.debug(
            "'Middleware' all resource and security successfully loaded!"
        )
