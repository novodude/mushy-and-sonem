import asyncio
import os

import discord
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv

from core.persistence import load_state, save_state
from core.tool_loader import load_tools
from core.tool_parser import parse_response, dispatch_tools
from core.ai import generate_response
from core.self_improvement import self_improvement_loop, CYCLE_MINUTES

load_dotenv()

OWNER_DISCORD_ID = int(os.getenv("OWNER_DISCORD_ID", "951539463224451102"))
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

state = load_state()


def _read(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


@tasks.loop(seconds=60)
async def autosave_loop():
    save_state(state)


@bot.event
async def on_ready():
    await tree.sync()
    if not autosave_loop.is_running():
        autosave_loop.start()
    if not self_improvement_loop.is_running():
        self_improvement_loop.start(bot, state)
    state.log(f"woke up as {bot.user}")
    print(f"Logged in as {bot.user} (ID: {bot.user.id}) — self-improvement cycle every {CYCLE_MINUTES} min")


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user or bot.user is None:
        return
    if bot.user not in message.mentions:
        return

    async with message.channel.typing():
        soul = _read("instructions/SOUL.md")
        mission = _read("instructions/MISSION.md")
        tools_doc = _read("instructions/TOOLS.md")

        system = f"{soul}\n\n---\n\n{mission}\n\n---\n\n{tools_doc}"
        user_content = (
            f"**Status:** {state.status} | **Mood:** {state.mood}\n\n"
            f"{message.author.display_name}: {message.content}"
        )

        try:
            response = await generate_response(
                [{"role": "system", "content": system}, {"role": "user", "content": user_content}]
            )
        except Exception as e:
            await message.channel.send("-# every model I've got is down right now, sorry :(")
            state.log(f"chat generation failed: {e}")
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
    await _install_shutdown_save()
    async with bot:
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
