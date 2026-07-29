import discord
from discord import app_commands
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from pilmoji import Pilmoji
import io
import textwrap
import random
import os
import math

# 20+ colorful backgrounds with random shapes!
BACKGROUNDS = [
    # Warm tones
    (255, 240, 230),  # peach
    (255, 235, 220),  # warm cream
    (250, 220, 200),  # soft coral
    (240, 210, 190),  # terracotta
    (230, 200, 180),  # toasted almond
    
    # Cool tones
    (230, 240, 255),  # sky blue
    (220, 230, 250),  # powder blue
    (210, 220, 240),  # periwinkle
    (200, 210, 230),  # lavender mist
    (190, 200, 220),  # soft lilac
    
    # Earthy tones
    (240, 250, 230),  # mint cream
    (230, 240, 220),  # sage green
    (220, 230, 210),  # mossy
    (210, 220, 200),  # olive
    (200, 210, 190),  # khaki
    
    # Fun extras
    (255, 250, 240),  # vanilla
    (250, 240, 255),  # lavender
    (240, 255, 250),  # seafoam
    (255, 240, 255),  # cotton candy
    (240, 255, 240),  # pistachio
]

# Tiny mushroom doodles and random shapes!
MUSHROOM_DOODLES = [
    "🍄", "🌱", "✨", "🌿", "☁️", "🍃", "🌲", "🍂",
    "*tiny cap*", "*wobbly stem*", "*spore puff*", "*glowing mycelium*",
    "🔮", "💫", "🌌", "🌠", "🌀", "🎨", "🖌️", "🎨"
]

def draw_random_shapes(draw: ImageDraw.Draw, img_size: tuple):
    """Draw random shapes (circles, blobs, squiggles) on the background!"""
    width, height = img_size
    
    # Draw 5-10 random shapes
    for _ in range(random.randint(5, 10)):
        shape_type = random.choice(["circle", "blob", "squiggle"])
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(10, 50)
        color = (
            random.randint(200, 255),
            random.randint(200, 255),
            random.randint(200, 255)
        )
        opacity = random.randint(50, 150)
        color = (*color, opacity)
        
        if shape_type == "circle":
            draw.ellipse([x, y, x + size, y + size], fill=color)
        elif shape_type == "blob":
            # Draw a blobby shape
            points = []
            for i in range(5):
                angle = 2 * math.pi * i / 5
                radius = size * (0.7 + 0.3 * random.random())
                px = x + radius * math.cos(angle)
                py = y + radius * math.sin(angle)
                points.extend([px, py])
            draw.polygon(points, fill=color)
        elif shape_type == "squiggle":
            # Draw a squiggly line
            points = []
            for i in range(10):
                px = x + random.randint(-size, size)
                py = y + random.randint(-size, size)
                points.extend([px, py])
            draw.line(points, fill=color, width=2)

def create_quote_image(quote: str, author: str = "") -> io.BytesIO:
    """Create a cozy quote image with a tiny mushroom doodle and random shapes!"""
    # Pick a random background and doodle
    bg_color = random.choice(BACKGROUNDS)
    doodle = random.choice(MUSHROOM_DOODLES)
    
    # Create the image
    img = Image.new('RGBA', (800, 400), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw random shapes in the background
    draw_random_shapes(draw, (800, 400))
    
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