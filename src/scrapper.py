import datetime
import os
import re

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from utils.exceptions import ReviewReportedError

import logging
logging.basicConfig(filename='scrapper.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', 
                    level=logging.INFO)
logger = logging.getLogger(__name__)

class ReviewScrapper():
    """
    This class launches the scrapper to gather the data for the sentiment analysis tool.
    The data is scrapped from Trustpilot, in this case for Curry's. 
    Also, it is important to note that the scrapper runs for 150 pages, which might lead to some pages being scrapped more than once. This is fixed by dropping duplicated reviews in the data_cleaning class.

    :param url: URL of the reviews provided
    :type url: ``string``
    """
    def __init__(self, url=None):
        if url is None:
            raise Exception('No URL provided')
        else:
            self.url_company = url

        self.review_pages = np.arange(1, 150, 1)
        self.reviews = pd.DataFrame()

        self.path = os.path.dirname(__file__)
        self.file_name = str(datetime.datetime.today().strftime('%Y-%m-%d')) + '_trustpilot_reviews.csv'

    def initialise_browser(self):
        """
        Initialise the Chrome browser. 
        """
        self.browser = webdriver.Chrome()

    def iterate_through_pages(self):
        """
        This function iterates through all the pages to scrape, collecting the id of the review, the review and the date of the review.

        For consistency purposes, if a reported review is encountered, the whole page is discarded, as it is not possible with this code to match ids with reviews if not in order.
        """
        for i in self.review_pages:
            self.url = self.url_company + str(i)
            self.browser.get(self.url)

            self.load_html()
            self.get_review_id()
            self.get_review_content()
            self.get_review_dates()

            try:
                reviews_i = pd.DataFrame({'Id':self.review_ids, 'Review': self.review_text, 'Date': self.date})
                self.reviews = pd.concat([self.reviews, reviews_i], axis=0, ignore_index=True)
            except ValueError:
                logger.error("Page %i not included due to reported review" % i)
                continue

    def load_html(self):
        """
        Initialise page source and BeautifulSoup parser.
        """
        self.html_source = self.browser.page_source
        self.bsoup_parse = BeautifulSoup(self.html_source, 'html.parser')

    def get_review_id(self):
        """
        Gather review id using the `article` tag with **class** `review`.
        """
        self.reviewid_tag = self.bsoup_parse.find_all('article', attrs={'class': 'review'})
        self.review_ids = []
        for d in self.reviewid_tag:
            self.review_ids.append(d['id'])

    def get_review_content(self):
        """
        Gather review text using the `p` tag with **class** `review-content__text`.
        """
        self.review_tag = self.bsoup_parse.find_all('p', attrs={'class': 'review-content__text'})
        self.review_text = []
        for d in self.review_tag:
            review_d = re.sub(r'\s+', ' ', d.text).strip().split('\n')[0]
            self.review_text.append(review_d)

    def get_review_dates(self):
        """
        Gather review text using the `div` tag with **class** `v-popover`.
        """
        self.date_tag = self.bsoup_parse.find_all('div', attrs={'class': 'v-popover'})

        self.date = []
        for d in self.date_tag:
            for time in d.findAll('time'):
                if time.has_attr('datetime'):
                    date = time['datetime'].split('T')[0]
                    self.date.append(date)
                else:
                    self.date.append(np.nan)

    def save_raw_reviews(self):
        """
        Save results to csv.
        """
        self.reviews.to_csv(os.path.join(self.path, "..", "results", self.file_name), sep=',')

    def do_all_scrapper(self):
        """
        Do all functions required to run the scrapper.
        """
        self.initialise_browser()
        self.iterate_through_pages()
        self.save_raw_reviews()

if __name__ == "__main__":
    scrapper = ReviewScrapper(url=u'https://uk.trustpilot.com/review/www.currys.co.uk?page=')
    scrapper.initialise_browser()
    scrapper.iterate_through_pages()


    