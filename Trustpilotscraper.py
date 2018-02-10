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

    # we wait 1 second to let the page load everything
    time.sleep(1)

    # we load the HTML body (the main page content without headers, footers, etc.)
    body = browser.find_element_by_tag_name('body')

    # sleep again, let everything load
    time.sleep(1)

    # loop the following 10 times
    for _ in range(20):

        # get the page content for beautiful soup
        html_source = browser.page_source

        # see beautifulsoup
        soup = BeautifulSoup(html_source, 'html.parser')

        # find all the elements of class pros and print them
        divTag = soup.find_all('div', attrs={'class': 'review-body'})
        for d in divTag:
            print("Review " + d.text)
            dataset = pd.DataFrame({'review': d.text}, index=[0])
            dataset.to_csv('Trustpilot_reviews.csv', sep=';', mode='a', header=False)