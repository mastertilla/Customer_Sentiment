import pandas as pd
import numpy as np

import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# browser = webdriver.Chrome()
browser = webdriver.Chrome('C:/Users/Daniel.Navas/Documents/personal_workspace/Customer_Sentiment/chromedriver.exe')

reviews_page = np.arange(1, 543, 1)

# For loop is used to construct all urls to avoid having to click

for i in reviews_page:

    # the url we want to open
    url_basic = u'https://uk.trustpilot.com/review/www.currys.co.uk?page='
    page = i
    # This builds up the url for each review page
    url = url_basic + str(i)

    # the browser will start and load the webpage
    browser.get(url)


    # we load the HTML body (the main page content without headers, footers, etc.)
    body = browser.find_element_by_tag_name('body')
    reviews = pd.DataFrame()

    # get the page content for beautiful soup
    html_source = browser.page_source

    # see beautifulsoup
    soup = BeautifulSoup(html_source, 'html.parser')


    # Find class review-body that contains the review and store it
    # The review is pre-processed before storing it
    divTag = soup.find_all('div', attrs={'class': 'review-body'})
    reviews_dataset = pd.DataFrame()
    for d in divTag:
        review_original = d.text
        review_only = review_original.split('\n                ')
        review_only_ = review_only[1]
        review_only_ = review_only_.split('\n')
        review_only_text = review_only_[0]
        dataset = pd.DataFrame({'review': review_only_text}, index=[0])
        reviews_dataset = pd.concat([reviews_dataset, dataset])


    # Find class review-info clearfix that contains the date of publication and store it
    date_reviews = pd.DataFrame()
    divTag = soup.find_all('div', attrs={'class': 'review-info clearfix'})
    for d in divTag:
        for time in d.findAll('time'):
            update = []
            update = (time['class'])


            if time.has_attr('datetime') and len(update) < 2:
                date1 = (time['datetime'])
                datetime = date1.split("T")
                date = datetime[0]
                date = date.split("-")

                year = date[0]
                month = date[1]
                day = date[2]

                dataset_time = pd.DataFrame({'Year': year, 'Month': month, 'Day': day}, index=[0])
                date_reviews = pd.concat([date_reviews, dataset_time])

    # Concatenate reviews with dates and write to csv
    reviews = pd.concat([reviews_dataset, date_reviews], axis=1)
    reviews.to_csv('Trustpilot_reviews.csv', sep=';', mode='a', header=False)

    print("Page review number:" + str(i))



