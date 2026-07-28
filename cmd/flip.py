import discord
from discord import app_commands
from discord.ext import commands
import random

async def flip_setup(bot: commands.Bot):
    """Setup the /flip command for coin flips!"""
    
    @bot.tree.command(name="flip", description="Flip a coin (heads or tails)")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def flip(interaction: discord.Interaction):
        await interaction.response.defer()
        
        result = random.choice(["heads", "tails"])
        emoji = "🪙" if result == "heads" else "🐌"
        await interaction.followup.send(f"{emoji} **{result.upper()}!**")
