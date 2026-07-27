import json
import os
import asyncio
from datetime import datetime, timedelta
import parsedatetime as pdt
from discord.ext import tasks

# File to store reminders
REMINDERS_FILE = "data/reminders.json"

# Ensure data directory exists
os.makedirs(os.path.dirname(REMINDERS_FILE), exist_ok=True)

# Load reminders from file
def load_reminders():
    try:
        if os.path.exists(REMINDERS_FILE):
            with open(REMINDERS_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading reminders: {e}")
    return []

# Save reminders to file
def save_reminders(reminders):
    try:
        with open(REMINDERS_FILE, 'w') as f:
            json.dump(reminders, f, indent=2)
    except Exception as e:
        print(f"Error saving reminders: {e}")

async def h_remind(params: dict, ctx) -> str:
    """Set a reminder. Parameters: time (str), message (str)"""
    time_str = params.get("time", "")
    message = params.get("message", "")
    
    if not time_str or not message:
        return "Please provide both a time and a message for the reminder."
    
    # Parse the time using parsedatetime
    cal = pdt.Calendar()
    time_struct, parse_status = cal.parse(time_str)
    
    if not parse_status:
        return f"Couldn't understand the time: '{time_str}'. Try something like 'in 1 hour' or 'tomorrow at 3pm'."
    
    # Convert to datetime
    reminder_time = datetime(*time_struct[:6])
    
    # Check if the time is in the past
    if reminder_time < datetime.now():
        return "That time is in the past! Please specify a future time for your reminder."
    
    # Calculate time until reminder
    time_until = reminder_time - datetime.now()
    
    # Create reminder object
    reminder = {
        "user_id": ctx.message.author.id,
        "channel_id": ctx.message.channel.id,
        "time": reminder_time.isoformat(),
        "message": message
    }
    
    # Load existing reminders
    reminders = load_reminders()
    reminders.append(reminder)
    save_reminders(reminders)
    
    return f"Okay! I'll remind you about '{message}' in {time_until.total_seconds()//60} minutes (at {reminder_time.strftime('%Y-%m-%d %H:%M')})."

# Background task to check reminders
@tasks.loop(minutes=1)
async def check_reminders(bot):
    reminders = load_reminders()
    now = datetime.now()
    updated_reminders = []
    
    for reminder in reminders:
        reminder_time = datetime.fromisoformat(reminder["time"])
        if reminder_time <= now:
            # Send reminder
            user = bot.get_user(reminder["user_id"])
            channel = bot.get_channel(reminder["channel_id"]) if reminder["channel_id"] else None
            
            if user:
                try:
                    if channel:
                        await channel.send(f"{user.mention}, reminder: {reminder['message']}")
                    else:
                        await user.send(f"Reminder: {reminder['message']}")
                except Exception as e:
                    print(f"Error sending reminder: {e}")
        else:
            updated_reminders.append(reminder)
    
    # Save updated reminders (without the ones we just sent)
    save_reminders(updated_reminders)

# Start the background task when the bot is ready
async def setup(bot):
    check_reminders.start(bot)

TOOLS = {"remind": h_remind}