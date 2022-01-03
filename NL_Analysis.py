from dotenv import load_dotenv
from google.cloud import language_v1
from stock_news_scraper import *
import os
import csv
import numpy as np
import matplotlib.pyplot as plt

load_dotenv()

ADMIN_JSON_PATH = os.getenv("ADMIN_JSON_PATH")
GRAPH_NUM_STOCKS = 30

# Client initiation
client = language_v1.LanguageServiceClient.from_service_account_json(ADMIN_JSON_PATH)


def analyze_text(text):
    # Sample text to analyze
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    # Score: Overall emotion (-1.0 ~ 1.0)
    # Magnitude: Strength of emotion (0.0 ~ +inf)
    return sentiment.score, sentiment.magnitude

def gen_graph(tickers, scores, magnitudes):
    x_indexes = np.arange(len(tickers))
    width = 0.25

    f = plt.figure()
    f.set_figwidth(16)
    f.set_figheight(8)

    plt.style.use("fivethirtyeight")
    plt.bar(x_indexes-width, width=0.25, height=scores, color="goldenrod", label="Score")
    plt.bar(x_indexes, width=0.25, height=magnitudes, color="mediumseagreen", label="Magnitude")
    plt.legend()

    plt.title("Sentiment Score and Magnitude of Stocks")
    plt.xticks(ticks=x_indexes, labels=tickers)
    plt.xlabel("Stocks")
    plt.tight_layout()

    plt.show()

def main():
    stock_dict = create_list("./s&p500_ticker.txt")
    
    for stock in stock_dict.values():
        # Create thread only if list is not empty
        if stock.news_titles:
            with concurrent.futures.ThreadPoolExecutor() as executer:
                results = executer.map(analyze_text, stock.news_titles)
                for result in results:
                    stock.total_score += result[0]
                    stock.total_magnitude += result[1]

    desc_score_dict = {k: v for k, v in sorted(stock_dict.items(), key=lambda item: item[1].get_score(), reverse=True)}

    tickers, scores, magnitudes = [], [], []
    for ticker, stock in desc_score_dict.items():
        tickers.append(ticker)
        scores.append(stock.get_score())
        magnitudes.append(stock.get_magnitude())
    print(tickers)
    print(scores)
    print(magnitudes)

    gen_graph(tickers[0: GRAPH_NUM_STOCKS], scores[0: GRAPH_NUM_STOCKS], magnitudes[0: GRAPH_NUM_STOCKS])

if __name__=="__main__":
    main()