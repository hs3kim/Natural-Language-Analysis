
# Stock NLP

* Scrapes titles of news articles for a selected list of stocks
* Conduct sentiment analysis on scraped news headlines using Google Cloud Natural Language API
* Generate a report and a graph of the analyzed stocks

## Dependencies

Use the package manager [pip](https://pypi.org/project/pip/) to install dependencies

```bash
pip install beautifulsoup4
pip install fake-useragent
pip install matplotlib
pip install numpy
pip install python-dotenv
pip install requests
```

Setup the [Natural Language API](https://cloud.google.com/natural-language/docs/setup) on your local device by following the Google's quickstart guide

Set ADMIN_JSON_PATH variable in NL_Analysis.py to be the path to Cloud Authentication JSON file

## Usage

1. Run NL_Analysis.py
2. Enter path to the txt file containing a list of ticker symbols to analyze, through console input
3. Enter the time window to scrape news headlines from, through console input
4. A csv file and a graph will be generated in the results folder

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
