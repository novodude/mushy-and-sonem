import discord
from discord.ext import commands
from cmd.roll import roll_setup
from cmd.flip import flip_setup
from cmd.choose import choose_setup
from cmd.donut import donut_setup
from cmd.remind import remind_setup
from cmd.quote import quote_setup

async def commands_setup(bot):
    await roll_setup(bot)
    await flip_setup(bot)
    await choose_setup(bot)
    await donut_setup(bot)
    await remind_setup(bot)
    await quote_setup(bot)