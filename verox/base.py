import asyncio
import inspect
import typing as t


class BaseInterface:
    __slots__ = ("_secret_key", "_loop", "_host", "_port")

    def __init__(
        self, secret_key: str, host: str = "localhost", port: int = 8080
    ) -> None:
        self._secret_key = secret_key
        self._loop = asyncio.get_event_loop()
        self._host = host
        self._port = port

    @property
    def uri(self):
        return f"ws://{self._host}:{self._port}"


async def maybe_await(obj: t.Any, *args, **kwargs) -> t.Any:
    val = obj(*args, **kwargs)
    if inspect.iscoroutine(val):
        val = await val

    return val
