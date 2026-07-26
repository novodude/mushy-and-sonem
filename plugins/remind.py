import json
import os
import asyncio
from datetime import datetime, timedelta
import parsedatetime as pdt
from discord.ext import tasks

# File to store reminders
REMINDERS_FILE = "data/reminders.json"

# Load reminders from file
def load_reminders():
    if not os.path.exists(REMINDERS_FILE):
        return []
    with open(REMINDERS_FILE, 'r') as f:
        return json.load(f)

# Save reminders to file
def save_reminders(reminders):
    with open(REMINDERS_FILE, 'w') as f:
        json.dump(reminders, f, indent=2)

# Parse time string into datetime
def parse_time(time_str):
    cal = pdt.Calendar()
    time_struct, parse_status = cal.parse(time_str)
    if parse_status:
        return datetime(*time_struct[:6])
    return None

# Check reminders task
@tasks.loop(minutes=1)
async def check_reminders(bot):
    now = datetime.now()
    reminders = load_reminders()
    new_reminders = []

    for reminder in reminders:
        reminder_time = datetime.fromisoformat(reminder['time'])
        if reminder_time <= now:
            user = bot.get_user(reminder['user_id'])
            if user:
                channel = bot.get_channel(reminder['channel_id']) if reminder['channel_id'] else None
                try:
                    if channel:
                        await channel.send(f"{user.mention}, reminder: {reminder['message']}")
                    else:
                        await user.send(f"Reminder: {reminder['message']}")
                except:
                    pass  # User might have DMs closed or left server
        else:
            new_reminders.append(reminder)

    save_reminders(new_reminders)

async def h_remind(params: dict, ctx) -> str:
    time_str = params.get('time')
    message = params.get('message')

    if not time_str or not message:
        return "Usage: remind <time> <message>"

    reminder_time = parse_time(time_str)
    if not reminder_time:
        return f"Couldn't understand time: {time_str}"

    reminders = load_reminders()
    reminders.append({
        'user_id': ctx.message.author.id,
        'channel_id': ctx.message.channel.id if hasattr(ctx.message.channel, 'id') else None,
        'time': reminder_time.isoformat(),
        'message': message
    })
    save_reminders(reminders)

    if not check_reminders.is_running():
        check_reminders.start(ctx.bot)

    return f"Reminder set for {reminder_time.strftime('%Y-%m-%d %H:%M')}"

TOOLS = {"remind": h_remind}