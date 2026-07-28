import asyncio
import os

import discord
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv

from core.persistence import load_state, save_state
from core.tool_loader import load_tools
from core.tool_parser import parse_response, dispatch_tools
from core.ai import generate_response, allmodelsfailederror
from core.self_improvement import run_forever
from core.paths import read as read_instruction

from commands import commands_setup

import logging

load_dotenv()

owner_discord_id = int(os.getenv("owner_discord_id", "951539463224451102"))
token = os.getenv("discord_token")

handler = logging.filehandler(filename="sonem.log", encoding="utf-8", mode="w")
intents = discord.intents.default()
intents.message_content = true
intents.members = true

bot = commands.bot(command_prefix="!", intents=intents)
tree = bot.tree


state = load_state()
_self_improvement_task: asyncio.task | none = none


@tasks.loop(seconds=60)
async def autosave_loop():
    try:
        save_state(state)
    except exception as e:
        print(f"[main] autosave failed: {e}")


@bot.event
async def on_ready():
    global _self_improvement_task
    try:
        await commands_setup(bot)
    except exception as e:
        error = f"faild to load the bot | {e}"
        state.log(error)       

    await tree.sync()
    if not autosave_loop.is_running():
        autosave_loop.start()
    if _self_improvement_task is none or _self_improvement_task.done():
        _self_improvement_task = asyncio.create_task(run_forever(bot, state))
    try:
        await bot.change_presence(activity=discord.customactivity(name=state.status[:128]))
    except exception as e:
        print(f"[main] couldn't set initial presence: {e}")
    state.log(f"woke up as {bot.user}")
    print(f"logged in as {bot.user} (id: {bot.user.id}) — self-improvement running continuously, no cooldown")


@bot.event
async def on_message(message: discord.message):
    if message.author == bot.user or bot.user is none:
        return
    if bot.user not in message.mentions:
        return

    async with message.channel.typing():
        soul = read_instruction("instructions/soul.md")
        mission = read_instruction("instructions/mission.md")
        tools_doc = read_instruction("instructions/tools.md")
        commands_doc = read_instruction("instructions/commands.md")

        system = f"{soul}\n\n---\n\n{mission}\n\n---\n\n{commands_doc}"
        user_content = (
            f"**status:** {state.status} | **mood:** {state.mood}\n\n"
            f"(message id: {message.id}, channel: #{message.channel.name if hasattr(message.channel, 'name') else 'dm'})\n"
            f"{message.author.display_name}: {message.content}"
        )

        try:
            response = await generate_response(
                [{"role": "system", "content": system}, {"role": "user", "content": user_content}]
            )
        except allmodelsfailederror as e:
            await message.channel.send("-# every model i've got is down (or i'm out of quota) right now, sorry :(")
            state.log(f"chat generation failed, all models exhausted: {e}")
            return

        text, tools = parse_response(response)
        if text.strip():
            await message.channel.send(text[:2000])

        if tools:
            registry = load_tools()
            await dispatch_tools(tools, message, state, bot, registry, force_owner=false)

    await bot.process_commands(message)


@tree.command(name="suggest", description="suggest a feature for sonem to add")
@app_commands.describe(feature="what should sonem add or fix?")
async def suggest(interaction: discord.interaction, feature: str):
    state.add_suggestion(str(interaction.user), feature)
    save_state(state)
    await interaction.response.send_message(
        f"🍄 got it — added to the pile! i'll take a look next time i'm working on myself.",
        ephemeral=true,
    )
    state.log(f"suggestion from {interaction.user}: {feature}")


@tree.command(name="set_server", description="(novo only) set this server as sonem's ai server")
async def set_server(interaction: discord.interaction):
    if interaction.user.id != owner_discord_id:
        await interaction.response.send_message("this one's not for you 🍄", ephemeral=true)
        return
    if interaction.guild is none:
        await interaction.response.send_message("this only works inside a server.", ephemeral=true)
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

    for sig in (signal.sigint, signal.sigterm):
        try:
            loop.add_signal_handler(sig, lambda: asyncio.ensure_future(_save_and_close()))
        except notimplementederror:
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

