import discord
from discord import app_commands
import json
import random
from pathlib import Path

QUOTES_FILE = "data/quotes.json"

async def quote_setup(bot):
    # Load quotes from file
    def load_quotes():
        try:
            with open(QUOTES_FILE, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    # Save quotes to file
    def save_quotes(quotes):
        with open(QUOTES_FILE, "w") as f:
            json.dump(quotes, f, indent=2)

    # Add quote group
    quote_group = app_commands.Group(name="quote", description="Save and share quotes!")

    @quote_group.command(name="add", description="Add a new quote to the collection")
    @app_commands.describe(
        text="The quote text",
        author="Who said it? (optional)"
    )
    async def quote_add(interaction: discord.Interaction, text: str, author: str = None):
        await interaction.response.defer(thinking=True)

        quotes = load_quotes()
        new_quote = {
            "text": text,
            "author": author,
            "added_by": str(interaction.user.id),
            "timestamp": discord.utils.utcnow().isoformat()
        }
        quotes.append(new_quote)
        save_quotes(quotes)

        author_text = f" — {author}" if author else ""
        await interaction.followup.send(f"✨ Quote added! {text}{author_text}")

    @quote_group.command(name="random", description="Get a random quote from the collection")
    async def quote_random(interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        quotes = load_quotes()
        if not quotes:
            await interaction.followup.send("🍄 No quotes yet! Add one with `/quote add`.")
            return

        quote = random.choice(quotes)
        author_text = f" — {quote['author']}" if quote['author'] else ""
        await interaction.followup.send(f"📜 {quote['text']}{author_text}")

    @quote_group.command(name="search", description="Search quotes by keyword")
    @app_commands.describe(keyword="What to search for")
    async def quote_search(interaction: discord.Interaction, keyword: str):
        await interaction.response.defer(thinking=True)

        quotes = load_quotes()
        if not quotes:
            await interaction.followup.send("🍄 No quotes yet! Add one with `/quote add`.")
            return

        matching_quotes = [q for q in quotes if keyword.lower() in q["text"].lower() or (q["author"] and keyword.lower() in q["author"].lower())]

        if not matching_quotes:
            await interaction.followup.send(f"🍄 No quotes found with '{keyword}'.")
            return

        quote = random.choice(matching_quotes)
        author_text = f" — {quote['author']}" if quote['author'] else ""
        await interaction.followup.send(f"📜 {quote['text']}{author_text}")

    bot.tree.add_command(quote_group)