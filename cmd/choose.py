import discord
from discord import app_commands
from discord.ext import commands

async def choose_setup(bot: commands.Bot):
    """Setup the /choose command"""
    @bot.tree.command(name="choose", description="Pick between options!")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(options="Comma-separated options (e.g., 'tea, coffee, nap')")
    async def choose(interaction: discord.Interaction, options: str):
        await interaction.response.defer()
        
        from plugins.choose import choose_option
        options_list = [opt.strip() for opt in options.split(",")]
        result = choose_option(options_list)
        
        if "error" in result:
            await interaction.followup.send(f"❌ {result['error']}")
        else:
            await interaction.followup.send(f"✨ {result['message']}")
