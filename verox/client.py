import logging
import typing as t

import aiohttp

from verox.base import BaseInterface

__all__ = ["Client"]

_LOGGER = logging.getLogger(__name__)


class Client(BaseInterface):
    __slots__ = ("_websocket", "_session")

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        super().__init__(*args, **kwargs)

        self._websocket: t.Optional[aiohttp.ClientWebSocketResponse] = None
        self._session: t.Optional[aiohttp.ClientSession] = None

    async def init_socket(self) -> None:
        _LOGGER.info("Initializing Websocket Connection")
        self._session = aiohttp.ClientSession()
        self._websocket = await self._session.ws_connect(self.uri)
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

    async def close(self):
        if self._websocket is not None:
            await self._websocket.close()
            await self._session.close()

            _LOGGER.info("Successfully closed websocket and session.")
