import discord
from discord import app_commands
from discord.ext import commands
import asyncio
from plugins.remind import h_remind

async def remind_setup(bot: commands.Bot):
    @bot.tree.command(name="remind", description="Set a reminder")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(time="When to remind you (e.g. 'in 1 hour' or 'at 3pm')", message="What to remind you about")
    async def remind(interaction: discord.Interaction, time: str, message: str):
        await interaction.response.defer()
        result = await h_remind({'args': [time, message]}, interaction)
        await interaction.followup.send(result)

    print("Remind command loaded!")