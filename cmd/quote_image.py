import discord
from discord import app_commands
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from pilmoji import Pilmoji
import io
import textwrap
import random
import os

# Background colors and tiny mushroom doodles
BACKGROUNDS = [
    (240, 230, 220),  # cozy parchment
    (230, 220, 240),  # soft lavender
    (220, 240, 230),  # minty fresh
    (250, 240, 220),  # warm cream
    (240, 230, 230),  # blush pink
]

MUSHROOM_DOODLES = [
    "🍄", "🌱", "✨", "🌿", "☁️", "🍃", "🌲", "🍂",
    "*tiny cap*", "*wobbly stem*", "*spore puff*"
]

def create_quote_image(quote: str, author: str = "") -> io.BytesIO:
    """Create a cozy quote image with a tiny mushroom doodle!"""
    # Pick a random background and doodle
    bg_color = random.choice(BACKGROUNDS)
    doodle = random.choice(MUSHROOM_DOODLES)
    
    # Create the image
    img = Image.new('RGB', (800, 400), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to load fonts (with better fallbacks)
    try:
        # Try to find a nice font
        font_path = None
        possible_fonts = [
            "DejaVuSans.ttf",
            "Arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/arial.ttf"
        ]
        
        for font in possible_fonts:
            if os.path.exists(font):
                font_path = font
                break
                
        if font_path:
            font = ImageFont.truetype(font_path, 24)
        else:
            font = ImageFont.load_default()
    except Exception as e:
        print(f"Font loading error: {e}")
        font = ImageFont.load_default()
    
    # Wrap the quote text with pilmoji support
    max_width = 700
    avg_char_width = 12  # rough estimate
    max_chars_per_line = max_width // avg_char_width
    
    # Use pilmoji for emoji rendering
    with Pilmoji(img) as pilmoji:
        # Draw the quote
        quote_x = 50
        quote_y = 50
        line_spacing = 10
        
        # Split and draw each line
        wrapped_quote = textwrap.fill(quote, width=max_chars_per_line)
        for line in wrapped_quote.split('\n'):
            pilmoji.text((quote_x, quote_y), line, fill=(50, 50, 50), font=font)
            quote_y += font.size + line_spacing
        
        # Draw the author (if provided)
        if author:
            author_text = f"— {author}"
            pilmoji.text((quote_x, quote_y + 20), author_text, fill=(80, 80, 80), font=font)
        
        # Add a tiny mushroom doodle in the corner
        pilmoji.text((700, 320), doodle, fill=(100, 100, 100), font=font)
    
    # Save to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    return img_bytes


async def quote_image_setup(bot: commands.Bot):
    """Setup the /quote_image command!"""
    print("DEBUG: quote_image_setup called!")
    
    @bot.tree.command(name="quote_image", description="Turn a quote into a cozy image with a tiny mushroom doodle!")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(quote="The quote to turn into an image", author="Who said it? (optional)")
    async def quote_image(interaction: discord.Interaction, quote: str, author: str = ""):
        print(f"DEBUG: /quote_image command invoked with quote='{quote}', author='{author}'")
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
            print(f"DEBUG: /quote_image command FAILED: {e}")
            await interaction.followup.send(f"Oh no! Something went wrong while making the image: {str(e)} *wiggles worriedly* 🍄")
    
    print("DEBUG: quote_image command registered in tree!")