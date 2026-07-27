import random
from typing import List

def roll_dice(count: int, sides: int) -> dict:
    """Roll XdY dice with fun flair for crits/min/max"""
    if count < 1 or sides < 2:
        return {"error": "Need at least 1 die with 2+ sides!"}
    
    rolls = [random.randint(1, sides) for _ in range(count)]
    total = sum(rolls)
    
    # Fun flair
    flair = []
    if 1 in rolls:
        flair.append("Oof! Low roll...")
    if sides in rolls:
        flair.append("Crit! Nice!")
    if len(set(rolls)) == 1 and len(rolls) > 1:
        flair.append("All the same! Weird...")
    
    return {
        "rolls": rolls,
        "total": total,
        "flair": flair[0] if flair else None
    }
