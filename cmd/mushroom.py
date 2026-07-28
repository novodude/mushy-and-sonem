import discord
from discord import app_commands
from discord.ext import commands
import random

async def mushroom_setup(bot: commands.Bot):
    """Setup the /mushroom command for tiny mushroom fun!"""
    
    # Tiny mushroom facts (fun, surprising, or silly!)
    mushroom_facts = [
        "Did you know? Some mushrooms glow in the dark! *floats gently* ✨🍄",
        "Mushrooms are more closely related to humans than to plants! *gasps* 🧬🍄",
        "The largest living organism on Earth is a fungus! It’s in Oregon and covers 2,385 acres. *whispers* That’s bigger than 1,665 football fields! 🌍🍄",
        "Some mushrooms can ‘eat’ plastic! Scientists are studying them to help clean up pollution. *nods proudly* 🍄♻️",
        "Mushrooms can communicate with each other through tiny electrical signals! *listens closely* 🔌🍄",
        "The ‘death cap’ mushroom is one of the most poisonous in the world. *shudders* Don’t eat it! ☠️🍄",
        "Mushrooms can grow in space! Astronauts have grown them on the International Space Station. *floats in zero-G* 🚀🍄",
        "Some mushrooms can break down oil spills! They’re like tiny cleanup crews. *cheers* 🍄🛢️",
        "The ‘bleeding tooth’ mushroom oozes a red liquid that looks like blood! *giggles* 🩸🍄",
        "Mushrooms can ‘hear’ sounds! They grow toward vibrations. *tilts head* 🎵🍄",
        "The ‘veiled lady’ mushroom looks like a tiny ghost! *boos gently* 👻🍄",
        "Some mushrooms can survive extreme temperatures, from freezing cold to scorching heat! *shivers* ❄️🔥🍄",
        "Mushrooms can ‘farm’ bacteria! They release chemicals to attract and trap them. *nods* 🧫🍄",
        "The ‘turkey tail’ mushroom looks like a colorful bird’s tail! *fluffs feathers* 🦃🍄",
        "Mushrooms can ‘talk’ to trees! They help trees share nutrients through their roots. *whispers* It’s called the ‘Wood Wide Web’! 🌳🍄🌐"
    ]
    
    # Tiny mushroom jokes (because why not?)
    mushroom_jokes = [
        "Why did the mushroom go to the party? Because he was a *fun-gi*! *giggles* 🍄🎉",
        "What do you call a mushroom who’s a detective? A *spore*-tective! *nods seriously* 🍄🔍",
        "Why don’t mushrooms ever get lost? Because they always follow their *mycelium*! *floats confidently* 🍄🗺️",
        "What’s a mushroom’s favorite game? *Mushroom*-opoly! *rolls tiny dice* 🍄🎲",
        "Why did the mushroom get a job at the bakery? Because he was a *yeast* of all trades! *kneads dough* 🍄🍞",
        "What do you call a mushroom who’s a musician? A *spore*-ano! *plays tiny piano* 🍄🎹",
        "Why did the mushroom break up with the toadstool? It just wasn’t *working out*! *sighs* 🍄💔",
        "What’s a mushroom’s favorite drink? *Shiitake*-tea! *sips tiny cup* ☕🍄",
        "Why did the mushroom get promoted? Because he was *outstanding in his field*! *stands tall* 🍄🌾",
        "What do you call a mushroom who’s a superhero? *Captain Spore*! *flexes tiny arms* 🍄🦸"
    ]
    
    # Cozy mushroom stories (short, sweet, and a little magical!)
    mushroom_stories = [
        "*Once, a tiny mushroom found a lost firefly. It glowed so brightly that the mushroom could see the whole forest at night. They became best friends, and the firefly would light the way whenever the mushroom needed to find home. ✨🍄🔥*",
        "*Deep in the forest, there was a mushroom who loved to tell stories. Every night, tiny creatures would gather around it, listening to tales of far-off lands and magical adventures. The mushroom’s cap would glow softly, lighting up the faces of its friends. 🌟🍄📖*",
        "*A little girl once found a tiny mushroom in her backyard. She named it ‘Pip’ and would visit it every day. One morning, she found a tiny note under Pip’s cap: *‘Thank you for being my friend. Love, Pip.’* She kept the note forever. 💌🍄👧*",
        "*In a quiet corner of the forest, there was a mushroom who could sing. Its voice was soft and sweet, and every time it sang, the wind would carry the melody to the trees, who would hum along. The forest felt a little cozier because of it. 🎶🍄🌳*",
        "*A tiny mushroom once grew in the middle of a busy city. It didn’t know where it came from, but it loved the sound of rain on the pavement. People would stop to look at it, and for a moment, they’d remember how magical the world could be. 🌧️🍄🏙️*",
        "*One day, a mushroom found a tiny door at the base of a tree. It was just the right size for a mushroom! When it opened the door, it found a whole world of tiny creatures living inside. They invited the mushroom to stay, and it lived there happily ever after. 🚪🍄🌍*",
        "*A mushroom once grew in the middle of a library. It loved the smell of old books and would listen to the stories as people read aloud. One day, a child read a story about mushrooms, and the mushroom felt so proud it glowed for a whole week. 📚🍄✨*",
        "*In a forest where it never rained, a tiny mushroom kept a single dewdrop in its cap. Every morning, it would share the drop with the other plants, and they’d all grow a little taller. The mushroom’s kindness made the forest bloom. 💧🍄🌸*"
    ]
    
    # Tiny mushroom flair (for extra coziness!)
    mushroom_flair = [
        "*floats gently* 🍄✨",
        "*wiggles cap excitedly* 🍄💫",
        "*sways in the breeze* 🍄🌿",
        "*hums a tiny tune* 🍄🎶",
        "*blinks tiny eyes* 🍄👀",
        "*giggles softly* 🍄😄",
        "*stretches tiny arms* 🍄🤸",
        "*sighs happily* 🍄💖"
    ]
    
    @bot.tree.command(name="mushroom", description="Get a tiny mushroom surprise! (facts, jokes, or cozy stories)")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(type="What kind of surprise? (fact, joke, story, or random)")
    async def mushroom(interaction: discord.Interaction, type: str = "random"):
        await interaction.response.defer()
        
        # Pick the type of surprise
        if type.lower() == "fact":
            response = random.choice(mushroom_facts)
        elif type.lower() == "joke":
            response = random.choice(mushroom_jokes)
        elif type.lower() == "story":
            response = random.choice(mushroom_stories)
        else:  # random
            all_surprises = mushroom_facts + mushroom_jokes + mushroom_stories
            response = random.choice(all_surprises)
        
        # Add a tiny flair for extra coziness!
        flair = random.choice(mushroom_flair)
        await interaction.followup.send(f"{response} {flair}")