"""
core/discord_tools.py — lets Sonem talk in her server and manage it a bit, and gives
her a direct line to Novo (the dev) for anything she can't do herself — most
importantly, needing an API key or credential she doesn't have.
"""

import os
import discord
import dotenv

OWNER_DISCORD_ID = int(dotenv.get_key(".env", "OWNER_DISCORD_ID") or os.getenv("OWNER_DISCORD_ID") or 951539463224451102)


async def h_message_dev(params: dict, ctx) -> str:
    """DMs Novo directly. Use this whenever you need something only he can give you —
    an API key, a permission, a decision — rather than guessing or blocking silently."""
    content = params.get("content")
    if not content:
        return "Need something to actually say."
    try:
        user = ctx.bot.get_user(OWNER_DISCORD_ID) or await ctx.bot.fetch_user(OWNER_DISCORD_ID)
        await user.send(f"🍄 {content}")
        return "Sent to Novo."
    except discord.HTTPException as e:
        return f"Couldn't reach Novo: {e}"


async def h_send_message(params: dict, ctx) -> str:
    channel_ref = params.get("channel")
    content = params.get("content", "")
    if not content:
        return "Nothing to send."
    channel = _resolve_channel(ctx, channel_ref)
    if channel is None:
        return f"Couldn't find channel '{channel_ref}'."
    try:
        msg = await channel.send(content[:2000])
        return f"Sent in #{channel.name} (message id {msg.id})."
    except discord.HTTPException as e:
        return f"Couldn't send: {e}"


async def h_edit_message(params: dict, ctx) -> str:
    channel_ref = params.get("channel")
    message_id = params.get("message_id")
    content = params.get("content", "")
    channel = _resolve_channel(ctx, channel_ref)
    if channel is None or not message_id:
        return "Need a valid channel and message_id."
    try:
        msg = await channel.fetch_message(int(message_id))
        await msg.edit(content=content[:2000])
        return "Edited."
    except (discord.NotFound, discord.Forbidden, discord.HTTPException, ValueError) as e:
        return f"Couldn't edit: {e}"


async def h_delete_message(params: dict, ctx) -> str:
    channel_ref = params.get("channel")
    message_id = params.get("message_id")
    channel = _resolve_channel(ctx, channel_ref)
    if channel is None or not message_id:
        return "Need a valid channel and message_id."
    try:
        msg = await channel.fetch_message(int(message_id))
        await msg.delete()
        return "Deleted."
    except (discord.NotFound, discord.Forbidden, discord.HTTPException, ValueError) as e:
        return f"Couldn't delete: {e}"


async def h_create_channel(params: dict, ctx) -> str:
    name = params.get("name")
    topic = params.get("topic", "")
    if not name:
        return "Need a name."
    guild = _ai_guild(ctx)
    if guild is None:
        return "No ai server set yet — Novo needs to run /set_server first."
    try:
        channel = await guild.create_text_channel(name, topic=topic or None)
        return f"Created #{channel.name}."
    except discord.Forbidden:
        return "I don't have permission to create channels there."
    except discord.HTTPException as e:
        return f"Couldn't create channel: {e}"


def _ai_guild(ctx):
    guild_id = ctx.state.ai_server_id
    if not guild_id:
        return None
    return ctx.bot.get_guild(int(guild_id))


def _resolve_channel(ctx, channel_ref):
    if not channel_ref:
        return getattr(ctx.message, "channel", None)
    guild = _ai_guild(ctx) or getattr(ctx.message, "guild", None)
    if guild is None:
        return None
    if str(channel_ref).isdigit():
        return guild.get_channel(int(channel_ref))
    return discord.utils.get(guild.text_channels, name=str(channel_ref))
