import bot

from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

def getLoginInfo():
    with open("password") as f:
        for i, line in enumerate(f):
            if i == 0: email = line
            if i == 1: password = line
    return email, password

def local():
    pass

def multiplayer(gameUrl):
    driver = webdriver.Chrome()
    driver.set_window_size(2272, 1324)

    email, password = getLoginInfo()
    driver.get("https://www.geoguessr.com/signin?target=%2Fmaps%2Fworld%2Fplay")
    driver.find_element("name", "email").send_keys(email)
    driver.find_element("name", "password").send_keys(password).submit()
    WebDriverWait(driver, 15).until(expected_conditions.presence_of_element_located((By.XPATH, "//*[@id='__next']/div/div[2]/div[1]/main/div/div[2]/div/div/div[5]/div/div[1]/div[2]/input")))

    if gameUrl == "":
        driver.find_element(By.XPATH, "//*[@id='__next']/div/div[2]/div[1]/main/div/div[2]/div/div/div[5]/div/div[1]/div[2]/input").click()
        driver.find_element(By.XPATH, "//*[@id='__next']/div/div[2]/div[1]/main/div/div[2]/div/div/div[5]/div/div[2]/div/div[2]/label[1]/div[3]/input").click()
        driver.find_element(By.XPATH, "//*[@id='__next']/div/div[2]/div[1]/main/div/div[2]/div/div/div[5]/div/div[2]/div/div[2]/label[2]/div[3]/input").click()
        driver.find_element(By.XPATH, "//*[@id='__next']/div/div[2]/div[1]/main/div/div[2]/div/div/div[5]/div/div[2]/div/div[2]/label[3]/div[3]/input").click()
        driver.find_element(By.XPATH, "//*[@id='__next']/div/div[2]/div[1]/main/div/div[2]/div/div/div[2]/div[2]").click()
        driver.find_element(By.XPATH, "//*[@id='__next']/div/div[2]/div[1]/main/div/div[2]/div/div/div[3]/button/div").click()
        WebDriverWait(driver, 15).until(expected_conditions.presence_of_element_located((By.XPATH, "//*[@id='__next']/div/div[2]/div[1]/main/div/div[2]/div/div/section/article/div/span/input")))
        inviteLink = driver.find_element(By.XPATH, "//*[@id='__next']/div/div[2]/div[1]/main/div/div[2]/div/div/section/article/div/span/input")
        print("The game link is: " + inviteLink.get_attribute('value'))
        input("Press enter to start game")
        driver.find_element(By.XPATH, "//*[@id='__next']/div/div[2]/div[1]/main/div/div[2]/div/div/button").click()
    else: driver.get(gameUrl)

    WebDriverWait(driver, 15).until(expected_conditions.presence_of_element_located((By.XPATH, "//*[@id='__next']/div/div/main/div/div/div[2]/div")))

    # driver.save_screenshot("screenshot.png")
    # country, coordinates, _ = bot.predict("screenshot.png")