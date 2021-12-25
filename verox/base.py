from __future__ import annotations

import asyncio
import inspect
import typing as t

import attr

__all__ = [
    "BaseInterface",
    "Context",
    "EndpointCallbackT",
    "Endpoint",
    "Data",
    "maybe_await",
]


class BaseInterface:
    __slots__ = ("_secret_key", "_loop", "_host", "_port")

    def __init__(
        self, secret_key: str, host: str = "localhost", port: int = 8080
    ) -> None:
        self._secret_key = secret_key
        self._loop = asyncio.get_event_loop()
        self._host = host
        self._port = port

    def __new__(cls, *args, **kwargs) -> t.Union[t.NoReturn, BaseInterface]:
        if cls is BaseInterface:
            raise TypeError(f"Can't instantiate {cls.__name__} directly.")

        return super().__new__(cls)

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
