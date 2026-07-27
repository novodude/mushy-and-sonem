from discord.ext import commands
from cmd.file_viewer import FileViewer_setup
from cmd.donut import donut_setup

async def commands_setup(bot: commands.Bot):
    await donut_setup(bot)
    await FileViewer_setup(bot)
