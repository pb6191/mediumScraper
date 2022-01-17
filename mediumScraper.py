# %%
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

# df = pd.DataFrame(columns=["headline", "section1", "section2", "section3", "section4", "section5", "section6", "section7", "section8", "section9", "section10", "section11", "section12", "section13", "section14", "section15", "section16", "section17", "section18", "section19", "section20", "section21", "section22", "section23", "section24", "section25", "section26", "section27", "section28", "section29", "section30", "section31", "section32", "section33", "section34", "section35", "section36", "section37", "section38", "section39", "section40", "section41", "section42", "section43", "section44", "section45", "section46", "section47", "section48", "section49", "section50", "section51", "section52", "section53", "section54", "section55", "section56", "section57", "section58", "section59", "section60", "section61", "section62", "section63", "section64", "section65", "section66", "section67", "section68", "section69", "section70", "section71", "section72", "section73", "section74", "section75", "section76", "section77", "section78", "section79", "section80", "section81", "section82", "section83", "section84", "section85", "section86", "section87", "section88", "section89", "section90", "section91", "section92", "section93", "section94", "section95", "section96", "section97", "section98", "section99", "section100"])
df = pd.DataFrame(columns=["headline", "desc", "writer", "where", "date"])

chrome_options = webdriver.ChromeOptions()
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("enable-automation")
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(5)
x = 3840
y = x / 16 * 10
driver.set_window_size(x, y)
driver.delete_all_cookies()
# %%

dates_all = pd.date_range("2021-12-17", end="2021-12-17").strftime("%Y/%m/%d")

# %%
url = "https://medium.com/tag/politics/archive/2021/12/01"


def write_csv(header, data, path, mode):
    with open(path, mode, encoding="utf-8") as f:
        writer = csv.writer(f)
        if mode == "w":
            writer.writerow(header)
        writer.writerows(data)


for k3, d3 in enumerate(dates_all):
    url = "https://medium.com/tag/politics/archive/" + d3
    time.sleep(2)
    driver.get(url)
    time.sleep(10)
    for i in range(0):
        elements = driver.find_elements(
            By.XPATH, "//div[contains(@class, 'postPreview')]"
        )
        print(len(elements))
        driver.execute_script(
            "arguments[0].scrollIntoView();", elements[len(elements) - 1]
        )
        time.sleep(3)

    headlineEles = driver.find_elements(
        By.XPATH, "//div[contains(@class, 'postPreview')]"
    )

    for i, h in enumerate(headlineEles, start=1):
        headlinetext = ""
        desctext = ""
        writertext = ""
        sourcetext = ""
        datetext = ""
        readtimetext = ""
        claptext = ""
        responsetext = ""
        try:
            headline = h.find_element(
                By.XPATH, ".//div[contains(@class, 'section-inner')]//h3"
            )
            headlinetext = headline.text
        except:
            headlinetext = ""
        try:
            desc = h.find_element(
                By.XPATH,
                ".//div[contains(@class, 'section-inner')]//h3//following-sibling::*",
            )
            desctext = desc.text
        except:
            desctext = ""
        try:
            writer = h.find_element(
                By.XPATH,
                ".//a[@data-action='show-user-card' and not(contains(@class, 'avatar'))]",
            )
            writertext = writer.text
        except:
            writertext = ""
        try:
            source = h.find_element(
                By.XPATH, ".//a[@data-action='show-collection-card']"
            )
            sourcetext = source.text
        except:
            sourcetext = ""
        try:
            date = h.find_element(By.XPATH, ".//time")
            datetext = date.text
        except:
            datetext = ""
        try:
            readtime = h.find_element(By.XPATH, ".//span[@class='readingTime']")
            readtimetext = date.get_attribute("title")
        except:
            readtimetext = ""
        try:
            claps = h.find_element(
                By.XPATH, ".//button[@data-action='show-recommends']"
            )
            claptext = claps.text
        except:
            claptext = ""
        try:
            responses = h.find_element(
                By.XPATH, ".//a[contains(@class, 'button button--chromeless')]"
            )
            responsetext = responses.text
        except:
            responsetext = ""
        print(headlinetext)
        mode = "w" if (k3 == 0 and i == 1) else "a"
        write_csv(
            header=[
                "headline",
                "desc",
                "writer",
                "where",
                "date",
                "readTime",
                "claps",
                "responses",
            ],
            data=zip(
                [headlinetext],
                [desctext],
                [writertext],
                [sourcetext],
                [datetext],
                [readtimetext],
                [claptext],
                [responsetext],
            ),
            path=os.path.join("medDATA.csv"),
            mode=mode,
        )
# for i in range(3):
#    driver.get(url)
#    time.sleep(5)
#    headlineEles = driver.find_elements(By.XPATH, "//section/div/div/div/h3/a")
#    h = headlineEles[i]
#    df.at[i+1, 0] = h.text
#    h.click()
#    time.sleep(5)
#    sectionEles = driver.find_elements(By.XPATH, "//section")
#    for j, s in enumerate(sectionEles, start=1):
#        df.at[i+1, j] = s.text


# df.to_csv('dataMedium.csv', sep=',', encoding='utf-8')
