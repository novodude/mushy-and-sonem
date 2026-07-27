import random
import re

def roll_dice(dice_str: str) -> dict:
    """Roll dice with fun messages! Supports formats like 1d6, 2d20, d100, etc."""
    if not dice_str:
        return {"error": "No dice specified!"}
    
    # Parse dice string (e.g., "2d6" -> num=2, sides=6)
    match = re.match(r'^(\d*)d(\d+)$', dice_str.lower())
    if not match:
        return {"error": "Invalid dice format! Use something like '1d6' or '2d20'."}
    
    num_dice = int(match.group(1)) if match.group(1) else 1
    sides = int(match.group(2))
    
    if num_dice < 1 or num_dice > 100:
        return {"error": "Number of dice must be between 1 and 100!"}
    if sides < 2 or sides > 1000:
        return {"error": "Dice sides must be between 2 and 1000!"}
    
    rolls = [random.randint(1, sides) for _ in range(num_dice)]
    total = sum(rolls)
    
    # Fun messages for special rolls
    if num_dice == 1 and sides == 20:
        if total == 20:
            message = "CRITICAL SUCCESS! *tiny mushroom cap flips excitedly*"
        elif total == 1:
            message = "CRITICAL FAILURE! *tiny mushroom whimpers*"
        else:
            message = f"You rolled a {total}! *tiny mushroom nods approvingly*"
    else:
        if len(rolls) == 1:
            message = f"You rolled a {total}! (d{sides})"
        else:
            message = f"You rolled {total}! ({' + '.join(map(str, rolls))})"
    
    return {
        "rolls": rolls,
        "total": total,
        "message": message
    }
