import requests
from bs4 import BeautifulSoup
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage

LINK = "https://coinmarketcap.com/"
PRICE = "price"
PERCENTAGE = "percentage"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
USER_ID = "YOUR USER ID"
CHANNEL_SECRET = "YOUR CHANNEL SECRET"


BTC = "BTC"
ETH = "ETH"
LTC = "LTC"
NEO = "NEO"
XMR = "XMR"

BTC_TARGET_PRICE = 8500
ETH_TARGET_PRICE = 800
LTC_TARGET_PRICE = 210
NEO_TARGET_PRICE = 130
XMR_TARGET_PRICE = 350

class CoinMarketCapScrapper:
    def __init__(self):
        self.result = dict()
        self.line_bot_api = LineBotApi(ACCESS_TOKEN)
        self.handler = WebhookHandler(CHANNEL_SECRET)

    def scrape_coin_market_cap(self, url):
        # self.driver.get(url)
        page = requests.get(LINK)
        # soup = BeautifulSoup(self.driver.page_source, "html.parser")
        soup = BeautifulSoup(page.content, "html.parser")
        rows = soup.find("tbody").find_all("tr")

        for row in rows:
            try:
                currency =  row.find("td", class_="no-wrap currency-name").span.a.get_text()
                price = row.find("td", class_="no-wrap text-right").a.get_text()
                is_target = self.isBTC(currency) or self.isETH(currency) or self.isLTC(currency) or self.isNEO(currency) or self.isXMR(currency)

                if(is_target):
                    self.result[currency] = dict()
                    self.result[currency][PRICE] = price

            except:
                pass

    def send_text(self, content):
        try:
            self.line_bot_api.push_message(USER_ID, TextSendMessage(text=content))
        except:
            pass

    def price_above_target(self):
        if len(self.result) != 0:
            try:
                currencies = self.result.keys()
                for currency in currencies:
                    if self.result[currency][PRICE] < currency + "_TARGET_PRICE":
                        content = currency + " price is now " + str(self.result[currency][PRICE] + "!")
                        self.send_text(content)
            except:
                pass

    def isBTC(self, name):
        return name == BTC

    def isETH(self, name):
        return name == ETH

    def isNEO(self, name):
        return name == NEO

    def isLTC(self, name):
        return name == LTC

    def isXMR(self, name):
        return name == XMR

    def process(self):
        self.scrape_coin_market_cap(LINK)
        self.price_above_target()


if __name__ == '__main__':
    coin_market_cap_scraper = CoinMarketCapScrapper()
    coin_market_cap_scraper.process()
