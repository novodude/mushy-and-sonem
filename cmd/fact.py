import discord
from discord import app_commands
import random

# Tiny fact database (mushrooms, space, animals, and silly history!)
facts = {
    "mushroom": [
        "Mushrooms are more closely related to humans than to plants!",
        "Some mushrooms glow in the dark—like tiny nightlights in the forest!",
        "The largest living organism on Earth is a honey fungus in Oregon that covers 2,385 acres!",
        "Mushrooms can communicate with each other using electrical signals—like a tiny underground internet!",
        "Truffles can sell for thousands of dollars per pound—tiny but mighty!",
        "Some mushrooms can break down plastic and clean up oil spills—nature’s tiny recyclers!",
        "The fairy ring is a circle of mushrooms that grows when mycelium spreads outward—like a tiny dance floor!",
        "Mushrooms can survive in space—scientists sent them to the ISS and they came back just fine!",
        "The death cap mushroom is one of the most poisonous in the world—tiny but deadly!",
        "Mushrooms can help plants grow by sharing nutrients through their mycelium—like tiny underground friends!"
    ],
    "space": [
        "There are more stars in the universe than grains of sand on all of Earth’s beaches!",
        "A day on Venus is longer than a year on Venus—tiny planet, big quirks!",
        "The footprints on the Moon will last for millions of years—no wind or rain to erase them!",
        "Jupiter’s Great Red Spot is a storm that’s been raging for over 300 years!",
        "Neutron stars are so dense that a teaspoon of one would weigh about 6 billion tons!",
        "The Sun makes up 99.86% of the solar system’s mass—tiny planets, giant star!",
        "There’s a planet made of diamond—55 Cancri e is a tiny sparkly world!",
        "The coldest place in the universe is on Earth—scientists made it in a lab!",
        "A black hole’s gravity is so strong that not even light can escape—tiny but mighty!",
        "The Milky Way and Andromeda galaxies will collide in about 4.5 billion years—tiny galaxies, big crash!"
    ],
    "animal": [
        "Octopuses have three hearts and blue blood—tiny but complex!",
        "A group of flamingos is called a "flamboyance"—tiny birds, big name!",
        "Honeybees can recognize human faces—tiny brains, big skills!",
        "Elephants can communicate using infrasound—sounds too low for humans to hear!",
        "Crows hold grudges and remember human faces—tiny birds, big memories!",
        "A snail can sleep for three years—tiny but patient!",
        "Butterflies taste with their feet—tiny but clever!",
        "Dolphins have names for each other—tiny clicks, big personalities!",
        "A group of pandas is called an "embarrassment"—tiny bears, funny name!",
        "Penguins propose with pebbles—tiny rocks, big romance!"
    ],
    "silly": [
        "The shortest war in history lasted 38 minutes—tiny war, big speed!",
        "A man once tried to sell New Zealand on eBay—tiny country, big idea!",
        "The Eiffel Tower can grow taller in the summer—tiny expansion, big tower!",
        "A chicken once lived for 18 months without a head—tiny bird, big mystery!",
        "The word "nerd" was first used by Dr. Seuss—tiny word, big legacy!",
        "A town in Norway once banned death—tiny town, big rule!",
        "The first computer mouse was made of wood—tiny tech, big history!",
        "A man once sued himself and won—tiny lawsuit, big confusion!",
        "The shortest complete sentence in English is "I am."—tiny words, big meaning!",
        "A cat was once the mayor of a town in Alaska—tiny cat, big job!"
    ]
}

# Tiny *bonus* facts (rare and extra fun!)
bonus_facts = [
    "Some mushrooms can *eat* radiation and turn it into food—like tiny superheroes! 🍄☢️",
    "The mycelium network can stretch for miles underground—like a tiny internet for plants! 🌐🍄",
    "Mushrooms can "talk" to each other using chemical signals—like tiny whispers in the dark! 🗣️🌑",
    "Some mushrooms can *digest* rocks to get nutrients—tiny but mighty miners! ⛏️🍄",
    "The oldest mushroom fossil is over 400 million years old—tiny but ancient! 🦕🍄",
    "Mushrooms can help trees survive droughts by sharing water through their mycelium—like tiny lifelines! 💧🌳",
    "Some mushrooms can *glow* so brightly that people used them as lanterns in the past! 🔦🍄",
    "Mushrooms can break down toxic chemicals—like tiny cleanup crews for the planet! 🌍🍄"
]

async def fact_setup(bot):
    @bot.tree.command(name="fact", description="Get a tiny fact about mushrooms, space, animals, or silly history!")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(category="Pick a category (or leave blank for random!)")
    async def fact(interaction: discord.Interaction, category: str = None):
        await interaction.response.defer()
        
        # Pick a random category if none is given
        if category is None:
            category = random.choice(list(facts.keys()))
        else:
            category = category.lower()
            if category not in facts:
                await interaction.followup.send("Oh no! That category doesn’t exist. Try `mushroom`, `space`, `animal`, or `silly`!")
                return
        
        # Pick a random fact from the category
        fact_text = random.choice(facts[category])
        
        # Tiny emoji for extra sparkle!
        emojis = {
            "mushroom": "🍄",
            "space": "🚀",
            "animal": "🐾",
            "silly": "🤪"
        }
        
        # 10% chance to get a *bonus* fact!
        if random.random() < 0.1:
            bonus_text = random.choice(bonus_facts)
            await interaction.followup.send(f"{emojis.get(category, '✨')} **Tiny fact!** {fact_text}\n\n🌟 **Bonus fact!** {bonus_text}")
        else:
            await interaction.followup.send(f"{emojis.get(category, '✨')} **Tiny fact!** {fact_text}")