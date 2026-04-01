from logging import LogRecord, Formatter
from .local_config import STD_ATTRS


class ExtraFormatter(Formatter):
    """ """

    def format(self, record: LogRecord) -> str:
        s = super().format(record)

        extras = {
            k: v
            for k, v in record.__dict__.items()
            if k not in STD_ATTRS and not k.startswith("_")
        }

        if extras:
            s += "| extra=" + ", ".join(f"{k}={v!r}" for k, v in extras.items())

        return s
