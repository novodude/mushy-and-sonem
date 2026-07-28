# Commands

To add commands to the bot you make a file in `cmd/` with the commands function inside a setup function, example:

```python
import discord
from discord import app_commands

async def say_setup(bot):
    @bot.tree.command(name="say", description="say something")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(text="what do you want to say?")
    async def say(interaction: discord.Interaction, text: str)
        await interaction.response.defer()
        await interaction.followup.send(text)

```

Then inside the file called `commands.py` import your setup function and add await it in the `commmands_setup` function, before writing check if there's already something there, don't overwrite the file and delete stuff.
DO NOT OVERWRITE THE FILE WITHOUT READING THE WHOLE FILE.
