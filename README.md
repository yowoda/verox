[![PyPI](https://img.shields.io/pypi/v/verox)](https://pypi.org/project/verox)
![Maintenance](https://img.shields.io/maintenance/yes/2022)
![Code Style](https://img.shields.io/badge/code%20style-black-black)

# Verox
Verox (inspired by [discord-ext-ipc](https://github.com/Ext-Creators/discord-ext-ipc)) is an implementation of [IPC](https://en.wikipedia.org/wiki/Inter-process_communication) using websockets.
It's designed to make dashboard development a lot easier and quicker.
While it's aimed at the hikari community, it does not depend on it at all which means you can use it for any discord API wrapper you like.

## Installation
```
pip install verox
```
<details>
<summary>
    Didn't work?
</summary>

- `pip` is not in `PATH`
    ```sh
    python -m pip install verox
    ```

- Check if the path of your python executable matches the path of the interpreter you run your code with<br>
    In UNIX-like systems:
    ```sh
    which python
    ```

</details>

## Usage

Verox is split into client-side and server-side. The client-side is usually the web app, the server-side is the bot.

The following example uses [quart](https://github.com/pgjones/quart) and [hikari](https://github.com/hikari-py/hikari):

`webapp.py`
```py
from quart import Quart
from verox import Client

app = Quart(__name__)
client = Client("your_secret_key")

@app.route("/")
async def home():
    count = await client.request("guild_member_count", guild_id=1234567890)
    return str(count)

@app.after_serving
async def close_client():
    await client.close()

app.run(debug=True)
```

`bot.py`
```py
import hikari
import verox

bot = hikari.GatewayBot(token="your_token", intents=hikari.Intents.ALL)
server = verox.Server("your_secret_key") #must match the secret key of your client

@verox.endpoint()
async def guild_member_count(context: verox.Context):
    return len(bot.cache.get_members_view_for_guild(context.data.guild_id))

@bot.listen()
async def close_server(event: hikari.StoppingEvent):
    await server.close()

server.start()
bot.run()
```

For more advanced examples, please take a look at [examples](examples) and its README