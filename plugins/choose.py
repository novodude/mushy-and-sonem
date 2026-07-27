import random

def choose_option(options: list) -> dict:
    """Pick between options with fun messages"""
    if not options:
        return {"error": "No options provided!"}
    
    messages = [
        "Hmm... I pick {choice}!",
        "After much deliberation... {choice}!",
        "The universe whispers... {choice}!",
        "My tiny mushroom brain says... {choice}!",
        "{choice} wins! (I rolled a d20 in my head.)"
    ]
    
    choice = random.choice(options)
    message = random.choice(messages).format(choice=choice)
    
    return {
        "choice": choice,
        "message": message
    }
