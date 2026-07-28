import discord
from discord import app_commands
from discord.ext import commands
import os

# Cozy sound options (with emoji flair!)
SOUNDS = {
    "rain": {
        "file": "assets/sounds/rain.mp3",
        "emoji": "☔",
        "flair": "*rain patters on the log above you*"
    },
    "fire": {
        "file": "assets/sounds/fire.mp3",
        "emoji": "🔥",
        "flair": "*a tiny campfire crackles in a mushroom cap*"
    },
    "log": {
        "file": "assets/sounds/log_creaks.mp3",
        "emoji": "🌲",
        "flair": "*the log creaks softly—home sweet home*"
    },
    "wind": {
        "file": "assets/sounds/wind.mp3",
        "emoji": "🌬️",
        "flair": "*wind rustles through the forest*"
    },
    "mushroom": {
        "file": "assets/sounds/mushroom.mp3",
        "emoji": "🍄",
        "flair": "*a spore goes 'plink' somewhere nearby*"
    }
}

async def cozy_sounds_setup(bot: commands.Bot):
    """Setup the /cozy_sounds command!"""
    
    @bot.tree.command(name="cozy_sounds", description="Play cozy sounds to relax with! 🍄")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(sound="Which sound would you like?", duration="How long to play (minutes, optional)")
    async def cozy_sounds(interaction: discord.Interaction, sound: str, duration: int = 1):
        await interaction.response.defer(thinking=True)
        
        # Check if sound exists
        if sound.lower() not in SOUNDS:
            options = ", ".join(SOUNDS.keys())
            await interaction.followup.send(f"Oh no! I don’t know that sound. Try one of these: {options} *wiggles worriedly* 🍄")
            return
            
        sound_data = SOUNDS[sound.lower()]
        
        # Check if file exists (placeholder if not)
        if not os.path.exists(sound_data["file"]):
            await interaction.followup.send(f"{sound_data['emoji']} *{sound_data['flair']}* (Sorry, the sound file is missing! I’ll fix this soon!) 🍄")
            return
        
        # Send the sound!
        file = discord.File(sound_data["file"])
        await interaction.followup.send(
            content=f"{sound_data['emoji']} {sound_data['flair']} (Playing for {duration} minute{'s' if duration != 1 else ''}!)",
            file=file
        )
    
    @bot.tree.command(name="cozy_stop", description="Stop the cozy sounds if they’re playing!")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def cozy_stop(interaction: discord.Interaction):
        await interaction.response.send_message("*the sounds fade away softly* 🍄")