"""
print.py just have function like print for writing message to terminal screen

im bored :S
this why i build this.
"""

import os
import sys
import logging
from logging import Handler
from share.contract.logger.logger import BaseLogger
from share.support.time.date import date
from share.support.style.color import Colors
from .components import ExtraFormatter

VERBOSE: bool = False
SILENT_ALL: bool = True

class Logger(Handler, BaseLogger):
    """it's just parent from many function in down. hehe"""

    def __init__(
        self, log_file: str = "assets/logs/Application/Session-[time].log"
    ) -> None:
        super().__init__()
        self.log_file = (
            log_file.replace("[time]", f"{date.get_date_as_ymd()}")
            if "[time]" in log_file
            else log_file
        )
        self.logger: logging.Logger = None
        self.handlers = None
        self._setup_logger_()

    def _setup_logger_(self):
        """
        setup the logger file: ensure directory exists and attach file handler
        without relying on global basicConfig (to avoid duplicate handlers).
        """
        # Ensure directory exists (fix: previously created 'assets/log' instead
        # of 'assets/logs')
        log_dir = os.path.dirname(os.path.abspath(self.log_file))
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        # Setup dedicated logger per file to avoid handler duplication
        logger_name = f"session:{os.path.abspath(self.log_file)}"
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        self.handlers = self.logger.handlers

        # Attach a single FileHandler if not yet attached
        if not any(
            isinstance(h, logging.FileHandler)
            and getattr(h, "baseFilename", "") == os.path.abspath(self.log_file)
            for h in self.logger.handlers
        ):
            fh = logging.FileHandler(self.log_file, mode="a", encoding="utf-8")
            formatter = ExtraFormatter("%(asctime)s - %(levelname)s - %(message)s")
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)
            # Prevent propagating to root to avoid duplicate logs when
            # basicConfig is used elsewhere
            self.logger.propagate = False

    def _write(
        self, tag: str, color: str, message: str, log_level: str = "info", **kwargs
    ):
        lvl = (log_level or "info").lower()

        if lvl == "silent":
            if self.logger:
                self.logger.debug(message, **kwargs)
            return
        if lvl == "vuln":
            lvl = "warning"

        output = f"[{self._timestamp_()}] [{color}{tag}{Colors.END}]: {message}"

        sys.stdout.write(output + "\n")
        sys.stdout.flush()

        if not SILENT_ALL:
            # Logging to file
            if self.logger:
                log_func = getattr(self.logger, lvl, self.logger.info)
                log_func(message, **kwargs)

    # Public methods

    def vulnerable(self, message: str, **kwargs):
        self._write("VULNERABLE", Colors.LIGHT_GREEN, message, "vuln", **kwargs)

    def info(self, message: str, **kwargs):
        self._write("INFO", Colors.YELLOW, message, "info", **kwargs)

    def success(self, message: str, **kwargs):
        self._write("SUCCESS", Colors.LIGHT_GREEN, message, "info", **kwargs)

    def failed(self, message: str, **kwargs):
        self._write("FAILED", Colors.LIGHT_RED, message, "warning", **kwargs)

    def error(self, message: str, **kwargs):
        self._write("ERROR", Colors.LIGHT_RED, message, "error", **kwargs)

    def critical(self, message: str, **kwargs):
        self._write("CRITICAL", Colors.RED, message, "critical", **kwargs)

    def warn(self, message: str, **kwargs):
        self._write("WARN", Colors.YELLOW, message, "warning", **kwargs)

    def vsilent(self, message: str, **kwargs):
        self.logger.debug(message, **kwargs)

    def silent(self, message: str, **kwargs):
        # Respect VERBOSE: only print when verbose; still log to file at DEBUG
        # level
        if VERBOSE:
            self._write("SILENT", Colors.DARK_GRAY, message, "silent", **kwargs)
        else:
            # Even when not printing, keep a lightweight file log
            if self.logger:
                self.logger.debug(message)

    def debug(self, message: str, **kwargs):
        if VERBOSE:
            self._write("DEBUG", Colors.CYAN, message, "debug", **kwargs)
        else:
            # Log debug to file even when not verbose
            if self.logger:
                self.logger.debug(message)

    def custom(self, level: str, title: str, message: str, *args, **kwargs):
        self._write(
            tag=title,
            color=Colors.LIGHT_GRAY,
            message=message,
            log_level=level,
            *args,
            **kwargs,
        )
