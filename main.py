import asyncio
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

from commands import commands_setup

import logging

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

async def main():
    discord.utils.setup_logging(handler=handler, level=logging.INFO)
    await _install_shutdown_save()

    backoff = 5
    max_backoff = 300

    async with bot:
        while not bot.is_closed():
            try:
                await bot.start(TOKEN)
                break  # bot.close() was called deliberately (e.g. shutdown signal), exit loop
            except discord.LoginFailure:
                # bad token — retrying won't help, so don't loop forever
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
                backoff = 5  # reset after a clean run


if __name__ == "__main__":
    asyncio.run(main())
