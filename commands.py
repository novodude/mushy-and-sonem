import discord
from discord.ext import commands

# Import all command setups here
from cmd.donut import donut_setup

async def commands_setup(bot: commands.Bot):
    """Setup all commands"""
    await donut_setup(bot)
