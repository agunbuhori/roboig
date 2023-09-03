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
    # chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")

    # Set up ChromeDriver service
    service = Service(ChromeDriverManager().install())

    # Set up ChromeDriver instance
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Log in to Instagram
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(2)

    username_input = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
    password_input = driver.find_element(By.CSS_SELECTOR, "input[name='password']")

    username_input.send_keys(username)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    time.sleep(3)

    # Like stories of each follower
    # for follower in usernames:
    story_url = f"https://www.instagram.com/{target}"
    driver.get(story_url)
    time.sleep(2)


    follow_button = driver.find_elements(By.TAG_NAME, 'button')

    if follow_button:
        follow_button[0].click()
        follow_button[1].click()
        print("[TRUE] User -> " + target + " has been followed")
        time.sleep(3)
    else:
        print("[FALSE] User -> " + target + " has no story up.")
        # continue
        driver.quit()

    # Close the ChromeDriver instance


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python run.py <username> <password> <target>")
        sys.exit(1)

    username = sys.argv[1]
    password = sys.argv[2]
    target = sys.argv[3]

    follow_account(username, password, target)