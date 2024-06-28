import base64
import time
import requests
import os
from colorama import Fore, init
from random import randint
import platform

init()

current_directory = os.getcwd()
folder_name = os.path.basename(current_directory)
username = os.getenv("USERNAME")

if not os.path.exists('config.txt'):
    with open('config.txt', 'w') as f:
        f.write('kali')
# https://discord.com/api/v9/users/@me request: PATCH https://discord.com/api/v9/users/@me/profile request: PATCH
# need authorization token
# 2. bio: "test"
# 1. global_name: "test"

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
                {Fore.LIGHTWHITE_EX}9 - idk what here
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
                {Fore.LIGHTWHITE_EX}1 - test
                {Fore.LIGHTWHITE_EX}0 - Back to page 2
                {Fore.RESET}
    """)

def get_friends_list(user_token):
    url = "https://discord.com/api/v9/users/@me/relationships"
    headers = {"Authorization": user_token}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        friends = response.json()
        friend_ids = [friend["id"] for friend in friends]
        return friend_ids
    else:
        print(f"Failed to retrieve friends list: {response.status_code}")
        return []

def get_friends_list_user(user_token):
    url = "https://discord.com/api/v9/users/@me/relationships"
    headers = {"Authorization": user_token}

    response = requests.get(url, headers=headers)

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

    response = requests.get(url, headers=headers)

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

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        guilds = response.json()
        return '\n'.join([f"{guild['id']} - {guild['name']}" for guild in guilds])
    else:
        print(f"Failed to fetch guilds: {response.status_code}")
        return []

def change_bio(user_token, bio):
    request_url = "https://discord.com/api/v9/users/@me/profile"
    payload = {
        "bio": bio,
    }
    headers = {"Content-Type": "application/json", "Authorization": user_token}

    response = requests.patch(request_url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Successfully changed bio")
    elif response.status_code == 401:
        print("Failed to change bio: Unauthorized. Please check your token.")
    elif response.status_code == 400:
        print("Captcha error")
    else:
        print(f"Failed to change bio: {response.status_code} {response.text}")

def change_display_name(user_token, display_name):
    request_url = "https://discord.com/api/v9/users/@me"
    payload = {
        'global_name': display_name,
    }
    headers = {"Content-Type": "application/json", "Authorization": user_token}

    response = requests.patch(request_url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Successfully changed display name")
    elif response.status_code == 401:
        print("Failed to change display name: Unauthorized. Please check your token.")
    elif response.status_code == 400:
        print("Captcha error")
    else:
        print(f"Failed to change display name: {response.status_code} {response.text}")

def change_pronouns(user_token, pronouns):
    request_url = "https://discord.com/api/v9/users/@me/profile"
    payload = {
        'pronouns': pronouns,
    }
    headers = {"Content-Type": "application/json", "Authorization": user_token}

    response = requests.patch(request_url, json=payload, headers=headers)

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

    response = requests.patch(request_url, json=payload, headers=headers)

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

    response = requests.post(request_url, json=payload, headers=headers)

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
    # Decode the base64 string
    decoded_bytes = base64.b64decode(encoded_str)
    decoded_str = decoded_bytes.decode('utf-8', errors='ignore')

    # Perform the replacements
    for old_word, new_word in replacements.items():
        decoded_str = decoded_str.replace(old_word, new_word)

    # Encode the modified string back to base64
    modified_bytes = decoded_str.encode('utf-8')
    modified_encoded_str = base64.b64encode(modified_bytes).decode('utf-8')

    request_url = 'https://discord.com/api/v9/users/@me/settings-proto/1'
    payload = {
        "settings": modified_encoded_str
    }
    headers = {"Content-Type": "application/json", 'Authorization': token}

    response = requests.patch(request_url, json=payload, headers=headers)

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

    response = requests.get(f'https://discord.com/api/v10/guilds/{guild_id}/channels', headers=headers)

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

    response = requests.get(f'https://discord.com/api/v10/guilds/{guild_id}/channels', headers=headers)

    if response.status_code == 200:
        channels = response.json()
        channels_id = [channel["id"] for channel in channels]
        return channels_id
    else:
        print(f'Failed to fetch channels: {response.status_code} - {response.text}')

def join_server(invite_link, USER_TOKEN):
    HEADERS = {
        'Authorization': USER_TOKEN
    }
    # Извлечение кода приглашения из ссылки
    invite_code = invite_link.split('/')[-1]
    url = f'https://discord.com/api/v9/invites/{invite_code}'
    response = requests.post(url, headers=HEADERS)
    if response.status_code == 200:
        print(f'Successfully joined server with invite code {invite_code}')
    elif response.status_code == 400:
        print("Captcha Error")
    else:
        print(f'Failed to join server: {response.status_code} - {response.text}')
def send_message_to_friend(user_token, message_content, id):
    headers = {'Authorization': user_token, 'Content-Type': 'application/json'}

    for friend_id in id:
        url = f'https://discord.com/api/v10/users/@me/channels'
        try:
            response = requests.post(url, headers=headers, json={'recipient_id': friend_id})
            if response.status_code == 200:
                channel_id = response.json()['id']
                url_message = f'https://discord.com/api/v10/channels/{channel_id}/messages'
                response_message = requests.post(url_message, headers=headers, json={'content': message_content})

                if response_message.status_code == 200:
                    print(f'Message sent successfully to friend with ID {friend_id}')
                else:
                    print(f'Error sending message to friend with ID {friend_id}: {response_message.status_code}')
            else:
                print(f'Error creating channel for friend with ID {friend_id}: {response.status_code}')
        except requests.exceptions.RequestException as e:
            print(f'Error sending message to friend with ID {friend_id}: {e}')


def send_message_to_channel(user_token, message_content, channel_ids):
    headers = {'Authorization': user_token, 'Content-Type': 'application/json'}

    for channel_id in channel_ids:
        url = f'https://discord.com/api/v9/channels/{channel_id}/messages'

        try:
            response = requests.post(url, headers=headers, json={'content': message_content})

            if response.status_code == 200:
                print(f'Message sent successfully to channel with ID {channel_id}')
            else:
                print(f'Error sending message to channel with ID {channel_id}: {response.status_code}')

        except requests.exceptions.RequestException as e:
            print(f'Error sending message to channel with ID {channel_id}: {e}')

def leaver(token, guild_id):
    # URL API для выхода из сервера
    url = f'https://discord.com/api/v9/users/@me/guilds/{guild_id}'

    # Заголовки для запроса
    headers = {
        'Authorization': f'{token}',
        # Если вы используете бот токен, замените 'Bot' на 'Bearer' для пользовательского токена
    }

    # Выполнение DELETE-запроса для выхода из сервера
    response = requests.delete(url, headers=headers)

    # Проверка результата
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

                # Dictionary of replacements
                replacements = {
                    "online": type,
                    "Thinking": text
                }

                change_custom_status(encoded_str, replacements, token)
                input("Press enter to return to the main menu")
            elif choice_page_2 == '2':
                bot_token = input(Fore.CYAN + f'Enter your token: ')
                boost_count = input(Fore.CYAN + f'Enter boost count: ')
                server_id = input(Fore.CYAN + f'Enter your server id: ')
                url = f'https://discord.com/api/v9/guilds/{server_id}/premium/subscriptions'

                headers = {
                    'Authorization': f'{bot_token}',
                    'Content-Type': 'application/json',
                }

                for _ in range(int(boost_count)):
                    time.sleep(0.5)
                    response = requests.post(url, headers=headers)

                    if response.status_code in [200, 201]:
                        print(f'Server boosted successfully!')
                    else:
                        print(f'Failed to boost server. Status code: {response.status_code}')
                        print(response.text)
                    continue
            elif choice_page_2 == '4':
                bot_token = input(Fore.CYAN + f'Enter your token: ')
                server_id = input(Fore.CYAN + f'Enter your server id: ')
                leaver(bot_token, server_id)
                input("Press enter to return to the main menu")
            elif choice_page_2 == '6':
                bot_token = input(Fore.CYAN + f'Enter your token: ')
                server_id = input(Fore.CYAN + f'Enter your server id: ')
                get_channels_id(server_id, bot_token)
                input("Press enter to return to the main menu")
            elif choice_page_2 == '7':
                bot_token = input(Fore.CYAN + f'Enter your token: ')
                server_id = input(Fore.CYAN + f'Enter your server id: ')
                message_content = input(Fore.CYAN + f'What message to send?: ')
                ids = get_channels_id_sys(server_id, bot_token)
                send_message_to_channel(bot_token, message_content, ids)
                input("Press enter to return to the main menu")
            elif choice_page_2 == '8':
                bot_token = input(Fore.CYAN + f'Enter your token: ')
                server_id = input(Fore.CYAN + f'Enter your server id: ')
                message_content = input(Fore.CYAN + f'What message to send?: ')
                id = input(Fore.CYAN + f"Enter channel id or channels ids: ")
                send_message_to_channel(bot_token, message_content, id)
                input("Press enter to return to the main menu")
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
