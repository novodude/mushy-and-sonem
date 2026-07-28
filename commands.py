from cmd.roll import roll_setup
from cmd.choose import choose_setup
from cmd.donut import donut_setup
from cmd.remind import remind_setup
from cmd.eightball import eightball_setup
from cmd.tictactoe import tictactoe_setup
from cmd.hangman import hangman_setup
from cmd.flip import flip_setup
from cmd.hug import hug_setup
from cmd.quote_image import quote_image_setup
from cmd.fact import fact_setup
from cmd.forage import forage_setup
from cmd.spore import spore_setup
from cmd.mushroom import mushroom_setup


async def commands_setup(bot):
    await roll_setup(bot)
    await choose_setup(bot)
    await donut_setup(bot)
    await remind_setup(bot)
    await eightball_setup(bot)
    await tictactoe_setup(bot)
    await hangman_setup(bot)
    await flip_setup(bot)
    await hug_setup(bot)
    await quote_image_setup(bot)
    await fact_setup(bot)
    await forage_setup(bot)
    await spore_setup(bot)
    await mushroom_setup(bot)