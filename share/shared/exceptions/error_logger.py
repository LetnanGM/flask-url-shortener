# shared/exceptions/error_writer.py
import logging
import traceback
from .parent import AppError

logging.basicConfig(
    level=logging.ERROR,  # ganti ke ERROR kalau production
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)


def handle_exception(exc: Exception):
    """Global handler untuk semua exception"""

    tb = traceback.extract_tb(exc.__traceback__)
    last_call = tb[-1] if tb else None

    if isinstance(exc, AppError):
        logging.error(
            f"[{exc.code}] {exc.message}"
            + (f" | Context: {exc.context}" if exc.context else "")
            + (
                f" | Function: {exc.func_name}"
                if getattr(exc, "func_name", None)
                else ""
            )
            + (
                f" | File: {last_call.filename}, Line: {last_call.lineno}"
                if last_call
                else ""
            )
        )
    else:
        logging.exception("Unhandled exception occurred", exc_info=exc)
