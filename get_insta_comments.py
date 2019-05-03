from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
from langdetect import detect
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import argparse


def get_comments():

    insta_address = input("Enter the Post Address and Press Enter: ")
    lan = input("Only English Comments (y/n): ")

    driver = webdriver.Chrome()

    driver.get(insta_address)
    plain_html = click_load(driver)
    soup = bs(plain_html, 'html.parser')
    comments = soup.find_all('li', {'class':'gElp9'})

    encount = 0
    all_comments = []
    en_comments = []
    for i in range(len(comments)):
        if i == 0:
            continue
        res = comments[i]
        txt = res.find("span").text
        all_comments.append(txt)
        try:
            if detect(txt)=='en':
                en_comments.append(txt)
                encount = encount + 1
        except:
            pass
    if lan == 'y':
        print(*en_comments, sep = '\n')
    else:
        print(*all_comments, sep = '\n')
    print("Number of English Comments: ", len(en_comments))
    print("Number of all comments:", len(comments))
    time.sleep(1)
    driver.quit()

def click_load(driver):
    html = driver.page_source
    flag = False
    if 'Load more comments' in html:
        flag=True
    while flag==True:
        try:
            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "myDynamicElement")))
        except:
            pass
        driver.find_element(By.XPATH, '//button[text()="Load more comments"]').click()
        html = driver.page_source
        if 'Load more comments' not in html:
            flag=False

    return html

if __name__ == "__main__":
    get_comments()
