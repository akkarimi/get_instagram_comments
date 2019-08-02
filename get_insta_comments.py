from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
from langdetect import detect
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementNotVisibleException, TimeoutException


def init_driver():
    driver = webdriver.Chrome(executable_path='/home/akbar/chromedriver/chromedriver')
    driver.wait = WebDriverWait(driver, 5)
    return driver


def get_comments(plain_html):
    lan = input("Only English Comments (y/n): ")
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
    print("===================================================")
    if lan == 'y':
        print(*en_comments, sep='\n')
    else:
        print(*all_comments, sep='\n')
    print("===================================================")
    print("Number of English Comments: ", len(en_comments))
    print("Number of all comments:", len(comments))
    time.sleep(1)


def click_more_comments(driver):
    post_address = input("Enter the Post Address and Press Enter: ")
    print("Please wait...")
    driver.get(post_address)
    driver.implicitly_wait(5)
    while driver.find_elements_by_xpath('//span[@aria-label="Load more comments"]'):
        button = driver.find_element_by_xpath('//span[@aria-label="Load more comments"]')
        button.click()
        driver.implicitly_wait(10)
    return driver.page_source


if __name__ == "__main__":
    driver = init_driver()
    expanded_page_source = click_more_comments(driver)
    get_comments(expanded_page_source)
    driver.quit()
