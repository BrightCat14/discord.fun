import os
import platform
from datetime import datetime

from colorama import Fore

from src import utils, tabber, constants

def convert_iso_to_readable(iso_timestamp):
    dt = datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00"))
    return dt.strftime("%d %B %Y, %H:%M:%S (UTC)")

def get_input(prompt_text):
    return input(Fore.CYAN + f"{prompt_text}: ")

def get_return_input():
    return input("Press enter to return to the main menu")

def get_prompt():
    with open(utils.theme_cfg, 'r') as f:
        theme = f.read().strip()
    with open(utils.custom_prompt_path, 'r') as f:
        custom_prompt = utils.parse_custom_prompt(f.read().strip())

    prompt = f"{Fore.LIGHTGREEN_EX}{utils.username}@kali:{Fore.BLUE}/{utils.folder_name}${Fore.LIGHTGREEN_EX}{tabber.space()}"
    
    if theme == 'kali-old':
        pass # by default prompt is kali old, see up
    elif theme == 'windows':
        prompt = f"{utils.current_directory}>{tabber.space()}"
    elif theme == 'omz':
        prompt = f"{Fore.LIGHTGREEN_EX}→{Fore.RESET}{tabber.space()}{Fore.LIGHTBLUE_EX}{utils.folder_name}{Fore.RESET}{tabber.space()}{Fore.MAGENTA}git:({Fore.RED}{constants.vX}{Fore.MAGENTA}){Fore.RESET}{tabber.space()}{Fore.YELLOW}✘{Fore.RESET}{tabber.space()}"
    elif theme == 'boring':
        prompt = f"${tabber.space()}"
    elif theme == 'custom':
        prompt = custom_prompt

    return prompt

def clear_screen():
    os.system("cls" if platform.system() == "Windows" else "clear")