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
    value = models.FloatField(default=0.0, null=False)
    updated_at = models.DateTimeField(
        null=True,
        auto_now=True
    )

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Scraper, self).save(*args, **kwargs)
