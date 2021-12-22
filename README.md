# Verox
Verox (inspired by [discord-ext-ipc](https://github.com/Ext-Creators/discord-ext-ipc)) is an implementation of [IPC](https://en.wikipedia.org/wiki/Inter-process_communication) using websockets.
It's designed to make dashboard development a lot easier and quicker.
While it's aimed at the hikari community, it does not depend on it at all which means you can use it for any discord API wrapper you like.

## Installation
```
pip install git+https://github.com/YodaPY/hikari-verox
```

## Usage

Verox is split into client-side and server-side. The client-side is usually the web app, the server-side is the bot.

The following example uses [quart](https://github.com/pgjones/quart) and [hikari](https://github.com/hikari-py/hikari)

`webapp.py`
```py
from quart import Quart
from verox import Client

app = Quart(__name__)
client = Client("your_secret_key")

@app.route("/")
async def lol():
    count = await client.request("guild_member_count", guild_id=1234567890)
    return str(count)

app.run(debug=True)
```

`bot.py`
```py
import hikari

from verox import Server, endpoint

bot = hikari.GatewayBot(token="your_token", intents=hikari.Intents.GUILD_MEMBERS)
server = Server("your_secret_key") #must match the secret key of your client

@endpoint()
async def guild_member_count(data):
    return len(bot.cache.get_members_view_for_guild(data.guild_id))

server.start()
bot.run()
```