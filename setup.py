#!/usr/bin/env python

import os
from sys import version_info
from setuptools import setup

fp = open(os.path.join(os.path.dirname(__file__), "README.rst"))
readme_text = fp.read()
fp.close()

DESCRIPTION = 'tool to scrape soton for RSS feeds'

setup(
    name='soton-rss-scrape',
    author='Thomas Grainger',
    author_email='tagrain@gmail.com',
    packages=['rss_scrape', 'rss_scrape.spiders'],
    version='0.0.1dev',
    description=DESCRIPTION,
    long_description=readme_text,
    install_requires=[
        'scrapy',
        'feedparse',
        'lxml',
        'chardet',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities'
    ]
)
