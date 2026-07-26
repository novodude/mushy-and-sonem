# Dice roller plugin for Sonem
# Supports:
# - /dice_roll (defaults to 1d6)
# - /dice_roll d20
# - /dice_roll 2d6
# - /dice_roll 10 (rolls d10)

import random

async def h_dice_roll(params: dict, ctx) -> str:
    # Default to 1d6 if no params
    if not params or not params.get("input"):
        return f"🎲 Rolled a {random.randint(1, 6)} (default 1d6)"

    input_str = params["input"].strip().lower()

    # Handle simple "d20" or "2d6" format
    if "d" in input_str:
        try:
            num_dice, sides = input_str.split("d")
            num_dice = int(num_dice) if num_dice else 1
            sides = int(sides)
            if num_dice < 1 or sides < 2:
                return "❌ Need at least 1 die and 2+ sides!"
            rolls = [random.randint(1, sides) for _ in range(num_dice)]
            total = sum(rolls)
            return f"🎲 Rolled {input_str}: {rolls} (total: {total})"
        except ValueError:
            return "❌ Use format like `d20` or `2d6`!"
    else:
        # Handle single number (e.g., "20" -> d20)
        try:
            sides = int(input_str)
            if sides < 2:
                return "❌ Need at least 2 sides!"
            return f"🎲 Rolled a {random.randint(1, sides)} (d{sides})"
        except ValueError:
            return "❌ Use a number (like `20`) or dice format (like `2d6`)!"

TOOLS = {"dice_roll": h_dice_roll}