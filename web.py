import bot
from selenium import webdriver

def local():
    # TODO
    driver = webdriver.Chrome()
    driver.get()
    country, coordinates, _ = bot.predict("/screenshot.png")

def multiplayer():
    # TODO
    driver = webdriver.Chrome()
    driver.get()
    country, coordinates, _ = bot.predict("/screenshot.png")
    