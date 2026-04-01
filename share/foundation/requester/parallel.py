import asyncio
import aiohttp
from aiohttp import ClientResponse
from typing import Union


class Response:
    def __init__(self, response: ClientResponse) -> None:
        self._resp = response

    @property
    def json(self):
        return self._resp.json()

    @property
    def text(self):
        return self._resp.text()

    @property
    def status_code(self) -> int | str:
        return self._resp.status


class BaseParallel:
    def __init__(self) -> None:
        self._url: str = None
        self._session: aiohttp.ClientSession = None

    @property
    def get_url(self) -> str:
        return self._url

    @property
    def get_session(self) -> aiohttp.ClientSession:
        return self._session

    def clientSession(*args, **kwargs) -> aiohttp.ClientSession:
        return aiohttp.ClientSession(*args, **kwargs)

    async def open_connection(self, *args, **kwargs) -> aiohttp.ClientSession:
        try:
            if not self._session:
                self._session = self.clientSession(*args, **kwargs)

            async with self._session as session:
                return session
        except Exception as e:
            print(f"[ERROR]: {e}")
            return e

    async def get(self, host: str, *args, **kwargs) -> Response:
        try:
            async with self.open_connection(*args, **kwargs) as session:
                response = await session.get(host)
                return Response(response=response)
        except Exception as e:
            print(f"[ERROR]: {e}")
            return str(e)

    async def post(self, host: str, *args, **kwargs) -> Response:
        try:
            async with self.open_connection(*args, **kwargs) as session:
                response = await session.post(host)
                return Response(response=response)
        except Exception as e:
            print(f"[ERROR]: {e}")
            return str(e)

    async def update(self, host: str, *args, **kwargs) -> Response:
        try:
            async with self.open_connection(*args, **kwargs) as session:
                response = await session.update(host)
                return Response(response=response)
        except Exception as e:
            print(f"[ERROR]: {e}")
            return str(e)

    async def put(self, host: str, *args, **kwargs) -> Response:
        try:
            async with self.open_connection(*args, **kwargs) as session:
                response = await session.put(host)
                return Response(response=response)
        except Exception as e:
            print(f"[ERROR]: {e}")
            return str(e)

    async def delete(self, host: str, *args, **kwargs) -> Response:
        try:
            async with self.open_connection(*args, **kwargs) as session:
                response = await session.delete(host)
                return Response(response=response)
        except Exception as e:
            print(f"[ERROR]: {e}")
            return str(e)


class Parallel(BaseParallel):
    def __init__(self) -> None:
        """Sending some request"""
        super().__init__()

    async def put_image(
        self,
        host: str,
        headers: dict,
        data: dict,
        files: dict,
        retries: int = 3,
        *args,
        **kwargs,
    ) -> Union[str, bool]:
        """
        upload image to web service 'image_hosting'.
        Param:
            host: host or URL endpoint service.
            headers: headers for send data to endpoint.
            data: data is data, needed if service is using data.
            files: where file you want to upload?.
            retries: default is 3, if you want add more, add it.

        Return:
            first is string and second is single boolean.
        """
        try:
            async with self.open_connection(*args, **kwargs) as session:
                response = await session.post(
                    url=host, headers=headers, data=data, files=files, **args**kwargs
                )

                return response
        except Exception as e:
            print("[PARALLEL] Exception occurred: ", str(e))
            return None, False

        except (TimeoutError, ConnectionError):
            print("[PARALLEL] Connection error or timeout error, retrying to connect..")
            asyncio.run(self.put_image(host, headers, data, files, retries - 1))
