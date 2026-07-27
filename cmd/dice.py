import discord
from discord import app_commands
from plugins.dice import roll_dice

async def dice_setup(bot):
    @bot.tree.command(name="dice", description="Roll dice! Supports formats like 1d6, 2d20, d100, etc.")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(dice="What dice to roll? (e.g., 1d6, 2d20)")
    async def dice(interaction: discord.Interaction, dice: str):
        await interaction.response.defer()
        result = roll_dice(dice)
        
        if "error" in result:
            await interaction.followup.send(f"❌ {result['error']}")
        else:
            await interaction.followup.send(f"🎲 {result['message']}")
