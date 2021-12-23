import os

import hikari
from dotenv import load_dotenv
from verox import Server, endpoint

load_dotenv()

bot = hikari.GatewayBot(token=os.environ["TOKEN"], intents=hikari.Intents.ALL)
server = Server(os.environ["APP_SECRET"])


@endpoint()
async def get_guild_ids(_):
    return list(bot.cache.get_available_guilds_view().keys())


server.start()
bot.run()
