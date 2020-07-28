#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""

BeautifulSoup does not support XPath expression by default, so we use CSS
the expression here, but you can use https://github.com/scrapy/parsel to write
XPath to extract data as you like

"""
from __future__ import print_function
from bs4 import BeautifulSoup
import re
import requests
from time import sleep
from api.models import Scraper
import threading
from sqlite3 import OperationalError

QUEUE = []
WEB_SCRAPER_URL = 'https://coinmarketcap.com'
PAGE = 0
MAX_PAGE = 28
jump = 7
num_threads = int(MAX_PAGE / jump)


def extract_by_regex(data):
    # <tr class=\"cmc-table-row\".*<a href=.*title=\"(\w+)\".*class=\"cmc-link\">.*class=\"cmc-link\">([\$\,\.\d+]+).*<\/tr>$
    # <tr class="cmc-table-row".*<a href=.*title="([\w\s]+)".*class="cmc-link">([\$\,\.\d+]+).*<\/tr>$
    # <tr class="cmc-table-row".*<a href=.*title="([\w\s]+)".*class="cmc-link">([\$\,\.\d]+)</a>
    # p = re.compile(bytes(r'<tr class="cmc-table-row"(.*)<a href=(.+)title="([\w\s]+)"(.+)class="cmc-link">([\$\.\d]+)</a>(.*)</tr>', encoding='utf8'))
    # p = re.compile(bytes(
    #     r'<tr class="cmc-table-row".+<a href=.+title="([\w\s]+)".+class="cmc-link">([\$\.\d]+)</a>',
    #     encoding='utf8'))
    p = re.compile(bytes(r'<a href=(.+)title="([\w\s]+)"(.+)class="cmc-link">([\$\.\d]+)</a>', encoding='utf8'))
    print(data)
    matches = p.findall(data)
    matches_iter = p.finditer(data)
    print(matches[0][2], matches[0][4])
    print(matches[1][2], matches[1][4])
    # for iter in matches_iter:
    #     print(iter.span())
    # print(matches[1][2])


class Job(object):

    def __init__(self, currencies):
        self.currency_targets = {currency: 'to_update' for currency in currencies}
        self.currency_fetched = {}
        self.currency_done = {}
        self.scrapers_obj = []
        
    def fetch_currencies(self, page=0, step=1):
        init_page = page
        while True:
            URL = f'{WEB_SCRAPER_URL}/{page}'
            print('fetching... ', URL)
            r = requests.get(URL)
            # content = r.content
            soup = BeautifulSoup(r.text, "lxml")
            rows = soup.select('tr[class="cmc-table-row"]')
            currencies = {}
            for row in rows:
                columns =list(row.children)
                currency = columns[1].text
                value = columns[3].text
                currencies[currency] = value
            self.currency_fetched[str(page)] = currencies
            page += step
            sleep(2)
    
    def set_currencies(self, page=0, step=1):
        init_page = page
        while len(self.currency_targets) and (page - init_page) <= jump:
            if self.currency_fetched.get(str(page)):
                print('processing page... ', page)
                for currency, value in self.currency_fetched.get(str(page)).items():
                    if self.currency_targets.get(currency) == 'to_update':
                        self.currency_done[currency] = value
                        del self.currency_targets[currency]
                del self.currency_fetched[str(page)]
                page += step
            else:
                print('not available page... ', page)
            sleep(2)

    def update_currencies(self):
        while len(self.currency_targets):
            if len(self.currency_done):
                print('loop through currency done... ')
                while self.currency_done:
                    currency, value = self.currency_done.popitem()
                    print('update: ', currency, value)
                    try:
                        scraper = Scraper.objects.filter(currency=currency).first()
                        scraper.value = value
                        self.scrapers_obj.append(scraper)
                    except OperationalError as er:
                        print(er)
                        self.currency_done[currency] = value
                    sleep(1)
            sleep(2)
        Scraper.objects.bulk_update(self.scrapers_obj, ['value'])

    def step(self, func, threads=num_threads, step=1):
        x = [threading.Thread(target=func, args=(step * i,))
             for i in range(threads + 1)
             ]
        for num in range(threads):
            x[num].start()

    # def step2(self):
    #     y = [threading.Thread(target=self.set_currencies, args=(jump * j))
    #          for j in range(num_threads)
    #     ]
    #     for num in range(num_threads):
    #         y[num].start()
    # x1 = threading.Thread(target=self.set_currencies, args=())
    # x2 = threading.Thread(target=self.set_currencies, args=(jump))
    # x3 = threading.Thread(target=self.set_currencies, args=(jump*2))
    # x4 = threading.Thread(target=self.set_currencies, args=(jump*3))
    # x1.start()
    # x2.start()
    # x3.start()
    # x4.start()

    def step3(self):
        x1 = threading.Thread(target=self.update_currencies, args=())
        x1.start()

    def run(self):
        self.step(self.fetch_currencies, MAX_PAGE)
        # self.step(self.set_currencies)
        # self.step3()

    
def main():
    """
    Push callback method and url to queue
    """
    job = Job()
    QUEUE.append(
        (job.fetch_currencies, WEB_SCRAPER_URL)
    )
    #
    while len(QUEUE):
        call_back, url = QUEUE.pop(0)
        call_back(url)


if __name__ == '__main__':
    main()