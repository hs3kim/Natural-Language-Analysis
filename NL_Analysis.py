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


if __name__=="__main__":
    main()