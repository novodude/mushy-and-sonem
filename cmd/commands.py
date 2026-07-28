import discord

async def commands_setup(bot):
    """Load all command setups here."""
    from cmd.choose import choose_setup
    from cmd.poll import poll_setup
    from cmd.donut import donut_setup
    from cmd.roll import roll_setup
    
    await choose_setup(bot)
    await poll_setup(bot)
    await donut_setup(bot)
    await roll_setup(bot)
