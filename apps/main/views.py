from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse

import ast
import requests

from .utils import format_response_weather

from .models import Cookie
# Create your views here.


class IndexView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        request.session.save()

        try:
            search_history = [
                {
                    'name': search.city,
                    'long': search.long,
                    'lat': search.lat,
                }
                for search in Cookie.objects.get(
                    sessionid=request.COOKIES['sessionid']
                ).search_history.all().order_by('city', '-created_at').distinct('city')[:3]
            ]
        except (Cookie.DoesNotExist, KeyError):
            search_history = None

        return render(request, 'main/index.html', {
            'search_history': search_history
        })

    def post(self, request: HttpRequest) -> HttpResponse:
        city = ast.literal_eval(request.POST.get('city'))
        weather = requests.get(
            f'https://api.open-meteo.com/v1/forecast?latitude={city['lat']}&longitude={city['long']}&'
            'current=temperature_2m&daily=temperature_2m_max,temperature_2m_min'
        ).json()
        weather = format_response_weather(weather)
        cookie, _ = Cookie.objects.get_or_create(
            sessionid=request.COOKIES['sessionid'],
        )
        cookie.search_history.create(
            city=city['name'],
            lat=city['lat'],
            long=city['long'],
        )
        return render(request, 'main/index.html', {
            'city': city,
            'weather': weather
        })


def suggest(request):
    city = request.POST.get('city')
    suggestions = [
        {
            'name': suggestion['name'],
            'long': suggestion['longitude'],
            'lat': suggestion['latitude'],
        } for suggestion in requests.get(
            f'https://geocoding-api.open-meteo.com/v1/search?name={
                city}&count=10&language=ru&format=json'
        ).json().get('results') or []
    ]
    return render(request, 'main/includes/suggestions.html', {
        'suggestions': suggestions,
    })
