"""Customer Sentiment Analysis Review

Usage:
  main.py [--scrape=<y/n>]
  main.py [--scrape|--sentiment]
  main.py -h | --help
  main.py --version

Options:
  -h --help       Show this screen.
  --version       Show version.
  --scrape=<y/n>  Run scrapper (yes/no)
"""
import os
from src.scrapper import ReviewScrapper
from src.data_cleaning import DataPrep
from src.sent_analysis import SentimentAnalysis
import time

from docopt import docopt

if __name__=="__main__":
    main_path = os.path.dirname(__file__)
    start = time.time()
    arguments = docopt(__doc__, version='1.0')
    if arguments['--scrape'] == 'y':
        scrapper = ReviewScrapper(url=u'https://uk.trustpilot.com/review/www.currys.co.uk?page=')
        scrapper.do_all_scrapper()
        data_prep = DataPrep(data=scrapper.reviews)
    else:
        data_prep = DataPrep()

    data_prep.do_all_dataprep()

    sentiment_model = SentimentAnalysis(reviews=data_prep.reviews_cleaned, test=True)
    sentiment_model.do_all_sentiment()


    print("Took %.2f seconds" %(time.time() - start))

