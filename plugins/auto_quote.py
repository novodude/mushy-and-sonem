# plugins/auto_quote.py
import discord

async def h_auto_quote(params: dict, ctx) -> None:
    # This is a listener, not a command—no return needed.
    pass

async def on_message(message: discord.Message, bot):
    if message.reference and not message.author.bot:
        ref_msg = await message.channel.fetch_message(message.reference.message_id)
        quote = f"> **{ref_msg.author.display_name}:** {ref_msg.content}\n"
        await message.channel.send(quote + message.content)
        await message.delete()  # Remove the original to avoid duplication

TOOLS = {}  # No commands, just the listener
LISTENERS = {"on_message": on_message}