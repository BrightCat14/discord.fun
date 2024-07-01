import base64
import os
import platform
import time
from itertools import cycle
from discord_webhook import DiscordWebhook
import requests
from colorama import Fore, init
from lxml.html import fromstring

init()

current_directory = os.getcwd()
folder_name = os.path.basename(current_directory)
username = os.getenv("USERNAME")

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
                {Fore.LIGHTWHITE_EX}1 - test 4
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
        "Authorization": token
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
    headers = {"Authorization": token}

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
    headers = {"Authorization": token}

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
        "Authorization": f"{token}"
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
        'Content-Type': 'application/json'
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
        'Content-Type': 'application/json'
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
    headers = {"Content-Type": "application/json", "Authorization": token}

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
    headers = {"Content-Type": "application/json", "Authorization": token}

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
        'Content-Type': 'application/json'
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
        'Content-Type': 'application/json'
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

def change_pronouns(token, pronouns):
    request_url = "https://discord.com/api/v9/users/@me/profile"
    payload = {
        'pronouns': pronouns,
    }
    headers = {"Content-Type": "application/json", "Authorization": token}

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
    headers = {"Content-Type": "application/json", "Authorization": token}

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
    headers = {"Content-Type": "application/json"}

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
    headers = {"Content-Type": "application/json", 'Authorization': token}

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
        'Authorization': TOKEN
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
    headers = {'Authorization': token, 'Content-Type': 'application/json'}

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
    headers = {'Authorization': token, 'Content-Type': 'application/json'}
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
        'Authorization': token
    }

    response = requests.get(url, headers=headers, proxies={"http": proxy})

    if response.status_code == 200:
        channels = response.json()
        group_dms = [channel for channel in channels if channel['type'] == 3]
        return group_dms
    else:
        response.raise_for_status()

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
        'Content-Type': 'application/json'
    }
    payload = {
        'content': message
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200 or response.status_code == 201:
        print(f"Message sent to channel ID {channel_id}")
    else:
        print(f"Failed to send message to channel ID {channel_id}: {response.status_code} {response.text}")


def leaver(token, guild_id):
    url = f'https://discord.com/api/v9/users/@me/guilds/{guild_id}'

    headers = {
        'Authorization': f'{token}',
    }

    response = requests.delete(url, headers=headers, proxies={"http": proxy})

    if response.status_code == 204:
        print('Successfully left the server.')
    else:
        print(f'Failed to leave the server. Status code: {response.status_code}, Response: {response.text}')


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
                }

                for _ in range(int(boost_count)):
                    proxies = get_proxies()
                    proxy_pool = cycle(proxies)
                    proxy = next(proxy_pool)
                    time.sleep(0.5)
                    response = requests.post(url, headers=headers, proxies={"http": proxy})

                    if response.status_code in [200, 201]:
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
