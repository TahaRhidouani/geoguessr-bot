import bot
from selenium import webdriver

def local():
    # TODO
    driver = webdriver.Chrome()
    driver.get()
    country, coordinates, _ = bot.predict("/screenshot.png")

def multiplayer(game_id):
    # TODO
    driver = webdriver.Chrome()
    driver.get()
    country, coordinates, _ = bot.predict("/screenshot.png")
    