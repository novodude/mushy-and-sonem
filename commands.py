from cmd.roll import roll_setup
from cmd.flip import flip_setup
from cmd.choose import choose_setup
from cmd.donut import donut_setup
from cmd.remind import remind_setup
from cmd.eightball import eightball_setup
from cmd.poll import poll_setup

async def commands_setup(bot):
    await roll_setup(bot)
    await flip_setup(bot)
    await choose_setup(bot)
    await donut_setup(bot)
    await remind_setup(bot)
    await eightball_setup(bot)
    await poll_setup(bot)
