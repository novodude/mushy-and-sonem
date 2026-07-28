import discord
from discord import app_commands
import random

async def eightball_setup(bot):
    @bot.tree.command(name="8ball", description="Ask the magic 8-ball a question! ⚫")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(question="What do you want to ask?")
    async def eightball(interaction: discord.Interaction, question: str):
        await interaction.response.defer()
        responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."
        ]
        answer = random.choice(responses)
        await interaction.followup.send(f"⚫ **Magic 8-Ball says:** {answer}")