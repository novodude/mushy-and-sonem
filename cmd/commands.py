import discord

async def commands_setup(bot):
    """Load all command setups here."""
    from cmd.choose import choose_setup
    from cmd.poll import poll_setup
    
    await choose_setup(bot)
    await poll_setup(bot)
