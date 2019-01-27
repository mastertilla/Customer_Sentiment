#!/usr/bin/env python

import os
from setuptools import setup

root_dir = os.path.abspath(os.path.dirname(__file__))

setup(
    name='customer-sentiment',
    version='0.0.0',
    author='Daniel Montilla',
    author_email='danielmontillanavas@gmail.com',
    description='Customer Sentiment applied to Online Reviews',
)