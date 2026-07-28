import discord

async def commands_setup(bot):
    """Load all command setups here."""
    from cmd.choose import choose_setup
    from cmd.poll import poll_setup
    from cmd.donut import donut_setup
    
    await choose_setup(bot)
    await poll_setup(bot)
    await donut_setup(bot)
