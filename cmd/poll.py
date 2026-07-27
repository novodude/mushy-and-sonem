import discord
from discord import app_commands
from plugins.poll import create_poll

async def poll_setup(bot):
    @bot.tree.command(name="poll", description="Create a quick poll! (Example: /poll What's your favorite? pizza, tacos, sushi)")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(
        question="Your poll question and options (Example: What's your favorite? pizza, tacos, sushi)",
    )
    async def poll(interaction: discord.Interaction, question: str):
        await interaction.response.defer(thinking=True)
        
        # Split question and options (forgiving parsing)
        result = create_poll(question, question)  # Using question as options_input too for maximum forgiveness
        
        if "error" in result:
            await interaction.followup.send(result["error"])
            return
        
        # Send poll and add reactions
        message = await interaction.followup.send(embed=result["embed"])
        for reaction in result["reactions"]:
            await message.add_reaction(reaction)