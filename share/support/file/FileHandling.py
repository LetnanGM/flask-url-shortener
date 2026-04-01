from share.contract.file import BaseFileHandler, ReadHandler, WriteHandler


class File(BaseFileHandler):
    def __init__(self, path_file: str) -> None:
        """
        simple file operation
        """
        super().__init__(path_file=path_file)
        self._namefile: str = None
        self._path_file: str = path_file

    @property
    def get_current_file(self) -> str:
        """get current processed file"""
        return self._path_file

    def Read(self, ModeHandler: str = "r") -> ReadHandler:
        """
        Read file making system file handling for reading target file with ModeHandler "r" or "rb".

        :param ModeHandler: Mode file handler,'mode=' argument in open function like 'r' or 'rb'.
        :return: string or list string.
        """

        if not self._exist(Target=self._path_file):
            raise FileNotFoundError("Can't reach where file placed! File not found!")

        # with open(self._path_file, ModeHandler) as fp:
        #    return ReadHandler(fp=fp)

        fp = open(self._path_file, ModeHandler)
        return ReadHandler(fp=fp)  # no close

    def Write(
        self, Message: str | dict, ModeHandler: str = "w", indent: int = 4
    ) -> bool:
        """
        Writer function for writing some message to target or pathfile.

        :param Message: for writing message, we need some message for write to target file.
        :param ModeHandler: like Read function, but we use 'w' or 'wb'.
        :return: boolean True or False.
        """
        if not Message:
            raise TypeError("'message' params must be str or dict! not empty. ")

        if not self._exist(Target=self._path_file):
            raise FileNotFoundError(f"File path '{self._path_file}' are not found!")

        fp = open(self._path_file, ModeHandler)
        if fp:
            return WriteHandler(fp=fp, obj=Message, indent=indent)

        return False
