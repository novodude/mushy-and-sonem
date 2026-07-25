"""
core/self_improvement.py — the actual autonomous loop. Runs on a cooldown (not
tight-looped — that would burn through API calls and give nobody a chance to notice
if something's gone sideways), each cycle bounded to a handful of tool-call rounds.

Anchored on a DM to Novo, same as everything else that needs a real discord.Message
to act through but isn't a reply to anyone.
"""

import os
import dotenv
from discord.ext import commands, tasks

from core.ai import generate_response
from core.tool_parser import parse_response, dispatch_tools
from core.tool_loader import load_tools
from core.persistence import State, save_state

OWNER_DISCORD_ID = int(dotenv.get_key(".env", "OWNER_DISCORD_ID") or os.getenv("OWNER_DISCORD_ID") or 951539463224451102)
CYCLE_MINUTES = int(os.getenv("SONEM_CYCLE_MINUTES", "20"))
MAX_ROUNDS_PER_CYCLE = 8


def _read(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def _build_prompt(state: State) -> list[dict]:
    soul = _read("instructions/SOUL.md")
    mission = _read("instructions/MISSION.md")
    tools_doc = _read("instructions/TOOLS.md")

    pending = [s for s in (state.suggestions or []) if not s.get("done")]
    suggestions_text = "\n".join(f"- (from {s['by']}): {s['text']}" for s in pending[:10]) or "(none pending)"
    log_tail = "\n".join((state.log or [])[-15:]) or "(nothing logged yet)"

    system = f"{soul}\n\n---\n\n{mission}\n\n---\n\n{tools_doc}"
    user = (
        f"## Self-improvement cycle {state.cycle_count}\n\n"
        f"**Status:** {state.status}\n"
        f"**Mood:** {state.mood}\n"
        f"**Current task:** {state.current_task or '(none — pick something)'}\n\n"
        f"**Pending /suggest submissions:**\n{suggestions_text}\n\n"
        f"**Recent activity log:**\n{log_tail}\n\n"
        "Continue or start your work for this cycle. Call `send_message`/`message_dev` "
        "if you want to say something out loud. When you're done for this cycle, say so "
        "and include the literal token [[cycle_done]]."
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


async def _run_cycle(bot: commands.Bot, state: State):
    try:
        owner = bot.get_user(OWNER_DISCORD_ID) or await bot.fetch_user(OWNER_DISCORD_ID)
        anchor = await owner.send(f"-# 🍄 cycle {state.cycle_count} starting — {state.status}")
    except Exception as e:
        print(f"[self_improvement] couldn't DM owner, skipping cycle: {e}")
        return

    registry = load_tools()
    state.cycle_count = (state.cycle_count or 0) + 1

    for _ in range(MAX_ROUNDS_PER_CYCLE):
        messages = _build_prompt(state)
        try:
            response = await generate_response(messages)
        except Exception as e:
            state.log(f"cycle generation failed: {e}")
            break

        text, tools = parse_response(response)
        done = "[[cycle_done]]" in response

        if text.strip():
            state.log(f"(thinking) {text.strip()[:200]}")

        if tools:
            await dispatch_tools(tools, anchor, state, bot, registry, force_owner=True)
            # A plugin may have just been added — reload the registry so this same
            # cycle can use it without waiting for a restart.
            registry = load_tools()

        save_state(state)

        if done or not tools:
            break

    try:
        await owner.send(f"-# 🍄 cycle {state.cycle_count} done for now — {state.status}")
    except Exception:
        pass
    save_state(state)


@tasks.loop(minutes=CYCLE_MINUTES)
async def self_improvement_loop(bot: commands.Bot, state: State):
    await _run_cycle(bot, state)
