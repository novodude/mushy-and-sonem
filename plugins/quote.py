# Quote plugin for Sonem
# Features:
# - quote: quotes a message by ID (with optional preview)
# - show_ids: shows message IDs in current channel for easy quoting
# - quote_this: quotes the message being replied to (no ID needed)
# - message IDs now show next to every message automatically!

import discord
from typing import Optional

async def h_show_ids(params: dict, ctx) -> str:
    """Show message IDs in current channel for easy quoting"""
    channel = ctx.message.channel
    messages = [msg async for msg in channel.history(limit=10)]
    
    if not messages:
        return "No messages found in this channel!"
    
    response = "Recent messages with IDs:\n"
    for msg in reversed(messages):
        author = msg.author.display_name
        content = msg.content[:50] + "..." if len(msg.content) > 50 else msg.content
        response += f"`{msg.id}` {author}: {content}\n"
    
    return response

async def h_quote(params: dict, ctx) -> Optional[str]:
    """Quote a message by ID (with optional preview)"""
    message_id = params.get("message_id")
    preview = params.get("preview", False)
    
    if not message_id:
        return "Please provide a message ID to quote!"
    
    try:
        channel = ctx.message.channel
        message = await channel.fetch_message(int(message_id))
        
        if preview:
            # Just show what would be quoted
            author = message.author.display_name
            content = message.content
            return f"Preview of quote for `{message_id}`:\n**{author}**: {content}"
        else:
            # Actually send the quote
            author = message.author.display_name
            content = message.content
            await ctx.bot.send_message(
                channel=channel.name,
                content=f"> **{author}**: {content}\n- *quoted by {ctx.message.author.display_name}*"
            )
            return None
    except (ValueError, discord.NotFound, discord.HTTPException) as e:
        return f"Couldn't quote message: {e}"

async def h_quote_this(params: dict, ctx) -> Optional[str]:
    """Quote the message being replied to (no ID needed)"""
    if not ctx.message.reference:
        return "You need to reply to a message to use quote_this!"
    
    try:
        referenced_msg = await ctx.message.channel.fetch_message(ctx.message.reference.message_id)
        author = referenced_msg.author.display_name
        content = referenced_msg.content
        
        await ctx.bot.send_message(
            channel=ctx.message.channel.name,
            content=f"> **{author}**: {content}\n- *quoted by {ctx.message.author.display_name}*"
        )
        return None
    except (discord.NotFound, discord.HTTPException) as e:
        return f"Couldn't quote that message: {e}"

# Message ID display hook - this will show IDs next to every message!
async def display_message_id(message: discord.Message) -> str:
    """Format message with ID for display"""
    author = message.author.display_name
    content = message.content
    return f"`[{message.id}]` {author}: {content}"

TOOLS = {
    "show_ids": h_show_ids,
    "quote": h_quote,
    "quote_this": h_quote_this
}