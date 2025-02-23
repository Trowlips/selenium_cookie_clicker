from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.remote.webdriver import WebElement

import time
import os
from dotenv import load_dotenv

load_dotenv()

chrome = os.getenv("CHROMEDRIVER_PATH")
web_link = os.getenv("WEB_LINK")

service = Service(chrome)

# Chrome Options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("window-size=1024,1080")

driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get(web_link)

cookie = driver.find_element(By.ID, "cookie")

def get_store_items():
    store_items = driver.find_elements(By.CSS_SELECTOR, "#store > div:not(:last-child)")
    item_list = [item.get_attribute("id") for item in store_items]
    return item_list

def able_to_buy(elem:WebElement) -> bool:
    classes = elem.get_attribute("class")
    if classes:
        return False
    else:
        return True

def buy_items(item_list:list):
    to_buy = None
    web_elem = None
    for index, item in enumerate(reversed(item_list)):
        store_item = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, item))
        )
        buyable = able_to_buy(store_item)
        # print(f"{item} is buyable: {buyable}")
        if buyable:
            to_buy = index
            web_elem = store_item
            break

    if to_buy is not None:
        web_elem.click()
        #check if anything we are still able to buy
        time.sleep(0.5)
        new_item_list = get_store_items()
        buy_items(new_item_list)

clicking = True
while clicking:
    # initial loop for checking if 5 second has passed
    temp_record = time.time()

    while time.time() - temp_record < 5:
        # second loop for buying items in the store
        cookie.click()

    # get store item options
    item_list = get_store_items()

    #check store if anything is available for purchase
    buy_items(item_list)

    # resting time
    time.sleep(1)










