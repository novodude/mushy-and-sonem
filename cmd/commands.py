import discord
from discord.ext import commands

# Import all command setup functions here
from cmd.roll import roll_setup
from cmd.flip import flip_setup

async def commands_setup(bot: commands.Bot):
    """Setup all commands for the bot."""
    await roll_setup(bot)
    await flip_setup(bot)