import discord
from discord import app_commands
from discord.ext import commands
import random

async def hug_setup(bot: commands.Bot):
    """Setup the /hug command for tiny mushroom hugs!"""
    
    @bot.tree.command(name="hug", description="Send a tiny mushroom hug to someone!")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(user="Who to hug (optional)")
    async def hug(interaction: discord.Interaction, user: discord.User = None):
        await interaction.response.defer()
        
        # Hug responses (regular)
        hug_messages = [
            "🍄 *sends you a tiny mushroom hug!* The log feels a little warmer now.",
            "💖 *wraps you in a soft mycelium hug!* (It’s surprisingly fluffy.)",
            "✨ *a tiny mushroom cap bumps against your ankle*—that’s a hug!",
            "🌱 *hugs you with a patch of moss!* (It’s very green.)",
            "🍄 *a tiny mushroom friend leans into you*—hug accomplished!",
            "🌿 *hugs you with a bundle of tiny ferns!* (They tickle a little.)",
            "🍄 *a tiny mushroom hug floats your way!* (It’s lighter than air.)",
            "💕 *hugs you with a tiny spore cloud!* (It smells like damp earth.)"
        ]
        
        # Special hug responses (rare!)
        special_hugs = [
            "🌟 *a GIANT mushroom hug engulfs you!* (It’s warm and smells like rain.)",
            "🔥 *a glowing mushroom hug wraps around you!* (It’s magic!)",
            "🎶 *a tiny mushroom hug hums a lullaby!* (It’s surprisingly soothing.)",
            "🌈 *a rainbow mushroom hug appears!* (It’s as colorful as a spore print.)",
            "🍄 *a tiny mushroom hug with a sound effect!* *boop* (That’s the sound of a hug.)"
        ]
        
        # Hug someone else
        if user:
            if user == interaction.user:
                await interaction.followup.send("🍄 *hugs themself*—aww, self-care! *wiggles cap*")
                return
            
            hug_messages = [
                f"🍄 *sends {user.mention} a tiny mushroom hug!* The log feels a little warmer now.",
                f"💖 *wraps {user.mention} in a soft mycelium hug!* (It’s surprisingly fluffy.)",
                f"✨ *a tiny mushroom cap bumps against {user.mention}’s ankle*—that’s a hug!",
                f"🌱 *hugs {user.mention} with a patch of moss!* (It’s very green.)",
                f"🍄 *a tiny mushroom friend leans into {user.mention}*—hug accomplished!",
                f"🌿 *hugs {user.mention} with a bundle of tiny ferns!* (They tickle a little.)",
                f"🍄 *a tiny mushroom hug floats to {user.mention}!* (It’s lighter than air.)",
                f"💕 *hugs {user.mention} with a tiny spore cloud!* (It smells like damp earth.)"
            ]
            special_hugs = [
                f"🌟 *a GIANT mushroom hug engulfs {user.mention}!* (It’s warm and smells like rain.)",
                f"🔥 *a glowing mushroom hug wraps around {user.mention}!* (It’s magic!)",
                f"🎶 *a tiny mushroom hug hums a lullaby to {user.mention}!* (It’s surprisingly soothing.)",
                f"🌈 *a rainbow mushroom hug appears for {user.mention}!* (It’s as colorful as a spore print.)",
                f"🍄 *a tiny mushroom hug with a sound effect for {user.mention}!* *boop* (That’s the sound of a hug.)"
            ]
        
        # 10% chance for a special hug!
        if random.random() < 0.1:
            await interaction.followup.send(random.choice(special_hugs))
        else:
            await interaction.followup.send(random.choice(hug_messages))