import bot
import os
import time
import pickle
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, InvalidCookieDomainException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from credentials import email, password

def play(gameUrl = "", multiplayer = False):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1200, 850)

    print("Logging in...")
    try:
        driver.get("https://www.geoguessr.com/maps/world/play")
        cookies = pickle.load(open("cookies", "rb"))
        for cookie in cookies: driver.add_cookie(cookie)
        driver.refresh()
        WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, "//*[@id='__next']/div/div[2]/div[1]/main/div/div[2]/div/div/div[5]/div/div[1]/div[2]/input")))
    except (FileNotFoundError, InvalidCookieDomainException, TimeoutException) as e:
        print("Authentication error: ", e)
        print("Logging in manually...")
        driver.get("https://www.geoguessr.com/signin?target=%2Fmaps%2Fworld%2Fplay")
        driver.find_element("name", "email").send_keys(email)
        driver.find_element("name", "password").send_keys(password)
        driver.find_element(By.XPATH, "//*[@id='__next']/div/div[2]/div[1]/main/div/div/form/div/div[3]/div/button/div").click()
        WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, "//*[@id='__next']/div/div[2]/div[1]/main/div/div[2]/div/div/div[5]/div/div[1]/div[2]/input")))
        cookies = driver.get_cookies()
        pickle.dump(cookies, open("cookies","wb"))

    print("Creating game...")
    if multiplayer:
        if gameUrl == "":
            driver.find_element(By.XPATH, "//*[@id='__next']/div/div[2]/div[1]/main/div/div[2]/div/div/div[5]/div/div[1]/div[2]/input").click()
            driver.find_element(By.XPATH, "//*[@id='__next']/div/div[2]/div[1]/main/div/div[2]/div/div/div[5]/div/div[2]/div/div[2]/label[1]/div[3]/input").click()
            driver.find_element(By.XPATH, "//*[@id='__next']/div/div[2]/div[1]/main/div/div[2]/div/div/div[5]/div/div[2]/div/div[2]/label[2]/div[3]/input").click()
            driver.find_element(By.XPATH, "//*[@id='__next']/div/div[2]/div[1]/main/div/div[2]/div/div/div[5]/div/div[2]/div/div[2]/label[3]/div[3]/input").click()
            driver.find_element(By.XPATH, "//*[@id='__next']/div/div[2]/div[1]/main/div/div[2]/div/div/div[2]/div[2]").click()
            driver.find_element(By.XPATH, "//*[@id='__next']/div/div[2]/div[1]/main/div/div[2]/div/div/div[3]/button/div").click()
            try: WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, "//*[@id='__next']/div/div[2]/div[1]/main/div/div[2]/div/div/section/article/div/span/input")))
            except TimeoutException: return print("You need Geoguessr Pro to host a multiplayer game.")
            inviteLink = driver.find_element(By.XPATH, "//*[@id='__next']/div/div[2]/div[1]/main/div/div[2]/div/div/section/article/div/span/input")
            print("The game link is: " + inviteLink.get_attribute('value'))
            driver.find_element(By.XPATH, "//*[@id='__next']/div/div[2]/div[1]/main/div/div[2]/div/div/button").click()
        else:
            driver.get(gameUrl)
    else:
        driver.find_element(By.XPATH, "//*[@id='__next']/div/div[2]/div[1]/main/div/div[2]/div/div/div[5]/div/div[1]/div[2]/input").click()
        driver.find_element(By.XPATH, "//*[@id='__next']/div/div[2]/div[1]/main/div/div[2]/div/div/div[5]/div/div[2]/div/div[2]/label[1]/div[3]/input").click()
        driver.find_element(By.XPATH, "//*[@id='__next']/div/div[2]/div[1]/main/div/div[2]/div/div/div[5]/div/div[2]/div/div[2]/label[2]/div[3]/input").click()
        driver.find_element(By.XPATH, "//*[@id='__next']/div/div[2]/div[1]/main/div/div[2]/div/div/div[5]/div/div[2]/div/div[2]/label[3]/div[3]/input").click()
        driver.find_element(By.XPATH, "//*[@id='__next']/div/div[2]/div[1]/main/div/div[2]/div/div/div[3]/div/div/button/div").click()

    try: WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, "//*[@id='__next']/div/div/main/div/div/div[2]/div")))
    except TimeoutException: return print("Your 5 minutes of free exploring has ended. Please wait 15 minutes for your play time to refill.")

    for cookie in cookies:
        if cookie["name"] == "_ncfa": ncfa = cookie["value"]
        if cookie["name"] == "devicetoken": deviceToken = cookie["value"]

    token = requests.get("https://geoguessr.com/api/v3/social/events/unfinishedgames", headers={"Content-Type":"application/json","Cookie":"devicetoken="+deviceToken+"; G_ENABLED_IDPS=google; _ncfa="+ncfa+";"}).json()["games"][0]["token"]

    for i in range(5):
        WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, "//*[@id='__next']/div/div/main/div/div/div[4]/div/div[4]/button")))
        time.sleep(4)
        driver.save_screenshot("screenshot.png")
        coordinates = bot.predict("screenshot.png")[1]
        print("Round " + str(i+1) + "/5", end='\r')
        if os.path.isfile("screenshot.png"): os.remove("screenshot.png")
        requests.post("https://www.geoguessr.com/api/v3/games/"+token, json={"token":token,"lat":coordinates[0],"lng":coordinates[1],"timedOut":False}, headers={"Content-Type":"application/json","Cookie":"devicetoken="+deviceToken+"; G_ENABLED_IDPS=google; _ncfa="+ncfa+";"})
        driver.refresh()
        if multiplayer and i != 4:
            WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, "//*[@id='__next']/div/div/main/div[2]/div/div[2]/div/div[1]/div/div[4]/button/div")))
            driver.find_element(By.XPATH, "//*[@id='__next']/div/div/main/div[2]/div/div[2]/div/div[1]/div/div[4]/button/div").click()

    if multiplayer:
        print("The bot's final score is: " + driver.find_element(By.XPATH, "//*[@id='__next']/div/div[2]/div[1]/main/div/div/div[4]/div[3]/div[7]/div[1]").text + ".")
    else:
        driver.find_element(By.XPATH, "//*[@id='__next']/div/div/main/div[2]/div/div[2]/div/div[1]/div/div[4]/div/button/div").click()
        print("The bot's final score is: " + driver.find_element(By.XPATH, "//*[@id='__next']/div/div/main/div[2]/div/div[2]/div/div[1]/div/div[1]").text + ".")

    driver.close()