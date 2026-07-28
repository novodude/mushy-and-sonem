import discord
from discord import app_commands
from discord.ui import Button, View
import random

# Store active games (for now, just in memory)
active_games = {}

class TicTacToeButton(Button):
    def __init__(self, row: int, col: int, game_id: str):
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=row)
        self.row = row
        self.col = col
        self.game_id = game_id

    async def callback(self, interaction: discord.Interaction):
        # We'll fill this in later!
        await interaction.response.defer()

class TicTacToeView(View):
    def __init__(self, game_id: str):
        super().__init__(timeout=None)  # Persistent view
        self.game_id = game_id
        
        # Create 3x3 grid of buttons
        for row in range(3):
            for col in range(3):
                self.add_item(TicTacToeButton(row, col, game_id))

async def tictactoe_setup(bot):
    @bot.tree.command(name="tictactoe", description="Play a game of tic-tac-toe!")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(opponent="Who do you want to play against? (leave blank for random)")
    async def tictactoe(interaction: discord.Interaction, opponent: discord.User = None):
        # We'll fill this in too!
        await interaction.response.defer()
        await interaction.followup.send("Tic-tac-toe coming soon! 🎲🍄")
