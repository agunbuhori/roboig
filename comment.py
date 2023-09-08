import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
import sys

def get_random_comment(filename):
    with open(filename, 'r') as file:
        comments = file.read().splitlines()
    return random.choice(comments)

def comment_post(username, password, target, comment_file):
    # Set up ChromeDriver options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("detach", True)

    # chrome_options.add_argument("--headless")
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
    driver.get(target)
    time.sleep(3)

    try:
        max_retries = 3
        retries = 0
        comment = get_random_comment(comment_file)

        while retries < max_retries:
            try:
                element = driver.find_element(By.TAG_NAME, "textarea")
                element.click()
                element.send_keys(comment)
                element.send_keys(Keys.RETURN)
                break  # Exit the loop if the click is successful
            except StaleElementReferenceException:
                retries += 1
    except Exception as e:
        print(e)
        time.sleep(3)
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python follow.py accounts.txt <target> comments.txt")
        sys.exit(1)

    target = sys.argv[2]
    comment_file = sys.argv[3]

    with open('accounts.txt', 'r') as file:
        for line in file:
            account_info = line.strip().split()
            if len(account_info) == 2:
                username, password = account_info
                comment_post(username, password, target, comment_file)
