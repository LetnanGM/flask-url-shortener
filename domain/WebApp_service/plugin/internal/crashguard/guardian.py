from flask import Flask

import sys
import traceback
from typing import Any
from share.shared.logger.print import Logger

GuardianLogger = Logger(log_file="assets/logs/guardian/error-[time].log")


class guardian:
    __PLUGIN_NAME__ = "CrashGuard"
    __VERSION__ = "1.0.0"
    __DEVELOPER__ = "LetnanDev"
    __SUPPORTED__ = ["Flask"]

    def handle_exception(exc_type: Any, exc_value: Any, exc_traceback: Any):
        if issubclass(exc_type, KeyboardInterrupt):
            return

        message = (
            ">>> UNHANDLED EXCEPTION CAUGHT (Server still running) <<<\n"
            + "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        )

        GuardianLogger.error(message)
        GuardianLogger.vsilent(message)

    @staticmethod
    def setup(app: Flask):
        @app.errorhandler(Exception)
        def handle_flask_error(e):
            GuardianLogger.error(
                f">>> FLASK ERROR, SERVER STILL RUNNING <<< \n{e}\n>>> END OF REPORT ERROR <<<"
            )
            GuardianLogger.vsilent(
                f">>> FLASK ERROR, SERVER STILL RUNNING <<< \n{e}\n>>> END OF REPORT ERROR <<<"
            )
            return (
                "You found some bug in our application!, the bug will reported into server developer!\nThanks for your report",
                500,
            )

    sys.excepthook = handle_exception
