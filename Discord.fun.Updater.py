import os
import wget
import time


def download_file(url, dest_folder):
    print("Discord.fun Updater")
    print("Wait 3-6 seconds for update")

    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
        print("Making directory:", dest_folder)

    local_filename = os.path.join(dest_folder, url.split('/')[-1])

    print("Downloading...")
    try:
        wget.download(url, local_filename)
        print(f"\nFile downloaded and saved to {local_filename}")
        return local_filename
    except Exception as e:
        print(f"\nFailed to download file: {e}")
        return None


def open_file(filepath):
    if os.path.isfile(filepath) and filepath.endswith('.exe'):
        try:
            if os.name == 'nt':  # Windows
                os.startfile(filepath)
                print("Opening...")
            else:
                print("Unsupported OS for opening files automatically.")
        except Exception as e:
            print(f"Failed to open file: {e}")
    else:
        print(f"File '{filepath}' is not a valid executable or does not exist.")


def main():
    url = "https://github.com/BrightCat14/discord.fun/releases/download/Discord.fun/discord.fun.exe"
    appdata_folder = os.getenv('APPDATA')
    dest_folder = os.path.join(appdata_folder, 'discordfun')
    downloaded_file = os.path.join(dest_folder, "discord.fun.exe")

    downloaded_file = download_file(url, dest_folder)
    if not downloaded_file:
        print("Update process failed.")
        return

    print(f"Attempting to open file: {downloaded_file}")
    open_file(downloaded_file)

    print("Update process completed successfully.")
    time.sleep(1.5)
    print("Closing...")


if __name__ == "__main__":
    main()
