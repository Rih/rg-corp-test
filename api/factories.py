# -*- encoding: utf-8 -*-
import factory
from factory import SubFactory
from django.contrib.auth.models import User
from api.models import Scraper


class ScraperFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Scraper

    currency = 'c1'
    frequency = 2
    value = '$ 1.024'
