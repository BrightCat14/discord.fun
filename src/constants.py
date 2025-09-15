import random

import ua_generator
from colorama import Fore

from src import tabber

# info
author = "BrightCat14"  # akaruineko
name = "discord.fun"
vX = "v2"
version = vX + tabber.separator() + "dev"
title = name + tabber.space() + version

# hints functionality
hints = [
    f"You knew that {name} v1 is trash?",
    "Also try VanishCord",
    f"Also try {name} v1",
    "Discord is blocking self-bots btw",
    "Self-bots are pain in the ass",
    "Remember: do not share your token!",
    "Try customizing your status with magic",
    "Legend says Discord can ban self-bots in 5 minutes",
    "Sometimes API just says 'no'",
    "Want more fun? Check out hidden commands in dev",
    "Your friends might notice your new status",
    "Keep your token secret, even from your cat",
    "Explore the menus, surprises await!",
    "Remember: no refunds on virtual hugs",
]
hints_dev = [
    "REFACTORING REFACTORING REFACTORING!!!",
    "Some features may be broken, proceed with caution",
    "Did you update your dependencies today?",
    "Pro tip: coffee makes coding faster",
    "Be careful with loops... infinite loops are deadly",
    "Refactor your spaghetti code before lunch",
    "Always read the docs (or at least pretend to)",
    "Debugging mode activated: chaos incoming",
    "Warning: feature might explode on contact",
    "Alpha builds are basically an adventure game",
    "Remember to commit often or cry later",
    "Dev mode enabled: anything can happen",
    "Console logs may contain traces of despair",
    "Beta testing is like juggling chainsaws blindfolded",
    "If it interpretable, it ships... maybe",
    "Warning: random crashes included for fun",
    "Hack the planet, then commit",
    "Typo in code? Feature, not a bug",
    "Your console screams in binary at night",
    "May contain traces of caffeine and despair",
    "Merge conflicts are your new best friends",
    "Remember: StackOverflow is watching you",
]
hint_formatted = (
    Fore.YELLOW + random.choice(hints_dev) + Fore.RESET
    if any(word in version for word in ["beta", "dev", "alpha", "test"])
    else Fore.YELLOW + random.choice(hints) + Fore.RESET
)
# useful in code
UA = ua_generator.generate().text
ICON_URL = f"https://raw.githubusercontent.com/{author}/{name}/refs/heads/{vX}/resources/icon.webp"

if __name__ == "__main__":
    print(author)
    print(title)
    print(ICON_URL)
    print(hint_formatted)
