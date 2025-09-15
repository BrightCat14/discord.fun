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
    prompt = f"{Fore.LIGHTGREEN_EX}{utils.username}@kali:{Fore.BLUE}/{utils.folder_name}${Fore.LIGHTGREEN_EX}{tabber.space()}"

    with open(utils.theme_cfg, "r") as f:
        theme = f.read().strip()
    with open(utils.custom_prompt_path, "r") as f:
        try:
            custom_prompt = utils.parse_custom_prompt(f.read().strip())
        except Exception:
            custom_prompt = prompt

    plugin_prompts = []
    for key, plugin in utils.plugins_globals.items():
        if key.startswith("__"):
            continue
        prompt_func = getattr(plugin, "prompt", None)
        if callable(prompt_func):
            try:
                plugin_prompts.append(str(prompt_func()))
            except Exception as e:
                utils.log(
                    f"[!] Failed to get prompt from plugin {key}: {e}", no_silent=True
                )

    if plugin_prompts:
        return " ".join(plugin_prompts) + tabber.space()

    if theme == "kali-old":
        pass  # by default prompt is kali old, see up
    elif theme == "windows":
        prompt = f"{utils.current_directory}>{tabber.space()}"
    elif theme == "omz":
        prompt = f"{Fore.LIGHTGREEN_EX}→{Fore.RESET}{tabber.space()}{Fore.LIGHTBLUE_EX}{utils.folder_name}{Fore.RESET}{tabber.space()}{Fore.MAGENTA}git:({Fore.RED}{constants.vX}{Fore.MAGENTA}){Fore.RESET}{tabber.space()}{Fore.YELLOW}✘{Fore.RESET}{tabber.space()}"
    elif theme == "boring":
        prompt = f"${tabber.space()}"
    elif theme == "custom":
        prompt = custom_prompt

    return prompt


def clear_screen():
    os.system("cls" if platform.system() == "Windows" else "clear")


def set_console_title(title):
    system = platform.system()
    if system == "Windows":
        os.system(f"title {title}")
    elif system in ["Linux", "Darwin"]:
        print(f"\x1b]2;{title}\x07", end="")
    else:
        utils.log(
            "Unsupported operating system for setting console title.", no_silent=True
        )
