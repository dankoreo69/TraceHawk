import requests
from datetime import datetime
from time import sleep
import random
import os

BLUE = "\033[34m"
RESET = "\033[0m"

banner = """\033[91m
                                                  __
  __  __________  _____________  ____ ___________/ /_
 / / / / ___/ _ \/ ___/ ___/ _ \/ __ `/ ___/ ___/ __ \ 
/ /_/ (__  )  __/ /  (__  )  __/ /_/ / /  / /__/ / / /
\__,_/____/\___/_/  /____/\___/\__,_/_/   \___/_/ /_/

\033[0m"""

def current_time():
    """Return current time formatted as HH:MM:SS"""
    return datetime.now().strftime("%H:%M:%S")

def slow_print(text, delay=0.02):
    """Prints text with slow printing effect, all in blue"""
    print(BLUE, end="")
    for char in text:
        print(char, end="", flush=True)
        sleep(delay)
    print(RESET)

def choose_user_agent():
    """Randomly select a User-Agent for requests"""
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (X11; Linux x86_64)",
    ]
    return random.choice(agents)

def log(message, prefix="INFO"):
    """Log messages with current time and prefix"""
    print(f"{BLUE}[{current_time()}] [{prefix}] {message}{RESET}")

def is_username_found(response_text, username, site_info):
    """Check if username appears to be present based on verification method"""
    if site_info["verification"] == "status":
        return response_text.status_code == 200
    if site_info["verification"] == "username":
        if site_info.get("except"):
            for ex in site_info["except"]:
                if ex.lower() in response_text.text.lower():
                    return False
        return username.lower() in response_text.text.lower()
    return False


def get_sites(username):
    """Returns the dictionary with dynamic URLs based on username"""
    return {
        "Steam": {
            "url": f"https://steamcommunity.com/id/{username}",
            "method": "get",
            "verification": "username",
            "except": None
        },
        "Telegram": {
            "url": f"https://t.me/{username}",
            "method": "get",
            "verification": "username",
            "except": [f"if you have telegram, you can contact @{username} right away.", f"resolve?domain={username}", f"telegram: contact @{username}"]
        },
        "TikTok": {
            "url": f"https://www.tiktok.com/@{username}",
            "method": "get",
            "verification": "username",
            "except": [f"\\u002f@{username}\""]
        },
        "Instagram": {
            "url": f"https://www.instagram.com/{username}",
            "method": "get",
            "verification": "username",
            "except": None
        },
        "Paypal": {
            "url": f"https://www.paypal.com/paypalme/{username}",
            "method": "get",
            "verification": "username",
            "except": [f"slug_name={username}", f"\"slug\":\"{username}\"", f"2F{username}&amp"]
        },
        "GitHub": {
            "url": f"https://github.com/{username}",
            "method": "get",
            "verification": "status",
            "except": None
        },
        "Giters": {
            "url": f"https://giters.com/{username}",
            "method": "get",
            "verification": "status",
            "except": None
        },
        "Pinterest": {
            "url": f"https://www.pinterest.com/{username}",
            "method": "get",
            "verification": "username",
            "except": [f"[\\\"username\\\",\\\"{username}\\\"]"]
        },
        "Snapchat": {
            "url": f"https://www.snapchat.com/add/{username}",
            "method": "get",
            "verification": "status",
            "except": None
        },
        "Blogger": {
            "url": f"https://{username}.blogspot.com",
            "method": "get",
            "verification": "status",
            "except": None
        },
        "Tumblr": {
            "url": f"https://{username}.tumblr.com",
            "method": "get",
            "verification": "status",
            "except": None
        },
        "SoundCloud": {
            "url": f"https://soundcloud.com/{username}",
            "method": "get",
            "verification": "status",
            "except": None
        },
        "DeviantArt": {
            "url": f"https://www.deviantart.com/{username}",
            "method": "get",
            "verification": "status",
            "except": None
        },
        "About.me": {
            "url": f"https://about.me/{username}",
            "method": "get",
            "verification": "status",
            "except": None
        },
        "Flickr": {
            "url": f"https://www.flickr.com/people/{username}",
            "method": "get",
            "verification": "status",
            "except": None
        },
        "Keybase": {
            "url": f"https://keybase.io/{username}",
            "method": "get",
            "verification": "status",
            "except": None
        },
        "Last.fm": {
            "url": f"https://www.last.fm/user/{username}",
            "method": "get",
            "verification": "status",
            "except": None
        },
        "Behance": {
            "url": f"https://www.behance.net/{username}",
            "method": "get",
            "verification": "status",
            "except": None
        },
        "Quora": {
            "url": f"https://www.quora.com/profile/{username}",
            "method": "get",
            "verification": "status",
            "except": None
        },
        "Patreon": {
            "url": f"https://www.patreon.com/{username}",
            "method": "get",
            "verification": "status",
            "except": None
        },
        "Myspace": {
            "url": f"https://myspace.com/{username}",
            "method": "get",
            "verification": "username",
            "except": None
        },
        "Kaggle": {
            "url": f"https://www.kaggle.com/{username}",
            "method": "get",
            "verification": "username",
            "except": None
        },
        "Periscope": {
            "url": f"https://www.pscp.tv/{username}",
            "method": "get",
            "verification": "username",
            "except": None
        },
        "Disqus": {
            "url": f"https://disqus.com/by/{username}",
            "method": "get",
            "verification": "username",
            "except": None
        },
        "Mastodon": {
            "url": f"https://mastodon.social/@{username}",
            "method": "get",
            "verification": "username",
            "except": None
        },
        "GitLab": {
            "url": f"https://gitlab.com/{username}",
            "method": "get",
            "verification": "username",
            "except": None
        },
        "LiveJournal": {
            "url": f"https://{username}.livejournal.com",
            "method": "get",
            "verification": "username",
            "except": None
        },
        "CodeWars": {
            "url": f"https://www.codewars.com/users/{username}",
            "method": "get",
            "verification": "username",
            "except": None
        },
        "Gumroad": {
            "url": f"https://gumroad.com/{username}",
            "method": "get",
            "verification": "username",
            "except": None
        },
        "Spotify": {
            "url": f"https://open.spotify.com/user/{username}",
            "method": "get",
            "verification": "username",
            "except": None
        },
        "Weebly": {
            "url": f"https://{username}.weebly.com",
            "method": "get",
            "verification": "username",
            "except": None
        },
        "YouTube": {
            "url": f"https://www.youtube.com/@{username}",
            "method": "get",
            "verification": "username",
            "except": None
        },
        "ProductHunt": {
            "url": f"https://www.producthunt.com/@{username}",
            "method": "get",
            "verification": "username",
            "except": None
        },
        "Mix": {
            "url": f"https://mix.com/{username}",
            "method": "get",
            "verification": "username",
            "except": None
        },
        "Facebook": {
            "url": f"https://www.facebook.com/{username}",
            "method": "get",
            "verification": "username",
            "except": None
        },
        "Strava": {
            "url": f"https://www.strava.com/athletes/{username}",
            "method": "get",
            "verification": "username",
            "except": None
        },
        "Internet Archive": {
            "url": f"https://archive.org/search?query={username}",
            "method": "get",
            "verification": "status",
            "except": None
        },
        "Twitter Archive": {
            "url": f"https://web.archive.org/web/*/https://twitter.com/{username}/status/*",
            "method": "get",
            "verification": "status",
            "except": ["No URL has been captured for this URL prefix."]
        },
        "Linktree": {
            "url": f"https://linktr.ee/{username}",
            "method": "get",
            "verification": "status",
            "except": None
        },
        "Xbox": {
            "url": f"https://www.xboxgamertag.com/search/{username}",
            "method": "get",
            "verification": "status",
            "except": None
        },
        "Twitter": {
            "url": f"https://twitter.com/{username}",
            "method": "get",
            "verification": "status",
            "except": None
        },
        "Vimeo": {
            "url": f"https://vimeo.com/{username}",
            "method": "get",
            "verification": "status",
            "except": None
        },
        "Twitch": {
            "url": f"https://www.twitch.tv/{username}",
            "method": "get",
            "verification": "username",
            "except": None
        },
        "Goodreads": {
            "url": f"https://www.goodreads.com/{username}",
            "method": "get",
            "verification": "status",
            "except": None
        },
        "VK": {
            "url": f"https://vk.com/{username}",
            "method": "get",
            "verification": "status",
            "except": None
        },
        "TripAdvisor": {
            "url": f"https://www.tripadvisor.com/members/{username}",
            "method": "get",
            "verification": "status",
            "except": None
        },
        "Dribbble": {
            "url": f"https://dribbble.com/{username}",
            "method": "get",
            "verification": "status",
            "except": None
        },
        "AngelList": {
            "url": f"https://angel.co/{username}",
            "method": "get",
            "verification": "status",
            "except": None
        },
        "500px": {
            "url": f"https://500px.com/{username}",
            "method": "get",
            "verification": "username",
            "except": None
        },
        "LinkedIn": {
            "url": f"https://www.linkedin.com/in/{username}",
            "method": "get",
            "verification": "status",
            "except": None
        },
        "WhatsApp": {
            "url": f"https://wa.me/{username}",
            "method": "get",
            "verification": "status",
            "except": None
        },
        "Weibo": {
            "url": f"https://weibo.com/{username}",
            "method": "get",
            "verification": "username",
            "except": None
        },
        "OKCupid": {
            "url": f"https://www.okcupid.com/profile/{username}",
            "method": "get",
            "verification": "status",
            "except": None
        },
        "Meetup": {
            "url": f"https://www.meetup.com/members/{username}",
            "method": "get",
            "verification": "username",
            "except": None
        },
        "CodePen": {
            "url": f"https://codepen.io/{username}",
            "method": "get",
            "verification": "status",
            "except": None
        },
        "StackOverflow": {
            "url": f"https://stackoverflow.com/users/{username}",
            "method": "get",
            "verification": "status",
            "except": None
        },
        "HackerRank": {
            "url": f"https://www.hackerrank.com/{username}",
            "method": "get",
            "verification": "username",
            "except": None
        },
        "Xing": {
            "url": f"https://www.xing.com/profile/{username}",
            "method": "get",
            "verification": "status",
            "except": None
        },
        "Deezer": {
            "url": f"https://www.deezer.com/en/user/{username}",
            "method": "get",
            "verification": "status",
            "except": None
        },
        "Snapfish": {
            "url": f"https://www.snapfish.com/{username}",
            "method": "get",
            "verification": "status",
            "except": None
        },
    }


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(banner)
    slow_print("🔍 Username Tracker Tool")
    
    user_agent = choose_user_agent()
    headers = {"User-Agent": user_agent}
    
    log(f"Using User-Agent: {user_agent}")
    username = input(f"{BLUE}Enter the username to check: {RESET}").strip()

    found = []
    not_found = []

    SITES = get_sites(username)
    
    for site, config in SITES.items():
        try:
            url = config["url"].format(username=username)

            log(f"Checking {site}: {url}", "CHECK")

            response = requests.get(url, headers=headers, timeout=5)

            if is_username_found(response, username, config):
                found.append((site, url))
                log(f"✅ Found on {site}: {url}", "FOUND")
            else:
                not_found.append(site)
                log(f"❌ Not found on {site}", "NOTFOUND")

        except requests.RequestException as e:
            log(f"⚠ Error checking {site}: {e}", "ERROR")
            continue

        sleep(1.2)

    print("\n====== SUMMARY ======")
    print(f"✅ Found on {len(found)} platforms: ")
    for s, u in found:
        print(f"  - {BLUE}{s}: {u}{RESET}")

    print(f"❌ Not found on {len(not_found)} platforms.")

if __name__ == "__main__":
    main()
