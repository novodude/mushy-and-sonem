async def h_guilds(params: dict, ctx) -> str:
    guild_names = [guild.name for guild in ctx.bot.guilds]
    return f"I'm in {len(guild_names)} servers: {', '.join(guild_names)}"

TOOLS = {"guilds": h_guilds}