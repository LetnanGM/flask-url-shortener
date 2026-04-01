import os
from abc import ABC, abstractmethod
from .response import ReadHandler, WriteHandler


class BaseFileHandler(ABC):
    def __init__(self, path_file: str) -> None:
        self._namefile: str = None
        self._path_file: str = path_file

    def _exist(self, Target: str) -> bool:
        """
        for checking and confirmation file target are exists.

        :param Target: namefile or pathfile to check the target file are exists.
        :return: boolean True or False.
        """
        if not isinstance(Target, str):
            raise TypeError("target must be string!")

        assert Target != ""

        if os.path.exists(path=Target):
            return True

        return False

    @abstractmethod
    def Read(self, *args, **kwargs) -> ReadHandler:
        """
        Readfile logic.
        """
        return ReadHandler

    @abstractmethod
    def Write(self, *args, **kwargs) -> WriteHandler:
        """
        Writefile logic.
        """
        return WriteHandler
