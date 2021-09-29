from bs4 import BeautifulSoup
import requests
import datetime as dt

# Scrapes news articule urls from the input domain published within the past 12 hours
def scrape_urls(stock):
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

    url_finviz = "https://finviz.com/quote.ashx?t={}"
    req = requests.get(url_finviz.format(stock), headers=headers)
    doc = BeautifulSoup(req.text, "html.parser")
    
    news_table = doc.find(id='news-table').find_all("tr")

    # obtains all news urls 
    for idx, news in enumerate(news_table):
        news_table[idx] = news.find("a")["href"]
        
    return news_table

def main():
    stock_tickers = ["FB", "AMZN", "AAPL", "NFLX", "GOOG"]
    url_dict = {}
    for ticker in stock_tickers:
        url_dict[ticker] = scrape_urls(ticker)

if __name__=="__main__":
    main()