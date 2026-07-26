# plugins/test_channel.py
import discord

async def h_test_channel(params: dict, ctx) -> str:
    """Find a good channel to test commands in"""
    # Try to find the first available text channel
    for channel in ctx.bot.get_all_channels():
        if isinstance(channel, discord.TextChannel) and channel.permissions_for(channel.guild.me).send_messages:
            return f"Found a good test channel: {channel.mention} (id: {channel.id})!"
    return "Couldn't find any text channel I can talk in!"