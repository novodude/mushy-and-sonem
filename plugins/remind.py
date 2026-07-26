import json
import os
import asyncio
from datetime import datetime, timedelta
import parsedatetime as pdt
from discord.ext import tasks

# File to store reminders
REMINDERS_FILE = "data/reminders.json"

# Load reminders from file
async def load_reminders():
    if not os.path.exists(REMINDERS_FILE):
        return []
    with open(REMINDERS_FILE, "r") as f:
        return json.load(f)

# Save reminders to file
async def save_reminders(reminders):
    os.makedirs(os.path.dirname(REMINDERS_FILE), exist_ok=True)
    with open(REMINDERS_FILE, "w") as f:
        json.dump(reminders, f, indent=2)

# Parse time string into datetime
async def parse_time(time_str, reference_time=None):
    if reference_time is None:
        reference_time = datetime.now()
    
    cal = pdt.Calendar()
    time_struct, parse_status = cal.parse(time_str, reference_time)
    
    if parse_status == 0:
        return None  # Couldn't parse
    
    return datetime(*time_struct[:6])

# Check reminders task
@tasks.loop(minutes=1.0)
async def check_reminders(bot):
    reminders = await load_reminders()
    now = datetime.now()
    due_reminders = []
    
    # Find due reminders
    for reminder in reminders:
        if datetime.fromisoformat(reminder["time"]) <= now:
            due_reminders.append(reminder)
    
    # Remove due reminders from list
    reminders = [r for r in reminders if r not in due_reminders]
    await save_reminders(reminders)
    
    # Send due reminders
    for reminder in due_reminders:
        try:
            user = await bot.fetch_user(reminder["user_id"])
            channel = bot.get_channel(reminder["channel_id"]) if reminder["channel_id"] else None
            
            message = f"⏰ **Reminder!** {reminder['message']}"
            if channel:
                await channel.send(f"{user.mention} {message}")
            else:
                await user.send(message)
        except Exception as e:
            print(f"Failed to send reminder: {e}")

# Start the reminder checker when bot is ready
async def start_reminder_checker(bot):
    check_reminders.start(bot)

# Handler for /remind command
async def h_remind(params: dict, ctx) -> str:
    time_str = params.get("time")
    message = params.get("message")
    channel_id = params.get("channel_id")  # Optional: if not provided, DM the user
    
    if not time_str or not message:
        return "Please provide both a time and a message! Example: `/remind me in 1 hour to water my plants`"
    
    # Parse the time
    reminder_time = await parse_time(time_str)
    if not reminder_time:
        return f"Couldn't understand the time: '{time_str}'. Try something like 'in 1 hour' or 'tomorrow at 3pm'"
    
    # Create reminder
    reminder = {
        "user_id": ctx.message.author.id,
        "channel_id": channel_id,
        "time": reminder_time.isoformat(),
        "message": message
    }
    
    # Save reminder
    reminders = await load_reminders()
    reminders.append(reminder)
    await save_reminders(reminders)
    
    # Calculate time until reminder
    time_diff = reminder_time - datetime.now()
    total_seconds = int(time_diff.total_seconds())
    
    # Handle tiny time differences
    if total_seconds < 60:
        return "⏰ I'll remind you in less than a minute!"
    
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    
    time_str = ""
    if time_diff.days > 0:
        time_str += f"{time_diff.days} day{'s' if time_diff.days != 1 else ''} "
    if hours > 0:
        time_str += f"{hours} hour{'s' if hours != 1 else ''} "
    if minutes > 0:
        time_str += f"{minutes} minute{'s' if minutes != 1 else ''}"
    
    return f"⏰ I'll remind you in {time_str.strip()}!"

# Handler to list your reminders
async def h_my_reminders(params: dict, ctx) -> str:
    reminders = await load_reminders()
    user_reminders = [r for r in reminders if r["user_id"] == ctx.message.author.id]
    
    if not user_reminders:
        return "You don't have any reminders set!"
    
    response = "**Your reminders:**\n"
    for i, reminder in enumerate(user_reminders, 1):
        time = datetime.fromisoformat(reminder["time"])
        time_str = time.strftime("%Y-%m-%d %H:%M")
        response += f"{i}. {time_str}: {reminder['message']}\n"
    
    return response

# Handler to delete a reminder
async def h_delete_reminder(params: dict, ctx) -> str:
    index = params.get("index")
    if index is None:
        return "Please provide the number of the reminder to delete!"
    
    try:
        index = int(index) - 1
    except ValueError:
        return "That's not a valid number!"
    
    reminders = await load_reminders()
    user_reminders = [r for r in reminders if r["user_id"] == ctx.message.author.id]
    
    if index < 0 or index >= len(user_reminders):
        return "That's not a valid reminder number!"
    
    # Find the actual reminder in the full list
    reminder_to_delete = user_reminders[index]
    reminders = [r for r in reminders if r != reminder_to_delete]
    await save_reminders(reminders)
    
    return "✅ Reminder deleted!"

TOOLS = {
    "remind": h_remind,
    "my_reminders": h_my_reminders,
    "delete_reminder": h_delete_reminder
}

# Start the reminder checker when the bot starts
async def setup(bot):
    await start_reminder_checker(bot)