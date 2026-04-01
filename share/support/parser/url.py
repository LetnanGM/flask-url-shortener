from .url_utils import uri


class URLParse(uri):
    def __init__(self, uri: str | None = ...) -> None:
        """ """
        super().__init__()
        self.parse(uri)

        self._url: str = None
        self._scheme: str = None
        self._netloc: str = None
        self._path: str = None
        self._params: str = None
        self._fragment: str = None

    @property
    def url(self) -> str:
        return self._url

    @property
    def scheme(self) -> str:
        return self._scheme

    @property
    def netloc(self) -> str:
        return self._netloc

    @property
    def path(self) -> str:
        return self._path

    @property
    def params(self) -> str:
        return self._params

    @property
    def fragment(self) -> str:
        return self._fragment

    def parse(self, string: str):
        from urllib.parse import urlparse

        parsed_url = urlparse(string)
        self._scheme = parsed_url.scheme
        self._netloc = parsed_url.netloc
        self._path = parsed_url.path
        self._params = parsed_url.params
        self._fragment = parsed_url.fragment
