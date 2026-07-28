import discord
from typing import List, Optional

def create_poll(question: str, options_input: str) -> dict:
    """Create a poll embed and reactions from forgiving input."""
    
    # Clean up the question
    question = question.strip()
    if not question:
        return {"error": "Oops! Your poll needs a question. Try something like `/poll What's your favorite food? pizza, tacos, sushi`"}
    
    # Parse options - split by commas or newlines, then clean each one
    options = []
    for part in options_input.replace('\n', ',').split(','):
        option = part.strip()
        if option:  # Skip empty options
            options.append(option)
    
    # Validate
    if len(options) < 2:
        return {"error": f"Oops! You need at least 2 options. You gave me {len(options)}: {', '.join(f'`{o}`' for o in options)}"}
    if len(options) > 10:
        return {"error": "Whoa! That's too many options (max 10)."}
    
    # Create embed
    embed = discord.Embed(
        title=question,
        color=discord.Color.blurple()
    )
    
    # Add options to embed and prepare reactions
    reactions = []
    for i, option in enumerate(options):
        emoji = chr(0x1F1E6 + i)  # Regional indicator letters (🇦, 🇧, etc.)
        embed.add_field(name=f"{emoji} {option}", value="\u200b", inline=False)
        reactions.append(emoji)
    
    return {
        "embed": embed,
        "reactions": reactions
    }