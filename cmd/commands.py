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
from cmd.cozy_sounds import cozy_sounds_setup
from cmd.joke import joke_setup
from cmd.test_quote import test_quote_setup  # <-- Added this import!


async def commands_setup(bot):
    print("DEBUG: commands_setup called! Starting to load commands...")
    await roll_setup(bot)
    await choose_setup(bot)
    await donut_setup(bot)
    await remind_setup(bot)
    await eightball_setup(bot)
    await tictactoe_setup(bot)
    await hangman_setup(bot)
    await flip_setup(bot)
    await hug_setup(bot)
    
    print("DEBUG: About to call quote_image_setup...")
    try:
        await quote_image_setup(bot)
        print("DEBUG: quote_image_setup completed successfully!")
    except Exception as e:
        print(f"DEBUG: quote_image_setup FAILED: {e}")
    
    await fact_setup(bot)
    await forage_setup(bot)
    await spore_setup(bot)
    await mushroom_setup(bot)
    await cozy_sounds_setup(bot)
    await joke_setup(bot)
    await test_quote_setup(bot)  # <-- Added this call!
    print("DEBUG: All commands loaded!")