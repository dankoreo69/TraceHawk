import base64
import os
import subprocess
import sys

from tools import IGscrape, phonelookup
from tools.angryipscanner import run_scan
from tools.darkweb import darkweb
from tools.dirbuster import dirbuster
from tools.dork import dork
from tools.doxx import create_osint_profile
from tools.internetsearch import start_search
from tools.ip_grabber import ipgrabber
from tools.ip_lookup import run_menu
from tools.nmapscan import nmapscan
from tools.passcrack import passcrack
from tools.passhasher import passhasher
from tools.rev import generate
from tools.snake import start_game
from tools.usersearch import main as username_search

PURPLE = "\033[35m"
RESET = "\033[0m"

if sys.platform == "win32":
    # Redirected Windows output defaults to the legacy code page, which cannot
    # encode the banner's box-drawing characters. Force UTF-8 when possible.
    for _stream in (sys.stdout, sys.stderr):
        try:
            _stream.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass

def obfuscate_payload():
    lang = input("\033[36mEnter language (bash/python/php/nc/powershell): \033[0m").strip().lower()
    payload = input("\033[36mEnter your payload: \033[0m").strip()

    def obfuscate(p, l):
        if l == "bash":
            return f"eval $(echo {base64.b64encode(p.encode()).decode()} | base64 -d)"
        elif l == "python":
            encoded = base64.b64encode(p.encode()).decode()
            return f"import base64; exec(base64.b64decode('{encoded}'))"
        elif l == "php":
            encoded = base64.b64encode(p.encode()).decode()
            return f"<?php eval(base64_decode('{encoded}')); ?>"
        elif l == "nc":
            return f"# Original: {p}\n# Netcat doesn't obfuscate well. Wrap in a script instead."
        elif l == "powershell":
            encoded = base64.b64encode(p.encode('utf-16le')).decode()
            return f"powershell -EncodedCommand {encoded}"
        else:
            return "[ERROR] Unsupported language."

    result = obfuscate(payload, lang)
    print(f"\n\033[32m[+] Obfuscated Payload:\033[0m\n{result}")

def insta_scrape():
    target = input("\033[36mEnter the Instagram username to scrape (e.g., 'username'):\033[0m ").strip()
    if target:
        IGscrape.IGScrape(target)
    else:
        print("\033[31m[ERROR]\033[0m No username provided!")

def reverse_shell():
    ip = input("Enter IP: ")
    port = input("Enter Port: ")
    lang = input("Enter language (bash/python/php/nc/powershell): ")
    try:
        payload = generate(ip, port, lang)
        print(f"\nPayload:\n{payload}")
    except ValueError as e:
        print(f"\033[31m[ERROR]\033[0m {e}")

def play_flappy():
    script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools", "flappy.py")
    try:
        subprocess.call([sys.executable, script])
    except OSError as e:
        print(f"\033[31m[ERROR]\033[0m Could not start Flappy Bird: {e}")

TOOLS = {
    "1": ("IP Lookup", run_menu),
    "2": ("InstaScrape", insta_scrape),
    "3": ("Phone Lookup", lambda: phonelookup.LookUp(input("\033[36mEnter phone number (With Country Code): \033[0m "))),
    "4": ("Username Search", username_search),
    "5": ("Search Dorks", dork),
    "6": ("DuckDuckGo Search Links", start_search),
    "7": ("DarkWeb Links", darkweb),
    "9": ("Obfuscate", obfuscate_payload),
    "10": ("Reverse Shell", reverse_shell),
    "12": ("DOXX Creator", create_osint_profile),
    "13": ("AngryIPScanner", run_scan),
    "14": ("IP Grabber", lambda: ipgrabber().start()),
    "15": ("Pass-Cracker", passcrack),
    "16": ("Pass-Hasher", passhasher),
    "21": ("DirBuster", dirbuster),
    "22": ("Nmap Scan", nmapscan),
    "90": ("Snake Game", start_game),
    "91": ("Flappy Bird", play_flappy),
}

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

MENU_ART = r"""
 ______                 __ __            __
/_  __/______ ________ / // /__ __    __/ /__
 / / / __/ _ `/ __/ -_) _  / _ `/ |/|/ /  '_/
/_/ /_/  \_,_/\__/\__/_//_/\_,_/|__,__/_/\_\ 
                                              Created by dankoreo69
                Support on YouTube: https://youtube.com/@dankoreo69
                Support on github:  https://github.com/dankoreo69
 ┌──────────────┐  ┌──────────────────┐   ┌────────────┐   ┌────────────┐
 │    OSINT     ├──┤ OFFENSIVE TOOLS  ├───┤   WEBSITE  ├───┤  T.GAMES   │
 └──────────────┘  └──────────────────┘   └────────────┘   └────────────┘
 (01) IPlookup      (09) Obfuscate         (21) DirBuster   (90) Snake
 (02) InstaScrape   (10) Rev Shell Payload (22) Nmap Scan   (91) Flappy Bird
 (03) Phone Lookup  (11)                   (23)             (92)
 (04) UserSearch    (12) DOXX Creator      (24)             (93)
 (05) Search Dorks  (13) AngryIPScanner    (25)             (94)
 (06) Internet Surf (14) IP-Grabber        (26)             (95)
 (07) DarkWeb Links (15) Pass-Cracker      (27)             (96)
 (08)               (16) Pass-Hasher       (28)             (97)
"""

def menu():
    print(PURPLE + MENU_ART + RESET)

def main():
    clear()
    while True:
        try:
            menu()
            choice = input("\033[32mEnter your choice (0 to exit): \033[0m").strip()
            if choice == "0":
                print("\033[33m[!] Goodbye!\033[0m")
                print("\033[34mCreated by dankoreo69\033[0m")
                print("\033[34mSupport on YouTube: https://youtube.com/@dankoreo69?si=YqcM1PeIRUJRSg_H\033[0m")
                break
            elif choice in TOOLS:
                try:
                    TOOLS[choice][1]()
                except ValueError as e:
                    print(f"\033[31m[ERROR]\033[0m Invalid value: {e}")
                except Exception as e:
                    print(f"\033[31m[ERROR]\033[0m Unexpected error: {e}")

                input(f"\n{PURPLE}Press Enter to return to the menu...{RESET}")
                clear()
            else:
                clear()
                continue
        except KeyboardInterrupt:
            print(f"\n\033[33m[!] Interrupted - returning to the menu (0 to exit).{RESET}")
            clear()
        except EOFError:
            print()
            break

if __name__ == "__main__":
    main()

