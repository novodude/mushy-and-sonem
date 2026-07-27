import json
import os
import asyncio
from datetime import datetime, timedelta
import parsedatetime as pdt
from discord.ext import tasks

# File to store reminders
REMINDERS_FILE = "data/reminders.json"

# Create data directory if it doesn't exist
os.makedirs(os.path.dirname(REMINDERS_FILE), exist_ok=True)

# Load reminders from file
async def load_reminders():
    if not os.path.exists(REMINDERS_FILE):
        return []
    with open(REMINDERS_FILE, 'r') as f:
        return json.load(f)

# Save reminders to file
async def save_reminders(reminders):
    with open(REMINDERS_FILE, 'w') as f:
        json.dump(reminders, f)

# Reminder task function
async def check_reminders(bot):
    reminders = await load_reminders()
    now = datetime.now()
    
    for reminder in reminders[:]:
        reminder_time = datetime.fromisoformat(reminder['time'])
        if reminder_time <= now:
            try:
                channel = bot.get_channel(reminder['channel_id'])
                if channel:
                    await channel.send(f"🔔 Reminder for <@{reminder['user_id']}>: {reminder['message']}")
                reminders.remove(reminder)
            except Exception as e:
                print(f"Error sending reminder: {e}")
    
    await save_reminders(reminders)

# Handle remind command
async def h_remind(params: dict, ctx) -> str:
    try:
        cal = pdt.Calendar()
        time_text = ' '.join(params.get('args', []))
        
        # Parse time
        time_struct, parse_status = cal.parse(time_text)
        if not parse_status:
            return "I couldn't understand that time format. Try something like '1 hour' or 'tomorrow at 3pm'"
        
        reminder_time = datetime(*time_struct[:6])
        if reminder_time < datetime.now():
            return "That time is in the past! Try a future time."
        
        # Get message (everything after time)
        message_start = len(' '.join(params.get('time_words', [])))
        message = time_text[message_start:].strip()
        if not message:
            return "You need to tell me what to remind you about!"
        
        # Save reminder
        reminders = await load_reminders()
        reminders.append({
            'user_id': ctx.message.author.id,
            'channel_id': ctx.message.channel.id,
            'time': reminder_time.isoformat(),
            'message': message
        })
        await save_reminders(reminders)
        
        return f"Okay! I'll remind you about '{message}' at {reminder_time.strftime('%Y-%m-%d %H:%M')}"
    except Exception as e:
        return f"Something went wrong: {e}"

# Plugin setup function
async def setup(bot):
    # Create and start the task
    reminder_task = tasks.loop(minutes=1.0)(check_reminders)
    reminder_task.bot = bot
    reminder_task.start()
    print("Reminder task started")
    
    # Store the task in the bot for reference
    bot.reminder_task = reminder_task

TOOLS = {"remind": h_remind}