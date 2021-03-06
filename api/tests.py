# -*- encoding: utf-8 -*-

from django.test import TestCase
import requests
from django.test import TestCase
from django.test import Client
import json
from django.urls import reverse
from api.factories import  ScraperFactory
from django.conf import settings
from django.test.utils import override_settings
from api.models import Scraper
from api.scrapper.crypto import Job
from api.background import main_sc

# Create your tests here.
@override_settings(ENVIRONMENT='UNIT_TEST')
class ScraperTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.scraper1 = ScraperFactory(currency='Ethereum', frequency=2)
        self.scraper2 = ScraperFactory(currency='Hive', frequency=5)
        self.scraper2 = ScraperFactory(currency='CyberVein', frequency=5)
        self.scraper3 = ScraperFactory(currency='Cardano', frequency=2)
        self.scraper3 = ScraperFactory(currency='Aragon', frequency=3)

    def test_scraper_get(self):
        '''
        python3.7 manage.py test api.tests.ScraperTestCase.test_scraper_get
        :return: assertions
        '''
        url = reverse('scrapers')
        response = self.client.get(url)
        data = json.loads(response.content)
        self.assertEquals(200, response.status_code)
        self.assertTrue(len(data) > 0)

    def test_scraper_post(self):
        '''
        python3.7 manage.py test api.tests.ScraperTestCase.test_scraper_post
        :return: assertions
        '''
        url = reverse('scrapers')
        payload = {
            'currency': 'c_new',
            'frequency': 2
        }
        response = self.client.post(
            url,
            json.dumps(payload),
            content_type='application/json'
        )
        data = json.loads(response.content)
        self.assertEquals(200, response.status_code)
        self.assertEquals('c_new', data.get('currency'))

    def test_scraper_put(self):
        '''
        python3.7 manage.py test api.tests.ScraperTestCase.test_scraper_put
        :return: assertions
        '''
        url = reverse('scrapers')
        payload = {
            'id': self.scraper1.pk,
            'frequency': 3
        }
        response = self.client.put(
            url,
            json.dumps(payload),
            content_type='application/json'
        )
        data = json.loads(response.content)
        self.assertEquals(200, response.status_code)
        self.assertEquals('Scraper updated', data.get('msg'))

    def test_scraper_delete(self):
        '''
        python3.7 manage.py test api.tests.ScraperTestCase.test_scraper_delete
        :return: assertions
        '''
        url = reverse('scrapers')
        payload = {
            'id': self.scraper1.pk,
        }
        response = self.client.delete(
            url,
            json.dumps(payload),
            content_type='application/json'
        )
        data = json.loads(response.content)
        self.assertEquals(200, response.status_code)
        self.assertEquals('Scraper deleted', data.get('msg'))

    def test_webscrap_get(self):
        '''
        python3.7 manage.py test api.tests.ScraperTestCase.test_webscrap_get
        :return: assertions
        '''
        # main_sc()
        scrapers = list(
            Scraper.objects.filter(frequency=2).values_list('currency',
                                                               'page_found'))
        print(scrapers)
        # # response = Job(sc).run()
        response = Job(scrapers).run_pages()
        # print(response)
