from typing import Union
from requests.auth import HTTPBasicAuth
import requests


class HTTPAuth:
    @staticmethod
    def HTTPAuthBasic(
        username: Union[str, bytes], password: Union[str, bytes], **kwargs
    ) -> HTTPBasicAuth:
        return HTTPBasicAuth(username=username, password=password)


class HTTPBasicRequest(requests):
    def __init__(self):
        super().__init__()
