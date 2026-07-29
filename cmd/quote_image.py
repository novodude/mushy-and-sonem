import discord
from discord import app_commands
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap
import random

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

async def quote_image_setup(bot: commands.Bot):
    """Setup the /quote_image command!"""
    @bot.tree.command(name="quote_image", description="Turn a quote into a cozy image with a tiny mushroom doodle!")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(quote="The quote to turn into an image", author="Who said it? (optional)")
    async def quote_image(interaction: discord.Interaction, quote: str, author: str = ""):
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
            await interaction.followup.send(f"Oh no! Something went wrong while making the image: {e} *wiggles worriedly* 🍄")