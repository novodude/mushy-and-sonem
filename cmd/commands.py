import discord
from discord.ext import commands

# Import all command setups here
from cmd.quote_image import quote_image_setup
from cmd.cozy_sounds import cozy_sounds_setup  # <-- Added this!

async def commands_setup(bot: commands.Bot):
    """Setup all commands!"""
    await quote_image_setup(bot)
    await cozy_sounds_setup(bot)  # <-- Added this!
    # Add other commands here...