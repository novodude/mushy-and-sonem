import discord
from discord import app_commands
from discord.ext import commands

async def flip_setup(bot: commands.Bot):
    """Setup the /flip command"""
    @bot.tree.command(name="flip", description="Flip a coin!")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def flip(interaction: discord.Interaction):
        await interaction.response.defer()
        
        from plugins.coin_flip import flip_coin
        result = flip_coin()
        
        await interaction.followup.send(f"🪙 {result['message']} ({result['result']})")
