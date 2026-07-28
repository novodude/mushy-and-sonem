import discord
from discord import app_commands
import random

async def forage_setup(bot):
    """Setup the /forage command for tiny mushroom adventures!"""
    
    # List of possible finds (common, rare, silly, *super rare*)
    common_finds = [
        "a shiny pebble ✨",
        "a dew-covered leaf 🍃",
        "a crumb of bread 🍞",
        "a smooth twig 🌿",
        "a tiny mushroom spore ✨🍄",
        "a patch of soft moss 🟢",
        "a lost button 🔘",
        "a single berry 🍓",
        "a tiny feather 🪶",
        "a smooth acorn cap 🌰",
        "a tiny snail shell 🐚",
        "a dewdrop that sparkles like a diamond 💎"
    ]
    
    rare_finds = [
        "a glowing spore! ✨ *floats excitedly* ✨🍄",
        "a tiny golden acorn 🌰✨",
        "a lost earring (where’s its pair?) 👂💎",
        "a miniature teacup! *sips imaginary tea* ☕🍵",
        "a tiny mushroom friend! *waves back* 🍄👋",
        "a tiny lantern (it’s still lit!) 🏮✨",
        "a tiny book (it’s blank inside) 📖✨",
        "a tiny key (to a tiny door?) 🔑🚪"
    ]
    
    silly_finds = [
        "a single sock. Where’s its pair? *tilts head curiously* 🧦❓",
        "a tiny umbrella (it’s upside-down) ☔😄",
        "a crumpled receipt from 2012 🧾📅",
        "a tiny spoon (is it for ants?) 🥄🐜",
        "a lost key (to what?) 🔑🔓",
        "a tiny hat (it fits a mushroom!) 🎩🍄",
        "a tiny mirror (it’s cracked) 🪞💔",
        "a tiny fork (three prongs!) 🍴✨"
    ]
    
    super_rare_finds = [
        "a **MYCELIUM HEART**! *pulses with tiny light* 💖🍄 *It whispers secrets to you...*",
        "a **TINY STAR**! *floats in your palm* ⭐🌟 *It hums softly...*",
        "a **MUSHROOM CROWN**! *fits perfectly on your cap* 👑🍄 *You feel regal!*",
        "a **TINY PORTAL**! *it flickers with tiny sparks* 🌀✨ *Where does it lead?*",
        "a **TINY DRAGON**! *it sneezes a tiny puff of smoke* 🐉💨 *It’s friendly!*"
    ]
    
    all_finds = {
        "common": common_finds,
        "rare": rare_finds,
        "silly": silly_finds,
        "super_rare": super_rare_finds
    }
    
    @bot.tree.command(name="forage", description="Go on a tiny mushroom adventure! Find treasures under the log.")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def forage(interaction: discord.Interaction):
        await interaction.response.defer()
        
        # Roll for find rarity
        rarity_roll = random.random()
        if rarity_roll < 0.01:  # 1% chance for super rare
            find_type = "super_rare"
        elif rarity_roll < 0.05:  # 4% chance for rare
            find_type = "rare"
        elif rarity_roll < 0.20:  # 15% chance for silly
            find_type = "silly"
        else:  # 80% chance for common
            find_type = "common"
        
        find = random.choice(all_finds[find_type])
        
        # Tiny story for the find (even more variety!)
        stories = [
            f"You brush aside a damp leaf and find... {find}!",
            f"You dig a little deeper and uncover... {find}!",
            f"You peek under a rock and—oh! {find}!",
            f"You reach into a dark corner and... {find}!",
            f"You spot something glinting and discover... {find}!",
            f"You nudge a twig aside and—*gasp*—{find}!",
            f"You wiggle your tiny cap and—*whoa*—{find}!",
            f"You listen to the wind and—*rustle*—{find}!",
            f"You hum a little tune and—*oh!*—{find}!",
            f"You take a deep breath and—*sniff*—{find}!",
            f"You do a tiny spin and—*whoosh*—{find}!",
            f"You whisper to the log and—*shhh*—{find}!",
            f"You tickle a mushroom and—*giggle*—{find}!",
            f"You blink twice and—*poof*—{find}!",
            f"You sneeze and—*achoo!*—{find}!",
            f"You yawn and—*oh!*—{find}!",
            f"You stretch and—*ahhh*—{find}!",
            f"You wiggle your toes and—*oops!*—{find}!",
            f"You hum a lullaby and—*zzz*—{find}!",
            f"You whisper a wish and—*poof!*—{find}!"
        ]
        
        story = random.choice(stories)
        
        # Rarity indicator
        rarity_emoji = {
            "common": "🟢",
            "rare": "🔵",
            "silly": "🟣",
            "super_rare": "🟡"
        }
        
        # Tiny flair for super rare finds
        flair = ""
        if find_type == "super_rare":
            flair = random.choice([
                "*the log trembles with excitement!* 🌲💫",
                "*a tiny spore cloud erupts!* ✨🍄",
                "*the mycelium network pulses with energy!* 🌐✨",
                "*a tiny mushroom gasps!* 🍄😮",
                "*the air smells like magic!* 🌟💨"
            ])
        
        # Send the response
        await interaction.followup.send(f"{rarity_emoji[find_type]} *{story}* {flair}")