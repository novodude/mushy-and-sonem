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

# Background task to check reminders
@tasks.loop(minutes=1.0)
async def check_reminders(bot):
    reminders = load_reminders()
    now = datetime.now()
    
    for reminder in reminders[:]:  # Iterate over a copy to allow modification
        reminder_time = datetime.fromisoformat(reminder['time'])
        
        # Check if it's time to send this reminder (now or in the past)
        if reminder_time <= now:
            try:
                user = await bot.get_user(reminder['user_id'])
                if user:
                    channel = None
                    if reminder['channel_id']:
                        channel = await bot.get_channel(reminder['channel_id'])
                    
                    # Send to DM if no channel or channel not found
                    if not channel:
                        await user.send(f"🔔 Reminder: {reminder['message']}")
                    else:
                        await channel.send(f"{user.mention} 🔔 Reminder: {reminder['message']}")
                
                # Remove the reminder after sending
                reminders.remove(reminder)
            except Exception as e:
                print(f"Error sending reminder: {e}")
    
    save_reminders(reminders)

# Setup function to start the background task
async def setup(bot):
    check_reminders.start(bot)

# Tool handler for setting reminders
async def h_remind(params: dict, ctx) -> str:
    try:
        text = params.get('text', '')
        
        # Parse time from natural language
        cal = pdt.Calendar()
        time_struct, parse_status = cal.parse(text)
        
        if not parse_status:
            return "Couldn't understand the time in your reminder. Try something like 'in 5 minutes' or 'tomorrow at 3pm'."
        
        reminder_time = datetime(*time_struct[:6])
        
        # Create reminder object
        reminder = {
            'user_id': ctx.message.author.id,
            'channel_id': ctx.message.channel.id if hasattr(ctx.message.channel, 'id') else None,
            'time': reminder_time.isoformat(),
            'message': text.split(' ', 1)[1] if ' ' in text else 'Reminder!'
        }
        
        # Save reminder
        reminders = load_reminders()
        reminders.append(reminder)
        save_reminders(reminders)
        
        return f"Okay! I'll remind you at {reminder_time.strftime('%Y-%m-%d %H:%M')}"
    except Exception as e:
        return f"Oops! Something went wrong: {str(e)}"

TOOLS = {"remind": h_remind}