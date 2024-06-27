import os
import wget
import time

def download_file(url, dest_folder):
    print("Discord.fun Updater")
    print("Wait 3-6 seconds for update")
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
        print("Making dir")
    
    local_filename = os.path.join(dest_folder, url.split('/')[-1])
    
    print("downloading...")
    wget.download(url, local_filename)
    print(f"\nFile downloaded and saved to {local_filename}")
    return local_filename

def open_file(filepath):
    if os.path.isfile(filepath) and filepath.endswith('.exe'):
        if os.name == 'nt':
            os.startfile(filepath)
            print("opening...")
    else:
        print(f"File '{filepath}' is not a valid executable or does not exist.")

def main():
    url = "https://github.com/BrightCat14/discord.fun/releases/download/Discord.fun/discord.fun.exe"
    appdata_folder = os.getenv('APPDATA')
    dest_folder = os.path.join(appdata_folder, 'discordfun')
    if not os.path.exists(os.path.join(dest_folder, "discord.fun.exe")):
        downloaded_file = download_file(url, dest_folder)
    print(f"Attempting to open file: {downloaded_file}")
    open_file(downloaded_file)
    print("Update process completed successfully.")
    time.sleep(1.5)
    print("Closing...")
    exit()

if __name__ == "__main__":
    main()
