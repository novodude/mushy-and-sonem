import discord
from discord import app_commands
from plugins.poll import create_poll

async def poll_setup(bot):
    @bot.tree.command(name="poll", description="Create a quick poll!")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(question="What's the poll about?", options="List of options (e.g., 'Minecraft' 'Terraria')")
    async def poll(interaction: discord.Interaction, question: str, options: str):
        await interaction.response.defer()
        
        # Split options into a list
        option_list = options.split('\" \"')
        if len(option_list) < 2:
            option_list = options.split()
        
        # Remove quotes if present
        option_list = [opt.strip('\"') for opt in option_list]
        
        result = create_poll(question, option_list)
        
        if "error" in result:
            await interaction.followup.send(f"❌ {result['error']}")
            return
        
        embed = discord.Embed.from_dict(result["embed"])
        message = await interaction.followup.send(embed=embed)
        
        # Add reactions
        for reaction in result["reactions"]:
            await message.add_reaction(reaction)
        
        # Store poll data in message (for future vote counting)
        bot.polls[message.id] = {
            "embed": result["embed"],
            "reactions": result["reactions"],
            "voters": set()
        }

    @bot.event
    async def on_reaction_add(reaction, user):
        if user.bot:
            return
        
        if reaction.message.id in bot.polls:
            poll_data = bot.polls[reaction.message.id]
            
            # Check if reaction is a poll option
            if str(reaction.emoji) in poll_data["reactions"]:
                # Remove user's previous vote if they voted before
                if user.id in poll_data["voters"]:
                    for emoji in poll_data["reactions"]:
                        async for u in reaction.message.reactions:
                            if str(u.emoji) == emoji:
                                await u.remove(user)
                
                # Add new vote
                poll_data["voters"].add(user.id)
                
                # Update embed with new vote counts
                updated_embed = get_poll_results(poll_data["embed"], [str(r.emoji) for r in reaction.message.reactions])
                await reaction.message.edit(embed=discord.Embed.from_dict(updated_embed["embed"]))
