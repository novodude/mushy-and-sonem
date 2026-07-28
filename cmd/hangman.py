import discord
from discord import app_commands
from discord.ui import Button, View
import random

# Store active games (for now, just in memory)
active_games = {}

# Word list (simple for now)
WORDS = [
    "apple", "banana", "cherry", "dragon", "elephant", 
    "forest", "garden", "happy", "island", "jungle"
]

class LetterButton(Button):
    def __init__(self, letter: str):
        super().__init__(style=discord.ButtonStyle.secondary, label=letter, custom_id=letter)
        self.letter = letter

    async def callback(self, interaction: discord.Interaction):
        game = active_games.get(interaction.message.id)
        if not game or game['player'] != interaction.user.id:
            await interaction.response.defer()
            return

        # Check if letter is in the word
        if self.letter.lower() in game['word'].lower():
            # Reveal the letter
            for i, char in enumerate(game['word']):
                if char.lower() == self.letter.lower():
                    game['guessed'][i] = char
            
            # Check for win
            if '_' not in game['guessed']:
                await end_game(interaction, 'win')
                return
        else:
            # Increment mistakes
            game['mistakes'] += 1
            
            # Check for loss
            if game['mistakes'] >= 6:
                await end_game(interaction, 'lose')
                return
        
        # Update button
        self.disabled = True
        self.style = discord.ButtonStyle.success if self.letter.lower() in game['word'].lower() else discord.ButtonStyle.danger
        
        # Update message
        await update_message(interaction, game)

async def update_message(interaction: discord.Interaction, game):
    # Update the word display
    word_display = ' '.join(game['guessed'])
    
    # Draw hangman (simple ASCII for now)
    hangman_art = [
        "  +---+",
        "  |   |",
        f"  {'O' if game['mistakes'] > 0 else ' '}   |",
        f" {'/|\\' if game['mistakes'] > 2 else ('/|' if game['mistakes'] > 1 else ' ')}  |",
        f" {'/ \\' if game['mistakes'] > 4 else ('/' if game['mistakes'] > 3 else ' ')}  |",
        "      |",
        "========="
    ]
    hangman_display = '\n'.join(hangman_art)
    
    # Update message
    content = f"**Hangman!**\nWord: {word_display}\nMistakes: {game['mistakes']}/6\n\n{hangman_display}"
    await interaction.response.edit_message(content=content, view=interaction.message.components[0])

async def end_game(interaction: discord.Interaction, result):
    game = active_games.get(interaction.message.id)
    
    # Disable all buttons
    for row in interaction.message.components:
        for button in row.children:
            button.disabled = True
    
    # Update message
    word_display = ' '.join(game['guessed'])
    if result == 'win':
        content = f"🎉 You win! The word was: **{game['word']}**"
    else:
        content = f"💀 You lose! The word was: **{game['word']}**"
    
    await interaction.response.edit_message(content=content, view=interaction.message.components[0])
    del active_games[interaction.message.id]

async def hangman_setup(bot):
    @bot.tree.command(name="hangman", description="Play a game of Hangman!")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def hangman(interaction: discord.Interaction):
        # Initialize game
        word = random.choice(WORDS)
        guessed = ['_' for _ in word]
        
        # Create view with letter buttons
        view = View(timeout=None)
        
        # Add buttons in rows (A-M, N-Z)
        for i, letter in enumerate('ABCDEFGHIJKLM'):
            view.add_item(LetterButton(letter))
        
        row2 = View()
        for letter in 'NOPQRSTUVWXYZ':
            row2.add_item(LetterButton(letter))
        view.add_item(row2)
        
        # Store game state
        active_games[interaction.message.id] = {
            'word': word,
            'guessed': guessed,
            'mistakes': 0,
            'player': interaction.user.id
        }
        
        # Initial message
        hangman_art = [
            "  +---+",
            "  |   |",
            "      |",
            "      |",
            "      |",
            "      |",
            "========="
        ]
        hangman_display = '\n'.join(hangman_art)
        
        await interaction.response.send_message(
            f"**Hangman!**\nWord: {' '.join(guessed)}\nMistakes: 0/6\n\n{hangman_display}",
            view=view
        )