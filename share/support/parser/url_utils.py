import re
from typing import List


class vmodel:
    SCHEME: List[str] = ["https", "http"]
    PATTERN_URI = re.compile(r"^(https?://|www\.|[\w\-]+\.[a-z]{2,})(/[^\s]*)?$")

    CURRENT_URI: str = ...


class uri:
    def __init__(self) -> None:
        """
        uri utilities
        """
        self._current_url: str = None

    @property
    def get_url(self) -> str:
        """
        history url
        """
        return self._current_url

    def is_url(self, string: str | None = ...) -> bool:
        """
        validating url structure with core question 'is this url?'.

        Params:
            string: your url.

        Returns:
            true if url is url.
        """
        from urllib.parse import urlparse

        if not isinstance(string, str):
            raise TypeError("URL must be string.")

        assert string != ""

        vmodel.CURRENT_URI = string
        parsed_url = urlparse(string)
        if parsed_url.scheme in vmodel.SCHEME:
            return True

        return False
