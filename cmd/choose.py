import discord
from discord import app_commands
from discord.ext import commands
import random

# Tiny cache to remember last options per user
last_options = {}

async def choose_setup(bot: commands.Bot):
    """Setup the /choose command with reset button!"""
    @bot.tree.command(name="choose", description="Pick randomly from a list of options")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(options="Comma-separated list of options")
    async def choose(interaction: discord.Interaction, options: str):
        choices = [opt.strip() for opt in options.split(",")]
        if len(choices) < 2:
            await interaction.response.send_message("You need at least two options to choose from!", ephemeral=True)
            return

        # Remember these options for reset
        last_options[interaction.user.id] = choices

        # Create reset button
        view = discord.ui.View()
        reset_button = discord.ui.Button(label="Reset", style=discord.ButtonStyle.secondary, emoji="🔄")
        async def reset_callback(interaction: discord.Interaction):
            if interaction.user.id in last_options:
                del last_options[interaction.user.id]
            await interaction.response.send_message("Options cleared! Use `/choose` again to start fresh.", ephemeral=True)
        reset_button.callback = reset_callback
        view.add_item(reset_button)

        await interaction.response.send_message(f"I choose: **{random.choice(choices)}**", view=view)
