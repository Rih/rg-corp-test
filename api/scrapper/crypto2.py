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
pages = [p for p in range(MAX_PAGE)]
MAX_THREADS = 3

class Job2(object):

    def __init__(self, currency_tuple):
        self.pages = pages
        self.valid_pages = pages
        self.currency, self.page = currency_tuple
        self.currency_done = {}
        self.scrapers_obj = []
        
    # when added or removed
    def reset_pages(self):
        self.pages = pages

    def set_currency(self, currency):
        self.currency = currency
    
    @staticmethod
    def set_next_page(page):
        if page < 0:
            page = MAX_PAGE
        if page > MAX_PAGE:
            page = 0
        return page
    
    #  asuming the currency probably will be moved
    #  one step page forward or backward
    def set_valid_pages(self, page):
        self.valid_pages = [
            Job2.set_next_page(page - 1),
            page,
            Job2.set_next_page(page + 1)
        ]
    '''
        asdfas
        @returns
    '''
    def fetch_currencies(self, page=0, step=1):
        init_page = page
        first_time = True
        if first_time or page in self.valid_pages:
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
            first_time = False
            # else:
            #     print('page: ', page)
    
    def find_currency(self, name, start=True, init_page=0, current_page=0, step=1, forward=True):
        print('step::: ', name, start, init_page, current_page, step, forward)
        if init_page == current_page and not start:
            return False
        # find
        if self.currency_fetched.get(str(current_page)):
            print('processing page... ', current_page)
            for currency, value in self.currency_fetched.get(str(current_page)).items():
                if currency == name:
                    self.set_valid_pages(current_page)
                    self.currency_targets[name] = current_page
                    self.currency_done[name] = {
                        'value': value,
                        'page': current_page
                    }
                    return True
            if start:
                next = current_page + step
                prev = current_page - step
                found_right = self.find_currency(name, False, init_page, next, step, True)
                found_prev = self.find_currency(name, False, init_page, prev, step, False)
                return found_prev or found_right
        next_page = current_page + 1 if forward else current_page - 1
        next_page = Job2.set_next_page(next_page)
        return self.find_currency(name, False, init_page, next_page, step, forward)

    def search_currency(self, name, page):
        print('searching...', name, 'in page:', page)
        return self.find_currency(name, True, page, MAX_PAGE, page)

    def update_currency(self):
        if self.currency_done.get(self.currency):
            values = self.currency_done.get(self.currency)
            Scraper.objects.filter(currency=self.currency).update(
                value=values['value'],
                page_found=values['page'],
                tobe_found=False
            )
            
    def step(self, func, threads=num_threads, step=1):
        x = [threading.Thread(target=func, args=(step * i,))
             for i in range(threads)
        ]
        for num in range(threads):
            x[num].start()
        for n in range(threads):
            x[num].join()
            print(n, 'join()')

    def step3(self):
        x1 = threading.Thread(target=self.update_currencies, args=())
        x1.start()

    def run(self):
        found = False
        while not found:
            self.step(self.fetch_currencies, MAX_THREADS)
            found = self.search_currency(self.currency, self.page)
            if found:
                self.update_currency()
            sleep(0.5)
        # self.step(self.set_currencies)
        # self.step3()

    
def main():
    """
    Push callback method and url to queue
    """
    job = Job2()
  

if __name__ == '__main__':
    main()