import bot
from selenium import webdriver

def local():
    driver = webdriver.Chrome()
    driver.get()
    country, coordinates, _ = bot.predict("/screenshot.png")

def multiplayer(game_id):
    if game_id == "":
        # Create game and print code
        pass
    else:
        # Join game
        pass

    driver = webdriver.Chrome()
    driver.get()
    country, coordinates, _ = bot.predict("/screenshot.png")
    