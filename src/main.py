import os
import platform
import sys
import traceback

from colorama import Fore

if not os.getenv("TERM") and platform.system() == "Linux":
    os.environ.setdefault(
        "TERM", "dumb"
    )  # for correct work of colorama, sorry for stupid fix

# for time
import time

# for cli
import colorama

# for discord api
import requests
from discord_webhook import DiscordWebhook

# some utils
from src import utils, cli, api, constants, nuke_bot

colorama.init()
utils.__init()


def main():
    while True:
        cli.clear_screen()

        prompt = cli.get_prompt()

        utils.print_menu(1)
        choice = input(prompt)
        utils.log(f"Menu is 1, choice: {choice}", no_silent=False)

        if choice == "1":
            cli.clear_screen()
            token = cli.get_input("Enter your token")
            friends = api.get_friends_list_user(token)
            utils.log(friends)
            cli.get_return_input()
        elif choice == "2":
            cli.clear_screen()
            login = cli.get_input("Enter your email")
            password = cli.get_input("Enter your password")
            api.get_token(login, password)
            cli.get_return_input()
        elif choice == "3":
            cli.clear_screen()
            token = cli.get_input("Enter your token")
            friend_ids = api.get_friends_list(token)
            message_content = cli.get_input("What message to send?")
            api.send_message_to_friend(token, message_content, friend_ids)
            cli.get_return_input()
        elif choice == "9":
            cli.clear_screen()
            while True:
                cli.clear_screen()
                utils.print_menu(2)
                choice_page_2 = input(prompt)
                utils.log(f"Menu is 2, choice: {choice_page_2}", no_silent=False)
                if choice_page_2 == "1":
                    cli.clear_screen()
                    token = cli.get_input("Enter your token")
                    _type = cli.get_input(
                        f"Enter type of custom status (online, idle, dnd, invisible): "
                    )
                    text = cli.get_input(f"Enter text of custom status: ")

                    encoded_str = r"WicKCAoGb25saW5lEhcKDFRoaW5raW5n8J+klCGAfH9bkAEAABoCCAE="  # magic string, please dont change it

                    replacements = {"online": _type, "Thinking": text}

                    api.change_custom_status(encoded_str, replacements, token)
                    cli.get_return_input()
                elif choice_page_2 == "2":
                    token = cli.get_input("Enter your token")
                    boost_count = cli.get_input(f"Enter boost count")
                    server_id = cli.get_input(f"Enter your server id")
                    url = api.BASE_URL + f"/guilds/{server_id}/premium/subscriptions"

                    headers = {
                        "Authorization": f"{token}",
                        "Content-Type": "application/json",
                        "User-Agent": constants.UA,
                    }

                    payload = {
                        "user_premium_guild_subscription_slot_ids": f"{server_id}"
                    }

                    for _ in range(int(boost_count)):
                        time.sleep(0.5)
                        response = requests.post(url, headers=headers, json=payload)

                        if response.status_code == 201:
                            utils.log(f"Server boosted successfully!")
                        else:
                            utils.log(
                                f"Failed to boost server. Status code: {response.status_code}"
                            )
                            utils.log(response.text)
                        continue
                elif choice_page_2 == "4":
                    token = cli.get_input("Enter your token")
                    server_id = cli.get_input(f"Enter your server id")
                    api.leaver(token, server_id)
                    cli.get_return_input()
                elif choice_page_2 == "6":
                    token = cli.get_input("Enter your token")
                    server_id = cli.get_input(f"Enter your server id")
                    api.get_list_channels_id(server_id, token)
                    cli.get_return_input()
                elif choice_page_2 == "7":
                    token = cli.get_input("Enter your token")
                    server_id = cli.get_input(f"Enter your server id")
                    message_content = cli.get_input(f"What message to send?")
                    ids = api.sys_get_channels_id(server_id, token)
                    api.send_message_to_channel(token, message_content, ids)
                    cli.get_return_input()
                elif choice_page_2 == "8":
                    token = cli.get_input("Enter your token")
                    # server_id = cli.get_input(f'Enter your server id') wtf
                    message_content = cli.get_input(f"What message to send?")
                    identifier = cli.get_input(f"Enter channel id or channels ids")
                    api.send_message_to_channel(token, message_content, identifier)
                    cli.get_return_input()
                elif choice_page_2 == "9":
                    while True:
                        cli.clear_screen()
                        utils.print_menu(3)
                        choice_page_3 = input(prompt)
                        utils.log(
                            f"Menu is 3, choice: {choice_page_3}", no_silent=False
                        )
                        if choice_page_3 == "1":
                            token = cli.get_input("Enter your token")
                            group_id = cli.get_input(f"Enter your group id")
                            is_enabled = True

                            message = utils.crazy_big
                            name = utils.crazy_small

                            while is_enabled:
                                api.send_message_group(group_id, message, token)
                                api.change_name_group(group_id, name, token)
                            cli.get_return_input()
                        elif choice_page_3 == "2":
                            token = cli.get_input(f"Enter your token")
                            channel_id = cli.get_input(f"Enter the channel ID")
                            message_id = cli.get_input(f"Enter the message ID")
                            thread_name = cli.get_input(f"Enter the thread name")
                            is_enabled = True

                            # message = utils.crazy_big
                            # name = utils.crazy_small

                            while is_enabled:
                                api.thread_spammer(
                                    token, channel_id, message_id, thread_name
                                )
                            cli.get_return_input()
                        elif choice_page_3 == "3":
                            token = cli.get_input(f"Enter your token")
                            channel_id = cli.get_input(f"Enter the channel ID")
                            is_enabled = True
                            while is_enabled:
                                time.sleep(1.5)
                                api.typer(channel_id, token)
                            cli.get_return_input()
                        elif choice_page_3 == "4":
                            token = cli.get_input(f"Enter your token")

                            groups_ids = api.get_discord_group_dms(token)
                            if not isinstance(groups_ids, int):
                                api.print_group_dms(groups_ids)
                            else:
                                utils.log(f"Failed to fetch, error: {groups_ids}")
                            cli.get_return_input()
                        elif choice_page_3 == "5":
                            token = cli.get_input(f"Enter your token")
                            message = cli.get_input(f"What message to send?")

                            groups_dms = api.get_discord_group_dms(token)
                            if not isinstance(groups_dms, int):
                                for dm in groups_dms:
                                    utils.log(f"Sending message to {dm['id']}")
                                    api.send_message_to_group(token, message, dm["id"])
                            else:
                                utils.log(f"Failed to fetch, error: {groups_dms}")
                        elif choice_page_3 == "6":
                            token = cli.get_input(f"Enter your token")
                            message = cli.get_input(f"What message to send?")
                            groups_dms = cli.get_input(
                                "Enter group id or ids (e.g. 1234567890, 1234567890)"
                            )
                            dm_list = groups_dms.split(",")
                            for dm in dm_list:
                                dm = dm.strip()
                                utils.log(f"Sending message to {dm}")
                                api.send_message_to_group(token, message, dm)
                        elif choice_page_3 == "7":
                            url = cli.get_input(f"Enter webhook url")
                            content = cli.get_input(f"What message to send?")
                            while True:
                                webhook = DiscordWebhook(url=url, content=content)
                                response = webhook.execute()
                                if response.status_code in (200, 201):
                                    utils.log("Successfully sent message to " + url)
                                elif response.status_code == 429:
                                    retry_after = response.json().get("retry_after", 1)
                                    time.sleep(retry_after)

                                    webhook = DiscordWebhook(url=url, content=content)
                                    response = webhook.execute()
                                    if response.status_code in (200, 201):
                                        utils.log("Successfully sent message to " + url)
                        elif choice_page_3 == "8":
                            url = cli.get_input(f"Enter webhook url")
                            content = cli.get_input(f"What message to send?")

                            webhook = DiscordWebhook(url=url, content=content)
                            response = webhook.execute()
                            if response.status_code == 201 or 200:
                                utils.log("Successfully sent the message")
                            else:
                                utils.log("Error: " + response.json())
                        elif choice_page_3 == "9":
                            while True:
                                cli.clear_screen()
                                utils.print_menu(4)
                                choice_page_4 = input(prompt)
                                utils.log(
                                    f"Menu is 4, choice: {choice_page_4}",
                                    no_silent=False,
                                )
                                if choice_page_4 == "1":
                                    token = cli.get_input(f"Enter your token")
                                    api.discord_nitro_expire(token)
                                    cli.get_return_input()
                                elif choice_page_4 == "2":
                                    token = cli.get_input(f"Enter your token")
                                    api.country_code_by(token)
                                    cli.get_return_input()
                                elif choice_page_4 == "3":
                                    token = cli.get_input(f"Enter your token")
                                    api.get_sessions(token)
                                    cli.get_return_input()
                                elif choice_page_4 == "4":
                                    token = cli.get_input(f"Enter your token")
                                    message = cli.get_input(f"What message to send?")
                                    dm = cli.get_input(
                                        "Enter channel id (e.g. 1234567890)"
                                    )
                                    is_enabled = True
                                    while is_enabled:
                                        api.send_message_to_group(token, message, dm)
                                elif choice_page_4 == "5":
                                    token = cli.get_input(f"Enter your token")
                                    house_id = cli.get_input(
                                        f"1 - Bravery\n2 - Brilliance\n3 - Balance\nEnter house_id"
                                    )
                                    api.change_hype_squad(token, house_id)
                                    cli.get_return_input()
                                elif choice_page_4 == "6":
                                    token = cli.get_input(f"Enter your token")
                                    channel_id = cli.get_input(f"Enter channel id")
                                    webhook_name = cli.get_input(f"Enter webhook name")
                                    api.create_webhook(token, channel_id, webhook_name)
                                elif choice_page_4 == "7":
                                    choice_raid = cli.get_input(
                                        "Which type of raid do you prefer? (1 - Self-bot, 2 - Bot)"
                                    )
                                    if choice_raid == "1":
                                        token = cli.get_input(f"Enter your token")
                                        guild_id = cli.get_input(f"Enter guild id")
                                        utils.log("Starting server nuke...")
                                        api.delete_channels(guild_id, token)
                                        api.delete_roles(guild_id, token)
                                        api.change_server_name(
                                            guild_id, constants.name, token
                                        )
                                        image_url = constants.ICON_URL
                                        api.change_logo_guild(
                                            utils.get_picture_by_url(image_url),
                                            token,
                                            guild_id,
                                        )
                                        api.change_description(
                                            f"Nuked by {constants.name}",
                                            token,
                                            guild_id,
                                        )
                                        utils.log("Server has been nuked.")
                                        cli.get_return_input()
                                    elif choice_raid == "2":
                                        token = cli.get_input(f"Enter bot token")
                                        bot = nuke_bot.bot
                                        bot.run(token)
                                elif choice_page_4 == "8":
                                    token = cli.get_input(f"Enter your token")
                                    api.print_info_user(token)
                                    cli.get_return_input()
                                elif choice_page_4 == "0":
                                    break
                        elif choice_page_3 == "0":
                            break
                elif choice_page_2 == "3":
                    token = cli.get_input("Enter your token")
                    invite_link = cli.get_input(
                        f"Enter your invite link (https://discord.gg/example)"
                    )
                    api.join_server(invite_link, token)
                    cli.get_return_input()
                elif choice_page_2 == "5":
                    token = cli.get_input("Enter your token")
                    guilds = api.get_discord_guilds_user(token)
                    utils.log(guilds)
                    cli.get_return_input()
                elif choice_page_2 == "0":
                    break
                else:
                    utils.log("Invalid choice")
                    cli.get_return_input()
        elif choice == "4":
            cli.clear_screen()
            token = cli.get_input(f"Enter your token")
            friend_ids = cli.get_input(
                f"Enter friend id or ids (e.g. 1234567890, 1234567890)"
            )
            friend_ids1 = [friend_ids]
            message_content = cli.get_input("What message to send?")
            api.send_message_to_friend(token, message_content, friend_ids1)
        elif choice == "5":
            cli.clear_screen()
            token = cli.get_input(f"Enter your token")
            bio = cli.get_input(f"Enter bio to change")
            api.change_bio(token, bio)
            cli.get_return_input()
        elif choice == "6":
            cli.clear_screen()
            token = cli.get_input(f"Enter your token")
            display_name = cli.get_input(f"Enter display name to change")
            api.change_display_name(token, display_name)
            cli.get_return_input()
        elif choice == "8":
            cli.clear_screen()
            token = cli.get_input(f"Enter your token")
            pronouns = cli.get_input(f"Enter pronouns to change")
            api.change_pronouns(token, pronouns)
            cli.get_return_input()
        elif choice == "7":
            cli.clear_screen()
            password = cli.get_input(f"Enter your password")
            token = cli.get_input(f"Enter your token")
            username = cli.get_input(f"Enter username to change")
            api.change_username(username, password, token)
            cli.get_return_input()
        elif choice == "0":
            sys.exit(0)
        else:
            utils.log("Invalid choice. Please enter a valid option.")
            cli.get_return_input()


if __name__ == "__main__":
    try:
        error = main()
        utils.log(
            f"{Fore.RED}{constants.name.capitalize()} {constants.version} is exited, code: {error}{Fore.RESET}"
        )
    except Exception as e:
        utils.log(
            f"{Fore.RED}{constants.name.capitalize()} {constants.version} is crashed, code: {e}{Fore.RESET}"
        )
        utils.log(f"Traceback:")
        traceback.print_exc()
