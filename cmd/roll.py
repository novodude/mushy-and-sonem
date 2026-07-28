import discord
from discord import app_commands
import random

async def roll_setup(bot):
    @bot.tree.command(name="roll", description="Roll some dice! 🎲")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(dice="Format like 2d6 or 1d20 (default: 1d6)")
    async def roll(interaction: discord.Interaction, dice: str = "1d6"):
        await interaction.response.defer()

        # Parse the dice string (like "2d6")
        try:
            num_dice, max_val = map(int, dice.lower().split('d'))
            if num_dice < 1 or max_val < 1:
                raise ValueError
        except ValueError:
            await interaction.followup.send("Hmm, that doesn’t look like dice! Try something like `2d6` or `1d20`.")
            return

        # Roll the dice!
        rolls = [random.randint(1, max_val) for _ in range(num_dice)]
        total = sum(rolls)

        # Format the response
        if num_dice == 1:
            response = f"You rolled a **{total}**! 🎲"
        else:
            rolls_str = ", ".join(str(r) for r in rolls)
            response = f"You rolled: {rolls_str} (total: **{total}**)! 🎲"

        await interaction.followup.send(response)