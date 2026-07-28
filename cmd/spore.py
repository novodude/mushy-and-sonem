import discord
from discord import app_commands
from discord.ext import commands
import random

async def spore_setup(bot: commands.Bot):
    """Setup the /spore command for tiny mushroom surprises!"""
    
    @bot.tree.command(name="spore", description="Send a tiny spore cloud with a fun message!")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(user="Who to send the spore to (optional)")
    async def spore(interaction: discord.Interaction, user: discord.User = None):
        await interaction.response.defer()
        
        # Tiny spore messages (fun and cozy!)
        spore_messages = [
            "🍄 *a tiny spore cloud drifts by!* It smells like damp earth and adventure.",
            "✨ *a spore cloud floats gently!* It hums a tiny mushroom lullaby.",
            "🌿 *a spore cloud tickles your nose!* It’s full of tiny secrets.",
            "💨 *a spore cloud dances in the sunlight!* It’s lighter than air.",
            "🍄 *a spore cloud lands on your shoulder!* It whispers, *‘You’re doing great!’*",
            "🌱 *a spore cloud blooms into tiny flowers!* (They’re imaginary.)",
            "🌟 *a spore cloud glows softly!* It’s magic, but don’t tell anyone.",
            "🍄 *a spore cloud bumps into you!* It’s friendly, promise."
        ]
        
        # Special spore messages (rare!)
        special_spores = [
            "🌈 *a RAINBOW spore cloud appears!* It’s as colorful as a mushroom cap. *floats excitedly*",
            "🔥 *a GLOWING spore cloud wraps around you!* It’s warm and smells like cinnamon.",
            "🎶 *a spore cloud hums a tiny tune!* It’s surprisingly catchy.",
            "💖 *a HEART-SHAPED spore cloud floats by!* It’s full of tiny love.",
            "🍄 *a spore cloud with a TINY MUSHROOM inside!* It waves at you. *waves back*"
        ]
        
        # Send to someone else
        if user:
            if user == interaction.user:
                await interaction.followup.send("🍄 *sends a spore cloud to themself*—aww, self-care! *wiggles cap*")
                return
            
            spore_messages = [
                f"🍄 *a tiny spore cloud drifts to {user.mention}!* It smells like damp earth and adventure.",
                f"✨ *a spore cloud floats gently to {user.mention}!* It hums a tiny mushroom lullaby.",
                f"🌿 *a spore cloud tickles {user.mention}’s nose!* It’s full of tiny secrets.",
                f"💨 *a spore cloud dances in the sunlight to {user.mention}!* It’s lighter than air.",
                f"🍄 *a spore cloud lands on {user.mention}’s shoulder!* It whispers, *‘You’re doing great!’*",
                f"🌱 *a spore cloud blooms into tiny flowers for {user.mention}!* (They’re imaginary.)",
                f"🌟 *a spore cloud glows softly for {user.mention}!* It’s magic, but don’t tell anyone.",
                f"🍄 *a spore cloud bumps into {user.mention}!* It’s friendly, promise."
            ]
            special_spores = [
                f"🌈 *a RAINBOW spore cloud appears for {user.mention}!* It’s as colorful as a mushroom cap. *floats excitedly*",
                f"🔥 *a GLOWING spore cloud wraps around {user.mention}!* It’s warm and smells like cinnamon.",
                f"🎶 *a spore cloud hums a tiny tune to {user.mention}!* It’s surprisingly catchy.",
                f"💖 *a HEART-SHAPED spore cloud floats to {user.mention}!* It’s full of tiny love.",
                f"🍄 *a spore cloud with a TINY MUSHROOM inside floats to {user.mention}!* It waves at you. *waves back*"
            ]
        
        # 10% chance for a special spore!
        if random.random() < 0.1:
            await interaction.followup.send(random.choice(special_spores))
        else:
            await interaction.followup.send(random.choice(spore_messages))