import discord
from discord import app_commands
import random

async def roll_setup(bot):
    @bot.tree.command(name="roll", description="Roll some dice! 🎲")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(dice="Format like 1d6, 2d20, etc.")
    async def roll(interaction: discord.Interaction, dice: str):
        await interaction.response.defer()
        try:
            num_dice, max_val = map(int, dice.lower().split('d'))
            if num_dice < 1 or max_val < 1:
                raise ValueError
            rolls = [random.randint(1, max_val) for _ in range(num_dice)]
            result = sum(rolls)
            await interaction.followup.send(f"🎲 **Roll result:** {result} (for {dice})\n*Individual rolls: {rolls}*")
        except ValueError:
            await interaction.followup.send("❌ Oops! Use format like `1d6` or `2d20`.")