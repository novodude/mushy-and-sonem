import discord
from discord import app_commands
from discord.ext import commands

async def roll_setup(bot: commands.Bot):
    """Setup the /roll command"""
    @bot.tree.command(name="roll", description="Roll XdY dice (e.g. 2d6)")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(dice="Number and type of dice (e.g. 2d6)")
    async def roll(interaction: discord.Interaction, dice: str):
        await interaction.response.defer()
        
        # Parse dice notation
        try:
            count, sides = map(int, dice.lower().split('d'))
        except ValueError:
            await interaction.followup.send("Use format like '2d6' or '1d20'!")
            return
        
        # Import and use the plugin
        from plugins.dice_roll import roll_dice
        result = roll_dice(count, sides)
        
        if "error" in result:
            await interaction.followup.send(result["error"])
            return
        
        # Format response
        rolls_str = ", ".join(map(str, result["rolls"]))
        response = f"🎲 Rolled {dice}: {rolls_str} (Total: {result['total']})"
        if result["flair"]:
            response += f"\n{result['flair']}"
        
        await interaction.followup.send(response)
