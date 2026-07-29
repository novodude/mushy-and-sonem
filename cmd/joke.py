import discord
from discord import app_commands
import random

async def joke_setup(bot):
    @bot.tree.command(name="joke", description="Tell a random joke!")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def joke(interaction: discord.Interaction):
        await interaction.response.defer()
        
        jokes = [
            "Why don't skeletons fight each other?\nThey don't have the guts.",
            "What do you call a fake noodle?\nAn impasta!",
            "Why did the mushroom go to the party?\nBecause he was a fungi!",
            "Why can't you trust an atom?\nBecause they make up everything!",
            "What's brown and sticky?\nA stick!",
            "Why did the scarecrow win an award?\nBecause he was outstanding in his field!",
            "What do you call cheese that isn't yours?\nNacho cheese!",
            "Why did the bicycle fall over?\nBecause it was two-tired!",
            "What did one wall say to the other wall?\nI'll meet you at the corner!",
            "Why don't eggs tell jokes?\nThey might crack up!"
        ]
        
        selected_joke = random.choice(jokes)
        await interaction.followup.send(selected_joke)