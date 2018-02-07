import pandas as pd
import numpy as np

import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# define the browser
# on learn, the Chrome webdriver is included, which is used here, make sure it is in the same folder as the py file
browser = webdriver.Chrome()

# the url we want to open
url = u'https://www.currys.co.uk/gbuk/phones-broadband-and-sat-nav/mobile-phones-and-accessories/mobile-phones/apple-iphone-8-64-gb-space-grey-10168742-pdt.html?intcmpid=display~RR'

# the browser will start and load the webpage
browser.get(url)

# we wait 1 second to let the page load everything
time.sleep(1)

# we load the HTML body (the main page content without headers, footers, etc.)
body = browser.find_element_by_tag_name('body')

# we use seleniums' send_keys() function to physically scroll down where we want to click
body.send_keys(Keys.PAGE_DOWN)

# we search for an element that is called 'customer reviews', which is a button
# the button can be clicked with the .click() function
browser.find_element_by_link_text("Customer reviews").click();

# we need to scroll further down to collect the reviews and especially click the next button
body.send_keys(Keys.PAGE_DOWN)

# sleep again, let everything load
time.sleep(1)

# loop the following 10 times
for _ in range(10):
    # search for the next button to access the next reviews
    browser.find_element_by_link_text('Next').click()

    # scroll down to get the reviews
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)

    # get the page content for beautiful soup
    html_source = browser.page_source

    # see beautifulsoup
    soup = BeautifulSoup(html_source, 'html.parser')

    # find all the elements of class pros and print them
    divTag = soup.find_all('dd', attrs={'class': 'pros'})
    for d in divTag:
        print("Positive point: " + d.text)

    # do the same for negative points
    divTag = soup.find_all('dd', attrs={'class': 'cons'})
    for d in divTag:
        print("Negative point: " + d.text)
