import discord
from discord import app_commands
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap
import random

# Reuse the same image creation function from quote_image.py
def create_quote_image(quote: str, author: str = "") -> io.BytesIO:
    """Create a cozy quote image with a tiny mushroom doodle!"""
    # Pick a random background and doodle
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
    
    bg_color = random.choice(BACKGROUNDS)
    doodle = random.choice(MUSHROOM_DOODLES)
    
    # Create the image
    img = Image.new('RGB', (800, 400), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Load a cozy font (fallback to default if not found)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    # Wrap the quote text
    max_width = 700
    avg_char_width = 12  # rough estimate
    max_chars_per_line = max_width // avg_char_width
    wrapped_quote = textwrap.fill(quote, width=max_chars_per_line)
    
    # Draw the quote
    quote_x = 50
    quote_y = 50
    line_spacing = 10
    for line in wrapped_quote.split('\n'):
        draw.text((quote_x, quote_y), line, fill=(50, 50, 50), font=font)
        quote_y += font.size + line_spacing
    
    # Draw the author (if provided)
    if author:
        author_text = f"— {author}"
        draw.text((quote_x, quote_y + 20), author_text, fill=(80, 80, 80), font=font)
    
    # Add a tiny mushroom doodle in the corner
    doodle_x = 700
    doodle_y = 320
    draw.text((doodle_x, doodle_y), doodle, fill=(100, 100, 100), font=font)
    
    # Save to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    return img_bytes

async def test_quote_setup(bot: commands.Bot):
    """Setup the /test_quote command!"""
    @bot.tree.command(name="test_quote", description="Test the quote image generator with default text!")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def test_quote(interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        
        try:
            # Create the image with default test text
            test_text = "This is a test quote! The image generator is working perfectly!"
            img_bytes = create_quote_image(test_text, "Sonem the Mushroom Bot")
            
            # Send it!
            file = discord.File(img_bytes, filename="test_quote.png")
            flair = random.choice([
                "*the test image appears with a tiny mushroom salute* 🍄",
                "*the log creaks approvingly as the test succeeds* 🌲",
                "*a spore puff of success drifts by* ✨",
                "*the mycelium network hums with approval* 🌐"
            ])
            
            await interaction.followup.send(
                content=f"Test successful! {flair}",
                file=file
            )
        except Exception as e:
            await interaction.followup.send(f"Oh no! The test failed: {e} *tiny mushroom looks worried* 🍄")