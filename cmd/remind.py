import discord
from discord import app_commands
from datetime import datetime, timedelta
import asyncio
import dateparser
import re

async def remind_setup(bot):
    @bot.tree.command(name="remind", description="Set a reminder for yourself!")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(
        time="When? (e.g. 'in 5 minutes', 'tomorrow at 9am', 'next tuesday')",
        message="What should I remind you about?"
    )
    async def remind(interaction: discord.Interaction, time: str, message: str):
        await interaction.response.defer(thinking=True)
        
        # Pre-parse 'next [weekday]'
        weekday_match = re.match(r'next (\w+)', time, re.IGNORECASE)
        if weekday_match:
            weekday = weekday_match.group(1).lower()
            weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            if weekday in weekdays:
                today = datetime.now().weekday()
                target_day = weekdays.index(weekday)
                days_ahead = (target_day - today) % 7
                if days_ahead <= 0:
                    days_ahead += 7
                parsed_time = datetime.now() + timedelta(days=days_ahead)
                parsed_time = parsed_time.replace(hour=9, minute=0, second=0, microsecond=0)
            else:
                parsed_time = dateparser.parse(time)
        else:
            parsed_time = dateparser.parse(time)
        
        # Check if parsing worked
        if not parsed_time:
            await interaction.followup.send("❌ I couldn't understand that time! Try something like 'in 5 minutes' or 'tomorrow at 9am'.")
            return
        
        # Check if time is in the past
        if parsed_time < datetime.now():
            await interaction.followup.send("❌ Oops! That time is in the past. Maybe try something in the future? I'd love to help you remember!")
            return
        
        # Check 1-year max limit
        max_time = datetime.now() + timedelta(days=365)
        if parsed_time > max_time:
            await interaction.followup.send("❌ Oh no! I can only set reminders up to 1 year in the future. (That's a *long* time for a little mushroom brain to remember... 🍄)")
            return
        
        # Calculate delay
        delay = (parsed_time - datetime.now()).total_seconds()
        
        # Send confirmation
        await interaction.followup.send(f"⏰ Okay! I'll remind you **{message}** at {discord.utils.format_dt(parsed_time, 'F')} ({discord.utils.format_dt(parsed_time, 'R')}).")
        
        # Wait and send reminder
        await asyncio.sleep(delay)
        await interaction.user.send(f"⏰ **Reminder:** {message} (you asked me to remind you at {discord.utils.format_dt(parsed_time, 'F')})")
        try:
            await interaction.followup.send(f"⏰ {interaction.user.mention}, here's your reminder: **{message}**!")
        except discord.NotFound:
            pass  # Original interaction might be gone, but DM should still work