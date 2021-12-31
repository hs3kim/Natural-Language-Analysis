from google.cloud import language_v1
from dotenv import load_dotenv
from stock_news_scraper import *
import os

load_dotenv()

ADMIN_JSON_PATH = os.getenv("ADMIN_JSON_PATH")

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
    sample_text = "Tesla is recalling almost as many vehicles as it delivered last yea"
    score, magnitude = analyze_text(sample_text)
    print("score: {}, magnitude: {}".format(score, magnitude))
    

if __name__=="__main__":
    main()