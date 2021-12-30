from bs4 import BeautifulSoup
import requests
import datetime as dt
from fake_useragent import UserAgent

ua = UserAgent()

class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.news_titles = []
        self.total_score = 0
        self.total_magnitude = 0
    
    def append_news(self, news):
        self.news_titles.append(news)

    def get_score(self):
        if len(self.news_titles) > 0:
            return self.total_score/len(self.news_titles)
        else:
            return 0

    def get_magnitude(self):
        if len(self.news_titles) > 0:
            return self.total_magnitude/len(self.news_titles)
        else:
            return 0

# Initiate Stock objects into a dictionary
def create_list(file_name):
    stock_dict = {}
    with open(file_name, "r") as f:
        for ticker in f:
            stock_dict[ticker.strip()] = Stock(ticker.strip())
    return stock_dict


# Scrapes titles of news articles for a stock
def scrape_urls(stock):
    HEADER={'User-Agent': ua.chrome}

    url_finviz = "https://finviz.com/quote.ashx?t={}"
    req = requests.get(url_finviz.format(stock), headers=HEADER)
    doc = BeautifulSoup(req.text, "html.parser")

    news_table = doc.find(id='news-table').find_all("tr")

    # obtain all time values
    news_date = None
    for idx, news in enumerate(news_table):
        news_table[idx] = (news.find("td")).string
        
    return news_table

def main():
    stock_tickers = ["FB", "AMZN", "AAPL", "NFLX", "GOOG"]
    url_dict = {}
    for ticker in stock_tickers:
        url_dict[ticker] = scrape_urls(ticker)

if __name__=="__main__":
    main()