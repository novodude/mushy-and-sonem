import random

def flip_coin() -> dict:
    """Flip a coin with fun outcomes"""
    outcomes = [
        "Heads! The coin glints in the light...",
        "Tails! It wobbles before settling.",
        "...it landed on its side! How?! (Heads.)",
        "The coin vanishes into the void! (Tails.)",
        "It splits in half! (Heads and tails?)"
    ]
    result = random.choice(["Heads", "Tails"])
    message = random.choice(outcomes)
    return {
        "result": result,
        "message": message
    }
