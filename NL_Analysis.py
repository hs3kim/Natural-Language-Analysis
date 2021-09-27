from google.cloud import language_v1
from dotenv import load_dotenv
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

    return sentiment.score, sentiment.magnitude

def main():
    sample_text = "BEIJING (Reuters) - Tesla Inc's Shanghai factory is expected to produce 300,000 cars in the first nine months of the year, capped by a delivery rush in the end of the July-September quarter, despite a global semiconductor shortage, two sources said. The factory makes the electric Model 3 sedans and Model Y sport-utility vehicles for domestic and international markets, including Germany and Japan. Around 240,000 vehicles were shipped from the factory in the first eight months, including many for export, according to data from the China Passenger Car Association. Tesla has not announced details on the factory's production. The sources requested anonymity, as they were not allowed to speak to media. Tesla did not immediately respond to a request for comment. In August, an official in the area where Tesla's factory is located said it is expected to product 450,000 vehicles this year, including 66,100 for export. Tesla is hiring managers for legal and external relations teams in China as it faces public scrutiny in the country over data security and customer service complaints."
    score, magnitude = analyze_text(sample_text)
    print("score: {}, magnitude: {}".format(score, magnitude))

if __name__=="__main__":
    main()