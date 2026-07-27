import discord
from typing import List

def create_poll(question: str, options: List[str]) -> dict:
    """Create a poll embed and reactions."""
    if len(options) < 2:
        return {"error": "Need at least 2 options for a poll!"}
    if len(options) > 10:
        return {"error": "Too many options! Max 10."}
    
    embed = discord.Embed(title=question, color=0x98FB98)
    for i, option in enumerate(options, start=1):
        embed.add_field(name=f"{i}. {option}", value="⬜", inline=False)
    
    reactions = [f"{i}⃣" for i in range(1, len(options) + 1)]
    
    return {
        "embed": embed.to_dict(),
        "reactions": reactions
    }

def get_poll_results(embed: dict, reactions: List[str]) -> dict:
    """Update embed with vote counts."""
    updated_embed = discord.Embed.from_dict(embed)
    for i, field in enumerate(updated_embed.fields):
        field.value = f"Votes: {reactions.count(f"{i+1}⃣")}"
    
    return {"embed": updated_embed.to_dict()}
