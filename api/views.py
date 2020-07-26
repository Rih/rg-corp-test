# -*- encoding: utf-8 -*-
from django.views.generic import View
from api.models import Scraper
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse
import json
from django.db.utils import IntegrityError
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from api.exceptions import FrequencyException
from api.exceptions import check_frequency


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
            final_json = json.dumps(dict_obj, cls=DjangoJSONEncoder)
            return HttpResponse(
                final_json,
                content_type='application/json'
            )
        except IntegrityError:
            return HttpResponse(
                json.dumps({
                    'error': 'currency invalid',
                }),
                content_type='application/json',
                status=400
            )
        except FrequencyException:
            return HttpResponse(
                json.dumps({
                    'error': 'frequency invalid',
                }),
                content_type='application/json',
                status=400
            )

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
                return HttpResponse(
                    json.dumps({'msg': 'Scraper updated'}),
                    content_type='application/json',
                )
            return HttpResponse(
                json.dumps({'error': 'error_msg'}),
                content_type='application/json',
                status=400
            )
        except Scraper.DoesNotExist:
            return HttpResponse(
                json.dumps({'error': 'not valid id'}),
                content_type='application/json',
                status=400
            )
        except IntegrityError:
            return HttpResponse(
                json.dumps({'error': 'not valid frequency'}),
                content_type='application/json',
                status=400
            )
        except FrequencyException:
            return HttpResponse(
                json.dumps({
                    'error': 'frequency invalid',
                }),
                content_type='application/json',
                status=400
            )
        
    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        try:
            scraper = Scraper.objects.get(
                pk=data.get('id')
            )
            scraper.delete()
            return HttpResponse(
                json.dumps({'msg': 'Scraper deleted'}),
                content_type='application/json',
            )
        except Scraper.DoesNotExist:
            return HttpResponse(
                json.dumps({'error': 'not valid id'}),
                content_type='application/json',
                status=400
            )