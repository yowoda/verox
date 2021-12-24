import lightbulb
import verox

example_plugin = lightbulb.Plugin("IPC")


def get_guild_members(context: verox.Context):
    return len(context.bot.cache.get_members_view_for_guild(context.data.guild_id))


def load(bot):
    bot.add_plugin(example_plugin)
    verox.add_endpoint(get_guild_members, bot=bot)
