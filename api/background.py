from background_task import background
from api.models import Scraper
from api.scrapper.crypto import Job
from django.contrib.auth.models import User


def main_sc():
    freqs = Scraper.objects.all().values_list('frequency', flat=True)
    uniq_freq = set(freqs)
    for freq in uniq_freq:
        scrapers = list(Scraper.objects.filter(frequency=freq).values_list('currency', 'page_found'))
        print(scrapers)


@background(schedule=60)
def main_scraper():
    print('background setting up')
    freqs = Scraper.objects.all().values_list('frequency', flat=True)
    uniq_freq = set(freqs)
    start_over(uniq_freq)
    
@background()
def start_over(uniq_freq):
    print('start over', uniq_freq)
    for freq in uniq_freq:
        scrapers = list(
            Scraper.objects.filter(frequency=freq).values_list('currency',
                                                               'page_found'))
        scraper_names = [c for c, p in scrapers]
        print(freq)
        print(scraper_names)
        job = refresh_scraper(
            scrapers, freq,
            verbose_name='|'.join(scraper_names),
            repeat=freq,
            repeat_until=None,
        )
    
@background()
def found_missing_scraper_page():
    scrapers = list(
        Scraper.objects
            .filter(tobe_found=True)
            .values_list('currency', 'page_found')
    )
    if len(scrapers):
        run_missing(
            scrapers,
            verbose_name='find_missing',
            repeat=11,
            repeat_until=None
        )


@background()
def run_missing(scrapers):
    print(scrapers, len(scrapers))
    if len(scrapers):
        Job(scrapers, 'set_pages').run_pages()
    print("done missing.")
    
    
@background()
def refresh_scraper(scrapers, frequency):
    
    # lookup user by id and send them a message
    Job(scrapers, 'refresh').run_values()
    print('refreshing done', scrapers, 'freq: ', frequency)
    
#undefined
# notify_user(repeat_until=None)