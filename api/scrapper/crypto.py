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
MAX_PAGE = 30
jump = 4
num_threads = int(MAX_PAGE / jump)
pages = [p for p in range(MAX_PAGE)]
MAX_THREADS = 6
MAX_RETRIES = 5


class Job(object):

    def __init__(self, currencies, mode='set_pages'):
        self.pages = pages
        self.currencies = currencies
        self.mode = mode
        self.valid_pages = [p for c, p in currencies]
        print('valid pages... ', self.valid_pages)
        self.currency_targets = self.set_targets(currencies)
        self.currencies_fetched = {}
        self.currencies_found = {}
        self.scraping_done = False
        self.scrapers_obj = []
        
    def set_targets(self, currencies):
        targets = {}
        for currency, page in currencies:
            targets[currency] = {'to_update': True, 'page': page}
        return targets
    
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
    def set_valid_pages(self, old_page, new_page):
        self.valid_pages.remove(old_page)
        self.valid_pages.append(new_page)

    def fetch(self, page=0, max_try=1, step=1):
        init_page = page
        attempt = 1
        while attempt <= max_try and page < MAX_PAGE:
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
            self.currencies_fetched[str(page)] = currencies
            # else:
            #     print('page: ', page)
            if self.mode == 'refresh':
                break
            page += step
            attempt += 1
            sleep(0.1)
    '''
        asdfas
        @returns
    '''
    def fetch_currencies(self, page=0, step=1):
        init_page = page
        while len(self.currency_targets) != len(self.currencies_found) and (page - init_page) <= MAX_PAGE:
            if self.currencies_fetched.get(str(page)):
                page += step
                continue
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
            self.currencies_fetched[str(page)] = currencies
            # else:
            #     print('page: ', page)
            page += step
            sleep(0.12)
        self.scraping_done = True
    
    def find_currency(self, start, name, init_page=0, current_page=0, step=1, all_page=False):
        if init_page == current_page and not start:
            return False
        # find
        if self.currencies_fetched.get(str(current_page)):
            print('processing page... ', current_page)
            for currency, value in self.currencies_fetched.get(str(current_page)).items():
                found_currency = self.currency_targets.get(currency)
                if found_currency and found_currency.get('to_update'):
                    self.currencies_found[currency] = {
                        'value': value,
                        'page': current_page
                    }
            if len(self.currencies_found) == len(self.currency_targets):
                return True
            
        if start:
            next = current_page + 1
            prev = current_page - 1
            found_right = self.find_currency(name, False, init_page, next, 1, all_page)
            found_prev = self.find_currency(name, False, init_page, prev, -1, all_page)
            return found_prev or found_right
        next_page = current_page + step
        next_page = Job.set_next_page(next_page)
        return self.find_currency(name, False, init_page, next_page, step, all_page)

    def search_currency(self, name, page):
        print('searching...', name, 'in page:', page)
        found = self.find_currency(name, True, page, page, 1, True)
        if not found:
            Scraper.objects.filter(currency=name).update(tobe_found=True)

    def update_currency(self, currency):
        self.set_currency(currency)
    
    def set_currency_page(self, currency):
        values = self.currencies_found.get(currency)
        scraper = Scraper.objects.filter(currency=currency).get()
        scraper.page_found = values['page']
        scraper.tobe_found = not(self.currencies_found.get(currency))
        return scraper

    def set_currency_value(self, currency):
        values = self.currencies_found.get(currency)
        scraper = Scraper.objects.filter(currency=currency).get()
        scraper.value = values['value']
        scraper.tobe_found = not(self.currencies_found.get(currency))
        return scraper

    def step(self, func, threads=num_threads, tries=1):
        x = [
            threading.Thread(target=func, args=(i, tries, threads))
            for i in range(threads)
        ]
        for num in range(threads):
            x[num].start()
        for n in range(threads):
            x[num].join()
        
    def step_scraping(self):
        x = [
            threading.Thread(target=self.fetch_currencies, args=(page, 1))
            for page in self.valid_pages
        ]
        for num in range(len(self.valid_pages)):
            x[num].start()
            
    def step_search(self):
        y = [
            threading.Thread(target=self.search_currency, args=(currency, page))
            for currency, page in self.currencies
         ]
        for num in range(len(self.currencies)):
            y[num].start()
        for n in range(len(self.currencies)):
            y[n].join()
            
    def step_update(self, func, columns):
        self.currencies_obj = []
        for currency, page in self.currencies:
            self.currencies_obj.append(func(currency))
        Scraper.objects.bulk_update(self.currencies_obj, columns)

    def run_pages(self):
        self.step(self.fetch, MAX_THREADS, MAX_RETRIES)
        self.scraping_done = True
        self.step_search()
        self.step_update(self.set_currency_page, ['page_found', 'tobe_found'])
        
    def run_values(self):
        self.fetch(1, 1)
        self.step_search()
        self.step_update(self.set_currency_value, ['value', 'tobe_found'])
        # self.step(self.set_currencies)
        # self.step3()
