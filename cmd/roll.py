import discord
from discord import app_commands
import random

async def roll_setup(bot):
    @bot.tree.command(name="roll", description="Roll some dice! 🎲")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(dice="e.g. 2d6, 1d20, 3d4+2")
    async def roll(interaction: discord.Interaction, dice: str):
        await interaction.response.defer()
        
        # Parse dice notation (e.g., 2d6+1)
        try:
            parts = dice.lower().split('d')
            num_dice = int(parts[0]) if parts[0] else 1
            if '+' in parts[1]:
                die_type, modifier = parts[1].split('+')
                modifier = int(modifier)
            else:
                die_type = parts[1]
                modifier = 0
            die_type = int(die_type)
        except:
            await interaction.followup.send("❌ Invalid dice format! Use something like `2d6` or `1d20+3`.")
            return
        
        # Roll the dice
        rolls = []
        total = 0
        for _ in range(num_dice):
            roll = random.randint(1, die_type)
            rolls.append(roll)
            total += roll
        total += modifier
        
        # Check for crits (max roll on any die)
        crit_emoji = ""
        if any(roll == die_type for roll in rolls):
            crit_emoji = " 🎉"
        
        # Format the response
        rolls_str = ", ".join(map(str, rolls))
        response = f"🎲 **Roll result:** {rolls_str}"
        if num_dice > 1 or modifier != 0:
            response += f" (Total: {total})"
        response += crit_emoji
        
        await interaction.followup.send(response)