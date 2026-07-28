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
        if self.game_id not in active_games:
            await interaction.response.send_message("This game has ended!", ephemeral=True)
            return
            
        game = active_games[self.game_id]
        
        # Check if it's this player's turn
        if interaction.user.id != game['current_player']:
            await interaction.response.send_message(f"It's <@{game['current_player']}>'s turn!", ephemeral=True)
            return
            
        # Check if spot is already taken
        if game['board'][self.row][self.col] != 0:
            await interaction.response.send_message("That spot is already taken!", ephemeral=True)
            return
            
        # Make the move
        game['board'][self.row][self.col] = game['players'][interaction.user.id]
        
        # Check for win
        if check_win(game['board'], game['players'][interaction.user.id]):
            await interaction.response.edit_message(content=f"🎉 <@{interaction.user.id}> wins!", view=None)
            del active_games[self.game_id]
            return
            
        # Check for tie
        if all(cell != 0 for row in game['board'] for cell in row):
            await interaction.response.edit_message(content="It's a tie!", view=None)
            del active_games[self.game_id]
            return
            
        # Switch turns
        game['current_player'] = game['player2'] if interaction.user.id == game['player1'] else game['player1']
        await interaction.response.edit_message(content=f"<@{game['current_player']}>'s turn!", view=TicTacToeView(self.game_id))

class TicTacToeView(View):
    def __init__(self, game_id: str):
        super().__init__(timeout=None)  # Persistent view
        self.game_id = game_id
        
        # Create 3x3 grid of buttons
        for row in range(3):
            for col in range(3):
                self.add_item(TicTacToeButton(row, col, game_id))

def check_win(board, player):
    # Check rows
    for row in board:
        if all(cell == player for cell in row):
            return True
    
    # Check columns
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True
    
    return False

async def tictactoe_setup(bot):
    @bot.tree.command(name="tictactoe", description="Play a game of tic-tac-toe!")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(opponent="Who do you want to play against? (leave blank for random)")
    async def tictactoe(interaction: discord.Interaction, opponent: discord.User = None):
        # Set up the game
        player1 = interaction.user.id
        player2 = opponent.id if opponent else None
        
        # If no opponent specified, pick a random one (but not the bot or the player themselves)
        if not opponent:
            guild = interaction.guild
            if guild:
                members = [m for m in guild.members if not m.bot and m.id != player1]
                if members:
                    player2 = random.choice(members).id
                else:
                    await interaction.response.send_message("Couldn't find anyone to play with! Try specifying an opponent.", ephemeral=True)
                    return
            else:
                await interaction.response.send_message("You need to specify an opponent in DMs!", ephemeral=True)
                return
        
        # Make sure player2 is valid
        if player2 == player1:
            await interaction.response.send_message("You can't play against yourself!", ephemeral=True)
            return
            
        # Initialize game state
        game_id = f"{interaction.channel.id}-{interaction.id}"
        active_games[game_id] = {
            'board': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            'players': {player1: 1, player2: 2},
            'player1': player1,
            'player2': player2,
            'current_player': player1
        }
        
        # Send the game board
        view = TicTacToeView(game_id)
        await interaction.response.send_message(
            content=f"Tic-tac-toe! <@{player1}> (❌) vs <@{player2}> (⭕)\n<@{player1}>'s turn!",
            view=view
        )