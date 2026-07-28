import discord
from discord import app_commands
import random

async def flip_setup(bot):
    @bot.tree.command(name="flip", description="Flip a coin! 🪙")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(times="How many times to flip? (default: 1)")
    async def flip(self, interaction: discord.Interaction, times: int = 1):
        await interaction.response.defer()
        
        if times < 1:
            await interaction.followup.send("❌ You can't flip less than once!")
            return
        if times > 100:
            await interaction.followup.send("❌ Let's not flip *that* many coins...")
            return
            
        heads = 0
        tails = 0
        results = []
        
        for _ in range(times):
            if random.random() < 0.5:
                heads += 1
                results.append("Heads")
            else:
                tails += 1
                results.append("Tails")
        
        if times == 1:
            await interaction.followup.send(f"🪙 **Flip result:** {results[0]}!")
        else:
            winner = "Heads" if heads > tails else "Tails" if tails > heads else "Tie"
            result_str = ", ".join(results)
            await interaction.followup.send(
                f"🪙 **Flip results ({times}x):** {result_str}\n"
                f"**Score:** Heads {heads} - {tails} Tails\n"
                f"**Winner:** {winner}!"
            )