"""
# Preparation
1. Modify login information in `login_info_sample.json` as yours, and rename file name as `login_info.json`
2. Required libraries as follows: bs4, selenium, webdriver_manager (`pip install bs4 selenium==3.141 webdriver_manager`)
"""
import time
import os
import json
from collections import Counter
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))  # selenium >= 4.
browser = webdriver.Chrome("./chromedriver")

def load_login_info() -> tuple:
    item = dict(json.load(open("./login_info.json", 'r', encoding='utf-8')))
    return item['username'], item['password']


def login(username, password):
    """Method 1: Deprecated
    browser.get(f'https://www.instagram.com/{username}')
    browser.execute_script("document.querySelectorAll('.-nal3')[1].click();")
    time.sleep(2)  # 2 Seconds break
    browser.find_element(By.ID, 'username').send_keys(username)
    browser.find_element(By.ID, 'password').send_keys(password)
    browser.find_element(By.XPATH, '//*[@id="loginForm"]/div[1]/div[3]/button').submit()  # Send login request
    time.sleep(4)  # 4 Seconds break
    browser.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/div/button').click()
    """

    """Method 2"""
    browser.get('https://www.instagram.com/')
    time.sleep(3)
    id_box = browser.find_element(By.CSS_SELECTOR, "#loginForm > div > div:nth-child(1) > div > label > input")
    pw_box = browser.find_element(By.CSS_SELECTOR, "#loginForm > div > div:nth-child(2) > div > label > input")
    login_btn = browser.find_element(By.CSS_SELECTOR, "#loginForm > div > div:nth-child(3) > button")
    action = ActionChains(browser)
    action.send_keys_to_element(id_box, username).send_keys_to_element(pw_box, password).click(login_btn).perform()
    time.sleep(5)

    if browser.current_url.rsplit("/", 1)[-1].startswith("two_factor"):
        two_factor_code = input("Enter Two-Factor Authentication code: ")
        two_factor_code_box = browser.find_element(By.CSS_SELECTOR, "._ab3i > div:nth-child(1) > div > label > input")
        confirm_btn = browser.find_element(By.CSS_SELECTOR, "._ab3i > div:nth-child(2) > button")
        # act = ActionChains(browser)
        action.send_keys_to_element(two_factor_code_box, two_factor_code).click(confirm_btn).perform()

    save_login_info_popup = browser.find_element(By.CSS_SELECTOR, "#react-root > section > main > div > div > div > div > button")
    save_login_info_popup.click()
    time.sleep(5)

    notification_popup = browser.find_element(By.CSS_SELECTOR, "body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.HoLwm")
    notification_popup.click()
    time.sleep(5)

    my_photo = browser.find_element(By.CSS_SELECTOR, "#react-root > section > nav > div._8MQSO.Cx7Bp > div > div > div.ctQZg.KtFt3 > div > div:nth-child(6)")
    my_photo.click()
    time.sleep(1)

    profile = browser.find_element(By.CSS_SELECTOR, "#react-root > section > nav > div._8MQSO.Cx7Bp > div > div > div.ctQZg.KtFt3 > div > div:nth-child(6) > div.poA5q > div.uo5MA._2ciX.tWgj8.XWrBI > div._01UL2 > a:nth-child(1)")
    profile.click()
    time.sleep(2)

"""Deprecated
def check_followings():
    browser.find_element(By.XPATH, '/html/body/div[4]/div/div/div[1]/div/div[2]/button').click()
    time.sleep(0.5)
    browser.execute_script("document.querySelectorAll('.-nal3')[2].click();")
    time.sleep(1)
    oldHeight = -1
    newHeight = -2
    while oldHeight != newHeight:
        oldHeight = newHeight
        newHeight = browser.execute_script("return document.querySelectorAll('.jSC57')[0].scrollHeight")
        browser.execute_script("document.querySelectorAll('.isgrP')[0].scrollTo(0,document.querySelectorAll('.jSC57')[0].scrollHeight)")
        time.sleep(0.5)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    return set([item.get_text() for item in soup.findAll('a', ['FPmhX', 'notranslate', '_0imsa'])])


def check_followers():
    browser.find_element(By.XPATH, '/html/body/div[4]/div/div/div[1]/div/div[2]/button').click()
    time.sleep(0.5)
    browser.execute_script("document.querySelectorAll('.-nal3')[1].click();")
    time.sleep(1)
    oldHeight = -1
    newHeight = -2
    while oldHeight != newHeight:
        oldHeight = newHeight
        newHeight = browser.execute_script("return document.querySelectorAll('.jSC57')[0].scrollHeight")
        browser.execute_script("document.querySelectorAll('.isgrP')[0].scrollTo(0,document.querySelectorAll('.jSC57')[0].scrollHeight)")
        time.sleep(0.5)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    return set([item.get_text() for item in soup.findAll('a', ['FPmhX', 'notranslate', '_0imsa'])])
"""

def get_follow_info():
    flwrs = browser.find_element(By.XPATH, "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/div/span")
    flngs = browser.find_element(By.XPATH, "/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/div/span")
    return set(flngs.text), set(flwrs.text)


user, pw = load_login_info()
login(user, pw)
followings, followers = get_follow_info()

not_follow_me = followers - followings
not_follow_I = followings - followers

print("I Don't Follow:", not_follow_I)
print("Who Doesn't Follow me:", not_follow_me)

def get_last_followers():
    last_data = "./lastest.txt"
    if not os.path.exists(last_data):
        with open(last_data, 'w', encoding='utf-8') as f:
            f.write(str(followers))
        return False, None
    else:
        with open(last_data, 'r', encoding='utf-8') as f:
            previous = set(f.read())
        return True, list((Counter(previous) - Counter(followers)).keys())


flag, list = get_last_followers()
if flag:
    print("Have unfollowed me:", list)
else:
    print("There is no previous data, current follower data saved into 'latest.txt' file.")