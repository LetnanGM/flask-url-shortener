from abc import ABC, abstractmethod
from share.support.time.date import date
from share.support.style.color import Colors
from data.configuration.internal.system import ASSETS


class BaseLogger(ABC):
    def __init__(
        self, log_file: str = f"{ASSETS}/logs/Application/Session-[time].log"
    ) -> None:
        """ """
        self.log_file: str = (
            log_file.replace("[time]", f"{date.get_date_as_ymd()}")
            if "[time]" in log_file
            else log_file
        )

        self._setup_logger_()

    def _timestamp_(self) -> str:
        """
        timestamp for stamp time in terminal
        """
        from datetime import datetime

        now = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        return f"{Colors.YELLOW}{now}{Colors.END}"

    @abstractmethod
    def _setup_logger_(self) -> None:
        """logic logger and setup make object here"""
        ...

    @abstractmethod
    def _write(self) -> None:
        """logic logger write into console"""

    @abstractmethod
    def vulnerable(self) -> None:
        """vulnerable message"""
        ...

    @abstractmethod
    def info(self) -> None:
        """info message"""
        ...

    @abstractmethod
    def success(self) -> None:
        """success message"""
        ...

    @abstractmethod
    def failed(self) -> None:
        """failed message"""
        ...

    @abstractmethod
    def error(self) -> None:
        """error message"""
        ...

    @abstractmethod
    def critical(self) -> None:
        """critical message"""
        ...

    @abstractmethod
    def warn(self) -> None:
        """warn message"""
        ...

    @abstractmethod
    def vsilent(self) -> None:
        """vsilent message"""
        ...

    @abstractmethod
    def silent(self) -> None:
        """silent message"""
        ...

    @abstractmethod
    def debug(self) -> None:
        """debug message"""
        ...

    @abstractmethod
    def custom(self) -> None:
        """custom message"""
        ...
