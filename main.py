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

from src.scrapper import ReviewScrapper
from src.data_cleaning import DataPrep
import time

from docopt import docopt

if __name__=="__main__":
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

    print("Took %.2f seconds" %(time.time() - start))

