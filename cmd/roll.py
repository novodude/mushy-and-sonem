import discord
from discord import app_commands
from discord.ext import commands
import random

async def roll_setup(bot: commands.Bot):
    """Setup the /roll command for dice rolling!"""
    
    @bot.tree.command(name="roll", description="Roll dice (e.g., 1d20, 2d6+3, d100)")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(dice="Dice notation (e.g., 1d20, 2d6+3)")
    async def roll(interaction: discord.Interaction, dice: str):
        await interaction.response.defer()
        
        # TODO: Parse dice notation here
        # For now, just handle simple cases
        if dice.lower() == "d100":
            result = random.randint(1, 100)
            await interaction.followup.send(f"🎲 d100: **{result}**")
            return
        
        # Basic 1dX case
        if dice.lower().startswith("1d"):
            sides = dice[2:]
            try:
                sides = int(sides)
                result = random.randint(1, sides)
                await interaction.followup.send(f"🎲 {dice}: **{result}**")
            except ValueError:
                await interaction.followup.send(f"Hmm, I don't understand '{dice}'. Try something like '1d20' or 'd100'!")
            return
        
        await interaction.followup.send(f"I'm still learning! For now, try '1d20' or 'd100'. More dice types coming soon! *wiggles cap*")
