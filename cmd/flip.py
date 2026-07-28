import discord
from discord import app_commands
import random

async def flip_setup(bot):
    @bot.tree.command(name="flip", description="Flip a coin! Heads or tails? 🪙")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def flip(interaction: discord.Interaction):
        result = random.choice(["Heads 👑", "Tails 🍃"])
        await interaction.response.defer()
        await interaction.followup.send(f"🪙 The coin landed on... **{result}**!")
