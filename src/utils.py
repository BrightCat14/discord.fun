import os
import platform

import aiohttp
import requests
from colorama import Fore

current_directory = os.getcwd()
folder_name = os.path.basename(current_directory)
username = os.getenv("USERNAME") if platform.system() == "win32" else os.getenv("USER")

def menu():
    print(f"""
{Fore.CYAN} ___    ____ _____   __   ___   ____   ___        _____  __ __  ____  
{Fore.CYAN} |   \  |    / ___/  /  ] /   \ |    \ |   \      |     ||  |  ||    \ 
{Fore.CYAN} |    \  |  (   \_  /  / |     ||  D  )|    \     |   __||  |  ||  _  |
{Fore.CYAN} |  D  | |  |\__  |/  /  |  O  ||    / |  D  |    |  |_  |  |  ||  |  |
{Fore.CYAN} |     | |  |/  \ /   \_ |     ||    \ |     | __ |   _] |  :  ||  |  |
{Fore.CYAN} |     | |  |\    \     ||     ||  .  \|     ||  ||  |   |     ||  |  |
{Fore.CYAN} |_____||____|\___|\____| \___/ |__|\_||_____||__||__|    \__,_||__|__|
{Fore.RESET}
                {Fore.LIGHTWHITE_EX}1 - Get a list of friends from the token
                {Fore.LIGHTWHITE_EX}2 - Get token from email and password
                {Fore.LIGHTWHITE_EX}3 - Send a message to friends
                {Fore.LIGHTWHITE_EX}4 - Send a message to friend id or ids
                {Fore.LIGHTWHITE_EX}5 - Change bio by token
                {Fore.LIGHTWHITE_EX}6 - Change display name by token
                {Fore.LIGHTWHITE_EX}7 - Change username by password and token
                {Fore.LIGHTWHITE_EX}8 - Change pronouns by token
                {Fore.LIGHTWHITE_EX}9 - Go to Page 2
                {Fore.LIGHTWHITE_EX}0 - Exit
                {Fore.RESET}
    """)

def menu_page_2():
    print(f"""
{Fore.CYAN} ___    ____ _____   __   ___   ____   ___        _____  __ __  ____  
{Fore.CYAN} |   \  |    / ___/  /  ] /   \ |    \ |   \      |     ||  |  ||    \ 
{Fore.CYAN} |    \  |  (   \_  /  / |     ||  D  )|    \     |   __||  |  ||  _  |
{Fore.CYAN} |  D  | |  |\__  |/  /  |  O  ||    / |  D  |    |  |_  |  |  ||  |  |
{Fore.CYAN} |     | |  |/  \ /   \_ |     ||    \ |     | __ |   _] |  :  ||  |  |
{Fore.CYAN} |     | |  |\    \     ||     ||  .  \|     ||  ||  |   |     ||  |  |
{Fore.CYAN} |_____||____|\___|\____| \___/ |__|\_||_____||__||__|    \__,_||__|__|
{Fore.RESET}
                {Fore.LIGHTWHITE_EX}1 - Change custom status by token
                {Fore.LIGHTWHITE_EX}2 - Boost server by token (I dont know if it works or not)
                {Fore.LIGHTWHITE_EX}3 - Join server by token
                {Fore.LIGHTWHITE_EX}4 - Leave server by token
                {Fore.LIGHTWHITE_EX}5 - Get guilds list
                {Fore.LIGHTWHITE_EX}6 - Get channels in guild
                {Fore.LIGHTWHITE_EX}7 - Send Message to all channels in guild
                {Fore.LIGHTWHITE_EX}8 - Send Message to channel or channels in guild
                {Fore.LIGHTWHITE_EX}9 - Go to page 3
                {Fore.LIGHTWHITE_EX}0 - Back to page 1
                {Fore.RESET}
    """)

def menu_page_3():
    print(f"""
{Fore.CYAN} ___    ____ _____   __   ___   ____   ___        _____  __ __  ____  
{Fore.CYAN} |   \  |    / ___/  /  ] /   \ |    \ |   \      |     ||  |  ||    \ 
{Fore.CYAN} |    \  |  (   \_  /  / |     ||  D  )|    \     |   __||  |  ||  _  |
{Fore.CYAN} |  D  | |  |\__  |/  /  |  O  ||    / |  D  |    |  |_  |  |  ||  |  |
{Fore.CYAN} |     | |  |/  \ /   \_ |     ||    \ |     | __ |   _] |  :  ||  |  |
{Fore.CYAN} |     | |  |\    \     ||     ||  .  \|     ||  ||  |   |     ||  |  |
{Fore.CYAN} |_____||____|\___|\____| \___/ |__|\_||_____||__||__|    \__,_||__|__|
{Fore.RESET}
                {Fore.LIGHTWHITE_EX}1 - Discord group nuker
                {Fore.LIGHTWHITE_EX}2 - thread spammer
                {Fore.LIGHTWHITE_EX}3 - typing spammer
                {Fore.LIGHTWHITE_EX}4 - Get discord groups id
                {Fore.LIGHTWHITE_EX}5 - Send message to all groups
                {Fore.LIGHTWHITE_EX}6 - Send message to group id or ids
                {Fore.LIGHTWHITE_EX}7 - Discord Webhook Spammer
                {Fore.LIGHTWHITE_EX}8 - Send message to webhook
                {Fore.LIGHTWHITE_EX}9 - Go to page 4
                {Fore.LIGHTWHITE_EX}0 - Back to page 2
                {Fore.RESET}
    """)

def menu_page_4():
    print(f"""
{Fore.CYAN} ___    ____ _____   __   ___   ____   ___        _____  __ __  ____  
{Fore.CYAN} |   \  |    / ___/  /  ] /   \ |    \ |   \      |     ||  |  ||    \ 
{Fore.CYAN} |    \  |  (   \_  /  / |     ||  D  )|    \     |   __||  |  ||  _  |
{Fore.CYAN} |  D  | |  |\__  |/  /  |  O  ||    / |  D  |    |  |_  |  |  ||  |  |
{Fore.CYAN} |     | |  |/  \ /   \_ |     ||    \ |     | __ |   _] |  :  ||  |  |
{Fore.CYAN} |     | |  |\    \     ||     ||  .  \|     ||  ||  |   |     ||  |  |
{Fore.CYAN} |_____||____|\___|\____| \___/ |__|\_||_____||__||__|    \__,_||__|__|
{Fore.RESET}
                {Fore.LIGHTWHITE_EX}1 - Get Discord Nitro expiration by token
                {Fore.LIGHTWHITE_EX}2 - Get Country Code by token
                {Fore.LIGHTWHITE_EX}3 - Get sessions by token
                {Fore.LIGHTWHITE_EX}4 - Spammer
                {Fore.LIGHTWHITE_EX}5 - Hypesquad changer
                {Fore.LIGHTWHITE_EX}6 - Create Webhook by token
                {Fore.LIGHTWHITE_EX}7 - Discord server nuker by token
                {Fore.LIGHTWHITE_EX}8 - Get basic user info by token
                {Fore.LIGHTWHITE_EX}0 - Back to page 3
                {Fore.RESET}
    """)



def get_picture_by_url(image_url):
    response = requests.get(image_url)
    if response.status_code != 200:
        print(f'Failed to fetch image: {response.status_code} - {response.text}')
    return response.content

def clear_screen():
    os.system("cls" if platform.system() == "Windows" else "clear")

def get_prompt():
    with open('config.txt', 'r') as f:
        theme = f.read().strip()
    if theme == 'kali':
        prompt = f"{Fore.LIGHTGREEN_EX}{username}@kali:{Fore.BLUE}/{folder_name}${Fore.LIGHTGREEN_EX} "
    elif theme == 'windows':
        prompt = f"{current_directory}>"
    else:
        prompt = f"{Fore.LIGHTGREEN_EX}{username}@kali:{Fore.BLUE}/{folder_name}$ "
    return prompt

async def fetch_image_bytes(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()

def init():
    if not os.path.exists('config.txt'):
        with open('config.txt', 'w') as f:
            f.write('kali')