from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.request
import time

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
   'Accept-Encoding': 'none',
   'Accept-Language': 'en-US,en;q=0.8',
   'Connection': 'keep-alive'}


class User:
    __user_id = ""
    __user_name = ""
    __location = ""
    __live_level = 0
    __self_level = 0
    __tags = []
    __followers_count = 0
    __like_received = 0
    __gift_received = 0
    __gift_sent = 0
    __rank_list = {}

    def __init__(self, user_id, user_name, location, l_level, s_level, tags, followers_count, like, gift_r, gift_s, rank_list):
        self.__user_id = user_id
        self.__user_name = user_name
        self.__location = location
        self.__live_level = l_level
        self.__self_level = s_level
        self.__tags = tags
        self.__followers_count = followers_count
        self.__like_received = like
        self.__gift_received = gift_r
        self.__gift_sent = gift_s
        self.__rank_list = rank_list

    def get_user_id(self):
        return self.__user_id

    def get_user_name(self):
        return self.__user_name

    def get_location(self):
        return self.__location

    def get_live_level(self):
        return self.__live_level

    def get_self_level(self):
        return self.__self_level

    def get_tags(self):
        return self.__tags

    def get_followers_count(self):
        return self.__followers_count

    def get_like_received(self):
        return self.__like_received

    def get_gift_received(self):
        return self.__gift_received

    def get_gift_sent(self):
        return self.__gift_sent

    def get_rank_list(self):
        return self.__rank_list


class TopFollower:
    __rank = 0
    __user_name = ""
    __user_id = ""
    __gift_no = 0

    def __init__(self, rank, user_name, user_id, gift_no):
        self.__rank = rank
        self.__user_name = user_name
        self.__user_id = user_id
        self.__gift_no = gift_no

    def get_rank(self):
        return self.__rank

    def get_user_name(self):
        return self.__user_name

    def get_user_id(self):
        return self.__user_id

    def get_gift_no(self):
        return self.__gift_no



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


def parse_live_url(url):
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


def parse_user_ranklist(user_info_page_url):
    """
    Fetches the top followers for a user
    :param user_info_page_url:
    :return: a dictionary key: rank, value: TopFollower instance
    """
    rank_list = {}
    browser = webdriver.Chrome()
    browser.get(user_info_page_url)
    browser.maximize_window()
    browser = scroll_down(browser, 15)
    time.sleep(1)
    div_elements = browser.find_elements_by_xpath("//ul[@id='rankList']/li/div")
    if div_elements is not None and len(div_elements) > 0:
        for div in div_elements:
            # rank: int
            rank = int(div.find_element_by_xpath("./div[@class='rank-box']/div").text)
            info = div.find_element_by_xpath("./div[@class='info']")
            a = info.find_element_by_xpath("./h3/a")
            # gift number: int
            gift = int(info.find_element_by_xpath("./p/span").text)
            a_href = a.get_attribute("href")
            # user_name: str
            user_name = a.text
            #user_id: str
            user_id = extract_user_id_from_ranklist_url(a_href)
            follower = TopFollower(rank, user_name, user_id, gift)
            rank_list[rank] = follower
    return rank_list


def parse_user_info_page_from_live_url(live_url):
    global headers
    request = urllib.request.Request(live_url, data=None, headers=headers)
    html = urlopen(request, timeout=10)
    soup = BeautifulSoup(html, "html.parser")
    a_nav = soup.find("a", {"class": "js-ulink js-nickname link"})
    user_info_page_url = ""
    if a_nav is not None:
        user_info_page_url = "http://www.huajiao.com" + a_nav["href"]
    else:
        print("a_nav is None!")
    return user_info_page_url


def extract_user_id_from_ranklist_url(url):
    res = ""
    if url is None or len(url) == 0:
        return res

    for i in range(0, len(url)):
        if url[i].isdigit():
            res += url[i]
    return res
