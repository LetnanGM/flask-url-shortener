"""
Application custom exceptions.
"""

import inspect


class AppError(Exception):
    """Base class untuk semua custom error + util"""

    code = "APP-000"
    category = "GENERAL"

    def __init__(self, message=None, *, context=None):
        """there's used for took name function called"""
        frame = inspect.currentframe().f_back
        self.func_name = frame.f_code.co_name if frame else None

        self.message = message or self.__class__.__name__
        self.context = context
        super().__init__(self.message)

    def __str__(self):
        """shows where error code and traceback custom"""
        return (
            f"[{self.code}] {self.message}"
            + (f" | Context: {self.context}" if self.context else "")
            + (f" | Function: {self.func_name}" if self.func_name else "")
        )

    @staticmethod
    def format_context(filename, line=None, func=None):
        """adding more context format for utility traceback :D"""
        return f"File={filename}, Line={line}, Func={func}"
