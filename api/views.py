# -*- encoding: utf-8 -*-
from django.views.generic import View
from api.models import Scraper
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.http import JsonResponse, HttpResponse
import json
from django.db.utils import IntegrityError
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from api.exceptions import FrequencyException
from api.exceptions import check_frequency
from api.background import refresh_scraper

class ScraperAPI(View):
    def get(self, *args, **kwargs):
        scrappers = Scraper.objects.all()
        final_json = json.dumps(list(scrappers.values()), cls=DjangoJSONEncoder)
        return HttpResponse(
            final_json,
            content_type='application/json'
        )

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        try:
            check_frequency(data.get('frequency'))
            scraper = Scraper.objects.create(
                currency=data.get('currency'),
                frequency=data.get('frequency')
            )
            dict_obj = model_to_dict(scraper)
            # final_json = json.dumps(dict_obj, cls=DjangoJSONEncoder)
            return JsonResponse(
                dict_obj,
                status=200
            )
        except IntegrityError:
            return JsonResponse({'error': 'currency invalid'}, status=400)
        except FrequencyException:
            return JsonResponse({'error': 'frequency invalid'}, status=400)

    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        try:
            check_frequency(data.get('frequency'))
            scraper = Scraper.objects.get(
                pk=data.get('id')
            )
            scraper.frequency = data.get('frequency')
            scraper.save()
            if scraper.frequency == data.get('frequency'):
                return JsonResponse({'msg': 'Scraper updated'}, status=200)
            return JsonResponse({'error': 'error_msg'}, status=400)
        except Scraper.DoesNotExist:
            return JsonResponse({'error': 'not valid id'}, status=400)
        except IntegrityError:
            return JsonResponse({'error': 'not valid frequency'}, status=400)
        except FrequencyException:
            return JsonResponse({'error': 'frequency invalid'}, status=400)
        
    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        try:
            scraper = Scraper.objects.get(
                pk=data.get('id')
            )
            scraper.delete()
            return JsonResponse({'msg': 'Scraper deleted'}, status=200)
        except Scraper.DoesNotExist:
            return JsonResponse({'error': 'not valid id'}, status=400)
