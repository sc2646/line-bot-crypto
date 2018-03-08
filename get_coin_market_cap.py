import requests
# import urllib2
from bs4 import BeautifulSoup
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage

LINK = "https://coinmarketcap.com/"
PRICE = "price"
PERCENTAGE = "percentage"
ACCESS_TOKEN = "6lWwrvOTgNh+eg1WXm9XUv47Yr3sjFKI/T1cJTSJyLGRAT2wvitx8dp3EKDiY4cukWr52C99J4oFYGpd2H/7KzAfRZYlou9E4XsZ1pK71t156zg79eOGRxoN+dNPRaDja6CKMH4+kzJJslm3gU9UywdB04t89/1O/w1cDnyilFU="
USER_ID = "Uce312f440fb25d82bf07f7c943089969"
CHANNEL_SECRET = "aae2b4b36e80ec3ddce3b42352492b6c"

class CoinMarketCapScrapper:
    def __init__(self):
        # self.driver = webdriver.PhantomJS()
        # self.response =
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
                # percentage_change = row.find("td", class_="no-wrap percent-change text-right negative_change").get_text()
                # print percentage_change
                is_target = self.isBTC(currency) or self.isETH(currency) or self.isLTC(currency) or self.isNEO(currency) or self.isXMR(currency)

                if(is_target):
                    self.result[currency] = dict()
                    self.result[currency][PRICE] = price

            except:
                pass

    def send_text(self):
        if len(self.result) != 0 :
            try:
                if self.result["BTC"][PRICE] > 8500:
                    print "============="
                    content = "BTC price is now " + str(self.result["BTC"][PRICE] + "!")
                    print content
                    self.line_bot_api.push_messsage(USER_ID, TextSendMessage(text="HELLO!"))
            except:
                pass

    def isBTC(self, name):
        return name == "BTC"

    def isETH(self, name):
        return name == "ETH"

    def isNEO(self, name):
        return name == "NEO"

    def isLTC(self, name):
        return name == "LTC"

    def isXMR(self, name):
        return name == "XMR"


    def process(self):
        self.scrape_coin_market_cap(LINK)
        self.send_text()

if __name__ == '__main__':
    coin_market_cap_scraper = CoinMarketCapScrapper()
    coin_market_cap_scraper.process()
