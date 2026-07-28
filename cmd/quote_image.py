import discord
from discord import app_commands
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap
import random

# Cozy background colors (like a mushroom's home!)
BACKGROUNDS = {
    "moss": {"color": (50, 70, 40), "text_color": (220, 230, 200)},
    "log": {"color": (80, 50, 30), "text_color": (230, 220, 200)},
    "spore": {"color": (200, 180, 220), "text_color": (60, 40, 80)},
    "sunset": {"color": (120, 60, 80), "text_color": (250, 230, 200)}
}

# Tiny mushroom doodles (simple shapes!)
MUSHROOM_DOODLES = {
    "classic": {
        "cap": (200, 50, 50),
        "stem": (240, 220, 200),
        "spots": [(220, 80, 80)]
    },
    "glow": {
        "cap": (180, 220, 100),
        "stem": (240, 240, 220),
        "spots": [(200, 250, 120)]
    },
    "tiny": {
        "cap": (200, 150, 150),
        "stem": (250, 240, 230),
        "spots": [(220, 180, 180)]
    }
}

def create_quote_image(quote: str, author: str = "") -> io.BytesIO:
    """Create a cozy quote image with a tiny mushroom doodle!"""
    # Image size (Discord-friendly!)
    width, height = 800, 400
    
    # Pick a random background and mushroom
    bg_name = random.choice(list(BACKGROUNDS.keys()))
    bg = BACKGROUNDS[bg_name]
    mushroom = random.choice(list(MUSHROOM_DOODLES.values()))
    
    # Create image
    image = Image.new("RGB", (width, height), bg["color"])
    draw = ImageDraw.Draw(image)
    
    # Try to load a font (fallback to default if not found)
    try:
        font = ImageFont.truetype("arial.ttf", 30)
        small_font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Wrap text to fit
    max_width = width - 100
    avg_char_width = sum(font.getbbox(char)[2] for char in "abcdefghijklmnopqrstuvwxyz") / 26
    max_chars = int(max_width / avg_char_width)
    wrapped_quote = textwrap.fill(quote, width=max_chars)
    
    # Draw quote text
    text_x = width // 2
    text_y = height // 2 - 40
    draw.text((text_x, text_y), wrapped_quote, font=font, fill=bg["text_color"], anchor="mm", align="center")
    
    # Draw author (if provided)
    if author:
        author_text = f"— {author}"
        draw.text((text_x, text_y + 60), author_text, font=small_font, fill=bg["text_color"], anchor="mm", align="center")
    
    # Draw a tiny mushroom doodle in the corner!
    mushroom_x, mushroom_y = 70, height - 70
    
    # Stem
    draw.ellipse([
        (mushroom_x - 10, mushroom_y - 20),
        (mushroom_x + 10, mushroom_y + 20)
    ], fill=mushroom["stem"])
    
    # Cap
    draw.ellipse([
        (mushroom_x - 30, mushroom_y - 40),
        (mushroom_x + 30, mushroom_y - 10)
    ], fill=mushroom["cap"])
    
    # Spots (tiny circles!)
    for i in range(3):
        spot_x = mushroom_x - 20 + (i * 15)
        spot_y = mushroom_y - 30
        draw.ellipse([
            (spot_x - 5, spot_y - 5),
            (spot_x + 5, spot_y + 5)
        ], fill=random.choice(mushroom["spots"]))
    
    # Save to bytes
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="PNG")
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