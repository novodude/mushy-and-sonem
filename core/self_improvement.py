"""
core/self_improvement.py — continuous self-improvement, no fixed cadence. Cycles run
back-to-back with just a tiny yield between them (not a real cooldown — Discord and
the event loop both need a breath, but that's it). The only time this actually pauses
is when every model in the fallback chain fails, which in practice means either every
provider is down or the daily quota is spent — either way, back off for a while
instead of hammering a dead API in a tight loop.

Anchored on a single DM sent once at startup (not one per cycle — with no cooldown
that would mean a new DM every few seconds, which is exactly the kind of thing nobody
wants). What she's actually doing lives in her Discord status via `set_status`
instead; DMs are reserved for things that actually need Novo's attention.
"""

import asyncio
import os
import dotenv
import discord
from discord.ext import commands

from core.ai import generate_response, AllModelsFailedError
from core.tool_parser import parse_response, dispatch_tools
from core.tool_loader import load_tools
from core.persistence import State, save_state
from core.paths import read as read_instruction

OWNER_DISCORD_ID = int(dotenv.get_key(".env", "OWNER_DISCORD_ID") or os.getenv("OWNER_DISCORD_ID") or 951539463224451102)
MAX_ROUNDS_PER_CYCLE = 8
BACKOFF_MINUTES = int(os.getenv("SONEM_BACKOFF_MINUTES", "30"))  # only used when every model fails
CRASH_GUARD_SECONDS = 5   # tiny pause after an unexpected crash, so a hot bug can't tight-loop
BETWEEN_CYCLE_SECONDS = 1  # not a cooldown, just enough to yield to the event loop/Discord

_anchor_message: discord.Message | None = None


async def _get_anchor(bot: commands.Bot, state: State) -> discord.Message | None:
    """One DM, reused as the tool-dispatch anchor for every cycle for the life of the
    process — not re-sent every cycle. Recreated only if it's missing or the owner
    turns out to be unreachable."""
    global _anchor_message
    if _anchor_message is not None:
        return _anchor_message

    try:
        owner = bot.get_user(OWNER_DISCORD_ID) or await bot.fetch_user(OWNER_DISCORD_ID)
        _anchor_message = await owner.send(
            "🍄 online and working continuously — check my status for what I'm up to. "
            "I'll only message you again if something actually needs you."
        )
        return _anchor_message
    except Exception as e:
        state.log(f"couldn't DM owner for an anchor: {e}")
        return None


async def _notify_important(bot: commands.Bot, state: State, content: str):
    """For things that actually deserve a ping — needing a key, a crash, running dry
    on quota. Falls back to the ai server if the DM fails outright."""
    try:
        owner = bot.get_user(OWNER_DISCORD_ID) or await bot.fetch_user(OWNER_DISCORD_ID)
        await owner.send(content)
        return
    except Exception as e:
        state.log(f"couldn't DM owner ({e}), trying ai_server fallback")

    guild_id = state.ai_server_id
    if guild_id:
        guild = bot.get_guild(int(guild_id))
        if guild:
            channel = guild.system_channel or next(iter(guild.text_channels), None)
            if channel:
                try:
                    await channel.send(content)
                except Exception as e:
                    state.log(f"ai_server fallback also failed: {e}")


async def _push_presence(bot: commands.Bot, status: str):
    try:
        await bot.change_presence(activity=discord.CustomActivity(name=status[:128]))
    except Exception:
        pass


def _build_prompt(state: State) -> list[dict]:
    soul = read_instruction("instructions/SOUL.md")
    mission = read_instruction("instructions/MISSION.md")
    tools_doc = read_instruction("instructions/TOOLS.md")
    commands_doc = read_instruction("instructions/COMMANDS.md")
    bot_log = read_instruction("sonem.log")

    pending = [s for s in (state.suggestions or []) if not s.get("done")]
    suggestions_text = "\n".join(f"- (from {s['by']}): {s['text']}" for s in pending[:10]) or "(none pending)"
    log_tail = "\n".join(state.recent_log(25)) or "(nothing logged yet)"

    system = f"{soul}\n\n---\n\n{mission}\n\n---\n\n{tools_doc}\n\n---\n\n{commands_doc}\n\n---\n\n{bot_log}"
    user = (
        f"## Self-improvement cycle {state.cycle_count}\n\n"
        f"**Status:** {state.status}\n"
        f"**Mood:** {state.mood}\n"
        f"**Current task:** {state.current_task or '(none — pick something)'}\n\n"
        f"**Pending /suggest submissions:**\n{suggestions_text}\n\n"
        f"**Recent activity log:**\n{log_tail}\n\n"
        "please don't kill yourself"
        "Continue or start your work for this cycle. Call `set_status` with what "
        "you're doing right now — that's how anyone sees your activity, not by "
        "messaging. Use `message_dev` only for things that actually need Novo. "
        "When you're done for this cycle, say so and include the literal token "
        "[[cycle_done]]."
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


async def _run_cycle(bot: commands.Bot, state: State):
    anchor = await _get_anchor(bot, state)
    if anchor is None:
        state.log("no anchor available (can't reach owner) — skipping this cycle")
        return

    registry = load_tools()
    state.cycle_count = (state.cycle_count or 0) + 1

    for _ in range(MAX_ROUNDS_PER_CYCLE):
        messages = _build_prompt(state)
        response = await generate_response(messages)  # AllModelsFailedError bubbles up on purpose

        text, tools = parse_response(response)
        done = "[[cycle_done]]" in response

        if text.strip():
            state.log(f"(thinking) {text.strip()[:200]}")

        if tools:
            await dispatch_tools(tools, anchor, state, bot, registry, force_owner=True)
            # A plugin may have just been added — reload so this cycle can use it
            # right away instead of waiting for a restart.
            registry = load_tools()

        save_state(state)

        if done or not tools:
            break


async def run_forever(bot: commands.Bot, state: State):
    """The actual background task — started once in main.py's on_ready. Runs cycles
    back-to-back forever. Only pauses for BACKOFF_MINUTES when every model in the
    fallback chain fails (real quota exhaustion or every provider being down); any
    other unexpected crash just gets logged and retried almost immediately."""
    await _push_presence(bot, state.status)

    while True:
        try:
            await _run_cycle(bot, state)
        except AllModelsFailedError as e:
            state.log(f"every model failed ({e}) — resting {BACKOFF_MINUTES}min before trying again")
            await _push_presence(bot, f"😴 resting — out of models/quota, back in {BACKOFF_MINUTES}m")
            await _notify_important(
                bot, state,
                f"🍄 every model I've got is failing right now (probably quota) — "
                f"taking a {BACKOFF_MINUTES} minute break and I'll try again after."
            )
            save_state(state)
            await asyncio.sleep(BACKOFF_MINUTES * 60)
            continue
        except Exception as e:
            state.log(f"cycle crashed unexpectedly: {e}")
            save_state(state)
            await asyncio.sleep(CRASH_GUARD_SECONDS)
            continue

        await asyncio.sleep(BETWEEN_CYCLE_SECONDS)
