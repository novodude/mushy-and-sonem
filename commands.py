from discord.ext import commands
from cmd.donut import donut_setup

async def commands_setup(bot: commands.Bot):
    await donut_setup(bot)
