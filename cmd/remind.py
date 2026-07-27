import discord
from discord import app_commands
from discord.ext import commands
import asyncio
from plugins.remind import h_remind, setup

async def remind_setup(bot: commands.Bot):
    @bot.tree.command(name="remind", description="Set a reminder (e.g., 'remind me in 5 minutes to take a break')")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(text="When and what to remind you about")
    async def remind(interaction: discord.Interaction, text: str):
        await interaction.response.defer(thinking=True)
        response = await h_remind({'text': text}, interaction)
        await interaction.followup.send(response)
    
    # Start the background task
    await setup(bot)