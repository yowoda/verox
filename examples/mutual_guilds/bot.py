import os

import hikari
from dotenv import load_dotenv
import verox

load_dotenv()

bot = hikari.GatewayBot(token=os.environ["TOKEN"], intents=hikari.Intents.ALL)
server = verox.Server(os.environ["APP_SECRET"])


@verox.endpoint()
async def get_guild_ids(_):
    return list(bot.cache.get_available_guilds_view().keys())


server.start()
bot.run()
