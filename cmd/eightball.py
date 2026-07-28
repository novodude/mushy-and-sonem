import discord
from discord import app_commands
from discord.ext import commands
import random

async def eightball_setup(bot: commands.Bot):
    """Setup the /8ball command for mystical mushroom answers!"""
    
    # Mushroom-themed 8ball answers
    answers = [
        "The spores say... **yes!** *floats gently*",
        "My mycelium network whispers... **no.** *sighs*",
        "Ask again after the next rain... *pauses dramatically*",
        "The log spirits agree: **definitely!** *glows faintly*",
        "Not today, little spore... **try again later.**",
        "The wind through the trees says... **yes!** *rustles cap*",
        "My cap is too heavy to decide... **ask again.**",
        "The answer is **yes**, but only if you share a snack. *eyes your sandwich*",
        "The dark under the log says... **no.** *shivers*",
        "**Outlook good!** *bounces slightly*",
        "**Don’t count on it.** *hides under a leaf*",
        "**Signs point to yes!** *points with a tiny stem*",
        "**Very doubtful.** *sneezes (allergies to doubt)*",
        "**You may rely on it!** *nods firmly*",
        "**Better not tell you now.** *whispers* (I forgot)",
        "**Concentrate and ask again.** *stares intently at your soul*",
        "**Mycelium says... yes!** *spreads invisible threads*",
        "**No way.** *crosses tiny mushroom arms*"
    ]

    @bot.tree.command(name="8ball", description="Ask the mystical mushroom a question!")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(question="What do you want to ask the mushroom?")
    async def eightball(interaction: discord.Interaction, question: str):
        await interaction.response.defer()
        
        # Pick a random answer and send it
        answer = random.choice(answers)
        await interaction.followup.send(f"🍄 *You ask:* **{question}**
🍄 *The mushroom replies:* {answer}")