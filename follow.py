import time
import os
import fileinput
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import sys

def follow_account(username, password, target):
    # Set up ChromeDriver options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Log in to Instagram
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(3)

    username_input = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
    password_input = driver.find_element(By.CSS_SELECTOR, "input[name='password']")

    username_input.send_keys(username)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    time.sleep(3)

    # Like stories of each follower
    # for follower in usernames:
    profile_url = f"https://www.instagram.com/{target}"
    driver.get(profile_url)
    time.sleep(3)

    header = driver.find_element(By.TAG_NAME, 'header')
    buttons = header.find_elements(By.TAG_NAME, 'button')
    try:
        # Iterate through the buttons and click each one
        for button in buttons:
            button.click()
            print("Following...")

        print(f"Followed")
        time.sleep(3)
        driver.quit()
    except Exception as e:
        print(f"Failed")
        time.sleep(3)
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python follow.py accounts.txt <target>")
        sys.exit(1)

    target = sys.argv[2]

    with open('accounts.txt', 'r') as file:
        for line in file:
            account_info = line.strip().split()
            if len(account_info) == 2:
                username, password = account_info
                follow_account(username, password, target)
