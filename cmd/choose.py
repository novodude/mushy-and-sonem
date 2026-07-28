import discord
from discord import app_commands
from discord.ext import commands
import random

async def choose_setup(bot: commands.Bot):
    """Setup the /choose command for picking between options!"""
    
    @bot.tree.command(name="choose", description="Pick between options (separate with commas)")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(options="Options to choose from (e.g., pizza, tacos, sushi)")
    async def choose(interaction: discord.Interaction, options: str):
        await interaction.response.defer()
        
        # Split options by commas, strip whitespace, and filter out empty strings
        choices = [opt.strip() for opt in options.split(",") if opt.strip()]
        
        if len(choices) < 2:
            await interaction.followup.send("❌ You need at least 2 options to choose from!")
            return
        
        result = random.choice(choices)
        await interaction.followup.send(f"🎲 I choose... **{result}**!")
