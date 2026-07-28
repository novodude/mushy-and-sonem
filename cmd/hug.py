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
        
        # Hug responses
        hug_messages = [
            "🍄 *sends you a tiny mushroom hug!* The log feels a little warmer now.",
            "💖 *wraps you in a soft mycelium hug!* (It’s surprisingly fluffy.)",
            "✨ *a tiny mushroom cap bumps against your ankle*—that’s a hug!",
            "🌱 *hugs you with a patch of moss!* (It’s very green.)",
            "🍄 *a tiny mushroom friend leans into you*—hug accomplished!"
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
                f"🍄 *a tiny mushroom friend leans into {user.mention}*—hug accomplished!"
            ]
        
        await interaction.followup.send(random.choice(hug_messages))