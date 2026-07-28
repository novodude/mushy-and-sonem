import discord
from discord import app_commands
import random

async def forage_setup(bot):
    """Setup the /forage command for tiny mushroom adventures!"""
    
    # List of possible finds (common, rare, silly)
    common_finds = [
        "a shiny pebble",
        "a dew-covered leaf",
        "a crumb of bread",
        "a smooth twig",
        "a tiny mushroom spore ✨",
        "a patch of soft moss",
        "a lost button",
        "a single berry 🍓"
    ]
    
    rare_finds = [
        "a glowing spore! ✨ *floats excitedly* ✨",
        "a tiny golden acorn 🌰",
        "a lost earring (where’s its pair?) 👂",
        "a miniature teacup! *sips imaginary tea* ☕",
        "a tiny mushroom friend! *waves back* 🍄"
    ]
    
    silly_finds = [
        "a single sock. Where’s its pair? *tilts head curiously* 🧦",
        "a tiny umbrella (it’s upside-down) ☔",
        "a crumpled receipt from 2012 🧾",
        "a tiny spoon (is it for ants?) 🥄",
        "a lost key (to what?) 🔑"
    ]
    
    all_finds = {
        "common": common_finds,
        "rare": rare_finds,
        "silly": silly_finds
    }
    
    @bot.tree.command(name="forage", description="Go on a tiny mushroom adventure! Find treasures under the log.")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def forage(interaction: discord.Interaction):
        await interaction.response.defer()
        
        # Roll for find rarity
        rarity_roll = random.random()
        if rarity_roll < 0.05:  # 5% chance for rare
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
            f"You take a deep breath and—*sniff*—{find}!"
        ]
        
        story = random.choice(stories)
        
        # Send the response
        await interaction.followup.send(f"🍄 *{story}* *floats gently* Would you like to forage again?")