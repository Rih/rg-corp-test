from background_task import background
from api.models import Scraper
from api.scrapper.crypto2 import Job2
from django.contrib.auth.models import User

@background()
def main_scraper():
    # lookup user by id and send them a message
    # user = User.objects.get(pk=user_id)
    # user.email_user('Here is a notification', 'You have been notified')
    print('background done')
    scrapers = Scraper.objects.all().group_by('frequency')
    for scraper in scrapers:
        currency = scraper.currency
        page = scraper.page_found,
        frequency = scraper.frequency
        print(currency, page, frequency)
        # job = refresh_scraper(
        #     currency, page, frequency,
        #     verbose_name=currency,
        #     repeat=frequency,
        #     repeat_until=None,
        #     creator=scraper
        # )
        # print('id job', job.id)
        # print('job', job.__dict__)

    # while True:
    #     pass
    #
   
   
@background()
def refresh_scraper(currency, page, frequency):
    
    # lookup user by id and send them a message
    # user = User.objects.get(pk=user_id)
    # user.email_user('Here is a notification', 'You have been notified')
    # Job2((currency, page)).run()
    print('fetching done', currency, page, 'freq: ', frequency)
#undefined
# notify_user(repeat_until=None)