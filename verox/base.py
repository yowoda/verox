from __future__ import annotations

import abc
import asyncio
import inspect
import typing as t

import attr

from verox.ux import init_logger

__all__ = [
    "BaseInterface",
    "Context",
    "EndpointCallbackT",
    "Endpoint",
    "Data",
    "maybe_await",
]


class BaseInterface(abc.ABC):
    __slots__ = ("_secret_key", "_host", "_port", "_loop", "_session")

    def __init__(
        self,
        secret_key: str,
        host: str = "localhost",
        port: int = 8080,
        *,
        logs: t.Optional[t.Union[str, int, dict[str, t.Any]]] = "INFO",
    ) -> None:
        self._secret_key = secret_key
        self._host = host
        self._port = port
        self._loop = asyncio.get_event_loop()

        if logs is not None:
            init_logger(logs)

    @abc.abstractmethod
    async def close(self):
        raise NotImplementedError

    @property
    def uri(self) -> str:
        return f"ws://{self._host}:{self._port}"


class Context:
    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)


EndpointCallbackT = t.TypeVar("EndpointCallbackT", bound=t.Callable[[Context], t.Any])


@attr.s(slots=True)
class Endpoint:
    callback: EndpointCallbackT = attr.ib()
    context: Context = attr.ib()


class Data:
    def __init__(self, payload: dict[str, t.Any]) -> None:
        self.payload = payload
        self.endpoint: str = payload["endpoint"]

        self.__dict__.update(payload["data"])

    def __repr__(self) -> str:
        return f"Data({self.payload['data']})"


async def maybe_await(obj: t.Any, *args: t.Any, **kwargs: t.Any) -> t.Any:
    val = obj(*args, **kwargs)
    if inspect.iscoroutine(val):
        val = await val

    return val
