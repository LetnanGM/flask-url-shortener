import json
from types import EllipsisType
from typing import List, Dict, Any, Tuple
from io import TextIOWrapper, IOBase, BufferedWriter
from share.shared.logger.print import Logger

# logging output :D
_log = Logger()


class ReadHandler:
    def __init__(self, fp: TextIOWrapper | IOBase) -> None:
        self.fp = fp
        _log.debug(f"ReadHandler: Intialized with fp > {fp}")

    @property
    def json(self) -> Dict[Any, Any]:
        data = json.load(fp=self.fp)
        self.fp.close()
        return data

    @property
    def read_all(self) -> str:
        data = self.fp.read()
        self.fp.close()
        return data

    @property
    def everyline(self) -> List[Any]:
        lines: List[str | Any] = []

        lines_fp = self.fp.readlines()
        for line in lines_fp:
            lines.append(line)

        self.fp.close()
        return lines

    @property
    def all(self) -> Tuple[Dict[Any, Any], List[Any], str]:
        data_json = json.load(fp=self.fp)
        self.fp.seek(0)
        data_rawreaded = self.fp.read()
        self.fp.seek(0)
        data_everylines = self.everyline
        return data_json, data_everylines, data_rawreaded


class WriteHandler:
    def __init__(
        self, fp: BufferedWriter | IOBase, obj: Any, indent: int | None = ...
    ) -> None:
        if not obj:
            raise TypeError("self.obj or obj must be str or dict, not empty!")

        self.fp = fp
        self.obj = obj
        self.indent: int | EllipsisType = ...
        _log.debug(
            f"WriteHandler initialized: Params(fp={fp}, obj=Blocked, indent={indent})"
        )

    def __repr__(self, *args, **kwargs) -> None:
        _mess = f"<WriteHandler memory(0x{id(self.fp)}), Params(fp={self.fp}, obj=Blcoked, indent={self.indent})>"
        _log.debug(_mess)
        return _mess

    @property
    def to_json(self) -> json.dump:
        _log.debug(
            f"WriteHandler: json_write triggered! \n  Flag: Params(fp={self.fp}, obj=Blocked, indent={self.indent})"
        )
        if isinstance(self.indent, EllipsisType):
            self.indent: int = 4

        object = json.dump(obj=self.obj, fp=self.fp, indent=self.indent)
        self.fp.close()
        return object

    @property
    def to_dummyfile(self) -> int:
        _log.debug(
            f"WriteHandler: dummyfile triggred! \n    Flag: Params(fp={self.fp}, obj=Blocked, indent={self.indent})"
        )
        res = self.fp.write(self.obj)
        self.fp.close()
        return res
