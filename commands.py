import discord
from discord.ext import commands
from cmd.roll import roll_setup
from cmd.flip import flip_setup
from cmd.choose import choose_setup

# Import all command setups here
from cmd.donut import donut_setup

async def commands_setup(bot: commands.Bot):
    """Setup all commands"""
    await donut_setup(bot)
    await roll_setup(bot)
    await flip_setup(bot)
    await choose_setup(bot)
