# -*- coding: utf-8 -*-

import re
import json
import datetime

from selenium import webdriver
from bs4 import BeautifulSoup
from linebot import LineBotApi
from linebot.models import TextSendMessage

LINK = "https://www.ptt.cc/bbs/WomenTalk/index.html"

class WomenTalkScraper:
    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.result=[]
        self.names = []

    def scrape_one_url(self, url):
        self.driver.get(url)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        posts = soup.find_all("div", class_="r-ent")
        for post in posts:
            if(post.find("div", class_="title").a!= None):
                title = post.find("div", class_="title").a.get_text()
            else:
                continue
            author = post.find("div", class_="meta").find("div", class_="author").get_text()
            print title
            print "================"
            print author

            # if r.match(title):
            if re.match(u'^[女]', title):
                self.result.append(title)
                self.names.append(author)

        print self.result
        print self.names
if __name__ == '__main__':
    womentalk_scraper = WomenTalkScraper()
    womentalk_scraper.scrape_one_url(LINK)
