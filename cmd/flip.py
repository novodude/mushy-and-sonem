import discord
from discord import app_commands
from discord.ext import commands
import random

async def flip_setup(bot: commands.Bot):
    """Setup the /flip command for quick coin flips!"""
    
    @bot.tree.command(name="flip", description="Flip a coin (heads or tails)")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def flip(interaction: discord.Interaction):
        await interaction.response.defer()
        
        result = random.choice(["heads", "tails"])
        emoji = "🪙" if result == "heads" else "🐌"
        
        # Tiny mushroom-themed responses
        responses = [
            f"{emoji} **{result}**! *flips a tiny mushroom-shaped coin*",
            f"{emoji} **{result}**! *the coin lands with a tiny *plink* under the log*",
            f"{emoji} **{result}**! *a tiny mushroom cap wobbles as the coin settles*",
            f"{emoji} **{result}**! *the coin rolls into a patch of moss*",
            f"{emoji} **{result}**! *you hear a faint *clink* from under the log*"
        ]
        
        await interaction.followup.send(random.choice(responses))