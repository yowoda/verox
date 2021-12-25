import verox


def get_guild_members(context: verox.Context):
    return len(context.bot.cache.get_members_view_for_guild(context.data.guild_id))


def load(bot):  # function name depends on the library you're using it with
    verox.add_endpoint(get_guild_members, bot=bot)
