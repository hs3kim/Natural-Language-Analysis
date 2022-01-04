from dotenv import load_dotenv
from google.cloud import language_v1
from os import makedirs, getenv
from os.path import isfile, join, basename
from stock_news_scraper import LOCAL_DT, create_dict, set_scrape_t
import concurrent.futures
import csv
import matplotlib.pyplot as plt
import numpy as np

load_dotenv()

ADMIN_JSON_PATH = getenv("ADMIN_JSON_PATH")
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


def gen_graph(tickers, scores, magnitudes, save_dir):
    x_indexes = np.arange(len(tickers))
    width = 0.25

    f = plt.figure()
    f.set_figwidth(16)
    f.set_figheight(8)

    plt.style.use("fivethirtyeight")
    plt.bar(x_indexes - width/2, width=width, height=scores, color="goldenrod", label="Score")
    plt.bar(x_indexes + width/2, width=width, height=magnitudes, color="mediumseagreen", label="Magnitude")
    plt.legend()

    plt.title("Sentiment Score and Magnitude of Stocks")
    plt.xticks(ticks=x_indexes, labels=tickers, rotation='vertical')
    plt.xlabel("Stocks")
    plt.tight_layout()

    plt.savefig(save_dir)
    plt.show()


def get_source_dir():
    while(True):
        dir = input("Enter path to source file of ticker symbols:")
        if (isfile(dir) and dir.endswith(".txt")):
            return dir
        else:
            print("Invalid directory/file format.")


def get_scrape_time():
    while(True):
        t = input("Enter the past number of hours to scrape news from (1~48):")
        try:
            int_t = int(t)
        except ValueError:
            print("Invalid input type")
            continue
        if (int_t > 0 and int_t < 49):
            return int_t
        else:
            print("Number of hours out of bounds.")


def main():
    TICKER_DIR = get_source_dir()
    SCRAPE_NUM_HR = get_scrape_time()
    set_scrape_t(SCRAPE_NUM_HR)

    print("[Status] Processing input file...")
    stock_dict = create_dict(TICKER_DIR)

    print("[Status] Conducting sentiment analysis...")
    for stock in stock_dict.values():
        # Create thread only if list is not empty
        if stock.news_titles:
            with concurrent.futures.ThreadPoolExecutor() as executer:
                results = executer.map(analyze_text, stock.news_titles)
                for result in results:
                    stock.total_score += result[0]
                    stock.total_magnitude += result[1]

    score_dict_desc = {k: v for k, v in sorted(stock_dict.items(), key=lambda item: item[1].get_score(), reverse=True)}

    tickers, scores, magnitudes = [], [], []
    for ticker, stock in score_dict_desc.items():
        tickers.append(ticker)
        scores.append(stock.get_score())
        magnitudes.append(stock.get_magnitude())

    # Folder to save output for selected input file
    output_dir = join("./outputs", basename(TICKER_DIR)[:-4])

    # Subfolder in output_dir to save output files
    subdir_str = LOCAL_DT.strftime("%Y-%m-%d-%H") + f"-{SCRAPE_NUM_HR}hrs"

    # Make directory to save output files
    full_output_dir = join(output_dir, subdir_str)
    try:
        makedirs(full_output_dir)
    except FileExistsError:
        print("File already exists. Existing files will be overwritten")

    # Generate and save graph as a png file
    graph_output_dir = join(full_output_dir, subdir_str) + ".png"
    gen_graph(tickers[0: GRAPH_NUM_STOCKS], scores[0: GRAPH_NUM_STOCKS], magnitudes[0: GRAPH_NUM_STOCKS], graph_output_dir)

    # Save scores and magnitudes as a csv file
    csv_output_dir = join(full_output_dir, subdir_str) + ".csv"
    with open(csv_output_dir, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Ticker", "Score", "Magnitude"])
        for ticker, stock in score_dict_desc.items():
            writer.writerow([ticker, stock.get_score(), stock.get_magnitude()])


if __name__ == "__main__":
    main()
