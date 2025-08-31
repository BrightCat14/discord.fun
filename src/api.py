import base64
import time

import requests

from src import cli

BASE_URL = 'https://discord.com/api/v10'

def typer(channel_id, token):
    request = f'https://discord.com/api/v9/channels/{channel_id}/typing'

    headers = {
        "Content-Type": 'text/html; charset=utf-8',
        "Authorization": token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    response = requests.post(url=request, headers=headers)
    if response.status_code == 204:
        print("Successfully send request to type")
    elif response.status_code == 429:
        retry_after = response.json().get('retry_after', 1)
        print(f'Rate limit, retry after {retry_after} seconds.')
        time.sleep(retry_after)
        typer(channel_id, token)
    else:
        print(f"Error: {response.status_code}")


def get_friends_list(token):
    url = BASE_URL + "/users/@me/relationships"
    headers = {
        "Authorization": token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        friends = response.json()
        friend_ids = [friend["id"] for friend in friends]
        return friend_ids
    else:
        print(f"Failed to retrieve friends list: {response.status_code}")
        return []


def get_friends_list_user(token):
    url = BASE_URL + "/users/@me/relationships"
    headers = {
        "Authorization": token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        friends = response.json()
        return '\n'.join([f"{friend['id']} - {friend['name']}" for friend in friends])
    else:
        print(f"Failed to retrieve friends list: {response.status_code}")
        return []


def get_discord_guilds(token):
    url = BASE_URL + "/users/@me/guilds"
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
    url = BASE_URL + "/users/@me/guilds"
    headers = {
        "Authorization": f"{token}",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        guilds = response.json()
        return '\n'.join([f"{guild['id']} - {guild['name']}" for guild in guilds])
    else:
        print(f"Failed to fetch guilds: {response.status_code}")
        return []


def send_message_group(channel_id, message_content, discord_token):
    url = BASE_URL + f"/channels/{channel_id}/messages"
    headers = {
        'Authorization': f'{discord_token}',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }
    payload = {
        'content': message_content
    }
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print(f'Send message successfully to ID {channel_id}')
    elif response.status_code == 429:
        retry_after = response.json().get('retry_after', 1)
        print(f'Rate limit. Retry after {retry_after} seconds.')
        time.sleep(retry_after)
        send_message_group(channel_id, message_content, discord_token)
    else:
        print(f'Error to ID {channel_id}: {response.status_code}')
        print(f"Response: {response.json()}")


def change_name_group(channel_id, message_content, discord_token):
    url = BASE_URL + f"/channels/{channel_id}"
    headers = {
        'Authorization': f'{discord_token}',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }
    payload = {
        'name': message_content
    }

    response = requests.patch(url, headers=headers, json=payload)

    if response.status_code == 200:
        print(f'Change group name request successfully send to ID {channel_id}')
    elif response.status_code == 429:
        retry_after = response.json().get('retry_after', 1)
        print(f'Rate limit. Retry after {retry_after} seconds.')
        time.sleep(retry_after)

        change_name_group(channel_id, message_content, discord_token)
    else:
        print(f'Error to id {channel_id}: {response.status_code}')
        print(f"Response: {response.json()}")


def change_bio(token, bio):
    request_url = BASE_URL + "/users/@me/profile"
    payload = {
        "bio": bio,
    }
    headers = {
        "Content-Type": "application/json", "Authorization": token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    response = requests.patch(request_url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Successfully changed bio")
    elif response.status_code == 401:
        print("Failed to change bio: Unauthorized. Please check your token.")
    elif response.status_code == 400:
        print("Captcha error")
    else:
        print(f"Failed to change bio: {response.status_code} {response.text}")


def change_display_name(token, display_name):
    request_url = BASE_URL + "/users/@me"
    payload = {
        'global_name': display_name,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    response = requests.patch(request_url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Successfully changed display name")
    elif response.status_code == 401:
        print("Failed to change display name: Unauthorized. Please check your token.")
    elif response.status_code == 400:
        print("Captcha error")
    else:
        print(f"Failed to change display name: {response.status_code} {response.text}")

thread_data = None
def thread_spammer(token, channel_id, message_id, thread_name):
    global thread_data
    request_url = BASE_URL + f"/channels/{channel_id}/messages/{message_id}/threads"
    headers = {
        'Authorization': f'{token}',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }
    payload = {
        'name': thread_name
    }

    response = requests.post(request_url, headers=headers, json=payload)

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
    request_url = BASE_URL + f"/channels/{thread_data['id']}"
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

        thread_spammer(token, channel_id, message_id, thread_name)
    else:
        print("Error: " + response.json())


def print_info_user(token):
    request_url = BASE_URL + "/users/@me"
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
    request_url = BASE_URL + "/users/@me/profile"
    payload = {
        'pronouns': pronouns,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

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
    request_url = BASE_URL + "/users/@me"
    payload = {
        'password': password,
        'username': username
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    response = requests.patch(request_url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Successfully changed username")
    elif response.status_code == 401:
        print("Failed to change username: Unauthorized. Please check your token.")
    elif response.status_code == 400:
        print("Captcha error")
    else:
        print(f"Failed to change username: {response.status_code} {response.text}")


def get_token(email, password):
    request_url = BASE_URL + "/auth/login"
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
    decoded_bytes = base64.b64decode(encoded_str)
    decoded_str = decoded_bytes.decode('utf-8', errors='ignore')

    for old_word, new_word in replacements.items():
        decoded_str = decoded_str.replace(old_word, new_word)

    modified_bytes = decoded_str.encode('utf-8')
    modified_encoded_str = base64.b64encode(modified_bytes).decode('utf-8')

    request_url = BASE_URL + "/users/@me/settings-proto/1"
    payload = {
        "settings": modified_encoded_str
    }
    headers = {
        "Content-Type": "application/json",
        'Authorization': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    response = requests.patch(request_url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Changed custom status successfully")
    elif response.status_code == 400:
        print("Captcha error")
    else:
        print(f"Failed to retrieve access token: {response.status_code} {response.text}")


def get_list_channels_id(guild_id, token):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    response = requests.get(BASE_URL + f"/guilds/{guild_id}/channels", headers=headers)

    if response.status_code == 200:
        channels = response.json()
        return '\n'.join([f"{channel['id']} - {channel['name']}" for channel in channels])
    else:
        print(f'Failed to fetch channels: {response.status_code} - {response.text}')


def sys_get_channels_id(guild_id, token):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    response = requests.get(f'https://discord.com/api/v10/guilds/{guild_id}/channels', headers=headers)

    if response.status_code == 200:
        channels = response.json()
        channels_id = [channel["id"] for channel in channels]
        return channels_id
    else:
        print(f'Failed to fetch channels: {response.status_code} - {response.text}')


def join_server(invite_link, token):
    headers = {
        'Authorization': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    invite_code = invite_link.split('/')[-1]
    url = BASE_URL + f"/invites/{invite_code}"
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        print(f'Successfully joined server with invite code {invite_code}')
    elif response.status_code == 400:
        print("Captcha Error")
    else:
        print(f'Failed to join server: {response.status_code} - {response.text}')


def send_message_to_friend(token, message_content, identifier):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    for friend_id in identifier:
        url = BASE_URL + "/users/@me/channels"
        try:

            response = requests.post(url, headers=headers, json={'recipient_id': friend_id})
            if response.status_code == 200:
                channel_id = response.json()['id']
                url_message = f'https://discord.com/api/v9/channels/{channel_id}/messages'
                response_message = requests.post(url_message, headers=headers, json={'content': message_content})

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
    for channel_id in channel_ids:

        url = BASE_URL + f"/channels/{channel_id}/messages"

        try:
            response = requests.post(url, headers=headers, json={'content': message_content})

            if response.status_code == 200:
                print(f'Message sent successfully to channel with ID {channel_id}')
            else:
                print(f'Error sending message to channel with ID {channel_id}: {response.status_code}')

        except requests.exceptions.RequestException as e:
            print(f'Error sending message to channel with ID {channel_id}: {e}')


def get_discord_group_dms(token):
    url = BASE_URL + "/users/@me/channels"
    headers = {
        'Authorization': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        channels = response.json()
        group_dms = [channel for channel in channels if channel['type'] == 3]
        return group_dms
    else:
        response.raise_for_status()


def hypesquad(token, house_id):
    url = BASE_URL + "/hypesquad/online"
    headers = {
        'Authorization': f'{token}',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }
    payload = {
        'house_id': house_id
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
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
            print(
                f'  - Username: {recipient["username"]}, Global Name: {recipient.get("global_name")}, ID: {recipient["id"]}')
        print('-' * 40)


def send_message_to_group(token, message, channel_id):
    url = BASE_URL + f"/channels/{channel_id}/messages"
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


def discord_nitro_expire(token):
    url = BASE_URL + "/users/@me/billing/subscriptions"
    headers = {
        'Authorization': f'{token}',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        subscriptions = response.json()
        if subscriptions:
            for subscription in subscriptions:
                current_period_start = cli.convert_iso_to_readable(subscription['current_period_start'])
                current_period_end = cli.convert_iso_to_readable(subscription['current_period_end'])
                print(f"Current Period Start: {current_period_start}")
                print(f"Current Period End: {current_period_end}")
        else:
            print("No active subscriptions found.")
    else:
        print(f"Error {response.status_code}: {response.text}")


def get_sessions(token):
    url = BASE_URL + "/auth/sessions"
    headers = {
        'Authorization': f'{token}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
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
    url = BASE_URL + "/users/@me/billing/country-code"
    headers = {
        'Authorization': f'{token}',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
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
    url = BASE_URL + f"/users/@me/guilds/{guild_id}"

    headers = {
        'Authorization': f'{token}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        print('Successfully left the server.')
    else:
        print(f'Failed to leave the server. Status code: {response.status_code}, Response: {response.text}')


def create_webhook(token, channel_id, webhook_name):
    url = BASE_URL + f"/channels/{channel_id}/webhooks"

    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    json_data = {
        "name": webhook_name
    }

    response = requests.post(url, headers=headers, json=json_data)

    if response.status_code == 200:
        webhook_info = response.json()
        print(f"Webhook created: {webhook_info['url']}")
    else:
        print(f"Error: {response.status_code}")
        print(response.json())


def delete_channels(guild_id, token):
    # Headers for authorization
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    # Get all channels
    response = requests.get(f'{BASE_URL}/guilds/{guild_id}/channels', headers=headers)
    if response.status_code == 200:
        channels = response.json()
        for channel in channels:
            try:
                channel_id = channel['id']
                # Delete channel

                requests.delete(f'{BASE_URL}/channels/{channel_id}', headers=headers)
                print(f'Channel {channel["name"]} deleted.')
            except Exception as e:
                print(f'Failed to delete channel {channel["name"]}: {e}')
    else:
        print('Failed to retrieve channels:', response.json())


def delete_roles(guild_id, token):
    # Headers for authorization
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }
    # Get all roles

    response = requests.get(f'{BASE_URL}/guilds/{guild_id}/roles', headers=headers)
    if response.status_code == 200:
        roles = response.json()
        for role in roles:
            if role['name'] != "@everyone":  # Do not delete @everyone role
                try:
                    role_id = role['id']
                    # Delete role
                    requests.delete(f'{BASE_URL}/guilds/{guild_id}/roles/{role_id}', headers=headers)
                    print(f'Role {role["name"]} deleted.')
                except Exception as e:
                    print(f'Failed to delete role {role["name"]}: {e}')
    else:
        print('Failed to retrieve roles:', response.json())


def ban_members(guild_id, token):
    # Headers for authorization
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }
    # Get all members

    response = requests.get(f'{BASE_URL}/guilds/{guild_id}/members', headers=headers)
    if response.status_code == 200:
        members = response.json()
        for member in members:
            if member['user']['id'] != guild_id:  # Do not ban server owner
                try:
                    user_id = member['user']['id']
                    # Ban member

                    requests.put(f'{BASE_URL}/guilds/{guild_id}/bans/{user_id}', headers=headers)
                    print(f'{member["user"]["username"]} banned.')
                except Exception as e:
                    print(f'Failed to ban {member["user"]["username"]}: {e}')
    else:
        print('Failed to retrieve members:', response.json())


def change_logo_guild(image_data, token, guild_id):
    base64_image = base64.b64encode(image_data).decode('utf-8')
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    url = f'https://discord.com/api/v9/guilds/{guild_id}'

    json_data = {
        'icon': f'data:image/png;base64,{base64_image}'
    }

    response = requests.patch(
        url,
        headers=headers,
        json=json_data
    )
    if response.status_code == 200:
        print('Server icon changed successfully.')
    else:
        print(f'Failed to change server icon: {response.status_code} - {response.text}')


def change_description(description, token, guild_id):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9154 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36'
    }

    url = BASE_URL + f"/guilds/{guild_id}"

    json_data = {
        'description': description
    }

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
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }

    url = f'{BASE_URL}/guilds/{guild_id}'

    data = {
        'name': new_name
    }

    response = requests.patch(url, headers=headers, json=data)

    if response.status_code == 200:
        print(f'Successfully changed server name to "{new_name}".')
    else:
        print(f'Failed to change server name: {response.status_code}, {response.json()}')
