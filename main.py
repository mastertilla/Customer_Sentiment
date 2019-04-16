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
import time

from docopt import docopt

if __name__=="__main__":
    main_path = os.path.dirname(__file__)
    start = time.time()
    arguments = docopt(__doc__, version='1.0')
    if arguments['--scrape'] == 'y':
        scrapper = ReviewScrapper(url=u'https://uk.trustpilot.com/review/www.currys.co.uk?page=')
        scrapper.do_all()
        data_prep = DataPrep(data=scrapper.reviews)
    else:
        data_prep = DataPrep()

    data_prep.read_data()
    data_prep.parse_document()
    data_prep.cleaning_reviews()
    data_prep.return_dataframe()

    data_prep.reviews_cleaned.to_csv(os.path.join(main_path, 'results', 'cleaned_reviews.csv'), sep=',')

    print("Took %.2f seconds" %(time.time() - start))

