from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
from fake_useragent import UserAgent
import concurrent.futures

ua = UserAgent()
LOCAL_DT = datetime.now()
SCRAPE_NUM_HR = 24

class Stock:
    def __init__(self, ticker, news_titles):
        self.ticker = ticker
        self.news_titles = news_titles
        self.total_score = 0
        self.total_magnitude = 0

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
        ticker_lst = [ticker.strip() for ticker in f]
        with concurrent.futures.ThreadPoolExecutor() as executer:
            news_titles = executer.map(scrape_news, ticker_lst)
            stock_dict = {ticker_lst[i]: Stock(ticker_lst[i], titles) for i, titles in enumerate(news_titles)}
    return stock_dict


# Scrapes titles of news articles for a stock
def scrape_news(stock):
    HEADER={'User-Agent': ua.chrome}

    url_finviz = "https://finviz.com/quote.ashx?t={}"
    req = requests.get(url_finviz.format(stock), headers=HEADER)
    doc = BeautifulSoup(req.text, "html.parser")
    news_table = doc.find(id='news-table').find_all("tr")

    # Format datetime string
    news_date = None
    news_lst = []
    for news in news_table:
        unparsed_dt = news.find("td").string
        # Date & time given in unparsed datetime
        if len(unparsed_dt) == 19:
            news_date = (unparsed_dt)[:9]
            news_dt_str = unparsed_dt[:17]
        # Only time given in in unparsed datetime
        else:
            news_dt_str = news_date + " " + unparsed_dt[:7]

        news_dt_obj = datetime.strptime(news_dt_str, '%b-%d-%y %I:%M%p')
        
        # Add to list if news were published within the past num_hr
        if ((LOCAL_DT - timedelta(hours=SCRAPE_NUM_HR)) < news_dt_obj):
            news_lst.append(news.find("a").string)
        else:
            break

    return news_lst

def main():
    stock_dict = create_list("./s&p500_ticker.txt")
    print(stock_dict['AAPL'].news_titles)

if __name__=="__main__":
    main()