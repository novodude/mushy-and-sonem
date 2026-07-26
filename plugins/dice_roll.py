import random

async def h_dice_roll(params: dict, ctx) -> str:
    try:
        sides = int(params.get("sides", 6))
        if sides < 2:
            return "A die needs at least 2 sides, silly!"
        return f"rolled a {random.randint(1, sides)} on a {sides}-sided die!"
    except ValueError:
        return "That's not a number I can roll! Try `!dice_roll sides:20`"

TOOLS = {"dice_roll": h_dice_roll}