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


async def commands_setup(bot):
    print("DEBUG: commands_setup called! Starting to load commands...")
    
    # Load all commands with extra debug
    print("DEBUG: Loading roll_setup...")
    await roll_setup(bot)
    
    print("DEBUG: Loading choose_setup...")
    await choose_setup(bot)
    
    print("DEBUG: Loading donut_setup...")
    await donut_setup(bot)
    
    print("DEBUG: Loading remind_setup...")
    await remind_setup(bot)
    
    print("DEBUG: Loading eightball_setup...")
    await eightball_setup(bot)
    
    print("DEBUG: Loading tictactoe_setup...")
    await tictactoe_setup(bot)
    
    print("DEBUG: Loading hangman_setup...")
    await hangman_setup(bot)
    
    print("DEBUG: Loading flip_setup...")
    await flip_setup(bot)
    
    print("DEBUG: Loading hug_setup...")
    await hug_setup(bot)
    
    print("DEBUG: Loading quote_image_setup...")
    try:
        await quote_image_setup(bot)
        print("DEBUG: quote_image_setup completed successfully!")
    except Exception as e:
        print(f"DEBUG: quote_image_setup FAILED: {e}")
    
    print("DEBUG: Loading fact_setup...")
    await fact_setup(bot)
    
    print("DEBUG: Loading forage_setup...")
    await forage_setup(bot)
    
    print("DEBUG: Loading spore_setup...")
    await spore_setup(bot)
    
    print("DEBUG: Loading mushroom_setup...")
    await mushroom_setup(bot)
    
    print("DEBUG: Loading cozy_sounds_setup...")
    await cozy_sounds_setup(bot)
    
    print("DEBUG: Loading joke_setup...")
    await joke_setup(bot)
    
    print("DEBUG: All commands loaded! Checking command tree...")
    commands_in_tree = [cmd.name for cmd in bot.tree.get_commands()]
    print(f"DEBUG: Commands in tree after setup: {commands_in_tree}")
    
    # Add a small delay to ensure all commands are properly registered
    print("DEBUG: Waiting 2 seconds to ensure all commands are registered...")
    import asyncio
    await asyncio.sleep(2)
    
    # Sync the command tree to Discord!
    print("DEBUG: Syncing command tree to Discord...")
    try:
        synced = await bot.tree.sync()
        print(f"DEBUG: Successfully synced {len(synced)} commands to Discord!")
        print(f"DEBUG: Synced commands: {[cmd.name for cmd in synced]}")
    except Exception as e:
        print(f"DEBUG: Failed to sync command tree: {e}")