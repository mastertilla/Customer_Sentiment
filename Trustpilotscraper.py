import pandas as pd
import numpy as np

import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# define the browser
# on learn, the Chrome webdriver is included, which is used here, make sure it is in the same folder as the py file
browser = webdriver.Chrome()

reviews_page = np.arange(1, 542, 1)

for i in reviews_page:

    # the url we want to open
    url_basic = u'https://uk.trustpilot.com/review/www.currys.co.uk?page='
    page = i

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


    # find all the elements of class pros and print them
    divTag = soup.find_all('div', attrs={'class': 'review-body'})
    reviews_dataset = pd.DataFrame()
    for d in divTag:
        print("Review " + d.text)
        dataset = pd.DataFrame({'review': d.text}, index=[0])
        reviews_dataset = pd.concat([reviews_dataset, dataset])

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

    reviews = pd.concat([reviews_dataset, date_reviews], axis=1)
    reviews.to_csv('Trustpilot_reviews.csv', sep=';', mode='a', header=False)



