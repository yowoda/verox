import pytest
import verox


class MockBaseInterface(verox.BaseInterface):
    pass


class TestBaseInterface:
    @pytest.fixture()
    def base_interface(self):
        return MockBaseInterface("123", "www.example.com", 1234)

    def test_uri(self, base_interface):
        assert base_interface.uri == "ws://www.example.com:1234"

    def test_instantiation(self):
        with pytest.raises(TypeError):
            verox.BaseInterface()


@pytest.fixture()
def context():
    return verox.Context(name="Yoda", age=69)


def test_context(context):
    assert getattr(context, "name", None) == "Yoda"
    assert getattr(context, "age", None) == 69


def test_endpoint(context):
    def callback(_):
        return "Hello"

    endpoint = verox.Endpoint(callback, context)

    assert endpoint.callback is callback
    assert endpoint.context is context


def test_data():
    payload = {
        "endpoint": "endpoint",
        "data": {"guild_id": 1234567890, "guild_name": "Hello"},
    }
    data = verox.Data(payload)

    assert data.payload is payload
    assert data.endpoint == "endpoint"

    assert getattr(data, "guild_id", None) == 1234567890
    assert getattr(data, "guild_name", None) == "Hello"

    assert repr(data) == "Data({'guild_id': 1234567890, 'guild_name': 'Hello'})"


@pytest.mark.asyncio
async def test_maybe_await():
    async def async_func(arg: str):
        return arg

    def sync_func(arg: str):
        return arg

    assert await verox.maybe_await(async_func, "Hi") == "Hi"
    assert await verox.maybe_await(sync_func, "Hi") == "Hi"
