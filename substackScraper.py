import os
import shutil
import time
from io import BytesIO
from os import environ
import csv
import re
import pandas as pd
from PIL import Image, ImageOps
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def write_csv(header, data, path, mode):
    with open(path, mode, encoding="utf-8") as f:
        writer = csv.writer(f)
        if mode == "w":
            writer.writerow(header)
        writer.writerows(data)


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("enable-automation")
driver = webdriver.Chrome(
    options=chrome_options
)
driver.implicitly_wait(5)
x = 3840
y = x / 16 * 10
driver.set_window_size(x, y)
driver.delete_all_cookies()
url = "https://substack.com/discover/category/politics/all"

driver.get(url)
time.sleep(5)
clickViewMore = 1
while (clickViewMore == 1):
    elements = driver.find_elements(By.XPATH, "//button[.='View more']")
    print("view more")
    if (len(elements)!=0):
        time.sleep(5)
        elements[0].click()
        time.sleep(5)
    else:
        clickViewMore = 0
time.sleep(5)
linkelems = driver.find_elements(By.XPATH, "//div[@class='publications']/a")
publinks = [linkelem.get_attribute('href') for linkelem in linkelems]

new_publinks = []

for publink in publinks:
    new_publink = publink.replace("?utm_source=discover", "archive?sort=top")
    new_publinks.append(new_publink)

howManyScrollsEachPub = 3
for i, h in enumerate(new_publinks):
    print(h)
    driver.get(h)
    time.sleep(5)
    for j in range(howManyScrollsEachPub):
        newsCards = driver.find_elements(By.XPATH, "//div[contains(@class,'portable-archive-post')]")
        driver.execute_script("arguments[0].scrollIntoView();", newsCards[-1])
        time.sleep(5)
    newsCards = driver.find_elements(By.XPATH, "//div[contains(@class,'portable-archive-post')]")
    for k, card in enumerate(newsCards):
        print("doing")
        try:
            imgElem = card.find_element(By.XPATH, "./div[contains(@class,'image')]")
            imgUrl = imgElem.get_attribute('style')
        except:
            imgUrl = ""
        try:
            titleElem = card.find_element(By.XPATH, "./div[contains(@class,'content')]/a[contains(@class, 'title')]")
            titleText = titleElem.text
        except:
            titleText = ""
        try:
            titleElem = card.find_element(By.XPATH, "./div[contains(@class,'content')]/a[contains(@class, 'title')]")
            titleUrl = titleElem.get_attribute('href')
        except:
            titleUrl = ""
        try:
            descElem = card.find_element(By.XPATH, "./div[contains(@class,'content')]/a[contains(@class, 'desc')]")
            descText = descElem.text
        except:
            descText = ""
        try:
            descElem = card.find_element(By.XPATH, "./div[contains(@class,'content')]/a[contains(@class, 'desc')]")
            descUrl = descElem.get_attribute('href')
        except:
            descUrl = ""
        try:
            authElem = card.find_element(By.XPATH, "./div[contains(@class,'content')]/div[contains(@class, 'author')]//a")
            authText = authElem.text
        except:
            authText = ""
        try:
            authElem = card.find_element(By.XPATH, "./div[contains(@class,'content')]/div[contains(@class, 'author')]//a")
            authUrl = authElem.get_attribute('href')
        except:
            authUrl = ""
        try:
            dateElem = card.find_element(By.XPATH, "./div[contains(@class,'content')]/table[contains(@class, 'meta')]//td[contains(@class, 'date')]")
            dateText = dateElem.text
        except:
            dateText = ""
        try:
            likeElem = card.find_element(By.XPATH, "./div[contains(@class,'content')]/table[contains(@class, 'meta')]//a[contains(@class, 'like')]")
            likeText = likeElem.text
        except:
            likeText = ""
        try:
            commentElem = card.find_element(By.XPATH, "./div[contains(@class,'content')]/table[contains(@class, 'meta')]//a[contains(@href, 'comments')]")
            commentText = commentElem.text
        except:
            commentText = ""
        try:
            commentElem = card.find_element(By.XPATH, "./div[contains(@class,'content')]/table[contains(@class, 'meta')]//a[contains(@href, 'comments')]")
            commentUrl = commentElem.get_attribute('href')
        except:
            commentUrl = ""
        mode = "w" if (i == 0 and k ==0) else "a"
        write_csv(
            header=["publicationLink", "imgUrl", "titleText", "titleUrl", "descText","descUrl", "authText", "authUrl", "dateText", "likeText", "commentText", "commentUrl"],
            data=zip([h], [imgUrl], [titleText], [titleUrl], [descText], [descUrl], [authText], [authUrl], [dateText], [likeText], [commentText], [commentUrl]),
            path=os.path.join("substDATA.csv"),
            mode=mode,
        )
