# -*- encoding: utf-8 -*-

from django.db import models
from django.utils import timezone


class Scraper(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(
        auto_now=False,
        editable=True
    )
    currency = models.CharField(
        max_length=50,
        unique=True
    )
    frequency = models.IntegerField(null=False)
    value = models.CharField(max_length=20, default='$ 0.0', null=False)
    updated_at = models.DateTimeField(
        null=True,
        auto_now=True
    )
    page_found = models.IntegerField(default=0, null=False)
    tobe_found = models.IntegerField(default=True, null=False)
    
    def __str__(self):
        return f'{self.currency} - {self.frequency}'

    def __unicode__(self):
        return f'{self.currency} - {self.frequency}'

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        # self.updated_at = timezone.now()
        return super(Scraper, self).save(*args, **kwargs)
    
    # def update(self, *args, **kwargs):
    #     ''' On update, update timestamps '''
    #     self.updated_at = timezone.now()
    #     return super(Scraper, self).update(*args, **kwargs)