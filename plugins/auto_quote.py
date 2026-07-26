# Auto-quote plugin for Sonem
# Features:
# - /quote_this: quotes the message being replied to (with preview)

import discord

async def h_quote_this(params: dict, ctx) -> str:
    # Check if the message is a reply
    if not ctx.message.reference:
        return "❌ You need to reply to a message to use `/quote_this`!"

    # Get the referenced message
    try:
        referenced_msg = await ctx.message.channel.fetch_message(ctx.message.reference.message_id)
    except discord.NotFound:
        return "❌ Couldn't find the message you're replying to!"
    except discord.Forbidden:
        return "❌ I don't have permission to see that message!"

    # Format the quote (same as the regular quote plugin)
    author = referenced_msg.author.display_name
    content = referenced_msg.content
    jump_url = referenced_msg.jump_url
    
    # Truncate long messages
    if len(content) > 200:
        content = content[:200] + "..."
    
    return f"> **{author}:** {content}\n[Jump to message]({jump_url})"

# Listener for on_message (not used yet, but could be for future features)
async def on_message(message: discord.Message):
    pass

TOOLS = {"quote_this": h_quote_this}