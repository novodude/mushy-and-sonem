import json
import os
import asyncio
from datetime import datetime, timedelta
import parsedatetime as pdt
from discord.ext import tasks

# File to store reminders
REMINDERS_FILE = "data/reminders.json"

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# Load reminders from file
def load_reminders():
    if not os.path.exists(REMINDERS_FILE):
        return []
    try:
        with open(REMINDERS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

# Save reminders to file
def save_reminders(reminders):
    try:
        with open(REMINDERS_FILE, "w") as f:
            json.dump(reminders, f, indent=2)
    except IOError as e:
        print(f"Error saving reminders: {e}")

# Parse time string into datetime
async def parse_time(time_str):
    cal = pdt.Calendar()
    time_struct, parse_status = cal.parse(time_str)
    if parse_status:
        return datetime(*time_struct[:6])
    return None

# Check and send reminders
async def check_reminders(bot):
    reminders = load_reminders()
    now = datetime.now()
    updated_reminders = []
    for reminder in reminders:
        reminder_time = datetime.fromisoformat(reminder["time"])
        if reminder_time <= now:
            try:
                channel = bot.get_channel(int(reminder["channel_id"]))
                if channel:
                    await channel.send(f"<@{reminder['user_id']}> Reminder: {reminder['message']}")
                else:
                    print(f"Couldn't find channel {reminder['channel_id']} for reminder")
            except Exception as e:
                print(f"Error sending reminder: {e}")
        else:
            updated_reminders.append(reminder)
    save_reminders(updated_reminders)

# Background task to check reminders
@tasks.loop(minutes=1)
async def reminder_task(bot):
    await check_reminders(bot)

# Set a reminder
async def h_remind(params: dict, ctx) -> str:
    time_str = params.get("time", "")
    message = params.get("message", "")
    if not time_str or not message:
        return "Please provide both time and message! Example: `remind 1 hour Do the thing`"

    reminder_time = await parse_time(time_str)
    if not reminder_time:
        return "Couldn't understand that time format! Try something like 'in 1 hour' or 'tomorrow at 3pm'"

    reminders = load_reminders()
    reminders.append({
        "user_id": str(ctx.message.author.id),
        "time": reminder_time.isoformat(),
        "message": message,
        "channel_id": str(ctx.message.channel.id)
    })
    save_reminders(reminders)

    if not reminder_task.is_running():
        reminder_task.start(ctx.bot)

    return f"I'll remind you about '{message}' at {reminder_time.strftime('%Y-%m-%d %H:%M:%S')}!"

# List all reminders for a user
async def h_list_reminders(params: dict, ctx) -> str:
    reminders = load_reminders()
    user_reminders = [r for r in reminders if r["user_id"] == str(ctx.message.author.id)]
    if not user_reminders:
        return "You have no reminders set!"

    response = "Your reminders:\n"
    for i, reminder in enumerate(user_reminders, 1):
        reminder_time = datetime.fromisoformat(reminder["time"])
        response += f"{i}. {reminder['message']} at {reminder_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
    return response

# Delete a reminder
async def h_delete_reminder(params: dict, ctx) -> str:
    index = params.get("index")
    if index is None:
        return "Please provide a reminder index to delete! Example: `delete_reminder 1`"

    try:
        index = int(index) - 1
    except ValueError:
        return "Index must be a number!"

    reminders = load_reminders()
    user_reminders = [r for r in reminders if r["user_id"] == str(ctx.message.author.id)]
    if not user_reminders or index < 0 or index >= len(user_reminders):
        return "Invalid reminder index!"

    # Find the actual index in the full list
    user_reminder = user_reminders[index]
    full_index = reminders.index(user_reminder)
    del reminders[full_index]
    save_reminders(reminders)
    return "Reminder deleted!"

# Initialize the task when the bot starts
async def setup(bot):
    reminders = load_reminders()
    if reminders and not reminder_task.is_running():
        reminder_task.start(bot)

TOOLS = {
    "remind": h_remind,
    "list_reminders": h_list_reminders,
    "delete_reminder": h_delete_reminder
}