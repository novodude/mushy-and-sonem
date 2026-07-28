import discord
from discord import app_commands
from discord.ui import Button, View
import random

# Store active games (for now, just in memory)
active_games = {}

class TicTacToeButton(Button):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        game = active_games.get(interaction.message.id)
        if not game or game['player2'] != interaction.user.id:
            await interaction.response.defer()
            return

        # Update the board
        if game['board'][self.y][self.x] is None:
            game['board'][self.y][self.x] = 'O'
            self.label = 'O'
            self.style = discord.ButtonStyle.success
            self.disabled = True
            
            # Check for win/tie
            if check_win(game['board'], 'O'):
                await end_game(interaction, 'O')
                return
            elif check_tie(game['board']):
                await end_game(interaction, None)
                return
            
            # Bot's turn
            await bot_move(interaction, game)
        await interaction.response.edit_message(view=self.view)

async def bot_move(interaction: discord.Interaction, game):
    # Find empty spots
    empty_spots = [(y, x) for y in range(3) for x in range(3) if game['board'][y][x] is None]
    if not empty_spots:
        return
    
    # Random move (for now)
    y, x = random.choice(empty_spots)
    game['board'][y][x] = 'X'
    
    # Update button
    for child in interaction.message.components[0].children:
        if child.x == x and child.y == y:
            child.label = 'X'
            child.style = discord.ButtonStyle.danger
            child.disabled = True
            break
    
    # Check for win/tie
    if check_win(game['board'], 'X'):
        await end_game(interaction, 'X')
    elif check_tie(game['board']):
        await end_game(interaction, None)

def check_win(board, player):
    # Check rows, columns, diagonals
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True
    if board[0][0] == board[1][1] == board[2][2] == player or board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

def check_tie(board):
    return all(board[y][x] is not None for y in range(3) for x in range(3))

async def end_game(interaction: discord.Interaction, winner):
    # Disable all buttons
    for row in interaction.message.components:
        for button in row.children:
            button.disabled = True
    
    # Update message
    if winner == 'X':
        result = "I win! 🍄"
    elif winner == 'O':
        result = f"{interaction.user.mention} wins!"
    else:
        result = "It's a tie!"
    
    await interaction.response.edit_message(content=f"Game over! {result}", view=interaction.message.components[0])
    if interaction.message.id in active_games:
        del active_games[interaction.message.id]

async def tictactoe_setup(bot):
    @bot.tree.command(name="tictactoe", description="Play a game of Tic-Tac-Toe!")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def tictactoe(interaction: discord.Interaction):
        # Initialize game
        board = [[None for _ in range(3)] for _ in range(3)]
        view = View(timeout=None)
        
        # Add buttons
        for y in range(3):
            for x in range(3):
                view.add_item(TicTacToeButton(x, y))
        
        # Send initial message and store game state
        await interaction.response.defer()
        message = await interaction.followup.send("Let's play Tic-Tac-Toe! You're O, I'm X.", view=view)
        
        # Store game state with the message ID
        active_games[message.id] = {
            'board': board,
            'player2': interaction.user.id
        }