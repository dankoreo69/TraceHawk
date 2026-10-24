from tools.IGscrape import IGScrape

def handle_ig_scrape():
    username = input("Enter Instagram username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return
    IGScrape(username)
