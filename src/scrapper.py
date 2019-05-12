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
        # self.browser = webdriver.Chrome(os.path.join(self.path, 'chromedriver.exe')) 
        self.browser = webdriver.Chrome()

    def iterate_through_pages(self):
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
        self.html_source = self.browser.page_source
        self.bsoup_parse = BeautifulSoup(self.html_source, 'html.parser')

    def get_review_id(self):
        self.reviewid_tag = self.bsoup_parse.find_all('article', attrs={'class': 'review'})
        self.review_ids = []
        for d in self.reviewid_tag:
            self.review_ids.append(d['id'])

    def get_review_content(self):
        # self.review_tag = self.bsoup_parse.find_all('p', attrs={'class': 'review-content__text'})
        self.review_tag = self.bsoup_parse.find_all('p', attrs={'class': 'review-content__text'})
        self.review_text = []
        for d in self.review_tag:
            review_d = re.sub(r'\s+', ' ', d.text).strip().split('\n')[0]
            self.review_text.append(review_d)

    def get_review_dates(self):
        self.date_tag = self.bsoup_parse.find_all('div', attrs={'class': 'v-popover'})

        self.date = []
        for d in self.date_tag:
            for time in d.findAll('time'):
                if time.has_attr('datetime'):
                    date = time['datetime'].split('T')[0]
                    #date = date_raw[0].split('-')
                    self.date.append(date)
                else:
                    self.date.append(np.nan)

    def save_raw_reviews(self):
        self.reviews.to_csv(os.path.join(self.path, "..", "results", self.file_name), sep=',')

    def do_all_scrapper(self):
        self.initialise_browser()
        self.iterate_through_pages()
        self.save_raw_reviews()

if __name__ == "__main__":
    scrapper = ReviewScrapper(url=u'https://uk.trustpilot.com/review/www.currys.co.uk?page=')
    scrapper.initialise_browser()
    scrapper.iterate_through_pages()


    