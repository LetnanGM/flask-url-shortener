from abc import ABC, abstractmethod


class Storage(ABC):
    def __init__(self, path_db: str | None = ...) -> None:
        self._path_db: str = path_db

    @abstractmethod
    def create_element(self) -> None:
        """create new element object, column"""
        ...

    @abstractmethod
    def update_element(self) -> None:
        """update value of element, like column or table"""
        ...

    @abstractmethod
    def delete_element(self) -> None:
        """delete column or element"""
        ...
