import pandas as pd
import re
import numpy as np
import os
from bs4 import BeautifulSoup
from selenium import webdriver


class ReviewScrapper():
    def __init__(self, url=None):
        if url is None:
            raise Exception('No URL provided')
        else:
            self.url = url

        self.path = os.path.dirname(__file__)
    def initialise_browser(self):
        self.browser = webdriver.Chrome(os.path.join(self.path, '..', 'chromedriver.exe'))
