import os
import platform
from datetime import datetime

from colorama import Fore

from src import utils

def convert_iso_to_readable(iso_timestamp):
    dt = datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00"))
    return dt.strftime("%d %B %Y, %H:%M:%S (UTC)")

def get_input(prompt_text):
    return input(Fore.CYAN + f"{prompt_text}: ")

def get_return_input():
    return input("Press enter to return to the main menu")

def get_prompt():
    with open(utils.config_path, 'r') as f:
        theme = f.read().strip()

    prompt = f"{Fore.LIGHTGREEN_EX}{utils.username}@kali:{Fore.BLUE}/{utils.folder_name}${Fore.LIGHTGREEN_EX} "
    
    if theme == 'kali':
        prompt = f"{Fore.LIGHTGREEN_EX}{utils.username}@kali:{Fore.BLUE}/{utils.folder_name}${Fore.LIGHTGREEN_EX} "
    elif theme == 'windows':
        prompt = f"{utils.current_directory}>"

    return prompt

def clear_screen():
    os.system("cls" if platform.system() == "Windows" else "clear")