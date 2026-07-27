from discord.ext import commands
from cmd.donut import donut_setup
from cmd.remind import remind_setup

async def commands_setup(bot: commands.Bot):
    await donut_setup(bot)
    await remind_setup(bot)