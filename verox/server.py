from __future__ import annotations

import functools
import inspect
import logging
import typing as t

import aiohttp

from verox.base import *
from verox.ux import check_for_updates

__all__ = ["endpoint", "add_endpoint", "Server"]

_LOGGER = logging.getLogger(__name__)


def endpoint(
    name: t.Optional[str] = None, **context
) -> t.Callable[[EndpointCallbackT], EndpointCallbackT]:
    def decorator(func: EndpointCallbackT) -> EndpointCallbackT:
        add_endpoint(func, name, **context)

        return func

    return decorator


def add_endpoint(
    func: EndpointCallbackT, name: t.Optional[str] = None, **context
) -> None:
    Server.ENDPOINTS[name or func.__name__] = Endpoint(func, Context(**context))


class Server(BaseInterface):
    __slots__ = "_check_for_updates"
    ENDPOINTS: dict[str, Endpoint] = {}

    def __init__(self, *args, check_for_updates: bool = True, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._check_for_updates = check_for_updates

    async def handle_request(self, request: aiohttp.web_request.Request) -> None:
        websocket = aiohttp.web.WebSocketResponse()
        await websocket.prepare(request)

        async for message in websocket:
            payload = message.json()

            _LOGGER.debug("IPC Server received %r", payload)

            endpoint_name = payload.get("endpoint")
            headers = payload.get("headers")

            if endpoint_name not in self.ENDPOINTS:
                response = {"error": "Requested endpoint not found.", "code": 404}
                _LOGGER.error(response["error"])

            elif not headers or headers.get("Authorization") != self._secret_key:
                response = {"error": "Authorization failed.", "code": 403}
                _LOGGER.error(response["error"])

            else:
                endpoint = self.ENDPOINTS[endpoint_name]
                endpoint.context.data = Data(payload)
                response = await maybe_await(endpoint.callback, endpoint.context)

            await websocket.send_json(response)
            _LOGGER.debug("IPC Server sent %r back", response)

    async def _start_servers(self, app: aiohttp.web.Application) -> None:
        if self._check_for_updates is True:
            await check_for_updates(self._session)

        runner = aiohttp.web.AppRunner(app)
        await runner.setup()

        site = aiohttp.web.TCPSite(runner, self._host, self._port)
        await site.start()

    def start(self) -> None:
        app = aiohttp.web.Application()
        app.router.add_route("GET", "/", self.handle_request)

        self._loop.run_until_complete(self._start_servers(app))
