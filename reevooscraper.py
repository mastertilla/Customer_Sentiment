import pandas as pd
import numpy as np

import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def month_converter(month):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    return months.index(month) + 1

# define the browser
# on learn, the Chrome webdriver is included, which is used here, make sure it is in the same folder as the py file
browser = webdriver.Chrome()

# the url we want to open
url = u'https://www.reevoo.com/retailer/6-currys'

# the browser will start and load the webpage
browser.get(url)

headers = ['would buy again from Currys', 'on time and in good order', 'said enquiries handled effectively']

# we load the HTML body (the main page content without headers, footers, etc.)
body = browser.find_element_by_tag_name('body')

reviews = pd.DataFrame()
for i in range(1, 8970):

    html_source = browser.page_source

    # see beautifulsoup
    soup = BeautifulSoup(html_source, 'html.parser')

    divTag = soup.find_all('p', attrs={'class': 'comment'})
    reviews_dataset = pd.DataFrame()
    for d in divTag:
        review = d.text
        if review not in headers:
            dataset = pd.DataFrame({'review': review}, index=[0])
            reviews_dataset = pd.concat([reviews_dataset, dataset])

    date_reviews_published = pd.DataFrame()
    divTag = soup.find_all('span', attrs={'class': 'date date_publish'})
    for tp in divTag:
        date = tp.text
        date = date.split(' ')
        day = date[0]
        month = month_converter(date[1])
        year = date[2]
        dataset_published = pd.DataFrame({'Year_published': year, 'Month_published': month, 'Day_published': day}, index = [0])
        date_reviews_published = pd.concat([date_reviews_published, dataset_published])

    date_reviews_purchased = pd.DataFrame()
    divTag = soup.find_all('span', attrs={'class': 'date date_purchase'})
    for tp in divTag:
        date = tp.text
        date = date.split(' ')
        day = date[0]
        month = month_converter(date[1])
        year = date[2]
        dataset_purchased = pd.DataFrame({'Year_purchased': year, 'Month_purchased': month, 'Day_purchased': day}, index = [0])
        date_reviews_purchased = pd.concat([date_reviews_purchased, dataset_purchased])


    reviews = pd.concat([reviews_dataset, date_reviews_published, date_reviews_purchased], axis=1)
    reviews.to_csv('Reevoo_reviews.csv', sep=';', mode='a', header=False)

    body.send_keys(Keys.END)

    browser.find_element_by_class_name('next_page').click()
