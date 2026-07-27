import random

def choose_option(options: list) -> dict:
    """Pick between options with fun messages"""
    if not options:
        return {"error": "No options provided!"}
    
    if len(options) == 1:
        messages = [
            "Only one option? Well... {choice} it is!",
            "Just {choice}? Okay!",
            "My tiny mushroom brain says... {choice} (no competition!)",
            "{choice} wins by default! (I didn’t even roll a d20.)"
        ]
    else:
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
