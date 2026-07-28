import discord
from discord import app_commands
from discord.ext import commands
import random
import re

async def roll_setup(bot: commands.Bot):
    """Setup the /roll command for fancy dice rolling!"""

    @bot.tree.command(name="roll", description="Roll dice (e.g., 1d20, 2d6+3, d100)")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(dice="Dice notation (e.g., 1d20, 2d6+3, d100)")
    async def roll(interaction: discord.Interaction, dice: str):
        await interaction.response.defer()
        
        # Check for empty input
        if not dice.strip():
            await interaction.followup.send("Hmm, you didn't specify any dice! Try something like '1d20' or '2d6+3'. *wiggles cap*")
            return
        
        # Parse dice notation using stricter regex
        match = re.match(r'^(\d+)d(\d+)([+-]\d+)?$', dice.lower())
        if not match:
            # Try d100 as a special case
            if dice.lower() == "d100":
                result = random.randint(1, 100)
                responses = [
                    f"🎲 d100: **{result}** *a tiny mushroom cap wobbles as the die settles*",
                    f"🎲 d100: **{result}** *the die rolls into a patch of moss*",
                    f"🎲 d100: **{result}** *you hear a faint *clink* from under the log*"
                ]
                await interaction.followup.send(random.choice(responses))
                return
            await interaction.followup.send(f"Hmm, I don't understand '{dice}'. Try something like '1d20', '2d6+3', or 'd100'! *wiggles cap*")
            return
        
        # Extract components
        num_dice = int(match.group(1))
        sides = int(match.group(2))
        modifier = match.group(3) or "+0"
        
        # Validate dice/sides (no zero or negative)
        if num_dice <= 0:
            await interaction.followup.send("You can't roll zero or negative dice! Try something like '1d6'. *tilts cap*")
            return
        if sides <= 0:
            await interaction.followup.send("Dice can't have zero or negative sides! Try something like '1d6'. *wiggles worriedly*")
            return
        
        # Validate modifier (no negative)
        modifier_value = int(modifier)
        if modifier_value < 0:
            await interaction.followup.send("Modifiers can't be negative! Try something like '1d20+5'. *peers at you*")
            return
        
        # Check for reasonable limits
        if num_dice > 100:
            await interaction.followup.send("That's too many dice! (max 100)")
            return
        if sides > 1000:
            await interaction.followup.send("That's too many sides! (max 1000)")
            return
        
        # Roll the dice!
        rolls = [random.randint(1, sides) for _ in range(num_dice)]
        total = sum(rolls) + modifier_value
        
        # Format the response
        roll_str = ", ".join(map(str, rolls))
        modifier_str = f" {modifier}" if modifier != "+0" else ""
        
        # Special responses for crits (natural 1 or max roll)
        crit_responses = []
        if sides == 20:  # Only check for d20 crits
            if 1 in rolls:
                crit_responses.append("*OH NO!* A natural 1! *a tiny mushroom cap flops over dramatically* 🍄💥")
            if 20 in rolls:
                crit_responses.append("*CRITICAL!* A natural 20! *a tiny mushroom cap glows with excitement* ✨🍄")
        
        # Base response
        if num_dice == 1 and modifier == "+0":
            base_response = f"🎲 {dice}: **{total}**"
        else:
            base_response = f"🎲 {dice}: [{roll_str}]{modifier_str} = **{total}**"
        
        # Combine responses (crit first, then base)
        response_parts = crit_responses + [base_response]
        response = "\n".join(response_parts)
        
        # Add tiny mushroom flair
        flair_responses = [
            "*a tiny mushroom cap wobbles as the dice settle*",
            "*the dice roll into a patch of moss*",
            "*you hear a faint *clink* from under the log*",
            "*a tiny mushroom friend peeks at the result* 👀🍄",
            "*the dice glow faintly under the log* ✨"
        ]
        
        await interaction.followup.send(f"{response}\n{random.choice(flair_responses)}")