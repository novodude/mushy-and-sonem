import discord
from discord import app_commands
from datetime import datetime, timedelta
import asyncio
import dateparser

async def remind_setup(bot):
    @bot.tree.command(name="remind", description="Set a reminder")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(time="When to remind you (e.g. 'in 1 hour' or 'at 3pm tomorrow')", message="What to remind you about")
    async def remind(interaction: discord.Interaction, time: str, message: str):
        await interaction.response.defer(thinking=True)
        
        # Parse the time string
        reminder_time = dateparser.parse(time)
        if not reminder_time:
            await interaction.followup.send("I couldn't understand that time! Try something like 'in 1 hour' or 'at 3pm tomorrow'.")
            return
            
        # Calculate how long until the reminder
        now = datetime.now(reminder_time.tzinfo)
        delta = reminder_time - now
        if delta.total_seconds() <= 0:
            await interaction.followup.send("That time is in the past! I can't remind you about that.")
            return
            
        # Send confirmation
        await interaction.followup.send(f"Okay! I'll remind you about: **{message}** at {reminder_time.strftime('%I:%M %p on %B %d')}")
        
        # Wait until the reminder time
        await asyncio.sleep(delta.total_seconds())
        
        # Send the reminder
        try:
            await interaction.user.send(f"⏰ Reminder: {message}")
        except discord.Forbidden:
            await interaction.followup.send(f"⏰ {interaction.user.mention}, reminder: {message}")
