import discord
from discord import app_commands
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap
import random
import sys

print("DEBUG: quote_image.py module loaded!", file=sys.stderr)  # <-- Added super obvious debug

# [previous BACKGROUNDS and MUSHROOM_DOODLES definitions remain exactly the same...]

def create_quote_image(quote: str, author: str = "") -> io.BytesIO:
    """Create a cozy quote image with a tiny mushroom doodle!"""
    # [previous create_quote_image function remains exactly the same...]

async def quote_image_setup(bot: commands.Bot):
    """Setup the /quote_image command!"""
    print("DEBUG: quote_image_setup called! Checking if bot is ready...")  # <-- More obvious debug
    print(f"DEBUG: bot.ready: {bot.is_ready()}")  # <-- Check bot state
    
    @bot.tree.command(name="quote_image", description="Turn a quote into a cozy image with a tiny mushroom doodle!")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(quote="The quote to turn into an image", author="Who said it? (optional)")
    async def quote_image(interaction: discord.Interaction, quote: str, author: str = ""):
        print(f"DEBUG: quote_image command called with quote: {quote}")  # <-- Added debug print
        await interaction.response.defer(thinking=True)
        
        try:
            # Create the image
            img_bytes = create_quote_image(quote, author)
            
            # Send it!
            file = discord.File(img_bytes, filename="quote.png")
            flair = random.choice([
                "*a tiny mushroom cap wobbles as the image appears* 🍄",
                "*the mycelium network pulses with creativity* 🌐",
                "*a spore drifts into the sunlight* ✨",
                "*the log creaks softly as the image renders* 🌲"
            ])
            
            await interaction.followup.send(
                content=f"Here's your cozy quote image! {flair}",
                file=file
            )
        except Exception as e:
            print(f"DEBUG: quote_image error: {e}")  # <-- Added debug print
            await interaction.followup.send(f"Oh no! Something went wrong while making the image: {e} *wiggles worriedly* 🍄")