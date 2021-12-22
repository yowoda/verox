import logging
import typing as t

import aiohttp

from verox import BaseInterface

__all__ = ["Client"]

_LOGGER = logging.getLogger(__name__)


class Client(BaseInterface):
    __slots__ = ("_websocket",)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._websocket = None

    async def init_socket(self) -> None:
        _LOGGER.info("Initializing Websocket Connection")
        session = aiohttp.ClientSession()

        self._websocket = await session.ws_connect(self.uri)
        _LOGGER.info("Connected to %s", self.uri)

    async def request(self, endpoint: str, **kwargs: t.Any) -> t.Any:
        _LOGGER.info("Requesting endpoint %s", endpoint)

        if self._websocket is None:
            await self.init_socket()

        payload = {
            "endpoint": endpoint,
            "data": kwargs,
            "headers": {"Authorization": self._secret_key},
        }

        await self._websocket.send_json(payload)

        recv = await self._websocket.receive()

        return recv.json()
