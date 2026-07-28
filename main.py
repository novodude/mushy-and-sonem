import asyncio
import importlib
import re
import sys
import traceback
import logging
import os

import discord
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv

from core.persistence import load_state, save_state
from core.tool_loader import load_tools
from core.tool_parser import parse_response, dispatch_tools
from core.ai import generate_response, AllModelsFailedError
from core.self_improvement import run_forever
from core.paths import read as read_instruction


load_dotenv()

OWNER_DISCORD_ID = int(os.getenv("OWNER_DISCORD_ID", "951539463224451102"))
TOKEN = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename="sonem.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree


state = load_state()
_self_improvement_task: asyncio.Task | None = None


@tasks.loop(seconds=60)
async def autosave_loop():
    try:
        save_state(state)
    except Exception as e:
        print(f"[main] autosave failed: {e}")


@bot.event
async def on_ready():
    global _self_improvement_task
    try:
        await commands_setup(bot)
    except Exception as e:
        error = f"faild to load the bot | {e}"
        state.log(error)       

    await tree.sync()
    if not autosave_loop.is_running():
        autosave_loop.start()
    if _self_improvement_task is None or _self_improvement_task.done():
        _self_improvement_task = asyncio.create_task(run_forever(bot, state))
    try:
        await bot.change_presence(activity=discord.CustomActivity(name=state.status[:128]))
    except Exception as e:
        print(f"[main] couldn't set initial presence: {e}")
    state.log(f"woke up as {bot.user}")
    print(f"Logged in as {bot.user} (ID: {bot.user.id}) — self-improvement running continuously, no cooldown")


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user or bot.user is None:
        return
    if bot.user not in message.mentions:
        return

    async with message.channel.typing():
        soul = read_instruction("instructions/SOUL.md")
        mission = read_instruction("instructions/MISSION.md")
        tools_doc = read_instruction("instructions/TOOLS.md")
        commands_doc = read_instruction("instructions/COMMANDS.md")

        system = f"{soul}\n\n---\n\n{mission}\n\n---\n\n{commands_doc}"
        user_content = (
            f"**Status:** {state.status} | **Mood:** {state.mood}\n\n"
            f"(message id: {message.id}, channel: #{message.channel.name if hasattr(message.channel, 'name') else 'DM'})\n"
            f"{message.author.display_name}: {message.content}"
        )

        try:
            response = await generate_response(
                [{"role": "system", "content": system}, {"role": "user", "content": user_content}]
            )
        except AllModelsFailedError as e:
            await message.channel.send("-# every model I've got is down (or I'm out of quota) right now, sorry :(")
            state.log(f"chat generation failed, all models exhausted: {e}")
            return

        text, tools = parse_response(response)
        if text.strip():
            await message.channel.send(text[:2000])

        if tools:
            registry = load_tools()
            await dispatch_tools(tools, message, state, bot, registry, force_owner=False)

    await bot.process_commands(message)


@tree.command(name="suggest", description="Suggest a feature for Sonem to add")
@app_commands.describe(feature="What should Sonem add or fix?")
async def suggest(interaction: discord.Interaction, feature: str):
    state.add_suggestion(str(interaction.user), feature)
    save_state(state)
    await interaction.response.send_message(
        f"🍄 got it — added to the pile! I'll take a look next time I'm working on myself.",
        ephemeral=True,
    )
    state.log(f"suggestion from {interaction.user}: {feature}")


@tree.command(name="set_server", description="(Novo only) set this server as Sonem's ai server")
async def set_server(interaction: discord.Interaction):
    if interaction.user.id != OWNER_DISCORD_ID:
        await interaction.response.send_message("this one's not for you 🍄", ephemeral=True)
        return
    if interaction.guild is None:
        await interaction.response.send_message("this only works inside a server.", ephemeral=True)
        return

    state.ai_server_id = interaction.guild_id
    save_state(state)
    state.log(f"ai server set to {interaction.guild.name} ({interaction.guild_id})")
    await interaction.response.send_message(f"this is home now — set **{interaction.guild.name}** as my ai server.")


async def _install_shutdown_save():
    loop = asyncio.get_running_loop()
    import signal

    async def _save_and_close():
        save_state(state)
        await bot.close()

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, lambda: asyncio.ensure_future(_save_and_close()))
        except NotImplementedError:
            pass


MAX_IMPORT_RETRIES = 10


def _extract_failing_file(tb: str) -> str | None:
    """Pull the last local (non-venv) file path out of a traceback string."""
    matches = re.findall(r'File "([^"]+)", line \d+', tb)
    for path in reversed(matches):
        if "site-packages" not in path and ".venv" not in path:
            return path
    return None


async def _ai_fix_file(filepath: str, error_text: str) -> str:
    """Ask the AI to fix a broken source file given its traceback, then overwrite it."""
    with open(filepath, "r", encoding="utf-8") as f:
        original = f.read()

    system = (
        "You are a Python code-fixing assistant. You will be given a Python file's "
        "full source and the error/traceback it caused. Return ONLY the complete, "
        "corrected file contents — no explanations, no markdown fences, no commentary. "
        "Preserve the original logic, structure, and style; fix only what's broken."
    )
    user_content = f"File: {filepath}\n\n--- ERROR ---\n{error_text}\n\n--- CURRENT SOURCE ---\n{original}"

    response = await generate_response(
        [{"role": "system", "content": system}, {"role": "user", "content": user_content}]
    )

    fixed = response.strip()
    fixed = re.sub(r"^```(?:python)?\n", "", fixed)
    fixed = re.sub(r"\n```$", "", fixed)

    if not fixed.strip():
        raise RuntimeError("AI returned an empty fix, refusing to overwrite")

    backup_path = filepath + ".bak"
    with open(backup_path, "w", encoding="utf-8") as f:
        f.write(original)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(fixed)

    return backup_path


async def import_commands_with_self_heal():
    for attempt in range(1, MAX_IMPORT_RETRIES + 1):
        try:
            import commands
            importlib.reload(commands)
            return commands.commands_setup
        except Exception:
            tb = traceback.format_exc()
            print(f"[main] import failed on attempt {attempt}/{MAX_IMPORT_RETRIES}:\n{tb}")
            state.log(f"boot import failed (attempt {attempt}): {tb.splitlines()[-1]}")

            failing_file = _extract_failing_file(tb)
            if failing_file is None:
                print("[main] couldn't identify which file to fix, giving up")
                raise

            print(f"[main] asking the AI to fix {failing_file}")
            backup = await _ai_fix_file(failing_file, tb)
            print(f"[main] wrote a fix to {failing_file} (backup saved at {backup})")

            # drop cached modules so the next import actually re-reads the patched files
            for mod_name in list(sys.modules):
                if mod_name == "commands" or mod_name.startswith("cmd."):
                    sys.modules.pop(mod_name, None)

    raise RuntimeError(f"gave up after {MAX_IMPORT_RETRIES} self-heal attempts")

async def main():
    discord.utils.setup_logging(handler=handler, level=logging.INFO)
    await _install_shutdown_save()

    try:
        commands_setup_fn = await import_commands_with_self_heal()
    except Exception as e:
        state.log(f"failed to boot even after self-heal attempts: {e}")
        print(f"[main] giving up on boot: {e}")
        return

    globals()["commands_setup"] = commands_setup_fn  # on_ready reads this name

    backoff = 5
    max_backoff = 300
    async with bot:
        while not bot.is_closed():
            try:
                await bot.start(TOKEN)
                break
            except discord.LoginFailure:
                state.log("login failed — bad token, not retrying")
                print("[main] LoginFailure: check DISCORD_TOKEN, not retrying")
                break
            except Exception as e:
                state.log(f"bot crashed on boot/run: {e}")
                print(f"[main] bot.start() raised {e!r}, retrying in {backoff}s")
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, max_backoff)
                continue
            else:
                backoff = 5

if __name__ == "__main__":
    asyncio.run(main())
