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
                {Fore.LIGHTWHITE_EX}5 - Settings
                {Fore.LIGHTWHITE_EX}0 - Exit
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
    else:
        print(f"Failed to retrieve access token: {response.status_code} {response.text}")

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
def clear():
    os.system("cls")

while True:
    clear()
    with open('config.txt', 'r') as f:
        theme = f.read().strip()
    if theme == 'kali':
        setting = f"{Fore.LIGHTGREEN_EX}{username}@kali:{Fore.BLUE}/{folder_name}$ "
    elif theme == 'windows':
        setting = f"{current_directory}>"
    else:
        setting = f"{Fore.LIGHTGREEN_EX}{username}@kali:{Fore.BLUE}/{folder_name}$ "
    menu()
    choice = input(setting)

    if choice == '1':
        clear()
        token = input(Fore.CYAN + f"Enter your token: ")
        get_friends_list(token)
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
    elif choice == '5':
        clear()
        choice_settings = input(Fore.CYAN + f'Enter your choice (1 - kali, 2 - windows): ')
        if choice_settings == '1':
            with open('config.txt', 'w') as f:
                f.write('kali')
        elif choice_settings == '2':
            with open('config.txt', 'w') as f:
                f.write('windows')
        else:
            print('Invalid choice')
    elif choice == '4':
        clear()
        token = input(Fore.CYAN + f"Enter your token: ")
        friend_ids = input(Fore.CYAN + f"Enter friend id or ids (e.g. 1234567890, 1234567890): ")
        friend_ids1 = [friend_ids]
        message_content = input("What message to send?: ")
        send_message_to_friend(token, message_content, friend_ids1)
    elif choice == '0':
        exit(0)
    else:
        print("Invalid choice. Please enter a valid option.")
