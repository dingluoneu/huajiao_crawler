from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


def scroll_down(browser, number_of_scroll_down):
    """
    The method can let browser scroll down automatically
    :param browser: selenium webdtriver
    :param number_of_scroll_down:
    :return: selenium webdriver
    """
    body = browser.find_element_by_tag_name("body")
    while number_of_scroll_down >= 0:
        body.send_keys(Keys.PAGE_DOWN)
        number_of_scroll_down -= 1
        time.sleep(1)
    return browser


def parse_live_id(url):
    """
    Fetches live_id from www.huajiao.com popular rank list
    :param url: "http://www.huajiao.com/category/1000"
    :return: a list contain top 300 popular
    """
    live_id_list = []
    browser = webdriver.Chrome()
    browser.get(url)
    browser.maximize_window()
    browser = scroll_down(browser, 20)
    time.sleep(2)
    a_elements = browser.find_elements_by_xpath("//ul[@class='pic-items js-list-ul']/li/a")
    if a_elements is not None and len(a_elements) > 0:
        for a in a_elements:
            a_href = a.get_attribute("href")
            live_id_list.append(a_href)
            print(a_href)
    else:
        print("a_elements is None or empty!!!")
    browser.quit()
    return live_id_list





