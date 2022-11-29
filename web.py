import bot
from selenium import webdriver

def local():
    # TODO
    driver = webdriver.Chrome()
    driver.get()
    country, coordinates, _ = bot.predict("/screenshot.png")

def multiplayer(game_id):
    # TODO
    if game_id == "":
        pass
    else:
        pass
    
    driver = webdriver.Chrome()
    driver.get()
    country, coordinates, _ = bot.predict("/screenshot.png")
    