from __future__ import annotations

import inspect
import logging
import typing as t

import aiohttp

from verox import BaseInterface, maybe_await

__all__ = ["endpoint", "Data", "Server"]

_LOGGER = logging.getLogger(__name__)


def endpoint(name: str = None):
    def decorator(func):
        Server.ENDPOINTS[name or func.__name__] = func

        return func

    return decorator


class Data:
    def __init__(self, payload: dict[str, t.Any]) -> None:
        self.payload = payload
        self.endpoint: str = payload["endpoint"]

        for key, value in payload["data"].items():
            setattr(self, key, value)

    def __repr__(self):
        return f"Data({self.payload['data']})"


class Server(BaseInterface):
    __slots__ = ()
    ENDPOINTS: dict[str, t.Coroutine] = {}

    async def handle_request(self, request: aiohttp.web_request.Request) -> None:
        websocket = aiohttp.web.WebSocketResponse()
        await websocket.prepare(request)

        async for message in websocket:
            payload = message.json()

            _LOGGER.debug("IPC Server < %r", payload)

            endpoint = payload.get("endpoint")
            headers = payload.get("headers")

            if endpoint not in self.ENDPOINTS:
                response = {"error": "Requested endpoint not found.", "code": 404}
                _LOGGER.info(response["error"])

            elif not headers or headers.get("Authorization") != self._secret_key:
                response = {"error": "Authorization failed.", "code": 403}
                _LOGGER.info(response["error"])

            else:
                data = Data(payload)
                callback = self.ENDPOINTS[endpoint]
                response = await maybe_await(callback, data)

            await websocket.send_json(response)
            _LOGGER.debug("IPC Server > %r", response)

    async def _start_servers(self, app: aiohttp.web.Application) -> None:
        runner = aiohttp.web.AppRunner(app)
        await runner.setup()

        site = aiohttp.web.TCPSite(runner, self._host, self._port)
        await site.start()

    def start(self):
        app = aiohttp.web.Application()
        app.router.add_route("GET", "/", self.handle_request)

        self._loop.run_until_complete(self._start_servers(app))
