# -*- coding: UTF-8 -*-
"""
A Yahoo Finance News Scrapper API

This module is a test API for fetching news data from Yahoo Finance.

Import Requirements
-------------------
Make sure the "yahoo.py" file is located in the same directory of your python script,
    or in a directory linked to your $PATH.

To view the directories in your path, open a terminal and run this command:
    (mac) $> echo $PATH
    (win) $> echo %path%

Available News Types
--------------------
Industry News Feed : most recent news items for the industry to which a company belongs to
Company News Feed  : most recent news items for a particular company

Adjust Multithreading Number of Threads
---------------------------------------
num_threads = 4 : Default is 4 threads

"""

num_threads = 4

import logging
import subprocess
import sys
import time
from collections import OrderedDict
from threading import Thread

try:
    from Queue import Queue
except ImportError:
    from queue import Queue
try:
    import requests
except ImportError:
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'requests', '--user'])
    import requests
try:
    import feedparser
except ImportError:
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'feedparser', '--user'])
    import feedparser
try:
    from bs4 import BeautifulSoup
except ImportError:
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'beautifulsoup4', '--user'])
    from bs4 import BeautifulSoup
try:
    import lxml
except ImportError:
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'lxml', '--user'])
    import lxml
try:
    from tqdm import tqdm
except ImportError:
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'tqdm', '--user'])
    from tqdm import tqdm
try:
    from unidecode import unidecode
except ImportError:
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'unidecode', '--user'])
    from unidecode import unidecode


### UTILITY FUNCTIONS ###


def convertUnicode(s):
    return str(''.join(unidecode(c) for c in s))


def getNews(source_feed, kind):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14'
    headers = {'User-Agent': user_agent, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

    def getData(data):
        article = OrderedDict()
        try:
            logging.info('fetching: %s', data['link'])
            link = data['link']
            src = requests.get(link, headers=headers)
            src.raise_for_status()
            summary = BeautifulSoup(data['summary'], 'lxml').text

            soup = BeautifulSoup(src.content, 'lxml')
            if kind == 'company':
                if soup.find("a", class_='read-more-button'):
                    link = soup.find("a", class_='read-more-button')['href']
                    src = requests.get(link, headers=headers)
                    src.raise_for_status()
                    soup = BeautifulSoup(src.content, 'lxml')
            for script in soup(['script']):
                script.decompose()
            content = ' '.join(soup.find('article').text.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').split())

            article['title'] = data['title']
            article['link'] = link
            article['summary'] = convertUnicode(summary)
            article['content'] = convertUnicode(content)
        except Exception as e:
            # print(sys.exc_info())
            logging.debug(e)
        return article

    def worker():
        while True:
            item = q.get()
            news = getData(item)
            if news:
                articles.append(news)
            q.task_done()

    articles = []
    q = Queue(num_threads*2)
    for i in range(num_threads):
        t = Thread(target=worker)
        t.daemon = True
        t.start()

    for data in tqdm(source_feed['entries']):
        if 'video' not in data['link']:
            q.put(data)
    q.join()

    return articles

### API CALLS ##


def get_industry_news(ticker):
    """
    Industry News RSS Feed
    ----------------------
    Source: https://finance.yahoo.com/rss/industry?s=<ticker>
    Fetches the most recent 20 Industry News articles for given ticker.

    Parameters
    ----------
    ticker (str) : The stock ticker of target company

    Returns
    -------
    t : A list of news articles containing news objects:
        list: [
            dict: {
                'title' : 'title of news article'
                'link' : 'link to news article'
                'summary' : 'short summary of news article'
                'content' : 'raw text of news article with unicode converted to string'
            }, ...
        ]

    Usage_Example
    -------------
    >>> import yahoo
    >>> apple_industry_news = yahoo.get_industry_news('appl')
    100%|███████████████████████████████████████████████████████████████| 50/50 [00:07<00:00,  6.26it/s]
    Successfully Retreived: 40 Industry News articles...

    >>> for news in apple_industry_news:
    ...     for key in news.keys():
    ...         print key + ' =', news[key]
    ...     print '*'*100

    title = Amazon just accidentally leaked details about 2 new Alexa devices ahead of an event today
    link = https://finance.yahoo.com/news/amazon-just-accidentally-leaked-details-145441439.html
    summary = <p><a href="https://finance.yahoo.com/news/amazon-just-accidentally-leaked-details-1454414
    content = Listings for an Amazon Echo Sub subwoofer and an Amazon Smart Plug were leaked ahead of a
    ****************************************************************************************************
    title = New U.S. LNG projects, enough to double exports, on verge of launch
    link = https://finance.yahoo.com/news/u-lng-projects-enough-double-153020633.html
    summary = <p><a href="https://finance.yahoo.com/news/u-lng-projects-enough-double-153020633.html"><i
    content = * FERC filings show progress of terminal commissioning* Initial cargoes sold on spot basis
    ****************************************************************************************************
    ...


    """
    logging.info('Scraping Industry News...')
    logging.info('source =  https://finance.yahoo.com/rss/industry?s=%s', ticker)
    source = feedparser.parse('https://finance.yahoo.com/rss/industry?s='+ticker)
    result = getNews(source, 'industry')

    print('Successfully Retreived: ' + str(len(result)) + ' Industry News articles...')
    return result


def get_company_news(ticker):
    """
    Company News RSS Feed
    ----------------------
    Source: http://finance.yahoo.com/rss/headline?s=<ticker>
    Fetches the most recent 20 Industry News articles for given ticker.

    Parameters
    ----------
    ticker (str) : The stock ticker of target company

    Returns
    -------
    news_articles : A list of news articles containing news objects:
        list: [
            dict: {
                'title' : 'title of news article'
                'link' : 'link to news article'
                'summary' : 'short summary of news article'
                'content' : 'raw text of news article with unicode converted to string'
            }, ...
        ]

    Usage_Example
    -------------
    >>> import yahoo
    >>> apple_industry_news = yahoo.get_company_news('appl')
    100%|███████████████████████████████████████████████████████████████| 50/50 [00:07<00:00,  6.26it/s]
    Successfully Retreived: 40 Industry News articles...

    >>> for news in apple_company_news:
    ...     for key in news.keys():
    ...         print key + ' =', news[key]
    ...     print '*'*100

    title = Amazon just accidentally leaked details about 2 new Alexa devices ahead of an event today
    link = https://finance.yahoo.com/news/amazon-just-accidentally-leaked-details-145441439.html
    summary = <p><a href="https://finance.yahoo.com/news/amazon-just-accidentally-leaked-details-1454414
    content = Listings for an Amazon Echo Sub subwoofer and an Amazon Smart Plug were leaked ahead of a
    ****************************************************************************************************
    title = New U.S. LNG projects, enough to double exports, on verge of launch
    link = https://finance.yahoo.com/news/u-lng-projects-enough-double-153020633.html
    summary = <p><a href="https://finance.yahoo.com/news/u-lng-projects-enough-double-153020633.html"><i
    content = * FERC filings show progress of terminal commissioning* Initial cargoes sold on spot basis
    ****************************************************************************************************
    ...

    """
    logging.info('Scraping Company News...')
    logging.info('source = http://finance.yahoo.com/rss/headline?s=%s', ticker)
    source = feedparser.parse('http://finance.yahoo.com/rss/headline?s='+ticker)
    result = getNews(source, 'company')
  
    print('Successfully Retreived: ' + str(len(result)) + ' Company News articles...')
    
    
    return result


logging.basicConfig(filename='yahoo.log', filemode='a', level=logging.DEBUG)
